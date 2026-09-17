import os
from openai import OpenAI

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

content = None
model_output = ""
while True:
    usr_input = "user_input:" + input("send massage\n>>>") + "|"

    if content == None:
        content = usr_input
    content += model_output + usr_input
    model_output ="model_output:" +  ask(content) + "|"

    print(content)
    print("\ndeepseek:",model_output,"\n")
    