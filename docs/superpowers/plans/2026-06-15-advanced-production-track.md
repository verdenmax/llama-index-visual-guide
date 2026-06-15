# Part 6 Production-Advanced Track Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 6 full production-grade lessons (21–26) on hardening a working RAG for production, and renumber the glossary to 27.

**Architecture:** A new content module `src/part6.py` holds `LESSON_21..LESSON_26` as bilingual HTML strings (same pattern as `part1..5.py`). `registry.py` + `shell.py PAGES` register them and move the glossary to `27-glossary.html`; `check_html.py` auto-validates the "共 N 课 · N 个部分" count from `PAGES`, so renumbering is data-driven. Each lesson reuses the existing component/diagram/quiz/interview systems and DoD.

**Tech Stack:** Python 3 stdlib only for build (zero third-party); content authored via `components` (`c.*`), `diagrams` (`d.*`), `i18n.L`; quizzes in `quizzes.py`, interview drills in `interviews.py`. Anchor: llama-index-core 0.14.22.

**Spec:** `docs/superpowers/specs/2026-06-15-advanced-production-track-design.md`. Branch: `advanced-track`.

---

## Conventions (every task)
- Work in repo root `/home/verden/course/llama-index-visual-guide` (branch `advanced-track`).
- Build: `cd src && python build.py && python build_print.py`. Checks: `python check_html.py && python check_links.py`. Tests: `cd src && python -m pytest tests -q`.
- Commit at end of each task with the Copilot trailer; commit regenerated `index.html lessons/ print.html` too.
- Zero third-party imports in `src/*.py` (except `src/tests/`).
- **Verified API surface** (use these exact names; all confirmed in vendored core 0.14.22 unless marked *(integration)*):
  - L21: `from llama_index.core.retrievers import QueryFusionRetriever`; `HyDEQueryTransform` (`llama_index.core.indices.query.query_transform`); `RetrieverQueryEngine.from_args`; *(integration)* `from llama_index.retrievers.bm25 import BM25Retriever`, `from llama_index.postprocessor.cohere_rerank import CohereRerank`, `from llama_index.core.postprocessor import SentenceTransformerRerank`.
  - L22: `from llama_index.core.evaluation import BatchEvalRunner, FaithfulnessEvaluator, RelevancyEvaluator, RetrieverEvaluator`; `from llama_index.core.evaluation import DatasetGenerator`.
  - L23: `from llama_index.core import set_global_handler`; `from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler`; *(integration)* `set_global_handler("arize_phoenix")` / `"langfuse"`.
  - L24: `from llama_index.core.ingestion import IngestionCache`; `index.as_query_engine(streaming=True)` → `resp.response_gen` / `resp.print_response_stream()`; `await engine.aquery(...)`.
  - L25: `from llama_index.core.vector_stores import MetadataFilters, MetadataFilter, FilterOperator`; `from llama_index.core.postprocessor import PIINodePostprocessor, NERPIINodePostprocessor`.
  - L26: `from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent, Event`; `from llama_index.core.agent import FunctionAgent, ReActAgent`; `from llama_index.core.tools import QueryEngineTool, FunctionTool`.

## File Structure
| File | Responsibility |
|---|---|
| `src/part6.py` | NEW. `LESSON_21..LESSON_26` (production lessons). `import components as c`, `import diagrams as d`, `import i18n`, `from i18n import L`. |
| `src/registry.py` | MODIFY. `import part6`; add 21–26 → `part6.LESSON_2x`; glossary key → `27-glossary.html`. |
| `src/shell.py` | MODIFY. `PAGES` += 6 (new `P6` = Production); glossary row → `27-glossary.html` with new `P7` = Reference. `SUBTITLES` += 6 + glossary key→27. |
| `src/quizzes.py` | MODIFY. `QUIZZES` += 21–26 (≥1 MCQ + 1 open each). |
| `src/interviews.py` | MODIFY. `INTERVIEW` += 21–26 (2–3 drills each, 🔑 + some figs). |
| `src/glossary.py` | MODIFY. Add 6 advanced terms. |
| `lessons/21-glossary.html` | `git rm` (build emits `27-glossary.html`). |
| `index.html`, `lessons/`, `print.html` | Regenerated artifacts (committed). |

---

## Task 1: Scaffolding — module, renumbering, green build

**Files:**
- Create: `src/part6.py`
- Modify: `src/registry.py`, `src/shell.py`
- Delete: `lessons/21-glossary.html`
- Test: `src/tests/test_registry_structure.py` (new)

