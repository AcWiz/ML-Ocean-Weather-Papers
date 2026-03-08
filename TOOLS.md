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
