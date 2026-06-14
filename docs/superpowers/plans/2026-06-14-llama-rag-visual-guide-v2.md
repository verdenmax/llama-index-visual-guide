# LlamaIndex RAG Visual Guide — v2 (Diagrams + Depth) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Upgrade the existing 21-lesson guide into a true "图解 + 详尽" tutorial: a reusable bilingual HTML/CSS (+minimal SVG) diagram system, then 2–3 diagrams + an expandable deep-dive + a 2nd code example per lesson, lifting each lesson to ~6–8k visible chars.

**Architecture:** New `src/diagrams.py` provides bilingual diagram primitives (`fig`, `flow`, `vflow`, `layers`, `annot`, `compare2`, `grid`, `scatter`) returning HTML strings whose labels render via `i18n` (so they follow the 中/EN toggle). Its `DIAGRAM_CSS` is injected by `shell.py` + `build_print.py`. Content modules (`part1..5.py`, `glossary.py`) `import diagrams as d` and are rewritten per the v2 template. Build/checks/tests unchanged in mechanism; `check_html.py` gains a soft "≥2 figures per lesson" guard.

**Tech Stack:** Python 3 stdlib only (zero third-party for build); HTML/CSS + tiny inline SVG; pytest (dev). Bilingual via `i18n.L`.

**Spec:** `docs/superpowers/specs/2026-06-14-llama-rag-visual-guide-v2-design.md`
**Source anchor:** llama-index-core 0.14.22. Branch: `v2-enhance`.

---

## Conventions (every task)
- Work in repo root `/home/verden/course/llama-index-visual-guide` (branch `v2-enhance`).
- Build: `cd src && python build.py && python build_print.py`. Tests: `cd src && python -m pytest tests -q`. Checks: `python check_html.py && python check_links.py`.
- After a lesson task, restore `print.html` is NOT needed in v2 — the per-task DoD commits `print.html` too (it is now real content and deterministic, and CI guards it).
- Commit at end of each task with the Copilot trailer.
- Zero third-party imports in `src/*.py` (except `src/tests/`).

## File Structure
| File | Responsibility |
|---|---|
| `src/diagrams.py` | NEW. Bilingual diagram primitives + `DIAGRAM_CSS`. Depends only on `i18n`. |
| `src/tests/test_diagrams.py` | NEW. Unit tests for the primitives. |
| `src/shell.py` | MODIFY. Inject `diagrams.DIAGRAM_CSS` into page/index `<style>`. |
| `src/build_print.py` | MODIFY. Inject `diagrams.DIAGRAM_CSS` + add `.fig` print rules. |
| `src/check_html.py` | MODIFY. Soft guard: ≥2 `class="fig"` per non-exempt lesson (WARN→ERR). |
| `src/part1..5.py`, `src/glossary.py` | MODIFY. Rewrite lessons per v2 template (`import diagrams as d`). |
| `index.html`, `lessons/`, `print.html` | Regenerated artifacts (committed). |

---

## Phase 1 — Diagram foundation

### Task 1: `src/diagrams.py` — bilingual diagram primitives (TDD)

**Files:** Create `src/diagrams.py`, `src/tests/test_diagrams.py`.

- [ ] **Step 1: Write `src/tests/test_diagrams.py`:**

