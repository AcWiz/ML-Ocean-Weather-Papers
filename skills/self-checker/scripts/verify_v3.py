#!/usr/bin/env python3
"""
完整论文验证系统 V3
支持多平台验证：CrossRef, Semantic Scholar, arXiv
"""
import requests
import json
import sys

class FullPaperVerifier:
    def __init__(self):
        self.results = []
    
    def verify_by_title(self, title, platform="crossref"):
        """通过标题搜索并验证论文"""
        
        if platform == "crossref":
            return self.verify_crossref(title)
        elif platform == "semanticscholar":
            return self.verify_semantic(title)
        elif platform == "arxiv":
            return self.verify_arxiv(title)
        else:
            return {"valid": False, "error": "Unknown platform"}
    
    def verify_crossref(self, query):
        """CrossRef 验证"""
        url = "https://api.crossref.org/works"
        params = {"query": query, "rows": 3}
        
        try:
            resp = requests.get(url, params=params, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("message", {}).get("items", [])
                
                if items:
                    item = items[0]
                    authors = item.get("author", [])
                    return {
                        "valid": True,
                        "platform": "CrossRef",
                        "title": item.get("title", [""])[0],
                        "doi": item.get("DOI", ""),
                        "authors": [f"{a.get('given', '')} {a.get('family', '')}" for a in authors[:3]],
                        "year": item.get("published-print", {}).get("date-parts", [[0]])[0][0],
                        "journal": item.get("container-title", [""])[0]
                    }
        except Exception as e:
            return {"valid": False, "error": str(e)}
        
        return {"valid": False, "error": "Not found"}
    
    def verify_semantic(self, query):
        """Semantic Scholar 验证"""
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {"query": query, "limit": 3, "fields": "title,authors,year,venue,externalIds"}
        
        try:
            resp = requests.get(url, params=params, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                papers = data.get("data", [])
                
                if papers:
                    p = papers[0]
                    external = p.get("externalIds", {})
                    return {
                        "valid": True,
                        "platform": "Semantic Scholar",
                        "title": p.get("title", ""),
                        "arxiv": external.get("ArXiv", ""),
                        "doi": external.get("DOI", ""),
                        "authors": [a.get("name", "") for a in p.get("authors", [])[:3]],
                        "year": p.get("year", ""),
                        "venue": p.get("venue", "")
                    }
        except Exception as e:
            return {"valid": False, "error": str(e)}
        
        return {"valid": False, "error": "Not found"}
    
    def verify_arxiv(self, query):
        """arXiv 验证"""
        import re
        url = "http://export.arxiv.org/api/query"
        params = {"search_query": f"all:{query}", "max_results": 3, "sortBy": "relevance"}
        
        try:
            resp = requests.get(url, params=params, timeout=20)
            entries = re.findall(r'<entry>(.*?)</entry>', resp.text, re.DOTALL)
            
            if entries:
                e = entries[0]
                title = re.search(r'<title>([^<]+)</title>', e)
                arxiv_id = re.search(r'<id>([^<]+)</id>', e)
                published = re.search(r'<published>([^<]+)</published>', e)
                authors = re.findall(r'<name>([^<]+)</name>', e)
                
                return {
                    "valid": True,
                    "platform": "arXiv",
                    "title": title.group(1).strip() if title else "",
                    "arxiv_id": arxiv_id.group(1).split('/')[-1] if arxiv_id else "",
                    "authors": authors[:3],
                    "year": published.group(1)[:4] if published else "",
                    "link": f"https://arxiv.org/abs/{arxiv_id.group(1).split('/')[-1]}" if arxiv_id else ""
                }
        except Exception as e:
            return {"valid": False, "error": str(e)}
        
        return {"valid": False, "error": "Not found"}

if __name__ == "__main__":
    verifier = FullPaperVerifier()
    
    # 测试
    test_queries = [
        "GraphCast weather forecasting",
        "Pangu-Weather",
        "FourCastNet weather"
    ]
    
    print("🔍 完整论文验证系统 V3")
    print("=" * 60)
    
    for q in test_queries:
        print(f"
查询: {q}")
        
        # 尝试多个平台
        for platform in ["semanticscholar", "crossref", "arxiv"]:
            result = verifier.verify_by_title(q, platform)
            if result.get("valid"):
                print(f"   [{platform}] ✅ {result['title'][:45]}...")
                print(f"      作者: {result.get('authors', [''])[0]}")
                if result.get("arxiv"):
                    print(f"      arXiv: {result.get('arxiv')}")
                if result.get("doi"):
                    print(f"      DOI: {result.get('doi')}")
                break
        else:
            print(f"   ❌ 未找到")
