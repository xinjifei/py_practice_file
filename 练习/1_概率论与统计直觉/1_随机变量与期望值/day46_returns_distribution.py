"""
第46天：随机变量与期望值 — 茅台日收益率分布
=============================================
核心认知：收益率是一个随机变量——你不知道明天具体是多少，
但可以通过历史数据了解它的「典型范围」（期望 ± 波动）。

本脚本完成：
  1. 从 CSV 读取收盘价，计算日收益率序列
  2. 计算期望值（均值）、标准差（波动率）
  3. 画直方图 + 拟合正态曲线 + 标注 ±2σ
  4. 打印统计摘要
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

# 中文显示修复：指定支持中文的字体（Windows 用 Microsoft YaHei）
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "PingFang SC"]
matplotlib.rcParams["axes.unicode_minus"] = False  # 避免负号显示为方块

# ============================================================
# 1. 读取数据 & 计算日收益率
# ============================================================

DATA_DIR = Path("D:/PY_practice_file/练习用数据源/stock_daily")
df = pd.read_csv(DATA_DIR / "600519.csv", parse_dates=["date"])

# .pct_change()：每个元素相对于前一个元素的变化率
# (close_t - close_{t-1}) / close_{t-1}
# 第一条记录的收益率是 NaN（没有前一日），直接丢弃
returns = df["close"].pct_change().dropna()

print("=" * 55)
print("茅台日收益率 — 统计摘要")
print("=" * 55)
print(f"  数据条数（交易日）: {len(returns)}")
print(f"  日期范围            : {df['date'].iloc[0].date()} ~ {df['date'].iloc[-1].date()}")

# ============================================================
# 2. 三个核心统计量
# ============================================================

mean_ret = np.mean(returns)         # 期望值 — 长期平均日收益率
var_ret = np.var(returns)            # 方差   — 收益率偏离均值的平方平均
std_ret = np.std(returns)            # 标准差 — 方差的平方根，和收益率同单位

print(f"\n  期望值 (日均收益率): {mean_ret:+.6f}  = {mean_ret*100:+.4f}%")
print(f"  方差                 : {var_ret:.8f}")
print(f"  标准差 (日波动率)    : {std_ret:.6f}  = {std_ret*100:.4f}%")
print(f"  年化波动率           : {std_ret * np.sqrt(252):.4f}  = {std_ret * np.sqrt(252) * 100:.2f}%")
print(f"                     (日波动率 × √252)")

# ±2σ 覆盖范围
print(f"\n  约 95% 的交易日收益率落在:")
print(f"    [{mean_ret - 2*std_ret:.6f}, {mean_ret + 2*std_ret:.6f}]")
print(f"    即 [{ (mean_ret - 2*std_ret)*100:.2f}%, {(mean_ret + 2*std_ret)*100:.2f}%]")

# 实际统计 ±2σ 内的数据比例
within_2sigma = ((returns >= mean_ret - 2*std_ret) & (returns <= mean_ret + 2*std_ret)).sum()
pct_2sigma = within_2sigma / len(returns) * 100
print(f"  实际落在 ±2σ 内的比例: {within_2sigma}/{len(returns)} = {pct_2sigma:.1f}%")

# ============================================================
# 3. 画图 — 收益率分布直方图 + 正态曲线 + 标注
# ============================================================

# ---------- 3a. 创建画布 ----------
# plt.figure(figsize=(宽, 高)) 创建一个画布
# figsize 单位是英寸，这里 12×7 比较适合屏幕观看
fig, ax = plt.subplots(figsize=(12, 7))

# ---------- 3b. 画直方图 ----------
# ax.hist() 把数据分成一个个 "箱子" (bin)，统计每个箱子里有多少数据点
# bins=60       → 切成 60 个箱子
# density=True  → 不画"次数"，画"概率密度"（总面积为 1），这样才能和正态曲线比较
# alpha=0.7     → 透明度 0.7，让背后的曲线能透过来
# color='steelblue' → 柱子颜色
# edgecolor='white' → 柱子边缘白色，视觉区分
# label=...     → 图例的文字
ax.hist(
    returns, bins=60, density=True, alpha=0.7,
    color="steelblue", edgecolor="white",
    label=f"茅台日收益率 (n={len(returns)})",
)

# ---------- 3c. 叠加正态分布曲线 ----------
# 用收益率的均值(μ)和标准差(σ)生成一条"理论上的正态分布"曲线
# 这条曲线假设收益率服从正态分布，用来和实际数据对比

# np.linspace(start, stop, num): 在 [start, stop] 之间均匀生成 num 个点
# 这里生成 300 个 x 坐标，从最小值到最大值，用于画平滑曲线
x = np.linspace(returns.min(), returns.max(), 300)

# 正态分布的概率密度函数（PDF）:
#   f(x) = (1 / (σ * √(2π))) * exp(-0.5 * ((x - μ) / σ)²)
# scipy 里有现成的，但这里手写公式更直观
normal_pdf = (1 / (std_ret * np.sqrt(2 * np.pi))) * \
             np.exp(-0.5 * ((x - mean_ret) / std_ret) ** 2)

# ax.plot() 画的折线会自动连接所有 (x, y) 点
ax.plot(
    x, normal_pdf, "r-", linewidth=2,
    label=f"正态分布拟合 (μ={mean_ret*100:.2f}%, σ={std_ret*100:.2f}%)",
)

# ---------- 3d. 标注均值线和 ±2σ 线 ----------

# ax.axvline() = "axis vertical line" — 在 x 轴的指定位置画一条竖线
# x=...    → 竖线的 x 坐标
# color=   → 颜色
# linestyle= → 线型: '--' 虚线, ':' 点线
# linewidth → 线宽
# label=   → 图例文字

# 均值线（黑色虚线）
ax.axvline(mean_ret, color="black", linestyle="--", linewidth=1.5,
           label=f"均值 μ = {mean_ret*100:+.3f}%")

# ±1σ（绿色点线）
ax.axvline(mean_ret + std_ret, color="green", linestyle=":", linewidth=1.2)
ax.axvline(mean_ret - std_ret, color="green", linestyle=":", linewidth=1.2,
           label=f"±1σ = ±{std_ret*100:.3f}%")

# ±2σ（橙色点线）
ax.axvline(mean_ret + 2*std_ret, color="orange", linestyle=":", linewidth=1.2)
ax.axvline(mean_ret - 2*std_ret, color="orange", linestyle=":", linewidth=1.2,
           label=f"±2σ = ±{2*std_ret*100:.3f}%")

# ---------- 3e. 装饰：标题、坐标轴标签、图例、网格 ----------

ax.set_title(
    "贵州茅台 (600519) 日收益率分布\n"
    "红线 = 拟合正态分布 | 黑线 = 均值 | 绿/橙 = ±1σ/±2σ",
    fontsize=14, fontweight="bold",
)
ax.set_xlabel("日收益率", fontsize=12)
ax.set_ylabel("概率密度", fontsize=12)
ax.legend(loc="upper left", fontsize=9)     # 图例放左上角
ax.grid(True, alpha=0.3)                     # 网格线，透明度 0.3
plt.tight_layout()                           # 自动调整边距，防止标签被截

# ---------- 3f. 保存和显示 ----------
output_dir = Path(__file__).resolve().parent
plt.savefig(output_dir / "returns_distribution.png", dpi=150, bbox_inches="tight")
print(f"\n  图表已保存: {output_dir / 'returns_distribution.png'}")
plt.show()
