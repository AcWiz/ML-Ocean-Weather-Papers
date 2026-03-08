#!/usr/bin/env python3
"""
完整论文验证系统
逐篇验证所有论文的准确性
"""
import requests
import re
import json
import sys
import os
from pathlib import Path

PROXIES = {"http": "http://192.168.74.1:7890", "https": "http://192.168.74.1:7890"}

class PaperVerifier:
    def __init__(self):
        self.results = []
        self.errors = []
    
    def verify_arxiv(self, arxiv_id):
        """验证单篇 arXiv 论文"""
        url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
        try:
            resp = requests.get(url, proxies=PROXIES, timeout=20)
            
            entry = re.search(r'<entry>(.*?)</entry>', resp.text, re.DOTALL)
            if not entry:
                return {"valid": False, "error": "论文不存在", "arxiv_id": arxiv_id}
            
            e = entry.group(1)
            
            # 提取信息
            title = re.search(r'<title>([^<]+)</title>', e)
            authors = re.findall(r'<name>([^<]+)</name>', e)
            published = re.search(r'<published>([^<]+)</published>', e)
            abstract = re.search(r'<summary>([^<]+)</summary>', e)
            
            title_text = title.group(1).strip() if title else ""
            year = published.group(1)[:4] if published else ""
            
            return {
                "valid": True,
                "arxiv_id": arxiv_id,
                "title": title_text,
                "authors": authors[:10],  # 取前10个作者
                "year": year,
                "abstract": abstract.group(1).strip()[:200] if abstract else "",
                "link": f"https://arxiv.org/abs/{arxiv_id}",
                "pdf": f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            }
        except Exception as e:
            return {"valid": False, "error": str(e), "arxiv_id": arxiv_id}
    
    def search_paper(self, query):
        """根据关键词搜索论文"""
        url = "http://export.arxiv.org/api/query"
        params = {"search_query": f"all:{query}", "max_results": 10, "sortBy": "relevance"}
        
        try:
            resp = requests.get(url, params=params, proxies=PROXIES, timeout=20)
            entries = re.findall(r'<entry>(.*?)</entry>', resp.text, re.DOTALL)
            
            results = []
            for e in entries:
                title = re.search(r'<title>([^<]+)</title>', e)
                arxiv_id = re.search(r'<id>([^<]+)</id>', e)
                published = re.search(r'<published>([^<]+)</published>', e)
                
                if title and arxiv_id:
                    aid = arxiv_id.group(1).split('/')[-1].split('v')[0]
                    results.append({
                        "arxiv_id": aid,
                        "title": title.group(1).strip(),
                        "year": published.group(1)[:4] if published else ""
                    })
            return results
        except Exception as e:
            return []
    
    def verify_readme(self, readme_path):
        """验证 README 中的所有论文链接"""
        with open(readme_path, 'r') as f:
            content = f.read()
        
        # 提取所有 arXiv ID
        arxiv_pattern = r'arXiv:(\d{4}\.\d{4,5})'
        found_ids = re.findall(arxiv_pattern, content)
        
        print(f"\n{'='*70}")
        print(f"🔍 完整验证开始 - 共发现 {len(found_ids)} 个论文链接")
        print(f"{'='*70}\n")
        
        results = []
        for i, arxiv_id in enumerate(found_ids, 1):
            print(f"[{i}/{len(found_ids)}] 验证 {arxiv_id}...", end=" ")
            
            result = self.verify_arxiv(arxiv_id)
            
            if result["valid"]:
                print(f"✅ ({result['year']})")
                print(f"    标题: {result['title'][:60]}...")
                print(f"    作者: {result['authors'][0]} et al.")
            else:
                print(f"❌ {result.get('error', 'Unknown error')}")
            
            results.append(result)
            self.results.append(result)
        
        return results
    
    def generate_report(self):
        """生成验证报告"""
        total = len(self.results)
        valid = sum(1 for r in self.results if r.get("valid", False))
        invalid = total - valid
        
        print(f"\n{'='*70}")
        print(f"📋 验证报告")
        print(f"{'='*70}")
        print(f"总计: {total}")
        print(f"✅ 有效: {valid}")
        print(f"❌ 无效: {invalid}")
        
        if invalid > 0:
            print(f"\n⚠️ 需要修正的论文:")
            for r in self.results:
                if not r.get("valid", False):
                    print(f"  - arXiv:{r.get('arxiv_id', 'N/A')} - {r.get('error', 'Unknown')}")
        
        return {
            "total": total,
            "valid": valid,
            "invalid": invalid,
            "results": self.results
        }

if __name__ == "__main__":
    # 验证 GitHub 项目
    readme_path = "/home/flh/ml-ocean-weather-papers/README.md"
    
    if not os.path.exists(readme_path):
        print(f"文件不存在: {readme_path}")
        sys.exit(1)
    
    verifier = PaperVerifier()
    verifier.verify_readme(readme_path)
    report = verifier.generate_report()
    
    # 保存详细报告
    with open("/tmp/verify_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n详细报告已保存到: /tmp/verify_report.json")
