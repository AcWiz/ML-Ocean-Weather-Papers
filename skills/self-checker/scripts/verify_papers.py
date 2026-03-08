#!/usr/bin/env python3
"""
论文信息验证脚本
用于验证论文标题、作者、链接是否正确
"""
import requests
import re
import sys
import json

PROXIES = {"http": "http://192.168.74.1:7890", "https": "http://192.168.74.1:7890"}

def verify_arxiv(arxiv_id):
    """验证 arXiv 论文"""
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    try:
        resp = requests.get(url, proxies=PROXIES, timeout=15)
        
        # 解析
        entry = re.search(r'<entry>(.*?)</entry>', resp.text, re.DOTALL)
        if not entry:
            return {"valid": False, "error": "Not found"}
        
        e = entry.group(1)
        
        title = re.search(r'<title>([^<]+)</title>', e)
        authors = re.findall(r'<name>([^<]+)</name>', e)[:3]
        published = re.search(r'<published>([^<]+)</published>', e)
        
        return {
            "valid": True,
            "arxiv_id": arxiv_id,
            "title": title.group(1).strip() if title else "",
            "authors": authors,
            "year": published.group(1)[:4] if published else "",
            "link": f"https://arxiv.org/abs/{arxiv_id}"
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}

def verify_nature(doi_or_url):
    """验证 Nature 论文（简化版）"""
    # 提取 DOI
    doi_match = re.search(r'(10\.\d{4,}/[^\s]+)', doi_or_url)
    if doi_match:
        doi = doi_match.group(1)
        url = f"https://api.crossref.org/works/{doi}"
        try:
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                item = data.get("message", {})
                return {
                    "valid": True,
                    "title": item.get("title", [""])[0],
                    "authors": [a.get("family", "") for a in item.get("author", [])[:3]],
                    "year": str(item.get("published-print", {}).get("date-parts", [[0]])[0][0]),
                    "journal": item.get("container-title", [""])[0]
                }
        except:
            pass
    return {"valid": False, "error": "Cannot verify"}

def verify_batch(papers):
    """批量验证论文"""
    results = []
    
    for p in papers:
        arxiv_id = p.get("arxiv_id", "")
        doi = p.get("doi", "")
        
        if arxiv_id:
            result = verify_arxiv(arxiv_id)
            result["expected_title"] = p.get("title", "")
            results.append(result)
        elif doi:
            result = verify_nature(doi)
            results.append(result)
        else:
            results.append({"valid": False, "error": "No ID provided"})
    
    return results

if __name__ == "__main__":
    # 测试
    test_papers = [
        {"arxiv_id": "2305.00080"},
        {"arxiv_id": "2212.12794"},
        {"arxiv_id": "2208.05419"}
    ]
    
    print("🔍 验证测试...")
    for result in verify_batch(test_papers):
        print(f"\n{'✅' if result['valid'] else '❌'} {result.get('arxiv_id', result.get('error'))}")
        if result.get('title'):
            print(f"   标题: {result['title'][:50]}...")
        if result.get('authors'):
            print(f"   作者: {', '.join(result['authors'])}")
