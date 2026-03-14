# ⚡ PINN + 数据同化

> 物理信息神经网络与数据同化的结合

## 核心思想

将物理方程作为损失函数约束嵌入神经网络：

### 物理损失
$$
\mathcal{L}_{physics} = \lambda_1 \mathcal{L}_{mass} + \lambda_2 \mathcal{L}_{momentum}
$$

### 质量守恒 (浅水方程)
$$
\frac{\partial \eta}{\partial t} + \frac{\partial (Hu)}{\partial x} + \frac{\partial (Hv)}{\partial y} = 0
$$

## 论文列表
- Physics-informed machine learning (2021)
- PINN for Fluid Dynamics
- Phase-resolved DA with PINN
