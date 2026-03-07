#!/usr/bin/env python3
"""
学术搜索统一入口
"""
import sys
import os

# 添加当前目录
sys.path.insert(0, os.path.dirname(__file__))

def main():
    if len(sys.argv) < 3:
        print("""
🔬 学术搜索工具 v1.0
========================
用法: python search.py <平台> <关键词>

平台:
  arxiv    - arXiv 预印本
  semantic - Semantic Scholar  
  pubmed   - PubMed 生物医学
  all      - 全部平台

示例:
  python search.py arxiv "machine learning"
  python search.py semantic "data assimilation"
  python search.py all "neural network"
""")
        return
    
    platform = sys.argv[1].lower()
    query = " ".join(sys.argv[2:])
    
    if platform == "arxiv" or platform == "all":
        print("\n" + "="*50)
        os.system(f"python3 {__file__}/arxiv_search.py {query}")
    
    if platform == "semantic" or platform == "all":
        print("\n" + "="*50)
        os.system(f"python3 {__file__}/semantic_scholar.py {query}")
    
    if platform == "pubmed" or platform == "all":
        print("\n" + "="*50)
        os.system(f"python3 {__file__}/scholar_search.py {query}")

if __name__ == "__main__":
    main()
