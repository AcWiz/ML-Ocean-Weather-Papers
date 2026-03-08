#!/usr/bin/env python3
"""
学术搜索替代方案
使用 Bing API 搜索学术内容
"""
import requests
import re
from bs4 import BeautifulSoup

class AcademicSearchBing:
    """使用 Bing 搜索学术论文"""
    
    def __init__(self):
        self.base_url = "https://www.bing.com/search"
    
    def search(self, query, max_results=10):
        """搜索学术论文"""
        params = {
            "q": f"{query} scholarly",
            "count": max_results
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            resp = requests.get(self.base_url, params=params, headers=headers, timeout=20)
            soup = BeautifulSoup(resp.text, "html.parser")
            
            results = []
            for item in soup.select("li.b_algo")[:max_results]:
                try:
                    title_elem = item.select_one("h2 a")
                    if title_elem:
                        title = title_elem.get_text()
                        link = title_elem.get("href", "")
                        
                        # 提取摘要
                        snippet = item.select_one("p")
                        abstract = snippet.get_text() if snippet else ""
                        
                        # 检查是否是学术链接
                        if any(x in link for x in ["scholar.google", "arxiv.org", "ieee.org", 
                                                     "nature.com", "sciencedirect.com", "springer.com"]):
                            results.append({
                                "title": title,
                                "link": link,
                                "abstract": abstract[:200]
                            })
                except:
                    continue
            
            return results
        except Exception as e:
            return []

# 另一个方案：使用 SearXNG (开源搜索引擎)
class SearXNGSearch:
    """使用 SearXNG (开源隐私搜索引擎)"""
    
    def __init__(self):
        # 公共 SearXNG 实例
        self.instances = [
            "https://searx.be",
            "https://searx.org",
            "https://search.bcow.cn"
        ]
        self.base_url = self.instances[0]
    
    def search(self, query, max_results=10):
        """搜索"""
        params = {
            "q": query,
            "format": "json"
        }
        
        for instance in self.instances:
            try:
                resp = requests.get(f"{instance}/search", params=params, timeout=15)
                if resp.status_code == 200:
                    data = resp.json()
                    
                    results = []
                    for item in data.get("results", [])[:max_results]:
                        results.append({
                            "title": item.get("title", ""),
                            "link": item.get("url", ""),
                            "abstract": item.get("content", "")[:200]
                        })
                    
                    return results
            except:
                continue
        
        return []

if __name__ == "__main__":
    # 测试
    print("🔍 测试 Bing 学术搜索...")
    
    searcher = AcademicSearchBing()
    results = searcher.search("machine learning weather forecasting", 10)
    
    print(f"\n找到 {len(results)} 个学术结果:\n")
    
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title'][:60]}...")
        print(f"   🔗 {r['link'][:50]}...")
        print()
