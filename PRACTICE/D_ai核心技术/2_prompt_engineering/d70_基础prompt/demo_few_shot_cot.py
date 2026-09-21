# demo_few_shot_cot.py —— 参考脚手架：Few-shot（用例子划格式）和 CoT（用中间步骤换准确率）
# ⚠️ 演示数据用「菜谱文本 → JSON」和「三家供应商比价」。
#    你练习时换成自己的文本和问题——思路一样，数据必须不同。
#

import os
import json
from openai import OpenAI

print("复习防失忆==========需要在当前终端中创建临时环境变量：")
print("$env:DEEPSEEK_API_KEY = '<deepseek api key>'")

# 1. 建客户端：和 d68 / d69 完全一样，openai 库指向 DeepSeek 服务器
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),   # 从环境变量读，不写死在代码里，避免泄露进 git
    base_url="https://api.deepseek.com",         # DeepSeek 的固定地址，换个 base_url 就复用了 openai 库
)


def ask(user_prompt):
    """把一段 prompt 发给模型，返回回复正文。

    参数 user_prompt：完整的一段话。今天不用 system——专心看 prompt 内部怎么设计。
    """
    resp = client.chat.completions.create(
        model="deepseek-v4-flash",                              # 和 d68 / d69 同一个模型
        messages=[{"role": "user", "content": user_prompt}],    # 单轮对话：列表里只有一条 user
        temperature=0,     # ★ 今天特意固定成 0。对比两种写法时，要排除随机性干扰——
                           #   否则你分不清「输出变了」是因为 prompt 变了，还是因为模型这次心情不同
    )
    return resp.choices[0].message.content    # choices[0] 取第 1 条候选回复，.message.content 取正文


# ============================================================
# 第一部分：Few-shot —— 例子不是在教知识，是在划格式
# ============================================================

# 2. 两段「输入 → 输出」的例子。仔细看：例子里没有一个字在解释"什么是菜谱"。
#    它只示范了「该用哪些字段、按什么结构来回答」。
#    模型从例子里学到的是格式，不是知识——这就是 Few-shot 的本质。
example_1_in = "番茄炒蛋。两个番茄切块，三个鸡蛋打散。先炒蛋盛出，再炒番茄，最后混一起加盐。"
example_1_out = '{"菜名": "番茄炒蛋", "食材": ["番茄", "鸡蛋"], "步骤数": 3, "难度": "简单"}'

example_2_in = "红烧肉。五花肉焯水，炒糖色，加酱油料酒炖一小时收汁。"
example_2_out = '{"菜名": "红烧肉", "食材": ["五花肉", "酱油", "料酒"], "步骤数": 4, "难度": "中等"}'

# 3. 第三段：这次不给答案，让模型照着上面的样子自己补
target = "紫菜蛋花汤。水烧开下紫菜，淋蛋液，加盐和香油，出锅。"

# 4. 0-shot 写法：只提要求，不给例子
prompt_0shot = f"""把下面这段菜谱转成 JSON：

{target}"""

# 5. 2-shot 写法：给两个例子，再让它处理第三个
#    结构正好是三段：指令（做什么）+ 例子（怎么做）+ 目标（现在轮到它）
prompt_2shot = f"""把菜谱文本转成 JSON。

例子1：
输入：{example_1_in}
输出：{example_1_out}

例子2：
输入：{example_2_in}
输出：{example_2_out}

现在处理这一段：
输入：{target}
输出："""

print("\n" + "=" * 50)
print("【0-shot】只说要 JSON，不给例子")
print("=" * 50)
out_0shot = ask(prompt_0shot)
print(out_0shot)

print("\n" + "=" * 50)
print("【2-shot】给两个例子，让它照着模仿")
print("=" * 50)
out_2shot = ask(prompt_2shot)
print(out_2shot)


# 6. 验货：这两次输出，程序能不能直接接住？
#    这才是「结构化输出」的意义——不是给人看着舒服，是给程序直接解析。
def strip_fence(text):
    """去掉模型爱加的 ``` 代码块标记，只留里面的内容。

    参数 text：模型返回的原始文本
    返回值  ：去掉首尾 ``` 之后的纯内容

    为什么要这一步：模型经常把 JSON 包在 Markdown 代码块里，
    直接扔给 json.loads 会报错。实际工程里这是必做的一步。
    """
    t = text.strip()                    # 去掉首尾空白（换行、空格）
    if t.startswith("```"):             # 开头是不是 ```
        t = t.split("\n", 1)[1]         #   split(分隔符, 最大分割次数)：
                                        #   按换行切一刀，最多切 1 次 → [第一行, 剩下的全部]
                                        #   [1] 取"剩下的全部"，就丢掉了 ```json 那一行
        t = t.rsplit("```", 1)[0]       #   rsplit 是「从右边往左切」，同样只切 1 次
                                        #   [0] 取"切剩下的前半段"，就丢掉了结尾的 ```
    return t.strip()


print("\n=== 两次输出能不能被程序直接解析？ ===")
for name, text in [("0-shot", out_0shot), ("2-shot", out_2shot)]:
    try:
        data = json.loads(strip_fence(text))     # json.loads：JSON 字符串 → Python 字典
        print(f"{name}：成功，解析出字段 {list(data.keys())}")
    except json.JSONDecodeError as e:            # 解析失败会抛这个异常，说明吐出来的不是合法 JSON
        print(f"{name}：失败 —— {e}")


# ============================================================
# 第二部分：CoT —— 把中间步骤先落到纸面上
# ============================================================

# 7. 一道需要多步计算的问题：三家各算一次总价，再比大小。
#    直接要答案，模型容易拍脑袋；让它写过程，正确率会明显不一样。
question = """三家供应商报价，要采购 1200 件，选哪家最便宜？
A：每件 12 元，满 1000 件打 8 折
B：每件 11 元，无折扣，另收运费 500 元
C：每件 13 元，含运费，满 500 件打 9 折"""

# 8. 直接要答案：不给它写过程的机会
prompt_direct = f"""{question}

直接告诉我选哪家，不要过程。"""

# 9. 加 CoT：注意这不是什么魔法咒语。
#    本质是「要求它把中间步骤写出来」——因为模型是逐 token 生成的，
#    先写下的字会变成后面生成时的上下文。写出来的过程 = 给它自己一块草稿纸。
prompt_cot = f"""{question}

让我们一步一步思考：先分别算出三家在 1200 件下的总价，列出算式，再比较大小，最后下结论。"""

print("\n" + "=" * 50)
print("【直接要答案】")
print("=" * 50)
print(ask(prompt_direct))

print("\n" + "=" * 50)
print("【加 CoT：让它先写过程】")
print("=" * 50)
print(ask(prompt_cot))

print("\n↑ 正确答案：A = 11520 元，B = 13700 元，C = 14040 元 → 选 A")
print("  对比两次输出：CoT 多花的 token 买到了什么？")
print("  反过来说——如果问题只是「把这句话翻译成英文」，CoT 就是纯浪费。")
