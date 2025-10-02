#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
"""

import os
import sys
from typing import List, Optional
from datetime import datetime
from loguru import logger
from telegram import User


def setup_logging():
    """设置日志配置"""
    # 移除默认处理器
    logger.remove()
    
    # 添加控制台输出
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # 添加文件输出
    logger.add(
        "bot.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        compression="zip"
    )


def is_user_allowed(user_id: int, allowed_users: List[str]) -> bool:
    """
    检查用户是否有权限使用机器人
    
    Args:
        user_id: 用户ID
        allowed_users: 允许的用户ID列表
        
    Returns:
        bool: 是否有权限
    """
    if not allowed_users:
        return True  # 如果没有限制，允许所有用户
    
    return str(user_id) in allowed_users


def format_file_info(result: dict, user: User, file_type: str) -> str:
    """
    格式化文件信息为消息文本
    
    Args:
        result: 文件处理结果
        user: 用户对象
        file_type: 文件类型
        
    Returns:
        str: 格式化的消息文本
    """
    try:
        # 只返回文件名
        file_name = result.get('file_name', '未知文件')
        
        # 如果文件名包含扩展名，去掉扩展名
        if '.' in file_name:
            name_without_ext = file_name.rsplit('.', 1)[0]
            return name_without_ext
        else:
            return file_name
        
    except Exception as e:
        logger.error(f"格式化文件信息失败: {str(e)}")
        return result.get('file_name', '未知文件')


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 文件大小（字节）
        
    Returns:
        str: 格式化的大小字符串
    """
    if size_bytes == 0:
        return "未知大小"
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} PB"


def get_user_display_name(user: User) -> str:
    """
    获取用户显示名称
    
    Args:
        user: Telegram 用户对象
        
    Returns:
        str: 用户显示名称
    """
    if user.first_name:
        name = user.first_name
        if user.last_name:
            name += f" {user.last_name}"
        return name
    elif user.username:
        return f"@{user.username}"
    else:
        return "未知用户"


def validate_group_id(group_id: str) -> bool:
    """
    验证群组ID格式
    
    Args:
        group_id: 群组ID字符串
        
    Returns:
        bool: 是否为有效的群组ID
    """
    try:
        # 群组ID应该是负数（超级群组以-100开头）
        if not group_id.startswith('-'):
            return False
        
        # 转换为整数验证格式
        int(group_id)
        return True
        
    except (ValueError, TypeError):
        return False


def create_env_file():
    """创建环境变量文件"""
    env_content = """# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_here
TARGET_GROUP_ID=your_target_group_id_here

# Optional: 限制允许的用户 (用逗号分隔)
ALLOWED_USERS=user_id1,user_id2

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=bot.log

# File Configuration
MAX_FILE_SIZE=50
"""
    
    env_file = ".env"
    if not os.path.exists(env_file):
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        logger.info(f"已创建环境变量文件: {env_file}")
        return True
    else:
        logger.info(f"环境变量文件已存在: {env_file}")
        return False


def check_dependencies():
    """检查依赖包是否安装"""
    required_packages = [
        'telegram',
        'python-dotenv',
        'loguru'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'telegram':
                import telegram
            elif package == 'python-dotenv':
                import dotenv
            elif package == 'loguru':
                import loguru
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"缺少依赖包: {', '.join(missing_packages)}")
        logger.info("请运行: pip install -r requirements.txt")
        return False
    
    return True


def get_bot_info(bot_token: str) -> Optional[dict]:
    """
    获取机器人信息
    
    Args:
        bot_token: 机器人Token
        
    Returns:
        dict: 机器人信息
    """
    try:
        import requests
        
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                return data.get('result', {})
        
        return None
        
    except Exception as e:
        logger.error(f"获取机器人信息失败: {str(e)}")
        return None


def format_duration(seconds: int) -> str:
    """
    格式化时长（秒转换为时分秒）
    
    Args:
        seconds: 秒数
        
    Returns:
        str: 格式化的时长字符串
    """
    if seconds < 60:
        return f"{seconds}秒"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        if remaining_seconds == 0:
            return f"{minutes}分钟"
        else:
            return f"{minutes}分{remaining_seconds}秒"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        
        if remaining_minutes == 0 and remaining_seconds == 0:
            return f"{hours}小时"
        elif remaining_seconds == 0:
            return f"{hours}小时{remaining_minutes}分钟"
        else:
            return f"{hours}小时{remaining_minutes}分{remaining_seconds}秒"


def extract_topic_id_from_message(message) -> Optional[int]:
    """
    从消息中提取话题ID
    
    Args:
        message: Telegram 消息对象
        
    Returns:
        int: 话题ID，如果没有则返回None
    """
    try:
        if hasattr(message, 'message_thread_id') and message.message_thread_id:
            return message.message_thread_id
        return None
    except Exception as e:
        logger.error(f"提取话题ID失败: {str(e)}")
        return None


def get_group_info_from_link(link: str) -> dict:
    """
    从群组链接获取基本信息
    
    Args:
        link: 群组邀请链接
        
    Returns:
        dict: 群组信息
    """
    try:
        # 解析群组链接
        if link.startswith('https://t.me/'):
            # 处理公开群组链接
            group_username = link.replace('https://t.me/', '')
            return {
                'type': 'public',
                'username': group_username,
                'link': link
            }
        elif link.startswith('https://t.me/+'):
            # 处理私人群组链接
            invite_hash = link.replace('https://t.me/+', '')
            return {
                'type': 'private',
                'invite_hash': invite_hash,
                'link': link
            }
        else:
            return {
                'type': 'unknown',
                'link': link
            }
    except Exception as e:
        logger.error(f"解析群组链接失败: {str(e)}")
        return {
            'type': 'error',
            'link': link,
            'error': str(e)
        }
