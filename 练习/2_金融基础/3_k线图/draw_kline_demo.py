"""
K线图绘制 —— 演示脚本
用 mplfinance 把 akshare 拉取的日线数据画成标准K线图（含成交量副图）
"""
import pandas as pd
import mplfinance as mpf
from get_stock import pull_stock

# ============================================================
# 第一步：拉取数据（用你写好的 pull_stock 函数）
# ============================================================
# 先拉一只股票试试手，save_csv="yes" 会同时存 CSV 到 ./data/
df = pull_stock(
    symbol="sz000001",      # 股票代码，深市加 sz 前缀
    stock_name="平安银行",
    start_date="20250620",  # 多拉几天，这样图上有足够的 K 线
    end_date="20260623",
    save_csv="yes"
)

# ============================================================
# 第二步：整理成 mplfinance 要求的格式
# ============================================================
# mplfinance 要求：
#   1. date 列必须是 DatetimeIndex（不是普通列）
#   2. 列名必须包含 Open, High, Low, Close, Volume（大小写不敏感）
#
# akshare 返回的 df 列名：date(日期), open(开盘), high(最高), low(最低),
#                        close(收盘), volume(成交量), amount(成交额),
#                        outstanding_share(流通股本), turnover(换手率)
# → 列名已经对齐，只需要把 date 设成索引

df["date"] = pd.to_datetime(df["date"])  # 字符串 → 日期类型
df.set_index("date", inplace=True)       # date 列变成行索引
df.sort_index(inplace=True)              # 按时间升序排列（万一是倒序的）

print("\n整理后的数据预览：")
print(df.head())
print(f"\n数据形状: {df.shape}, 列名: {list(df.columns)}")

# ============================================================
# 第三步：画图 —— mplfinance 核心调用
# ============================================================
# mpf.plot() 的参数按功能分成三块：
#
# 【画什么】
#   type="candle"  → K线风格（空心阳线/实心阴线）
#   volume=True    → 底部加成交量副图
#
# 【外观控制】
#   style="charles" → 配色主题（charles 是黑白配色，适合打印/截图）
#   title="..."     → 图表标题
#   ylabel="价格"   → 纵轴标签
#   ylabel_lower="成交量" → 成交量副图的纵轴标签
#
# 【数据控制】
#   如果不传切片，会画全部数据。数据太多时可以只画最近 N 根：
#   df.tail(60)  → 最近 60 个交易日

# 创建自定义风格：继承 charles 的黑白配色，但字体换成微软雅黑
# make_mpf_style() 把字体嵌入风格对象内部，不会被 mpf 内部覆盖
my_style = mpf.make_mpf_style(
    base_mpf_style="charles",                    # 配色方案继承 charles
    rc={
        "font.sans-serif": ["Microsoft YaHei"],  # 中文字体：Windows 自带微软雅黑
        "axes.unicode_minus": False,             # 负号正常显示，不变成方块
    }
)

mpf.plot(
    df,
    type="candle",
    volume=True,
    title="平安银行 日K线图",
    ylabel="价格（元）",
    ylabel_lower="成交量",
    style=my_style,           # 用自定义风格对象，不用字符串
    figsize=(14, 7),
    # savefig="./data/平安银行_kline.png"  # 需要保存图片时取消这行注释
)

print("\nK线图窗口已弹出。关闭窗口后程序结束。")

# ============================================================
# 关于弹窗 vs 保存
# ============================================================
#   mpf.plot() 不传 savefig  → 弹窗显示（可以缩放、拖拽）
#   mpf.plot() 传了 savefig  → 只保存文件，不弹窗
#   想两个都要？跑两遍 mpf.plot()，一次不传 savefig，一次传


# ============================================================
# 附：mplfinance 常用配色 style 一览
# ============================================================
# "charles"   — 黑白配，阳线白底黑边，阴线黑底
# "binance"   — 模仿币安配色，绿涨红跌
# "yahoo"     — 模仿雅虎财经
# "tradingview" — 类似 TradingView（需要额外配置）
# "default"   — matplotlib 默认色
#
# 红涨绿跌 vs 绿涨红跌：
# A股习惯"红涨绿跌"，但 mplfinance 默认是西方习惯"绿涨红跌"。
# 要改成红涨绿跌，用 marketcolors 自定义颜色（进阶操作，后续讲）
