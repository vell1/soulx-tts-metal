# 安装指南

## 前置条件检查

在开始安装之前，请确保：

### 1. Python 环境

```bash
python3 --version
# 应该显示 Python 3.11 或更高版本
```

如果没有 Python 3.11+，请先安装：

**macOS (使用 Homebrew)**:
```bash
brew install python@3.11
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### 2. Git

```bash
git --version
```

如果没有 Git：
```bash
# macOS
brew install git

# Linux
sudo apt install git
```

### 3. 硬盘空间

检查可用空间：
```bash
df -h .
```

至少需要 **10GB** 可用空间（用于模型文件）

### 4. 内存

确保至少有 **16GB** RAM

```bash
# macOS
sysctl hw.memsize

# Linux
free -h
```

## 安装步骤

### 方法 1: 自动安装（推荐）

```bash
cd /Users/zhaojianyun/Downloads/soulx-tts-metal
bash setup.sh
```

等待安装完成（可能需要 10-30 分钟，取决于网速）

### 方法 2: 手动安装

#### 步骤 1: 创建虚拟环境（可选但推荐）

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
# venv\Scripts\activate  # Windows
```

#### 步骤 2: 安装依赖包

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**可能遇到的问题**:

- **macOS 上 triton 安装失败**: 正常，macOS 不需要 triton
- **torch 安装慢**: 文件较大（约 800MB），请耐心等待
- **网络问题**: 可以使用国内镜像

  ```bash
  pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
  ```

**注意**: SoulX-Podcast 模块已集成到项目中（`./soulxpodcast/`），无需单独安装。

#### 步骤 3: 安装 Hugging Face CLI

```bash
pip install -U huggingface_hub
```

#### 步骤 4: 下载模型

```bash
cd /Users/zhaojianyun/Downloads/soulx-tts-metal

# 创建模型目录
mkdir -p pretrained_models

# 下载模型（约 4GB，需要时间）
huggingface-cli download --resume-download \
  Soul-AILab/SoulX-Podcast-1.7B-dialect \
  --local-dir pretrained_models/SoulX-Podcast-1.7B-dialect
```

**下载加速（如果在中国）**:

```bash
# 使用镜像站点
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download --resume-download \
  Soul-AILab/SoulX-Podcast-1.7B-dialect \
  --local-dir pretrained_models/SoulX-Podcast-1.7B-dialect
```

#### 步骤 5: 验证参考音频

```bash
ls -lh prompt_audios/
# 应该看到:
# female_1.wav
# male_1.wav
```

## 验证安装

### 1. 检查 Python 包

```bash
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import transformers; print('Transformers:', transformers.__version__)"
python -c "from soulxpodcast import __version__; print('SoulX-Podcast:', __version__)"
```

### 2. 检查模型文件

```bash
ls -lh pretrained_models/SoulX-Podcast-1.7B-dialect/
# 应该看到多个文件，包括:
# model.safetensors
# config.json
# soulxpodcast_config.json
# flow.pt
# hift.pt
```

### 3. 检查设备支持

```bash
python -c "
import torch
print('CUDA available:', torch.cuda.is_available())
print('MPS available:', torch.backends.mps.is_available())
if hasattr(torch, 'accelerator'):
    print('Accelerator:', torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else 'CPU')
"
```

**预期输出**:
- **macOS (Apple Silicon)**: `MPS available: True`
- **Linux (NVIDIA GPU)**: `CUDA available: True`
- **CPU only**: 两者都为 `False`

## 启动服务

```bash
bash start.sh
```

或

```bash
python app.py
```

访问: http://localhost:8000

## 常见问题

### Q1: `ModuleNotFoundError: No module named 'soulxpodcast'`

**A**: 请确认项目结构完整，`soulxpodcast/` 目录应该在项目根目录下：
```bash
ls -la soulxpodcast/
# 应该看到: __init__.py, config.py, engine/, models/, utils/
```

### Q2: `FileNotFoundError: 模型路径不存在`

**A**: 请下载模型：
```bash
bash setup.sh
# 或手动下载
```

### Q3: 下载模型太慢

**A**: 使用镜像站点：
```bash
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download --resume-download \
  Soul-AILab/SoulX-Podcast-1.7B-dialect \
  --local-dir pretrained_models/SoulX-Podcast-1.7B-dialect
```

### Q4: macOS 上无法使用 MPS

**A**: 确保：
- macOS >= 12.3
- PyTorch >= 2.0
- 使用 Apple Silicon (M1/M2/M3) 芯片

```bash
python -c "import torch; print(torch.backends.mps.is_available())"
```

### Q5: 内存不足

**A**: 
- 关闭其他占用内存的应用
- 如果是 Mac，重启可以释放内存
- 考虑增加物理内存或使用更小的模型

### Q6: pip install 超时

**A**: 使用国内镜像：
```bash
pip install -r requirements.txt \
  -i https://mirrors.aliyun.com/pypi/simple/ \
  --trusted-host=mirrors.aliyun.com
```

## 卸载

```bash
# 删除虚拟环境（如果使用了）
rm -rf venv

# 删除模型文件（约 4GB）
rm -rf pretrained_models

# 卸载 Python 包
pip uninstall -y soulxpodcast
```

## 需要帮助？

- 查看 [README.md](README.md) 了解使用方法
- 查看 [官方 GitHub](https://github.com/Soul-AILab/SoulX-Podcast)
- 提交 Issue 报告问题

