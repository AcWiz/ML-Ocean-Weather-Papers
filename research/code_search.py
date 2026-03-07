#!/usr/bin/env python3
"""
代码搜索工具
在 GitHub 上搜索相关代码实现
"""

import urllib.request
import json
import sys

def search_code(query: str, per_page: int = 10) -> list:
    """搜索 GitHub 代码"""
    url = f"https://api.github.com/search/code?q={query}&per_page={per_page}"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get('items', [])
    except Exception as e:
        print(f"搜索失败: {e}")
        return []

def main():
    if len(sys.argv) < 2:
        print("用法: code_search.py <关键词>")
        print("示例: code_search.py data assimilation pytorch")
        sys.exit(1)
    
    query = "+".join(sys.argv[1:])
    
    print(f"=== 代码搜索: {sys.argv[1:]} ===\n")
    
    results = search_code(query)
    for i, item in enumerate(results, 1):
        print(f"{i}. {item.get('name', 'N/A')}")
        print(f"   📁 {item.get('path', 'N/A')}")
        print(f"   🔗 {item.get('html_url', 'N/A')[:60]}...")
        print()
    
    if not results:
        print("未找到相关代码")

if __name__ == "__main__":
    main()
