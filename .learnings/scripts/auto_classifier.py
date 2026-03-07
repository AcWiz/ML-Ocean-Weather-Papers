#!/usr/bin/env python3
"""
重要性自动分类器
分析学习日志，自动判断重要性级别
"""

import re
import sys
from datetime import datetime

# 重要性关键词
IMPORTANCE_KEYWORDS = {
    "critical": [
        "安全", "漏洞", "后门", "木马", "攻击", "紧急", "失控",
        "security", "vulnerability", "emergency", "critical"
    ],
    "high": [
        "错误", "失败", "崩溃", "bug", "修复", "纠正", "不对",
        "error", "fail", "bug", "fix", "wrong"
    ],
    "medium": [
        "优化", "改进", "提升", "更好的方法", "重构",
        "improve", "refactor", "optimize", "better"
    ],
    "low": [
        "笔记", "记录", "学习", "了解", "发现",
        "note", "learn", "discover", "note"
    ]
}

# 分类关键词
CATEGORY_KEYWORDS = {
    "correction": ["纠正", "不对", "错了", "实际上", "no that's"],
    "error": ["错误", "失败", "异常", "error", "fail", "exception"],
    "feature_request": ["需要", "请求", "希望", "wish", "want", "request"],
    "knowledge_gap": ["不知道", "不了解", "原来", "没发现", "outdated"],
    "best_practice": ["更好的", "最优", "最佳", "better", "best", "optimal"]
}

def classify_importance(text: str) -> str:
    """根据文本内容判断重要性"""
    text_lower = text.lower()
    
    for level, keywords in IMPORTANCE_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                return level
    
    return "medium"  # 默认中等重要性

def classify_category(text: str) -> str:
    """根据文本内容判断分类"""
    text_lower = text.lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                return category
    
    return "other"

def analyze_entry(entry_text: str) -> dict:
    """分析单个日志条目"""
    return {
        "importance": classify_importance(entry_text),
        "category": classify_category(entry_text),
        "timestamp": datetime.now().isoformat()
    }

def process_learnings_file(filepath: str) -> list:
    """处理学习日志文件"""
    results = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 按条目分割 (以 ## 开头)
        entries = re.split(r'^##\s+', content, flags=re.MULTILINE)
        
        for entry in entries:
            if entry.strip():
                result = analyze_entry(entry)
                results.append(result)
                
    except FileNotFoundError:
        print(f"文件不存在: {filepath}")
    except Exception as e:
        print(f"处理错误: {e}")
    
    return results

if __name__ == "__main__":
    # 测试
    test_text = "用户纠正我说这个方法是错的"
    result = analyze_entry(test_text)
    print(f"测试结果: {result}")
