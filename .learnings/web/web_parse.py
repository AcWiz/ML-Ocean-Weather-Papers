#!/usr/bin/env python3
"""
智能网页解析 - 提取标题、链接、内容
"""
import sys
import urllib.request
import re
from html import unescape

def parse_web(url):
    """解析网页结构"""
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode("utf-8", errors="ignore")
        
        result = {}
        
        # 标题
        title = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        result["title"] = unescape(title.group(1).strip()) if title else ""
        
        # Meta描述
        desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if not desc:
            desc = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', html, re.IGNORECASE)
        result["description"] = desc.group(1).strip() if desc else ""
        
        # 所有链接
        links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>', html)
        result["links"] = [{"url": l[0], "text": l[1].strip()} for l in links[:20] if l[0].startswith("http")]
        
        # 主要内容
        content = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
        content = re.sub(r'<style.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<[^>]+>', ' ', content)
        content = unescape(content)
        content = re.sub(r'\s+', ' ', content).strip()
        result["content"] = content[:3000]
        
        return result
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("用法: python web_parse.py <URL>")
        return
    
    url = sys.argv[1]
    if not url.startswith("http"):
        url = "https://" + url
    
    print(f"🔍 解析: {url}\n")
    
    result = parse_web(url)
    
    if "error" in result:
        print(f"错误: {result['error']}")
        return
    
    print(f"📄 标题: {result.get('title', 'N/A')}")
    print(f"\n📝 描述: {result.get('description', 'N/A')[:200]}...")
    print(f"\n🔗 链接 ({len(result.get('links', []))}个):")
    for link in result.get('links', [])[:5]:
        print(f"  - {link['text'][:30]}: {link['url'][:50]}")
    print(f"\n📄 内容预览:\n{result.get('content', '')[:500]}...")

if __name__ == "__main__":
    main()
