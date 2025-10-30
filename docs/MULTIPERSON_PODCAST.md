# 多人播客功能使用指南

本文档详细介绍如何使用 SoulX-TTS 的多人播客功能，创建包含多个角色的对话式音频内容。

## 📖 目录

- [功能概述](#功能概述)
- [快速开始](#快速开始)
- [脚本格式详解](#脚本格式详解)
- [使用方法](#使用方法)
- [高级功能](#高级功能)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)

## 功能概述

### 支持的场景

- 🎙️ **对话播客**: 两人或多人交流讨论
- 🗣️ **访谈节目**: 主持人采访嘉宾
- ⚖️ **辩论节目**: 多方观点碰撞
- 📚 **有声剧**: 多角色叙事内容
- 🌍 **多方言对话**: 不同方言角色互动

### 核心特性

- ✅ 支持 2-10 个角色同时参与
- ✅ 每个角色可独立设置声音和方言
- ✅ 支持副语言标签（笑声、叹气等）
- ✅ 自动添加对话间隔，提升自然度
- ✅ 支持跨方言对话（普通话、四川话、河南话、粤语）
- ✅ 简单易用的脚本格式

## 快速开始

### 5 分钟入门

#### 步骤 1: 启动服务

```bash
python app.py
```

#### 步骤 2: 访问 Web 界面

打开浏览器访问: http://localhost:8000

#### 步骤 3: 切换到多人播客标签页

在界面顶部点击"🎙️ 多人播客"标签

#### 步骤 4: 编写脚本

点击"📄 加载示例脚本"按钮，或手动输入以下内容：

```
# 角色定义
@角色: 主持人, 女声1, 普通话
@角色: 嘉宾, 男声1, 普通话

# 对话内容
[主持人]: 大家好，欢迎收听今天的节目！
[嘉宾]: 你好，很高兴来到这里。
[主持人]: 今天我们要聊聊人工智能的话题。
[嘉宾]: 好的，这是一个非常有趣的话题。
```

#### 步骤 5: 生成播客

点击"🎙️ 生成播客"按钮，等待生成完成

#### 步骤 6: 播放和下载

生成完成后，可以在线播放或下载 WAV 文件

## 脚本格式详解

### 基本结构

播客脚本由两部分组成：

1. **角色定义区**: 声明所有参与者
2. **对话内容区**: 编写对话内容

```
# 角色定义区
@角色: 角色名称, 声音ID, 方言

# 对话内容区
[角色名称]: 对话文本
```

### 角色定义

#### 语法

```
@角色: <角色名称>, <声音ID>, <方言>
```

#### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| 角色名称 | 自定义的角色标识 | 主持人、嘉宾、小明 |
| 声音ID | 预设的声音模板 | 女声1、男声1 |
| 方言 | 语言方言类型 | 普通话、四川话、河南话、粤语 |

#### 示例

```
@角色: 主持人, 女声1, 普通话
@角色: 嘉宾A, 男声1, 四川话
@角色: 嘉宾B, 女声1, 粤语
```

### 对话内容

#### 语法

```
[<角色名称>]: <对话文本>
```

#### 规则

- 角色名称必须用方括号 `[]` 包围
- 角色名称后紧跟冒号 `:`
- 对话文本可以包含标点符号和副语言标签
- 每行一个对话

#### 示例

```
[主持人]: 大家好，欢迎收听今天的节目！
[嘉宾]: 你好，很高兴来到这里。<|laughter|>
[主持人]: 今天的话题很有意思。<|sigh|>
```

### 副语言标签

在对话中可以插入副语言标签来增强表现力：

| 标签 | 效果 | 使用场景 |
|------|------|----------|
| `<|laughter|>` | 笑声 | 开心、幽默的时刻 |
| `<|sigh|>` | 叹气 | 感慨、无奈的情绪 |
| `<|breathing|>` | 呼吸声 | 思考、停顿 |
| `<|coughing|>` | 咳嗽 | 打断、清嗓子 |

#### 示例

```
[主持人]: 这个问题很有意思。<|laughter|> 让我来想想。<|breathing|>
[嘉宾]: 是啊。<|sigh|> 我当时也很困惑。
```

### 注释

使用 `#` 开头的行为注释，会被解析器忽略：

```
# 这是一个注释，不会被处理

# 第一幕：开场
[主持人]: 大家好！

# 第二幕：讨论环节
[嘉宾]: 我认为...
```

## 使用方法

### 方式 1: Web 界面

这是最简单的使用方式，适合快速测试和小规模制作。

#### 操作步骤

1. 启动服务: `python app.py`
2. 访问 http://localhost:8000
3. 切换到"🎙️ 多人播客"标签页
4. 编写或加载脚本
5. 调整对话间隔（可选，默认 0.5 秒）
6. 点击"🎙️ 生成播客"按钮
7. 等待生成完成
8. 播放或下载音频

#### 界面功能

- **📄 加载示例脚本**: 加载预设的示例脚本
- **🗑️ 清空**: 清空脚本编辑器
- **对话间隔滑块**: 调整对话之间的静音时长（0.1-2.0 秒）

### 方式 2: REST API

适合程序化调用和批量生成。

#### 基本调用

```bash
curl -X POST http://localhost:8000/api/podcast \
  -H "Content-Type: application/json" \
  -d '{
    "script": "# 角色定义\n@角色: 主持人, 女声1, 普通话\n@角色: 嘉宾, 男声1, 普通话\n\n[主持人]: 你好！\n[嘉宾]: 你好！",
    "silence_duration": 0.5
  }' \
  --output podcast.wav
```

#### 从文件读取脚本

```bash
# 读取脚本文件并调用 API
SCRIPT=$(cat examples/podcast_example_simple.txt)

curl -X POST http://localhost:8000/api/podcast \
  -H "Content-Type: application/json" \
  -d "{\"script\": \"$SCRIPT\", \"silence_duration\": 0.5}" \
  --output podcast.wav
```

#### Python 调用

```python
import requests

# 方式 1: 直接传入脚本文本
script = """
@角色: 主持人, 女声1, 普通话
@角色: 嘉宾, 男声1, 普通话

[主持人]: 大家好！
[嘉宾]: 你好！
"""

response = requests.post(
    "http://localhost:8000/api/podcast",
    json={
        "script": script,
        "silence_duration": 0.5
    }
)

with open("podcast.wav", "wb") as f:
    f.write(response.content)

# 方式 2: 从文件读取脚本
with open("examples/podcast_example_simple.txt", "r", encoding="utf-8") as f:
    script = f.read()

response = requests.post(
    "http://localhost:8000/api/podcast",
    json={"script": script, "silence_duration": 0.5}
)

with open("podcast.wav", "wb") as f:
    f.write(response.content)
```

#### JavaScript/Node.js 调用

```javascript
const fs = require('fs');
const axios = require('axios');

// 读取脚本文件
const script = fs.readFileSync('examples/podcast_example_simple.txt', 'utf-8');

// 调用 API
axios.post('http://localhost:8000/api/podcast', {
  script: script,
  silence_duration: 0.5
}, {
  responseType: 'arraybuffer'
})
.then(response => {
  // 保存音频文件
  fs.writeFileSync('podcast.wav', response.data);
  console.log('播客已生成: podcast.wav');
})
.catch(error => {
  console.error('生成失败:', error);
});
```

### 方式 3: Python 脚本

直接在 Python 代码中使用功能模块。

```python
from app import generate_multiperson_podcast
from soulxpodcast.utils.podcast_utils import auto_parse_script
import soundfile as sf

# 脚本文本
script_text = """
@角色: 主持人, 女声1, 普通话
@角色: 嘉宾, 男声1, 普通话

[主持人]: 大家好，欢迎收听今天的节目！
[嘉宾]: 你好，很高兴来到这里。
"""

# 解析脚本
script = auto_parse_script(script_text)

# 生成播客
audio_array = generate_multiperson_podcast(script, silence_duration=0.5)

# 保存音频
sf.write("podcast.wav", audio_array, 24000)
print("播客已生成: podcast.wav")
```

## 高级功能

### 多方言混合对话

在同一播客中使用多种方言，增加趣味性和地域特色。

```
@角色: 主持人, 女声1, 普通话
@角色: 成都朋友, 男声1, 四川话
@角色: 广东朋友, 女声1, 粤语

[主持人]: 今天我们请来了两位不同地区的朋友。
[成都朋友]: 哈喽大家好，我来自成都。
[广东朋友]: 大家好呀，我是广东人。
[主持人]: 你们能分享一下各自家乡的特色吗？
```

### 动态对话间隔

根据对话内容调整间隔，在关键转折处使用更长的停顿。

**实现方式**: 在脚本中手动添加空白角色的对话来创建额外停顿

```
@角色: 主持人, 女声1, 普通话
@角色: 嘉宾, 男声1, 普通话

[主持人]: 现在，我要宣布一个重要消息。
# （手动添加更长停顿的方法：调整 API 参数）
[嘉宾]: 什么消息？
```

### 批量生成

使用脚本批量生成多个播客。

```python
import os
from app import generate_multiperson_podcast
from soulxpodcast.utils.podcast_utils import auto_parse_script
import soundfile as sf

# 脚本文件列表
script_files = [
    "examples/podcast_example_simple.txt",
    "examples/podcast_example_debate.txt",
    "examples/podcast_example_interview.txt",
]

# 批量生成
for script_file in script_files:
    print(f"正在处理: {script_file}")
    
    # 读取脚本
    with open(script_file, 'r', encoding='utf-8') as f:
        script_text = f.read()
    
    # 解析脚本
    script = auto_parse_script(script_text)
    
    # 生成播客
    audio_array = generate_multiperson_podcast(script, silence_duration=0.5)
    
    # 保存音频
    output_file = os.path.basename(script_file).replace('.txt', '.wav')
    sf.write(output_file, audio_array, 24000)
    
    print(f"已生成: {output_file}\n")
```

### JSON 格式脚本

除了简单文本格式，还支持 JSON 格式的脚本。

```json
{
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
      "text": "大家好，欢迎收听今天的节目！"
    },
    {
      "speaker": "嘉宾",
      "text": "你好，很高兴来到这里。"
    }
  ]
}
```

使用 JSON 格式的优势：
- 更容易通过程序生成
- 结构化数据，便于解析和验证
- 支持复杂的元数据（虽然当前版本未使用）

## 最佳实践

### 1. 脚本编写建议

#### 对话长度
- ✅ **推荐**: 每句 20-100 字
- ❌ **避免**: 超过 200 字的长段落

```
# 好的示例
[主持人]: 今天我们要聊的话题是人工智能。
[嘉宾]: 好的，这是一个很有趣的话题。

# 不好的示例
[嘉宾]: 人工智能是一个非常广泛的话题，它涉及到机器学习、深度学习、自然语言处理、计算机视觉等多个领域，每个领域都有其独特的技术和应用场景...（过长）
```

#### 角色设计
- ✅ 男女声搭配，便于区分
- ✅ 角色性格与方言匹配
- ✅ 2-4 个角色最佳，不超过 6 个

```
# 好的角色配置
@角色: 主持人, 女声1, 普通话  # 温和、专业
@角色: 专家, 男声1, 普通话    # 权威、稳重
@角色: 听众, 女声1, 普通话    # 好奇、活泼
```

#### 自然对话
- ✅ 使用口语化表达
- ✅ 适当添加语气词
- ✅ 使用副语言标签增强自然感

```
# 自然的对话
[主持人]: 哎呀，这个问题问得好！<|laughter|>
[嘉宾]: 是吧。<|sigh|> 我当时也是这么想的。

# 生硬的对话
[主持人]: 您的问题提得很好。
[嘉宾]: 确实如此。我当时也有此想法。
```

### 2. 技术优化建议

#### 对话间隔设置
- **快节奏对话**: 0.3-0.5 秒
- **正常节奏**: 0.5-0.8 秒
- **深度访谈**: 0.8-1.2 秒

#### 性能优化
- 长播客（>10 分钟）拆分为多个片段
- 使用缓存的参考音频
- 批量生成时控制并发数

#### 质量提升
- 使用高质量的参考音频（清晰、无噪音）
- 检查脚本中的错别字
- 测试不同方言组合的效果

### 3. 制作流程建议

#### 标准流程

1. **策划阶段**
   - 确定主题和形式
   - 设计角色和声音
   - 编写大纲

2. **脚本编写**
   - 根据大纲编写对话
   - 添加副语言标签
   - 审核和修改

3. **测试生成**
   - 生成前几句测试效果
   - 调整对话间隔和语气
   - 验证角色区分度

4. **完整生成**
   - 生成完整播客
   - 质量检查
   - 必要时重新生成特定片段

5. **后期处理**（可选）
   - 添加背景音乐
   - 音量归一化
   - 添加开头和结尾

## 故障排除

### 常见错误

#### 1. "未定义的角色" 错误

**错误信息**: `ValueError: 未定义的角色: XXX`

**原因**: 对话中使用的角色名称未在角色定义中声明

**解决方案**:
```
# 错误
@角色: 主持人, 女声1, 普通话
[嘉宾]: 你好  # 错误：嘉宾未定义

# 正确
@角色: 主持人, 女声1, 普通话
@角色: 嘉宾, 男声1, 普通话
[嘉宾]: 你好
```

#### 2. "未知说话人" 错误

**错误信息**: `ValueError: 未知说话人: XXX`

**原因**: 使用的声音ID不存在

**解决方案**: 查看可用声音列表
- Web 界面：在单人语音标签页查看下拉列表
- 命令行：运行 `python -c "from app import SPEAKERS; print(SPEAKERS)"`

#### 3. "脚本中没有对话内容" 错误

**错误信息**: `ValueError: 脚本中没有对话内容`

**原因**: 脚本中只有角色定义，没有实际对话

**解决方案**: 添加至少一句对话
```
@角色: 主持人, 女声1, 普通话

[主持人]: 大家好！  # 添加对话
```

#### 4. 生成时间过长

**症状**: 生成过程超过 5 分钟仍未完成

**可能原因**:
- 对话数量过多（>20 句）
- 单句文本过长（>200 字）
- 系统资源不足

**解决方案**:
1. 拆分长播客为多个片段
2. 缩短单句对话长度
3. 关闭其他占用资源的程序
4. 检查系统日志了解瓶颈

#### 5. 音频质量问题

**症状**: 生成的音频有杂音或不自然

**可能原因**:
- 参考音频质量差
- 文本中有特殊字符
- 方言标记使用错误

**解决方案**:
1. 使用高质量的参考音频（清晰、无背景噪音）
2. 移除文本中的特殊符号和表情符号
3. 确认方言标记正确（检查拼写）

### 调试技巧

#### 1. 启用详细日志

查看控制台输出，了解生成进度和可能的错误：

```bash
python app.py
# 观察控制台输出的 [INFO], [PERF], [ERROR] 等信息
```

#### 2. 测试简化脚本

先测试最简单的两人对话，确认系统正常：

```
@角色: A, 女声1, 普通话
@角色: B, 男声1, 普通话

[A]: 你好
[B]: 你好
```

#### 3. 逐步增加复杂度

- 先测试 2 个角色，再增加到 3-4 个
- 先使用普通话，再尝试方言
- 先不使用副语言标签，确认基本功能正常

#### 4. 检查文件格式

确保脚本文件使用 UTF-8 编码：

```bash
file -I examples/podcast_example_simple.txt
# 应该显示: charset=utf-8
```

## 参考资源

### 示例脚本

查看 `examples/` 目录下的示例脚本：
- `podcast_example_simple.txt` - 基础对话
- `podcast_example_debate.txt` - 辩论形式
- `podcast_example_interview.txt` - 访谈形式
- `podcast_example_dialect.txt` - 方言混合

### 相关文档

- [主 README](README.md) - 项目总体介绍
- [示例脚本 README](examples/README.md) - 示例脚本详细说明
- [安装指南](INSTALL.md) - 安装和配置
- [API 文档](docs/API.md) - API 接口详细文档（如有）

### 官方资源

- [SoulX-Podcast 项目](https://github.com/Soul-AILab/SoulX-Podcast)
- [技术论文](https://arxiv.org/abs/2510.23541)
- [Hugging Face 模型](https://huggingface.co/Soul-AILab/SoulX-Podcast-1.7B-dialect)

## 贡献与反馈

欢迎提交问题和改进建议！

- **问题反馈**: 提交 GitHub Issue
- **功能建议**: 提交 Feature Request
- **贡献代码**: 提交 Pull Request
- **分享脚本**: 提交优秀的播客脚本示例

---

**最后更新**: 2025-10-30  
**版本**: 1.0.0

