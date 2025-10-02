# 使用Python 3.10官方镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
RUN pip install --no-cache-dir \
    python-telegram-bot==20.7 \
    python-dotenv==1.0.0 \
    loguru==0.7.2 \
    nest-asyncio==1.5.8

# 复制应用程序代码
COPY . .

# 创建日志目录
RUN mkdir -p /app/logs

# 设置文件权限
RUN chmod +x start_ultra_stable.py

# 暴露端口（如果需要）
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python test_bot_status.py || exit 1

# 启动命令
CMD ["python", "start_ultra_stable.py"]
