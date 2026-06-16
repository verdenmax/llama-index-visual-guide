# Part 7–8 Advanced Topics Track Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 9 full lessons (L27–L35) in two new parts — Part 7 "Beyond plain-text RAG" (graph, SQL/Pandas, multimodal, sub-question, structured outputs) and Part 8 "Agentic depth & shipping" (multi-agent, HITL, serving, fine-tuning) — and renumber the glossary to 36.

**Architecture:** Two new content modules `src/part7.py` (`LESSON_27..31`) and `src/part8.py` (`LESSON_32..35`) hold bilingual HTML strings (same pattern as `part1..6.py`). `registry.py` + `shell.py PAGES` register them and move the glossary to `36-glossary.html`; `check_html.py` auto-validates the "共 N 课 · N 个部分" count from `PAGES`, so renumbering is data-driven. Each lesson reuses the existing component/diagram/quiz/interview systems and DoD.

**Tech Stack:** Python 3 stdlib only for build (zero third-party); content authored via `components` (`c.*`), `diagrams` (`d.*`), `i18n.L`; quizzes in `quizzes.py`, interview drills in `interviews.py`. Anchor: llama-index-core 0.14.22.

**Spec:** `docs/superpowers/specs/2026-06-16-advanced-topics-track-design.md`. Branch: `advanced-topics`.

---

## Conventions (every task)
- Work in repo root `/home/verden/course/llama-index-visual-guide` (branch `advanced-topics`).
- Build: `cd src && python build.py && python build_print.py`. Checks: `python check_html.py && python check_links.py`. Tests: `cd src && python -m pytest tests -q`.
- Commit at end of each task with the Copilot trailer; commit regenerated `index.html lessons/ print.html` too.
- Zero third-party imports in `src/*.py` (except `src/tests/`).
- Escaping: inside `c.code(...)` escape `<` `>` `&`; diagram labels/captions may use literal `→ · ✓ “”`; never a bare `&` (use `&amp;`).
- DoD per lesson: `c.pipeline(stage)` + `c.lead`; `c.section`s; **≥2** `d.*` figures (each a distinct "aha"); ≥1 `c.code` + ≥1 `c.source_ref`; `c.analogy` + `c.key_points`; quizzes ≥1 MCQ + ≥1 open; interviews 2–3 drills each leading with `🔑`; bilingual balance.

### Verified API surface (use these exact names; all confirmed in vendored core 0.14.22 unless marked *(integration)*)
- **L27 Graph:** `from llama_index.core import PropertyGraphIndex`; extractors `SimpleLLMPathExtractor` / `SchemaLLMPathExtractor` / `ImplicitPathExtractor` and retrievers `LLMSynonymRetriever` / `VectorContextRetriever` (`llama_index.core.indices.property_graph`). Legacy mention only: `KnowledgeGraphIndex`.
- **L28 SQL/Pandas:** `from llama_index.core import SQLDatabase`; `from llama_index.core.query_engine import NLSQLTableQueryEngine, SQLTableRetrieverQueryEngine`; `from llama_index.core.query_engine import PandasQueryEngine` (`query_engine/pandas/pandas_query_engine.py`). For big schemas: `ObjectIndex` + `SQLTableNodeMapping` (`llama_index.core.objects`).
- **L29 Multimodal:** `from llama_index.core.indices import MultiModalVectorStoreIndex`; `from llama_index.core.multi_modal_llms import MultiModalLLM` (base); `from llama_index.core.schema import ImageNode, ImageDocument`; `SimpleDirectoryReader`. *(integration)* concrete models e.g. `OpenAIMultiModal`, CLIP embeddings.
- **L30 Sub-question:** `from llama_index.core.query_engine import SubQuestionQueryEngine`; `from llama_index.core.tools import QueryEngineTool, ToolMetadata`.
- **L31 Structured outputs:** `from llama_index.core.program import LLMTextCompletionProgram, FunctionCallingProgram`; `llm.structured_predict(MyModel, prompt)` (`llms/llm.py`); `pydantic.BaseModel`.
- **L32 Multi-agent/workflow:** `from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent, ReActAgent`; `from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent, Event, Context`.
- **L33 HITL:** `from llama_index.core.workflow import InputRequiredEvent, HumanResponseEvent, Context` (re-exported via `workflow/__init__.py`).
- **L34 Serving:** *(integration / non-core — illustrative only)* FastAPI wrapping `index.as_query_engine()`, `await qe.aquery(...)` / streaming (core), `llama-deploy`, `create-llama`.
- **L35 Fine-tuning:** *(integration — illustrative only)* `generate_qa_embedding_pairs`, `SentenceTransformersFinetuneEngine` (`llama-index-finetuning`).

## File Structure
| File | Responsibility |
|---|---|
| `src/part7.py` | NEW. `LESSON_27..31` (beyond-text RAG). `import components as c`, `import diagrams as d`, `import i18n`, `from i18n import L`. |
| `src/part8.py` | NEW. `LESSON_32..35` (agentic depth & shipping). Same imports. |
| `src/registry.py` | MODIFY. `import part7, part8`; add 27–35 → `part7/part8.LESSON_*`; glossary key → `36-glossary.html`. |
| `src/shell.py` | MODIFY. `PAGES` += 9 (new `P7`=Beyond-text, `P8`=Agentic); glossary row → `36-glossary.html` with `P9`=Reference. `SUBTITLES` += 9 + glossary key→36. |
| `src/quizzes.py` | MODIFY. `QUIZZES` += 27–35 (≥1 MCQ + 1 open each). |
| `src/interviews.py` | MODIFY. `INTERVIEW` += 27–35 (2–3 drills each, 🔑 + some figs). |
| `src/glossary.py` | MODIFY. Add a new "进阶专题 / Advanced topics" group of terms. |
| `src/tests/test_registry_structure.py` | MODIFY. 36 lessons, glossary last, 9 parts. |
| `lessons/27-glossary.html` | `git rm` (build emits `36-glossary.html`). |
| `index.html`, `lessons/`, `print.html` | Regenerated artifacts (committed). |

---

## Task 1: Scaffolding — modules, renumbering, green build

**Files:**
- Create: `src/part7.py`, `src/part8.py`
- Modify: `src/registry.py`, `src/shell.py`, `src/tests/test_registry_structure.py`
- Delete: `lessons/27-glossary.html`

- [ ] **Step 1: Update the structure test to the new shape** — `src/tests/test_registry_structure.py`. Replace the count assertions:

