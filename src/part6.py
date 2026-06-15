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


LESSON_21 = (
    c.pipeline("retrieve")
    + c.lead(L(
        "到了生产环境，朴素 top-k 的“一路向量、直接取前 k”常常不够：精确编号查不准、罕见词召不回、"
        "真正相关的排在后面。生产级检索的标准答案是<strong>混合检索</strong>（向量 + BM25 两路召回）+ "
        "<strong>Rerank 精排</strong>，必要时再加 <strong>HyDE</strong> 改写——核心是把<strong>召回</strong>和"
        "<strong>精度</strong>分两步拿。",
        "In production, naive top-k — one vector path, take the first k — often isn't enough: exact ids miss, rare "
        "words don't get recalled, and the truly relevant hits rank too low. The standard answer is "
        "<strong>hybrid retrieval</strong> (vector + BM25 dual recall) + <strong>reranking</strong>, plus "
        "<strong>HyDE</strong> rewriting when needed — the core idea is to get <strong>recall</strong> and "
        "<strong>precision</strong> in two separate steps.",
    ))
    + d.flow([
        ("ask", L("问题", "Question")),
        ("recall", L("向量检索 · BM25", "Vector · BM25"), L("两路各取 top-10（宁可多召）", "top-10 each (over-fetch)")),
        ("fuse", L("融合 (RRF)", "Fuse (RRF)"), L("倒数排名累加、去重", "reciprocal-rank, deduped")),
        ("rerank", L("Rerank 精排", "Rerank"), L("交叉编码器逐条打分", "cross-encoder re-scores")),
        ("top3", L("top-3", "top-3"), L("最相关的几条进 prompt", "the few best into the prompt")),
    ], active="rerank", caption=L(
        "先广召回，再精排：向量 + BM25 两路召回 → RRF 融合 → rerank 精排 → top-3",
        "Recall broad, then rerank narrow: vector + BM25 recall → RRF fusion → rerank → top-3",
    ))
    + c.analogy(L(
        "像招聘：先<strong>广撒网</strong>多收简历（混合召回，宁可多别漏），再让资深面试官<strong>逐份细看</strong>"
        "挑出最合适的几个（rerank 精排）——海选要全，终面要准。",
        "Like hiring: first <strong>cast a wide net</strong> for résumés (hybrid recall — over-collect, never miss), "
        "then let a senior interviewer <strong>read each closely</strong> and pick the best few (rerank) — screening "
        "wants completeness, the final round wants precision.",
    ))
    + c.section(
        L("混合检索：向量懂语义，BM25 补字面", "Hybrid retrieval: vectors for meaning, BM25 for the letter"),
        c.compare_table(
            [L("对比项", "Aspect"), L("纯向量检索", "Vector-only"), L("BM25（关键词）", "BM25 (keyword)"),
             L("混合 + Rerank", "Hybrid + Rerank")],
            [
                [L("核心机制", "Mechanism"), L("embedding 语义近邻", "semantic nearest-neighbor"),
                 L("词频 / 精确匹配", "term-frequency / exact match"),
                 L("两路召回 → 交叉编码器精排", "dual recall → cross-encoder rerank")],
                [L("擅长", "Strong at"), L("近义、改写、换种问法", "synonyms, rephrasings, paraphrase"),
                 L("精确编号、罕见词、专有名词", "exact ids, rare words, proper nouns"),
                 L("语义 + 字面都覆盖", "both meaning and letter")],
                [L("盲区", "Blind spot"), L("精确符号“X-2000”可能漏", "may miss an exact symbol like “X-2000”"),
                 L("读不懂同义改写", "blind to synonymy / paraphrase"),
                 L("多一步算力，更慢更贵", "one extra step — slower, pricier")],
            ],
        ),
    )
    + c.section(
        L("为什么生产 RAG 几乎都要混合检索 + Rerank", "Why production RAG almost always needs hybrid retrieval + rerank"),
        L(
            "纯向量检索懂<strong>语义</strong>——近义、换种问法都能命中，但它把文本压成一个语义向量，对"
            "<strong>精确 token</strong> 和<strong>罕见词</strong>（产品编号、报错码、专有名词）不敏感，这类查询常常"
            "排不进 top-k。BM25 正好相反：按<strong>字面词频</strong>匹配，精确编号一击即中，却读不懂同义改写。"
            "于是生产里把两路<strong>并联召回</strong>、用 RRF 融合，语义与字面互补。但召回求“全”难免带进噪声，"
            "所以再加一层 <strong>rerank</strong>：用<strong>交叉编码器</strong>把 query 和每个候选<strong>放在一起</strong>"
            "重新打分，把真正相关的提到最前——召回与精度<strong>分两步</strong>拿，这就是几乎所有生产 RAG 的检索骨架。",
            "Pure vector search understands <strong>meaning</strong> — synonyms and rephrasings still hit — but it "
            "squeezes text into one semantic vector and is weak on <strong>exact tokens</strong> and <strong>rare "
            "words</strong> (product ids, error codes, proper nouns), so such queries often fall out of top-k. BM25 is "
            "the mirror image: it matches <strong>literal term frequency</strong>, nailing an exact id but blind to "
            "synonymy. So production runs both paths <strong>in parallel</strong> and fuses them with RRF, letting "
            "meaning and letter complement each other. Recall chasing completeness inevitably drags in noise, so a "
            "<strong>rerank</strong> layer follows: a <strong>cross-encoder</strong> scores the query and each "
            "candidate <strong>together</strong>, lifting the truly relevant to the top — getting recall and precision "
            "in <strong>two separate steps</strong>, the retrieval backbone of nearly every production RAG.",
        ),
        d.compare2(
            (L("纯向量检索", "Vector-only"), i18n.render(L(
                "问“<code>X-2000</code> 的保修期”，embedding 把它读成“某型号保修”，却对精确编号 <code>X-2000</code> "
                "不敏感——相关条款排在第 12 名，进不了 top-5，答案只能靠猜。",
                "Ask “warranty of <code>X-2000</code>” and the embedding reads it as “warranty of some model”, blind to "
                "the exact id <code>X-2000</code> — the right clause ranks #12, never enters top-5, and the answer is a "
                "guess.",
            ))),
            (L("混合检索 + Rerank", "Hybrid + Rerank"), i18n.render(L(
                "BM25 直接按字面命中含 <code>X-2000</code> 的那一条，和向量召回一起进候选池；rerank 再把真正写明保修期"
                "的那条提到第 1——精确编号不再漏。",
                "BM25 hits the line literally containing <code>X-2000</code> and joins the vector candidates in the pool; "
                "rerank then lifts the clause that actually states the warranty to #1 — the exact id is never missed "
                "again.",
            ))),
            caption=L(
                "同一个查询：纯向量漏掉精确编号，混合用 BM25 补回字面匹配再精排",
                "Same query: vector-only misses the exact id; hybrid adds BM25's literal match, then reranks",
            ),
        ),
    )
    + c.section(
        L("再进一步：HyDE 用“假设答案”贴近文档", "Going further: HyDE uses a “hypothetical answer” to match the docs"),
        L(
            "混合检索和 rerank 解决“召回 + 精排”，<strong>HyDE</strong>（Hypothetical Document Embeddings）则换个角度"
            "提升召回：先让 LLM 根据问题写一段<strong>假设答案</strong>，再用这段<strong>更像文档</strong>的文本去做向量"
            "检索。短问句和文档措辞往往对不齐，而“假设答案”天然贴近文档语气，召回常常更准。",
            "Hybrid retrieval and rerank handle recall-plus-rerank; <strong>HyDE</strong> (Hypothetical Document "
            "Embeddings) lifts recall from another angle: let the LLM first draft a <strong>hypothetical answer</strong> "
            "to the question, then run vector search with that <strong>doc-like</strong> text. Terse questions rarely "
            "match document wording, but a hypothetical answer naturally echoes the document's tone, so recall is often "
            "better.",
        ),
        d.flow([
            ("q", L("原始问句", "Raw question"), L("“远程办公要审批吗？”", "“need approval to WFH?”")),
            ("hyde", L("LLM 写假设答案", "LLM drafts a hypothetical"), L("一段像文档的回答", "a doc-like passage")),
            ("embed", L("用假设答案检索", "Retrieve with it"), L("它的向量更贴文档措辞", "its vector matches doc wording")),
            ("hit", L("命中更准", "Better hits"), L("召回贴近政策原文", "recall closer to the policy text")),
        ], caption=L(
            "HyDE：先让 LLM 写个“假设答案”，再用它的向量去检索——往往比用问句本身更贴文档措辞",
            "HyDE: let the LLM draft a hypothetical answer, then search with its vector — often closer to the document's wording than the question",
        )),
    )
    + c.source_ref(
        "retrievers/fusion_retriever.py", "QueryFusionRetriever",
        L("把多路检索器用 RRF 融合成一路（混合检索的核心）", "fuses multiple retrievers into one via RRF (the heart of hybrid retrieval)"),
    )
    + c.source_ref(
        "llama-index-retrievers-bm25", "BM25Retriever",
        L("关键词 / 精确 token 检索，作为向量之外的另一路召回（独立集成包）",
          "keyword / exact-token retrieval as the second recall path beside vectors (a separate integration package)"),
    )
    + c.accordion(
        L("深入：混合检索、RRF 与 Rerank 的取舍", "Deep dive: hybrid retrieval, RRF and the rerank trade-offs"),
        c.qa_item(
            L("🧪 示例：装配“混合 + 精排”一条链", "🧪 Example: wiring a hybrid + rerank chain"),
            L(
                "两路召回各取 top-10：<code>index.as_retriever()</code> 走向量，"
                "<code>BM25Retriever.from_defaults(docstore=index.docstore)</code> 走关键词；用 "
                "<code>QueryFusionRetriever([vector, bm25], mode='reciprocal_rerank')</code> 融合，再把 "
                "<code>CohereRerank(top_n=3)</code> 作为 node_postprocessor 精排到 3 条。",
                "Two recall paths, top-10 each: <code>index.as_retriever()</code> for vectors and "
                "<code>BM25Retriever.from_defaults(docstore=index.docstore)</code> for keywords; fuse with "
                "<code>QueryFusionRetriever([vector, bm25], mode='reciprocal_rerank')</code>, then add "
                "<code>CohereRerank(top_n=3)</code> as a node_postprocessor to narrow to 3.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "一步到位很难同时做到“全”和“准”。生产 RAG 索性<strong>解耦</strong>：召回阶段只求<strong>别漏</strong>"
                "（向量 + BM25 多路、each top-10~20，宁可多召），精排阶段只求<strong>排得准</strong>（rerank 用更贵的"
                "交叉编码器在小候选集上细判）。两步各自优化，比单一相似度分数既快又准。",
                "One pass can't be both complete and precise, so production RAG <strong>decouples</strong> them: the "
                "recall stage only avoids <strong>misses</strong> (vector + BM25, top-10~20 each, over-fetch on "
                "purpose), and the rerank stage only gets the <strong>order right</strong> (a pricier cross-encoder "
                "judges the small candidate set). Optimizing each step separately beats a single similarity score on "
                "both speed and accuracy.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "<code>QueryFusionRetriever</code> 把每路结果按<strong>倒数排名（RRF）</strong>累加打分再合并去重，"
                "<code>num_queries=1</code> 表示不改写问句、只融合多个检索器；rerank 不在检索器里，而是作为 "
                "<code>node_postprocessor</code> 挂在 QueryEngine 上，对融合后的候选<strong>逐条</strong>用 query+doc "
                "一起打分、取 top-n。",
                "<code>QueryFusionRetriever</code> merges each path's results by <strong>reciprocal rank (RRF)</strong>, "
                "deduping as it goes; <code>num_queries=1</code> means don't rewrite the query, just fuse the "
                "retrievers. Rerank lives not in the retriever but as a <code>node_postprocessor</code> on the "
                "QueryEngine, scoring each fused candidate with query+doc together and keeping the top-n.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "精排器可换：<strong>CohereRerank</strong>（托管 API，最省事最准，但按调用计费且数据出网）、"
                "<strong>本地 SentenceTransformer 交叉编码器</strong>（<code>SentenceTransformerRerank</code>，数据不出网、"
                "免调用费，但要本地 GPU/算力）、<strong>LLMRerank</strong>（让 LLM 直接判相关性，最灵活但最慢最贵）。"
                "按数据合规、延迟预算和成本三角去选。",
                "The reranker is swappable: <strong>CohereRerank</strong> (hosted API — easiest and most accurate, but "
                "billed per call and data leaves your network), a <strong>local SentenceTransformer cross-encoder</strong> "
                "(<code>SentenceTransformerRerank</code> — data stays in, no per-call fee, but needs local GPU/compute), "
                "and <strong>LLMRerank</strong> (an LLM judges relevance directly — most flexible but slowest and "
                "priciest). Pick along the data-compliance / latency / cost triangle.",
            ),
        ),
    )
    + c.code(
        "from llama_index.core.retrievers import QueryFusionRetriever\n"
        "from llama_index.core.query_engine import RetrieverQueryEngine\n"
        "from llama_index.retrievers.bm25 import BM25Retriever            # pip install llama-index-retrievers-bm25\n"
        "from llama_index.postprocessor.cohere_rerank import CohereRerank  # pip install llama-index-postprocessor-cohere-rerank\n\n"
        "# 两路召回：向量(语义) + BM25(精确 token)，先各取 10\n"
        "vector = index.as_retriever(similarity_top_k=10)\n"
        "bm25 = BM25Retriever.from_defaults(docstore=index.docstore, similarity_top_k=10)\n\n"
        "# 用 reciprocal-rank fusion 融合两路（num_queries=1 表示不改写、只融合检索器）\n"
        "hybrid = QueryFusionRetriever([vector, bm25], num_queries=1,\n"
        "                              similarity_top_k=10, mode='reciprocal_rerank')\n\n"
        "# 再用 rerank 模型把 10 条精排到最相关的 3 条（需 COHERE_API_KEY）\n"
        "engine = RetrieverQueryEngine.from_args(\n"
        "    retriever=hybrid, node_postprocessors=[CohereRerank(top_n=3)])\n"
        "print(engine.query('X-2000 的保修期是多久？'))",
        caption=L("生产配方：向量 + BM25 两路召回 → RRF 融合 → Cohere 精排 top-3",
                  "Production recipe: vector + BM25 recall → RRF fusion → Cohere rerank to top-3"),
    )
    + c.code(
        "from llama_index.core.indices.query.query_transform import HyDEQueryTransform\n"
        "from llama_index.core.query_engine import TransformQueryEngine\n\n"
        "# HyDE：先让 LLM 写一个“假设答案”，用它的向量去检索——往往比用问句本身更贴近文档措辞\n"
        "hyde = HyDEQueryTransform(include_original=True)\n"
        "engine = TransformQueryEngine(index.as_query_engine(similarity_top_k=5), query_transform=hyde)\n"
        "print(engine.query('远程办公需要审批吗？'))",
        caption=L("HyDE：先写“假设答案”，再用它的向量检索——更贴文档措辞",
                  "HyDE: draft a hypothetical answer, then retrieve with its vector — closer to the doc's wording"),
    )
    + c.key_points([
        L("生产检索 = <strong>广召回</strong>（向量 + BM25 混合）+ <strong>精排</strong>（rerank），召回与精度分两步拿。",
          "Production retrieval = <strong>broad recall</strong> (vector + BM25 hybrid) + <strong>precise rerank</strong> — "
          "recall and precision in two steps."),
        L("纯向量对精确编号 / 罕见词不敏感；<strong>BM25</strong> 补字面匹配，二者用 <strong>RRF</strong> 融合。",
          "Vectors miss exact ids / rare tokens; <strong>BM25</strong> adds literal matching, fused via <strong>RRF</strong>."),
        L("<strong>Rerank</strong> 是 node_postprocessor（不是检索器），用交叉编码器把真正相关的提前。",
          "<strong>Rerank</strong> is a node_postprocessor (not a retriever) — a cross-encoder that lifts the truly relevant ones."),
        L("<strong>HyDE</strong> 用“假设答案”的向量检索，往往比原问句更贴文档措辞。",
          "<strong>HyDE</strong> retrieves with a hypothetical answer's vector, often closer to the document's wording than the raw question."),
    ])
    + c.design_highlight(L(
        "生产检索的精髓是<strong>把召回和精度拆开</strong>：先用混合检索“宁可多召、别漏”，再用 rerank“在小候选集里"
        "排得准”——一步求全、一步求准，比单一相似度分数又快又稳。",
        "The essence of production retrieval is <strong>splitting recall from precision</strong>: hybrid retrieval "
        "first (over-fetch, never miss), then rerank (order the small candidate set precisely) — one step for "
        "completeness, one for correctness, beating a single similarity score on both speed and reliability.",
    ))
)
LESSON_22 = _skeleton("规模化评估与 CI 回归闸", "evaluation at scale &amp; CI gating")
LESSON_23 = _skeleton("可观测与追踪", "observability &amp; tracing")
LESSON_24 = _skeleton("成本与延迟工程", "cost &amp; latency engineering")
LESSON_25 = _skeleton("安全与防护", "security &amp; guardrails")
LESSON_26 = _skeleton("Agent 与 Workflows", "agents &amp; workflows")
