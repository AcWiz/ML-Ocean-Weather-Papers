#!/usr/bin/env python3
"""
文献检索工具
快速搜索相关论文和代码
"""

import urllib.request
import urllib.parse
import json
import sys

def search_github(query: str, per_page: int = 5) -> list:
    """搜索 GitHub 仓库"""
    encoded_query = urllib.parse.quote(query, safe='')
    url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc&per_page={per_page}"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get('items', [])
    except Exception as e:
        print(f"搜索失败: {e}")
        return []

def format_result(repo: dict) -> str:
    """格式化搜索结果"""
    return f"""★ {repo.get('full_name', 'N/A')}
   ⭐ {repo.get('stargazers_count', 0)}
   {repo.get('description', 'N/A')[:80]}
   🔗 {repo.get('html_url', 'N/A')}
"""

def main():
    if len(sys.argv) < 2:
        print("用法: literature_search.py <关键词>")
        sys.exit(1)
    
    query = "+".join(sys.argv[1:])
    
    print(f"=== 搜索: {sys.argv[1:]} ===\n")
    print("📚 GitHub 项目:\n")
    
    results = search_github(query)
    for i, repo in enumerate(results, 1):
        print(f"{i}. {format_result(repo)}")
    
    if not results:
        print("未找到相关项目")

if __name__ == "__main__":
    main()
