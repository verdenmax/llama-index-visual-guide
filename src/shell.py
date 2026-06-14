"""Shared HTML shell (CSS design system + nav + language toggle) for the
LlamaIndex RAG visual guide. No third-party dependencies."""

import base64

import diagrams
import i18n
from i18n import L

_FAVICON_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
    "<rect width='32' height='32' rx='7' fill='#1a7f64'/>"
    "<text x='16' y='23' font-family='system-ui,sans-serif' font-size='17'"
    " font-weight='700' fill='#fff' text-anchor='middle'>Li</text></svg>"
)
FAVICON = "data:image/svg+xml;base64," + base64.b64encode(_FAVICON_SVG.encode()).decode()
SITE = "LlamaIndex RAG 图解教程"


def _attr(s):
    return s.replace('"', "&quot;")


def head_meta(title, description, og_type="website"):
    t = title.replace('"', "&quot;")
    d = description.replace('"', "&quot;")
    return (
        f'<meta name="description" content="{d}">\n'
        f'<meta name="theme-color" content="#1a7f64">\n'
        f'<link rel="icon" type="image/svg+xml" href="{FAVICON}">\n'
        f'<meta property="og:type" content="{og_type}">\n'
        f'<meta property="og:site_name" content="{SITE}">\n'
        f'<meta property="og:title" content="{t}">\n'
        f'<meta property="og:description" content="{d}">\n'
        f'<meta name="twitter:card" content="summary">'
    )


P1 = L("第一部分 · 宏观全景", "Part 1 · Big Picture")
P2 = L("第二部分 · 写入路径", "Part 2 · Write Path")
P3 = L("第三部分 · 查询路径", "Part 3 · Query Path")
P4 = L("第四部分 · 进阶", "Part 4 · Advanced")
P5 = L("第五部分 · 实战", "Part 5 · Capstone")
P6 = L("第六部分 · 速查", "Part 6 · Reference")

PAGES = [
    ("01-what-is-llamaindex.html", L("LlamaIndex 与 RAG 是什么", "What is LlamaIndex &amp; RAG"), P1),
    ("02-architecture.html", L("架构全景", "Architecture Overview"), P1),
    ("03-rag-lifecycle.html", L("一次 RAG 的生命周期", "Lifecycle of a RAG Query"), P1),
    ("04-documents-nodes.html", L("Document 与 Node 数据模型", "Documents &amp; Nodes"), P2),
    ("05-readers.html", L("数据加载 Readers", "Loading Data: Readers"), P2),
    ("06-node-parsers.html", L("切块 Node Parsers", "Chunking: Node Parsers"), P2),
    ("07-metadata-extractors.html", L("元数据与抽取器", "Metadata &amp; Extractors"), P2),
    ("08-embeddings.html", L("Embedding 向量化", "Embeddings"), P2),
    ("09-vector-stores.html", L("向量存储 Vector Stores", "Vector Stores"), P2),
    ("10-index-abstraction.html", L("索引 Index 抽象", "The Index Abstraction"), P2),
    ("11-ingestion-storage.html", L("Ingestion 管道与持久化", "Ingestion &amp; Storage"), P2),
    ("12-retrievers.html", L("检索器 Retrievers", "Retrievers"), P3),
    ("13-postprocessors.html", L("节点后处理 Postprocessors", "Node Postprocessors"), P3),
    ("14-response-synthesizers.html", L("响应合成 Response Synthesizers", "Response Synthesizers"), P3),
    ("15-query-engine.html", L("查询引擎 Query Engine", "Query Engines"), P3),
    ("16-chat-engine.html", L("聊天引擎 Chat Engine", "Chat Engines"), P3),
    ("17-settings-prompts.html", L("全局配置 Settings 与 Prompt", "Settings &amp; Prompts"), P4),
    ("18-advanced-retrieval.html", L("进阶检索", "Advanced Retrieval"), P4),
    ("19-evaluation.html", L("评估 Evaluation", "Evaluation"), P4),
    ("20-capstone.html", L("端到端 Capstone", "End-to-End Capstone"), P5),
    ("21-glossary.html", L("术语表 · 概念索引", "Glossary &amp; Concept Index"), P6),
]

