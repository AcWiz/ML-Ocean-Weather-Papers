# 📚 神经数据同化相关论文集
## Neural Data Assimilation Papers Collection
**更新日期**: 2026-03-12

---

## 一、扩散模型 + 数据同化 (Diffusion for DA)

| 论文 | 年份 | 核心贡献 | 类型 |
|------|------|----------|------|
| **LO-SDA** (Latent Optimization for Score-based DA) | 2026 | 潜在空间score优化 | ⭐⭐⭐⭐⭐ |
| **GenDA** (Generative DA) | 2026 | Classifier-free diffusion guidance | ⭐⭐⭐⭐ |
| **The Ensemble Schrödinger Bridge Filter** | 2026 | 非线性DA新框架 | ⭐⭐⭐⭐ |
| **IEnSF** (Iterative Ensemble Score Filter) | 2026 | 迭代ensemble score filter | ⭐⭐⭐⭐ |
| **Fire-EnSF** | 2026 | 野火蔓延同化 | ⭐⭐⭐ |
| **D-Flow SGLD** | 2026 | Flow matching for inverse problems | ⭐⭐⭐⭐ |
| **Control-Augmented Autoregressive Diffusion** | 2026 | 控制增强扩散 | ⭐⭐⭐ |
| **Diffusion-Based Probabilistic Streamflow** | 2026 | 概率流预测 | ⭐⭐⭐ |

---

## 二、神经4DVar (Neural 4DVar)

| 论文 | 年份 | 核心贡献 |
|------|------|----------|
| **Neural 4DVar** 系列 | 2023-2025 | 神经网络替代数值模式 |
| **Variational Neural DA** | 2024 | 变分框架 |

---

## 三、海洋/大气预报 (Ocean & Weather ML)

| 论文 | 年份 | 核心贡献 |
|------|------|----------|
| **GraphCast** | 2023 | 图神经网络全球预报 |
| **Pangu-Weather** | 2023 | 3D Earth Transformer |
| **NeuralGCM** | 2023 | 神经参数化环流模式 |
| **Ensemble Graph Neural Networks for SST** | 2026 | 概率海温预报 |
| **Generative deep learning for climate records** | 2026 | 气候记录重建 |

---

## 四、物理约束神经方法 (Physics-Informed)

| 论文 | 年份 | 核心贡献 |
|------|------|----------|
| **PINN-DA** | 2024 | 物理信息神经DA |
| **PDE-Constrained Diffusion** | 2026 | 扩散模型+物理约束 |
| **Function-Space Decoupled Diffusion** | 2026 | 碳捕集正向/逆向建模 |

---

## 五、关键空白点 (Research Gaps)

1. **海洋浅水方程 + 扩散模型** - 几乎空白 ⭐⭐⭐⭐⭐
2. **稀疏观测专门设计** - 海洋卫星观测 ⭐⭐⭐⭐
3. **物理守恒 + 海洋DA** - 海洋层结约束 ⭐⭐⭐⭐
4. **非线性DA** - 突破EnKF线性假设 ⭐⭐⭐⭐

---

## 六、推荐阅读顺序

### 入门
1. LO-SDA (2026) - 理解score-based DA基础
2. GraphCast/Pangu-Weather - 了解ML预报现状

### 进阶
3. Schrödinger Bridge Filter - 非线性DA
4. NeuralGCM - 神经参数化思路

### 深入
5. D-Flow SGLD - Flow matching
6. PINN-DA - 物理约束

---

*持续更新中...*
