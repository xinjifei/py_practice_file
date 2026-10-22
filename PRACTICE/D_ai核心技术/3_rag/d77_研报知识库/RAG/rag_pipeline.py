"""d77 研报知识库 —— 六环节流水线（取文档 → 清洗 → 分块 → 向量化 → 入库 → 检索验证）

六个 stage 一一对应，上一步的输出就是下一步的输入：
    1. stage1_fetch   输入 data/pdf/*.pdf          输出 docs[].pages（并落盘 output/raw/）
    2. stage2_clean   输入 docs[].pages            输出 docs[].clean_pages（并落盘 output/clean/）
    3. stage3_chunk   输入 docs[].clean_pages      输出 chunks[]（并落盘 output/chunks.jsonl）
    4. stage4_embed   输入 chunks[].text           输出 vectors[]（内存）
    5. stage5_store   输入 chunks + vectors        输出 Chroma collection
    6. stage6_verify  输入 collection + questions  输出 output/retrieval_report.md

先下载 PDF（只有第一次需要）：
    uv run python "PRACTICE/D_ai核心技术/3_rag/d77_研报知识库/RAG/download_reports.py"

再跑整条链（在项目根目录 ~/stu/py_practice_file 下）：
    uv run python "PRACTICE/D_ai核心技术/3_rag/d77_研报知识库/RAG/rag_pipeline.py"

只跑到某一环，便于中途验收（比如先看清洗结果再决定切块参数）：
    uv run python ".../rag_pipeline.py" --until 2
"""

import argparse
import bisect
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

import chromadb
import pypdfium2 as pdfium
from fastembed import TextEmbedding

BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR / "data" / "pdf"
REPORTS_PATH = BASE_DIR / "data" / "reports.json"
QUESTIONS_PATH = BASE_DIR / "data" / "questions.json"
OUTPUT_DIR = BASE_DIR / "output"
RAW_DIR = OUTPUT_DIR / "raw"
CLEAN_DIR = OUTPUT_DIR / "clean"
DB_PATH = BASE_DIR / "chroma_db"

COLLECTION_NAME = "research_reports_d77"
CHUNK_SIZE = 400
OVERLAP = 60
MODEL_NAME = "BAAI/bge-small-zh-v1.5"
TOP_K = 3


# ════════════════════════════════════════════════════════════════
# 环节 1：取文档 —— PDF → 每页原始文本
# ════════════════════════════════════════════════════════════════
def _render_pages(pages: list[str]) -> str:
    """把逐页文本拼成一个带页码分隔的 txt，方便人工核对。"""
    parts = [f"===== 第 {i} 页 =====\n{page}" for i, page in enumerate(pages, 1)]
    return "\n\n".join(parts).strip() + "\n"


def stage1_fetch() -> list[dict]:
    """输入 PDF，输出 docs：每份文档带 pages（每页一段原始文本）。

    这一步只负责「拿到文本」，不判断内容好坏。
    坏的典型症状：页数为 0、某页文本为空、整份只有几百字（扫描版）。
    """
    if not REPORTS_PATH.exists():
        sys.exit(f"找不到 {REPORTS_PATH}，先运行 download_reports.py")

    reports = json.loads(REPORTS_PATH.read_text(encoding="utf-8"))
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print("\n【环节 1/6 · 取文档】PDF → 每页原始文本")
    print(f"{'文档':<24}{'页数':>4}{'原始字数':>8}")
    docs = []
    for report in reports:
        pdf_path = BASE_DIR / report["pdf"]
        if not pdf_path.exists():
            sys.exit(f"缺文件 {pdf_path}，先重新运行 download_reports.py")

        # PDFium 按文本块读，双栏研报不会把图表坐标轴和正文按字符交错
        pdf = pdfium.PdfDocument(str(pdf_path))
        pages = [pdf[i].get_textpage().get_text_range() for i in range(len(pdf))]
        doc = dict(report, pages=pages)
        docs.append(doc)

        raw_path = RAW_DIR / f"{report['doc_id']}.txt"
        raw_path.write_text(_render_pages(pages), encoding="utf-8")
        print(f"{report['doc_id']:<24}{len(pages):>4}{sum(map(len, pages)):>8}")

    print(f"合计 {len(docs)} 份文档，原文落盘 → {RAW_DIR.relative_to(BASE_DIR)}")
    return docs