INDEX_FILE = "index.html"

SUBTITLES = {
    "01-what-is-llamaindex.html": L("为什么需要 RAG · 核心心智模型", "Why RAG · core mental model"),
    "02-architecture.html": L("core + 集成分层 · 命名约定", "core + integrations · import naming"),
    "03-rag-lifecycle.html": L("5 行跑通 · 写入 vs 查询数据流", "5-line demo · write vs query flow"),
    "04-documents-nodes.html": L("Document / TextNode · relationships · metadata", "Document / TextNode · relationships · metadata"),
    "05-readers.html": L("SimpleDirectoryReader · LlamaHub", "SimpleDirectoryReader · LlamaHub"),
    "06-node-parsers.html": L("Sentence / Token / Semantic · chunk_size", "Sentence / Token / Semantic · chunk_size"),
    "07-metadata-extractors.html": L("Title / Keyword / QA 抽取器", "Title / Keyword / QA extractors"),
    "08-embeddings.html": L("BaseEmbedding · 语义检索原理", "BaseEmbedding · semantic search"),
    "09-vector-stores.html": L("VectorStoreIndex · 集成", "VectorStoreIndex · integrations"),
    "10-index-abstraction.html": L("Vector / Summary / Graph 索引", "Vector / Summary / Graph indices"),
    "11-ingestion-storage.html": L("IngestionPipeline · persist / load", "IngestionPipeline · persist / load"),
    "12-retrievers.html": L("VectorIndexRetriever · top-k", "VectorIndexRetriever · top-k"),
    "13-postprocessors.html": L("相似度过滤 · rerank", "similarity cutoff · rerank"),
    "14-response-synthesizers.html": L("refine / compact / tree_summarize", "refine / compact / tree_summarize"),
    "15-query-engine.html": L("RetrieverQueryEngine · as_query_engine", "RetrieverQueryEngine · as_query_engine"),
    "16-chat-engine.html": L("Context / CondenseQuestion · 记忆", "Context / CondenseQuestion · memory"),
    "17-settings-prompts.html": L("Settings 取代 ServiceContext · PromptTemplate", "Settings replaces ServiceContext · PromptTemplate"),
    "18-advanced-retrieval.html": L("Fusion / AutoMerging / Router", "Fusion / AutoMerging / Router"),
    "19-evaluation.html": L("Faithfulness / Relevancy / Correctness", "Faithfulness / Relevancy / Correctness"),
    "20-capstone.html": L("把所有阶段拼成可跑的 RAG 应用", "assemble every stage into a runnable app"),
    "21-glossary.html": L("术语一句话查 + 跳转", "one-line term lookup + jump"),
}

