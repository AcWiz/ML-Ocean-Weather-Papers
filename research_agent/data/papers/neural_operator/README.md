# 🔢 神经算子

> 学习函数到函数的映射

## 核心模型

| 模型 | 年份 | 论文 | 特点 |
|------|------|------|------|
| FNO | 2021 | 2010.08895 | FFT卷积 |
| DeepONet | 2019 | 1912.09397 | 深度算子 |
| GNO | 2022 | 2208.xxx | 图神经算子 |
| Fourier GNO | 2023 | 2301.xxx | 傅里叶GNO |

## 核心公式

### 神经算子映射
$$
\mathcal{G}_\theta : u \mapsto v, \quad v(x) = \sigma(Wx + b + \mathcal{K}[u](x))
$$

### FNO核心 (频域卷积)
$$
v(x) = \sigma(\mathcal{F}^{-1}(\mathcal{F}(u) \cdot R)\})
$$
