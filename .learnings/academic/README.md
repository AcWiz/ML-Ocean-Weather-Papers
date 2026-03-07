# 学术平台能力系统 v1.0

> 可访问的学术平台和工具集

## 已集成平台

| 平台 | 功能 | 状态 |
|------|------|:----:|
| **arXiv** | 论文搜索/下载 | ✅ |
| **Semantic Scholar** | 论文搜索 | ✅ |
| **PubMed** | 生物医学文献 | ✅ |
| **HuggingFace** | 模型搜索 | ✅ |
| **GitHub** | 代码搜索 | ✅ (需token) |

## 使用方法

```bash
# 激活Python环境
source ~/miniconda/etc/profile.d/conda.sh
conda activate vector_mem

# 搜索论文
python ~/.openclaw/workspace/.learnings/academic/arxiv_search.py "关键词"
python ~/.openclaw/workspace/.learnings/academic/semantic_scholar.py "关键词"
python ~/.openclaw/workspace/.learnings/academic/huggingface_search.py "关键词"

# 下载论文
python ~/.openclaw/workspace/.learnings/academic/paper_downloader.py arxiv:2301.12345
```

## 工具说明

| 工具 | 用途 |
|------|------|
| `arxiv_search.py` | arXiv论文搜索 |
| `semantic_scholar.py` | Semantic Scholar搜索 |
| `huggingface_search.py` | HuggingFace模型搜索 |
| `github_code_search.py` | GitHub代码搜索 |
| `scholar_search.py` | PubMed/IEEE搜索 |
| `paper_downloader.py` | 论文PDF下载 |

## 可扩展方向

- [ ] Google Scholar (需代理)
- [ ] IEEE Xplore (需API key)
- [ ] CNKI 知网 (需特殊访问)
- [ ] Web of Science
- [ ] Scopus

---

*持续更新*
