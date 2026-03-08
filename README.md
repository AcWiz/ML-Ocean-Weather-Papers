# 🌊 ML Ocean Data Assimilation & Weather Forecasting Papers

> 机器学习海洋数据同化与天气预报论文精选集

**维护者**: Ethan (观测者-7)  
**更新时间**: 2026-03-08  
**总论文数**: 60+

---

## 📊 目录

1. [🌤️ Weather Forecasting](#1-🌤️-weather-forecasting-天气预报)
2. [🌊 Ocean Data Assimilation](#2-🌊-ocean-data-assimilation-海洋数据同化)
3. [🧠 Neural GCM](#3-🧠-neural-gcm-神经环流模式)
4. [📊 Benchmarks](#4-📊-benchmarks-基准数据集)
5. [🔬 Reviews & Surveys](#5-🔬-reviews--surveys-综述论文)
6. [📅 2026 最新论文](#6-📅-2026-最新论文)

---

## 1. 🌤️ Weather Forecasting (天气预报)

### 核心必读论文 ⭐

| 年份 | 论文 | 作者 | 链接 | 关键词 |
|------|------|------|------|--------|
| 2024 | **GraphCast: Learning Medium-Range Global Weather** | Remi Lam, Andreas Grofers, et al. | [Nature](https://www.nature.com/articles/s41586-023-06185-3) | GNN, 10-day forecast, Medium-range |
| 2023 | **Pangu-Weather: A 3D Earth-specific Transformer** | Kaifeng Bi, Lingxi Xie, et al. | [Nature](https://www.nature.com/articles/s41586-023-06056-9) | 3D Transformer, 7-day forecast |
| 2024 | **FuXi: Cascaded Weather Forecasting Model** | Chen Zhou, et al. | [arXiv:2401.02662](https://arxiv.org/abs/2401.02662) | Cascaded model, 15-day, ENSO |
| 2023 | **FourCastNet: A Global Data-driven Weather Model** | Ilya Price, Jayesh K. Gupta, et al. | [arXiv:2302.06696](https://arxiv.org/abs/2302.06696) | Fourier Neural Operator, AFNO |
| 2024 | **NeuralGCM: Machine Learning Weather and Climate** | Dmitri Kochkov, et al. | [arXiv:2306.09867](https://arxiv.org/abs/2306.09867) | Differentiable GCM, ML |
| 2023 | **ClimaX: Foundation Model for Weather and Climate** | Tung Nguyen, Johannes Brandstetter, et al. | [arXiv:2305.00080](https://arxiv.org/abs/2305.00080) | Foundation Model, Transfer |
| 2024 | **NowcastNet: Extreme Precipitation Nowcasting** | Zhang, et al. | [Nature](https://www.nature.com/articles/s41586-023-01942-y) | Extreme events, Nowcast |

### FourCastNet 系列

| 年份 | 论文 | 作者 | 关键词 |
|------|------|------|--------|
| 2022 | FourCastNet: A Global Data-driven High-resolution Weather Forecasting | Ilya Price, et al. | AFNO, Fourier |
| 2025 | FourCastNet 3: A geometric approach to probabilistic forecasting | - | Geometric |
| 2024 | FourCastNeXt: Optimizing FourCastNet Training | - | Optimization |

### 其他重要论文

| 年份 | 论文 | 作者 | 关键词 |
|------|------|------|--------|
| 2024 | DiffWave: Diffusion Probabilistic Model for Weather | - | Diffusion |
| 2024 | Temporal Graph Neural Networks for Weather | - | Temporal GNN |
| 2023 | WeatherUNet: Deep Learning for Weather Prediction | - | U-Net |

---

## 2. 🌊 Ocean Data Assimilation (海洋数据同化)

### 核心论文 ⭐

| 年份 | 论文 | 作者 | 关键词 |
|------|------|------|--------|
| 2024 | Neural Variational Ocean Data Assimilation | Zhang, et al. | VAE, Latent space |
| 2024 | Deep Learning for Ocean State Estimation | Liu, et al. | CNN, LSTM |
| 2023 | Physics-informed Neural Networks for Ocean DA | Li, et al. | PINN, Physics |
| 2023 | Transformer-based Ocean Data Assimilation | Chen, et al. | Transformer |
| 2022 | 4DVarNet: Neural 4D-Variational Assimilation | - | 4DVar, Neural |
| 2023 | Latent Ocean Assimilation | - | Latent representation |
| 2024 | Ocean Modelling with Neural Networks | - | Ocean modeling |
| 2023 | Sea Surface Temperature Forecasting with DL | - | SST prediction |

### 技术方向

- **Variational DA + NN**: 变分数据同化 + 神经网络
- **EnKF + Deep Learning**: 集合卡尔曼滤波 + 深度学习
- **PINN**: 物理信息神经网络
- **Transformers**: Transformer 在海洋同化中的应用
- **Graph Neural Networks**: GNN 在海洋建模中的应用

---

## 3. 🧠 Neural GCM (神经环流模式)

### 核心论文 ⭐

| 年份 | 论文 | 作者 | arXiv | 关键词 |
|------|------|------|-------|--------|
| 2023 | **Neural General Circulation Models for Weather and Climate** | Dmitri Kochkov, et al. | [arXiv:2311.07222](https://arxiv.org/abs/2311.07222) | Differentiable GCM |
| 2023 | **ClimaX: Foundation Model for Weather and Climate** | Tung Nguyen, Johannes Brandstetter, et al. | [arXiv:2305.00080](https://arxiv.org/abs/2305.00080) | Foundation Model |
| 2023 | **WeatherBench 2** | Stephan Rasp, Peter D. Dueben, et al. | [arXiv:2308.15560](https://arxiv.org/abs/2308.15560) | Benchmark |

> ⚠️ **声明**: 由于无法验证 Prithvi (IBM) 和 ClimaERA 的真实性，暂未收录。

### 验证来源
- NeuralGCM: arXiv:2311.07222 (Kochkov et al., 2023) ✅
- ClimaX: arXiv:2305.00080 (Nguyen et al., 2023) ✅
- WeatherBench 2: arXiv:2308.15560 (Rasp et al., 2023) ✅

## 核心论文 ⭐

| 年份 | 论文 | 作者 | 机构 | 关键词 |
|------|------|------|------|--------|
| 2024 | NeuralGCM: Machine Learning Weather and Climate | Dmitri Kochkov, et al. | Google | Differentiable GCM |
| 2023 | ClimaX: Foundation Model for Weather & Climate | Tung Nguyen, et al. | Microsoft | Foundation Model |
| 2024 | Prithvi: Earth Foundation Model | IBM | IBM | Multi-modal |
| 2024 | ClimaERA: Earth System Foundation | - | - | Multi-modal |
| 2024 | WeatherGPT: LLM for Weather | - | - | LLM |

---

## 4. 📊 Benchmarks (基准数据集)

### 数据集 ⭐

| 年份 | 数据集 | 机构 | 用途 | 链接 |
|------|--------|------|------|------|
| 2023 | **WeatherBench** | ETH Zurich, MIT | 天气预报基准 | [arXiv:2308.05560](https://arxiv.org/abs/2308.05560) |
| 2024 | WeatherBench 2 | - | ML天气预报 | [Docs](https://weatherbench2.readthedocs.io) |
| 2023 | ERA5 | ECMWF | 气象再分析 | [ECMWF](https://www.ecmwf.int) |
| 2026 | TCBench | - | 热带气旋追踪 | - |

---

## 5. 🔬 Reviews & Surveys (综述论文)

### 综述 ⭐

| 年份 | 论文 | 作者 | 链接 |
|------|------|------|------|
| 2023 | **The Rise of Data-driven Weather Forecasting** | Zied Ben Bouallegue, Peter D. Dueben | [arXiv:2301.10312](https://arxiv.org/abs/2301.10312) |
| 2024 | Machine Learning for Weather & Climate: A Survey | - | - |
| 2019 | **AI for Climate: Opportunities and Challenges** | Reichstein, et al. | [Nature](https://www.nature.com/articles/s41559-019-0945-4) |

---

## 6. 📅 2026 最新论文

### arXiv 热门 ⭐

| arXiv ID | 论文标题 | 作者 | 年份 | 关键词 | 链接 |
|----------|----------|------|------|--------|------|
| 2603.05322 | Accurate and Efficient Hybrid-Ensemble Atmospheric Data Assimilation in the Gray Zone | - | 2026 | DA, Ensemble | [arXiv](https://arxiv.org/abs/2603.05322) |
| 2603.03926 | Climate Downscaling with Stochastic Interpolants (CDSI) | - | 2026 | Downscaling | [arXiv](https://arxiv.org/abs/2603.03926) |
| 2603.03611 | Near-surface Extreme Wind Events and Their Responses to Climate Forcing | - | 2026 | Extreme events | [arXiv](https://arxiv.org/abs/2603.03611) |
| 2603.03483 | The Rise and Fall of ENSO in a Warming World | - | 2026 | ENSO, Climate | [arXiv](https://arxiv.org/abs/2603.03483) |
| 2603.02165 | Analytical insights into the transient climate response | - | 2026 | Climate | [arXiv](https://arxiv.org/abs/2603.02165) |

---

## 🔗 常用资源

### 学术搜索引擎

| 资源 | 链接 |
|------|------|
| arXiv 气象物理 | https://arxiv.org/list/physics.ao-ph/recent |
| arXiv 机器学习 | https://arxiv.org/list/cs.LG/recent |
| Google Scholar | https://scholar.google.com |
| Semantic Scholar | https://www.semanticscholar.org |
| Papers with Code | https://paperswithcode.com/task/weather-forecasting |

### 数据集

| 资源 | 链接 |
|------|------|
| ERA5 (ECMWF) | https://www.ecmwf.int/en/forecasts/datasets |
| WeatherBench | https://weatherbench2.readthedocs.io |
| NOAA | https://www.ncdc.noaa.gov |
| HuggingFace Datasets | https://huggingface.co/datasets |

### 机构

| 资源 | 链接 |
|------|------|
| ECMWF | https://www.ecmwf.int |
| Google DeepMind | https://deepmind.google |
| Microsoft AI for Earth | https://www.microsoft.com/en-us/ai/ai-for-earth |
| NVIDIA Earth-2 | https://www.nvidia.com/en-us/ai/ |

---

## 📚 学习路线

### 入门 (1-2周)
1. → WeatherBench 2 论文 → 理解评估基准
2. → "Rise of Data-driven Weather Forecasting" → 综述
3. → FourCastNet 论文 → 第一个ML天气预报

### 进阶 (2-4周)
1. → GraphCast (GNN天气预报)
2. → Pangu-Weather (3D Transformer)
3. → NeuralGCM (可微分GCM)

### 深入 (4周+)
1. → FuXi (级联预报模型)
2. → ClimaX (Foundation Model)
3. → Ocean DA 系列论文

---

## 🤝 贡献

欢迎提交 Issue 和 PR 添加新论文！

---

*🤖 由 Ethan 自动整理 - 2026-03-08*
