#!/usr/bin/env python3
"""
网页深度内容提取 - 提取文章、论文主要内容
"""
import sys
import urllib.request
import re
from html import unescape

def extract_article(url):
    """提取文章主要内容"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode("utf-8", errors="ignore")
        
        # 提取标题
        title = ""
        for pattern in [r'<title>(.*?)</title>', r'<h1[^>]*>(.*?)</h1>']:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match:
                title = unescape(match.group(1).strip())
                break
        
        # 移除不需要的元素
        html = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style.*?</style>', '', html, flags=re.DOTALL)
        html = re.sub(r'<nav.*?</nav>', '', html, flags=re.DOTALL)
        html = re.sub(r'<header.*?</header>', '', html, flags=re.DOTALL)
        html = re.sub(r'<footer.*?</footer>', '', html, flags=re.DOTALL)
        html = re.sub(r'<aside.*?</aside>', '', html, flags=re.DOTALL)
        
        # 提取段落
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        
        # 清理段落
        content = []
        for p in paragraphs:
            # 移除HTML标签
            text = re.sub(r'<[^>]+>', '', p)
            text = unescape(text)
            text = re.sub(r'\s+', ' ', text).strip()
            # 过滤短文本
            if len(text) > 50:
                content.append(text)
        
        return {
            "title": title,
            "content": content[:20],  # 最多20段
            "url": url
        }
    except Exception as e:
        return {"error": str(e), "url": url}

def main():
    if len(sys.argv) < 2:
        print("用法: python content_extractor.py <URL>")
        return
    
    url = sys.argv[1]
    if not url.startswith("http"):
        url = "https://" + url
    
    print(f"📄 提取: {url}\n")
    
    result = extract_article(url)
    
    if "error" in result:
        print(f"错误: {result['error']}")
        return
    
    print(f"标题: {result['title']}\n")
    print("内容:")
    for i, p in enumerate(result.get("content", []), 1):
        print(f"\n{i}. {p[:200]}...")

if __name__ == "__main__":
    main()
