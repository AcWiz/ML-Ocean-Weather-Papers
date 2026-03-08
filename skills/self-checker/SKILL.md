---
name: self-checker
description: 任务自检与验证技能。在完成用户任务后自动检查完成质量、数据准确性、链接有效性，并自我纠正错误。
---

# Self-Checker 自检技能

## 触发条件

- 用户任务完成后
- 发现数据/信息可能不准确时
- 提交结果前

## 自检流程

### Step 1: 完整性检查

```python
# 检查清单
checklist = [
    "任务要求的所有项目是否完成？",
    "是否有遗漏的内容？",
    "格式是否符合要求？"
]
```

### Step 2: 数据准确性验证

**必须验证的内容：**

1. **论文链接验证**
   ```bash
   # 验证 arXiv 链接
   curl -s "https://arxiv.org/abs/{arxiv_id}" | grep "Title"
   
   # 或使用 API
   curl -s "http://export.arxiv.org/api/query?id_list={arxiv_id}"
   ```

2. **作者信息验证**
   - 通过 Semantic Scholar API 验证
   - 或通过 arXiv API 获取

3. **来源验证**
   - Nature 论文 → 检查 nature.com
   - arXiv 论文 → 检查 arxiv.org

### Step 3: 交叉验证

- 同一论文信息在多个来源交叉验证
- 关键数据（年份、作者）至少两个来源确认

### Step 4: 自我纠正

如果发现问题：
1. 立即标记错误
2. 尝试修正
3. 无法修正的删除或标注"未验证"
4. 向用户报告问题

## 输出格式

```
📋 自检报告
═══════════════════════════════════
任务: [任务名称]
检查时间: [时间]
─────────────────────────────────
✅ 通过项:
- [项目1]
- [项目2]

❌ 问题项:
- [问题1] → [修正方案/删除]

⚠️ 需确认:
- [未确定项]
─────────────────────────────────
结论: [通过/需修改]
═══════════════════════════════════
```

## 关键原则

1. **准确性 > 速度** - 宁可慢也要保证正确
2. **验证 > 猜测** - 不确定的要查证
3. **删除 > 虚假** - 无法验证的宁可删除
4. **透明** - 发现问题主动报告用户

## 快速验证命令

```bash
# 验证 arXiv 论文
python3 -c "
import requests, re
proxies = {'http':'http://192.168.74.1:7890','https':'http://192.168.74.1:7890'}
r = requests.get('http://export.arxiv.org/api/query?id_list=2305.00080', proxies=proxies)
title = re.search(r'<title>([^<]+)</title>', r.text)
print(title.group(1) if title else 'Error')
"

# 验证 Nature 论文
curl -s "https://www.nature.com/articles/s41586-023-06185-3" | grep -o "<title>[^<]*</title>"
```

---

*自检是保证质量的最后一道防线*
