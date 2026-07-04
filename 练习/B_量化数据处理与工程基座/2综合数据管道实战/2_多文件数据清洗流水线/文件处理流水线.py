import pandas as pd
from glob import glob
import os

#输出日志函数
def log_write(file_path, log_str):
    with open(file_path, "w", encoding="utf-8")as f:
        f.write("文件清洗记录：\n")
        f.write(log_str)

#单个dataframe清洗函数
def clean_df(df):
    #删除整行都为空的行
    df = df.dropna(how="all")  # how="all" 意为 (怎么删 = 删除所有)
    #删除close数据为空的行
    df = df[df["close"].notna()]
    #重置行索引
    df = df.reset_index(drop=True)
    
    return df

#输出文件夹创建>
#总文件夹
os.makedirs("D:/PY_practice_file/练习/2综合数据管道实战/2多文件数据清洗流水线/result", exist_ok=True)
#清洗后存放文件夹
os.makedirs("D:/PY_practice_file/练习/2综合数据管道实战/2多文件数据清洗流水线/result/cleaned_csv", exist_ok=True)
#日志存放文件夹
os.makedirs("D:/PY_practice_file/练习/2综合数据管道实战/2多文件数据清洗流水线/result/log", exist_ok=True)

#提取数据源地址
path_list = glob("D:/PY_practice_file\练习/2综合数据管道实战/1本地数据源批量读取脚本编写/*.csv")

#依次清洗并保存文件
#初始化计数变量
result_file_name_index = 0
#初始化日志拼接后字符串变量
all_log = ""
error_all_log = ""

for path in path_list:
    #正常情况下
    try:
        #清洗
        df = pd.read_csv(path)
        df_cleaned = clean_df(df)

        #保存清洗后的csv>
        #文件名变量
        result_file_name_index += 1
        result_file_path = \
            "D:/PY_practice_file/练习/2综合数据管道实战/2多文件数据清洗流水线/result/cleaned_csv/result_" + \
            str(result_file_name_index) + \
            ".csv"
        #保存
        df_cleaned.to_csv(result_file_path, index=False, encoding="utf-8")
        
        #拼接日志>
        #单次日志文本
        log_line = f"文件路径={path}，清洗成功，处理后的文件存放路径={result_file_path}\n"
        #拼接单行日志文本
        all_log = all_log + log_line

    #如果错误，导出日志
    except Exception as e:
        #拼接错误日志>
        #单次错误日志文本
        log_line = f"文件={path}，错误原因={e}，清洗失败，错误日志存放路径=D:/PY_practice_file/练习/2综合数据管道实战/2多文件数据清洗流水线/result/log\n"
        #拼接单行错误日志文本
        error_all_log = error_all_log + log_line

#保存日志
log_write("D:/PY_practice_file/练习/2综合数据管道实战/2多文件数据清洗流水线/result/log/success_log.txt", all_log)
log_write("D:/PY_practice_file/练习/2综合数据管道实战/2多文件数据清洗流水线/result/log/error_log.txt", error_all_log)

