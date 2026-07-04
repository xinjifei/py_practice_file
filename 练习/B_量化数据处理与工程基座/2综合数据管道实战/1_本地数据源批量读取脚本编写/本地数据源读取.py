import pandas as pd
#glob 批量找文件
#导入库(从函数文件中引用特定的函数，而不是所有函数，用于简化)
from glob import glob

def write_log(file_path, log_str):
    with open(file_path, "w", encoding="utf8")as f:
        f.write("文件读取记录：\n")
        f.write(log_str)
#找出某目录中所有的某类型文件（比如下面的.csv），输出为存放着文件路径的路径
file_list = glob("D:\PY_practice_file\练习/1本地数据源批量读取脚本编写\*.csv")

#print(file_list)

#for 循环批量读取
#新建用于存放所有dataframe的空列表
all_csv_read = []
#用于存放日志文本
all_log_str = ""
#循环file_list中的路径，逐个读取
for file_path in file_list:
    df = pd.read_csv(file_path)
    #将读取到的dataframe添加到列表
    all_csv_read.append(df)
    print(f"读取成功，源文件路径={file_path}")

    #创建日志文本
    log_str = f"文件路径={file_path}，读取成功\n"
    #添加单条文本到
    all_log_str = all_log_str + log_str

#导出读取日志
log_txt_path = "D:/PY_practice_file/练习/1本地数据源批量读取脚本编写/log.txt"

write_log(log_txt_path, all_log_str)

print("结束")
#for df in all_csv_read:
#    print(df[["close"]].head(31))