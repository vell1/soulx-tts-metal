import time
from datetime import datetime

from tqdm import tqdm
from itertools import chain
from copy import deepcopy

import numpy as np
import s3tokenizer
import torch
device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
print(f"Using {device} device")
from transformers import AutoTokenizer, AutoModelForCausalLM, DynamicCache
from soulxpodcast.config import Config, SamplingParams, AutoPretrainedConfig
from soulxpodcast.engine.llm_engine import (
    HFLLMEngine, VLLMEngine
)
from soulxpodcast.models.modules.flow import CausalMaskedDiffWithXvec
from soulxpodcast.models.modules.hifigan import HiFTGenerator

class SoulXPodcast(torch.nn.Module):
    def __init__(self, config: Config = None):
        super().__init__()
        self.config = Config() if config is None else config

        self.audio_tokenizer = s3tokenizer.load_model("speech_tokenizer_v2_25hz").to(device).eval()
        if self.config.llm_engine == "hf":
            self.llm = HFLLMEngine(**self.config.__dict__)
        elif self.config.llm_engine == "vllm":
            self.llm = VLLMEngine(**self.config.__dict__)
        else:
            raise NotImplementedError

        self.use_tqdm = True

        self.flow = CausalMaskedDiffWithXvec()
        if self.config.hf_config.fp16_flow:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
            tqdm.write(f"[{timestamp}] - [INFO] - Casting flow to fp16")
            self.flow.half()
        self.flow.load_state_dict(torch.load(f"{self.config.model}/flow.pt", map_location="cpu", weights_only=True), strict=True)
        self.flow.to(device).eval()

        self.hift = HiFTGenerator()
        hift_state_dict = {k.replace('generator.', ''): v for k, v in torch.load(f"{self.config.model}/hift.pt", map_location="cpu", weights_only=True).items()}
        self.hift.load_state_dict(hift_state_dict, strict=True)
        self.hift.to(device).eval()

    
    @torch.inference_mode()
    def forward_longform(
        self, prompt_mels_for_llm,
        prompt_mels_lens_for_llm: torch.Tensor,
        prompt_text_tokens_for_llm: list[list[int]],
        text_tokens_for_llm: list[list[int]],
        prompt_mels_for_flow_ori, 
        spk_emb_for_flow: torch.Tensor,
        sampling_params: SamplingParams | list[SamplingParams],
        spk_ids: list[list[int]],
        use_dialect_prompt: bool = False,
        dialect_prompt_text_tokens_for_llm: list[list[int]] = None,
        dialect_prefix: list[list[int]] = None,
        **kwargs,  # for compatibility
    ):
        import time
        stage_start = time.time()
        total_start = time.time()

        prompt_size, turn_size = len(prompt_mels_for_llm), len(text_tokens_for_llm)

        # Audio tokenization (CPU 密集型操作)
        print(f"[DETAIL] 🎵 开始音频 tokenization...")
        tokenization_start = time.time()
        prompt_speech_tokens_ori, prompt_speech_tokens_lens_ori = self.audio_tokenizer.quantize(
            prompt_mels_for_llm.to(device), prompt_mels_lens_for_llm.to(device)
        )
        tokenization_time = time.time() - tokenization_start
        print(f"[DETAIL] ✓ 音频 tokenization 完成: {tokenization_time:.3f}s [CPU]")

        # align speech token with speech feat as to reduce
        #    the noise ratio during the generation process.
        print(f"[DETAIL] 🔄 对齐 speech tokens...")
        align_start = time.time()
        prompt_speech_tokens = []
        prompt_mels_for_flow, prompt_mels_lens_for_flow = [], []

        for prompt_index in range(prompt_size):
            prompt_speech_token_len = prompt_speech_tokens_lens_ori[prompt_index].item()
            prompt_speech_token = prompt_speech_tokens_ori[prompt_index, :prompt_speech_token_len]
            prompt_mel = prompt_mels_for_flow_ori[prompt_index]
            prompt_mel_len = prompt_mel.shape[0]
            if prompt_speech_token_len * 2 > prompt_mel_len:
                prompt_speech_token = prompt_speech_token[:int(prompt_mel_len/2)]
                # 🔥 优化: 直接在目标设备上创建
                prompt_mel_len = torch.tensor([prompt_mel_len], device=device)
            else:
                prompt_mel = prompt_mel.detach().clone()[:prompt_speech_token_len * 2].to(device)
                # 🔥 优化: 直接在目标设备上创建
                prompt_mel_len = torch.tensor([prompt_speech_token_len * 2], device=device)
            prompt_speech_tokens.append(prompt_speech_token)
            prompt_mels_for_flow.append(prompt_mel)
            prompt_mels_lens_for_flow.append(prompt_mel_len)
        align_time = time.time() - align_start
        print(f"[DETAIL] ✓ Speech tokens 对齐完成: {align_time:.3f}s")

        # Prepare LLM inputs
        print(f"[DETAIL] 📝 准备 LLM 输入...")
        prepare_start = time.time()
        prompt_inputs = []
        history_inputs = []
        
        for i in range(prompt_size):
            speech_tokens_i = [token+self.config.hf_config.speech_token_offset for token in prompt_speech_tokens[i].tolist()]
            speech_tokens_i += [self.config.hf_config.eos_token_id]
            if use_dialect_prompt and len(dialect_prompt_text_tokens_for_llm[i])>0:
                dialect_prompt_input = prompt_text_tokens_for_llm[i] + speech_tokens_i + dialect_prompt_text_tokens_for_llm[i]
                if i>0:
                    dialect_prompt_input = dialect_prefix[0] + dialect_prompt_input
                prompt_input = self.llm.generate(dialect_prompt_input, sampling_params, past_key_values=None)['token_ids']
                prompt_inputs.append(dialect_prefix[i+1]+dialect_prompt_text_tokens_for_llm[i] + prompt_input)
                history_inputs.append(dialect_prefix[i+1]+dialect_prompt_text_tokens_for_llm[i] + prompt_input)
            else:
                prompt_inputs.append(prompt_text_tokens_for_llm[i] + speech_tokens_i )
                history_inputs.append(prompt_text_tokens_for_llm[i] + speech_tokens_i )
        prepare_time = time.time() - prepare_start
        print(f"[DETAIL] ✓ LLM 输入准备完成: {prepare_time:.3f}s")

        generated_wavs, results_dict = [], {}
        
        # LLM generation
        print(f"[DETAIL] 🤖 开始 LLM 生成...")
        llm_total_start = time.time()
        inputs = list(chain.from_iterable(prompt_inputs))
        cache_config = AutoPretrainedConfig().from_dataclass(self.llm.config.hf_config)
        past_key_values = DynamicCache(config=cache_config)
        valid_turn_size = prompt_size
        
        # 初始化计时变量（防止空循环导致未定义错误）
        flow_time_total = 0
        vocoder_time_total = 0
        
        for i in range(turn_size):

            # # set ratio: reach the reset cache ratio;
            if valid_turn_size > self.config.max_turn_size or len(inputs)>self.config.turn_tokens_threshold:
                assert self.config.max_turn_size >= self.config.prompt_context + self.config.history_context, "Invalid Long history size setting, "
                prompt_text_bound = max(self.config.prompt_context, len(history_inputs)-self.config.history_text_context-self.config.history_context)
                inputs = list(chain.from_iterable(
                    history_inputs[:self.config.prompt_context]+ \
                    history_inputs[prompt_text_bound:-self.config.history_context]+ \
                    prompt_inputs[-self.config.history_context:]
                ))
                valid_turn_size = self.config.prompt_context + len(history_inputs) - prompt_text_bound
                past_key_values = DynamicCache(config=cache_config)
            valid_turn_size += 1
            
            inputs.extend(text_tokens_for_llm[i])
            start_time = time.time()
            llm_outputs = self.llm.generate(inputs, sampling_params, past_key_values=past_key_values)

            inputs.extend(llm_outputs['token_ids'])
            prompt_inputs.append(text_tokens_for_llm[i]+llm_outputs['token_ids'])
            history_inputs.append(text_tokens_for_llm[i][:-1]) # remove the <|audio_start|>
            
            # Prepare Flow inputs
            turn_spk = spk_ids[i]
            generated_speech_tokens = [token - self.config.hf_config.speech_token_offset for token in  llm_outputs['token_ids'][:-1]]  # ignore last eos
            prompt_speech_token = prompt_speech_tokens[turn_spk].tolist()
            # 🔥 优化: 直接在目标设备上创建 tensor，避免 CPU→GPU 传输
            flow_input = torch.tensor([prompt_speech_token + generated_speech_tokens], device=device)
            flow_inputs_len = torch.tensor([len(prompt_speech_token) + len(generated_speech_tokens)], device=device)

            # Flow generation and HiFi-GAN generation            
            start_idx = spk_ids[i]
            prompt_mels = prompt_mels_for_flow[start_idx][None]
            prompt_mels_lens = prompt_mels_lens_for_flow[start_idx][None]
            spk_emb = spk_emb_for_flow[start_idx:start_idx+1]

            # Flow generation
            flow_start = time.time()
            # 使用动态设备类型和精度（支持 CUDA/MPS/CPU）
            use_autocast = device == "cuda" and self.config.hf_config.fp16_flow
            if use_autocast:
                # 只在 CUDA + fp16 时使用 autocast
                with torch.amp.autocast("cuda", dtype=torch.float16):
                    generated_mels, generated_mels_lens = self.flow(
                        flow_input, flow_inputs_len,  # 已在正确设备上
                        prompt_mels, prompt_mels_lens, spk_emb.to(device),
                        streaming=False, finalize=True
                    )
            else:
                # MPS/CPU 或 fp32：直接推理，不使用 autocast
                generated_mels, generated_mels_lens = self.flow(
                    flow_input, flow_inputs_len,  # 已在正确设备上
                    prompt_mels, prompt_mels_lens, spk_emb.to(device),
                    streaming=False, finalize=True
                )
            flow_time = time.time() - flow_start
            flow_time_total += flow_time

            # HiFi-GAN generation
            vocoder_start = time.time()
            mel = generated_mels[:, :, prompt_mels_lens[0].item():generated_mels_lens[0].item()]
            wav, _ = self.hift(speech_feat=mel)
            generated_wavs.append(wav)
            vocoder_time = time.time() - vocoder_start
            vocoder_time_total += vocoder_time
        
        # LLM generation 完成
        llm_total_time = time.time() - llm_total_start
        print(f"[DETAIL] ✓ LLM+Flow+Vocoder 完成: {llm_total_time:.3f}s [GPU]")
        if turn_size > 0:
            print(f"[DETAIL]   - 总共 {turn_size} 轮")
            print(f"[DETAIL]   - Flow 总计: {flow_time_total:.3f}s (平均 {flow_time_total/turn_size:.3f}s/轮)")
            print(f"[DETAIL]   - Vocoder 总计: {vocoder_time_total:.3f}s (平均 {vocoder_time_total/turn_size:.3f}s/轮)")

        # Save the generated wav;
        results_dict['generated_wavs'] = generated_wavs
        
        # 总计
        total_time = time.time() - total_start
        print(f"[DETAIL] ⏱️  forward_longform 总耗时: {total_time:.3f}s")
        print(f"[DETAIL]   └─ tokenization: {tokenization_time:.3f}s ({tokenization_time/total_time*100:.1f}%)")
        
        return results_dict