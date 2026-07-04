"""技术指标计算模块。

提供 calc_all_indicators 函数，计算：
- SMA (简单移动平均): 5日、10日
- EMA (指数移动平均): 20日
- RSI (相对强弱指标): 7日、14日
- MACD 三件套: DIF、DEA、HIST
"""

import pandas as pd
import pandas_ta_classic as ta


def calc_all_indicators(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """根据配置计算全部技术指标。

    指标列表：
    - SMA_5, SMA_10 (均线)
    - EMA_20 (指数均线)
    - RSI_7, RSI_14 (相对强弱)
    - DIF, DEA, HIST (MACD 三件套)

    Args:
        df: 包含 "close" 列的行情 DataFrame
        config: 指标参数字典，必须包含以下键:
            sma5, sma10, ema20, rsi7, rsi14

    Returns:
        在原 DataFrame 基础上追加了指标列的 DataFrame

    Note:
        - 不会修改原始传入的 DataFrame（取决于调用方是否 .copy()）
        - close 列的值不会改变
        - 行数不会改变
    """
    df["SMA_5"] = ta.sma(df["close"], length=config["sma5"])
    df["SMA_10"] = ta.sma(df["close"], length=config["sma10"])

    df["EMA_20"] = ta.ema(df["close"], length=config["ema20"])

    df["RSI_7"] = ta.rsi(df["close"], length=config["rsi7"])
    df["RSI_14"] = ta.rsi(df["close"], length=config["rsi14"])

    macd = ta.macd(df["close"])
    df["DIF"] = macd["MACD_12_26_9"]
    df["DEA"] = macd["MACDs_12_26_9"]
    df["HIST"] = macd["MACDh_12_26_9"]

    return df
