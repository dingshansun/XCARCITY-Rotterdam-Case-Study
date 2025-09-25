import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

# === 加载数据 ===
# data = loadmat("0521/Pareto_move_2D_all.mat")

Obj_before = loadmat("0521/2025-05-21-N150-before.mat")["Obj"]      # 干预前最优解（起点）
# Obj_before_change = loadmat("0521/2025-06-19-N150-before.mat")["Obj"] 
# Obj_before_increased = loadmat("0521/2025-05-31-N200-before.mat")["Obj"]
Obj_after_mapped = loadmat("0521/0521_mapped.mat")["Objective_after"] # 干预前最优解在干预后网络下的结果（箭头终点）

# data_after_opt = loadmat("New_folder_2D/Pareto_2D_after.mat")
# Obj_after_front = loadmat("0521/2025-05-21-N150-after.mat")["Obj"]  # 干预后最优解集（目标 Pareto front）
# Obj_after_front_change = loadmat("0521/2025-06-10-N150-after.mat")["Obj"]
Obj_after_front_increased = loadmat("0521/2025-05-26-N250-after.mat")["Obj"] 
# Obj_after_front_increased_2 = loadmat("0521/2025-05-31-N250-after.mat")["Obj"] 

# === 解包 ===
Xb, Yb = Obj_before[:, 0], Obj_before[:, 1]
# Xbc, Ybc = Obj_before_change[:, 0], Obj_before_change[:, 1]
# Xbi, Ybi = Obj_before_increased[:, 0], Obj_before_increased[:, 1]

Xm, Ym = Obj_after_mapped[:, 0], Obj_after_mapped[:, 2]

Xf, Yf = Obj_after_front_increased[:, 0], Obj_after_front_increased[:, 1]
# Xfc, Yfc = Obj_after_front_change[:, 0], Obj_after_front_change[:, 1]
# Xf1, Yf1 = Obj_after_front_increased[:, 0], Obj_after_front_increased[:, 1]
# Xf2, Yf2 = Obj_after_front_increased_2[:, 0], Obj_after_front_increased_2[:, 1]


# === 绘图 ===
plt.figure(figsize=(11, 8))
ax = plt.gca()

## 画箭头：Before → Mapped
for i in range(0, len(Xb), 4):
    ax.annotate("",
        xy=(Xm[i], Ym[i]), xycoords='data',
        xytext=(Xb[i], Yb[i]), textcoords='data',
        arrowprops=dict(arrowstyle="->", color='gray', lw=1, alpha=0.4),
        annotation_clip=False)

# 画点
ax.scatter(Xb, Yb, c='white', edgecolors='black', marker='o', label='Baseline scenario')
# ax.scatter(Xbc, Ybc, c='white', edgecolors='red', marker='^', label='Before Intervention (Optimal-Change)')

ax.scatter(Xm, Ym, c='black', marker='^', label='Low-car zone (LCZ) scenario')
ax.scatter(Xf, Yf, c='red', marker='s', label='LCZ reoptimized traffic management (LCZ-RTM) scenario')
# ax.scatter(Xfc, Yfc, c='red', marker='^', label='After Intervention (Optimal-Change')
# ax.scatter(Xf1, Yf1, c='red', marker='o', label='After Intervention (Optimal-Increased)')
# ax.scatter(Xf2, Yf2, c='red', marker='^', label='After Intervention (Optimal-Increased-2)')
# print(f"Before: {len(Xb)} points, unique: {len(np.unique(np.array(list(zip(Xb, Yb))), axis=0))}")
# print(f"After:  {len(Xf)} points, unique: {len(np.unique(np.array(list(zip(Xf, Yf))), axis=0))}")

# Extra solution points (by manual trying)
# ax.scatter(3133561, 15200, c='red', marker='*', s=100, label='Manual Selected Solution')
# ax.scatter(3133907, 14800, c='red', marker='*', s=100)

# 样式
ax.set_xlabel("Total Travel Cost [€]", fontsize=12)
ax.set_ylabel("Public Transport Cost [€]", fontsize=12)
ax.set_title("Objective Comparison: TTC vs PT Cost\nArrows: Baseline → LCZ Scenario", fontsize=12)
ax.grid(True)
ax.legend()
plt.tight_layout()
plt.show()
