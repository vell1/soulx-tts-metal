"""
SoulX-Podcast: Text-to-Speech System
====================================

高质量的播客式多说话人对话语音合成系统。

支持特性:
- 多说话人、多轮对话
- 零样本声音克隆
- 跨方言生成（普通话、四川话、河南话、粤语）
- 副语言控制（笑声、叹气等）

作者: Soul AI Lab
许可: Apache 2.0
"""

__version__ = "1.0.0"
__author__ = "Soul AI Lab"

# 导入主要组件
from .config import Config, SamplingParams, SoulXPodcastLLMConfig
from .models.soulxpodcast import SoulXPodcast
from .utils.infer_utils import initiate_model, process_single_input
from .utils.parser import podcast_format_parser

__all__ = [
    'Config',
    'SamplingParams', 
    'SoulXPodcastLLMConfig',
    'SoulXPodcast',
    'initiate_model',
    'process_single_input',
    'podcast_format_parser',
]

