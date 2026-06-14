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
            {"q": L("写入路径（建索引）和查询路径（问答）在你的系统里该分别跑在哪里、用什么节奏？为什么不该每次提问都重建索引？",
                    "Where and at what cadence should the write path (indexing) vs query path (answering) run, and why not rebuild the index on every question?"),
             "answer": L("写入路径重、做一次：放离线/批处理或后台任务，产物用 <code>persist</code> 落盘；查询路径轻、做多次：在线、低延迟、复用同一索引。每次提问都重建＝把 O(语料) 的工作塞进每个请求，又慢又烧钱，还无法水平扩展。",
                         "The write path is heavy and runs once: offline/batch or a background job, with results <code>persist</code>ed; the query path is light and runs many times: online, low-latency, reusing the index. Rebuilding per question forces O(corpus) work into every request — slow, costly, and impossible to scale out.")},
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
             "answer": L("确定性、来源已知的字段（文件名、页码、日期、部门）直接在 Reader 阶段手写，零成本；只有需要“理解内容”才产生的字段（摘要、关键词、可回答的问题）才值得花 LLM。还要权衡：逐块抽取器对 N 个块约 N 次调用，而文档级抽取器（TitleExtractor）只看每篇文档<strong>前几个节点</strong>——几次调用加一次汇总，与总块数无关。",
                         "Deterministic, known fields (filename, page, date, dept) are hand-written at the Reader stage for free; only fields that require 'understanding' the content (summary, keywords, answerable questions) justify an LLM. Mind the cost: per-chunk extractors cost ~N calls, while document-level ones (TitleExtractor) look at only the <strong>first few nodes</strong> per doc — a handful of calls plus a combine, independent of total chunk count.")},
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
        "interview": [
            {"q": L("为什么向量检索能懂“同义不同词”，而关键词匹配不能？",
                    "Why can vector search catch paraphrases ('same meaning, different words') when keyword matching can't?"),
             "answer": L("Embedding 把文本映射到向量空间，使<strong>语义相近 = 向量距离近</strong>（按余弦/夹角度量）。所以“退款要多久”能命中“几天到账”——它们用词不同但语义相邻；关键词匹配只看字面重叠，错过同义改写。",
                         "Embeddings map text into a space where <strong>similar meaning = nearby vectors</strong> (by cosine/angle). So 'how long for a refund' matches 'arrives in a few days' — different words, adjacent meaning; keyword matching sees only literal overlap and misses paraphrases.")},
            {"q": L("为什么查询和文档<strong>必须</strong>用同一个 embedding 模型？不一致会怎样？",
                    "Why <strong>must</strong> the query and documents use the same embedding model? What breaks otherwise?"),
             "answer": L("不同模型产生不同的坐标系，两套向量不可比，算出的相似度毫无意义、检索基本失效。这也是为什么换 embedding 模型必须重建索引——旧向量要用新模型全部重算。",
                         "Different models produce different coordinate systems; the two sets of vectors aren't comparable, so similarities are meaningless and retrieval collapses. It's also why swapping the embedding model forces a full re-index — old vectors must be recomputed.")},
            {"q": L("“换一个更强的 embedding 模型就能提升召回”——这句话哪里不严谨？",
                    "'Just switch to a stronger embedding model and recall improves' — what's sloppy about that claim?"),
             "answer": L("更强的<strong>通用</strong>模型未必在<strong>你的领域</strong>更好——领域/微调的小模型常反超。且换模型要重建整个索引（成本）、可能改变维度与相似度分布。该用评估集量化，而不是默认“更大=更好”。",
                         "A stronger <strong>general</strong> model isn't always better in <strong>your domain</strong> — domain/fine-tuned smaller models often win. And switching forces a full re-index (cost) and can change dimensions/score distributions. Measure with an eval set rather than assuming 'bigger = better'.")},
            {"q": L("RAG 召回差，你怎么判断是 embedding 的问题，还是切块/检索的问题？",
                    "Recall is poor — how do you tell whether it's the embedding vs the chunking/retrieval?"),
             "answer": L("先看 <code>retrieve()</code> 的 top-k：正确块根本没进来→可能是切块太碎/太粗或 embedding 不贴领域；正确块进来了但排名靠后→调 top_k 或加 rerank。可用一组带“标准答案块”的查询量化命中率，分别替换变量验证。",
                         "Inspect the top-k from <code>retrieve()</code>: the right chunk never appears → likely bad chunking or an off-domain embedding; it appears but ranks low → tune top_k or add a reranker. Quantify hit-rate with queries that have known gold chunks, swapping one variable at a time.")},
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
        "interview": [
            {"q": L("一个 VectorStore 要承担哪三件事？为什么把它抽象成可替换接口很重要？",
                    "What three jobs does a VectorStore do, and why abstract it behind a swappable interface?"),
             "answer": L("存向量、存（可过滤的）metadata、做近邻查询（给定查询向量返回 top-k）。统一接口（<code>VectorStoreQuery</code> 契约）让“原型用内存版、生产换 Chroma/pgvector”只是换实现、不改链路——选库变成运维/规模问题而非架构问题。",
                         "Store vectors, store (filterable) metadata, and do nearest-neighbor search (given a query vector, return top-k). A uniform interface (the <code>VectorStoreQuery</code> contract) makes 'prototype in-memory, ship on Chroma/pgvector' a swap of implementation — choosing a store becomes an ops/scale decision, not an architectural one.")},
            {"q": L("<code>SimpleVectorStore</code> 和生产向量库（Chroma / FAISS / pgvector）你按什么标准选？",
                    "How do you choose between <code>SimpleVectorStore</code> and a production store (Chroma / FAISS / pgvector)?"),
             "answer": L("规模与持久化（内存版重启即失、不适合大库）、元数据过滤能力、是“库”还是“服务”、事务/一致性、运维成本。例：FAISS 极快但偏库；pgvector 复用现成 Postgres、便于事务；Chroma 开箱即用。",
                         "Scale and persistence (in-memory dies on restart), metadata filtering, library-vs-service, transactions/consistency, and ops cost. E.g. FAISS is blazing but library-style; pgvector reuses existing Postgres with transactions; Chroma is batteries-included.")},
            {"q": L("生产向量库号称“百万级毫秒查询”，靠的是什么？代价是什么？",
                    "Production stores boast 'millisecond queries at million-scale' — how, and at what cost?"),
             "answer": L("靠<strong>近似最近邻（ANN）</strong>索引（如 HNSW/IVF），用近似换速度——并不保证 100% 召回。召回率可通过参数调（更高召回=更慢/更耗内存）。精确扫描虽 100% 准确，但在大规模下太慢。",
                         "Via <strong>Approximate Nearest Neighbor (ANN)</strong> indexes (HNSW/IVF) that trade exactness for speed — recall isn't guaranteed 100%. Recall is a tunable knob (higher recall = slower/more memory). Exact scan is 100% accurate but too slow at scale.")},
            {"q": L("既要语义检索、又要“只在某部门/某年份里找”，你会怎么实现？",
                    "You need semantic search AND 'only within a dept/year' — how do you implement it?"),
             "answer": L("用 <code>MetadataFilters</code> 把检索先约束到对的子集，再在子集里做向量近邻——即“先按标签筛、再按语义排”。前提是建索引时把这些字段写进 Node 的 metadata。",
                         "Use <code>MetadataFilters</code> to constrain retrieval to the right subset, then do vector nearest-neighbor within it — 'filter by tag, then rank by meaning'. It works only if those fields were written into each Node's metadata at index time.")},
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
        "interview": [
            {"q": L("为什么说“选 Index = 选检索范式”？Index 和向量库是一回事吗？",
                    "Why is 'choosing an Index = choosing a retrieval paradigm'? Is an Index the same as a vector store?"),
             "answer": L("不是。向量库是<strong>存储</strong>；Index 是<strong>为某种检索方式组织 Node 的结构</strong>，它决定的不是“存哪儿”而是“怎么找”。VectorStoreIndex 按相似度定点召回，SummaryIndex 遍历全部做总结——选 Index 就选定了检索行为。",
                         "No. A vector store is <strong>storage</strong>; an Index is a <strong>structure that organizes Nodes for a retrieval style</strong> — it decides not 'where things live' but 'how you find them'. VectorStoreIndex pinpoints by similarity; SummaryIndex walks everything to summarize. Choosing the Index fixes the retrieval behavior.")},
            {"q": L("定点 FAQ 问答 vs 整篇合同的全局摘要，你分别选哪种 Index？为什么？",
                    "Pinpoint FAQ Q&amp;A vs a global summary of a whole contract — which Index for each, and why?"),
             "answer": L("FAQ → VectorStoreIndex：问题指向某几段，按相似度取 top-k 最省、最准。全局摘要 → SummaryIndex + <code>response_mode='tree_summarize'</code>：需要看<strong>全部</strong>内容再逐层合并，定点检索反而会漏。",
                         "FAQ → VectorStoreIndex: the question targets a few chunks, so top-k by similarity is cheapest and most precise. Global summary → SummaryIndex with <code>response_mode='tree_summarize'</code>: you must see <strong>all</strong> content and merge it up; pinpoint retrieval would miss parts.")},
            {"q": L("一个知识库里既有定点 FAQ、又要支持“整库总结”，怎么办？",
                    "One knowledge base needs both pinpoint FAQ and 'summarize the whole base' — how do you handle it?"),
             "answer": L("建多个 Index（向量索引 + 摘要索引），用 <code>RouterQueryEngine</code> 按问题自动路由到合适的那个；或用 <code>QueryEngineTool</code> 把它们包成工具交给上层选择。一个 Index 难以同时擅长两种范式。",
                         "Build multiple indices (vector + summary) and let a <code>RouterQueryEngine</code> route each question to the right one; or wrap them as <code>QueryEngineTool</code>s for an upper layer to choose. One Index can't excel at both paradigms.")},
            {"q": L("四种 Index 都通过同一个 <code>from_documents</code> 入口构建，这种统一带来什么好处？",
                    "All four Index types build via the same <code>from_documents</code> entry — what does that uniformity buy?"),
             "answer": L("可替换性：换检索范式只换 Index 类、上层 <code>as_query_engine()</code> 用法不变；学习与组合成本低；也便于做 Router 这类“多 Index 一致调度”的上层抽象。",
                         "Interchangeability: switching paradigm means switching the Index class while the upstream <code>as_query_engine()</code> usage stays; low learning/composition cost; and it enables 'uniformly dispatch many indices' abstractions like the Router.")},
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
        "interview": [
            {"q": L("IngestionPipeline 的缓存与去重，让“重建索引”的代价正比于什么？为什么这在生产里重要？",
                    "With IngestionPipeline's caching and dedup, the cost of 're-indexing' is proportional to what — and why does that matter in production?"),
             "answer": L("正比于<strong>变化量</strong>而非总量：没变的块命中缓存、跳过切块/向量化；docstore 按内容哈希去重。生产里知识库天天小幅更新，全量重建既慢又烧钱，增量摄取才可持续。",
                         "Proportional to the <strong>delta</strong>, not the total: unchanged chunks hit the cache and skip split/embed; the docstore dedups by content hash. In production the base changes a little daily, so full rebuilds are slow and costly — incremental ingestion is what scales.")},
            {"q": L("<code>persist</code> 到底把索引存成了哪几件？换成生产向量库后有什么不同？",
                    "What does <code>persist</code> actually write to disk, and how does that change with a production vector store?"),
             "answer": L("默认落盘三件套：docstore（Node 内容）、index store（索引结构）、vector store（向量）。换成 Chroma/pgvector 后，向量由<strong>外部数据库</strong>托管，本地不再是那个 vector_store.json——加载时要连回同一个库。",
                         "By default three pieces: the docstore (Node content), the index store (index structure), and the vector store (vectors). With Chroma/pgvector the vectors live in an <strong>external DB</strong>, so it's no longer a local vector_store.json — loading must reconnect to that same store.")},
            {"q": L("一篇文档更新了，你怎么做到“只重算那一篇”，而不是整库重建？",
                    "A single document changed — how do you recompute only that one instead of rebuilding everything?"),
             "answer": L("给 IngestionPipeline 配 docstore 并用 <code>DocstoreStrategy</code>：再次 run 同一批文档时，未变的命中缓存/被去重，只有内容变化的文档触发重新切块与向量化。前提是文档有稳定的 id（如 ref_doc_id）。",
                         "Give the IngestionPipeline a docstore with a <code>DocstoreStrategy</code>: on a re-run, unchanged docs hit the cache / are deduped, and only changed docs trigger re-split and re-embed. It relies on stable doc ids (e.g. ref_doc_id).")},
            {"q": L("把建索引做成“幂等管道”而不是一次性脚本，实际解决了哪些工程问题？",
                    "Making indexing an 'idempotent pipeline' rather than a one-off script solves which engineering problems?"),
             "answer": L("可重跑而不重复劳动（幂等）、增量更新、失败可恢复、成本可控、可纳入 CI/定时任务。本质是把“建索引”从一次性动作变成可维护、可观测的生产管道。",
                         "Re-runnable without redoing work (idempotent), incremental updates, recoverable from failures, controlled cost, and fit for CI/scheduled jobs. Essentially it turns 'build the index' from a one-shot action into a maintainable, observable production pipeline.")},
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
        "interview": [
            {"q": L("Retriever 只检索、不生成。把检索单独拎出来，最大的工程好处是什么？",
                    "A Retriever only retrieves, no generation. What's the biggest engineering benefit of isolating it?"),
             "answer": L("可以<strong>脱离 LLM 单独评估与优化召回</strong>：直接看 <code>retrieve()</code> 返回的 Node 有没有命中正确依据，用 hit-rate/MRR 量化。于是调 top_k、换 embedding、改切块都能秒级验证，不必每次跑昂贵的生成。",
                         "You can <strong>evaluate and optimize recall without the LLM</strong>: inspect whether the Nodes from <code>retrieve()</code> contain the right evidence, quantified by hit-rate/MRR. Then tuning top_k, embedding or chunking is verified instantly, without paying for generation.")},
            {"q": L("向量检索漏掉了一个含精确型号“X-2000”的关键段落——字面明明就在文档里。为什么会漏？怎么补救？",
                    "Vector search missed a key passage with the exact part number 'X-2000' — even though it's literally in the docs. Why, and how do you fix it?"),
             "answer": L("向量化偏“语义”，对精确符号/罕见 token/型号/代码不敏感——语义上“X-2000”与别的型号很近，可能排不进 top-k。补救：混合检索（向量 + BM25/关键词，把精确匹配召回回来）、把型号存进 metadata 做精确过滤、或对这类查询加 rerank。",
                         "Embeddings capture meaning and are weak on exact symbols/rare tokens/part numbers/code — semantically 'X-2000' sits near other models and may miss top-k. Fixes: hybrid retrieval (vector + BM25/keyword to recover exact matches), store the part number in metadata for exact filtering, or add a reranker for such queries.")},
            {"q": L("检索分数普遍偏低，你会先调 <code>top_k</code>、换 embedding，还是改切块？怎么定位？",
                    "Scores are uniformly low — would you tune <code>top_k</code>, swap the embedding, or re-chunk first? How do you localize it?"),
             "answer": L("调 top_k 不改变分数高低，只改数量，所以不是第一手。先看正确块是否进了 top-k：没进→多半是切块太碎/太粗或 embedding 不贴领域；进了但分低→可能是 query 与 doc 表述差距大（考虑 HyDE/改写）。用带 gold 块的查询逐一验证。",
                         "Tuning top_k changes count, not scores, so it's not the first move. Check whether the right chunk is even in top-k: not there → likely bad chunking or off-domain embedding; there but low → query/doc phrasing gap (consider HyDE/rewriting). Verify with gold-chunk queries, one variable at a time.")},
            {"q": L("<code>similarity_top_k</code> 太小、太大各有什么代价？通常从多少起步？",
                    "What are the costs of <code>similarity_top_k</code> too small vs too large, and where do you start?"),
             "answer": L("太小→漏召回，答案残缺；太大→引入低相关噪声、占上下文、稀释答案、增成本。常从 3–5 起步，再配合后处理（cutoff/rerank）“先多取、再筛精”。",
                         "Too small → missed recall, incomplete answers; too large → low-relevance noise that eats context, dilutes the answer and raises cost. Start around 3–5, then pair with post-processing (cutoff/rerank) to 'fetch wide, then trim'.")},
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
        "interview": [
            {"q": L("为什么说后处理是 RAG 调优里“性价比最高”的一环？",
                    "Why is post-processing the 'best bang-for-buck' step in RAG tuning?"),
             "answer": L("它在“检索之后、生成之前”，多为非 LLM 的轻量操作（打分阈值、窗口替换）或一次轻调用（rerank），却能去噪、补上下文、显著提升答案——<strong>不重训、不换模型</strong>，改动小、见效快。",
                         "It sits 'after retrieval, before generation' and is mostly lightweight non-LLM work (score thresholds, window replacement) or one light call (rerank), yet it denoises and restores context for a clear quality lift — <strong>no retraining, no model swap</strong>.")},
            {"q": L("<code>similarity_cutoff</code> 设太高、太低各会怎样？你用什么信号来定它？",
                    "What happens if <code>similarity_cutoff</code> is too high vs too low, and what signal sets it?"),
             "answer": L("太高→把相关块也误杀、召回不足；太低→噪声混进生成。定法：看一批查询里相关/不相关块的<strong>分数分布</strong>，把阈值卡在两者之间的“谷”；不同 embedding 模型的分数尺度不同，阈值要按模型重标，别照搬。",
                         "Too high → kills relevant chunks, under-recall; too low → noise reaches generation. Set it from the <strong>score distribution</strong> of relevant vs irrelevant chunks across sample queries, placing the threshold in the valley between them. Score scales differ per embedding model, so re-calibrate rather than copy a number.")},
            {"q": L("阈值过滤和交叉编码器 rerank，分别什么时候用？",
                    "When do you use threshold filtering vs cross-encoder reranking?"),
             "answer": L("阈值过滤便宜但粗糙，适合先砍掉明显低分；rerank（Cohere/LLM）更准——它用更强模型对 query-doc 配对重新打分，能纠正向量召回的排序错误，但要额外一次调用、更慢更贵。常组合：先 top_k 多取 → cutoff 粗筛 → rerank 精排。",
                         "Threshold filtering is cheap but blunt — good for cutting obvious low scores; reranking (Cohere/LLM) is more accurate, re-scoring query-doc pairs with a stronger model to fix vector-ranking mistakes, but costs an extra slower call. Often combined: fetch wide → cutoff → rerank.")},
            {"q": L("句窗（sentence-window）+ <code>MetadataReplacementPostProcessor</code> 解决了什么矛盾？",
                    "What tension do sentence-window + <code>MetadataReplacementPostProcessor</code> resolve together?"),
             "answer": L("“检索要精准（小块）”与“生成要上下文（大块）”的矛盾：以单句检索保证精准，命中后用后处理把单句替换成它前后句的 window 再喂给 LLM，等于检索粒度和喂入粒度解耦。",
                         "The clash between 'retrieve precisely (small)' and 'generate with context (large)': retrieve on single sentences for precision, then post-process replaces the hit sentence with its surrounding window before generation — decoupling retrieval granularity from what the LLM reads.")},
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
        "interview": [
            {"q": L("“多片段 → 单答案”的核心矛盾是什么？ResponseMode 本质在权衡什么？",
                    "What's the core tension of 'many chunks → one answer'? What does the ResponseMode fundamentally trade off?"),
             "answer": L("检索到的片段可能<strong>装不进一次上下文窗口</strong>。选 mode 本质是在“上下文窗口大小”和“片段数量”之间取舍——要么塞满一次写，要么分批迭代/分层合并。",
                         "The retrieved chunks may <strong>not fit in one context window</strong>. Choosing a mode is fundamentally a trade-off between 'context window size' and 'number of chunks' — pack-and-write-once vs iterate/merge in batches.")},
            {"q": L("compact / refine / tree_summarize / accumulate 各适合什么问题？",
                    "Which problem suits compact vs refine vs tree_summarize vs accumulate?"),
             "answer": L("compact（默认）：通用问答、省调用，尽量塞满再生成；refine：片段多、需细读，逐块迭代精炼；tree_summarize：全局总结类，分组逐层向上合并；accumulate：逐条抽取、每块各答再汇总。",
                         "compact (default): general Q&amp;A, fewer calls, pack then generate; refine: many chunks needing careful reading, iterate chunk by chunk; tree_summarize: global summaries, merge up a tree; accumulate: per-chunk extraction, answer each then collect.")},
            {"q": L("<code>compact</code> 实际上是什么？为什么把它设为默认？",
                    "What is <code>compact</code> actually, and why is it the default?"),
             "answer": L("它其实是 compact_and_refine：先把尽量多的片段塞满一个 prompt（减少调用次数），装不下时再退回 refine 的逐块迭代。兼顾省钱与不丢信息，所以适合做通用默认。",
                         "It's really compact_and_refine: pack as many chunks as fit into one prompt (fewer calls), falling back to refine's chunk-by-chunk iteration when they don't all fit. It balances cost and completeness, making it a sensible default.")},
            {"q": L("上下文窗口很小但片段很多时，refine 和 compact 各付出什么代价？",
                    "With a small context window but many chunks, what does refine cost vs compact?"),
             "answer": L("refine 要对每个片段各调一次 LLM——调用多、慢、贵，但每段都读到；compact 尽量合并、调用少，但窗口小的时候能塞进的片段有限，可能漏掉信息或频繁退化为 refine。窗口小+片段多正是两者矛盾最尖锐处。",
                         "refine calls the LLM once per chunk — many calls, slow and costly, but every chunk is read; compact merges to cut calls, but a small window limits how much fits, risking dropped info or frequent fallback to refine. Small window + many chunks is exactly where the tension peaks.")},
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
        "interview": [
            {"q": L("为什么把 QueryEngine 叫“组合根”？它把哪三件正交的组件装在一起？",
                    "Why call the QueryEngine a 'composition root'? Which three orthogonal components does it assemble?"),
             "answer": L("检索器、后处理器、合成器——三者正交（换检索器不影响合成、加后处理不影响检索）。QueryEngine 只负责把它们装配起来、对外暴露一个 <code>.query()</code>。理解这个组合根，就能把“默认问答”改造成任意 RAG 变体。",
                         "The retriever, postprocessors and synthesizer — orthogonal (swapping the retriever doesn't touch synthesis; adding postprocessing doesn't touch retrieval). The QueryEngine just wires them behind one <code>.query()</code>. Grasp this root and you can reshape default Q&amp;A into any variant.")},
            {"q": L("<code>as_query_engine()</code> 和 <code>RetrieverQueryEngine.from_args()</code> 有何区别？什么时候用后者？",
                    "How do <code>as_query_engine()</code> and <code>RetrieverQueryEngine.from_args()</code> differ, and when do you use the latter?"),
             "answer": L("两者产出<strong>同一种 QueryEngine</strong>，只是装配深度不同：前者用默认装配、一行起步；后者让你逐件指定检索器/后处理/合成器。需要自定义任一组件（自建 retriever、加 cutoff/rerank、换合成策略）时用 from_args。",
                         "Both yield the <strong>same kind of QueryEngine</strong>, differing only in wiring depth: the former is one-line default wiring; the latter lets you specify each of retriever/postprocessors/synthesizer. Use from_args when customizing any component (custom retriever, add cutoff/rerank, change synthesis).")},
            {"q": L("要把“默认问答”改造成“只引用、不编造”的客服引擎，你会替换或新增哪几件组件？",
                    "To turn default Q&amp;A into a 'cite-only, never invent' support engine, which components would you change or add?"),
             "answer": L("① 合成器换更严的 <code>text_qa_template</code>（“只依据资料、未提及就说不知道、给出处”）；② 加后处理 SimilarityPostprocessor/rerank 提纯依据；③ 在响应里渲染 <code>source_nodes</code> 做脚注；④ 挂 Faithfulness 评估当上线前质量闸。骨架（QueryEngine）不变。",
                         "(1) a stricter <code>text_qa_template</code> in the synthesizer ('answer only from sources, say unknown otherwise, cite'); (2) a SimilarityPostprocessor/rerank to purify evidence; (3) render <code>source_nodes</code> as footnotes; (4) attach a Faithfulness evaluator as a pre-launch gate. The QueryEngine skeleton stays.")},
            {"q": L("一次 <code>.query()</code> 内部依次发生了什么？",
                    "What happens, in order, inside a single <code>.query()</code> call?"),
             "answer": L("<code>retrieve()</code> 取 top-k NodeWithScore → 过一遍 node_postprocessors（过滤/重排/替换）→ <code>synthesize()</code> 把精选片段合成答案 → 返回 Response（answer + source_nodes）。",
                         "<code>retrieve()</code> fetches top-k NodeWithScore → runs node_postprocessors (filter/rerank/replace) → <code>synthesize()</code> fuses the curated chunks into an answer → returns a Response (answer + source_nodes).")},
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
        "interview": [
            {"q": L("多轮 RAG 的两个真正难点是什么？为什么说聊天不只是“给 QueryEngine 套个循环”？",
                    "What are the two real hard parts of multi-turn RAG, and why is chat more than 'a loop around a QueryEngine'?"),
             "answer": L("① 指代消解——“它/那/上面说的”要先还原成具体所指；② 用<strong>哪个问题</strong>去检索——原话还是消解补全后的独立问题。直接套循环既解析不了指代、检索也会被残缺的追问带偏。",
                         "(1) Coreference — 'it / that / the one above' must resolve to a concrete referent; (2) <strong>which question</strong> to retrieve with — the raw turn or a condensed standalone query. A naive loop neither resolves references nor retrieves well on a fragmentary follow-up.")},
            {"q": L("<code>condense_question</code> 和 <code>context</code> 都是每轮都检索吗？“要不要检索”由谁决定？",
                    "Do <code>condense_question</code> and <code>context</code> both retrieve every turn? Who decides whether to retrieve at all?"),
             "answer": L("是的，两者都<strong>每轮检索</strong>（context 总是检索注入；condense 先把历史+新问压成独立问题再检索）。真正“按需决定要不要检索”是 <strong>agent/router</strong> 的能力，不是这两个 mode。",
                         "Yes — both <strong>retrieve every turn</strong> (context always retrieves and injects; condense first compresses history+question into a standalone query, then retrieves). Deciding <strong>whether</strong> to retrieve on demand is an <strong>agent/router</strong> capability, not these two modes.")},
            {"q": L("condense_question / context / condense_plus_context 你怎么选？",
                    "How do you choose among condense_question / context / condense_plus_context?"),
             "answer": L("condense_question：检索更聚焦（先消解再检索），但压缩可能丢上下文；context：保留原始对话上下文、实现直接，但追问含指代时检索可能不准；condense_plus_context：两者结合、通用性最好，是多数客服/问答助手的默认。",
                         "condense_question: focused retrieval (resolve then retrieve), but compression may drop context; context: keeps raw conversational context and is simple, but retrieval can miss on pronoun-laden follow-ups; condense_plus_context: both combined, most general — the default for most assistants.")},
            {"q": L("用户追问“那它呢？”，引擎把“它”解析错了，检索全跑偏。你怎么排查和改善？",
                    "On 'and what about it?', the engine resolves 'it' wrong and retrieval derails. How do you debug and improve it?"),
             "answer": L("先看 condense 后生成的“独立问题”长什么样（很多实现可打印改写后的 query）；若改写错→优化 condense 的 prompt、或保留更多对话历史、或换 condense_plus_context；必要时让用户的指代更明确，或上 agent 做更强的对话状态管理。",
                         "Inspect the condensed standalone question (many implementations let you print the rewritten query); if the rewrite is wrong → improve the condense prompt, keep more history, or switch to condense_plus_context; when needed, disambiguate references or move to an agent with stronger dialogue-state management.")},
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
        "interview": [
            {"q": L("有人到处用全局 <code>Settings</code>、有人坚持每个组件显式传参。各自的利弊是什么？你会怎么定规范？",
                    "Some use the global <code>Settings</code> everywhere; others pass config explicitly to each component. Trade-offs, and what convention would you set?"),
             "answer": L("全局 Settings：少样板、改一处全局生效，但是隐式依赖、难追踪“这条链路到底用了哪个模型”、测试易串味；显式传参：可读、可测、可在同进程跑多套配置，但啰嗦。规范：全局设默认值，关键/差异化组件（评估用的 judge、特殊 query engine）显式覆盖并就近声明。",
                         "Global Settings: less boilerplate, one change applies everywhere — but it's an implicit dependency, hard to trace 'which model did this path use', and tests can leak state; explicit args: readable, testable, multiple configs can coexist in one process — but verbose. Convention: set sane global defaults, and explicitly override key/divergent components (an eval judge, a special query engine) declared close to use.")},
            {"q": L("为什么说 Prompt 是 RAG 的“最后一公里”？",
                    "Why is the prompt the 'last mile' of RAG?"),
             "answer": L("检索结果<strong>一字不变</strong>，只换一句 prompt（语气、约束、输出格式），答案就可能大不相同。检索决定“给 LLM 看什么”，prompt 决定“让 LLM 怎么用它”——是质量的最后一道可控旋钮。",
                         "With the retrieved context <strong>unchanged</strong>, swapping one prompt (tone, constraints, output format) can change the answer entirely. Retrieval decides 'what the LLM sees'; the prompt decides 'how it uses it' — the last controllable knob on quality.")},
            {"q": L("同样的检索结果，换 prompt 就能改变答案——质量责任更多在检索还是 prompt？怎么分工调优？",
                    "Same retrieval, different prompt, different answer — does quality rest more on retrieval or the prompt? How do you split the tuning?"),
             "answer": L("两者分工：检索决定“依据对不对”（召回不到，prompt 再好也是巧妇难为无米之炊）；prompt 决定“依据用得对不对”（约束不编造、要出处、控格式）。先用评估把<strong>检索召回</strong>调达标，再用 prompt 调“忠实度/格式”，避免把两类问题混在一起。",
                         "They divide labor: retrieval decides whether the evidence is right (no recall, no prompt can save it); the prompt decides whether the evidence is used right (don't invent, cite, control format). Get <strong>recall</strong> to target first via evaluation, then tune faithfulness/format with the prompt — don't conflate the two.")},
            {"q": L("<code>text_qa_template</code> 里的 <code>{context_str}</code> 和 <code>{query_str}</code> 是什么？怎么用它强制“只引用”？",
                    "What are <code>{context_str}</code> and <code>{query_str}</code> in a <code>text_qa_template</code>, and how do you use it to force 'cite-only'?"),
             "answer": L("它们是占位符：<code>{context_str}</code> 注入检索到的片段，<code>{query_str}</code> 注入用户问题。写明“只依据下列资料回答；资料未提及就回答‘资料未提及’；并标注出处”，即可把“只引用、不编造”落到 prompt 层。",
                         "They're placeholders: <code>{context_str}</code> injects the retrieved chunks, <code>{query_str}</code> the user's question. Instruct 'answer only from the context below; if not mentioned, say so; cite sources' to enforce 'cite-only, never invent' at the prompt layer.")},
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
        "interview": [
            {"q": L("朴素 top-k 检索有哪三类典型短板？进阶检索分别怎么补？",
                    "What are the three typical weaknesses of naive top-k retrieval, and how does advanced retrieval address each?"),
             "answer": L("① 召回不全（换个问法本能命中的被漏掉）→ Query Fusion 改写多版查询再融合；② 命中碎片（块太碎、上下文不全）→ AutoMerging 合并父块 / Recursive 跟随引用；③ 多库分流（该查哪个源）→ Router 自动路由。",
                         "(1) Incomplete recall (a rephrasing would have hit) → Query Fusion rewrites and fuses several queries; (2) fragmented hits (chunks too small, missing context) → AutoMerging merges parent blocks / Recursive follows references; (3) multi-source routing (which store to query) → Router auto-routes.")},
            {"q": L("Query Fusion 是怎么提升召回的？它的额外成本是什么？",
                    "How does Query Fusion lift recall, and what's its extra cost?"),
             "answer": L("把一个问题<strong>改写成 <code>num_queries</code>−1 个变体（再加上原问题）</strong>各自检索，再把多路结果<strong>融合</strong>（常用 reciprocal-rank fusion / RRF，需显式设 <code>mode</code>）——覆盖更多“问法”，召回更全。代价：多跑几轮检索 + 一次改写的 LLM 调用，更慢、更贵。",
                         "It generates <strong><code>num_queries</code>−1 rewrites (plus the original)</strong>, retrieves each, then <strong>fuses</strong> the result lists (commonly with reciprocal-rank fusion / RRF, set via <code>mode</code>) — covering more phrasings for fuller recall. Cost: several extra retrieval passes plus a rewrite LLM call — slower and pricier.")},
            {"q": L("“进阶检索没有免费的午餐”——对延迟敏感的线上问答，你会接受 fusion 的开销吗？怎么权衡？",
                    "'Advanced retrieval is no free lunch' — for latency-sensitive live Q&amp;A, would you accept fusion's overhead? How do you weigh it?"),
             "answer": L("先量化：fusion 提升的召回/答案质量值多少？延迟预算还剩多少？高价值、可容忍几百 ms 的场景值得；强延迟约束下可改用更便宜的手段（更好的 embedding、轻量 rerank、缓存常见查询），或只对“难问题”按需触发 fusion。",
                         "Quantify first: how much does fusion improve recall/answer quality, and what's the latency budget? High-value flows tolerant of a few hundred ms justify it; under tight latency, prefer cheaper levers (better embedding, light rerank, caching common queries) or trigger fusion only for 'hard' questions.")},
            {"q": L("AutoMerging 检索解决什么？它和单纯调大 chunk_size 有何不同？",
                    "What does AutoMerging retrieval solve, and how is it different from just using a bigger chunk_size?"),
             "answer": L("它用<strong>小块检索</strong>（精准），当命中同一父块的多个小块时再<strong>合并成父块</strong>喂给 LLM（补上下文）——兼得精准与上下文。直接调大 chunk_size 则全程用大块，检索会更糊、噪声更多。",
                         "It retrieves with <strong>small chunks</strong> (precise), and when several small chunks under the same parent are hit, <strong>merges them into the parent</strong> for the LLM (context) — precision and context together. A larger chunk_size uses big chunks throughout, blurring retrieval and adding noise.")},
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
        "interview": [
            {"q": L("Faithfulness / Relevancy / Correctness 各衡量什么？分别需要什么输入？",
                    "What does each of Faithfulness / Relevancy / Correctness measure, and what input does each need?"),
             "answer": L("Faithfulness：答案是否<strong>忠于检索到的上下文</strong>（防幻觉），要 response（含 source_nodes）；Relevancy：检索到的上下文+答案是否<strong>切题</strong>，要 query+response；Correctness：答案对不对，要 query+response+<strong>参考答案</strong>，多为 1–5 评分。",
                         "Faithfulness: is the answer <strong>grounded in the retrieved context</strong> (anti-hallucination), needs response (+ source_nodes); Relevancy: are context+answer <strong>on-topic</strong>, needs query+response; Correctness: is the answer right, needs query+response+<strong>a reference answer</strong>, usually a 1–5 score.")},
            {"q": L("为什么说评估能把 RAG 调优从“凭感觉”变成“闭环”？",
                    "Why does evaluation turn RAG tuning from 'vibes' into a 'closed loop'?"),
             "answer": L("它给出可量化指标，于是“改切块/检索/Prompt → 评估 → 对比指标 → 决定保留或回退”成为可重复的闭环，还能挡住“修好一个、悄悄弄坏一批”的回归——把调优变成工程纪律而非手感。",
                         "It yields quantifiable metrics, so 'change chunking/retrieval/prompt → evaluate → compare → keep or revert' becomes a repeatable loop, and it catches the 'fix one, silently break many' regression — making tuning an engineering discipline, not a feel.")},
            {"q": L("评估用的是 LLM-as-judge。它有哪些局限？你怎么缓解？",
                    "Evaluation uses LLM-as-judge. What are its limits, and how do you mitigate them?"),
             "answer": L("局限：评判本身有噪声/偏见、可能偏向某种风格、成本高、对边界判断不稳。缓解：固定评判模型与 prompt、用二值/明确 rubric、对关键集做人评校准、看趋势而非单点分数、维护回归集对比相对变化。",
                         "Limits: the judge is noisy/biased, may favor a style, costs money, and is shaky on edge cases. Mitigate: pin the judge model and prompt, use binary/explicit rubrics, calibrate with human review on a key set, watch trends over single scores, and compare relative change on a fixed regression set.")},
            {"q": L("你会如何搭一个最小回归集，防止改动让 RAG 变差？",
                    "How would you build a minimal regression set so changes don't quietly degrade the RAG?"),
             "answer": L("挑一组有代表性的问题（覆盖常见、长尾、易错），尽量配“标准答案块/参考答案”；每次改动后用 BatchEvalRunner 跑这组、记录 Faithfulness/Relevancy 等分数；只在指标不降时合并改动，下降就定位回退。先小而稳，再逐步扩充。",
                         "Pick representative questions (common, long-tail, error-prone), ideally with gold chunks/reference answers; after each change run them via BatchEvalRunner and record Faithfulness/Relevancy; merge only when metrics hold, locate and revert when they drop. Start small and stable, then grow it.")},
        ],
        "open": [
            L("你会如何搭一个最小的回归评估集，防止改动让 RAG 变差？",
              "How would you build a minimal regression eval set to keep changes from degrading the RAG?"),
        ],
    },
    "20-capstone.html": {
        "interview": [
            {"q": L("端到端 RAG 应用，“首次建库”和“以后复用”代码应该怎么分支？",
                    "In an end-to-end RAG app, how should the code branch between 'first build' and 'later reuse'?"),
             "answer": L("用 <code>if os.path.exists(PERSIST)</code>：存在就 <code>load_index_from_storage</code> 秒级复活；否则跑一遍写入路径（load → 切块/摄取 → 建索引）再 <code>persist</code> 落盘。把“建一次（重）”和“问多次（轻）”分开，启动才快。",
                         "Use <code>if os.path.exists(PERSIST)</code>: if present, <code>load_index_from_storage</code> revives it in seconds; otherwise run the write path (load → split/ingest → index) once, then <code>persist</code>. Separating 'build once (heavy)' from 'ask many (light)' keeps startup fast.")},
            {"q": L("为什么 <code>Settings.embed_model</code> 必须在<strong>建索引之前</strong>设好？设晚了会怎样？",
                    "Why must <code>Settings.embed_model</code> be set <strong>before</strong> building the index? What breaks if it's set late?"),
             "answer": L("落盘的向量由 embed_model 决定；加载后必须用<strong>同一个</strong>模型才能对齐检索。若建索引时用了默认/错的 embed_model，向量就是错坐标系的——查询要么报错、要么相似度全错，且只能重建索引才能修。",
                         "The persisted vectors are determined by the embed_model; after loading you must use the <strong>same</strong> model for retrieval to line up. If the index was built with a default/wrong embed_model, the vectors are in the wrong space — queries error or score nonsensically, fixable only by re-indexing.")},
            {"q": L("把这套 capstone 改造成“带引用脚注的客服机器人”，你会替换或新增哪几件？",
                    "To turn this capstone into a 'support bot with citation footnotes', which parts would you change or add?"),
             "answer": L("① QueryEngine 换成 <code>chat_mode='condense_plus_context'</code> 的 Chat Engine（多轮记忆）；② 加引用后处理，把 <code>source_nodes</code> 渲染成脚注；③ 收紧 prompt（只引用、给出处）；④ 挂 Faithfulness 评估当上线前质量闸。写入/查询主干骨架不变。",
                         "(1) swap the QueryEngine for a Chat Engine (<code>chat_mode='condense_plus_context'</code>) for memory; (2) add a citation postprocessor rendering <code>source_nodes</code> as footnotes; (3) tighten the prompt (cite-only); (4) attach a Faithfulness evaluator as a pre-launch gate. The write/query backbone stays.")},
            {"q": L("用一句话概括整本书的核心思想——LlamaIndex 的 RAG 观是什么？",
                    "In one sentence, what's the core idea of the whole guide — LlamaIndex's view of RAG?"),
             "answer": L("RAG 是一条<strong>由可组合标准件搭成</strong>的数据管道：写入路径（加载→切块→向量化→存储→索引）把知识外置成可检索、可更新的索引，查询路径（检索→后处理→合成）在其上据此作答；每一站都遵守统一接口、可独立替换与评估。",
                         "RAG is a data pipeline <strong>assembled from composable standard parts</strong>: the write path (load→split→embed→store→index) externalizes knowledge into a searchable, refreshable index, and the query path (retrieve→post-process→synthesize) answers from it — every stop sharing one interface, independently swappable and measurable.")},
        ],
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
