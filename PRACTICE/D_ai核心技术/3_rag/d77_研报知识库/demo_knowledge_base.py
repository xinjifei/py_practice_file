"""
demo_knowledge_base.py —— 一条最小的「知识库」流水线

今天的练习（取 ≥10 份研报 → 清洗 → 分块 → 向量化 → 入库 → 检索验证），
这个 demo 故意换成「3 篇带脏数据的产品说明」，chunk 大小 120 字。
数据量小到你能一眼看出每一步在干什么——看思路，数据换成你自己的。

⚠️ 为什么用 fastembed 不用 sentence-transformers：
   它的导入链会拉进 sklearn → scipy，这台机器上的 scipy 二进制与 macOS 不兼容。
   fastembed 走 ONNX 运行时，同时支持中文模型 bge-small-zh-v1.5（首次运行自动下载约 90MB）。

运行（在项目根目录 ~/stu/py_practice_file 下）：
    uv run python "PRACTICE/D_ai核心技术/3_rag/d77_研报知识库/demo_knowledge_base.py"
"""

import re                              # 正则：清洗文本、按句子切分都要用

import chromadb                        # 向量数据库本体
from fastembed import TextEmbedding    # 把文本变成向量（ONNX 运行时）

# 全局参数：分块大小（字）和相邻块的重叠（字）
CHUNK_SIZE = 120
OVERLAP = 20
COLLECTION_NAME = "kb_demo"            # Chroma 里的「表名」
DB_PATH = "./chroma_demo_db"           # 数据库目录；相对路径基于运行脚本时所在的目录

# ── 1. 原始文档：故意带脏数据 ─────────────────────────
# 真实 PDF/网页提取出来的文本就是这个样子：页眉页脚、多余空格、\r\n、连续空行。
# 练习时你的文档大概率比这个更脏（表格错位、断行、水印）。
RAW_DOCS = {
    # 每一条是一个文档：key 是文档编号（后面当 metadata 的 source 用）
    "manual_kettle": """第 1 页 / 共 2 页

  电热水壶使用说明

本产品额定功率 1800W，容量 1.7 升，采用 304 不锈钢内胆。
使用前请先加水至最低水位线，避免干烧。


第 2 页 / 共 2 页

清洁保养：断电并完全冷却后，用湿布擦拭外壳即可，内胆可用清水冲洗。
本产品不建议放入洗碗机清洗，高温水流会损坏底座密封圈。
""",
    "manual_earbuds": """第 1 页 / 共 2 页

  无线耳机快速指南

充满电约需 1.5 小时，单次续航 6 小时，配合充电盒总续航约 24 小时。
蓝牙有效连接距离为 10 米，超出后会先降音质再断开。


第 2 页 / 共 2 页

首次配对：长按充电盒按钮 3 秒进入配对模式，在手机蓝牙列表中选择设备名称。
若无法连接，请先在手机中删除旧配对记录后重试。
""",
    "policy_return": """第 1 页 / 共 1 页

  售后服务政策

自签收之日起 7 天内可无理由退货，商品需保持完好、不影响二次销售。
退换货时请保留原包装、赠品及全部配件，否则可能无法办理。
""",
}


# ── 2. 清洗：把提取出来的「脏文本」变成可切分的干净文本 ──
def clean_text(raw: str) -> str:
    """输入：解析器吐出来的原始文本。输出：去掉噪声、保留段落结构的文本。"""
    # re.sub(模式, 替换成什么, 原文)
    #   r"第\s*\d+\s*页\s*/\s*共\s*\d+\s*页" → 「第 1 页 / 共 2 页」这类页眉页脚
    #   \d+ 是一个及以上数字，\s* 是零个及以上空白（所以有没有空格都能匹配）
    text = re.sub(r"第\s*\d+\s*页\s*/\s*共\s*\d+\s*页", "", raw)
    # 统一换行符：Windows 导出的 \r\n、老式 Mac 的 \r，全变成 \n
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # 行内连续空格/制表符压成一个空格
    text = re.sub(r"[ \t]+", " ", text)
    # 三个以上连续换行压成两个——正好等于一个「段落分隔」，分块要靠它
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 每一行去掉首尾空白（PDF 提取经常带前导空格，不处理会影响长度统计）
    lines = [line.strip() for line in text.split("\n")]
    return "\n".join(lines).strip()


