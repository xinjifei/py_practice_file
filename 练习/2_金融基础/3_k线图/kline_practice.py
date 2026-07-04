#导入库
import pandas as pd
import os
import mplfinance as mpf
from get_stock import pull_stock

#画图函数
def draw_kline(
        symbol:str,
        stock_name:str,
        start_date:str,
        end_date:str,
        save_csv:str="no"
        ):
    #创建输出文件夹
    os.makedirs("./data/",exist_ok=True)
    
    #抓数据
    df = pull_stock(
        symbol,
        stock_name,
        start_date,
        end_date,
        save_csv
    )
    #重置行索引为绝对日期
    df["date"] = pd.to_datetime(df["date"])  # 字符串变成日期类型
    df.set_index("date", inplace=True)       # date 列变成行索引

    #画图风格设置
    style_config = mpf.make_mpf_style(
        base_mpf_style="charles",
        rc={
            "font.sans-serif": ["Microsoft YaHei"],
            "axes.unicode_minus": False
        }
    )

    #画图
    try:
        mpf.plot(
            df,
            type="candle",
            volume=True,
            title=stock_name,
            ylabel="价格（元）",
            ylabel_lower="成交量",
            style=style_config,           # 用自定义风格对象，不用字符串
            figsize=(14, 7),
            savefig="./data/" + stock_name + ".png"
        )
        print("画图正常")

    except Exception as e:
        print(f"画图错误，原因{e}")
    

#调用画图函数输出
if __name__ == "__main__":
    print("画图示例开始")
    draw_kline(
        symbol="sz000001",      # 股票代码，深市加 sz 前缀
        stock_name="平安银行",
        start_date="20250620",  # 多拉几天，这样图上有足够的 K 线
        end_date="20260623"
    )

    draw_kline(
        symbol="sz000858",      # 股票代码，深市加 sz 前缀
        stock_name="五粮液",
        start_date="20250620",  # 多拉几天，这样图上有足够的 K 线
        end_date="20260623"
    )

    draw_kline(
        symbol="sz300750",      # 股票代码，深市加 sz 前缀
        stock_name="宁德时代",
        start_date="20250620",  # 多拉几天，这样图上有足够的 K 线
        end_date="20260623"
    )


    
