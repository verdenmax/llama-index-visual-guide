# Part 6「生产进阶」(Production track) 设计

**Goal:** 在现有 20 课入门 + 术语表之上，新增 6 节<strong>生产阶段</strong>完整课（第 21–26 课），讲清"把一个能跑的 RAG 做成可上线、可维护、可信赖的系统"还需要什么；术语表顺延为第 27 课。每课沿用现有完整格式。

**Branch:** `advanced-track`. **Anchor:** llama-index-core 0.14.22（集成/第三方 API 从各自包文档引用）。

---

## 1. 范围

- 6 节新课（完整格式）：21 生产级检索 · 22 规模化评估+CI 闸 · 23 可观测与追踪 · 24 成本与延迟 · 25 安全与防护 · 26 Agent 与 Workflows。
- 术语表 `21-glossary.html` → `27-glossary.html`，补 6 个进阶术语。
- 新部分：**Part 6 · 生产进阶**（含 21–26）；术语表移入 **Part 7 · 速查**。

## 2. 结构与重编号机制

`check_html.py` 已根据 `PAGES` 自动校验目录计数（`共 N 课 · N 个部分` 对照 `len(PAGES)` 与不同 part 数），故重编号只需改数据源：

| 文件 | 改动 |
|---|---|
| `src/part6.py` | **新建**。`LESSON_21..LESSON_26`，每课一大串（同 part1-5 风格）。`import components as c`, `import diagrams as d`, `import i18n`, `from i18n import L`。 |
| `src/registry.py` | `import part6`；`CONTENT` 插入 `"21-..".."26-.."→part6.LESSON_2x`；术语表键 `"21-glossary.html"`→`"27-glossary.html"`。 |
| `src/shell.py` | `PAGES` 插入 6 条（新 part `P6 = L("第六部分 · 生产进阶","Part 6 · Production")`）；术语表行改 `"27-glossary.html"` + 新 part `P7 = L("第七部分 · 速查","Part 7 · Reference")`。`SUBTITLES` 加 6 条 + 术语表键改 27。 |
| `src/quizzes.py` | 为 21–26 各加 `QUIZZES` 条目（≥1 MCQ + 1 open）。 |
| `src/interviews.py` | `INTERVIEW` 加 21–26（每课 2–3 道深题，🔑 重点，部分配图）。 |
| `src/glossary.py` | 术语表补 6 个进阶术语；其余不变（链接仍指向 01–19，不受影响）。 |
| `lessons/21-glossary.html` | `git rm`（build 生成 `27-glossary.html`）。 |

- 文件名编号顺序：`21-production-retrieval`, `22-eval-scale`, `23-observability`, `24-cost-latency`, `25-security`, `26-agents-workflows`, `27-glossary`。
- index 计数 pill 由 `index_page` 从 `PAGES` 自动生成（→「共 27 课 · 7 个部分」）。

## 3. 每课 DoD（同现有完整课）

`c.pipeline(...)`（生产课可用 `None` 或最贴近的阶段）+ `c.lead` + `c.analogy` + **≥2 张 `d.*` 图** + `c.compare_table` + ≥1 `c.source_ref` + 深入 `c.section` + `c.accordion`(4×`c.qa_item`) + **2 段 `c.code`** + `c.key_points` + `c.design_highlight`；并在 `quizzes.py` 加 MCQ+open、`interviews.py` 加 2–3 道面试 drill。满足 check_html（≥2 图、双语平衡、转义、details/summary 配对）。

## 4. 六课内容大纲

**L21 生产级检索（production-retrieval）** — pipeline("retrieve")
- 混合检索：向量 + BM25/关键词，用 `QueryFusionRetriever` 融合（或 `BM25Retriever` + 向量）；为什么纯向量漏精确 token。
- Rerank：`node_postprocessor` 接 Cohere / SentenceTransformer / LLM rerank；"多取再精排"。
- 查询改写 / HyDE：`HyDEQueryTransform`、多查询融合。
- 怎么评估收益（命中率/MRR/端到端）。
- code①混合+rerank 装配；code②HyDE。source_ref：core fusion / 集成包 cohere-rerank、sbert。

**L22 规模化评估与 CI 回归闸（eval-scale）** — pipeline(None)
- 金标数据集：`RagDatasetGenerator` / `generate_question_context_pairs` 自动造 QA 对。
- 批量评估：`BatchEvalRunner`（Faithfulness/Relevancy/Correctness）聚合。
- CI 闸：把分数门槛写进 pytest/CI，低于阈值 fail；RAGAS 式指标（context precision/recall）对照。
- code①造数据集+BatchEvalRunner；code②断言闸（assert mean ≥ 阈值）。延伸 L19。

