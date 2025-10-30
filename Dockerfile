# SoulX-Podcast TTS Docker 镜像
FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制 SoulX-Podcast 模块（已集成）
COPY soulxpodcast/ ./soulxpodcast/

# 复制应用代码
COPY app.py .
COPY start.sh .
COPY prompt_audios/ ./prompt_audios/

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# 启动命令
CMD ["python", "app.py"]

# 使用说明:
# 
# 构建镜像:
#   docker build -t soulx-tts .
#
# 运行容器（需要挂载模型）:
#   docker run -d -p 8000:8000 \
#     -v $(pwd)/pretrained_models:/app/pretrained_models \
#     -v $(pwd)/prompt_audios:/app/prompt_audios \
#     --name soulx-tts \
#     soulx-tts
#
# 注意：模型文件较大（约 4GB），建议通过卷挂载方式使用预先下载的模型
