import akshare as ak
import os
OUTPUT_DIR = "./data/"

def pull_stock(
        symbol:str,
        stock_name:str,
        start_date:str,
        end_date:str,
        save_csv:str="no"
        ):
    df = ak.stock_zh_a_daily(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        adjust="",
    )

    print()
    print(f"==============={stock_name}===============")
    print(f"区间={start_date}~{end_date}")
    print(f"数据源=新浪财经")
    print(f"数据周期=日")
    print("前十行预览：")
    print(df.head(10))
    
    if save_csv == "yes":
        os.makedirs(OUTPUT_DIR,exist_ok=True)
        df.to_csv(OUTPUT_DIR + stock_name + ".csv",  index=False, encoding="utf-8-sig")
        print("保存了csv文件")
    return df
