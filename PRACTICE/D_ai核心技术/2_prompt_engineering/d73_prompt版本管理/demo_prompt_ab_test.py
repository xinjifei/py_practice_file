# demo_prompt_ab_test.py —— 参考脚手架：Prompt 当文件管 + 做一次 A/B 对比
#
# 今天要看的就两件事：
#   ① Prompt 模板 = 固定的骨架 + {占位符}，运行时把具体数据填进去
#   ② A/B 对比   = 两个版本的 prompt，**其他条件全部锁死**，只看质量差在哪
#
# ⚠️ 演示任务用的是「财经新闻标题 → 事件 + 情绪 JSON」。
#    你练习要换任务（财报指标提取 / 策略生成）和换数据，别照抄。
#
# 运行前先设 key（终端里临时设，别写进代码）：
#   Windows:    $env:DEEPSEEK_API_KEY = 'sk-xxx'
#   Mac/Linux:  export DEEPSEEK_API_KEY='sk-xxx'
#
# 运行方式：
#   uv run --with openai python demo_prompt_ab_test.py

import json
import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


# ============================================================
# 第 1 部分：Prompt 模板 —— 骨架不变，数据靠 {占位符} 填
# ============================================================
#
# ★ 今天说的「Prompt 存独立文件」，读文件就是这一个函数的事。
#   真实项目里下面两段模板不该躺在 .py 里，而是各存一个文件：
#       prompts/news_v1.txt
#       prompts/news_v2.txt
#   代码里只留「怎么读、怎么填」，正文交给文件 —— 这样改 prompt
#   不用碰代码，Git 也能单独追踪 prompt 的每一次修改。
#
#   下面这个函数 demo 里不调用，留给练习时用：


def load_prompt(path):
    """从文件读一段 prompt 文本。

    参数 path：文件路径，字符串，比如 "prompts/news_v1.txt"
    返回     ：文件里的全部内容，一个字符串
    """
    with open(path, encoding="utf-8") as f:
        # encoding="utf-8" 一定要显式写：prompt 里有中文，
        # 不写的话 Windows 默认按 GBK 打开，直接 UnicodeDecodeError
        return f.read()


# ★ 下面两段是「同一个任务的两个版本」。
#   v1 是一句话指令；v2 把字段、取值范围、边界规则、输出格式全钉死了。
#   两版**不一样的地方**，就是这次 A/B 唯一在对比的那个变量。
TEMPLATE_V1 = """判断下面这条财经新闻是利好还是利空。

新闻标题：{headline}"""

TEMPLATE_V2 = """你是一个金融文本标注员。判断下面这条财经新闻对该公司股价的影响。

新闻标题：{headline}

要求：
1. 只输出 JSON，不要任何解释，不要 markdown 代码块
2. JSON 必须且只能包含这两个字段：
   - "event"：事件类型，只能从 [业绩, 融资, 监管, 人事, 合作] 里选一个
   - "sentiment"：影响方向，只能是 "利好" / "利空" / "中性" 之一
3. 如果标题信息不足以判断，sentiment 填 "中性"，不要瞎猜
"""


def render(template, **kwargs):
    """把模板里的 {占位符} 换成真实数据。

    参数 template：带 {xxx} 占位符的字符串
    参数 **kwargs：要填进去的键值对，键名必须和占位符里的名字一模一样
    返回        ：填好的字符串

    为什么用 **kwargs：它能接**任意多个**具名参数。
    调用 render(TEMPLATE_V1, headline="...") 时，
    kwargs 就是 {"headline": "..."} 这个字典，
    里面的键去和模板里的 {headline} 对上号。
    """
    return template.format(**kwargs)


# ============================================================
# 第 2 部分：A/B 对比 —— 只放一个变量动，其他全部锁死
# ============================================================

