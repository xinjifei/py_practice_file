'''自动读取昨天 cleaned_csv 下所有清洗好的 CSV
调用 calc_all_indicators 批量加全套指标
自动创建 indicators_output 文件夹存放结果
记录指标计算成功日志、错误日志
故意留一个格式异常文件，测试脚本能否跳过不崩'''

import pandas as pd
import pandas_ta_classic as ta
from glob import glob
import os

#定义全套指标计算函数>>>>>>>>>>
def calc_all_indictors(file_path):
    df = pd.read_csv(file_path)
    
    #移动平均值
    df["SMA_5"] = ta.sma(df["close"], 5)
    df["SMA_10"] = ta.sma(df["close"], 10)

    #指数移动值
    df["EMA_20"] = ta.ema(df["close"], 20)

    #相对强弱值
    df["RSI_7"] = ta.rsi(df["close"], 7)
    df["RSI_14"] = ta.rsi(df["close"], 14)

    #指数平滑异同平均值三件套>
    macd = ta.macd(df["close"])
    #差离值
    df["DIF"] = macd["MACD_12_26_9"]
    #平滑差离值
    df["DEA"] = macd["MACDs_12_26_9"]
    #离差值
    df["HIST"] = macd["MACDh_12_26_9"]

    #返回单个dataframe的计算结果
    return df

#定义日志写入函数>>>>>>>>>>
def write_log(txt_path, log, tips):
    with open(txt_path, "w", encoding="utf-8")as f:
        f.write(tips)
        f.write(log)

#创建输出文件夹>>>>>>>>>>>>>
os.makedirs("D:/PY_practice_file/练习/2综合数据管道实战/3_指标批量计算脚本/result", exist_ok=True)
os.makedirs("D:/PY_practice_file/练习/2综合数据管道实战/3_指标批量计算脚本/result/indictors", exist_ok=True)
os.makedirs("D:/PY_practice_file/练习/2综合数据管道实战/3_指标批量计算脚本/result/log", exist_ok=True)

#获取数据源文件路径列表>>>>>>>>>>>>
all_path = glob("D:/PY_practice_file/练习/2综合数据管道实战/2_多文件数据清洗流水线/result/cleaned_csv/*.csv") 

success_all_log_str = ""
error_all_log_str = ""
result_file_name_index = 0
#循环计算+存储+日志文本拼接>>>>>>>>>>>>>>>
for path in all_path:
    try:
        #引用指标计算函数
        after_df = calc_all_indictors(path)
        #保存至文件>
        #文件名拼接
        result_file_name_index += 1
        result_file_path = \
        "D:/PY_practice_file/练习/2综合数据管道实战/3_指标批量计算脚本/result/indictors/"+\
        str(result_file_name_index)+\
        "_after_calk.csv"
        after_df.to_csv(result_file_path, index=False, encoding="utf-8")
        #成功日志文本拼接
        success_all_log_str = success_all_log_str + f"处理成功，处理后文件保存路径{result_file_path}\n"
        
        print(f"第{result_file_name_index}个文件处理成功")

    except Exception as e:
        #错误信息文本拼接
        error_all_log_str = error_all_log_str + f"处理失败，原因={e}\n"

#日志文本写入文件>>>>>>>>>>>
write_log("D:/PY_practice_file/练习/2综合数据管道实战/3_指标批量计算脚本/result/log/success_log.txt", success_all_log_str, "success:\n")
write_log("D:/PY_practice_file/练习/2综合数据管道实战/3_指标批量计算脚本/result/log/error_log.txt", error_all_log_str, "error:\n")

#打印结束>>>>>>>>>>>>>>>
print("程序结束")