# ════════════════════════════════════════════════════════════════
# 环节 2：清洗 —— 去掉页眉页脚、联系方式、图表坐标轴、免责声明
# ════════════════════════════════════════════════════════════════
# 逐行判断：命中就整行丢掉。每条都对应研报解析里见过的一种噪声。
_DROP_LINE_PATTERNS = [
    re.compile(r"请务必(阅读|参阅)"),                       # 页脚声明
    re.compile(r"^\s*\d+\s*/\s*\d+\s*$"),                   # 页码 1 / 4
    re.compile(r"^(证券分析师|E-?MAIL|分析师登记编号|证书编号|联系电话|"
               r"电话|传真|地址|邮编|邮箱)[:：]?"),          # 联系方式块
    re.compile(r"^[\w.+-]+[@＠][\w.-]+$"),                   # 邮箱单行（有全角＠的）
    re.compile(r"^(数据来源|资料来源|来源)[:：]"),             # 图表来源
    re.compile(r"^相关研究报告?\s*$"),
    re.compile(r"^相关报告[:：]"),                            # 旧研报推荐列表
    re.compile(r"^\d+\.《"),                                 # 旧研报条目：1.《……》
    re.compile(r"^[\s%+\-.()0-9,，]+$"),                     # 纯数字/百分比行（图表坐标轴）
    re.compile(r"^(公司点评|公司信息更新报告|公司深度报告|行业研究|"
               r"行业深度报告|投资策略报告)\s*$"),             # 页眉报告类型
    re.compile(r"^证券研究报告[·|｜\s]"),                     # 页眉：证券研究报告 | 日期
    re.compile(r"^(证券研究报告|公司研究|公司点评报告|公司深度报告|"
               r"行业研究|行业深度报告|投资策略报告|公司信息更新报告)\s*$"),
    re.compile(r"^执业(证书|编号)[:：]?"),                     # 执业证书：S…
    re.compile(r"^[一-鿿]+(/[一-鿿]+)+$"),    # 行业分类页眉：美容护理/个护用品
    re.compile(r"分析师[:：]"),                               # 分析师：某某（执业 S…）
    re.compile(r"（分析师）|\(分析师\)"),                      # 分析师署名行
    re.compile(r"执业\s*S\d+"),                               # 执业编号
    re.compile(r"^市价（人民币）"),                           # 首面行情块
    re.compile(r"^(投资评级|日期|当前股价|一年最高最低|总市值|流通市值|"
               r"总股本|流通股本|近\s*\d+\s*个月换手率)[\s(（:：]"),  # 首面信息表
    re.compile(r"^股价走势图\s*$"),
    re.compile(r"^(?:\S+\s+)?(?:沪深300|创业板指|上证指数|中证\S+)\s*$"),  # 走势图图例
    re.compile(r"^[一-鿿]{2,4}\s+.*分析师\s*$"),      # 姓名 + 职位
]

# 免责声明/评级说明/团队简介从这一行开始，后面（含后续页）全部不要
_DISCLAIMER_START = re.compile(
    r"^(法律声明|免责声明|重要声明|特别声明|分析师声明|分析师承诺|"
    r"免责及评级说明部分|投资评级的说明|投资评级说明|"
    r"市场中相关报告评级比率分析|评级说明|研究团队简介)\s*[:：]?\s*$")

# PDF 里残留的排版标记，如 [Table_Profit]、[Table_Summary]
_TABLE_TAG = re.compile(r"\[Table_[^\]]*\]")


def _normalize_line(line: str) -> str:
    """归一化后再比较：删空白、数字全换成 0。

    这样「请务必参阅…… 1 / 4」和「请务必参阅…… 2 / 4」会变成同一个键，
    按「多页重复出现」就能自动找出页眉页脚，不用把每家券商的模板都写死。
    """
    key = re.sub(r"\s+", "", line)
    return re.sub(r"\d+", "0", key)


