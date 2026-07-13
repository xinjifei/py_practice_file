"""Day 55: SQLite 基础 — SELECT / WHERE / GROUP BY / JOIN"""

import sqlite3
import os
import numpy as np
import pandas as pd

# ============================================================
# 第一步：准备数据 — 生成模拟股票日线 CSV
# ============================================================
np.random.seed(42)

STOCKS = [
    ("600519", "贵州茅台", "白酒"),
    ("002594", "比亚迪",   "新能源车"),
    ("300750", "宁德时代", "电池"),
]

dates = pd.date_range("2024-01-01", "2024-12-31", freq="B")  # 交易日
n_days = len(dates)

rows = []
for code, name, industry in STOCKS:
    # 每只股票模拟一条随机游走价格路径
    base_price = {"600519": 1700, "002594": 250, "300750": 180}[code]
    price = base_price
    for d in dates:
        daily_return = np.random.normal(0.0002, 0.02)  # 日均约 0.02% 涨幅，2% 波动
        price = price * (1 + daily_return)
        open_p = round(price * (1 + np.random.uniform(-0.005, 0.005)), 2)
        close_p = round(price, 2)
        high_p = round(max(open_p, close_p) * (1 + abs(np.random.normal(0, 0.005))), 2)
        low_p = round(min(open_p, close_p) * (1 - abs(np.random.normal(0, 0.005))), 2)
        volume = int(np.random.uniform(1_000_000, 10_000_000))
        rows.append([d.strftime("%Y-%m-%d"), code, name, open_p, high_p, low_p, close_p, volume])

df_daily = pd.DataFrame(rows, columns=["date", "stock_code", "stock_name", "open", "high", "low", "close", "volume"])

# 股票信息表（用于 JOIN）
df_info = pd.DataFrame(STOCKS, columns=["stock_code", "stock_name", "industry"])

# 保存为 CSV
csv_path = os.path.join(os.path.dirname(__file__), "stocks_daily.csv")
df_daily.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"已生成 CSV: {csv_path}")
print(f"数据规模: {len(df_daily)} 行 ({len(STOCKS)} 只股票 × {n_days} 个交易日)")

# ============================================================
# 第二步：创建 SQLite 数据库，导入数据
# ============================================================
db_path = os.path.join(os.path.dirname(__file__), "stocks.db")

