"""取文档 · 第 1 步：从东方财富研报接口抓 10 份个股研报 PDF。

这是六环节里「取文档」的前半段，只负责把 PDF 落到本地，
不做解析、不做清洗——那些在 rag_pipeline.py 的 stage1 之后做。

用法（在项目根目录 ~/stu/py_practice_file 下）：
    uv run python "PRACTICE/D_ai核心技术/3_rag/d77_研报知识库/RAG/download_reports.py"

产物：
    data/pdf/<doc_id>.pdf     每份研报一个文件，doc_id 形如 r01_宝丰能源
    data/reports.json         每份文档的标题/公司/机构/日期/页数等元数据

重复运行会复用已有的 reports.json 和 PDF，不会重新下载。
想重新抓（比如换一批），删掉 data/ 目录再跑。
"""

import json
import re
import sys
import time
from datetime import date, timedelta
from pathlib import Path

import pypdfium2 as pdfium
import requests

BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR / "data" / "pdf"
META_PATH = BASE_DIR / "data" / "reports.json"

API_URL = "https://reportapi.eastmoney.com/report/list"
PDF_URL_TMPL = "https://pdf.dfcfw.com/pdf/H3_{info_code}_1.pdf"

TARGET_COUNT = 10          # 要几份
MIN_PAGES, MAX_PAGES = 2, 8  # 只要小篇幅研报：解析快、噪声少、适合学习
LOOKBACK_DAYS = 60         # 往回找多少天
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0 Safari/537.36"),
    "Referer": "https://data.eastmoney.com/report/",
}


def fetch_candidates() -> list[dict]:
    """向东方财富要最近 60 天的个股研报列表（qType=0）。"""
    end = date.today()
    begin = end - timedelta(days=LOOKBACK_DAYS)
    params = {
        "industryCode": "*", "industry": "*",
        "rating": "", "ratingChange": "",
        "beginTime": begin.isoformat(), "endTime": end.isoformat(),
        "pageNo": "1", "pageSize": "100",
        "fields": "", "qType": "0",          # 0 = 个股研报
        "orgCode": "", "code": "*", "rcode": "",
        "p": "1", "pageNum": "1", "pageNumber": "1",
    }
    resp = requests.get(API_URL, params=params, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    payload = resp.json()
    rows = payload.get("data") or []
    print(f"接口返回 {payload.get('hits', 0)} 条，本次取回 {len(rows)} 条")
    return rows


def pick_candidates(rows: list[dict], count: int) -> list[dict]:
    """按「页数合适 + 股票不重复 + 行业尽量不重复」挑出候选。"""
    picked, used_codes, used_industries = [], set(), set()

    def page_ok(row):
        pages = row.get("attachPages") or 0
        return MIN_PAGES <= pages <= MAX_PAGES and row.get("stockName")

    # 第一轮：优先行业不重复，让 10 份文档主题分散，检索时好区分
    for row in rows:
        if len(picked) >= count:
            break
        if not page_ok(row) or row["stockCode"] in used_codes:
            continue
        industry = row.get("indvInduName") or ""
        if industry and industry in used_industries:
            continue
        picked.append(row)
        used_codes.add(row["stockCode"])
        if industry:
            used_industries.add(industry)

    # 第二轮：行业实在不够分散，就用不同股票补齐
    for row in rows:
        if len(picked) >= count:
            break
        if not page_ok(row) or row["stockCode"] in used_codes:
            continue
        picked.append(row)
        used_codes.add(row["stockCode"])

    return picked


def safe_name(text: str) -> str:
    """文件名里去掉空格和路径分隔符，中文保留。"""
    return re.sub(r"[\\/:*?\"<>| ]+", "_", text).strip("_")


def download_one(row: dict, doc_id: str) -> Path | None:
    """下一份 PDF，并做最基本的体检：是不是 PDF、有没有可提取文字。"""
    url = PDF_URL_TMPL.format(info_code=row["infoCode"])
    path = PDF_DIR / f"{doc_id}.pdf"
    if path.exists() and path.stat().st_size > 10_000:
        print(f"  {doc_id:18s} 已存在，复用")
        return path

    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    if not resp.content.startswith(b"%PDF"):
        print(f"  {doc_id:18s} 不是 PDF，跳过")
        return None
    path.write_bytes(resp.content)

    # 扫描版 PDF 提取不出文字，放进知识库只会变成空块，这里直接淘汰
    # 用 PDFium 而不是 pdfplumber：同一份双栏研报，PDFium 能按栏读出干净正文，
    # pdfplumber 会把图表里的坐标轴文字和正文按字符交错拼在一起。
    try:
        pdf = pdfium.PdfDocument(str(path))
        pages = len(pdf)
        text = "".join(pdf[i].get_textpage().get_text_range()
                       for i in range(min(pages, 3)))
    except Exception as exc:
        print(f"  {doc_id:18s} 打不开：{exc}")
        path.unlink(missing_ok=True)
        return None

    if pages < MIN_PAGES or len(text.strip()) < 300:
        print(f"  {doc_id:18s} 文字太少（{len(text.strip())} 字 / {pages} 页），跳过")
        path.unlink(missing_ok=True)
        return None

    print(f"  {doc_id:18s} 下载成功：{pages} 页，前 3 页 {len(text.strip())} 字")
    return path


def main() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    META_PATH.parent.mkdir(parents=True, exist_ok=True)

    if META_PATH.exists():
        reports = json.loads(META_PATH.read_text(encoding="utf-8"))
        if len(reports) >= TARGET_COUNT and all(
                (PDF_DIR / f"{r['doc_id']}.pdf").exists() for r in reports):
            print(f"已有 {len(reports)} 份文档，直接复用 {META_PATH}")
            return

    rows = pick_candidates(fetch_candidates(), TARGET_COUNT)
    if not rows:
        sys.exit("没挑到合适的研报，检查接口参数或换一个时间窗口")

    reports, seq = [], 0
    for row in rows:
        if len(reports) >= TARGET_COUNT:
            break
        seq += 1
        doc_id = f"r{seq:02d}_{safe_name(row['stockName'])}"
        print(f"[{len(reports) + 1}/{TARGET_COUNT}] {row['title']}")
        if download_one(row, doc_id) is None:
            seq -= 1                    # 没下成，编号不算数
            continue
        reports.append({
            "doc_id": doc_id,
            "info_code": row["infoCode"],
            "title": row["title"],
            "stock_name": row["stockName"],
            "stock_code": row["stockCode"],
            "industry": row.get("indvInduName") or "",
            "org": row.get("orgSName") or "",
            "researcher": row.get("researcher") or "",
            "publish_date": (row.get("publishDate") or "")[:10],
            "pages": row.get("attachPages"),
            "pdf": f"data/pdf/{doc_id}.pdf",
        })
        time.sleep(0.4)                 # 别把人家接口打急了

    if len(reports) < TARGET_COUNT:
        print(f"⚠️ 只拿到 {len(reports)} 份，没到 {TARGET_COUNT} 份")

    META_PATH.write_text(
        json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n完成：{len(reports)} 份 PDF → {PDF_DIR}")
    print(f"元数据 → {META_PATH}")


if __name__ == "__main__":
    main()
