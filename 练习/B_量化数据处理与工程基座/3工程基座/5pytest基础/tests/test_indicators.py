"""
测试 calc_all_indicators 函数
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from 练习题.main import calc_all_indicators


config = {
    "sma5": 5, "sma10": 10, "ema20": 20,
    "rsi7": 7, "rsi14": 14
}


# ============ 测试1：验证新增的列都存在 ============
def test_calc_indicators_新增列存在():
    """计算后 DataFrame 应该包含所有指标列"""
    # 最少需要 26 行才能跑完 SMA(10)、EMA(20)、RSI(14) 和 MACD(12,26,9)
    df = pd.DataFrame({"close": range(1, 31)})  # 30 行，够用且不浪费

    result = calc_all_indicators(df.copy(), config)

    expected_cols = ["SMA_5", "SMA_10", "EMA_20", "RSI_7", "RSI_14", "DIF", "DEA", "HIST"]
    for col in expected_cols:
        assert col in result.columns, f"缺少列: {col}"


# ============ 测试2：close 列的值不能变（防手贱） ============
def test_calc_indicators_close列不变():
    """计算指标不应该修改原始 close 列——防未来的自己或别人改错"""
    df = pd.DataFrame({"close": range(100, 131)})

    original_close = df["close"].copy()
    result = calc_all_indicators(df.copy(), config)

    # close 列的值应该和原来完全一样
    assert original_close.equals(result["close"]), "close 列被改动了！"


# ============ 测试3：行数不变 ============
def test_calc_indicators_行数不变():
    """计算指标后行数不应该变"""
    df = pd.DataFrame({"close": range(1, 31)})

    result = calc_all_indicators(df.copy(), config)

    assert result.shape[0] == 30
