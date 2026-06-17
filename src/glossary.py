"""Part 9 (reference): lesson 36 glossary. Content filled task-by-task."""
import components as c
import diagrams as d
from i18n import L


def _term(zh, en):
    return L(zh, en)


_H = [L("术语", "Term"), L("一句话", "In a line"), L("课", "Lesson")]


def _row(term, zh, en, num, fname, term_en=None):
    link = f'<a href="{fname}">{num}</a>'
    return [L(term, term_en or term), _term(zh, en), L(link, link)]


LESSON_36 = (
    c.lead(L(
        "全书术语<strong>按数据流分组</strong>速查——基础 → 写入路径 → 查询路径 → 进阶 → 生产 → 进阶专题。点“课”跳到对应讲解。",
        "Every term, <strong>grouped by data flow</strong> — foundations → write path → query path → advanced → production → advanced topics. "
        "Click the lesson to jump.",
    ))
    + d.flow([
        ("load", L("加载", "Load")),
        ("split", L("切块", "Split")),
        ("embed", L("向量化", "Embed")),
        ("index", L("索引", "Index")),
        ("retrieve", L("检索", "Retrieve")),
        ("synth", L("合成", "Synthesize")),
        ("answer", L("回答", "Answer")),
    ], caption=L("按数据流复习全书术语", "Review the whole guide's terms along the data flow"))
    + c.section(
        L("基础概念", "Foundations"),
        c.compare_table(_H, [
            _row("<code>RAG</code>", "检索增强生成：先检索相关片段再让 LLM 生成", "retrieve relevant chunks, then let the LLM generate", "01", "01-what-is-llamaindex.html"),
            _row("<code>Document</code>", "一整份原始资料", "one whole raw source", "04", "04-documents-nodes.html"),
            _row("<code>Node</code>", "切块后带元数据/关系的检索单位", "a chunked, metadata- and relationship-bearing unit of retrieval", "04", "04-documents-nodes.html"),
        ]),
    )
    + c.section(
        L("写入路径：把数据建成索引", "Write path: build data into an index"),
        c.compare_table(_H, [
            _row("Reader", "把来源加载成 Document", "loads a source into Documents", "05", "05-readers.html"),
            _row("Node Parser", "把 Document 切成 Node（chunking）", "splits Documents into Nodes (chunking)", "06", "06-node-parsers.html"),
            _row("<code>chunk_size/overlap</code>", "切块大小与相邻重叠", "chunk length and adjacent overlap", "06", "06-node-parsers.html"),
            _row("Extractor", "用 LLM 为 Node 生成元数据", "LLM-generates metadata for Nodes", "07", "07-metadata-extractors.html"),
            _row("Embedding", "文本→向量，使语义相近=距离近", "text→vector so similar=close", "08", "08-embeddings.html"),
            _row("Vector Store", "存向量+元数据并做近邻查询", "stores vectors+metadata, does nearest-neighbor search", "09", "09-vector-stores.html"),
            _row("Index", "为某种检索方式组织 Node 的结构", "structure organizing Nodes for a retrieval style", "10", "10-index-abstraction.html"),
            _row("Ingestion Pipeline", "可缓存/去重的摄取管道", "cacheable, dedup-aware ingestion", "11", "11-ingestion-storage.html"),
            _row("<code>persist/load</code>", "索引落盘与恢复", "persist an index and reload it", "11", "11-ingestion-storage.html"),
        ]),
    )
    + c.section(
        L("查询路径：把问题查成答案", "Query path: turn a question into an answer"),
        c.compare_table(_H, [
            _row("Retriever", "取回 top-k 相关 Node", "fetches the top-k relevant Nodes", "12", "12-retrievers.html"),
            _row("Postprocessor", "生成前过滤/重排/替换 Node", "filter/rerank/replace Nodes before generation", "13", "13-postprocessors.html"),
            _row("Response Synthesizer", "多片段→单答案的策略", "the many-chunks→one-answer strategy", "14", "14-response-synthesizers.html"),
            _row("Query Engine", "检索+后处理+合成的组合根", "composition root: retrieve+postproc+synth", "15", "15-query-engine.html"),
            _row("Chat Engine", "带记忆的多轮 RAG", "multi-turn RAG with memory", "16", "16-chat-engine.html"),
        ]),
    )
    + c.section(
        L("进阶 · 配置 · 评估", "Advanced · config · evaluation"),
        c.compare_table(_H, [
            _row("<code>Settings</code>", "全局默认配置（取代 ServiceContext）", "global defaults (replaces ServiceContext)", "17", "17-settings-prompts.html"),
            _row("进阶检索 Advanced Retrieval", "融合 / 自动合并 / 递归 / 路由等进阶检索器", "fusion / auto-merging / recursive / router retrievers", "18", "18-advanced-retrieval.html", term_en="Advanced Retrieval"),
            _row("Evaluation", "忠实/相关/正确三类打分", "faithful/relevant/correct scoring", "19", "19-evaluation.html"),
        ]),
    )
    + c.section(
        L("生产进阶", "Production"),
        c.compare_table(_H, [
            _row("混合检索 Hybrid Retrieval", "向量 + 关键词(BM25)融合检索", "fuse vector + keyword (BM25) retrieval", "21", "21-production-retrieval.html", term_en="Hybrid Retrieval"),
            _row("精排 Rerank", "用更强模型对召回结果精排", "re-score recall with a stronger model", "21", "21-production-retrieval.html", term_en="Rerank"),
            _row("回归闸 Regression Gate", "评估分数低于阈值则拦截上线", "block release when eval scores drop below a threshold", "22", "22-eval-scale.html", term_en="Regression Gate"),
            _row("可观测 Observability", "追踪每步耗时 / token / 检索结果", "trace per-step latency / tokens / retrieved nodes", "23", "23-observability.html", term_en="Observability"),
            _row("缓存 Caching", "复用 embedding / 响应以省成本降延迟", "reuse embeddings / responses to cut cost &amp; latency", "24", "24-cost-latency.html", term_en="Caching"),
            _row("多租户隔离 Multi-tenant Isolation", "强制按 tenant 过滤防越权", "enforce per-tenant filtering to prevent leakage", "25", "25-security.html", term_en="Multi-tenant Isolation"),
            _row("Agent / Workflow", "会决策的循环，按需用工具 / 多步", "a deciding loop that uses tools / multi-step on demand", "26", "26-agents-workflows.html"),
        ]),
    )
    + c.section(
        L("进阶专题", "Advanced topics"),
        c.compare_table(_H, [
            _row("图谱 RAG Graph RAG", "用 实体-关系-实体 多跳找连起来的事实", "multi-hop over entity-relation triples", "27", "27-graph-rag.html", term_en="Graph RAG"),
            _row("text-to-SQL", "让 LLM 写 SQL，精确计算交数据库", "LLM writes SQL; the DB does exact compute", "28", "28-structured-data.html"),
            _row("多模态 RAG Multimodal", "图文进同一向量空间，跨模态检索", "text &amp; images in one vector space for cross-modal retrieval", "29", "29-multimodal-rag.html", term_en="Multimodal RAG"),
            _row("查询分解 Sub-Question", "把复杂问题拆成子问题分别检索再汇总", "split a complex query, retrieve each, aggregate", "30", "30-sub-question.html", term_en="Sub-Question"),
            _row("结构化输出 Structured Output", "让 LLM 直接产出 Pydantic 对象", "LLM emits a typed Pydantic object", "31", "31-structured-outputs.html", term_en="Structured Output"),
            _row("多智能体 Multi-agent", "多个 agent 分工 + 交接(handoff)", "multiple agents split work with handoffs", "32", "32-multi-agent.html", term_en="Multi-agent"),
            _row("人在回路 HITL", "高风险动作前暂停等人确认", "pause for human confirmation on risky actions", "33", "33-human-in-the-loop.html", term_en="Human-in-the-loop"),
            _row("服务化 Serving", "索引常驻、查询引擎包成服务", "keep the index resident; wrap the engine as a service", "34", "34-serving.html", term_en="Serving"),
            _row("微调 embedding Fine-tuning", "用自家 QA 对校准领域语义", "calibrate domain semantics with your QA pairs", "35", "35-finetuning-embeddings.html", term_en="Fine-tuning embeddings"),
        ]),
    )
)
