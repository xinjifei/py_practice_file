# d73_check.py —— 自动判据：拿代码给模型输出判分
#
# 「判据」= 判断的依据。人工判据靠你看，自动判据靠这段代码跑。
#
# 这个文件只做**第一层（结构层）**的检查，也就是机器能百分百判定的事：
#   1. 这段输出能不能被 json.loads 解析
#   2. 字段齐不齐
#   3. 类型对不对、取值在不在允许范围内
#
# 它**故意不碰**另外两层：
#   - 语义层：「营收 2830.72 亿」有没有抄错？—— 得对着原文核
#   - 业务层：「万科该算利空还是中性」？—— 得人来判
# 硬把这两层塞进判据，判据自己就先不可靠了。
#
# 用法：
#   from d73_check import check, SPEC_财报摘要
#   ok, problems = check(模型输出, SPEC_财报摘要)

import json


# ===============================================================
# 类型记号：写 spec 时用，比写裸类型好读
# ===============================================================
# isinstance 可以接一个类型，也可以接一个**元组**（满足其中之一就算过）。
# 所以"数字"直接写成 (int, float)——JSON 里 3 和 3.0 都是数字，不该挑。
NUM = (int, float)
NUM_OR_NULL = (int, float, type(None))
# ↑ 允许 null：原文没给这个数的时候，模型应该留空，而不是编一个


def strip_fence(text):
    """扒掉模型爱加的 ``` 代码块外壳。（d70/d71 学过，原样复用）

    参数 text：模型返回的原始文本
    返回     ：去掉首尾 ``` 之后的纯内容

    为什么这是判据的第一步：模型经常把 JSON 包在 Markdown 代码块里。
    不先扒皮就 json.loads，报的错是"不是合法 JSON"——
    可那根本不是 prompt 写得差，是你没先扒皮。判据会冤枉 prompt。
    """
    t = text.strip()                      # 去掉首尾空白（换行、空格）
    if t.startswith("```"):               # 开头是不是 ```
        t = t.split("\n", 1)[1]           # 按换行切一刀 → [第一行, 剩下的]，取剩下的
        t = t.rsplit("```", 1)[0]         # 从右往左切一刀，丢掉结尾的 ```
    return t.strip()


def _types_of(expected):
    """把"类型记号"统一成元组，方便 isinstance 和成员判断。

    expected 可能是单个类型（str），也可能是元组（(int, float)）。
    统一成元组后，两种写法后面的代码不用分情况。
    """
    return expected if isinstance(expected, tuple) else (expected,)


def _type_label(expected):
    """把类型记号转成报错时给人看的文字，如 (int, float) → "int / float"。"""
    return " / ".join(getattr(t, "__name__", str(t)) for t in _types_of(expected))


def _is_type_spec(spec_value):
    """判断 spec 里这一项写的是"类型"还是"允许的取值"。

    两种写法都支持，靠长相区分：
        "要素": list                      ← 类型（list 本身是个 type）
        "难度": ["简单", "中等", "复杂"]   ← 取值范围（这是个 list 实例，不是 type）

    为什么值得支持第二种：类型对了不代表内容对。
    模型完全可以给你 "难度": "很难" —— 类型是 str，检查通过，但业务上就是错的。
    """
    if isinstance(spec_value, type):
        return True
    return isinstance(spec_value, tuple) and all(isinstance(t, type) for t in spec_value)


