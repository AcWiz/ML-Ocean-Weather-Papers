# 🔮 扩散模型 + 数据同化

> 扩散模型在数据同化中的应用

## 论文列表

### 2024年

| 论文 | arXiv | 核心贡献 |
|------|-------|----------|
| Score-Based Diffusion for Atmospheric DA | 2403.07832 | 分数网络+郎之万动力学 |
| Latent Diffusion for Scientific Simulation | 2401.00045 | 潜在空间扩散 |
| Training-Free DA with GenCast | 2401.xxx | 无训练同化 |

### 2023年

| 论文 | arXiv | 核心贡献 |
|------|-------|----------|
| Diffusion Models for Data Assimilation | 2310.20182 | 条件生成框架 |
| Generative Diffusion for Weather | 2310.xxx | 天气扩散 |

### 2022年

| 论文 | arXiv | 核心贡献 |
|------|-------|----------|
| Diffusion Probabilistic Models for DA | 2206.xxx | 早期探索 |

---

## 核心公式

### 扩散前向过程
$$
q(x_t|x_0) = \mathcal{N}(\sqrt{\bar{\alpha}_t}x_0, (1-\bar{\alpha}_t)I)
$$

### 条件逆向过程
$$
p_\theta(x_{t-1}|x_t, y) = \mathcal{N}(\mu_\theta(x_t, t, y), \sigma_t^2 I)
$$