# sqlite3.connect() 连接数据库——文件不存在则自动创建
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# CREATE TABLE: 定义表结构（列名 + 数据类型）
cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_prices (
        date         TEXT,
        stock_code   TEXT,
        stock_name   TEXT,
        open         REAL,
        high         REAL,
        low          REAL,
        close        REAL,
        volume       INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_info (
        stock_code  TEXT PRIMARY KEY,
        stock_name  TEXT,
        industry    TEXT
    )
""")

# 用 pandas 把 DataFrame 写入 SQLite
df_daily.to_sql("daily_prices", conn, if_exists="replace", index=False)
df_info.to_sql("stock_info", conn, if_exists="replace", index=False)

print(f"已创建数据库: {db_path}")
print(f"表: daily_prices, stock_info")

# ============================================================
# 第三步：SQL 查询演示
# ============================================================

def run_query(description, sql):
    """执行 SQL 并用 pandas 读取结果"""
    print(f"\n{'='*60}")
    print(f"【{description}】")
    print(f"SQL: {sql}")
    result = pd.read_sql_query(sql, conn)
    print(result.to_string(index=False))
    return result


# --- 3.1 SELECT + WHERE：基础查询 ----------------------------------
run_query(
    "SELECT + WHERE — 查询贵州茅台 2024-03 的所有交易日",
    """
    SELECT date, stock_name, open, close, volume
    FROM daily_prices
    WHERE stock_name = '贵州茅台'
      AND date >= '2024-03-01'
      AND date < '2024-04-01'
    ORDER BY date
    """
)

# --- 3.2 计算涨跌幅列 + WHERE 筛选 --------------------------------
run_query(
    "计算每日涨跌幅 + WHERE 筛选 — 2024年涨幅最大的5天",
    """
    SELECT date,
           stock_name,
           close,
           ROUND((close - open) / open * 100, 2) AS pct_change
    FROM daily_prices
    WHERE strftime('%Y', date) = '2024'
    ORDER BY pct_change DESC
    LIMIT 5
    """
)

# --- 3.3 GROUP BY + 聚合函数 --------------------------------------
run_query(
    "GROUP BY — 每只股票的平均日涨幅(%)、最大单日涨幅、交易天数",
    """
    SELECT stock_name,
           ROUND(AVG((close - open) / open * 100), 4) AS avg_daily_pct,
           ROUND(MAX((close - open) / open * 100), 2) AS max_daily_pct,
           ROUND(MIN((close - open) / open * 100), 2) AS min_daily_pct,
           COUNT(*) AS trading_days
    FROM daily_prices
    GROUP BY stock_name
    ORDER BY avg_daily_pct DESC
    """
)

# --- 3.4 分组 + HAVING 过滤组 -------------------------------------
run_query(
    "GROUP BY + HAVING — 日均成交量超过500万的股票",
    """
    SELECT stock_name,
           ROUND(AVG(volume) / 10000, 0) AS avg_vol_wan,
           COUNT(*) AS days
    FROM daily_prices
    GROUP BY stock_name
    HAVING AVG(volume) > 5000000
    ORDER BY avg_vol_wan DESC
    """
)

# --- 3.5 JOIN — 两张表按 stock_code 关联 ---------------------------
run_query(
    "JOIN — 把 daily_prices 和 stock_info 拼在一起，加行业信息",
    """
    SELECT d.date,
           d.stock_name,
           s.industry,
           d.close,
           ROUND((d.close - d.open) / d.open * 100, 2) AS pct_change
    FROM daily_prices d
    JOIN stock_info s ON d.stock_code = s.stock_code
    WHERE d.date = '2024-06-14'
    ORDER BY d.stock_name
    """
)

# --- 3.6 JOIN + GROUP BY 组合 -------------------------------------
run_query(
    "JOIN + GROUP BY — 按行业统计平均日涨幅",
    """
    SELECT s.industry,
           ROUND(AVG((d.close - d.open) / d.open * 100), 4) AS avg_daily_pct,
           COUNT(*) AS total_records
    FROM daily_prices d
    JOIN stock_info s ON d.stock_code = s.stock_code
    GROUP BY s.industry
    ORDER BY avg_daily_pct DESC
    """
)

# ============================================================
# 第四步：SQL 结果 → pandas DataFrame 做后续处理
# ============================================================
print(f"\n{'='*60}")
print("【SQL 结果写回 pandas DataFrame，继续处理】")

# 用 SQL 查出每只股票的月度平均收盘价
sql_monthly = """
    SELECT stock_name,
           strftime('%Y-%m', date) AS month,
           ROUND(AVG(close), 2) AS avg_close
    FROM daily_prices
    GROUP BY stock_name, strftime('%Y-%m', date)
    ORDER BY stock_name, month
"""
df_monthly = pd.read_sql_query(sql_monthly, conn)

print(f"SQL 返回 DataFrame: {df_monthly.shape[0]} 行 × {df_monthly.shape[1]} 列")
print(df_monthly.head(10).to_string(index=False))

# 在 pandas 里做 SQL 不方便做的事：计算月度环比变化
df_monthly["prev_avg_close"] = df_monthly.groupby("stock_name")["avg_close"].shift(1)
df_monthly["mom_pct"] = (
    (df_monthly["avg_close"] - df_monthly["prev_avg_close"])
    / df_monthly["prev_avg_close"] * 100
).round(2)

print(f"\n月度环比变化 (pandas 计算):")
print(df_monthly.dropna().head(10).to_string(index=False))

# ============================================================
# 第五步：SQL vs pandas — 同一件事，两种写法
# ============================================================
print(f"\n{'='*60}")
print("【SQL vs pandas 对比 — 同一查询两种写法】")
print("查询: 比亚迪 2024年上半年，收盘价 > 250 的交易日，按日期排序\n")

# SQL 写法
print("--- SQL 写法 (1行) ---")
print("""
SELECT date, close
FROM daily_prices
WHERE stock_name = '比亚迪'
  AND date >= '2024-01-01'
  AND date < '2024-07-01'
  AND close > 250
ORDER BY date
""")

# pandas 写法
print("--- pandas 写法 (~8行) ---")
print("""
mask = (
    (df_daily['stock_name'] == '比亚迪')
    & (df_daily['date'] >= '2024-01-01')
    & (df_daily['date'] < '2024-07-01')
    & (df_daily['close'] > 250)
)
result = df_daily[mask].sort_values('date')[['date', 'close']]
""")

# 实际执行两种方式，验证结果一致
sql_result = pd.read_sql_query("""
    SELECT date, close
    FROM daily_prices
    WHERE stock_name = '比亚迪'
      AND date >= '2024-01-01' AND date < '2024-07-01'
      AND close > 250
    ORDER BY date
""", conn)

mask = (
    (df_daily["stock_name"] == "比亚迪")
    & (df_daily["date"] >= "2024-01-01")
    & (df_daily["date"] < "2024-07-01")
    & (df_daily["close"] > 250)
)
pd_result = df_daily[mask].sort_values("date")[["date", "close"]]

print(f"\nSQL 结果: {len(sql_result)} 行")
print(f"pandas 结果: {len(pd_result)} 行")
print(f"结果一致: {sql_result.reset_index(drop=True).equals(pd_result.reset_index(drop=True))}")

# ============================================================
# 收尾
# ============================================================
conn.close()
print(f"\n数据库连接已关闭。")
