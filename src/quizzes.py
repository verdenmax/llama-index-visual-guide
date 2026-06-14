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
        "interview": [
            {"q": L("用一句话向非技术同事解释 RAG，再用一句话说清它和微调的区别。",
                    "Explain RAG to a non-technical colleague in one sentence, then contrast it with fine-tuning in one more."),
             "answer": L("RAG＝答题前先“翻资料”再作答（开卷）；微调＝把知识焊进模型权重。要点：RAG 更新知识只需重建索引、可溯源、便宜；微调贵、难溯源，更适合改风格/格式而非加事实知识。",
                         "RAG = look up sources first, then answer (open-book); fine-tuning = bake knowledge into weights. Key points: RAG updates by re-indexing, is traceable and cheap; fine-tuning is costly, hard to cite, and better for changing style/format than adding facts.")},
            {"q": L("什么情况下你<strong>不</strong>用 RAG，而是直接长上下文全塞或微调？",
                    "When would you <strong>not</strong> use RAG, and instead stuff long context or fine-tune?"),
             "answer": L("语料极小且固定→直接塞进上下文；要改变模型的行为/语气/输出格式→微调；强实时的单一短文档→长上下文。RAG 的甜区是大、私有、时效性强、且需要溯源的知识库。",
                         "Tiny fixed corpus → just stuff context; need to change behavior/tone/output format → fine-tune; one short real-time doc → long context. RAG's sweet spot is large, private, time-sensitive knowledge that needs citations.")},
            {"q": L("上线后用户反馈“它还是会编”，在 RAG 框架下你会从哪几处依次排查？",
                    "Users report 'it still makes things up' — where do you investigate, in order?"),
             "answer": L("先看 <code>response.source_nodes</code>：① 检索有没有命中正确依据（召回问题→调 top_k/embedding/切块）；② Prompt 有没有约束“只依据资料、未提及就说不知道”；③ 合成是否越界发挥；④ 用 Faithfulness 评估量化。",
                         "Start from <code>response.source_nodes</code>: (1) did retrieval surface the right evidence (recall → tune top_k/embedding/chunking); (2) does the prompt constrain 'answer only from sources, say unknown otherwise'; (3) is synthesis over-reaching; (4) quantify with a Faithfulness evaluator.")},
            {"q": L("RAG 把模型“记忆”外置成索引，最大的运维好处和最大的新负担各是什么？",
                    "RAG externalizes memory into an index — what's the biggest ops benefit and the biggest new burden?"),
             "answer": L("好处：更新知识只重建索引、模型零改动、答案可溯源。负担：你要维护一整条数据管道（加载→切块→embedding→向量库→重建→评估），检索质量成为新瓶颈与新的失败点。",
                         "Benefit: update knowledge by re-indexing, model untouched, answers traceable. Burden: you now own a whole data pipeline (load→split→embed→store→rebuild→eval), and retrieval quality becomes the new bottleneck and failure point.")},
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
        "interview": [
            {"q": L("看到 <code>from llama_index.llms.openai import OpenAI</code>，你立刻能判断哪几件事？",
                    "Seeing <code>from llama_index.llms.openai import OpenAI</code>, what do you instantly know?"),
             "answer": L("路径不含 <code>core</code> → 这是第三方<strong>集成实现</strong>，不是核心抽象；它是独立 pip 包（需单独安装）；换厂商通常只改这一行导入 + 一行配置；core 只定义接口。",
                         "No <code>core</code> in the path → it's a third-party <strong>integration</strong>, not a core abstraction; it's a separate pip package; swapping vendors is usually this import + one config line; core only defines the interface.")},
            {"q": L("“接口在 core、实现在集成包”的分层，什么时候反而成为<strong>负担</strong>？",
                    "When does the core/integration split become a <strong>burden</strong> instead of a benefit?"),
             "answer": L("要点：装的小包变多、版本矩阵变复杂；某个集成可能滞后于 core 的接口变更而踩坑；调试要跨包跳转；小项目嫌零碎。代价换来的是生态能独立演进。",
                         "Key points: more small packages, a more complex version matrix; an integration may lag behind a core interface change; debugging hops across packages; small projects find it fragmented. The price buys an ecosystem that evolves independently.")},
            {"q": L("本地用 Ollama 跑通的 RAG 要上线换成 OpenAI，你会改哪些、不改哪些？为什么 Embedding 要特别小心？",
                    "Moving a local Ollama RAG to OpenAI for production — what changes, what doesn't, and why is the embedding special?"),
             "answer": L("改 <code>Settings.llm</code>（基本一行）；retriever / index / query engine 不动。换 Embedding 模型则<strong>必须重建索引</strong>——已落盘的向量用旧模型算出，与新模型坐标系不可比。",
                         "Change <code>Settings.llm</code> (about one line); retriever / index / query engine stay. But swapping the <strong>embedding</strong> model forces a re-index — stored vectors were computed by the old model and aren't comparable to the new one's space.")},
            {"q": L("为什么 LlamaIndex 把 300+ 集成拆成独立包，而不是打成一个大包？",
                    "Why split 300+ integrations into separate packages instead of one monolith?"),
             "answer": L("独立发版与依赖隔离（不会因为装一个就拖入一堆无关依赖）、按需安装、各厂商自行迭代；core 保持稳定、不被任一集成的节奏绑死。",
                         "Independent releases and dependency isolation (one install doesn't drag in unrelated deps), à-la-carte installs, vendors iterate on their own; core stays stable, not bound to any one integration's cadence.")},
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
        "interview": [
            {"q": L("<code>VectorStoreIndex.from_documents(docs)</code> 这一行背后，依次发生了什么？",
                    "What happens, step by step, behind the single line <code>VectorStoreIndex.from_documents(docs)</code>?"),
             "answer": L("写入路径三步合一：把每个 Document 切块成 Node → 用 embed_model 把每个 Node 向量化 → 把向量与 Node 写入索引。它是 <code>BaseIndex.from_documents</code> 提供的快捷方式。",
                         "Three write-path steps in one: chunk each Document into Nodes → embed each Node via embed_model → write vectors and Nodes into the index. It's the shortcut from <code>BaseIndex.from_documents</code>.")},
            {"q": L("写入路径做一次、查询路径做很多次——这对你的部署架构意味着什么？",
                    "The write path runs once, the query path many times — what does that mean for your deployment?"),
             "answer": L("建索引可放离线/批处理、结果用 <code>persist</code> 落盘；查询在线、要低延迟、复用同一索引。把“建一次”与“问多次”分开，才能各自扩容（如查询侧无状态水平扩展）。",
                         "Index-building can be offline/batch with results <code>persist</code>ed; querying is online, latency-sensitive, reusing the same index. Separating 'build once' from 'ask many' lets each scale independently (e.g. stateless horizontal scaling on the query side).")},
            {"q": L("如果同一个索引要服务上千 QPS，你会缓存或持久化哪一步？为什么？",
                    "If one index must serve thousands of QPS, which step would you cache or persist, and why?"),
             "answer": L("持久化索引本身（<code>persist</code> + <code>load_index_from_storage</code>），避免每次启动重新切块/向量化；向量库交给可托管的生产库；查询路径尽量无状态，便于水平扩展。",
                         "Persist the index itself (<code>persist</code> + <code>load_index_from_storage</code>) so you never re-chunk/re-embed on startup; move the vector store to a managed production DB; keep the query path stateless to scale out.")},
            {"q": L("高层 API（5 行）和手装低层管道是什么关系？什么时候该“下沉”到低层？",
                    "How do the 5-line high-level API and the hand-wired low-level pipeline relate, and when should you drop down?"),
             "answer": L("高层 API 只是低层管道默认装配的快捷方式，二者共享同一套对象。当你要自定义某一站——换检索器、加后处理、改合成策略或 prompt——就用 <code>from_args</code> 等低层入口拆开装配。",
                         "The high-level API is just a shortcut over the low-level pipeline's default wiring; both share the same objects. Drop down (e.g. <code>from_args</code>) when you need to customize a stop — swap the retriever, add postprocessing, change synthesis or the prompt.")},
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
        "interview": [
            {"q": L("为什么 RAG 的检索单位是 <code>Node</code> 而不是整篇 <code>Document</code>？",
                    "Why is the unit of retrieval a <code>Node</code> rather than the whole <code>Document</code>?"),
             "answer": L("整篇文档里通常只有一两段相关，把整篇压成<strong>一个</strong>向量会被无关内容稀释、命中不准；切成 Node 后检索更精准，且 Node 携带 metadata 与 relationships，让下游“说同一种语言”。",
                         "A whole doc is usually relevant only in a paragraph or two; squeezing it into <strong>one</strong> vector dilutes the signal. Nodes make retrieval precise and carry metadata + relationships so everything downstream speaks one language.")},
            {"q": L("<code>relationships</code>（SOURCE / PREVIOUS / NEXT）在什么真实需求下派上用场？",
                    "When do <code>relationships</code> (SOURCE / PREVIOUS / NEXT) actually earn their keep?"),
             "answer": L("溯源（SOURCE 指回原 Document）、前后文扩展（命中一个 Node 时把相邻 Node 一起带上，避免断句）、以及句窗/自动合并等进阶检索的基础。",
                         "Provenance (SOURCE points back to the Document), prev/next context expansion (pull neighbors so a hit isn't a half-sentence), and as the basis for sentence-window / auto-merging retrieval.")},
            {"q": L("如果有人坚持“直接用整篇文档做检索更省事”，你会用什么例子反驳？",
                    "If someone insists 'just retrieve whole documents, it's simpler', how would you push back with an example?"),
             "answer": L("一份 50 页手册里只有半页讲退款：整篇的向量被另外 49.5 页稀释，查“退款”可能根本排不进 top-k；即便命中，也要把 50 页塞进 LLM，既贵又“迷失在中间”。",
                         "A 50-page manual with half a page on refunds: the doc vector is drowned by the other 49.5 pages, so 'refund' may not even rank into top-k; and even if it hits, you'd feed 50 pages to the LLM — costly and 'lost in the middle'.")},
            {"q": L("检索老是返回相关但不对的段落，<code>metadata</code> 能怎样帮你收窄？",
                    "Retrieval keeps returning related-but-wrong chunks — how can <code>metadata</code> help narrow it?"),
             "answer": L("用 metadata 过滤（如 <code>MetadataFilters</code> 限定 <code>product=&quot;X&quot;</code> 或 <code>year=2024</code>）把检索范围先缩到对的子集，相当于“先按标签筛、再按语义排”，是向量检索的第二通道。",
                         "Filter by metadata (e.g. <code>MetadataFilters</code> for <code>product=&quot;X&quot;</code> or <code>year=2024</code>) to restrict retrieval to the right subset — 'filter by tag, then rank by meaning', the second channel alongside vectors.")},
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
        "interview": [
            {"q": L("Reader 的统一产出是什么？为什么这层抽象对整条管道很关键？",
                    "What do all Readers output, and why does that abstraction matter for the whole pipeline?"),
             "answer": L("统一产出 <code>Document</code> 列表。它把“来源千奇百怪”挡在管道之外——换数据源（PDF→网页→数据库）不影响后续切块/向量化/检索任何一站，是 RAG 可组合性的起点。",
                         "A list of <code>Document</code>s. It keeps source quirks out of the pipeline — changing the source (PDF→web→DB) touches no later stage, which is where RAG composability begins.")},
            {"q": L("一个 PDF 常常每页产出一个 Document，<code>len(docs) ≠ 文件数</code>。这会影响你设计什么？",
                    "A PDF often yields one Document per page, so <code>len(docs) ≠ file count</code>. What design choices does that affect?"),
             "answer": L("影响下游 Node 数量与“引用到第几页”的溯源粒度；做引用脚注/页码定位时要靠每个 Document 的 metadata（page）；估算 embedding 成本也要按 Document/Node 数而非文件数。",
                         "It drives the downstream Node count and page-level citation granularity; footnotes/page anchors rely on each Document's <code>page</code> metadata; and you estimate embedding cost by Document/Node count, not file count.")},
            {"q": L("自己写一个 Reader vs 用 LlamaHub 现成集成，你怎么选？",
                    "Writing your own Reader vs using an off-the-shelf LlamaHub integration — how do you choose?"),
             "answer": L("常见格式/来源（PDF、网页、Notion、S3…）优先用现成集成，省事且久经测试；只有内部专有格式或需要特殊清洗/分块逻辑时才自写——只要实现 <code>BaseReader.load_data</code> 返回 Document 即可接入。",
                         "Prefer existing integrations for common formats/sources (PDF, web, Notion, S3…) — battle-tested and quick; write your own only for proprietary formats or special cleaning/splitting, implementing <code>BaseReader.load_data</code> to return Documents.")},
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
        "interview": [
            {"q": L("<code>chunk_size</code> 太大、太小各会出什么问题？你会怎么定它？",
                    "What goes wrong if <code>chunk_size</code> is too large vs too small, and how do you set it?"),
             "answer": L("太大：块里混入无关内容、检索噪声多、还挤占 LLM 上下文；太小：完整语义被切碎、块间断裂读不成句。定法：看内容结构（手册偏小、叙事偏大），并受 embedding token 上限约束（多在 512 左右），最后用评估调。",
                         "Too large: irrelevant content, noisy retrieval, and it hogs LLM context; too small: complete thoughts get shredded. Set it by content structure (manuals smaller, narrative larger), bounded by the embedding token limit (~512), then tune via evaluation.")},
            {"q": L("<code>chunk_overlap</code> 解决什么问题？把它设为 0 会怎样？",
                    "What problem does <code>chunk_overlap</code> solve, and what happens if you set it to 0?"),
             "answer": L("让相邻块共享边界句，避免把一句话从中间切断。设为 0 时，跨块的句子可能两边都答不全（“7 个工作” | “日内到账”），检索命中任一块都拿不到完整语义。",
                         "It makes adjacent chunks share boundary sentences so a thought isn't cut in half. At 0, a sentence split across chunks is incomplete on both sides, so hitting either chunk loses the full meaning.")},
            {"q": L("sentence-window 是怎么同时做到“检索精准”和“上下文完整”的？",
                    "How does sentence-window get both precise retrieval and full context at once?"),
             "answer": L("它把<strong>检索单位</strong>和<strong>喂给 LLM 的单位</strong>解耦：以单句为 Node 去检索（足够精准），命中后用 <code>MetadataReplacementPostProcessor</code> 把单句换成它前后句组成的 window 再交给 LLM（补回上下文）。",
                         "It decouples the <strong>retrieval unit</strong> from the <strong>unit fed to the LLM</strong>: retrieve on single sentences (precise), then on a hit swap the sentence for its surrounding window via <code>MetadataReplacementPostProcessor</code> before generation (full context).")},
            {"q": L("SentenceSplitter / TokenTextSplitter / SemanticSplitterNodeParser 各适合什么场景？",
                    "When would you reach for SentenceSplitter vs TokenTextSplitter vs SemanticSplitterNodeParser?"),
             "answer": L("SentenceSplitter：通用默认，按句凑到 chunk_size、不切断句子；TokenTextSplitter：要严格控长（贴 token 预算）时；SemanticSplitter：主题多变的长文，按语义断点切，块更内聚但更慢、更贵。",
                         "SentenceSplitter: the general default, packs sentences up to chunk_size without cutting them; TokenTextSplitter: when you need strict length control against a token budget; SemanticSplitter: topically varied long text, splitting at semantic breakpoints — more coherent but slower and costlier.")},
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
        "interview": [
            {"q": L("为什么说元数据是“检索的第二通道”？举一个它比纯向量更管用的例子。",
                    "Why call metadata the 'second channel' of retrieval? Give a case where it beats pure vectors."),
             "answer": L("纯向量按语义排序，但答不了“只在 2024 年的合同里找”这类结构化约束。metadata 既能<strong>过滤</strong>（年份/产品/部门），又能让“问句”与“块”对齐（如 questions_this_excerpt_can_answer）——这是向量之外的第二条命中路径。",
                         "Vectors rank by meaning but can't honor structured constraints like 'only 2024 contracts'. Metadata both <strong>filters</strong> (year/product/dept) and aligns questions with chunks (e.g. questions_this_excerpt_can_answer) — a second hit path beyond vectors.")},
            {"q": L("LLM 抽取元数据是有成本的。你怎么决定哪些字段用 LLM 抽、哪些不用？",
                    "LLM extraction costs money. How do you decide which metadata to extract with an LLM vs not?"),
             "answer": L("确定性、来源已知的字段（文件名、页码、日期、部门）直接在 Reader 阶段手写，零成本；只有需要“理解内容”才产生的字段（摘要、关键词、可回答的问题）才值得花 LLM。还要权衡：N 个块逐块抽就是 N 次调用，文档级抽取器（TitleExtractor）则约每文档一次。",
                         "Deterministic, known fields (filename, page, date, dept) are hand-written at the Reader stage for free; only fields that require 'understanding' the content (summary, keywords, answerable questions) justify an LLM. Mind the cost: per-chunk extractors cost N calls, while document-level ones (TitleExtractor) run ~once per doc.")},
            {"q": L("<code>excluded_embed_metadata_keys</code> 是干嘛的？什么时候必须用它？",
                    "What is <code>excluded_embed_metadata_keys</code> for, and when must you use it?"),
             "answer": L("控制哪些 metadata <strong>不</strong>拼进被 embedding 的文本。当某些字段（如长 URL、内部 ID、时间戳）会污染语义向量、拉偏相似度时，就排除它们——保留用于过滤/展示，但不进 embedding。",
                         "It controls which metadata is <strong>not</strong> concatenated into the text that gets embedded. Exclude fields (long URLs, internal IDs, timestamps) that would pollute the semantic vector and skew similarity — keep them for filtering/display, but out of the embedding.")},
            {"q": L("<code>questions_this_excerpt_can_answer</code> 为什么能提升召回？背后的直觉是什么？",
                    "Why does <code>questions_this_excerpt_can_answer</code> lift recall? What's the intuition?"),
             "answer": L("用户用<strong>问句</strong>检索，而文档块多是<strong>陈述句</strong>，两者在向量空间未必靠得近。预先为块生成“它能回答的问题”并一并 embedding，相当于把“问”和“答”在语义空间对齐，命中率更高。",
                         "Users search with <strong>questions</strong>, but chunks are usually <strong>statements</strong> — not always close in vector space. Pre-generating the questions a chunk can answer and embedding them aligns 'question' with 'answer' in semantic space, raising hit rate.")},
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
    interviews = data.get("interview", [])
    if interviews:
        ihead = i18n.t("🎯 面试官提问 · 试着答出要点", "🎯 Interviewer asks · cover the key points")
        reveal = i18n.t("看参考要点", "Show key points")
        hint = i18n.t("点击展开", "expand")
        out.append(f"<h3>{ihead}</h3>")
        for j, item in enumerate(interviews, 1):
            out.append(
                f'<div class="quiz interview">\n'
                f'  <div class="qn">🎯 {j}. {i18n.render(item["q"], block=False)}</div>\n'
                f'  <details class="accordion">\n'
                f'    <summary>{reveal} <span class="hint">{hint}</span></summary>\n'
                f'    <div class="acc-body"><div class="qa"><div class="a">'
                f'{i18n.render(item["answer"], block=False)}'
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
