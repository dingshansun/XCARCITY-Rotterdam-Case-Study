import re
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from scipy.io import loadmat

def draw_rotterdam_circle(ax, pos, node_ids, alpha=0.15):  # 默认更轻一点
    coords = np.array([pos[n] for n in node_ids])
    cx, cy = np.mean(coords[:, 0]), np.mean(coords[:, 1])
    radius = np.max(np.linalg.norm(coords - [cx, cy], axis=1)) + 0.02
    circle = plt.Circle((cx, cy), radius,
                        edgecolor='royalblue',
                        facecolor='lightblue',
                        alpha=alpha,
                        linewidth=1.5, zorder=0)
    ax.add_patch(circle)
    ax.text(cx + 0.3, cy, "Rotterdam",
        fontsize=12, color='royalblue',
        ha='center', va='center', alpha=0.8,
        clip_on=True)


# === Step 1: Load MATLAB files ===
link_names_raw = loadmat("x_link_unimode.mat")['x_link_unimode']
link_names = [str(x[0]) for x in link_names_raw.squeeze()]
link_flow_after = loadmat("Plot_data/Link_travel_time_after_0620_A.mat")['time_cost_unimode'].flatten()
link_flow_before = loadmat("Plot_data/Link_travel_time_before_0620_A.mat")['time_cost_unimode'].flatten()
link_flow_before_mapped = loadmat("Plot_data/Link_travel_time_Mapped_0620_A.mat")['time_cost_unimode'].flatten()

# === Step 2: Parse link name into structured dataframe ===
records_before, records_after, records_mapped = [], [], []
for name, flow_b, flow_a, flow_m in zip(link_names, link_flow_before, link_flow_after, link_flow_before_mapped):
    match = re.match(r'x_(\w+?)_(\d+)to(\d+)_Origin\d+', name)
    if match:
        mode, from_node, to_node = match.groups()
        from_node, to_node = int(from_node), int(to_node)
        records_before.append({"Mode": mode, "From": from_node, "To": to_node, "Flow": float(flow_b)*60})
        records_after.append({"Mode": mode, "From": from_node, "To": to_node, "Flow": float(flow_a)*60})
        records_mapped.append({"Mode": mode, "From": from_node, "To": to_node, "Flow": float(flow_m)*60})

df_before = pd.DataFrame(records_before)
df_after = pd.DataFrame(records_after)
df_mapped = pd.DataFrame(records_mapped)

# === Step 3: Define node positions ===
pos = {
    1: (0.3, 0.7), 2: (0.5, 0.75), 3: (0.7, 0.7), 4: (0.4, 0.55), 5: (0.65, 0.55),
    6: (0.3, 0.39), 7: (0.45, 0.37), 8: (0.6, 0.32), 9: (0.25, 0.2), 10: (0.45, 0.15),
    11: (0.65, 0.2), 12: (0.22, 0.8), 13: (0.25, 0.93), 14: (0.75, 0.05), 15: (0.75, 0.8),
    16: (0.1, 0.05), 17: (0.1, 0.65), 18: (0.5, 0.9)
}

rotterdam_nodes = list(range(1, 11))

# === Step 4: Visualize for each mode ===
modes = df_before['Mode'].unique()
mode_vmax_dict = {
    'Car': 60,
    'Bus': 80,
    'Bike': 120,
    'Metro': 40,
    'Rail': 30,
    # 你可以根据实际值继续添加
}

for mode in modes:
    df_b = df_before[df_before['Mode'] == mode]
    df_a = df_after[df_after['Mode'] == mode]
    df_m = df_mapped[df_mapped['Mode'] == mode]

    G_b, G_a, G_m = nx.DiGraph(), nx.DiGraph(), nx.DiGraph()
    for _, row in df_b.iterrows():
        G_b.add_edge(row['From'], row['To'], flow=row['Flow'])
    for _, row in df_a.iterrows():
        G_a.add_edge(row['From'], row['To'], flow=row['Flow'])
    for _, row in df_m.iterrows():
        G_m.add_edge(row['From'], row['To'], flow=row['Flow'])

    # === Unified colorbar ===
    flows_all = [d['flow'] for _, _, d in G_b.edges(data=True)] + \
                [d['flow'] for _, _, d in G_a.edges(data=True)] + \
                [d['flow'] for _, _, d in G_m.edges(data=True)]
    vmax_limit = mode_vmax_dict.get(mode, 60)
    flows_all_clipped = [min(flow, vmax_limit) for flow in flows_all]
    cmap = plt.cm.viridis
    norm = plt.Normalize(vmin=0, vmax=vmax_limit)

    # fig, axs = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
    fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)
    # for ax, G, label in zip(axs, [G_b, G_a], ["After Intervention", "Before Intervention"]):
    # for ax, G, label in zip(axs, [G_b], ["After Intervention"]):
    G = G_a
    # label = "Before Intervention"
    # label = "Mapped Intervention"
    label = "After Intervention"
    flows = [d['flow'] for _, _, d in G.edges(data=True)]
    # colors = [cmap(norm(min(G[u][v]['flow'], vmax_limit))) for u, v in G.edges()]
#     widths = [1 + 4 * min(G[u][v]['flow'], vmax_limit) / vmax_limit for u, v in G.edges()]
    colors = []
    widths = []
    for u, v in G.edges():
        flow_val = G[u][v]['flow']
        if flow_val > vmax_limit:
            colors.append('red')
            widths.append(1.5)  # 设置为细一点的宽度
        else:
            colors.append(cmap(norm(flow_val)))
            widths.append(1 + 4 * flow_val / vmax_limit)  # 保持原有宽度策略

    draw_rotterdam_circle(ax, pos, rotterdam_nodes, alpha=0.15)
    nx.draw_networkx_nodes(G, pos, node_size=400, node_color='lightgray', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

    for (u, v), color, width in zip(G.edges(), colors, widths):
        offset = 0.01
        dx, dy = pos[v][0] - pos[u][0], pos[v][1] - pos[u][1]
        norm_vec = np.sqrt(dx**2 + dy**2)
        shift = (-dy, dx)
        shift = (shift[0] * offset / norm_vec, shift[1] * offset / norm_vec)
        pos_u = (pos[u][0] + shift[0], pos[u][1] + shift[1])
        pos_v = (pos[v][0] + shift[0], pos[v][1] + shift[1])

        ax.annotate("",
            xy=pos_v, xycoords='data',
            xytext=pos_u, textcoords='data',
            arrowprops=dict(
                arrowstyle="-|>",
                color=color,
                lw=width,
                mutation_scale=10,
                shrinkA=16,
                shrinkB=10
            ))
        # threshold = 0.2 * max_flow  # 标注阈值为最大流量的20%
        threshold = 180  # 展示所有流量

        flow_val = G[u][v]['flow']
        if flow_val < threshold:
            x_text = (pos_u[0] + (pos_v[0]-pos_u[0])*0.6)
            y_text = (pos_u[1] + (pos_v[1]-pos_u[1])*0.6)  # 轻微上移
            ax.text(x_text, y_text, f"{round(flow_val)}",
                    fontsize=9, color='black', ha='center',
                    bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', boxstyle='round,pad=0.1'))
        


    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Link time cost [min]")
    ax.set_title(f"{mode} - {label}")
    ax.axis('off')

    # plt.suptitle(f"{mode} Mode - Link Flow After vs Before", fontsize=16)
    # plt.savefig(f"{mode}_flow_comparison.png", dpi=300)
    plt.show()
