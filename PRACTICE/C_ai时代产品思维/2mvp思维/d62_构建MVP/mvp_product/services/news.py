"""抓取 RSS 信息源，解析成干净的标题 + 链接 + 摘要。"""
import feedparser


def fetch_articles(feed_url: str, max_items: int = 12) -> list[dict]:
    """抓一个 RSS/Atom 源，返回前 max_items 条 {title, link, summary}。"""
    feed = feedparser.parse(feed_url)

    articles = []
    for entry in feed.entries[:max_items]:
        summary = entry.get("summary") or entry.get("description") or ""
        articles.append({
            "title": (entry.get("title") or "").strip(),
            "link": entry.get("link") or "",
            "summary": summary.strip(),
        })
    return articles
