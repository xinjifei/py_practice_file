# 量化 + AI 自学仓库

> 从零开始的量化金融与人工智能自学代码备份，方便手机端复习 + 灾备。

---

## 目录结构

```
PY_practice_file/
│
├── 练习/
│   ├── A_核心语法与数据操控基础/      # Python 基础（变量、循环、函数、类、文件 I/O）
│   ├── B_量化数据处理与工程基座/      # 数据处理管线 + 工程栈（Git/uv/pytest/logging）
│   │   ├── 1技术指标生成/
│   │   ├── 2综合数据管道实战/
│   │   ├── 3工程基座/
│   │   └── 4数学与金融基础/
│   ├── 1_概率论与统计直觉/           # 概率分布、统计方法直觉训练
│   ├── 2_金融基础/                   # 收益率计算、K 线、金融概念
│   ├── 3_数据可视化强化/             # Matplotlib/Plotly 可视化练习
│   └── 4_SQLite基础数据处理整合/     # 数据库查询 + 完整数据管道综合
│
├── 练习用数据源/                     # 行情 CSV 数据（沪深 300 日线、个股日线）
├── 临时/                             # 临时文件
├── 使用/                             # 实用工具脚本
└── 备份/                             # 代码备份
```

---

## .git_local 说明

部分子目录下有 `.git_local` 文件夹（而非 `.git`），这是练习过程中创建的本地 Git 仓库。为兼容父仓库管理，重命名为 `.git_local` 保留历史记录。需要查看练习时的 commit 历史时：

```bash
cd 某目录
mv .git_local .git
git log --oneline
mv .git .git_local   # 用完改回去
```

---

## 本地代理配置

通过 SingBox（端口 1080）+ Git 按域名代理实现 GitHub 访问，详见 `D:\agent_work_file\cc_work_file\git_poxy\` 下的配置脚本。

当前 Git 代理配置（仅对 GitHub 生效）：

```
http.https://github.com.proxy = socks5://127.0.0.1:1080
http.https://api.github.com.proxy = socks5://127.0.0.1:1080
...
```

---

## 统计

- 练习 Python 文件：~200+
- 练习数据文件（CSV/JSON）：~340
- 覆盖阶段：Python 基础 → 量化数据处理 → 金融数学 → 可视化 → 数据库 → 工程基座
