"""
第48天 延伸实验：用 Bootstrap 检验「使劲投硬币」策略
=========================================================
你的策略：使劲投，希望得到更多正面。
用今天学的 Bootstrap 假设检验来量化验证这个策略有没有用。

流程（和 Sharpe 检验完全一样，只是把「收益率」换成「硬币正反」）：
    1. 采集实际投掷结果（模拟 10 次使劲投）
    2. 归零：假设硬币是公平的（p=0.5），把数据归到公平硬币的基线
    3. Bootstrap 1000 次，每次算正面率
    4. 看真实正面率在分布中的位置
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ============================================================
# 0. 中文字体
# ============================================================
CANDIDATE_FONTS = [
    "Microsoft YaHei", "SimHei", "KaiTi", "FangSong", "SimSun",
]
available_fonts = {f.name for f in fm.fontManager.ttflist}
chosen = None
for f in CANDIDATE_FONTS:
    if f in available_fonts:
        chosen = f
        break
if chosen:
    plt.rcParams["font.sans-serif"] = [chosen, "DejaVu Sans"]
else:
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 1. 「使劲投」10 次硬币的原始数据
# ============================================================
# 1 = 正面, 0 = 反面
# 模拟你使劲投 10 次的结果（实际上硬币是公平的，p=0.5）
np.random.seed(42)  # 固定随机种子，结果可复现
n_tosses = 10
observed_tosses = np.random.choice([1, 0], size=n_tosses, p=[0.5, 0.5])

observed_heads = observed_tosses.sum()
observed_rate = observed_heads / n_tosses

print("=" * 60)
print("硬币实验：使劲投 10 次")
print("=" * 60)
print(f"结果序列: {observed_tosses.tolist()}")
print(f"正面次数: {observed_heads} / {n_tosses}")
print(f"正面率:   {observed_rate:.1%}")
print()

# ============================================================
# 2. 原假设：硬币是公平的（p=0.5），你的「使劲」没用
# ============================================================
# 意味着每次投掷的「基准」是 0.5
# 归零操作：把原始数据归到 H0 的基线
#   H0 基线 = 每次投掷的期望正面率 = 0.5
#   归零后数据 = 原始数据 - observed_mean + 0.5

observed_mean = observed_tosses.mean()        # 真实均值（比如 0.7）
centered_tosses = observed_tosses - observed_mean + 0.5  # 归到 0.5
# centered_tosses 现在均值 = 0.5，也就是公平硬币的数据池

# ============================================================
# 3. Bootstrap 1000 次：模拟「公平硬币」的世界
# ============================================================
n_bootstrap = 1000
bootstrap_rates = []

for _ in range(n_bootstrap):
    # 从归零后的数据池有放回抽样 10 次
    sample = np.random.choice(centered_tosses, size=n_tosses, replace=True)
    # 这次抽样的正面率
    bootstrap_rates.append(sample.mean())

bootstrap_rates = np.array(bootstrap_rates)
bootstrap_std = bootstrap_rates.std()

# ============================================================
# 4. 判断
# ============================================================
p_value = (bootstrap_rates >= observed_rate).mean()
distance = (observed_rate - 0.5) / bootstrap_std  # 离公平硬币有几个 std

print(f"Bootstrap 分布统计（1000 次公平硬币模拟）:")
print(f"  均值:     {bootstrap_rates.mean():.4f}")
print(f"  标准差:   {bootstrap_std:.4f}")
print(f"  范围:     [{bootstrap_rates.min():.4f}, {bootstrap_rates.max():.4f}]")
print()
print(f"真实正面率: {observed_rate:.1%}")
print(f"偏离距离:   {distance:.2f} 倍标准差")
print(f"p 值:       {p_value:.4f}  ({p_value:.1%})")
print()
if p_value < 0.05:
    print("结论: 使劲投可能有某种效果（或硬币不是公平的）")
else:
    print("结论: 不能排除运气——公平硬币也经常出现这种结果")

# ============================================================
# 5. 画图
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 左图：Bootstrap 分布 + 真实正面率
axes[0].hist(bootstrap_rates, bins=12, color="steelblue", edgecolor="white", alpha=0.8)
axes[0].axvline(observed_rate, color="red", linewidth=2.5,
                label=f"使劲投 = {observed_rate:.0%} ({observed_heads}/10)")
axes[0].axvline(0.5, color="gray", linewidth=1.5, linestyle="--", label="公平硬币 = 50%")
axes[0].set_title(f"Bootstrap 分布（{n_bootstrap} 次模拟）\n真实结果在公平硬币世界中的位置", fontsize=12)
axes[0].set_xlabel("正面率")
axes[0].set_ylabel("频次")
axes[0].legend(fontsize=9)

# 右图：对比 10 次 vs 100 次（样本量的影响）
# 同样 Bootstrap，但样本量换成 100
n_tosses_large = 100
centered_large = np.random.choice(centered_tosses, size=n_tosses_large, replace=True)
# 归零
centered_large = centered_large - centered_large.mean() + 0.5

bootstrap_rates_large = []
for _ in range(n_bootstrap):
    sample = np.random.choice(centered_large, size=n_tosses_large, replace=True)
    bootstrap_rates_large.append(sample.mean())
bootstrap_rates_large = np.array(bootstrap_rates_large)

# 把 10 次和 100 次的分布叠在一起
axes[1].hist(bootstrap_rates, bins=15, color="steelblue", alpha=0.5, density=True,
             label=f"10 次 (std={bootstrap_std:.3f})")
axes[1].hist(bootstrap_rates_large, bins=15, color="darkorange", alpha=0.5, density=True,
             label=f"100 次 (std={bootstrap_rates_large.std():.3f})")
axes[1].axvline(observed_rate, color="red", linewidth=2,
                label=f"真实 = {observed_rate:.0%}")
axes[1].set_title("样本量的影响\n10 次 vs 100 次", fontsize=12)
axes[1].set_xlabel("正面率")
axes[1].set_ylabel("密度")
axes[1].legend(fontsize=9)

plt.tight_layout()
plt.show()