```python
import diagrams as d
from i18n import L


def test_fig_wraps_with_caption():
    h = d.fig("<x>", caption=L("图注", "cap"))
    assert h.startswith('<div class="fig">') and "figcap" in h
    assert 'data-lang="en">cap' in h


def test_flow_boxes_arrows_and_active():
    h = d.flow([("a", L("甲", "A")), ("b", L("乙", "B"), L("注", "note"))], active="b")
    assert h.count('class="fbox') == 2
    assert "fbox on" in h            # active highlighted
    assert "farrow" in h            # arrow between boxes
    assert "fsub" in h              # the note on box b
    assert 'data-lang="en">A' in h and 'data-lang="en">B' in h


def test_vflow_down_arrows_and_produces():
    h = d.vflow([(L("加载", "Load"), L("→Documents", "→Documents")), (L("切块", "Split"),)])
    assert h.count("fvbox") == 2
    assert "fvarrow" in h           # one down-arrow between 2 stages
    assert "fprod" in h             # the 'produces' label


def test_layers_stack():
    h = d.layers([(L("core", "core"), L("抽象", "abstractions")), (L("集成", "integrations"),)])
    assert h.count("flayer") == 2
    assert "fllabel" in h and "flstack" in h


def test_annot_center_and_callouts():
    h = d.annot(L("Node", "Node"), [(L("metadata", "metadata"), L("键值", "key-values"))])
    assert "fcenter" in h and "fcall" in h
    assert 'data-lang="en">metadata' in h


def test_compare2_two_columns():
    h = d.compare2((L("左", "L"), "<p>a</p>"), (L("右", "R"), "<p>b</p>"))
    assert h.count("fcol") == 2 and "fvs" in h
    assert "<p>a</p>" in h and "<p>b</p>" in h


def test_grid_shape():
    h = d.grid([L("h1", "h1"), L("h2", "h2")], [[L("a", "a"), L("b", "b")]])
    assert h.count("fgh") == 2 and h.count("fgc") == 2
    assert "repeat(2,1fr)" in h


def test_scatter_svg_and_legend():
    pts = [(20, 20, L("d1", "d1")), (80, 80, L("d2", "d2")), (25, 30, L("d3", "d3"))]
    h = d.scatter(pts, (22, 22), k=2)
    assert "<svg" in h and h.count("fsdot") == 3
    assert "fsq" in h and "fsknn" in h          # query dot + knn circle
    assert h.count("near") >= 2                 # k nearest highlighted
    assert "fslegend" in h


def test_diagram_css_present():
    assert ".fig" in d.DIAGRAM_CSS and ".fbox" in d.DIAGRAM_CSS and ".fscatter" in d.DIAGRAM_CSS


def test_no_third_party_imports():
    import ast, pathlib
    tree = ast.parse(pathlib.Path("diagrams.py").read_text(encoding="utf-8"))
    mods = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            mods += [a.name.split(".")[0] for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            mods.append((n.module or "").split(".")[0])
    assert set(mods) <= {"i18n", "math"}
```

- [ ] **Step 2: Run → fail** (`cd src && python -m pytest tests/test_diagrams.py -q` → ModuleNotFoundError).

- [ ] **Step 3: Write `src/diagrams.py`:**

```python
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
    SVG carries only geometry; readable labels live in the bilingual HTML legend."""
    qx, qy = query_pt
    dists = sorted((math.hypot(x - qx, y - qy), i) for i, (x, y, _l) in enumerate(doc_pts))
    near = {i for _d, i in dists[:k]}
    radius = dists[k - 1][0] if len(dists) >= k else 0.0
    svg = ['<svg viewBox="0 0 100 100" class="fscatter" preserveAspectRatio="xMidYMid meet" role="img">']
    if radius:
        svg.append(f'<circle cx="{qx}" cy="{qy}" r="{radius:.1f}" class="fsknn"/>')
    for i, (x, y, _lab) in enumerate(doc_pts):
        cls = "fsdot near" if i in near else "fsdot"
        svg.append(f'<circle cx="{x}" cy="{y}" r="2.4" class="{cls}"/>')
    svg.append(f'<circle cx="{qx}" cy="{qy}" r="3.2" class="fsq"/>')
    svg.append("</svg>")
    legend = (
        '<div class="fslegend">'
        f'<span class="fsl fsl-q">{t("查询", "query")}</span>'
        f'<span class="fsl fsl-near">{t("最近邻 top-k", "nearest top-k")}</span>'
        f'<span class="fsl fsl-doc">{t("文档块", "doc chunks")}</span>'
        "</div>"
    )
    return fig(f'<div class="fscatterwrap">{"".join(svg)}{legend}</div>', caption)


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
```

- [ ] **Step 4: Run → pass** (`cd src && python -m pytest tests/test_diagrams.py -q` → 10 passed). Full suite stays green.

