#!/usr/bin/env python3
"""
智能记忆管理器
自动管理多层级记忆的存储、检索和清理
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# 配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
LEARNINGS_DIR = WORKSPACE / ".learnings"

class MemoryManager:
    """智能记忆管理器"""
    
    def __init__(self):
        self.short_term_max = 50  # 短期记忆最大轮数
        self.medium_term_days = 7  # 中期记忆保留天数
        
    def should_remember(self, conversation_text: str) -> bool:
        """
        判断是否应该记住当前对话
        基于关键词和重要性
        """
        important_keywords = [
            "记住", "不要忘", "重要", "关键",
            "remember", "important", "critical",
            "偏好", "喜欢", "讨厌", "过敏"
        ]
        
        for keyword in important_keywords:
            if keyword in conversation_text:
                return True
        return False
    
    def categorize_memory(self, text: str) -> str:
        """分类记忆到正确的层级"""
        # 检查是否是错误/纠正
        error_keywords = ["错误", "失败", "不对", "wrong", "error", "fail"]
        for kw in error_keywords:
            if kw in text:
                return "errors"
        
        # 检查是否是功能请求
        feature_keywords = ["需要", "希望", "想要", "wish", "want"]
        for kw in feature_keywords:
            if kw in text:
                return "feature_requests"
        
        # 检查是否是学习
        learn_keywords = ["学到了", "发现", "原来", "learn", "discover"]
        for kw in learn_keywords:
            if kw in text:
                return "learnings"
        
        return "general"
    
    def save_to_memory(self, text: str, category: str = None) -> bool:
        """保存记忆到适当位置"""
        if category is None:
            category = self.categorize_memory(text)
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 根据分类保存到不同文件
        if category == "errors":
            filepath = LEARNINGS_DIR / "ERRORS.md"
        elif category == "feature_requests":
            filepath = LEARNINGS_DIR / "FEATURE_REQUESTS.md"
        elif category == "learnings":
            filepath = LEARNINGS_DIR / "LEARNINGS.md"
        else:
            filepath = MEMORY_DIR / f"{today}.md"
        
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(f"\n## {today} - 自动记录\n")
                f.write(f"{text}\n")
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False
    
    def cleanup_old_memories(self) -> int:
        """清理过期中期记忆"""
        cutoff = datetime.now() - timedelta(days=self.medium_term_days)
        cleaned = 0
        
        for md_file in MEMORY_DIR.glob("*.md"):
            try:
                # 解析文件名日期
                date_str = md_file.stem
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                
                if file_date < cutoff:
                    md_file.unlink()
                    cleaned += 1
            except Exception:
                continue
        
        return cleaned
    
    def get_memory_stats(self) -> dict:
        """获取记忆统计"""
        stats = {
            "short_term": self.short_term_max,
            "medium_term_days": self.medium_term_days,
            "total_memories": 0,
            "categories": {}
        }
        
        # 统计各分类
        for category, dirname in [
            ("learnings", LEARNINGS_DIR),
            ("memory", MEMORY_DIR)
        ]:
            if dirname.exists():
                count = len(list(dirname.glob("*.md")))
                stats["categories"][category] = count
                stats["total_memories"] += count
        
        return stats

if __name__ == "__main__":
    mm = MemoryManager()
    print("=== 智能记忆管理器 ===\n")
    
    # 显示统计
    stats = mm.get_memory_stats()
    print(f"短期记忆容量: {stats['short_term']} 轮")
    print(f"中期记忆保留: {stats['medium_term_days']} 天")
    print(f"长期记忆文件: {stats['total_memories']} 个")
    
    # 测试保存
    print("\n✅ 记忆管理器就绪")
