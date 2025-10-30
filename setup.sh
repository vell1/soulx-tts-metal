#!/bin/bash
# SoulX-Podcast TTS 安装脚本

set -e  # 遇到错误立即退出

echo "========================================"
echo "🎙️  SoulX-Podcast TTS 安装脚本"
echo "========================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Python 版本
echo "📌 检查 Python 版本..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "   当前 Python 版本: $PYTHON_VERSION"

# 检查是否在 macOS 上
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${GREEN}✓ 检测到 macOS 系统，将使用 MPS (Metal) 加速${NC}"
    IS_MAC=true
else
    echo "✓ 检测到 Linux 系统，将使用 CUDA 加速"
    IS_MAC=false
fi

echo ""
echo "========================================"
echo "步骤 1: 安装依赖包"
echo "========================================"

# 安装项目依赖
echo "📦 安装 requirements.txt 中的依赖..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "步骤 2: 验证 SoulX-Podcast 模块"
echo "========================================"

if [ -d "soulxpodcast" ]; then
    echo -e "${GREEN}✓ SoulX-Podcast 模块已集成到项目${NC}"
    echo "   模块路径: ./soulxpodcast/"
else
    echo -e "${RED}❌ 错误: 找不到 soulxpodcast 模块${NC}"
    echo "   请确保项目结构完整"
    exit 1
fi

echo ""
echo "========================================"
echo "步骤 3: 下载模型文件"
echo "========================================"

MODEL_DIR="pretrained_models/SoulX-Podcast-1.7B-dialect"

if [ -d "$MODEL_DIR" ]; then
    echo -e "${YELLOW}⚠️  模型目录已存在，跳过下载${NC}"
else
    echo "📥 下载 SoulX-Podcast-1.7B-dialect 模型..."
    echo "   这可能需要几分钟时间..."
    huggingface-cli download --resume-download Soul-AILab/SoulX-Podcast-1.7B-dialect \
        --local-dir "$MODEL_DIR"
    echo -e "${GREEN}✓ 模型下载完成${NC}"
fi

echo ""
echo "========================================"
echo "步骤 4: 检查参考音频文件"
echo "========================================"

if [ -f "prompt_audios/female_1.wav" ] && [ -f "prompt_audios/male_1.wav" ]; then
    echo -e "${GREEN}✓ 参考音频文件已就绪${NC}"
else
    echo -e "${YELLOW}⚠️  参考音频文件缺失${NC}"
    echo "   请查看 prompt_audios/README.md 了解如何准备参考音频"
fi

echo ""
echo "========================================"
echo "✅ 安装完成！"
echo "========================================"
echo ""
echo "🚀 启动服务："
echo "   bash start.sh"
echo ""
echo "   或者："
echo "   python app.py"
echo ""
echo "🌐 访问地址："
echo "   http://localhost:8000"
echo ""
echo "========================================"