- [ ] **Step 5: Commit** `git add src/diagrams.py src/tests/test_diagrams.py && git commit -m "feat(diagrams): bilingual HTML/CSS+SVG diagram primitives" + trailer`.

---

### Task 2: Wire `DIAGRAM_CSS` into shell + print

**Files:** Modify `src/shell.py`, `src/build_print.py`.

- [ ] **Step 1:** In `src/shell.py`, add `import diagrams` near the other imports (after `import i18n`). Then in BOTH `page()` and `index_page()` change the style line
  `<style>{CSS}{EXTRA_CSS}{i18n.LANG_CSS}</style>`
  →
  `<style>{CSS}{EXTRA_CSS}{diagrams.DIAGRAM_CSS}{i18n.LANG_CSS}</style>`

- [ ] **Step 2:** In `src/build_print.py`, add `import diagrams` (after `import i18n`). Change the style line
  `<style>{shell.CSS}{shell.EXTRA_CSS}{i18n.LANG_CSS}{PRINT_CSS}</style>`
  →
  `<style>{shell.CSS}{shell.EXTRA_CSS}{diagrams.DIAGRAM_CSS}{i18n.LANG_CSS}{PRINT_CSS}</style>`
  And append to `PRINT_CSS` (inside its string, before the closing `"""`):
  `\n.fig, .frow, .fvcol, .flstack, .fannot, .fcompare, .fgrid, .fscatterwrap { break-inside: avoid; }`

- [ ] **Step 3:** `cd src && python build.py && python -m pytest tests -q` (still green). Spot-check a built lesson still renders (no diagrams yet, so output unchanged except CSS grows).

- [ ] **Step 4: Commit** `git add src/shell.py src/build_print.py index.html lessons/ print.html && git commit -m "feat(diagrams): inject DIAGRAM_CSS into site + print" + trailer`.

---

### Task 3: `check_html.py` soft guard — ≥2 figures per lesson

**Files:** Modify `src/check_html.py`, `src/tests/test_check_html.py`.

- [ ] **Step 1:** In `check_lesson`, inside the `if fname not in SOFT_EXEMPT:` block, add:

```python
        if len(re.findall(r'class="fig"', html)) < 2:
            add("WARN", "fewer than 2 diagrams (class=\"fig\") — v2 target is >=2")
```

(WARN, not ERR, so the build never breaks mid-migration; the final task confirms all lessons reach ≥2 and 0 errors.)

- [ ] **Step 2:** Add a test in `src/tests/test_check_html.py`:

```python
def test_few_figures_is_a_warning():
    issues = check_html.check_lesson("02-architecture.html", GOOD)  # GOOD has 0 figs
    assert any(i[0] == "WARN" and "diagrams" in i[2] for i in issues)
```

- [ ] **Step 3:** `cd src && python -m pytest tests/test_check_html.py -q` (pass). `python build.py && python check_html.py` will now print WARNs for not-yet-migrated lessons — that's expected (0 errors).

- [ ] **Step 4: Commit** `git add src/check_html.py src/tests/test_check_html.py && git commit -m "feat(checks): warn when a lesson has <2 diagrams (v2 target)" + trailer`.

---

## Phase 2 — Lesson v2 enhancement (one task per lesson)

