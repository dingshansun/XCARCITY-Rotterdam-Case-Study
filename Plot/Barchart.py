import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 设置主题风格
sns.set_theme(style="whitegrid")

# 模式 & 原始数据
modes = ["Car", "Bus", "Bike", "Metro", "Rail"]

# before_data = {
#     "Total flow": [22978, 3194, 187270, 18557, 40682],
#     "Total money cost": [59846.0, 8837.6, 0, 37994, 116930],
#     "Total time cost": [5176.2, 1908.9, 77814.0, 6466.1, 13540.0]
# }
# after_data = {
#     "Total flow": [20153, 3654, 188160, 19006, 42483],
#     "Total money cost": [52138.0, 9569.8, 0, 38533, 121440],
#     "Total time cost": [4391.7, 2087.3, 78508.0, 6579.8, 14098.0]
# }

after_data = {   # Before intervention
    "Total flow": [39633, 947, 173960, 17493, 38756],
    "Total money cost": [174370.0, 3296.7, 25866.0, 38681.0, 118800.0],
    "Total time cost": [21164.0, 1761.6, 70237.0, 8978.3, 17820.0]
}

before_data = {    # After intervention
    "Total flow": [33251, 1650, 178300, 18501, 40176],
    "Total money cost": [149940.0, 3726.3, 26562.0, 38512.0, 121920.0],
    "Total time cost": [14601.0, 959.0, 72811.0, 7692.0, 18395.0]
}


# 差值计算
flow_change = np.array(after_data["Total flow"]) - np.array(before_data["Total flow"])
money_change = (np.array(after_data["Total money cost"]) - np.array(before_data["Total money cost"]))/10
time_change = np.array(after_data["Total time cost"]) - np.array(before_data["Total time cost"])

# x 轴 & 柱宽
x = np.arange(len(modes))
width = 0.25

# 使用更自然的 Seaborn 配色
# colors = sns.color_palette("Set1", 3)  # 选3个不同的颜色
colors = ['#4878CF', '#6ACC65', '#D65F5F']  

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6))

bars1 = ax.bar(x - width, flow_change, width, label='Flow Change', color=colors[0])
bars2 = ax.bar(x, money_change, width, label='Money Cost Change [10€]', color=colors[1])
bars3 = ax.bar(x + width, time_change, width, label='Time Cost Change [h]', color=colors[2])

# 添加数值标签
def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}', 
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

autolabel(bars1)
autolabel(bars2)
autolabel(bars3)

# 图表细节设置
ax.set_ylabel('Change Value')
ax.set_title('Changes per Mode: Flow, Money, Time (Before - After)')
ax.set_xticks(x)
ax.set_xticklabels(modes)
ax.axhline(0, color='gray', linewidth=0.8)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
