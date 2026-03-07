#!/usr/bin/env python3
"""
通用网页搜索 - 使用DuckDuckGo
"""
import sys
import urllib.request
import urllib.parse
import re
import json

def search_web(query, engine="duckduckgo", num_results=10):
    """网页搜索"""
    
    if engine == "duckduckgo":
        # 使用DuckDuckGo HTML
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                html = response.read().decode("utf-8")
            
            # 提取结果
            results = []
            items = re.findall(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>.*?<a[^>]+class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
            
            for item in items[:num_results]:
                url = item[0]
                if url.startswith('//'):
                    url = 'https:' + url
                title = re.sub(r'<[^>]+>', '', item[1]).strip()
                snippet = re.sub(r'<[^>]+>', '', item[2]).strip()
                results.append({"title": title, "url": url, "snippet": snippet})
            
            return results
        except Exception as e:
            return [{"error": str(e)}]
    
    return [{"error": "Unknown engine"}]

def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "machine learning"
    
    print(f"🔍 搜索: {query}")
    print("=" * 50)
    
    results = search_web(query)
    
    for i, r in enumerate(results, 1):
        if "error" in r:
            print(f"错误: {r['error']}")
            continue
        print(f"\n{i}. {r['title'][:60]}")
        print(f"   📍 {r['url'][:60]}")
        print(f"   📝 {r['snippet'][:100]}")

if __name__ == "__main__":
    main()