### Shared Definition of Done (Tasks 4–24)
Each lesson task **edits the existing `LESSON_xx`** in its module (does not rewrite from scratch — keep the verified v1 lead/analogy/compare_table/source_ref/code/key_points/design_highlight/quiz) and **adds** per the v2 template:
- [ ] **A. Hero diagram** right after the `lead` (a `d.flow`/`d.vflow`/`d.annot`/`d.scatter` per the brief, with a bilingual `caption`).
- [ ] **B. A 2nd diagram** inside a body section (and a 3rd where the brief lists one).
- [ ] **C. A new `<h2>` deep section** (`c.section(...)`) expanding the concept in 2–4 sentences (bilingual), so visible text grows toward ~6–8k chars.
- [ ] **D. An expandable deep-dive** after the `source_ref`(s): `c.accordion(L("深入：…","Deep dive: …"), c.qa_item(L("🧪 示例","🧪 Example"), …), c.qa_item(L("❓ 为什么这么设计","❓ Why designed this way"), …), c.qa_item(L("⚙️ 内部怎么跑","⚙️ How it runs inside"), …), c.qa_item(L("🔀 替代方案","🔀 Alternatives"), …))`. All four blocks bilingual.
- [ ] **E. A 2nd `c.code(...)` example** (a variant/advanced usage per the brief; escape `<`→`&lt;`, `&`→`&amp;`).
- [ ] **F. Build + validate:** `cd src && python build.py && python build_print.py`; `python check_html.py` → **0 errors** and **no WARN about <2 diagrams for this lesson**; `python check_links.py` OK; `python -m pytest tests -q` green.
- [ ] **G. Commit:** `git add src/<module>.py index.html lessons/ print.html && git commit -m "feat(content): v2 lesson NN — <topic> (diagrams + depth)" + trailer`.

Authoring notes: import is already `import components as c` + `from i18n import L`; **add `import diagrams as d`** to the module's import block (once per module, in the first lesson task that touches it). Diagrams' labels must be `L`/str (bilingual). No raw `&`/`<` in `<pre>` or diagram text. Keep it deterministic (no clocks/random).

> Diagram-content briefs below are concrete specs; author the bilingual labels to match the lesson. Where a brief gives `d.flow([...])` content, use those exact stages.

---

### Task 4 — L01 (part1.py) what-is-llamaindex
- **add `import diagrams as d` to part1.py.**
- **Hero `flow`** (full RAG overview): `d.flow([("load","加载/Load"),("split","切块/Split"),("embed","Embed"),("store","存储/Store"),("index","索引/Index"),("retrieve","检索/Retrieve"),("synth","合成/Synthesize"),("answer","回答/Answer")], caption=L("RAG 全景：写入路径建索引，查询路径出答案","The RAG pipeline: write path builds the index, query path answers"))`.
- **2nd `compare2`**: 闭卷 LLM vs 开卷 RAG — left=(L("闭卷 LLM","Closed-book LLM"), zh/en body "只凭记忆、会编"/"answers from memory, hallucinates"), right=(L("开卷 RAG","Open-book RAG"), "先检索再据此作答"/"retrieves first, then answers").
- **Deep section**: "RAG 解决的根本问题" — knowledge cutoff / hallucination / private data, 2–3 句.
- **Deep-dive accordion**: 示例(一个朴素 prompt-stuffing 的失败) / 为什么(外置记忆) / 内部(from_documents→query 隐藏了什么) / 替代(微调 vs RAG vs 长上下文).
- **2nd code**: 展示带 `response.source_nodes` 的可溯源查询（区别于第 1 段 5 行）。

### Task 5 — L02 architecture
- **Hero `layers`**: `[(L("应用/你的代码","Your app"),...),(L("llama-index-core","llama-index-core"),L("稳定抽象与编排","stable abstractions + orchestration")),(L("300+ 集成包","300+ integrations"),L("LLM/Embedding/向量库 实现","LLM/embedding/store impls"))]`, caption 命名约定.
- **2nd `flow`**: 换 provider 只改一行 —`d.flow([("iface","core 接口/core interface"),("openai","openai 实现"),("anthropic","anthropic 实现")], caption=...)` 或 compare2 OpenAI↔本地.
- **Deep section**: 为什么把接口与实现分层（独立发版/生态演进）。
- **Deep-dive**: 示例(三个 pip 包) / 为什么(独立演进) / 内部(命名空间约定 llama_index.core vs llama_index.x.y) / 替代(单体 vs 插件).
- **2nd code**: 安装 + 切换两家 LLM 的对照（`Settings.llm = OpenAI(...)` vs 另一家）。

