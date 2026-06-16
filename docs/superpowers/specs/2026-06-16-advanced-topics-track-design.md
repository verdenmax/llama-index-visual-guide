# Part 7–8「进阶专题」(Advanced topics track) 设计

> 锚定 **llama-index-core 0.14.22**（vendored 于 `/home/verden/course/llama_index`）。承接 Part 6 生产进阶之后，补齐"超越文本 RAG"与"Agentic 进阶 / 上线"两大盲区。

## 1. 背景与目标（Why）

现有 26 课覆盖核心 RAG 管道 + 生产加固，但 grep 证实有若干真空白：图谱 RAG、结构化数据查询(SQL/Pandas)、多模态、查询分解(SubQuestion)、结构化输出(Pydantic)、多智能体/工作流控制流、人在回路(HITL)、上线服务、embedding 微调。本轨道把这些补成正式课程，保持现有质量标准（双语、≥2 图、测验 + 面试题、技术对照 core 0.14.22）。

## 2. 范围决策（已与用户确认）

- **9 节新课**，"平衡版"颗粒度（天然同类合并，其余独立），每节沿用现有完整课 DoD。
- 编为**两个新部分**，**追加在 Part 6 生产之后**（L21–26 是文本 RAG 的加固，本批是其他模态/进阶能力，接其后最自然，且避免重排 L21–26）：
  - **Part 7 · 超越文本 RAG**：L27 图谱、L28 结构化数据、L29 多模态、L30 查询分解、L31 结构化输出。
  - **Part 8 · Agentic 进阶与上线**：L32 多智能体与控制流、L33 人在回路、L34 上线服务、L35 微调 embedding。
- 词汇表由 `27-glossary.html` 顺延为 **`36-glossary.html`**（最后一页）。
- 实现**分两阶段**：先 Part 7（L27–31）再 Part 8（L32–35）。

## 3. 结构与重编号机制

- 新增 `src/part7.py`（`LESSON_27..31`）、`src/part8.py`（`LESSON_32..35`），沿用 `import components as c` / `import diagrams as d` / `from i18n import L` 体系。
- `src/registry.py`：`import part7, part8`；插入 L27–35 → `part7/part8.LESSON_2x/3x`；glossary 键改 `36-glossary.html`。
- `src/shell.py`：`PAGES` += 9（新增 `P7`=超越文本 RAG、`P8`=Agentic 进阶与上线）；glossary 行移到 `36-glossary.html`，其部分标签 `P9REF`=Reference。`SUBTITLES` 同步。
- `check_html.py` 已从 `PAGES` 数据驱动校验"共 N 课 · N 个部分"，重编号无痛（与 21→27 同理）。
- `glossary.py`：在"生产进阶"后追加新分组术语（图谱/SQL/多模态/SubQuestion/Pydantic/多智能体/HITL/serving/finetune）。

## 4. 每课 DoD（同现有完整课）

每节须含：`c.pipeline(stage)` 头 + `c.lead` 导语；正文分 `c.section`；**≥2 张** `d.*` 图（各扣一个"aha"）；≥1 段 `c.code`（真实可跑/示例标注）+ ≥1 `c.source_ref`；`c.analogy` + `c.key_points`；`quizzes.py` 加 ≥1 MCQ + ≥1 开放题；`interviews.py` 加 2–3 道面试题（每题 `🔑` 重点，部分配图）；双语均衡；`check_html` 0/0。

## 5. 九课内容大纲（aha + 锚定 API + 关键示例/图）

### Part 7 · 超越文本 RAG

**L27 图谱 RAG（Graph RAG）** — `c.pipeline("index")`
- **aha**：向量召回"相似片段"，图谱召回"**连起来的事实**"；多跳关系（A→B→C）是纯向量答不出的。
- **锚定**：`PropertyGraphIndex`（`indices/property_graph/base.py`）；抽取器 `SimpleLLMPathExtractor`/`SchemaLLMPathExtractor`/`ImplicitPathExtractor`；检索器 `LLMSynonymRetriever`/`VectorContextRetriever`。`KnowledgeGraphIndex` 作 legacy 一句带过。
- **代码**：`PropertyGraphIndex.from_documents(docs, kg_extractors=[SchemaLLMPathExtractor(...)])` → `index.as_retriever(sub_retrievers=[...])` / `as_query_engine()`。
- **图**：① `d.annot`：中心实体 + 关系 callouts（实体-关系-实体三元组）；② `d.compare2`：向量"相似块" vs 图谱"多跳路径"。

