"""最小的「无 RAG / 有 RAG」对照测试。

本例为了只学习对照和引用验证，直接使用已经召回的 r01_春风动力#000，
不重复搭建向量库。运行前：
    export DEEPSEEK_API_KEY=你的_key
    uv run python "PRACTICE/D_ai核心技术/3_rag/d78_rag问答系统/compare_cfmoto_rag.py"
"""

import json
import os
from pathlib import Path

from openai import OpenAI


QUESTION = "春风动力 2026 年前三季度营收和归母净利润是多少？"
CHUNK_ID = "r01_春风动力#000"
CHUNKS_PATH = (
    Path(__file__).resolve().parent.parent
    / "d77_研报知识库/RAG/output/chunks.jsonl"
)


def load_retrieved_chunk() -> dict:
    """本例把 d77 已验证的命中块当作「已召回结果」。"""
    with CHUNKS_PATH.open(encoding="utf-8") as file:
        for line in file:
            chunk = json.loads(line)
            if chunk["id"] == CHUNK_ID:
                return chunk
    raise ValueError(f"未找到 {CHUNK_ID}：{CHUNKS_PATH}")


def ask(client: OpenAI, messages: list[dict[str, str]]) -> str:
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


def main() -> None:
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise SystemExit("请先设置 DEEPSEEK_API_KEY，再运行此脚本。")

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    chunk = load_retrieved_chunk()

    without_rag = ask(client, [{"role": "user", "content": QUESTION}])
    with_rag = ask(client, [
        {"role": "system", "content": "只依据资料回答；资料外不要编造。每个数字结论后标注 [1]。"},
        {"role": "user", "content": f"[1] 资料：\n{chunk['text']}\n\n问题：{QUESTION}"},
    ])

    print("[无 RAG]（直接问模型）\n", without_rag)
    print("\n[有 RAG]（给已召回的 chunk）\n", with_rag)
    print("\n[引用核对] [1] 由代码从 metadata 映射：")
    print(f"  id={chunk['id']}，source={chunk['source']}，"
          f"chunk_index={chunk['chunk_index']}，页码={chunk['page_start']}-{chunk['page_end']}")
    print(f"  原文：{chunk['text']}")
    print("\n核对方法：检查答案中的 [1]，再逐字核对其后的原文是否包含两个数字。")


if __name__ == "__main__":
    main()
