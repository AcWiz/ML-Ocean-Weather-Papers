#!/usr/bin/env python3
"""
学术论文下载工具
"""
import sys
import os
import urllib.request
import urllib.parse

DOWNLOAD_DIR = os.path.expanduser("~/papers/academic")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_pdf(url, filename):
    """下载PDF"""
    try:
        print(f"下载: {filename}")
        path = os.path.join(DOWNLOAD_DIR, filename)
        urllib.request.urlretrieve(url, path)
        print(f"✅ 保存至: {path}")
        return True
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False

def download_arxiv(paper_id):
    """下载arXiv论文"""
    pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
    filename = f"{paper_id}.pdf"
    return download_pdf(pdf_url, filename)

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python paper_downloader.py arxiv:<paper_id>")
        print("  python paper_downloader.py <pdf_url> <filename>")
        return
    
    arg = sys.argv[1]
    
    if arg.startswith("arxiv:"):
        paper_id = arg[6:]
        download_arxiv(paper_id)
    else:
        print("请提供arXiv ID或PDF URL")

if __name__ == "__main__":
    main()
