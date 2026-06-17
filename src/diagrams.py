"""HTML/CSS (+ minimal inline SVG) bilingual diagram primitives.

Every primitive accepts ``i18n.L`` (or a plain HTML ``str``) and returns an
HTML string. Diagram labels are real DOM text rendered via ``i18n``, so they
follow the 中/EN toggle. Only ``scatter`` uses inline SVG (for geometry); its
human-readable labels stay in HTML (the legend). No third-party dependencies.
"""

import math

import i18n
from i18n import render, t


def fig(body, caption=None):
    """Wrap a diagram body in a figure container with an optional bilingual caption."""
    cap = f'<div class="figcap">{render(caption, block=False)}</div>' if caption is not None else ""
    return f'<div class="fig">{body}{cap}</div>'


def flow(steps, active=None, caption=None):
    """Horizontal boxes joined by arrows. steps: (key, title[, note]); title/note are L/str."""
    cells = []
    for s in steps:
        key, title = s[0], s[1]
        note = s[2] if len(s) > 2 else None
        cls = "fbox on" if key == active else "fbox"
        sub = f'<div class="fsub">{render(note, block=False)}</div>' if note is not None else ""
        cells.append(f'<div class="{cls}"><div class="ft">{render(title, block=False)}</div>{sub}</div>')
    inner = '<div class="farrow" aria-hidden="true">→</div>'.join(cells)
    return fig(f'<div class="frow">{inner}</div>', caption)


def vflow(stages, caption=None):
    """Vertical flow: stage boxes top-to-bottom with down-arrows. stages: (title[, produces])."""
    rows = []
    for i, s in enumerate(stages):
        title = s[0]
        produces = s[1] if len(s) > 1 else None
        prod = f'<span class="fprod">{render(produces, block=False)}</span>' if produces is not None else ""
        rows.append(f'<div class="fvbox"><span class="ft">{render(title, block=False)}</span>{prod}</div>')
        if i < len(stages) - 1:
            rows.append('<div class="fvarrow" aria-hidden="true">↓</div>')
    return fig(f'<div class="fvcol">{"".join(rows)}</div>', caption)


def layers(rows, caption=None):
    """Stacked layers top-to-bottom. rows: (label[, items]); label/items are L/str."""
    out = []
    for r in rows:
        label = r[0]
        items = r[1] if len(r) > 1 else None
        it = f'<span class="flitems">{render(items, block=False)}</span>' if items is not None else ""
        out.append(f'<div class="flayer"><span class="fllabel">{render(label, block=False)}</span>{it}</div>')
    return fig(f'<div class="flstack">{"".join(out)}</div>', caption)


def annot(center, callouts, caption=None):
    """A center node with callout labels around it. callouts: list of (label, desc)."""
    cells = "".join(
        f'<div class="fcall"><div class="fclab">{render(lab, block=False)}</div>'
        f'<div class="fcdesc">{render(desc, block=False)}</div></div>'
        for lab, desc in callouts
    )
    return fig(
        f'<div class="fannot"><div class="fcenter">{render(center, block=False)}</div>'
        f'<div class="fcalls">{cells}</div></div>',
        caption,
    )


def compare2(left, right, caption=None):
    """Two side-by-side panels. left/right = (title, body_html); title is L/str, body raw HTML."""
    lt, lb = left
    rt, rb = right
    return fig(
        f'<div class="fcompare">'
        f'<div class="fcol"><div class="fcoltitle">{render(lt, block=False)}</div>{lb}</div>'
        f'<div class="fvs" aria-hidden="true">vs</div>'
        f'<div class="fcol"><div class="fcoltitle">{render(rt, block=False)}</div>{rb}</div>'
        f"</div>",
        caption,
    )


def grid(headers, cells, caption=None):
    """A visual grid/matrix (styled cards). headers: list of L/str; cells: list of rows of L/str."""
    head = "".join(f'<div class="fgh">{render(h, block=False)}</div>' for h in headers)
    body = ""
    for row in cells:
        body += "".join(f'<div class="fgc">{render(c, block=False)}</div>' for c in row)
    cols = len(headers)
    return fig(
        f'<div class="fgrid" style="grid-template-columns:repeat({cols},1fr)">{head}{body}</div>',
        caption,
    )


def scatter(doc_pts, query_pt, k=3, caption=None):
    """Vector-space scatter (inline SVG). doc_pts: (x, y, label) with x,y in 0..100;
    query_pt: (x, y). Draws doc dots, the query dot, and a circle around the k nearest.
    Each dot's bilingual label surfaces as an SVG ``<title>`` hover tooltip; the
    legend names the three roles (query / nearest top-k / doc chunk)."""
    def _label_text(lab):
        if isinstance(lab, i18n.L):
            txt = f"{lab.zh} / {lab.en}" if lab.en != lab.zh else lab.zh
        else:
            txt = str(lab)
        return txt.replace("&", "&amp;").replace("<", "&lt;")

    qx, qy = query_pt
    dists = sorted((math.hypot(x - qx, y - qy), i) for i, (x, y, _l) in enumerate(doc_pts))
    near = {i for _d, i in dists[:k]}
    radius = dists[k - 1][0] if len(dists) >= k else 0.0
    svg = ['<svg viewBox="0 0 100 100" class="fscatter" preserveAspectRatio="xMidYMid meet" role="img">']
    if radius:
        svg.append(f'<circle cx="{qx}" cy="{qy}" r="{radius:.1f}" class="fsknn"/>')
    for i, (x, y, lab) in enumerate(doc_pts):
        cls = "fsdot near" if i in near else "fsdot"
        svg.append(f'<circle cx="{x}" cy="{y}" r="2.4" class="{cls}"><title>{_label_text(lab)}</title></circle>')
    svg.append(f'<circle cx="{qx}" cy="{qy}" r="3.2" class="fsq"><title>查询 / query</title></circle>')
    svg.append("</svg>")
    legend = (
        '<div class="fslegend">'
        f'<span class="fsl fsl-q">{t("查询", "query")}</span>'
        f'<span class="fsl fsl-near">{t("最近邻 top-k", "nearest top-k")}</span>'
        f'<span class="fsl fsl-doc">{t("文档块", "doc chunks")}</span>'
        "</div>"
    )
    return fig(f'<div class="fscatterwrap">{"".join(svg)}{legend}</div>', caption)