CSS = r"""
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #f6f7f9; --panel: #ffffff; --panel-2: #f0f2f5; --ink: #1d2129;
  --muted: #5b6470; --faint: #8a939f; --line: #e1e5ea;
  --accent: #1a7f64; --accent-soft: #e4f3ee; --accent-ink: #0f5c48;
  --blue: #2563eb; --blue-soft: #e7efff; --amber: #b4690e; --amber-soft: #fdf1dd;
  --purple: #7c3aed; --purple-soft: #f0e9ff; --red: #d23f3f; --red-soft: #fbe6e6;
  --code-bg: #0f172a; --code-ink: #e2e8f0; --code-line: #1e293b;
  --shadow: 0 1px 2px rgba(16,24,40,.06), 0 8px 24px rgba(16,24,40,.06);
  --radius: 14px;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0e1116; --panel: #161b22; --panel-2: #1c232c; --ink: #e6edf3;
    --muted: #9aa6b2; --faint: #6e7a86; --line: #2a323c;
    --accent: #3fb892; --accent-soft: #14302a; --accent-ink: #8ee0c6;
    --blue: #6ea8fe; --blue-soft: #16243f; --amber: #e0a44a; --amber-soft: #33270f;
    --purple: #b794f6; --purple-soft: #271a40; --red: #f08080; --red-soft: #3a1a1a;
    --code-bg: #0a0f1a; --code-ink: #d8e2f0; --code-line: #14202f;
    --shadow: 0 1px 2px rgba(0,0,0,.4), 0 10px 30px rgba(0,0,0,.35);
  }
}
html { scroll-behavior: smooth; overflow-x: hidden; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC",
    "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
  background: var(--bg); color: var(--ink); line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--accent); text-decoration: none; }
code, .mono { font-family: "SF Mono", "JetBrains Mono", "Fira Code", ui-monospace, Menlo, Consolas, monospace; overflow-wrap: break-word; }

/* ---- top progress bar ---- */
.topbar {
  position: sticky; top: 0; z-index: 50; background: var(--panel);
  border-bottom: 1px solid var(--line); backdrop-filter: blur(8px);
}
.topbar-inner {
  max-width: 960px; margin: 0 auto; padding: .7rem 1.25rem;
  display: flex; align-items: center; justify-content: space-between; gap: 1rem;
}
.topbar .home { font-size: .82rem; color: var(--muted); font-weight: 600; display:flex; gap:.5rem; align-items:center; }
.topbar .home b { color: var(--accent); }
.topbar .pill { font-size: .72rem; color: var(--muted); background: var(--panel-2);
  padding: .2rem .6rem; border-radius: 999px; border: 1px solid var(--line); white-space: nowrap; }
.progress { height: 3px; background: var(--panel-2); }
.progress > span { display: block; height: 100%; background: linear-gradient(90deg, var(--accent), var(--blue)); }

.wrap { max-width: 820px; margin: 0 auto; padding: 2.4rem 1.25rem 5rem; }

/* ---- hero ---- */
.hero { margin-bottom: 2rem; }
.hero .part { font-size: .76rem; letter-spacing: .08em; text-transform: uppercase;
  color: var(--accent); font-weight: 700; margin-bottom: .55rem; }
.hero h1 { font-size: 2.05rem; line-height: 1.2; letter-spacing: -.01em; font-weight: 750; }
.hero .lead { margin-top: .9rem; font-size: 1.06rem; color: var(--muted); }

h2 { font-size: 1.32rem; margin: 2.4rem 0 .9rem; letter-spacing: -.01em;
  display: flex; align-items: center; gap: .55rem; }
h2::before { content: ""; width: 4px; height: 1.05em; background: var(--accent); border-radius: 3px; display: inline-block; }
h3 { font-size: 1.05rem; margin: 1.4rem 0 .5rem; }
p { margin: .7rem 0; }
ul, ol { margin: .6rem 0 .6rem 1.3rem; }
li { margin: .3rem 0; }
strong { color: var(--ink); font-weight: 680; }
.inline { background: var(--panel-2); border: 1px solid var(--line); border-radius: 6px;
  padding: .08em .4em; font-size: .9em; color: var(--accent-ink); }

/* ---- callout cards ---- */
.card { border-radius: var(--radius); padding: 1.05rem 1.2rem; margin: 1.2rem 0;
  border: 1px solid var(--line); background: var(--panel); box-shadow: var(--shadow); }
.card .tag { font-size: .72rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase;
  display: inline-flex; align-items: center; gap: .4rem; margin-bottom: .5rem; }
.card.macro { border-left: 4px solid var(--blue); }
.card.macro .tag { color: var(--blue); }
.card.detail { border-left: 4px solid var(--purple); }
.card.detail .tag { color: var(--purple); }
.card.analogy { border-left: 4px solid var(--amber); background: var(--amber-soft); }
.card.analogy .tag { color: var(--amber); }
.card.key { border-left: 4px solid var(--accent); background: var(--accent-soft); }
.card.key .tag { color: var(--accent-ink); }
.card.warn { border-left: 4px solid var(--red); background: var(--red-soft); }
.card.warn .tag { color: var(--red); }
.card.spark { border-left: 4px solid #e0a000;
  background: linear-gradient(100deg, rgba(224,160,0,.12), transparent 70%); }
.card.spark .tag { color: #c98a00; }
@media (prefers-color-scheme: dark) { .card.spark .tag { color: #f0c050; } }

/* ---- code file callout ---- */
.codefile { margin: 1.2rem 0; border-radius: 12px; overflow: hidden; border: 1px solid var(--line);
  box-shadow: var(--shadow); }
.codefile .cf-head { display: flex; align-items: center; gap: .55rem; padding: .5rem .85rem;
  background: var(--panel-2); border-bottom: 1px solid var(--line); font-size: .8rem; }
.codefile .cf-head .dot { width: 9px; height: 9px; border-radius: 50%; background: var(--accent); flex-shrink:0; }
.codefile .cf-head .path { font-family: ui-monospace, monospace; color: var(--ink); font-weight: 600; }
.codefile .cf-head .ln { margin-left: auto; color: var(--faint); font-size: .72rem; }
.codefile pre { background: var(--code-bg); color: var(--code-ink); padding: .9rem 1rem;
  overflow-x: auto; font-size: .82rem; line-height: 1.6; }
.codefile pre .cm { color: #7d8aa3; }
.codefile pre .kw { color: #c792ea; }
.codefile pre .fn { color: #82aaff; }
.codefile pre .st { color: #c3e88d; }
.codefile pre .nb { color: #f78c6c; }

pre.code { background: var(--code-bg); color: var(--code-ink); padding: .9rem 1rem; border-radius: 12px;
  overflow-x: auto; font-size: .83rem; line-height: 1.6; margin: 1.1rem 0; box-shadow: var(--shadow); }
pre.code .cm { color: #7d8aa3; } pre.code .kw { color: #c792ea; }
pre.code .fn { color: #82aaff; } pre.code .st { color: #c3e88d; } pre.code .nb { color: #f78c6c; }

/* ---- collapsible accordion (details/summary) ---- */
.accordion { border: 1px solid var(--line); border-radius: 12px; background: var(--panel);
  margin: .7rem 0; box-shadow: var(--shadow); overflow: hidden; }
.accordion > summary { cursor: pointer; padding: .85rem 1.1rem; font-weight: 650; font-size: .96rem;
  list-style: none; display: flex; align-items: center; gap: .6rem; user-select: none; }
.accordion > summary::-webkit-details-marker { display: none; }
.accordion > summary::after { content: "▶"; font-size: .68rem; color: var(--accent);
  margin-left: auto; transition: transform .15s ease; }
.accordion[open] > summary::after { transform: rotate(90deg); }
.accordion > summary:hover { background: var(--panel-2); }
.accordion[open] > summary { border-bottom: 1px solid var(--line); }
.accordion .badge-num { background: var(--accent-soft); color: var(--accent-ink);
  width: 1.6rem; height: 1.6rem; border-radius: 7px; display: inline-flex; align-items: center;
  justify-content: center; font-size: .82rem; font-weight: 700; flex-shrink: 0; }
.accordion .hint { font-size: .72rem; color: var(--faint); font-weight: 400; }
.acc-body { padding: .9rem 1.1rem 1.1rem; }
.acc-intro { color: var(--muted); font-size: .9rem; margin: .2rem 0 .4rem; }
.qa { margin: 1rem 0; }
.qa:first-child { margin-top: .3rem; }
.qa .q { font-weight: 680; font-size: .9rem; display: flex; gap: .45rem; align-items: center; margin-bottom: .3rem; }
.qa .a { color: var(--muted); font-size: .9rem; }
.qa .a strong { color: var(--ink); }
.qa pre.code { margin: .5rem 0 0; font-size: .78rem; }

/* ---- flow diagram ---- */
.flow { display: flex; align-items: stretch; gap: 0; flex-wrap: wrap; margin: 1.3rem 0;
  background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius);
  padding: 1.2rem 1rem; box-shadow: var(--shadow); }
.flow .node { flex: 1 1 0; min-width: 110px; text-align: center; padding: .7rem .5rem;
  border-radius: 10px; background: var(--panel-2); border: 1px solid var(--line); }
.flow .node .nt { font-weight: 700; font-size: .92rem; }
.flow .node .nd { font-size: .76rem; color: var(--muted); margin-top: .2rem; }
.flow .node.hl { background: var(--accent-soft); border-color: var(--accent); }
.flow .arrow { align-self: center; color: var(--faint); font-size: 1.3rem; padding: 0 .35rem; }

/* vertical flow */
.vflow { margin: 1.3rem 0; }
.vflow .step { display: flex; gap: .9rem; position: relative; padding-bottom: 1.1rem; }
.vflow .step:not(:last-child)::before { content:""; position:absolute; left: 15px; top: 34px; bottom: -2px;
  width: 2px; background: var(--line); }
.vflow .num { width: 32px; height: 32px; border-radius: 50%; background: var(--accent); color: #fff;
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: .85rem; flex-shrink: 0; z-index:1; }
.vflow .sc h4 { margin: .25rem 0 .2rem; font-size: 1rem; }
.vflow .sc p { margin: .15rem 0; font-size: .92rem; color: var(--muted); }
.vflow .sc .mono { font-size: .8rem; color: var(--accent-ink); }

/* layered architecture */
.layers { margin: 1.3rem 0; display: flex; flex-direction: column; gap: .55rem; }
.layer { border-radius: 12px; padding: .85rem 1.1rem; border: 1px solid var(--line); background: var(--panel);
  box-shadow: var(--shadow); }
.layer .lh { display: flex; align-items: center; gap: .6rem; }
.layer .lh .badge { font-size: .7rem; font-weight: 700; padding: .12rem .5rem; border-radius: 999px; }
.layer .lh .name { font-weight: 700; font-family: ui-monospace, monospace; }
.layer .ld { font-size: .85rem; color: var(--muted); margin-top: .35rem; }
.layer.l-core { border-left: 4px solid var(--accent); } .layer.l-core .badge { background: var(--accent-soft); color: var(--accent-ink); }
.layer.l-main { border-left: 4px solid var(--blue); } .layer.l-main .badge { background: var(--blue-soft); color: var(--blue); }
.layer.l-part { border-left: 4px solid var(--purple); } .layer.l-part .badge { background: var(--purple-soft); color: var(--purple); }
.layer.l-app { border-left: 4px solid var(--amber); } .layer.l-app .badge { background: var(--amber-soft); color: var(--amber); }

/* two-column compare */
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.2rem 0; }
@media (max-width: 640px) { .cols { grid-template-columns: 1fr; } }
.col { background: var(--panel); border: 1px solid var(--line); border-radius: 12px; padding: 1rem 1.1rem; box-shadow: var(--shadow); min-width: 0; }
.col h4 { margin: 0 0 .4rem; font-size: .95rem; }

table.t { width: 100%; border-collapse: collapse; margin: 1.1rem 0; font-size: .9rem;
  background: var(--panel); border-radius: 12px; overflow: hidden; box-shadow: var(--shadow); }
table.t th, table.t td { padding: .6rem .8rem; text-align: left; border-bottom: 1px solid var(--line); }
table.t th { background: var(--panel-2); font-size: .8rem; letter-spacing: .02em; }
table.t tr:last-child td { border-bottom: none; }
table.t td.mono, table.t td .mono { font-family: ui-monospace, monospace; font-size: .82rem; color: var(--accent-ink); }
@media (max-width: 640px) {
  /* Wide multi-column tables: scroll within their own box instead of
     forcing page-level horizontal overflow (which clipped right columns). */
  table.t { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }
  table.t th, table.t td { padding: .5rem .6rem; }
}
.selftest { margin: 2.2rem 0 0; border-top: 2px dashed var(--line); padding-top: 1.2rem; }
.selftest > h2 { margin-top: .2rem; }
.quiz { background: var(--panel); border: 1px solid var(--line); border-left: 4px solid var(--blue);
  border-radius: 12px; padding: .9rem 1.1rem; margin: 1rem 0; box-shadow: var(--shadow); }
.quiz .qn { font-weight: 650; }
.quiz ol.opts { list-style: upper-alpha; margin: .55rem 0 .6rem 1.5rem; padding: 0; }
.quiz ol.opts li { margin: .3rem 0; padding-left: .15rem; }
.quiz details.accordion { margin: .5rem 0 0; }
.selftest code { font-family: ui-monospace, monospace; font-size: .9em; color: var(--accent-ink);
  background: var(--accent-soft); padding: 0 .28em; border-radius: 4px; }

/* footer nav */
.footnav { display: flex; justify-content: space-between; gap: 1rem; margin-top: 3rem;
  padding-top: 1.4rem; border-top: 1px solid var(--line); }
.footnav a { flex: 1; padding: .85rem 1.1rem; border-radius: 12px; border: 1px solid var(--line);
  background: var(--panel); box-shadow: var(--shadow); transition: .15s; }
.footnav a:hover { border-color: var(--accent); transform: translateY(-1px); }
.footnav a.next { text-align: right; }
.footnav .dir { font-size: .72rem; color: var(--faint); text-transform: uppercase; letter-spacing: .05em; }
.footnav .ttl { font-weight: 700; color: var(--ink); margin-top: .15rem; }
.footnav a.disabled { opacity: .35; pointer-events: none; }

/* index page */
.toc { display: grid; gap: .7rem; margin-top: 1.6rem; }
.toc-part { font-size: .78rem; font-weight: 700; letter-spacing: .05em; text-transform: uppercase;
  color: var(--accent); margin: 1.4rem 0 .2rem; }
.toc a { display: flex; align-items: center; gap: .9rem; padding: .85rem 1.05rem; border-radius: 12px;
  background: var(--panel); border: 1px solid var(--line); box-shadow: var(--shadow); transition: .15s; }
.toc a:hover { border-color: var(--accent); transform: translateX(3px); }
.toc .n { width: 30px; height: 30px; border-radius: 8px; background: var(--accent-soft); color: var(--accent-ink);
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: .85rem; flex-shrink: 0; }
.toc .tt { font-weight: 650; color: var(--ink); }
.toc .ts { font-size: .8rem; color: var(--muted); margin-left: auto; text-align: right; }
.toc-search { position: relative; margin: 1.6rem 0 -.4rem; }
.toc-search input { width: 100%; box-sizing: border-box; padding: .75rem 2.8rem .75rem 1rem;
  border-radius: 12px; border: 1px solid var(--line); background: var(--panel); color: var(--ink);
  font-size: .98rem; box-shadow: var(--shadow); }
.toc-search input:focus { outline: none; border-color: var(--accent); }
.toc-search .qcount { position: absolute; right: 1rem; top: 50%; transform: translateY(-50%);
  color: var(--faint); font-size: .8rem; pointer-events: none; }
.toc a.hide, .toc .toc-part.hide { display: none; }
.toc-empty { display: none; color: var(--muted); padding: 1rem; text-align: center; }
.toc-empty.show { display: block; }
.hero.index h1 { font-size: 2.3rem; }
.legend { display:flex; gap:1.2rem; flex-wrap:wrap; margin-top:1rem; font-size:.8rem; color:var(--muted); }
.legend span { display:flex; align-items:center; gap:.4rem; }
.legend i { width:12px; height:12px; border-radius:3px; display:inline-block; }
.pdf-btn { display:inline-flex; align-items:center; gap:.4rem; padding:.55rem 1.1rem;
  background:var(--accent); color:#fff; border-radius:10px; font-size:.9rem; font-weight:650;
  box-shadow:var(--shadow); transition:.15s; }
.pdf-btn:hover { background:var(--accent-ink); transform:translateY(-1px); }
"""

