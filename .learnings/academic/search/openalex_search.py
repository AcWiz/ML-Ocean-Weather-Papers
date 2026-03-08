"""
OpenAlex 搜索模块
"""
import requests

class OpenAlexSearch:
    """OpenAlex 论文搜索 - 免费开放学术图谱"""
    
    def __init__(self):
        self.base_url = "https://api.openalex.org/works"
    
    def search(self, query, max_results=50):
        """搜索论文"""
        params = {
            "search": query,
            "per_page": max_results,
            "sort": "cited_by_count:desc"
        }
        
        try:
            resp = requests.get(self.base_url, params=params, timeout=30)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                
                papers = []
                for r in results:
                    title = r.get("title", "")
                    year = r.get("publication_year", "")
                    dois = r.get("doi", "")
                    cited = r.get("cited_by_count", 0)
                    
                    authors = r.get("authorships", [])[:5]
                    author_names = [a.get("author", {}).get("display_name", "") for a in authors]
                    
                    papers.append({
                        "source": "OpenAlex",
                        "id": dois.split("/")[-1] if dois else "",
                        "doi": dois,
                        "title": title,
                        "authors": author_names,
                        "year": str(year),
                        "cited": cited,
                        "url": dois if dois else ""
                    })
                return papers
        except:
            pass
        return []

# 测试
if __name__ == "__main__":
    search = OpenAlexSearch()
    results = search.search("machine learning weather", 5)
    for r in results:
        print(f"- {r['title'][:50]}... ({r['year']})")