**L28 结构化数据查询（SQL & Pandas）** — `c.pipeline("retrieve")`
- **aha**：数字/聚合/精确筛选别硬塞向量——**让 LLM 写 SQL**，把精确计算交给数据库；表格则交 Pandas。
- **锚定**：`SQLDatabase`（`utilities/sql_wrapper.py`）、`NLSQLTableQueryEngine`、`SQLTableRetrieverQueryEngine`（`indices/struct_store/sql_query.py`，大表用 ObjectIndex 选表）；`PandasQueryEngine`（`query_engine/pandas/pandas_query_engine.py`）。
- **代码**：① `NLSQLTableQueryEngine(sql_database=SQLDatabase(engine), tables=[...])`；② `PandasQueryEngine(df=...)`。注明 Pandas 引擎执行 LLM 生成代码的**安全告诫**。
- **图**：① `d.flow`：问题→LLM 生成 SQL→执行→自然语言答；② `d.grid`：何时用向量 / SQL / Pandas（数据形态 × 适用）。

**L29 多模态 RAG（Multimodal）** — `c.pipeline("embed")`
- **aha**：图文进**同一向量空间**——能"用文字查图、用图查图"；检索件与生成件都要换多模态版。
- **锚定**：`MultiModalVectorStoreIndex`（`indices/multi_modal/base.py`）、`MultiModalLLM`（`multi_modal_llms/base.py`，基类）、`ImageNode`/`ImageDocument`（`schema.py`）、`SimpleDirectoryReader` 读图。具体模型（如 OpenAIMultiModal、CLIP embedding）走**集成、示例标注**。
- **代码**：`MultiModalVectorStoreIndex.from_documents(docs)` （图像 + 文本 store）→ `index.as_query_engine(multi_modal_llm=...)`。
- **图**：① `d.compare2`：文本路径 vs 图像路径（各自 embedding→同一空间）；② `d.flow`：图文混合检索 → 多模态 LLM 合成。

