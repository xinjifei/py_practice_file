"""
第47天：相关性与协方差矩阵
===========================
5 个行业 × 5 只股票 = 25×25 协方差矩阵 + 相关系数热力图。
热力图上加行业分隔线，一眼看到：
    - 对角线上的 5×5 红色方块 → 行业内部高度正相关
    - 方块之外的浅色/蓝色区域 → 行业间相关性弱或为负

【依赖安装】
    uv pip install numpy pandas matplotlib seaborn akshare

【核心概念速查】
    - 收益率 = (今日收盘 - 昨日收盘) / 昨日收盘
    - 协方差矩阵：对角线是每只股票自己的方差，非对角线是两两之间的协方差
    - 热力图：红色 = 正相关（同涨同跌），蓝色 = 负相关（反向波动）
    - 行业内部 vs 行业间：同一行业的股票面对相同的政策/需求/成本 → 大概率同涨同跌
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
from datetime import datetime, timedelta

# ============================================================
# 1. 选股：5 个行业，每个行业 5 只 A 股
# ============================================================
# 格式：{行业名: {股票简称: 代码}}
INDUSTRY_STOCKS = {
    "银行": {
        "工商银行": "601398",
        "建设银行": "601939",
        "招商银行": "600036",
        "兴业银行": "601166",
        "农业银行": "601288",
    },
    "白酒": {
        "贵州茅台": "600519",
        "五粮液":   "000858",
        "泸州老窖": "000568",
        "山西汾酒": "600809",
        "洋河股份": "002304",
    },
    "新能源": {
        "宁德时代": "300750",
        "比亚迪":   "002594",
        "隆基绿能": "601012",
        "阳光电源": "300274",
        "通威股份": "600438",
    },
    "医药": {
        "恒瑞医药": "600276",
        "药明康德": "603259",
        "迈瑞医疗": "300760",
        "片仔癀":   "600436",
        "爱尔眼科": "300015",
    },
    "半导体": {
        "中芯国际": "688981",
        "北方华创": "002371",
        "韦尔股份": "603501",
        "中微公司": "688012",
        "兆易创新": "603986",
    },
}

# ============================================================
# 2. 中文字体设置
# ============================================================
CANDIDATE_FONTS = [
    "Microsoft YaHei", "SimHei", "KaiTi", "FangSong", "SimSun",
    "WenQuanYi Micro Hei", "Noto Sans CJK SC", "PingFang SC", "Heiti SC",
]

available_fonts = {f.name for f in fm.fontManager.ttflist}
chosen_font = None
for font_name in CANDIDATE_FONTS:
    if font_name in available_fonts:
        chosen_font = font_name
        break

if chosen_font:
    plt.rcParams["font.sans-serif"] = [chosen_font, "DejaVu Sans"]
    print(f"[字体] 使用: {chosen_font}")
else:
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
    print("[字体] 未找到中文字体！中文标题可能显示为方框 □□□")
    print(f"      系统可用字体（前20个）: {sorted(available_fonts)[:20]}")

plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 3. 获取数据（akshare）
# ============================================================
print("\n正在获取近一年日线数据...\n")

import akshare as ak

end_date = datetime.now().strftime("%Y%m%d")
start_date = (datetime.now() - timedelta(days=400)).strftime("%Y%m%d")

# 扁平化：保留行业标签，同时建立股票名→行业的映射
all_stocks = {}        # {简称: 代码}
stock_industry = {}    # {简称: 行业名}
for industry, stocks in INDUSTRY_STOCKS.items():
    for name, code in stocks.items():
        all_stocks[name] = code
        stock_industry[name] = industry

price_df = pd.DataFrame()

for name, code in all_stocks.items():
    try:
        raw = ak.stock_zh_a_hist(symbol=code, period="daily",
                                  start_date=start_date, end_date=end_date,
                                  adjust="qfq")
        raw["日期"] = pd.to_datetime(raw["日期"])
        raw = raw.set_index("日期").sort_index()
        price_df[name] = raw["收盘"]
        ind = stock_industry[name]
        print(f"  ✓ [{ind}] {name} ({code}) — {len(raw)} 个交易日")
    except Exception as e:
        print(f"  ✗ {name} ({code}) 获取失败: {e}")

price_df = price_df.dropna()
print(f"\n对齐后共 {len(price_df)} 个交易日（{price_df.index[0].date()} ~ {price_df.index[-1].date()}）")

# ============================================================
# 4. 计算日收益率
# ============================================================
returns_df = price_df.pct_change().dropna()

# ============================================================
# 5. 计算相关系数矩阵，并按行业排序
# ============================================================
# 按行业分组排列列顺序：同一行业的股票挨在一起
ordered_names = list(all_stocks.keys())  # 已经是按行业分组的插入顺序

corr_matrix = returns_df[ordered_names].corr()
cov_matrix = returns_df[ordered_names].cov()

# ============================================================
# 6. 画热力图（25×25 带行业分隔线）
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(22, 9))

# 帮助函数：在热力图上加行业分隔线
def draw_industry_lines(ax, line_color="black", line_width=1.5):
    """在行业边界处画粗线，把 5 个 5×5 方块分隔开"""
    # 计算每个行业的股票在排序后的起止位置
    boundaries = [0]
    for industry in INDUSTRY_STOCKS:
        count = len(INDUSTRY_STOCKS[industry])
        boundaries.append(boundaries[-1] + count)

    for b in boundaries[1:-1]:  # 跳过首尾
        # 画水平和垂直线
        ax.axhline(y=b, color=line_color, linewidth=line_width)
        ax.axvline(x=b, color=line_color, linewidth=line_width)

    # 在左侧标注行业名
    for i, industry in enumerate(INDUSTRY_STOCKS):
        start = boundaries[i]
        end = boundaries[i + 1]
        mid = (start + end) / 2
        ax.text(-1.5, mid, industry, ha="right", va="center",
                fontsize=10, fontweight="bold", transform=ax.transData)

# --- 左图：相关系数矩阵 ---
sns.heatmap(corr_matrix,
            annot=True,
            fmt=".2f",
            cmap="RdBu_r",
            vmin=-1, vmax=1,
            center=0,
            square=True,
            linewidths=0.3,
            annot_kws={"fontsize": 6},
            cbar_kws={"shrink": 0.8, "label": "相关系数 r"},
            ax=axes[0])
draw_industry_lines(axes[0])
axes[0].set_title("日收益率相关系数矩阵（25×25）", fontsize=14, fontweight="bold")
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45, ha="right", fontsize=7)
axes[0].set_yticklabels(axes[0].get_yticklabels(), rotation=0, fontsize=7)

# --- 右图：协方差矩阵（×10⁴） ---
cov_display = cov_matrix * 1e4
sns.heatmap(cov_display,
            annot=True,
            fmt=".2f",
            cmap="RdBu_r",
            center=0,
            square=True,
            linewidths=0.3,
            annot_kws={"fontsize": 6},
            cbar_kws={"shrink": 0.8, "label": "协方差 (×10⁻⁴)"},
            ax=axes[1])
draw_industry_lines(axes[1])
axes[1].set_title("日收益率协方差矩阵（×10⁻⁴）", fontsize=14, fontweight="bold")
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha="right", fontsize=7)
axes[1].set_yticklabels(axes[1].get_yticklabels(), rotation=0, fontsize=7)

plt.tight_layout()
plt.show()

# ============================================================
# 7. 统计分析：行业内部 vs 行业间
# ============================================================
print("\n" + "=" * 65)
print("行业内部 vs 行业间 相关性对比")
print("=" * 65)

# 收集所有股票对，按"同行" vs "跨行"分组
intra_corrs = []   # 行业内部
inter_corrs = []   # 行业间

for i, name_a in enumerate(ordered_names):
    for j, name_b in enumerate(ordered_names):
        if i >= j:
            continue  # 只看上三角，不重复
        r = corr_matrix.loc[name_a, name_b]
        if stock_industry[name_a] == stock_industry[name_b]:
            intra_corrs.append((name_a, name_b, r))
        else:
            inter_corrs.append((name_a, name_b, r))

intra_vals = [v for _, _, v in intra_corrs]
inter_vals = [v for _, _, v in inter_corrs]

print(f"\n行业内部股票对数量: {len(intra_corrs)}")
print(f"  平均相关系数: {np.mean(intra_vals):.4f}")
print(f"  中位数:       {np.median(intra_vals):.4f}")
print(f"  范围:         [{np.min(intra_vals):.4f}, {np.max(intra_vals):.4f}]")

print(f"\n行业间股票对数量: {len(inter_corrs)}")
print(f"  平均相关系数: {np.mean(inter_vals):.4f}")
print(f"  中位数:       {np.median(inter_vals):.4f}")
print(f"  范围:         [{np.min(inter_vals):.4f}, {np.max(inter_vals):.4f}]")

# --- 各行业内部相关性明细 ---
print("\n" + "-" * 65)
print("各行业内部平均相关系数（同行 5×5 方块内的均值）:")
for industry in INDUSTRY_STOCKS:
    stocks_in_ind = list(INDUSTRY_STOCKS[industry].keys())
    vals = []
    for i in range(len(stocks_in_ind)):
        for j in range(i + 1, len(stocks_in_ind)):
            vals.append(corr_matrix.loc[stocks_in_ind[i], stocks_in_ind[j]])
    print(f"  {industry}: 均值 = {np.mean(vals):.4f}, "
          f"范围 = [{np.min(vals):.4f}, {np.max(vals):.4f}]")

# --- 行业间相关最弱/最强的组合 ---
print("\n" + "-" * 65)
print("行业间相关性最强（跨行业最可能同涨同跌）Top 5:")
inter_sorted = sorted(inter_corrs, key=lambda x: x[2], reverse=True)
for a, b, r in inter_sorted[:5]:
    print(f"  [{stock_industry[a]}] {a} ↔ [{stock_industry[b]}] {b}: r = {r:.4f}")

print("\n行业间相关性最弱（分散投资的最佳选择）Top 5:")
for a, b, r in inter_sorted[-5:]:
    print(f"  [{stock_industry[a]}] {a} ↔ [{stock_industry[b]}] {b}: r = {r:.4f}")

print("\n" + "=" * 65)
print("观察提示：")
print("  - 热力图对角线上的 5 个红色方块 = 行业内部抱团")
print("  - 方块越红 → 同行业股票几乎绑定在一起波动")
print("  - 方块外颜色越浅/越蓝 → 行业间可以分散风险")
print("  - 如果 '行业内部均值' 远高于 '行业间均值'，说明行业壁垒清晰")
print("=" * 65)
