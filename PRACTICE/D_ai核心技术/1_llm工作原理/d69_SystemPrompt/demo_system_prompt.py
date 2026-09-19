# demo_system_prompt.py —— 参考脚手架：演示 system / user 两个 role 怎么分工
# ⚠️ 演示人设用「严格的代码审查员」，你练习时换成「A股量化研究员」——思路一样，人设不同。
#

import os
from openai import OpenAI

print("复习防失忆==========需要在当前终端中创建临时环境变量：")
print("$env:DEEPSEEK_API_KEY = '<deepseek api key>'")

# 1. 建客户端：和 d68 完全一样，openai 库指向 DeepSeek 服务器
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def ask(user_prompt, system_prompt=None):
    """发一次请求，返回模型回复的文本。

    参数 user_prompt：这次要做的具体任务（User Prompt，必给）
    参数 system_prompt：给模型立的人设/规矩（System Prompt，None = 不立）
    """
    # messages 是一个「对话列表」，每个元素是一个字典，字典有两个键：
    #   role    —— 谁说的话，三个取值：
    #              'system'    人设 / 规矩（设定舞台）
    #              'user'      你（指定任务）
    #              'assistant' 模型（模型自己说过的话）
    #   content —— 说的话本身（字符串）
    #
    # 关键点：system 必须放在列表最前面。顺序 = 优先级，改顺序模型理解就变了。
    messages = []
    if system_prompt is not None:              # 不传 system 时就不放这一条——这就是「无 System Prompt」
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})   # user 永远放最后，是"当前这一问"

    resp = client.chat.completions.create(
        model="deepseek-v4-flash",             # 和 d68 同一个模型
        messages=messages,                     # 把上面拼好的对话列表整发过去
    )
    # resp.choices[0] 取第 1 条候选回复；.message.content 取它的正文文本
    return resp.choices[0].message.content


# 2. 同一个 User Prompt —— 任务本身完全一样，一个字都不改
task = "帮我看看这段代码有没有问题：for i in range(10): print(i)"

# 3. 第一次：不给 System Prompt —— 模型用它出厂自带的默认人设回答
print("=== 没有 System Prompt ===")
print(ask(task))

# 4. 第二次：给一个「四要素」写全的 System Prompt —— 同一个任务，看风格怎么变
#    角色   ：你是一名严格的代码审查员
#    能力   ：你擅长发现边界条件、性能和可读性问题
#    边界   ：你不重写代码，只指出问题并说明原因          ← 最容易被漏的一条
#    输出格式：Markdown 有序列表，每条一行「问题 —— 原因」  ← 第二容易被漏的一条
system_prompt = """你是一名严格的代码审查员。
你擅长发现边界条件、性能和可读性问题。
你不重写代码，只指出问题并说明原因。
输出格式：用 Markdown 有序列表，每条一行，格式为「问题 —— 原因」。"""

print("\n=== 有 System Prompt ===")
print(ask(task, system_prompt=system_prompt))

# 5. 同一个人设 + 换一个 User Prompt —— 看风格是否稳定
#    这才是 System Prompt 的核心价值：任务换了，但回答的格式/角度/边界不变
print("\n=== 同一个人设，换一个任务 ===")
task2 = "帮我看看这段代码有没有问题：def f(x): return x[0]"
print(ask(task2, system_prompt=system_prompt))
print("↑ 注意：任务变了，但格式和边界没变——这就是 System Prompt 在「设定舞台」")
