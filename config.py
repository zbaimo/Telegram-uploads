import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类"""
    
    # Telegram Bot Token (从环境变量或直接设置)
    BOT_TOKEN = os.getenv('BOT_TOKEN', '8488795192:AAG540MhbhZQNx6NR29vnaNdb_KDZ7uhqpk')
    
    # 目标群组ID (需要替换为实际的群组ID)
    TARGET_GROUP_ID = os.getenv('TARGET_GROUP_ID', '-1003116625254')  # ASMR群组ID
    
    # 话题ID (可选，如果群组开启话题模式)
    TOPIC_ID = os.getenv('TOPIC_ID', '3')  # 话题ID，如果为空则不使用话题模式
    
    # 允许的用户ID列表 (可选，如果为空则允许所有用户)
    ALLOWED_USERS = os.getenv('ALLOWED_USERS', '').split(',') if os.getenv('ALLOWED_USERS') else []
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'bot.log')
    
    # 文件大小限制 (MB)
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', '2048'))  # 2GB = 2048MB
    
    @classmethod
    def validate(cls):
        """验证配置"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN 未设置")
        
        if not cls.TARGET_GROUP_ID or cls.TARGET_GROUP_ID == '-1001234567890':
            print("警告: 请设置正确的 TARGET_GROUP_ID")
        
        return True