### Task 6 — L03 rag-lifecycle
- **Hero `vflow`** (5 行 → 每步产出): `[(L("SimpleDirectoryReader.load_data()","..."),L("→ Document 列表","→ list of Document")),(L("VectorStoreIndex.from_documents()","..."),L("→ Node → 向量 → 索引","→ Node → vectors → index")),(L("as_query_engine()","..."),L("→ 装配检索/后处理/合成","→ wires retrieve/postproc/synth")),(L("engine.query()","..."),L("→ 检索→合成→答案+source_nodes","→ retrieve→synthesize→answer"))]`.
- **2nd `compare2`**: 写入路径(做一次) vs 查询路径(做多次)。
- **Deep section**: 高层 API 是低层管道的快捷方式 — 两种使用深度.
- **Deep-dive**: 示例(5 行) / 为什么(快捷方式) / 内部(from_documents 内部 split→embed→store) / 替代(手动逐步装配).
- **2nd code**: 持久化复用（`persist` + `load_index_from_storage`），呼应"写一次问多次"。

### Task 7 — L04 documents-nodes
- **Hero `annot`** (center=Node): callouts = text / metadata(键值,可过滤) / relationships(SOURCE·PREVIOUS·NEXT).
- **2nd `flow`**: Document →(切块)→ Node·Node·Node（注 relationships 串起来）。
- **Deep section**: 为什么以 Node 为检索单位（统一下游语言）。
- **Deep-dive**: 示例(构造 Node+关系) / 为什么(检索/溯源单位) / 内部(NodeRelationship 枚举、ref_doc_id) / 替代(整文档检索的弊端).
- **2nd code**: 用 `node.metadata` 做过滤的检索（`MetadataFilters` 简例）或展示 `node.relationships` 读取。

### Task 8 — L05 readers
- **Hero `flow`**: 多来源(文件夹/PDF/网页/DB) → Reader → 统一 Document。
- **2nd `grid`**: 扩展名 → 解析器（.pdf→PDFReader, .md/.txt→平文本, .docx→…）。
- **Deep section**: 统一 Document 让管道与来源解耦。
- **Deep-dive**: 示例(SimpleDirectoryReader 递归+过滤) / 为什么(解耦) / 内部(default_file_reader_cls 按扩展名分派) / 替代(LlamaHub 集成 readers).
- **2nd code**: LlamaHub 网页 reader（`from llama_index.readers.web import SimpleWebPageReader`）。

### Task 9 — L06 node-parsers (核心)
- **Hero 自定义/`annot` chunk+overlap 图**：用 `d.annot` 或 `d.flow` 表现"一长条文本切成多块、相邻块有重叠高亮"（caption: chunk_size 决定块长、chunk_overlap 决定相邻重叠）。可用 `d.compare2`：无 overlap(句子被切断) vs 有 overlap(语义连续)。
- **2nd `vflow`/`annot`**: sentence-window（节点=单句, metadata['window']=前后句上下文）。
- **Deep section**: chunk_size/overlap 的权衡（太大/太小）。
- **Deep-dive**: 示例(SentenceSplitter 参数) / 为什么(召回 vs 上下文) / 内部(get_nodes_from_documents 接口、按句凑到 chunk_size) / 替代(Token/Semantic/SentenceWindow 对比).
- **2nd code**: `SemanticSplitterNodeParser` 或 `TokenTextSplitter` 变体用法。

### Task 10 — L07 metadata-extractors
- **Hero `annot`**: Node + 抽取出的标签(document_title / excerpt_keywords / questions_this_excerpt_can_answer / section_summary)。
- **2nd `flow`**: transformations 串联 `split → TitleExtractor → QuestionsAnsweredExtractor`。
- **Deep section**: 元数据=检索第二通道（过滤 + 问句对齐）。
- **Deep-dive**: 示例(IngestionPipeline transformations) / 为什么(第二通道) / 内部(extractor 是 LLM 调用，键名) / 替代(手工 metadata vs LLM 抽取，成本).
- **2nd code**: 自定义 metadata + 用 `excluded_embed_metadata_keys` 控制是否进 embedding。

