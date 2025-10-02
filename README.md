# Telegram 文件上传机器人

一个功能强大的 Telegram 机器人，用于接收用户上传的文件并自动转发到指定群组。

## 功能特性

- 📁 **多文件类型支持**：支持文档、图片、视频、音频、语音等文件类型
- 🏷️ **智能标题提取**：自动提取文件名或使用用户提供的描述作为标题
- 🔄 **自动转发**：将文件连同标题信息转发到指定群组
- 🧵 **话题模式支持**：支持群组话题模式，可指定特定话题
- 👥 **用户权限控制**：支持限制允许使用的用户列表
- 📊 **文件大小限制**：可配置最大文件大小限制
- 📝 **详细日志记录**：完整的操作日志和错误追踪
- ⚙️ **灵活配置**：通过环境变量进行配置管理

## 安装部署

### 1. 环境要求

- Python 3.8+
- pip 包管理器

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置设置

#### 方法一：使用环境变量文件（推荐）

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件：
```env
# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_here
TARGET_GROUP_ID=your_target_group_id_here

# Topic Configuration (Optional)
# If your group uses topic mode, set the topic ID here
TOPIC_ID=your_topic_id_here

# Optional: 限制允许的用户 (用逗号分隔)
ALLOWED_USERS=user_id1,user_id2

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=bot.log

# File Configuration
MAX_FILE_SIZE=2048
```

#### 方法二：直接设置环境变量

```bash
export BOT_TOKEN="your_bot_token_here"
export TARGET_GROUP_ID="your_target_group_id_here"
```

### 4. 获取必要的ID

#### 获取机器人Token
1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot` 创建新机器人
3. 按照提示设置机器人名称和用户名
4. 获取机器人Token

#### 获取群组ID
1. 将机器人添加到目标群组
2. 给机器人管理员权限
3. 在群组中发送消息并包含机器人
4. 访问 `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
5. 查找群组的 `chat.id`（通常以 `-100` 开头）

#### 获取话题ID（如果群组开启话题模式）
1. 在群组中回复某个话题下的消息
2. 机器人会收到回复消息，其中包含 `message_thread_id`
3. 查看机器人日志或使用 `/topics` 命令获取帮助
4. 将话题ID设置到 `TOPIC_ID` 环境变量中

### 5. 运行机器人

#### 方法一：使用启动脚本（推荐）
```bash
python run.py
```

#### 方法二：直接运行
```bash
python bot.py
```

## 使用方法

### 用户操作

1. **开始使用**：发送 `/start` 开始使用机器人
2. **上传文件**：直接发送任何支持的文件类型
3. **添加描述**：在发送文件时添加文字描述，机器人会将其作为标题
4. **查看帮助**：发送 `/help` 查看帮助信息
5. **查看状态**：发送 `/status` 查看机器人状态
6. **话题配置**：发送 `/topics` 获取话题配置帮助

### 支持的文件类型

- **文档**：PDF, DOC, DOCX, TXT, RTF, ODT, PPT, PPTX, XLS, XLSX
- **图片**：JPG, JPEG, PNG, GIF, BMP, WEBP, TIFF
- **视频**：MP4, AVI, MOV, WMV, FLV, WEBM, MKV, 3GP
- **音频**：MP3, WAV, OGG, FLAC, AAC, M4A, WMA
- **语音**：OGG格式的语音消息

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `BOT_TOKEN` | Telegram机器人Token | - | ✅ |
| `TARGET_GROUP_ID` | 目标群组ID | - | ✅ |
| `TOPIC_ID` | 话题ID（群组话题模式） | 空 | ❌ |
| `ALLOWED_USERS` | 允许的用户ID列表（逗号分隔） | 空（允许所有用户） | ❌ |
| `LOG_LEVEL` | 日志级别 | INFO | ❌ |
| `LOG_FILE` | 日志文件名 | bot.log | ❌ |
| `MAX_FILE_SIZE` | 最大文件大小（MB） | 2048 | ❌ |

### 权限控制

- 如果 `ALLOWED_USERS` 为空，则允许所有用户使用
- 如果设置了 `ALLOWED_USERS`，则只有列表中的用户可以使用机器人
- 获取用户ID：在机器人中发送 `/status` 命令

## 工作流程

1. **用户上传文件** → 机器人接收
2. **提取文件信息** → 获取文件名、大小、类型等
3. **生成标题** → 使用用户描述或文件名作为标题
4. **转发到群组** → 将文件连同标题信息发送到目标群组
5. **记录日志** → 记录操作详情和错误信息

## 日志管理

- **控制台输出**：实时显示运行状态和错误信息
- **文件日志**：保存到 `bot.log` 文件
- **日志轮转**：自动轮转，保留7天
- **日志压缩**：自动压缩旧日志文件

## 故障排除

### 常见问题

1. **机器人无响应**
   - 检查Token是否正确
   - 确认网络连接正常
   - 查看日志文件中的错误信息

2. **无法转发到群组**
   - 确认机器人已添加到目标群组
   - 检查机器人是否有发送消息的权限
   - 验证群组ID是否正确

3. **用户权限被拒绝**
   - 检查 `ALLOWED_USERS` 配置
   - 确认用户ID是否正确

4. **文件大小超限**
   - 调整 `MAX_FILE_SIZE` 配置
   - 或使用较小的文件

### 调试模式

设置环境变量启用详细日志：
```bash
export LOG_LEVEL=DEBUG
python bot.py
```

## 开发说明

### 项目结构

```
Telegram-uploads/
├── bot.py              # 主机器人文件
├── config.py           # 配置管理
├── file_processor.py   # 文件处理模块
├── utils.py            # 工具函数
├── run.py              # 启动脚本
├── requirements.txt    # 依赖包列表
├── .env.example        # 环境变量模板
├── README.md           # 说明文档
└── bot.log             # 日志文件（运行时生成）
```

### 扩展功能

机器人采用模块化设计，便于扩展：

- **数据库存储**：可添加数据库模块存储文件记录
- **文件转码**：可集成转码功能处理不同格式
- **权限管理**：可扩展更复杂的权限控制
- **Web界面**：可添加Web管理界面
- **API接口**：可提供REST API进行管理

## 许可证

本项目采用 MIT 许可证。

## 支持

如有问题或建议，请通过以下方式联系：

- 创建 Issue
- 发送邮件
- Telegram 联系

---

**注意**：请妥善保管机器人Token，不要将其提交到公共代码仓库中。
