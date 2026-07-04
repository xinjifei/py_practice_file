#导入库
import sqlite3
import pandas as pd
import plotly.express as px

#建立连接
db_PATH = "D:/PY_practice_file/练习/4_SQLite基础数据处理整合/d55_SQLite基础_SELECT_WHERE_GROUPBY_JOIN/stocks.db"
conn = sqlite3.connect(db_PATH)

#读取转dataframe
##读取函数
def run_query(description:str, sql:str) ->pd.DataFrame:
    print(description)
    result = pd.read_sql_query(sql, conn)
    return result

##读取
df = run_query(
    "读取茅台一年的收益率",
    """
    SELECT *
    FROM daily_prices
    WHERE stock_name = '贵州茅台'
        AND date > '2023-12-31'
        AND date <= '2024-12-31'
    ORDER BY date
    """
)
#test = df

#用pandas算收益率
df["daily_return"] = df["close"].pct_change()
monthly_avg = df.groupby(
    df["date"].str[:7])["daily_return"].mean()
print("月均收入")
print(type(monthly_avg),monthly_avg)
df_plot = monthly_avg.reset_index()
df_plot.columns = ["month", "avg_return"]

#用plotly输出收益率柱状图
fig = px.bar(
    df_plot, x="month", y="avg_return",
    title="贵州茅台 2024 月度平均日收益率"
    )
fig.show()

#导到数据库
df_plot.to_sql("monthly_returns", 
               conn, 
               if_exists="replace", 
               index=False)

conn.close()