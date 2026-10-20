"""
demo_chunking.py —— 三种文本分块策略的最小示例

练习要求你拿一份 50 页研报、chunk 大小 500 字来切；这个 demo 故意换成
「一篇 600 字的咖啡小史」、chunk 大小 120 字 —— 输出短、看得清边界，
看思路，别抄数据，练习要你自己准备长文本。

运行前（在项目根目录 ~/stu/py_practice_file 下）：
    uv run python "PRACTICE/D_ai核心技术/3_rag/d76_chunking策略/demo_chunking.py"
"""

import re                    # 正则：用来按句号/问号/感叹号切句子
import chromadb              # 昨天学过：向量数据库
from fastembed import TextEmbedding   # 昨天学过：文本 → 向量（ONNX，中文模型 bge-small-zh）

# ── 0. 示例长文本 ──────────────────────────────────
# 三个 \n\n 把全文切成 4 个自然段，段落是作者写作时的语义单元。
# 你的练习换成自己找的研报正文（可以先把 PDF 复制成 txt）。
TEXT = """咖啡的起源可以追溯到公元九世纪的埃塞俄比亚。传说一位名叫柯迪的牧羊人发现，羊群在啃食一种红色浆果后异常兴奋，当地人由此开始尝试这种植物的果实。最早的使用方式并非冲泡饮品，而是把咖啡豆与动物脂肪混合，作为长途跋涉时的能量口粮。

十五世纪前后，咖啡传入阿拉伯半岛，也门出现了最早的咖啡种植园。咖啡馆在麦加、开罗和伊斯坦布尔相继出现，成为人们交谈、辩论和交换消息的场所。由于咖啡馆聚集人群，统治者曾多次下令关闭，但都没能阻止它的扩散。

十七世纪，咖啡经由威尼斯进入欧洲。起初它被当作药物出售，随后迅速成为社交饮品。伦敦的咖啡馆被称为「一便士大学」，只要花一便士买一杯咖啡，就能听到最新的商业消息和政治讨论。保险业和证券交易所的雏形，都与这些咖啡馆有渊源。

十八世纪以后，咖啡种植随殖民扩张扩散到美洲和东南亚。巴西凭借气候和土地成为全球最大的咖啡生产国。今天，咖啡是全球交易量最大的农产品之一，产业链从种植、烘焙一直延伸到连锁零售，养活了数千万人。"""


# ── 1. 策略一：固定长度切分 ────────────────────────
def fixed_chunks(text, size, overlap=0):
    """每 size 个字符切一刀，相邻块可以重叠 overlap 个字符。

    参数：
        text    → 要切的原文
        size    → 每块的目标长度（字符数）
        overlap → 相邻块的重合长度，0 表示不重叠
    """
    chunks = []
    step = size - overlap        # 每刀前进多少个字符：重叠越多，前进越少
    if step <= 0:                # 防呆：overlap >= size 会原地踏步，死循环
        raise ValueError("overlap 必须小于 size")
    for start in range(0, len(text), step):   # range(起点, 终点, 步长)
        chunk = text[start:start + size]      # 切片：从 start 取 size 个字符
        if chunk:                             # 最后一块可能不足 size，仍保留
            chunks.append(chunk)
    return chunks


# ── 2. 策略二：按段落切分 ──────────────────────────
def paragraph_chunks(text):
    """以空行（\n\n）为界切分，一块 = 一个自然段。

    最简单，也最尊重作者的写作结构；缺点是段落长短完全不受控，
    一段 3000 字的研报正文会被原样塞成一个大 chunk。
    """
    parts = text.split("\n\n")                       # 按空行切成列表
    return [p.strip() for p in parts if p.strip()]   # strip() 去掉首尾空白；if 过滤空段


# ── 3. 策略三：递归切分 ────────────────────────────
def hard_split(text, size):
    """兜底：连句子都超长时，只能按固定长度硬切。"""
    return [text[i:i + size] for i in range(0, len(text), size)]


def split_by_sentence(piece, size):
    """把一段超长文本按句子装箱：句子完整放得下就放，放不下就换下一块。

    re.split(r'(?<=[。！？])', piece) 的拆解：
        r'...'              → 原始字符串，避免反斜杠转义
        (?<=[。！？])        → 零宽断言：只在「前面是。！？」之后再切
        因为标点留在前一句末尾，所以切出来的句子自带句号
    """
    sentences = [s for s in re.split(r'(?<=[。！？])', piece) if s.strip()]
    out, buf = [], ""                  # buf = 当前正在装箱的那一块
    for s in sentences:
        if len(s) > size:              # 单个句子本身就超长 → 硬切
            if buf:
                out.append(buf)
                buf = ""
            out.extend(hard_split(s, size))
        elif len(buf) + len(s) <= size:  # 装得下 → 继续装
            buf += s
        else:                          # 装不下 → 封箱，新句子开新箱
            out.append(buf)
            buf = s
    if buf:                            # 最后没封的箱
        out.append(buf)
    return out


