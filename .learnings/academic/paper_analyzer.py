#!/usr/bin/env python3
"""
论文影响力分析器
分析引用网络、作者影响力、领域趋势
"""
import requests
import json

class PaperAnalyzer:
    """论文分析器"""
    
    def __init__(self):
        self.cache_file = "~/.openclaw/workspace/.learnings/academic/analyzer_cache.json"
    
    def analyze_paper(self, title):
        """分析单篇论文"""
        # 获取论文信息
        paper_info = self._get_paper_info(title)
        
        if not paper_info:
            return None
        
        # 分析影响力
        analysis = {
            "title": paper_info.get("title"),
            "year": paper_info.get("year"),
            "citations": paper_info.get("cited_by_count", 0),
            "influence_score": self._calc_influence(paper_info),
            "authors": paper_info.get("authors", []),
            "venue": paper_info.get("venue", ""),
            "topics": self._extract_topics(paper_info)
        }
        
        return analysis
    
    def _get_paper_info(self, title):
        """获取论文信息"""
        # 尝试 OpenAlex
        url = "https://api.openalex.org/works"
        params = {"search": title, "per_page": 1}
        
        try:
            resp = requests.get(url, params=params, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                if results:
                    r = results[0]
                    return {
                        "title": r.get("title", ""),
                        "year": r.get("publication_year"),
                        "cited_by_count": r.get("cited_by_count", 0),
                        "authors": [a.get("author", {}).get("display_name", "") 
                                  for a in r.get("authorships", [])[:5]],
                        "venue": r.get("primary_location", {}).get("source", {}).get("display_name", ""),
                        "doi": r.get("doi", "")
                    }
        except:
            pass
        
        return None
    
    def _calc_influence(self, paper):
        """计算影响力分数"""
        citations = paper.get("cited_by_count", 0)
        year = paper.get("year", 2020)
        
        # 基础分数
        score = min(citations / 100, 100)  # 最多100分
        
        # 年份加成（越新越有价值）
        import datetime
        years_old = datetime.datetime.now().year - year
        if years_old < 2:
            score *= 1.5
        elif years_old < 5:
            score *= 1.2
        
        return round(score, 1)
    
    def _extract_topics(self, paper):
        """提取主题"""
        # 简单关键词提取
        title = paper.get("title", "").lower()
        topics = []
        
        topic_keywords = {
            "Weather Forecasting": ["weather", "forecast", "precipitation"],
            "Ocean": ["ocean", "sea", "marine"],
            "Deep Learning": ["deep learning", "neural", "transformer"],
            "Data Assimilation": ["assimilation", "reanalysis"],
            "Climate": ["climate", "gcm", "circulation"]
        }
        
        for topic, kws in topic_keywords.items():
            if any(k in title for k in kws):
                topics.append(topic)
        
        return topics if topics else ["Other"]
    
    def generate_trend_report(self, papers):
        """生成趋势报告"""
        # 按年份统计
        year_counts = {}
        topic_counts = {}
        
        for p in papers:
            year = p.get("year", 0)
            if year:
                year_counts[year] = year_counts.get(year, 0) + 1
            
            for topic in p.get("topics", []):
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        return {
            "year_distribution": year_counts,
            "topic_distribution": topic_counts
        }

if __name__ == "__main__":
    analyzer = PaperAnalyzer()
    
    # 测试
    test_papers = [
        "GraphCast weather forecasting",
        "Pangu-Weather",
        "FourCastNet"
    ]
    
    print("📊 论文影响力分析")
    print("=" * 50)
    
    for title in test_papers:
        result = analyzer.analyze_paper(title)
        if result:
            print(f"\n📄 {result['title'][:40]}...")
            print(f"   年份: {result['year']}")
            print(f"   引用: {result['citations']}")
            print(f"   影响力: {result['influence_score']}")
            print(f"   主题: {', '.join(result['topics'])}")
