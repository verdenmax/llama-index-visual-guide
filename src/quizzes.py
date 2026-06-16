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
import interviews as _iv
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
        "open": [
            L("把接口放在 core、实现放在集成包，这种分层在什么情况下反而会成为负担？",
              "Putting interfaces in core and implementations in integrations — when might this layering become a burden rather than a benefit?"),
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
        "open": [
            L("如果检索单位从 Node 改回整篇 Document，RAG 的哪些环节会变好、哪些会变差？",
              "If the unit of retrieval went back from Node to the whole Document, which parts of RAG would improve and which would suffer?"),
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
        "open": [
            L("一个 PDF 通常每页产出一个 Document，这会如何影响你后续的切块大小与“引用到第几页”的设计？",
              "A PDF usually yields one Document per page — how does that shape your downstream chunk size and page-level citation design?"),
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
                    L("增强检索与过滤（向量相似之外的第二通道）", "Strengthen retrieval &amp; filtering (a second channel beyond vector similarity)"),
                    L("加快 LLM 生成", "Speed up the LLM"),
                    L("替代 embedding", "Replace embeddings"),
                ],
                "answer": 1,
                "why": L("元数据支持按来源/标签过滤，并让问题与片段更易匹配，与向量相似互补。",
                         "Metadata enables filtering by source/tag and better question-to-chunk matching, complementing vector similarity."),
            },
        ],
        "open": [
            L("LLM 抽取元数据要花钱花时间。对你的语料，哪些元数据值得用 LLM 抽，哪些直接在 Reader 阶段手写就够？",
              "LLM metadata extraction costs time and money. For your corpus, which metadata is worth an LLM, and which is fine to hand-write at the Reader stage?"),
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
        "open": [
            L("如果上线后想换一个更好的 embedding 模型，需要付出什么代价？这对“多久重建一次索引”有什么启示？",
              "If you wanted a better embedding model after launch, what's the cost — and what does that imply about how often you rebuild the index?"),
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
        "open": [
            L("从内存版 SimpleVectorStore 迁到生产向量库，你会用哪些标准来选（规模、过滤、事务、运维）？",
              "Moving from the in-memory SimpleVectorStore to a production vector DB, what criteria would you choose by (scale, filtering, transactions, ops)?"),
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
              "FAQ Q&amp;A vs summarizing a full contract — which index would you pick for each, and why?"),
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
        "open": [
            L("如果知识库每天只变动 1%，“每次全量重建”与“增量摄取”在成本和复杂度上如何取舍？",
              "If your knowledge base changes 1% a day, how do you trade off 'full rebuild each time' vs 'incremental ingestion' in cost and complexity?"),
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
        "open": [
            L("如果检索分数普遍偏低，你会先调 top_k、换 embedding，还是改切块？怎么判断是哪一环的问题？",
              "If retrieval scores are uniformly low, would you tune top_k, swap the embedding, or re-chunk first — and how would you tell which stage is at fault?"),
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
        "open": [
            L("相似度阈值设太高会怎样、太低又会怎样？你会用什么信号来定这个阈值？",
              "What happens if the similarity cutoff is too high vs too low — and what signal would you use to set it?"),
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
        "open": [
            L("要把“默认问答”改造成“只引用、不编造”的客服引擎，你会替换 QueryEngine 的哪几件组件？",
              "To reshape default Q&amp;A into a 'cite-only, never invent' support engine, which components of the QueryEngine would you swap?"),
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
        "open": [
            L("多轮对话里“每轮都检索”有时是浪费。你会用什么规则决定某一轮要不要触发检索？",
              "In multi-turn chat, retrieving every turn is sometimes wasteful. What rule would you use to decide whether a given turn should trigger retrieval?"),
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
        "open": [
            L("同样的检索结果，换一句 prompt 就能改变答案——这把“质量责任”更多压在检索上还是 prompt 上？你怎么分工调优？",
              "Same retrieval, different prompt, different answer — does that put more of the quality burden on retrieval or on the prompt, and how would you split your tuning effort?"),
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
        "open": [
            L("进阶检索都用更多计算换更好结果。对一个延迟敏感的线上问答，你会接受 query fusion 的额外开销吗？如何权衡？",
              "Advanced retrieval trades more compute for better results. For a latency-sensitive live Q&amp;A, would you accept query-fusion's overhead — and how would you weigh it?"),
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
    "21-production-retrieval.html": {
        "mcq": [{
            "q": L("纯向量检索为什么会漏掉精确编号“X-2000”这样的查询？",
                   "Why can pure vector search miss an exact id like 'X-2000'?"),
            "opts": [
                L("向量库坏了", "the vector store is broken"),
                L("embedding 偏语义，对精确符号/罕见 token 不敏感，可能排不进 top-k",
                  "embeddings capture meaning and are weak on exact symbols/rare tokens, so it may miss top-k"),
                L("必须重建索引", "you must re-index"),
                L("top_k 一定太小", "top_k is always too small"),
            ],
            "answer": 1,
            "why": L("解决靠混合检索(向量 + BM25/关键词)或把编号写进 metadata 精确过滤。",
                     "Fix with hybrid retrieval (vector + BM25) or exact metadata filtering."),
        }],
        "open": [L("你的查询里既有自然语言问题也有精确产品编号，你会怎么配比向量与关键词两路的权重？",
                   "With both natural-language questions and exact product ids in your queries, how would you weight the vector vs keyword paths?")],
    },
    "22-eval-scale.html": {
        "mcq": [{
            "q": L("把固定的<strong>回归金标集</strong>接进 CI 闸，最关键的作用是？",
                   "Wiring a fixed <strong>regression gold set</strong> into a CI gate matters most because it…"),
            "opts": [
                L("让单次回答的分数更高", "makes a single answer score higher"),
                L("用同一批题重跑，挡住“修好一个却悄悄弄坏一批”的回归",
                  "re-runs the same questions to block “fix one, silently break many” regressions"),
                L("彻底取代人工标注", "fully replaces human labeling"),
                L("让评估不再需要 LLM", "removes the need for an LLM in evaluation"),
            ],
            "answer": 1,
            "why": L("回归集的价值在“同一批题、每次重跑、比趋势”：你盯的那题修好了，分数还能告诉你别的题有没有悄悄退化；达不到阈值就 fail，坏改动合不进主干。",
                     "A regression set's value is “same questions, re-run every time, watch the trend”: the case you fixed may pass while others quietly regress, and the score reveals it; below threshold it fails, so the bad change can't reach main."),
        }],
        "open": [L("你只有 200 条无标准答案的历史问答，想搭一个最小可用的回归评估闸，你会怎么做？（提示：哪几把尺子不需要参考答案？）",
                   "You have 200 historical Q&amp;A pairs with no reference answers and want a minimal usable regression gate. How would you build it? (Hint: which rulers need no reference?)")],
    },
    "23-observability.html": {
        "mcq": [{
            "q": L("线上一条问答答错了，你打开它的 trace。<strong>最该先看</strong>哪一项来判断“是检索还是生成的问题”？",
                   "A production answer is wrong and you open its trace. <strong>What should you look at first</strong> to decide “retrieval problem or generation problem”?"),
            "opts": [
                L("LLM 这步花了多少毫秒", "how many ms the LLM step took"),
                L("检索到的 node 里有没有正确依据、相似度高不高",
                  "whether the retrieved nodes contain the right evidence and their similarity"),
                L("这次请求一共烧了多少钱", "the total cost of this request"),
                L("用的是哪个 embedding 模型", "which embedding model was used"),
            ],
            "answer": 1,
            "why": L("先看检索召回的 node：若正确依据<strong>压根没召到</strong>，那是检索问题（调 chunk / 加 BM25 / 调 top_k），改 prompt 没用；只有在“召到了却答错”时才是生成问题。耗时和成本是<strong>性能 / 费用</strong>维度，不用来判断答案对错的归因。",
                     "Read the retrieved nodes first: if the right evidence <strong>was never recalled</strong>, it's a retrieval problem (tune chunking / add BM25 / adjust top_k) and editing the prompt won't help; only when it “was recalled yet still wrong” is it a generation problem. Latency and cost are <strong>performance / spend</strong> axes, not for attributing correctness."),
        }],
        "open": [L("你只能在<strong>本地零依赖</strong>（不接任何外部后端）的前提下排查一条“答得慢又不准”的查询，你会用 <code>LlamaDebugHandler</code> 看哪些信息、按什么顺序定位问题？",
                   "Restricted to a <strong>local, zero-dependency</strong> setup (no external backend), how would you use <code>LlamaDebugHandler</code> to debug one “slow and inaccurate” query — which signals would you read, and in what order?")],
    },
    "24-cost-latency.html": {
        "mcq": [{
            "q": L("给生产 RAG 开了 <code>streaming=True</code>（流式），它主要改善的是哪个指标？",
                   "You enable <code>streaming=True</code> on a production RAG. Which metric does it mainly improve?"),
            "opts": [
                L("总延迟（答完整段话的总时间）大幅下降",
                  "total latency (time to finish the whole answer) drops sharply"),
                L("首字延迟（看到第一个 token 的时间）大幅下降，总延迟几乎不变",
                  "time-to-first-token drops sharply, while total latency is nearly unchanged"),
                L("每问的 token 成本下降", "token cost per question drops"),
                L("检索召回率提升", "retrieval recall improves"),
            ],
            "answer": 1,
            "why": L("流式让 LLM 边生成边逐 token 吐出，用户几百毫秒就看到第一个字，<strong>体感“立刻在答”</strong>；但模型要生成的 token 总数没变，<strong>答完整段话的总时间几乎一样</strong>，token 成本也不变。要真正缩短总延迟得靠缓存命中、换更快/更小的模型、压 context 或降 top_k。",
                     "Streaming makes the LLM emit tokens as it generates, so the first character shows in a few hundred ms and it <strong>feels like it's answering instantly</strong>; but the total tokens to generate are unchanged, so <strong>finishing the whole answer takes about the same time</strong>, and token cost is unchanged too. Actually shortening total latency takes cache hits, a faster/smaller model, trimming context, or lowering top_k."),
        }],
        "open": [L("你的 RAG 每问成本偏高、p95 延迟也超标。在不明显牺牲答案质量的前提下，你会<strong>按什么顺序</strong>动手，每一步用<strong>什么数字</strong>判断“砍对了”？",
                   "Your RAG has high cost-per-question and an over-budget p95 latency. Without obviously sacrificing answer quality, in <strong>what order</strong> would you act, and <strong>which numbers</strong> tell you each step “cut the right thing”?")],
    },
    "25-security.html": {
        "mcq": [{
            "q": L("多租户 RAG 要保证“A 公司绝不会检索到 B 公司的数据”，这个隔离<strong>最该在哪一层强制</strong>？",
                   "A multi-tenant RAG must guarantee “company A can never retrieve company B's data”. <strong>Which layer should enforce</strong> this isolation?"),
            "opts": [
                L("在 system prompt 里写“只回答本租户的问题”，叮嘱模型别越权",
                  "write “only answer for this tenant” in the system prompt and trust the model"),
                L("在<strong>检索层</strong>用 MetadataFilters 按 tenant_id 下推过滤，别租户的数据根本不会被召回",
                  "at the <strong>retrieval layer</strong>, push a tenant_id MetadataFilters filter down so other tenants' data is never recalled"),
                L("让前端在请求里自己带上 tenant_id，后端直接信任",
                  "have the frontend send its own tenant_id and trust it on the backend"),
                L("答完之后再用一个 LLM 检查答案里有没有混入别租户的信息",
                  "after answering, use another LLM to check whether the answer mixed in other tenants' info"),
            ],
            "answer": 1,
            "why": L("隔离必须在<strong>检索层</strong>强制：用 MetadataFilters 把 tenant_id 过滤<strong>下推到向量库</strong>，别租户的向量根本不参与打分 / 召回，从源头杜绝越权。靠 prompt 叮嘱不可靠——指令会被忽略、被注入绕过；让前端自带 tenant_id 等于把锁交给访客，必须用<strong>已认证</strong>身份在服务端注入；事后再用 LLM 复查是亡羊补牢，数据已经离开隔离边界、可能进了日志。把“绝不能漏”的隔离放在<strong>数据根本进不来</strong>的那一层，才是结构性保证。",
                     "Isolation must be enforced at the <strong>retrieval layer</strong>: MetadataFilters push the tenant_id filter <strong>down into the vector store</strong> so other tenants' vectors are never scored or recalled, stopping breaches at the source. A prompt hint is unreliable — instructions get ignored or overridden by injection; letting the frontend supply its own tenant_id hands the lock to the visitor (inject it server-side from an <strong>authenticated</strong> identity); a post-hoc LLM check is too late — the data has already left the boundary and may sit in the logs. Putting “never-leak” isolation at the layer where <strong>data can't even enter</strong> is the only structural guarantee."),
        }],
        "open": [L("你的多租户 RAG 还要支持“管理员可跨租户检索”。你会怎么设计 tenant 过滤，既保证普通用户绝不越权、又安全地放开管理员？（提示：过滤条件由谁、在<strong>哪一层</strong>决定？）",
                   "Your multi-tenant RAG must also let “admins retrieve across tenants”. How would you design the tenant filter so ordinary users can never breach isolation while admins are safely allowed through? (Hint: who decides the filter, and at <strong>which layer</strong>?)")],
    },
    "26-agents-workflows.html": {
        "mcq": [{
            "q": L("下面哪种情况<strong>最该</strong>从固定管道升级成 agent（而不是继续用一次性检索）？",
                   "Which situation <strong>most warrants</strong> upgrading from a fixed pipeline to an agent (rather than sticking with one-shot retrieval)?"),
            "opts": [
                L("问题简单、单一知识源，每次问法都差不多",
                  "the question is simple, single-source, and phrased about the same every time"),
                L("一个问题要跨多个库分多步查、还可能要看中间结果再决定补查",
                  "one question needs several steps across multiple stores and may re-retrieve based on intermediate results"),
                L("只是想让答案输出更快（首字延迟更低）",
                  "you just want the answer to start streaming faster (lower time-to-first-token)"),
                L("想降低每问的 token 成本", "you want to cut the token cost per question"),
            ],
            "answer": 1,
            "why": L("agent 的价值在于<strong>会决策的多步循环</strong>：当一个问题需要<strong>多源 / 多步 / 看中间结果再自我纠错</strong>（比如“对比退款和换货政策”要分别查两次再综合）时，固定的一次性检索就答不全，才值得上 agent。而“问得简单稳定”恰恰应该留在固定管道（更快更好调）；“想更快出字”是<strong>流式（streaming）</strong>的范畴；agent <strong>反而增加</strong> LLM 调用、抬高 token 成本和延迟，绝不是降本手段。一句话：<strong>为多步决策付费，别为简单问题买单</strong>。",
                     "An agent's value is its <strong>deciding, multi-step loop</strong>: when a question needs <strong>multiple sources / steps / self-correction from intermediate results</strong> (e.g. “compare the refund and exchange policies” needs two lookups then a synthesis), a fixed one-shot retrieval can't answer fully — that's when an agent earns its keep. A “simple, stable” question should stay on a fixed pipeline (faster, easier to debug); “answer faster” is what <strong>streaming</strong> is for; and an agent <strong>adds</strong> LLM calls, raising token cost and latency — never a cost-cutting move. In a line: <strong>pay for multi-step decisions, not for simple questions</strong>."),
        }],
        "open": [L("你有两类查询：① “X-2000 的保修期是多久”（单库、一步能答）；② “把 A、B、C 三款机型的保修与退换政策做个对比表”（要多次检索再综合）。你会让<strong>哪一类</strong>走固定管道、哪一类上 agent？为什么？又怎么<strong>用数据</strong>证明给 ② 上 agent 是划算的（对比固定管道，看哪些指标）？",
                   "You have two query types: (1) “what's the warranty of X-2000” (single store, one step); (2) “build a comparison table of the warranty and return policies for models A, B and C” (needs several retrievals then a synthesis). <strong>Which</strong> goes on a fixed pipeline and which on an agent — and why? And how would you <strong>use data</strong> to prove the agent pays off for (2) versus a fixed pipeline (which metrics would you compare)?")],
    },
    "27-graph-rag.html": {
        "mcq": [{
            "q": L("下列哪种问题最该用图谱 RAG 而非纯向量？",
                   "Which question most warrants Graph RAG over pure vectors?"),
            "opts": [
                L("找与“退款政策”语义相近的段落", "find passages semantically close to “refund policy”"),
                L("X 的供应商的总部在哪个国家（多跳）", "which country is the HQ of X's supplier in (multi-hop)"),
                L("这段话的情感是正还是负", "is this passage's sentiment positive or negative"),
                L("把文档翻译成英文", "translate the document into English"),
            ],
            "answer": 1,
            "why": L("正确的是“多跳关系查询”（X 的供应商的总部在哪个国家）：要顺着 供应商→总部→国家 的边走，图谱把事实存成可遍历的三元组正好胜任。找语义相近段落是相似检索（向量更划算），判断情感正负是分类，翻译就是翻译——都用不上图的多跳能力。",
                     "The correct one is the “multi-hop relation query” (which country is X's supplier's HQ in): you must walk supplier→HQ→country, and a graph stores facts as traversable triples for exactly this. Finding semantically close passages is similarity retrieval (vectors are cheaper), judging sentiment is classification, and translation is translation — none need a graph's multi-hop power."),
        }],
        "open": [L("你的知识库是产品-配件-兼容关系网，为什么图谱比向量更合适？（提示：<strong>关系 / 多跳 / 可解释路径</strong>）",
                   "Your knowledge base is a product-part-compatibility web of relations. Why is a graph more suitable than vectors? (Hint: <strong>relations / multi-hop / explainable path</strong>)")],
    },
    "28-structured-data.html": {
        "mcq": [{
            "q": L("“各区域季度环比增长率”最该用哪种方式？",
                   "Which approach best fits “quarter-over-quarter growth rate per region”?"),
            "opts": [
                L("向量检索", "vector retrieval"),
                L("text-to-SQL", "text-to-SQL"),
                L("rerank 重排序", "rerank"),
                L("HyDE 查询改写", "HyDE query rewrite"),
            ],
            "answer": 1,
            "why": L("正确的是 <strong>text-to-SQL</strong>：季度环比增长率是<strong>聚合计算</strong>（按季度分组、求和，再算环比），"
                     "要让 LLM 写出 SQL、交数据库<strong>精确算</strong>。其余三个都在解决“<strong>找相似</strong>”而非“精确算数字”——"
                     "<strong>向量检索</strong>按语义近似召回片段，<strong>rerank 重排序</strong>只是把已召回的片段重新排个序，"
                     "<strong>HyDE 查询改写</strong>是先造个假设答案再去检索；它们都不会做 <code>GROUP BY/SUM</code> 这类精确聚合。",
                     "The right one is <strong>text-to-SQL</strong>: quarter-over-quarter growth is an <strong>aggregation</strong> "
                     "(group by quarter, sum, then compute the ratio), so have the LLM write SQL and let the database <strong>"
                     "compute it exactly</strong>. The other three all solve “<strong>find similar</strong>”, not “compute exact "
                     "numbers” — <strong>vector retrieval</strong> recalls chunks by semantic proximity, <strong>rerank</strong> only "
                     "reorders already-retrieved chunks, and <strong>HyDE</strong> drafts a hypothetical answer to retrieve with; "
                     "none of them do <code>GROUP BY/SUM</code>-style exact aggregation."),
        }],
        "open": [L("为什么 <code>PandasQueryEngine</code> 要特别小心？（提示：<strong>它会执行 LLM 生成的 Python / 提示注入 · 越权 / "
                   "沙箱 · 只读 · 最小权限</strong>）",
                   "Why must you be especially careful with <code>PandasQueryEngine</code>? (Hint: <strong>it executes "
                   "LLM-generated Python / prompt injection · over-reach / sandbox · read-only · least privilege</strong>)")],
    },
    "29-multimodal-rag.html": {
        "mcq": [{
            "q": L("多模态 RAG 能“用文字查图”的根本前提是什么？",
                   "What is the fundamental prerequisite that lets multimodal RAG “query images with text”?"),
            "opts": [
                L("图和文被映射到同一个向量空间", "images and text are mapped into the same vector space"),
                L("先把每张图用 caption 转成文字再做纯文本检索",
                  "caption every image into text first, then do text-only retrieval"),
                L("换一个更大参数量的 LLM", "switch to an LLM with more parameters"),
                L("关闭 rerank 重排", "turn off reranking"),
            ],
            "answer": 0,
            "why": L("正确的是“图和文被映射到同一个向量空间”：跨模态检索的前提，是图、文的 embedding 落在<strong>同一空间</strong>，"
                     "才能拿文字向量去和图像向量比距离、互相召回。“先把图用 caption 转成文字再做纯文本检索”是另一种<strong>降级方案"
                     "</strong>（能跑，但丢视觉细节），并没有让图文向量对齐；“换更大参数量的 LLM”和“关闭 rerank 重排”都在调别的环节，"
                     "<strong>都不解决跨模态对齐</strong>这个根本前提。",
                     "The right one is “images and text are mapped into the same vector space”: cross-modal retrieval hinges on "
                     "image and text embeddings sitting in <strong>one shared space</strong>, so a text vector can be "
                     "distance-compared to image vectors and recall them. “Caption images into text first, then do text-only "
                     "retrieval” is a <strong>downgrade</strong> (it runs, but loses visual detail) and never aligns the "
                     "image/text vectors; “use a larger LLM” and “turn off reranking” tweak other stages and <strong>none "
                     "address the cross-modal alignment</strong> that is the real prerequisite."),
        }],
        "open": [L("纯文字 RAG 遇到“这张架构图说明了什么”为什么无能为力、多模态怎么解决？（提示：<strong>视觉细节 / 同一向量空间 / "
                   "会看图的 LLM</strong>）",
                   "Why is text-only RAG helpless on “what does this architecture diagram show”, and how does multimodal solve "
                   "it? (Hint: <strong>visual detail / same vector space / a vision-capable LLM</strong>)")],
    },
    "30-sub-question.html": {
        "mcq": [{
            "q": L("<code>SubQuestionQueryEngine</code> 最擅长哪类问题？",
                   "Which kind of question is <code>SubQuestionQueryEngine</code> best at?"),
            "opts": [
                L("单文档里的相似检索", "similarity retrieval inside a single document"),
                L("跨多个来源的对比或多步问题", "comparison or multi-step questions across multiple sources"),
                L("压缩 prompt 省 token", "compressing the prompt to save tokens"),
                L("流式逐字输出", "streaming the output token by token"),
            ],
            "answer": 1,
            "why": L("正确的是“跨多个来源的对比或多步问题”：sub-question 的价值正是把这类问题<strong>拆成子问、分别检索、再汇总</strong>，"
                     "补上单次 top-k 答不全的部分。“单文档里的相似检索”普通 retriever 一次召回就够，用不上拆解；“压缩 prompt 省 token”是"
                     "省成本的关注点（拆问反而会<strong>多花</strong> token），“流式逐字输出”是响应方式——两者都和“把复杂问题拆开”无关。",
                     "The right one is “comparison or multi-step questions across multiple sources”: that's exactly sub-question's "
                     "value — <strong>split such a question into sub-questions, retrieve each, then aggregate</strong>, covering what a "
                     "single top-k can't. “Similarity retrieval inside a single document” is handled by an ordinary retriever in one "
                     "recall and needs no decomposition; “compressing the prompt to save tokens” is a cost concern (splitting actually "
                     "<strong>spends more</strong> tokens), and “streaming output token by token” is a delivery style — neither has "
                     "anything to do with breaking a complex question apart."),
        }],
        "open": [L("“对比 A、B 两份合同的违约条款差异”为什么适合 sub-question？（提示：<strong>拆成两个子问 / 各自检索 / 再对比汇总"
                   "</strong>）",
                   "Why is “compare the breach-clause differences between contracts A and B” a good fit for sub-question? (Hint: "
                   "<strong>split into two sub-questions / retrieve each / then compare and aggregate</strong>)")],
    },
    "31-structured-outputs.html": {
        "mcq": [{
            "q": L("为什么用 Pydantic program 而不是正则 parse LLM 的自由文本？",
                   "Why use a Pydantic program instead of regex-parsing the LLM's free text?"),
            "opts": [
                L("输出有类型校验、契约稳定，下游可直接用", "the output is type-validated with a stable contract, ready for downstream use"),
                L("更省 token", "it saves tokens"),
                L("完全不需要 LLM", "it removes the need for an LLM entirely"),
                L("自动获得多模态能力", "it automatically gains multimodal ability"),
            ],
            "answer": 0,
            "why": L("正确的是“输出有类型校验、契约稳定，下游可直接用”：结构化输出的价值是“<strong>类型即契约</strong>”——LLM 直接产出"
                     "<strong>校验过的对象</strong>，下游 <code>.total</code> 拿来就用，措辞一变也不再让解析崩。“更省 token”不对——把 "
                     "schema 塞进提示反而<strong>多花</strong> token；“完全不需要 LLM”更不对——<strong>仍然要 LLM</strong> 来生成，只是把"
                     "生成目标从“一段话”换成“一个对象”；“自动获得多模态能力”与结构化输出<strong>无关</strong>，那是另一回事（L29）。",
                     "The right one is “the output is type-validated with a stable contract, ready for downstream use”: structured "
                     "output's value is “<strong>the type is the contract</strong>” — the LLM emits a <strong>validated object</strong> "
                     "directly, downstream <code>.total</code> just works, and shifting wording no longer breaks parsing. “It saves "
                     "tokens” is wrong — stuffing the schema into the prompt actually <strong>spends more</strong> tokens; “it removes "
                     "the need for an LLM entirely” is more wrong — you <strong>still need the LLM</strong> to generate, just with the "
                     "target changed from “a paragraph” to “an object”; and “multimodal ability” is <strong>unrelated</strong> to "
                     "structured output — that's a different topic (L29)."),
        }],
        "open": [L("把 RAG 的答案变成 <code>{answer, sources, confidence}</code> 结构有什么工程价值？（提示：<strong>下游可程序化消费 / "
                   "可校验 / 可监控（如按 confidence 兜底）</strong>）",
                   "What is the engineering value of turning a RAG answer into a <code>{answer, sources, confidence}</code> structure? "
                   "(Hint: <strong>programmatically consumable downstream / validatable / monitorable, e.g. fall back on confidence"
                   "</strong>)")],
    },
    "32-multi-agent.html": {
        "mcq": [{
            "q": L("<code>AgentWorkflow</code> 里的 handoff 指什么？",
                   "What does a handoff mean in <code>AgentWorkflow</code>?"),
            "opts": [
                L("把当前任务移交给另一个更合适的 agent", "hand the current task to another, more suitable agent"),
                L("关闭某个工具的调用", "disable calling a particular tool"),
                L("压缩对话历史省 token", "compress the conversation history to save tokens"),
                L("给 agent 切换更大的模型", "switch the agent to a bigger model"),
            ],
            "answer": 0,
            "why": L("handoff 是多 agent 协作的核心——一个 agent 干完自己那段，把<strong>控制权和上下文</strong>交给下一个专精 agent；"
                     "它与<strong>关工具、压历史、换模型</strong>都无关。把任务“<strong>移交给更合适的 agent</strong>”才是它的本义："
                     "底层框架其实把 handoff 实现成一个<strong>自动注入的工具</strong>，被调用的“工具”是<strong>另一个 agent</strong>。"
                     "“关闭某个工具的调用”是改工具集、“压缩对话历史省 token”是省上下文成本、“切换更大的模型”是换 LLM——三者都不是把"
                     "任务<strong>交接</strong>给队友。",
                     "A handoff is the core of multi-agent cooperation — one agent finishes its slice and passes <strong>control and "
                     "context</strong> to the next, specialized agent; it has nothing to do with <strong>disabling a tool, compressing "
                     "history, or switching models</strong>. Its real meaning is “<strong>handing the task to a more suitable agent</strong>”: "
                     "under the hood the framework implements a handoff as an <strong>auto-injected tool</strong> whose “tool” is "
                     "<strong>another agent</strong>. “Disable calling a tool” edits the toolset, “compress history to save tokens” trims "
                     "context cost, and “switch to a bigger model” swaps the LLM — none of them <strong>hand the task off</strong> to a "
                     "teammate."),
        }],
        "open": [L("什么时候该从单 agent 升级到多 agent？（提示：<strong>单 agent 工具 / 职责过载、prompt 太杂 / 任务能按角色清晰拆分 / "
                   "需要不同专精、不同 system_prompt</strong>）",
                   "When should you upgrade from a single agent to multiple agents? (Hint: <strong>one agent's tools / duties are "
                   "overloaded and its prompt is a mess / the task splits cleanly by role / you need different specialties and different "
                   "system prompts</strong>)")],
    },
    "33-human-in-the-loop.html": {
        "mcq": [{
            "q": L("在 LlamaIndex workflow 里，HITL（暂停等人确认）靠什么实现？",
                   "In a LlamaIndex workflow, what implements HITL (pausing for a human's confirmation)?"),
            "opts": [
                L("一个 <code>@step</code> 返回 <code>InputRequiredEvent</code> 挂起、调用方回 <code>HumanResponseEvent</code> 恢复",
                  "a <code>@step</code> returns <code>InputRequiredEvent</code> to pause; the caller sends back <code>HumanResponseEvent</code> to resume"),
                L("关闭 LLM 调用", "disable the LLM call"),
                L("用 rerank 重排候选", "re-rank candidates with a reranker"),
                L("打开流式逐字输出", "turn on token-by-token streaming"),
            ],
            "answer": 0,
            "why": L("HITL 的机制<strong>就是这一对事件</strong>：某个 <code>@step</code> <strong>返回 <code>InputRequiredEvent</code>"
                     "</strong>——它被自动写入事件流、无需下游消费即<strong>挂起</strong>流程；调用方从流里取到后，回一个 "
                     "<code>HumanResponseEvent(response=…)</code>，<strong>消费它的 <code>@step</code> 据此恢复或中止</strong>。"
                     "“<strong>关闭 LLM 调用</strong>”只是不用模型、与“暂停等人”无关；“<strong>用 rerank 重排候选</strong>”是检索"
                     "后处理（L13）、改的是结果顺序；“<strong>打开流式逐字输出</strong>”只是把答案一个字一个字地吐出来、是"
                     "<strong>展示方式</strong>——三者都<strong>不会让流程停下来等人点头</strong>。",
                     "HITL's mechanism <strong>is exactly this pair of events</strong>: a <code>@step</code> <strong>returns an "
                     "<code>InputRequiredEvent</code></strong> — auto-written to the event stream and <strong>pausing</strong> the flow "
                     "with no downstream consumer; the caller picks it up from the stream and sends back a "
                     "<code>HumanResponseEvent(response=…)</code>, and <strong>the <code>@step</code> consuming it resumes or aborts"
                     "</strong>. “<strong>Disabling the LLM call</strong>” just means not using the model — nothing to do with “pause for "
                     "a human”; “<strong>re-ranking candidates with a reranker</strong>” is retrieval post-processing (L13) that reorders "
                     "results; “<strong>turning on token-by-token streaming</strong>” merely emits the answer one token at a time, a "
                     "<strong>display choice</strong> — none of the three <strong>stops the flow to wait for a human nod</strong>."),
        }],
        "open": [L("哪些动作<strong>该</strong>加人工确认、哪些<strong>不该</strong>？（提示：<strong>不可逆 / 高风险</strong>——删除 / 转账 / "
                   "外发——该加闸；<strong>只读 / 可撤销 / 低风险</strong>——检索 / 起草 / 计算——放行；别让 HITL 把<strong>吞吐</strong>拖垮、"
                   "把人<strong>烦走</strong>）",
                   "Which actions <strong>should</strong> get a human confirm and which <strong>shouldn't</strong>? (Hint: "
                   "<strong>irreversible / high-risk</strong> — delete / transfer / outbound — gate them; <strong>read-only / reversible / "
                   "low-risk</strong> — retrieve / draft / compute — let them through; don't let HITL <strong>grind throughput</strong> or "
                   "<strong>annoy the human away</strong>)")],
    },
    "34-serving.html": {
        "mcq": [{
            "q": L("把 RAG 上线成服务，<strong>最该避免</strong>的做法是？",
                   "When shipping a RAG as a service, which practice should you <strong>most avoid</strong>?"),
            "opts": [
                L("每个请求都重新加载 / 重建索引", "reload / rebuild the index on every request"),
                L("启动时加载一次、查询引擎常驻复用", "load once at startup and reuse a resident query engine"),
                L("用 <code>aquery</code> 异步处理并发", "use <code>aquery</code> to handle concurrency asynchronously"),
                L("把索引持久化到磁盘", "persist the index to disk"),
            ],
            "answer": 0,
            "why": L("题目问的是「<strong>最该避免</strong>」。<strong>每个请求都重新加载 / 重建索引</strong>会把<strong>"
                    "一次性建库成本</strong>（读文件 / 切块 / embedding / 写库）摊到<strong>每一次查询</strong>上——又慢"
                    "又浪费，并发一上来就垮，正是上线第一大忌。其余三项<strong>恰恰都是该做的正解</strong>：「<strong>"
                    "启动时加载一次、查询引擎常驻复用</strong>」把重活留在启动、请求里只剩轻活；「<strong>用 "
                    "<code>aquery</code> 异步处理并发</strong>」在等 LLM / 向量库时让别的请求继续跑（承 L24）；「<strong>"
                    "把索引持久化到磁盘</strong>」让启动用 <code>load_index_from_storage</code> 秒级恢复、免去重建"
                    "（承 L11）。",
                    "The question asks what to <strong>most avoid</strong>. <strong>Reloading / rebuilding the index on "
                    "every request</strong> smears the <strong>one-time build cost</strong> (read files / chunk / embed "
                    "/ write) across <strong>every single query</strong> — slow, wasteful, and collapsing under "
                    "concurrency: the cardinal serving sin. The other three are exactly the <strong>right things to "
                    "do</strong>: “<strong>load once at startup and reuse a resident query engine</strong>” keeps the "
                    "heavy work at startup and leaves only light work in the request; “<strong>use <code>aquery</code> "
                    "to handle concurrency</strong>” lets other requests run while waiting on the LLM / vector store "
                    "(from L24); and “<strong>persist the index to disk</strong>” lets startup restore in seconds via "
                    "<code>load_index_from_storage</code> instead of rebuilding (from L11)."),
        }],
        "open": [L("为什么服务里要用 <code>aquery</code> / 流式，而不是同步的 <code>query</code>？（提示：<strong>异步"
                   "</strong>提升<strong>并发吞吐</strong>——一条请求等 LLM / 向量库时别的请求照跑；<strong>流式</strong>"
                   "降低<strong>首 token 延迟</strong>、改善体验，但不缩总耗时——都承 L24）",
                   "Why use <code>aquery</code> / streaming in a service instead of synchronous <code>query</code>? (Hint: "
                   "<strong>async</strong> lifts <strong>concurrent throughput</strong> — while one request waits on the "
                   "LLM / vector store others keep running; <strong>streaming</strong> cuts <strong>first-token "
                   "latency</strong> for a better experience but doesn't shorten total time — both from L24)")],
    },
}


def render(fname):
    data = QUIZZES.get(fname) or {}
    mcqs = data.get("mcq", [])
    interviews = _iv.INTERVIEW.get(fname, [])
    opens = data.get("open", [])
    if not (mcqs or interviews or opens):
        return ""
    head = i18n.t("🧪 自测 · 想一想为什么这么设计", "🧪 Self-check · think about the design")
    out = ['<div class="selftest">', f"<h2>{head}</h2>"]
    for i, item in enumerate(mcqs, 1):
        shuffled, ans = _shuffle(item["opts"], item["answer"], f"{fname}:{i}")
        opts = "\n".join(f"    <li>{i18n.render(o, block=False)}</li>" for o in shuffled)
        letter = chr(65 + ans)
        reveal = i18n.t("看答案与解析", "Show answer &amp; explanation")
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
    if interviews:
        ihead = i18n.t("🎯 面试官提问 · 试着答出要点", "🎯 Interviewer asks · cover the key points")
        reveal = i18n.t("看参考要点", "Show key points")
        hint = i18n.t("点击展开", "expand")
        out.append(f"<h3>{ihead}</h3>")
        for j, item in enumerate(interviews, 1):
            fig = item.get("fig", "")
            out.append(
                f'<div class="quiz interview">\n'
                f'  <div class="qn">🎯 {j}. {i18n.render(item["q"], block=False)}</div>\n'
                f'  <details class="accordion">\n'
                f'    <summary>{reveal} <span class="hint">{hint}</span></summary>\n'
                f'    <div class="acc-body"><div class="qa"><div class="a">'
                f'{i18n.render(item["answer"], block=False)}'
                f"</div></div>{fig}</div>\n"
                f"  </details>\n"
                f"</div>"
            )
    if opens:
        spark = i18n.t("💭 发散思考（没有标准答案）", "💭 Open questions (no single right answer)")
        lis = "\n".join(f"    <li>{i18n.render(o, block=False)}</li>" for o in opens)
        out.append(
            f'<div class="card spark">\n  <div class="tag">{spark}</div>\n  <ul>\n{lis}\n  </ul>\n</div>'
        )
    out.append("</div>")
    return "\n".join(out)
