# demo_extract_json.py —— 参考脚手架：提取型 Prompt 的三层防线
#
# ⚠️ 演示场景是「体检报告摘要 → JSON」。你的练习场景是「财报摘要 → JSON」，
#    字段、数据、文本都必须你自己写——看思路，别抄数据。
#
# 运行前先设 key（终端里临时设，别写进代码——写进去会跟着 git 一起泄露）：
#   Windows:    $env:DEEPSEEK_API_KEY = 'sk-xxx'
#   Mac/Linux:  export DEEPSEEK_API_KEY='sk-xxx'
#
# 运行方式（openai 库不在项目依赖里，用 --with 临时装上，不动 pyproject.toml）：
#   uv run --with openai python demo_extract_json.py

import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),   # 从环境变量读，和 d68/d69/d70 一样
    base_url="https://api.deepseek.com",
)


def ask(prompt, json_mode=False):
    """把 prompt 发出去，返回模型回复的正文。

    参数 prompt    ：完整的一段话（今天还是只用 user，不碰 system）
    参数 json_mode ：是否开启 API 层的结构化输出约束（第二层防线）
                     False = 只靠 Prompt 自己约束（第一层防线）
                     True  = 额外告诉服务端「必须吐合法 JSON」

    为什么要加这个参数：今天要对比「约束加在哪一层，效果差多少」。
    注意 API 名称不统一——OpenAI 叫 response_format，有些服务叫别的，用法要现查。
    """
    kwargs = {
        "model": "deepseek-v4-flash",                           # 和 d68/d69/d70 同一个模型
        "messages": [{"role": "user", "content": prompt}],      # 单轮对话
        "temperature": 0,   # 固定 0，排除随机性——否则分不清"输出变了"是 prompt 变了还是模型心情不同
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}     # ★ 第二层防线：API 层的硬约束
    resp = client.chat.completions.create(**kwargs)
    return resp.choices[0].message.content


def strip_fence(text):
    """去掉模型爱加的 ``` 代码块外壳，只留里面的内容。（d70 学过，直接复用）

    参数 text：模型返回的原始文本
    返回值  ：去掉首尾 ``` 之后的纯内容

    为什么必须有这一步：模型经常把 JSON 包在 Markdown 代码块里，
    直接 json.loads 一定报错。这是工程里必做的一步，不是可选项。
    """
    t = text.strip()                    # 去掉首尾空白
    if t.startswith("```"):             # 开头是 ```
        t = t.split("\n", 1)[1]         #   split(分隔符, 最大切几次)：切 1 次 → [第一行, 剩下的]
                                        #   [1] 取"剩下的全部"，丢掉 ```json 那一行
        t = t.rsplit("```", 1)[0]       #   rsplit 从右往左切，同样只切 1 次
                                        #   [0] 取"切剩下的前半段"，丢掉结尾的 ```
    return t.strip()


# ============================================================
# 演示数据：一段体检报告摘要（你的练习要换成财报文本） 
# ============================================================

REPORT = """体检报告摘要（2026-06-12，男性，41岁）
身高 175cm，体重 78kg，体质指数 25.5。
血压测量：收缩压 142 mmHg，舒张压 91 mmHg。
空腹血糖 6.3 mmol/L，总胆固醇 5.8 mmol/L，甘油三酯 1.4 mmol/L。
腹部超声提示轻度脂肪肝。结论：血压偏高、空腹血糖偏高，建议控制饮食、
增加有氧运动，三个月后复查血压与血糖。"""

# 字段清单 = 「结构层校验」的判据。
# 注意每个字段都是机器能判定的东西（键名存在、类型对），
# 这是校验的第一关——过了这关只说明"程序接得住"，不代表"数值可信"。
REQUIRED_FIELDS = ["检查日期", "空腹血糖", "收缩压", "舒张压", "体质指数BMI", "异常项", "医生建议"]


# ============================================================
# 第一层防线：Prompt 内约束（字段定义 + 示范 JSON + 反例）
# ============================================================

# 弱约束版：只说要 JSON，不定义字段、不给模板。
# 这一版就是"以为说清楚了"的典型——它没犯错，但什么都没约束住。
PROMPT_WEAK = f"""把下面这段体检报告提取成 JSON：

{REPORT}"""

