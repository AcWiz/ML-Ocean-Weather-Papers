#!/usr/bin/env python3
"""
混合搜索脚本
结合关键词搜索和重要性排序
"""

import os
import re
from pathlib import Path

LEARNINGS_DIR = Path.home() / ".openclaw" / "workspace" / ".learnings"

def hybrid_search(query: str, importance_filter: str = None) -> list:
    """
    混合搜索学习日志
    
    Args:
        query: 搜索关键词
        importance_filter: 重要性过滤 (critical/high/medium/low)
    
    Returns:
        匹配的结果列表
    """
    results = []
    
    # 搜索所有学习文件
    for md_file in LEARNINGS_DIR.glob("*.md"):
        if md_file.name == "scripts":
            continue
            
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 按条目分割
            entries = re.split(r'^##\s+', content, flags=re.MULTILINE)
            
            for entry in entries:
                if not entry.strip():
                    continue
                    
                # 关键词匹配
                if query.lower() in entry.lower():
                    # 提取重要性
                    importance = "medium"
                    if "**Priority**: critical" in entry:
                        importance = "critical"
                    elif "**Priority**: high" in entry:
                        importance = "high"
                    elif "**Priority**: low" in entry:
                        importance = "low"
                    
                    # 重要性过滤
                    if importance_filter and importance != importance_filter:
                        continue
                    
                    # 提取标题
                    title_match = re.match(r'\[.*?\]\s*(.*)', entry)
                    title = title_match.group(1) if title_match else "未命名"
                    
                    results.append({
                        "file": md_file.name,
                        "title": title.strip(),
                        "importance": importance,
                        "preview": entry[:200]
                    })
                    
        except Exception as e:
            continue
    
    # 按重要性排序
    importance_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    results.sort(key=lambda x: importance_order.get(x["importance"], 3))
    
    return results

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    
    if not query:
        print("用法: hybrid_search.py <关键词> [importance_filter]")
        sys.exit(0)
    
    results = hybrid_search(query)
    print(f"找到 {len(results)} 条结果:")
    for r in results[:5]:
        print(f"  [{r['importance']}] {r['title']}")
