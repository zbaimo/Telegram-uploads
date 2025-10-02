# 🔧 修复部署问题

## 问题分析
容器启动失败的原因是日志配置问题：
- `docker-compose.yml` 中映射了 `./bot.log:/app/bot.log`
- 但主机上没有 `bot.log` 文件，Docker 创建了目录
- 应用程序尝试写入日志文件时失败

## 解决方案

### 1. 停止当前容器
```bash
# 在服务器上执行
docker compose down
```

### 2. 更新文件
将修复后的文件复制到服务器：

**需要更新的文件：**
- `docker-compose.yml` (已修复日志映射)
- `utils.py` (已修复日志路径)

### 3. 重新部署
```bash
# 在服务器上执行
docker compose up -d --build
```

### 4. 检查状态
```bash
# 查看容器状态
docker compose ps

# 查看日志
docker compose logs -f
```

## 修复内容

### docker-compose.yml 修复
```yaml
# 移除了有问题的日志文件映射
volumes:
  - ./bot_config.json:/app/bot_config.json
  - ./detected_topics.json:/app/detected_topics.json
  - ./logs:/app/logs  # 只映射日志目录
```

### utils.py 修复
```python
# 日志文件路径改为 logs/bot.log
logger.add(
    "logs/bot.log",  # 改为相对路径到 logs 目录
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="10 MB",
    retention="7 days",
    compression="zip"
)
```

## 验证修复
修复后，容器应该能够正常启动，日志文件将保存在 `./logs/bot.log` 中。