EXTRA_CSS = r"""
/* ---- language toggle button ---- */
.langbtn{font:600 .72rem/1 inherit;color:var(--accent);background:var(--accent-soft);
  border:1px solid var(--accent);border-radius:999px;padding:.28rem .6rem;cursor:pointer;}
.langbtn:hover{background:var(--accent);color:#fff;}
/* ---- RAG pipeline strip ---- */
.pipeline{display:flex;flex-direction:column;gap:.4rem;margin:.2rem 0 1.4rem;
  padding:.8rem .9rem;background:var(--panel-2);border:1px solid var(--line);border-radius:var(--radius);}
.flowrow{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem;}
.flowlabel{font-size:.72rem;font-weight:700;color:var(--muted);min-width:5.2em;}
.stage{font-size:.74rem;padding:.2rem .55rem;border-radius:999px;background:var(--panel);
  border:1px solid var(--line);color:var(--faint);white-space:nowrap;}
.stage.on{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700;}
/* ---- code caption + key-points / highlight cards ---- */
.codewrap{margin:1rem 0;}
.cf-head{font-size:.78rem;color:var(--muted);margin-bottom:.3rem;}
.card.keypts{border-left:3px solid var(--accent);}
.card.highlight{border-left:3px solid var(--amber);background:var(--amber-soft);}
"""


