import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat

# === Step 1: Load data ===
# 假设你已经加载好 name 和 flow 数组：
transfer_names_raw = loadmat("x_link_desti.mat")['x_link_desti']
desti_names = [str(x[0]) for x in transfer_names_raw.squeeze()]
desti_flows_before = loadmat("Plot_data/Link_flow_before_0618_A.mat")['X_link_desti'].flatten()
desti_flows_before_mapped = loadmat("Plot_data/Link_flow_before_mapped_0618_A.mat")['X_link_desti'].flatten()
desti_flows_after = loadmat("Plot_data/Link_flow_after_0618_A.mat")['X_link_desti'].flatten()


# === Step 2: Parse mode and destination ===
records = []
for name, flow in zip(desti_names, desti_flows_after):
    match = re.match(r'x_(\w+?)_\d+to(D\d+)_Origin\d+', name)
    if match:
        mode, dest = match.groups()
        records.append({"Mode": mode, "Destination": dest, "Flow": float(flow)})

df = pd.DataFrame(records)

# === Step 3: Pivot table for stacked bar chart ===
pivot_df = df.pivot_table(index='Destination', columns='Mode', values='Flow', aggfunc='sum', fill_value=0)

# 保持 mode 顺序一致
mode_order = ['Car', 'Bus', 'Bike', 'Metro', 'Rail']
pivot_df = pivot_df.reindex(columns=mode_order)

def sort_key(label):
    return int(label[1:])  # "D12" -> 12
pivot_df = pivot_df.reindex(sorted(pivot_df.index, key=sort_key))

# === Step 4: Plot ===
colors = {
    "Car": "#1f77b4",
    "Bus": "#ff7f0e",
    "Bike": "#2ca02c",
    "Metro": "#d62728",
    "Rail": "#9467bd"
}
ax = pivot_df.plot(kind='bar', stacked=True, figsize=(10, 6), color=[colors.get(col, "#999999") for col in pivot_df.columns])

ax.set_xlabel("Destination Node")
ax.set_ylabel("Total Incoming Flow")
ax.set_title("Mode Share per Destination Node (After Intervention)")
ax.legend(title="Mode", bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.show()
