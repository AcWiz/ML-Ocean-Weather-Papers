#!/usr/bin/env python3
"""
每日学术简报生成器
自动追踪最新论文，生成每日摘要
"""
import json
import time
from datetime import datetime, timedelta

class DailyBriefing:
    """每日简报"""
    
    def __init__(self):
        self.topics = [
            "machine learning weather forecasting",
            "deep learning ocean",
            "neural network climate",
            "data assimilation neural"
        ]
    
    def generate(self):
        """生成每日简报"""
        print("📰 每日学术简报")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d')}")
        print("=" * 50)
        
        all_papers = []
        
        for topic in self.topics:
            papers = self._search_latest(topic, days=7)
            all_papers.extend(papers)
            time.sleep(0.5)
        
        # 去重
        unique = self._deduplicate(all_papers)
        
        print(f"\n📊 本周新增: {len(unique)} 篇相关论文\n")
        
        # 按主题分组显示
        self._display_by_topic(unique)
        
        return unique
    
    def _search_latest(self, topic, days=7):
        """搜索最新论文"""
        import requests
        
        url = "https://api.openalex.org/works"
        
        # 计算日期
        from datetime import datetime, timedelta
        date_from = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        params = {
            "search": topic,
            "filter": f"from_publication_date:{date_from}",
            "per_page": 10,
            "sort": "publication_date:desc"
        }
        
        try:
            resp = requests.get(url, params=params, timeout=15)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                
                papers = []
                for r in results:
                    papers.append({
                        "title": r.get("title", ""),
                        "year": r.get("publication_year"),
                        "date": r.get("publication_date", ""),
                        "cited": r.get("cited_by_count", 0),
                        "authors": [a.get("author", {}).get("display_name", "") 
                                   for a in r.get("authorships", [])[:2]],
                        "doi": r.get("doi", ""),
                        "topic": topic
                    })
                return papers
        except:
            pass
        
        return []
    
    def _deduplicate(self, papers):
        seen = set()
        unique = []
        for p in papers:
            key = p.get("title", "").lower()
            if key and key not in seen:
                seen.add(key)
                unique.append(p)
        return unique
    
    def _display_by_topic(self, papers):
        """按主题显示"""
        by_topic = {}
        
        for p in papers:
            topic = p.get("topic", "Other")
            if topic not in by_topic:
                by_topic[topic] = []
            by_topic[topic].append(p)
        
        for topic, ps in by_topic.items():
            print(f"\n🔹 {topic} ({len(ps)} 篇)")
            print("-" * 40)
            
            for p in ps[:5]:
                title = p.get("title", "")[:50]
                date = p.get("date", "")
                print(f"  • {title}... ({date})")

# 设置定时任务
CRON_SETUP = """
# 每日学术简报 - 每天早上8点
0 8 * * * python3 ~/.openclaw/workspace/.learnings/academic/daily_briefing.py >> ~/daily_academic_briefing.md 2>&1
"""

if __name__ == "__main__":
    briefing = DailyBriefing()
    papers = briefing.generate()
    
    # 保存
    output_file = Path("~/daily_academic_briefing.md").expanduser()
    with open(output_file, "w") as f:
        f.write(f"# 每日学术简报 - {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"本周新增: {len(papers)} 篇\n")
