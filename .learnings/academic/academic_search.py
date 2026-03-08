#!/usr/bin/env python3
"""
学术论文综合搜索系统
支持多平台：arXiv, OpenAlex, CrossRef
"""
import requests
import re
import json
import time
import sys

PROXIES = {"http": "http://192.168.74.1:7890", "https": "http://192.168.74.1:7890"}

class AcademicSearch:
    def __init__(self):
        self.results = []
    
    def search_arxiv(self, query, max_results=20):
        """搜索 arXiv"""
        url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "max_results": max_results,
            "sortBy": "relevance"
        }
        
        try:
            resp = requests.get(url, params=params, proxies=PROXIES, timeout=20)
            entries = re.findall(r'<entry>(.*?)</entry>', resp.text, re.DOTALL)
            
            papers = []
            for e in entries[:max_results]:
                title = re.search(r'<title>([^<]+)</title>', e)
                arxiv_id = re.search(r'<id>([^<]+)</id>', e)
                published = re.search(r'<published>([^<]+)</published>', e)
                authors = re.findall(r'<name>([^<]+)</name>', e)[:5]
                abstract = re.search(r'<summary>([^<]+)</summary>', e)
                
                if title and arxiv_id:
                    aid = arxiv_id.group(1).split('/')[-1]
                    papers.append({
                        "source": "arXiv",
                        "arxiv_id": aid.split('v')[0],
                        "title": title.group(1).strip(),
                        "authors": authors,
                        "year": published.group(1)[:4] if published else "",
                        "abstract": abstract.group(1).strip()[:300] if abstract else "",
                        "url": f"https://arxiv.org/abs/{aid}",
                        "pdf": f"https://arxiv.org/pdf/{aid}"
                    })
            return papers
        except Exception as e:
            print(f"arXiv 错误: {e}")
            return []
    
    def search_openalex(self, query, max_results=20):
        """搜索 OpenAlex"""
        url = "https://api.openalex.org/works"
        params = {
            "search": query,
            "per_page": max_results,
            "filter": "concepts.id:C86841326",  # Computer Science
            "sort": "cited_by_count:desc"
        }
        
        try:
            resp = requests.get(url, params=params, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                papers = []
                
                for r in data.get("results", [])[:max_results]:
                    title = r.get("title", "")
                    year = r.get("publication_year", "")
                    dois = r.get("doi", "")
                    doi = dois.split("/")[-1] if dois else ""
                    
                    # 获取 arXiv ID
                    arxiv = ""
                    for host in r.get("host_organizations", []):
                        if "arXiv" in str(host):
                            arxiv = "arXiv"
                    
                    authors = r.get("authorships", [])[:5]
                    author_names = [a.get("author", {}).get("display_name", "") for a in authors]
                    
                    papers.append({
                        "source": "OpenAlex",
                        "arxiv_id": arxiv,
                        "doi": doi,
                        "title": title,
                        "authors": author_names,
                        "year": str(year),
                        "url": dois if dois else "",
                    })
                return papers
        except Exception as e:
            print(f"OpenAlex 错误: {e}")
            return []
    
    def search_crossref(self, query, max_results=10):
        """搜索 CrossRef"""
        url = "https://api.crossref.org/works"
        params = {"query": query, "rows": max_results}
        
        try:
            resp = requests.get(url, params=params, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                papers = []
                
                for item in data.get("message", {}).get("items", [])[:max_results]:
                    title = item.get("title", [""])[0]
                    doi = item.get("DOI", "")
                    year = item.get("published-print", {}).get("date-parts", [[0]])[0][0]
                    authors = item.get("author", [])[:5]
                    author_names = [f"{a.get('given', '')} {a.get('family', '')}" for a in authors]
                    
                    papers.append({
                        "source": "CrossRef",
                        "doi": doi,
                        "title": title,
                        "authors": author_names,
                        "year": str(year),
                        "url": f"https://doi.org/{doi}"
                    })
                return papers
        except Exception as e:
            print(f"CrossRef 错误: {e}")
            return []
    
    def search_all(self, query):
        """综合搜索"""
        print(f"\n🔍 搜索: {query}")
        print("-" * 40)
        
        all_results = []
        
        # arXiv 搜索
        print("  arXiv...", end=" ")
        arxiv_results = self.search_arxiv(query, 15)
        print(f"+{len(arxiv_results)}")
        all_results.extend(arxiv_results)
        
        time.sleep(0.5)
        
        # OpenAlex 搜索
        print("  OpenAlex...", end=" ")
        openalex_results = self.search_openalex(query, 15)
        print(f"+{len(openalex_results)}")
        all_results.extend(openalex_results)
        
        time.sleep(0.5)
        
        # CrossRef 搜索
        print("  CrossRef...", end=" ")
        crossref_results = self.search_crossref(query, 10)
        print(f"+{len(crossref_results)}")
        all_results.extend(crossref_results)
        
        return all_results

def main():
    if len(sys.argv) < 2:
        print("用法: python academic_search.py <搜索关键词>")
        sys.exit(1)
    
    query = sys.argv[1]
    
    searcher = AcademicSearch()
    results = searcher.search_all(query)
    
    print(f"\n✅ 总计: {len(results)} 篇")
    
    # 去重并显示
    seen = set()
    unique = []
    for r in results:
        key = r.get("title", "")
        if key and key not in seen:
            seen.add(key)
            unique.append(r)
    
    print(f"去重后: {len(unique)} 篇\n")
    
    for i, p in enumerate(unique[:10], 1):
        print(f"{i}. {p['title'][:60]}...")
        print(f"   [{p['source']}] {p.get('year', '')} | {', '.join(p.get('authors', [])[:2])}")

if __name__ == "__main__":
    main()
