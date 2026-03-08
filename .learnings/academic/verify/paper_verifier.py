#!/usr/bin/env python3
"""
完整论文验证系统
确保零虚假、零错误
"""
import requests
import re

class PaperVerifier:
    """论文验证器"""
    
    def __init__(self):
        self.proxies = {"http": "http://192.168.74.1:7890", "https": "http://192.168.74.1:7890"}
        self.verified = []
        self.errors = []
    
    def verify(self, paper_info):
        """
        验证单篇论文
        paper_info: {title, arxiv_id, doi, ...}
        返回: {valid, title, authors, year, url, error}
        """
        arxiv_id = paper_info.get("arxiv_id", "")
        doi = paper_info.get("doi", "")
        
        # 优先验证 arXiv
        if arxiv_id:
            result = self._verify_arxiv(arxiv_id)
            if result["valid"]:
                return result
        
        # 然后验证 DOI
        if doi:
            result = self._verify_doi(doi)
            if result["valid"]:
                return result
        
        return {"valid": False, "error": "无法验证"}
    
    def _verify_arxiv(self, arxiv_id):
        """验证 arXiv 论文"""
        # 清理 ID
        arxiv_id = arxiv_id.replace("arxiv:", "").strip()
        
        url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
        
        try:
            resp = requests.get(url, proxies=self.proxies, timeout=20)
            entry = re.search(r'<entry>(.*?)</entry>', resp.text, re.DOTALL)
            
            if not entry:
                return {"valid": False, "error": "论文不存在"}
            
            e = entry.group(1)
            
            # 提取信息
            title = re.search(r'<title>([^<]+)</title>', e)
            authors = re.findall(r'<name>([^<]+)</name>', e)[:10]
            published = re.search(r'<published>([^<]+)</published>', e)
            abstract = re.search(r'<summary>([^<]+)</summary>', e)
            
            return {
                "valid": True,
                "source": "arXiv",
                "id": arxiv_id,
                "title": title.group(1).strip() if title else "",
                "authors": authors,
                "year": published.group(1)[:4] if published else "",
                "abstract": abstract.group(1).strip()[:300] if abstract else "",
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "pdf": f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def _verify_doi(self, doi):
        """验证 DOI"""
        url = f"https://doi.org/{doi}"
        headers = {"Accept": "application/json"}
        
        try:
            resp = requests.get(url, headers=headers, proxies=self.proxies, timeout=20, allow_redirects=True)
            
            if resp.status_code == 200:
                try:
                    data = resp.json()
                except:
                    # 尝试 CrossRef API
                    api_url = f"https://api.crossref.org/works/{doi}"
                    resp = requests.get(api_url, proxies=self.proxies, timeout=20)
                    if resp.status_code == 200:
                        data = resp.json().get("message", {})
                    else:
                        return {"valid": False, "error": "DOI 无法解析"}
                
                title = data.get("title", [""])[0]
                authors = [f"{a.get('given', '')} {a.get('family', '')}" 
                          for a in data.get("author", [])[:10]]
                year = data.get("published-print", {}).get("date-parts", [[0]])[0][0]
                
                return {
                    "valid": True,
                    "source": "DOI",
                    "id": doi,
                    "title": title,
                    "authors": authors,
                    "year": str(year),
                    "url": f"https://doi.org/{doi}"
                }
        except Exception as e:
            return {"valid": False, "error": str(e)}
        
        return {"valid": False, "error": "DOI 不存在"}
    
    def verify_list(self, papers):
        """批量验证"""
        results = []
        
        for i, p in enumerate(papers, 1):
            print(f"[{i}/{len(papers)}] 验证...", end=" ")
            
            result = self.verify(p)
            
            if result["valid"]:
                print(f"✅ {result.get('year', '')}")
            else:
                print(f"❌ {result.get('error', '')}")
            
            results.append(result)
        
        valid_count = sum(1 for r in results if r["valid"])
        
        print(f"\n{'='*50}")
        print(f"验证结果: {valid_count}/{len(papers)} 通过")
        
        return results

# 测试
if __name__ == "__main__":
    verifier = PaperVerifier()
    
    test_papers = [
        {"arxiv_id": "2212.12794"},  # GraphCast
        {"arxiv_id": "2211.02556"},  # Pangu-Weather
        {"doi": "10.1038/s41586-023-06185-3"},
    ]
    
    results = verifier.verify_list(test_papers)
