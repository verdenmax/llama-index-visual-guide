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
    "06-node-parsers.html": {
        "mcq": [
            {
                "q": L("<code>chunk_overlap</code> 的主要作用是？", "What is the main purpose of <code>chunk_overlap</code>?"),
                "opts": [
                    L("让每个块更大", "Make each chunk bigger"),
                    L("相邻块重叠几句，避免语义在边界被切断", "Overlap adjacent chunks by a few sentences so meaning isn't cut at the boundary"),
                    L("加快向量化", "Speed up embedding"),
                    L("对块去重", "Deduplicate chunks"),
                ],
                "answer": 1,
                "why": L("重叠让跨越块边界的句子/语义不丢失，提升检索召回。",
                         "Overlap keeps sentences/meaning that straddle a boundary from being lost, improving recall."),
            },
        ],
        "open": [
            L("你的文档是 API 手册 vs 小说，chunk_size 该偏大还是偏小？为什么？",
              "For an API manual vs a novel, should chunk_size lean larger or smaller? Why?"),
        ],
    },
    "07-metadata-extractors.html": {
        "mcq": [
            {
                "q": L("给 Node 加 metadata 的主要价值是？", "What's the main value of adding metadata to Nodes?"),
                "opts": [
                    L("减少存储占用", "Reduce storage"),
                    L("增强检索与过滤（向量相似之外的第二通道）", "Strengthen retrieval & filtering (a second channel beyond vector similarity)"),
                    L("加快 LLM 生成", "Speed up the LLM"),
                    L("替代 embedding", "Replace embeddings"),
                ],
                "answer": 1,
                "why": L("元数据支持按来源/标签过滤，并让问题与片段更易匹配，与向量相似互补。",
                         "Metadata enables filtering by source/tag and better question-to-chunk matching, complementing vector similarity."),
            },
        ],
    },
    "08-embeddings.html": {
        "mcq": [
            {
                "q": L("为什么向量检索能匹配“同义不同词”的内容？",
                       "Why can vector search match content that's synonymous but uses different words?"),
                "opts": [
                    L("因为做了关键词扩展", "Because it does keyword expansion"),
                    L("因为 embedding 把语义相近映射成向量距离近", "Because embeddings map semantic closeness to vector closeness"),
                    L("因为用了更大的模型", "Because it uses a bigger model"),
                    L("因为大小写不敏感", "Because it's case-insensitive"),
                ],
                "answer": 1,
                "why": L("语义相近的文本向量距离也近，所以即使用词不同也能被召回。",
                         "Semantically similar text has nearby vectors, so it's recalled even with different wording."),
            },
        ],
    },
    "09-vector-stores.html": {
        "mcq": [
            {
                "q": L("从内存版 SimpleVectorStore 换成 Chroma，主要需要改什么？",
                       "To switch from the in-memory SimpleVectorStore to Chroma, what mainly changes?"),
                "opts": [
                    L("重写切块与检索逻辑", "Rewrite the chunking and retrieval logic"),
                    L("只需通过 StorageContext 注入新的向量库", "Just inject the new store via StorageContext"),
                    L("必须更换 embedding 模型", "You must change the embedding model"),
                    L("重新训练模型", "Retrain the model"),
                ],
                "answer": 1,
                "why": L("VectorStore 接口统一，换实现只改注入这一步，主链路不动。",
                         "The VectorStore interface is uniform; swapping implementations only changes the injection — the pipeline stays."),
            },
        ],
    },
    "10-index-abstraction.html": {
        "mcq": [
            {
                "q": L("要对整个语料做一次全面总结，最贴合的索引是？",
                       "To produce one comprehensive summary of a whole corpus, which index fits best?"),
                "opts": [
                    L("VectorStoreIndex（top-k 近邻）", "VectorStoreIndex (top-k nearest neighbors)"),
                    L("SummaryIndex（遍历所有 Node）", "SummaryIndex (iterates over all Nodes)"),
                    L("关键词匹配", "Keyword matching"),
                    L("换一个更大的模型", "Switch to a bigger model"),
                ],
                "answer": 1,
                "why": L("总结需要覆盖全部内容，SummaryIndex 遍历所有 Node，而 VectorStoreIndex 只取 top-k。",
                         "Summarizing must cover everything; SummaryIndex iterates all Nodes, whereas VectorStoreIndex only takes top-k."),
            },
        ],
        "open": [
            L("FAQ 问答 vs 合同全文摘要，分别该选哪种 Index？为什么？",
              "FAQ Q&A vs summarizing a full contract — which index would you pick for each, and why?"),
        ],
    },
    "11-ingestion-storage.html": {
        "mcq": [
            {
                "q": L("文档每天小幅更新，如何避免每次全量重建索引？",
                       "Documents change a little every day — how do you avoid fully rebuilding the index each time?"),
                "opts": [
                    L("换更快的机器", "Use a faster machine"),
                    L("用 IngestionPipeline 的缓存 + docstore 去重做增量", "Use IngestionPipeline's cache + docstore dedup for incremental updates"),
                    L("关掉切块", "Turn off chunking"),
                    L("改用关键词检索", "Switch to keyword search"),
                ],
                "answer": 1,
                "why": L("缓存让相同输入不重复计算，docstore 去重让只处理新增/变化的文档。",
                         "The cache skips recomputing identical inputs, and docstore dedup processes only new/changed documents."),
            },
        ],
    },
    "12-retrievers.html": {
        "mcq": [
            {
                "q": L("调用 <code>retriever.retrieve(q)</code> 之后，得到的是？",
                       "After calling <code>retriever.retrieve(q)</code>, what do you get?"),
                "opts": [
                    L("最终的自然语言答案", "the final natural-language answer"),
                    L("top-k 个带相似度分数的 Node（NodeWithScore）", "the top-k scored Nodes (NodeWithScore)"),
                    L("一个新的索引", "a new index"),
                    L("向量的维度", "the vector dimension"),
                ],
                "answer": 1,
                "why": L("检索阶段只取回相关 Node（NodeWithScore）；生成答案是后面响应合成器的事。",
                         "Retrieval only fetches relevant Nodes (NodeWithScore); producing the answer is the synthesizer's job later."),
            },
        ],
    },
    "13-postprocessors.html": {
        "mcq": [
            {
                "q": L("<code>SimilarityPostprocessor(similarity_cutoff=0.7)</code> 的作用是？",
                       "What does <code>SimilarityPostprocessor(similarity_cutoff=0.7)</code> do?"),
                "opts": [
                    L("把所有分数提高到 0.7", "Raise every score to 0.7"),
                    L("丢弃相似度低于 0.7 的 Node", "Drop Nodes with similarity below 0.7"),
                    L("只取前 0.7 个 Node", "Keep only the first 0.7 Nodes"),
                    L("重新向量化", "Re-embed everything"),
                ],
                "answer": 1,
                "why": L("它按阈值过滤掉低相关 Node，减少噪声进入生成阶段。",
                         "It filters out low-relevance Nodes by threshold, reducing noise before generation."),
            },
        ],
    },
    "14-response-synthesizers.html": {
        "mcq": [
            {
                "q": L("片段很多、又想要一个全局总结，最贴合的 ResponseMode 是？",
                       "Many chunks, and you want one global summary — which ResponseMode fits best?"),
                "opts": [
                    L("compact", "compact"),
                    L("tree_summarize", "tree_summarize"),
                    L("generation", "generation"),
                    L("accumulate", "accumulate"),
                ],
                "answer": 1,
                "why": L("tree_summarize 分组逐层总结再合并，天然适合覆盖大量片段的总结型问题。",
                         "tree_summarize summarizes in groups and merges upward — ideal for summary questions over many chunks."),
            },
        ],
        "open": [
            L("上下文窗口很小但片段很多时，refine 和 compact 各有什么代价？",
              "With a small context window but many chunks, what are the costs of refine vs compact?"),
        ],
    },
    "15-query-engine.html": {
        "mcq": [
            {
                "q": L("RetrieverQueryEngine 把哪三件套组合在一起？",
                       "Which three pieces does RetrieverQueryEngine assemble?"),
                "opts": [
                    L("加载器 / 切块器 / 向量化", "loader / splitter / embedding"),
                    L("检索器 / 节点后处理 / 响应合成器", "retriever / node postprocessors / response synthesizer"),
                    L("LLM / Embedding / 向量库", "LLM / embedding / vector store"),
                    L("三种不同的 Index", "three kinds of Index"),
                ],
                "answer": 1,
                "why": L("QueryEngine 是查询路径的组合根：把 retriever + node_postprocessors + response_synthesizer 串成一个 .query()。",
                         "The QueryEngine is the query path's composition root: it chains retriever + node_postprocessors + response_synthesizer behind one .query()."),
            },
        ],
    },
    "16-chat-engine.html": {
        "mcq": [
            {
                "q": L("多轮对话里用户问“那它呢？”，<code>condense_question</code> 模式怎么处理？",
                       "In a multi-turn chat the user asks “and what about it?” — how does <code>condense_question</code> mode handle it?"),
                "opts": [
                    L("直接拿“那它呢”去检索", "Retrieve directly with “and what about it?”"),
                    L("先把对话历史+新问压成一个独立完整问题，再检索", "First condense history + new question into one standalone question, then retrieve"),
                    L("忽略对话历史", "Ignore the chat history"),
                    L("只用关键词匹配", "Use keyword matching only"),
                ],
                "answer": 1,
                "why": L("condense 模式先把指代消解成一个独立问题，确保检索到正确片段。",
                         "Condense mode resolves the reference into a standalone question first, so retrieval finds the right chunks."),
            },
        ],
    },
    "17-settings-prompts.html": {
        "mcq": [
            {
                "q": L("新版 LlamaIndex 中，<code>Settings</code> 取代了什么？",
                       "In recent LlamaIndex, what did <code>Settings</code> replace?"),
                "opts": [
                    L("VectorStore", "the VectorStore"),
                    L("ServiceContext（旧的全局配置）", "ServiceContext (the old global config)"),
                    L("Retriever", "the Retriever"),
                    L("Document", "the Document"),
                ],
                "answer": 1,
                "why": L("Settings 是全局默认配置单例，取代了过去到处传递的 ServiceContext。",
                         "Settings is the global default-config singleton that replaced the old, widely-passed ServiceContext."),
            },
        ],
    },
    "18-advanced-retrieval.html": {
        "mcq": [
            {
                "q": L("为什么进阶检索器能直接替换基础检索器、塞进原来的 QueryEngine？",
                       "Why can advanced retrievers drop into an existing QueryEngine in place of the basic one?"),
                "opts": [
                    L("因为它们更快", "Because they're faster"),
                    L("因为它们都实现同一个 BaseRetriever 接口", "Because they all implement the same BaseRetriever interface"),
                    L("因为它们不用 embedding", "Because they skip embeddings"),
                    L("因为它们是 core 内置的", "Because they're built into core"),
                ],
                "answer": 1,
                "why": L("统一的 BaseRetriever 接口让检索策略可插拔，QueryEngine 不感知具体实现。",
                         "The uniform BaseRetriever interface makes retrieval strategies pluggable; the QueryEngine doesn't care which one."),
            },
        ],
    },
    "19-evaluation.html": {
        "mcq": [
            {
                "q": L("<code>FaithfulnessEvaluator</code> 主要检查什么？",
                       "What does <code>FaithfulnessEvaluator</code> mainly check?"),
                "opts": [
                    L("答案的语法是否正确", "Whether the answer's grammar is correct"),
                    L("答案是否被检索到的上下文支撑（防幻觉）", "Whether the answer is supported by the retrieved context (anti-hallucination)"),
                    L("检索速度", "Retrieval speed"),
                    L("向量维度", "Vector dimension"),
                ],
                "answer": 1,
                "why": L("忠实度衡量答案是否有据可依，是 RAG 防幻觉的核心指标。",
                         "Faithfulness measures whether the answer is grounded in the context — the core anti-hallucination metric."),
            },
        ],
        "open": [
            L("你会如何搭一个最小的回归评估集，防止改动让 RAG 变差？",
              "How would you build a minimal regression eval set to keep changes from degrading the RAG?"),
        ],
    },
    "20-capstone.html": {
        "open": [
            L("把这套 capstone 改造成“带引用脚注的客服机器人”，你会替换或新增哪些组件？",
              "To turn this capstone into a “support bot with cited footnotes”, which components would you swap or add?"),
            L("如果知识库有上百万文档，写入路径与查询路径各自最先遇到的瓶颈是什么？",
              "With millions of documents, what's the first bottleneck on the write path vs the query path?"),
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
