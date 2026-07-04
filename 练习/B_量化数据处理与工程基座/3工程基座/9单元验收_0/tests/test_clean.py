"""测试 clean_df 函数。

覆盖：正常数据、NaN 处理、空数据、索引重置。
使用 @pytest.mark.parametrize 一次性覆盖多组数据。
"""

import pandas as pd
import pytest

from quant_pipeline.clean import clean_df

# ── 参数化：正常 / NaN / 全空 场景 ──────────────────────


@pytest.mark.parametrize(
    "close_data, expected_rows",
    [
        pytest.param([100, 101, 102, 103], 4, id="正常-无NaN"),
        pytest.param([100, None, 102], 2, id="中间有NaN"),
        pytest.param([], 0, id="完全空"),
        pytest.param([None, None, None], 0, id="全是NaN"),
    ],
)
def test_clean_df_行数(close_data, expected_rows):
    """各种数据场景下，清洗后行数符合预期。"""
    df = pd.DataFrame({"close": close_data})
    result = clean_df(df)
    assert result.shape[0] == expected_rows


# ── 参数化：索引始终从 0 开始 ─────────────────────────


@pytest.mark.parametrize(
    "close_data",
    [
        pytest.param([100, 101, 102], id="无删除-索引不变"),
        pytest.param([100, None, 102], id="删中间行"),
        pytest.param([None, None, 100, 101], id="删前两行"),
    ],
)
def test_clean_df_索引从零开始(close_data):
    """无论删了多少行，索引必须从 0 开始连续。"""
    df = pd.DataFrame({"close": close_data})
    result = clean_df(df)
    assert result.index[0] == 0
    assert list(result.index) == list(range(len(result)))


# ── 使用 fixture 的测试 ──────────────────────────────


def test_正常数据无需清洗(sample_df):
    """无 NaN 的数据，清洗后行数不变。"""
    result = clean_df(sample_df)
    assert result.shape[0] == 5


def test_脏数据被清洗(dirty_df):
    """有 NaN 和全空行，清洗后只剩有效行。"""
    result = clean_df(dirty_df)
    assert result.shape[0] == 3
    assert result["close"].notna().all()


def test_空数据不崩溃(empty_df):
    """空 DataFrame 清洗后仍为空，不报错。"""
    result = clean_df(empty_df)
    assert result.shape[0] == 0
    assert list(result.columns) == ["close", "volume"]


def test_全NaN变空(all_nan_df):
    """全 NaN 数据，洗完后一行不剩。"""
    result = clean_df(all_nan_df)
    assert result.shape[0] == 0


def test_close列无NaN():
    """清洗后 close 列不能有任何空值。"""
    df = pd.DataFrame(
        {
            "close": [100, None, 102, None, 104],
            "volume": [1000, 500, 2000, 800, 3000],
        }
    )
    result = clean_df(df)
    assert result["close"].notna().all()


def test_列名不变():
    """清洗不应改变列名。"""
    df = pd.DataFrame({"close": [100, 101], "volume": [1000, 2000]})
    result = clean_df(df)
    assert list(result.columns) == ["close", "volume"]
