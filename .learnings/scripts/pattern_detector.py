#!/usr/bin/env python3
"""
模式识别脚本
自动检测重复出现的问题模式
"""

import re
from pathlib import Path
from collections import Counter

LEARNINGS_DIR = Path.home() / ".openclaw" / "workspace" / ".learnings"

def extract_patterns() -> dict:
    """提取所有模式"""
    patterns = {
        "categories": [],
        "areas": [],
        "statuses": [],
        "recurring_issues": []
    }
    
    # 收集所有文件
    files = list(LEARNINGS_DIR.glob("*.md"))
    files = [f for f in files if f.name != "scripts"]
    
    for md_file in files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取分类
            categories = re.findall(r'\[LRN-.*?\]\s*(\w+)', content)
            patterns["categories"].extend(categories)
            
            # 提取领域
            areas = re.findall(r'\*\*Area\*\*:\s*(\w+)', content)
            patterns["areas"].extend(areas)
            
            # 提取状态
            statuses = re.findall(r'\*\*Status\*\*:\s*(\w+)', content)
            patterns["statuses"].extend(statuses)
            
            # 提取 See Also 链接 (重复问题)
            see_also = re.findall(r'See Also:.*?\[(.*?)\]', content)
            if see_also:
                patterns["recurring_issues"].extend(see_also)
                
        except Exception as e:
            continue
    
    return patterns

def analyze_patterns() -> dict:
    """分析模式并生成报告"""
    patterns = extract_patterns()
    
    report = {
        "category_counts": Counter(patterns["categories"]),
        "area_counts": Counter(patterns["areas"]),
        "status_counts": Counter(patterns["statuses"]),
        "recurring_count": len(patterns["recurring_issues"]),
        "needs_attention": []
    }
    
    # 检测需要关注的问题
    # 1. 多次出现的分类
    for cat, count in report["category_counts"].items():
        if count >= 2:
            report["needs_attention"].append({
                "type": "recurring_category",
                "detail": f"'{cat}' 出现 {count} 次"
            })
    
    # 2. pending 状态过多
    pending_count = report["status_counts"].get("pending", 0)
    total = sum(report["status_counts"].values())
    if pending_count > 3:
        report["needs_attention"].append({
            "type": "backlog",
            "detail": f"有 {pending_count}/{total} 个待处理项"
        })
    
    return report

if __name__ == "__main__":
    report = analyze_patterns()
    
    print("=== 模式识别报告 ===\n")
    
    print("分类统计:")
    for cat, count in report["category_counts"].most_common(5):
        print(f"  {cat}: {count}")
    
    print(f"\n领域统计:")
    for area, count in report["area_counts"].most_common(5):
        print(f"  {area}: {count}")
    
    print(f"\n状态统计:")
    for status, count in report["status_counts"].most_common():
        print(f"  {status}: {count}")
    
    if report["needs_attention"]:
        print("\n⚠️ 需要关注:")
        for item in report["needs_attention"]:
            print(f"  - {item['type']}: {item['detail']}")
    else:
        print("\n✅ 暂无需要特别关注的问题")
