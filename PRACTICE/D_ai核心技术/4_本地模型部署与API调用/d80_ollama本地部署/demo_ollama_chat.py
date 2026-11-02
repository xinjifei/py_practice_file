# 运行前：先用命令 `ollama pull qwen2.5:0.5b` 下载这个示例模型，并确认 Ollama 服务已启动。
import ollama  # 导入 ollama Python 客户端；它把请求发给本机的 Ollama 服务，而不是云端 API。

# 调用 chat() 发起一次对话：
# - model：本机已经下载的模型标签；换模型时必须与 `ollama list` 中的名称一致。
# - messages：按聊天顺序组成的消息列表；每条消息都用 role 标明说话者、用 content 放文本。
reply = ollama.chat(
    model="qwen2.5:0.5b",  # 使用与练习不同的小模型标签，避免把 demo 当成练习答案。
    messages=[
        {"role": "user", "content": "用一句话解释为什么雨后会有彩虹。"},  # 这是发送给本地模型的用户消息。
    ],
)

# reply 是服务返回的字典；其中 message 是回复消息，content 是模型生成的纯文本。
print(reply["message"]["content"])  # 只打印回复正文，便于确认“Python 客户端 → 本机服务 → 模型”的链路打通。
