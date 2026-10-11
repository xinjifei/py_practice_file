# demo_strategy_fewshot.py —— 参考脚手架：Few-shot 生成策略 + 前视偏差长什么样
#
# ⚠️ 两部分演示都用的是「演示数据」：
#    第一部分给的例子策略是布林带 / RSI（你练习要用**均线交叉**）
#    第二部分用的是**合成随机行情**（你练习要用真实数据：akshare 拉一段，或自己造）
#    看思路，数据自己换。
#
# 运行前先设 key（终端里临时设，别写进代码）：
#   Windows:    $env:DEEPSEEK_API_KEY = 'sk-xxx'
#   Mac/Linux:  export DEEPSEEK_API_KEY='sk-xxx'
#
# 运行方式：
#   uv run --with openai python demo_strategy_fewshot.py

import os
import numpy as np
import pandas as pd
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def ask(prompt):
    """发一段 prompt，返回回复正文。（和 d70/d71 完全一样，可以直接复用）

    参数 prompt：完整的一段话
    """
    resp = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,      # 固定 0：今天要看清 AI 的"套路模仿"，不要随机性干扰
    )
    return resp.choices[0].message.content


# ============================================================
# 第一部分：Few-shot 示范的是「结构」，不是「格式」
# ============================================================

# 1. 两个例子。★ 关键不在内容（布林带、RSI 是什么），在**它们长得一样**：
#    每个例子都是同一副骨架 —— 信号 → 过滤 → 仓位 → 出场。
#    这就是今天和 d70 的区别：d70 示范 JSON 字段长什么样（格式），
#    今天示范「一类策略该怎么描述」（结构）。
#    如果两个例子结构不一致（一个写四段、一个只写一句话），
#    AI 模仿到的就是噪声，不是套路。
EXAMPLE_1 = """策略名：布林带下轨反弹
- 信号：收盘价跌破布林带下轨（20日均线 - 2倍标准差）
- 过滤：只在 20日均线仍向上时做多（趋势向上才抄底）
- 仓位：固定 100% 仓位买入
- 出场：收盘价回到中轨（20日均线）之上，或持有超过 10 个交易日"""

EXAMPLE_2 = """策略名：RSI 超卖反转
- 信号：14日 RSI 跌破 30
- 过滤：当日成交量大于 20日均量的 1.2 倍（要有恐慌抛售）
- 仓位：固定 100% 仓位买入
- 出场：RSI 回到 50 以上，或持有超过 10 个交易日"""

# 2. 让 AI 照着这副骨架生成新的。（prompt 还是三段：指令 + 例子 + 要求）
#    注意最后那条"必须能写成可执行规则"——这就是审查的第二把半尺子，
#    先说死要求，再看它到底做没做到。
prompt = f"""你是一个量化策略研究员。请模仿下面两个策略的描述结构，生成 3 个新的交易策略思路。

例子1：
{EXAMPLE_1}

例子2：
{EXAMPLE_2}

要求：
1. 每个策略必须包含同样的四段：信号 / 过滤 / 仓位 / 出场
2. 3 个策略要用**不同的**指标组合或逻辑，不要重复上面的布林带和 RSI
3. 描述必须具体到能直接写成 Python 代码——不许出现「择机」「适当时候」这类含糊说法
4. 不许使用未来数据（不许用明天、后天或整段数据的统计量来做今天的决策）

直接输出 3 个策略，不要解释。"""

print("=" * 60)
print("【第一部分】Few-shot 生成策略")
print("=" * 60)
strategies = ask(prompt)
print(strategies)

print()
print("← 拿到这 3 个策略后，先别急着挑。逐条过三把尺子：")
print("   ① 逻辑自洽：它说得出为什么能赚钱吗？还是只是「历史上有效」？")
print("   ② 前视偏差：哪一条偷偷用了未来的信息？（下面第二部分告诉你它长什么样）")
print("   ③ 可执行：每一条规则都能写成 if 语句吗？有没有藏含糊词？")


