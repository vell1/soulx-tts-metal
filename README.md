# SoulX Podcast TTS (Metal/CUDA Auto)

🎙️ 基于 **SoulX-Podcast-1.7B-dialect** 的本地高质量语音合成服务

支持 Apple Silicon (Metal) 和 NVIDIA CUDA 自动加速

## ✨ 特性

- 🌐 **Web 界面**: 用户友好的浏览器界面，无需命令行
- 🎯 **REST API**: 可供程序调用的 HTTP 接口
- 🎙️ **多人播客**: 支持多角色对话，自动生成播客节目 ⭐ **新功能**
- 🎭 **多说话人**: 支持多个预设音色
- 🗣️ **多方言**: 支持普通话、四川话、河南话、粤语
- 🎨 **副语言控制**: 支持笑声、叹气、呼吸等情感表达
- 🚀 **零样本克隆**: 使用 3-10 秒参考音频即可克隆声音
- 🍎 **Apple Silicon 优化**: 原生支持 M1/M2/M3 芯片 (MPS)
- 💻 **跨平台**: 自动检测并使用最佳加速方案 (MPS/CUDA/CPU)

## 📋 系统要求

### 硬件要求
- **内存**: 至少 16GB RAM
- **存储**: 至少 10GB 可用空间（用于模型）
- **GPU**:
  - macOS: M1/M2/M3 芯片（自动使用 Metal Performance Shaders）
  - Linux/Windows: NVIDIA GPU with CUDA support（可选）

### 软件要求
- Python 3.11+
- pip
- git
- huggingface-cli（用于下载模型）

## 🚀 快速开始

### 1. 克隆或解压项目

```bash
cd /Users/zhaojianyun/Downloads/soulx-tts-metal
```

**注意**: SoulX-Podcast 模块已集成到项目中（`./soulxpodcast/`），无需额外安装。

### 2. 运行安装脚本

```bash
bash setup.sh
```

安装脚本会自动完成：
- ✅ 安装所有依赖包（自动适配 macOS/Linux）
- ✅ 验证 SoulX-Podcast 模块
- ✅ 下载预训练模型（约 4GB）
- ✅ 检查参考音频文件

### 3. 启动服务

```bash
bash start.sh
```

或者直接运行：

```bash
python app.py
```

### 4. 访问界面

打开浏览器访问: **http://localhost:8000**

## 📦 手动安装（如果自动安装失败）

### 步骤 1: 安装依赖

```bash
pip install -r requirements.txt
```

**注意**: SoulX-Podcast 模块已集成，无需单独安装。

### 步骤 2: 下载模型

```bash
# 安装 Hugging Face CLI
pip install -U huggingface_hub

# 下载方言模型
huggingface-cli download --resume-download Soul-AILab/SoulX-Podcast-1.7B-dialect \
  --local-dir pretrained_models/SoulX-Podcast-1.7B-dialect
```

### 步骤 3: 准备参考音频

查看 `prompt_audios/README.md` 了解如何准备参考音频文件。

项目已包含两个示例参考音频：
- `prompt_audios/female_1.wav` - 女声
- `prompt_audios/male_1.wav` - 男声

## 💻 使用方法

### Web 界面

1. 访问 http://localhost:8000
2. 选择使用模式：
   - **🎤 单人语音**: 单个说话人的文本转语音
   - **🎙️ 多人播客**: 多角色对话播客生成 ⭐ **新功能**

#### 单人语音模式

1. 在文本框中输入要转换的文本
2. 选择说话人（女声1、男声1 等）
3. 选择方言（普通话、四川话、河南话、粤语）
4. 点击"生成语音"按钮
5. 播放或下载生成的音频

#### 多人播客模式 ⭐ **新功能**

1. 编写播客脚本或点击"加载示例脚本"
2. 调整对话间隔（可选）
3. 点击"生成播客"按钮
4. 等待生成完成
5. 播放或下载生成的播客

**脚本格式示例**:
```
# 角色定义
@角色: 主持人, 女声1, 普通话
@角色: 嘉宾, 男声1, 普通话

# 对话内容
[主持人]: 大家好，欢迎收听今天的节目！
[嘉宾]: 你好，很高兴来到这里。
```

**📚 详细文档**: 查看 [多人播客使用指南](MULTIPERSON_PODCAST.md)

**🤖 AI 辅助**: 使用 [AI 提示词](prompts/README.md) 让 ChatGPT/Claude 帮你生成脚本 ⭐ 新增

#### 副语言控制标签

在文本中插入以下标签可以增强表现力：

- `<|laughter|>` - 笑声
- `<|sigh|>` - 叹气
- `<|breathing|>` - 呼吸声
- `<|coughing|>` - 咳嗽

