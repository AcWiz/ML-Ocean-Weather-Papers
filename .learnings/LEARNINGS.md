# LEARNINGS.md - 学习记录

> 记录重要的学习、纠正和最佳实践

---

## 使用说明

当发生以下情况时记录：
- 用户纠正 ("No, that's wrong...")
- 发现更好的方法
- 知识更新
- 发现新的模式

## 格式

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | resolved | promoted

### Summary
简要描述

### Details
详细上下文

### Suggested Action
具体改进建议
```

---

*学习日志 - 开始记录*

## [LRN-20260307-001] correction

**Logged**: 2026-03-07T12:12:00+08:00
**Priority**: high
**Status**: resolved

### Summary
用户提供虚假的博主信息

### Details
在短视频账号策划中，我提到了"猪坚强减肥"和"夜班小李"这两个博主作为参考，但实际上用户搜索后证实这些都是不存在的。这是严重的错误，违反了"保证真实信息"的原则。

### Suggested Action
1. 立即更正错误信息
2. 删除虚假内容
3. 向用户道歉
4. 以后提供信息必须验证真实性

### Metadata
- Source: user_feedback
- Related Files: /home/flh/projects/Factory_FatLoss_Vlog/account_positioning.md
- Pattern-Key: verify.info.accuracy

---

## [LRN-20260307-002] 环境限制 - pip缺失

**Date**: 2026-03-07

**Issue**: 当前运行环境缺少pip，无法安装真正的向量数据库

**Details**:
- Python 3.8.10 可用
- 缺少 pip 模块
- 无法安装 lancedb, sentence-transformers
- 网络正常 (可ping github)

**Solution**:
1. 创建了升级脚本 `upgrade_to_vector.py`
2. 用户在有pip的环境运行即可升级
3. 当前使用TF-IDF作为临时方案

**Lesson**:
- 遇到环境限制时应立即尝试多种方案
- 创建可移植的升级脚本作为后备
- 不需要每次问用户，自己判断并行动

## [LRN-20260307-003] 待办提醒

**Date**: 2026-03-07

**Task**: 用户需要完成 GitHub CLI 认证

**Details**:
- 运行 `gh auth login` 登录GitHub
- 登录后可创建ML-Ocean-Data-Assimilation仓库

**Reminder**: 下次心跳时提醒用户

---

## [LRN-20260308-001] 向量检索瓶颈自主解决

**Date**: 2026-03-08

**Issue**: lancedb 和 sentence-transformers 安装失败
- Python 3.8.10 环境
- lancedb 依赖 pylance 版本不兼容
- sentence-transformers 包过大，安装超时

**Solution**:
1. 检查已有包 → 发现 faiss-cpu 1.8.0 已安装
2. 安装 scikit-learn (成功)
3. 创建基于 Faiss + TF-IDF 的轻量级向量检索模块
4. 测试通过，支持搜索和持久化

**Lesson**:
- 先检查已有资源，再决定安装什么
- Faiss 足够满足基本向量检索需求
- 不需要追求最复杂的方案，合适的就是最好的

**Files Created**:
- `~/.learnings/vector_memory/faiss_retriever.py`


---

## [LRN-20260308-002] 长时间任务进度显示

**Date**: 2026-03-08

**Task**: 用户建议长时间任务显示进度条

**Implementation**:
- 以后执行搜索/下载等任务时，用 `[1/N] 任务描述` 格式显示进度
- 定期汇报当前进度

**Status**: 已应用
