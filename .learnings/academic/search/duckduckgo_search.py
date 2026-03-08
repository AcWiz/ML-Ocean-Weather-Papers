#!/usr/bin/env python3
"""
DuckDuckGo 学术搜索模块
替代 Google 搜索
"""
import httpx
import re

class DuckDuckGoSearch:
    """DuckDuckGo HTML 搜索"""
    
    def __init__(self):
        self.base_url = "https://html.duckduckgo.com/html/"
    
    def search(self, query, max_results=15):
        """搜索学术相关结果"""
        
        params = {"q": query}
        
        try:
            resp = httpx.get(self.base_url, params=params, timeout=30)
            
            if resp.status_code != 200:
                return []
            
            # 解析 HTML
            titles = re.findall(r'<a class="result__a"[^>]*>([^<]+)</a>', resp.text)
            links = re.findall(r'<a class="result__a"[^>]*href="([^"]+)"', resp.text)
            snippets = re.findall(r'<a class="result__snippet"[^>]*>([^<]+)</a>', resp.text)
            
            results = []
            for i, (title, link) in enumerate(zip(titles, links)):
                # 清理链接
                if link.startswith("//"):
                    link = "https:" + link
                elif link.startswith("/"):
                    continue
                
                # 检查是否是学术相关链接
                academic_domains = [
                    "arxiv.org", "scholar.google", "ieee.org", 
                    "nature.com", "sciencedirect.com", "springer.com",
                    "semanticscholar.org", "paperswithcode.com",
                    "acm.org", "jstor.org"
                ]
                
                # 优先学术结果，但也保留其他
                results.append({
                    "title": title.strip(),
                    "link": link,
                    "snippet": snippets[i].strip() if i < len(snippets) else "",
                    "is_academic": any(d in link for d in academic_domains)
                })
                
                if len(results) >= max_results:
                    break
            
            # 优先排序学术结果
            academic = [r for r in results if r["is_academic"]]
            non_academic = [r for r in results if not r["is_academic"]]
            
            return academic + non_academic
            
        except Exception as e:
            print(f"搜索错误: {e}")
            return []

# 测试
if __name__ == "__main__":
    searcher = DuckDuckGoSearch()
    
    print("🔍 DuckDuckGo 学术搜索测试...")
    results = searcher.search("machine learning weather forecasting", 10)
    
    print(f"\n找到 {len(results)} 个结果:")
    for i, r in enumerate(results, 1):
        academic = "📚" if r["is_academic"] else "🌐"
        print(f"\n{academic} {i}. {r['title'][:50]}...")
        print(f"   {r['link'][:55]}...")
