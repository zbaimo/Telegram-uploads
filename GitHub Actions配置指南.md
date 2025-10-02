# 🚀 GitHub Actions 配置指南

## 📋 概述

本指南将帮助您配置GitHub Actions工作流，实现自动构建和发布Docker镜像到GitHub Container Registry。

## 🔧 配置步骤

### 1. 推送代码到GitHub

首先需要将代码推送到GitHub仓库：

```bash
# 进入项目目录
cd C:\Users\ZBaimo\Desktop\Telegram-uploads

# 添加所有文件
git add .

# 提交更改
git commit -m "Add GitHub Actions workflow"

# 推送到GitHub
git push origin main
```

### 2. 启用GitHub Actions

1. 进入您的GitHub仓库：`https://github.com/zbaimo/Telegram-uploads`
2. 点击 **"Actions"** 标签
3. 点击 **"I understand my workflows, go ahead and enable them"**
4. 启用GitHub Actions

### 3. 配置Container Registry权限

1. 进入仓库设置：**Settings** → **Actions** → **General**
2. 在 **"Workflow permissions"** 部分：
   - 选择 **"Read and write permissions"**
   - 勾选 **"Allow GitHub Actions to create and approve pull requests"**

### 4. 触发工作流

推送代码后，GitHub Actions会自动触发：

```bash
# 推送到main分支会触发构建
git push origin main

# 或者创建标签也会触发构建
git tag v1.0.0
git push origin v1.0.0
```

## 📦 工作流配置说明

### 触发条件

工作流会在以下情况下触发：

- **推送到main分支**：自动构建并推送镜像
- **创建Pull Request**：构建测试镜像
- **创建标签**：构建发布镜像

### 镜像标签

工作流会自动生成以下标签：

- `latest` - 最新版本（main分支）
- `main` - main分支版本
- `v1.0.0` - 版本标签
- `1.0` - 主版本标签

### 多架构支持

工作流支持以下架构：

- `linux/amd64` - Intel/AMD 64位
- `linux/arm64` - ARM 64位

## 🔍 查看构建状态

### 1. 查看工作流运行

1. 进入仓库的 **"Actions"** 标签
2. 查看 **"Build and Push Docker Image"** 工作流
3. 点击具体的运行记录查看详情

### 2. 查看构建日志

1. 点击工作流运行记录
2. 点击 **"build-and-push"** 作业
3. 查看各个步骤的日志

### 3. 查看镜像

构建成功后，镜像会发布到：

- **GitHub Container Registry**: `ghcr.io/zbaimo/telegram-uploads`
- **标签**: `latest`, `main`, `v1.0.0` 等

## 🚨 故障排除

### 常见问题

#### 1. 权限错误

**错误**: `permission denied`

**解决方案**:
```bash
# 检查仓库权限设置
# Settings → Actions → General → Workflow permissions
# 选择 "Read and write permissions"
```

#### 2. 构建失败

**错误**: `Docker build failed`

**解决方案**:
```bash
# 检查Dockerfile语法
# 确保所有依赖都正确安装
# 查看构建日志确定具体错误
```

#### 3. 推送失败

**错误**: `push to registry failed`

**解决方案**:
```bash
# 检查GitHub Token权限
# 确保仓库有packages:write权限
# 检查镜像名称是否正确
```

### 调试方法

#### 1. 查看工作流日志

```bash
# 进入Actions页面
# 点击失败的运行记录
# 查看详细错误信息
```

#### 2. 本地测试

```bash
# 本地构建测试
docker build -t test-image .

# 本地运行测试
docker run -d test-image
```

#### 3. 检查配置文件

```bash
# 检查工作流文件语法
# 确保所有步骤都正确配置
# 验证环境变量设置
```

## 📚 高级配置

### 1. 环境变量

可以在工作流中添加环境变量：

```yaml
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
  CUSTOM_VAR: "value"
```

### 2. 条件构建

可以添加构建条件：

```yaml
- name: Build only on main
  if: github.ref == 'refs/heads/main'
  run: echo "Building on main branch"
```

### 3. 多环境部署

可以配置多个环境：

```yaml
jobs:
  build:
    strategy:
      matrix:
        environment: [staging, production]
    steps:
      - name: Deploy to ${{ matrix.environment }}
        run: echo "Deploying to ${{ matrix.environment }}"
```

## 🎯 使用构建的镜像

### 1. 拉取镜像

```bash
# 拉取最新镜像
docker pull ghcr.io/zbaimo/telegram-uploads:latest

# 拉取特定版本
docker pull ghcr.io/zbaimo/telegram-uploads:v1.0.0
```

### 2. 运行镜像

```bash
# 运行镜像
docker run -d \
  --name telegram-bot \
  --env-file .env \
  ghcr.io/zbaimo/telegram-uploads:latest
```

### 3. 使用Docker Compose

```bash
# 使用Docker Compose
docker-compose up -d
```

## 🔄 自动化流程

### 完整流程

1. **开发代码** → 本地测试
2. **提交代码** → `git commit`
3. **推送代码** → `git push origin main`
4. **自动构建** → GitHub Actions触发
5. **构建镜像** → 多架构支持
6. **发布镜像** → GitHub Container Registry
7. **部署使用** → 拉取镜像部署

### 版本管理

```bash
# 创建版本标签
git tag v1.0.0
git push origin v1.0.0

# 创建发布说明
# GitHub会自动创建Release
```

## 🎉 完成

配置完成后，您的项目将拥有：

- ✅ **自动构建**: 推送代码自动构建镜像
- ✅ **多架构支持**: 支持amd64和arm64
- ✅ **版本管理**: 自动标签管理
- ✅ **容器注册**: 发布到GitHub Container Registry
- ✅ **持续集成**: 完整的CI/CD流程

**您的Telegram文件上传机器人现在支持自动化构建和部署！** 🚀
