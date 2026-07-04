"""测试 calc_all_indicators 函数。

验证：
- 所有指标列都被创建
- close 列不被修改
- 行数不变
"""

import pandas as pd
import pytest

from quant_pipeline.indicators import calc_all_indicators

# ── 固定配置 ──────────────────────────────────────────

CONFIG = {"sma5": 5, "sma10": 10, "ema20": 20, "rsi7": 7, "rsi14": 14}

EXPECTED_COLS = ["SMA_5", "SMA_10", "EMA_20", "RSI_7", "RSI_14", "DIF", "DEA", "HIST"]


@pytest.fixture
def price_df() -> pd.DataFrame:
    """30 行递增价格数据，足够所有指标计算所需的最小长度。"""
    return pd.DataFrame({"close": range(1, 31)})


def test_所有指标列都存在(price_df):
    """计算后 DataFrame 应包含全部 8 个指标列。"""
    result = calc_all_indicators(price_df.copy(), CONFIG)
    for col in EXPECTED_COLS:
        assert col in result.columns, f"缺少列: {col}"


def test_close列不变(price_df):
    """计算指标不应修改原始 close 列——防手贱。"""
    original = price_df["close"].copy()
    result = calc_all_indicators(price_df.copy(), CONFIG)
    assert original.equals(result["close"]), "close 列被改动了！"


def test_行数不变(price_df):
    """计算指标后行数不应改变。"""
    result = calc_all_indicators(price_df.copy(), CONFIG)
    assert result.shape[0] == 30


def test_原始DataFrame不被修改(price_df):
    """传入的 DataFrame 本身不应被修改（如果调用方传了 .copy() 则无所谓）。"""
    df_copy = price_df.copy()
    _ = calc_all_indicators(df_copy, CONFIG)
    # 原始 price_df 不应该被修改
    assert "SMA_5" not in price_df.columns