# ============================================================
# 第二部分：前视偏差 —— 偷看未来能把烂策略变成神仙策略
# ============================================================

# 3. 造一段合成行情：60 天的随机游走。
#    ★ 为什么用随机数据？因为随机数据里**根本不存在**能赚钱的规律——
#    如果这上面还能跑出漂亮收益，那收益一定来自作弊，不来自策略。
np.random.seed(42)                      # 固定随机种子：保证你每次跑出来一样，方便对比
n_days = 60                             # 天数
daily_ret = np.random.normal(0, 0.02, n_days)   # normal(均值, 标准差, 个数)：每天涨跌幅，均值 0
price = 100 * np.exp(np.cumsum(daily_ret))      # cumsum 累加 → 价格 = 100 元起步的复利路径

df = pd.DataFrame({"close": price})
# pct_change()：算每一天相对前一天的涨跌幅，和 daily_ret 是一回事
df["ret"] = df["close"].pct_change()

# 4. 【作弊版】信号 = 今天收盘价站上 5 日均线就满仓。
df["ma5"] = df["close"].rolling(5).mean()                     # rolling(5)：取最近 5 天；.mean()：求这 5 天均值
df["signal_cheat"] = (df["close"] > df["ma5"]).astype(int)    # astype(int)：True/False → 1/0

# 5. 【老实版】同一个信号，只多一步：delay 一天。
#    ★ 为什么必须 delay：「今天收盘价站上均线」这个判断要等今天收盘才知道，
#      最早也只能**明天**按它持仓。可作弊版是在**当天**就用它交易了——
#      等于用今天的答案做今天的题。这就是前视偏差最日常的样子：**少了一个 shift**。
#    它有多不起眼：语法完全正确、不报错、回测框架也不会拦你，只是数字全假。
df["signal_honest"] = df["signal_cheat"].shift(1).fillna(0)
#   shift(1) ：整体下移一行 —— 第 t 行拿到的是第 t-1 天的值，也就是「用昨天的信号」
#   fillna(0)：下移之后第一行是空的，填 0（第一天还没有信号，空仓）
#
#   更露骨的表亲是 shift(-1)：直接把**明天**的涨跌搬来今天当信号。
#   方向上是一回事——都是让"未来才知道的信息"参与到"当下的决策"里。

# 6. 算两版的日收益：当日收益 = 持仓信号 × 当日涨跌幅
df["ret_cheat"] = df["signal_cheat"] * df["ret"]
df["ret_honest"] = df["signal_honest"] * df["ret"]

# 7. 累计净值：(1 + 日收益) 连乘 —— 这就是回测曲线
nav_cheat = (1 + df["ret_cheat"].fillna(0)).cumprod()
nav_honest = (1 + df["ret_honest"].fillna(0)).cumprod()

print()
print("=" * 60)
print("【第二部分】前视偏差实验（合成随机行情，60 天）")
print("=" * 60)
print(f"行情本身：涨了 {(df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100:.1f}%")
print()
print(f"作弊版（signal 用了 shift(-1)）：累计 {(nav_cheat.iloc[-1] - 1) * 100:>7.1f}%")
print(f"老实版（只用过去数据 + delay 一天）：累计 {(nav_honest.iloc[-1] - 1) * 100:>7.1f}%")
print()
print("看点：")
print("1. 合成数据里没有任何真实规律——老实版跑出来就是行情的水平（甚至还不如它），")
print("   而作弊版凭空多赚几十个百分点。多出来的不是策略赚的，是偷看赚的。")
print("2. 这个作弊版写进回测框架里，不会报任何错，只会给你一条漂亮的曲线。")
print("   实盘上线那天，未来不再可偷，收益立刻回归随机。")
print("3. 两版之间的差别只有一行 shift(1)。练习时把你的策略也写两版，")
print("   用真实数据跑一遍：老实版那版，才是你策略的真实水平。")
