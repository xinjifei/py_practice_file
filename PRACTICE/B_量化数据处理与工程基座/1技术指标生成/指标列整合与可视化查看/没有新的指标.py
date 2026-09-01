import pandas as pd
import pandas_ta_classic as ta

def indicators_cal(data_file, result_file, log_file):
    df = pd.read_csv(data_file)  #使用到值(data_file)

    def write_txt(file_name, str_data):
        try:
            with open(file_name, "w", encoding="utf8")as f:
                f.write(str_data)
        except TypeError:
            print("写入的数据源不是字符串")

    #rsi
    df["RSI_7"] = ta.rsi(df["close"], length=7)
    df["RSI_14"] = ta.rsi(df["close"], length=14)

    #macd三件套（直接生成出来的是字典数据，上面生成的是单列数据）
    macd = ta.macd(df["close"])
    df["DIF"] = macd["MACD_12_26_9"]
    df["DEA"] = macd["MACDs_12_26_9"]
    df["HIST"] = macd["MACDh_12_26_9"]

    #临时查看
    #print(df[["close", "RSI_7", "RSI_14", "DIF", "DEA", "HIST"]].head(50))

    #把经过处理的df表格存至csv文件
    df.to_csv(result_file, index=False, encoding="utf8")  #使用到值(result_file)

    #输出txt日志
    show_str = (df[["close", "RSI_7", "RSI_14", "DIF", "DEA", "HIST"]].head(5))
    write_txt(log_file, str(show_str))  #用到值（log_file）


data_file = "D:\PY_practice_file\练习\指标列整合与可视化查看\data.csv"
result_file= "D:\PY_practice_file\练习\指标列整合与可视化查看/result.csv"
log_file= "D:\PY_practice_file\练习\指标列整合与可视化查看/log.txt"

indicators_cal(data_file, result_file, log_file)




    