def recursive_chunks(text, size):
    """递归：先按段落切；某段太长，就把它降级按句子切；还太长再硬切。

    这就是「递归」二字的含义——从最粗的语义边界往下找，
    直到每块都不超过 size。它同时保住了段落语义和长度上限。
    """
    chunks = []
    for para in text.split("\n\n"):        # 第一层：段落
        para = para.strip()
        if not para:
            continue
        if len(para) <= size:              # 段落本身够短 → 直接用
            chunks.append(para)
        else:                              # 第二层（第三层在 split_by_sentence 里）
            chunks.extend(split_by_sentence(para, size))
    return chunks


# ── 4. 三种策略跑一遍，比数量、比边界 ──────────────
def report(name, chunks):
    """打印一种策略的统计和样例：数量、最短/最长、每块开头露出的样子。"""
    lengths = [len(c) for c in chunks]
    print(f"\n【{name}】共 {len(chunks)} 块")
    print(f"  长度：最短 {min(lengths)} / 最长 {max(lengths)} / 平均 {sum(lengths) / len(lengths):.1f}")
    print(f"  第1块结尾 15 字：...{chunks[0][-15:]}")
    print(f"  第2块开头 15 字：{chunks[1][:15]}...")


SIZE = 90                     # 练习里用 500，demo 用 90 方便看边界（比大多数段落短，递归会真正降级）

fixed_no_overlap = fixed_chunks(TEXT, SIZE, overlap=0)
fixed_overlap_20 = fixed_chunks(TEXT, SIZE, overlap=20)   # 重叠 20 字，约 1/6
paras = paragraph_chunks(TEXT)
recursive = recursive_chunks(TEXT, SIZE)

report("固定长度·不重叠", fixed_no_overlap)
report("固定长度·重叠20", fixed_overlap_20)
report("按段落", paras)
report("递归切分", recursive)

# 观察点（做题时对着自己的输出回答）：
#   1. 固定长度里，第2块是不是从半句话中间开始的？——这就是「切断句子」。
#   2. 重叠版块数变多了多少？这是 overlap 的直接代价。
#   3. 按段落切，最长的一段有多长？它会不会超出 embedding 模型能吃的长度？
#   4. 递归切分的块，开头是不是总在句子边界？长度是不是都被压到了 SIZE 以内？


# ── 5. 三种切分分别入库，同一个问题比检索 ──────────
# 每一步就是昨天练过的 Chroma 用法：文本 → 向量 → add()。
# 关键：三份数据必须用同一个 embedding 模型，否则向量空间不同，没法比。
model = TextEmbedding(model_name="BAAI/bge-small-zh-v1.5")   # 第一次下载约 90MB，之后走缓存
client = chromadb.PersistentClient(path="./chroma_demo_db")  # 数据落在磁盘上

strategies = {
    "chunk_fixed_novlp": fixed_no_overlap,
    "chunk_fixed_ovlp": fixed_overlap_20,
    "chunk_para": paras,
    "chunk_recursive": recursive,
}

# 先清掉上一次运行留下的同名 collection，否则同一批 id 再 add 会报「已存在」。
# list_collections() 返回已有 collection 对象，.name 取名字；delete_collection() 按名字删。
for c in client.list_collections():
    if c.name.startswith("chunk_"):
        client.delete_collection(c.name)

# 建四个 collection：每个策略一个，互不干扰，方便对比。
# 名字要求：3~63 个字符，只能字母/数字/下划线/连字符，首尾必须是字母或数字。
for name, chunks in strategies.items():
    collection = client.get_or_create_collection(name=name)   # 有就复用，没有就新建
    collection.add(
        ids=[f"{name}_{i}" for i in range(len(chunks))],      # id 唯一即可，这里用「策略名_序号」
        documents=chunks,                                     # 原文，查询结果会原样返回
        embeddings=[v.tolist() for v in model.embed(chunks)],  # embed() 收可迭代对象，返回生成器
    )

query = "最早的咖啡馆出现在哪些城市？"
query_vec = [v.tolist() for v in model.embed([query])]        # 查询也必须用同一个模型转向量

print(f"\n查询：{query}")
for name in strategies:
    collection = client.get_collection(name=name)             # 按名字取回已有 collection
    res = collection.query(
        query_embeddings=query_vec,                           # 查询向量，外面还要套一层列表
        n_results=2,                                          # Top-K
        include=["documents", "distances"],                   # 想看的字段
    )
    print(f"\n  ── {name} ──")
    for i, doc in enumerate(res["documents"][0]):             # enumerate 同时给序号和元素
        print(f"    第{i + 1}名（距离 {res['distances'][0][i]:.4f}）：{doc[:60]}...")

# 观察点：
#   同一条问题，四个 collection 的 Top-1 是同一段吗？
#   固定长度的块如果恰好把「十五世纪…咖啡馆在麦加、开罗」切成两半，
#   命中里面一半的那一块就缺了另一半的上下文——这就是 chunk 边界改变检索效果。