```python
import registry
import shell


def test_36_lessons_and_glossary_last():
    keys = list(registry.CONTENT.keys())
    assert len(keys) == 36
    assert keys[-1] == "36-glossary.html"            # glossary renumbered + last
    assert "27-graph-rag.html" in keys               # first beyond-text lesson
    assert "31-structured-outputs.html" in keys      # last Part 7 lesson
    assert "32-multi-agent.html" in keys             # first Part 8 lesson
    assert "35-finetuning-embeddings.html" in keys   # last Part 8 lesson


def test_pages_has_nine_parts():
    parts = {p[2].zh for p in shell.PAGES}
    assert len(parts) == 9                            # was 7 → +Beyond-text +Agentic
    assert len(shell.PAGES) == 36
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd src && python -m pytest tests/test_registry_structure.py -q`
Expected: FAIL (registry has 27 keys, glossary is `27-glossary.html`).

- [ ] **Step 3: Create `src/part7.py` with 5 minimal-valid skeleton lessons**

Each skeleton must satisfy `check_html` (≥2 `d.fig`, an analogy card, a key-points card, bilingual). Repeat this block for 27–31, changing the title/stage/pipeline:

```python
"""Part 7 (beyond plain-text RAG): lessons 27-31. Content filled task-by-task."""
import components as c
import diagrams as d
import i18n
from i18n import L


def _skeleton(stage, zh_topic, en_topic):
    return (
        c.pipeline(stage)
        + c.lead(L(f"本课讲 <strong>{zh_topic}</strong>（内容完善中）。",
                   f"This lesson covers <strong>{en_topic}</strong> (being written)."))
        + d.flow([("a", L("场景", "Scenario")), ("b", L("做法", "Approach")), ("c", L("权衡", "Trade-off"))],
                 caption=L("占位流程图", "placeholder flow"))
        + d.compare2((L("不做", "Without"), i18n.render(L("有什么问题", "what breaks"))),
                     (L("做了", "With"), i18n.render(L("解决什么", "what it fixes"))),
                     caption=L("占位对照", "placeholder compare"))
        + c.analogy(L("占位类比。", "Placeholder analogy."))
        + c.key_points([L("本课要点占位。", "Key-points placeholder.")])
    )


LESSON_27 = _skeleton("index", "图谱 RAG", "Graph RAG")
LESSON_28 = _skeleton("retrieve", "结构化数据查询（SQL & Pandas）", "querying structured data (SQL & Pandas)")
LESSON_29 = _skeleton("embed", "多模态 RAG", "multimodal RAG")
LESSON_30 = _skeleton("retrieve", "查询分解（Sub-Question）", "query decomposition (Sub-Question)")
LESSON_31 = _skeleton("synthesize", "结构化输出", "structured outputs")
```

- [ ] **Step 4: Create `src/part8.py` with 4 minimal-valid skeleton lessons** — same `_skeleton` helper, copy it into `part8.py` (each module self-contained; do NOT import across part modules):

```python
"""Part 8 (agentic depth & shipping): lessons 32-35. Content filled task-by-task."""
import components as c
import diagrams as d
import i18n
from i18n import L


def _skeleton(stage, zh_topic, en_topic):
    return (
        c.pipeline(stage)
        + c.lead(L(f"本课讲 <strong>{zh_topic}</strong>（内容完善中）。",
                   f"This lesson covers <strong>{en_topic}</strong> (being written)."))
        + d.flow([("a", L("场景", "Scenario")), ("b", L("做法", "Approach")), ("c", L("权衡", "Trade-off"))],
                 caption=L("占位流程图", "placeholder flow"))
        + d.compare2((L("不做", "Without"), i18n.render(L("有什么问题", "what breaks"))),
                     (L("做了", "With"), i18n.render(L("解决什么", "what it fixes"))),
                     caption=L("占位对照", "placeholder compare"))
        + c.analogy(L("占位类比。", "Placeholder analogy."))
        + c.key_points([L("本课要点占位。", "Key-points placeholder.")])
    )


LESSON_32 = _skeleton("answer", "多智能体与工作流控制流", "multi-agent & workflow control flow")
LESSON_33 = _skeleton("answer", "人在回路（HITL）", "human-in-the-loop")
LESSON_34 = _skeleton("answer", "把 RAG 上线成服务", "serving your RAG")
LESSON_35 = _skeleton("embed", "微调 embedding", "fine-tuning embeddings")
```

- [ ] **Step 5: Wire `src/registry.py`** — add `import part7` and `import part8` (after `import part6`), insert the 9 entries before glossary, and renumber glossary. The new `CONTENT` tail becomes:

```python
    "26-agents-workflows.html": part6.LESSON_26,
    "27-graph-rag.html": part7.LESSON_27,
    "28-structured-data.html": part7.LESSON_28,
    "29-multimodal-rag.html": part7.LESSON_29,
    "30-sub-question.html": part7.LESSON_30,
    "31-structured-outputs.html": part7.LESSON_31,
    "32-multi-agent.html": part8.LESSON_32,
    "33-human-in-the-loop.html": part8.LESSON_33,
    "34-serving.html": part8.LESSON_34,
    "35-finetuning-embeddings.html": part8.LESSON_35,
    "36-glossary.html": glossary.LESSON_21,
```

- [ ] **Step 6: Wire `src/shell.py PAGES` + `SUBTITLES`** — exact edits (current part labels at lines 39–45; `PAGES` tuples are `("NN-slug.html", L(zh,en), PART)`; `SUBTITLES` dict at ~line 106; titles with `&` must be `&amp;`).