- [ ] **Step 1: Write the failing test** — `src/tests/test_registry_structure.py`

```python
import registry
import shell


def test_27_lessons_and_glossary_last():
    keys = list(registry.CONTENT.keys())
    assert len(keys) == 27
    assert keys[-1] == "27-glossary.html"          # glossary renumbered + last
    assert "21-production-retrieval.html" in keys   # first production lesson
    assert "26-agents-workflows.html" in keys       # last production lesson


def test_pages_has_seven_parts():
    parts = {p[2].zh for p in shell.PAGES}
    assert len(parts) == 7                          # was 6 → +Production part
    assert len(shell.PAGES) == 27
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd src && python -m pytest tests/test_registry_structure.py -q`
Expected: FAIL (registry has 21 keys, glossary is `21-glossary.html`).

- [ ] **Step 3: Create `src/part6.py` with 6 minimal-valid skeleton lessons**

Each skeleton is real but minimal (full content lands in Tasks 2–7); it must satisfy `check_html` (≥2 `d.fig`, an analogy card, a key-points card, bilingual). Repeat this block for 21–26, changing the title/stage:

```python
"""Part 6 (production-advanced): lessons 21-26. Content filled task-by-task."""
import components as c
import diagrams as d
import i18n
from i18n import L


def _skeleton(zh_topic, en_topic):
    return (
        c.pipeline(None)
        + c.lead(L(f"本课讲生产阶段的 <strong>{zh_topic}</strong>（内容完善中）。",
                   f"This lesson covers <strong>{en_topic}</strong> for production (being written)."))
        + d.flow([("a", L("场景", "Scenario")), ("b", L("做法", "Approach")), ("c", L("评测", "Evaluate"))],
                 caption=L("占位流程图", "placeholder flow"))
        + d.compare2((L("不做", "Without"), i18n.render(L("有什么问题", "what breaks"))),
                     (L("做了", "With"), i18n.render(L("解决什么", "what it fixes"))),
                     caption=L("占位对照", "placeholder compare"))
        + c.analogy(L("占位类比。", "Placeholder analogy."))
        + c.key_points([L("本课要点占位。", "Key-points placeholder.")])
    )


LESSON_21 = _skeleton("生产级检索", "production retrieval")
LESSON_22 = _skeleton("规模化评估与 CI 回归闸", "evaluation at scale & CI gating")
LESSON_23 = _skeleton("可观测与追踪", "observability & tracing")
LESSON_24 = _skeleton("成本与延迟工程", "cost & latency engineering")
LESSON_25 = _skeleton("安全与防护", "security & guardrails")
LESSON_26 = _skeleton("Agent 与 Workflows", "agents & workflows")
```

- [ ] **Step 4: Wire `src/registry.py`** — add `import part6` (after `import part5`), insert the 6 entries before glossary, and renumber glossary. The `CONTENT` dict's glossary line becomes:

```python
import part6
# ... in CONTENT, replace the glossary entry with:
    "20-capstone.html": part5.LESSON_20,
    "21-production-retrieval.html": part6.LESSON_21,
    "22-eval-scale.html": part6.LESSON_22,
    "23-observability.html": part6.LESSON_23,
    "24-cost-latency.html": part6.LESSON_24,
    "25-security.html": part6.LESSON_25,
    "26-agents-workflows.html": part6.LESSON_26,
    "27-glossary.html": glossary.LESSON_21,
```

- [ ] **Step 5: Wire `src/shell.py PAGES` + `SUBTITLES`** — add two new part labels and the 6 rows; move glossary. Add near the other `P#` definitions:

```python
P6PROD = L("第六部分 · 生产进阶", "Part 6 · Production")
P7REF = L("第七部分 · 速查", "Part 7 · Reference")
```

Replace the final `PAGES` glossary row with:

```python
    ("20-capstone.html", L("端到端 Capstone", "End-to-End Capstone"), P5),
    ("21-production-retrieval.html", L("生产级检索", "Production Retrieval"), P6PROD),
    ("22-eval-scale.html", L("规模化评估与 CI 闸", "Evaluation at Scale"), P6PROD),
    ("23-observability.html", L("可观测与追踪", "Observability & Tracing"), P6PROD),
    ("24-cost-latency.html", L("成本与延迟工程", "Cost & Latency"), P6PROD),
    ("25-security.html", L("安全与防护", "Security & Guardrails"), P6PROD),
    ("26-agents-workflows.html", L("Agent 与 Workflows", "Agents & Workflows"), P6PROD),
    ("27-glossary.html", L("术语表 · 概念索引", "Glossary &amp; Concept Index"), P7REF),
```

