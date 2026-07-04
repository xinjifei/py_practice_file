"""
测试 clean_df 函数
"""

import sys
from pathlib import Path

# 把项目根目录加到搜索路径，这样能 import 练习题里的代码
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from 练习题.main import clean_df


# ============ 测试1：删除全空行 ============
def test_clean_df_删除全空行():
    """制造一个包含全空行的 DataFrame，验证空行被删掉"""
    df = pd.DataFrame({
        "close": [100, 101, 102],
        "volume": [1000, None, 2000],      # 故意让中间一行全是 None
    })
    # 把第二行变成全空
    df.loc[1] = [None, None]

    result = clean_df(df)

    # 全空行被删了，应该只剩 2 行
    assert result.shape[0] == 2, f"期望2行，实际{result.shape[0]}行"


# ============ 测试2：删除 close 为空的行 ============
def test_clean_df_删除close为空的行():
    """close 列有 NaN 的行应该被删掉"""
    df = pd.DataFrame({
        "close": [100, None, 102],   # 第二行 close 为空
        "volume": [1000, 500, 2000],
    })

    result = clean_df(df)

    # close 为空的被删了，剩 2 行
    assert result.shape[0] == 2


# ============ 测试3：验证列名不变 ============
def test_clean_df_列名不变():
    """清洗不应该改变列名"""
    df = pd.DataFrame({
        "close": [100, 101],
        "volume": [1000, 2000],
    })

    result = clean_df(df)

    # 列名应该完全相同
    assert list(result.columns) == ["close", "volume"]


# ============ 测试4：验证没有 NaN ============
def test_clean_df_无NaN():
    """清洗后的 DataFrame close 列不应该有任何 NaN"""
    df = pd.DataFrame({
        "close": [100, 101, None, 102],
        "volume": [1000, 2000, 500, 3000],
    })

    result = clean_df(df)

    # close 列不能有 NaN
    assert result["close"].notna().all(), "close 列还有空值！"


# ============ 测试5：验证索引被重置 ============
def test_clean_df_索引重置():
    """删除行后索引应该从 0 开始连续"""
    df = pd.DataFrame({
        "close": [100, None, 102],
        "volume": [1000, 500, 2000],
    })

    result = clean_df(df)

    # 索引应该是 [0, 1]，而不是 [0, 2]
    assert list(result.index) == [0, 1]

