"""DRY, bilingual building blocks for lesson pages.

Every helper accepts an :class:`i18n.L` (or a plain HTML ``str``) and returns
an HTML string. Block-level text is rendered as paired ``data-lang`` ``<div>``;
inline text (titles, labels, table cells, list items) as paired ``<span>``.
"""

from i18n import render, t


def lead(text):
    return f'<p class="lead">{render(text, block=False)}</p>'


def analogy(text):
    tag = t("🧩 生活类比", "🧩 Analogy")
    return f'<div class="card analogy"><div class="tag">{tag}</div>{render(text)}</div>'


def section(title, *blocks):
    body = "".join(render(b) for b in blocks)
    return f"<h2>{render(title, block=False)}</h2>{body}"


def compare_table(headers, rows):
    th = "".join(f"<th>{render(h, block=False)}</th>" for h in headers)
    body = ""
    for row in rows:
        tds = "".join(f"<td>{render(cell, block=False)}</td>" for cell in row)
        body += f"<tr>{tds}</tr>"
    return f'<table class="t"><tr>{th}</tr>{body}</table>'


def source_ref(path, symbol, note=None):
    tag = t("🔬 源码对应", "🔬 In the source")
    label = f"<code>{path}</code> · <code>{symbol}</code>"
    extra = f" — {render(note, block=False)}" if note is not None else ""
    return f'<div class="card codefile"><div class="tag">{tag}</div>{label}{extra}</div>'


def code(snippet, caption=None):
    head = f'<div class="cf-head">{render(caption, block=False)}</div>' if caption else ""
    return f'<div class="codewrap">{head}<pre class="code">{snippet}</pre></div>'


def key_points(items):
    tag = t("✅ 本课要点", "✅ Key points")
    lis = "".join(f"<li>{render(it, block=False)}</li>" for it in items)
    return f'<div class="card keypts"><div class="tag">{tag}</div><ul>{lis}</ul></div>'


def design_highlight(text):
    tag = t("💡 设计亮点", "💡 Design insight")
    return f'<div class="card highlight"><div class="tag">{tag}</div>{render(text)}</div>'


def qa_item(label, body):
    return (
        f'<div class="qa"><div class="q">{render(label, block=False)}</div>'
        f'<div class="a">{render(body)}</div></div>'
    )


def accordion(summary, *items):
    hint = t("点击展开", "expand")
    body = "".join(items)
    return (
        f'<details class="accordion"><summary>{render(summary, block=False)}'
        f'<span class="hint">{hint}</span></summary>'
        f'<div class="acc-body">{body}</div></details>'
    )


# The RAG pipeline strip; ``stage`` highlights one step (or None).
_WRITE = [
    ("load", "加载", "Load"), ("split", "切块", "Split"), ("embed", "Embed", "Embed"),
    ("store", "存储", "Store"), ("index", "索引", "Index"),
]
_QUERY = [
    ("retrieve", "检索", "Retrieve"), ("postprocess", "后处理", "Post-process"),
    ("synthesize", "合成", "Synthesize"), ("answer", "回答", "Answer"),
]


def _strip(items, label_zh, label_en, stage):
    cells = ""
    for key, zh, en in items:
        cls = "stage on" if key == stage else "stage"
        cells += f'<span class="{cls}">{t(zh, en)}</span>'
    return f'<div class="flowrow"><span class="flowlabel">{t(label_zh, label_en)}</span>{cells}</div>'


def pipeline(stage):
    return (
        '<div class="pipeline">'
        + _strip(_WRITE, "写入路径", "Write path", stage)
        + _strip(_QUERY, "查询路径", "Query path", stage)
        + "</div>"
    )