# 强约束版：三段结构（指令 + 例子/模板 + 格式）在今天的具体落地。
# ★ 关键在【字段定义】那一段——字段名谁都能写，"这是什么口径"才是今天要学的东西。
PROMPT_STRONG = f"""你是体检报告结构化助手。把下面的体检报告提取成 JSON。

【字段定义】
- 检查日期：字符串，"YYYY-MM-DD" 格式
- 空腹血糖：数字，单位 mmol/L，只填数值不填单位
- 收缩压：整数，单位 mmHg
- 舒张压：整数，单位 mmHg
- 体质指数BMI：数字，保留 1 位小数
- 异常项：字符串数组，只列报告明确写了"偏高/偏低/异常/提示"的项目简称，如 ["血压", "空腹血糖"]
- 医生建议：字符串，原文照抄建议部分，不要自己总结

【格式模板】（严格照这个结构，字段一个都不能少）
{{
  "检查日期": "2026-06-12",
  "空腹血糖": 0.0,
  "收缩压": 0,
  "舒张压": 0,
  "体质指数BMI": 0.0,
  "异常项": [],
  "医生建议": ""
}}

【反面例子】不要输出这样——少了字段、还带了单位字符串，程序接不住：
{{"空腹血糖": "6.3 mmol/L", "血压": "142/91"}}

【输出要求】只输出 JSON 本身，不要解释、不要 Markdown 代码块。

体检报告原文：
{REPORT}"""


# ============================================================
# 代码层：校验 + 重试（第三层防线）——这段是固定写法模板，照抄即可
# ============================================================

def validate(data):
    """结构层校验：返回缺了什么 / 类型错了什么。

    参数 data：json.loads 之后的字典
    返回值  ：问题描述列表；空列表 = 通过

    只做机器能判定的检查：键在不在、类型对不对。
    「6.3 是不是真的偏高」这种语义判断不在这里做——那是语义层，交给业务规则。
    """
    problems = []
    for f in REQUIRED_FIELDS:                       # 逐个字段过一遍
        if f not in data:
            problems.append(f"缺字段「{f}」")
        elif f == "异常项" and not isinstance(data[f], list):   # isinstance(值, 类型)：判断类型
            problems.append(f"「{f}」应该是数组，实际是 {type(data[f]).__name__}")
        elif f == "医生建议" and not isinstance(data[f], str):
            problems.append(f"「{f}」应该是字符串，实际是 {type(data[f]).__name__}")
    return problems


def extract(prompt, json_mode=False, max_retry=1, tag=""):
    """调用 → 解析 → 校验 → 不合格就带着错误信息重试。返回 (数据或None, 尝试次数)。

    参数 prompt   ：完整 prompt
    参数 json_mode：是否开第二层防线
    参数 max_retry：最多重试几次（今天只给 1 次——它是兜底，不是主力）
    参数 tag      ：打印时用的标签
    """
    current = prompt                                # 会在重试时被改写，所以用副本
    for attempt in range(max_retry + 1):            # range(2) → 0,1 两次：首次 + 1 次重试
        raw = ask(current, json_mode=json_mode)
        text = strip_fence(raw)                     # 先扒掉 ``` 外壳
        try:
            data = json.loads(text)                 # JSON 字符串 → Python 字典
        except json.JSONDecodeError as e:
            problem = f"不是合法 JSON（{e}）"        # 解析失败也是"可反馈的错误信息"
            print(f"[{tag}] 第{attempt + 1}次：解析失败 —— {problem}")
            data = None
        else:
            problems = validate(data)
            if not problems:
                print(f"[{tag}] 第{attempt + 1}次：✅ 通过（字段 {list(data.keys())}）")
                return data, attempt + 1
            problem = "；".join(problems)
            print(f"[{tag}] 第{attempt + 1}次：结构不合格 —— {problem}")

        if attempt < max_retry:                     # 还有重试机会 → 把错误写回 prompt
            current = prompt + f"""

【上一次输出不合格】{problem}
请重新输出，修正上述问题，只输出 JSON。"""
            print(f"[{tag}] → 把错误信息写回 Prompt，重试一次")

    print(f"[{tag}] ❌ 重试用完仍未通过")
    return None, max_retry + 1


# ============================================================
# 跑对比：约束加在哪一层，结果差多少
# ============================================================

print("=" * 60)
print("【弱约束】只说「输出 JSON」，不给字段定义、不给模板")
print("=" * 60)
extract(PROMPT_WEAK, tag="弱约束")

print()
print("=" * 60)
print("【强约束】字段定义 + 示范 JSON + 反例（第一层防线）")
print("=" * 60)
extract(PROMPT_STRONG, tag="强约束")

print()
print("=" * 60)
print("【强约束 + JSON mode】再加 API 层硬约束（第二层防线）")
print("=" * 60)
try:
    extract(PROMPT_STRONG, json_mode=True, tag="强+API")
except Exception as e:
    # 万一这个 API/模型不支持 response_format，这里会炸——把它当成一次观察，不是失败
    print(f"服务端不接受 json_mode 参数：{type(e).__name__} —— {e}")
    print("说明这一层防线的开关名/支持情况要按服务商文档现查，不能照抄。")

print()
print("=" * 60)
print("看点：")
print("=" * 60)
print("1. 弱约束那一次，缺了哪个字段？—— 它没报错，它只是「猜」了你的口径")
print("2. 强约束第一次就通过了吗？如果它也错了，错在哪一层？")
print("3. 把重试次数改成 0 再跑一遍强约束：重试是兜底，不是主力——")
print("   如果同一条 Prompt 每次都靠重试才过，该改的是 Prompt，不是重试")
