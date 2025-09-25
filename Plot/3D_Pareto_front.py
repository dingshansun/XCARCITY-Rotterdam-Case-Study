import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

# === Pareto front 提取函数（针对最小化目标） ===
def extract_pareto_front(X, Y):
    points = np.column_stack((X, Y))
    pareto_mask = np.ones(points.shape[0], dtype=bool)
    for i in range(points.shape[0]):
        if pareto_mask[i]:
            # 若存在其他点在所有目标上都小于等于该点（且至少一个更小），则该点不是Pareto最优
            dominates = (points[:, 0] <= points[i, 0]) & (points[:, 1] <= points[i, 1])
            dominates[i] = False
            if np.any(dominates):
                pareto_mask[i] = False
    pareto_points = points[pareto_mask]
    # 按照第一目标排序以利于画线
    pareto_points = pareto_points[np.argsort(pareto_points[:, 0])]
    return pareto_points[:, 0], pareto_points[:, 1]


# === 加载数据 ===
data_before = loadmat("Original_data_3D/Pareto_3D_before.mat")
Obj_before = data_before["Obj"]
Xb, Yb, Zb = Obj_before[:, 0], Obj_before[:, 2], Obj_before[:, 1]

data_after = loadmat("Original_data_3D/Pareto_3D_after.mat")
Obj_after = data_after["Obj"]
Xa, Ya, Za = Obj_after[:, 0], Obj_after[:, 2], Obj_after[:, 1]

car_flow_all = np.concatenate([Zb, Za])
vmin = np.min(car_flow_all)
vmax = np.max(car_flow_all)

# === 提取Pareto边界（最优解） ===
Xb_pareto, Yb_pareto = extract_pareto_front(Xb, Yb)
Xa_pareto, Ya_pareto = extract_pareto_front(Xa, Ya)

# === 绘图 ===
plt.figure(figsize=(10, 7))

# 散点图
plt.scatter(Xb, Yb, c=Zb, cmap='Greys', marker='o', edgecolors='k',
            label='Before Intervention', vmin=vmin, vmax=vmax)
plt.scatter(Xa, Ya, c=Za, cmap='Greys', marker='^', edgecolors='k',
            label='After Intervention', vmin=vmin, vmax=vmax)

# Pareto 曲线
plt.plot(Xb_pareto, Yb_pareto, 'k--', linewidth=2, label='Before Intervention Pareto Front')
plt.plot(Xa_pareto, Ya_pareto, 'r-', linewidth=2, label='After Intervention Pareto Front')

# colorbar 和样式
cbar = plt.colorbar()
cbar.set_label('Private Car Flow')

plt.xlabel('Total Travel Cost')
plt.ylabel('Public Transport Cost')
plt.title('PT Cost vs Travel Cost (Color = Private Car Flow)\nPareto Fronts: Minimization')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
