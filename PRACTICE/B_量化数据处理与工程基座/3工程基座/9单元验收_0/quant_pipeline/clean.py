"""数据清洗模块。

提供 clean_df 函数，负责：
- 删除全空行
- 删除 close 列为空的行
- 重置行索引
"""

import pandas as pd


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """清洗 DataFrame。

    执行三个操作：
    1. 删除整行都为 NaN 的行
    2. 删除 close 列为 NaN 的行（核心价格数据不能缺）
    3. 重置索引，从 0 开始连续编号

    Args:
        df: 原始行情 DataFrame，必须包含 "close" 列

    Returns:
        清洗后的 DataFrame，索引从 0 开始连续

    Examples:
        >>> df = pd.DataFrame({"close": [100, None, 102], "volume": [1000, 500, 2000]})
        >>> clean_df(df).shape[0]
        2
    """
    df = df.dropna(how="all")
    df = df[df["close"].notna()]
    df = df.reset_index(drop=True)
    return df
