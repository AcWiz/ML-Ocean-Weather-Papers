# 搜索方案状态报告

## 已测试的方案

### ❌ 失败方案

| 方案 | 原因 |
|------|------|
| Google 直接请求 | 反爬虫 + JS 渲染 |
| Playwright 模拟 | 被检测为机器人 |
| Bing 请求 | 反爬虫 + JS 渲染 |
| DuckDuckGo | 返回空结果 |
| SearXNG 实例 | 全部不可用/限流 |
| Whoogle | 服务不可用 |
| YaCy | 需要本地安装 |
| Brave Search | 需要 API Key |

### ✅ 可用方案

| 方案 | 覆盖量 |
|------|--------|
| arXiv | 200万+ |
| OpenAlex | 2亿+ |
| CrossRef | 1亿+ |
| IEEE | 通过 CrossRef |
| Semantic Scholar | 2亿+ |

## 结论

1. **Google/Bing 搜索无法在服务端自动化**
   - 原因：反爬虫 + JavaScript 渲染
   - 解决方案：使用浏览器插件或手动搜索

2. **学术搜索已有替代**
   - 现有 API 已覆盖主要学术资源
   - 建议使用统一搜索命令

3. **可能的解决方案**
   - 使用付费 API 服务（SerpAPI, ScrapingBee）
   - 自托管搜索服务（Whoogle, SearXNG）
   - 使用浏览器扩展
