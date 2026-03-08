#!/usr/bin/env python3
"""
机构认证系统
用于下载付费学术资源
"""
import os
import json
from pathlib import Path

CONFIG_FILE = os.path.expanduser("~/.openclaw/workspace/.learnings/academic/auth_config.json")

class InstitutionalAuth:
    def __init__(self):
        self.credentials = self._load_config()
    
    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                return json.load(f)
        return {}
    
    def _save_config(self):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        # 只保存标识，不保存密码
        config = {
            "configured": True,
            "institution": self.credentials.get("institution", ""),
            "email": self.credentials.get("email", ""),
            "has_proxy": self.credentials.get("has_proxy", False)
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    
    def configure(self, institution, email, proxy_url="", password=""):
        """配置机构信息"""
        # 密码不保存，只在内存中使用
        self.credentials = {
            "institution": institution,
            "email": email,
            "proxy_url": proxy_url,
            "has_proxy": bool(proxy_url)
        }
        self._save_config()
        print(f"✅ 机构认证已配置: {institution}")
        print(f"   邮箱: {email}")
        if proxy_url:
            print(f"   代理: {proxy_url}")
    
    def get_auth(self):
        """获取认证信息"""
        return self.credentials
    
    def has_auth(self):
        """检查是否已配置"""
        return bool(self.credentials.get("institution"))

def main():
    auth = InstitutionalAuth()
    
    if auth.has_auth():
        creds = auth.get_auth()
        print(f"已配置机构: {creds.get('institution')}")
        print(f"邮箱: {creds.get('email')}")
    else:
        print("""
🔐 机构认证配置
================
请提供以下信息来配置机构认证:

1. 机构名称 (如: 清华大学)
2. 邮箱 (机构邮箱)
3. 代理地址 (可选，如: http://127.0.0.1:7890)
4. 密码 (仅内存使用，不保存)

使用方式:
  python institutional_auth.py config "机构名" "邮箱" "代理" "密码"
""")

if __name__ == "__main__":
    main()