**示例**：
```
最近活得特别赛博朋克哈！<|sigh|> 以前觉得 AI 是科幻片里的，<|laughter|> 现在连我妈都用 AI 写广场舞文案了。
```

### REST API

#### 单人语音生成

```bash
curl -X POST http://localhost:8000/api/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好，欢迎来到 SoulX 播客！",
    "speaker": "女声1",
    "dialect": "普通话"
  }' \
  --output output.wav
```

#### 多人播客生成 ⭐ **新功能**

```bash
curl -X POST http://localhost:8000/api/podcast \
  -H "Content-Type: application/json" \
  -d '{
    "script": "# 角色定义\n@角色: 主持人, 女声1, 普通话\n@角色: 嘉宾, 男声1, 普通话\n\n[主持人]: 大家好！\n[嘉宾]: 你好！",
    "silence_duration": 0.5
  }' \
  --output podcast.wav
```

#### 获取示例脚本

```bash
curl http://localhost:8000/api/podcast/example?format=simple
```

#### Python 调用示例

```python
import requests

url = "http://localhost:8000/api/tts"
data = {
    "text": "这是一段测试语音",
    "speaker": "男声1",
    "dialect": "四川话"
}

response = requests.post(url, json=data)

with open("output.wav", "wb") as f:
    f.write(response.content)

print("音频已保存到 output.wav")
```

## 🎨 自定义说话人

### 添加新的说话人

1. 准备 3-10 秒的清晰音频文件（WAV 格式，22050 Hz 或 24000 Hz）
2. 将文件放入 `prompt_audios/` 目录，例如 `female_2.wav`
3. 在 `app.py` 中添加说话人配置：

```python
SPEAKERS = {
    # ... 现有说话人 ...
    "女声2": {
        "id": "female_2",
        "audio": os.path.join(PROMPT_AUDIO_DIR, "female_2.wav"),
        "text": "参考音频的对应文本内容"
    }
}
```

4. 重启服务

## 📁 项目结构

```
soulx-tts-metal/
├── app.py                          # 主应用程序
├── requirements.txt                # Python 依赖
├── setup.sh                        # 自动安装脚本
├── start.sh                        # 启动脚本
├── README.md                       # 本文档
├── Dockerfile                      # Docker 配置
├── ecosystem.config.js             # PM2 配置
├── .gitignore                      # Git 忽略规则
├── docs/                           # 📚 文档目录
│   ├── README.md                   # 文档索引
│   ├── MULTIPERSON_PODCAST.md      # 多人播客使用指南 ⭐
│   ├── AI_PROMPTS_SUMMARY.md       # AI 提示词系统总结 ⭐
│   ├── INSTALL.md                  # 安装指南
│   ├── PERFORMANCE_OPTIMIZATION.md # 性能优化指南
│   ├── 功能完成报告.md              # 功能完成报告
│   └── ... (其他文档)
├── tests/                          # 🧪 测试目录
│   ├── README.md                   # 测试说明
│   ├── test_api_complete.py        # API 完整测试
│   ├── test_web_interface.py       # Web 界面测试
│   ├── test_podcast.py             # 播客单元测试
│   ├── TEST_REPORT_COMPLETE.md     # 完整测试报告
│   └── ... (其他测试)
├── examples/                       # 📝 示例脚本目录 ⭐
│   ├── README.md                   # 示例说明
│   ├── podcast_example_simple.txt  # 基础对话示例
│   ├── podcast_example_debate.txt  # 辩论形式示例
│   ├── podcast_example_interview.txt # 访谈形式示例
│   └── podcast_example_dialect.txt # 多方言示例
├── prompts/                        # 🤖 AI 提示词模板 ⭐
│   ├── README.md                   # 提示词使用指南
│   ├── podcast_generation_prompt.md # 主提示词模板
│   └── scenarios/                  # 场景化提示词
├── prompt_audios/                  # 🎵 参考音频目录
│   ├── README.md
│   ├── female_1.wav                # 女声参考
│   ├── male_1.wav                  # 男声参考
│   ├── sichuan.wav                 # 四川话示例
│   └── yue.wav                     # 粤语示例
├── soulxpodcast/                   # 🎙️ 核心模块
│   ├── models/                     # 模型定义
│   ├── engine/                     # 推理引擎
│   └── utils/                      # 工具函数
│       └── podcast_utils.py        # 多人播客工具 ⭐
├── pretrained_models/              # 📦 模型文件（自动下载）
│   └── SoulX-Podcast-1.7B-dialect/
├── logs/                           # 📋 日志文件目录
├── temp/                           # 🗑️ 临时文件目录
└── test_outputs/                   # 🎵 测试音频输出
```