(a) After `P6PROD`/`P7REF` (line ~45), define the two new parts and rename the reference label to Part 9 (replace `P7REF`'s definition + its single use on the glossary row with `P9REF`):
```python
P7BEYOND = L("第七部分 · 超越文本 RAG", "Part 7 · Beyond Plain-Text RAG")
P8AGENT = L("第八部分 · Agentic 进阶与上线", "Part 8 · Agentic Depth & Shipping")
P9REF = L("第九部分 · 速查", "Part 9 · Reference")
```

(b) In `PAGES`, after the `26-agents-workflows.html` row, insert the 9 rows and replace the old `27-glossary.html` row with the renumbered glossary row:
```python
    ("27-graph-rag.html", L("图谱 RAG", "Graph RAG"), P7BEYOND),
    ("28-structured-data.html", L("结构化数据查询", "Querying Structured Data"), P7BEYOND),
    ("29-multimodal-rag.html", L("多模态 RAG", "Multimodal RAG"), P7BEYOND),
    ("30-sub-question.html", L("查询分解 Sub-Question", "Query Decomposition"), P7BEYOND),
    ("31-structured-outputs.html", L("结构化输出", "Structured Outputs"), P7BEYOND),
    ("32-multi-agent.html", L("多智能体与控制流", "Multi-Agent Workflows"), P8AGENT),
    ("33-human-in-the-loop.html", L("人在回路 HITL", "Human-in-the-Loop"), P8AGENT),
    ("34-serving.html", L("上线服务", "Serving Your RAG"), P8AGENT),
    ("35-finetuning-embeddings.html", L("微调 Embedding", "Fine-Tuning Embeddings"), P8AGENT),
    ("36-glossary.html", L("术语表 · 概念索引", "Glossary &amp; Concept Index"), P9REF),
```

(c) In `SUBTITLES`, change the glossary key `27-glossary.html`→`36-glossary.html` and add 9 entries (keep them short; no bare `&`):
```python
    "27-graph-rag.html": L("实体-关系多跳检索", "multi-hop over entities and relations"),
    "28-structured-data.html": L("文字转 SQL / 表格分析", "text-to-SQL and table analysis"),
    "29-multimodal-rag.html": L("图文同空间检索", "text and images in one space"),
    "30-sub-question.html": L("拆子问题再汇总", "split into sub-questions, then combine"),
    "31-structured-outputs.html": L("LLM 直出 Pydantic 对象", "LLM emits typed objects"),
    "32-multi-agent.html": L("多 agent 分工 + 工作流控制流", "agents with handoffs; workflow control flow"),
    "33-human-in-the-loop.html": L("高风险动作前人工确认", "human confirmation before risky actions"),
    "34-serving.html": L("把 RAG 包成服务上线", "wrap RAG as a service"),
    "35-finetuning-embeddings.html": L("用 QA 对微调领域 embedding", "fine-tune domain embeddings with QA pairs"),
    "36-glossary.html": L("术语一句话查 + 跳转", "one-line term lookup + jump"),
```

- [ ] **Step 7: Remove the stale glossary artifact**

Run: `git rm lessons/27-glossary.html`

- [ ] **Step 8: Build + verify the scaffold is green**

Run: `cd src && python build.py && python build_print.py && python check_html.py && python check_links.py && python -m pytest tests -q`
Expected: build writes `36-glossary.html` + 9 new lessons; `check_html` reports **36 lessons + index, 0 errors/0 warnings**; `check_links` all resolve; pytest green (incl. the updated structure test).

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "feat(part7-8): scaffold advanced-topics tracks (lessons 27-35) + renumber glossary to 36

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Stage 1 — Part 7 lessons (L27–L31)

### Task 2 — L27 Graph RAG (`27-graph-rag.html`)

**Files:** Modify `src/part7.py` (`LESSON_27`), `src/quizzes.py`, `src/interviews.py`.

- [ ] **Step 1: Replace `LESSON_27`** — `c.pipeline("index")`. Sections (bilingual prose per spec §5): ① 为什么图谱 — 向量召回"相似片段"，图谱召回"连起来的事实"，多跳关系(A→B→C)纯向量答不出；② 怎么建 — `PropertyGraphIndex` + path extractors 抽实体/关系；③ 怎么查 — sub-retrievers 同义词扩展 + 向量上下文；④ 何时用 — 关系密集/多跳问答用图，普通相似检索用向量。`c.analogy`：向量像"找长得像的书页"，图谱像"顺着引用链翻"。`c.key_points`。

- [ ] **Step 2: code① + source_ref** — verbatim (no `<>&` to escape):

```python
from llama_index.core import PropertyGraphIndex
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor

index = PropertyGraphIndex.from_documents(
    documents,
    kg_extractors=[SchemaLLMPathExtractor(llm=llm)],   # LLM 抽 实体-关系-实体
)
qe = index.as_query_engine(include_text=True)
print(qe.query("X-2000 和它的替代型号有什么兼容差异？"))
```
`c.source_ref("indices/property_graph/base.py", "PropertyGraphIndex", L("从文档抽取实体/关系建成属性图，可多跳检索。", "builds a property graph of entities/relations from docs for multi-hop retrieval."))`.

- [ ] **Step 3: Add ≥2 figures** — verbatim:

```python
    + d.annot(
        L("实体：X-2000", "Entity: X-2000"),
        [
            (L("属于 → 产品线 A", "belongs to → line A"), L("一跳", "1 hop")),
            (L("兼容 → 配件 B", "compatible with → part B"), L("一跳", "1 hop")),
            (L("替代 → 旧款 X-1000", "replaces → old X-1000"), L("可继续多跳", "hop again")),
        ],
        caption=L("图谱把事实存成 实体—关系—实体 三元组，可顺着边多跳遍历",
                  "a graph stores facts as entity—relation—entity triples you can traverse hop by hop"),
    )
    + d.compare2(
        (L("向量检索", "Vector"), i18n.render(L("取回 top-k <strong>相似</strong>片段；跨片段的关系丢失",
                                               "fetches top-k <strong>similar</strong> chunks; cross-chunk relations are lost"))),
        (L("图谱检索", "Graph"), i18n.render(L("沿 实体→关系→实体 <strong>多跳</strong>找到连起来的事实",
                                              "walks entity→relation→entity to find <strong>connected</strong> facts"))),
        caption=L("同一问题：向量看“像不像”，图谱看“连不连”", "Same question: vector asks ‘similar?’, graph asks ‘connected?’"),
    )
```

- [ ] **Step 4: Quiz** — in `src/quizzes.py`, key `"27-graph-rag.html"`: 1 MCQ + 1 open.
  - MCQ: "下列哪种问题最该用图谱 RAG 而非纯向量？" options: [A "找与‘退款政策’语义相近的段落", B "X 的供应商的总部在哪个国家（多跳）"✓, C "这段话的情感是正还是负", D "把文档翻译成英文"]; explain B 是多跳关系查询。
  - Open: "你的知识库是产品-配件-兼容关系网，为什么图谱比向量更合适？答题点：关系/多跳/可解释路径。"

- [ ] **Step 5: Interview drills** — in `src/interviews.py`, key `"27-graph-rag.html"`: 2–3 drills, each leading `🔑`. e.g. ①"图谱 RAG 的抽取（extractor）质量差会怎样、怎么控？"(🔑 schema 约束 + 评估抽取准确率)；②"什么时候 <em>不</em> 该上图谱？"(🔑 关系稀疏/成本高时向量更划算)；配一张 `d.grid` 比较 PropertyGraph vs KnowledgeGraph(legacy) vs 纯向量（关系表达/构建成本/可解释）。

- [ ] **Step 6: Gate + commit** — `git commit -m "feat(content): L27 graph RAG"` (per Conventions).

### Task 3 — L28 Structured data: SQL & Pandas (`28-structured-data.html`)

**Files:** Modify `src/part7.py` (`LESSON_28`), `src/quizzes.py`, `src/interviews.py`.

- [ ] **Step 1: Replace `LESSON_28`** — `c.pipeline("retrieve")`. Sections: ① 痛点 — 数字/聚合/精确筛选塞进向量必然不准；② text-to-SQL — 让 LLM 写 SQL、DB 执行精确计算（大库用 `SQLTableRetrieverQueryEngine` + ObjectIndex 先选表）；③ Pandas — 内存表交 `PandasQueryEngine`；④ 安全 — Pandas 引擎执行 LLM 生成的 Python，须沙箱/限信任。`c.analogy`：向量是"模糊回忆"，SQL 是"拿计算器精确算"。

- [ ] **Step 2: code①②  + source_ref** — verbatim:

```python
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine

sql_db = SQLDatabase(engine, include_tables=["orders"])
qe = NLSQLTableQueryEngine(sql_database=sql_db, tables=["orders"])
print(qe.query("上个月每个区域的总销售额是多少，降序排列？"))
```
```python
from llama_index.core.query_engine import PandasQueryEngine

qe = PandasQueryEngine(df=df, verbose=True)   # ⚠️ 会执行 LLM 生成的 Python，仅用于可信环境
print(qe.query("销量最高的 3 个产品是哪些？"))
```
`c.source_ref("indices/struct_store/sql_query.py", "NLSQLTableQueryEngine", L("把自然语言转成 SQL 在数据库上执行。", "turns NL into SQL executed on the database."))`.

- [ ] **Step 3: Add ≥2 figures** — verbatim:

```python
    + d.flow([
        ("q", L("自然语言问题", "NL question")),
        ("sql", L("LLM 写 SQL", "LLM writes SQL"), L("据表结构", "from schema")),
        ("run", L("数据库执行", "DB executes"), L("精确计算", "exact compute")),
        ("ans", L("自然语言答案", "NL answer")),
    ], active="run", caption=L("text-to-SQL：把精确计算交给数据库，LLM 只负责翻译",
                               "text-to-SQL: hand exact compute to the DB; the LLM only translates"))
    + d.grid(
        [L("数据形态", "Data shape"), L("最该用", "Best tool"), L("为什么", "Why")],
        [
            [L("非结构化文档", "unstructured docs"), L("向量检索", "vector"), L("语义相似", "semantic similarity")],
            [L("数据库表（大）", "DB tables (large)"), L("text-to-SQL", "text-to-SQL"), L("精确聚合/筛选", "exact aggregation")],
            [L("内存 DataFrame", "in-memory DataFrame"), L("PandasQueryEngine", "PandasQueryEngine"), L("快速表分析", "quick table analysis")],
        ],
        caption=L("按数据形态选工具——数字别硬塞向量", "pick by data shape — don't force numbers into vectors"),
    )
```

- [ ] **Step 4: Quiz** — key `"28-structured-data.html"`: MCQ "‘各区域季度环比增长率’最该用？" [A 向量检索, B text-to-SQL✓, C rerank, D HyDE]，解释聚合计算要交数据库；Open: "为什么 PandasQueryEngine 要特别小心？答题点：执行 LLM 生成代码 → 注入/越权风险 → 沙箱。"

- [ ] **Step 5: Interview drills** — key `"28-structured-data.html"`: ①"text-to-SQL 在大库上准确率低，怎么提升？"(🔑 先用 ObjectIndex 选相关表 + few-shot + 限定列)；②"结构化与非结构化混合的问题怎么路由？"(🔑 RouterQueryEngine 按问题类型分流，呼应 L18)。

- [ ] **Step 6: Gate + commit** — `git commit -m "feat(content): L28 structured-data (SQL & Pandas)"`.

### Task 4 — L29 Multimodal RAG (`29-multimodal-rag.html`)

**Files:** Modify `src/part7.py` (`LESSON_29`), `src/quizzes.py`, `src/interviews.py`.

- [ ] **Step 1: Replace `LESSON_29`** — `c.pipeline("embed")`. Sections: ① 图文进同一向量空间 → 文字查图、图查图；② 建多模态索引（图像 store + 文本 store）；③ 检索件 + 生成件都要换多模态版（具体模型走集成）；④ 适用 — 图表/截图/产品图问答。`c.analogy`：把图和字翻译成"同一种坐标"，就能互相检索。

- [ ] **Step 2: code① + source_ref** — verbatim:

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.indices import MultiModalVectorStoreIndex

documents = SimpleDirectoryReader("./mixed_docs").load_data()   # 文本 + 图片
index = MultiModalVectorStoreIndex.from_documents(documents)
qe = index.as_query_engine(multi_modal_llm=mm_llm)              # mm_llm 走集成（如 OpenAIMultiModal）
print(qe.query("图里这台设备的型号和接口数量是多少？"))
```
`c.source_ref("indices/multi_modal/base.py", "MultiModalVectorStoreIndex", L("文本与图像各建向量库，统一检索。", "separate text/image vector stores, retrieved together."))` + integration 注：具体多模态模型在 core 之外。

- [ ] **Step 3: Add ≥2 figures** — verbatim:

```python
    + d.compare2(
        (L("文本路径", "Text path"), i18n.render(L("文字 → 文本 embedding", "text → text embedding"))),
        (L("图像路径", "Image path"), i18n.render(L("图片 → 图像 embedding", "image → image embedding"))),
        caption=L("两条路径映到<strong>同一向量空间</strong>，于是能跨模态互相检索",
                  "both map into the <strong>same vector space</strong>, enabling cross-modal retrieval"),
    )
    + d.flow([
        ("q", L("问题（文/图）", "query (text/img)")),
        ("ret", L("跨模态检索", "cross-modal retrieve"), L("图+文都召回", "images + text")),
        ("mm", L("多模态 LLM", "multimodal LLM"), L("看图作答", "reads images")),
        ("ans", L("答案", "answer")),
    ], caption=L("多模态 RAG：检索召回图与文，再交会看图的 LLM 合成",
                 "multimodal RAG: retrieve images+text, then a vision-capable LLM synthesizes"))
```

- [ ] **Step 4: Quiz** — key `"29-multimodal-rag.html"`: MCQ "多模态 RAG 能‘用文字查图’的前提是？" [A 图和文在同一向量空间✓, B 图先转文字, C 用更大的 LLM, D 关闭 rerank]；Open: "纯文字 RAG 遇到‘这张架构图说明了什么’为什么无能为力、多模态怎么解决？"

- [ ] **Step 5: Interview drills** — key `"29-multimodal-rag.html"`: ①"多模态 RAG 成本/延迟更高，怎么权衡？"(🔑 仅图文必要时启用，文本优先 + 图像按需)；②"评估多模态 RAG 与纯文本有何不同？"(🔑 需含图的金标问答，呼应 L19/L22)。

- [ ] **Step 6: Gate + commit** — `git commit -m "feat(content): L29 multimodal RAG"`.

### Task 5 — L30 Query decomposition / Sub-Question (`30-sub-question.html`)

**Files:** Modify `src/part7.py` (`LESSON_30`), `src/quizzes.py`, `src/interviews.py`.

- [ ] **Step 1: Replace `LESSON_30`** — `c.pipeline("retrieve")`. Sections: ① 痛点 — 对比/跨源/多步问题单次 top-k 答不全；② SubQuestion — 自动把母问题拆成子问题，每个路由到对应 `QueryEngineTool`，再汇总；③ 与 L18 区别 — L18 是"换更强检索器"，这里是"拆问题 + 多引擎编排"。`c.analogy`：像把一道复杂题拆成几个小题分别查资料，再合并。

- [ ] **Step 2: code① + source_ref** — verbatim:

```python
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata

tools = [
    QueryEngineTool(query_engine=qe_2022, metadata=ToolMetadata(name="y2022", description="2022 年财报")),
    QueryEngineTool(query_engine=qe_2023, metadata=ToolMetadata(name="y2023", description="2023 年财报")),
]
engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=tools)
print(engine.query("2023 年的营收比 2022 年增长了多少？"))   # 自动拆成两个子问题再相减
```
`c.source_ref("query_engine/sub_question_query_engine.py", "SubQuestionQueryEngine", L("把复杂问题拆成子问题分别路由检索再汇总。", "splits a complex question into sub-questions, routes each, then aggregates."))`.

- [ ] **Step 3: Add ≥2 figures** — verbatim:

```python
    + d.vflow([
        (L("母问题：2023 比 2022 增长多少？", "Q: growth 2023 vs 2022?"), L("LLM 拆解", "LLM decomposes")),
        (L("子问 q1：2023 营收？ → y2023 工具", "sub-q1: 2023 revenue? → y2023"),),
        (L("子问 q2：2022 营收？ → y2022 工具", "sub-q2: 2022 revenue? → y2022"),),
        (L("汇总两答相减 → 最终答案", "combine the two → final answer"),),
    ], caption=L("Sub-Question：拆 → 各自检索 → 汇总，单次 top-k 做不到的对比题这样答",
                 "Sub-Question: split → retrieve each → combine; answers comparisons a single top-k can't"))
    + d.annot(
        L("母问题", "parent question"),
        [
            (L("子问题 1", "sub-question 1"), L("→ 工具 A", "→ tool A")),
            (L("子问题 2", "sub-question 2"), L("→ 工具 B", "→ tool B")),
            (L("汇总", "aggregate"), L("综合作答", "synthesize")),
        ],
        caption=L("一个母问题扇出到多个数据源工具，再收敛成一个答案",
                  "one parent question fans out to several source tools, then converges to one answer"),
    )
