########################### Changed from pie chart to bar chart #################################
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.io import loadmat
import re

scenarios = [
    {
        "file": "Plot_data/Link_flow_before_0616_A.mat",
        "title": "Baseline"
    },
    {
        "file": "Plot_data/Link_flow_before_mapped_0616_A.mat",
        "title": "LCZ"
    },
    {
        "file": "Plot_data/Link_flow_after_0616_A.mat",
        "title": "LCZ-RTM"
    }
]
mode_order = ["Car", "Bus", "Bike", "Metro", "Rail"]

# 这次 scenario 用颜色
scenario_colors = ['#66c2a5', '#fc8d62', '#8da0cb']

link_names_raw = loadmat("x_link_unimode.mat")['x_link_unimode']
link_names = [str(x[0]) for x in link_names_raw.squeeze()]
mode_totals_per_scenario = []

for scenario in scenarios:
    link_flows = loadmat(scenario['file'])['X_link_unimode_before'].flatten()
    records = []
    for name, flow in zip(link_names, link_flows):
        match = re.match(r'x_(\w+?)_', name)
        if match:
            mode = match.group(1)
            records.append({"Mode": mode, "Flow": float(flow)})
    df = pd.DataFrame(records)
    mode_totals = df.groupby('Mode')['Flow'].sum()
    mode_totals_per_scenario.append([mode_totals.get(m, 0) for m in mode_order])

mode_totals_per_scenario = np.array(mode_totals_per_scenario)  # shape: (3, 5)

# 画柱状图，每组为 mode，每组3根（不同scenario）
bar_width = 0.22
x = np.arange(len(mode_order))
fig, ax = plt.subplots(figsize=(8, 5))

for i, scenario in enumerate(scenarios):
    ax.bar(x + i*bar_width, mode_totals_per_scenario[i], width=bar_width,
           color=scenario_colors[i], label=scenario["title"])

ax.set_xticks(x + bar_width)
ax.set_xticklabels(mode_order)
ax.set_ylabel("Total Flow")
ax.set_title("Mode Flow Changes Over the Entire Network under Three Scenarios")
ax.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()



############################# Original Pie Chart #################################
# from scipy.io import loadmat
# import re
# import matplotlib.pyplot as plt
# import pandas as pd

# # === 文件与标题对应 ===
# scenarios = [
#     {
#         "file": "Plot_data/Link_flow_before_0616_A.mat",
#         "title": "Baseline Scenario"
#     },
#     {
#         "file": "Plot_data/Link_flow_before_mapped_0616_A.mat",
#         "title": "LCZ Scenario"
#     },
#     {
#         "file": "Plot_data/Link_flow_after_0616_A.mat",
#         "title": "LCZ-RTM Scenario"
#     }
# ]

# # === 颜色设定 ===
# # custom_colors = {
# #     "Car": "#5ca1d3",     # 蓝色
# #     "Bus": "#ce6666",     # 红色
# #     "Bike": "#70c570",    # 绿色
# #     "Metro": "#ba96db",   # 紫色
# #     "Rail": "#d18c4f"     # 橙色
# # }

# custom_colors = {
#     "Car": "#8da0cb",     # 蓝色
#     "Bus": "#fc8d62",     # 橙红色
#     "Bike": "#66c2a5",    # 绿色
#     "Metro": "#e78ac3",   # 粉紫色
#     "Rail": "#a6d854"     # 浅橙绿色
# }

# # === 读取所有场景数据 ===
# link_names_raw = loadmat("x_link_unimode.mat")['x_link_unimode']
# link_names = [str(x[0]) for x in link_names_raw.squeeze()]

# # === 绘图区域 ===
# fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # 1行3列
# for idx, scenario in enumerate(scenarios):
#     # 加载当前场景的数据
#     link_flows = loadmat(scenario['file'])['X_link_unimode_before'].flatten()

#     # 解析 mode 与 flow
#     records = []
#     for name, flow in zip(link_names, link_flows):
#         match = re.match(r'x_(\w+?)_', name)
#         if match:
#             mode = match.group(1)
#             records.append({"Mode": mode, "Flow": float(flow)})
#     df = pd.DataFrame(records)
#     mode_totals = df.groupby('Mode')['Flow'].sum().to_dict()

#     # === 绘制饼图 ===
#     labels = list(mode_totals.keys())
#     sizes = list(mode_totals.values())
#     colors = [custom_colors.get(label, "#cccccc") for label in labels]

#     axes[idx].pie(
#         sizes,
#         labels=labels,
#         autopct='%1.1f%%',
#         startangle=140,
#         colors=colors,
#         textprops={'fontsize': 10}
#     )
#     axes[idx].set_title(f"Mode Share\n({scenario['title']})", fontsize=12)
#     axes[idx].axis('equal')

# # === 布局优化并显示 ===
# plt.tight_layout()
# plt.show()
