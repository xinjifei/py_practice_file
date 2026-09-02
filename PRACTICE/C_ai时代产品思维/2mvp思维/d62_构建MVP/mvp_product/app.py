"""Flask 入口：两条路由——/ 单源总结，/compare 双源对比。"""
import markdown
from flask import Flask, render_template

import config
from services import ai, news

app = Flask(__name__)


def _no_key():
    return "还没填 DEEPSEEK_API_KEY：打开项目根目录的 .env 文件，在等号右边粘贴你的 key。", 500


def _md(text: str) -> str:
    """把 AI 返回的 markdown 渲染成 HTML。"""
    return markdown.markdown(text, extensions=["sane_lists", "fenced_code", "tables"])


@app.route("/")
def index():
    if not config.DEEPSEEK_API_KEY:
        return _no_key()

    articles = news.fetch_articles(config.RSS_URL, config.MAX_ITEMS)
    summary = ai.summarize(
        articles,
        config.DEEPSEEK_API_KEY,
        config.MODEL,
        config.DEEPSEEK_BASE_URL,
    )
    return render_template("index.html", articles=articles, summary=_md(summary))


@app.route("/compare")
def compare():
    if not config.DEEPSEEK_API_KEY:
        return _no_key()

    left = news.fetch_articles(config.SOURCE_LEFT_URL, config.MAX_ITEMS)
    right = news.fetch_articles(config.SOURCE_RIGHT_URL, config.MAX_ITEMS)
    result = ai.compare(
        config.SOURCE_LEFT_NAME, left,
        config.SOURCE_RIGHT_NAME, right,
        config.DEEPSEEK_API_KEY,
        config.MODEL,
        config.DEEPSEEK_BASE_URL,
    )
    return render_template(
        "compare.html",
        left_name=config.SOURCE_LEFT_NAME, left=left,
        right_name=config.SOURCE_RIGHT_NAME, right=right,
        result=_md(result),
    )


if __name__ == "__main__":
    app.run(debug=True)