```

- [ ] **Step 4: Quiz** — key `"30-sub-question.html"`: MCQ "SubQuestionQueryEngine 最擅长？" [A 单文档相似检索, B 跨多个来源的对比/多步问题✓, C 压缩 prompt, D 流式输出]；Open: "‘对比 A、B 两份合同的违约条款差异’为什么适合 sub-question？答题点：拆子问 + 各自检索 + 汇总。"

- [ ] **Step 5: Interview drills** — key `"30-sub-question.html"`: ①"sub-question 拆错/子问跑偏怎么办？"(🔑 工具 description 要准 + 限定子问数量 + 可观测每个子问，呼应 L23)；②"它和 Router、Agent 有何区别？"(🔑 Router 选一条；SubQuestion 拆成多条并行汇总；Agent 动态循环——为 L32 铺垫)。

- [ ] **Step 6: Gate + commit** — `git commit -m "feat(content): L30 sub-question decomposition"`.

### Task 6 — L31 Structured outputs (`31-structured-outputs.html`)

**Files:** Modify `src/part7.py` (`LESSON_31`), `src/quizzes.py`, `src/interviews.py`.

- [ ] **Step 1: Replace `LESSON_31`** — `c.pipeline("synthesize")`. Sections: ① 痛点 — 用正则/手工 parse 自由文本脆弱易碎；② Pydantic program — 直接让 LLM 产出 `BaseModel` 对象，类型即契约；③ 两条路 — `LLMTextCompletionProgram`(模板) 与 `FunctionCallingProgram`/`structured_predict`(函数调用)；④ 用途 — 抽取、表单填充、把 RAG 答案结构化给下游。`c.analogy`：与其让对方写一段话你再猜重点，不如直接给一张"表格让他填"。

- [ ] **Step 2: code① + source_ref** — verbatim (escape none needed; keep ASCII in code):

```python
from pydantic import BaseModel
from llama_index.core.program import LLMTextCompletionProgram

