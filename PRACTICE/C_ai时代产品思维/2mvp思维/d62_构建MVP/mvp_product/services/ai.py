"""调用 DeepSeek 模型：单源总结 + 双源对比。"""
import requests


def _chat(messages: list[dict], api_key: str, model: str, base_url: str) -> str:
    """底层的 DeepSeek 调用，总结和对比都走这里。"""
    resp = requests.post(
        f"{base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": messages,
            "temperature": 0.3,
            "stream": False,
        },
        timeout=90,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def summarize(articles: list[dict], api_key: str, model: str, base_url: str) -> str:
    """把文章标题拼成 prompt，总结成 3~5 个主题、各一句话。"""
    titles = "\n".join(f"- {a['title']}" for a in articles)
    prompt = (
        "以下是今天从一个信息源抓取的文章标题：\n"
        f"{titles}\n\n"
        "请用中文总结：这些信息主要围绕哪几个主题（3~5 个）？"
        "每个主题用一句话概括。只写总结，不要复述原文，不要编造原文没有的内容。"
    )
    messages = [
        {"role": "system", "content": "你是一个客观、克制的信息总结助手。"},
        {"role": "user", "content": prompt},
    ]
    return _chat(messages, api_key, model, base_url)


def compare(left_name: str, left_articles: list[dict],
            right_name: str, right_articles: list[dict],
            api_key: str, model: str, base_url: str) -> str:
    """对比两个源的报道角度，把茧房显形。"""
    left_titles = "\n".join(f"- {a['title']}" for a in left_articles)
    right_titles = "\n".join(f"- {a['title']}" for a in right_articles)

    prompt = (
        f"下面是两个立场不同的媒体今天各自的文章标题。\n\n"
        f"【{left_name}】\n{left_titles}\n\n"
        f"【{right_name}】\n{right_titles}\n\n"
        "请做三件事：\n"
        "1. 找出两边都涉及的话题（如有）。\n"
        "2. 对同一个话题，对比两边的报道角度：各自强调什么、忽略什么、用什么措辞。\n"
        "3. 如果两边几乎没有重叠话题，就直接指出：它们今天在讲完全不同的世界，"
        "这本身就是信息茧房的证据。\n\n"
        "用中文，简洁具体，尽量引用真实标题做例子，不要编造原文没有的内容。"
    )
    messages = [
        {"role": "system", "content": "你是一个客观、克制的信息对比助手。"},
        {"role": "user", "content": prompt},
    ]
    return _chat(messages, api_key, model, base_url)
