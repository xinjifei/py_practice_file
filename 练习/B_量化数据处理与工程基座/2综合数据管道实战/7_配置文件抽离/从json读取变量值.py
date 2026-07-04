import json
import pandas as pd
import pandas_ta_classic as ta
import argparse



def write_json(file_name, data):
    with open (file_name, "w", encoding="utf-8") as f1:
        json.dump(data, f1, ensure_ascii=False, indent=4)

def read_json(file_path):
    with open(file_path, "r", encoding="utf-8")as f:
        parameter = json.load(f)
        return parameter


def calc(df, sma_num, ema_num):
    sma_name = "SMA_" + str(sma_num)
    ema_name = "EMA_" + str(ema_num)
    
    df[sma_name] = ta.sma(df["close"], length=sma_num)
    df[ema_name] = ta.ema(df["close"], length=sma_num)

    print(df[["close", sma_name, ema_name]].head(20))

    return df

def main(json_path):
    parameter = read_json(json_path)
    pr = parameter

    df = pd.read_csv(pr["source_path"])

    calc(df, pr["sma_length"], pr["ema_length"])

    df.to_csv(pr["output_path"], index=False, encoding="utf-8")

if __name__ == "__main__" :
    try:
        parser = argparse.ArgumentParser(description="none")
        parser.add_argument("json_path", help="none")
        args = parser.parse_args()
        json_path = args.json_path
        main(json_path)
        print("成功完成了操作")

    except Exception as e:
        print(f"发生了错误，详见={e}")

        
        
    