class Invoice(BaseModel):
    vendor: str
    total: float
    due_date: str

program = LLMTextCompletionProgram.from_defaults(
    output_cls=Invoice,
    prompt_template_str="Extract the invoice fields from:\n{doc}",
)
invoice = program(doc=text)     # -> Invoice(vendor=..., total=..., due_date=...)
```
也可一行：`invoice = llm.structured_predict(Invoice, prompt)`。
`c.source_ref("program/llm_program.py", "LLMTextCompletionProgram", L("按 Pydantic 模型约束 LLM 输出为结构化对象。", "constrains LLM output to a structured Pydantic object."))`.

- [ ] **Step 3: Add ≥2 figures** — verbatim:

```python
    + d.compare2(
        (L("自由文本 + 手工 parse", "Free text + manual parse"),
         i18n.render(L("LLM 写一段话 → 正则/分割提字段 → 措辞一变就<strong>碎</strong>",
                       "LLM writes prose → regex/split fields → <strong>breaks</strong> when wording shifts"))),
        (L("结构化输出", "Structured output"),
         i18n.render(L("LLM 直接产出 <strong>Pydantic 对象</strong> → 类型校验 → 下游直接用",
                       "LLM emits a <strong>Pydantic object</strong> → type-validated → ready downstream"))),
        caption=L("把“解析自由文本”换成“契约化的类型”", "swap ‘parse free text’ for ‘a typed contract’"),
    )
    + d.flow([
        ("schema", L("定义 Pydantic 模型", "define Pydantic model")),
        ("prompt", L("Program 组 prompt", "program builds prompt")),
        ("llm", L("LLM 产出", "LLM emits")),
        ("valid", L("校验/重试", "validate/retry"), L("不合格再来", "retry if invalid")),
        ("obj", L("类型化对象", "typed object")),
    ], active="valid", caption=L("结构化输出管道：模型即 schema，校验保证可用",
                                 "structured-output pipeline: the model is the schema; validation guarantees usability"))
