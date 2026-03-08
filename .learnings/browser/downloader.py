#!/usr/bin/env python3
"""
文件下载模块
自动下载文件并保存
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import time
import os

class FileDownloader:
    """文件下载器"""
    
    def __init__(self, download_dir="/tmp/downloads"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
    
    def download(self, url, filename=None, wait_time=10):
        """
        下载文件
        
        Args:
            url: 下载链接
            filename: 保存文件名（可选）
            wait_time: 等待下载完成的时间
        
        Returns:
            str: 下载文件路径
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                accept_downloads=True
            )
            page = context.new_page()
            
            # 监听下载事件
            download_path = [None]
            
            def handle_download(download):
                filename = filename or download.suggested_filename
                path = self.download_dir / filename
                # 保存文件
                download.save_as(str(path))
                download_path[0] = str(path)
            
            page.on("download", handle_download)
            
            try:
                # 访问下载页面
                page.goto(url, wait_until="domcontentloaded")
                
                # 触发下载（可能需要点击按钮）
                page.wait_for_timeout(wait_time * 1000)
                
                return download_path[0]
                
            finally:
                browser.close()
    
    def download_multiple(self, urls):
        """批量下载"""
        results = []
        for url in urls:
            print(f"下载: {url}")
            path = self.download(url)
            results.append({"url": url, "path": path})
        return results

# PDF 下载特定功能
class PDFDownloader(FileDownloader):
    """PDF 下载器"""
    
    def download_pdf(self, url, filename=None):
        """下载 PDF"""
        # 如果URL是直接的PDF链接
        if url.endswith('.pdf'):
            return self.download(url, filename)
        
        # 否则尝试从页面中查找PDF链接
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.goto(url, wait_until="domcontentloaded")
            
            # 查找 PDF 链接
            pdf_links = page.query_selector_all("a[href$='.pdf']")
            
            if pdf_links:
                pdf_url = pdf_links[0].get_attribute("href")
                browser.close()
                return self.download(pdf_url, filename)
            
            browser.close()
            return None

if __name__ == "__main__":
    downloader = FileDownloader()
    
    # 测试
    print("🔧 文件下载测试")
