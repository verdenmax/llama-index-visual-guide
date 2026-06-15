"""Part 3 (query path): lessons 12-16. Content filled task-by-task."""
import components as c
import diagrams as d
import i18n
from i18n import L


LESSON_12 = (
    c.pipeline("retrieve")
    + c.lead(L(
        "查询路径的第一步：<strong>Retriever</strong> 把问题向量化，去索引里取回最相关的 <strong>top-k</strong> 个 Node"
        "（带相似度分数的 <code>NodeWithScore</code>）。<code>index.as_retriever()</code> 是入口，此刻还没调用 LLM。",
        "First stop of the query path: a <strong>Retriever</strong> embeds the question and fetches the most relevant "
        "<strong>top-k</strong> Nodes (scored <code>NodeWithScore</code>). <code>index.as_retriever()</code> is the "
        "entry point — no LLM has been called yet.",
    ))
    + d.compare2(
        (L("好召回", "Good recall"), i18n.render(L(
            "问「退款政策是什么？」→ <code>retrieve()</code> 取回 top-3：<br>"
            "<strong>0.89</strong> 退款政策条款 ✓<br>"
            "<strong>0.86</strong> 退款到账时限 ✓<br>"
            "<strong>0.83</strong> 退款申请流程 ✓<br>"
            "三块全相关、分数高，正确依据都在 top-k 里。",
            "Ask “What's the refund policy?” → <code>retrieve()</code> returns top-3:<br>"
            "<strong>0.89</strong> refund-policy clause ✓<br>"
            "<strong>0.86</strong> refund timing ✓<br>"
            "<strong>0.83</strong> how to file a refund ✓<br>"
            "all relevant, all high-scoring — the right evidence sits in the top-k.",
        ))),
        (L("坏召回", "Bad recall"), i18n.render(L(
            "同一个问题，却取回：<br>"
            "<strong>0.71</strong> 配送时效 ✗ 跑题<br>"
            "<strong>0.55</strong> 账户注册 ✗ 跑题<br>"
            "<strong>0.31</strong> 退款政策条款 —— 正确块分数偏低、险些没进 top-k<br>"
            "无关块挤进来、正确依据沉到末尾，召回失准。",
            "Same query, yet it fetches:<br>"
            "<strong>0.71</strong> delivery times ✗ off-topic<br>"
            "<strong>0.55</strong> account signup ✗ off-topic<br>"
            "<strong>0.31</strong> refund-policy clause — the right chunk, scoring low, barely in the top-k<br>"
            "noise crowds in and the right evidence sinks to the bottom — recall is off.",
        ))),
        caption=L(
            "不调用 LLM，只看 <code>retrieve()</code> 的结果就能判断召回好坏",
            "Without calling the LLM, you can judge recall from <code>retrieve()</code>'s results alone",
        ),
    )
    + c.analogy(L(
        "图书管理员按你的主题<strong>取回最相关的几页</strong>，整齐摆在桌上——但还没开始替你写答案。",
        "The librarian <strong>brings back the few most relevant pages</strong> and lays them out — but hasn't started "
        "writing your answer yet.",
    ))
    + c.section(
        L("检索的关键旋钮", "The key retrieval knob"),
        c.compare_table(
            [L("概念", "Concept"), L("含义", "Meaning")],
            [
                [L("<code>similarity_top_k</code>", "<code>similarity_top_k</code>"), L("取回多少个最相近 Node", "how many nearest Nodes to fetch")],
                [L("<code>NodeWithScore</code>", "<code>NodeWithScore</code>"), L("Node + 相似度分数", "a Node plus its similarity score")],
                [L("<code>QueryBundle</code>", "<code>QueryBundle</code>"), L("封装查询（文本/向量）", "wraps the query (text/embedding)")],
            ],
        ),
    )
    + d.compare2(
        (L("top_k 太小", "top_k too small"), i18n.render(L(
            "只取回 1–2 个块，容易漏掉真正相关的内容，答案残缺。",
            "Fetching only 1–2 chunks risks missing the truly relevant content, so the answer comes out incomplete.",
        ))),
        (L("top_k 太大", "top_k too large"), i18n.render(L(
            "取回过多块会混入无关噪声，既增加成本，也可能稀释真正的答案。",
            "Fetching too many chunks lets in irrelevant noise, raising cost and potentially diluting the real answer.",
        ))),
        caption=L(
            "similarity_top_k 是召回与噪声之间的平衡旋钮（常从 3–5 起步）",
            "similarity_top_k balances recall against noise (often start at 3–5)",
        ),
    )
    + c.section(
        L("为什么把检索单独拎出来", "Why isolate retrieval as its own step"),
        L(
            "检索与生成解耦后，“召回对不对”可以脱离 LLM 单独度量：直接看 <code>retrieve()</code> 返回的 Node "
            "是否包含正确依据。于是调相似度阈值、换检索器、改 top_k 都能立刻验证，而不必每次都跑一遍昂贵的生成。",
            "Once retrieval is decoupled from generation, “did we recall the right content?” can be measured without the "
            "LLM at all: just inspect whether the Nodes from <code>retrieve()</code> contain the right evidence. Tuning "
            "the cutoff, swapping retrievers or changing top_k is then verified instantly, without paying for "
            "generation every time.",
        ),
        L(
            "这正是把检索单列一课的原因：命中率（hit-rate）、MRR 这类指标只对 <code>retrieve()</code> 的输出打分，"
            "完全不跑生成。召回这关没过，再强的 LLM 也只是在错误的资料上一本正经地作答；先把“取回对的内容”调好，"
            "后面的后处理与合成才谈得上意义。",
            "That's exactly why retrieval earns a lesson of its own: metrics like hit-rate or MRR score only the output "
            "of <code>retrieve()</code>, never running generation. If recall fails, even the strongest LLM merely "
            "reasons fluently over the wrong material; get “fetch the right content” right first, and only then do "
            "post-processing and synthesis even matter.",
        ),
    )
    + c.source_ref("indices/vector_store/retrievers/retriever.py", "VectorIndexRetriever", L("向量索引的检索器", "the vector-index retriever"))
    + c.source_ref("base/base_retriever.py", "BaseRetriever.retrieve", L("所有检索器的统一入口", "the unified entry point every retriever shares"))
    + c.accordion(
        L("深入：检索这一步的里里外外", "Deep dive: the ins and outs of retrieval"),
        c.qa_item(
            L("🧪 示例：只检索不生成", "🧪 Example: retrieve without generating"),
            L(
                "<code>index.as_retriever(similarity_top_k=3).retrieve('…')</code> 返回 <code>List[NodeWithScore]</code>，"
                "你可以直接打印分数和文本，确认召回是否命中——完全不碰 LLM。",
                "<code>index.as_retriever(similarity_top_k=3).retrieve('…')</code> returns a "
                "<code>List[NodeWithScore]</code>; print the scores and text to confirm the recall hit — without "
                "touching the LLM.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "把检索独立成一等公民，你就能<strong>单独评估与优化召回</strong>，再分别优化生成，两个问题不再纠缠。",
                "Making retrieval a first-class citizen lets you <strong>evaluate and optimize recall on its own</strong>, "
                "then optimize generation separately — the two problems stop entangling.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "<code>BaseRetriever.retrieve()</code> 是模板方法：它处理 QueryBundle 等通用逻辑，再调用各子类实现的 "
                "<code>_retrieve()</code>（如 <code>VectorIndexRetriever</code> 做向量近邻搜索）。",
                "<code>BaseRetriever.retrieve()</code> is a template method: it handles shared logic like the QueryBundle, "
                "then calls each subclass's <code>_retrieve()</code> (e.g. <code>VectorIndexRetriever</code> does vector "
                "nearest-neighbor search).",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "除了向量检索，还有关键词检索（BM25）、知识图谱检索，以及把多者融合的混合检索——它们都实现同一个 "
                "<code>BaseRetriever</code> 接口，可直接替换。",
                "Beyond vector search there's keyword retrieval (BM25), knowledge-graph retrieval, and hybrid retrieval "
                "that fuses several — all implementing the same <code>BaseRetriever</code> interface, so they drop in "
                "interchangeably.",
            ),
        ),
    )
    + c.code(
        "retriever = index.as_retriever(similarity_top_k=3)\n"
        "nodes = retriever.retrieve('退款政策是什么？')   # List[NodeWithScore]\n"
        "for n in nodes:\n"
        "    print(round(n.score, 3), n.node.text[:50])\n"
        "# 注意：此处只检索，尚未生成答案",
        caption=L("检索独立于生成，可单独评估", "retrieval is separate from generation — evaluate it alone"),
    )
    + c.code(
        "from llama_index.core.retrievers import VectorIndexRetriever\n\n"
        "# 直接构造检索器（等价于 index.as_retriever，但更显式）\n"
        "retriever = VectorIndexRetriever(index=index, similarity_top_k=4)\n"
        "for n in retriever.retrieve('国际订单的退款要多久？'):\n"
        "    print(f'{n.score:.3f}  {n.node.get_content()[:50]}')\n"
        "    print('  来源:', n.node.metadata.get('file_name'))",
        caption=L("显式构造 VectorIndexRetriever，逐条查看分数与来源", "Construct VectorIndexRetriever explicitly to inspect each score and source"),
    )
    + c.key_points([
        L("Retriever 返回 <strong>top-k 个带分数的 Node</strong>，不产生最终答案。",
          "A Retriever returns the <strong>top-k scored Nodes</strong>, not the final answer."),
        L("<code>similarity_top_k</code> 太小漏召回、太大引噪声。",
          "Too small a <code>similarity_top_k</code> misses; too large adds noise."),
        L("检索与生成<strong>解耦</strong>，便于单独调试与评估检索质量。",
          "Decoupling retrieval from generation lets you debug and evaluate retrieval on its own."),
    ])
    + c.design_highlight(L(
        "把“取相关片段”独立成 Retriever，意味着你能在不动 LLM 的前提下，专门优化“召回了对的内容没有”这一核心问题。",
        "Isolating “fetch relevant pieces” as a Retriever means you can optimize the core question — “did we recall the "
        "right content?” — without ever touching the LLM.",
    ))
)
LESSON_13 = (
    c.pipeline("postprocess")
    + c.lead(L(
        "检索回来的 Node 在喂给 LLM <strong>之前</strong>还能再加工：<strong>过滤</strong>低分、<strong>重排（rerank）</strong>"
        "把最相关的提前、或<strong>替换</strong>为句窗上下文。这一步便宜却常常显著提升答案质量。",
        "Before the Nodes reach the LLM they can be reworked: <strong>filter</strong> low scores, <strong>rerank</strong> "
        "the most relevant to the top, or <strong>replace</strong> them with sentence-window context. It's cheap yet "
        "often a big quality win.",
    ))
    + d.flow([
        ("ret", L("检索结果", "Retrieved"), L("原始 top-k Node", "raw top-k Nodes")),
        ("pp", L("后处理", "Post-process"), L("过滤 / 重排 / 替换", "filter / rerank / replace")),
        ("kept", L("精选 Node", "Curated Nodes")),
        ("llm", L("交给 LLM", "Hand to the LLM")),
    ], active="pp", caption=L(
        "后处理是检索与生成之间的“质检站”：先把 Node 修整好，再送进 LLM",
        "Post-processing is a “QC station” between retrieval and generation: groom the Nodes before they reach the LLM",
    ))
    + c.analogy(L(
        "取回的资料先<strong>筛掉跑题的</strong>、把<strong>最相关的排到最前</strong>，再交给写手——写手只读精选过的几页。",
        "Sift out the off-topic pages, move the <strong>most relevant to the front</strong>, then hand them to the "
        "writer — who only reads the curated few.",
    ))
    + c.section(
        L("常用后处理器", "Common postprocessors"),
        c.compare_table(
            [L("后处理器", "Postprocessor"), L("做什么", "What it does")],
            [
                [L("SimilarityPostprocessor", "SimilarityPostprocessor"), L("按 <code>similarity_cutoff</code> 丢掉低分", "drop nodes below <code>similarity_cutoff</code>")],
                [L("Rerank（LLM / Cohere…）", "Rerank (LLM / Cohere…)"), L("用更强模型重排相关性", "re-score relevance with a stronger model")],
                [L("MetadataReplacementPostProcessor", "MetadataReplacementPostProcessor"), L("把句窗节点换成 window 上下文", "swap window-node text for its window")],
            ],
        ),
    )
    + d.compare2(
        (L("过滤前", "Before cutoff"), i18n.render(L(
            "问「退款多久到账？」检索 top-k：<br>"
            "<strong>0.86</strong> 退款到账时限 ✓<br>"
            "<strong>0.41</strong> 配送时效 ✗ 低分却混进 top-k<br>"
            "→ 答案被带偏：<em>“一般 3–5 个工作日<strong>送达</strong>”</em>——答成了配送，答非所问。",
            "Ask “How long until a refund lands?”; top-k:<br>"
            "<strong>0.86</strong> refund timing ✓<br>"
            "<strong>0.41</strong> delivery times ✗ low score, still slips in<br>"
            "→ Answer derails: <em>“usually <strong>delivered</strong> in 3–5 business days”</em> — that's shipping, off-question.",
        ))),
        (L("过滤后", "After cutoff (0.7)"), i18n.render(L(
            "<code>similarity_cutoff=0.7</code> 丢掉 0.41 那块，只留：<br>"
            "<strong>0.86</strong> 退款到账时限 ✓<br>"
            "→ 答案命中：<em>“退款 3–5 个工作日原路退回”</em>——同一个问题，这次答对了。",
            "<code>similarity_cutoff=0.7</code> drops the 0.41 chunk, leaving:<br>"
            "<strong>0.86</strong> refund timing ✓<br>"
            "→ Answer lands: <em>“refunds post back to source in 3–5 business days”</em> — same question, now correct.",
        ))),
        caption=L(
            "同一个问题：滤掉一个低分噪声块，答案就从“答非所问”变成“命中正确依据”",
            "Same question: drop one low-score noise chunk and the answer flips from off-topic to on-target",
        ),
    )
    + c.section(
        L("最便宜的一档提质", "The cheapest quality lever"),
        L(
            "后处理介于“检索之后、生成之前”，多是非 LLM 的轻量操作（打分阈值、重排），却能去掉噪声、补回上下文。"
            "因为不重训、不换模型，它往往是 RAG 调优里<strong>性价比最高</strong>的一步。",
            "Post-processing sits “after retrieval, before generation,” and is mostly lightweight non-LLM work (score "
            "thresholds, reranking) that removes noise and restores context. Because it needs no retraining and no model "
            "swap, it is often the <strong>best bang-for-buck</strong> step in RAG tuning.",
        ),
    )
    + c.source_ref("postprocessor/node.py", "SimilarityPostprocessor", L("相似度阈值过滤", "similarity-threshold filtering"))
    + c.source_ref("postprocessor/metadata_replacement.py", "MetadataReplacementPostProcessor", L("配合句窗切块还原上下文", "restores context for sentence-window chunks"))
    + c.accordion(
        L("深入：后处理的来龙去脉", "Deep dive: the ins and outs of post-processing"),
        c.qa_item(
            L("🧪 示例：一行阈值过滤", "🧪 Example: a one-line threshold filter"),
            L(
                "<code>SimilarityPostprocessor(similarity_cutoff=0.7).postprocess_nodes(nodes)</code> 直接返回保留下来的 "
                "Node，可对比过滤前后的数量。",
                "<code>SimilarityPostprocessor(similarity_cutoff=0.7).postprocess_nodes(nodes)</code> returns just the kept "
                "Nodes; compare the count before and after.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "把“检索后、生成前”做成<strong>可插拔的一串 postprocessor</strong>，你能用最低成本叠加多种提质手段，互不影响。",
                "Modeling “after retrieval, before generation” as a <strong>pluggable chain of postprocessors</strong> lets "
                "you stack several quality boosts at minimal cost, each independent of the others.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "每个后处理器实现 <code>postprocess_nodes(nodes)</code>，输入输出都是 <code>List[NodeWithScore]</code>；"
                "<code>SimilarityPostprocessor</code> 把分数低于 cutoff 的直接丢弃。",
                "Each postprocessor implements <code>postprocess_nodes(nodes)</code>, taking and returning a "
                "<code>List[NodeWithScore]</code>; <code>SimilarityPostprocessor</code> simply drops anything below the cutoff.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "阈值过滤便宜但粗糙；交叉编码器 rerank（如 Cohere / LLM rerank）更准但要额外一次调用——按预算与质量需求取舍。",
                "Threshold filtering is cheap but blunt; cross-encoder reranking (e.g. Cohere / LLM rerank) is more accurate "
                "but costs an extra call — trade off by budget and quality needs.",
            ),
        ),
    )
    + c.code(
        "from llama_index.core.postprocessor import SimilarityPostprocessor\n\n"
        "nodes = index.as_retriever(similarity_top_k=5).retrieve('退款政策？')\n"
        "pp = SimilarityPostprocessor(similarity_cutoff=0.7)\n"
        "kept = pp.postprocess_nodes(nodes)   # 丢掉分数低于 0.7 的\n"
        "print(len(nodes), '-&gt;', len(kept))\n\n"
        "# 句窗专用：把单句节点替换为其上下文窗口\n"
        "from llama_index.core.postprocessor import MetadataReplacementPostProcessor\n"
        "mr = MetadataReplacementPostProcessor(target_metadata_key='window')",
        caption=L("检索与生成之间的“质检站”", "a QC station between retrieval and generation"),
    )
    + c.code(
        "from llama_index.core.node_parser import SentenceWindowNodeParser\n"
        "from llama_index.core.postprocessor import MetadataReplacementPostProcessor\n\n"
        "# 建索引时按单句切，并把前后句存进 metadata['window']\n"
        "parser = SentenceWindowNodeParser.from_defaults(\n"
        "    window_size=3, window_metadata_key='window',\n"
        "    original_text_metadata_key='original')\n\n"
        "# 查询时把命中的单句节点，还原成它的上下文窗口再交给 LLM\n"
        "engine = index.as_query_engine(\n"
        "    similarity_top_k=3,\n"
        "    node_postprocessors=[MetadataReplacementPostProcessor(target_metadata_key='window')],\n"
        ")",
        caption=L("句窗检索：命中一句，却把整段上下文喂给 LLM", "Sentence-window: match one sentence, feed the LLM its whole window"),
    )
    + c.key_points([
        L("后处理在<strong>检索之后、生成之前</strong>，调整喂给 LLM 的 Node。",
          "Postprocessing sits <strong>after retrieval, before generation</strong>, shaping the Nodes the LLM sees."),
        L("<code>similarity_cutoff</code> 滤噪；rerank 提相关性；窗口替换补上下文。",
          "<code>similarity_cutoff</code> denoises; rerank lifts relevance; window replacement restores context."),
        L("它便宜（多为非 LLM 或一次轻量调用）却常带来明显提升。",
          "It's cheap (often non-LLM or one light call) yet frequently a clear win."),
    ])
    + c.design_highlight(L(
        "把“检索后、生成前”抽象成一串可插拔 postprocessor，让你<strong>在不重训、不换模型</strong>的情况下，"
        "用最低成本提升答案质量——RAG 调优性价比最高的一环。",
        "Modeling “after retrieval, before generation” as pluggable postprocessors lets you raise answer quality at the "
        "lowest cost — <strong>no retraining, no model swap</strong>. The best bang-for-buck in RAG tuning.",
    ))
)
LESSON_14 = (
    c.pipeline("synthesize")
    + c.lead(L(
        "拿到（过滤/重排后的）top-k Node，怎么揉成<strong>一个答案</strong>？<strong>Response Synthesizer</strong> 决定"
        "“多个片段→单个回答”的策略，核心是应对<strong>上下文窗口</strong>与<strong>片段数量</strong>的权衡。",
        "Given the (filtered/reranked) top-k Nodes, how do you fuse them into <strong>one answer</strong>? The "
        "<strong>Response Synthesizer</strong> sets the “many chunks → one answer” strategy — chiefly trading off "
        "<strong>context window</strong> against <strong>number of chunks</strong>.",
    ))
    + d.grid(
        [L("模式", "Mode"), L("形态：多个片段如何变成一个答案", "Shape: how many chunks become one answer")],
        [
            [L("compact（默认）", "compact (default)"), L("尽量塞满上下文，一次写完", "pack the context, write once")],
            [L("refine", "refine"), L("逐块链式精炼，答案不断被改写", "chain through chunks, refining the answer each step")],
            [L("tree_summarize", "tree_summarize"), L("分组总结，再把总结向上合并", "summarize in groups, then merge summaries upward")],
            [L("accumulate", "accumulate"), L("每块各自作答，最后汇总", "answer each chunk separately, then collect")],
        ],
        caption=L("四种 ResponseMode 的“形态”速览", "The four ResponseModes at a glance, by shape"),
    )
    + c.analogy(L(
        "写手拿到几页资料的几种写法：<strong>逐页精炼</strong>（refine）、<strong>塞满一次写</strong>（compact）、"
        "<strong>分组总结再合并</strong>（tree_summarize）、<strong>每页各答再汇总</strong>（accumulate）。",
        "Different ways a writer drafts from several pages: <strong>refine page by page</strong>, <strong>pack as many "
        "as fit and write once</strong> (compact), <strong>summarize in groups then merge</strong> (tree_summarize), or "
        "<strong>answer each page then collect</strong> (accumulate).",
    ))
    + c.section(
        L("常用 ResponseMode", "Common ResponseModes"),
        c.compare_table(
            [L("模式", "Mode"), L("适合", "Good for")],
            [
                [L("compact（默认）", "compact (default)"), L("通用、省调用", "general, fewer calls")],
                [L("refine", "refine"), L("片段多、需细读", "many chunks, careful reading")],
                [L("tree_summarize", "tree_summarize"), L("总结类问题", "summary questions")],
                [L("accumulate", "accumulate"), L("逐条抽取", "per-chunk extraction")],
            ],
        ),
    )
    + c.section(
        L("多片段如何收敛成一个答案", "How many chunks converge into one answer"),
        L(
            "合成的核心矛盾是：检索到的片段可能装不进一次上下文窗口。compact 尽量塞、少调用；refine 逐块迭代、读得细；"
            "tree_summarize 分层合并、擅长全局总结。<strong>选 mode 本质上是在“上下文窗口”和“片段数量”之间取舍。</strong>",
            "The core tension of synthesis: the retrieved chunks may not fit in one context window. compact packs them and "
            "minimizes calls; refine iterates chunk by chunk and reads carefully; tree_summarize merges in layers and "
            "excels at global summaries. <strong>Choosing a mode is fundamentally a trade-off between context window and "
            "number of chunks.</strong>",
        ),
        d.vflow([
            (L("8 个检索片段", "8 retrieved chunks"), L("太多，装不进一次上下文", "too many for a single context window")),
            (L("分组各自总结", "summarize each group"), L("→ 几个小结", "→ a few partial summaries")),
            (L("再总结这些小结", "summarize those summaries"), L("→ 更少的中间结果", "→ fewer intermediate results")),
            (L("单个最终答案", "one final answer"), None),
        ], caption=L("tree_summarize：像锦标赛一样逐层向上合并", "tree_summarize: merge upward, round by round, like a tournament")),
    )
    + c.source_ref("response_synthesizers/factory.py", "get_response_synthesizer", L("按 ResponseMode 造合成器", "builds a synthesizer for a ResponseMode"))
    + c.source_ref("response_synthesizers/type.py", "ResponseMode", L("所有合成策略的枚举", "the enum of synthesis strategies"))
    + c.accordion(
        L("深入：响应合成的取舍", "Deep dive: the trade-offs of response synthesis"),
        c.qa_item(
            L("🧪 示例：显式造合成器", "🧪 Example: build a synthesizer explicitly"),
            L(
                "<code>get_response_synthesizer(response_mode='tree_summarize')</code> 造出的合成器可单独使用，"
                "也可传给 query engine，便于精确控制合成策略。",
                "<code>get_response_synthesizer(response_mode='tree_summarize')</code> builds a synthesizer you can use on "
                "its own or pass to a query engine, for precise control over the synthesis strategy.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "把“拼接片段”抽象成可切换的 ResponseMode，让同一套检索结果既能服务精确问答，也能服务全局总结，无需改检索。",
                "Abstracting “stitch the chunks” into switchable ResponseModes lets one set of retrieved results serve both "
                "precise Q&amp;A and global summarization — with no change to retrieval.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "<code>ResponseMode</code> 是个枚举；<code>compact</code> 实际是 compact_and_refine——先把片段尽量塞满，"
                "装不下时再退回 refine 的逐块迭代。",
                "<code>ResponseMode</code> is an enum; <code>compact</code> is really compact_and_refine — pack chunks "
                "first, falling back to refine's chunk-by-chunk iteration when they don't all fit.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "通用问答用 compact（省调用）；要细读多片段用 refine；要全局总结用 tree_summarize；要逐条抽取用 accumulate。",
                "Use compact for general Q&amp;A (fewer calls), refine to read many chunks carefully, tree_summarize for "
                "global summaries, and accumulate for per-chunk extraction.",
            ),
        ),
    )
    + c.code(
        "from llama_index.core import get_response_synthesizer\n\n"
        "# 方式一：直接在 query engine 上选模式\n"
        "engine = index.as_query_engine(response_mode='tree_summarize')\n"
        "print(engine.query('把这些文档总结成 3 点'))\n\n"
        "# 方式二：显式造一个合成器（便于自定义装配，见下一课）\n"
        "synth = get_response_synthesizer(response_mode='compact')",
        caption=L("选 mode = 选“多片段→单答案”的策略", "choosing a mode = choosing the many→one strategy"),
    )
    + c.code(
        "from llama_index.core import get_response_synthesizer\n\n"
        "# 显式造一个 refine 合成器，逐块迭代精炼答案\n"
        "synth = get_response_synthesizer(response_mode='refine')\n\n"
        "# 装到 query engine 上：检索照旧，合成改用 refine\n"
        "engine = index.as_query_engine(response_synthesizer=synth, similarity_top_k=6)\n"
        "print(engine.query('把这几篇文档的结论逐点对比一下'))",
        caption=L("显式装配合成器：把 refine 接到查询引擎上", "Wire a synthesizer explicitly: attach refine to the query engine"),
    )
    + c.section(
        L("把三课串成一条查询路径", "Threading lessons 12–14 into one query path"),
        L(
            "第 12、13、14 课各自从 <code>index.as_retriever</code> 起步，读起来像三段彼此独立的代码。其实一次 "
            "<code>.query()</code> 就把它们串成一条流水线：同一批 Node 被检索取回、被后处理筛选、再交合成器落笔，"
            "一路传递下去。",
            "Lessons 12, 13 and 14 each start over at <code>index.as_retriever</code>, so they read like three "
            "disconnected snippets. In reality one <code>.query()</code> threads them into a single pipeline: the same "
            "batch of Nodes is retrieved, filtered by post-processing, then handed to the synthesizer — flowing straight "
            "through.",
        ),
        d.vflow([
            (L("问「国际订单的退款要几天？」", "Q “How many days for an international-order refund?”"),
             L("第 12 课 · retrieve(similarity_top_k=5)", "Lesson 12 · retrieve(similarity_top_k=5)")),
            (L("取回 5 个 NodeWithScore", "5 NodeWithScore returned"),
             L("0.88 退款时限 ✓ · 0.83 国际退款 ✓ · 0.79 退款流程 ✓ · 0.48 配送时效 ✗ · 0.31 账户注册 ✗",
               "0.88 refund timing ✓ · 0.83 intl refund ✓ · 0.79 refund flow ✓ · 0.48 delivery ✗ · 0.31 signup ✗")),
            (L("第 13 课 · similarity_cutoff=0.7 筛", "Lesson 13 · similarity_cutoff=0.7 filters"),
             L("丢掉 0.48 与 0.31 两块，只留 3 个高分 Node", "drops the 0.48 and 0.31 chunks, keeping 3 high-score Nodes")),
            (L("第 14 课 · synthesize（compact）", "Lesson 14 · synthesize (compact)"),
             L("把 3 个 Node 揉成一个答案", "fuses the 3 Nodes into one answer")),
            (L("Response", "Response"),
             L("“国际订单退款约 5–7 个工作日” + source_nodes（3 条可溯源）",
               "“International-order refunds take ~5–7 business days” + source_nodes (3 traceable)")),
        ], caption=L(
            "一个问题一路传递：第 12 课取回 → 第 13 课筛 → 第 14 课合成",
            "One question passed straight through: Lesson 12 retrieves → Lesson 13 filters → Lesson 14 synthesizes",
        )),
    )
    + c.key_points([
        L("Synthesizer 解决“<strong>多个 Node 如何合成一个答案</strong>”。",
          "The synthesizer solves “<strong>how many Nodes become one answer</strong>”."),
        L("<code>compact</code> 省调用，<code>tree_summarize</code> 擅总结，<code>refine</code> 重细读。",
          "<code>compact</code> saves calls, <code>tree_summarize</code> summarizes, <code>refine</code> reads carefully."),
        L("模式选择本质是<strong>上下文窗口 vs 片段数量</strong>的权衡。",
          "Mode choice is fundamentally <strong>context window vs number of chunks</strong>."),
    ])
    + c.design_highlight(L(
        "把“拼接片段”这件容易写死的事抽象成可切换的 ResponseMode，让同一套检索结果能服务“精确问答”到“全局总结”不同需求。",
        "Abstracting “stitch the chunks” into switchable ResponseModes lets one set of retrieved results serve "
        "everything from precise Q&amp;A to global summarization.",
    ))
)
LESSON_15 = (
    c.pipeline("answer")
    + c.lead(L(
        "<strong>QueryEngine</strong> 把<strong>检索器 + 后处理 + 响应合成器</strong>装配成一个 <code>.query()</code> 入口。"
        "<code>index.as_query_engine()</code> 是快捷方式；<code>RetrieverQueryEngine.from_args(...)</code> 让你自由拼装。",
        "A <strong>QueryEngine</strong> assembles <strong>retriever + postprocessors + synthesizer</strong> behind one "
        "<code>.query()</code> call. <code>index.as_query_engine()</code> is the shortcut; "
        "<code>RetrieverQueryEngine.from_args(...)</code> lets you wire it by hand.",
    ))
    + d.flow([
        ("ret", L("检索器", "Retriever"), L("取 top-k", "fetch top-k")),
        ("pp", L("后处理器", "Postprocessors"), L("过滤 / 重排", "filter / rerank")),
        ("synth", L("合成器", "Synthesizer"), L("多片段→单答案", "many → one")),
        ("q", L(".query()", ".query()"), L("一个入口", "one entry")),
    ], active="q", caption=L(
        "QueryEngine = 把三个正交组件装配进一个 .query() 入口",
        "A QueryEngine wires three orthogonal components behind one .query() call",
    ))
    + c.analogy(L(
        "把“图书管理员（检索）+ 质检（后处理）+ 写手（合成）”组装成一个<strong>一键问答窗口</strong>。",
        "Bundle “librarian (retrieve) + QC (postprocess) + writer (synthesize)” into a single <strong>one-click Q&amp;A "
        "window</strong>.",
    ))
    + c.section(
        L("两种装配方式", "Two ways to assemble"),
        c.compare_table(
            [L("方式", "Way"), L("适合", "Good for")],
            [
                [L("<code>index.as_query_engine(...)</code>", "<code>index.as_query_engine(...)</code>"), L("快速、默认装配", "fast, default wiring")],
                [L("<code>RetrieverQueryEngine.from_args(...)</code>", "<code>RetrieverQueryEngine.from_args(...)</code>"), L("自定义检索器/后处理/合成器", "custom retriever/postproc/synth")],
            ],
        ),
    )
    + c.section(
        L("QueryEngine 是查询路径的组合根", "The QueryEngine is the query path's composition root"),
        L(
            "检索器、后处理器、合成器是三个<strong>正交</strong>的组件：换检索器不影响合成策略，加后处理器不影响检索。"
            "QueryEngine 只负责把它们装配起来、对外暴露一个 <code>.query()</code>。值得记住的是：<code>index.as_query_engine(...)</code> "
            "与 <code>RetrieverQueryEngine.from_args(...)</code> 产出的其实是<strong>同一种 QueryEngine</strong>，只是装配深度不同——"
            "前者用默认接线、一行起步，后者让你逐件指定检索器 / 后处理器 / 合成器。",
            "The retriever, postprocessors and synthesizer are three <strong>orthogonal</strong> components: swapping the "
            "retriever doesn't touch the synthesis strategy, and adding a postprocessor doesn't touch retrieval. The "
            "QueryEngine just wires them together behind one <code>.query()</code>. Worth remembering: "
            "<code>index.as_query_engine(...)</code> and <code>RetrieverQueryEngine.from_args(...)</code> yield the "
            "<strong>very same kind of QueryEngine</strong> — they differ only in wiring depth: the former starts in one "
            "line with default wiring, the latter lets you specify the retriever / postprocessors / synthesizer piece by piece.",
        ),
        d.vflow([
            (L("engine.query('…')", "engine.query('…')"), L("收到问题", "receives the question")),
            (L("retrieve()", "retrieve()"), L("→ top-k NodeWithScore", "→ top-k NodeWithScore")),
            (L("postprocess", "postprocess"), L("→ 过滤/重排后的 Node", "→ filtered/reranked Nodes")),
            (L("synthesize()", "synthesize()"), L("→ 交 LLM 据此作答", "→ LLM answers from them")),
            (L("Response", "Response"), L("answer + source_nodes", "answer + source_nodes")),
        ], caption=L("一次 query 的内部时序", "the internal timeline of a single query")),
    )
    + c.source_ref("query_engine/retriever_query_engine.py", "RetrieverQueryEngine.from_args", L("可定制的查询引擎装配", "customizable query-engine assembly"))
    + c.source_ref("base/base_query_engine.py", "BaseQueryEngine.query", L("查询路径的统一入口", "the unified query entry point"))
    + c.accordion(
        L("深入：查询引擎的装配", "Deep dive: assembling the query engine"),
        c.qa_item(
            L("🧪 示例：手装三件套", "🧪 Example: wire the three parts by hand"),
            L(
                "<code>RetrieverQueryEngine.from_args(retriever=…, node_postprocessors=[…], response_synthesizer=…)</code> "
                "让你逐件指定，组合出非默认的行为。",
                "<code>RetrieverQueryEngine.from_args(retriever=…, node_postprocessors=[…], response_synthesizer=…)</code> "
                "lets you specify each part to compose non-default behavior.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "组合根模式把“装配”与“组件”分离：组件各自演进，装配方式保持稳定，于是定制 RAG 不必重写每一站。",
                "The composition-root pattern separates “wiring” from “components”: components evolve on their own while "
                "the wiring stays stable, so customizing RAG never means rewriting every stop.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "<code>BaseQueryEngine.query()</code> 内部调 <code>_query()</code>，后者先 <code>retrieve()</code> 取 Node、"
                "过一遍后处理，再 <code>synthesize()</code> 生成 Response。",
                "<code>BaseQueryEngine.query()</code> calls <code>_query()</code>, which first <code>retrieve()</code>s "
                "Nodes, runs them through postprocessing, then <code>synthesize()</code>s the Response.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "那什么时候才真的需要 <code>from_args(...)</code>？当你要换非默认检索器（如 BM25 / 混合检索）、"
                "串联多个后处理器，或指定特定 ResponseMode 时——否则 <code>as_query_engine(...)</code> 的默认装配已经够用。",
                "So when do you actually reach for <code>from_args(...)</code>? When you need a non-default retriever "
                "(e.g. BM25 / hybrid), a chain of postprocessors, or a specific ResponseMode — otherwise the default "
                "wiring of <code>as_query_engine(...)</code> already suffices.",
            ),
        ),
    )
    + c.code(
        "from llama_index.core.query_engine import RetrieverQueryEngine\n"
        "from llama_index.core.postprocessor import SimilarityPostprocessor\n"
        "from llama_index.core import get_response_synthesizer\n\n"
        "# 手动拼装：检索器 + 后处理 + 合成器\n"
        "engine = RetrieverQueryEngine.from_args(\n"
        "    retriever=index.as_retriever(similarity_top_k=5),\n"
        "    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],\n"
        "    response_synthesizer=get_response_synthesizer(response_mode='compact'),\n"
        ")\n"
        "resp = engine.query('退款政策是什么？')\n"
        "print(resp, '\\n依据:', [n.node_id for n in resp.source_nodes])",
        caption=L("QueryEngine = 查询路径的“组合根”", "the QueryEngine is the query path's composition root"),
    )
    + c.code(
        "from llama_index.core import PromptTemplate\n\n"
        "qa = PromptTemplate(\n"
        "    '仅根据下面的资料回答；若资料不足就说不知道。\\n'\n"
        "    '资料：{context_str}\\n问题：{query_str}\\n答案：')\n\n"
        "# 一行定制：自定义 prompt + top_k（对照上面的 from_args 手装）\n"
        "engine = index.as_query_engine(text_qa_template=qa, similarity_top_k=4)\n"
        "print(engine.query('退款政策是什么？'))",
        caption=L("as_query_engine 一行定制：换 prompt 与 top_k，无需手装", "Customize in one line with as_query_engine: swap prompt and top_k, no hand-wiring"),
    )
    + c.key_points([
        L("QueryEngine 串起<strong>检索→后处理→合成</strong>，对外只暴露 <code>.query()</code>。",
          "A QueryEngine chains <strong>retrieve→postprocess→synthesize</strong>, exposing only <code>.query()</code>."),
        L("三件套可<strong>独立替换</strong>，组合出不同行为。",
          "Each of the three parts is <strong>independently swappable</strong>."),
        L("<code>response.source_nodes</code> 保留可溯源的依据。",
          "<code>response.source_nodes</code> keeps the traceable evidence."),
    ])
    + c.design_highlight(L(
        "QueryEngine 是查询路径的<strong>组合根</strong>：把三个正交组件组装起来。理解它，你就能把“默认问答”改造成任意 RAG 变体。",
        "The QueryEngine is the query path's <strong>composition root</strong>: it assembles three orthogonal "
        "components. Grasp it and you can reshape “default Q&amp;A” into any RAG variant.",
    ))
)
LESSON_16 = (
    c.pipeline("answer")
    + c.lead(L(
        "<strong>ChatEngine</strong> 在 QueryEngine 之上加<strong>多轮记忆</strong>。两种范式：<code>condense_question</code>"
        "（把对话历史压成一个独立问题再检索）和 <code>context</code>（每轮都检索并把片段注入上下文）。",
        "A <strong>ChatEngine</strong> adds <strong>multi-turn memory</strong> on top of a QueryEngine. Two paradigms: "
        "<code>condense_question</code> (condense the history into one standalone question, then retrieve) and "
        "<code>context</code> (retrieve every turn and inject the snippets into context).",
    ))
    + d.compare2(
        (L("condense_question", "condense_question"), i18n.render(L(
            "先把“对话历史 + 新问题”压成一个独立问题，再用它检索。指代先消解，检索更准。",
            "First condense “history + new question” into one standalone question, then retrieve with it. Coreference is "
            "resolved first, so retrieval is sharper.",
        ))),
        (L("context", "context"), i18n.render(L(
            "每一轮都直接检索，把命中的片段注入系统上下文，连同历史一起交给 LLM。",
            "Every turn retrieves directly and injects the hit snippets into the system context, handed to the LLM along "
            "with the history.",
        ))),
        caption=L("两种多轮范式：先压缩问题，还是每轮注入上下文", "Two multi-turn paradigms: condense the question first, or inject context each turn"),
    )
    + c.analogy(L(
        "QueryEngine 像<strong>一次性问答台</strong>；ChatEngine 像<strong>记得前文的客服</strong>，能听懂“那它的退款呢？”里的“它”。",
        "A QueryEngine is a <strong>one-shot help desk</strong>; a ChatEngine is a <strong>support agent who remembers "
        "the thread</strong> and understands what “it” refers to in “and its refund?”.",
    ))
    + c.section(
        L("三种聊天模式", "Three chat modes"),
        c.compare_table(
            [L("ChatMode", "ChatMode"), L("怎么处理多轮", "How it handles turns")],
            [
                [L("condense_question", "condense_question"), L("历史+新问 → 独立问题 → 检索", "history+new → standalone question → retrieve")],
                [L("context", "context"), L("每轮检索，片段注入系统上下文", "retrieve each turn, inject as context")],
                [L("condense_plus_context", "condense_plus_context"), L("先压缩问题，再检索注入（两者结合）", "condense then retrieve+inject (both)")],
            ],
        ),
    )
    + c.section(
        L("多轮的真正难点", "What's actually hard about multi-turn"),
        L(
            "多轮聊天不是给 QueryEngine 套个循环就行。难点有二：一是<strong>指代消解</strong>——“它 / 那 / 上面说的”"
            "要先还原成具体所指；二是<strong>用哪个问题去检索</strong>——是拿用户这轮的原话，还是拿指代消解后补全的独立问题？"
            "两种 ChatMode 正是这第二个问题的两种答案：<code>condense_question</code> 先把“历史 + 新问”压成一个独立问题、再用它检索；"
            "<code>context</code> 直接用原话每轮检索、把片段注入上下文。<strong>注意：两种模式都每轮检索</strong>——"
            "真正“要不要检索”的按需判断属于 Agent / Router 的范畴（见第 18 课）。",
            "Multi-turn chat is not just wrapping a loop around a QueryEngine. Two things are hard: "
            "<strong>coreference</strong> — “it / that / the one above” must be resolved to a concrete referent first; and "
            "<strong>which question to retrieve with</strong> — the user's raw words this turn, or the standalone question "
            "rebuilt after resolving the coreference? The two ChatModes are two answers to this second problem: "
            "<code>condense_question</code> first condenses “history + new question” into one standalone query, then "
            "retrieves with it; <code>context</code> retrieves every turn with the raw words and injects the snippets. "
            "<strong>Note: both modes retrieve on every turn</strong> — truly deciding <em>whether</em> to retrieve at all "
            "is agent / router behavior (Lesson 18).",
        ),
        d.flow([
            ("u", L("“那它呢？”", "“and its …?”"), L("含指代", "has a pronoun")),
            ("co", L("指代消解", "Coreference"), L("→ “国际订单的退款呢？”", "→ “refund for intl orders?”")),
            ("ret", L("检索", "Retrieve")),
            ("ans", L("作答", "Answer")),
            ("mem", L("写入记忆", "Update memory")),
        ], active="co", caption=L(
            "多轮的关键：先把“它 / 那”解析成具体所指，再检索作答，并记住本轮",
            "The crux of multi-turn: resolve “it / that” to a concrete referent, then retrieve, answer, and remember the turn",
        )),
    )
    + c.source_ref("chat_engine/condense_question.py", "CondenseQuestionChatEngine", L("压缩式多轮", "condense-style chat"))
    + c.source_ref("chat_engine/context.py", "ContextChatEngine", L("上下文注入式多轮", "context-injection chat"))
    + c.source_ref("chat_engine/types.py", "ChatMode", L("聊天模式枚举", "the chat-mode enum"))
    + c.accordion(
        L("深入：多轮 RAG 的机制", "Deep dive: the mechanics of multi-turn RAG"),
        c.qa_item(
            L("🧪 示例：连问两轮", "🧪 Example: two chained turns"),
            L(
                "<code>chat.chat('退款政策？')</code> 后再 <code>chat.chat('那国际订单呢？')</code>，引擎会用上一轮把“那”消解成"
                "“国际订单的退款”，再检索作答。",
                "After <code>chat.chat('refund policy?')</code>, a follow-up <code>chat.chat('and intl orders?')</code> "
                "uses the prior turn to resolve “and …” into “refund for intl orders,” then retrieves and answers.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "因为多轮的难点不在“记历史”，而在“理解依赖历史的新问题”。把指代消解与检索时机显式化，聊天才会稳。",
                "Because the hard part of multi-turn isn't “storing history,” it's “understanding a new question that "
                "depends on it.” Making coreference and retrieval-timing explicit is what makes chat robust.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "<code>CondenseQuestionChatEngine</code> 先用 LLM 把历史+新问压成独立问题再检索；"
                "<code>ContextChatEngine</code> 每轮检索并把片段塞进 system 提示。",
                "<code>CondenseQuestionChatEngine</code> first uses the LLM to condense history+question into a standalone "
                "query, then retrieves; <code>ContextChatEngine</code> retrieves each turn and stuffs the snippets into "
                "the system prompt.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "<code>condense_plus_context</code> 兼顾两者——先压缩问题、再检索注入，通用性最好，是大多数客服 / 问答助手的默认选择。",
                "<code>condense_plus_context</code> combines both — condense the question, then retrieve and inject — the "
                "most general option and the default for most support / Q&amp;A assistants.",
            ),
        ),
    )
    + c.code(
        "chat = index.as_chat_engine(chat_mode='condense_plus_context')\n"
        "print(chat.chat('你们的退款政策是什么？'))\n"
        "print(chat.chat('那国际订单也一样吗？'))   # ‘那/也’ 依赖上一轮，引擎会消解指代\n\n"
        "chat.reset()   # 清空多轮记忆",
        caption=L("多轮 RAG = 指代消解 + 每轮检索", "multi-turn RAG = coreference + retrieval each turn"),
    )
    + c.code(
        "from llama_index.core.chat_engine import ContextChatEngine\n"
        "from llama_index.core.memory import ChatMemoryBuffer\n\n"
        "memory = ChatMemoryBuffer.from_defaults(token_limit=3000)\n"
        "chat = ContextChatEngine.from_defaults(\n"
        "    retriever=index.as_retriever(similarity_top_k=3),\n"
        "    memory=memory,\n"
        "    system_prompt='你是一名严谨的客服，只依据检索到的资料回答。',\n"
        ")\n"
        "print(chat.chat('你们支持哪些支付方式？'))",
        caption=L("显式装配 ContextChatEngine：自带记忆与系统提示", "Wire ContextChatEngine explicitly: with its own memory and system prompt"),
    )
    + c.key_points([
        L("ChatEngine = QueryEngine + <strong>记忆</strong>，支持指代消解的多轮问答。",
          "ChatEngine = QueryEngine + <strong>memory</strong>, enabling coreference-aware multi-turn Q&amp;A."),
        L("<code>condense_question</code> 重写问题；<code>context</code> 每轮注入检索片段。",
          "<code>condense_question</code> rewrites the question; <code>context</code> injects retrieved snippets each turn."),
        L("<code>condense_plus_context</code> 兼顾两者，通用性最好。",
          "<code>condense_plus_context</code> combines both and is the most general."),
    ])
    + c.design_highlight(L(
        "多轮 RAG 的真正难点是<strong>指代消解</strong>，以及<strong>用哪个问题去检索</strong>——用原话，还是用消解后补全的独立问题。"
        "两种 mode 给出两种答案（且都每轮检索）——这也是为什么聊天不只是“给 QueryEngine 套个循环”。",
        "The real challenge of multi-turn RAG is <strong>coreference</strong> and <strong>which question to retrieve "
        "with</strong> — the raw words, or the standalone question rebuilt after resolving it. The two modes give two "
        "answers (both retrieving every turn) — which is why chat is more than “wrap a loop around a QueryEngine.”",
    ))
)
