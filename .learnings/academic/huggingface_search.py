#!/usr/bin/env python3
"""
HuggingFace 模型搜索
"""
import sys
import urllib.request
import urllib.parse
import json

def search_huggingface(query, task="", max_results=10):
    """搜索HuggingFace模型"""
    params = {
        "search": query,
        "limit": max_results,
        "sort": "downloads"
    }
    
    if task:
        params["pipeline_tag"] = task
    
    url = f"https://huggingface.co/api/models?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        
        models = []
        for m in data:
            models.append({
                "name": m.get("modelId", ""),
                "downloads": m.get("downloads", 0),
                "likes": m.get("likes", 0),
                "task": m.get("pipeline_tag", ""),
                "author": m.get("author", ""),
                "url": f"https://huggingface.co/{m.get('modelId', '')}"
            })
        return models
    except Exception as e:
        return [{"error": str(e)}]

def main():
    query = " ".join(sys.argv[1:]) or "data assimilation"
    print(f"🤗 HuggingFace模型搜索: {query}")
    print("-" * 50)
    
    models = search_huggingface(query, max_results=5)
    
    for i, m in enumerate(models, 1):
        if "error" in m:
            print(f"错误: {m['error']}")
            continue
        print(f"\n{i}. {m['name']}")
        print(f"   📥 {m['downloads']:,} downloads | ❤️ {m['likes']}")
        print(f"   📍 {m['url']}")

if __name__ == "__main__":
    main()
