"""
行情数据拉取脚本 — stock-puller
================================
从 akshare 拉取 A 股个股/指数历史行情，输出为 CSV 文件。

用法示例：
    # 拉取单只股票日线（默认日期从 config.json 读取）
    python main.py --type stock_daily --code 600519

    # 拉取所有关注股票
    python main.py --type stock_daily --all

    # 拉取指数日线，指定日期范围
    python main.py --type index_daily --code 000300 --start 20230101 --end 20250609

    # 拉取个股，不复权
    python main.py --type stock_daily --code 002594 --adjust none
"""

import argparse
import json
import sys
import time
from pathlib import Path

import akshare as ak
import pandas as pd


# ---- 配置文件加载 ----

def load_config(config_path: str | Path = "config.json") -> dict:
    """读取 config.json，返回配置字典。

    配置文件路径相对于脚本所在目录，也接受绝对路径。
    """
    config_file = Path(config_path)
    if not config_file.is_absolute():
        config_file = Path(__file__).resolve().parent / config_file
    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_file}")
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)


# ---- 路径工具 ----

def ensure_output_dir(base_dir: str, subdir: str) -> Path:
    """确保输出子目录存在并返回 Path 对象。"""
    out = Path(base_dir) / subdir
    out.mkdir(parents=True, exist_ok=True)
    return out


# ---- 数据拉取（含重试） ----

def _to_sina_symbol(code: str) -> str:
    """将纯数字代码转换为新浪格式: 600519 → sh600519, 000858 → sz000858"""
    code = code.strip()
    if code.startswith(("sh", "sz")):
        return code
    if code.startswith(("6", "5", "9")):
        return f"sh{code}"
    else:
        return f"sz{code}"


def _retry_fetch(fn, max_retries: int = 3, label: str = ""):
    """带指数退避的重试包装器。"""
    for attempt in range(1, max_retries + 1):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries:
                print(f"  [错误] {label} 拉取失败（已重试{max_retries}次）: {e}")
                raise
            wait = 2 ** (attempt - 1)
            print(f"  [重试 {attempt}/{max_retries}] {label}: {e}，{wait}秒后重试...")
            time.sleep(wait)


def fetch_stock_daily(code: str, start_date: str, end_date: str, adjust: str) -> pd.DataFrame | None:
    """拉取单只 A 股个股日线数据（新浪源，stock_zh_a_daily）。

    参数
    ----
    code     : 股票代码，如 "600519"
    start_date : 起始日期 YYYYMMDD，空字符串表示不限
    end_date   : 截止日期 YYYYMMDD，空字符串表示到最新
    adjust     : 复权方式 "qfq"(前复权) / "hfq"(后复权) / ""(不复权)

    返回
    ----
    DataFrame，列包含 date/open/high/low/close/volume/amount/turnover
    失败返回 None
    """
    sina_symbol = _to_sina_symbol(code)
    actual_end = end_date if end_date else "20500101"

    def _call():
        return ak.stock_zh_a_daily(
            symbol=sina_symbol,
            start_date=start_date if start_date else "19900101",
            end_date=actual_end,
            adjust=adjust if adjust else "",
        )

    label = f"个股日线 {code}"
    print(f"  拉取 {label} ({start_date or '不限'} ~ {end_date or '最新'}, {adjust or '不复权'})")
    df = _retry_fetch(_call, label=label)

    if df is None or df.empty:
        print(f"  [提示] {code} 返回空数据")
        return None

    print(f"  {code} 获取 {len(df)} 条记录")
    return df


def fetch_index_daily(code: str, start_date: str, end_date: str) -> pd.DataFrame | None:
    """拉取单只指数日线数据。

    参数
    ----
    code       : 指数代码，如 "000300"（沪深300）
    start_date : 起始日期 YYYYMMDD
    end_date   : 截止日期 YYYYMMDD，空字符串表示到最新

    返回
    ----
    DataFrame，失败返回 None
    """
    actual_end = end_date if end_date else "20500101"

    def _call():
        return ak.stock_zh_index_daily(symbol=f"sh{code}")

    label = f"指数日线 {code}"
    print(f"  拉取 {label} ({start_date} ~ {end_date or '最新'})")

    # akshare 指数接口通常返回全部历史，需要手动截断日期
    df = _retry_fetch(_call, label=label)
    if df is None or df.empty:
        print(f"  [提示] {code} 返回空数据")
        return None

    # 统一列名：akshare 指数返回的日期列可能是 "date"
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(actual_end)
        df = df[(df["date"] >= start_dt) & (df["date"] <= end_dt)]

    print(f"  {code} 获取 {len(df)} 条记录")
    return df


