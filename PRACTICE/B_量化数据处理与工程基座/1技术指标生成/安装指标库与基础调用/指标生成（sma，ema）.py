#
import pandas as pd
import pandas_ta_classic as ta
#pandas读取csv文件函数
df = pd.read_csv("./练习/安装指标库与基础调用/read.csv")

#在读取的内容中新建列数据；pandas-ta计算金融数据函数（输入值格式：数据源列， 指标
df["SMA_5"] =   ta.sma(df["收盘价"], length=5)
df["SMA_10"] = ta.sma(df["收盘价"], length=10)
df["EMA_20"] = ta.ema(df["收盘价"], length=20)

print("生成指标成功")

print(df[["收盘价", "SMA_5", "SMA_10", "EMA_20"]].head(20))

df.to_csv("indictors.csv", index=False, encoding="utf-8")

print("文件成功保存")


