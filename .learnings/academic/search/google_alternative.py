#!/usr/bin/env python3
"""
Google 搜索替代方案
由于 Google 有严格反爬虫，使用以下替代方案：
1. DuckDuckGo - 隐私搜索
2. Bing - 微软搜索
3. Qwant - 欧洲隐私搜索
4. Startpage - 隐私搜索
"""
import httpx
import re

class GoogleAlternative:
    """Google 替代搜索"""
    
    def __init__(self):
        self.providers = [
            ("Bing", self._search_bing),
            ("Startpage", self._search_startpage),
            ("Qwant", self._search_qwant),
        ]
    
    def search(self, query, max_results=10):
        """尝试多个搜索提供商"""
        
        for name, func in self.providers:
            try:
                results = func(query, max_results)
                if results:
                    print(f"✅ {name} 成功")
                    return results
            except Exception as e:
                print(f"❌ {name}: {e}")
                continue
        
        # 如果都失败，返回空列表
        return []
    
    def _search_bing(self, query, max_results):
        """Bing 搜索"""
        url = "https://www.bing.com/search"
        params = {"q": query, "form": "QBLH", "count": max_results}
        
        resp = httpx.get(url, params=params, timeout=15, follow_redirects=True)
        
        # 解析
        results = []
        
        # 提取标题和链接
        titles = re.findall(r'<h2><a[^>]*href=["\']([^"\']+)["\'][^>]*>([^<]+)</a></h2>', resp.text)
        
        for link, title in titles[:max_results]:
            if link.startswith("http"):
                results.append({
                    "title": title.strip(),
                    "link": link,
                    "source": "Bing"
                })
        
        return results
    
    def _search_startpage(self, query, max_results):
        """Startpage 搜索"""
        url = "https://www.startpage.com/do/search"
        params = {"query": query, "lui": "english"}
        
        resp = httpx.get(url, params=params, timeout=15, follow_redirects=True)
        
        # 解析
        results = []
        
        # 查找链接和标题
        links = re.findall(r'<a class="web_result_url"[^>]*href=["\']([^"\']+)["\']', resp.text)
        titles = re.findall(r'<a class="result_link"[^>]*>([^<]+)</a>', resp.text)
        
        for title, link in zip(titles[:max_results], links[:max_results]):
            if link.startswith("http"):
                results.append({
                    "title": title.strip(),
                    "link": link,
                    "source": "Startpage"
                })
        
        return results
    
    def _search_qwant(self, query, max_results):
        """Qwant 搜索"""
        url = "https://www.qwant.com/"
        params = {"q": query, "lt": "web"}
        
        resp = httpx.get(url, params=params, timeout=15)
        
        # Qwant 使用 JavaScript 渲染，静态解析困难
        return []

# 如果都不行，使用备用学术搜索
class FallbackAcademicSearch:
    """备用学术搜索 - 当所有 Web 搜索失败时使用"""
    
    def __init__(self):
        self.apis = [
            ("arXiv", "http://export.arxiv.org/api/query"),
            ("OpenAlex", "https://api.openalex.org/works"),
            ("CrossRef", "https://api.crossref.org/works"),
        ]
    
    def search(self, query, max_results=10):
        """学术 API 搜索"""
        
        results = []
        
        # arXiv
        try:
            import requests
            proxies = {"http": "http://192.168.74.1:7890", "https": "http://192.168.74.1:7890"}
            
            url = "http://export.arxiv.org/api/query"
            params = {"search_query": f"all:{query}", "max_results": max_results}
            
            resp = requests.get(url, params=params, proxies=proxies, timeout=15)
            entries = re.findall(r'<entry>(.*?)</entry>', resp.text, re.DOTALL)
            
            for e in entries[:max_results]:
                title = re.search(r'<title>([^<]+)</title>', e)
                arxiv_id = re.search(r'<id>([^<]+)</id>', e)
                
                if title and arxiv_id:
                    aid = arxiv_id.group(1).split('/')[-1]
                    results.append({
                        "title": title.group(1).strip(),
                        "link": f"https://arxiv.org/abs/{aid}",
                        "source": "arXiv"
                    })
        except Exception as e:
            print(f"arXiv 错误: {e}")
        
        return results

if __name__ == "__main__":
    searcher = GoogleAlternative()
    
    print("🔍 搜索: machine learning weather forecasting\n")
    results = searcher.search("machine learning weather forecasting", 10)
    
    print(f"\n找到 {len(results)} 个结果:")
    for i, r in enumerate(results[:5], 1):
        print(f"{i}. {r['title'][:50]}...")
        print(f"   来源: {r['source']}")