### Task 11 — L08 embeddings
- **Hero `scatter`** (SVG 向量空间)：给定若干文档点 + 1 个查询点 + top-k 近邻圈（坐标在源码里给定，如 doc_pts=[(18,24,L("退款政策","refund policy")),(70,72,L("配送时效","shipping")),(28,30,L("退货流程","returns")),(80,30,L("账号注册","signup")),(22,68,L("发票","invoice"))], query=(24,28), k=3）。
- **2nd `flow`**: text → embed_model → 向量[1536]。
- **Deep section**: 语义相近=向量距离近（余弦相似度）；查询/文档须同模型。
- **Deep-dive**: 示例(get_text_embedding) / 为什么(语义检索地基) / 内部(BaseEmbedding 接口、相似度) / 替代(关键词/BM25 vs 向量，混合).
- **2nd code**: 计算两段文本的余弦相似度（`Settings.embed_model.similarity(a,b)` 或手算）。

### Task 12 — L09 vector-stores
- **Hero `flow`**: 查询向量 → VectorStore（近邻搜索）→ top-k Node。
- **2nd `compare2`**: 内存 SimpleVectorStore vs 生产(Chroma/FAISS/pgvector)。
- **Deep section**: VectorStore 职责（存向量+元数据+近邻查询）与可替换性。
- **Deep-dive**: 示例(默认 vs Chroma 注入) / 为什么(接口统一) / 内部(VectorStoreQuery 契约) / 替代(各向量库取舍).
- **2nd code**: 带 `MetadataFilters` 的向量检索（元数据过滤 + 近邻）。

### Task 13 — L10 index-abstraction
- **Hero `grid`**: 四种 Index × (组织方式 / 适合) — VectorStoreIndex/SummaryIndex/DocumentSummaryIndex/PropertyGraphIndex。
- **2nd `flow`**: Index → as_query_engine → 统一问答入口（可加 Router 分流）。
- **Deep section**: "选 Index = 选检索范式"。
- **Deep-dive**: 示例(Vector vs Summary 两段) / 为什么(组织+检索策略) / 内部(都继承 BaseIndex.from_documents) / 替代(多 Index + RouterQueryEngine).
- **2nd code**: `SummaryIndex` + `response_mode='tree_summarize'` 做全局总结。

### Task 14 — L11 ingestion-storage
- **Hero `flow`**: IngestionPipeline = `[split → extract → embed]` + cache + docstore 去重。
- **2nd `annot`/`layers`**: persist → 磁盘（docstore / index store / vector store 三件套）→ load。
- **Deep section**: 把建索引做成幂等可缓存管道（生产关键）。
- **Deep-dive**: 示例(pipeline + docstore) / 为什么(增量/幂等) / 内部(run_transformations 哈希缓存、DocstoreStrategy) / 替代(每次全量重建的代价).
- **2nd code**: 增量更新——第二次 run 同一文档命中缓存/去重（带 `IngestionCache` 持久化或 docstore）。

### Task 15 — L12 retrievers
- **Hero `flow`**: 问题 → 向量化 → 索引近邻 → top-k NodeWithScore（注：尚未调用 LLM）。
- **2nd `annot`**: similarity_top_k 旋钮（太小漏召回 / 太大引噪声）。
- **Deep section**: 检索与生成解耦 → 可单独评估"召回对不对"。
- **Deep-dive**: 示例(as_retriever.retrieve) / 为什么(可独立评估) / 内部(retrieve 模板方法 → 子类实现 _retrieve) / 替代(关键词/混合检索器).
- **2nd code**: 直接构造 `VectorIndexRetriever` 并读 `n.score`/`n.node`。

### Task 16 — L13 postprocessors
- **Hero `flow`**: 检索结果 → [SimilarityPostprocessor / Rerank / MetadataReplacement] → 精选 Node → LLM（"质检站"）。
- **2nd `compare2`**: cutoff 前(混入低分) vs 后(只留高相关)。
- **Deep section**: 检索后/生成前——最低成本提质量。
- **Deep-dive**: 示例(SimilarityPostprocessor) / 为什么(便宜的提升) / 内部(postprocess_nodes、score<cutoff 丢弃) / 替代(rerank 模型 vs 阈值).
- **2nd code**: 句窗 + `MetadataReplacementPostProcessor(target_metadata_key='window')` 还原上下文。

