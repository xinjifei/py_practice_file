"""
demo_rag_ask.py —— 最小可运行的 RAG 问答：检索 → 拼 Prompt → 生成 → 带引用

今天的练习是在你自己的研报库上实现 rag_ask(question)；
这个 demo 故意换成「咖啡机说明书 + 保修条款 + 配送说明」三份小文档，
问题也换成客服场景——看的是「四步怎么接起来」，数据换成你自己的。

四步一一对应下面的函数：
    1. 问题 Embedding      model.embed([question])        → 查询向量
    2. 向量检索 top-k       collection.query(...)          → 相关 chunk + metadata
    3. 拼 Prompt           build_context(...) + messages  → 带编号的资料 + 问题
    4. LLM 生成            client.chat.completions.create → 带 [编号] 的答案

运行（在项目根目录 ~/stu/py_practice_file 下）：
    export DEEPSEEK_API_KEY=你的key
    uv run python "PRACTICE/D_ai核心技术/3_rag/d78_rag问答系统/demo_rag_ask.py"

没有 DEEPSEEK_API_KEY 也能把前半段跑完（建库 + 检索），只是最后生成一步会跳过。
"""

import os                       # 读环境变量里的 API key
from pathlib import Path        # 以脚本所在目录为基准定位数据库目录

import chromadb                 # 向量数据库（d75 起就在用）
from fastembed import TextEmbedding   # 本地 embedding 模型，和 d77 用的是同一个
from openai import OpenAI       # DeepSeek 兼容 OpenAI 的调用格式（d68 起就在用）

# ── 参数区：改这里就能做对比实验 ─────────────────────────
CHUNK_SIZE = 150                # 每块最多多少个字（今天不是重点，够用就行）
COLLECTION_NAME = "faq_demo_d78"
DB_PATH = Path(__file__).resolve().parent / "demo_chroma_db"
EMBED_MODEL = "BAAI/bge-small-zh-v1.5"   # 中文语料；首次运行自动下载约 90MB
LLM_MODEL = "deepseek-v4-flash"          # 和 d70~d73 用的同一个模型
TOP_K = 3                       # 检索返回前几条；K 太小漏答案，太大塞噪声

# ── 0. 原始文档：三份互不重叠的资料 ───────────────────────
RAW_DOCS = {
    "coffee_manual": """青禾全自动咖啡机使用说明

水箱容量为 1.8 升，加满一次约可制作 12 杯意式浓缩。
水箱清洗：可取下后用温水手洗，切勿放入洗碗机，高温水流会使底部密封圈变形。
机器建议每制作 50 杯或每两周除垢一次，除垢剂按 1:10 兑水使用。""",

    "warranty": """产品保修条款

整机保修期为 2 年，自签收之日起计算。
核心部件（水泵、加热模块、控制主板）保修期为 3 年。
以下情况不在保修范围内：人为摔碰、进水、未按说明书清洗保养导致的故障。
申请保修需提供订单号与故障照片。""",

    "shipping": """配送与签收说明

现货订单在付款后 48 小时内发出，偏远地区物流约需 5 至 7 天。
运输过程中出现破损，请在签收后 48 小时内拍照并联系客服报备，逾期不予受理。
支持指定工作日送货，需在订单备注中说明。""",
}


# ── 1. 分块：按段落切，超长再硬切（d76 的简化版，今天够用）──
def split_chunks(text: str, size: int = CHUNK_SIZE) -> list[str]:
    """输入一段纯文本，输出若干不超过 size 字的块。"""
    chunks = []
    for para in text.split("\n\n"):          # 空行是段落分隔（我们的文档约定这么写）
        para = para.strip()
        if not para:
            continue
        while len(para) > size:              # 段落还超长就硬切，不搞重叠了，demo 从简
            chunks.append(para[:size])
            para = para[size:]
        if para:
            chunks.append(para)
    return chunks


# ── 2. 建库：分块 → 向量化 → 入库（和 d77 一样，只是规模小）──
def build_collection(model: TextEmbedding):
    ids, texts, metadatas = [], [], []
    for doc_id, raw in RAW_DOCS.items():
        for index, chunk in enumerate(split_chunks(raw)):
            ids.append(f"{doc_id}#{index}")   # 全局唯一：文档名#块号
            texts.append(chunk)               # 原文要存，检索后要拿回来喂给模型
            metadatas.append({"source": doc_id, "chunk_index": index})
            # metadata 不进相似度计算，但会跟着检索结果一起返回——
            # 今天的「来源引用」就是从这里取的，不是模型自己猜的

    embeddings = [v.tolist() for v in model.embed(texts)]   # 生成器 → 普通列表

    client = chromadb.PersistentClient(path=str(DB_PATH))
    try:
        client.delete_collection(COLLECTION_NAME)   # 每次重建，避免新旧块混在一起
    except Exception:
        pass
    collection = client.create_collection(COLLECTION_NAME)
    collection.add(ids=ids, documents=texts,
                   embeddings=embeddings, metadatas=metadatas)
    print(f"[建库] {len(texts)} 个 chunk 入库")
    return collection


