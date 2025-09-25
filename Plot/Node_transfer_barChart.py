import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat

transfer_names_raw = loadmat("x_link_intermode.mat")['x_link_intermode']
transfer_names = [str(x[0]) for x in transfer_names_raw.squeeze()]
transfer_flows_before = loadmat("Plot_data/Link_flow_before_0618_C.mat")['X_link_intermode_before'].flatten()
transfer_flows_mapped = loadmat("Plot_data/Link_flow_before_mapped_0618_C.mat")['X_link_intermode_before'].flatten()
transfer_flows_after = loadmat("Plot_data/Link_flow_after_0618_C.mat")['X_link_intermode_before'].flatten()
records = []


# === Step 1: 解析模式转移与起点节点 ===
for name, flow in zip(transfer_names, transfer_flows_before):
    match = re.match(r"x_(\w+)to(\w+)_(\d+)_Origin\d+", name)
    if match:
        mode_from, mode_to, node = match.groups()
        records.append({
            "Node": int(node),
            "From": mode_from,
            "To": mode_to,
            "Flow": float(flow)
        })

df = pd.DataFrame(records)

# === Step 2: 对每个 Node 和 To 模式进行聚合 ===
pivot_df = df.pivot_table(index="Node", columns="From", values="Flow", aggfunc="sum", fill_value=0)
pivot_df = pivot_df.sort_index()

# === Step 3: 绘制堆叠条形图 ===
colors = {
    "Car": "#1f77b4",
    "Bus": "#ff7f0e",
    "Bike": "#2ca02c",
    "Metro": "#d62728",
    "Rail": "#9467bd"
}

ax = pivot_df.plot(kind="bar", stacked=True, figsize=(12, 6),
                   color=[colors.get(col, "#999999") for col in pivot_df.columns])

plt.xlabel("Node")
plt.ylabel("Total Transfer Flow")
plt.title("Outgoing Mode Distribution per Node (Before Intervention)")
plt.legend(title="From Car Mode")
plt.tight_layout()
plt.show()
