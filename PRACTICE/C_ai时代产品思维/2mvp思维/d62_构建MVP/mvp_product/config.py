"""项目配置。换源、换模型、改条数，都在这一个文件里。"""
import os

from dotenv import load_dotenv

# 读取 .env 里的环境变量（key 放 .env，不进 git）
load_dotenv()

# ---- AI 配置（DeepSeek，OpenAI 兼容接口）----
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
# deepseek-chat = 通用对话模型；如果报"模型不存在 / model not found"，
# 把它改成 deepseek-v4-flash 再试（新账号可能已经弃用旧名）。
MODEL = "deepseek-chat"

# ---- 信息源配置 ----
# 改这一行就能换源。下面是实测能访问的：
#   https://feeds.npr.org/1001/rss.xml            NPR 新闻（默认，美国主流媒体）
#   https://sspai.com/feed                         少数派（中文科技）
#   https://www.ruanyifeng.com/blog/atom.xml       阮一峰博客（中文）
# 注：BBC 的 feed 在国内被墙（502），别用。
RSS_URL = "https://feeds.npr.org/1001/rss.xml"

# 每次抓多少条给 AI 总结
MAX_ITEMS = 12

# ---- 功能2：同题对比（两个立场相反的源）----
# 中左源
SOURCE_LEFT_NAME = "NPR"
SOURCE_LEFT_URL = "https://feeds.npr.org/1001/rss.xml"
# 右源（更极端的备选：https://www.breitbart.com/feed/）
SOURCE_RIGHT_NAME = "NY Post"
SOURCE_RIGHT_URL = "https://nypost.com/feed/"
