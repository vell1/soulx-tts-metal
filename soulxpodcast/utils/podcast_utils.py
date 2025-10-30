"""
多人播客工具模块

支持多人对话脚本的解析、生成和管理
"""

import re
import json
from typing import List, Dict, Tuple, Optional


class PodcastScript:
    """
    播客脚本类
    
    支持以下格式：
    1. 简单格式：[角色名]: 对话内容
    2. JSON 格式：结构化的对话数据
    """
    
    def __init__(self):
        self.speakers = {}  # 角色配置
        self.dialogues = []  # 对话列表
    
    def add_speaker(self, name: str, voice: str, dialect: str = "普通话"):
        """
        添加角色
        
        Args:
            name: 角色名称（如 "主持人"、"嘉宾A"）
            voice: 声音ID（如 "女声1"、"男声1"）
            dialect: 方言（如 "普通话"、"四川话"）
        """
        self.speakers[name] = {
            "voice": voice,
            "dialect": dialect
        }
    
    def add_dialogue(self, speaker: str, text: str):
        """
        添加对话
        
        Args:
            speaker: 角色名称
            text: 对话内容
        """
        if speaker not in self.speakers:
            raise ValueError(f"未定义的角色: {speaker}。请先使用 add_speaker() 添加角色。")
        
        self.dialogues.append({
            "speaker": speaker,
            "text": text.strip()
        })
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "speakers": self.speakers,
            "dialogues": self.dialogues
        }
    
    def to_json(self) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


def parse_simple_script(script_text: str) -> PodcastScript:
    """
    解析简单脚本格式
    
    格式示例:
    ```
    # 角色定义
    @角色: 主持人, 女声1, 普通话
    @角色: 嘉宾, 男声1, 四川话
    
    # 对话内容
    [主持人]: 大家好，欢迎来到今天的节目！
    [嘉宾]: 你好，很高兴来到这里。<|laughter|>
    [主持人]: 今天我们要聊聊人工智能的话题。
    ```
    
    Args:
        script_text: 脚本文本
    
    Returns:
        PodcastScript 对象
    """
    script = PodcastScript()
    
    lines = script_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        
        # 跳过空行和注释
        if not line or line.startswith('#'):
            continue
        
        # 角色定义: @角色: 名称, 声音, 方言
        if line.startswith('@角色:') or line.startswith('@speaker:'):
            parts = line.split(':', 1)[1].split(',')
            if len(parts) < 2:
                raise ValueError(f"角色定义格式错误: {line}")
            
            name = parts[0].strip()
            voice = parts[1].strip()
            dialect = parts[2].strip() if len(parts) > 2 else "普通话"
            
            script.add_speaker(name, voice, dialect)
        
        # 对话内容: [角色名]: 对话文本
        elif line.startswith('['):
            match = re.match(r'\[(.*?)\]:\s*(.*)', line)
            if match:
                speaker = match.group(1).strip()
                text = match.group(2).strip()
                script.add_dialogue(speaker, text)
            else:
                raise ValueError(f"对话格式错误: {line}")
    
    return script


def parse_json_script(json_text: str) -> PodcastScript:
    """
    解析 JSON 格式脚本
    
    格式示例:
    ```json
    {
      "speakers": {
        "主持人": {"voice": "女声1", "dialect": "普通话"},
        "嘉宾": {"voice": "男声1", "dialect": "四川话"}
      },
      "dialogues": [
        {"speaker": "主持人", "text": "大家好！"},
        {"speaker": "嘉宾", "text": "你好！"}
      ]
    }
    ```
    
    Args:
        json_text: JSON 格式的脚本
    
    Returns:
        PodcastScript 对象
    """
    data = json.loads(json_text)
    script = PodcastScript()
    
    # 添加角色
    for name, config in data.get("speakers", {}).items():
        script.add_speaker(
            name,
            config["voice"],
            config.get("dialect", "普通话")
        )
    
    # 添加对话
    for dialogue in data.get("dialogues", []):
        script.add_dialogue(
            dialogue["speaker"],
            dialogue["text"]
        )
    
    return script


