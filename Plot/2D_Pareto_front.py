import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

# 读取数据（两个目标：TTC 与 PTC）
data_before_opt = loadmat("New_folder_2D/Pareto_2D_before.mat")
data_after_opt = loadmat("New_folder_2D/Pareto_2D_after.mat")

Obj_b = data_before_opt["Obj"]  # shape: (N, 2) or (N, ≥2) —只用前两列
Obj_a = data_after_opt["Obj"]

# 仅提取 TTC 和 PTC 两个目标
TTC_b, PTC_b = Obj_b[:, 0], Obj_b[:, 1]
TTC_a, PTC_a = Obj_a[:, 0], Obj_a[:, 1]

# 绘图
plt.figure(figsize=(10, 7))

# 干预前：圆点
plt.scatter(TTC_b, PTC_b, marker='o', color='gray',
            edgecolors='k', label='Before Intervention Optimal')

# 干预后：三角形
plt.scatter(TTC_a, PTC_a, marker='^', color='black',
            edgecolors='k', label='After Intervention Optimal')

# 坐标轴、图例、标题
plt.xlabel('Total Travel Cost [€]')
plt.ylabel('Public Transport Cost [€]')
plt.title('Pareto Comparison: TTC vs PT Cost')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
