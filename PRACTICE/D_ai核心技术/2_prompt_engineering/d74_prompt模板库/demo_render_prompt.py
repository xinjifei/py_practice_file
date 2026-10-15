"""
demo_render_prompt.py —— 把「模板 + 变量」渲染成最终 prompt 的最小示例

今天的目标：让模板从"一段文字"变成"代码能用的资产"。
这个 demo 演示渲染机制，以及一个几乎必踩的坑。

⚠️ demo 用的是「策略评审」模板。你练习时请从模板库里换一个模板、换一组变量。
"""

from pathlib import Path        # Path：比 os.path 更现代的路径写法
from string import Template     # Template：专门做「占位符替换」的类

# ── 1. 模板长什么样 ────────────────────────────────────────────
# 实际使用时这一行改成从模板库读文件：
#     tpl_text = Path("prompts/策略思路生成.txt").read_text(encoding="utf-8")
# read_text() 的参数：
#   encoding：文件编码。中文模板必须写 "utf-8"，
#             否则 Windows 默认按 GBK 打开，会乱码或直接报 UnicodeDecodeError
tpl_text = """你是量化策略评审员。
请评审以下策略：$strategy_name
重点检查：$check_point
输出格式：{"verdict": "...", "reason": "..."}"""

# ── 2. 变量（模板里要填的空）──────────────────────────────────
# 一个 dict：key = 占位符的名字，value = 要填进去的内容
values = {"strategy_name": "双均线交叉", "check_point": "是否有止损"}

# ── 3. 先试 .format() —— 会挂，看清楚为什么 ────────────────────
# .format() 把每一对花括号 {} 都当成占位符。
# 可模板里那段 JSON 示例 {"verdict": ...} 也被当成了占位符，
# 于是它去找一个名叫 '"verdict"' 的变量 → KeyError。
# 这是 prompt 模板最典型的坑：**prompt 里几乎必然出现 JSON 示例**。
#   **values 是"解包"：把 dict 拆成关键字参数传进去，等价于 format(strategy_name=..., check_point=...)
try:
    print("[.format() ] " + tpl_text.format(**values))
except KeyError as e:
    print(f"[.format() ] 挂了 —— KeyError: {e}")
    print("             原因：JSON 的花括号被误当成占位符\n")

# ── 4. 换成 string.Template —— 正确姿势 ────────────────────────
# Template(模板字符串)：包装出模板对象，识别 $名字 形式的占位符，花括号原样保留。
#   .substitute(mapping)：mapping 传一个 dict，逐项替换。
#       也可以写成 .substitute(**values)，效果相同。
#       有变量没提供 → 直接报 KeyError（严格模式，适合"必须填全"的模板）。
#   .safe_substitute(...)：同上，但缺变量时不报错、原样留着（适合先搭骨架）。
# 注意：模板里如果要写**字面的美元符号**，必须写成 $$，否则会被当成占位符开头。
final_prompt = Template(tpl_text).substitute(values)

print("[Template  ] 渲染成功，最终 prompt：")
print("-" * 50)
print(final_prompt)
print("-" * 50)
