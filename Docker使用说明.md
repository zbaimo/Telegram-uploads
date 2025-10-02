# 🐳 Docker 部署指南

## 📋 概述

本指南将帮助您使用Docker部署Telegram文件上传机器人，支持自动构建和发布到GitHub Container Registry。

## 🚀 快速开始

### 1. 准备环境文件

```bash
# 复制环境配置文件
cp env.example .env

# 编辑配置文件
nano .env
```

### 2. 配置环境变量

在 `.env` 文件中设置以下变量：

```env
# 必填配置
BOT_TOKEN=your_bot_token_here
TARGET_GROUP_ID=-1003116625254

# 可选配置
TOPIC_ID=3
MAX_FILE_SIZE=2048
ALLOWED_USERS=
LOG_LEVEL=INFO
```

### 3. 使用Docker Compose启动

```bash
# 构建并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f telegram-bot

# 停止服务
docker-compose down
```

## 🔧 手动Docker命令

### 构建镜像

```bash
# 构建镜像
docker build -t telegram-file-upload-bot .

# 构建多架构镜像
docker buildx build --platform linux/amd64,linux/arm64 -t telegram-file-upload-bot .
```

### 运行容器

```bash
# 运行容器
docker run -d \
  --name telegram-bot \
  --env-file .env \
  -v $(pwd)/bot_config.json:/app/bot_config.json \
  -v $(pwd)/detected_topics.json:/app/detected_topics.json \
  -v $(pwd)/logs:/app/logs \
  telegram-file-upload-bot

# 查看日志
docker logs -f telegram-bot

# 停止容器
docker stop telegram-bot
docker rm telegram-bot
```

## 📦 GitHub Container Registry

### 自动构建

当您推送代码到GitHub时，GitHub Actions会自动：

1. 构建Docker镜像
2. 推送到GitHub Container Registry
3. 使用 `latest` 标签

### 手动拉取镜像

```bash
# 拉取最新镜像
docker pull ghcr.io/your-username/your-repo:latest

# 运行镜像
docker run -d \
  --name telegram-bot \
  --env-file .env \
  -v $(pwd)/bot_config.json:/app/bot_config.json \
  -v $(pwd)/detected_topics.json:/app/detected_topics.json \
  -v $(pwd)/logs:/app/logs \
  ghcr.io/your-username/your-repo:latest
```

## 🔍 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `BOT_TOKEN` | Telegram机器人令牌 | - | ✅ |
| `TARGET_GROUP_ID` | 目标群组ID | - | ✅ |
| `TOPIC_ID` | 话题ID | - | ❌ |
| `MAX_FILE_SIZE` | 最大文件大小(MB) | 2048 | ❌ |
| `ALLOWED_USERS` | 允许的用户ID列表 | - | ❌ |
| `LOG_LEVEL` | 日志级别 | INFO | ❌ |
| `RETRY_ATTEMPTS` | 重试次数 | 5 | ❌ |
| `RETRY_DELAY` | 重试延迟(秒) | 10 | ❌ |
| `CONNECT_TIMEOUT` | 连接超时(秒) | 30 | ❌ |
| `READ_TIMEOUT` | 读取超时(秒) | 60 | ❌ |

### 卷挂载

| 容器路径 | 宿主机路径 | 说明 |
|----------|------------|------|
| `/app/bot_config.json` | `./bot_config.json` | 机器人配置 |
| `/app/detected_topics.json` | `./detected_topics.json` | 检测到的话题 |
| `/app/logs` | `./logs` | 日志目录 |
| `/app/bot.log` | `./bot.log` | 主日志文件 |

## 🛠️ 开发模式

### 本地开发

```bash
# 使用开发模式启动
docker-compose -f docker-compose.dev.yml up -d

# 实时查看日志
docker-compose logs -f telegram-bot
```

### 调试模式

```bash
# 进入容器调试
docker exec -it telegram-bot bash

# 查看容器状态
docker exec telegram-bot python test_bot_status.py
```

## 📊 监控和日志

### 健康检查

容器包含健康检查功能：

```bash
# 查看健康状态
docker ps
```

### 日志管理

```bash
# 查看实时日志
docker-compose logs -f telegram-bot

# 查看最近100行日志
docker-compose logs --tail=100 telegram-bot

# 导出日志
docker-compose logs telegram-bot > bot.log
```

## 🔄 更新和维护

### 更新镜像

```bash
# 拉取最新镜像
docker-compose pull

# 重启服务
docker-compose up -d
```

### 备份数据

```bash
# 备份配置文件
cp bot_config.json bot_config.json.backup
cp detected_topics.json detected_topics.json.backup

# 备份日志
cp bot.log bot.log.backup
```

## 🚨 故障排除

### 常见问题

1. **容器启动失败**
   ```bash
   # 检查日志
   docker-compose logs telegram-bot
   
   # 检查环境变量
   docker-compose config
   ```

2. **网络连接问题**
   ```bash
   # 检查网络
   docker network ls
   
   # 重启网络
   docker-compose down
   docker-compose up -d
   ```

3. **权限问题**
   ```bash
   # 检查文件权限
   ls -la bot_config.json detected_topics.json
   
   # 修复权限
   chmod 644 bot_config.json detected_topics.json
   ```

### 性能优化

```bash
# 限制资源使用
docker run -d \
  --name telegram-bot \
  --memory=512m \
  --cpus=1 \
  --env-file .env \
  telegram-file-upload-bot
```

## 📚 相关文档

- [Docker官方文档](https://docs.docker.com/)
- [Docker Compose文档](https://docs.docker.com/compose/)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

## 🎉 完成

现在您可以使用Docker部署Telegram文件上传机器人了！

- ✅ **自动构建**: GitHub Actions自动构建镜像
- ✅ **多架构支持**: 支持amd64和arm64架构
- ✅ **配置管理**: 通过.env文件管理配置
- ✅ **数据持久化**: 配置和日志数据持久化
- ✅ **健康检查**: 自动监控容器状态
- ✅ **日志管理**: 完整的日志记录和管理

**您的机器人现在可以在任何支持Docker的环境中运行！** 🚀
