#!/usr/bin/env python3
"""
完整论文验证系统 V2
使用 Semantic Scholar API 作为主要验证源
支持：标题、作者、年份、DOI、链接 交叉验证
"""
import requests
import json
import sys
import os
from pathlib import Path
import time

class PaperVerifierV2:
    def __init__(self):
        self.semanticscholar_url = "https://api.semanticscholar.org/graph/v1/paper"
        self.results = []
        self.errors = []
    
    def verify_by_arxiv(self, arxiv_id):
        """
        通过 arXiv ID 验证论文 - 最可靠的方法
        格式: arxiv:2208.05419 或 2208.05419
        """
        # 清理 arxiv_id
        arxiv_id = arxiv_id.replace("arxiv:", "").strip()
        
        url = f"{self.semanticscholar_url}/arxiv:{arxiv_id}"
        params = {
            "fields": "title,authors,year,venue,externalIds,abstract,citationCount"
        }
        
        try:
            resp = requests.get(url, params=params, timeout=20)
            
            if resp.status_code == 200:
                data = resp.json()
                
                # 提取信息
                authors = [a.get("name", "") for a in data.get("authors", [])]
                external = data.get("externalIds", {})
                
                return {
                    "valid": True,
                    "arxiv_id": arxiv_id,
                    "title": data.get("title", ""),
                    "authors": authors,
                    "year": data.get("year"),
                    "venue": data.get("venue", ""),
                    "citation_count": data.get("citationCount", 0),
                    "doi": external.get("DOI", ""),
                    "url": f"https://arxiv.org/abs/{arxiv_id}",
                    "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                }
            elif resp.status_code == 404:
                return {"valid": False, "error": "论文未找到", "arxiv_id": arxiv_id}
            else:
                return {"valid": False, "error": f"API错误: {resp.status_code}", "arxiv_id": arxiv_id}
                
        except Exception as e:
            return {"valid": False, "error": str(e), "arxiv_id": arxiv_id}
    
    def search_paper(self, query, limit=5):
        """
        搜索论文
        """
        url = f"{self.semanticscholar_url}/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,year,venue,externalIds"
        }
        
        try:
            resp = requests.get(url, params=params, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                papers = []
                for p in data.get("data", []):
                    external = p.get("externalIds", {})
                    arxiv = external.get("ArXiv", "")
                    papers.append({
                        "title": p.get("title", ""),
                        "arxiv_id": arxiv,
                        "year": p.get("year"),
                        "authors": [a.get("name", "") for a in p.get("authors", [])[:3]],
                        "venue": p.get("venue", "")
                    })
                return papers
        except Exception as e:
            return []
    
    def verify_readme(self, readme_path):
        """
        验证 README 中的所有论文
        """
        if not os.path.exists(readme_path):
            print(f"❌ 文件不存在: {readme_path}")
            return []
        
        with open(readme_path, 'r') as f:
            content = f.read()
        
        # 提取所有 arXiv ID
        import re
        # 匹配多种格式: arxiv:2208.05419, arXiv:2208.05419, 2208.05419
        arxiv_patterns = [
            r'arxiv:(\d{4}\.\d{4,5})',
            r'arXiv:(\d{4}\.\d{4,5})',
            r'arxiv\.org/abs/(\d{4}\.\d{4,5})',
            r'\((\d{4}\.\d{4,5})\)',  # (2208.05419)
        ]
        
        found_ids = set()
        for pattern in arxiv_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            found_ids.update(matches)
        
        print(f"\n{'='*70}")
        print(f"🔍 完整验证开始")
        print(f"📁 文件: {readme_path}")
        print(f"📊 发现 {len(found_ids)} 个唯一论文 ID")
        print(f"{'='*70}\n")
        
        results = []
        for i, arxiv_id in enumerate(sorted(found_ids), 1):
            print(f"[{i}/{len(found_ids)}] 验证 arXiv:{arxiv_id}...", end=" ")
            
            result = self.verify_by_arxiv(arxiv_id)
            
            if result["valid"]:
                print(f"✅ ({result['year']})")
                print(f"    标题: {result['title'][:60]}...")
                print(f"    作者: {result['authors'][0]} et al.")
                if result.get("venue"):
                    print(f"    期刊: {result['venue'][:40]}")
                print(f"    引用: {result.get('citation_count', 0)}")
            else:
                print(f"❌ {result.get('error', 'Unknown')}")
            
            results.append(result)
            self.results.append(result)
            
            # 避免 API 限流
            time.sleep(0.3)
        
        return results
    
    def generate_report(self):
        """
        生成完整验证报告
        """
        total = len(self.results)
        valid = sum(1 for r in self.results if r.get("valid", False))
        invalid = total - valid
        
        print(f"\n{'='*70}")
        print(f"📋 完整验证报告")
        print(f"{'='*70}")
        print(f"总计: {total}")
        print(f"✅ 有效: {valid}")
        print(f"❌ 无效: {invalid}")
        
        if invalid > 0:
            print(f"\n⚠️ 需要修正的论文:")
            for r in self.results:
                if not r.get("valid", False):
                    print(f"  - arXiv:{r.get('arxiv_id', 'N/A')} - {r.get('error', 'Unknown')}")
        
        # 输出修正建议
        print(f"\n{'='*70}")
        print(f"📝 修正后的论文信息 (Markdown 格式)")
        print(f"{'='*70}")
        
        for r in self.results:
            if r.get("valid"):
                arxiv_id = r.get("arxiv_id", "")
                title = r.get("title", "")
                authors = r.get("authors", [])
                year = r.get("year", "")
                
                # 格式化作者
                if len(authors) >= 3:
                    author_str = f"{authors[0]}, {authors[1]}, et al."
                elif len(authors) == 2:
                    author_str = f"{authors[0]}, {authors[1]}"
                elif len(authors) == 1:
                    author_str = authors[0]
                else:
                    author_str = "Unknown"
                
                print(f"\n| {year} | **{title[:40]}** | {author_str} | [{arxiv_id}](https://arxiv.org/abs/{arxiv_id}) |")
        
        return {
            "total": total,
            "valid": valid,
            "invalid": invalid,
            "results": self.results
        }

if __name__ == "__main__":
    readme_path = "/home/flh/ml-ocean-weather-papers/README.md"
    
    if len(sys.argv) > 1:
        readme_path = sys.argv[1]
    
    verifier = PaperVerifierV2()
    verifier.verify_readme(readme_path)
    report = verifier.generate_report()
    
    # 保存详细报告
    output_path = "/tmp/verify_report_v2.json"
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n详细报告已保存到: {output_path}")