(Delete the old `("21-glossary.html", …, P6)` row and its `P6 = …` label if `P6` is now unused; keep whatever label constant name the file already used for the glossary part and repoint it.)

Add to `SUBTITLES` (and change the glossary key to `27-glossary.html`):

```python
    "21-production-retrieval.html": L("混合检索 · Rerank · HyDE", "hybrid · rerank · HyDE"),
    "22-eval-scale.html": L("数据集 · BatchEvalRunner · CI 闸", "datasets · BatchEvalRunner · CI gate"),
    "23-observability.html": L("instrumentation · Phoenix / Langfuse", "instrumentation · Phoenix / Langfuse"),
    "24-cost-latency.html": L("缓存 · 异步 · 流式", "caching · async · streaming"),
    "25-security.html": L("多租户隔离 · PII · 注入", "multi-tenant · PII · injection"),
    "26-agents-workflows.html": L("Workflow · FunctionAgent · 工具", "Workflow · FunctionAgent · tools"),
    "27-glossary.html": L("术语一句话查 + 跳转", "one-line term lookup + jump"),
```

- [ ] **Step 6: Remove the stale glossary artifact**

Run: `git rm lessons/21-glossary.html`

- [ ] **Step 7: Build + verify the scaffold is green**

Run: `cd src && python build.py && python build_print.py && python -m pytest tests/test_registry_structure.py -q && python check_html.py && python check_links.py`
Expected: tests PASS; `check_html` → **0 errors, 0 warnings** and index pill reads "共 27 课 · 7 个部分" (auto-validated); links resolve; `lessons/27-glossary.html` exists.

- [ ] **Step 8: Commit**

```bash
git add src/part6.py src/registry.py src/shell.py src/tests/test_registry_structure.py index.html lessons/ print.html
git commit -m "feat(part6): scaffold production track (lessons 21-26) + renumber glossary to 27"
```

---
## Phase 2 — Lesson content (one task per lesson, replaces the skeleton)

### Shared Definition of Done (Tasks 2–7)
Each task **replaces the `_skeleton(...)` assignment** for its `LESSON_2x` in `src/part6.py` with full content, and adds its quiz + interview entries. Required pieces (same as existing courses):
- `c.pipeline(stage)` (use the closest stage or `None`) + `c.lead` + `c.analogy` + **≥2 `d.*` diagrams** + `c.compare_table` + ≥1 `c.source_ref` + a deep `c.section` + `c.accordion(L("深入：…","Deep dive: …"), 4×c.qa_item(🧪/❓/⚙️/🔀))` + **2 `c.code` examples** (the verified snippets below) + `c.key_points` + `c.design_highlight`.
- In `src/quizzes.py` add a `"NN-….html"` entry: ≥1 `mcq` (with `why`) + 1 `open`.
- In `src/interviews.py` add a `"NN-….html"` list: 2–3 drills, each `{"q": L(…), "answer": L("🔑 <strong>重点：…</strong> …")}`, ≥1 with a `"fig"`. Style = scenario + why + how-conceived + how-evaluated.
- Escaping: literal `&`→`&amp;`; inside `c.code` `<`→`&lt;`,`>`→`&gt;`,`->`→`-&gt;`. Diagram/`compare2` labels via `L`/`i18n.render(L(...))`.
- `c.source_ref` for integration APIs points at the **integration package name** (e.g. `llama-index-retrievers-bm25 · BM25Retriever`); core APIs point at the core path. Code that needs an integration package or API key gets a `# pip install …` / `# 需 … key` comment — illustrative, not guaranteed end-to-end runnable (per spec §5).
- **Gate (each task):** `cd src && python build.py && python build_print.py`; `python check_html.py` → **0 errors, no <2-fig warning for this lesson**; `python check_links.py` OK; `python -m pytest tests -q` green. Then commit `src/part6.py src/quizzes.py src/interviews.py index.html lessons/ print.html`.

---

### Task 2 — L21 `21-production-retrieval.html` (生产级检索)

**Files:** Modify `src/part6.py` (`LESSON_21`), `src/quizzes.py`, `src/interviews.py`.

