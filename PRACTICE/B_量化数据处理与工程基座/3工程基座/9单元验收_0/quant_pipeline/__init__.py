"""量化数据流水线核心模块。

用法:
    from quant_pipeline import clean_df, calc_all_indicators, run_pipeline
    python -m quant_pipeline.pipeline config.json  # CLI 入口
"""

from quant_pipeline.clean import clean_df
from quant_pipeline.indicators import calc_all_indicators
from quant_pipeline.pipeline import PipelineResult, run_pipeline

__all__ = [
    "PipelineResult",
    "calc_all_indicators",
    "clean_df",
    "run_pipeline",
]
