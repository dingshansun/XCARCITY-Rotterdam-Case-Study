import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

# 加载三组数据
before = loadmat("Original_data_3D/Pareto_3D_before.mat")["Obj"]
after = loadmat("Original_data_3D/Pareto_3D_after.mat")["Obj"]
after_map = loadmat("Original_data_3D/Pareto_3D_after_map.mat")["Objective_after"]

# 分别解包数据
Xb, Yb, Cb = before[:, 0], before[:, 1], before[:, 2]       # TTC, PT cost, PC flow
Xa, Ya, Ca = after[:, 0], after[:, 1], after[:, 2]
Xm, Ym, Cm = after_map[:, 0], after_map[:, 1], after_map[:, 2]

# 提取 Pareto 前沿（最小化问题）
def extract_pareto_front(X, Y):
    points = np.column_stack((X, Y))
    pareto_mask = np.ones(points.shape[0], dtype=bool)
    for i in range(points.shape[0]):
        if pareto_mask[i]:
            dominates = (points[:, 0] <= points[i, 0]) & (points[:, 1] <= points[i, 1])
            dominates[i] = False
            if np.any(dominates):
                pareto_mask[i] = False
    pareto_points = points[pareto_mask]
    pareto_points = pareto_points[np.argsort(pareto_points[:, 0])]
    return pareto_points[:, 0], pareto_points[:, 1]

Xb_p, Yb_p = extract_pareto_front(Xb, Yb)
Xa_p, Ya_p = extract_pareto_front(Xa, Ya)
Xm_p, Ym_p = extract_pareto_front(Xm, Ym)

# 统一 color scale
C_all = np.concatenate([Cb, Ca, Cm])
vmin, vmax = C_all.min(), C_all.max()

# === 绘图 ===
plt.figure(figsize=(10, 7))

# 三组散点
plt.scatter(Xb, Yb, c=Cb, cmap='Greys', marker='o', edgecolors='k', label='Before Intervention', vmin=vmin, vmax=vmax, alpha=0.5)
plt.scatter(Xa, Ya, c=Ca, cmap='Greys', marker='^', edgecolors='k', label='After Intervention', vmin=vmin, vmax=vmax, alpha=0.5)
plt.scatter(Xm, Ym, c=Cm, cmap='Greys', marker='s', edgecolors='k', label='Mapped After (No Optimization)', vmin=vmin, vmax=vmax, alpha=0.5)

# Pareto 曲线
plt.plot(Xb_p, Yb_p, linestyle='--', color='black', linewidth=2, label='Before Pareto Front')
plt.plot(Xa_p, Ya_p, linestyle='-', color='red', linewidth=2, label='After Pareto Front')
plt.plot(Xm_p, Ym_p, linestyle='-.', color='blue', linewidth=2, label='Mapped After Pareto Front')

# 图例与样式
plt.xlabel('Total Travel Cost')
plt.ylabel('Private Car Flow')
plt.title('PT Cost vs Travel Cost (Color = Private Car Flow)\nPareto Fronts: Minimization')
plt.colorbar(label='Public Transport Cost')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
