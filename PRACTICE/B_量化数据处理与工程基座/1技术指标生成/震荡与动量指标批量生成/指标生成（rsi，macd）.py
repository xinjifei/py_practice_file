import pandas as pd
import pandas_ta_classic as ta

#从文件中读取表格到pandas``
df = pd.read_csv("D:\PY_practice_file\练习\震荡与动量指标批量生成\data.csv")

#新建不同区间的指数移动平均线（rsi）列到df
df["RSI_7"] = ta.rsi(df["close"], length=7)
df["RSI_14"] = ta.rsi(df["close"], length=14)

#print(df[["close", "RSI_7", "RSI_14"]].head(40))
#新建macd三件套列

#先赋值存储三件套的字典
macd = ta.macd(df["close"])
#添加三件套到当前加载的pandas表格
df["DIF"] = macd["MACD_12_26_9"]
df["DEA"] = macd["MACDs_12_26_9"]
df["HIST"] = macd["MACDh_12_26_9"]

#打印观察最后的结果
print(df[["close", "RSI_7", "RSI_14", "DIF", "DEA", "HIST"]].head(40))

df.to_csv("rsi_macd.csv", index=False, encoding="utf8")