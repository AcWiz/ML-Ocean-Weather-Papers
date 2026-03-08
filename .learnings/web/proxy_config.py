#!/usr/bin/env python3
"""
代理配置 - 自动检测并使用系统代理
"""
import os

def get_proxy():
    """自动获取代理配置"""
    # 检查环境变量
    proxy_addr = os.environ.get("proxy_addr", "")
    proxy_port = os.environ.get("proxy_port", "")
    
    if proxy_addr and proxy_port:
        return {
            "http": f"http://{proxy_addr}:{proxy_port}",
            "https": f"http://{proxy_addr}:{proxy_port}"
        }
    
    # 检查常见代理
    common_proxies = [
        "http://127.0.0.1:7890",
        "http://127.0.0.1:1080",
        "http://192.168.1.1:7890",
    ]
    
    for proxy in common_proxies:
        if check_proxy(proxy):
            return {"http": proxy, "https": proxy}
    
    return None

def check_proxy(proxy):
    """检查代理是否可用"""
    import urllib.request
    try:
        req = urllib.request.Request("https://www.google.com")
        req.set_proxy(proxy, "http")
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status == 200
    except:
        return False

def configure_proxy():
    """配置全局代理"""
    proxy = get_proxy()
    if proxy:
        os.environ["http_proxy"] = proxy["http"]
        os.environ["https_proxy"] = proxy["https"]
        print(f"✅ 代理已配置: {proxy['http']}")
    else:
        print("⚠️ 未检测到代理")
    return proxy

if __name__ == "__main__":
    configure_proxy()