- [ ] **Step 1: Replace `LESSON_21`** — pipeline("retrieve"). Author per the DoD with:
  - **Hero `d.flow`**: `问题 → [向量检索 · BM25] → 融合(RRF) → Rerank 精排 → top-3`（active 在 "rerank"），caption「先广召回，再精排」。
  - **2nd `d.compare2`**: 纯向量（漏精确编号“X-2000”）vs 混合（BM25 补精确匹配）。
  - **Deep `c.section`**「为什么生产 RAG 几乎都要混合检索 + Rerank」：向量懂语义但弱在精确 token/罕见词；BM25 补字面；rerank 用交叉编码器把"广召回"里真正相关的提到前面——召回与精度分两步拿。
  - **Accordion** 深入：🧪(装配混合+rerank) / ❓(召回 vs 精度解耦) / ⚙️(QueryFusionRetriever 用 RRF 融合多路；rerank 是 node_postprocessor) / 🔀(Cohere vs 本地 SentenceTransformer rerank vs LLMRerank 的成本取舍)。
  - **`c.source_ref`**: `retrievers/fusion_retriever.py · QueryFusionRetriever`（core）+ `llama-index-retrievers-bm25 · BM25Retriever`（集成）。

- [ ] **Step 2: code① (hybrid + rerank)** — use verbatim (escape in `c.code`: none needed except none):

```python
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.retrievers.bm25 import BM25Retriever            # pip install llama-index-retrievers-bm25
from llama_index.postprocessor.cohere_rerank import CohereRerank  # pip install llama-index-postprocessor-cohere-rerank

# 两路召回：向量(语义) + BM25(精确 token)，先各取 10
vector = index.as_retriever(similarity_top_k=10)
bm25 = BM25Retriever.from_defaults(docstore=index.docstore, similarity_top_k=10)

# 用 reciprocal-rank fusion 融合两路（num_queries=1 表示不改写、只融合检索器）
hybrid = QueryFusionRetriever([vector, bm25], num_queries=1,
                              similarity_top_k=10, mode='reciprocal_rerank')

# 再用 rerank 模型把 10 条精排到最相关的 3 条（需 COHERE_API_KEY）
engine = RetrieverQueryEngine.from_args(
    retriever=hybrid, node_postprocessors=[CohereRerank(top_n=3)])
print(engine.query('X-2000 的保修期是多久？'))
```

- [ ] **Step 3: code② (HyDE query transform)** — verbatim:

```python
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.query_engine import TransformQueryEngine

# HyDE：先让 LLM 写一个“假设答案”，用它的向量去检索——往往比用问句本身更贴近文档措辞
hyde = HyDEQueryTransform(include_original=True)
engine = TransformQueryEngine(index.as_query_engine(similarity_top_k=5), query_transform=hyde)
print(engine.query('远程办公需要审批吗？'))
```

- [ ] **Step 4: Add quiz** — in `src/quizzes.py`, `"21-production-retrieval.html"`:

```python
    "21-production-retrieval.html": {
        "mcq": [{
            "q": L("纯向量检索为什么会漏掉精确编号“X-2000”这样的查询？",
                   "Why can pure vector search miss an exact id like 'X-2000'?"),
            "opts": [
                L("向量库坏了", "the vector store is broken"),
                L("embedding 偏语义，对精确符号/罕见 token 不敏感，可能排不进 top-k",
                  "embeddings capture meaning and are weak on exact symbols/rare tokens, so it may miss top-k"),
                L("必须重建索引", "you must re-index"),
                L("top_k 一定太小", "top_k is always too small"),
            ],
            "answer": 1,
            "why": L("解决靠混合检索(向量 + BM25/关键词)或把编号写进 metadata 精确过滤。",
                     "Fix with hybrid retrieval (vector + BM25) or exact metadata filtering."),
        }],
        "open": [L("你的查询里既有自然语言问题也有精确产品编号，你会怎么配比向量与关键词两路的权重？",
                   "With both natural-language questions and exact product ids in your queries, how would you weight the vector vs keyword paths?")],
    },
```

- [ ] **Step 5: Add interview drills** — in `src/interviews.py`, `"21-production-retrieval.html"`: 2–3 drills (scenario+why+eval). At least one with a `d.grid` fig comparing Cohere / SentenceTransformer / LLM rerank on (准确/成本/是否本地). Lead each answer with `🔑 <strong>重点：…</strong>`.

- [ ] **Step 6: Gate + commit** (per Shared DoD).

```bash
git add src/part6.py src/quizzes.py src/interviews.py index.html lessons/ print.html
git commit -m "feat(content): L21 production retrieval (hybrid + rerank + HyDE)"
```

---
### Task 3 — L22 `22-eval-scale.html` (规模化评估与 CI 回归闸)

