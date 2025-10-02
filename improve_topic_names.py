#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进话题名称获取
"""

import json
import os

def improve_topic_names():
    """改进话题名称"""
    try:
        if not os.path.exists("detected_topics.json"):
            print("没有话题数据文件")
            return
        
        with open("detected_topics.json", "r", encoding="utf-8") as f:
            topics_data = json.load(f)
        
        print("当前话题数据:")
        for topic_id, topic_info in topics_data.items():
            print(f"  ID: {topic_id}, 名称: {topic_info.get('name', '未设置')}")
        
        # 改进话题名称
        improved = False
        for topic_id, topic_info in topics_data.items():
            current_name = topic_info.get("name", "")
            
            # 如果当前名称只是数字或很短，尝试改进
            if current_name.isdigit() or len(current_name) < 3:
                # 根据话题ID设置更有意义的名称
                if topic_id == "2":
                    new_name = "文件分享"
                elif topic_id == "3":
                    new_name = "文档存储"
                elif topic_id == "5":
                    new_name = "图片资源"
                elif topic_id == "7":
                    new_name = "讨论区"
                elif topic_id == "10":
                    new_name = "批量上传"
                else:
                    new_name = f"话题{topic_id}"
                
                topics_data[topic_id]["name"] = new_name
                improved = True
                print(f"改进话题 {topic_id}: '{current_name}' -> '{new_name}'")
        
        if improved:
            # 保存改进后的数据
            with open("detected_topics.json", "w", encoding="utf-8") as f:
                json.dump(topics_data, f, ensure_ascii=False, indent=2)
            print("\n话题名称已改进并保存")
        else:
            print("\n话题名称无需改进")
        
        print("\n改进后的话题数据:")
        for topic_id, topic_info in topics_data.items():
            name = topic_info.get("name", f"话题{topic_id}")
            count = topic_info.get("count", 0)
            print(f"  - {name}：{topic_id} (消息数: {count})")
            
    except Exception as e:
        print(f"改进话题名称时发生错误: {str(e)}")

def create_sample_topic_data():
    """创建示例话题数据"""
    sample_data = {
        "2": {
            "name": "文件分享",
            "count": 5,
            "last_detected": "2025-10-02T18:00:00"
        },
        "3": {
            "name": "文档存储",
            "count": 8,
            "last_detected": "2025-10-02T18:01:00"
        },
        "5": {
            "name": "图片资源",
            "count": 3,
            "last_detected": "2025-10-02T18:02:00"
        },
        "7": {
            "name": "讨论区",
            "count": 12,
            "last_detected": "2025-10-02T18:03:00"
        }
    }
    
    with open("detected_topics.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    print("已创建示例话题数据:")
    for topic_id, topic_info in sample_data.items():
        name = topic_info["name"]
        count = topic_info["count"]
        print(f"  - {name}：{topic_id} (消息数: {count})")

if __name__ == "__main__":
    print("话题名称改进工具")
    print("=" * 40)
    
    choice = input("选择操作:\n1. 改进现有话题名称\n2. 创建示例数据\n请输入选择 (1/2): ").strip()
    
    if choice == "1":
        improve_topic_names()
    elif choice == "2":
        create_sample_topic_data()
    else:
        print("无效选择")