# ---- 保存 ----

def save_data(df: pd.DataFrame, output_dir: Path, code: str) -> Path:
    """保存 DataFrame 为 CSV（UTF-8 BOM，Windows Excel 友好）。

    返回保存的文件路径。
    """
    filepath = output_dir / f"{code}.csv"
    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    print(f"  → 已保存: {filepath}")
    return filepath


# ---- 命令行入口 ----

def main() -> None:
    parser = argparse.ArgumentParser(
        description="A 股行情数据拉取工具 — 从 akshare 获取并保存为 CSV"
    )
    parser.add_argument(
        "--type", "-t",
        choices=["stock_daily", "index_daily"],
        default="stock_daily",
        help="数据类型 (默认: stock_daily)",
    )
    parser.add_argument(
        "--code", "-c",
        default="",
        help="股票/指数代码（与 --all 二选一）",
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="拉取 config.json watchlist 中所有标的",
    )
    parser.add_argument(
        "--start",
        default="",
        help="起始日期 YYYYMMDD（覆盖 config 默认值）",
    )
    parser.add_argument(
        "--end",
        default="",
        help="截止日期 YYYYMMDD（默认到最新）",
    )
    parser.add_argument(
        "--adjust",
        default="",
        help="复权方式: qfq / hfq / 空=不复权（仅 stock_daily 有效，覆盖 config）",
    )
    parser.add_argument(
        "--config",
        default="config.json",
        help="配置文件路径 (默认: config.json)",
    )

    args = parser.parse_args()

    # 校验：--code 和 --all 至少指定一个
    if not args.code and not args.all:
        parser.error("必须指定 --code 或 --all 之一")

    # 加载配置
    try:
        config = load_config(args.config)
    except FileNotFoundError as e:
        print(f"[致命错误] {e}")
        sys.exit(1)

    # 合并默认值：CLI 参数 > config.defaults
    default_start = args.start or config.get("defaults", {}).get("start_date", "20240101")
    default_adjust = args.adjust or config.get("defaults", {}).get("adjust", "qfq")
    output_base = config.get("output", {}).get("base_dir", "D:/PY_practice_file/练习用数据源")

    print(f"输出根目录: {output_base}")
    print(f"默认起始日期: {default_start}")
    if args.type == "stock_daily":
        print(f"复权方式: {default_adjust}")

    # 确定标的列表
    if args.all:
        key = "stocks" if args.type == "stock_daily" else "indices"
        codes = config.get(key, {}).get("watchlist", [])
        if not codes:
            print(f"[提示] config.json 中 {key}.watchlist 为空，没有需要拉取的标的")
            sys.exit(0)
        print(f"批量拉取 {len(codes)} 个标的: {codes}")
    else:
        codes = [args.code]

    # 确定输出子目录
    subdir_map = {
        "stock_daily": "stock_daily",
        "index_daily": "index_daily",
    }
    subdir = subdir_map[args.type]
    output_dir = ensure_output_dir(output_base, subdir)

    # 统计
    success_count = 0
    fail_codes: list[str] = []

    for code in codes:
        print(f"\n[{code}]")
        try:
            if args.type == "stock_daily":
                df = fetch_stock_daily(code, default_start, args.end, default_adjust)
            else:
                df = fetch_index_daily(code, default_start, args.end)

            if df is not None and not df.empty:
                save_data(df, output_dir, code)
                success_count += 1
            else:
                fail_codes.append(code)
        except Exception:
            fail_codes.append(code)

    # 汇总
    print(f"\n{'='*50}")
    print(f"完成: 成功 {success_count}/{len(codes)}")
    if fail_codes:
        print(f"失败/空数据: {fail_codes}")


if __name__ == "__main__":
    main()
