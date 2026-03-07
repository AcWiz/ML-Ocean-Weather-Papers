#!/usr/bin/env python3
"""
主题记忆系统
类似 Memary 的多主题记忆管理
"""

import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory" / "topics"

class TopicMemory:
    """主题记忆系统"""
    
    def __init__(self):
        self.memory_dir = MEMORY_DIR
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.topics = self.load_topics()
        
    def load_topics(self) -> dict:
        """加载主题"""
        topics_file = self.memory_dir / "topics.json"
        if topics_file.exists():
            with open(topics_file, 'r') as f:
                return json.load(f)
        return defaultdict(list)
    
    def save_topics(self):
        """保存主题"""
        topics_file = self.memory_dir / "topics.json"
        with open(topics_file, 'w') as f:
            json.dump(dict(self.topics), f, indent=2)
    
    def add_memory(self, topic: str, content: str, importance: float = 0.5):
        """添加记忆"""
        memory = {
            "content": content,
            "importance": importance,
            "timestamp": datetime.now().isoformat(),
            "access_count": 0
        }
        self.topics[topic].append(memory)
        self.save_topics()
        print(f"✅ 添加记忆: {topic}")
    
    def recall(self, topic: str, limit: int = 5) -> list:
        """回忆主题记忆"""
        if topic not in self.topics:
            return []
        
        memories = self.topics[topic]
        # 按重要性和访问次数排序
        memories.sort(key=lambda x: (x["importance"], x["access_count"]), reverse=True)
        
        # 更新访问次数
        for m in memories[:limit]:
            m["access_count"] += 1
        self.save_topics()
        
        return memories[:limit]
    
    def get_all_topics(self) -> list:
        """获取所有主题"""
        return list(self.topics.keys())
    
    def search_across_topics(self, query: str) -> dict:
        """跨主题搜索"""
        results = {}
        query_lower = query.lower()
        
        for topic, memories in self.topics.items():
            matches = [m for m in memories if query_lower in m["content"].lower()]
            if matches:
                results[topic] = matches
        
        return results

if __name__ == "__main__":
    tm = TopicMemory()
    print("=== 主题记忆系统 ===\n")
    
    # 测试
    tm.add_memory("AI", "用户关注数据同化和海洋动力学", 0.9)
    tm.add_memory("工具", "每周自动更新科研工具箱", 0.7)
    
    print(f"\n主题列表: {tm.get_all_topics()}")
    print(f"\n回忆 AI: {tm.recall('AI')}")
