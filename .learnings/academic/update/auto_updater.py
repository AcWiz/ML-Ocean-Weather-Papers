#!/usr/bin/env python3
"""
学术论文自动更新系统
定期获取最新论文
"""
import json
import time
import os
from datetime import datetime
from pathlib import Path

class AutoUpdater:
    """自动更新论文库"""
    
    def __init__(self, data_dir=None):
        self.data_dir = data_dir or Path("~/.openclaw/workspace/academic_data").expanduser()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.papers_file = self.data_dir / "papers.json"
        self.history_file = self.data_dir / "history.json"
    
    def load_papers(self):
        """加载现有论文"""
        if self.papers_file.exists():
            with open(self.papers_file) as f:
                return json.load(f)
        return {"papers": [], "updated": ""}
    
    def save_papers(self, papers):
        """保存论文"""
        data = {
            "papers": papers,
            "updated": datetime.now().isoformat()
        }
        with open(self.papers_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def add_papers(self, new_papers):
        """添加新论文"""
        data = self.load_papers()
        existing = {p.get("title", "").lower() for p in data["papers"]}
        
        added = 0
        for p in new_papers:
            if p.get("title", "").lower() not in existing:
                data["papers"].append(p)
                added += 1
        
        data["updated"] = datetime.now().isoformat()
        self.save_papers(data["papers"])
        
        return added
    
    def get_latest(self, days=7):
        """获取最近更新的论文"""
        data = self.load_papers()
        # 按日期排序
        # 返回最新论文
        return data["papers"][:50]

# Cron 任务示例
CRON_TEMPLATE = """
# 学术论文自动更新 - 每天早上9点运行
0 9 * * * cd ~/.openclaw/workspace && python3 .learnings/academic/update/auto_updater.py --query "machine learning weather" >> /tmp/academic_update.log 2>&1
"""

if __name__ == "__main__":
    import sys
    
    updater = AutoUpdater()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--query":
        query = sys.argv[2] if len(sys.argv) > 2 else "machine learning weather"
        
        print(f"🔄 更新论文库: {query}")
        
        # 导入搜索模块
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from search.comprehensive_search import ComprehensiveSearch
        
        searcher = ComprehensiveSearch()
        results = searcher.search(query)
        
        added = updater.add_papers(results)
        
        print(f"✅ 添加了 {added} 篇新论文")
    else:
        print("用法: python auto_updater.py --query <关键词>")
        print("\n当前论文库状态:")
        data = updater.load_papers()
        print(f"  总计: {len(data['papers'])} 篇")
        print(f"  更新: {data.get('updated', '从未更新')}")
