#!/usr/bin/env python3
"""
Semantic Scholar 搜索模块
带限流处理和缓存
"""
import requests
import time
import json
from pathlib import Path

class SemanticScholarSearch:
    """Semantic Scholar 搜索 - 带限流处理"""
    
    def __init__(self):
        self.api_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        self.cache_file = Path("~/.cache/semantic_scholar_cache.json").expanduser()
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.last_request_time = 0
        self.min_request_interval = 10  # 最小请求间隔（秒）
    
    def _load_cache(self):
        """加载缓存"""
        if self.cache_file.exists():
            with open(self.cache_file) as f:
                return json.load(f)
        return {}
    
    def _save_cache(self, cache):
        """保存缓存"""
        with open(self.cache_file, "w") as f:
            json.dump(cache, f)
    
    def search(self, query, max_results=20, use_cache=True):
        """搜索论文 - 带限流处理"""
        
        # 检查缓存
        if use_cache:
            cache = self._load_cache()
            if query in cache:
                cached_data = cache[query]
                # 缓存有效期 1 小时
                if time.time() - cached_data.get("timestamp", 0) < 3600:
                    print(f"   [缓存] 返回 {len(cached_data.get('papers', []))} 篇")
                    return cached_data.get("papers", [])[:max_results]
        
        # 限流等待
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < self.min_request_interval:
            wait = self.min_request_interval - elapsed
            print(f"   [限流] 等待 {wait:.1f}秒...")
            time.sleep(wait)
        
        params = {
            "query": query,
            "limit": max_results,
            "fields": "title,authors,year,venue,externalIds"
        }
        
        try:
            resp = requests.get(self.api_url, params=params, timeout=30)
            
            self.last_request_time = time.time()
            
            if resp.status_code == 200:
                data = resp.json()
                papers = data.get("data", [])
                
                # 保存到缓存
                if use_cache:
                    cache = self._load_cache()
                    cache[query] = {
                        "papers": papers,
                        "timestamp": time.time()
                    }
                    self._save_cache(cache)
                
                return papers
            
            elif resp.status_code == 429:
                print(f"   [限流] API 限流")
                return []
            else:
                print(f"   [错误] {resp.status_code}")
                return []
                
        except Exception as e:
            print(f"   [异常] {e}")
            return []
    
    def search_multiple(self, queries, max_per_query=15):
        """多查询搜索 - 自动限流"""
        all_papers = []
        
        for i, q in enumerate(queries):
            print(f"\n[{i+1}/{len(queries)}] {q}")
            papers = self.search(q, max_per_query)
            all_papers.extend(papers)
            
            # 查询间隔
            time.sleep(1)
        
        # 去重
        seen = set()
        unique = []
        for p in all_papers:
            key = p.get("title", "").lower()
            if key and key not in seen:
                seen.add(key)
                unique.append(p)
        
        return unique

if __name__ == "__main__":
    searcher = SemanticScholarSearch()
    
    print("🔍 Semantic Scholar 搜索测试...\n")
    
    queries = [
        "machine learning weather forecasting",
        "deep learning ocean",
    ]
    
    results = searcher.search_multiple(queries)
    
    print(f"\n✅ 总计: {len(results)} 篇去重论文")
    
    for i, p in enumerate(results[:10], 1):
        print(f"{i}. {p.get('title', '')[:50]}... ({p.get('year', '')})")