# ★ 测试样本：3 条标题，两个版本跑的是**同一组**。
#   如果 v1 跑这 3 条、v2 跑另外 3 条，比出来的差异就分不清是
#   "版本造成"的还是"题目难易造成"的 —— 这就是变量没控制住。
SAMPLES = [
    "宁德时代发布三季度财报：净利润同比增长 42%，超市场预期",
    "某医药公司因信披违规被证监会立案调查",
    "公司公告：拟以自有资金回购股份，金额不超过 5 亿元",
]


def ask(prompt):
    """发一段 prompt，返回回复正文。

    参数 prompt：完整的一段话
    """
    resp = client.chat.completions.create(
        model="deepseek-v4-flash",
        # ↑ 两个版本必须用同一个模型，否则差异可能来自换模型而不是换 prompt
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        # ↑ ★ 锁死 0。不锁死的话，**同一个 prompt 跑两次结果都可能不同**，
        #    你就分不清差异来自版本还是来自随机性（接 d68 学的 temperature）
    )
    return resp.choices[0].message.content


def check_json(text):
    """自动判据：这段输出是合格 JSON 吗？两个字段齐不齐？

    参数 text：模型回复的正文，字符串
    返回     ：(是否合格, 原因) —— 布尔值 + 一句说明

    为什么要有这个函数：d72 学过的「审查」在这里必须**变成代码**。
    靠肉眼感觉"这个版本好像好一点"，得出的结论站不住；
    能不能被程序解析、字段齐不齐，是硬指标（接 d71 的校验兜底）。
    """
    try:
        obj = json.loads(text)
        # json.loads：把 JSON 格式的字符串解析成 Python 的 dict
        # 解析失败会抛 JSONDecodeError，所以下面要接住它
    except json.JSONDecodeError:
        return False, "不是合法 JSON"
    missing = [key for key in ("event", "sentiment") if key not in obj]
    # 列表推导式：把两个必需字段里**缺的**那些挑出来
    if missing:
        return False, f"缺字段 {missing}"
    return True, "通过"


def run_version(name, template):
    """跑一个 prompt 版本，返回 [(标题, 输出, 是否合格, 原因), ...]。

    参数 name    ：版本名，只用来打印（"v1" / "v2"）
    参数 template：这一版的模板字符串
    返回        ：每条样本一行的结果列表
    """
    print("=" * 70)
    print(f"【版本 {name}】")
    print("=" * 70)
    rows = []
    for headline in SAMPLES:
        prompt = render(template, headline=headline)   # 填占位符
        output = ask(prompt).strip()                   # 发出去，拿到回复
        ok, reason = check_json(output)                # 自动判据
        rows.append((headline, output, ok, reason))
        print(f"标题：{headline}")
        print(f"输出：{output[:120]}")
        print(f"判定：{'✅' if ok else '❌'} {reason}")
        print("-" * 70)
    return rows


print()
v1_rows = run_version("v1", TEMPLATE_V1)
print()
v2_rows = run_version("v2", TEMPLATE_V2)

# ---- 汇总：把两版通过率并排摆出来 ----
print()
print("=" * 70)
print("【对比汇总】")
print("=" * 70)
for name, rows in (("v1", v1_rows), ("v2", v2_rows)):
    passed = sum(1 for r in rows if r[2])       # 数一数有几条通过
    print(f"{name}：{passed}/{len(rows)} 条通过自动判据")

print()
print("看点：")
print("1. v1 大概率通不过 —— 它不是「写得差」，是**没被约束**。")
print("   模型会自作主张给你一段解释性文字，程序直接没法用。")
print("2. v2 通过率高，靠的是要求里的三条硬约束（格式、取值范围、边界处理），")
print("   而不是「说得更客气」。好的 prompt 是**规格说明书**，不是更好的措辞。")
print("3. 这就是为什么 prompt 该进 Git：这两个版本只差几行字，")
print("   差异有多大，上面这个通过率就是证据。改了不记，下次你没法复现、")
print("   也没法证明「新版确实更好」。")
print()
print("练习时：把 v1/v2 换成你自己的任务（财报指标提取 / 策略生成），")
print("       样本换成你自己的数据，判据换成你要的字段 —— 结构照这个来。")
