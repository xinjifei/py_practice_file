# 导入库
import akshare as ak
import os
OUTPUT_DIR = "D:/PY_practice_file/练习/2_金融基础/2_金融数据源/output/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 拉取数据
def get_stock_data(
        symbol:str, 
        stock_name:str,
        start_date:str,
        end_date:str
        ):
    df = ak.stock_zh_a_daily(
        #函数名含义翻译：akshare简写_股票类型数据_中国地区_a股_历史记录
        symbol = symbol, #股票代码
        start_date =start_date, # 字面意思
        end_date = end_date,
        adjust = ""
        )
    print(f"==========={stock_name}============")
    print ("df类型 = ",type(df))
    print("df形状 =",df.shape)
    print("行数 =", len(df))
    print("起始日期 =", start_date)
    print("截止日期 =", end_date)
    print(df.head(10))
    #df.to_csv(
        #OUTPUT_DIR + f"{stock_name}.csv", index=False, encoding="utf-8-sig")
    return df

if __name__ == "__main__":
    get_stock_data(
        symbol="sz000001", 
        stock_name="平安银行",
        start_date="20250623",
        end_date="20260623"
        )
    get_stock_data(
        symbol="sz000858", 
        stock_name="五粮液",
        start_date="20250623",
        end_date="20260623"
        )
    get_stock_data(
        symbol="sz300750", 
        stock_name="宁德时代",
        start_date="20250623",
        end_date="20260623"
        )