# ── 3. 把检索结果拼成「带编号的资料」────────────────────
def build_context(result: dict) -> str:
    """输入 collection.query() 的返回值，输出喂给模型的资料文本。"""
    blocks = []
    # query 的结果按「查询」分组，这里只有一个查询，所以取 [0]
    for i, (doc, meta) in enumerate(
            zip(result["documents"][0], result["metadatas"][0]), start=1):
        # 编号 [1][2][3] 让模型能在答案里引用；source#index 让人能回原文核对
        blocks.append(f"[{i}] 来源：{meta['source']}#{meta['chunk_index']}\n{doc}")
    return "\n\n".join(blocks)


# ── 4. RAG 主函数：问题 → 检索 → 拼 Prompt → 生成 ────────
SYSTEM_PROMPT = (
    "你是一个严谨的客服助理。只依据【参考资料】回答问题；"
    "资料里没有的信息就说「资料中没有提到」，不要编造。"
    "每条结论后面用 [编号] 标注它来自哪条资料。"
)


def rag_ask(question: str, collection, model: TextEmbedding, top_k: int = TOP_K) -> dict:
    # 第 1 步：问题也要向量化，而且必须和建库用同一个模型——
    # 不同模型的向量空间不能互相比，距离会失去意义
    query_vector = [v.tolist() for v in model.embed([question])]

    # 第 2 步：检索 top-k
    #   query_embeddings → 查询向量，列表套列表（支持一次问多个问题）
    #   n_results        → 返回几条，也就是 K
    #   include          → 结果里要带哪些字段：原文、metadata、距离
    result = collection.query(
        query_embeddings=query_vector,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    # 第 3 步：拼 Prompt——资料在前，问题在后，并明确要求标引用
    context = build_context(result)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"【参考资料】\n{context}\n\n【问题】\n{question}"},
    ]

    # 第 4 步：生成
    #   model       → 模型名
    #   messages    → 对话列表；system 定规则，user 装资料和问题
    #   temperature → 0.1 表示尽量贴着资料说，减少自由发挥（RAG 场景通常调低）
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=0.1,
    )
    answer = resp.choices[0].message.content

    # 来源列表：直接取自检索结果的 metadata，而不是解析模型答案里写了什么——
    # 模型的 [编号] 只是文字，真正可信的是这份由代码生成、可回查的清单
    sources = []
    for doc, meta, dist in zip(
            result["documents"][0], result["metadatas"][0], result["distances"][0]):
        sources.append({
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": round(dist, 4),
            "excerpt": doc[:50].replace("\n", " ") + ("…" if len(doc) > 50 else ""),
        })
    return {"answer": answer, "sources": sources}


# ── 5. 对照组：同一个问题，不给任何资料 ─────────────────
def ask_without_rag(question: str) -> str:
    """不检索、不塞资料，直接问模型——用来对比「小抄」到底起了多大作用。"""
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "你是一个简洁的客服助理。"},
            {"role": "user", "content": question},
        ],
        temperature=0.1,
    )
    return resp.choices[0].message.content


# ── 6. 跑一遍：建库 → 检索 → 回答 → 并排打印 ──────────────
if __name__ == "__main__":
    print("[加载 embedding 模型] 首次运行会下载模型…")
    embed_model = TextEmbedding(model_name=EMBED_MODEL)   # 模型对象后面两处都要用
    collection = build_collection(embed_model)

    question = "咖啡机的水箱能放进洗碗机洗吗？保修期是几年？"

    print(f"\n{'=' * 60}\n问题：{question}\n{'=' * 60}")

    # 先看检索到了什么——这一步是在验收「小抄挑得对不对」
    hits = collection.query(
        query_embeddings=[v.tolist() for v in embed_model.embed([question])],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )
    print("\n[检索结果]")
    for i, (meta, dist) in enumerate(zip(hits["metadatas"][0], hits["distances"][0]), 1):
        print(f"  {i}. {meta['source']}#{meta['chunk_index']}  距离={dist:.4f}")

    # 没有 API key 时，到此为止；有 key 才继续做生成和对比
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("\n[跳过生成] 没有设置 DEEPSEEK_API_KEY")
        print("   设置方法：export DEEPSEEK_API_KEY=你的key，然后重跑")
    else:
        # client 放在这里初始化：前面检索不需要网络，没 key 也能跑
        client = OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],   # 从环境变量读，不写死在代码里
            base_url="https://api.deepseek.com",     # DeepSeek 的固定地址
        )

        print(f"\n{'─' * 60}\n[无 RAG · 直接问模型]\n{'─' * 60}")
        print(ask_without_rag(question))

        print(f"\n{'─' * 60}\n[有 RAG · 先检索再回答]\n{'─' * 60}")
        result = rag_ask(question, collection, embed_model)
        print(result["answer"])

        print(f"\n{'─' * 60}\n[来源清单 · 由代码从 metadata 生成，可回原文核对]\n{'─' * 60}")
        for i, src in enumerate(result["sources"], 1):
            print(f"  [{i}] {src['source']}#{src['chunk_index']}  "
                  f"距离={src['distance']}  {src['excerpt']}")
        print("\n核对思路：把答案里每个 [编号] 对回上面的来源清单，再翻原文看那段话"
              "是不是真的支持这个结论——模型写的 [编号] 可能错位，清单不会。")
