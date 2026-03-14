# 🌊 神经数据同化 + 海洋AI 论文库

> 每日更新的高质量论文清单 | 聚焦: 扩散模型、数据同化、海洋预报AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/AcWiz/ML-Ocean-Weather-Papers/pulls)
[![Last Updated](https://img.shields.io/badge/last%20updated-2026--03--14-blue.svg)](https://github.com/AcWiz/ML-Ocean-Weather-Papers)

---

## 📑 目录

- [🎯 研究方向](#-研究方向)
- [📚 论文分类](#-论文分类)
- [⭐ 必读论文](#-必读论文)
- [🚀 快速开始](#-快速开始)
- [📊 论文统计](#-论文统计)
- [🤝 贡献指南](#-贡献指南)

---

## 🎯 研究方向

| 方向 | 关键词 | 热度 |
|------|--------|------|
| 扩散模型+DA | Diffusion, Score, Generative | ⭐⭐⭐⭐⭐ |
| 神经变分同化 | 4DVarNet, Neural Var | ⭐⭐⭐⭐⭐ |
| 流匹配 | Flow Matching, Rectified Flow | ⭐⭐⭐⭐ |
| 海洋AI预报 | Ocean, SST, SSH | ⭐⭐⭐⭐ |
| PINN+DA | Physics-informed, Constrained | ⭐⭐⭐⭐ |
| 神经算子 | FNO, DeepONet, GNN | ⭐⭐⭐ |

---

## 📚 论文分类

### 🔬 核心方向

| 分类 | 论文数 | 描述 |
|------|--------|------|
| [扩散模型+数据同化](./papers/diffusion_da/) | 15+ | DDPM、Score-Based、潜在扩散 |
| [神经变分同化](./papers/neural_da/) | 10+ | 4DVarNet、神经增量DA |
| [天气/海洋预报AI](./papers/weather_ai/) | 25+ | GraphCast、FourCastNet、Pangu |
| [神经算子](./papers/neural_operator/) | 8+ | FNO、DeepONet、GNO |
| [PINN+数据同化](./papers/pinn_da/) | 10+ | 物理约束同化 |
| [海洋ML](./papers/ocean_ml/) | 12+ | 海洋环流、ENSO、潮汐 |

---

## ⭐ 必读论文 (Top 10)

> 按阅读优先级排列

| # | 论文 | 年份 | 方向 | 必读理由 |
|---|------|------|------|----------|
| 1 | [Diffusion Models for Data Assimilation](https://arxiv.org/2310.20182) | 2023 | 扩散+DA | 奠基之作 |
| 2 | [GraphCast](https://arxiv.org/2212.12794) | 2022 | 天气AI | SOTA预报 |
| 3 | [4DVarNet-SSH](https://arxiv.org/2211.05904) | 2022 | 神经同化 | 海面高度DA |
| 4 | [NeuralGCM](https://arxiv.org/2306.16967) | 2023 | 神经GCM | 混合建模 |
| 5 | [Score-Based Diffusion for DA](https://arxiv.org/2403.07832) | 2024 | 分数扩散 | 最新工作 |
| 6 | [Fourier Neural Operator](https://arxiv.org/2010.08895) | 2021 | 神经算子 | 基础必读 |
| 7 | [FourCastNet](https://arxiv.org/2208.02199) | 2022 | 天气AI | NVIDIA出品 |
| 8 | [Pangu-Weather](https://arxiv.org/2111.15367) | 2021 | 天气AI | 华为云 |
| 9 | [DeepONet](https://arxiv.org/1912.09397) | 2019 | 神经算子 | 算子学习 |
| 10 | [Physics-informed PINN](https://arxiv.org/2010.08895) | 2021 | PINN | 物理约束 |

---

## 🚀 快速开始

### 搜索论文

```bash
# 激活环境
source ~/miniconda/etc/profile.d/conda.sh 
conda activate vector_mem 

# 搜索论文
python ~/.openclaw/workspace/.learnings/academic/search/comprehensive_search.py "关键词"
```

### 每日KPI

| 任务 | 目标 |
|------|------|
| 论文精读 | 4篇 |
| 论文初筛 | 10篇 |
| 数学公式 | 6个 |

---

## 📊 论文统计

```
扩散模型+DA    ████████████████░░░░  15+
神经变分同化   ██████████░░░░░░░░░  10+
天气/海洋AI    ████████████████████  25+
神经算子       ████████░░░░░░░░░░░  8+
PINN+DA        ██████████░░░░░░░░░  10+
海洋ML         █████████████░░░░░░░  12+
─────────────────────────────
总计           80+ 篇
```

---

## 🤝 贡献指南

欢迎提交PR！请参考以下格式：

```markdown
### 论文名称
- **arXiv**: xxxx.xxxxx
- **方向**: xxx
- **相关度**: ⭐⭐⭐⭐⭐
- **备注**: xxx
```

---

## 📞 联系方式

- GitHub: [AcWiz/ML-Ocean-Weather-Papers](https://github.com/AcWiz/ML-Ocean-Weather-Papers)
- Email: 1462396613@qq.com

---

*🎯 致力于构建最全的神经数据同化论文库*
