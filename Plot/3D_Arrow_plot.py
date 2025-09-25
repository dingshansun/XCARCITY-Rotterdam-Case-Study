import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

data = loadmat("Pareto_move.mat")

Obj_before = data["Objective_before"]  # shape = (30, 3)
Xb, Yb, Zb = Obj_before[:, 1], Obj_before[:, 0], Obj_before[:, 2]

obj_after = data["Objective_after"]  # shape = (30, 3)
Xa, Ya, Za = obj_after[:, 1], obj_after[:, 0], obj_after[:, 2]


# 颜色映射基于干预前或后的 PC flow（任选）
color_by_total = np.concatenate([Zb, Za])  # 拼接统一映射范围
norm = plt.Normalize(vmin=np.min(color_by_total), vmax=np.max(color_by_total))
cmap = plt.cm.Greys  

plt.figure(figsize=(11, 8))
ax = plt.gca()

# 画箭头（统一颜色）
for i in range(len(Zb)):
    ax.annotate("",
        xy=(Xa[i], Ya[i]), xycoords='data',
        xytext=(Xb[i], Yb[i]), textcoords='data',
        arrowprops=dict(arrowstyle="->", color='dimgray', lw=1.2),
        annotation_clip=False)

# before: 按 Zb 映射颜色
sc1 = ax.scatter(Xb, Yb, c=Zb, cmap=cmap, norm=norm,
                 marker='o', edgecolors='black', linewidths=0.5, label='Before')

# after: 按 Za 映射颜色
sc2 = ax.scatter(Xa, Ya, c=Za, cmap=cmap, norm=norm,
                 marker='^', edgecolors='black', linewidths=0.5, label='After')

# 添加颜色条
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label("Public Transport Cost")

# 标签和图例
ax.set_xlabel("Private Car Flow")
ax.set_ylabel("Total Travel Cost")
ax.set_title("Shift of Solutions in Objective Space\n(2D with Color = PC Flow, Arrows = Before → After)")
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.show()