def page(filename, content, home_href="../index.html"):
    idx = next(i for i, p in enumerate(PAGES) if p[0] == filename)
    _f, title, part = PAGES[idx]
    total = len(PAGES)
    pct = int((idx + 1) / total * 100)
    num = f"{idx + 1:02d}"

    def navlink(cls, target, dir_zh, dir_en, ttl):
        return (
            f'<a class="{cls}" href="{target}">'
            f'<div class="dir">{i18n.t(dir_zh, dir_en)}</div>'
            f'<div class="ttl">{i18n.render(ttl, block=False)}</div></a>'
        )

    if idx > 0:
        prev_link = navlink("prev", PAGES[idx - 1][0], "← 上一课", "← Prev", PAGES[idx - 1][1])
    else:
        prev_link = navlink("prev", home_href, "← 返回", "← Back", L("目录", "Contents"))
    if idx + 1 < total:
        next_link = navlink("next", PAGES[idx + 1][0], "下一课 →", "Next →", PAGES[idx + 1][1])
    else:
        next_link = navlink("next", home_href, "完成 →", "Done →", L("返回目录", "Back to contents"))

    title_zh = f"{num} · {title.zh} — {SITE}"
    title_en = f"{num} · {title.en} — LlamaIndex RAG Visual Guide"
    desc = f"{part.zh}｜{title.zh}：面向新手的 LlamaIndex RAG 图解教程，配真实源码对应、可运行代码与设计亮点。"
    home_label = i18n.t(f"🦙 {SITE} · 目录", "🦙 LlamaIndex RAG Visual Guide · Contents")
    return f"""<!DOCTYPE html>
<html lang="zh-CN" data-uilang="zh" data-title-zh="{_attr(title_zh)}" data-title-en="{_attr(title_en)}"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_zh}</title>
{head_meta(title_zh, desc, og_type="article")}
<style>{CSS}{EXTRA_CSS}{diagrams.DIAGRAM_CSS}{i18n.LANG_CSS}</style>
</head><body>
<div class="topbar">
  <div class="topbar-inner">
    <a class="home" href="{home_href}">{home_label}</a>
    <span class="pill">{i18n.render(part, block=False)}</span>
    <span class="pill">{num} / {total:02d}</span>
    <button class="langbtn" type="button" data-lang-toggle aria-label="Switch to English">EN</button>
  </div>
  <div class="progress"><span style="width:{pct}%"></span></div>
</div>
<div class="wrap">
  <div class="hero">
    <div class="part">{i18n.render(part, block=False)}</div>
    <h1>{i18n.render(title, block=False)}</h1>
  </div>
  {content}
  <div class="footnav">{prev_link}{next_link}</div>
</div>
<script>{i18n.LANG_TOGGLE_JS}</script>
</body></html>"""