def _is_short_cjk(line: str) -> bool:
    """竖排页眉会被拆成一字一行（公 / 司 / 研 / 究），这类行直接丢。"""
    compact = re.sub(r"\s+", "", line)
    return 0 < len(compact) <= 2 and all("一" <= ch <= "鿿" for ch in compact)


def _find_repeated_lines(pages: list[str]) -> set[str]:
    """找出在 60% 以上页面重复出现的短行 —— 页眉/页脚/报告类型的通用识别。"""
    if len(pages) < 2:
        return set()
    counter = Counter()
    for page in pages:
        seen = set()
        for line in page.splitlines():
            key = _normalize_line(line)
            if len(key) >= 4 and key not in seen:   # 太短的行交给 _is_short_cjk 处理
                seen.add(key)
                counter[key] += 1
    threshold = max(2, int(len(pages) * 0.6 + 0.999))
    return {key for key, n in counter.items() if n >= threshold}


def _clean_page(page: str, repeated: set[str]) -> tuple[str, bool]:
    """清洗一页。返回 (干净文本, 是否遇到免责声明)。

    第二个返回值是给调用方看的：免责声明之后的页直接整页丢弃。
    """
    kept = []
    for raw_line in page.splitlines():
        # 先撕掉 PDF 排版标记，再按内容判断（有的标签被正文挤到括号中间了）
        line = re.sub(r"Table_[A-Za-z_]*", "", _TABLE_TAG.sub("", raw_line)).strip()
        if not line:
            kept.append("")
            continue
        if _DISCLAIMER_START.match(line):
            return _tidy(kept), True
        if _normalize_line(line) in repeated:
            continue
        if any(pattern.search(line) for pattern in _DROP_LINE_PATTERNS):
            continue
        if _is_short_cjk(line):
            continue
        kept.append(line)
    return _tidy(kept), False


def _tidy(lines: list[str]) -> str:
    """收尾：行内空白压缩、连续空行压成一个段落分隔。"""
    text = "\n".join(lines)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def stage2_clean(docs: list[dict]) -> list[dict]:
    """输入原始分页文本，输出 clean_pages（与页一一对应）。

    判定这一步坏没坏的信号：清洗后字数只剩零头（正则误杀正文）、
    或清洗后几乎没少字（噪声没去掉，向量里会混进页眉页脚）。
    """
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    print("\n【环节 2/6 · 清洗】去页眉页脚 / 联系方式 / 免责声明")
    print(f"{'文档':<24}{'原始字数':>8}{'清洗后':>8}{'保留率':>8}{'有效页':>6}")
    for doc in docs:
        repeated = _find_repeated_lines(doc["pages"])
        clean_pages, stopped, removed_lines = [], False, 0

        for page in doc["pages"]:
            if stopped:                      # 免责声明之后整页不要
                clean_pages.append("")
                continue
            clean, hit_disclaimer = _clean_page(page, repeated)
            clean_pages.append(clean)
            if hit_disclaimer:
                stopped = True
            removed_lines += page.count("\n") + 1 - (clean.count("\n") + 1 if clean else 0)

        doc["clean_pages"] = clean_pages
        raw_chars = sum(map(len, doc["pages"]))
        clean_chars = sum(map(len, clean_pages))
        valid_pages = sum(1 for p in clean_pages if p)

        clean_path = CLEAN_DIR / f"{doc['doc_id']}.txt"
        clean_path.write_text(_render_pages(clean_pages), encoding="utf-8")
        print(f"{doc['doc_id']:<24}{raw_chars:>8}{clean_chars:>8}"
              f"{clean_chars / max(raw_chars, 1):>7.0%}{valid_pages:>6}")

    print(f"清洗结果落盘 → {CLEAN_DIR.relative_to(BASE_DIR)}")
    return docs


