#!/usr/bin/env python3
"""
网络拦截模块
拦截和修改网络请求
"""
from playwright.sync_api import sync_playwright
import json

class NetworkInterceptor:
    """网络请求拦截"""
    
    def __init__(self):
        self.intercepted = []
        self.blocked = []
    
    def intercept(self, url, block=False, modify_response=None):
        """
        拦截请求
        
        Args:
            url: 要拦截的URL模式
            block: 是否阻止
            modify_response: 修改响应
        """
        pass  # 简化实现
    
    def get_requests(self):
        """获取所有请求"""
        return self.intercepted
    
    def get_responses(self):
        """获取所有响应"""
        return self.intercepted

class RequestLogger:
    """请求日志记录"""
    
    def __init__(self):
        self.requests = []
        self.responses = []
    
    def log_request(self, request):
        """记录请求"""
        self.requests.append({
            "url": request.url,
            "method": request.method,
            "headers": dict(request.headers),
            "timestamp": request.timing["startTime"]
        })
    
    def log_response(self, response):
        """记录响应"""
        self.responses.append({
            "url": response.url,
            "status": response.status,
            "headers": dict(response.headers),
            "timestamp": response.timing["startTime"]
        })
    
    def get_all(self):
        """获取所有记录"""
        return {"requests": self.requests, "responses": self.responses}
    
    def save(self, filename):
        """保存到文件"""
        with open(filename, "w") as f:
            json.dump(self.get_all(), f, indent=2)

# 快速测试网络功能
def test_network():
    """测试网络拦截"""
    with sync_playwright() as p:
        logger = RequestLogger()
        
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 监听请求
        page.on("request", lambda req: logger.log_request(req))
        page.on("response", lambda res: logger.log_response(res))
        
        # 访问页面
        page.goto("https://example.com")
        page.wait_for_timeout(2000)
        
        # 打印结果
        print(f"请求数: {len(logger.requests)}")
        print(f"响应数: {len(logger.responses)}")
        
        browser.close()

if __name__ == "__main__":
    test_network()