**L30 查询分解（Sub-Question / 多文档）** — `c.pipeline("retrieve")`
- **aha**：对比/跨源/**并行多部分**问题，单次 top-k 答不全——**拆成可并行的子问题**分别检索、再汇总。（注：依赖链——前一步答案喂下一步——属 Agent/L32，不是 SubQuestion）
- **锚定**：`SubQuestionQueryEngine`（`query_engine/sub_question_query_engine.py`）、`QueryEngineTool`/`ToolMetadata`（`tools/`）。
- **代码**：`SubQuestionQueryEngine.from_defaults(query_engine_tools=[QueryEngineTool(qe_A, ToolMetadata(...)), ...])`，问"对比 A 与 B"自动拆子问题。
- **图**：① `d.vflow`：母问题→拆出子问 q1/q2→各自检索→汇总答；② `d.annot`：一个母问题节点 + 多个子问题 callouts。

**L31 结构化输出（Structured outputs）** — `c.pipeline("synthesize")`
- **aha**：别用正则 parse 自由文本——**直接让 LLM 吐 Pydantic 对象**，类型即契约，下游可直接用。
- **锚定**：`LLMTextCompletionProgram`、`FunctionCallingProgram`（`program/`）、`llm.structured_predict(...)`（`llms/llm.py`）、配 `pydantic.BaseModel`。
- **代码**：`program = LLMTextCompletionProgram.from_defaults(output_cls=MyModel, prompt_template_str=...)` → `obj = program(...)`；或 `llm.structured_predict(MyModel, prompt)`。
- **图**：① `d.compare2`：自由文本+脆弱 parse vs 直接 Pydantic 对象；② `d.flow`：prompt → LLM → 校验 → 类型化对象。

### Part 8 · Agentic 进阶与上线

**L32 多智能体与工作流控制流** — `c.pipeline("answer")`
- **aha**：单 agent 不够时**分工 + 交接(handoff)**；workflow 用**事件**把分支/循环显式编排，而非藏在 if 里。
- **锚定**：`AgentWorkflow`（`agent/workflow/multi_agent_workflow.py`）、`FunctionAgent`/`ReActAgent`；`Workflow`/`@step`/`Event`/`Context`（core re-export，承 L26）。
- **代码**：`AgentWorkflow(agents=[research_agent, write_agent], root_agent=...)`（带 handoff）；workflow 内 `@step` 返回不同 `Event` 实现分支/循环。
- **图**：① `d.flow`：研究 agent →(handoff)→ 写作 agent →(handoff)→ 复核；② `d.vflow`：workflow 事件驱动的分支/循环控制流。

**L33 人在回路（Human-in-the-loop）** — `c.pipeline("answer")`
- **aha**：高风险动作（下单/删库/外发）前**暂停等人确认**——workflow 发事件挂起、拿到人答再恢复。
- **锚定**：`InputRequiredEvent`/`HumanResponseEvent`（`workflow/__init__.py` re-export）、`Context`（`ctx.wait_for_event` 模式）。
- **代码**：`@step` 发 `InputRequiredEvent` → 外部回 `HumanResponseEvent` → 据此继续/中止。
- **图**：① `d.flow`：执行→需确认？→(发 InputRequired，挂起)→人答→继续/中止；② `d.compare2`：全自动(危险) vs 关键步加闸(可控)。

**L34 把 RAG 上线成服务（Serving）** — `c.pipeline("answer")`
- **aha**：从 notebook 到**真服务**：FastAPI 包查询引擎、并发/流式、持久化索引一次加载常驻；再到 llama-deploy / create-llama 脚手架。
- **锚定**：**core 之外，概念 + 集成、全部示例标注**——FastAPI 包 `index.as_query_engine()`、`aquery`/streaming、`llama-deploy`、`create-llama`。复用 L24 的流式/异步、L11 的 persist/load。
- **代码**：最小 FastAPI：启动时 `load_index_from_storage`，`@app.post('/query')` 调 `await qe.aquery(q)`（标注示例）。
- **图**：① `d.layers`：请求 → FastAPI → 常驻索引/查询引擎 → LLM；② `d.flow`：notebook 原型 → FastAPI 服务 → llama-deploy 编排。

**L35 微调 embedding（Fine-tuning embeddings）** — `c.pipeline("embed")`
- **aha**：通用 embedding 在你的领域常"语义错位"——**用自家 QA 对微调**，把正样本拉近、负样本推远，召回质量直接提升。
- **锚定**：**集成、示例标注**——`generate_qa_embedding_pairs`、`SentenceTransformersFinetuneEngine`（`llama-index-finetuning`）；评估接 L19/L22。
- **代码**：`generate_qa_embedding_pairs(nodes)` → `SentenceTransformersFinetuneEngine(train_dataset, model_id, ...).finetune()` → 用微调模型重建索引（标注示例）。
- **图**：① `d.compare2`：通用 embedding(领域错位) vs 微调后(正负拉开)；② `d.flow`：自家文档→造 QA 对→微调→换模型重建→评估提升。

## 6. 准确性与源码引用策略

- **L27–L33 锚定真实 core 0.14.22 API**（上方路径已逐一在 vendored 源码核实）；计划阶段再列一份"已核 API 清单"逐课对照，像 Part 6 一样在最终审计中复核。
- **L34（serving）、L35（finetune）、以及多模态具体模型**：core 之外，按现有第三方写法（如 BM25/Cohere/Phoenix）**明确标注为示例 / 集成**（`# pip install ...` 注释 + 文案点明"非 core"）。
- 凡 `c.code` 中的 `<`/`>`/`&` 一律转义；`d.*` 标签可用 `→·✓“”` 字面量。

## 7. 校验与成功标准

- 更新 `src/tests/test_registry_structure.py`：`len==36`、`keys[-1]=="36-glossary.html"`、`PAGES` 9 个部分、L27/L35 边界键存在。
- `python build.py && python build_print.py && python check_html.py && python check_links.py && python -m pytest tests -q` 全绿（`check_html` 0/0、链接全解析、测试全过）；二次构建字节一致（确定性）。
- 每节 ≥2 图、配齐 quiz/interview；glossary 新术语链接解析。
- 合并前跑一次**全量审计子代理**（对照 vendored 0.14.22）+ spec/质量双审。

## 8. 不做 / YAGNI

- 不拆 SQL 与 Pandas 为两课（同属结构化数据）；不为 KnowledgeGraphIndex 单列课（legacy，一句带过）。
- 不引入新 `d.*` 图元（现有 8 种够用：图谱用 `annot`、多模态用 `compare2` 等）。
- 不真正训练/部署（serving、finetune 仅讲法 + 示例，不在 CI 跑重组件）。
- 不改动 L01–26 既有内容（仅追加 + glossary 重编号）。

## 9. 实现阶段（细节见 plan）

1. **阶段一 Part 7**：脚手架（part7.py + 注册 + glossary 重编号 + 测试转绿）→ 逐课 L27–31（内容 + quiz + interview + 图）。
2. **阶段二 Part 8**：part8.py + 注册 → 逐课 L32–35。
3. **收尾**：glossary 术语、全量审计、双审、合并 main、推送、验证 CI/Deploy。
- 每 task 走 subagent-driven（实现 → spec 审 → 质量审），子代理用主会话模型。