# ── 3. 分块：段落 → 句子 → 硬切，逐级降级 ──────────────
def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    """昨天（d76）的三种策略在这里合成一条：先按段落，段落超长再按句子，句子还超长硬切。"""
    assert overlap < size, "重叠必须小于块大小，否则会切不动"

    pieces = []                                  # 先拆成「不超过 size 的最小片段」
    for para in text.split("\n\n"):              # 第一层：段落
        para = para.strip()
        if not para:
            continue
        if len(para) <= size:
            pieces.append(para)
            continue
        # 第二层：按句末标点切句。(?<=[。！？]) 是「在 。！？ 之后切」的零宽断言
        for sentence in re.split(r"(?<=[。！？])", para):
            sentence = sentence.strip()
            if not sentence:
                continue
            # 第三层：句子还是太长，硬切；每切一段往回退 overlap 个字做重叠
            while len(sentence) > size:
                pieces.append(sentence[:size])
                sentence = sentence[size - overlap:]
            if sentence:
                pieces.append(sentence)

    # 把小片段合并到接近 size：碎成一堆小块会让上下文断裂
    chunks, buf = [], ""
    for piece in pieces:
        if len(buf) + len(piece) <= size:
            buf += piece
        else:
            if buf:
                chunks.append(buf)
            buf = piece
    if buf:
        chunks.append(buf)
    return chunks


# ── 4. 走完 清洗 → 分块 → 向量化 → 入库 ────────────────
def build_knowledge_base(raw_docs: dict):
    ids, texts, metadatas = [], [], []

    print("── 清洗 + 分块 ──")
    for doc_id, raw in raw_docs.items():
        clean = clean_text(raw)                          # 先洗
        chunks = chunk_text(clean)                       # 再切
        # 这一行是今天要自己盯的数：每份文档产出几块、块多长
        print(f"{doc_id:16s} 清洗后 {len(clean):4d} 字 → {len(chunks)} 块，块长 "
              f"{[len(c) for c in chunks]}")
        for index, chunk in enumerate(chunks):
            ids.append(f"{doc_id}#{index}")              # id 必须全局唯一：文档号#块号
            texts.append(chunk)                          # 存原文，检索后原样返回
            metadatas.append({"source": doc_id, "chunk_index": index})  # 附加信息，不参与相似度

    # 加载 embedding 模型：输入文本，输出 512 维向量
    #   model_name → 模型名，中文语料用 bge-small-zh；首次运行自动下载
    print("\n── 加载 embedding 模型 ──")
    model = TextEmbedding(model_name="BAAI/bge-small-zh-v1.5")

    # embed(texts) 返回生成器，每个元素是一条文本的 numpy 向量；tolist() 转成 Python 列表
    embeddings = [vector.tolist() for vector in model.embed(texts)]

    # PersistentClient 把数据写进磁盘目录，关掉程序再开还在
    client = chromadb.PersistentClient(path=DB_PATH)
    # 演示每次都重建：换切法要整库重来，往旧库里追加会让两种切法混在一起
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass                                             # 第一次运行还没有这个表，删失败很正常
    collection = client.create_collection(name=COLLECTION_NAME)

    # add() 四个参数一一对应，长度必须一致：
    #   ids        → 唯一编号列表
    #   documents  → 原文列表（不用自己去算向量时不传 embeddings）
    #   embeddings → 向量列表，相似度靠它算
    #   metadatas  → 附加字段列表，可用来过滤和追溯来源
    collection.add(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)
    print(f"入库完成：{collection.count()} 个 chunk")
    return collection, model


# ── 5. 检索验证：用「你先知道答案」的问题检验 ────────────
# 每个问题都带一个 expected_source —— 这就是把「感觉相关」换成可判定的信号
TEST_QUESTIONS = [
    ("水壶能不能放进洗碗机清洗？", "manual_kettle"),
    ("耳机一次充电能用多久？", "manual_earbuds"),
    ("退货要保留哪些东西？", "policy_return"),
    ("电池用完了怎么办？", "manual_earbuds"),        # 故意留一个措辞不准的问题
]


def check_quality(collection, model) -> None:
    print("\n── 检索质量检查（Top-3）──")
    for question, expected in TEST_QUESTIONS:
        # 查询也要转成向量，而且必须是同一个模型——不同模型的向量空间不能互相比
        query_vector = [v.tolist() for v in model.embed([question])]
        # query() 参数：
        #   query_embeddings → 查询向量（列表的列表，支持一次问多个）
        #   n_results        → 返回几条，Top-K 里的 K
        #   include          → 结果里带哪些字段：原文、metadata、距离
        result = collection.query(
            query_embeddings=query_vector,
            n_results=3,
            include=["documents", "metadatas", "distances"],
        )
        hits = result["metadatas"][0]                    # 结果按查询分组，[0] 是第一个查询
        sources = [m["source"] for m in hits]            # 每条的来源文档
        distances = result["distances"][0]

        # 判定：答案所在文档在不在 Top-3、排第几
        rank = sources.index(expected) + 1 if expected in sources else None
        verdict = f"命中第 {rank} 名" if rank else "未命中"
        print(f"\n问题：{question}")
        print(f"  期望来源：{expected} → {verdict}")
        for i, (doc, dist) in enumerate(zip(sources, distances), start=1):
            print(f"  {i}. [{doc}] 距离={dist:.4f}")
            # 只看一眼命中的内容，判断它能不能直接回答这个问题
            print(f"     {result['documents'][0][i - 1][:40]}...")


if __name__ == "__main__":
    collection, model = build_knowledge_base(RAW_DOCS)
    check_quality(collection, model)
