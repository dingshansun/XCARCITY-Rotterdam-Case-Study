import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

# 加载数据（双目标）
data = loadmat("Pareto_move_2D_all.mat")
Obj_before = data["Objective_before"]  # shape = (N, 2 or 3)
Obj_after = data["Objective_after"]

# 仅提取 TTC 和 PT Cost 两个目标（假设为前两列）
Xb, Yb = Obj_before[:, 0], Obj_before[:, 1]
Xa, Ya = Obj_after[:, 0], Obj_after[:, 2]

# 绘图
plt.figure(figsize=(10, 7))
ax = plt.gca()

# 画偏移箭头（统一颜色）
for i in range(len(Xb)):
    ax.annotate("",
        xy=(Xa[i], Ya[i]), xycoords='data',
        xytext=(Xb[i], Yb[i]), textcoords='data',
        arrowprops=dict(arrowstyle="->", color='gray', lw=1.0),
        annotation_clip=False)

# 干预前点（圆）
ax.scatter(Xb, Yb, marker='o', color='lightgray', edgecolors='black', label='Opt. Before')

# 干预后点（三角）
ax.scatter(Xa, Ya, marker='^', color='black', edgecolors='black', label='After')

# 图形设置
ax.set_xlabel("Total Travel Cost [€]")
ax.set_ylabel("Public Transport Cost [€]")
ax.set_title("Objective Shift: TTC vs PT Cost\n(Arrow = Opt. Before → After)")
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.show()
