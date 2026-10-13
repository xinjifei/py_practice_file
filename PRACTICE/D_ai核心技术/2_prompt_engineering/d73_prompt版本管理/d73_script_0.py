# d73_script_0.py —— 把 prompts/ 里的模板和 samples/ 里的数据接起来跑，并自动判分
#
# 今天这条链路：模板文件 + 数据文件 → 填占位符 → 发给模型 → **自动判据打分**
#   prompts/xxx.txt   骨架，占位符原样留着，不装具体数据
#   samples/xxx.txt   数据，每次要换的那部分
#   d73_check.py      判据，拿代码给输出判"过/不过"
#   前两者在**运行时**才拼到一起 —— 这就是"模板"和"一次性 prompt"的区别
#
# 运行前先设 key（终端里临时设，别写进代码）：
#   Windows:    $env:DEEPSEEK_API_KEY = 'sk-xxx'
#   Mac/Linux:  export DEEPSEEK_API_KEY='sk-xxx'
#
# 运行方式（★ 在任意目录下都能跑，路径问题见下面 BASE 那一段）：
#   uv run --with openai python d73_script_0.py

import os
from pathlib import Path

from openai import OpenAI

from d73_check import check, SPEC_财报摘要, SPEC_三段法
# ↑ 判据单独放 d73_check.py。拆开有两个好处：
#   1. 判据不掺在教学脚本里——将来做 A/B 对比，两个版本能共用同一套判据，
#      这是"变量控制"的前提：判据也必须一致。
#   2. 调判据的松紧不用动主流程。

# 先拦一道：没设 key 就直接说清楚，别等发请求时报一个看不懂的 401
if not os.environ.get("DEEPSEEK_API_KEY"):
    raise SystemExit("没找到 DEEPSEEK_API_KEY 环境变量，先在终端里设一下再跑。")

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


# ===============================================================
# 路径锚定 —— 修掉"换个目录跑就 FileNotFoundError"
# ===============================================================
# ★ 上一版写的是 "./prompts/xxx.txt"。那个 "./" 指的是**当前工作目录**，
#   也就是"你在哪个目录敲的命令"，不是"这个脚本文件放在哪"。
#   你人在数学仓库里敲命令，它就去数学仓库找 prompts/ —— 当然找不到。
#
# 下面这行：不管从哪儿启动，先算出**本脚本自己所在的目录**，再拿它当基准拼路径。
# 脚本搬到哪、从哪跑，都不会错。
#
#   __file__     Python 自动塞进每个脚本的变量，值是**本脚本自己的路径**
#                （你从没定义过它，但一直存在）
#   .resolve()   转成绝对路径（__file__ 有时给的是相对路径）
#   .parent      取上一层，也就是脚本所在的那个文件夹
BASE = Path(__file__).resolve().parent


def ask(prompt):
    """把一段 prompt 发给模型，返回回复正文。（和 d70/d71/d72 一样，没改）"""
    resp = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return resp.choices[0].message.content


def read(rel_path):
    """读一个文本文件，返回内容字符串。

    参数 rel_path：相对**本脚本所在目录**的路径，如 "prompts/财报摘要提取_v2.txt"
    """
    path = BASE / rel_path
    # BASE / "prompts" / "x.txt" 是 pathlib 的拼路径写法：用 / 而不是字符串加号。
    # 好处是它会自己处理目录分隔符，Windows 上不会拼出混乱的反斜杠。
    with open(path, "r", encoding="utf-8") as f:
        # encoding="utf-8" 必须显式写：文件里有中文，
        # 不写的话 Windows 默认按 GBK 打开，直接 UnicodeDecodeError
        content = f.read()      # ★ 上一版这行叫 read，和函数名重名了，改掉
    return content


def fill(template, placeholder, data):
    """把模板里的占位符换成真实数据，返回可以整段发出去的 prompt。

    参数 template    ：模板原文（读自 prompts/）
    参数 placeholder ：要替换掉的占位符本身，如 "{财报摘要}"；传 None 表示不用填
    参数 data        ：用来替换进去的数据（读自 samples/）
    """
    if placeholder is None:
        # 有些 prompt 里根本没有变量（比如策略思路生成），原样返回
        return template
    # ★ 这里用 replace 而不是 format，是个关键选择：
    #   财报模板里【格式模板】那段本身就是一段 JSON，含大量**字面**花括号 {}。
    #   format() 分不清"这是待填的槽位"还是"这就是我要输出的 JSON"，
    #   会把 {"公司名称": ...} 也当成槽位，直接抛 KeyError。
    #   replace() 只认你点名的那一个字符串，其它花括号一律不碰。
    return template.replace(placeholder, data)


# ===============================================================
# 配对表：哪个模板、填哪个占位符、配哪些样本、用哪套判据
# ===============================================================
# 模板在 prompts/、数据在 samples/、判据在 d73_check.py，靠这张表连起来。
# 一个模板配多个样本 = 同一副骨架喂不同数据 —— 这正是模板的价值。
# 财报提取的样本单拎出来定义 —— ★ 因为 v1 和 v2 必须跑**同一组**样本。
# 这是 A/B 的硬要求：如果 v1 跑这三条、v2 跑另外三条，
# 比出来的差异就分不清是"版本变好了"还是"题目变简单了"。
# 变量控制不是嘴上说说，它就长这个样子——两个 job 共用同一个列表对象。
SAMPLES_财报 = [
    "samples/财报摘要_1_宁德时代.txt",
    "samples/财报摘要_2_贵州茅台.txt",
    "samples/财报摘要_3_万科.txt",
]

