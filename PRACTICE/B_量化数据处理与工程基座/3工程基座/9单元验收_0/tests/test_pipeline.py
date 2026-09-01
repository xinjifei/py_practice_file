"""测试完整流水线：读取 → 清洗 → 计算指标 → 保存。

集成测试，验证各模块能正确协作。
"""

import os
from pathlib import Path

import pandas as pd
import pytest

from quant_pipeline.pipeline import PipelineResult, run_pipeline

# ── 路径 ─────────────────────────────────────────────

DATA_DIR = str(Path(__file__).parent / "data")
OUT_DIR = str(Path(__file__).parent / "tmp_output")

CONFIG = {"sma5": 5, "sma10": 10, "ema20": 20, "rsi7": 7, "rsi14": 14}


@pytest.fixture(autouse=True)
def setup_output_dir():
    """每个测试前后：确保输出目录干净。"""
    import shutil

    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR, exist_ok=True)
    yield
    # 清理
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)


def test_读取单个CSV并清洗():
    """从 test_data 读取一个文件，验证 clean 能处理真实数据。"""
    from quant_pipeline.clean import clean_df

    df = pd.read_csv(os.path.join(DATA_DIR, "source_1.csv"))
    result = clean_df(df)

    assert len(result) > 0, "清洗后不应该为空"
    assert result["close"].notna().all(), "close 列有 NaN"
    assert result.index[0] == 0


def test_完整流水线跑通():
    """读取全部 test_data，跑完流水线，验证输出正确。"""
    result = run_pipeline(DATA_DIR, OUT_DIR, CONFIG)

    assert isinstance(result, PipelineResult)
    assert result.file_count == 4, f"应该有 4 个文件，实际 {result.file_count}"
    assert result.total_processed == 4
    assert result.success_count >= 1, "至少应该成功 1 个"
    assert len(result.df) > 0, "最终输出不应为空"

    expected_cols = [
        "close",
        "SMA_5",
        "SMA_10",
        "EMA_20",
        "RSI_7",
        "RSI_14",
        "DIF",
        "DEA",
        "HIST",
    ]
    for col in expected_cols:
        assert col in result.df.columns, f"输出缺列: {col}"


def test_输出文件已创建():
    """流水线运行后，final_dataset.csv 应该被创建且不为空。"""
    run_pipeline(DATA_DIR, OUT_DIR, CONFIG)

    csv_path = os.path.join(OUT_DIR, "final_dataset.csv")
    assert os.path.exists(csv_path), f"没找到输出文件: {csv_path}"
    assert os.path.getsize(csv_path) > 0, "输出文件是空的"


def test_运行日志已创建():
    """流水线运行后，应该生成运行日志文件。"""
    run_pipeline(DATA_DIR, OUT_DIR, CONFIG)

    log_files = [f for f in os.listdir(OUT_DIR) if f.startswith("run_log_")]
    assert len(log_files) >= 1, "运行日志未生成"


def test_损坏文件不崩流水线(tmp_path):
    """在数据目录中放一个损坏的 CSV，流水线不应崩溃。"""
    # 拷贝正常数据到临时目录
    import shutil

    tmp_data = tmp_path / "data"
    tmp_out = tmp_path / "output"
    os.makedirs(tmp_data, exist_ok=True)

    for src in Path(DATA_DIR).glob("*.csv"):
        shutil.copy(src, tmp_data / src.name)

    # 放入一个损坏文件
    bad_file = tmp_data / "bad.csv"
    bad_file.write_text("这不是一个合法的CSV\n乱码乱码乱码", encoding="utf-8")

    result = run_pipeline(str(tmp_data), str(tmp_out), CONFIG)

    # 不应该崩溃，且失败数 >= 1
    assert result.error_count >= 1
    # 成功文件仍然正常处理
    assert result.success_count >= 1
