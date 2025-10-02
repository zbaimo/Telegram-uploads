#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超稳定版机器人启动脚本 - 专门处理网络问题
"""

import os
import sys
import time
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.error import NetworkError, TimedOut, Conflict, BadRequest
from config import Config
from file_processor import FileProcessor
from utils import setup_logging, is_user_allowed, format_file_info
from loguru import logger

# 设置环境变量
os.environ['BOT_TOKEN'] = '8488795192:AAG540MhbhZQNx6NR29vnaNdb_KDZ7uhqpk'
os.environ['TARGET_GROUP_ID'] = '-1003116625254'
os.environ['TOPIC_ID'] = '3'
os.environ['MAX_FILE_SIZE'] = '2048'

# 全局变量
config = Config()
file_processor = FileProcessor()
setup_logging()

# 网络重试配置
MAX_RETRIES = 5
RETRY_DELAY = 10  # 秒
CONNECTION_TIMEOUT = 30  # 秒

async def safe_send_message(message, text: str, max_retries: int = 3):
    """安全发送消息，带重试机制"""
    for attempt in range(max_retries):
        try:
            await message.reply_text(text)
            return True
        except (NetworkError, TimedOut) as e:
            logger.warning(f"发送消息失败 (第 {attempt + 1} 次): {str(e)}")
            if attempt < max_retries - 1:
                await asyncio.sleep(5)
            else:
                logger.error(f"发送消息最终失败: {str(e)}")
                return False
        except Exception as e:
            logger.error(f"发送消息时发生未知错误: {str(e)}")
            return False
    return False

async def start_command(update: Update, context) -> None:
    """处理 /start 命令"""
    user = update.effective_user
    
    if not is_user_allowed(user.id, config.ALLOWED_USERS):
        await safe_send_message(update.message, "您没有权限使用此机器人。")
        return
    
    welcome_text = f"""
欢迎使用文件上传机器人！

你好 {user.first_name}！

使用方法：
• 直接发送任何文件给我
• 我会自动提取文件信息
• 然后将文件转发到指定群组

可用命令：
• /start - 显示此欢迎信息
• /status - 查看机器人状态
• /topics - 查看群组话题信息
• /select ID - 选择话题ID（如：/select 5）

当前配置：
• 目标群组：ASMR
• 默认话题ID：{config.TOPIC_ID or '未设置'}
• 最大文件大小：{config.MAX_FILE_SIZE}MB
    """
    
    await safe_send_message(update.message, welcome_text)
    logger.info(f"用户 {user.id} 开始使用机器人")

async def status_command(update: Update, context) -> None:
    """处理 /status 命令"""
    user = update.effective_user
    
    if not is_user_allowed(user.id, config.ALLOWED_USERS):
        await safe_send_message(update.message, "您没有权限使用此机器人。")
        return
    
    status_text = f"""
机器人状态信息

