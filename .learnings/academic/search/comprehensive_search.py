#!/usr/bin/env python3
"""
综合学术搜索系统
覆盖所有主要学术平台
"""
import sys
import json
from arxiv_search import ArxivSearch
from openalex_search import OpenAlexSearch
import requests
import time

class ComprehensiveSearch:
    """综合学术搜索"""
    
    def __init__(self):
        self.arxiv = ArxivSearch()
        self.openalex = OpenAlexSearch()
        self.results = []
    
    def search(self, query):
        """多平台综合搜索"""
        print(f"\n🔍 综合搜索: {query}")
        print("=" * 50)
        
        # 1. arXiv
        print("  📚 arXiv...", end=" ")
        arxiv_results = self.arxiv.search(query, 30)
        print(f"+{len(arxiv_results)}")
        self.results.extend(arxiv_results)
        
        time.sleep(0.5)
        
        # 2. OpenAlex
        print("  🌐 OpenAlex...", end=" ")
        openalex_results = self.openalex.search(query, 30)
        print(f"+{len(openalex_results)}")
        self.results.extend(openalex_results)
        
        time.sleep(0.5)
        
        # 3. CrossRef
        print("  📖 CrossRef...", end=" ")
        crossref_results = self._search_crossref(query, 20)
        print(f"+{len(crossref_results)}")
        self.results.extend(crossref_results)
        
        # 去重
        unique = self._deduplicate()
        
        print(f"\n✅ 总计: {len(unique)} 篇去重论文")
        
        return unique
    
    def _search_crossref(self, query, limit=20):
        """CrossRef 搜索"""
        url = "https://api.crossref.org/works"
        params = {"query": query, "rows": limit}
        
        try:
            resp = requests.get(url, params=params, timeout=20)
            if resp.status_code == 200:
                items = resp.json().get("message", {}).get("items", [])
                
                papers = []
                for item in items:
                    title = item.get("title", [""])[0]
                    doi = item.get("DOI", "")
                    year = item.get("published-print", {}).get("date-parts", [[0]])[0][0]
                    authors = item.get("author", [])[:5]
                    author_names = [f"{a.get('given', '')} {a.get('family', '')}" for a in authors]
                    
                    papers.append({
                        "source": "CrossRef",
                        "id": doi.split("/")[-1] if doi else "",
                        "doi": doi,
                        "title": title,
                        "authors": author_names,
                        "year": str(year),
                        "url": f"https://doi.org/{doi}" if doi else ""
                    })
                return papers
        except:
            pass
        return []
    
    def _deduplicate(self):
        """去重"""
        seen = set()
        unique = []
        
        for r in self.results:
            key = r.get("title", "").lower().strip()
            if key and key not in seen:
                seen.add(key)
                unique.append(r)
        
        # 按引用/相关性排序
        unique.sort(key=lambda x: x.get("cited", 0), reverse=True)
        
        return unique

def main():
    if len(sys.argv) < 2:
        print("用法: python comprehensive_search.py <关键词>")
        sys.exit(1)
    
    query = sys.argv[1]
    
    searcher = ComprehensiveSearch()
    results = searcher.search(query)
    
    print("\n📊 前20篇论文:")
    for i, p in enumerate(results[:20], 1):
        print(f"\n{i}. {p.get('title', '')[:60]}")
        print(f"   {p.get('year', '')} | {p.get('source', '')} | {p.get('authors', [''])[0]}")
        if p.get('url'):
            print(f"   🔗 {p['url'][:60]}")

if __name__ == "__main__":
    main()