**Files:** `src/part6.py` (`LESSON_22`), `src/quizzes.py`, `src/interviews.py`. pipeline(None).
- **Hero `d.flow`**: `文档 → 自动生成 QA 金标 → 批量评估器 → 聚合分数 → CI 闸(达标合并 / 不达回退)`（active 在 "CI 闸"）。
- **2nd `d.grid`**: 三把尺子 × (查什么 / 在哪跑：开发-CI-线上抽样)。
- **Deep `c.section`**「把'凭感觉调'变成'分数门槛守门'」：金标集怎么造与维护（自动生成起步、人工标注高价值子集）、为什么要回归集挡住"修一个坏一批"。
- **Accordion**: 🧪(造集+批量评估) / ❓(可度量闭环) / ⚙️(BatchEvalRunner 并发跑、EvaluationResult.passing) / 🔀(自动生成 vs 人工标注 vs 线上反馈)。
- **`c.source_ref`**: `evaluation/batch_runner.py · BatchEvalRunner`、`evaluation/dataset_generation.py · DatasetGenerator`。
- **code①** (verbatim):
```python
from llama_index.core.evaluation import (DatasetGenerator, BatchEvalRunner,
                                          FaithfulnessEvaluator, RelevancyEvaluator)

# 1) 自动造金标问题（生产里再人工挑选/标注更可靠的子集）
questions = DatasetGenerator.from_documents(
    docs, num_questions_per_chunk=2).generate_questions_from_nodes()

# 2) 并发批量评估：忠实度 + 相关性
runner = BatchEvalRunner(
    {'faithfulness': FaithfulnessEvaluator(), 'relevancy': RelevancyEvaluator()}, workers=8)
results = await runner.aevaluate_queries(index.as_query_engine(), queries=questions[:50])
```
- **code②** (verbatim — note `>=` is valid in `<pre>`, no escaping needed):
```python
# 把评估变成 CI 回归闸：均通过率低于阈值就 fail（放进 pytest / CI 脚本）
def pass_rate(rs):
    return sum(r.passing for r in rs) / len(rs)

faith = pass_rate(results['faithfulness'])
print(f'faithfulness pass-rate: {faith:.0%}')
assert faith >= 0.9, '忠实度回退，拦截本次变更'   # 守门：不达标就别合并
```
- **quiz**: 为什么需要回归集（防"修一个坏一批"）。**interview**: 2 drills（如"只有 200 条无标准答案的历史问答，怎么搭最小回归评估？"——呼应 L19）。
- **Gate + commit** `git commit -m "feat(content): L22 evaluation at scale + CI gating"`.

---

### Task 4 — L23 `23-observability.html` (可观测与追踪)

**Files:** `src/part6.py` (`LESSON_23`), `src/quizzes.py`, `src/interviews.py`. pipeline(None).
- **Hero `d.flow`**: `一次 query 的隐藏内部 → trace 暴露每步(检索 · rerank · LLM)的 耗时 / token / node / 成本`。
- **2nd `d.compare2`**: 没有 trace（黑盒、靠猜）vs 有 trace（每步可见、可定位慢/贵在哪）。
- **Deep `c.section`**「RAG 多步且中间结果隐藏，可观测是生产调试的地基」：要看检索到了什么、各步耗时、token/成本，才能定位是检索还是生成的问题。
- **Accordion**: 🧪(一行接 Phoenix) / ❓(为什么必须可观测) / ⚙️(instrumentation 事件/span、CallbackManager) / 🔀(Phoenix vs Langfuse vs OTel 取舍)。
- **`c.source_ref`**: `callbacks/global_handlers.py · set_global_handler`（core）、`llama-index-callbacks-arize-phoenix`（集成）。
- **code①** (verbatim):
```python
from llama_index.core import set_global_handler

# 一行接入追踪后端（需 pip install llama-index-callbacks-arize-phoenix 并本地启动 Phoenix）
set_global_handler('arize_phoenix')

# 之后任意 query 都会被记录：检索到的 node、各步耗时、token、成本
index.as_query_engine().query('退款多久到账？')
```
- **code②** (verbatim — zero external deps):
```python
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler

# 本地零依赖看内部：每个事件的耗时与中间结果
debug = LlamaDebugHandler(print_trace_on_end=True)
Settings.callback_manager = CallbackManager([debug])

index.as_query_engine().query('保修期多久？')
print(debug.get_event_pairs())   # 取检索/LLM 等事件对，看各步耗时
```
- **quiz**: 答案错时先看 trace 里的什么。**interview**: 2 drills（如"线上某些问答特别慢，你怎么用 trace 定位是检索、rerank 还是 LLM？"）。
- **Gate + commit** `git commit -m "feat(content): L23 observability & tracing"`.

