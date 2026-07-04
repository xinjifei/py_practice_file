"""
conftest.py —— pytest 的"公共物资仓库"
pytest 会自动读取这个文件，所有测试都能直接用里面定义的 fixture
"""

import pytest
import pandas as pd


# ============================================================
#   Fixture 1: 一个"标准"的正常 DataFrame
#   用法: 测试函数参数里写 sample_df，pytest 自动帮你注入
# ============================================================

@pytest.fixture
def sample_df():
    """返回一个包含 close 和 volume 两列的正常数据"""
    return pd.DataFrame({
        "close": [10.5, 11.2, 12.8, 13.1, 14.0],
        "volume": [1000, 2000, 1500, 3000, 2500],
    })


# ============================================================
#   Fixture 2: 一个"带脏数据"的 DataFrame
#   (中间有 NaN，方便测试清洗逻辑)
# ============================================================

@pytest.fixture
def dirty_df():
    """返回一个需要清洗的数据：有NaN、有空行"""
    return pd.DataFrame({
        "close": [100, None, None, 102, 103],
        "volume": [1000, 500, None, 2000, 3000],
    })


# ============================================================
#   Fixture 3: 全空（边界情况）
# ============================================================

@pytest.fixture
def empty_df():
    """返回一个空 DataFrame，只有列名，没有数据"""
    return pd.DataFrame({"close": [], "volume": []})


# ============================================================
#   Fixture 4: 全是 NaN（边界情况）
# ============================================================

@pytest.fixture
def all_nan_df():
    """返回一个全是 NaN 的 DataFrame"""
    return pd.DataFrame({"close": [None, None, None]})
