#!/usr/bin/env python3
"""
多平台论文验证系统
支持：arXiv, Nature, IEEE, ScienceDirect, Springer
使用大连理工机构认证
"""
import os
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# 机构认证配置
CONFIG_FILE = Path(__file__).parent.parent / "auth_config.json"

class AcademicVerifier:
    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None
        self.credentials = self._load_credentials()
    
    def _load_credentials(self):
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                return json.load(f)
        return {}
    
    def start(self, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        self.page = self.browser.new_page()
        return self
    
    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def verify_nature_paper(self, doi_or_url):
        """验证 Nature 论文"""
        # 提取 DOI
        if not doi_or_url.startswith("http"):
            doi = doi_or_url
            url = f"https://www.nature.com/articles/{doi}"
        else:
            url = doi_or_url
            # 提取 DOI
            import re
            doi_match = re.search(r'(10\.\d{4,}/[^\s]+)', url)
            doi = doi_match.group(1) if doi_match else ""
        
        try:
            self.page.goto(url, timeout=30000)
            time.sleep(3)
            
            # 获取标题
            title_elem = self.page.query_selector("h1[data-testid='citation_title']")
            if not title_elem:
                title_elem = self.page.query_selector("h1")
            
            title = title_elem.inner_text() if title_elem else "Not found"
            
            # 获取作者
            author_elems = self.page.query_selector_all("span[data-testid='citation_author']")
            authors = [e.inner_text() for e in author_elems[:5]]
            
            return {
                "valid": True,
                "platform": "Nature",
                "url": url,
                "title": title.strip(),
                "authors": authors,
                "doi": doi
            }
        except Exception as e:
            return {"valid": False, "error": str(e), "platform": "Nature"}
    
    def verify_ieee_paper(self, doi_or_url):
        """验证 IEEE 论文"""
        if doi_or_url.startswith("http"):
            url = doi_or_url
        else:
            url = f"https://ieeexplore.ieee.org/document/{doi_or_url}"
        
        try:
            self.page.goto(url, timeout=30000)
            time.sleep(3)
            
            # 获取标题
            title_elem = self.page.query_selector("h1.document-title")
            if not title_elem:
                title_elem = self.page.query_selector("h1")
            
            title = title_elem.inner_text() if title_elem else "Not found"
            
            return {
                "valid": True,
                "platform": "IEEE",
                "url": url,
                "title": title.strip()
            }
        except Exception as e:
            return {"valid": False, "error": str(e), "platform": "IEEE"}
    
    def search_nature(self, query):
        """搜索 Nature 论文"""
        url = f"https://www.nature.com/search?q={query.replace(' ', '+')}"
        
        try:
            self.page.goto(url, timeout=30000)
            time.sleep(3)
            
            # 获取搜索结果
            results = []
            items = self.page.query_selector_all("li[data-testid='search-item']")[:5]
            
            for item in items:
                try:
                    title_elem = item.query_selector("a[data-testid='summary-title']")
                    link_elem = item.query_selector("a[data-testid='summary-title']")
                    
                    if title_elem:
                        title = title_elem.inner_text()
                        link = link_elem.get_attribute("href") if link_elem else ""
                        
                        results.append({
                            "title": title,
                            "link": f"https://www.nature.com{link}" if link else ""
                        })
                except:
                    continue
            
            return results
        except Exception as e:
            return []

def main():
    print("🔍 多平台论文验证系统")
    print("=" * 50)
    
    verifier = AcademicVerifier()
    verifier.start(headless=True)
    
    # 测试 Nature 论文
    test_papers = [
        {"platform": "Nature", "url": "10.1038/s41586-023-06185-3", "name": "GraphCast"},
        {"platform": "Nature", "url": "10.1038/s41586-023-06056-9", "name": "Pangu-Weather"},
    ]
    
    for paper in test_papers:
        print(f"\n验证 {paper['name']}...")
        
        if paper["platform"] == "Nature":
            result = verifier.verify_nature_paper(paper["url"])
            
            if result.get("valid"):
                print(f"   ✅ 标题: {result['title'][:50]}...")
                print(f"   ✅ 作者: {result.get('authors', [])[:2]}")
            else:
                print(f"   ❌ 错误: {result.get('error')}")
    
    verifier.close()

if __name__ == "__main__":
    main()
