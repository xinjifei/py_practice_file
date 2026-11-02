"""
demo_rag_robust.py —— 复习日参考：给 RAG 加「出错不崩」的骨架 + chunk 级质量检查

昨天的 demo 演示了「顺利地走完四步」；今天这个 demo 演示另一面：
检索空了怎么办、LLM 报错怎么办、模型引用了不存在的编号怎么发现。
数据沿用「与练习不同」的原则：这里用相机说明 / 镜头保修 / 会员服务三份小文档，
练习请换成你自己的研报库。

三个部分：
    1. retrieve()        检索只是一个函数，可以独立测试、独立返回空列表
    2. rag_ask()         任何一步失败都返回结构化状态，而不是抛异常到用户脸上
    3. chunk_level_report()  判据细到 chunk：答案所在的那一块排第几

运行（在项目根目录 ~/stu/py_practice_file 下）：
    export DEEPSEEK_API_KEY=你的key
    uv run python "PRACTICE/D_ai核心技术/3_rag/d79_rag复盘/demo_rag_robust.py"

没有 API key 时：检索、chunk 级检查、空检索分支照常演示，生成分支会跳过。
"""

import os
import re
from pathlib import Path

import chromadb
from fastembed import TextEmbedding
from openai import OpenAI

CHUNK_SIZE = 120
COLLECTION_NAME = "camera_demo_d79"
DB_PATH = Path(__file__).resolve().parent / "demo_chroma_db"
EMBED_MODEL = "BAAI/bge-small-zh-v1.5"
LLM_MODEL = "deepseek-v4-flash"
TOP_K = 3

# ── 0. 三份小文档（和练习的研报库完全无关）────────────────
RAW_DOCS = {
    "camera_manual": """星野 X100 微单说明书

电池型号为 BP-X100，满电约可拍摄 320 张照片（CIPA 标准）。
支持 USB-C 充电，但不支持边充边拍，充电时相机会自动关机。
传感器为 2420 万像素 APS-C 画幅，机身重量 380 克。""",

    "lens_warranty": """镜头保修条款

镜头保修期为 18 个月，自签收之日起计算，需在官网完成产品注册。
人为进灰、摔落、进水导致的损坏不在保修范围内。
保修需提供订单号和注册成功的截图。""",

    "membership": """会员服务说明

会员每年可享受 2 次免费传感器清洁服务，需提前 3 天在 App 内预约。
清洁服务仅限机身，不含镜头内部除尘。
会员卡遗失不补，请妥善保管。""",
}


# ── 1. 建库（和 d78 demo 一样，规模小；复习日不折腾切块）──
def split_chunks(text: str, size: int = CHUNK_SIZE) -> list[str]:
    chunks = []
    for para in text.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        while len(para) > size:
            chunks.append(para[:size])
            para = para[size:]
        if para:
            chunks.append(para)
    return chunks


def build_collection(model: TextEmbedding):
    ids, texts, metadatas = [], [], []
    for doc_id, raw in RAW_DOCS.items():
        for index, chunk in enumerate(split_chunks(raw)):
            ids.append(f"{doc_id}#{index}")
            texts.append(chunk)
            # metadata 是今天「引用可追溯」的地基：source + chunk_index 缺一不可
            metadatas.append({"source": doc_id, "chunk_index": index})

    embeddings = [v.tolist() for v in model.embed(texts)]
    client = chromadb.PersistentClient(path=str(DB_PATH))
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(COLLECTION_NAME)
    collection.add(ids=ids, documents=texts,
                   embeddings=embeddings, metadatas=metadatas)
    print(f"[建库] {len(texts)} 个 chunk")
    return collection


