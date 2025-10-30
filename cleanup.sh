#!/bin/bash

# 项目清理脚本
# 用于清理临时文件和日志

echo "🧹 开始清理项目临时文件..."
echo ""

# 清理临时测试文件
if [ -d "temp" ] && [ "$(ls -A temp)" ]; then
    echo "📁 清理 temp/ 目录..."
    rm -rf temp/*
    echo "✅ temp/ 已清理"
else
    echo "⏭️  temp/ 目录为空或不存在"
fi

# 清理旧日志文件
if [ -d "logs" ] && [ "$(ls -A logs)" ]; then
    echo "📋 清理 logs/ 目录..."
    rm -rf logs/*.log
    echo "✅ logs/ 已清理"
else
    echo "⏭️  logs/ 目录为空或不存在"
fi

# 清理测试输出（可选，需要确认）
if [ -d "test_outputs" ] && [ "$(ls -A test_outputs)" ]; then
    read -p "❓ 是否清理 test_outputs/ 测试音频文件？(y/N): " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        rm -rf test_outputs/*
        echo "✅ test_outputs/ 已清理"
    else
        echo "⏭️  跳过 test_outputs/ 清理"
    fi
fi

# 清理 Python 缓存
echo "🐍 清理 Python 缓存..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null
echo "✅ Python 缓存已清理"

# 清理 macOS 垃圾文件
if [ "$(uname)" = "Darwin" ]; then
    echo "🍎 清理 macOS 临时文件..."
    find . -name ".DS_Store" -delete 2>/dev/null
    echo "✅ .DS_Store 已清理"
fi

echo ""
echo "🎉 清理完成！"
echo ""
echo "📊 当前磁盘使用情况:"
du -sh . 2>/dev/null || echo "无法获取磁盘使用情况"