运行状态：正常运行
机器人版本：v2.0 (超稳定版)
目标群组：{config.TARGET_GROUP_ID}
话题模式：话题ID: {config.TOPIC_ID}
最大文件大小：{config.MAX_FILE_SIZE}MB
允许用户：{'所有用户' if not config.ALLOWED_USERS else f'{len(config.ALLOWED_USERS)}个用户'}
网络状态：已优化重试机制
    """
    
    await safe_send_message(update.message, status_text)

async def topics_command(update: Update, context) -> None:
    """处理 /topics 命令"""
    user = update.effective_user
    
    if not is_user_allowed(user.id, config.ALLOWED_USERS):
        await safe_send_message(update.message, "您没有权限使用此机器人。")
        return
    
    try:
        topics_text = "群组话题信息\n\n"
        
        # 检查是否有检测到的话题
        if os.path.exists("detected_topics.json"):
            import json
            with open("detected_topics.json", "r", encoding="utf-8") as f:
                topics_data = json.load(f)
            
            if topics_data:
                topics_text += "检测到的话题：\n"
                for topic_id, topic_info in topics_data.items():
                    topic_name = topic_info.get("name", f"话题{topic_id}")
                    message_count = topic_info.get("count", 0)
                    topics_text += f"- {topic_name}：{topic_id} (消息数: {message_count})\n"
            else:
                topics_text += "暂无检测到的话题\n"
                topics_text += "\n注意：机器人需要先接收群组消息才能检测话题"
        else:
            topics_text += "暂无检测到的话题\n"
            topics_text += "\n注意：机器人需要先接收群组消息才能检测话题"
        
        # 显示当前配置的话题
        if config.TOPIC_ID:
            topics_text += f"\n当前默认话题ID：{config.TOPIC_ID}"
            topics_text += "\n（所有文件将转发到此话题）"
        
        topics_text += "\n\n如何检测话题："
        topics_text += "\n1. 在群组中发送消息到不同话题"
        topics_text += "\n2. 机器人会自动检测并记录话题信息"
        topics_text += "\n3. 再次使用 /topics 命令查看检测结果"
        topics_text += "\n4. 使用 /select ID 选择话题（如：/select 5）"
        
        await safe_send_message(update.message, topics_text)
        
    except Exception as e:
        logger.error(f"获取话题信息时发生错误: {str(e)}")
        await safe_send_message(update.message, "获取话题信息失败，请稍后重试。")

async def select_command(update: Update, context) -> None:
    """处理 /select 命令"""
    user = update.effective_user
    
    if not is_user_allowed(user.id, config.ALLOWED_USERS):
        await safe_send_message(update.message, "您没有权限使用此机器人。")
        return
    
    # 获取用户输入的话题ID
    if not context.args:
        await safe_send_message(update.message,
            "请指定话题ID！\n"
            "使用方法：/select 话题ID\n"
            "例如：/select 5\n\n"
            "使用 /topics 查看可用的话题ID"
        )
        return
    
    try:
        topic_id = context.args[0]
        
        # 验证话题ID是否为数字
        try:
            topic_id_int = int(topic_id)
        except ValueError:
            await safe_send_message(update.message,
                f"话题ID必须是数字！\n"
                f"您输入的：{topic_id}\n"
                f"请使用数字，例如：/select 5"
            )
            return
        
        # 更新环境变量和配置文件
        os.environ['TOPIC_ID'] = topic_id
        config.TOPIC_ID = topic_id
        
        # 保存到文件以便持久化
        try:
            import json
            config_data = {
                "TOPIC_ID": topic_id,
                "TARGET_GROUP_ID": config.TARGET_GROUP_ID,
                "MAX_FILE_SIZE": config.MAX_FILE_SIZE
            }
            with open("bot_config.json", "w", encoding="utf-8") as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"保存配置失败: {str(e)}")
        
        # 检查话题是否存在
        topic_exists = False
        topic_name = f"话题{topic_id}"
        
        if os.path.exists("detected_topics.json"):
            try:
                import json
                with open("detected_topics.json", "r", encoding="utf-8") as f:
                    topics_data = json.load(f)
                
                if topic_id in topics_data:
                    topic_exists = True
                    topic_name = topics_data[topic_id].get("name", f"话题{topic_id}")
            except:
                pass
        
        if topic_exists:
            await safe_send_message(update.message,
                f"[OK] 成功选择话题！\n\n"
                f"话题名称：{topic_name}\n"
                f"话题ID：{topic_id}\n\n"
                f"所有文件将转发到此话题。\n"
                f"使用 /topics 查看所有可用话题。"
            )
        else:
            await safe_send_message(update.message,
                f"[WARNING] 话题ID已设置，但未检测到此话题\n\n"
                f"话题ID：{topic_id}\n"
                f"话题名称：{topic_name}\n\n"
                f"注意：此话题可能不存在或机器人还未检测到。\n"
                f"文件仍会转发到此话题ID。\n"
                f"使用 /topics 查看已检测的话题。"
            )
        
        logger.info(f"用户 {user.id} 选择话题ID: {topic_id}")
        
    except Exception as e:
        logger.error(f"选择话题时发生错误: {str(e)}")
        await safe_send_message(update.message, "选择话题失败，请稍后重试。")

async def handle_file_upload(update: Update, context, file_type: str) -> None:
    """处理文件上传"""
    user = update.effective_user
    message = update.message
    
    if not is_user_allowed(user.id, config.ALLOWED_USERS):
        await safe_send_message(message, "您没有权限使用此机器人。")
        return
    
    processing_msg = None
    try:
        # 发送处理中消息
        processing_msg = await safe_send_message(message, f"正在处理{file_type}...")
        
        # 处理文件
        result = await file_processor.process_file(message, config)
        
        if result['success']:
            # 转发到目标群组
            await forward_to_group(result, user, file_type, context)
            
            # 更新处理完成消息
            if processing_msg:
                await safe_send_message(message,
                    f"{file_type}处理完成！\n"
                    f"标题：{result['title']}\n"
                    f"已转发到目标群组"
                )
            
            logger.info(f"成功处理{file_type}: {result['title']}")
        else:
            if processing_msg:
                await safe_send_message(message, f"处理{file_type}失败：{result['error']}")
            
    except Exception as e:
        logger.error(f"处理文件上传时发生错误: {str(e)}")
        await safe_send_message(message, "处理文件时发生错误，请稍后重试。")

async def forward_to_group(result: dict, user, file_type: str, context) -> None:
    """转发文件到目标群组"""
    caption = format_file_info(result, user, file_type)
    
    send_params = {
        'chat_id': config.TARGET_GROUP_ID,
        'caption': caption
    }
    
    # 如果配置了话题ID，添加到发送参数中
    if config.TOPIC_ID and config.TOPIC_ID.strip() and config.TOPIC_ID != '':
        try:
            topic_id = int(config.TOPIC_ID.strip())
            send_params['message_thread_id'] = topic_id
            logger.info(f"使用话题模式，话题ID: {topic_id}")
        except ValueError:
            logger.warning(f"话题ID格式错误: {config.TOPIC_ID}")
    
    # 根据文件类型发送到群组，带重试机制
    for attempt in range(MAX_RETRIES):
        try:
            if result['file_type'] == 'document':
                await context.bot.send_document(**send_params, document=result['file_id'])
            elif result['file_type'] == 'photo':
                await context.bot.send_photo(**send_params, photo=result['file_id'])
            elif result['file_type'] == 'video':
                await context.bot.send_video(**send_params, video=result['file_id'])
            elif result['file_type'] == 'audio':
                await context.bot.send_audio(**send_params, audio=result['file_id'])
            elif result['file_type'] == 'voice':
                await context.bot.send_voice(**send_params, voice=result['file_id'])
            
            logger.info(f"文件已转发到群组 {config.TARGET_GROUP_ID}")
            return
            
        except (NetworkError, TimedOut) as e:
            logger.warning(f"转发文件失败 (第 {attempt + 1} 次): {str(e)}")
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY)
            else:
                logger.error(f"转发文件最终失败: {str(e)}")
                raise

async def handle_document(update: Update, context) -> None:
    await handle_file_upload(update, context, "文档")

async def handle_photo(update: Update, context) -> None:
    await handle_file_upload(update, context, "图片")

async def handle_video(update: Update, context) -> None:
    await handle_file_upload(update, context, "视频")

async def handle_audio(update: Update, context) -> None:
    await handle_file_upload(update, context, "音频")

async def handle_voice(update: Update, context) -> None:
    await handle_file_upload(update, context, "语音")

async def handle_text(update: Update, context) -> None:
    """处理文本消息"""
    user = update.effective_user
    message = update.message
    
    if not is_user_allowed(user.id, config.ALLOWED_USERS):
        await safe_send_message(message, "您没有权限使用此机器人。")
        return
    
    # 检测话题信息
    try:
        if message.chat.id == int(config.TARGET_GROUP_ID) and message.message_thread_id:
            # 这是群组消息且有话题ID，记录话题信息
            topic_id = str(message.message_thread_id)
            
            # 尝试获取更好的话题名称
            topic_name = f"话题{topic_id}"
            if message.text and len(message.text.strip()) > 0:
                # 使用消息内容作为话题名称，但限制长度
                clean_text = message.text.strip()
                if len(clean_text) > 30:
                    topic_name = clean_text[:30] + "..."
                else:
                    topic_name = clean_text
            elif message.caption and len(message.caption.strip()) > 0:
                # 如果有图片说明，使用说明作为话题名称
                clean_caption = message.caption.strip()
                if len(clean_caption) > 30:
                    topic_name = clean_caption[:30] + "..."
                else:
                    topic_name = clean_caption
            
            # 读取现有话题数据
            topics_data = {}
            if os.path.exists("detected_topics.json"):
                import json
                try:
                    with open("detected_topics.json", "r", encoding="utf-8") as f:
                        topics_data = json.load(f)
                except:
                    topics_data = {}
            
            # 更新话题信息
            if topic_id not in topics_data:
                topics_data[topic_id] = {
                    "name": topic_name,
                    "count": 1,
                    "last_detected": message.date.isoformat()
                }
            else:
                topics_data[topic_id]["count"] += 1
                topics_data[topic_id]["last_detected"] = message.date.isoformat()
                # 更新话题名称（使用最新的消息内容）
                if message.text and len(message.text) > 0:
                    topics_data[topic_id]["name"] = topic_name
            
            # 保存话题数据
            import json
            with open("detected_topics.json", "w", encoding="utf-8") as f:
                json.dump(topics_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"检测到话题: {topic_name} (ID: {topic_id})")
    except Exception as e:
        logger.error(f"话题检测失败: {str(e)}")
    
    # 回复用户
    await safe_send_message(message,
        "请发送文件给我，我会帮您转发到指定群组。\n"
        "使用 /status 查看机器人状态，/topics 查看话题信息，/select ID 选择话题。"
    )

async def error_handler(update: Update, context) -> None:
    """错误处理器"""
    error = context.error
    logger.error(f"更新处理时发生错误: {error}")
    
    if isinstance(error, Conflict):
        logger.warning(f"机器人实例冲突: {error}")
        # 等待一段时间后重试
        await asyncio.sleep(10)
    elif isinstance(error, (NetworkError, TimedOut)):
        logger.warning(f"网络错误: {error}")
        # 等待一段时间后重试
        await asyncio.sleep(5)
    elif isinstance(error, BadRequest):
        logger.warning(f"请求错误: {error}")
    else:
        logger.error(f"未知错误: {error}")

def main():
    """主函数"""
    print("Telegram 文件上传机器人 (超稳定版)")
    print("=" * 50)
    print(f"群组: ASMR")
    print(f"群组ID: {config.TARGET_GROUP_ID}")
    print(f"话题ID: {config.TOPIC_ID}")
    print(f"话题模式: 已启用")
    print(f"最大文件大小: {config.MAX_FILE_SIZE}MB")
    print(f"网络重试: {MAX_RETRIES}次")
    print(f"连接超时: {CONNECTION_TIMEOUT}秒")
    print("=" * 50)
    print("正在启动机器人...")
    print("按 Ctrl+C 停止机器人")
    print("")
    
    try:
        # 创建应用程序
        app = Application.builder().token(config.BOT_TOKEN).build()
        
        # 设置处理器
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("status", status_command))
        app.add_handler(CommandHandler("topics", topics_command))
        app.add_handler(CommandHandler("select", select_command))
        app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        app.add_handler(MessageHandler(filters.VIDEO, handle_video))
        app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
        app.add_handler(MessageHandler(filters.VOICE, handle_voice))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        # 添加错误处理器
        app.add_error_handler(error_handler)
        
        logger.info("消息处理器设置完成")
        
        # 启动机器人
        logger.info("正在启动 Telegram 文件上传机器人...")
        app.run_polling(
            drop_pending_updates=True, 
            allowed_updates=Update.ALL_TYPES,
            timeout=CONNECTION_TIMEOUT
        )
        
    except KeyboardInterrupt:
        logger.info("机器人已停止")
    except Exception as e:
        logger.error(f"程序运行错误: {str(e)}")
        print(f"\n机器人启动失败: {str(e)}")
        print("请检查网络连接和机器人配置")

if __name__ == '__main__':
    main()