def index_page(lesson_prefix=""):
    parts, order = {}, []
    for i, (fname, title, part) in enumerate(PAGES):
        key = part.zh
        if key not in parts:
            parts[key] = (part, [])
            order.append(key)
        parts[key][1].append((i + 1, fname, title))

    blocks = []
    for key in order:
        part, items = parts[key]
        blocks.append(f'<div class="toc-part">{i18n.render(part, block=False)}</div>')
        for num, fname, title in items:
            sub = SUBTITLES.get(fname, L("", ""))
            blocks.append(
                f'<a href="{lesson_prefix}{fname}"><span class="n">{num:02d}</span>'
                f'<span class="tt">{i18n.render(title, block=False)}</span>'
                f'<span class="ts">{i18n.render(sub, block=False)}</span></a>'
            )
    toc = "\n".join(blocks)
    total = len(PAGES)
    nparts = len(order)
    count_pill = i18n.t(f"共 {total} 课 · {nparts} 个部分", f"{total} lessons · {nparts} parts")
    home_label = i18n.t(f"🦙 {SITE}", "🦙 LlamaIndex RAG Visual Guide")
    hero_part = i18n.t("从零开始 · 跟着数据流学 RAG", "From scratch · learn RAG by following the data")
    hero_h1 = i18n.render(
        L("用图解一步步理解 LlamaIndex 的 RAG", "Understand LlamaIndex RAG, step by step"),
        block=False,
    )
    hero_lead = i18n.render(L(
        "这套教程跟着<strong>两条数据流</strong>带你走：先看一份文档如何<strong>写入索引</strong>"
        "（加载→切块→Embedding→存储→索引），再看一个问题如何<strong>查出答案</strong>"
        "（检索→后处理→合成→回答）。每课都配真实源码对应、可运行代码与设计亮点。",
        "This guide follows <strong>two data flows</strong>: how a document gets <strong>written into "
        "an index</strong> (load→split→embed→store→index), then how a question gets <strong>answered"
        "</strong> (retrieve→post-process→synthesize→answer). Every lesson maps to real source, runnable "
        "code and a design insight.",
    ))
    pdf_btn = i18n.t(f"📄 下载完整 PDF（全 {total} 课）", f"📄 Download full PDF ({total} lessons)")
    anchor = i18n.render(L(
        "📌 对照 <strong>llama-index-core 0.14.22</strong> / Python 3.10+ · 最后核验 2026-06 · "
        "源码引用以「文件 + 符号名」为主（行号随上游更新而变）",
        "📌 Anchored to <strong>llama-index-core 0.14.22</strong> / Python 3.10+ · verified 2026-06 · "
        "source cited as “file · symbol” (line numbers drift upstream)",
    ))
    desc = "跟着写入路径与查询路径，一步步理解 LlamaIndex 的 RAG：21 课，每课配真实源码对应、可运行代码与设计亮点。"
    return f"""<!DOCTYPE html>
<html lang="zh-CN" data-uilang="zh" data-title-zh="{_attr(SITE + ' · 从数据流理解 RAG')}" data-title-en="{_attr('LlamaIndex RAG Visual Guide')}"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{SITE} · 从数据流理解 RAG</title>
{head_meta(SITE + " · 从数据流理解 RAG", desc, og_type="website")}
<style>{CSS}{EXTRA_CSS}{diagrams.DIAGRAM_CSS}{i18n.LANG_CSS}</style>
</head><body>
<div class="topbar">
  <div class="topbar-inner">
    <span class="home">{home_label}</span>
    <span class="pill">{count_pill}</span>
    <button class="langbtn" type="button" data-lang-toggle aria-label="Switch to English">EN</button>
  </div>
  <div class="progress"><span style="width:100%"></span></div>
</div>
<div class="wrap">
  <div class="hero index">
    <div class="part">{hero_part}</div>
    <h1>{hero_h1}</h1>
    <p class="lead">{hero_lead}</p>
    <div style="margin-top:1.1rem">
      <a href="llama-index-visual-guide.pdf" class="pdf-btn">{pdf_btn}</a>
    </div>
    <p style="margin:.8rem 0 0;color:var(--faint);font-size:.8rem">{anchor}</p>
  </div>
  <div class="toc">{toc}</div>
</div>
<script>{i18n.LANG_TOGGLE_JS}</script>
</body></html>"""