---

### Task 5 — L24 `24-cost-latency.html` (成本与延迟工程)

**Files:** `src/part6.py` (`LESSON_24`), `src/quizzes.py`, `src/interviews.py`. pipeline(None).
- **Hero `d.layers`**: 三层缓存（embedding 缓存 / LLM 响应缓存 / 检索-响应缓存）各砍哪块成本。
- **2nd `d.compare2`**: 同步阻塞（等全答出来）vs 流式（逐 token 先出，首字延迟骤降）。
- **Deep `c.section`**「成本 = token × 调用，延迟 = 多步串行」：缓存、异步/批、流式、选小模型/小 embedding + 控 top_k，四把刀；怎么度量（p50/p95、每问成本）。
- **Accordion**: 🧪(IngestionCache 复用) / ❓(缓存为什么是第一刀) / ⚙️(流式 response_gen、aquery 异步) / 🔀(缓存命中率 vs 新鲜度的取舍)。
- **`c.source_ref`**: `ingestion/cache.py · IngestionCache`、`base/response/schema.py · StreamingResponse`。
- **code①** (verbatim):
```python
# 流式：逐 token 返回，首字延迟大幅下降（生产体验关键）
engine = index.as_query_engine(streaming=True)
engine.query('详细解释一下退款流程').print_response_stream()   # 边生成边打印
```
- **code②** (verbatim):
```python
from llama_index.core import Settings
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.node_parser import SentenceSplitter

# embedding 缓存：相同输入直接复用上次向量，避免重复花钱
pipeline = IngestionPipeline(
    transformations=[SentenceSplitter(chunk_size=512), Settings.embed_model],
    cache=IngestionCache())
pipeline.run(documents=docs)          # 第二次跑命中缓存、近乎零成本
pipeline.persist('./pipeline_cache')  # 跨进程持久化缓存
```
- **quiz**: 流式优化的是哪个指标（首字延迟/总延迟）。**interview**: 2 drills（如"每问成本太高，你按什么顺序砍：缓存 / 小模型 / 降 top_k / 关 rerank？怎么验证质量没掉？"）。
- **Gate + commit** `git commit -m "feat(content): L24 cost & latency engineering"`.

---

### Task 6 — L25 `25-security.html` (安全与防护)

**Files:** `src/part6.py` (`LESSON_25`), `src/quizzes.py`, `src/interviews.py`. pipeline(None).
- **Hero `d.flow`**: `请求(带 tenant) → 强制 tenant 过滤 → 只检索本租户 → PII 脱敏 → grounding 校验 → 答 / 拒答`（active 在 "强制 tenant 过滤"）。
- **2nd `d.compare2`**: 无隔离（能检索到别租户数据＝越权）vs 强制 MetadataFilters。
- **Deep `c.section`**「生产三大安全面：越权(多租户)、PII、prompt 注入」+ grounding 强制（只引用、不足则拒答）。强调多租户过滤"绝不能漏"是最常见事故源。
- **Accordion**: 🧪(带 tenant 过滤的引擎) / ❓(为什么过滤要在检索层强制而非靠 prompt) / ⚙️(MetadataFilters 下推、PIINodePostprocessor 脱敏) / 🔀(检索内容当"数据"非"指令"防注入)。
- **`c.source_ref`**: `vector_stores/types.py · MetadataFilters`、`postprocessor/pii.py · NERPIINodePostprocessor`。
- **code①** (verbatim):
```python
from llama_index.core.vector_stores import MetadataFilters, MetadataFilter, FilterOperator

# 多租户隔离：每次检索都强制按 tenant_id 过滤（漏了就是越权事故）
def engine_for(tenant_id):
    flt = MetadataFilters(filters=[
        MetadataFilter(key='tenant_id', value=tenant_id, operator=FilterOperator.EQ)])
    return index.as_query_engine(filters=flt)

print(engine_for('acme').query('我们的合同到期日？'))   # 只看 acme 自己的数据
```
- **code②** (verbatim):
```python
from llama_index.core.postprocessor import NERPIINodePostprocessor

# 把检索到的片段里的 PII（人名/邮箱/电话等）脱敏后再喂给 LLM
engine = index.as_query_engine(node_postprocessors=[NERPIINodePostprocessor()])
```
- **quiz**: 多租户隔离应在哪一层强制（检索 vs prompt）。**interview**: 2 drills（如"如何防止检索到的文档里藏着'忽略以上指令'式的 prompt 注入？"）。
- **Gate + commit** `git commit -m "feat(content): L25 security & guardrails"`.

