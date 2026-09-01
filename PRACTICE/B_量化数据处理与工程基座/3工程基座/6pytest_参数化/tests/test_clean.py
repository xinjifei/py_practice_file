"""
对比演示：参数化 vs 普通写法
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import pytest
from 练习题.main import clean_df


# ============================================================
#   昨天的写法：5 个场景 = 5 个函数，每个函数几乎一模一样
#   缺点：重复代码多，加新场景就要复制粘贴
# ============================================================

def test_旧写法_删除全空行():
    df = pd.DataFrame({"close": [100, None, 102], "volume": [1000, None, 2000]})
    result = clean_df(df)
    assert result.shape[0] == 2

def test_旧写法_删除close为空():
    df = pd.DataFrame({"close": [100, None, 102], "volume": [1000, 500, 2000]})
    result = clean_df(df)
    assert result.shape[0] == 2

def test_旧写法_列名不变():
    df = pd.DataFrame({"close": [100, 101], "volume": [1000, 2000]})
    result = clean_df(df)
    assert list(result.columns) == ["close", "volume"]

def test_旧写法_无NaN():
    df = pd.DataFrame({"close": [100, 101, None, 102], "volume": [1000, 2000, 500, 3000]})
    result = clean_df(df)
    assert result["close"].notna().all()

def test_旧写法_索引重置():
    df = pd.DataFrame({"close": [100, None, 102], "volume": [1000, 500, 2000]})
    result = clean_df(df)
    assert list(result.index) == [0, 1]


# ============================================================
#   今天的写法：parametrize
#   一个函数，N 组数据，pytest 自动给你生成 N 个测试
#   ↓ 下面这行就是 parametrize 的语法
# ============================================================

#                          ↓参数名↓    ↓  第1组    ↓  第2组      ↓  第3组       第4组
@pytest.mark.parametrize("close_data, expected_rows, desc", [
    pytest.param([100, 101, 102, 103],  4, "正常数据，无NaN",    id="正常"),
    pytest.param([100, None, 102],      2, "中间有NaN被删",      id="有NaN"),
    pytest.param([],                    0, "全空输入",           id="全空"),
    pytest.param([None, None, None],    0, "全是NaN",            id="全NaN"),
])
def test_clean_df_param(close_data, expected_rows, desc):
    """
    这个函数会被 pytest 自动跑 4 次，
    每次用 parametrize 里的一组数据
    """
    df = pd.DataFrame({"close": close_data})
    result = clean_df(df)
    assert result.shape[0] == expected_rows, f"{desc}: 期望{expected_rows}行，实际{result.shape[0]}行"


# ============================================================
#   再加一组：验证索引总是从0开始
# ============================================================

@pytest.mark.parametrize("close_data", [
    [100, 101, 102],                # 没有删除，索引本就是 0,1,2
    [100, None, 102],               # 删了中间行，索引应该重置为 0,1
    [None, None, 100, 101],         # 删了前两行，索引应该重置为 0,1
])
def test_clean_df_索引总是从零开始(close_data):
    """不管你删了多少行，洗完之后索引必须从0开始连续"""
    df = pd.DataFrame({"close": close_data})
    result = clean_df(df)
    assert result.index[0] == 0
    # 索引里面不能有空隙: [0, 2] 不行，必须是 [0, 1]
    assert list(result.index) == list(range(len(result)))