# ── 2. 检索：独立函数，失败返回空列表而不是崩 ─────────────
def retrieve(question: str, collection, model: TextEmbedding, top_k: int = TOP_K) -> list[dict]:
    """输入问题，输出命中列表；任何一步出问题都返回 []，由调用方决定怎么处理。"""
    if collection.count() == 0:          # 库是空的，再查也没有意义
        return []
    try:
        # 查询向量必须和建库用同一个 embedding 模型，否则距离没有意义
        query_vector = [v.tolist() for v in model.embed([question])]
        result = collection.query(
            query_embeddings=query_vector,
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
    except Exception as exc:             # 数据库损坏、维度不匹配等，统一降级成「没检索到」
        print(f"  [retrieve 异常] {exc}")
        return []

    hits = []
    # query 的结果按查询分组，[0] 是第一个（也是唯一一个）查询
    for doc, meta, dist in zip(
            result["documents"][0], result["metadatas"][0], result["distances"][0]):
        hits.append({
            "id": f"{meta['source']}#{meta['chunk_index']}",
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "text": doc,
            "distance": dist,
        })
    return hits


# ── 3. 拼 context：编号 + 来源，模型能引用、人能回查 ────────
def build_context(hits: list[dict]) -> str:
    blocks = []
    for i, hit in enumerate(hits, start=1):
        blocks.append(f"[{i}] 来源：{hit['id']}\n{hit['text']}")
    return "\n\n".join(blocks)


SYSTEM_PROMPT = (
    "你是一个严谨的客服助理。只依据【参考资料】回答；"
    "资料里没有就说「资料中没有提到」，不要编造。每个结论后用 [编号] 标注来源。"
)


# ── 4. 检查引用：答案里的编号是否都真的存在 ────────────────
def check_citations(answer: str, sources: list[dict]) -> list[int]:
    """输入答案和来源清单，输出「答案里引用了、但清单里不存在」的编号列表。"""
    used = {int(n) for n in re.findall(r"\[(\d+)\]", answer)}   # 正则取出所有 [数字]
    valid = set(range(1, len(sources) + 1))                     # 清单里合法的编号
    return sorted(used - valid)                                 # 差集就是越界引用


# ── 5. rag_ask：把失败也当成一种正常返回值 ─────────────────
def rag_ask(question: str, collection, model: TextEmbedding, client,
            top_k: int = TOP_K, simulate_llm_error: bool = False) -> dict:
    """返回结构固定为 {status, answer, sources, message, bad_citations}。

    status 的三种取值就是今天的失败清单：
      no_hit    → 检索为空，问题该去查知识库/切块，而不是怪模型
      llm_error → 模型调用失败（超时/网络/key），问题在外部服务
      ok        → 正常返回；bad_citations 非空说明模型编了引用
    """
    hits = retrieve(question, collection, model, top_k)
    if not hits:                                          # ① 检索为空
        return {"status": "no_hit", "answer": "",
                "sources": [], "message": "没有检索到相关资料，请换个问法或补充文档",
                "bad_citations": []}

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"【参考资料】\n{build_context(hits)}\n\n【问题】\n{question}"},
    ]

    try:
        if simulate_llm_error:                            # 演示用：人为制造一次失败
            raise TimeoutError("模拟：LLM 调用超时")
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0.1,
        )
        answer = response.choices[0].message.content
    except Exception as exc:                              # ② LLM 超时/报错
        return {"status": "llm_error", "answer": "",
                "sources": hits, "message": f"模型调用失败：{exc}",
                "bad_citations": []}

    # 来源清单始终由代码从 metadata 生成——不解析模型说了什么
    sources = [{"id": h["id"], "source": h["source"],
                "chunk_index": h["chunk_index"],
                "distance": round(h["distance"], 4)} for h in hits]

    # ③ 引用越界：答案里出现的 [编号] 必须能在清单里找到
    bad = check_citations(answer, sources)
    return {"status": "ok", "answer": answer, "sources": sources,
            "message": "答案中引用了不存在的来源编号" if bad else "",
            "bad_citations": bad}


# ── 6. chunk 级质量检查：答案那一块到底排第几 ──────────────
# 每个用例写成 (问题, 答案应落在哪个 chunk) —— 这是你「先知道答案」的验证方式
CHECK_CASES = [
    ("X100 满电能拍多少张？", "camera_manual#0"),
    ("传感器清洁一年几次？", "membership#0"),
    ("镜头保修多久？", "lens_warranty#0"),
    ("相机支持边充边拍吗？", "camera_manual#1"),   # 答案被切到第二块，测切块边界
]


def chunk_level_report(collection, model: TextEmbedding) -> None:
    print("\n── chunk 级检索质量（判据：目标 chunk 在 top-k 里排第几）──")
    for question, expected_id in CHECK_CASES:
        hits = retrieve(question, collection, model)
        ids = [h["id"] for h in hits]
        if expected_id in ids:
            rank = ids.index(expected_id) + 1
            distance = hits[rank - 1]["distance"]
            print(f"  ✓ 第 {rank} 名  距离={distance:.4f}  {question}")
        else:
            print(f"  ✗ 未进 top-{TOP_K}  {question}（期望 {expected_id}，实际 {ids}）")


# ── 7. 跑一遍：正常 / 空检索 / 模型报错 三条分支 ───────────
if __name__ == "__main__":
    print("[加载 embedding 模型]")
    embed_model = TextEmbedding(model_name=EMBED_MODEL)
    collection = build_collection(embed_model)

    # 分支 A：正常情况，顺带看引用有没有越界
    client = None
    if os.environ.get("DEEPSEEK_API_KEY"):
        client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"],
                        base_url="https://api.deepseek.com")

    chunk_level_report(collection, embed_model)

    if client:
        question = "X100 的电池满电能拍多少张？传感器清洁一年几次？"
        result = rag_ask(question, collection, embed_model, client)
        print(f"\n[正常分支] status={result['status']}")
        print(result["answer"])
        print("来源：", [s["id"] for s in result["sources"]])
        print("越界引用：", result["bad_citations"] or "无")

        # 分支 B：模型调用失败（这里用 simulate_llm_error 人为触发）
        result = rag_ask(question, collection, embed_model, client,
                         simulate_llm_error=True)
        print(f"\n[LLM 失败分支] status={result['status']}  message={result['message']}")

    # 分支 C：空检索——用一个空 collection 模拟「知识库没建好/没命中」
    empty = chromadb.PersistentClient(path=str(DB_PATH)).create_collection("empty_demo_d79")
    result = rag_ask("无人机续航多久？", empty, embed_model, client)
    print(f"\n[空检索分支] status={result['status']}  message={result['message']}")

    print("\n注意：vector 检索默认总会返回 top-k 条，『空检索』在真实库里通常表现为"
          "「返回的都不相关」——所以还要靠距离阈值或 chunk 级检查来判失败。")
