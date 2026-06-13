"""Part 1 (macro overview): lessons 01-03. Content filled task-by-task."""
import components as c
from i18n import L


def _stub():
    return c.pipeline(None) + c.lead(L("（本课内容建设中）", "(Lesson content coming soon)"))


LESSON_01 = (
    c.pipeline(None)
    + c.lead(L(
        "<strong>LlamaIndex</strong> 是一个把<strong>检索增强生成（RAG）</strong>这条数据管道"
        "标准化、可编排的框架。它不训练模型，只负责模型<strong>周边的全部管道</strong>："
        "把你的数据加载、切块、向量化、建索引，再在提问时检索相关片段、喂给 LLM 生成<strong>有依据</strong>的回答。",
        "<strong>LlamaIndex</strong> is a framework that standardizes and orchestrates the "
        "<strong>Retrieval-Augmented Generation (RAG)</strong> pipeline. It doesn't train models — it owns "
        "everything <em>around</em> them: loading, chunking, embedding and indexing your data, then at query "
        "time retrieving the relevant pieces and feeding them to the LLM for a <strong>grounded</strong> answer.",
    ))
    + c.analogy(L(
        "把 LLM 想成一个聪明但在<strong>闭卷</strong>考试的学生：只能凭记忆答题，记不住就开始编。"
        "RAG 让它<strong>开卷</strong>——先翻到相关页（检索），再据此作答（生成）。"
        "LlamaIndex 就是帮你建好这座图书馆和索书系统的工具。",
        "Picture an LLM as a smart student in a <strong>closed-book</strong> exam: it answers from memory and "
        "invents things it can't recall. RAG makes it <strong>open-book</strong> — find the relevant pages first "
        "(retrieve), then answer from them (generate). LlamaIndex builds that library and its call-number system.",
    ))
    + c.section(
        L("RAG 解决什么问题？", "What problem does RAG solve?"),
        c.compare_table(
            [L("痛点", "Pain point"), L("只用 LLM", "LLM alone"), L("用 RAG", "With RAG")],
            [
                [L("知识截止", "Knowledge cutoff"), L("训练后的新知识一概不知", "Blind to anything after training"),
                 L("先检索实时/私有资料再答", "Retrieves fresh/private data first")],
                [L("幻觉", "Hallucination"), L("不确定也答得很自信", "Confidently makes things up"),
                 L("答案有检索到的出处支撑", "Answers grounded in retrieved sources")],
                [L("私有数据", "Private data"), L("没见过你的文档", "Never saw your documents"),
                 L("把你的文档建成可检索索引", "Indexes your docs for retrieval")],
            ],
        ),
    )
    + c.source_ref(
        "llama_index/core/__init__.py", "VectorStoreIndex · SimpleDirectoryReader",
        L("RAG 的高层入口都从这里导出", "the high-level RAG entry points are exported here"),
    )
    + c.code(
        "pip install llama-index\n\n"
        "from llama_index.core import VectorStoreIndex, SimpleDirectoryReader\n\n"
        "# 写入路径：加载 -&gt; 切块 -&gt; 向量化 -&gt; 建索引（一行搞定）\n"
        "docs = SimpleDirectoryReader('./data').load_data()\n"
        "index = VectorStoreIndex.from_documents(docs)\n\n"
        "# 查询路径：检索 -&gt; 合成 -&gt; 有依据的回答\n"
        "engine = index.as_query_engine()\n"
        "print(engine.query('这些文档讲了什么？'))",
        caption=L("最小可运行 RAG：5 行", "A minimal runnable RAG in 5 lines"),
    )
    + c.key_points([
        L("RAG = 先<strong>检索</strong>相关片段，再让 LLM 据此<strong>生成</strong>，避免重训与幻觉。",
          "RAG = <strong>retrieve</strong> relevant snippets, then <strong>generate</strong> from them — no "
          "retraining, fewer hallucinations."),
        L("LlamaIndex 负责 RAG 的<strong>数据与编排</strong>，不做训练或推理本身。",
          "LlamaIndex owns the <strong>data + orchestration</strong> of RAG, not training or inference."),
        L("两条主线贯穿全书：<strong>写入路径</strong>（建索引）与<strong>查询路径</strong>（问答）。",
          "Two through-lines: the <strong>write path</strong> (build the index) and the <strong>query path</strong> (ask)."),
    ])
    + c.design_highlight(L(
        "RAG 的精妙在于把模型的“记忆”<strong>外置</strong>为一个可随时更新、可检索的索引——"
        "更新知识只需重建索引，模型本身原封不动。",
        "RAG's elegance: it <strong>externalizes</strong> the model's “memory” into a searchable index you can "
        "refresh anytime — update knowledge by rebuilding the index, never touching the model.",
    ))
)
LESSON_02 = _stub()
LESSON_03 = _stub()
