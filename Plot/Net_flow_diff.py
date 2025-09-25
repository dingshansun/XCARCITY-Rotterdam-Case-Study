import re
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from scipy.io import loadmat

def draw_rotterdam_circle(ax, pos, node_ids, alpha=0.3):
    coords = np.array([pos[n] for n in node_ids])
    cx, cy = np.mean(coords[:, 0]), np.mean(coords[:, 1])
    radius = np.max(np.linalg.norm(coords - [cx, cy], axis=1)) + 0.02
    circle = plt.Circle((cx, cy), radius,
                        edgecolor="#94C7EC",
                        facecolor="#96C8EB",
                        alpha=alpha,
                        linewidth=1.5, zorder=0)
    ax.add_patch(circle)
    # ax.text(cx + 0.3, cy, "Rotterdam",
    #     fontsize=12, color='royalblue',
    #     ha='center', va='center', alpha=0.8,
    #     clip_on=True)

# === Step 1: Load data ===
link_names_raw = loadmat("x_link_unimode.mat")['x_link_unimode']
link_names = [str(x[0]) for x in link_names_raw.squeeze()]
link_flow_before = loadmat("Plot_data/Link_flow_before_0616_A.mat")['X_link_unimode_before'].flatten()
link_flow_before_mapped = loadmat("Plot_data/Link_flow_before_mapped_0616_A.mat")['X_link_unimode_before'].flatten()
link_flow_after = loadmat("Plot_data/Link_flow_after_0616_A.mat")['X_link_unimode_before'].flatten()
# link_flow_after = loadmat("Plot_data/Link_travel_time_after_0620_A.mat")['time_cost_unimode'].flatten()
# link_flow_before = loadmat("Plot_data/Link_travel_time_before_0620_A.mat")['time_cost_unimode'].flatten()
# link_flow_before_mapped = loadmat("Plot_data/Link_travel_time_Mapped_0620_A.mat")['time_cost_unimode'].flatten()

# === Step 2: Parse links into dataframe with delta ===
records_mb, records_am, records_ab = [], [], []
for name, flow_b, flow_a, flow_m in zip(link_names, link_flow_before, link_flow_after, link_flow_before_mapped):
    match = re.match(r'x_(\w+?)_(\d+)to(\d+)_Origin\d+', name)
    if match:
        mode, from_node, to_node = match.groups()
        from_node, to_node = int(from_node), int(to_node)
        records_mb.append({"Mode": mode, "From": from_node, "To": to_node, "Delta": (float(flow_m) - float(flow_b))})
        records_am.append({"Mode": mode, "From": from_node, "To": to_node, "Delta": (float(flow_a) - float(flow_m))})
        records_ab.append({"Mode": mode, "From": from_node, "To": to_node, "Delta": (float(flow_a) - float(flow_b))})

df_delta = pd.DataFrame(records_ab)

# === Step 3: Define node positions ===
pos = {
    1: (0.3, 0.7), 2: (0.5, 0.75), 3: (0.7, 0.7), 4: (0.4, 0.55), 5: (0.65, 0.55),
    6: (0.3, 0.39), 7: (0.45, 0.37), 8: (0.6, 0.32), 9: (0.25, 0.2), 10: (0.45, 0.15),
    11: (0.65, 0.2), 12: (0.22, 0.8), 13: (0.25, 0.93), 14: (0.75, 0.05), 15: (0.75, 0.8),
    16: (0.1, 0.05), 17: (0.1, 0.65), 18: (0.5, 0.9)
}
rotterdam_nodes = list(range(1, 11))

# === Step 4: Plot each mode ===
modes = df_delta['Mode'].unique()

for mode in modes:
    df = df_delta[df_delta['Mode'] == mode]

    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(row['From'], row['To'], delta=row['Delta'])

    fig, ax = plt.subplots(figsize=(5, 6), constrained_layout=True)

    draw_rotterdam_circle(ax, pos, rotterdam_nodes)
    nx.draw_networkx_nodes(G, pos, node_size=400, node_color='lightgray', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

    epsilon = 1e-2  # 容差范围
    for u, v, d in G.edges(data=True):
        delta = d['delta']
        # color = 'green' if delta > 0 else ('red' if delta < 0 else 'gray')
        if delta > epsilon:
            color = '#009E73'
        elif delta < -epsilon:
            color = '#D55E00'
        else:
            color = 'gray'

        label_threshold = 100000  # 超过这个阈值的 delta 不进行数值标注
        if abs(delta) <= label_threshold:
            width = 1 + min(abs(delta) / 600, 5)  # 正常按变化大小设置宽度
        else:
            width = 1.0  # 超过阈值的边使用细线宽度
            color = 'gray'
        # width = 1 + min(abs(delta) / 500, 5)

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


        if abs(delta) > 0 and abs(delta) <= label_threshold:
            x_text = (pos_u[0] + (pos_v[0] - pos_u[0]) * 0.6)
            y_text = (pos_u[1] + (pos_v[1] - pos_u[1]) * 0.6)
            ax.text(x_text, y_text, f"{round(delta)}",
                    fontsize=9, color='black', ha='center',
                    bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', boxstyle='round,pad=0.1'))

    # ax.set_title(f"{mode} – Flow Change (LCZ − Baseline )", fontsize=13)
    # ax.set_title(f"{mode} – Flow Change (LCZ-RTM − LCZ)", fontsize=13)
    ax.set_title(f"{mode} – Flow Change (LCZ-RTM − Baseline)", fontsize=13)
    ax.axis('off')
    plt.show()
