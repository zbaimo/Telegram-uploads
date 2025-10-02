# ⚡ 快速配置GitHub Actions

## 🚀 一键配置步骤

### 1. 推送代码到GitHub

```bash
# 进入项目目录
cd C:\Users\ZBaimo\Desktop\Telegram-uploads

# 添加文件并提交
git add .
git commit -m "Add GitHub Actions workflow"

# 推送到GitHub
git push origin main
```

### 2. 启用GitHub Actions

1. 访问：`https://github.com/zbaimo/Telegram-uploads`
2. 点击 **"Actions"** 标签
3. 点击 **"I understand my workflows, go ahead and enable them"**

### 3. 配置权限

1. 进入 **Settings** → **Actions** → **General**
2. 选择 **"Read and write permissions"**
3. 勾选 **"Allow GitHub Actions to create and approve pull requests"**

### 4. 触发构建

```bash
# 推送代码触发构建
git push origin main
```

## 📦 构建结果

构建成功后，镜像将发布到：

- **镜像地址**: `ghcr.io/zbaimo/telegram-uploads:latest`
- **标签**: `latest`, `main`, `v1.0.0`

## 🔍 查看构建状态

1. 进入仓库的 **"Actions"** 标签
2. 查看 **"Build and Push Docker Image"** 工作流
3. 点击运行记录查看构建日志

## 🚨 常见问题

### 权限错误
- 检查仓库权限设置
- 确保有packages:write权限

### 构建失败
- 查看构建日志确定错误
- 检查Dockerfile语法

### 推送失败
- 检查GitHub Token权限
- 验证镜像名称

## 🎯 使用构建的镜像

```bash
# 拉取镜像
docker pull ghcr.io/zbaimo/telegram-uploads:latest

# 运行镜像
docker run -d \
  --name telegram-bot \
  --env-file .env \
  ghcr.io/zbaimo/telegram-uploads:latest
```

## 🎉 完成

配置完成后，每次推送代码都会自动构建和发布Docker镜像！

**您的机器人现在支持自动化部署！** 🚀
