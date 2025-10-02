# 🐳 Docker Hub 配置指南

## 📋 概述

本指南将帮助您配置GitHub Actions，将Docker镜像自动推送到您的Docker Hub账户。

## 🔧 配置步骤

### 1. 创建Docker Hub账户

如果您还没有Docker Hub账户：

1. 访问 [Docker Hub](https://hub.docker.com/)
2. 点击 **"Sign Up"** 注册账户
3. 验证邮箱地址

### 2. 配置GitHub Secrets

需要在GitHub仓库中配置Docker Hub的认证信息：

#### 方法一：通过GitHub网页配置

1. 进入您的GitHub仓库：`https://github.com/zbaimo/Telegram-uploads`
2. 点击 **"Settings"** 标签
3. 在左侧菜单中点击 **"Secrets and variables"** → **"Actions"**
4. 点击 **"New repository secret"** 添加以下密钥：

#### 需要添加的Secrets：

| Secret名称 | 值 | 说明 |
|------------|-----|------|
| `DOCKER_USERNAME` | 您的Docker Hub用户名 | 例如：`zbaimo` |
| `DOCKER_PASSWORD` | 您的Docker Hub密码 | 或访问令牌 |

#### 方法二：通过GitHub CLI配置

```bash
# 安装GitHub CLI后
gh secret set DOCKER_USERNAME --body "您的Docker Hub用户名"
gh secret set DOCKER_PASSWORD --body "您的Docker Hub密码"
```

### 3. 推送代码触发构建

```bash
# 进入项目目录
cd C:\Users\ZBaimo\Desktop\Telegram-uploads

# 添加文件并提交
git add .
git commit -m "Configure Docker Hub deployment"

# 推送到GitHub
git push origin main
```

### 4. 验证构建

1. 进入仓库的 **"Actions"** 标签
2. 查看 **"Build and Push Docker Image"** 工作流
3. 等待构建完成

## 📦 构建结果

构建成功后，镜像将发布到：

- **镜像地址**: `docker.io/zbaimo/telegram-uploads:latest`
- **标签**: `latest`, `main`, `v1.0.0`

## 🔍 查看镜像

### 在Docker Hub查看

1. 访问 [Docker Hub](https://hub.docker.com/)
2. 登录您的账户
3. 搜索 `zbaimo/telegram-uploads`
4. 查看镜像详情和标签

### 在命令行查看

```bash
# 搜索镜像
docker search zbaimo/telegram-uploads

# 拉取镜像
docker pull zbaimo/telegram-uploads:latest

# 查看镜像信息
docker inspect zbaimo/telegram-uploads:latest
```

## 🚨 故障排除

### 常见问题

#### 1. 认证失败

**错误**: `authentication failed`

**解决方案**:
- 检查Docker Hub用户名和密码是否正确
- 确保GitHub Secrets配置正确
- 尝试使用访问令牌而不是密码

#### 2. 权限不足

**错误**: `permission denied`

**解决方案**:
- 确保Docker Hub账户有推送权限
- 检查镜像名称格式是否正确
- 验证仓库名称是否与Docker Hub用户名匹配

#### 3. 构建失败

**错误**: `build failed`

**解决方案**:
- 查看GitHub Actions构建日志
- 检查Dockerfile语法
- 确保所有依赖都正确安装

### 调试方法

#### 1. 查看构建日志

```bash
# 进入GitHub Actions页面
# 点击失败的构建记录
# 查看详细错误信息
```

#### 2. 本地测试

```bash
# 本地构建测试
docker build -t zbaimo/telegram-uploads:test .

# 本地登录测试
docker login
docker push zbaimo/telegram-uploads:test
```

#### 3. 检查配置

```bash
# 检查GitHub Secrets
# 确保DOCKER_USERNAME和DOCKER_PASSWORD正确设置
```

## 🎯 使用镜像

### 拉取镜像

```bash
# 拉取最新镜像
docker pull zbaimo/telegram-uploads:latest

# 拉取特定版本
docker pull zbaimo/telegram-uploads:v1.0.0
```

### 运行镜像

```bash
# 运行镜像
docker run -d \
  --name telegram-bot \
  --env-file .env \
  zbaimo/telegram-uploads:latest
```

### 使用Docker Compose

```bash
# 修改docker-compose.yml中的镜像名称
# 将镜像名改为: zbaimo/telegram-uploads:latest
docker-compose up -d
```

## 🔄 自动化流程

### 完整流程

1. **开发代码** → 本地测试
2. **提交代码** → `git commit`
3. **推送代码** → `git push origin main`
4. **自动构建** → GitHub Actions触发
5. **构建镜像** → 多架构支持
6. **推送镜像** → Docker Hub
7. **部署使用** → 拉取镜像部署

### 版本管理

```bash
# 创建版本标签
git tag v1.0.0
git push origin v1.0.0

# 镜像会自动标记为v1.0.0
```

## 🎉 完成

配置完成后，您的项目将拥有：

- ✅ **自动构建**: 推送代码自动构建镜像
- ✅ **Docker Hub推送**: 自动推送到您的Docker Hub账户
- ✅ **多架构支持**: 支持amd64和arm64
- ✅ **版本管理**: 自动标签管理
- ✅ **持续集成**: 完整的CI/CD流程

**您的Telegram文件上传机器人现在会自动推送到Docker Hub！** 🚀

## 📚 相关文档

- `快速配置Actions.md` - 快速配置指南
- `README-Docker.md` - Docker部署说明
- `README.md` - 项目说明

现在您可以按照上述步骤配置Docker Hub，实现自动推送镜像到您的Docker Hub账户！
