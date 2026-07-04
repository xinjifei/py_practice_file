"""
d53_matplotlib子图显示 — 演示文件
2×2 子图：价格走势 + 收益率分布 + 成交量 + 相关性热力图
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 修复 Windows 中文显示乱码
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "WenQuanYi Micro Hei"]
plt.rcParams["axes.unicode_minus"] = False  # 防止负号显示为方块

# ============================================================
# 0. 构造模拟数据（经典场景：一支股票 120 个交易日）
# ============================================================
np.random.seed(42)
dates = pd.date_range("2025-01-02", periods=120, freq="B")  # 交易日

# 价格：从 100 起步，带随机游走
returns = np.random.normal(0.0005, 0.018, 120)  # 日均收益 ≈0.05%，日波动 1.8%
price = 100 * np.cumprod(1 + returns)

# 成交量：均值为 500 万股，偶尔放量
volume = np.random.normal(5_000_000, 1_200_000, 120).astype(int)
volume = np.abs(volume)  # 成交量非负

df = pd.DataFrame({
    "date": dates,
    "close": price,
    "volume": volume,
})
df["return"] = df["close"].pct_change()  # 日收益率

# ============================================================
# 1. 创建 2×2 画布
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# ---- 左上：价格走势（折线图）----
ax1 = axes[0, 0]
ax1.plot(df["date"], df["close"], color="#d62728", linewidth=1.5)
ax1.set_title("价格走势", fontsize=13, fontweight="bold")
ax1.set_xlabel("日期")
ax1.set_ylabel("收盘价（元）")
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis="x", rotation=30)

# ---- 右上：收益率分布（直方图）----
ax2 = axes[0, 1]
ax2.hist(df["return"].dropna(), bins=30, color="#1f77b4", edgecolor="white", alpha=0.85)
ax2.axvline(0, color="gray", linestyle="--", linewidth=1)        # 零收益参考线
ax2.axvline(df["return"].mean(), color="red", linestyle="-", linewidth=1.2, label=f"均值={df['return'].mean():.4f}")
ax2.set_title("日收益率分布", fontsize=13, fontweight="bold")
ax2.set_xlabel("日收益率")
ax2.set_ylabel("频次")
ax2.legend(fontsize=9)

# ---- 左下：成交量（柱状图）----
ax3 = axes[1, 0]
ax3.bar(df["date"], df["volume"], color="#2ca02c", width=0.8)
ax3.set_title("成交量", fontsize=13, fontweight="bold")
ax3.set_xlabel("日期")
ax3.set_ylabel("成交量（股）")
ax3.tick_params(axis="x", rotation=30)
# y 轴用科学计数法，避免一长串 0
ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x/1e6:.1f}M"))

# ---- 右下：相关性热力图 ----
ax4 = axes[1, 1]
corr = df[["close", "volume", "return"]].corr()
sns.heatmap(corr, annot=True, fmt=".3f", cmap="RdBu_r", center=0,
            vmin=-1, vmax=1, square=True, linewidths=0.5,
            cbar_kws={"shrink": 0.8, "label": "相关系数"},
            ax=ax4)
ax4.set_title("相关性矩阵", fontsize=13, fontweight="bold")

# ---- 全局 ----
fig.suptitle("XX 股票 多维分析（120 个交易日）", fontsize=15, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig("d53_多维分析.png", dpi=150, bbox_inches="tight")
plt.show()
print("✅ 图已保存为 d53_多维分析.png")
