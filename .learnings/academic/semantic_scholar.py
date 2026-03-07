#!/usr/bin/env python3
"""
Semantic Scholar 学术论文搜索
"""
import sys
import urllib.request
import urllib.parse
import json

API_BASE = "https://api.semanticscholar.org/graph/v1"

def search_semantic(query, max_results=10):
    """搜索Semantic Scholar"""
    params = {
        "query": query,
        "limit": max_results,
        "fields": "title,authors,year,abstract,citationCount,venue,openAccessPdf"
    }
    
    url = f"{API_BASE}/paper/search?{urllib.parse.urlencode(params)}"
    
    headers = {"Accept": "application/json"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        
        papers = []
        for paper in data.get("data", []):
            papers.append({
                "title": paper.get("title", ""),
                "year": paper.get("year", ""),
                "authors": [a.get("name", "") for a in paper.get("authors", [])[:3]],
                "abstract": paper.get("abstract", "")[:300],
                "citations": paper.get("citationCount", 0),
                "venue": paper.get("venue", ""),
                "pdf": paper.get("openAccessPdf", {}).get("url", "") if paper.get("openAccessPdf") else ""
            })
        return papers
    except Exception as e:
        return [{"error": str(e)}]

def main():
    query = " ".join(sys.argv[1:]) or "data assimilation"
    print(f"🔍 搜索 Semantic Scholar: {query}")
    print("-" * 50)
    
    papers = search_semantic(query, 5)
    
    for i, p in enumerate(papers, 1):
        if "error" in p:
            print(f"错误: {p['error']}")
            continue
        print(f"\n{i}. {p['title']}")
        print(f"   📅 {p['year']} | 📚 {p['citations']} citations")
        print(f"   📍 {p['venue']}")
        if p['pdf']:
            print(f"   📄 {p['pdf']}")

if __name__ == "__main__":
    main()
