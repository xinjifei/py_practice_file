"""被测试的代码模块"""

import pandas as pd


def clean_df(df):
    """清洗 DataFrame：删全空行、删 close 为空的行、重置索引"""
    df = df.dropna(how="all")
    df = df[df["close"].notna()]
    df = df.reset_index(drop=True)
    return df
