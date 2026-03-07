# 网页浏览能力系统 v1.0

> 可浏览任意网站的工具集

## 工具

| 工具 | 功能 |
|------|------|
| `web_fetch.py` | 通用网页抓取 |
| `web_parse.py` | 网页结构解析 |
| `web_search.py` | 搜索引擎 |
| `content_extractor.py` | 文章内容提取 |

## 使用

```bash
# 搜索
python web_search.py "关键词"

# 抓取网页
python web_fetch.py https://example.com

# 解析结构
python web_parse.py https://example.com

# 提取文章
python content_extractor.py <文章URL>
```

## 原理

- 使用 urllib 直接请求
- 正则表达式解析HTML
- 无需额外依赖
