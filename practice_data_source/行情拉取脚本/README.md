# stock-puller — A 股行情数据拉取工具

基于 [akshare](https://github.com/akfamily/akshare)，从网络拉取 A 股个股/指数历史行情，输出为 CSV 文件。

**适用场景**：量化分析、统计学习、回测、可视化等需要本地行情数据的场合。

## 环境准备

```bash
# Python >= 3.10
uv sync          # 安装依赖（akshare + matplotlib + pandas）
```

## 配置说明（config.json）

```json
{
  "output": { "base_dir": "输出根目录" },
  "defaults": {
    "start_date": "默认起始日期 YYYYMMDD",
    "adjust": "qfq(前复权) / hfq(后复权) / 空(不复权)"
  },
  "stocks": { "watchlist": ["关注的个股代码列表"] },
  "indices": { "watchlist": ["关注的指数代码列表"] }
}
```

- 改日期、复权方式、关注列表都只需改 config.json，不需要改代码

## 使用示例

```bash
# 拉取单只股票日线（日期/复权用 config 默认值）
uv run python main.py --type stock_daily --code 600519

# 拉取所有关注股票
uv run python main.py --type stock_daily --all

# 拉取指数日线
uv run python main.py --type index_daily --code 000300

# 指定日期范围（覆盖 config）
uv run python main.py --type stock_daily --code 600519 --start 20200101 --end 20250609

# 指定不复权
uv run python main.py --type stock_daily --code 002594 --adjust none
```

## 输出文件

```
练习用数据源/
├── stock_daily/      ← 个股日线，文件名 = 股票代码.csv
├── index_daily/      ← 指数日线，文件名 = 指数代码.csv
└── ...               ← 后续扩展
```

CSV 列（个股日线）：`date, open, high, low, close, volume, amount, amplitude, pct_change, turnover, 换手率`

CSV 编码为 **UTF-8 BOM**，Windows Excel 直接双击打开无乱码。

## 扩展指南

需要新增数据类型（如分钟线、财报数据）时：

1. 在 config.json 中新增配置段
2. 在 `main.py` 中添加对应的 `fetch_xxx()` 函数
3. 在 argparse 的 `--type` choices 中添加新选项
4. 在 `subdir_map` 中添加输出子目录映射
