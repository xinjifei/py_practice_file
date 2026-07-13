"""
d54_交互式图表 — 演示文件
一张可交互的股价走势图（含成交量副图），导出为 HTML 在浏览器打开即可交互。
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# 0. 构造模拟数据 —— 一支股票 120 个交易日的 OHLCV
#    （实际项目用 yfinance 或 akshare 拉真实数据即可，逻辑完全一样）
# ============================================================
np.random.seed(42)
n = 120
dates = pd.date_range("2025-01-02", periods=n, freq="B")

# 用随机游走生成价格序列：每天在上一日基础上乘以 (1 + 随机收益率)
daily_returns = np.random.normal(0.0005, 0.018, n)  # 均值≈0.05%/天，波动≈1.8%/天
close = 100 * np.cumprod(1 + daily_returns)          # 从 100 元起步

# 从收盘价反推 OHLC（模拟日内波动）
high  = close * (1 + np.abs(np.random.normal(0, 0.015, n)))   # 最高价 ≈ 收盘价的上方波动
low   = close * (1 - np.abs(np.random.normal(0, 0.015, n)))   # 最低价 ≈ 收盘价的下方波动
open_ = close * (1 + np.random.normal(0, 0.008, n))           # 开盘价 ≈ 收盘价附近

# 成交量：随机生成，确保非负
volume = np.abs(np.random.normal(5_000_000, 1_500_000, n)).astype(int)

# 计算涨跌幅（相对于前一日收盘）
change_pct = np.round((close - np.roll(close, 1)) / np.roll(close, 1) * 100, 2)
change_pct[0] = 0  # 第一天没有前日数据可比较

# 组装 DataFrame
df = pd.DataFrame({
    "date":      dates,
    "open":      np.round(open_, 2),
    "high":      np.round(high, 2),
    "low":       np.round(low, 2),
    "close":     np.round(close, 2),
    "volume":    volume,
    "change_pct": change_pct,
})

# ============================================================
# 1. 创建双面板画布 —— make_subplots
#    上面是 K 线图（价格），下面是柱状图（成交量），共享 X 轴
#    rows=2, cols=1: 两行一列
#    row_heights: 上面占 70%，下面占 30%
#    shared_xaxes=True: 拖动缩放时上下同步
# ============================================================
fig = make_subplots(
    rows=2, cols=1,
    row_heights=[0.7, 0.3],       # 价格图占 7 成高度，成交量占 3 成
    shared_xaxes=True,             # 共享 X 轴——缩放/拖拽时间范围时上下同步
    vertical_spacing=0.03,         # 两块之间的间隙很小
    subplot_titles=("股价走势（OHLC）", "成交量"),  # 每块的小标题
)

# ============================================================
# 2. 上层：K 线图（Candlestick）
#    K 线是金融领域看价格的标配——一根"蜡烛"同时展示开/高/低/收四个值
#    - 红色实体：收盘 < 开盘，跌了
#    - 绿色实体：收盘 > 开盘，涨了
#    - 上下影线：当日最高价和最低价的范围
# ============================================================
candlestick = go.Candlestick(
    x=df["date"],
    open=df["open"],
    high=df["high"],
    low=df["low"],
    close=df["close"],
    name="OHLC",                    # 图例上的名字
    showlegend=True,
    # ---- 悬停信息模板 ----
    # %{x|%Y-%m-%d}  → 日期格式化
    # %{customdata[0]} → 涨跌幅（我们通过 customdata 传入）
    hovertemplate=(
        "<b>日期</b>: %{x|%Y-%m-%d}<br>"
        "<b>开盘</b>: %{open:.2f}<br>"
        "<b>最高</b>: %{high:.2f}<br>"
        "<b>最低</b>: %{low:.2f}<br>"
        "<b>收盘</b>: %{close:.2f}<br>"
        "<b>涨跌幅</b>: %{customdata[0]:+.2f}%<br>"
        "<extra></extra>"            # 去掉 trace 名字（不显示 "OHLC"）
    ),
    customdata=df[["change_pct"]],   # 传入额外数据供 hovertemplate 使用
)

fig.add_trace(candlestick, row=1, col=1)

# ============================================================
# 3. 下层：成交量柱状图
#    颜色跟着涨跌走——涨了红色，跌了绿色
# ============================================================
# 根据涨跌决定颜色
vol_colors = ["#ef5350" if pct >= 0 else "#26a69a" for pct in df["change_pct"]]

volume_bars = go.Bar(
    x=df["date"],
    y=df["volume"],
    name="成交量",
    showlegend=True,
    marker_color=vol_colors,         # 涨红跌绿
    marker_line_width=0,             # 柱子之间不需要边框线
    # ---- 悬停信息 ----
    hovertemplate=(
        "<b>日期</b>: %{x|%Y-%m-%d}<br>"
        "<b>成交量</b>: %{y:,.0f} 股<br>"
        "<extra></extra>"
    ),
)

fig.add_trace(volume_bars, row=2, col=1)

# ============================================================
# 4. 添加一根 5 日均线到上层图
#    均线是最简单的趋势指标——把短期波动"抹平"，看大方向
# ============================================================
df["ma5"] = df["close"].rolling(window=5).mean()  # 5 日简单移动平均

ma5_line = go.Scatter(
    x=df["date"],
    y=df["ma5"],
    mode="lines",                    # 只画线，不画点
    name="MA5（5日均线）",
    line=dict(color="#ff9800", width=2, dash="dash"),  # 橙色虚线
    hovertemplate=(
        "<b>MA5</b>: %{y:.2f}<br>"
        "<extra></extra>"
    ),
)

fig.add_trace(ma5_line, row=1, col=1)

# ============================================================
# 5. 全局布局配置
#    - 标题、坐标轴标签
#    - X 轴范围滑块（底部的缩略图，拖动选择时间范围）
#    - 交互工具栏（右上角的按钮组）
# ============================================================
fig.update_layout(
    title=dict(
        text="XX 股票 交互式走势图（120 个交易日）",
        font=dict(size=20),
        x=0.5,                       # 标题居中
    ),
    # 底部范围滑块：一拖一拉就能选时间范围
    xaxis_rangeslider_visible=False,  # K 线图自带的范围滑块关掉（我们用下面的）
    # 底层 X 轴（成交量图下方）加范围滑块
    xaxis2_rangeslider=dict(
        visible=True,
        thickness=0.05,              # 滑块的厚度
    ),
    # 悬停模式：同一 X 坐标上的所有 trace 一起显示
    hovermode="x unified",
    # 整体背景配色
    template="plotly_white",
    height=750,                      # 图的总高度（像素）
    # 图例放在下方
    legend=dict(
        orientation="h",             # 水平排列
        yanchor="top",
        y=-0.15,                     # 放到图下方
        xanchor="center",
        x=0.5,
    ),
)

# Y 轴标签
fig.update_yaxes(title_text="价格（元）", row=1, col=1)
fig.update_yaxes(title_text="成交量（股）", row=2, col=1)
fig.update_xaxes(title_text="日期", row=2, col=1)

# ============================================================
# 6. 导出为 HTML 文件
#    双击 d54_交互式股价图.html，浏览器就会打开
#    所有交互功能都在里面——悬停、缩放、平移、图例切换、截图
# ============================================================
output_path = "./d54_交互式图标/d54_交互式股价图.html"
fig.write_html(output_path)
print(f"✅ 交互式图表已保存为 {output_path}")
print("   双击该文件，浏览器打开即可交互。")
print("   试试：鼠标悬停看数值 | 底部滑块拖选时间范围 | 点击图例隐藏/显示某条线")

# 如果你在 Jupyter Notebook 里运行，取消下面这行的注释就能直接看到图：
# fig.show()
