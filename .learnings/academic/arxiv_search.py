#!/usr/bin/env python3
"""
arXiv 学术论文搜索
"""
import sys
import urllib.request
import urllib.parse
import json
import re

def search_arxiv(query, max_results=10):
    """搜索arXiv论文"""
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            content = response.read().decode("utf-8")
        
        # 解析XML
        papers = []
        entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
        
        for entry in entries:
            title = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
            summary = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
            published = re.search(r'<published>(.*?)</published>', entry)
            pdf = re.search(r'<link title="pdf" href="(.*?)"', entry)
            authors = re.findall(r'<name>(.*?)</name>', entry)
            
            if title:
                papers.append({
                    "title": title.group(1).replace("\n", " "),
                    "summary": summary.group(1).replace("\n", " ")[:300] if summary else "",
                    "published": published.group(1)[:10] if published else "",
                    "pdf": pdf.group(1) if pdf else "",
                    "authors": authors[:3]
                })
        
        return papers
    except Exception as e:
        return [{"error": str(e)}]

def main():
    query = " ".join(sys.argv[1:]) or "machine learning"
    print(f"🔍 搜索 arXiv: {query}")
    print("-" * 50)
    
    papers = search_arxiv(query, 5)
    
    for i, p in enumerate(papers, 1):
        if "error" in p:
            print(f"错误: {p['error']}")
            continue
        print(f"\n{i}. {p['title']}")
        print(f"   📅 {p['published']}")
        print(f"   📄 {p['pdf']}")
        print(f"   👥 {', '.join(p['authors'])}")
        print(f"   📝 {p['summary'][:150]}...")

if __name__ == "__main__":
    main()
