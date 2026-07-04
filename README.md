# 量化 + AI 自学项目

> 从零开始的量化金融与人工智能自学计划——用 137 个主日 + 61 个数学日完成从 Python 小白到 AI 量化系统构建者的转型。

---

## 人类阅读
> 以下的规则并非一成不变，会有迭代，数字序号代表版本
### 文件命名法
1. 
    - 每日学习根目录命名；`d<学习天数>_<学习内容概述>`
    - note.md文件命名：`d<学习天数>_note.md`
### git masage
1. 
    - 

---

## 目录

1. [项目概览](#项目概览)
2. [快速开始](#快速开始)
3. [目录结构](#目录结构)
4. [学习哲学：双轨并行](#学习哲学双轨并行)
5. [轨道总览](#轨道总览)
6. [每日工作流](#每日工作流)
7. [维护指南](#维护指南)
8. [验证管线](#验证管线)
9. [关键文件速查表](#关键文件速查表)
10. [项目溯源](#项目溯源)

---

## 项目概览

### 这是什么

一个**自顶向下、实战驱动**的量化金融 + AI 个人学习项目。学习内容分为两条独立轨道：

| 轨道 | 时长 | 定位 |
|------|------|------|
| **主轨道 (Main Track)** | 约 3 小时/天，共 ~137 天 | 实战驱动——用到什么学什么 |
| **数学轨道 (Math Track)** | 约 25 分钟/天，共 61 天 | 学科驱动——从地基一层层往上建 |

两条轨道加起来约 5 个月（含缓冲日），全部学习内容**存储为纯文本文件**，由 `plan/index.html` 单页应用集中管理进度。

### 为什么这么做

- AI 时代写代码的成本趋近于零，但**判断力、设计能力、领域理解**变得稀缺
- 同一个概念学 **两次**：第一次在 Main 当黑盒工具用，第二次在 Math 拆开理解原理 —— 间隔重复强化记忆
- 两条轨道互相独立：Main 不等待 Math，Math 不追赶 Main 节奏

### 7 个阶段循序渐进

| 阶段 | 天数 | 内容 |
|------|------|------|
| 一 | 12 | Python 核心概念速览（AI 辅助，不背语法） |
| 二 | 33 | 量化数据处理 + 工程基座 + 金融数学基础 |
| 三 | 8 | AI 时代的产品思维（痛点发现 + MVP） |
| 四 | 22 | AI 核心技术：LLM / RAG / Prompt Engineering / 本地部署 |
| 五 | 20 | 量化回测与策略开发 |
| 六 | 18 | 服务部署与自动化（FastAPI + Docker） |
| 七 | 20 | Agent 架构与智能应用（LangGraph + 风控） |

---

## 快速开始

### 1. 打开计划追踪器

用浏览器直接打开：

```
plan/index.html
```

这是一个纯前端 SPA（无构建工具、无后端），使用 localStorage 保存进度，Hash 路由导航。

- 点击 **"主计划"** 标签查看 Main 轨道的 137 天进度
- 点击 **"数学"** 标签查看 Math 轨道的 61 天进度
- GitHub 风格热力图：\#0e4429 → \#39d353 表示完成度
- 连续学习天数（Streak）自动统计

### 2. 读取每日内容

点击某一天 → 查看当天的 **learning prompt**（可直接复制给 AI 助手），包含：

- 学习目的
- 核心概念
- 练习任务
- 所需工具
- 学习标准和难度评估

### 3. 开始练习

练习代码存放在 `练习/` 目录下，按阶段分类：

```bash
cd 练习/
ls  # 查看各阶段子目录
```

---

## 目录结构

```
D:\PY_practice_file\
│
├── plan/                         # 学习计划核心目录
│   ├── index.html                # 计划追踪器 SPA（浏览器打开）
│   ├── app.js                    # 所有学习数据（MAIN_PLAN + MATH_TRACK）
│   ├── style.css                 # GitHub Dark 风格样式
│   ├── mine_outline.py           # ★ Main 轨道源文件（137 天，7 阶段）
│   ├── math_outline.py           # ★ Math 轨道源文件（61 天，5 模块）
│   │
│   ├── scripts/                  # 构建与验证脚本
│   │   ├── sync_math_to_appjs.py # math_outline.py → app.js MATH_TRACK
│   │   ├── update_appjs.py       # mine_outline.py → app.js MAIN_PLAN
│   │   ├── audit_math.py         # Math 轨道完整性审计
│   │   ├── sync_concept_map.py   # 概念映射表同步
│   │   └── verify_concept_map.py # 概念映射表防幻觉验证
│   │
│   ├── data/                     # 结构化数据（概念映射等）
│   │   ├── concept_map.py        # 概念映射表（防幻觉数据源）
│   │   └── concept_map_data.js   # 编译后的概念映射数据
│   │
│   ├── docs/                     # 核心文档
│   │   ├── 双轨哲学.md           # ★ 双轨学习哲学（必读）
│   │   └── math_rewrite_principles.md  # Math 轨道重写原则
│   │
│   ├── 学习对齐研究/             # 认知科学与对齐研究
│   │   ├── analysis.md
│   │   ├── implementation_plan.md
│   │   ├── 认知科学审计.md
│   │   └── validate_sync.py      # ★ 双轨对齐验证脚本
│   │
│   └── archive/                  # 历史方案存档
│       ├── style_demo/           # UI 重设计方案（3 种风格）
│       └── 统一轨道方案/          # 早期统一轨道方案
│
├── 练习/                         # 日常练习代码
│   ├── A_核心语法与数据操控基础/  # 阶段一练习（包含 befor/befor2/3/4 子目录）
│   ├── B_量化数据处理与工程基座/  # 阶段二练习
│   └── 1_概率论与统计直觉/       # 金融数学基础练习
│
├── 练习用数据源/                 # 练习用行情数据
│
├── 临时/                         # 临时文件（不入库）
├── 使用/                         # 实用工具脚本
├── 备份/                         # 代码备份
│
├── .claude/                      # Claude Code 配置与记忆
├── .venv/                        # Python 虚拟环境
├── .vscode/                      # VSCode 配置
├── .gitattributes                # Git 属性配置
└── README.md                     # ← 你在这里
```

---

## 学习哲学：双轨并行

核心哲学记录在 `plan/docs/双轨哲学.md`，这里提炼要点。

### 两条轨道各司其职

```text
Main 轨道（3h/天）            Math 轨道（25min/天）
    │                              │
    ▼                              ▼
项目 → 工具 → 理解         概念 → 直觉 → 代码验证
    │                              │
    ▼                              ▼
"怎么用"                     "为什么管用"
```

### 核心理念

1. **两条轨道互相独立**：Main 不需要先学 Math 同主题才能推进。Main 教"怎么用工具"，Math 教"工具背后的数学为什么管用"。

2. **syncMain 是信息标签，不是调度命令**：`【同步：Main Day X】` 标注该数学概念在 Main 轨道第 X 天**第一次用到**，但不要求你在该天之前学完 Math。

3. **Math 轨道保持学科递进**：数学按照认知顺序编排（函数 → 随机 → 分布 → 推断 → 矩阵 → 量化工具 → 进阶概念），不为了匹配 Main 节奏而打乱。

4. **一个概念，两次学习**：
   - 第一次（Main）：黑盒工具，能用的程度
   - 第二次（Math）：白盒原理，理解的程度
   - 先会用，再理解——间隔一周左右接触两次，记忆远超一次性学习

### Math 轨道的三级分类

| 级别 | 任务数 | 含义 | 占比 |
|------|--------|------|------|
| **核心日 ★★★** | 3 个练习 | 完整 7 字段 prompt | ~45% |
| **精炼日 ★★** | 2 个练习 | 精简 7 字段 prompt | ~30% |
| **概念速览 ★** | 1 个练习 | 缩减 prompt，仅核心直觉 | ~15% |
| **缓冲/复习日** | 0 | 回顾不做新课 | ~10% |

---

## 轨道总览

### Main 轨道 (137 天)

| 阶段 | 天数 | 核心产出 |
|------|:----:|----------|
| 一：Python 核心概念速览 | 12 | 能理解 AI 生成代码、能验证输出对错 |
| 二-1：量化数据处理与工程基座 | 21 | 完整数据管道 + uv/Git/pytest 工程栈 |
| 二-2：金融与数学基础 | 12 | 概率统计工具化理解 + SQL/可视化 |
| 三：AI 时代的产品思维 | 8 | 个人想法→MVP 工作流文档 |
| 四：AI 核心技术 | 22 | 本地 AI 投研助手 MVP |
| 五：量化回测与策略开发 | 20 | 完整策略研究报告 + 回测引擎 |
| 六：服务部署与自动化 | 18 | 一键 docker-compose up 启动系统 |
| 七：Agent 架构与智能应用 | 20 | AI 量化交易 Agent + 风控闭环 |

核心理念转变：**不记语法，让 AI 写代码；你学的是判断力、设计能力和领域理解。**

### Math 轨道 (61 天)

| 模块 | 天数 | 对应 Main 阶段 |
|------|:----:|----------------|
| 一：数学思维基础（函数→随机→分布） | 12 | 阶段一/二 |
| 二：统计推断（样本→大数定律→CLT→假设检验） | 14 | 阶段二/五 |
| 三：线性代数基础（向量→矩阵→Attention） | 16 | 阶段四 |
| 四：计算思维数学（收益率→组合→Big O→图网络） | 13 | 阶段五 |
| 五：进阶数学（信息论→优化→数值方法） | 9 | 阶段六/七 |

---

## 每日工作流

一个典型的学习日流程：

### Main 轨道

1. **打开 plan/index.html** → 查看今天的 globalDay
2. **阅读当天 prompt** → 复制给 AI 助手（Claude / ChatGPT）
3. **按 prompt 完成练习** → AI 生成代码 → 你审查逻辑 → 运行验证结果
4. **在计划追踪器上标记完成** → 点击当天格子标记为 Done
5. **最后 5 分钟**：系统思考——"今天学的概念和整体架构怎么连接？"

### Math 轨道

1. **切换到数学标签** → 找到对应 mathDay
2. **阅读 7 字段 prompt** → 复制给 AI
3. **25 分钟限时学习** → 按练习任务操作
4. **标记完成**

### 概念回想

打开某天的详情页，可以看到：

- **快速回顾**：回顾前一天的核心概念（来自 `concept_map.py`）
- **Sync Badge**：点击跳转到 Main/Math 关联天
- **Recall Badge**：Math 轨道的回想提示

---

## 维护指南

### 数据源结构

学习计划的数据不直接存在 app.js 中手动编辑，而是通过**源文件 + 构建脚本**管理：

```
mine_outline.py  ───→  update_appjs.py  ───→  app.js (MAIN_PLAN)
math_outline.py  ───→  sync_math_to_appjs.py  ───→  app.js (MATH_TRACK)
concept_map.py   ───→  sync_concept_map.py  ───→  concept_map_data.js
```

### 修改 Main 轨道

1. 编辑 `plan/mine_outline.py`（Python 三引号字符串格式，按阶段、section 组织）
2. 运行构建脚本（如有）：`python plan/scripts/update_appjs.py`
3. 注：当前 Mine Outline 直接同步到 app.js 需要脚本支持，日常修改可能直接编辑 app.js 更方便

### 修改 Math 轨道

1. 编辑 `plan/math_outline.py`（Python 三引号字符串格式，按模块、天组织）
2. 运行同步脚本：
   ```bash
   cd plan/
   python scripts/sync_math_to_appjs.py
   ```
3. 该脚本会自动解析 math_outline.py 中的 day headers，提取 prompt / 任务 / 描述，重新生成 app.js 中的 MATH_TRACK 对象

### 修改概念映射（快速回顾 / 回想提示）

1. 编辑 `plan/data/concept_map.py`
2. 运行验证脚本：`python scripts/verify_concept_map.py`
3. 运行同步脚本：`python scripts/sync_concept_map.py`

### app.js 的手动编辑

直接编辑 app.js 是可行的，但需要注意：

- MAIN_PLAN 和 MATH_TRACK 是两个独立的 JS 对象
- 每个 dayData 的 `globalDay` 必须连续且唯一
- `syncMain` 字段在 MATH_TRACK 中标注本日与 Main 轨道的关联
- `totalDays` 是 `modules.reduce(...)` 动态计算的，不需手动维护

---

## 验证管线

项目包含多层自动化验证，防止数据不一致：

### 1. 双轨对齐验证

```bash
python plan/学习对齐研究/validate_sync.py
```

检查 `DEPENDENCIES` 表中每一对 `(main_day, required_math_day)` 是否满足 `syncMain[math_day] <= main_day`。

退出码：0 = 通过，1 = 有硬约束违反。

### 2. Math 轨道完整性审计

```bash
python plan/scripts/audit_math.py
```

检查 math_outline.py 中每一天：
- 分类（核心/精炼/速览/缓冲）是否正确
- 练习任务数量匹配分类要求
- 7 字段是否完整（学习目的/核心概念/练习任务等）
- 学习时长是否统一为 25 分钟
- syncMain 映射是否与预期一致

### 3. 概念映射防幻觉验证

```bash
python plan/scripts/verify_concept_map.py
```

验证 `concept_map.py` 中的每一项：
- MAIN_CONCEPTS 的 main_day 在 mine_outline.py 中真实存在
- MATH_RECALL 的 main_day_used 与 sync_math_to_appjs.py 的 SYNC_MAIN_MAP 一致
- 概念关键词在源文件的 prompt 中出现
- contrast_with 交叉引用的 main_day 在 MAIN_CONCEPTS 中存在

退出码：0 = 通过，1 = 有错误。

### 4. 完整验证流程（修改后推荐运行）

```bash
# 修改同步映射后
python plan/scripts/sync_math_to_appjs.py
python plan/学习对齐研究/validate_sync.py

# 修改概念映射后
python plan/scripts/verify_concept_map.py

# 修改 Math 轨道内容后
python plan/scripts/audit_math.py
```

---

## 迭代原则

这个项目会持续演化。以下是保持项目健康的核心规则：

1. **源文件是真理。** `mine_outline.py` / `math_outline.py` / `concept_map.py` 是唯一手动编辑的数据源。`app.js` / `concept_map_data.js` 由脚本生成，不要手动改。
2. **改完就跑验证。** 至少跑 `node -c app.js`。涉及 syncMain 就跑 `validate_sync.py`。涉及概念映射就跑 `verify_concept_map.py`。
3. **Git 先 commit。** plan 文件夹有 `.git`。大改前先存盘，失败可回退。
4. **验证规则必须是机械检查。** 新增的任何自动化验证必须基于数字/字符串比对，不接受 AI 推断——这是之前 syncMain 错位 85 天的教训。
5. **扩展点：** 新增天数 → `mine_outline.py` / `math_outline.py`。新增回顾/回想 → `concept_map.py`。改 UI → `style.css`。改 DOM 结构 → `index.html` + `app.js` renderDay()。

已知故障模式（syncMain 错位、编码问题、JS 残留括号）的详细诊断见 `学习对齐研究/analysis.md`。

---

## 关键文件速查表

| 文件 | 作用 | 修改频率 |
|------|------|----------|
| `plan/mine_outline.py` | Main 轨道 137 天内容数据源（Python 字符串格式） | 低（大纲级修改） |
| `plan/math_outline.py` | Math 轨道 61 天内容数据源（Python 字符串格式） | 中（每天新内容） |
| `plan/app.js` | 计划追踪器 SPA 的数据层 + 应用逻辑（~350KB） | 高（每日标记进度） |
| `plan/index.html` | 计划追踪器 SPA 入口 | 低 |
| `plan/style.css` | GitHub Dark 风格样式 | 低 |
| `plan/data/concept_map.py` | 快速回顾 + 回想提示的数据源 | 中 |
| `plan/scripts/sync_math_to_appjs.py` | Math 数据源 → app.js 构建脚本 | 低 |
| `plan/scripts/update_appjs.py` | Main 数据源 → app.js 构建脚本 | 低 |
| `plan/scripts/audit_math.py` | Math 轨道完整性审计 | 低 |
| `plan/scripts/verify_concept_map.py` | 概念映射防幻觉验证 | 低 |
| `plan/学习对齐研究/validate_sync.py` | 双轨依赖约束验证 | 低 |
| `plan/docs/双轨哲学.md` | 核心学习哲学文档（必读） | 低 |
| `plan/docs/math_rewrite_principles.md` | Math 轨道重写规范 | 极低 |

---

## 项目溯源

- **起始时间**：2026 年初，从零开始学 Python
- **初始内容**：`练习/A_核心语法与数据操控基础/` 下的基础 Python 练习（变量、循环、函数等）
- **重大重构**：2026-06-01 重新定位为"AI 时代创造者"，阶段一从 22 天压缩到 12 天，新增"产品思维"阶段
- **当前状态**：Main 轨道 Day 47-48 附近（相关性 + 假设检验），Math 轨道同步推进中
- **双轨确立**：2026-06-16，基于 Day 47-48 实际学习体验提炼出双轨哲学

### 代码统计

```
练习 Python 文件: ~23,000+
练习数据文件 (CSV/JSON): ~340
计划追踪器: 3 文件 (HTML + CSS + JS, 无依赖)
验证脚本: 5 个 Python 文件
核心文档: 3 篇
```

---

> **核心信念**：AI 让你有能力实现任何想法，但"判断什么值得实现"是你永远不可替代的能力。
>
> 先会用，再理解。每一天的学习都比昨天多一个判断力的锚点。
