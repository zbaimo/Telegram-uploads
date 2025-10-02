#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件处理模块
负责提取文件信息、生成标题等功能
"""

import os
import mimetypes
from datetime import datetime
from typing import Dict, Optional, Any
from telegram import Message
from loguru import logger


class FileProcessor:
    """文件处理器"""
    
    def __init__(self):
        """初始化文件处理器"""
        self.supported_types = {
            'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.ppt', '.pptx', '.xls', '.xlsx'],
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'],
            'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.3gp'],
            'audio': ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a', '.wma']
        }
    
    async def process_file(self, message: Message, config) -> Dict[str, Any]:
        """
        处理文件消息
        
        Args:
            message: Telegram 消息对象
            config: 配置对象
            
        Returns:
            Dict: 处理结果
        """
        try:
            # 获取文件信息
            file_info = await self._get_file_info(message)
            
            if not file_info:
                return {'success': False, 'error': '无法获取文件信息'}
            
            # 检查文件大小
            if not self._check_file_size(file_info, config.MAX_FILE_SIZE):
                return {
                    'success': False, 
                    'error': f'文件过大，最大支持 {config.MAX_FILE_SIZE}MB'
                }
            
            # 生成文件标题
            title = self._generate_title(message, file_info)
            
            # 构建结果
            result = {
                'success': True,
                'file_id': file_info['file_id'],
                'file_type': file_info['file_type'],
                'title': title,
                'file_name': file_info['file_name'],
                'file_size': file_info['file_size'],
                'mime_type': file_info['mime_type'],
                'upload_time': datetime.now().isoformat(),
                'original_caption': message.caption or ''
            }
            
            logger.info(f"文件处理成功: {file_info['file_name']} ({file_info['file_type']})")
            return result
            
        except Exception as e:
            logger.error(f"文件处理失败: {str(e)}")
            return {'success': False, 'error': f'处理文件时发生错误: {str(e)}'}
    
    async def _get_file_info(self, message: Message) -> Optional[Dict[str, Any]]:
        """获取文件信息"""
        try:
            file_info = {}
            
            if message.document:
                # 文档文件
                document = message.document
                file_info = {
                    'file_id': document.file_id,
                    'file_name': document.file_name or '未知文档',
                    'file_size': document.file_size or 0,
                    'mime_type': document.mime_type or 'application/octet-stream',
                    'file_type': 'document'
                }
                
            elif message.photo:
                # 图片文件
                photo = message.photo[-1]  # 获取最高质量的图片
                file_info = {
                    'file_id': photo.file_id,
                    'file_name': f'图片_{photo.file_unique_id}.jpg',
                    'file_size': photo.file_size or 0,
                    'mime_type': 'image/jpeg',
                    'file_type': 'photo'
                }
                
            elif message.video:
                # 视频文件
                video = message.video
                file_info = {
                    'file_id': video.file_id,
                    'file_name': video.file_name or f'视频_{video.file_unique_id}.mp4',
                    'file_size': video.file_size or 0,
                    'mime_type': video.mime_type or 'video/mp4',
                    'file_type': 'video'
                }
                
            elif message.audio:
                # 音频文件
                audio = message.audio
                file_info = {
                    'file_id': audio.file_id,
                    'file_name': audio.file_name or f'音频_{audio.file_unique_id}.mp3',
                    'file_size': audio.file_size or 0,
                    'mime_type': audio.mime_type or 'audio/mpeg',
                    'file_type': 'audio'
                }
                
            elif message.voice:
                # 语音消息
                voice = message.voice
                file_info = {
                    'file_id': voice.file_id,
                    'file_name': f'语音_{voice.file_unique_id}.ogg',
                    'file_size': voice.file_size or 0,
                    'mime_type': 'audio/ogg',
                    'file_type': 'voice'
                }
            
            return file_info if file_info else None
            
        except Exception as e:
            logger.error(f"获取文件信息失败: {str(e)}")
            return None
    
    def _check_file_size(self, file_info: Dict[str, Any], max_size_mb: int) -> bool:
        """检查文件大小"""
        if not file_info.get('file_size'):
            return True  # 如果无法获取文件大小，允许通过
        
        file_size_mb = file_info['file_size'] / (1024 * 1024)
        return file_size_mb <= max_size_mb
    
    def _generate_title(self, message: Message, file_info: Dict[str, Any]) -> str:
        """
        生成文件标题
        
        优先级：
        1. 用户提供的 caption
        2. 原始文件名
        3. 根据文件类型生成的默认标题
        """
        try:
            # 1. 优先使用用户提供的 caption
            if message.caption and message.caption.strip():
                return message.caption.strip()
            
            # 2. 使用原始文件名（去除扩展名）
            file_name = file_info.get('file_name', '')
            if file_name and file_name != '未知文档':
                # 去除文件扩展名
                name_without_ext = os.path.splitext(file_name)[0]
                if name_without_ext:
                    return name_without_ext
            
            # 3. 根据文件类型生成默认标题
            file_type = file_info.get('file_type', 'document')
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            
            type_names = {
                'document': '文档',
                'photo': '图片',
                'video': '视频',
                'audio': '音频',
                'voice': '语音'
            }
            
            type_name = type_names.get(file_type, '文件')
            return f"{type_name} - {current_time}"
            
        except Exception as e:
            logger.error(f"生成标题失败: {str(e)}")
            return f"文件 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    def get_file_extension(self, file_name: str) -> str:
        """获取文件扩展名"""
        return os.path.splitext(file_name)[1].lower()
    
    def get_file_type_from_extension(self, file_name: str) -> str:
        """根据文件扩展名判断文件类型"""
        ext = self.get_file_extension(file_name)
        
        for file_type, extensions in self.supported_types.items():
            if ext in extensions:
                return file_type
        
        return 'document'  # 默认为文档类型
    
    def format_file_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "未知大小"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.1f} TB"
