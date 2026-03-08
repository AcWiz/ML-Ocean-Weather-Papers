#!/usr/bin/env python3
"""
浏览器自动化核心模块
功能：反检测浏览、智能等待、网络拦截、文件下载等
"""
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
import time
import os
from pathlib import Path

class BrowserAutomator:
    """浏览器自动化核心类"""
    
    def __init__(self, headless=True):
        self.headless = headless
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.playwright = None
    
    def launch(self, stealth=True):
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        
        # 启动参数
        args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-blink-features=AutomationControlled',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-gpu',
        ]
        
        if stealth:
            args.extend([
                '--disable-accelerated-2d-canvas',
                '--disable-software-rasterizer',
                '--disable-extensions',
                '--disable-background-networking',
                '--disable-sync',
                '--disable-translate',
                '--metrics-recording-only',
                '--mute-audio',
                '--no-first-run',
            ])
        
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=args
        )
        
        # 创建 context
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
        )
        
        # 反检测脚本
        if stealth:
            self.context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                window.chrome = { runtime: {} };
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            """)
        
        self.page = self.context.new_page()
        
        return self
    
    def goto(self, url, wait_until="domcontentloaded", timeout=30000):
        """访问页面"""
        response = self.page.goto(url, wait_until=wait_until, timeout=timeout)
        time.sleep(2)  # 等待 JS 执行
        return response
    
    def screenshot(self, name="screenshot", full_page=False):
        """截图"""
        output_dir = Path("/tmp/browser")
        output_dir.mkdir(exist_ok=True)
        path = output_dir / f"{name}.png"
        self.page.screenshot(path=str(path), full_page=full_page)
        return str(path)
    
    def click(self, selector, timeout=5000):
        """点击元素"""
        self.page.click(selector, timeout=timeout)
    
    def fill(self, selector, text):
        """填写表单"""
        self.page.fill(selector, text)
    
    def wait_for_selector(self, selector, timeout=10000):
        """等待元素出现"""
        return self.page.wait_for_selector(selector, timeout=timeout)
    
    def wait_for_load(self, timeout=10000):
        """等待页面加载"""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def download_file(self, url, output_path):
        """下载文件"""
        self.page.goto(url)
        # 等待下载完成
        self.page.wait_for_timeout(3000)
    
    def get_cookies(self):
        """获取 cookies"""
        return self.context.cookies()
    
    def set_cookies(self, cookies):
        """设置 cookies"""
        self.context.add_cookies(cookies)
    
    def close(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

# 便捷函数
def create_browser(headless=True):
    """创建浏览器实例"""
    bot = BrowserAutomator(headless=headless)
    bot.launch()
    return bot

# 测试
if __name__ == "__main__":
    print("🔧 浏览器自动化测试...")
    
    bot = create_browser(headless=True)
    
    # 测试访问
    print("访问 Google...")
    bot.goto("https://www.google.com")
    print(f"标题: {bot.page.title()}")
    
    # 截图
    path = bot.screenshot("test")
    print(f"截图保存: {path}")
    
    bot.close()
    print("✅ 测试完成")