---

### Task 7 — L26 `26-agents-workflows.html` (Agent 与 Workflows)

**Files:** `src/part6.py` (`LESSON_26`), `src/quizzes.py`, `src/interviews.py`. pipeline(None).
- **Hero `d.compare2`**: 固定管道（每问都同样地检索）vs Agent 循环（看问题→决定用哪个工具/要不要检索→可多步→可反思重检索）。
- **2nd `d.vflow`**: 最小 Workflow 时序：`StartEvent → @step retrieve → @step synthesize → StopEvent`。
- **Deep `c.section`**「从'写死的链'到'会决策的循环'」：何时升级到 agent（多源/多步/需自我纠错），以及代价——更慢、更贵、更难调（呼应 L23 可观测）。
- **Accordion**: 🧪(QueryEngine 包成 tool 给 agent) / ❓(agentic RAG 解决什么) / ⚙️(Workflow 事件驱动 @step；FunctionAgent 用工具) / 🔀(固定管道 vs Router vs Agent 的取舍)。
- **`c.source_ref`**: `workflow/workflow.py · Workflow`、`agent/workflow/function_agent.py · FunctionAgent`（core）。
- **code①** (verbatim):
```python
from llama_index.core import Settings
from llama_index.core.agent import FunctionAgent
from llama_index.core.tools import QueryEngineTool

# 把 RAG 查询引擎包成“工具”，交给会决策的 agent（它自行决定何时/调用几次）
rag_tool = QueryEngineTool.from_defaults(
    query_engine=index.as_query_engine(), name='company_docs',
    description='回答公司制度 / 合同相关问题')
agent = FunctionAgent(tools=[rag_tool], llm=Settings.llm,
                      system_prompt='需要事实时调用 company_docs 工具，并给出处。')
print(await agent.run('对比一下退款政策和换货政策'))
```
- **code②** — **ESCAPING NOTE:** the `->` return annotations MUST be written as `-&gt;` inside the `c.code` string. Source (with real `->` shown for readability):
```python
from llama_index.core import Settings
from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent, Event

class Retrieved(Event):
    nodes: list

class RAGFlow(Workflow):
    @step
    async def retrieve(self, ev: StartEvent) -> Retrieved:
        return Retrieved(nodes=index.as_retriever(similarity_top_k=3).retrieve(ev.query))

    @step
    async def synthesize(self, ev: Retrieved) -> StopEvent:
        return StopEvent(result=str(Settings.llm.complete(f'据此作答：{ev.nodes}')))

# result = await RAGFlow().run(query='退款多久到账？')
```
- **quiz**: 什么时候该从固定管道升级到 agent。**interview**: 2–3 drills（如"agent 让系统更强也更难控，你怎么权衡、怎么评测一个 agentic RAG？"）。
- **Gate + commit** `git commit -m "feat(content): L26 agents & workflows"`.

---
### Task 8 — Glossary: add production terms (L27)

**Files:** Modify `src/glossary.py` (`LESSON_21`, now rendered as `27-glossary.html`).

- [ ] **Step 1:** Append a new grouped section before the closing `)` of `LESSON_21`, reusing the existing `_H` headers and `_row(term, zh, en, num, fname, term_en=None)` helper:

```python
    + c.section(
        L("生产进阶", "Production"),
        c.compare_table(_H, [
            _row("Hybrid Retrieval", "向量 + 关键词(BM25)融合检索", "fuse vector + keyword (BM25) retrieval", "21", "21-production-retrieval.html"),
            _row("Rerank", "用更强模型对召回结果精排", "re-score recall with a stronger model", "21", "21-production-retrieval.html"),
            _row("回归闸 Regression Gate", "评估分数低于阈值则拦截上线", "block release when eval scores drop below a threshold", "22", "22-eval-scale.html", term_en="Regression Gate"),
            _row("可观测 Observability", "追踪每步耗时 / token / 检索结果", "trace per-step latency / tokens / retrieved nodes", "23", "23-observability.html", term_en="Observability"),
            _row("缓存 Caching", "复用 embedding / 响应以省成本降延迟", "reuse embeddings / responses to cut cost & latency", "24", "24-cost-latency.html", term_en="Caching"),
            _row("多租户隔离 Multi-tenant", "强制按 tenant 过滤防越权", "enforce per-tenant filtering to prevent leakage", "25", "25-security.html", term_en="Multi-tenant Isolation"),
            _row("Agent / Workflow", "会决策的循环，按需用工具 / 多步", "a deciding loop that uses tools / multi-step on demand", "26", "26-agents-workflows.html"),
        ]),
    )
```

