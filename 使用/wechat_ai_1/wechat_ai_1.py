# 导入wxpy核心依赖
from wxpy import *
import requests
import time

# ========== 配置项 ==========
# Ollama API地址（保持默认即可）
OLLAMA_API_URL = "http://localhost:11434/api/generate"
# 要使用的Ollama模型名（根据你的本地模型修改）
MODEL_NAME = "llama3.2:3b"
# 自动回复模板（可自定义）
PROMPT_TEMPLATE = """
你是专业的电商客服，仅按以下规则回复：
1. 仅回答发货/售后/人工客服相关问题，其他回复「抱歉，我暂时无法解答」；
2. 回复≤20字，不扩展、不反问；
3. 问答库：
   - 发货：48小时内发货，江浙沪1-2天到
   - 售后：7天无理由退换，商家承担运费
   - 人工客服：400-123-4567（9:00-18:00）
用户问题：{user_msg}
"""


# ========== 调用Ollama生成智能回复 ==========
def get_ollama_reply(user_msg):
    # 拼接提示词
    prompt = PROMPT_TEMPLATE.format(user_msg=user_msg.strip())
    try:
        # 调用Ollama API
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,  # 关闭流式输出，直接获取结果
                "temperature": 0.1  # 低随机性，回复更稳定
            },
            timeout=30  # 超时时间30秒
        )
        response.raise_for_status()  # 抛出HTTP错误
        result = response.json()
        # 返回清洗后的回复内容
        return result.get("response", "抱歉，我暂时无法解答").strip()
    except Exception as e:
        # 异常时返回兜底回复
        print(f"Ollama调用失败：{str(e)}")
        return "抱歉，暂时无法回复，请稍后再试"


# ========== 初始化微信机器人 ==========
if __name__ == "__main__":
    # 1. 初始化机器人（扫码登录，hotReload=True保留登录状态）
    print("🔍 正在启动微信，请扫码登录...")
    bot = Bot(
        cache_path=True,  # 保留登录缓存，无需重复扫码
        console_qr=1  # 终端显示二维码（1=普通显示，2=反色显示）
    )
    print("✅ 微信登录成功！")


    # 2. 注册消息监听（仅监听好友文本消息）
    @bot.register(chats=Friend, msg_types=TEXT)
    def auto_reply(msg):
        # 排除自己发送的消息
        if not msg.self:
            user_msg = msg.text
            print(f"\n📩 收到[{msg.sender.name}]的消息：{user_msg}")

            # 调用Ollama生成回复（若无需智能回复，可直接写固定内容）
            reply = get_ollama_reply(user_msg)
            # 也可以用固定回复：reply = f"自动回复：{user_msg}"

            print(f"💬 回复[{msg.sender.name}]：{reply}")
            # 发送回复（加1秒延迟避免风控）
            time.sleep(1)
            return reply


    # 3. 保持机器人运行
    print("\n🤖 微信自动回复机器人已启动，按Ctrl+C退出...")
    bot.join()