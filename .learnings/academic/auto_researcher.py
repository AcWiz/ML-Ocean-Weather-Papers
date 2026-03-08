#!/usr/bin/env python3
"""
智能学术研究助手
自动完成：搜索→验证→分类→生成报告
"""
import json
import time
from datetime import datetime
from pathlib import Path

class AutoResearcher:
    """自动学术研究"""
    
    def __init__(self):
        self.topics = [
            "machine learning ocean data assimilation",
            "deep learning weather forecasting",
            "neural network climate prediction",
            "transformer weather prediction",
            "physics informed neural networks ocean",
            "graph neural network weather",
            "data assimilation deep learning"
        ]
        self.results = []
    
    def run_full_research(self):
        """完整研究流程"""
        print("=" * 60)
        print("🔬 智能学术研究助手")
        print("=" * 60)
        
        # 1. 搜索所有主题
        print("\n📡 阶段1: 全网搜索")
        print("-" * 40)
        
        all_papers = []
        for topic in self.topics:
            print(f"\n搜索: {topic}")
            papers = self._search_topic(topic)
            all_papers.extend(papers)
            print(f"  +{len(papers)} 篇")
            time.sleep(1)
        
        # 2. 验证
        print("\n\n✅ 阶段2: 验证论文")
        print("-" * 40)
        
        verified = []
        for i, p in enumerate(all_papers[:50], 1):
            print(f"[{i}/50] 验证...", end=" ")
            if self._verify_paper(p):
                verified.append(p)
                print("✅")
            else:
                print("❌")
        
        # 3. 分类
        print("\n\n📂 阶段3: 智能分类")
        print("-" * 40)
        
        categorized = self._categorize(verified)
        
        for cat, papers in categorized.items():
            print(f"  {cat}: {len(papers)} 篇")
        
        # 4. 生成报告
        print("\n\n📝 阶段4: 生成报告")
        print("-" * 40)
        
        report = self._generate_report(categorized)
        
        return report
    
    def _search_topic(self, topic):
        """搜索单个主题"""
        # 使用搜索模块
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        
        try:
            from search.comprehensive_search import ComprehensiveSearch
            searcher = ComprehensiveSearch()
            return searcher.search(topic)
        except:
            return []
    
    def _verify_paper(self, paper):
        """验证论文有效性"""
        # 检查必要字段
        if not paper.get("title"):
            return False
        if not paper.get("authors"):
            return False
        # 检查标题长度
        if len(paper.get("title", "")) < 10:
            return False
        return True
    
    def _categorize(self, papers):
        """智能分类"""
        categories = {
            "Weather Forecasting": [],
            "Ocean Data Assimilation": [],
            "Neural Networks": [],
            "Climate Models": [],
            "Benchmarks": [],
            "Reviews": []
        }
        
        keywords = {
            "Weather Forecasting": ["weather", "forecast", "precipitation", "storm", "hurricane"],
            "Ocean Data Assimilation": ["ocean", "sea", "assimilation", "marine"],
            "Neural Networks": ["neural", "network", "deep learning", "transformer", "cnn", "lstm"],
            "Climate Models": ["climate", "gcm", "circulation", "atmospheric"],
            "Benchmarks": ["benchmark", "dataset", "weatherbench"],
            "Reviews": ["review", "survey", "overview"]
        }
        
        for p in papers:
            title = p.get("title", "").lower()
            categorized = False
            
            for cat, kws in keywords.items():
                if any(k in title for k in kws):
                    categories[cat].append(p)
                    categorized = True
                    break
            
            if not categorized:
                categories["Neural Networks"].append(p)
        
        return categories
    
    def _generate_report(self, categorized):
        """生成Markdown报告"""
        report = f"""# 🔬 机器学习海洋与气象论文研究报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**来源**: arXiv, OpenAlex, CrossRef

---

"""
        
        for cat, papers in categorized.items():
            if not papers:
                continue
            
            report += f"## {cat}\n\n"
            
            for p in papers[:10]:  # 每类最多10篇
                title = p.get("title", "")[:60]
                year = p.get("year", "")
                authors = ", ".join(p.get("authors", [])[:2])
                url = p.get("url", "")
                
                report += f"""### {title}...
- **年份**: {year}
- **作者**: {authors}
- **链接**: {url}

"""
        
        return report

if __name__ == "__main__":
    researcher = AutoResearcher()
    report = researcher.run_full_research()
    
    # 保存报告
    report_file = Path("~/ml-ocean-weather-papers/research_report.md").expanduser()
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, "w") as f:
        f.write(report)
    
    print(f"\n✅ 报告已保存到: {report_file}")
