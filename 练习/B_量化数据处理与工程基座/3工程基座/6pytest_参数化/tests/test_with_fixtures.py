"""
演示：用 conftest.py 里的 fixture 写测试
注意测试函数的参数名 —— 和 fixture 函数名一样
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 练习题.main import clean_df


# ============================================================
#   这些参数 sample_df, dirty_df, empty_df, all_nan_df
#   都不是你自己定义的，是 conftest.py 里的 fixture
#   pytest 看到参数名 → 找到同名 fixture → 调用它 → 把返回值注入
# ============================================================


def test_正常数据不需要清洗(sample_df):
    """sample_df 里没有 NaN，清洗后行数不应变"""
    result = clean_df(sample_df)
    assert result.shape[0] == 5

    # fixture: sample_df 是参数名
    # pytest 在 conftest.py 里找到了 @pytest.fixture 同名函数
    # 自动调用 sample_df()，把返回值传给这个参数


def test_脏数据被清洗(dirty_df):
    """dirty_df 里有 NaN 和空行，清洗后应该少行"""
    result = clean_df(dirty_df)

    # 原始 5 行，第2行 close=None 被删，第3行全空被删 → 剩 3 行
    assert result.shape[0] == 3
    assert result["close"].notna().all()


def test_空DataFrame不崩溃(empty_df):
    """空 DataFrame 洗完后还是空的，不应该报错"""
    result = clean_df(empty_df)
    assert result.shape[0] == 0
    assert list(result.columns) == ["close", "volume"]


def test_全NaN变成空DataFrame(all_nan_df):
    """全是 NaN，洗完后应该一行不剩"""
    result = clean_df(all_nan_df)
    assert result.shape[0] == 0
