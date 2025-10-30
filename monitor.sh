#!/bin/bash
# 简单的日志监控脚本

LOG_FILE="/tmp/soulx_optimized.log"

if [ ! -f "$LOG_FILE" ]; then
    echo "❌ 错误: 日志文件不存在: $LOG_FILE"
    echo "请先启动 TTS 服务: bash start.sh"
    exit 1
fi

echo "================================"
echo "🎙️  SoulX-Podcast TTS 监控"
echo "================================"
echo ""
echo "📊 实时性能日志（按 Ctrl+C 停止）"
echo "--------------------------------"
echo ""

# 监控关键性能指标
tail -f "$LOG_FILE" | grep --line-buffered -E "\[PERF\]|\[INFO\].*生成完成|RTF|处理后的文本" | while read line; do
    # 添加时间戳
    timestamp=$(date '+%H:%M:%S')
    
    # 根据内容着色
    if echo "$line" | grep -q "\[PERF\].*CPU"; then
        echo -e "[$timestamp] \033[93m$line\033[0m"  # 黄色 - CPU
    elif echo "$line" | grep -q "\[PERF\].*GPU"; then
        echo -e "[$timestamp] \033[96m$line\033[0m"  # 青色 - GPU
    elif echo "$line" | grep -q "生成完成"; then
        echo -e "[$timestamp] \033[92m$line\033[0m"  # 绿色 - 完成
    else
        echo "[$timestamp] $line"
    fi
done