# ════════════════════════════════════════════════════════════════
# 环节 3：分块 —— 段落 → 句子 → 硬切，逐级降级
# ════════════════════════════════════════════════════════════════
def _join_pages(clean_pages: list[str]) -> tuple[str, list[tuple[int, int, int]]]:
    """把各页拼成全文，同时记下每页在全文里的字符区间 [(start, end, 页码)]。

    有了字符区间，chunk 落在哪几页就能反查出来，metadata 里带页码靠它。
    """
    parts, spans, cursor = [], [], 0
    for page_no, page in enumerate(clean_pages, 1):
        if not page.strip():
            continue
        if parts:
            parts.append("\n\n")
            cursor += 2
        start = cursor
        parts.append(page)
        cursor += len(page)
        spans.append((start, cursor, page_no))
    return "".join(parts), spans


def _page_at(spans: list[tuple[int, int, int]], offset: int) -> int:
    """字符位置 → 页码。bisect 找最后一个 start <= offset 的页。"""
    if not spans:
        return 0
    starts = [s for s, _, _ in spans]
    idx = max(bisect.bisect_right(starts, offset) - 1, 0)
    return spans[idx][2]


def _iter_paragraphs(text: str):
    """按空行切段落，同时带出每段在全文中的 [start, end) 区间。"""
    cursor = 0
    for para in text.split("\n\n"):
        raw_start = cursor
        cursor += len(para) + 2
        stripped = para.strip()
        if stripped:
            lead = len(para) - len(para.lstrip())
            start = raw_start + lead
            yield stripped, start, start + len(stripped)


def _iter_sentences(text: str, offset: int):
    """按句末标点和换行切句，带出每句的 [start, end) 区间。

    换行也算切口，是因为研报里的财务表格没有句号：一整张表会被当成一个
    「超长句子」，只能硬切，切出来行和数字都是断的。按行切，至少表格行完整。
    """
    pos = 0
    for match in re.finditer(r"[。！？]\n?|\n", text):
        end = match.end()
        piece = text[pos:end]
        if piece.strip():
            lead = len(piece) - len(piece.lstrip())
            # 保留行尾换行，合并成块后行与行不会粘成一串
            yield piece[lead:], offset + pos + lead, offset + end
        pos = end
    rest = text[pos:]
    if rest.strip():
        lead = len(rest) - len(rest.lstrip())
        yield rest[lead:], offset + pos + lead, offset + len(rest)


def _iter_pieces(text: str, size: int, overlap: int):
    """三层降级：段落够短就整段；超长按句；句子还超长就硬切（保留 overlap）。

    每片最后一个值是「是不是硬切」——硬切会切断句子，是分块质量的关键信号。
    """
    for para, para_start, para_end in _iter_paragraphs(text):
        if len(para) <= size:
            yield para, para_start, para_end, False
            continue
        for sentence, sent_start, sent_end in _iter_sentences(para, para_start):
            if len(sentence) <= size:
                yield sentence, sent_start, sent_end, False
                continue
            current, current_start = sentence, sent_start
            while len(current) > size:
                yield current[:size], current_start, current_start + size, True
                current = current[size - overlap:]
                current_start += size - overlap
            if current:
                yield current, current_start, current_start + len(current), True


def chunk_document(clean_pages: list[str], size: int = CHUNK_SIZE,
                   overlap: int = OVERLAP) -> list[dict]:
    """一份文档 → 若干块。每块带 text、page_start、page_end。"""
    assert overlap < size, "重叠必须小于块大小，否则会切不动"
    text, spans = _join_pages(clean_pages)
    if not text.strip():
        return []

    chunks, buf, buf_start, buf_end, buf_hard = [], "", 0, 0, False

    def flush():
        chunks.append({
            "text": buf.strip(),
            "page_start": _page_at(spans, buf_start),
            "page_end": _page_at(spans, max(buf_start, buf_end - 1)),
            "hard_cut": buf_hard,
        })

    for piece, piece_start, piece_end, hard in _iter_pieces(text, size, overlap):
        # 小块合并到接近 size，避免碎成一堆上下文不完整的块
        if buf and len(buf) + len(piece) > size:
            flush()
            buf = ""
        if not buf:
            buf_start, buf_hard = piece_start, False
        buf += piece
        buf_end = piece_end
        buf_hard = buf_hard or hard
    if buf:
        flush()
    return chunks


