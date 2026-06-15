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
LESSON_22 = (
    c.pipeline(None)
    + c.lead(L(
        "L19 学会了给单个答案打分；到了生产和团队协作，<strong>评估必须规模化、还要自动守门</strong>。"
        "三件事：① 用 <strong>DatasetGenerator</strong> 从文档<strong>自动造一批金标问题</strong>（再人工挑高价值子集标注）；"
        "② 用 <strong>BatchEvalRunner</strong> <strong>并发批量</strong>跑几十上百题、聚合成一个通过率；"
        "③ 把通过率接进 CI 做<strong>回归闸</strong>——低于阈值就 fail，坏改动<strong>合不进主干</strong>。"
        "一句话：把“凭感觉调”升级成“分数门槛守门”。",
        "L19 taught you to score a single answer; in production and on a team, <strong>evaluation must scale and gate "
        "automatically</strong>. Three moves: (1) use <strong>DatasetGenerator</strong> to <strong>auto-build a batch of "
        "gold questions</strong> from your docs (then hand-label a high-value subset); (2) use <strong>BatchEvalRunner"
        "</strong> to run dozens-to-hundreds of them <strong>concurrently</strong> and aggregate into one pass-rate; "
        "(3) wire that pass-rate into CI as a <strong>regression gate</strong> — below threshold the build fails and the "
        "bad change <strong>can't reach main</strong>. In a line: upgrade “tune by feel” into “a score threshold guards "
        "the door”.",
    ))
    + d.flow([
        ("docs", L("文档", "Docs"), L("现有知识库", "your corpus")),
        ("gen", L("自动生成 QA 金标", "Auto-gen gold QA"), L("DatasetGenerator + 人工挑选", "DatasetGenerator + human pick")),
        ("batch", L("批量评估器", "Batch evaluator"), L("BatchEvalRunner 并发跑", "BatchEvalRunner, concurrent")),
        ("agg", L("聚合分数", "Aggregate score"), L("通过率 / 趋势", "pass-rate / trend")),
        ("gate", L("CI 闸", "CI gate"), L("达标→合并 · 不达→回退", "pass→merge · fail→revert")),
    ], active="gate", caption=L(
        "金标集 → 批量评估 → 聚合 → 守门：分数达标才让改动进主干，不达标自动拦回",
        "Gold set → batch eval → aggregate → gate: only a passing score lets a change into main; a failing one is blocked automatically",
    ))
    + c.analogy(L(
        "像工厂出货前的<strong>自动质检关</strong>：每批货（每次改动）都要过<strong>同一组固定抽检</strong>（回归金标集），"
        "合格才放行上线（合并主干），不合格当场拦下（回退）。检验标准事先定死、机器自动判，"
        "没人能靠“感觉还行”把次品偷偷放出去。",
        "Like an <strong>automated QC gate</strong> before shipping: every batch (each change) must pass the <strong>same "
        "fixed sample inspection</strong> (the regression gold set); only a pass ships (merges to main), a fail is stopped "
        "on the spot (revert). The spec is fixed in advance and a machine rules on it — nobody can sneak a defect through "
        "on “feels fine”.",
    ))
    + d.grid(
        [L("尺子", "Ruler"), L("查什么（要什么输入）", "Checks what (inputs)"),
         L("在哪跑：开发 · CI · 线上抽样", "Where: dev · CI · prod-sampling")],
        [
            [L("<code>Faithfulness</code> 忠实度", "<code>Faithfulness</code>"),
             L("答案是否忠于检索（防幻觉）· 需 response + source_nodes，<strong>免参考答案</strong>",
               "is the answer grounded in retrieval (anti-hallucination) · needs response + source_nodes, <strong>no reference</strong>"),
             L("CI 回归闸<strong>主力</strong>：免标注、可全自动", "<strong>the CI gate's workhorse</strong>: label-free, fully automatable")],
            [L("<code>Relevancy</code> 相关性", "<code>Relevancy</code>"),
             L("检索与答案是否切题 · 需 query + response + source_nodes，<strong>免参考答案</strong>",
               "are context + answer on-topic · needs query + response + source_nodes, <strong>no reference</strong>"),
             L("CI 闸 + 线上抽样：同样免标注", "CI gate + prod-sampling: also label-free")],
            [L("<code>Correctness</code> 正确性", "<code>Correctness</code>"),
             L("对照参考答案对不对（1–5 分）· <strong>需 reference</strong>",
               "right vs a reference (1–5) · <strong>needs a reference</strong>"),
             L("人工金标子集 · 离线/夜间跑（较贵）", "human gold subset · offline/nightly (pricier)")],
        ],
        caption=L(
            "同样三把尺子，关键看“在哪跑”：免参考的忠实/相关当 CI 闸主力，需参考答案的正确性留给人工金标子集离线跑",
            "Same three rulers — what matters is “where they run”: reference-free faithfulness/relevancy power the CI gate, while reference-needing correctness runs offline over a human gold subset",
        ),
    )
    + c.section(
        L("从“手动评一次”到“自动守门”", "From “evaluate once by hand” to “gate automatically”"),
        c.compare_table(
            [L("对比项", "Aspect"), L("手动评一次（L19）", "Evaluate once, by hand (L19)"),
             L("规模化 + CI 回归闸（本课）", "At scale + CI gate (this lesson)")],
            [
                [L("跑多少", "How many"), L("手挑几道题、看一眼分数", "a few hand-picked Qs, eyeball the score"),
                 L("几十上百题<strong>并发批量</strong>、聚合成通过率", "dozens-to-hundreds run <strong>concurrently</strong>, aggregated into a pass-rate")],
                [L("金标从哪来", "Where gold comes from"), L("临时想几个问题", "invent a few questions on the spot"),
                 L("<code>DatasetGenerator</code> 自动造 + 人工标注高价值子集，沉淀为固定回归集",
                   "<code>DatasetGenerator</code> auto-builds + a human-labeled high-value subset, hardened into a fixed regression set")],
                [L("何时触发", "When it runs"), L("改完想起来才跑一次", "run once, if you remember"),
                 L("每次 PR/提交在 <strong>CI 自动</strong>跑（pytest 脚本）", "every PR/commit, <strong>automatically in CI</strong> (a pytest script)")],
                [L("不达标怎样", "On a miss"), L("自己看一眼、容易忘", "you glance at it, easy to forget"),
                 L("<code>assert</code> 失败、构建变红、<strong>挡住合并</strong>", "<code>assert</code> fails, the build goes red, <strong>merge blocked</strong>")],
                [L("防的风险", "Risk it guards"), L("只知这次改动好不好", "only whether this one change is OK"),
                 L("“修一个<strong>坏一批</strong>”的悄悄回归", "the silent “fix one, <strong>break many</strong>” regression")],
            ],
        ),
    )
    + c.section(
        L("把“凭感觉调”变成“分数门槛守门”", "Turning “tune by feel” into “a score threshold guards the door”"),
        L(
            "评估要当“闸”用，前提是有一套<strong>稳定、可复跑的金标集</strong>。从零造太慢，所以<strong>先自动起步</strong>："
            "<code>DatasetGenerator</code> 按文档块批量生成问题，几分钟就能铺出几十上百题的基线。但自动题<strong>良莠不齐</strong>，"
            "于是再做一层<strong>人工策展</strong>：挑出高价值、易回归的场景，补上人工核对的参考答案，沉淀成一个"
            "<strong>越用越准的回归子集</strong>。有了固定金标集，每次改动都对<strong>同一批题</strong>重跑、比<strong>趋势</strong>"
            "——这正是挡住“修一个坏一批”的关键：你盯着的那道题修好了，分数却告诉你另外十道悄悄退化了。最后把“低于阈值就 fail”"
            "写进 CI，<strong>守门这件事就不再依赖人的自觉</strong>。",
            "Using evaluation as a <strong>gate</strong> requires a <strong>stable, re-runnable gold set</strong>. Building "
            "one from scratch is slow, so <strong>start automatically</strong>: <code>DatasetGenerator</code> mass-produces "
            "questions per document chunk, laying down a dozens-to-hundreds baseline in minutes. But auto-generated "
            "questions are <strong>uneven</strong>, so add a layer of <strong>human curation</strong>: pick the high-value, "
            "regression-prone scenarios, attach human-checked reference answers, and let them harden into a <strong>"
            "regression subset that grows more trustworthy with use</strong>. With a fixed gold set, every change re-runs "
            "against the <strong>same questions</strong> and you watch the <strong>trend</strong> — exactly what blocks "
            "“fix one, break many”: the case you were staring at got fixed, but the score tells you ten others quietly "
            "regressed. Finally write “below threshold → fail” into CI, and <strong>gatekeeping no longer depends on "
            "anyone's discipline</strong>.",
        ),
        d.flow([
            ("auto", L("自动生成草稿", "Auto-gen drafts"), L("DatasetGenerator 批量出题", "DatasetGenerator, in bulk")),
            ("pick", L("人工挑高价值", "Human-pick high-value"), L("易回归/高频场景", "regression-prone/high-freq")),
            ("label", L("补参考答案", "Add references"), L("支撑 Correctness", "unlocks Correctness")),
            ("freeze", L("固化为回归集", "Freeze as regression set"), L("每次改动都重跑", "re-run on every change")),
            ("feed", L("线上反馈回灌", "Feed back from prod"), L("点踩/转人工补长尾", "thumbs-down/escalations → long tail")),
        ], caption=L(
            "金标集的造与养：自动起量 → 人工提纯 → 补参考答案 → 固化回归集 → 线上真实问题持续回灌",
            "Building and maintaining the gold set: auto for volume → human refine → add references → freeze a regression set → keep feeding real production questions",
        )),
    )
    + c.section(
        L("一道闸怎么挡住“修一个坏一批”", "How one gate blocks “fix one, break many”"),
        L(
            "回归闸的价值不在“这次改得好不好”，而在“别处有没有被悄悄带坏”。把同一套金标接进 CI，"
            "单题的局部改进再也盖不住整体的退化——分数跌破阈值，改动就进不了主干。",
            "A regression gate's value isn't “is this change good?” but “did it quietly break something elsewhere?”. Wire "
            "the same gold set into CI and a local single-question win can no longer mask an overall regression — break the "
            "threshold and the change can't reach main.",
        ),
        d.compare2(
            (L("没有回归闸（手动）", "No gate (manual)"), i18n.render(L(
                "为修好“退款多久到账”这道投诉，把 <code>chunk_size</code> 从 512 调到 1024。本地一看那题确实顺了就合并"
                "——可“保修期”“发票抬头”等十几道题的忠实度悄悄从 0.92 掉到 0.78，没人察觉，线上开始答非所问。",
                "To fix one complaint — “how long do refunds take” — you bump <code>chunk_size</code> from 512 to 1024. "
                "Locally that one reads fine, so you merge — but a dozen others (“warranty period”, “invoice title”) "
                "quietly drop in faithfulness from 0.92 to 0.78, unnoticed, and production starts answering off-topic.",
            ))),
            (L("有 CI 回归闸", "With a CI gate"), i18n.render(L(
                "同样的改动推上 PR，CI 用 50 题金标集并发重跑：那道题虽好，但<strong>整体通过率 0.92 → 0.78</strong>、"
                "跌破 0.90 阈值，<code>assert</code> 失败、构建变红，PR <strong>合不进主干</strong>——“修一个坏一批”当场被拦。",
                "Push the same change as a PR and CI re-runs the 50-question gold set concurrently: that one improved, but "
                "the <strong>overall pass-rate 0.92 → 0.78</strong> breaks the 0.90 bar, <code>assert</code> fails, the "
                "build goes red, and the PR <strong>can't reach main</strong> — “fix one, break many” is caught on the spot.",
            ))),
            caption=L(
                "同一次改动：没有闸，单题修好却悄悄拖垮十几题；有 CI 闸，整体通过率跌破阈值就当场拦回",
                "Same change: without a gate one fix silently drags down a dozen others; with a CI gate, the overall pass-rate breaking the bar blocks it on the spot",
            ),
        ),
    )
    + c.source_ref(
        "evaluation/batch_runner.py", "BatchEvalRunner",
        L("把多个评估器、多道问题<strong>并发</strong>批量跑，聚合成可对比的分数（规模化评估的核心）",
          "runs many evaluators over many questions <strong>concurrently</strong>, aggregating comparable scores (the heart of evaluation at scale)"),
    )
    + c.source_ref(
        "evaluation/dataset_generation.py", "DatasetGenerator",
        L("从文档自动生成 QA 金标问题，作为回归集的起点（再人工策展）",
          "auto-generates gold QA questions from documents as a starting regression set (then human-curated)"),
    )
    + c.accordion(
        L("深入：造金标集、批量评估与 CI 闸的取舍", "Deep dive: building the gold set, batch eval and the CI-gate trade-offs"),
        c.qa_item(
            L("🧪 示例：造一批金标、并发批量评", "🧪 Example: build a gold batch, evaluate concurrently"),
            L(
                "<code>DatasetGenerator.from_documents(docs, num_questions_per_chunk=2)</code> 先按块批量出题，"
                "<code>.generate_questions_from_nodes()</code> 拿到一串问题；再交给 "
                "<code>BatchEvalRunner({'faithfulness': ..., 'relevancy': ...}, workers=8)</code> 的 "
                "<code>aevaluate_queries(engine, queries=...)</code> 并发跑完，结果按指标名分组、每题一个 <code>EvaluationResult</code>。",
                "<code>DatasetGenerator.from_documents(docs, num_questions_per_chunk=2)</code> mass-produces questions per "
                "chunk, <code>.generate_questions_from_nodes()</code> yields the list; hand them to "
                "<code>BatchEvalRunner({'faithfulness': ..., 'relevancy': ...}, workers=8)</code>'s "
                "<code>aevaluate_queries(engine, queries=...)</code> to run concurrently — results grouped by metric name, "
                "one <code>EvaluationResult</code> per question.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计（可度量闭环）", "❓ Why designed this way (a measurable loop)"),
            L(
                "L19 把单次改动变得“可度量”，生产要的是让度量<strong>自动守门</strong>。把通过率接进 CI，"
                "<strong>坏改动在合并前就被分数拦下</strong>，质量不再依赖谁记得手动跑评估——“修一个坏一批”的回归"
                "被一道常态化的闸挡住。免参考的忠实度/相关性最适合当这道闸（不需要参考答案、能完全自动化）。",
                "L19 made one change “measurable”; production wants the measurement to <strong>gate automatically</strong>. "
                "Wire pass-rate into CI and <strong>a bad change is blocked by the score before merge</strong> — quality no "
                "longer depends on who remembers to run evals by hand, and the “fix one, break many” regression is held "
                "back by a standing gate. Reference-free faithfulness/relevancy fit this gate best (no gold answers needed, "
                "fully automatable).",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑（并发 · EvaluationResult.passing）", "⚙️ How it runs inside (concurrency · EvaluationResult.passing)"),
            L(
                "<code>BatchEvalRunner</code> 用 <code>workers</code> 控制<strong>并发度</strong>，底层走 async：先用 "
                "QueryEngine 批量产生答案，再把每个 (query, response, source_nodes) 喂给各评估器（多为 LLM-as-judge）。"
                "返回是 <code>dict[str, list[EvaluationResult]]</code>，每个 <code>EvaluationResult</code> 带 "
                "<code>passing</code>（是否达标）与 <code>score</code>；把一列 <code>passing</code> 求平均就是<strong>通过率</strong>，"
                "CI 闸比的就是它。",
                "<code>BatchEvalRunner</code> uses <code>workers</code> to set <strong>concurrency</strong>, async under the "
                "hood: it first batch-produces answers via the QueryEngine, then feeds each (query, response, source_nodes) "
                "to the evaluators (mostly LLM-as-judge). It returns a <code>dict[str, list[EvaluationResult]]</code>; each "
                "<code>EvaluationResult</code> carries <code>passing</code> (met the bar) and <code>score</code> — averaging "
                "a column of <code>passing</code> gives the <strong>pass-rate</strong> the CI gate compares against.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案（自动生成 vs 人工标注 vs 线上反馈）", "🔀 Alternatives (auto-gen vs human labeling vs prod feedback)"),
            L(
                "金标从哪来，有三条路：<strong>自动生成</strong>（<code>DatasetGenerator</code>，最快铺量，但题目参差、可能问得很浅）；"
                "<strong>人工标注</strong>（最准、能给参考答案支撑 Correctness，但慢且贵，只配给高价值子集）；"
                "<strong>线上真实反馈</strong>（用户点踩、人工申诉、客服转人工的会话——最贴近真实分布，但要脱敏与清洗）。"
                "生产里三者<strong>叠用</strong>：自动起量、人工提纯、线上补真实长尾。",
                "Gold data comes from three sources: <strong>auto-generation</strong> (<code>DatasetGenerator</code> — "
                "fastest to scale, but uneven and often shallow questions); <strong>human labeling</strong> (most accurate, "
                "supplies the reference answers Correctness needs, but slow and costly — reserve it for a high-value "
                "subset); and <strong>real production feedback</strong> (thumbs-down, escalations, handed-off chats — "
                "closest to the true distribution, but needs redaction and cleanup). Production <strong>stacks all "
                "three</strong>: auto for volume, humans for purity, production for the real long tail.",
            ),
        ),
    )
    + c.code(
        "from llama_index.core.evaluation import (DatasetGenerator, BatchEvalRunner,\n"
        "                                         FaithfulnessEvaluator, RelevancyEvaluator)\n\n"
        "# 1) 自动造金标问题（生产里再人工挑选/标注更可靠的子集）\n"
        "questions = DatasetGenerator.from_documents(\n"
        "    docs, num_questions_per_chunk=2).generate_questions_from_nodes()\n\n"
        "# 2) 并发批量评估：忠实度 + 相关性\n"
        "runner = BatchEvalRunner(\n"
        "    {'faithfulness': FaithfulnessEvaluator(), 'relevancy': RelevancyEvaluator()}, workers=8)\n"
        "results = await runner.aevaluate_queries(index.as_query_engine(), queries=questions[:50])",
        caption=L("造集 + 并发批量评估：DatasetGenerator 自动出题 → BatchEvalRunner（workers=8）并发跑 50 题",
                  "Build the set + batch-evaluate concurrently: DatasetGenerator drafts questions → BatchEvalRunner (workers=8) runs 50 in parallel"),
    )
    + c.code(
        "# 把评估变成 CI 回归闸：均通过率低于阈值就 fail（放进 pytest / CI 脚本）\n"
        "def pass_rate(rs):\n"
        "    return sum(r.passing for r in rs) / len(rs)\n\n"
        "faith = pass_rate(results['faithfulness'])\n"
        "print(f'faithfulness pass-rate: {faith:.0%}')\n"
        "assert faith >= 0.9, '忠实度回退，拦截本次变更'   # 守门：不达标就别合并",
        caption=L("把通过率变成 CI 回归闸：低于阈值就 assert 失败、挡住合并",
                  "Turn pass-rate into a CI regression gate: below threshold, assert fails and the merge is blocked"),
    )
    + c.key_points([
        L("规模化评估 = <strong>自动造金标</strong>（DatasetGenerator）+ <strong>并发批量评</strong>（BatchEvalRunner）+ "
          "<strong>CI 回归闸</strong>（通过率阈值），把评估从手动升级成自动守门。",
          "Evaluation at scale = <strong>auto-built gold</strong> (DatasetGenerator) + <strong>concurrent batch eval</strong> "
          "(BatchEvalRunner) + a <strong>CI regression gate</strong> (pass-rate threshold) — manual evaluation upgraded to automatic gatekeeping."),
        L("固定<strong>回归金标集</strong>是闸的前提：自动生成起量、人工标注高价值子集，挡住“修一个坏一批”。",
          "A fixed <strong>regression gold set</strong> is the gate's prerequisite: auto-generate for volume, hand-label a high-value subset — blocking “fix one, break many”."),
        L("<code>BatchEvalRunner</code> 用 <code>workers</code> 并发跑、按指标聚合 <code>EvaluationResult.passing</code>；通过率就是闸比对的数。",
          "<code>BatchEvalRunner</code> runs concurrently via <code>workers</code> and aggregates <code>EvaluationResult.passing</code> per metric; the pass-rate is what the gate compares."),
        L("免参考的<strong>忠实/相关</strong>最适合当 CI 闸；<strong>正确性</strong>需参考答案，留给人工金标子集。",
          "Reference-free <strong>faithfulness/relevancy</strong> fit the CI gate best; <strong>correctness</strong> needs references — reserve it for the human gold subset."),
    ])
    + c.design_highlight(L(
        "规模化评估的精髓是把“评估”变成“<strong>闸</strong>”：一套<strong>固定可复跑的金标集</strong> + 一个"
        "<strong>通过率阈值</strong>，让每次改动都必须用<strong>同一把尺子</strong>自证没有变差——质量从“谁记得测”"
        "升级成“不达标就合不进来”。",
        "The essence of evaluation at scale is turning “evaluation” into a <strong>gate</strong>: a <strong>fixed, "
        "re-runnable gold set</strong> plus a <strong>pass-rate threshold</strong> forces every change to prove — against "
        "the <strong>same ruler</strong> — that it didn't regress; quality goes from “whoever remembers to test” to "
        "“below the bar, it can't get in”.",
    ))
)
LESSON_23 = (
    c.pipeline(None)
    + c.lead(L(
        "一次生产 RAG 查询要走<strong>检索 → rerank → LLM 合成</strong>好几步，但你通常只看到<strong>最后那句"
        "答案</strong>——答错、答慢、答贵时，根本分不清是<strong>哪一步</strong>出的问题。<strong>可观测"
        "（observability）/ 追踪（tracing）</strong>把每一步的<strong>耗时 / token / 检索到的 node / 成本</strong>都"
        "记录下来，把<strong>黑盒</strong>变成一条<strong>逐步可见的时间线</strong>。LlamaIndex 几乎零成本就能接上："
        "一行 <code>set_global_handler('arize_phoenix')</code> 接到追踪后端，或用零依赖的 "
        "<code>LlamaDebugHandler</code> 在本地直接看内部。一句话：把“靠猜”换成“看 trace”。",
        "A production RAG query runs several steps — <strong>retrieve → rerank → LLM synthesis</strong> — yet you "
        "usually see only the <strong>final answer</strong>; when it's wrong, slow, or expensive you can't tell "
        "<strong>which step</strong> is to blame. <strong>Observability / tracing</strong> records every step's "
        "<strong>latency / tokens / retrieved nodes / cost</strong>, turning a <strong>black box</strong> into a "
        "<strong>step-by-step timeline</strong>. LlamaIndex makes this nearly free: one line of "
        "<code>set_global_handler('arize_phoenix')</code> wires a tracing backend, or the zero-dependency "
        "<code>LlamaDebugHandler</code> shows the internals locally. In a line: replace “guessing” with “reading the "
        "trace”.",
    ))
    + d.flow([
        ("ask", L("一次 query", "One query"), L("你只看到最后的答案", "you see only the final answer")),
        ("steps", L("隐藏的内部多步", "Hidden internal steps"), L("检索 · rerank · LLM 合成", "retrieve · rerank · LLM")),
        ("trace", L("trace 暴露每一步", "Trace exposes each step"), L("每步记一个 span", "one span per step")),
        ("signal", L("耗时 / token / node / 成本", "latency / tokens / nodes / cost"), L("慢/贵/错都看得见", "slow/pricey/wrong all show")),
        ("locate", L("定位到那一步", "Pinpoint the step"), L("是检索还是生成", "retrieval or generation")),
    ], active="trace", caption=L(
        "一次 query 的隐藏内部 → trace 把检索 · rerank · LLM 每步的 耗时 / token / node / 成本 摊开，定位慢/贵/错在哪一步",
        "A query's hidden internals → trace lays out each step's (retrieve · rerank · LLM) latency / tokens / nodes / cost, pinpointing where it's slow/pricey/wrong",
    ))
    + c.analogy(L(
        "像<strong>查快递物流</strong>：没有单号追踪，你只知道“包裹还没到”（答案不对 / 很慢），却不知卡在哪个环节；"
        "接上<strong>物流轨迹</strong>后，每个中转站的<strong>到达时间</strong>一目了然，立刻看出是<strong>分拣慢了</strong>"
        "还是<strong>派送堵了</strong>——trace 之于 RAG，就是物流轨迹之于包裹。",
        "Like <strong>tracking a parcel</strong>: with no tracking number you only know “it hasn't arrived” (the answer "
        "is wrong or slow) but not where it's stuck; turn on the <strong>shipping trace</strong> and every hub's "
        "<strong>arrival time</strong> is laid bare, so you instantly see whether <strong>sorting was slow</strong> or "
        "<strong>delivery was jammed</strong> — a trace is to a RAG query what shipment tracking is to a parcel.",
    ))
    + d.grid(
        [L("trace 里的信号", "Signal in the trace"), L("这一步暴露什么", "What it exposes"),
         L("帮你定位什么问题", "Which problem it pinpoints")],
        [
            [L("检索到的 node", "Retrieved nodes"),
             L("实际召回了哪些块、相似度分、命中没命中", "which chunks came back, similarity scores, hit or miss"),
             L("答案没依据 → 多半是<strong>检索</strong>错（块没召到 / 召错）", "answer ungrounded → usually a <strong>retrieval</strong> miss (wrong/missing chunk)")],
            [L("各步耗时", "Per-step latency"),
             L("retrieve · rerank · LLM 每段各花多少毫秒", "ms spent in retrieve · rerank · LLM each"),
             L("慢在哪一步 → 该优化检索、精排还是生成", "where it's slow → optimize retrieval, rerank or generation")],
            [L("token 与成本", "Tokens and cost"),
             L("prompt / completion 各多少 token、折算单价", "prompt / completion token counts and the cost they convert to"),
             L("贵在哪 → context 太长还是输出太长", "where it's pricey → context too long or output too long")],
        ],
        caption=L(
            "trace 里最该看的三类信号：检索到的 node 看“答得对不对”，各步耗时看“慢在哪”，token / 成本看“贵在哪”",
            "The three signals worth reading in a trace: retrieved nodes for “is it right”, per-step latency for “where it's slow”, tokens/cost for “where it's pricey”",
        ),
    )
    + c.section(
        L("RAG 多步、中间结果隐藏：可观测是生产调试的地基", "RAG is multi-step with hidden intermediates: observability is the bedrock of production debugging"),
        L(
            "RAG 的答案是<strong>一条多步流水线</strong>跑出来的：查询改写 → 检索 → rerank → 组 prompt → LLM 合成，"
            "每一步都可能出错，而你<strong>默认只看到最后那句话</strong>。答案不对，可能是<strong>检索</strong>没召到对的块，"
            "也可能是块召到了但 <strong>LLM</strong> 没用好；答案太慢，可能慢在 rerank 的交叉编码器，也可能慢在 LLM 生成；"
            "账单太贵，可能是 context 塞太长、也可能是输出太啰嗦。<strong>不打开中间结果，这些都只能靠猜</strong>——而猜的"
            "代价是一版版乱改、还可能“修好一个、碰坏一批”。可观测就是把这条隐藏流水线<strong>摊开成数据</strong>：每一步记"
            "一个 span，带上<strong>检索到的 node、相似度、各步耗时、prompt / completion 的 token 与成本</strong>。有了它，"
            "调试从“凭直觉试”变成“看着证据改”——先定位<strong>是检索还是生成</strong>的问题，再对症下药。这就是为什么生产 "
            "RAG 上线前，可观测往往是要<strong>第一个补齐的地基</strong>：没有它，后面的评估、调优、降本都是盲飞。",
            "A RAG answer comes out of a <strong>multi-step pipeline</strong>: query rewrite → retrieve → rerank → build "
            "prompt → LLM synthesis, and every step can go wrong while you <strong>see only the final sentence by "
            "default</strong>. A wrong answer might be <strong>retrieval</strong> missing the right chunk, or the chunk "
            "being retrieved but the <strong>LLM</strong> using it poorly; a slow answer might be slow in the rerank "
            "cross-encoder or in LLM generation; an expensive bill might be an over-long context or an over-verbose "
            "output. <strong>Without opening the intermediates, all of this is guesswork</strong> — and guessing costs "
            "you version-after-version flailing, with a real risk of “fix one, break many”. Observability <strong>lays "
            "this hidden pipeline out as data</strong>: each step emits a span carrying the <strong>retrieved nodes, "
            "similarity scores, per-step latency, and prompt / completion tokens and cost</strong>. With it, debugging "
            "shifts from “try on a hunch” to “change on evidence” — first pinpoint whether it's a <strong>retrieval or a "
            "generation</strong> problem, then treat the right one. That's why, before a production RAG ships, "
            "observability is usually the <strong>first foundation to put in place</strong>: without it, the later "
            "evaluation, tuning and cost work is all flying blind.",
        ),
        d.compare2(
            (L("没有 trace（黑盒、靠猜）", "No trace (black box, guessing)"), i18n.render(L(
                "用户问“<code>退款多久到账？</code>”答错了。你看不到内部：检索到的是哪几个块？rerank 后留下谁？"
                "prompt 里到底塞了什么？只能<strong>凭猜</strong>改——调 top_k、换 prompt、改 chunk_size，改一版试一版，"
                "像<strong>蒙着眼修车</strong>，可能折腾半天问题根本在另一头。",
                "A user asks “<code>how long until my refund arrives?</code>” and the answer is wrong. You can't see "
                "inside: which chunks were retrieved? what survived rerank? what actually went into the prompt? You can "
                "only <strong>guess</strong> — bump top_k, swap the prompt, change chunk_size, one version at a time, "
                "like <strong>fixing a car blindfolded</strong> — and may burn hours while the real cause sits at the "
                "other end.",
            ))),
            (L("有 trace（每步可见、可定位）", "With a trace (every step visible)"), i18n.render(L(
                "同一个问题，trace 一摊开：<strong>检索</strong>这步召回的 5 个 node 里压根没有“退款时效”那条"
                "（相似度全偏低）——问题在<strong>检索</strong>，不在生成。于是直接去补该文档、加 BM25 或调检索，"
                "而不是瞎改 prompt；顺带还看到 <strong>LLM 这步耗时 1.8s、占了八成延迟</strong>，慢在哪也一并清楚。",
                "Same question, trace laid open: the 5 nodes from the <strong>retrieval</strong> step don't even contain "
                "the “refund timing” clause (all low similarity) — the problem is <strong>retrieval</strong>, not "
                "generation. So you go fix that document, add BM25 or tune retrieval instead of randomly editing the "
                "prompt; you also notice the <strong>LLM step took 1.8s, ~80% of the latency</strong>, so where it's "
                "slow is clear too.",
            ))),
            caption=L(
                "同一次答错：没有 trace 只能蒙着眼乱改；有 trace 一眼看出是检索没召到、还顺带定位了延迟大头",
                "Same wrong answer: without a trace you tweak blindfolded; with a trace you see at a glance it was a retrieval miss — and spot the latency hog too",
            ),
        ),
    )
    + c.section(
        L("把内部接出来：三种常用追踪接法", "Surfacing the internals: three common ways to trace"),
        c.compare_table(
            [L("对比项", "Aspect"), L("<code>LlamaDebugHandler</code>（本地零依赖）", "<code>LlamaDebugHandler</code> (local, zero-dep)"),
             L("Arize Phoenix（本地可视化）", "Arize Phoenix (local UI)"), L("Langfuse（自托管 / 托管）", "Langfuse (self-host / hosted)")],
            [
                [L("怎么接", "How to plug in"), L("<code>CallbackManager</code> 手动挂", "attach via <code>CallbackManager</code>"),
                 L("<code>set_global_handler('arize_phoenix')</code> 一行", "one line: <code>set_global_handler('arize_phoenix')</code>"),
                 L("<code>set_global_handler('langfuse')</code> 一行", "one line: <code>set_global_handler('langfuse')</code>")],
                [L("看到什么", "What you see"), L("事件对 + 各步耗时（<code>get_event_pairs()</code>）", "event pairs + per-step latency (<code>get_event_pairs()</code>)"),
                 L("可视化 span 时间线、检索 node、token", "visual span timeline, retrieved nodes, tokens"),
                 L("同上 + 团队留存、数据集、标注", "the above + team retention, datasets, annotations")],
                [L("数据在哪", "Where data lives"), L("只在内存 / 控制台，跑完即弃", "in memory / console only, gone after the run"),
                 L("本地进程 / 浏览器，开发期排查", "local process / browser, for dev triage"),
                 L("自托管或云端，<strong>长期留存</strong>", "self-hosted or cloud, <strong>long-term retention</strong>")],
                [L("最适合", "Best for"), L("本地快速 debug、CI / 单测里<strong>断言</strong>各步", "quick local debug, <strong>asserting</strong> steps in CI/tests"),
                 L("本地 / 开发期<strong>可视化</strong>排查", "local / dev-time <strong>visual</strong> triage"),
                 L("<strong>线上</strong>团队协作、长期回放与监控", "<strong>production</strong> team collaboration, long-term replay and monitoring")],
            ],
        ),
    )
    + c.source_ref(
        "callbacks/global_handlers.py", "set_global_handler",
        L("一行切换全局追踪后端（Phoenix / Langfuse 等都走它），core 内置",
          "one line to switch the global tracing backend (Phoenix / Langfuse all go through it), built into core"),
    )
    + c.source_ref(
        "llama-index-callbacks-arize-phoenix", "arize_phoenix",
        L("把 trace 接到 Arize Phoenix 可视化的集成包（独立安装）",
          "the integration package that wires traces into the Arize Phoenix UI (installed separately)"),
    )
    + c.accordion(
        L("深入：一行接 Phoenix、instrumentation 事件 / span 与后端取舍", "Deep dive: one-line Phoenix, instrumentation events/spans, and backend trade-offs"),
        c.qa_item(
            L("🧪 示例：一行接上 Phoenix 看 trace", "🧪 Example: one line to trace into Phoenix"),
            L(
                "本地 <code>pip install llama-index-callbacks-arize-phoenix</code> 并启动 Phoenix"
                "（<code>px.launch_app()</code> 或独立进程），然后 <code>set_global_handler('arize_phoenix')</code> 一行接上。"
                "之后<strong>任意 query 无需改代码</strong>都会被记录：浏览器里能看到一条 query 的 span 时间线——检索召回了"
                "哪些 node、rerank 留下谁、LLM 这步多少 token / 耗时 / 成本，逐层点开。",
                "Locally <code>pip install llama-index-callbacks-arize-phoenix</code> and start Phoenix "
                "(<code>px.launch_app()</code> or a standalone process), then one line: "
                "<code>set_global_handler('arize_phoenix')</code>. After that <strong>any query records itself with no "
                "code changes</strong>: in the browser you get a span timeline for a query — which nodes retrieval "
                "returned, what rerank kept, and the LLM step's tokens / latency / cost, expandable layer by layer.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么生产 RAG 必须可观测", "❓ Why production RAG must be observable"),
            L(
                "因为 RAG 是<strong>多步且中间结果默认隐藏</strong>：你只拿到最后一句答案，却看不到检索召回了什么、各步"
                "花了多久、烧了多少 token。答错时，分不清<strong>是检索没召到</strong>还是<strong>生成没用好</strong>，"
                "只能一版版瞎改、还可能“修一个坏一批”。可观测把每步<strong>摊成证据</strong>，让调试、评估、降本都有据可依"
                "——它是其他生产能力（评估闸、成本优化、告警）的<strong>地基</strong>，没有它后面全是盲飞。",
                "Because RAG is <strong>multi-step with intermediates hidden by default</strong>: you get only the final "
                "sentence, not what retrieval returned, how long each step took, or how many tokens it burned. On a "
                "wrong answer you can't tell <strong>a retrieval miss</strong> from <strong>poor generation</strong>, so "
                "you flail version by version and risk “fix one, break many”. Observability <strong>turns each step "
                "into evidence</strong>, giving debugging, evaluation and cost work something to stand on — it's the "
                "<strong>foundation</strong> under other production capabilities (eval gates, cost tuning, alerting); "
                "without it the rest is flying blind.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑：事件 / span 与 CallbackManager", "⚙️ How it runs inside: events / spans and the CallbackManager"),
            L(
                "LlamaIndex 在每个关键环节（检索、rerank、LLM、embedding、合成）<strong>发出成对的事件</strong>："
                "<code>CBEventType</code> 的 start / end 各一条，配对起来就是<strong>一个 span</strong>，带上耗时与 payload"
                "（检索到的 node、prompt、token 等）。这些事件由挂在 <code>Settings.callback_manager</code> 上的各个 "
                "<strong>handler</strong> 接收：<code>LlamaDebugHandler</code> 把它们打印 / 存成 event pairs，"
                "Phoenix / Langfuse 的 handler 则把同样的 span 转成 OpenTelemetry 上报后端。新版还有更细的 "
                "<code>instrumentation</code>（<code>dispatcher</code> + span / event）体系，但对使用者而言核心不变："
                "<strong>一处挂 handler，全链路自动埋点</strong>。",
                "At each key stage (retrieve, rerank, LLM, embedding, synthesis) LlamaIndex <strong>emits paired "
                "events</strong>: a start and an end of a <code>CBEventType</code> that pair into <strong>one "
                "span</strong> carrying duration and a payload (retrieved nodes, prompt, tokens, etc.). These events are "
                "received by the <strong>handlers</strong> attached to <code>Settings.callback_manager</code>: "
                "<code>LlamaDebugHandler</code> prints/stores them as event pairs, while the Phoenix / Langfuse handlers "
                "turn the same spans into OpenTelemetry sent to a backend. Newer versions add a finer "
                "<code>instrumentation</code> system (a <code>dispatcher</code> + spans/events), but for users the core "
                "is unchanged: <strong>attach a handler in one place and the whole chain is auto-instrumented</strong>.",
            ),
        ),
        c.qa_item(
            L("🔀 后端取舍：Phoenix vs Langfuse vs 纯 OTel", "🔀 Backend trade-offs: Phoenix vs Langfuse vs raw OTel"),
            L(
                "三条常见路：<strong>Arize Phoenix</strong>——本地一行起步、可视化强，最适合<strong>开发期</strong>排查检索 / "
                "延迟，但默认偏单机、非长期留存；<strong>Langfuse</strong>——可自托管或托管，带<strong>团队留存、数据集、"
                "标注、线上监控</strong>，适合<strong>生产</strong>长期回放与协作；<strong>纯 OpenTelemetry</strong>——不绑某个 "
                "UI，直接把 span 上报到你已有的可观测栈（Jaeger / Grafana / Datadog 等），最适合<strong>已有 OTel 基建"
                "</strong>、要把 LLM trace 和服务 trace 拼在一起的团队。按<strong>开发期 vs 线上、是否要长期留存、是否已有 "
                "OTel 栈</strong>三点来选。",
                "Three common paths: <strong>Arize Phoenix</strong> — one-line local start, strong visualization, best "
                "for <strong>dev-time</strong> triage of retrieval / latency, but defaults to single-machine and isn't "
                "for long-term retention; <strong>Langfuse</strong> — self-hosted or hosted, with <strong>team "
                "retention, datasets, annotations and production monitoring</strong>, suited to <strong>production"
                "</strong> replay and collaboration; <strong>raw OpenTelemetry</strong> — not tied to one UI, exporting "
                "spans straight into your existing observability stack (Jaeger / Grafana / Datadog), best for teams that "
                "<strong>already run OTel</strong> and want LLM traces stitched together with service traces. Choose "
                "along three axes: <strong>dev vs production, long-term retention or not, and whether you already run "
                "OTel</strong>.",
            ),
        ),
    )
    + c.code(
        "from llama_index.core import set_global_handler\n"
        "\n"
        "# 一行接入追踪后端（需 pip install llama-index-callbacks-arize-phoenix 并本地启动 Phoenix）\n"
        "set_global_handler('arize_phoenix')\n"
        "\n"
        "# 之后任意 query 都会被记录：检索到的 node、各步耗时、token、成本\n"
        "index.as_query_engine().query('退款多久到账？')",
        caption=L("一行接入：set_global_handler('arize_phoenix') 之后，任意 query 自动记录到 Phoenix",
                  "One line: after set_global_handler('arize_phoenix'), any query auto-records into Phoenix"),
    )
    + c.code(
        "from llama_index.core import Settings\n"
        "from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler\n"
        "\n"
        "# 本地零依赖看内部：每个事件的耗时与中间结果\n"
        "debug = LlamaDebugHandler(print_trace_on_end=True)\n"
        "Settings.callback_manager = CallbackManager([debug])\n"
        "\n"
        "index.as_query_engine().query('保修期多久？')\n"
        "print(debug.get_event_pairs())   # 取检索/LLM 等事件对，看各步耗时",
        caption=L("零依赖看内部：LlamaDebugHandler + CallbackManager 打印每个事件对的耗时与中间结果",
                  "Zero-dep internals: LlamaDebugHandler + CallbackManager prints each event pair's latency and intermediate results"),
    )
    + c.key_points([
        L("RAG 是<strong>多步、中间结果隐藏</strong>的流水线：可观测把检索 · rerank · LLM 每步的"
          "<strong>耗时 / token / node / 成本</strong>摊成证据。",
          "RAG is a <strong>multi-step pipeline with hidden intermediates</strong>: observability lays each step's "
          "(retrieve · rerank · LLM) <strong>latency / tokens / nodes / cost</strong> out as evidence."),
        L("答错先看 trace：<strong>检索到的 node</strong> 对不对——分清是<strong>检索</strong>没召到还是"
          "<strong>生成</strong>没用好，再对症下药。",
          "On a wrong answer, read the trace first: are the <strong>retrieved nodes</strong> right — separate a "
          "<strong>retrieval</strong> miss from poor <strong>generation</strong>, then treat the right one."),
        L("一行接入：<code>set_global_handler('arize_phoenix')</code> 接可视化后端；零依赖用 "
          "<code>LlamaDebugHandler</code> + <code>CallbackManager</code> 本地看事件对。",
          "Plug in with one line: <code>set_global_handler('arize_phoenix')</code> for a visual backend; zero-dep, use "
          "<code>LlamaDebugHandler</code> + <code>CallbackManager</code> to read event pairs locally."),
        L("后端按场景选：<strong>Phoenix</strong> 开发期可视化、<strong>Langfuse</strong> 线上长期留存、"
          "<strong>纯 OTel</strong> 并入已有可观测栈。",
          "Pick the backend by use: <strong>Phoenix</strong> for dev-time visualization, <strong>Langfuse</strong> for "
          "long-term production retention, <strong>raw OTel</strong> to merge into an existing observability stack."),
    ])
    + c.design_highlight(L(
        "可观测的精髓是把 RAG 这条<strong>隐藏的多步流水线</strong>变成<strong>可读的证据</strong>：每步一个带 "
        "耗时 / token / node 的 span，让调试从“凭感觉一版版试”升级成“看着 trace 定位是哪一步”——它是评估、调优、"
        "降本一切生产能力的<strong>地基</strong>。",
        "The essence of observability is turning RAG's <strong>hidden multi-step pipeline</strong> into <strong>readable "
        "evidence</strong>: one span per step with latency / tokens / nodes, upgrading debugging from “try version after "
        "version on feel” to “read the trace and pinpoint the step” — the <strong>foundation</strong> beneath "
        "evaluation, tuning and cost work, every production capability.",
    ))
)
LESSON_24 = _skeleton("成本与延迟工程", "cost &amp; latency engineering")
LESSON_25 = _skeleton("安全与防护", "security &amp; guardrails")
LESSON_26 = _skeleton("Agent 与 Workflows", "agents &amp; workflows")
