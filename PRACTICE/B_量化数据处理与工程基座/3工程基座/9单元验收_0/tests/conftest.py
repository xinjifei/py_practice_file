"""pytest 公共物资仓库.

所有测试函数共享的 fixture 定义在这里.
pytest 会自动发现并注入这些 fixture.
"""

import pandas as pd
import pytest


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """标准正常数据：5 行，close + volume 两列。"""
    return pd.DataFrame(
        {
            "close": [10.5, 11.2, 12.8, 13.1, 14.0],
            "volume": [1000, 2000, 1500, 3000, 2500],
        }
    )


@pytest.fixture
def dirty_df() -> pd.DataFrame:
    """含脏数据：有 NaN close、有空行。"""
    return pd.DataFrame(
        {
            "close": [100, None, None, 102, 103],
            "volume": [1000, 500, None, 2000, 3000],
        }
    )


@pytest.fixture
def empty_df() -> pd.DataFrame:
    """空 DataFrame：只有列名，无数据。"""
    return pd.DataFrame({"close": [], "volume": []})


@pytest.fixture
def all_nan_df() -> pd.DataFrame:
    """全是 NaN 的 DataFrame。"""
    return pd.DataFrame({"close": [None, None, None]})


@pytest.fixture
def default_config() -> dict:
    """默认技术指标参数。"""
    return {
        "sma5": 5,
        "sma10": 10,
        "ema20": 20,
        "rsi7": 7,
        "rsi14": 14,
    }