def trace(steps, caption=None):
    """Worked-example trace diagram showing real data flow.

    Args:
        steps: list of (title, value_html) or (title, value_html, note).
            title/note are L/str and follow the 中/EN toggle; title should embed
            its own step number (e.g. "① 原始文本 / Original Text").
            value_html is raw HTML for the green monospace value block.
        caption: Optional bilingual caption "zh / en"

    Returns:
        HTML string with badge + steps + green value blocks
    """
    body = '<div class="trace-badge">🔍 示例 worked example</div>\n'
    body += '<div class="trace">\n'

    for step in steps:
        if len(step) == 2:
            title, value_html = step
            note = None
        else:
            title, value_html, note = step

        body += f'  <h4>{render(title, block=False)}</h4>\n'
        body += f'  <div class="value">{value_html}</div>\n'
        if note:
            body += f'  <small>{render(note, block=False)}</small>\n'

    body += '</div>\n'

    return fig(body, caption)


DIAGRAM_CSS = r"""
/* ===== diagram primitives ===== */
.fig{margin:1.1rem 0;padding:.9rem;background:var(--panel-2);border:1px solid var(--line);
  border-radius:var(--radius);}
.figcap{margin-top:.55rem;font-size:.8rem;color:var(--muted);text-align:center;}
.ft{font-weight:700;font-size:.82rem;color:var(--ink);}
.fsub{font-size:.72rem;color:var(--muted);margin-top:.15rem;}
/* flow (horizontal) */
.frow{display:flex;flex-wrap:wrap;align-items:stretch;gap:.35rem;justify-content:center;}
.fbox{flex:1 1 auto;min-width:5.5em;text-align:center;background:var(--panel);
  border:1px solid var(--line);border-radius:10px;padding:.5rem .55rem;}
.fbox.on{background:var(--accent-soft);border-color:var(--accent);}
.fbox.on .ft{color:var(--accent-ink);}
.farrow{display:flex;align-items:center;color:var(--faint);font-weight:700;}
/* vflow (vertical) */
.fvcol{display:flex;flex-direction:column;align-items:center;gap:.25rem;}
.fvbox{width:min(420px,92%);text-align:center;background:var(--panel);border:1px solid var(--line);
  border-radius:10px;padding:.5rem .6rem;}
.fprod{display:block;font-size:.72rem;color:var(--accent-ink);margin-top:.15rem;}
.fvarrow{color:var(--faint);font-weight:700;line-height:1;}
/* layers */
.flstack{display:flex;flex-direction:column;gap:.3rem;}
.flayer{display:flex;flex-wrap:wrap;align-items:baseline;gap:.5rem;background:var(--panel);
  border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:8px;padding:.5rem .7rem;}
.fllabel{font-weight:700;font-size:.84rem;color:var(--ink);}
.flitems{font-size:.78rem;color:var(--muted);}
/* annot */
.fannot{display:flex;flex-direction:column;align-items:center;gap:.6rem;}
.fcenter{font-weight:700;background:var(--accent);color:#fff;border-radius:10px;padding:.5rem 1rem;}
.fcalls{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.5rem;width:100%;}
.fcall{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:.5rem .6rem;}
.fclab{font-weight:700;font-size:.8rem;color:var(--accent-ink);}
.fcdesc{font-size:.76rem;color:var(--muted);margin-top:.15rem;}
/* compare2 */
.fcompare{display:flex;flex-wrap:wrap;align-items:stretch;gap:.5rem;}
.fcol{flex:1 1 240px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:.6rem .7rem;}
.fcoltitle{font-weight:700;font-size:.84rem;margin-bottom:.35rem;color:var(--accent-ink);}
.fvs{display:flex;align-items:center;justify-content:center;color:var(--faint);font-weight:700;font-style:italic;}
/* grid */
.fgrid{display:grid;gap:.3rem;}
.fgh{font-weight:700;font-size:.78rem;background:var(--accent-soft);color:var(--accent-ink);
  border-radius:6px;padding:.35rem .5rem;text-align:center;}
.fgc{font-size:.78rem;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:.4rem .5rem;}
/* scatter (svg) */
.fscatterwrap{display:flex;flex-direction:column;align-items:center;gap:.5rem;}
.fscatter{width:min(280px,80%);height:auto;background:var(--panel);border:1px solid var(--line);border-radius:10px;}
.fsdot{fill:var(--faint);}
.fsdot.near{fill:var(--accent);}
.fsq{fill:var(--amber);stroke:#fff;stroke-width:.6;}
.fsknn{fill:var(--accent-soft);stroke:var(--accent);stroke-width:.7;opacity:.55;}
.fslegend{display:flex;flex-wrap:wrap;gap:.7rem;font-size:.74rem;color:var(--muted);}
.fsl{display:inline-flex;align-items:center;gap:.3rem;}
.fsl::before{content:"";width:.7rem;height:.7rem;border-radius:50%;display:inline-block;}
.fsl-q::before{background:var(--amber);}
.fsl-near::before{background:var(--accent);}
.fsl-doc::before{background:var(--faint);}
"""
