#!/bin/bash
# SoulX-Podcast TTS 启动脚本

cd "$(dirname "$0")"

echo "========================================"
echo "🎙️  SoulX-Podcast TTS 服务启动中..."
echo "========================================"
echo ""

# 检查模型是否存在
if [ ! -d "pretrained_models/SoulX-Podcast-1.7B-dialect" ]; then
    echo "❌ 错误: 找不到模型文件"
    echo "   请先运行: bash setup.sh"
    exit 1
fi

# 检查参考音频
if [ ! -f "prompt_audios/female_1.wav" ]; then
    echo "⚠️  警告: 找不到参考音频文件"
    echo "   请查看 prompt_audios/README.md"
fi

echo "✓ 检查通过，启动服务..."
echo ""

# 启动服务
python app.py

# 备选方式：
# uvicorn app:app --host 0.0.0.0 --port 8000