#!/usr/bin/env python3
"""
GitHub 代码搜索
"""
import sys
import urllib.request
import urllib.parse
import json

def search_github_code(query, language="", max_results=10):
    """搜索GitHub代码"""
    # 使用GitHub API
    token = os.environ.get("GH_TOKEN", "")
    
    params = {
        "q": query + (f" language:{language}" if language else ""),
        "per_page": max_results,
        "sort": "stars"
    }
    
    url = f"https://api.github.com/search/code?{urllib.parse.urlencode(params)}"
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        
        results = []
        for item in data.get("items", [])[:max_results]:
            results.append({
                "name": item.get("name", ""),
                "repo": item.get("repository", {}).get("full_name", ""),
                "path": item.get("path", ""),
                "url": item.get("html_url", ""),
                "score": item.get("score", 0)
            })
        return results
    except Exception as e:
        return [{"error": str(e)}]

import os

def main():
    query = " ".join(sys.argv[1:]) or "data assimilation"
    print(f"🔍 GitHub代码搜索: {query}")
    print("-" * 50)
    
    results = search_github_code(query, max_results=5)
    
    for i, r in enumerate(results, 1):
        if "error" in r:
            print(f"错误: {r['error']}")
            continue
        print(f"\n{i}. {r['name']}")
        print(f"   📁 {r['repo']}")
        print(f"   📍 {r['url']}")

if __name__ == "__main__":
    main()