def check(text, spec):
    """给一段模型输出判分。这就是"自动判据"本体。

    参数 text：模型返回的原始文本（不用自己先扒 ```，函数里会做）
    参数 spec：字段清单，形如 {"字段名": 期望}。
               "期望"写类型（str / list / NUM），或者写允许取值的列表。

    返回：(是否通过, 问题列表)
          (True,  [])            —— 全过
          (False, ["...", ...])  —— 有问题，每条一句话，可以直接打印给人看
    """
    problems = []

    try:
        data = json.loads(strip_fence(text))
    except json.JSONDecodeError as e:
        # 连解析都过不了，后面的字段检查没意义，直接返回
        return False, [f"不是合法 JSON（{e}）"]

    if not isinstance(data, dict):
        # 顶层必须是对象。模型要是吐了一个数组或一个裸数字，后面字段检查全得崩
        return False, [f"顶层应该是对象 {{}}，实际是 {type(data).__name__}"]

    for field, expected in spec.items():
        if field not in data:
            problems.append(f"缺字段「{field}」")
            continue                            # 字段都没有，类型就没得查了

        value = data[field]

        if _is_type_spec(expected):
            # ---- 检查一：类型 ----
            # ★ isinstance(True, int) 是 True —— 布尔是整数的子类。
            #   所以模型把数字写成 true 时，单靠 isinstance 会放它过去。
            #   判据的漏洞往往就长这样：不报错，只是悄悄放行。这里单独拦一下。
            if isinstance(value, bool) and bool not in _types_of(expected):
                problems.append(f"「{field}」应该是 {_type_label(expected)}，实际是布尔值")
            elif not isinstance(value, expected):
                problems.append(
                    f"「{field}」应该是 {_type_label(expected)}，实际是 {type(value).__name__}"
                )
        else:
            # ---- 检查二：取值范围 ----
            if value not in expected:
                problems.append(f"「{field}」只能是 {expected}，实际是 {value!r}")

    # ---- 检查三：交叉检查 —— 字段之间自不自洽 ----
    # 上面两步都是"一个字段自己看合不合法"。这一步不一样：
    # 它拿输出的**一部分去验另一部分**，所以不需要原文，纯代码就能做。
    #
    # 规则：「数据缺失项」是模型自己的声明。声明了缺失，值就必须真的是 null。
    # 模型一边说"这个数原文没有"，一边又填了个 0 —— 这是自己打自己脸，
    # 而单字段检查永远看不出来，因为 0 本来就是个合法的数字。
    declared = data.get("数据缺失项")
    if isinstance(declared, list):
        for field in declared:
            if field not in spec:
                problems.append(f"「数据缺失项」里的「{field}」不是本模板的字段名")
            elif data.get(field) is not None:
                problems.append(
                    f"「{field}」被列进「数据缺失项」，值却是 {data.get(field)!r}"
                    f"——既然声明缺失，就必须填 null"
                )

        # 反方向也查一遍：值是 null，却没声明缺失。
        # 这条比上一条更严，防的是"悄悄留空"——下游只看到一个 null，
        # 既不知道为什么空，也不知道该不该重试。
        for field in spec:
            if field == "数据缺失项":
                continue
            if field in data and data[field] is None and field not in declared:
                problems.append(f"「{field}」是 null，但没有列进「数据缺失项」")

    return (len(problems) == 0), problems


# ===============================================================
# 各模板的字段清单 —— 判据的"考纲"
# ===============================================================
# ★ 字段名必须和 prompts/ 里模板的【格式模板】**一字不差**。
#   对不上，判据会一直报"缺字段"，而其实缺的是你抄错了名字——
#   这时候你该改的是判据，不是 prompt。判据错了比没判据更坏，
#   它会指挥你去改一个本来没问题的地方。

SPEC_财报摘要 = {
    "公司名称": str,
    "报告期": str,
    # ★ 数值字段一律用 NUM_OR_NULL，不是 NUM。
    #   原因：模板的契约里写了"原文没提到的字段填 null 并列入数据缺失项"。
    #   只要模板允许 null，判据就必须允许 null——否则模型**正确地**填了 null，
    #   判据反倒判它失败，然后你回去改一个本来没问题的 prompt。
    #   一句话：判据必须和模板的契约对齐，不能比契约更严。
    "营业收入": NUM_OR_NULL,
    "营收同比": NUM_OR_NULL,
    "净利润": NUM_OR_NULL,
    "净利润同比": NUM_OR_NULL,
    "毛利率": NUM_OR_NULL,
    "经营现金流": NUM_OR_NULL,
    "风险提示": list,
    "数据缺失项": list,
}

SPEC_三段法 = {
    "名称": str,
    "要素": list,
    "步骤数": int,
    # ↑ 这里故意写 int 不写 NUM：步骤数就该是整数，3.0 也算不合格。
    #   这是"判据该多严"的一个判断题——你要更宽松就换成 NUM，但那是你的选择，
    #   得是有意识做的，不是顺手抄的。
    "难度": ["简单", "中等", "复杂"],
    # ↑ 取值范围检查：类型是 str 只说明它给了个字符串，
    #   "很难""一般般"也都是 str。列出允许值才拦得住。
}
