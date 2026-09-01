from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

# 加载训练后的模型和分词器
model_path = "D:\\gpt2_model"  # 训练后模型的保存路径
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)
model.eval()  # 切换到推理模式，关闭训练时的随机因素

# 设置对话参数（可根据需要调整）
max_response_length = 100  # 生成回答的最大长度
temperature = 0.7  # 控制生成的随机性（0-1之间，值越小回答越确定）
no_repeat_ngram_size = 2  # 避免连续重复的短语

print("已加载训练后的模型，可以开始对话了（输入'退出'结束对话）")

while True:
    # 获取用户输入
    user_input = input("你: ")

    # 退出条件
    if user_input == "退出":
        print("对话结束")
        break

    # 构造输入文本（可以根据你的语料格式添加前缀，比如"问：...答："）
    prompt = f"问：{user_input} 答："  # 如果你的语料是问答格式，这样更匹配

    # 编码输入文本
    inputs = tokenizer(prompt, return_tensors="pt")

    # 生成模型回答
    with torch.no_grad():  # 关闭梯度计算，节省资源
        outputs = model.generate(
            **inputs,
            max_length=len(inputs["input_ids"][0]) + max_response_length,
            temperature=temperature,
            no_repeat_ngram_size=no_repeat_ngram_size,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True  # 开启采样，让回答更灵活
        )

    # 解码生成的文本并提取回答部分
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # 提取"答："后面的内容作为模型回答
    if "答：" in full_response:
        model_response = full_response.split("答：")[1].strip()
    else:
        model_response = full_response.split(prompt)[1].strip()

    print(f"模型: {model_response}")