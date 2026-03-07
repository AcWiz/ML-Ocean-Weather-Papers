#!/usr/bin/env python3
"""
通用网页抓取工具
"""
import sys
import urllib.request
import urllib.parse
import re
from html import unescape

def fetch_url(url, text_only=True):
    """抓取网页"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode("utf-8", errors="ignore")
        
        if text_only:
            # 提取文本
            # 移除脚本和样式
            content = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
            content = re.sub(r'<style.*?</style>', '', content, flags=re.DOTALL)
            # 提取文本
            content = re.sub(r'<[^>]+>', ' ', content)
            # 解码HTML实体
            content = unescape(content)
            # 清理空白
            content = re.sub(r'\s+', ' ', content).strip()
        
        return content[:5000]  # 限制长度
    except Exception as e:
        return f"Error: {e}"

def main():
    if len(sys.argv) < 2:
        print("用法: python web_fetch.py <URL>")
        return
    
    url = sys.argv[1]
    if not url.startswith("http"):
        url = "https://" + url
    
    print(f"🌐 抓取: {url}")
    print("-" * 50)
    
    content = fetch_url(url)
    print(content[:2000])

if __name__ == "__main__":
    main()
