#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试机器人状态
"""

import requests
import json

def test_bot_status():
    """测试机器人状态"""
    bot_token = "8488795192:AAG540MhbhZQNx6NR29vnaNdb_KDZ7uhqpk"
    
    try:
        # 获取机器人信息
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                print("机器人状态测试")
                print("=" * 30)
                print(f"名称: {bot_info.get('first_name', '未知')}")
                print(f"用户名: @{bot_info.get('username', '未知')}")
                print(f"ID: {bot_info.get('id', '未知')}")
                print(f"状态: 正常运行")
                print("=" * 30)
                return True
            else:
                print("机器人响应错误")
                return False
        else:
            print(f"HTTP错误: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False

if __name__ == '__main__':
    test_bot_status()
