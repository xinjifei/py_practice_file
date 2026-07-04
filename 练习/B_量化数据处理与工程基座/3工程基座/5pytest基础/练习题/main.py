"""
在第 5 天代码基础上升级
用 try-except 包裹每个文件的处理
    读取
    清洗
    计算指标
    文件损坏 → 跳过，不崩整个程序
用 pathlib 管理所有输出目录
统计
    总文件数
    成功数
    失败数
输出
    final_dataset.csv
    skip_report.txt（失败文件列表）
运行测试要求
    故意放 3 个损坏文件 进数据文件夹，验证：
    程序不崩
    成功文件正常处理
    失败文件被记录
"""

import json
import pandas as pd
import pandas_ta_classic as ta
from glob import glob
import os
import argparse
import datetime
import sys
from pathlib import Path


# 清洗函数
def clean_df(df):
    # 删除整行都为空的行
    df = df.dropna(how="all")
    # 删除close数据为空的行
    df = df[df["close"].notna()]
    # 重置行索引
    df = df.reset_index(drop=True)

    return df


# 指标计算函数
def calc_all_indicators(df, config):
    # 移动平均值
    df["SMA_5"] = ta.sma(df["close"], config["sma5"])
    df["SMA_10"] = ta.sma(df["close"], config["sma10"])

    # 指数移动值
    df["EMA_20"] = ta.ema(df["close"], config["ema20"])

    # 相对强弱值
    df["RSI_7"] = ta.rsi(df["close"], config["rsi7"])
    df["RSI_14"] = ta.rsi(df["close"], config["rsi14"])

    # 指数平滑异同平均值三件套
    macd = ta.macd(df["close"])
    # 差离值
    df["DIF"] = macd["MACD_12_26_9"]
    # 平滑差离值
    df["DEA"] = macd["MACDs_12_26_9"]
    # 离差值
    df["HIST"] = macd["MACDh_12_26_9"]

    return df


# 主流水线函数
def run_pipeline(input_dir, output_dir, config):
    # 1. glob读所有csv
    path_list = glob(os.path.join(input_dir, "*.csv"))
    file_count = len(path_list)

    # 2. 循环读取→清洗→算指标
    all_df_list = []
    error_str_all = ""
    count_all = 0
    success_count = 0
    error_count = 0
    for path in path_list:
        count_all += 1
        try:
            df = pd.read_csv(path)
            df = clean_df(df)
            df = calc_all_indicators(df, config)
            all_df_list.append(df)
            success_count += 1
            print(f"第{success_count}个文件处理成功")
            
        except Exception as e:
            error_count += 1
            print(f"第{error_count}个文件处理失败，失败原因={e}")
            #拼接添加跳过处理日志文本
            error_str = "第" + str(count_all) + f"个文件处理失败，失败原因={e}，处理失败的文件共有{error_count}\n"
            error_str_all = error_str_all + error_str

    # 3. 合并、保存
    final_df = pd.concat(all_df_list, ignore_index=True)
    output_name = output_dir + "final_dataset.csv"
    final_df.to_csv(output_name , index=False, encoding="utf-8")

    return final_df, file_count, count_all, success_count, error_count, error_str_all


# 程序入口
if __name__ == "__main__":
    # 拿参数
    parser = argparse.ArgumentParser(description="数据流水线：读取csv→清洗→算指标→合并")
    parser.add_argument("config_path", help="配置文件路径")
    args = parser.parse_args()

    # 读取配置文件
    with open(args.config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 从配置读取路径
    input_dir = config["input_dir"]
    output_dir = config["output_dir"]

    #判断数据源是否存在
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"路径*{input_path}*下没有数据源文件，程序终止")
        sys.exit()

    #新建输出文件夹
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
        

    # 计时
    start_time = datetime.datetime.now()
    start_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"开始时间：{start_str}")

    # 调用run_pipeline
    final_df, file_count,count_all, success_count, error_count, error_str_all = run_pipeline(input_dir, output_dir, config)

    # 计时
    end_time = datetime.datetime.now()
    end_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
    duration = end_time - start_time

    print(f"结束时间：{end_str}")
    print(f"总耗时：{duration}")
    print(f"处理文件数：{file_count}")
    print(f"最终行数：{len(final_df)}")

    # 写日志
    log_file_name = output_dir + f"run_log_{start_time.strftime('%Y%m%d')}.txt"
    with open(log_file_name, "w", encoding="utf-8") as f:
        f.write(f"开始时间：{start_str}\n")
        f.write(f"结束时间：{end_str}\n")
        f.write(f"总耗时：{duration}\n")
        f.write(f"处理文件数：{file_count}\n")
        f.write(f"最终行数：{len(final_df)}\n")
        f.write(f"处理成功文件数：{success_count}\n")
        f.write(f"处理失败文件数：{error_count}（具体错误日志见./error_log）\n")
    
    error_log_path = output_dir + f"error_log_{start_time.strftime('%Y%m%d')}.txt"
    with open(error_log_path, "w", encoding="utf-8") as f:
        f.write(f"因错误而跳过处理的文件\n：{error_str_all}\n")
