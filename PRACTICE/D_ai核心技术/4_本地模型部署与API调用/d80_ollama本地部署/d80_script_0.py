# 脚本运行大模型最简闭环
import ollama

result = ollama.chat(
    model = "gemma3:1b",
    messages=[
        {"role": "user", "content": "introduce ur self"}
    ]
)

print(f"result = {result['message']['content']}")