# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## 备份与回滚

### 备份命令

```bash
# 手动备份核心文件
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR=~/.openclaw/backups
cp ~/.openclaw/workspace/SOUL.md "$BACKUP_DIR/${TIMESTAMP}_SOUL.md"
```

### 备份位置
- 目录: `~/.openclaw/backups/`
- 格式: `{TIMESTAMP}_{FILENAME}.md`

### 恢复备份
```bash
# 从备份恢复
cp ~/.openclaw/backup/2026-03-07_11-03-16_SOUL.md ~/.openclaw/workspace/SOUL.md
```

---

## 学习日志

### 位置
- 目录: `~/.openclaw/workspace/.learnings/`
- 文件:
  - LEARNINGS.md - 学习与纠正
  - ERRORS.md - 错误记录
  - FEATURE_REQUESTS.md - 功能请求

### 格式
- 学习: [LRN-YYYYMMDD-XXX]
- 错误: [ERR-YYYYMMDD-XXX]
- 功能: [FEAT-YYYYMMDD-XXX]


---

## 学术搜索配置

### 机构认证 (DLUT)
- 机构: Dalian University of Technology
- 邮箱: fenglonghan@mail.dlut.edu.cn
- 密码: FLHflh@2025 (内存加载，不持久化)
- 代理: http://192.168.74.1:7890

### 搜索脚本
```bash
# 激活环境
source ~/miniconda/etc/profile.d/conda.sh 
conda activate vector_mem 

# 学术论文搜索
python ~/.openclaw/workspace/.learnings/academic/arxiv_search.py "关键词"
python ~/.openclaw/workspace/.learnings/academic/semantic_scholar.py "关键词"
python ~/.openclaw/workspace/.learnings/academic/google_scholar.py "关键词"

# HuggingFace 模型搜索
python ~/.openclaw/workspace/.learnings/academic/huggingface_search.py "关键词"

# 通用网页搜索
python ~/.openclaw/workspace/.learnings/academic/web_search.py "关键词"
```

---

## 已安装的新技能 (2026-03-08)

### 学术研究
- **academic-deep-research** - 深度学术研究，文献综述
- **arxiv-watcher** - arXiv 论文追踪和摘要

### 数据分析
- **data-analyst** - 数据可视化、报告生成、SQL 查询

### 记忆系统
- **agent-memory** - 持久化记忆系统

### 已跳过 (安全原因)
- **agent-browser** - 被 VirusTotal 标记为可疑


---

## 学术研究完整系统 (2026-03-08)

### 搜索工具
```bash
# 综合搜索
python3 ~/.openclaw/workspace/.learnings/academic/search/comprehensive_search.py "关键词"

# 自动研究助手
python3 ~/.openclaw/workspace/.learnings/academic/auto_researcher.py
```

### 分析工具
```bash
# 论文影响力分析
python3 ~/.openclaw/workspace/.learnings/academic/paper_analyzer.py

# 每日简报生成
python3 ~/.openclaw/workspace/.learnings/academic/daily_briefing.py
```

### 验证工具
```bash
# 论文验证
python3 ~/.openclaw/workspace/skills/self-checker/scripts/verify_v3.py
```

### 自动更新
```bash
# 设置每日自动更新
# 添加到 crontab:
0 9 * * * python3 ~/.openclaw/workspace/.learnings/academic/update/auto_updater.py --query "machine learning weather"
```

