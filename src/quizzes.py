"""Per-lesson self-test (自测题): bilingual multiple-choice + open prompts.

Questions probe *why a thing is designed the way it is*, not rote syntax.
Content lives here as data (``L`` for bilingual text) keyed by filename;
``render(fname)`` turns it into HTML appended to each lesson by build.py /
build_print.py. Options are deterministically shuffled so the correct answer
isn't always first. No third-party dependencies.

Schema per lesson (used by every content task that extends ``QUIZZES``)::

    "NN-file.html": {
        "mcq": [
            {
                "q": L("问题", "question"),
                "opts": [L("选项A", "option A"), L("选项B", "option B"), ...],
                "answer": 1,            # 0-based index into ``opts`` AS WRITTEN
                "why": L("解析", "explanation"),
            },
            ...
        ],
        "open": [L("发散题", "open prompt"), ...],   # optional
    }

``answer`` is the 0-based index of the correct option *as listed above*, before
``_shuffle`` reorders them at render time. ``mcq``, ``open`` and ``why`` are all
optional. Wrap inline code in ``<code>…</code>`` and escape any literal ``<`` /
``&`` inside ``L`` strings (the text is emitted as raw HTML).
"""

import hashlib

import i18n
from i18n import L


def _shuffle(opts, answer, seed):
    """Deterministically permute ``opts`` (stable across builds) and return
    ``(new_opts, new_answer_index)`` so the correct option lands in a varied
    position instead of always first. ``answer`` is the index into ``opts`` as
    passed in; the returned index points at the same option after shuffling."""
    order = sorted(
        range(len(opts)),
        key=lambda i: hashlib.md5(f"{seed}:{i}".encode("utf-8")).hexdigest(),
    )
    return [opts[i] for i in order], order.index(answer)


QUIZZES = {
    "01-what-is-llamaindex.html": {
        "mcq": [
            {
                "q": L("RAG（检索增强生成）的核心思想是？", "What is the core idea of RAG?"),
                "opts": [
                    L("重新训练模型以记住新知识", "Retrain the model to memorize new knowledge"),
                    L("回答前先检索相关外部片段、塞进上下文再生成",
                      "Retrieve relevant external snippets first, put them in context, then generate"),
                    L("把全部数据塞进一个超大提示词", "Stuff all data into one giant prompt"),
                    L("换一个更大的模型", "Switch to a bigger model"),
                ],
                "answer": 1,
                "why": L(
                    "RAG = 先检索后生成：用检索到的相关片段作为上下文，让模型据此回答，避免重训成本与知识幻觉。",
                    "RAG retrieves first, then generates: relevant snippets become context so the model answers "
                    "from them, avoiding retraining cost and hallucination.",
                ),
            },
            {
                "q": L("LlamaIndex 在 RAG 里主要负责什么？", "What does LlamaIndex mainly provide for RAG?"),
                "opts": [
                    L("训练 embedding 模型", "Training embedding models"),
                    L("把加载→切块→索引→检索→合成这条管道标准化、可编排",
                      "Standardizing and orchestrating the load→split→index→retrieve→synthesize pipeline"),
                    L("托管一个向量数据库服务", "Hosting a vector database service"),
                    L("提供 GPU 推理", "Providing GPU inference"),
                ],
                "answer": 1,
                "why": L(
                    "LlamaIndex 是 RAG 的“数据与编排框架”：统一各阶段接口，底层换 LLM / 向量库 / embedding 都不改主链路。",
                    "LlamaIndex is the data + orchestration framework for RAG: it unifies each stage so swapping the "
                    "LLM / vector store / embedding doesn't change the main pipeline.",
                ),
            },
        ],
        "open": [
            L("如果你的文档每天都在更新，你会如何设计“增量重新索引”的策略？",
              "If your documents change daily, how would you design an incremental re-indexing strategy?"),
        ],
    },
    "02-architecture.html": {
        "mcq": [
            {
                "q": L("看到 <code>from llama_index.vector_stores.chroma import ...</code>，你能立刻判断什么？",
                       "Seeing <code>from llama_index.vector_stores.chroma import ...</code>, what do you instantly know?"),
                "opts": [
                    L("这是 core 的稳定抽象", "It's a stable core abstraction"),
                    L("这是一个第三方集成实现（路径不含 core）", "It's a third-party integration (path has no core)"),
                    L("Chroma 是 LlamaIndex 官方维护的", "Chroma is maintained by LlamaIndex itself"),
                    L("必须先 import core 才能用它", "You must import core before it works"),
                ],
                "answer": 1,
                "why": L("命名约定：路径不含 <code>core</code> 即为具体集成实现；core 只定义接口。",
                         "By convention, a path without <code>core</code> is a concrete integration; core only defines interfaces."),
            },
        ],
    },
    "03-rag-lifecycle.html": {
        "mcq": [
            {
                "q": L("<code>VectorStoreIndex.from_documents(docs)</code> 一行其实做了哪些事？",
                       "What does the single line <code>VectorStoreIndex.from_documents(docs)</code> actually do?"),
                "opts": [
                    L("只是把文档存成文件", "Just saves the documents to disk"),
                    L("切块 → 向量化 → 存入索引（写入路径三步合一）",
                      "Split → embed → store (three write-path steps in one)"),
                    L("立刻向 LLM 提问", "Immediately queries the LLM"),
                    L("训练一个新的 embedding 模型", "Trains a new embedding model"),
                ],
                "answer": 1,
                "why": L("它是写入路径的快捷方式：内部依次切块、调用 embed_model 向量化、写入向量索引。",
                         "It's the write-path shortcut: internally it chunks, embeds via embed_model, and writes vectors into the index."),
            },
        ],
        "open": [
            L("如果同一个索引要服务上千次提问，你会把哪一步的结果缓存或持久化？为什么？",
              "If one index serves thousands of queries, which step's output would you cache or persist, and why?"),
        ],
    },
    "04-documents-nodes.html": {
        "mcq": [
            {
                "q": L("RAG 中真正被检索、并喂给 LLM 的最小单位是？",
                       "In RAG, what is the smallest unit that actually gets retrieved and fed to the LLM?"),
                "opts": [
                    L("整篇 Document", "the whole Document"),
                    L("Node（切块后带元数据的片段）", "a Node (a chunked, metadata-bearing piece)"),
                    L("原始文件", "the raw file"),
                    L("向量本身", "the vector itself"),
                ],
                "answer": 1,
                "why": L("Document 会被切成 Node；检索、返回的 source_nodes、以及响应合成都以 Node 为单位。",
                         "A Document is split into Nodes; retrieval, the returned source_nodes, and synthesis all operate on Nodes."),
            },
        ],
    },
    "05-readers.html": {
        "mcq": [
            {
                "q": L("<code>SimpleDirectoryReader(...).load_data()</code> 的产出是什么？",
                       "What does <code>SimpleDirectoryReader(...).load_data()</code> produce?"),
                "opts": [
                    L("直接的向量", "vectors directly"),
                    L("Document 列表", "a list of Documents"),
                    L("已切好的 Node", "ready-made Nodes"),
                    L("一个索引", "an index"),
                ],
                "answer": 1,
                "why": L("Reader 只负责把来源加载成 Document；切块、向量化、建索引都是后续阶段。",
                         "A Reader only loads sources into Documents; chunking, embedding and indexing are later stages."),
            },
        ],
    },
}


