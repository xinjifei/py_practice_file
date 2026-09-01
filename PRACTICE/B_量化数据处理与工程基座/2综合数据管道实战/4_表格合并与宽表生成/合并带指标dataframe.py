import pandas as pd
from glob import glob
import os

#新建合并后文件
os.makedirs("D:/PY_practice_file/练习/2综合数据管道实战/4_表格合并与宽表生成/result", exist_ok=True)
os.makedirs("D:/PY_practice_file/练习/2综合数据管道实战/4_表格合并与宽表生成/log",exist_ok=True)

#定义写入日志函数
def write_log(log_path, log_str):
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(log_str)

#读取第三天练习题的成果（三个csv文件）>>>
#获取路径
source_list = glob("D:/PY_practice_file/练习/2综合数据管道实战/3_指标批量计算脚本/result/indictors/*.csv") #变量数据源路径

#循环读取并将dataframe添加至总列表>>>
count = 0
df_list = []
suc_all = ""
error_all = ""
for source in source_list:
    count += 1
    
    try:
        df = pd.read_csv(source)
        df_list.append(df)
        #拼接日志文本
        suc_all = suc_all + "第" + str(count) + "个文件读取成功，一共" + str(len(df)) + "行\n" 
    
    except Exception as e:
        #拼接日志文本
        error_all = error_all + "第" + str(count) + "个文件读取失败\n"
    
#拼接总列表里面的dataframe>>>
final_df = pd.concat(df_list, ignore_index=True)

#保存拼接后的dataframe>>>
final_df.to_csv("D:/PY_practice_file/练习/2综合数据管道实战/4_表格合并与宽表生成/result/result.csv", index=False)

#将拼接后的日志文本保存（日志需要包含，总文件数、每个文件行数、合并后总行数）>>>
#成功
final_suc_log = \
suc_all + \
"总文件数=" + str(count) + "\n" +\
"合并后总行数=" + str(len(final_df))
write_log("D:/PY_practice_file/练习/2综合数据管道实战/4_表格合并与宽表生成/log/success_log.txt", final_suc_log)
#错误
final_error_log = \
error_all
write_log("D:/PY_practice_file/练习/2综合数据管道实战/4_表格合并与宽表生成/log/error_log.txt", final_error_log)