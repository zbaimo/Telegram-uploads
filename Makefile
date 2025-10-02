# Makefile for Telegram File Upload Bot

.PHONY: help build run stop logs clean dev test

# 默认目标
help:
	@echo "Telegram文件上传机器人 - Docker管理命令"
	@echo ""
	@echo "可用命令:"
	@echo "  build     - 构建Docker镜像"
	@echo "  run       - 启动机器人（生产模式）"
	@echo "  dev       - 启动机器人（开发模式）"
	@echo "  stop      - 停止机器人"
	@echo "  logs      - 查看日志"
	@echo "  clean     - 清理容器和镜像"
	@echo "  test      - 测试机器人状态"
	@echo "  backup    - 备份配置文件"
	@echo "  restore   - 恢复配置文件"

# 构建镜像
build:
	@echo "构建Docker镜像..."
	docker-compose build

# 启动生产模式
run:
	@echo "启动机器人（生产模式）..."
	docker-compose up -d

# 启动开发模式
dev:
	@echo "启动机器人（开发模式）..."
	docker-compose -f docker-compose.dev.yml up -d

# 停止服务
stop:
	@echo "停止机器人..."
	docker-compose down

# 查看日志
logs:
	@echo "查看机器人日志..."
	docker-compose logs -f telegram-bot

# 清理
clean:
	@echo "清理容器和镜像..."
	docker-compose down
	docker rmi telegram-uploads_telegram-bot 2>/dev/null || true
	docker system prune -f

# 测试机器人状态
test:
	@echo "测试机器人状态..."
	docker-compose exec telegram-bot python test_bot_status.py

# 备份配置
backup:
	@echo "备份配置文件..."
	@mkdir -p backups
	@cp bot_config.json backups/bot_config_$(shell date +%Y%m%d_%H%M%S).json 2>/dev/null || true
	@cp detected_topics.json backups/detected_topics_$(shell date +%Y%m%d_%H%M%S).json 2>/dev/null || true
	@echo "备份完成"

# 恢复配置
restore:
	@echo "可用的备份文件:"
	@ls -la backups/ 2>/dev/null || echo "没有找到备份文件"
	@echo "请手动复制备份文件到当前目录"

# 安装依赖
install:
	@echo "安装Python依赖..."
	pip install -r requirements.txt

# 本地测试
local-test:
	@echo "本地测试机器人..."
	python test_bot_status.py

# 更新镜像
update:
	@echo "更新Docker镜像..."
	docker-compose pull
	docker-compose up -d

# 查看状态
status:
	@echo "机器人状态:"
	docker-compose ps
	@echo ""
	@echo "容器资源使用:"
	docker stats --no-stream telegram-uploads_telegram-bot 2>/dev/null || echo "容器未运行"