```

- [ ] **Step 4: Quiz** — key `"31-structured-outputs.html"`: MCQ "为什么用 Pydantic program 而非正则 parse LLM 文本？" [A 类型校验+契约稳定✓, B 更省 token, C 不用 LLM, D 自动多模态]；Open: "把 RAG 的答案变成 {answer, sources, confidence} 结构有什么工程价值？答题点：下游可用/可校验/可监控。"

- [ ] **Step 5: Interview drills** — key `"31-structured-outputs.html"`: ①"LLM 输出不符合 schema 怎么办？"(🔑 校验 + 重试/修复，function-calling 更稳)；②"structured output 和 function/tool calling 是什么关系？"(🔑 同一机制：约束模型产出结构，工具调用即结构化参数——为 L32 铺垫)。

- [ ] **Step 6: Gate + commit** — `git commit -m "feat(content): L31 structured outputs"`.

---

## Stage 2 — Part 8 lessons (L32–L35)

### Task 7 — L32 Multi-agent & workflow control flow (`32-multi-agent.html`)

**Files:** Modify `src/part8.py` (`LESSON_32`), `src/quizzes.py`, `src/interviews.py`.

- [ ] **Step 1: Replace `LESSON_32`** — `c.pipeline("answer")`. Sections: ① 单 agent 不够 → 多 agent 分工 + 交接(handoff)；② `AgentWorkflow` 编排多 agent；③ 底层是 workflow：`@step` + 事件显式表达分支/循环（承 L26）；④ 取舍 — 越多 agent 越强也越难调，先用最简的。`c.analogy`：从"一个全能选手"到"一支有分工、会交接的小队"。

- [ ] **Step 2: code①②  + source_ref** — verbatim (no `<>&` in code; union `|` is fine):

```python
from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent

research = FunctionAgent(name="research", tools=[search_tool], llm=llm,
                         system_prompt="查资料，把要点交给 writer", can_handoff_to=["write"])
write = FunctionAgent(name="write", tools=[], llm=llm, system_prompt="据要点写成答复")
workflow = AgentWorkflow(agents=[research, write], root_agent="research")
resp = await workflow.run(user_msg="写一段关于 X-2000 的简报")
```
```python
from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent, Event

class Retrieved(Event):
    nodes: list

class RAGFlow(Workflow):
    @step
    async def route(self, ev: StartEvent) -> Retrieved | StopEvent:
        if is_trivial(ev.query):
            return StopEvent(result="直接答，无需检索")   # 分支：跳过检索
        return Retrieved(nodes=retrieve(ev.query))
```
`c.source_ref("agent/workflow/multi_agent_workflow.py", "AgentWorkflow", L("编排多个 agent 协作与交接(handoff)。", "orchestrates multiple agents with handoffs."))`.

- [ ] **Step 3: Add ≥2 figures** — verbatim:

```python
    + d.flow([
        ("user", L("用户问题", "user query")),
        ("research", L("research agent", "research agent"), L("查资料", "gathers facts")),
        ("write", L("write agent", "write agent"), L("handoff 后写答", "writes after handoff")),
        ("review", L("review agent", "review agent"), L("复核把关", "checks")),
    ], caption=L("多智能体：按角色分工，用 handoff 把任务交给下一个专家",
                 "multi-agent: split by role, hand off the task to the next specialist"))
    + d.vflow([
        (L("StartEvent 进入", "StartEvent in"), L("路由 @step", "router @step")),
        (L("分支：琐碎问题 → StopEvent 直接答", "branch: trivial → StopEvent"),),
        (L("否则 → Retrieved 事件 → 合成 @step", "else → Retrieved → synth @step"),),
        (L("StopEvent 出", "StopEvent out"),),
    ], caption=L("workflow 用事件显式表达分支/循环——控制流看得见、可测",
                 "a workflow makes branches/loops explicit as events — visible, testable control flow"))
```

- [ ] **Step 4: Quiz** — key `"32-multi-agent.html"`: MCQ "AgentWorkflow 里的 handoff 指？" [A 把任务移交给另一个 agent✓, B 关闭工具, C 压缩历史, D 切换模型]；Open: "什么时候该从单 agent 升级到多 agent？答题点：职责清晰可拆/单 agent prompt 过载/需专精分工。"

- [ ] **Step 5: Interview drills** — key `"32-multi-agent.html"`: ①"多 agent 更强但更难控，你怎么评测与调试？"(🔑 给每次 handoff/工具调用加 trace，呼应 L23；定义任务级评测)；②"workflow 的事件模型相比写死的 if-else 链有什么好处？"(🔑 分支/循环显式化、可单测每个 @step、可流式观测)。

- [ ] **Step 6: Gate + commit** — `git commit -m "feat(content): L32 multi-agent & workflow control flow"`.

### Task 8 — L33 Human-in-the-loop (`33-human-in-the-loop.html`)

**Files:** Modify `src/part8.py` (`LESSON_33`), `src/quizzes.py`, `src/interviews.py`.

- [ ] **Step 1: Replace `LESSON_33`** — `c.pipeline("answer")`. Sections: ① 为什么 HITL — 高风险动作（下单/删库/外发）不能全自动；② 机制 — workflow 发 `InputRequiredEvent` 挂起、外部回 `HumanResponseEvent` 再恢复；③ 落点 — 审批闸、低置信度兜底、敏感工具确认。`c.analogy`：像支付前的"二次确认弹窗"。

- [ ] **Step 2: code① + source_ref** — verbatim:

```python
from llama_index.core.workflow import (Workflow, step, StartEvent, StopEvent,
                                        InputRequiredEvent, HumanResponseEvent)

class ApprovalFlow(Workflow):
    @step
    async def act(self, ev: StartEvent) -> InputRequiredEvent:
        return InputRequiredEvent(prefix="确认要执行『删除账户』吗？(yes/no)")   # 挂起，等人

    @step
    async def finish(self, ev: HumanResponseEvent) -> StopEvent:
        ok = ev.response.strip().lower() == "yes"
        return StopEvent(result="已执行" if ok else "已取消")
```
`c.source_ref("workflow/__init__.py", "InputRequiredEvent / HumanResponseEvent", L("workflow 暂停向人请求输入，拿到回应再继续。", "the workflow pauses to ask a human, then resumes on their response."))`.

- [ ] **Step 3: Add ≥2 figures** — verbatim:

```python
    + d.flow([
        ("act", L("准备高风险动作", "about to act")),
        ("ask", L("发 InputRequired", "emit InputRequired"), L("挂起等待", "pause & wait")),
        ("human", L("人确认", "human decides"), L("yes / no", "yes / no")),
        ("done", L("继续 / 中止", "continue / abort")),
    ], active="ask", caption=L("人在回路：危险动作前暂停，拿到人的确认再继续",
                               "HITL: pause before a risky action, resume only on human confirmation"))
    + d.compare2(
        (L("全自动", "Fully automatic"), i18n.render(L("快，但删错/下错单<strong>无法挽回</strong>",
                                                      "fast, but a wrong delete/order is <strong>irreversible</strong>"))),
        (L("关键步加闸", "Gate the risky step"), i18n.render(L("仅高风险动作要人确认，其余自动",
                                                            "only high-risk actions need a human; the rest stays automatic"))),
        caption=L("不是所有步都要人——只在<strong>不可逆/高风险</strong>处加闸",
                  "not every step needs a human — gate only the <strong>irreversible/high-risk</strong> ones"),
    )