**L23 可观测与追踪（observability）** — pipeline(None)
- 为什么 RAG 难调（多步、中间结果隐藏）。
- instrumentation：`llama_index.core.instrumentation` 事件/span、CallbackManager。
- 工具：`set_global_handler("arize_phoenix")` / Langfuse / OpenTelemetry。
- 看什么：检索到的 node、各步耗时、token、成本。
- code①`set_global_handler` + 带 trace 的 query；code②自定义事件 handler 取 retrieved nodes。

**L24 成本与延迟工程（cost-latency）** — pipeline(None)
- 三层缓存：embedding（`IngestionCache`）、LLM 响应缓存、检索/响应缓存。
- 异步 `aquery`、批处理；流式 `as_query_engine(streaming=True)` / `stream_chat`。
- token 预算、选小模型/小 embedding、`similarity_top_k` 与成本。
- 怎么度量（p50/p95、每问成本）。code①streaming + async；code②IngestionCache 复用。

**L25 安全与防护（security）** — pipeline(None)
- 多租户隔离：用 `MetadataFilters` 强制 `tenant_id` 过滤（最常见越权源），把过滤注入 retriever。
- PII：摄取期脱敏（`NERPIINodePostprocessor` / 自定义后处理）。
- Prompt 注入：检索内容当"数据"非"指令"、系统提示防护、输出校验。
- Grounding 强制：只引用 + Faithfulness 闸 + 不足则拒答。
- code①带 tenant 过滤的 query engine；code②PII 后处理 + 拒答模板。

**L26 Agent 与 Workflows（agents-workflows）** — pipeline(None)
- 从"固定管道"到"会决策的循环"：何时检索、用哪个工具、多步、自我纠错。
- LlamaIndex `Workflow`（事件驱动、`@step`）+ `FunctionAgent`/`ReActAgent` + `QueryEngineTool`。
- agentic RAG：router、多源、反思重检索；代价（更慢/更贵/更难调，呼应 L23）。
- code①QueryEngine 包成 `QueryEngineTool` 交给 agent；code②最小 `Workflow`（retrieve→synthesize 两步）。

**L27 术语表（顺延）** — 补 6 术语：Hybrid Retrieval、Rerank、Tracing/Observability、Caching、Multi-tenant Isolation、Agent/Workflow，归入"进阶·配置·评估"组或新增"生产"小组。

## 5. 准确性与源码引用策略

- **core 内 API**（`Workflow`/`@step`、`FunctionAgent`/`ReActAgent`、`QueryEngineTool`、`BatchEvalRunner`、`RagDatasetGenerator`、`MetadataFilters`、`IngestionCache`、`HyDEQueryTransform`、streaming、`instrumentation`、`set_global_handler`）：对照 vendored 0.14.22 校验存在与签名。
- **集成/第三方**（cohere-rerank、sentence-transformers rerank、arize-phoenix、langfuse、OpenTelemetry、PII NER）：`source_ref` 指向集成包名（如 `llama-index-postprocessor-cohere-rerank`）；代码注明「需 `pip install` 集成包 / 需 API key」为示意，不保证端到端可跑——此为已接受的漂移成本。
- 凡引用 core 符号，构建前用 `python -c "from llama_index.core... import X"`（在 vendored 环境）或对照源码确认。

## 6. 校验与成功标准

- `build` + `build_print` + `check_html`（**0 错 0 警**；计数自动变 27/7）+ `check_links`（含术语表新编号、capstone 链接不受影响）+ `pytest` + 构建确定性。
- 更新任何硬编码"21 课/glossary 编号"的测试（若有）。
- 每非术语表课 ≥2 图；6 课各 2–3 道面试 drill。
- 最终审查子代理（core API 准确性 + 渲染 + 双语）→ 合并 `advanced-track`→`main`→部署。

## 7. 实现步骤（细节见 plan）

1. 重编号脚手架：part6.py 占位 + registry/shell/PAGES/SUBTITLES + glossary 文件名迁移 + 删旧 html；build 通过、check_html 27/7。
2. 逐课撰写 L21–L26（含 quizzes + interviews）。
3. 术语表补 6 词。
4. 中心化校验 + 审查子代理。
5. 合并 + 推送 + 部署 + 线上核验。
