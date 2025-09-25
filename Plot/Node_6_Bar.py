import matplotlib.pyplot as plt
import numpy as np
import re
from scipy.io import loadmat

# === 1. 定义输入数据 ===
# 假设每个场景都有两个 list，分别是 link_name 和对应的 flow 值
# 你需要替换下面的三个元组为你自己的三组数据（可通过 .mat 或 Excel 等方式加载）

# 示例结构：
# scene_data = [(link_names1, flow_values1), (link_names2, flow_values2), (link_names3, flow_values3)]
link_names_raw = loadmat("x_link_unimode.mat")['x_link_unimode']
link_names = [str(x[0]) for x in link_names_raw.squeeze()]

flow_values1 = loadmat("Plot_data/Link_flow_before_0616_A.mat")['X_link_unimode_before'].flatten()
flow_values2 = loadmat("Plot_data/Link_flow_before_mapped_0616_A.mat")['X_link_unimode_before'].flatten()
flow_values3 = loadmat("Plot_data/Link_flow_after_0616_A.mat")['X_link_unimode_before'].flatten()
scene1 = (link_names, flow_values1)
scene2 = (link_names, flow_values2)
scene3 = (link_names, flow_values3)
scene_data = [scene1, scene2, scene3]
scene_labels = ['Baseline', 'LCZ', 'LCZ-RTM']

# === 2. 设置 node 6 相邻的 links（无向 link）===
node6_links = {('1', '6'), ('6', '1'), ('4', '6'), ('6', '4'), ('7', '6'),
               ('6', '7'), ('6', '9'), ('9', '6'), ('17', '6'), ('6', '17')}

# === 3. 定义交通模式列表 ===
modes = ['Car', 'Bus', 'Bike', 'Metro', 'Rail']

def extract_mode_flow(link_names, flows):
    """提取与 node 6 相连的 flow 并按 mode 聚合"""
    mode_flow = {mode: 0 for mode in modes}
    for name, val in zip(link_names, flows):
        match = re.match(r'x_(\w+?)_?(\d+)to(\d+)_', name)
        if match:
            mode = match.group(1)
            i, j = match.group(2), match.group(3)
            if (i, j) in node6_links:
                if mode in mode_flow:
                    mode_flow[mode] += val
    return [mode_flow[mode] for mode in modes]

# === 4. 提取所有场景的 mode flows ===
all_flows = [extract_mode_flow(links, flows) for links, flows in scene_data]

# === 5. 绘图 ===
x = np.arange(len(modes))
bar_width = 0.25
scene_colors = ['#66c2a5', '#fc8d62', '#8da0cb']  # 对应 Before, Mapped, Optimized
plt.figure(figsize=(8, 5))
for idx, scene_flow in enumerate(all_flows):
    plt.bar(x + idx * bar_width, scene_flow, width=bar_width,
        color=scene_colors[idx], alpha=1.0, label=scene_labels[idx])

plt.xticks(x + bar_width, modes)
plt.ylabel('Total Flow in the Low-Car Zone')
plt.title('Mode Flow Changes in the Low-Car Zone in Different Scenarios')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
