#!/usr/bin/env python3
"""
网页内容抓取模块
从任意网页提取内容
"""
from playwright.sync_api import sync_playwright
import re

class WebScraper:
    """网页内容抓取"""
    
    def __init__(self, headless=True):
        self.headless = headless
    
    def scrape(self, url, selectors=None):
        """
        抓取网页内容
        
        Args:
            url: 网页URL
            selectors: 自定义选择器 {name: selector}
        
        Returns:
            dict: 抓取的内容
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            try:
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                page.wait_for_timeout(3000)  # 等待 JS
                
                result = {"url": url, "title": page.title()}
                
                # 默认选择器
                default_selectors = {
                    "links": "a[href]",
                    "images": "img[src]",
                    "text": "p, h1, h2, h3, h4, h5, h6",
                }
                
                selectors = selectors or default_selectors
                
                for name, selector in selectors.items():
                    elements = page.query_selector_all(selector)
                    result[name] = []
                    for el in elements:
                        try:
                            if name == "links":
                                result[name].append({
                                    "text": el.inner_text().strip()[:50],
                                    "href": el.get_attribute("href")
                                })
                            elif name == "images":
                                result[name].append(el.get_attribute("src"))
                            else:
                                text = el.inner_text().strip()
                                if text:
                                    result[name].append(text)
                        except:
                            continue
                
                return result
                
            except Exception as e:
                return {"error": str(e)}
            finally:
                browser.close()
    
    def scrape_table(self, url, table_selector="table"):
        """抓取表格数据"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            try:
                page.goto(url, timeout=30000)
                page.wait_for_timeout(3000)
                
                table = page.query_selector(table_selector)
                if not table:
                    return {"error": "No table found"}
                
                # 提取表头
                headers = []
                header_cells = table.query_selector_all("thead th, thead td")
                for cell in header_cells:
                    headers.append(cell.inner_text().strip())
                
                # 提取数据行
                rows = []
                data_rows = table.query_selector_all("tbody tr")
                for row in data_rows:
                    cells = row.query_selector_all("td")
                    row_data = []
                    for cell in cells:
                        row_data.append(cell.inner_text().strip())
                    if row_data:
                        rows.append(row_data)
                
                return {"headers": headers, "rows": rows}
                
            finally:
                browser.close()

# 测试
if __name__ == "__main__":
    scraper = WebScraper()
    
    # 测试抓取
    print("🔍 测试网页抓取...")
    result = scraper.scrape("https://arxiv.org")
    
    print(f"标题: {result.get('title', 'N/A')}")
    print(f"链接数: {len(result.get('links', []))}")
