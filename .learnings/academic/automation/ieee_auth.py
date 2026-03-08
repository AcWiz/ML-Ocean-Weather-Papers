#!/usr/bin/env python3
"""
IEEE 机构认证系统
使用大连理工账号进行机构登录
"""
import os
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

# 配置
CONFIG_FILE = Path(__file__).parent.parent / "auth_config.json"

class IEEEAuth:
    """IEEE 机构认证"""
    
    def __init__(self):
        self.credentials = self._load_credentials()
        self.browser = None
        self.page = None
        self.playwright = None
    
    def _load_credentials(self):
        """加载凭证"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                return json.load(f)
        return {}
    
    def start_browser(self):
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False,  # 需要手动操作
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ]
        )
        self.page = self.browser.new_page()
        return self
    
    def login_via_institution(self):
        """通过机构登录"""
        if not self.credentials.get("email"):
            print("❌ 未配置机构邮箱")
            return False
        
        email = self.credentials.get("email", "")
        password = self.credentials.get("password", "")
        
        print(f"🔐 尝试机构登录: {email}")
        
        # 访问 IEEE
        self.page.goto("https://ieeexplore.ieee.org/", timeout=30000)
        time.sleep(3)
        
        # 点击 Sign in
        try:
            sign_in = self.page.query_selector("text=Sign in")
            if sign_in:
                sign_in.click()
                time.sleep(2)
        except:
            pass
        
        # 点击 Institution
        try:
            inst = self.page.query_selector("text=Institution")
            if inst:
                inst.click()
                time.sleep(2)
        except:
            pass
        
        # 输入邮箱
        try:
            email_input = self.page.query_selector("input[type='email']")
            if email_input:
                email_input.fill(email)
                print("✅ 已输入邮箱")
        except:
            print("⚠️ 无法找到邮箱输入框")
        
        return True
    
    def search_ieee(self, query):
        """搜索 IEEE 论文"""
        if not self.browser:
            self.start_browser()
        
        self.page.goto("https://ieeexplore.ieee.org/", timeout=30000)
        time.sleep(3)
        
        # 搜索
        try:
            search_box = self.page.query_selector("input[placeholder*='Search']")
            if search_box:
                search_box.fill(query)
                self.page.keyboard.press("Enter")
                time.sleep(5)
                
                # 获取结果
                results = self.page.query_selector_all("div[data-testid='result-item']")
                print(f"找到 {len(results)} 个结果")
                return results
        except Exception as e:
            print(f"搜索错误: {e}")
        
        return []
    
    def close(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

# 备用方案：通过 API
class IEEERestAPI:
    """IEEE Xplore REST API"""
    
    def __init__(self):
        self.api_key = None  # 需要申请 API key
    
    def search(self, query, max_results=10):
        """搜索论文"""
        # IEEE Xplore 需要 API key
        # 可以通过机构账户申请
        pass

def main():
    import sys
    
    auth = IEEEAuth()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "login":
            auth.start_browser()
            auth.login_via_institution()
            print("按 Enter 关闭浏览器...")
            input()
            auth.close()
        elif sys.argv[1] == "search":
            query = sys.argv[2] if len(sys.argv) > 2 else "machine learning"
            auth.start_browser()
            results = auth.search_ieee(query)
            print(f"找到 {len(results)} 篇论文")
            auth.close()
    else:
        print("用法:")
        print("  python ieee_auth.py login    # 登录 IEEE")
        print("  python ieee_auth.py search <关键词>  # 搜索")

if __name__ == "__main__":
    main()
