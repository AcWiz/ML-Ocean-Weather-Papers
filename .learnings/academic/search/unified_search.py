#!/usr/bin/env python3
"""
统一学术搜索系统
整合所有可用资源
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from arxiv_search import ArxivSearch
from openalex_search import OpenAlexSearch
from ieee_search import IEEESearch

class UnifiedAcademicSearch:
    """统一学术搜索"""
    
    def __init__(self):
        self.arxiv = ArxivSearch()
        self.openalex = OpenAlexSearch()
        self.ieee = IEEESearch()
        self.results = []
    
    def search(self, query, max_per_source=15):
        """多平台综合搜索"""
        print(f"\n🔍 统一搜索: {query}")
        print("=" * 60)
        
        all_results = []
        
        # 1. arXiv
        print("  📚 arXiv...", end=" ", flush=True)
        try:
            arxiv_results = self.arxiv.search(query, max_per_source)
            print(f"+{len(arxiv_results)}")
            all_results.extend(arxiv_results)
        except Exception as e:
            print(f"❌ {e}")
        
        time.sleep(0.5)
        
        # 2. OpenAlex
        print("  🌐 OpenAlex...", end=" ", flush=True)
        try:
            openalex_results = self.openalex.search(query, max_per_source)
            print(f"+{len(openalex_results)}")
            all_results.extend(openalex_results)
        except Exception as e:
            print(f"❌ {e}")
        
        time.sleep(0.5)
        
        # 3. IEEE
        print("  📡 IEEE...", end=" ", flush=True)
        try:
            ieee_results = self.ieee.search(query, max_per_source)
            print(f"+{len(ieee_results)}")
            all_results.extend(ieee_results)
        except Exception as e:
            print(f"❌ {e}")
        
        # 4. CrossRef
        print("  📖 CrossRef...", end=" ", flush=True)
        try:
            from comprehensive_search import ComprehensiveSearch
            cs = ComprehensiveSearch()
            crossref_results = cs._search_crossref(query, max_per_source)
            print(f"+{len(crossref_results)}")
            all_results.extend(crossref_results)
        except Exception as e:
            print(f"❌ {e}")
        
        # 去重
        unique = self._deduplicate(all_results)
        
        print(f"\n✅ 总计: {len(unique)} 篇去重论文")
        
        return unique
    
    def _deduplicate(self, papers):
        seen = set()
        unique = []
        
        for p in papers:
            key = p.get("title", "").lower().strip()
            if key and key not in seen:
                seen.add(key)
                unique.append(p)
        
        return unique

if __name__ == "__main__":
    import sys
    
    query = sys.argv[1] if len(sys.argv) > 1 else "machine learning weather"
    
    searcher = UnifiedAcademicSearch()
    results = searcher.search(query)
    
    print("\n📊 前10篇论文:")
    for i, r in enumerate(results[:10], 1):
        title = r.get("title", "")[:55]
        source = r.get("source", "Unknown")
        year = r.get("year", "")
        
        print(f"\n{i}. {title}...")
        print(f"   [{source}] {year}")
        
        if r.get("url"):
            print(f"   🔗 {r['url'][:55]}...")
