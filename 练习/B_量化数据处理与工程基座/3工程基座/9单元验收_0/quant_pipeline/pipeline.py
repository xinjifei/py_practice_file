"""主流水线 + CLI 入口。

流水线流程：
    1. 从 input_dir 读取所有 CSV
    2. 逐个文件：读取 → 清洗 → 计算指标
    3. 合并所有成功的 DataFrame
    4. 保存 final_dataset.csv + 运行日志

CLI 用法:
    uv run pipeline <config.json>
"""

import argparse
import datetime
import json
import logging
import os
import sys
from glob import glob
from pathlib import Path
from typing import NamedTuple

import pandas as pd

from quant_pipeline.clean import clean_df
from quant_pipeline.indicators import calc_all_indicators

# ── 日志配置 ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


class PipelineResult(NamedTuple):
    """流水线运行结果。

    可以像普通 tuple 一样解包:
        df, fcount, total, ok, err, err_log = result
    """

    df: pd.DataFrame
    file_count: int
    total_processed: int
    success_count: int
    error_count: int
    error_log: str


def run_pipeline(
    input_dir: str,
    output_dir: str,
    config: dict,
) -> PipelineResult:
    """主流水线：读取 CSV → 清洗 → 计算指标 → 合并保存。

    Args:
        input_dir: 存放源 CSV 文件的目录
        output_dir: 输出目录（不存在会自动创建）
        config: 指标参数字典，包含 sma5, sma10, ema20, rsi7, rsi14

    Returns:
        PipelineResult: 包含合并后的 DataFrame 和运行统计
    """
    # 1. 发现所有 CSV 文件
    path_list = glob(os.path.join(input_dir, "*.csv"))
    file_count = len(path_list)

    # 2. 逐个处理
    all_df_list: list[pd.DataFrame] = []
    error_log_parts: list[str] = []
    success_count = 0
    error_count = 0

    for i, path in enumerate(path_list, start=1):
        try:
            df = pd.read_csv(path)
            df = clean_df(df)
            df = calc_all_indicators(df, config)
            all_df_list.append(df)
            success_count += 1
            logger.info("第 %d 个文件处理成功: %s", success_count, os.path.basename(path))

        except KeyboardInterrupt:
            # 用户主动中断 → 不要当成文件损坏，直接向上抛
            raise

        except Exception:
            error_count += 1
            logger.exception("第 %d 个文件处理失败: %s", error_count, os.path.basename(path))
            error_log_parts.append(
                f"#{i} 文件处理失败: {os.path.basename(path)}（失败计数={error_count}）"
            )

    # 3. 合并并保存
    final_df = pd.concat(all_df_list, ignore_index=True)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "final_dataset.csv")
    final_df.to_csv(output_path, index=False, encoding="utf-8")

    # 4. 写运行日志和错误日志
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    error_log_text = "\n".join(error_log_parts)

    log_path = os.path.join(output_dir, f"run_log_{timestamp}.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"文件数: {file_count}\n")
        f.write(f"成功: {success_count}\n")
        f.write(f"失败: {error_count}\n")
        f.write(f"输出行数: {len(final_df)}\n")

    if error_log_text:
        err_path = os.path.join(output_dir, f"error_log_{timestamp}.txt")
        with open(err_path, "w", encoding="utf-8") as f:
            f.write(f"因错误跳过的文件:\n{error_log_text}\n")

    return PipelineResult(
        df=final_df,
        file_count=file_count,
        total_processed=success_count + error_count,
        success_count=success_count,
        error_count=error_count,
        error_log=error_log_text,
    )


# ── CLI 入口 ──────────────────────────────────────────────


def main() -> None:
    """命令行入口：解析参数 → 运行流水线 → 输出摘要。

    Usage:
        uv run pipeline config.json
    """
    parser = argparse.ArgumentParser(
        description="量化数据流水线：读取 CSV → 清洗 → 计算技术指标 → 合并输出"
    )
    parser.add_argument(
        "config_path",
        help="配置文件路径（JSON 格式）",
    )
    args = parser.parse_args()

    # 读取配置
    config_path = Path(args.config_path)
    if not config_path.exists():
        logger.error("配置文件不存在: %s", config_path)
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    input_dir = config["input_dir"]
    output_dir = config["output_dir"]

    # 校验输入路径
    if not Path(input_dir).exists():
        logger.error("数据源路径不存在: %s", input_dir)
        sys.exit(1)

    # 计时
    start_time = datetime.datetime.now()
    start_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("流水线启动 — %s", start_str)

    # 执行
    result = run_pipeline(input_dir, output_dir, config)

    # 计时
    end_time = datetime.datetime.now()
    end_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
    duration = end_time - start_time

    # 输出摘要（日志文件已由 run_pipeline 写入）
    logger.info("流水线完成 — %s", end_str)
    logger.info("耗时: %s", duration)
    logger.info(
        "文件数: %d | 成功: %d | 失败: %d | 输出行数: %d",
        result.file_count,
        result.success_count,
        result.error_count,
        len(result.df),
    )


if __name__ == "__main__":
    main()