def stage3_chunk(docs: list[dict]) -> list[dict]:
    """输入 clean_pages，输出 chunks（含 source / 页码 / 块号 / 长度）。"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\n【环节 3/6 · 分块】段落 → 句子 → 硬切（size=%d, overlap=%d）"
          % (CHUNK_SIZE, OVERLAP))
    print(f"{'文档':<24}{'块数':>4}{'最短':>6}{'最长':>6}{'平均':>6}")

    chunks, per_doc = [], {}
    for doc in docs:
        doc_chunks = chunk_document(doc["clean_pages"])
        lengths = [len(c["text"]) for c in doc_chunks]
        per_doc[doc["doc_id"]] = {
            "stock_name": doc["stock_name"],
            "chunks": len(doc_chunks),
            "min": min(lengths) if lengths else 0,
            "max": max(lengths) if lengths else 0,
            "avg": round(statistics.mean(lengths), 1) if lengths else 0,
        }
        for index, chunk in enumerate(doc_chunks):
            chunks.append({
                "id": f"{doc['doc_id']}#{index:03d}",
                "source": doc["doc_id"],
                "stock_name": doc["stock_name"],
                "stock_code": doc["stock_code"],
                "industry": doc["industry"],
                "org": doc["org"],
                "publish_date": doc["publish_date"],
                "title": doc["title"],
                "chunk_index": index,
                "length": len(chunk["text"]),
                "page_start": chunk["page_start"],
                "page_end": chunk["page_end"],
                "hard_cut": chunk["hard_cut"],
                "text": chunk["text"],
            })
        print(f"{doc['doc_id']:<24}{len(doc_chunks):>4}"
              f"{per_doc[doc['doc_id']]['min']:>6}{per_doc[doc['doc_id']]['max']:>6}"
              f"{per_doc[doc['doc_id']]['avg']:>6.0f}")

    lengths = [c["length"] for c in chunks]
    stats = {
        "documents": len(docs),
        "chunks": len(chunks),
        "chunk_size_limit": CHUNK_SIZE,
        "overlap": OVERLAP,
        "avg_length": round(statistics.mean(lengths), 1) if lengths else 0,
        "min_length": min(lengths) if lengths else 0,
        "max_length": max(lengths) if lengths else 0,
        "per_doc": per_doc,
        "length_buckets": {
            "0-99": sum(1 for n in lengths if n < 100),
            "100-199": sum(1 for n in lengths if 100 <= n < 200),
            "200-299": sum(1 for n in lengths if 200 <= n < 300),
            "300-399": sum(1 for n in lengths if 300 <= n < 400),
            "400": sum(1 for n in lengths if n >= 400),
        },
        # 硬切 = 句子长到 400 字还切不完，只能按字数砍断。块长贴上限多半是
        # 合并逻辑填满的（正常）；hard_cut 的块才是真的切断了句子。
        "hard_cut_chunks": sum(1 for c in chunks if c["hard_cut"]),
        # 异常信号：某文档只出 1 块 / 有硬切块 / 块特别短
        "alerts": [],
    }
    for doc_id, info in per_doc.items():
        if info["chunks"] <= 1:
            stats["alerts"].append(f"{doc_id} 只切出 {info['chunks']} 块")
    hard_ids = [c["id"] for c in chunks if c["hard_cut"]]
    if hard_ids:
        stats["alerts"].append(
            f"{len(hard_ids)} 个块是硬切（句子被切断）：{hard_ids[:5]}"
            + (" 等" if len(hard_ids) > 5 else ""))
    stats["alerts"] += [
        f"{c['id']} 只有 {c['length']} 字" for c in chunks if c["length"] < 80
    ]

    chunks_path = OUTPUT_DIR / "chunks.jsonl"
    with chunks_path.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    (OUTPUT_DIR / "stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n合计 {len(docs)} 份文档 / {len(chunks)} 块 | "
          f"平均 {stats['avg_length']} 字 / 最短 {stats['min_length']} / "
          f"最长 {stats['max_length']}")
    print(f"块长分布：{stats['length_buckets']} | "
          f"硬切块：{stats['hard_cut_chunks']}")
    if stats["alerts"]:
        print("异常信号：")
        for alert in stats["alerts"]:
            print(f"  - {alert}")
    print(f"blocks 落盘 → {chunks_path.relative_to(BASE_DIR)}")
    return chunks


# ════════════════════════════════════════════════════════════════
# 环节 4：向量化 —— 文本块 → 向量
# ════════════════════════════════════════════════════════════════
def stage4_embed(chunks: list[dict]) -> tuple[TextEmbedding, list[list[float]]]:
    """输入 chunk 文本，输出等长的向量列表（512 维）。

    判定信号：维度是否一致、向量数是否等于块数、有没有全 0 向量。
    """
    print("\n【环节 4/6 · 向量化】文本块 → 向量")
    print(f"模型：{MODEL_NAME}（首次运行会自动下载）")
    model = TextEmbedding(model_name=MODEL_NAME)
    vectors = [vector.tolist() for vector in model.embed([c["text"] for c in chunks])]

    if len(vectors) != len(chunks):
        sys.exit(f"向量数 {len(vectors)} 与块数 {len(chunks)} 不一致")
    zero_count = sum(1 for v in vectors if not any(v))
    print(f"完成：{len(vectors)} 条 × {len(vectors[0])} 维"
          + (f"，其中有 {zero_count} 条全 0" if zero_count else ""))
    return model, vectors


# ════════════════════════════════════════════════════════════════
# 环节 5：入库 —— 向量 + 原文 + metadata → Chroma
# ════════════════════════════════════════════════════════════════
def stage5_store(chunks: list[dict], vectors: list[list[float]]):
    """整库重建。换切法必须重建：两种切法的块混在一个库里，距离没有可比性。"""
    print("\n【环节 5/6 · 入库】向量 + 原文 + metadata → Chroma")
    client = chromadb.PersistentClient(path=str(DB_PATH))
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass                                   # 第一次运行还没有这个表
    collection = client.create_collection(COLLECTION_NAME)

    collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        embeddings=vectors,
        # metadata 不参与相似度，但检索后要能追溯：来源、页码、公司、日期
        metadatas=[{
            "source": c["source"],
            "stock_name": c["stock_name"],
            "stock_code": c["stock_code"],
            "industry": c["industry"],
            "org": c["org"],
            "publish_date": c["publish_date"],
            "title": c["title"],
            "chunk_index": c["chunk_index"],
            "page_start": c["page_start"],
            "page_end": c["page_end"],
            "hard_cut": c["hard_cut"],
        } for c in chunks],
    )
    print(f"collection={COLLECTION_NAME} | count={collection.count()} | 目录：{DB_PATH}")
    return collection


# ════════════════════════════════════════════════════════════════
# 环节 6：检索验证 —— 已知答案在哪份文档，看它排第几
# ════════════════════════════════════════════════════════════════
def _excerpt(text: str, width: int = 60) -> str:
    return re.sub(r"\s+", " ", text)[:width]


def stage6_verify(collection, model: TextEmbedding) -> list[dict]:
    """输入问题清单（含期望来源），输出 Top-3 命中 + 距离 + 报告。"""
    print("\n【环节 6/6 · 检索验证】Top-%d" % TOP_K)
    if not QUESTIONS_PATH.exists():
        print(f"没找到 {QUESTIONS_PATH}，跳过检索验证")
        return []

    questions = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    results = []
    for item in questions:
        query = item["question"]
        expected = item["expected_source"]
        # 查询必须和文档用同一个 embedding 模型，否则两个向量空间不可比
        query_vector = [v.tolist() for v in model.embed([query])]
        response = collection.query(
            query_embeddings=query_vector,
            n_results=TOP_K,
            include=["documents", "metadatas", "distances"],
        )
        documents = response["documents"][0]
        metadatas = response["metadatas"][0]
        distances = response["distances"][0]
        sources = [m["source"] for m in metadatas]

        rank = sources.index(expected) + 1 if expected in sources else None
        result = {
            "id": item.get("id", ""),
            "question": query,
            "expected_source": expected,
            "hit_rank": rank,
            "hits": [{
                "rank": i + 1,
                "source": m["source"],
                "stock_name": m["stock_name"],
                "page_start": m["page_start"],
                "page_end": m["page_end"],
                "distance": round(float(d), 4),
                "excerpt": _excerpt(documents[i]),
            } for i, (m, d) in enumerate(zip(metadatas, distances))],
        }
        results.append(result)

        verdict = f"命中第 {rank} 名" if rank else "未命中 Top-3"
        print(f"\n问题：{query}")
        print(f"  期望来源：{expected} → {verdict}")
        for hit in result["hits"]:
            print(f"  {hit['rank']}. [{hit['source']}] 第 {hit['page_start']}-"
                  f"{hit['page_end']} 页 | 距离 {hit['distance']:.4f}")
            print(f"     {hit['excerpt']}...")

    _write_retrieval_report(results, collection)
    return results


def _write_retrieval_report(results: list[dict], collection) -> None:
    """把结果写成 markdown：来源命中、距离、摘录都留档，相关度留给你填。"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    hits = sum(1 for r in results if r["hit_rank"])
    lines = [
        "# d77 研报知识库 · 检索验证报告",
        "",
        f"- 文档数：{len(json.loads(REPORTS_PATH.read_text(encoding='utf-8')))}",
        f"- 入库块数：{collection.count()}",
        f"- embedding：`{MODEL_NAME}`",
        f"- 检索：Top-{TOP_K}，期望来源命中 {hits}/{len(results)}",
        "",
        "判定标准：期望来源在不在 Top-3、排第几。",
        "「相关度」一列留给你按块内容填：相关 / 部分相关 / 不相关。",
        "",
        "| 问题 | 期望来源 | 命中 | Top1 距离 | 相关度 |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        rank = f"第 {r['hit_rank']} 名" if r["hit_rank"] else "未命中"
        top1 = r["hits"][0]["distance"] if r["hits"] else "-"
        lines.append(f"| {r['question']} | {r['expected_source']} | {rank} "
                     f"| {top1} |  |")

    lines += ["", "## 逐题 Top-%d 明细" % TOP_K, ""]
    for r in results:
        lines.append(f"### {r['id']} {r['question']}")
        lines.append("")
        lines.append(f"期望来源：`{r['expected_source']}`")
        lines.append("")
        lines.append("| # | 来源 | 页码 | 距离 | 摘录 |")
        lines.append("|---|---|---|---|---|")
        for hit in r["hits"]:
            excerpt = hit["excerpt"].replace("|", "｜")
            lines.append(f"| {hit['rank']} | {hit['source']} | "
                         f"{hit['page_start']}-{hit['page_end']} | "
                         f"{hit['distance']} | {excerpt} |")
        lines.append("")

    report_path = OUTPUT_DIR / "retrieval_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    (OUTPUT_DIR / "retrieval_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n检索报告 → {report_path.relative_to(BASE_DIR)}")


# ════════════════════════════════════════════════════════════════
def main() -> None:
    parser = argparse.ArgumentParser(description="d77 研报知识库六环节流水线")
    parser.add_argument("--until", type=int, default=6, choices=range(1, 7),
                        help="只跑到第几环（默认 6 全跑）")
    args = parser.parse_args()

    docs = stage1_fetch()
    if args.until == 1:
        return
    docs = stage2_clean(docs)
    if args.until == 2:
        return
    chunks = stage3_chunk(docs)
    if args.until == 3:
        return
    model, vectors = stage4_embed(chunks)
    if args.until == 4:
        return
    collection = stage5_store(chunks, vectors)
    if args.until == 5:
        return
    stage6_verify(collection, model)


if __name__ == "__main__":
    main()
