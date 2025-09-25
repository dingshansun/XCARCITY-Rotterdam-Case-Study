import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.io import loadmat

transfer_names_raw = loadmat("x_link_intermode.mat")['x_link_intermode']
transfer_names = [str(x[0]) for x in transfer_names_raw.squeeze()]
transfer_flows_before = loadmat("Plot_data/Link_flow_before_0616_A.mat")['X_link_intermode_before'].flatten()
transfer_flows_mapped = loadmat("Plot_data/Link_flow_before_mapped_0616_A.mat")['X_link_intermode_before'].flatten()
transfer_flows_after = loadmat("Plot_data/Link_flow_after_0616_A.mat")['X_link_intermode_before'].flatten()

# === Step 1: 解析模式转移对 ===
records = []
for name, flow_b, flow_a, flow_m in zip(transfer_names, transfer_flows_before, transfer_flows_after, transfer_flows_mapped):
    match = re.match(r'x_(\w+)to(\w+)_\d+_Origin\d+', name)
    if match:
        from_mode, to_mode = match.groups()
        records.append({
            "From": from_mode,
            "To": to_mode,
            "Flow_Before": flow_b,
            "Flow_After": flow_a,
            "Flow_mapped": flow_m
        })

df = pd.DataFrame(records)
df["Delta"] = df["Flow_After"] - df["Flow_Before"]

# === Step 2: 聚合并构造模式转移矩阵 ===
pivot = df.pivot_table(index="From", columns="To", values="Delta", aggfunc="sum", fill_value=0)
# pivot = df.pivot_table(index="From", columns="To", values="Flow_Before", aggfunc="sum", fill_value=0)
# === 指定模式顺序 ===
mode_order = ["Car", "Bus", "Bike", "Metro", "Rail"]
pivot = pivot.reindex(index=mode_order, columns=mode_order, fill_value=0)
# === Step 3: 绘制 heatmap ===
plt.figure(figsize=(6, 6))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="RdYlGn", center=0,
            cbar_kws={"label": "Flow"})
plt.title("Change in Transfer Flow Between Modes (After - Before)")
# plt.title("Transfer Flow Between Modes (Before)")
plt.xlabel("To")
plt.ylabel("From")
plt.tight_layout()
plt.show()
