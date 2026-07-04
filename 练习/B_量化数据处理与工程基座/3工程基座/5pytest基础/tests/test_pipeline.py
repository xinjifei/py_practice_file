"""
测试完整流水线：读取 → 清洗 → 计算指标 → 保存
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from 练习题.main import run_pipeline, clean_df, calc_all_indicators


config = {
    "sma5": 5, "sma10": 10, "ema20": 20,
    "rsi7": 7, "rsi14": 14
}

# 准备路径
DATA_DIR = str(Path(__file__).parent.parent / "练习题" / "test_data")
OUT_DIR  = str(Path(__file__).parent.parent / "tests" / "tmp_output") + "/"


def setup_function():
    """每个测试前自动执行：确保输出目录存在"""
    import os
    os.makedirs(OUT_DIR, exist_ok=True)


# ============ 测试1：读取 CSV 并清洗 ============
def test_读取单个CSV并清洗():
    """从 test_data 读取一个文件，验证 clean_df 能正常处理真实数据"""
    df = pd.read_csv(DATA_DIR + "/source_1.csv")

    result = clean_df(df)

    # 有数据
    assert len(result) > 0, "清洗后不应该为空"
    # 不能有 NaN
    assert result["close"].notna().all(), "close 列有 NaN"
    # 索引从 0 开始
    assert result.index[0] == 0


# ============ 测试2：完整流水线跑通 ============
def test_run_pipeline_完整流程():
    """读取 test_data 全部文件，跑完流水线，验证输出正确"""
    final_df, file_count, count_all, success_count, error_count, _ = run_pipeline(
        DATA_DIR, OUT_DIR, config
    )

    # 断言总数
    assert file_count == 4, f"应该有4个文件，实际{file_count}"
    assert count_all == 4, f"应该处理4个，实际{count_all}"
    assert success_count >= 1, "至少应该成功1个"
    # 最终合并的 DataFrame 应该包含所有成功的文件的数据
    assert len(final_df) > 0, "最终输出不应为空"

    # 最终输出的列必须包含原始列 + 指标列
    expected_cols = ["close", "SMA_5", "SMA_10", "EMA_20", "RSI_7", "RSI_14", "DIF", "DEA", "HIST"]
    for col in expected_cols:
        assert col in final_df.columns, f"输出缺列: {col}"


# ============ 测试3：保存的文件确实存在 ============
def test_run_pipeline_文件已保存():
    """流水线运行后，输出文件应该被创建"""
    import os

    run_pipeline(DATA_DIR, OUT_DIR, config)

    # final_dataset.csv 应该被创建
    csv_path = OUT_DIR + "final_dataset.csv"
    assert os.path.exists(csv_path), f"没找到输出文件: {csv_path}"

    # 文件大小应该 > 0
    assert os.path.getsize(csv_path) > 0, "输出文件是空的"
