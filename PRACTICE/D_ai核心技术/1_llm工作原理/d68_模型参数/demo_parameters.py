# demo_parameters.py —— 参考脚手架：用 DeepSeek API 演示 temperature / top_p 如何改变输出
# ⚠️ 演示 prompt 用「描述下雨的夜晚」，你练习时换成你自己的 prompt——思路一样，prompt 不同。
#

import os
from openai import OpenAI

print("复习防失忆==========需要在当前终端中创建临时环境变量：")
print("$env:DEEPSEEK_API_KEY = '<deepseek api key>'")

# 1. 建客户端：把 openai 库指向 DeepSeek 的服务器
#    DeepSeek 的接口兼容 OpenAI 协议，所以换个 base_url 就能复用 openai 库。
#    参数 api_key：从环境变量 DEEPSEEK_API_KEY 读（不写死在代码里，避免泄露进 git）
#    参数 base_url：DeepSeek 的固定地址 https://api.deepseek.com
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def ask(prompt, temperature=None, top_p=None):
    """把同一个 prompt 发给模型，返回模型回复的文本。"""
    resp = client.chat.completions.create(
        model="deepseek-v4-flash",          # DeepSeek 的对话模型名
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,        # None = 用模型默认值
        top_p=top_p,                    # None = 用模型默认值
    )
    return resp.choices[0].message.content


prompt = "用一句话描述下雨天"

# 2. Temperature：创造性 vs 确定性
#    temperature=0 死板确定，每次结果一样；越大越天马行空，每次不一样。
#    看「跑 3 次会不会一模一样」就能直接感受差别。
for t in [0.0, 0.7, 1.5]:
    print(f"\n=== temperature = {t} ===")
    for i in range(3):
        print(f"  第{i+1}次: {ask(prompt, temperature=t)}")

# 3. Top-P：另一种控制随机性的旋钮（核采样）
#    和 temperature 作用类似，都是控制"输出多随机"，所以通常只调其中一个。
for p in [0.1, 0.9]:
    print(f"\n=== top_p = {p}（temperature 固定 0.7）===")
    for i in range(3):
        print(f"  第{i+1}次: {ask(prompt, temperature=0.7, top_p=p)}")
