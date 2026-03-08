#!/usr/bin/env python3
"""
IEEE 论文搜索模块 V2
通过 CrossRef 搜索 IEEE 论文
"""
import requests
import time

class IEEESearch:
    """IEEE 论文搜索"""
    
    def __init__(self):
        self.base_url = "https://api.crossref.org/works"
    
    def search(self, query, max_results=20):
        """搜索 IEEE 论文"""
        params = {
            "query": f"{query} ieee",
            "rows": max_results * 2,  # 多取一些以便过滤
            "select": "DOI,title,author,published,container-title,publisher"
        }
        
        try:
            resp = requests.get(self.base_url, params=params, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("message", {}).get("items", [])
                
                papers = []
                for item in items:
                    # 过滤 IEEE
                    publisher = item.get("publisher", "")
                    if "IEEE" not in publisher:
                        continue
                    
                    title = item.get("title", [""])[0]
                    doi = item.get("DOI", "")
                    year = item.get("published-print", {}).get("date-parts", [[0]])[0][0]
                    
                    authors = item.get("author", [])
                    author_names = [f"{a.get('given', '')} {a.get('family', '')}" 
                                  for a in authors[:5]]
                    
                    papers.append({
                        "source": "IEEE Xplore",
                        "id": doi.split("/")[-1] if doi else "",
                        "doi": doi,
                        "title": title,
                        "authors": author_names,
                        "year": str(year),
                        "url": f"https://doi.org/{doi}" if doi else "",
                        "ieee_url": f"https://ieeexplore.ieee.org/document/{doi.split('/')[-1]}" if doi else "",
                        "publisher": publisher
                    })
                    
                    if len(papers) >= max_results:
                        break
                
                return papers
        except:
            pass
        
        return []
    
    def search_multiple_queries(self, queries, max_results=20):
        """多查询搜索"""
        all_papers = []
        
        for q in queries:
            papers = self.search(q, max_results)
            all_papers.extend(papers)
            time.sleep(0.3)
        
        # 去重
        seen = set()
        unique = []
        for p in all_papers:
            if p.get("doi") not in seen:
                seen.add(p.get("doi"))
                unique.append(p)
        
        return unique

# 测试
if __name__ == "__main__":
    search = IEEESearch()
    
    print("🔍 搜索 IEEE 论文...")
    
    queries = [
        "machine learning weather",
        "deep learning ocean",
        "neural network forecasting",
        "data assimilation"
    ]
    
    results = search.search_multiple_queries(queries, 10)
    
    print(f"\n找到 {len(results)} 篇 IEEE 论文:\n")
    
    for i, p in enumerate(results[:10], 1):
        print(f"{i}. {p['title'][:55]}...")
        print(f"   {p['year']} | {p['authors'][0]}")
        print(f"   🔗 {p.get('ieee_url', '')[:50]}...")
        print()