```

- [ ] **Step 4: Quiz** — key `"33-human-in-the-loop.html"`: MCQ "HITL 在 workflow 里靠什么实现？" [A InputRequiredEvent + HumanResponseEvent✓, B 关闭 LLM, C rerank, D 流式]；Open: "哪些动作该加人工确认、哪些不该？答题点：不可逆/高风险加闸，只读/可撤销放行。"

- [ ] **Step 5: Interview drills** — key `"33-human-in-the-loop.html"`: ①"HITL 会拖慢系统，怎么把打扰降到最低？"(🔑 只在不可逆/低置信处触发 + 批量确认)；②"HITL 与可观测、护栏怎么配合？"(🔑 HITL 是最后人工闸，前面还有 L25 护栏 + L23 trace 兜底)。

- [ ] **Step 6: Gate + commit** — `git commit -m "feat(content): L33 human-in-the-loop"`.

### Task 9 — L34 Serving your RAG (`34-serving.html`)

**Files:** Modify `src/part8.py` (`LESSON_34`), `src/quizzes.py`, `src/interviews.py`.

- [ ] **Step 1: Replace `LESSON_34`** — `c.pipeline("answer")`. Sections: ① 从 notebook 到服务 — 索引一次加载常驻，别每请求重建；② FastAPI 包查询引擎 + 异步/流式（承 L24）；③ 持久化（承 L11 persist/load）；④ 更进一步 — `llama-deploy` 编排、`create-llama` 脚手架。**全程标注：示例 / 集成，非 core API。** `c.analogy`：把"实验台上的原型"装进"7×24 营业的店面"。

- [ ] **Step 2: code① + source_ref** — verbatim (illustrative; the `# pip install` + 注释点明非 core):

```python
# pip install fastapi uvicorn  —— 以下为示例，FastAPI/llama-deploy 在 core 之外
from fastapi import FastAPI
from llama_index.core import StorageContext, load_index_from_storage

app = FastAPI()
index = load_index_from_storage(StorageContext.from_defaults(persist_dir="./store"))  # 启动时一次加载
qe = index.as_query_engine()

@app.post("/query")
async def query(q: str):
    return {"answer": str(await qe.aquery(q))}   # 异步，承 L24
```
`c.source_ref("base/response/schema.py / indices/base.py", "as_query_engine / aquery", L("查询引擎可异步、可流式，适合包成服务。", "query engines are async/streaming-capable, fit to wrap as a service."))` + 注：`load_index_from_storage` 是 core，FastAPI/llama-deploy/create-llama 是外部工具。

- [ ] **Step 3: Add ≥2 figures** — verbatim:

```python
    + d.layers([
        (L("HTTP 请求", "HTTP request"), L("FastAPI 路由", "FastAPI route")),
        (L("常驻查询引擎", "long-lived query engine"), L("启动时一次加载索引", "index loaded once at boot")),
        (L("检索 + 合成", "retrieve + synthesize"), L("异步/流式", "async/streaming")),
        (L("LLM", "LLM"), L("生成答案", "generates answer")),
    ], caption=L("上线关键：索引常驻、查询引擎复用，别每请求重建",
                 "serving rule: keep the index resident and reuse the engine — don't rebuild per request"))
    + d.flow([
        ("nb", L("notebook 原型", "notebook prototype")),
        ("api", L("FastAPI 服务", "FastAPI service"), L("并发/流式", "concurrent/streaming")),
        ("deploy", L("llama-deploy / create-llama", "llama-deploy / create-llama"), L("编排/脚手架", "orchestration/scaffold")),
    ], caption=L("从原型到生产服务的进阶路径", "the path from prototype to a production service"))
```

- [ ] **Step 4: Quiz** — key `"34-serving.html"`: MCQ "把 RAG 上线成服务，最该避免？" [A 每个请求都重建索引✓, B 复用常驻查询引擎, C 异步处理, D 持久化索引]；Open: "为什么服务里要用 aquery/streaming 而不是同步 query？答题点：并发吞吐 + 首 token 延迟（承 L24）。"

- [ ] **Step 5: Interview drills** — key `"34-serving.html"`: ①"RAG 服务的并发与冷启动怎么优化？"(🔑 索引常驻 + 连接池 + 预热 + 异步)；②"上线后怎么持续保证质量？"(🔑 接 L22 回归闸 + L23 trace + L25 护栏——把全书串起来)。

- [ ] **Step 6: Gate + commit** — `git commit -m "feat(content): L34 serving your RAG"`.

### Task 10 — L35 Fine-tuning embeddings (`35-finetuning-embeddings.html`)

**Files:** Modify `src/part8.py` (`LESSON_35`), `src/quizzes.py`, `src/interviews.py`.

- [ ] **Step 1: Replace `LESSON_35`** — `c.pipeline("embed")`. Sections: ① 痛点 — 通用 embedding 在专业领域"语义错位"，召回不准；② 思路 — 用自家文档造 QA 对当训练信号，把正样本拉近、负样本推远；③ 流程 — 造对 → 微调 → 换模型重建索引 → 评估提升（承 L19/L22）；④ 性价比 — 先穷尽 chunking/rerank/hybrid，仍不够再微调。**标注：集成，非 core。** `c.analogy`：通用 embedding 像"通用词典"，微调像"给你的行业编一本术语对照"。

- [ ] **Step 2: code① + source_ref** — verbatim (illustrative):

```python
# pip install llama-index-finetuning  —— 示例，微调在 core 之外
from llama_index.finetuning import generate_qa_embedding_pairs, SentenceTransformersFinetuneEngine

train = generate_qa_embedding_pairs(nodes, llm=llm)            # 用文档自动造 (问题, 相关块) 对
engine = SentenceTransformersFinetuneEngine(train, model_id="BAAI/bge-small-en",
                                            model_output_path="ft_model")
engine.finetune()
ft_model = engine.get_finetuned_model()                        # 用它重建索引，再按 L19/L22 评估
```
`c.source_ref("(integration) llama-index-finetuning", "SentenceTransformersFinetuneEngine", L("用自家 QA 对微调 embedding，提升领域召回。", "fine-tunes embeddings on your QA pairs to lift domain recall."))`.

- [ ] **Step 3: Add ≥2 figures** — verbatim:

```python
    + d.compare2(
        (L("通用 embedding", "Generic embedding"),
         i18n.render(L("领域术语<strong>语义错位</strong>，相关块排不上来", "domain terms <strong>misalign</strong>; relevant chunks rank low"))),
        (L("领域微调后", "After fine-tuning"),
         i18n.render(L("正样本拉近、负样本推远 → 召回更准", "positives pulled closer, negatives pushed apart → better recall"))),
        caption=L("微调把你的领域语义“校准”进向量空间", "fine-tuning calibrates your domain semantics into the vector space"),
    )
    + d.flow([
        ("docs", L("自家文档", "your docs")),
        ("pairs", L("造 QA 对", "build QA pairs"), L("自动+人工挑", "auto + curate")),
        ("ft", L("微调 embedding", "fine-tune")),
        ("rebuild", L("换模型重建索引", "rebuild index")),
        ("eval", L("评估提升", "evaluate gain"), L("承 L19/L22", "per L19/L22")),
    ], caption=L("微调闭环：造对 → 微调 → 重建 → 评估，用数字证明提升",
                 "fine-tune loop: pairs → train → rebuild → evaluate; prove the gain with numbers"))
```

