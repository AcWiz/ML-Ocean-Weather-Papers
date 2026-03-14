# 🧠 神经变分同化

> 神经网络与传统4DVar/EnKF的结合

## 论文列表

| 年份 | 论文 | arXiv | 核心贡献 |
|------|------|-------|----------|
| 2022 | 4DVarNet-SSH | 2211.05904 | 神经变分+海面高度 |
| 2023 | Neural Operator Ocean Forecast | 2308.11814 | 神经算子预报 |
| 2023 | Ensemble Kalman Filtering Meets GP | 2312.05910 | EnKF+高斯过程 |
| 2024 | Neural Incremental DA | 2402.xxx | 增量学习方法 |
| 2023 | Deep Bayesian Filter for DA | 2305.xxx | 深度贝叶斯滤波 |

## 核心方法

### 4DVar目标函数
$$
\mathcal{J}(x) = \frac{1}{2}(x-x_b)^T B^{-1}(x-x_b) + \frac{1}{2}(y-Hx)^T R^{-1}(y-Hx)
$$

### EnKF更新
$$
x^f_a = x^f + K(y - Hx^f), \quad K = PH^T(HPH^T + R)^{-1}
$$
