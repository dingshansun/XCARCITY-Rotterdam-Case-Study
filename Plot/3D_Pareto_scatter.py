import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

# 假设你已经有这些数据，分别是干预前（Before）和干预后（After）的三目标值：
# X: Private Car Flow, Y: Total Travel Cost, Z: Public Transport Cost
# data = loadmat("pareto_result_0413_before.mat")
data = loadmat("Original_data_3D/Pareto_3D_before.mat")
# 干预前
Obj = data["Obj"]  # shape = (150, 3)
Xb, Yb, Zb = Obj[:, 0], Obj[:, 2], Obj[:, 1]

# data = loadmat("pareto_result_0413_after.mat")
data = loadmat("Original_data_3D/Pareto_3D_after.mat")
# 干预后
Obj = data["Obj"]  # shape = (150, 3)
Xa, Ya, Za = Obj[:, 0], Obj[:, 2], Obj[:, 1]

car_flow_all = np.concatenate([Zb, Za])
vmin = np.min(car_flow_all)
vmax = np.max(car_flow_all)

# 创建图形
plt.figure(figsize=(10, 7))

# 干预前：圆点，统一 colormap
scatter1 = plt.scatter(Xb, Yb, c=Zb, cmap='Greys', marker='o',
                       edgecolors='k', label='Before Intervention',
                       vmin=vmin, vmax=vmax)

# 干预后：三角形，使用相同 colormap
scatter2 = plt.scatter(Xa, Ya, c=Za, cmap='Greys', marker='^',
                       edgecolors='k', label='After Intervention',
                       vmin=vmin, vmax=vmax)

# 添加 colorbar
cbar = plt.colorbar(scatter2)
cbar.set_label('Private Car Flow')

# 坐标轴、图例与排版
plt.xlabel('Public Transport Cost')
plt.ylabel('Total Travel Cost')
plt.title('PT Cost vs Travel Cost (Color = Private Car Flow)\nShape = Intervention Status')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