### Task 17 — L14 response-synthesizers
- **Hero `grid`** (四模式形态): refine / compact / tree_summarize / accumulate × (怎么合成 / 适合)。
- **2nd `vflow`**: tree_summarize 的分组逐层向上合并。
- **Deep section**: 多片段→单答案的核心权衡（上下文窗口 vs 片段数）。
- **Deep-dive**: 示例(get_response_synthesizer) / 为什么(可切换策略) / 内部(ResponseMode 枚举、compact 即 compact_and_refine) / 替代(各 mode 取舍).
- **2nd code**: `get_response_synthesizer(response_mode='refine')` 显式装配 + 用于 query engine。

### Task 18 — L15 query-engine
- **Hero `flow`**: 组合根 retriever + postprocessors + synthesizer → `.query()`。
- **2nd `vflow`**: 一次 query 的内部时序（retrieve → postprocess → synthesize → Response(answer+source_nodes)）。
- **Deep section**: QueryEngine 是查询路径的组合根（三正交件可独立替换）。
- **Deep-dive**: 示例(from_args 手装) / 为什么(组合根) / 内部(_query 调 retrieve()+synthesize()) / 替代(as_query_engine 快捷 vs from_args 定制).
- **2nd code**: `as_query_engine(text_qa_template=..., similarity_top_k=...)` 一行定制版（对照 from_args）。

### Task 19 — L16 chat-engine
- **Hero `compare2`**: condense_question(历史+新问→独立问题→检索) vs context(每轮检索注入上下文)。
- **2nd `flow`**: 多轮：用户"那它呢?" → 指代消解 → 检索 → 答 → 记忆。
- **Deep section**: 多轮难点=指代消解 + 何时检索。
- **Deep-dive**: 示例(as_chat_engine.chat ×2) / 为什么(不只是套循环) / 内部(CondenseQuestion 先压缩、Context 注入 system) / 替代(condense_plus_context 折中).
- **2nd code**: 显式 `ContextChatEngine.from_defaults(retriever=..., memory=...)` 或带 `chat_history`。

### Task 20 — L17 settings-prompts
- **Hero `annot`**: 全局 Settings 面板（llm / embed_model / node_parser / chunk_size）。
- **2nd `annot`**: Prompt 模板填空（{context_str} / {query_str} 注入位）。
- **Deep section**: 全局默认 + 局部覆盖；Prompt 控制"最后一公里"。
- **Deep-dive**: 示例(Settings + PromptTemplate) / 为什么(去样板/可审) / 内部(Settings 是 _Settings 单例；text_qa_template 流向 synthesizer) / 替代(局部传参 vs 全局).
- **2nd code**: 局部覆盖——某个 query engine 用不同的 `llm=` / `text_qa_template=`，不动全局。

### Task 21 — L18 advanced-retrieval
- **Hero `flow`** (fusion): 一个问题 → 改写成多版 → 各自检索 → reciprocal rerank 融合。
- **2nd `vflow`/`grid`**: auto-merging（命中多个小块 → 合并成父块）；列出 4 种进阶检索器与适用。
- **Deep section**: 进阶检索针对基础 top-k 的短板（召回/碎片/多库）。
- **Deep-dive**: 示例(QueryFusionRetriever) / 为什么(统一 BaseRetriever 可插拔) / 内部(num_queries 生成 n-1 改写、FUSION_MODES) / 替代(AutoMerging/Recursive/Router 各适用).
- **2nd code**: `RouterRetriever`/`AutoMergingRetriever` 之一的最小用法。

### Task 22 — L19 evaluation
- **Hero `grid`**: 三把尺子（Faithfulness/Relevancy/Correctness × 各查什么 / 需要什么输入）。
- **2nd `flow`**: 评估闭环（改切块/检索/Prompt → 评估 → 对比指标 → 决策）。
- **Deep section**: 把调优从"凭感觉"变"可度量闭环"。
- **Deep-dive**: 示例(FaithfulnessEvaluator.evaluate_response) / 为什么(可度量) / 内部(LLM-as-judge、Faithfulness 二值、Correctness 1–5) / 替代(人评 vs LLM 评、回归集).
- **2nd code**: `RelevancyEvaluator` 或 `BatchEvalRunner` 跑一小批问题。

