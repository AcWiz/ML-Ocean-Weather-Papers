"""
浏览器自动化模块

功能:
- automator: 核心浏览器自动化
- scraper: 网页内容抓取
- downloader: 文件下载
- network: 网络拦截

快速使用:
    from browser import create_browser
    browser = create_browser()
    browser.goto("https://example.com")
    browser.close()
"""

from .automator import BrowserAutomator, create_browser
from .scraper import WebScraper
from .downloader import FileDownloader, PDFDownloader

__all__ = ['BrowserAutomator', 'create_browser', 'WebScraper', 'FileDownloader', 'PDFDownloader']
