#!/usr/bin/env python3
"""
学术搜索 - 整合多个来源
"""
import sys
import os
import urllib.request
import urllib.parse
import re

# 配置代理
proxy_addr = os.environ.get("proxy_addr", "")
proxy_port = os.environ.get("proxy_port", "")

if proxy_addr and proxy_port:
    proxy_handler = urllib.request.ProxyHandler({
        'http': f'http://{proxy_addr}:{proxy_port}',
        'https': f'http://{proxy_addr}:{proxy_port}'
    })
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)

def search_arxiv_direct(query, num_results=10):
    """直接搜索arXiv API"""
    url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&max_results={num_results}&sortBy=submittedDate&sortOrder=descending"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            content = response.read().decode("utf-8")
        
        papers = []
        entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
        
        for entry in entries:
            title = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
            summary = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
            published = re.search(r'<published>(.*?)</published>', entry)
            pdf = re.search(r'<link title="pdf" href="(.*?)"', entry)
            
            if title:
                papers.append({
                    "source": "arXiv",
                    "title": title.group(1).replace("\n", " ").strip(),
                    "published": published.group(1)[:10] if published else "",
                    "pdf": pdf.group(1) if pdf else "",
                    "abstract": summary.group(1).replace("\n", " ")[:150] if summary else ""
                })
        return papers
    except Exception as e:
        return [{"error": str(e)}]

def search_semanticscholar(query, num_results=10):
    """搜索Semantic Scholar API"""
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(query)}&limit={num_results}&fields=title,authors,year,venue,url"
    
    headers = {"Accept": "application/json"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        
        papers = []
        for p in data.get("data", []):
            papers.append({
                "source": "Semantic Scholar",
                "title": p.get("title", ""),
                "year": p.get("year", ""),
                "venue": p.get("venue", ""),
                "url": p.get("url", ""),
                "authors": [a.get("name", "") for a in p.get("authors", [])[:3]]
            })
        return papers
    except Exception as e:
        return [{"error": str(e)}]

import json

def main():
    query = " ".join(sys.argv[1:]) or "data assimilation ocean"
    print(f"🔍 学术搜索: {query}")
    print("=" * 50)
    
    # 1. arXiv搜索
    print("\n📚 arXiv 预印本:")
    papers = search_arxiv_direct(query, 5)
    if papers and "error" not in papers[0]:
        for i, p in enumerate(papers, 1):
            print(f"  {i}. {p['title'][:60]}")
            print(f"     📅 {p['published']} | 📄 {p['pdf'][:50] if p['pdf'] else 'N/A'}")
    else:
        print(f"  错误: {papers[0].get('error', '未知')}")
    
    # 2. Semantic Scholar
    print("\n📚 Semantic Scholar:")
    papers = search_semanticscholar(query, 5)
    if papers and "error" not in papers[0]:
        for i, p in enumerate(papers, 1):
            print(f"  {i}. {p['title'][:60]}")
            print(f"     📅 {p['year']} | 📍 {p.get('venue', 'N/A')}")

if __name__ == "__main__":
    main()
