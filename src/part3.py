"""Part 3 (query path): lessons 12-16. Content filled task-by-task."""
import components as c
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
    + c.source_ref("indices/vector_store/retrievers/retriever.py", "VectorIndexRetriever", L("向量索引的检索器", "the vector-index retriever"))
    + c.source_ref("base/base_retriever.py", "BaseRetriever.retrieve", L("所有检索器的统一入口", "the unified entry point every retriever shares"))
    + c.code(
        "retriever = index.as_retriever(similarity_top_k=3)\n"
        "nodes = retriever.retrieve('退款政策是什么？')   # List[NodeWithScore]\n"
        "for n in nodes:\n"
        "    print(round(n.score, 3), n.node.text[:50])\n"
        "# 注意：此处只检索，尚未生成答案",
        caption=L("检索独立于生成，可单独评估", "retrieval is separate from generation — evaluate it alone"),
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
    + c.source_ref("postprocessor/node.py", "SimilarityPostprocessor", L("相似度阈值过滤", "similarity-threshold filtering"))
    + c.source_ref("postprocessor/metadata_replacement.py", "MetadataReplacementPostProcessor", L("配合句窗切块还原上下文", "restores context for sentence-window chunks"))
    + c.code(
        "from llama_index.core.postprocessor import SimilarityPostprocessor\n\n"
        "nodes = index.as_retriever(similarity_top_k=5).retrieve('退款政策？')\n"
        "pp = SimilarityPostprocessor(similarity_cutoff=0.7)\n"
        "kept = pp.postprocess_nodes(nodes)   # 丢掉分数低于 0.7 的\n"
        "print(len(nodes), '->', len(kept))\n\n"
        "# 句窗专用：把单句节点替换为其上下文窗口\n"
        "from llama_index.core.postprocessor import MetadataReplacementPostProcessor\n"
        "mr = MetadataReplacementPostProcessor(target_metadata_key='window')",
        caption=L("检索与生成之间的“质检站”", "a QC station between retrieval and generation"),
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
            [L("模式", "Mode"), L("怎么合成", "How it synthesizes"), L("适合", "Good for")],
            [
                [L("compact（默认）", "compact (default)"), L("尽量塞满上下文再生成", "pack context, then generate"), L("通用、省调用", "general, fewer calls")],
                [L("refine", "refine"), L("逐个片段迭代精炼答案", "iteratively refine over chunks"), L("片段多、需细读", "many chunks, careful reading")],
                [L("tree_summarize", "tree_summarize"), L("两两/分组总结向上合并", "summarize in a tree"), L("总结类问题", "summary questions")],
                [L("accumulate", "accumulate"), L("每片段各自作答再汇总", "answer per chunk, then collect"), L("逐条抽取", "per-chunk extraction")],
            ],
        ),
    )
    + c.source_ref("response_synthesizers/factory.py", "get_response_synthesizer", L("按 ResponseMode 造合成器", "builds a synthesizer for a ResponseMode"))
    + c.source_ref("response_synthesizers/type.py", "ResponseMode", L("所有合成策略的枚举", "the enum of synthesis strategies"))
    + c.code(
        "from llama_index.core import get_response_synthesizer\n\n"
        "# 方式一：直接在 query engine 上选模式\n"
        "engine = index.as_query_engine(response_mode='tree_summarize')\n"
        "print(engine.query('把这些文档总结成 3 点'))\n\n"
        "# 方式二：显式造一个合成器（便于自定义装配，见下一课）\n"
        "synth = get_response_synthesizer(response_mode='compact')",
        caption=L("选 mode = 选“多片段→单答案”的策略", "choosing a mode = choosing the many→one strategy"),
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
    + c.source_ref("query_engine/retriever_query_engine.py", "RetrieverQueryEngine.from_args", L("可定制的查询引擎装配", "customizable query-engine assembly"))
    + c.source_ref("base/base_query_engine.py", "BaseQueryEngine.query", L("查询路径的统一入口", "the unified query entry point"))
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
    + c.source_ref("chat_engine/condense_question.py", "CondenseQuestionChatEngine", L("压缩式多轮", "condense-style chat"))
    + c.source_ref("chat_engine/context.py", "ContextChatEngine", L("上下文注入式多轮", "context-injection chat"))
    + c.source_ref("chat_engine/types.py", "ChatMode", L("聊天模式枚举", "the chat-mode enum"))
    + c.code(
        "chat = index.as_chat_engine(chat_mode='condense_plus_context')\n"
        "print(chat.chat('你们的退款政策是什么？'))\n"
        "print(chat.chat('那国际订单也一样吗？'))   # ‘那/也’ 依赖上一轮，引擎会消解指代\n\n"
        "chat.reset()   # 清空多轮记忆",
        caption=L("多轮 RAG = 指代消解 + 每轮检索", "multi-turn RAG = coreference + retrieval each turn"),
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
        "多轮 RAG 的真正难点是“<strong>指代消解 + 何时检索</strong>”。两种 mode 是两种解法——这也是为什么聊天不只是“给 QueryEngine 套个循环”。",
        "The real challenge of multi-turn RAG is “<strong>coreference + when to retrieve</strong>.” The two modes are two "
        "answers — which is why chat is more than “wrap a loop around a QueryEngine.”",
    ))
)