## 🐳 Docker 部署

### 构建镜像

```bash
docker build -t soulx-tts .
```

### 运行容器

```bash
docker run -d -p 8000:8000 \
  -v $(pwd)/pretrained_models:/app/pretrained_models \
  -v $(pwd)/prompt_audios:/app/prompt_audios \
  soulx-tts
```

## 🔧 PM2 部署

```bash
# 安装 PM2
npm install -g pm2

# 启动服务
pm2 start ecosystem.config.js

# 查看状态
pm2 status

# 查看日志
pm2 logs soulx-tts

# 停止服务
pm2 stop soulx-tts
```

## ⚡ 性能优化

### macOS (Apple Silicon)

- 自动使用 Metal Performance Shaders (MPS)
- 确保 PyTorch 版本 >= 2.0
- 内存占用约 8-12GB

### Linux (CUDA)

- 自动使用 CUDA 加速
- 推荐 NVIDIA GPU with >= 8GB VRAM
- 可选启用 FP16 以提高速度

### CPU 模式

- 如果没有 GPU，自动使用 CPU
- 推荐至少 16GB RAM
- 生成速度较慢，但功能完整

## 🔍 故障排除

### 问题 1: 模型加载失败

```
FileNotFoundError: 模型路径不存在
```

**解决方案**:
```bash
bash setup.sh
# 或手动下载模型
huggingface-cli download --resume-download Soul-AILab/SoulX-Podcast-1.7B-dialect \
  --local-dir pretrained_models/SoulX-Podcast-1.7B-dialect
```

### 问题 2: 找不到 soulxpodcast 模块

```
ModuleNotFoundError: No module named 'soulxpodcast'
```

**解决方案**:
```bash
cd /Users/zhaojianyun/Downloads/SoulX-Podcast-main
pip install -e .
```

### 问题 3: macOS 上 triton 安装失败

这是正常的！macOS 不需要 triton。requirements.txt 已经配置为在 macOS 上跳过 triton。

### 问题 4: 内存不足

**解决方案**:
- 关闭其他占用内存的应用
- 考虑使用更小的批次大小
- 如果使用 Mac，确保关闭了不必要的浏览器标签页

## 📚 文档和资源

### 本项目文档

- **[多人播客使用指南](docs/MULTIPERSON_PODCAST.md)** - 多人播客功能详细说明 ⭐
- **[AI 脚本生成提示词](prompts/README.md)** - 使用 AI 快速生成播客脚本 ⭐
- **[示例脚本说明](examples/README.md)** - 播客脚本示例和使用方法 ⭐
- **[安装指南](docs/INSTALL.md)** - 详细的安装步骤
- **[更新日志](docs/CHANGES.md)** - 版本更新记录
- **[测试报告](tests/TEST_REPORT_COMPLETE.md)** - 完整测试报告 ⭐
- **[文档索引](docs/README.md)** - 查看所有文档

### 官方资源

- **官方项目**: [SoulX-Podcast GitHub](https://github.com/Soul-AILab/SoulX-Podcast)
- **演示页面**: [SoulX-Podcast Demo](https://soul-ailab.github.io/soulx-podcast/)
- **技术论文**: [arXiv:2510.23541](https://arxiv.org/abs/2510.23541)
- **Hugging Face**:
  - [基础模型](https://huggingface.co/Soul-AILab/SoulX-Podcast-1.7B)
  - [方言模型](https://huggingface.co/Soul-AILab/SoulX-Podcast-1.7B-dialect)

### 快速链接

- 🎙️ [多人播客快速开始](docs/MULTIPERSON_PODCAST.md#快速开始)
- 🤖 [AI 生成播客脚本](prompts/README.md#快速开始) - 使用 ChatGPT/Claude 快速创建脚本 ⭐
- 📝 [脚本格式说明](docs/MULTIPERSON_PODCAST.md#脚本格式详解)
- 💡 [最佳实践](docs/MULTIPERSON_PODCAST.md#最佳实践)
- 🔧 [故障排除](docs/MULTIPERSON_PODCAST.md#故障排除)

## 📝 许可证

本项目使用 Apache 2.0 许可证。

SoulX-Podcast 模型使用 Apache 2.0 许可证。

## 🙏 致谢

- Soul AI Lab 团队开发的 SoulX-Podcast 模型
- Hugging Face 提供的模型托管服务
- 所有贡献者和用户

## 📧 联系方式

如有问题或建议，请：
- 提交 GitHub Issue
- 查看官方文档
- 联系 Soul AI Lab 团队

---

**Made with ❤️ for the AI community**