def auto_parse_script(script_text: str) -> PodcastScript:
    """
    自动检测并解析脚本格式
    
    Args:
        script_text: 脚本文本
    
    Returns:
        PodcastScript 对象
    """
    script_text = script_text.strip()
    
    # 尝试 JSON 格式
    if script_text.startswith('{'):
        try:
            return parse_json_script(script_text)
        except Exception:
            pass
    
    # 尝试简单格式
    return parse_simple_script(script_text)


def validate_script(script: PodcastScript, available_voices: List[str]) -> Tuple[bool, Optional[str]]:
    """
    验证脚本有效性
    
    Args:
        script: 脚本对象
        available_voices: 可用的声音列表
    
    Returns:
        (是否有效, 错误信息)
    """
    # 检查是否有角色
    if not script.speakers:
        return False, "脚本中没有定义任何角色"
    
    # 检查是否有对话
    if not script.dialogues:
        return False, "脚本中没有对话内容"
    
    # 检查声音是否可用
    for name, config in script.speakers.items():
        voice = config["voice"]
        if voice not in available_voices:
            return False, f"角色 '{name}' 使用的声音 '{voice}' 不可用"
    
    # 检查对话中的角色是否已定义
    for dialogue in script.dialogues:
        speaker = dialogue["speaker"]
        if speaker not in script.speakers:
            return False, f"对话中使用了未定义的角色: {speaker}"
    
    return True, None


def create_example_script() -> str:
    """
    创建示例脚本
    
    Returns:
        示例脚本文本
    """
    return """# 播客示例脚本
# 这是一段关于 AI 的对话

# 角色定义
@角色: 主持人, 女声1, 普通话
@角色: 嘉宾, 男声1, 普通话

# 对话内容
[主持人]: 大家好，欢迎收听今天的科技播客！<|laughter|> 今天我们请到了一位特别的嘉宾。
[嘉宾]: 大家好，很高兴来到这里。
[主持人]: 那么今天我们要聊的话题是人工智能。嘉宾能不能给我们介绍一下最近 AI 的发展？
[嘉宾]: 当然可以。最近 AI 领域确实非常火热，<|sigh|> 特别是大语言模型的出现，改变了很多行业。
[主持人]: 听起来很有趣！那您觉得普通人应该如何看待 AI 的发展呢？
[嘉宾]: 我认为 AI 是一个工具，关键在于如何使用它。我们应该拥抱技术，但也要保持理性思考。
[主持人]: 说得太好了！好的，今天的节目就到这里，感谢大家的收听！<|laughter|>
"""


def create_example_json_script() -> str:
    """
    创建 JSON 格式的示例脚本
    
    Returns:
        JSON 格式的示例脚本
    """
    example = {
        "speakers": {
            "主持人": {
                "voice": "女声1",
                "dialect": "普通话"
            },
            "嘉宾": {
                "voice": "男声1",
                "dialect": "普通话"
            }
        },
        "dialogues": [
            {
                "speaker": "主持人",
                "text": "大家好，欢迎收听今天的科技播客！<|laughter|> 今天我们请到了一位特别的嘉宾。"
            },
            {
                "speaker": "嘉宾",
                "text": "大家好，很高兴来到这里。"
            },
            {
                "speaker": "主持人",
                "text": "那么今天我们要聊的话题是人工智能。嘉宾能不能给我们介绍一下最近 AI 的发展？"
            },
            {
                "speaker": "嘉宾",
                "text": "当然可以。最近 AI 领域确实非常火热，<|sigh|> 特别是大语言模型的出现，改变了很多行业。"
            },
            {
                "speaker": "主持人",
                "text": "听起来很有趣！那您觉得普通人应该如何看待 AI 的发展呢？"
            },
            {
                "speaker": "嘉宾",
                "text": "我认为 AI 是一个工具，关键在于如何使用它。我们应该拥抱技术，但也要保持理性思考。"
            },
            {
                "speaker": "主持人",
                "text": "说得太好了！好的，今天的节目就到这里，感谢大家的收听！<|laughter|>"
            }
        ]
    }
    
    return json.dumps(example, ensure_ascii=False, indent=2)

