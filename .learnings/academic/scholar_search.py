#!/usr/bin/env python3
"""
通用学术搜索 - 聚合多个来源
"""
import sys
import urllib.request
import urllib.parse
import re

def search_google_scholar(query):
    """搜索Google Scholar（简化版）"""
    # 注意：Google Scholar有反爬虫，这里是概念展示
    return [{"note": "需要设置代理或使用第三方API"}]

def search_pubmed(query, max_results=5):
    """搜索PubMed生物医学文献"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "sort": "relevance"
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            content = response.read().decode("utf-8")
        
        # 提取PMID
        ids = re.findall(r'<Id>(\d+)</Id>', content)
        
        # 获取详情
        if ids:
            fetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={','.join(ids)}"
            with urllib.request.urlopen(fetch_url, timeout=30) as response:
                summary = response.read().decode("utf-8")
            
            papers = []
            for id in ids:
                title = re.search(f'<Item Name="Title" Type="String">(.*?)</Item>', summary)
                authors = re.search(f'<Item Name="Authors" Type="String">(.*?)</Item>', summary)
                pubdate = re.search(f'<Item Name="PubDate" Type="String">(.*?)</Item>', summary)
                
                if title:
                    papers.append({
                        "id": id,
                        "title": title.group(1) if title else "",
                        "authors": authors.group(1)[:100] if authors else "",
                        "pubdate": pubdate.group(1) if pubdate else ""
                    })
            return papers
    except Exception as e:
        return [{"error": str(e)}]
    
    return []

def search_ieee(query, max_results=5):
    """搜索IEEE Xplore"""
    # IEEE需要API key，这里返回说明
    return [{"note": "需要IEEE Xplore API key"}]

def main():
    query = " ".join(sys.argv[1:]) or "neural network"
    print(f"🔍 学术搜索: {query}")
    print("=" * 50)
    
    # PubMed
    print("\n📚 PubMed 结果:")
    papers = search_pubmed(query, 3)
    for i, p in enumerate(papers, 1):
        if "error" in p:
            print(f"  错误: {p['error']}")
        else:
            print(f"  {i}. {p.get('title', '')[:60]}")
            print(f"     PMID: {p.get('id', '')}")
    
    print("\n📝 IEEE Xplore:")
    print("  需要API key")
    
    print("\n🔍 Google Scholar:")
    print("  需要代理或第三方API")

if __name__ == "__main__":
    main()