- [ ] **Step 4: Quiz** — key `"35-finetuning-embeddings.html"`: MCQ "embedding 微调最直接改善的是？" [A 领域内检索召回质量✓, B LLM 生成速度, C prompt 长度, D 多模态]；Open: "在微调 embedding 之前，应先尝试哪些更便宜的手段？答题点：chunking/metadata/hybrid/rerank（承 Part 2-3、L21）。"

- [ ] **Step 5: Interview drills** — key `"35-finetuning-embeddings.html"`: ①"什么时候微调 embedding 才划算？"(🔑 领域术语重、检索是瓶颈、且已穷尽便宜手段)；②"怎么证明微调真的有用、没过拟合？"(🔑 留出测试集 + 用 L19/L22 检索指标对比，别只看训练损失)。

- [ ] **Step 6: Gate + commit** — `git commit -m "feat(content): L35 fine-tuning embeddings"`.

---

## Stage 3 — Finalize

### Task 11 — Glossary: add Part 7–8 advanced terms

**Files:** Modify `src/glossary.py` (`LESSON_21`, rendered as `36-glossary.html`).

- [ ] **Step 1:** Append a new grouped section before the closing `)` of `LESSON_21`, after the existing "生产进阶 / Production" group, reusing the `_H` headers and `_row(term, zh, en, num, fname, term_en=None)` helper:

```python
    + c.section(
        L("进阶专题", "Advanced topics"),
        c.compare_table(_H, [
            _row("图谱 RAG Graph RAG", "用 实体-关系-实体 多跳找连起来的事实", "multi-hop over entity-relation triples", "27", "27-graph-rag.html", term_en="Graph RAG"),
            _row("text-to-SQL", "让 LLM 写 SQL，精确计算交数据库", "LLM writes SQL; the DB does exact compute", "28", "28-structured-data.html"),
            _row("多模态 RAG Multimodal", "图文进同一向量空间，跨模态检索", "text & images in one vector space", "29", "29-multimodal-rag.html", term_en="Multimodal RAG"),
            _row("查询分解 Sub-Question", "把复杂问题拆成子问题分别检索再汇总", "split a complex query, retrieve each, aggregate", "30", "30-sub-question.html", term_en="Sub-Question"),
            _row("结构化输出 Structured Output", "让 LLM 直接产出 Pydantic 对象", "LLM emits a typed Pydantic object", "31", "31-structured-outputs.html", term_en="Structured Output"),
            _row("多智能体 Multi-agent", "多个 agent 分工 + 交接(handoff)", "multiple agents split work with handoffs", "32", "32-multi-agent.html", term_en="Multi-agent"),
            _row("人在回路 HITL", "高风险动作前暂停等人确认", "pause for human confirmation on risky actions", "33", "33-human-in-the-loop.html", term_en="Human-in-the-loop"),
            _row("服务化 Serving", "索引常驻、查询引擎包成服务", "keep the index resident; wrap the engine as a service", "34", "34-serving.html", term_en="Serving"),
            _row("微调 embedding Fine-tuning", "用自家 QA 对校准领域语义", "calibrate domain semantics with your QA pairs", "35", "35-finetuning-embeddings.html", term_en="Fine-tuning embeddings"),
        ]),
    )
```
(No bare `&`; if `check_html` flags any, escape to `&amp;`.)

- [ ] **Step 2: Gate + commit**

Run: `cd src && python build.py && python build_print.py && python check_html.py && python check_links.py && python -m pytest tests -q`
Expected: 0 errors/0 warnings; the 9 new glossary links resolve.

```bash
git add src/glossary.py index.html lessons/ print.html
git commit -m "feat(content): glossary advanced-topics terms"
```

### Task 12 — Full verification + audit + merge

- [ ] **Step 1:** Confirm every new lesson (27–35) has ≥2 figures: `for f in lessons/2[7-9]*.html lessons/3[0-5]*.html; do echo -n "$f "; grep -o 'class=\"fig\"' "$f" | wc -l; done` — all ≥2.
- [ ] **Step 2: Remove dead scaffolding** — after Tasks 2–10 replaced every `LESSON_*`, the `_skeleton` helper in `src/part7.py` and `src/part8.py` is unused. Verify `grep -n '_skeleton' src/part7.py src/part8.py` shows only the `def` (no calls), then delete the `_skeleton` function from both modules. Keep `import i18n` (still used via `i18n.render(...)` in the real figures) — confirm with `grep -n 'i18n\.' src/part7.py src/part8.py`. Rebuild + confirm green.
- [ ] **Step 3:** Grep for any hardcoded lesson-count/glossary-number needing update: `grep -rn '27-glossary\|共 27\|== 27\|seven parts\|== 7' src/` — fix stragglers (the structure test was updated in Task 1).
- [ ] **Step 4:** Full build + verify idempotent/deterministic: build twice, `git status -s` clean; `check_html` 36 lessons 0/0; `check_links` all resolve; `pytest` green.
- [ ] **Step 5: Full audit subagent** (model claude-opus-4.8, read-only) over `git diff main -- src/part7.py src/part8.py src/quizzes.py src/interviews.py src/glossary.py src/registry.py src/shell.py`: verify each lesson's code/source_ref against vendored core 0.14.22 (core APIs) and that integration snippets (L34/L35, concrete multimodal models) are correctly labelled illustrative; check rendering, bilingual balance, ≥2 figs, quiz/interview quality. Fix any Blocker/Should-fix.
- [ ] **Step 6: Two-stage review** (spec-compliance then code-quality subagents) over the whole branch diff; fix findings.
- [ ] **Step 7: Finish the branch** — invoke superpowers:finishing-a-development-branch (verify gates → ff-merge `advanced-topics`→`main` → push origin/main → delete branch → confirm CI + Deploy green → verify L27–35 + 36-glossary live).

---

## Self-Review (run after writing; fix inline)
- **Spec coverage:** every spec §5 lesson (L27–35) → Task 2–10; glossary → Task 11; renumber/test/parts → Task 1; accuracy strategy → Task 12 audit. ✓
- **Numbering consistency:** filenames used in registry (Task 1), figures, glossary links (Task 11), and finalize greps (Task 12) all match `NN-slug.html` exactly. Glossary variable stays `glossary.LESSON_21`, key `36-glossary.html`.
- **Escaping:** code blocks avoid `<>&`; diagram labels use literal arrows/dots; no bare `&`.
