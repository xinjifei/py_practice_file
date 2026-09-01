# 📊 quant-pipeline

**量化数据流水线** — 读取股票 CSV → 清洗 → 计算技术指标 → 合并输出。

## 🚀 快速开始

```bash
# 1. 克隆项目
git clone <repo-url>
cd quant-pipeline

# 2. 安装 uv（如果没有）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 3. 一键同步环境
uv sync

# 4. 运行流水线
uv run python -m quant_pipeline.pipeline config.example.json
```

## 📁 项目结构

```
quant-pipeline/
├── quant_pipeline/             # 源代码包
│   ├── clean.py               # 数据清洗
│   ├── indicators.py          # 技术指标计算
│   └── pipeline.py            # 主流水线 + CLI 入口
├── tests/                     # 测试
│   ├── conftest.py           # 公共 fixture
│   ├── data/                 # 测试用 CSV
│   ├── test_clean.py         # 清洗测试
│   ├── test_indicators.py    # 指标测试
│   └── test_pipeline.py      # 集成测试
├── docs/                      # 学习笔记 & 截图
├── config.example.json        # 配置文件模板
├── pyproject.toml             # 项目配置
└── README.md
```

## 🔧 开发命令

| 操作 | 命令 |
|------|------|
| 运行流水线 | `uv run python -m quant_pipeline.pipeline config.json` |
| 运行测试 | `uv run pytest` |
| 代码格式化 | `uv run ruff format .` |
| 代码检查 | `uv run ruff check . --select=ALL` |
| 查看依赖树 | `uv tree` |

## ⚙️ 配置文件格式

```json
{
    "input_dir": "./tests/data",
    "output_dir": "./output",
    "sma5": 5,
    "sma10": 10,
    "ema20": 20,
    "rsi7": 7,
    "rsi14": 14
}
```

## 🧪 技术指标说明

| 指标 | 列名 | 参数 |
|------|------|------|
| 简单移动平均 | `SMA_5`, `SMA_10` | 5日, 10日 |
| 指数移动平均 | `EMA_20` | 20日 |
| 相对强弱指标 | `RSI_7`, `RSI_14` | 7日, 14日 |
| MACD 差离值 | `DIF` | (12, 26, 9) |
| MACD 平滑差离值 | `DEA` | (12, 26, 9) |
| MACD 离差值 | `HIST` | (12, 26, 9) |

## ✅ 新电脑验证清单

```bash
git clone <repo-url>    # [ ] 能克隆
uv sync                 # [ ] 环境对齐无报错
uv run pytest           # [ ] 全部测试通过
uv run python -m quant_pipeline.pipeline config.example.json  # [ ] 流水线跑通
```
