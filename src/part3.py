"""Part 3 (query path): lessons 12-16. Content filled task-by-task."""
import components as c
from i18n import L


def _stub():
    return c.pipeline(None) + c.lead(L("（本课内容建设中）", "(Lesson content coming soon)"))


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
LESSON_14 = _stub()
LESSON_15 = _stub()
LESSON_16 = _stub()
