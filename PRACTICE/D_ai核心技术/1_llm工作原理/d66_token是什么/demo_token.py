# demo_token.py —— 参考脚手架：tiktoken 统计 token 的核心逻辑
# ⚠️ 数据与你的练习不同：练习用金融研报，这里用短句子，让你先看懂思路、再自己动手跑研报

import tiktoken


# 1. 加载 tokenizer（分词器）
#    tiktoken.get_encoding(name) 按名字加载一个内置编码
#    参数 name：编码名。常见两个：
#       "cl100k_base" —— GPT-3.5 / GPT-4 用的
#       "o200k_base"  —— GPT-4o 及之后的模型用的
#    返回 Encoding 对象，负责「文本 <-> token」的双向转换
enc = tiktoken.get_encoding("cl100k_base")


# 2. encode()：把字符串切成 token 列表
#    参数 text：要切分的文本（str）
#    返回 List[int]：每个 token 的数字 id —— 模型真正"读到"的就是这一串数字，不是汉字
text = "量化交易的核心是概率。"
tokens = enc.encode(text)
print("原文：", text)
print("token 列表：", tokens)
print("token 数量：", len(tokens))
print("字符数：", len(text))
print("字符/token 比例：", round(len(text) / len(tokens), 2))
# 关键观察：字符数 ≠ token 数。一个中文词可能被切成 1~3 个 token


# 3. decode()：把 token 列表还原成字符串（encode 的逆操作）
#    参数 tokens：List[int]
#    返回 str：还原后的文本
restored = enc.decode(tokens)
print("还原文本：", restored)


# 4. 对比不同 tokenizer 对同一文本的 token 数
#    同一个词，在不同 tokenizer 下可能被切成不同数量的 token
enc_old = tiktoken.get_encoding("cl100k_base")
enc_new = tiktoken.get_encoding("o200k_base")
print(f"cl100k_base: {len(enc_old.encode(text))} tokens")
print(f"o200k_base:  {len(enc_new.encode(text))} tokens")


# 5. 中英对比：表达同样的意思，英文 token 通常更省
#    这是理解「为什么中文用 LLM 更费 token（更贵/更慢）」的入口
text_en = "Quantitative trading is about probability."
text_cn = "量化交易的核心是概率。"
print("英文：", len(text_en), "字符 →", len(enc.encode(text_en)), "tokens")
print("中文：", len(text_cn), "字符 →", len(enc.encode(text_cn)), "tokens")
