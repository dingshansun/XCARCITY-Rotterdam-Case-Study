from scipy.io import loadmat
import re
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ==== Step 1: 加载数据 ====
link_flow = loadmat("Plot_data/Link_flow_after_0616_A.mat")['X_link_unimode_before'].flatten()
link_names_data = loadmat("x_link_unimode.mat")
link_names_raw = link_names_data['x_link_unimode'].squeeze()
transfer_flows = loadmat("Plot_data/Link_flow_after_0616_A.mat")['X_link_intermode_before'].flatten()
transfer_names_raw = loadmat("x_link_intermode.mat")['x_link_intermode']

final_mode_flow = {}
for name_raw, flow in zip(link_names_raw, link_flow):
    name = str(name_raw[0])
    match = re.match(r'x_(\w+?)_', name)
    if match:
        mode = match.group(1)
        if mode not in final_mode_flow:
            final_mode_flow[mode] = 0
        final_mode_flow[mode] += flow

mode_names = ['Car', 'Bus', 'Bike', 'Metro', 'Rail']

transfer_matrix = pd.DataFrame(columns=['From', 'To', 'Flow'])

for name_raw, flow in zip(transfer_names_raw, transfer_flows):
    if isinstance(name_raw, (list, tuple, np.ndarray)):
        name = str(name_raw[0])
    else:
        name = str(name_raw)
    name = name.strip("[]'\"")
    match = re.match(r"x_(\w+)to(\w+)_\d+_Origin\d+", name)
    if match:
        from_mode, to_mode = match.groups()
        transfer_matrix.loc[len(transfer_matrix)] = [from_mode, to_mode, float(flow)]

# Step 3: 构造 origin mode flow
origin_mode_flow = {}
for mode in mode_names:
    total = final_mode_flow.get(mode, 0)
    inflow = transfer_matrix[transfer_matrix['To'] == mode]['Flow'].sum()
    outflow = transfer_matrix[transfer_matrix['From'] == mode]['Flow'].sum()
    origin_mode_flow[mode] = total - inflow + outflow

# Step 4: 桑基图绘制
node_labels = [f"{m} (From)" for m in mode_names] + [f"{m} (To)" for m in mode_names]
node_index = {label: i for i, label in enumerate(node_labels)}

color_map = {
    "Car": "rgba(141,160,203,0.3)",
    "Bus": "rgba(252,141,98,0.3)",
    "Bike": "rgba(102,194,165,0.3)",
    "Metro": "rgba(231,138,195,0.3)",
    "Rail": "rgba(166,216,84,0.3)"
}
color_map_trans = {
    "Car": "rgba(141,160,203,0.6)",
    "Bus": "rgba(252,141,98,0.6)",
    "Bike": "rgba(102,194,165,0.6)",
    "Metro": "rgba(231,138,195,0.6)",
    "Rail": "rgba(166,216,84,0.6)"
}
node_color_map = {
    "Car": "rgba(141,160,203,1)",
    "Bus": "rgba(252,141,98,1)",
    "Bike": "rgba(102,194,165,1)",
    "Metro": "rgba(231,138,195,1)",
    "Rail": "rgba(166,216,84,1)"
}

# 统计汇总 transfer
agg_transfer = transfer_matrix.groupby(['From', 'To'])['Flow'].sum().reset_index()

sankey_sources = []
sankey_targets = []
sankey_values = []
sankey_labels = []
sankey_colors = []

# 1. 先画 transfer（用更透明色，颜色可根据 from_mode/to_mode/混合自选）
# 1. 先画 transfer（只画非零流量）
for _, row in agg_transfer.iterrows():
    if row['Flow'] > 1e-1:  # 只画非零流量
        src = node_index[f"{row['From']} (From)"]
        tgt = node_index[f"{row['To']} (To)"]
        sankey_sources.append(src)
        sankey_targets.append(tgt)
        sankey_values.append(row['Flow'])
        sankey_labels.append(f"{row['From']}→{row['To']}: {int(row['Flow'])}")
        sankey_colors.append(color_map_trans[row['From']])


# 2. 再画 diagonal 自身流（非transfer部分，主色，不透明）
for mode in mode_names:
    total_origin = origin_mode_flow.get(mode, 0)
    transferred_out = agg_transfer[agg_transfer['From'] == mode]['Flow'].sum()
    stay = total_origin - transferred_out
    if stay > 0:
        src = node_index[f"{mode} (From)"]
        tgt = node_index[f"{mode} (To)"]
        sankey_sources.append(src)
        sankey_targets.append(tgt)
        sankey_values.append(stay)
        sankey_labels.append(f"{mode}→{mode}: {int(stay)}")
        sankey_colors.append(color_map[mode])

# 节点色（主色，透明度为1）
node_colors = [node_color_map[m] for m in mode_names] + [node_color_map[m] for m in mode_names]

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=20,
        # line=dict(color="black", width=0.5),   # ← 注释或删除原有行
        line=dict(color="rgba(0,0,0,0)", width=0),   # ← 新增这一行，透明且宽度为0
        label=node_labels,
        color=node_colors
    ),
    link=dict(
        source=sankey_sources,
        target=sankey_targets,
        value=sankey_values,
        color=sankey_colors,
        label=sankey_labels,   # 悬停可显示数据
        customdata=sankey_labels,
        hovertemplate='%{customdata}<extra></extra>',
    )
)])


# fig.update_layout(title_text="Baseline Scenario", title_x=0.5, font_size=11)
# fig.update_layout(title_text="LCZ Scenario", title_x=0.5, font_size=11)
fig.update_layout(title_text="LCZ-RTM Scenario", title_x=0.5, font_size=11)
fig.show()
