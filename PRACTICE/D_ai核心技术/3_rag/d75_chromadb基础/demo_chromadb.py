"""
demo_chromadb.py —— ChromaDB 最小可运行示例

今天练习的数据是「10 只 A 股公司简介」，这个 demo 故意换成
「4 部电影简介」——看思路，别抄数据，练习要你自己动手准备 10 条。

⚠️ 为什么不用 sentence-transformers：
   它的导入链会拉进 sklearn → scipy，而这台机器上的 scipy 二进制
   和当前 macOS 不兼容（__thread_bss 段报错）。
   fastembed 用 ONNX 运行时算向量，不经过 sklearn/scipy，
   同时支持中文模型 bge-small-zh-v1.5，语义搜索效果更好。

运行前（在项目根目录 ~/stu/py_practice_file 下）：
    uv add chromadb fastembed
然后运行：
    uv run python "PRACTICE/D_ai核心技术/3_rag/d75_chromadb基础/demo_chromadb.py"
"""

import chromadb                                    # 向量数据库本体
from fastembed import TextEmbedding                # 把文本变成向量（ONNX 版）

# ── 1. 准备原始文本 ────────────────────────────────
# 每条文本就是一个「文档」。练习里换成你的 10 条公司简介。
ids = ["m1", "m2", "m3", "m4"]                     # 每条文档的唯一编号，自己起，删除/更新都靠它
texts = [
    "一名宇航员在太空执行任务时与地球失联，独自面对未知的宇宙。",   # 太空、孤独、科幻
    "一群科学家乘坐飞船穿越虫洞，为人类寻找新的家园。",             # 太空、科幻、探索
    "一对情侣在巴黎的街头相遇，度过了一个浪漫的夏天。",             # 爱情、巴黎、浪漫
    "一名厨师回到家乡，用一碗面重新连接起与父亲的关系。",           # 家庭、美食、亲情
]
metadatas = [                                      # 附加信息，Chroma 不拿它算相似度，但可以用来过滤
    {"genre": "科幻", "year": 2013},
    {"genre": "科幻", "year": 2014},
    {"genre": "爱情", "year": 2011},
    {"genre": "剧情", "year": 2018},
]

# ── 2. 加载 Embedding 模型 ─────────────────────────
# 模型的作用：输入一段文本，输出一个固定长度的向量（bge-small-zh 是 512 维）。
# 语义越接近的文本，向量在空间里的方向越接近——这就是「语义搜索」的底层。
embedding_model = TextEmbedding(
    model_name="BAAI/bge-small-zh-v1.5",   # 参数1：模型名。中文小模型，首次运行自动下载（约 90MB）
    # 其他常用参数（今天不用）：
    #   cache_dir=...   → 模型文件存到哪个目录
    #   threads=...    → 用几个 CPU 线程做推理
)

# embed() 把一组文本批量转成向量。
#   texts   → 输入文本的可迭代对象（列表就行）
#   返回值   → 生成器，每次产出一个 numpy 数组（一条文本一个向量）
#   要转成 Python 列表的列表，Chroma 才收
embeddings = [vector.tolist() for vector in embedding_model.embed(texts)]

# ── 3. 打开数据库、拿到 Collection ─────────────────
# PersistentClient：数据写到磁盘，关掉程序再开还在。
#   path → 数据库目录。相对路径基于你运行脚本时所在的目录。
client = chromadb.PersistentClient(path="./chroma_demo_db")

# Collection 类似关系数据库里的「表」，一组相关文档放一起。
# get_or_create_collection：有就拿来用，没有就新建，重复运行不会报错。
#   name → collection 名字，自己起
collection = client.get_or_create_collection(name="movies_demo")

# ── 4. 存入 ───────────────────────────────────────
# add() 的四个参数一一对应：
#   ids        → 每条文档的唯一编号（列表）
#   documents  → 原始文本（列表），查询结果里会原样返回
#   embeddings → 文本对应的向量（列表的列表），相似度就是拿它算的
#   metadatas  → 每条文档的附加字段（列表），用于过滤，不参与相似度计算
collection.add(
    ids=ids,
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas,
)

print("存入后文档数：", collection.count())        # count() 返回当前 collection 里的文档条数

# ── 5. 查询 ───────────────────────────────────────
query = "有哪些关于太空探险的电影？"                # 注意：没有一个字和文档完全一样

# 查询也要先变成同一套向量空间里的向量——必须用同一个模型！
query_embedding = [
    vector.tolist() for vector in embedding_model.embed([query])
]                                                  # embed 收可迭代对象，所以查询包成 [query]

# query() 做的事：拿查询向量和库里每条向量算距离，返回最近的 n_results 条。
#   query_embeddings → 查询向量（列表的列表）
#   n_results        → 返回几条（Top-K）
#   include          → 指定结果里带哪些字段：documents 原文、metadatas 附加信息、distances 距离
results = collection.query(
    query_embeddings=query_embedding,
    n_results=2,
    include=["documents", "metadatas", "distances"],
)

print("\n查询：", query)
for i in range(len(results["ids"][0])):            # results 的每个字段都是「按查询分组」的二维列表
    print(f"  第{i + 1}名：{results['documents'][0][i]}")
    print(f"     id={results['ids'][0][i]} 距离={results['distances'][0][i]:.4f}")

# ── 6. 删除 ───────────────────────────────────────
# delete() 按 id 删除。删完再查，m3 不应该再出现。
collection.delete(ids=["m3"])
print("\n删除 m3 后文档数：", collection.count())

query_embedding_after = [
    vector.tolist() for vector in embedding_model.embed(["浪漫的爱情故事"])
]
results_after = collection.query(
    query_embeddings=query_embedding_after,
    n_results=3,
    include=["documents", "distances"],
)
print("删除后查询「浪漫的爱情故事」：")
for i in range(len(results_after["ids"][0])):
    print(f"  第{i + 1}名：{results_after['documents'][0][i]}")
