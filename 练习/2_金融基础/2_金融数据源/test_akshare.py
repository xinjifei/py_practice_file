"""akshare 安装验证脚本——只拉取 5 天数据，确认库能正常工作"""
import akshare as ak

# 取平安银行最近 5 个交易日的日线数据，不复权
df = ak.stock_zh_a_hist(
    symbol="000001",
    period="daily",
    start_date="20250616",
    end_date="20250623",
    adjust=""
)

print("akshare 安装正常，数据拉取成功！\n")
print(f"行数: {len(df)}")
print(f"列数: {df.shape[1]}")
print(f"列名: {df.columns.tolist()}\n")
print(df)