### Task 23 — L20 capstone
- **Hero 端到端架构大图** `flow`/`layers`：load→ingest→index→persist→retrieve→postproc→synth→query/chat→eval 全景（caption: 每一站都可替换）。
- **2nd `compare2`**: 首次建库(load→ingest→persist) vs 复用(load_index_from_storage)。
- **Deep section**: 把整本书拼成可维护、可回归的应用。
- **Deep-dive**: 示例(关键片段) / 为什么(可组合标准件) / 内部(persist/load 分支、Settings 先于分支) / 替代(改造成"带脚注客服机器人"要换哪些件).
- **2nd code**: 在 capstone 上加一段——`FaithfulnessEvaluator` 批量评估 或 切到 `chat_engine` 的多轮。

### Task 24 — L21 glossary (轻量)
- **Hero**: 一张 mini `flow` 复习图（写入路径 ▸ 查询路径），caption "按数据流复习全书术语"。其余术语表保持。
- glossary 是 SOFT_EXEMPT，但加这 1 张图即可（≥1 fig；不强制 2）。**Note:** keep the `<2 fig` guard's SOFT_EXEMPT exemption so glossary doesn't WARN.
- No deep-dive / 2nd code needed for the glossary (data table lesson).

---

## Phase 3 — Finalize

### Task 25: Final rebuild, full verification, tighten guard
**Files:** Modify `src/check_html.py` (optional: flip the <2-fig guard from WARN to ERR now that all lessons comply), regenerate artifacts.

- [ ] **Step 1:** Confirm every non-glossary lesson has ≥2 `class="fig"`: `cd src && python build.py && python -c "import re,glob; bad=[f for f in glob.glob('../lessons/*.html') if 'glossary' not in f and len(re.findall('class=\"fig\"', open(f,encoding='utf-8').read()))<2]; print('lessons with <2 figs:', bad)"` → expect `[]`.
- [ ] **Step 2 (optional):** In `check_html.py` change that guard from `add("WARN", ...)` to `add("ERR", ...)` so it permanently enforces ≥2 diagrams. Update the test `test_few_figures_is_a_warning` → assert it's now `"ERR"`. Glossary stays exempt (it's in SOFT_EXEMPT).
- [ ] **Step 3:** Full build + verify: `cd src && python build.py && python build_print.py && python -m pytest tests -q && python check_html.py && python check_links.py`. Expect: all tests pass; check_html **0 errors, 0 warnings**; links resolve; tree clean after build (idempotent).
- [ ] **Step 4:** Measure depth: `python3 -c "import re,glob; [print(f.split('/')[-1], len(re.sub('<[^>]+>','',re.sub(r'<style.*?</style>|<script.*?</script>','',open(f,encoding='utf-8').read(),flags=re.S)))) for f in sorted(glob.glob('lessons/*.html'))]"` — confirm most lessons are well above v1 (~3k) toward 6–8k chars.
- [ ] **Step 5: Commit** the final artifacts + any guard change: `git add -A && git commit -m "chore: v2 finalize — all lessons >=2 diagrams, full rebuild" + trailer`.

---

## Self-Review
- **Spec coverage:** §3 primitives → Task 1; §4 template → Phase-2 DoD; §5 per-lesson map → Tasks 4–24; §6 build/checks → Tasks 2,3,25; §8 success criteria → Task 25 verification. ✓
- **No placeholders:** diagram API fully written in Task 1; per-lesson briefs are concrete diagram specs + deep-dive/2nd-example topics (content authored against the existing v1 lesson).
- **Type consistency:** all lessons call the Task-1 primitives (`d.fig/flow/vflow/layers/annot/compare2/grid/scatter`) with the signatures defined there; `import diagrams as d` added per module.
