"""
d57 完整的量化分析数据线

akshare数据源
↓
写入SQL数据库
↓
SQL库读回数据
↓
pandas等工具分析数据
↓
plotly可视化显示结果
"""
import akshare as ak #type:ignore
import sqlite3
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import sys
sys.path.insert(0, "D:/PY_practice_file/练习/2_金融基础/2_金融数据源")
from get_data import get_stock_data #type:ignore

#akshare 拉数据
sou_df = get_stock_data(
    symbol="sz000858",
    stock_name="五粮液",
    start_date="20250623",
    end_date="20260623"
)

#写入sql数据库
##先创建
conn = sqlite3.connect("source.db")
##写入
sou_df.to_sql(name="stock_source_daily", con=conn, if_exists="replace",index=False)

#sql读回
def run_query(description:str, sql:str)->pd.DataFrame:
    print(description)
    result = pd.read_sql(sql,conn)
    return result
df = run_query(
    "读取所有行情",
    """
    SELECT *
    FROM stock_source_daily
    ORDER BY date
    """     
    )
#test = df
#统计数据
monthly_stats = run_query(
    "月度统计",
    """
    WITH ranked AS (
        SELECT
            strftime('%Y-%m', date) AS month,
            date, high, low, close, volume,
            ROW_NUMBER() OVER (
                PARTITION BY strftime('%Y-%m', date) ORDER BY date
            ) AS rn_asc,
            ROW_NUMBER() OVER (
                PARTITION BY strftime('%Y-%m', date) ORDER BY date DESC
            ) AS rn_desc
        FROM stock_source_daily
    )
    SELECT
        month                AS 月份,
        ROUND(
            (MAX(CASE WHEN rn_desc = 1 THEN close END) -
             MAX(CASE WHEN rn_asc  = 1 THEN close END)) /
             MAX(CASE WHEN rn_asc  = 1 THEN close END) * 100,
            2
        )                    AS 月涨跌幅,
        ROUND(AVG(volume), 0) AS 月均成交量,
        MAX(high)             AS 月最高价,
        MIN(low)              AS 月最低价
    FROM ranked
    GROUP BY month
    ORDER BY month
    """
)

# 可视化：3张图拼成一份报告
fig = make_subplots(
    rows=3, cols=1,
    subplot_titles=("收盘价走势", "月度涨跌幅(%)", "日成交量"),
    vertical_spacing=0.08
)

# 图1：收盘价折线
fig.add_trace(
    go.Scatter(x=df["date"], y=df["close"], mode="lines",
               line=dict(color="steelblue"), name="收盘价"),
    row=1, col=1
)

# 图2：月度涨跌幅柱状图（正数绿、负数红）
colors = ["green" if v >= 0 else "red" for v in monthly_stats["月涨跌幅"]]
fig.add_trace(
    go.Bar(x=monthly_stats["月份"], y=monthly_stats["月涨跌幅"],
           marker_color=colors, name="月涨跌幅"),
    row=2, col=1
)

# 图3：成交量柱状图
fig.add_trace(
    go.Bar(x=df["date"], y=df["volume"],
           marker_color="lightsteelblue", name="成交量"),
    row=3, col=1
)

fig.update_layout(
    height=900,
    showlegend=False,
    title_text="五粮液(sz000858) 近一年数据报告"
)
fig.show()





