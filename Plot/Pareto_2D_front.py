import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.interpolate import make_interp_spline
from statsmodels.nonparametric.smoothers_lowess import lowess

# === 加载数据 ===
data = loadmat("Plot_data/Pareto_move_2D_all.mat")
Obj_before = data["Objective_before"]      # 干预前最优解（起点）
Obj_after_mapped = data["Objective_after"] # 干预前最优解在干预后网络下的结果（箭头终点）

data_after_opt = loadmat("New_folder_2D/Pareto_2D_after.mat")
Obj_after_front = data_after_opt["Obj"]  # 干预后最优解集（目标 Pareto front）

# === 解包 ===
Xb, Yb = Obj_before[:, 0], Obj_before[:, 1]
Xm, Ym = Obj_after_mapped[:, 0], Obj_after_mapped[:, 2]
Xf, Yf = Obj_after_front[:, 0], Obj_after_front[:, 1]

# === 拟合函数（使用样条插值） ===
def fit_curve(x, y, frac=0.2):  # frac 可调整平滑程度
    sorted_idx = np.argsort(x)
    x_sorted = x[sorted_idx]
    y_sorted = y[sorted_idx]
    smoothed = lowess(y_sorted, x_sorted, frac=frac, return_sorted=True)
    return smoothed[:, 0], smoothed[:, 1]

Xb_fit, Yb_fit = fit_curve(Xb, Yb)
Xm_fit, Ym_fit = fit_curve(Xm, Ym)
Xf_fit, Yf_fit = fit_curve(Xf, Yf)

# === 绘图 ===
plt.figure(figsize=(11, 8))
ax = plt.gca()

# 箭头
for i in range(0, len(Xb), 4):
    ax.annotate("",
        xy=(Xm[i], Ym[i]), xycoords='data',
        xytext=(Xb[i], Yb[i]), textcoords='data',
        arrowprops=dict(arrowstyle="->", color='gray', lw=1, alpha=0.4),
        annotation_clip=False)

# 拟合曲线
ax.plot(Xb_fit, Yb_fit, color='black', linestyle='--', linewidth=2, label='Before Intervention (Optimal) - Curve')
ax.plot(Xm_fit, Ym_fit, color='black', linestyle='-.', linewidth=2, label='Mapped in After Network - Curve')
ax.plot(Xf_fit, Yf_fit, color='red', linestyle='-', linewidth=2, label='After Intervention (Optimal) - Curve')

# 原始散点
ax.scatter(Xb, Yb, c='white', edgecolors='black', marker='o', label='Before (Points)', alpha=0.1)
ax.scatter(Xm, Ym, c='black', marker='^', label='Mapped (Points)', alpha=0.1)
ax.scatter(Xf, Yf, c='red', marker='s', label='After (Points)', alpha=0.1)

# 样式
ax.set_xlabel("Total Travel Cost [€]", fontsize=12)
ax.set_ylabel("Public Transport Cost [€]", fontsize=12)
ax.set_title("Objective Comparison: TTC vs PT Cost\nArrows: Before → Mapped After", fontsize=14)
ax.grid(True)
ax.legend()
plt.tight_layout()
plt.show()