JOBS = [
    {
        "name": "财报提取 v1",
        "template": "prompts/财报摘要提取_v1.txt",
        "placeholder": "{财报摘要}",
        "samples": SAMPLES_财报,
        "spec": SPEC_财报摘要,
    },
    {
        "name": "财报提取 v2",
        "template": "prompts/财报摘要提取_v2.txt",
        "placeholder": "{财报摘要}",
        "samples": SAMPLES_财报,          # ★ 和 v1 同一个列表 —— 唯一在变的是模板
        "spec": SPEC_财报摘要,            # ★ 判据也要一致，否则比的就不是模板了
    },
    {
        # ★ v3 = v2 逐字复制，**只改了反面例子里的那几个数字**（换成人造哨兵值）。
        #   这是一个受控实验，不是一次"改进"：
        #   如果输出里冒出 44444 / 55555，说明模型在照抄反面例子；
        #   如果输出还是 0.0，说明它抄的不是例子，是"数值默认为 0"的先验。
        #   两个结论导向完全不同的修法，所以值得多跑这一版。
        "name": "财报提取 v3",
        "template": "prompts/财报摘要提取_v3.txt",
        "placeholder": "{财报摘要}",
        "samples": SAMPLES_财报,
        "spec": SPEC_财报摘要,
    },
    {
        "name": "基础三段法",
        "template": "prompts/基础三段法.txt",
        "placeholder": "{输入文本}",
        "samples": [
            "samples/三段法输入_1.txt",
            "samples/三段法输入_2.txt",
        ],
        "spec": SPEC_三段法,
    },
    {
        "name": "策略思路生成",
        "template": "prompts/策略思路生成.txt",
        "placeholder": None,   # ★ 这条没有占位符 —— 它不需要数据，也就谈不上"模板"
        "samples": [],         #   空列表 = 只跑一次，不填数据
        "spec": None,          # ★ 输出是自由文本，不是 JSON —— 结构判据用不上
    },
]


# ===============================================================
# 跑：模板读一次，样本逐个填进去，每次都用判据打一次分
# ===============================================================
summary = {}        # 汇总用：{"模板名": (通过次数, 总次数)}

for job in JOBS:
    template = read(job["template"])        # 骨架读一次就够

    samples = job["samples"] or [None]
    # ↑ "或"运算：左边是空列表（假值）时取右边 → [None]，
    #   意思是"这次没有数据要填"，下面的循环也就只跑一次。

    for i, sample in enumerate(samples, start=1):
        # enumerate(序列, start=1)：一次拿到"序号"和"数据"两样东西，序号从 1 数起。
        # 效果和你手写的 cun 计数器一样，但不用自己维护变量。
        data = read(sample) if sample else None
        prompt = fill(template, job["placeholder"], data)

        if job["placeholder"] and job["placeholder"] in prompt:
            # 填完之后占位符还在，说明配对表里的名字和模板里的对不上
            print(f"⚠️  {job['name']}：占位符 {job['placeholder']} 没被替换掉，检查配对表")

        print("=" * 60)
        print(f"【{job['name']}】第 {i}/{len(samples)} 次")
        # ★ 上一版三次输出全打印成 result1，根本分不清哪条对应哪个 prompt。
        #   这里把模板名和序号带上，输出才对得上人。
        print("=" * 60)

        result = ask(prompt)
        print(result)
        print("-" * 60)

        # ---- 判分：拿自动判据给这次输出打分 ----
        if job["spec"] is None:
            print("判据：跳过（这条输出是自由文本，结构判据用不上）")
        else:
            ok, problems = check(result, job["spec"])
            # check 返回两个东西：(是否通过, 问题列表)，这叫"元组解包"
            if ok:
                print("判据：✅ 通过")
            else:
                print("判据：❌ 不通过")
                for p in problems:          # 逐条把原因打印出来——这是判据最值钱的部分
                    print(f"      · {p}")

            passed, total = summary.get(job["name"], (0, 0))
            # dict.get(键, 默认值)：键不存在时返回默认值，不用先判断再取
            summary[job["name"]] = (passed + (1 if ok else 0), total + 1)

        print()


# ===============================================================
# 汇总：通过率
# ===============================================================
# 为什么一定要有这个汇总：单个案例的"过/不过"你已经看见了，
# 但**通过率才是可以拿去做 A/B 对比的那个数**。
# 将来你把模板改一版（v2），两版各跑这同一组样本，
# 比的就是这两行数字——那时候你就不用靠"我感觉 v2 好一点"了。
print("=" * 60)
print("【判据汇总】")
print("=" * 60)
for name, (passed, total) in summary.items():
    print(f"{name}：{passed}/{total} 通过")
