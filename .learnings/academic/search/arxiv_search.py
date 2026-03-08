"""
arXiv 搜索模块
"""
import requests
import re

class ArxivSearch:
    """arXiv 论文搜索"""
    
    def __init__(self, proxies=None):
        self.proxies = proxies or {"http": "http://192.168.74.1:7890", "https": "http://192.168.74.1:7890"}
        self.base_url = "http://export.arxiv.org/api/query"
    
    def search(self, query, max_results=50):
        """搜索 arXiv 论文"""
        params = {
            "search_query": f"all:{query}",
            "max_results": max_results,
            "sortBy": "relevance"
        }
        
        try:
            resp = requests.get(self.base_url, params=params, proxies=self.proxies, timeout=30)
            entries = re.findall(r'<entry>(.*?)</entry>', resp.text, re.DOTALL)
            
            papers = []
            for e in entries:
                title = re.search(r'<title>([^<]+)</title>', e)
                arxiv_id = re.search(r'<id>([^<]+)</id>', e)
                published = re.search(r'<published>([^<]+)</published>', e)
                authors = re.findall(r'<name>([^<]+)</name>', e)
                abstract = re.search(r'<summary>([^<]+)</summary>', e)
                
                if title and arxiv_id:
                    aid = arxiv_id.group(1).split('/')[-1]
                    papers.append({
                        "source": "arXiv",
                        "id": aid,
                        "title": title.group(1).strip(),
                        "authors": authors[:5],
                        "year": published.group(1)[:4] if published else "",
                        "abstract": abstract.group(1).strip()[:500] if abstract else "",
                        "url": f"https://arxiv.org/abs/{aid}",
                        "pdf": f"https://arxiv.org/pdf/{aid}.pdf"
                    })
            return papers
        except Exception as e:
            return []
    
    def verify(self, arxiv_id):
        """验证 arXiv ID 是否存在"""
        params = {"id_list": arxiv_id}
        try:
            resp = requests.get(self.base_url, params=params, proxies=self.proxies, timeout=15)
            entry = re.search(r'<entry>(.*?)</entry>', resp.text, re.DOTALL)
            return entry is not None
        except:
            return False

# 测试
if __name__ == "__main__":
    search = ArxivSearch()
    results = search.search("machine learning weather", 5)
    for r in results:
        print(f"- {r['title'][:50]}... ({r['year']})")