(Note: `&` in "cost & latency" is fine in this position; if `check_html` flags it, write `&amp;`.)

- [ ] **Step 2: Gate + commit**

Run: `cd src && python build.py && python build_print.py && python check_html.py && python check_links.py && python -m pytest tests -q`
Expected: 0 errors/warnings; the 7 new glossary links resolve.

```bash
git add src/glossary.py index.html lessons/ print.html
git commit -m "feat(content): glossary production terms (L27)"
```

---

## Phase 3 — Finalize

### Task 9: Full verification + final review + merge

- [ ] **Step 1: Confirm every non-glossary lesson (01–26) has ≥2 figures**

Run: `cd src && python build.py && cd .. && python3 -c "import re,glob; bad=[f for f in glob.glob('lessons/*.html') if 'glossary' not in f and open(f,encoding='utf-8').read().count('class=\"fig\"')<2]; print('LOW:', bad)"`
Expected: `LOW: []`.

- [ ] **Step 2: Grep for any hardcoded lesson-count/glossary-number that needs updating**

Run: `grep -rn "21-glossary\|共 21 课\|21 lessons\|len.*== 21" src/ ; echo done`
Expected: no stale references (the registry-structure test from Task 1 now asserts 27; `check_html` count is auto). Fix any that remain.

- [ ] **Step 3: Full build + verify (idempotent + deterministic)**

Run:
```bash
cd src && python build.py && python build_print.py && python -m pytest tests -q && python check_html.py && python check_links.py
cd .. && h1=$(cat index.html lessons/*.html print.html | sha256sum)
cd src && python build.py && python build_print.py && cd ..
h2=$(cat index.html lessons/*.html print.html | sha256sum); [ "$h1" = "$h2" ] && echo DETERMINISTIC || echo DRIFT
```
Expected: all tests pass; `check_html` **0 errors, 0 warnings** with pill "共 27 课 · 7 个部分"; links resolve; `DETERMINISTIC`; tree clean after build.

- [ ] **Step 4: Final code-review subagent** (model claude-opus-4.8) over `git diff main -- src/part6.py src/quizzes.py src/interviews.py src/glossary.py src/registry.py src/shell.py`: verify each lesson's code/source_ref against vendored core 0.14.22 (core APIs) and that integration/third-party snippets are correctly labelled illustrative; check rendering, bilingual balance, ≥2 figs, interview-drill quality. Fix any Should-fix/Blocker findings.

- [ ] **Step 5: Measure depth** (sanity): `python3 -c "import re,glob; [print(f.split('/')[-1], len(re.sub('<[^>]+>','',re.sub(r'<style.*?</style>|<script.*?</script>','',open(f,encoding='utf-8').read(),flags=re.S)))) for f in sorted(glob.glob('lessons/2[1-6]*.html'))]"` — confirm L21–26 are in the ~6–8k range like the rest.

- [ ] **Step 6: Finish the branch** — invoke superpowers:finishing-a-development-branch (verify tests → merge `advanced-track`→`main` ff → delete branch → push → confirm CI + Deploy green → verify lessons live).

---

## Self-Review

**1. Spec coverage:** §1 scope (6 lessons + glossary→27) → Tasks 1–8. §2 renumbering mechanics (registry/shell/check_html auto-count, file migration) → Task 1. §3 per-lesson DoD → Phase-2 Shared DoD. §4 the six content outlines → Tasks 2–7 (one each, matching the spec's table). §5 accuracy/source-ref strategy → Shared DoD bullet + verified API surface in Conventions + Task 9 Step 4 review. §6 verification/success criteria → Task 9. ✓

**2. Placeholder scan:** Task 1's `_skeleton` is a real-but-minimal helper (not a plan placeholder) explicitly replaced in Tasks 2–7; all code snippets are concrete and API-verified; no "TBD/handle edge cases/similar to Task N". ✓

**3. Type/name consistency:** filenames `21-production-retrieval / 22-eval-scale / 23-observability / 24-cost-latency / 25-security / 26-agents-workflows / 27-glossary` used identically in registry, PAGES, SUBTITLES, quizzes, interviews, glossary links, and tests; part labels `P6PROD`/`P7REF`; `_row`/`_H` reused from existing `glossary.py`; verified API names match the Conventions list. ✓
