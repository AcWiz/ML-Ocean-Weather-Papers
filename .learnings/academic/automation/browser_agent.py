#!/usr/bin/env python3
"""
学术网站浏览器自动化
用于登录机构账户和下载付费论文
"""
import os
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, Page

# 配置
CONFIG_FILE = Path(__file__).parent.parent / "auth_config.json"
HEADLESS = True

class AcademicBrowser:
    """学术网站浏览器自动化"""
    
    def __init__(self):
        self.browser: Browser = None
        self.page: Page = None
        self.playwright = None
        self.credentials = self._load_credentials()
    
    def _load_credentials(self):
        """加载凭证"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                config = json.load(f)
                return {
                    "email": config.get("email", ""),
                    "institution": config.get("institution", "")
                }
        return {}
    
    def start(self):
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=HEADLESS,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        self.page = self.browser.new_page()
        print("✅ 浏览器已启动")
        return self
    
    def close(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("✅ 浏览器已关闭")
    
    def goto(self, url: str):
        """访问页面"""
        self.page.goto(url, wait_until="networkidle")
        return self
    
    def screenshot(self, name="screenshot"):
        """截图"""
        self.page.screenshot(path=f"/tmp/{name}.png")
        return self
    
    def login_ieee(self, email: str, password: str):
        """登录 IEEE"""
        self.goto("https://ieeexplore.ieee.org/")
        # 点击登录
        self.page.click("text=Sign in")
        self.page.wait_for_timeout(2000)
        
        # 选择机构登录
        self.page.click("text=Institution")
        self.page.wait_for_timeout(1000)
        
        # 输入邮箱
        self.page.fill("input[type='email']", email)
        self.page.click("button[type='submit']")
        self.page.wait_for_timeout(3000)
        
        print("✅ IEEE 登录流程完成")
        return self
    
    def login_sciencedirect(self, email: str, password: str):
        """登录 ScienceDirect"""
        self.goto("https://www.sciencedirect.com/")
        self.page.click("text=Sign in")
        self.page.wait_for_timeout(2000)
        
        # 选择机构
        self.page.click("text=Institutional")
        self.page.wait_for_timeout(1000)
        
        # 输入邮箱
        self.page.fill("#inputId", email)
        self.page.click("button[type='submit']")
        self.page.wait_for_timeout(3000)
        
        print("✅ ScienceDirect 登录流程完成")
        return self
    
    def download_paper(self, url: str, output_dir: str = "/tmp"):
        """下载论文"""
        self.goto(url)
        self.page.wait_for_timeout(3000)
        
        # 尝试下载 PDF
        try:
            # 点击 PDF 链接
            pdf_link = self.page.query_selector("a[href*='pdf']")
            if pdf_link:
                pdf_url = pdf_link.get_attribute("href")
                print(f"📄 PDF 链接: {pdf_url}")
            else:
                print("⚠️ 未找到 PDF 链接")
        except Exception as e:
            print(f"❌ 下载失败: {e}")
        
        return self
    
    def get_page_content(self) -> str:
        """获取页面内容"""
        return self.page.content()
    
    def evaluate(self, js: str):
        """执行 JavaScript"""
        return self.page.evaluate(js)

def demo():
    """演示"""
    print("🧪 学术浏览器自动化演示")
    
    browser = AcademicBrowser()
    browser.start()
    
    # 访问 Google 验证
    browser.goto("https://www.google.com")
    print(f"标题: {browser.page.title()}")
    
    # 截图
    browser.screenshot("test")
    print("📸 截图保存到 /tmp/test.png")
    
    browser.close()
    print("✅ 演示完成")

if __name__ == "__main__":
    demo()
