import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat

def load_mode_flows(mat_path, linkname_path):
    link_names_raw = loadmat(linkname_path)['x_link_unimode']
    link_flows = loadmat(mat_path)['X_link_unimode_before'].flatten()
    link_names = [str(x[0]) for x in link_names_raw.squeeze()]

    records = []
    for name, flow in zip(link_names, link_flows):
        match = re.match(r'x_(\w+?)_', name)
        if match:
            mode = match.group(1)
            records.append({"Mode": mode, "Flow": float(flow)})
    df = pd.DataFrame(records)
    return df.groupby('Mode')['Flow'].sum().to_dict()

# === 路径设定（请替换为你自己的路径）===
linkname_path = "x_link_unimode.mat"
path_before   = "Plot_data/Link_flow_before_0616_C.mat"
path_mapped   = "Plot_data/Link_flow_before_mapped_0616_C.mat"
path_after    = "Plot_data/Link_flow_after_0616_C.mat"

# === 提取每个模式的总流量 ===
flow_before = load_mode_flows(path_before, linkname_path)
flow_mapped = load_mode_flows(path_mapped, linkname_path)
flow_after  = load_mode_flows(path_after,  linkname_path)

# === 构造 DataFrame ===
# modes = sorted(set(flow_before) | set(flow_mapped) | set(flow_after))
modes = ["Car", "Bus", "Bike", "Metro", "Rail"]
df_plot = pd.DataFrame({
    'Mode': modes,
    'Before': [flow_before.get(m, 0) for m in modes],
    'Mapped': [flow_mapped.get(m, 0) for m in modes],
    'After':  [flow_after.get(m, 0) for m in modes],
})

# === 可视化 ===
x = np.arange(len(modes))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width, df_plot['Before'], width, label='Before Intervention', color='#1f77b4')
bars2 = ax.bar(x,         df_plot['Mapped'], width, label='Mapped in After Network', color='#ff7f0e')
bars3 = ax.bar(x + width, df_plot['After'],  width, label='After Intervention', color='#2ca02c')

# 标签与细节
ax.set_xlabel("Mode", fontsize=13)
ax.set_ylabel("Total Flow", fontsize=13)
ax.set_title("Mode-wise Total Flow Comparison (3 Scenarios)", fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(modes, fontsize=12)
ax.legend()
ax.grid(True, axis='y', linestyle='--', alpha=0.5)

# 添加数值标签
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()