def render(fname):
    data = QUIZZES.get(fname)
    if not data:
        return ""
    head = i18n.t("🧪 自测 · 想一想为什么这么设计", "🧪 Self-check · think about the design")
    out = ['<div class="selftest">', f"<h2>{head}</h2>"]
    for i, item in enumerate(data.get("mcq", []), 1):
        shuffled, ans = _shuffle(item["opts"], item["answer"], f"{fname}:{i}")
        opts = "\n".join(f"    <li>{i18n.render(o, block=False)}</li>" for o in shuffled)
        letter = chr(65 + ans)
        reveal = i18n.t("看答案与解析", "Show answer & explanation")
        hint = i18n.t("点击展开", "expand")
        ans_label = i18n.t(f"答案：{letter}", f"Answer: {letter}")
        out.append(
            f'<div class="quiz">\n'
            f'  <div class="qn">{i}. {i18n.render(item["q"], block=False)}</div>\n'
            f'  <ol class="opts">\n{opts}\n  </ol>\n'
            f'  <details class="accordion">\n'
            f'    <summary>{reveal} <span class="hint">{hint}</span></summary>\n'
            f'    <div class="acc-body"><div class="qa"><div class="a">'
            f'<strong>{ans_label}</strong> {i18n.render(item.get("why", ""), block=False)}'
            f"</div></div></div>\n"
            f"  </details>\n"
            f"</div>"
        )
    opens = data.get("open", [])
    if opens:
        spark = i18n.t("💭 发散思考（没有标准答案）", "💭 Open questions (no single right answer)")
        lis = "\n".join(f"    <li>{i18n.render(o, block=False)}</li>" for o in opens)
        out.append(
            f'<div class="card spark">\n  <div class="tag">{spark}</div>\n  <ul>\n{lis}\n  </ul>\n</div>'
        )
    out.append("</div>")
    return "\n".join(out)
