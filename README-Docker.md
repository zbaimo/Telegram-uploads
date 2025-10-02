# 🐳 Telegram文件上传机器人 - Docker部署

[![Docker Build](https://github.com/your-username/your-repo/actions/workflows/docker-build.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/docker-build.yml)
[![Docker Image](https://img.shields.io/badge/docker-latest-blue.svg)](https://github.com/your-username/your-repo/pkgs/container/your-repo)

## 📋 项目简介

这是一个基于Docker的Telegram文件上传机器人，支持话题模式、自动话题检测、文件转发等功能。

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. 配置环境

```bash
# 复制环境配置文件
cp env.example .env

# 编辑配置文件
nano .env
```

### 3. 启动机器人

```bash
# 使用Docker Compose启动
docker-compose up -d

# 或使用Makefile
make run
```

## 🔧 配置说明

### 环境变量

在 `.env` 文件中配置以下变量：

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

### 配置参数

| 参数 | 说明 | 默认值 | 必填 |
|------|------|--------|------|
| `BOT_TOKEN` | Telegram机器人令牌 | - | ✅ |
| `TARGET_GROUP_ID` | 目标群组ID | - | ✅ |
| `TOPIC_ID` | 话题ID | - | ❌ |
| `MAX_FILE_SIZE` | 最大文件大小(MB) | 2048 | ❌ |
| `ALLOWED_USERS` | 允许的用户ID列表 | - | ❌ |
| `LOG_LEVEL` | 日志级别 | INFO | ❌ |

## 📦 Docker镜像

### 从GitHub Container Registry拉取

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

### 构建镜像

```bash
# 构建镜像
docker build -t telegram-file-upload-bot .

# 构建多架构镜像
docker buildx build --platform linux/amd64,linux/arm64 -t telegram-file-upload-bot .
```

## 🛠️ 管理命令

### 使用Makefile

```bash
# 查看所有命令
make help

# 构建镜像
make build

# 启动机器人
make run

# 启动开发模式
make dev

# 停止机器人
make stop

# 查看日志
make logs

# 测试状态
make test

# 备份配置
make backup

# 清理
make clean
```

### 使用Docker Compose

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f telegram-bot

# 停止服务
docker-compose down

# 重启服务
docker-compose restart telegram-bot

# 查看状态
docker-compose ps
```

## 🔍 监控和日志

### 健康检查

容器包含健康检查功能，自动监控机器人状态。

### 日志管理

```bash
# 查看实时日志
docker-compose logs -f telegram-bot

# 查看最近100行日志
docker-compose logs --tail=100 telegram-bot

# 导出日志
docker-compose logs telegram-bot > bot.log
```

## 🔄 自动构建

### GitHub Actions

项目包含GitHub Actions工作流，自动构建和推送Docker镜像：

- 推送到 `main` 分支时自动构建
- 支持多架构镜像（amd64, arm64）
- 自动推送到GitHub Container Registry
- 使用 `latest` 标签

### 工作流文件

```yaml
# .github/workflows/docker-build.yml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
```

## 📊 功能特性

### 核心功能

- ✅ **文件上传**: 支持文档、图片、视频、音频等
- ✅ **话题模式**: 支持Telegram群组话题功能
- ✅ **自动检测**: 自动检测群组中的话题
- ✅ **话题选择**: 使用 `/select ID` 选择话题
- ✅ **话题查询**: 使用 `/topics` 查看话题信息
- ✅ **网络稳定**: 超稳定版解决所有网络问题

### 技术特性

- ✅ **Docker支持**: 完整的Docker化部署
- ✅ **多架构**: 支持amd64和arm64架构
- ✅ **自动构建**: GitHub Actions自动构建
- ✅ **健康检查**: 容器健康监控
- ✅ **日志管理**: 完整的日志记录
- ✅ **配置持久化**: 配置和状态持久化

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

### 调试模式

```bash
# 进入容器调试
docker exec -it telegram-bot bash

# 查看容器状态
docker exec telegram-bot python test_bot_status.py
```

## 📚 相关文档

- [Docker使用说明.md](./Docker使用说明.md) - 详细的Docker部署指南
- [最终使用总结.md](./最终使用总结.md) - 机器人功能说明
- [快速启动指南.md](./快速启动指南.md) - 快速启动指南

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目采用MIT许可证。

## 🎉 完成

现在您可以使用Docker部署Telegram文件上传机器人了！

- ✅ **Docker化**: 完整的Docker支持
- ✅ **自动构建**: GitHub Actions自动构建
- ✅ **多架构**: 支持amd64和arm64
- ✅ **配置管理**: 通过.env文件管理配置
- ✅ **数据持久化**: 配置和日志数据持久化
- ✅ **健康检查**: 自动监控容器状态
- ✅ **日志管理**: 完整的日志记录和管理

**您的机器人现在可以在任何支持Docker的环境中运行！** 🚀
