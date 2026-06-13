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
LESSON_13 = _stub()
LESSON_14 = _stub()
LESSON_15 = _stub()
LESSON_16 = _stub()
