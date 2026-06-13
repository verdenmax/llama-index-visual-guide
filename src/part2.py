"""Part 2 (write path): lessons 04-11. Content filled task-by-task."""
import components as c
from i18n import L


LESSON_04 = (
    c.pipeline("load")
    + c.lead(L(
        "RAG 的最小检索单位是 <strong>Node</strong>，不是整篇 <strong>Document</strong>。Document 是一整份原始资料；"
        "切块后得到带<strong>元数据</strong>与<strong>关系</strong>的 Node——检索、返回、合成都围绕 Node 进行。",
        "The unit of retrieval in RAG is the <strong>Node</strong>, not the whole <strong>Document</strong>. A "
        "Document is one raw source; chunking yields Nodes carrying <strong>metadata</strong> and "
        "<strong>relationships</strong> — retrieval, results and synthesis all revolve around Nodes.",
    ))
    + c.analogy(L(
        "Document 是<strong>整本书</strong>；Node 是书里的<strong>一页便利贴</strong>，背面记着“来自哪本书、上一页/下一页是谁”"
        "（relationships）和“章节/页码”（metadata）。",
        "A Document is the <strong>whole book</strong>; a Node is <strong>one sticky note</strong> from it, whose back "
        "records “which book, previous/next note” (relationships) and “chapter/page” (metadata).",
    ))
    + c.section(
        L("Document vs Node", "Document vs Node"),
        c.compare_table(
            [L("", ""), L("Document", "Document"), L("Node (TextNode)", "Node (TextNode)")],
            [
                [L("粒度", "Granularity"), L("整份原始资料", "one whole source"), L("切块后的片段", "a chunked piece")],
                [L("角色", "Role"), L("输入：被切块", "input: gets chunked"), L("检索/合成的单位", "unit of retrieval/synthesis")],
                [L("携带", "Carries"), L("text + metadata", "text + metadata"), L("text + metadata + relationships", "text + metadata + relationships")],
            ],
        ),
    )
    + c.source_ref(
        "schema.py", "Document · TextNode · NodeRelationship · RelatedNodeInfo",
        L("数据模型与节点关系都定义在这里", "the data model and node relationships live here"),
    )
    + c.code(
        "from llama_index.core import Document\n"
        "from llama_index.core.schema import TextNode, NodeRelationship, RelatedNodeInfo\n\n"
        "doc = Document(text='LlamaIndex 让 RAG 更简单。', metadata={'source': 'faq.md'})\n\n"
        "n1 = TextNode(text='第一段', metadata={'page': 1})\n"
        "n2 = TextNode(text='第二段', metadata={'page': 2})\n"
        "# 关系：n2 来自 doc，且紧跟在 n1 之后\n"
        "n2.relationships[NodeRelationship.SOURCE] = RelatedNodeInfo(node_id=doc.doc_id)\n"
        "n2.relationships[NodeRelationship.PREVIOUS] = RelatedNodeInfo(node_id=n1.node_id)\n"
        "print(n2.metadata, n2.relationships.keys())",
        caption=L("元数据与关系随 Node 一起流动", "metadata and relationships travel with the Node"),
    )
    + c.key_points([
        L("<strong>Node 是检索单位</strong>；Document 只是它的来源。",
          "<strong>The Node is the unit of retrieval</strong>; the Document is just its source."),
        L("metadata 随 Node 流动，可用于<strong>过滤</strong>与<strong>溯源</strong>。",
          "metadata flows with the Node, enabling <strong>filtering</strong> and <strong>provenance</strong>."),
        L("relationships（SOURCE/PREVIOUS/NEXT）是进阶检索（如前后文扩展、溯源）的基础。",
          "relationships (SOURCE/PREVIOUS/NEXT) underpin advanced retrieval (e.g. prev/next context expansion, provenance)."),
    ])
    + c.design_highlight(L(
        "统一的 <strong>Node</strong> 抽象让整条管道“说同一种语言”：无论来源是 PDF 还是数据库，"
        "下游都只面对带元数据与关系的 Node。",
        "A single <strong>Node</strong> abstraction makes the whole pipeline speak one language: whether the source "
        "is a PDF or a database, everything downstream only deals with metadata-and-relationship-bearing Nodes.",
    ))
)
LESSON_05 = (
    c.pipeline("load")
    + c.lead(L(
        "Reader 把任意来源（文件夹、PDF、网页、数据库……）统一变成 <strong>Document</strong> 列表。"
        "<code>SimpleDirectoryReader</code> 是最常用的入口，按扩展名自动选解析器。",
        "A Reader turns any source (a folder, PDF, web page, database…) into a list of <strong>Documents</strong>. "
        "<code>SimpleDirectoryReader</code> is the go-to entry point, picking a parser per file extension.",
    ))
    + c.analogy(L(
        "Reader 像一排<strong>不同接口的扫描仪</strong>：无论纸张、幻灯片还是网页，扫出来都是同一种标准的 Document。",
        "Readers are like a row of <strong>scanners with different ports</strong>: paper, slides or web pages all "
        "come out as the same standard Document.",
    ))
    + c.section(
        L("SimpleDirectoryReader 常用能力", "What SimpleDirectoryReader gives you"),
        c.compare_table(
            [L("参数", "Argument"), L("作用", "Effect")],
            [
                [L("<code>input_dir</code> / <code>input_files</code>", "<code>input_dir</code> / <code>input_files</code>"),
                 L("读整个目录或指定文件", "read a folder or specific files")],
                [L("<code>recursive=True</code>", "<code>recursive=True</code>"), L("递归子目录", "recurse subfolders")],
                [L("<code>required_exts=['.pdf']</code>", "<code>required_exts=['.pdf']</code>"), L("只读特定扩展名", "limit to extensions")],
            ],
        ),
    )
    + c.source_ref("readers/file/base.py", "SimpleDirectoryReader", L("内置目录读取器", "the built-in directory reader"))
    + c.source_ref("readers/base.py", "BaseReader.load_data", L("所有 Reader 的统一接口", "the interface every Reader implements"))
    + c.code(
        "from llama_index.core import SimpleDirectoryReader\n\n"
        "docs = SimpleDirectoryReader(\n"
        "    input_dir='./data', recursive=True, required_exts=['.md', '.pdf'],\n"
        ").load_data()\n"
        "print(len(docs), docs[0].metadata)   # 每个文件 -&gt; 一个或多个 Document\n\n"
        "# 更多来源见 LlamaHub：pip install llama-index-readers-web 等\n"
        "# from llama_index.readers.web import SimpleWebPageReader",
        caption=L("一行加载整个目录", "load a whole directory in one line"),
    )
    + c.key_points([
        L("Reader 的统一产出是 <strong>Document</strong>，让管道与数据来源解耦。",
          "Readers all output <strong>Documents</strong>, decoupling the pipeline from data sources."),
        L("<code>SimpleDirectoryReader</code> 按扩展名自动选解析器。",
          "<code>SimpleDirectoryReader</code> auto-selects a parser by extension."),
        L("更多来源在 <strong>LlamaHub</strong>（独立集成包，按需安装）。",
          "More sources live on <strong>LlamaHub</strong> (separate integration packages)."),
    ])
    + c.design_highlight(L(
        "把“千奇百怪的来源”收敛到“一种 Document”，是 RAG 可组合性的起点——换数据源不影响后续任何一站。",
        "Collapsing wildly different sources into one Document type is where RAG composability begins — changing the "
        "source never disturbs any later stage.",
    ))
)
LESSON_06 = (
    c.pipeline("split")
    + c.lead(L(
        "切块（chunking）把 Document 拆成大小合适的 Node。为什么要切？因为 embedding 与 LLM 上下文都<strong>有限</strong>，"
        "且检索希望命中<strong>精准的小片段</strong>。<code>chunk_size</code> 与 <code>chunk_overlap</code> 是核心旋钮。",
        "Chunking splits a Document into right-sized Nodes. Why split? Because embeddings and LLM context are "
        "<strong>limited</strong>, and retrieval wants to hit a <strong>precise small piece</strong>. "
        "<code>chunk_size</code> and <code>chunk_overlap</code> are the key knobs.",
    ))
    + c.analogy(L(
        "把长文拆成便利贴：太大塞不下又检索不准，太小丢上下文。<strong>overlap</strong> 让相邻便利贴重叠几句，"
        "避免把一句话从中间切断。",
        "Cut long text into sticky notes: too big won't fit and retrieves imprecisely; too small loses context. "
        "<strong>overlap</strong> lets adjacent notes share a few sentences so a thought isn't cut mid-way.",
    ))
    + c.section(
        L("四种常用切块器", "Four common splitters"),
        c.compare_table(
            [L("切块器", "Splitter"), L("切法", "How it splits"), L("适合", "Good for")],
            [
                [L("SentenceSplitter", "SentenceSplitter"), L("按句子凑到 chunk_size", "sentences up to chunk_size"), L("通用默认", "general default")],
                [L("TokenTextSplitter", "TokenTextSplitter"), L("按 token 数硬切", "by token count"), L("严格控长", "strict length control")],
                [L("SemanticSplitterNodeParser", "SemanticSplitterNodeParser"), L("按语义相似度断点", "at semantic breakpoints"), L("主题清晰的长文", "topically varied text")],
                [L("SentenceWindowNodeParser", "SentenceWindowNodeParser"), L("单句为节点+窗口上下文", "one sentence + window"), L("精检索后补上下文", "precise hit, fuller context")],
            ],
        ),
    )
    + c.source_ref("node_parser/text/sentence.py", "SentenceSplitter", L("默认切块器", "the default splitter"))
    + c.source_ref("node_parser/text/sentence_window.py", "SentenceWindowNodeParser.from_defaults", L("句窗切块", "sentence-window parsing"))
    + c.code(
        "from llama_index.core.node_parser import SentenceSplitter, SentenceWindowNodeParser\n\n"
        "splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)\n"
        "nodes = splitter.get_nodes_from_documents(docs)\n"
        "print(len(nodes), nodes[0].text[:60])\n\n"
        "# 句窗：节点是单句，metadata['window'] 保留前后句作为上下文\n"
        "window = SentenceWindowNodeParser.from_defaults(window_size=3)\n"
        "wnodes = window.get_nodes_from_documents(docs)",
        caption=L("chunk_size / overlap 是 RAG 调优第一旋钮", "chunk_size / overlap: RAG's first tuning knob"),
    )
    + c.key_points([
        L("切块决定“检索能命中多准”——RAG 质量的第一旋钮。",
          "Chunking decides how precisely retrieval can hit — RAG quality's first knob."),
        L("<code>chunk_overlap</code> 防止把完整语义从中间切断。",
          "<code>chunk_overlap</code> keeps a complete thought from being cut in half."),
        L("句窗切块：用<strong>单句</strong>精准检索，再用<strong>窗口</strong>补回上下文。",
          "Sentence-window: retrieve precisely on a <strong>single sentence</strong>, then restore context via the <strong>window</strong>."),
    ])
    + c.design_highlight(L(
        "切块器都实现同一个 <code>get_nodes_from_documents</code> 接口，所以换切块策略<strong>零成本</strong>——"
        "这正是“先标准化接口，再谈策略”的威力。",
        "Every splitter implements the same <code>get_nodes_from_documents</code> interface, so swapping strategies "
        "is <strong>free</strong> — the payoff of “standardize the interface first, then vary the strategy”.",
    ))
)
LESSON_07 = (
    c.pipeline("split")
    + c.lead(L(
        "给 Node 补<strong>元数据</strong>（标题、关键词、它能回答的问题、摘要）能显著提升检索与过滤。"
        "Extractor 用 LLM 自动为每个 Node 生成这些元数据。",
        "Enriching Nodes with <strong>metadata</strong> (title, keywords, the questions it answers, a summary) boosts "
        "retrieval and filtering. Extractors use an LLM to generate that metadata per Node automatically.",
    ))
    + c.analogy(L(
        "给每张便利贴贴上<strong>标签和一句摘要</strong>：日后既能按主题筛，也能让“问题↔片段”更容易对上。",
        "Put a <strong>label and one-line summary</strong> on every sticky note: later you can filter by topic and "
        "match “question ↔ snippet” far more easily.",
    ))
    + c.section(
        L("常用抽取器", "Common extractors"),
        c.compare_table(
            [L("抽取器", "Extractor"), L("产出的元数据", "Metadata it adds")],
            [
                [L("TitleExtractor", "TitleExtractor"), L("文档标题（document_title）", "a document-level title (document_title)")],
                [L("KeywordExtractor", "KeywordExtractor"), L("关键词", "keywords")],
                [L("QuestionsAnsweredExtractor", "QuestionsAnsweredExtractor"), L("该片段能回答的问题", "questions this chunk answers")],
                [L("SummaryExtractor", "SummaryExtractor"), L("片段摘要", "a chunk summary")],
            ],
        ),
    )
    + c.source_ref("extractors/metadata_extractors.py", "TitleExtractor · QuestionsAnsweredExtractor · KeywordExtractor · SummaryExtractor",
                   L("都作为 transformation 接入管道", "all plug in as pipeline transformations"))
    + c.code(
        "from llama_index.core.extractors import TitleExtractor, QuestionsAnsweredExtractor\n"
        "from llama_index.core.node_parser import SentenceSplitter\n"
        "from llama_index.core.ingestion import IngestionPipeline\n\n"
        "pipeline = IngestionPipeline(transformations=[\n"
        "    SentenceSplitter(chunk_size=512),\n"
        "    TitleExtractor(nodes=5),               # 用 LLM 推断标题\n"
        "    QuestionsAnsweredExtractor(questions=3) # 该块能回答的 3 个问题\n"
        "])\n"
        "nodes = pipeline.run(documents=docs)\n"
        "print(nodes[0].metadata)   # 多了 document_title / questions_this_excerpt_can_answer",
        caption=L("抽取器即“管道里的一道工序”", "extractors are just steps in the pipeline"),
    )
    + c.key_points([
        L("元数据是<strong>检索的第二通道</strong>：不止向量相似，还能按标签/来源过滤。",
          "Metadata is retrieval's <strong>second channel</strong>: beyond vector similarity, filter by tag/source."),
        L("<code>QuestionsAnsweredExtractor</code> 让“问题↔片段”更易对齐。",
          "<code>QuestionsAnsweredExtractor</code> aligns “question ↔ chunk” better."),
        L("抽取器是 LLM 调用，有<strong>成本</strong>——按需启用。",
          "Extractors call the LLM, so they cost tokens — enable selectively."),
    ])
    + c.design_highlight(L(
        "Extractor 与 Splitter 都是 <strong>transformation</strong>，可任意串联——元数据增强变成管道里可插拔的一环。",
        "Extractors and splitters are both <strong>transformations</strong> you can chain freely — metadata enrichment "
        "becomes a pluggable link in the pipeline.",
    ))
)
LESSON_08 = (
    c.pipeline("embed")
    + c.lead(L(
        "Embedding 把文本变成<strong>向量</strong>，让“语义相近”变成“向量距离近”。检索时把问题也向量化，"
        "再找最近的若干 Node。模型由 <code>Settings.embed_model</code> 统一配置。",
        "Embeddings turn text into <strong>vectors</strong> so “semantically similar” becomes “close in vector space”. "
        "At query time the question is embedded too, then the nearest Nodes are found. The model is configured globally "
        "via <code>Settings.embed_model</code>.",
    ))
    + c.analogy(L(
        "把每段话放到一张<strong>语义地图</strong>上的坐标；提问就是在地图上落一个点，找<strong>最近的几个点</strong>。",
        "Place every passage at a coordinate on a <strong>semantic map</strong>; asking a question drops a point on it "
        "and grabs the <strong>nearest few</strong>.",
    ))
    + c.section(
        L("检索为什么靠向量", "Why retrieval rides on vectors"),
        c.compare_table(
            [L("做法", "Approach"), L("匹配方式", "Match by"), L("能否懂“同义不同词”", "Catches paraphrases?")],
            [
                [L("关键词匹配", "Keyword match"), L("字面相同", "literal overlap"), L("不能", "no")],
                [L("向量检索", "Vector search"), L("语义相近（余弦相似度）", "semantic closeness (cosine similarity)"), L("能", "yes")],
            ],
        ),
    )
    + c.source_ref("base/embeddings/base.py", "BaseEmbedding · similarity · SimilarityMode",
                   L("统一接口 + 相似度计算", "the unified interface + similarity"))
    + c.code(
        "from llama_index.core import Settings\n"
        "from llama_index.embeddings.openai import OpenAIEmbedding\n\n"
        "Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')\n"
        "v = Settings.embed_model.get_text_embedding('退款政策是什么？')\n"
        "print(len(v))   # 向量维度，如 1536\n\n"
        "# 语义越近，余弦相似度越高（检索就按它排序取 top-k）",
        caption=L("一次向量化，多次检索复用", "embed once, reuse across many queries"),
    )
    + c.key_points([
        L("Embedding 把<strong>语义相似</strong>变成<strong>向量距离</strong>，是语义检索的地基。",
          "Embeddings turn <strong>semantic similarity</strong> into <strong>vector distance</strong> — the bedrock of semantic search."),
        L("查询与文档必须用<strong>同一个</strong> embedding 模型。",
          "Query and documents must use the <strong>same</strong> embedding model."),
        L("统一 <code>BaseEmbedding</code> 接口让你随时换模型而不改主链路。",
          "The unified <code>BaseEmbedding</code> interface lets you swap models without touching the pipeline."),
    ])
    + c.design_highlight(L(
        "检索质量很大程度由 embedding 模型决定；把它抽象成可替换组件，意味着 RAG 可以随模型进步而<strong>免费升级</strong>。",
        "Retrieval quality largely rides on the embedding model; abstracting it as a swappable component means RAG can "
        "<strong>upgrade for free</strong> as models improve.",
    ))
)
LESSON_09 = (
    c.pipeline("store")
    + c.lead(L(
        "向量存哪儿？<strong>VectorStore</strong> 负责存 Node 的向量+元数据，并支持<strong>最近邻查询</strong>。"
        "默认是内存版 <code>SimpleVectorStore</code>，生产可换 Chroma / FAISS / PG 等，接口一致。",
        "Where do the vectors live? A <strong>VectorStore</strong> stores Node vectors + metadata and supports "
        "<strong>nearest-neighbor queries</strong>. The default is in-memory <code>SimpleVectorStore</code>; in "
        "production swap in Chroma / FAISS / PG — same interface.",
    ))
    + c.analogy(L(
        "向量库是语义地图的<strong>GPS 索引</strong>：给一个坐标，瞬间找出附近的点，而不必逐个比对全图。",
        "A vector store is the <strong>GPS index</strong> of the semantic map: given a coordinate it finds nearby points "
        "instantly, instead of scanning the whole map.",
    ))
    + c.section(
        L("默认 vs 生产", "Default vs production"),
        c.compare_table(
            [L("场景", "Scenario"), L("选择", "Choice")],
            [
                [L("学习 / 小数据 / 原型", "learning / small / prototype"), L("<code>SimpleVectorStore</code>（内存，零依赖）", "<code>SimpleVectorStore</code> (in-memory)")],
                [L("规模化 / 持久化 / 过滤", "scale / persistence / filters"), L("Chroma · FAISS · pgvector · Qdrant…", "Chroma · FAISS · pgvector · Qdrant…")],
            ],
        ),
    )
    + c.source_ref("vector_stores/simple.py", "SimpleVectorStore", L("默认内存向量库", "the default in-memory store"))
    + c.source_ref("vector_stores/types.py", "VectorStoreQuery", L("统一的相似度查询契约", "the unified similarity-query contract"))
    + c.code(
        "from llama_index.core import VectorStoreIndex, StorageContext\n\n"
        "# 默认：内存 SimpleVectorStore\n"
        "index = VectorStoreIndex.from_documents(docs)\n\n"
        "# 换生产向量库（接口一致，只改这几行）\n"
        "# pip install llama-index-vector-stores-chroma chromadb\n"
        "import chromadb\n"
        "from llama_index.vector_stores.chroma import ChromaVectorStore\n"
        "store = ChromaVectorStore(chroma_collection=chromadb.Client().create_collection('rag'))\n"
        "sc = StorageContext.from_defaults(vector_store=store)\n"
        "index = VectorStoreIndex.from_documents(docs, storage_context=sc)",
        caption=L("从内存到生产库，主链路不变", "in-memory → production, pipeline unchanged"),
    )
    + c.key_points([
        L("VectorStore = 存向量 + 元数据 + 近邻查询。",
          "A VectorStore = stores vectors + metadata + nearest-neighbor search."),
        L("默认内存库适合学习；生产换集成库，<strong>接口一致</strong>。",
          "The in-memory default suits learning; production swaps integrations with the <strong>same interface</strong>."),
        L("通过 <code>StorageContext</code> 注入向量库。",
          "Inject the store via <code>StorageContext</code>."),
    ])
    + c.design_highlight(L(
        "把“近邻搜索”抽象成 <code>VectorStoreQuery</code>，让笔记本内存版和生产级向量库对上层<strong>完全一样</strong>——"
        "上线只是换实现，不是重写。",
        "Abstracting nearest-neighbor search as <code>VectorStoreQuery</code> makes the laptop store and a production "
        "engine look <strong>identical</strong> upstream — going live is a swap, not a rewrite.",
    ))
)
LESSON_10 = (
    c.pipeline("index")
    + c.lead(L(
        "Index 不只是“向量库”——它是<strong>为某种检索方式组织 Node 的数据结构</strong>。不同 Index 对应不同问题："
        "相似问答用 VectorStoreIndex，整库总结用 SummaryIndex，实体关系用 PropertyGraphIndex。",
        "An Index isn't just a vector store — it's a <strong>data structure that organizes Nodes for a particular way "
        "of retrieving</strong>. Different Indexes fit different questions: VectorStoreIndex for similarity Q&amp;A, "
        "SummaryIndex for whole-corpus summaries, PropertyGraphIndex for entity relations.",
    ))
    + c.analogy(L(
        "同一堆资料的不同<strong>组织法</strong>：词典（按相似度近邻）、章节大纲（逐条遍历总结）、知识图谱（按实体关系跳转）。",
        "Different <strong>organizations</strong> of the same pile: a dictionary (nearest-neighbor), a chapter outline "
        "(walk every entry to summarize), a knowledge graph (hop by entity relations).",
    ))
    + c.section(
        L("常见 Index 与适用场景", "Common indexes and when to use them"),
        c.compare_table(
            [L("Index", "Index"), L("检索范式", "Retrieval style"), L("适合", "Best for")],
            [
                [L("VectorStoreIndex", "VectorStoreIndex"), L("向量近邻 top-k", "vector top-k"), L("相似问答（最常用）", "similarity Q&amp;A (most common)")],
                [L("SummaryIndex", "SummaryIndex"), L("遍历所有 Node", "iterate all Nodes"), L("整库总结", "summarize a corpus")],
                [L("DocumentSummaryIndex", "DocumentSummaryIndex"), L("先按文档摘要召回", "recall via doc summaries"), L("多文档路由", "routing across docs")],
                [L("PropertyGraphIndex", "PropertyGraphIndex"), L("图谱遍历", "graph traversal"), L("实体关系/多跳", "entities / multi-hop")],
            ],
        ),
    )
    + c.source_ref("indices/vector_store/base.py", "VectorStoreIndex", L("最常用的相似检索索引", "the common similarity index"))
    + c.source_ref("indices/list/base.py", "SummaryIndex", L("遍历式索引（原 ListIndex）", "the iterate-all index (formerly ListIndex)"))
    + c.code(
        "from llama_index.core import VectorStoreIndex, SummaryIndex\n\n"
        "vindex = VectorStoreIndex.from_documents(docs)   # 相似问答\n"
        "print(vindex.as_query_engine().query('退款政策？'))\n\n"
        "sindex = SummaryIndex.from_documents(docs)        # 整库总结\n"
        "print(sindex.as_query_engine(response_mode='tree_summarize').query('全文讲了什么？'))",
        caption=L("选 Index 就是选检索范式", "choosing an Index = choosing a retrieval style"),
    )
    + c.key_points([
        L("Index = <strong>组织方式 + 检索范式</strong>，不等于向量库本身。",
          "An Index = <strong>organization + retrieval style</strong>, not the vector store itself."),
        L("相似问答选 VectorStoreIndex；整库总结选 SummaryIndex。",
          "VectorStoreIndex for similarity Q&amp;A; SummaryIndex for whole-corpus summaries."),
        L("所有 Index 都用 <code>from_documents</code> / <code>as_query_engine</code> 同款入口。",
          "Every Index shares the <code>from_documents</code> / <code>as_query_engine</code> entry points."),
    ])
    + c.design_highlight(L(
        "“选 Index”本质是“选检索策略”。统一的 Index→QueryEngine 入口让你<strong>用同一套代码切换范式</strong>，"
        "甚至用 Router 在多个 Index 间自动路由。",
        "“Choosing an Index” is really “choosing a retrieval strategy.” The uniform Index→QueryEngine entry lets you "
        "<strong>switch paradigms with the same code</strong> — even auto-route across indexes with a Router.",
    ))
)
LESSON_11 = (
    c.pipeline("store")
    + c.lead(L(
        "<strong>IngestionPipeline</strong> 把切块、抽取、向量化串成一条<strong>可缓存、可去重</strong>的管道；"
        "<strong>StorageContext</strong> + <code>persist</code> / <code>load_index_from_storage</code> 让建好的索引落盘、下次秒开。",
        "<strong>IngestionPipeline</strong> chains splitting, extraction and embedding into a "
        "<strong>cacheable, dedup-aware</strong> pipeline; <strong>StorageContext</strong> + <code>persist</code> / "
        "<code>load_index_from_storage</code> let a built index hit disk and reload instantly next time.",
    ))
    + c.analogy(L(
        "Ingestion 像<strong>自动化装配线</strong>（切块→抽取→向量化），缓存让“已加工的零件”不重做；"
        "persist 像把建好的图书馆<strong>整体存档</strong>，下次直接开门营业。",
        "Ingestion is an <strong>assembly line</strong> (split→extract→embed); the cache skips “parts already made”; "
        "persist <strong>archives the finished library</strong> so next time you just open the doors.",
    ))
    + c.section(
        L("管道 + 存储解决什么", "What pipeline + storage solve"),
        c.compare_table(
            [L("能力", "Capability"), L("带来的好处", "Benefit")],
            [
                [L("transformations 串联", "chained transformations"), L("一处定义、可复用", "define once, reuse")],
                [L("cache", "cache"), L("相同输入不重复算", "skip recompute on same input")],
                [L("docstore 去重", "docstore dedup"), L("增量更新只处理变化的文档", "incremental: only changed docs")],
                [L("persist / load", "persist / load"), L("索引落盘，重启免重建", "index on disk, no rebuild on restart")],
            ],
        ),
    )
    + c.source_ref("ingestion/pipeline.py", "IngestionPipeline.run", L("可缓存/去重的摄取管道", "the cacheable, dedup-aware pipeline"))
    + c.source_ref("storage/storage_context.py", "StorageContext.persist", L("把 docstore/index/vector 一起落盘", "persists docstore/index/vector together"))
    + c.source_ref("indices/loading.py", "load_index_from_storage", L("从磁盘恢复索引", "reload an index from disk"))
    + c.code(
        "from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage\n"
        "from llama_index.core.ingestion import IngestionPipeline\n"
        "from llama_index.core.node_parser import SentenceSplitter\n"
        "from llama_index.core.storage.docstore import SimpleDocumentStore\n\n"
        "# 可缓存 + 去重的摄取管道：相同输入不重算，相同文档不重复处理\n"
        "pipeline = IngestionPipeline(\n"
        "    transformations=[SentenceSplitter(chunk_size=512)],\n"
        "    docstore=SimpleDocumentStore(),   # 配 docstore 才能按文档去重做增量\n"
        ")\n"
        "nodes = pipeline.run(documents=docs)\n"
        "index = VectorStoreIndex(nodes)\n\n"
        "# 落盘，下次秒开\n"
        "index.storage_context.persist(persist_dir='./storage')\n"
        "index2 = load_index_from_storage(StorageContext.from_defaults(persist_dir='./storage'))",
        caption=L("建一次、存起来、反复用", "build once, persist, reuse"),
    )
    + c.key_points([
        L("IngestionPipeline 让“建索引”变成<strong>幂等、可缓存</strong>的管道。",
          "IngestionPipeline makes “building the index” an <strong>idempotent, cacheable</strong> process."),
        L("docstore 去重支持<strong>增量更新</strong>：只处理变化的文档。",
          "docstore dedup enables <strong>incremental updates</strong>: only changed docs are processed."),
        L("<code>persist</code> / <code>load_index_from_storage</code> 避免每次启动都重建。",
          "<code>persist</code> / <code>load_index_from_storage</code> avoid rebuilding on every startup."),
    ])
    + c.design_highlight(L(
        "把摄取做成<strong>幂等可缓存</strong>的管道，是 RAG 从“demo 跑通”走向“生产可维护”的关键一步——"
        "数据天天变，但只重算变化的部分。",
        "Making ingestion an <strong>idempotent, cacheable</strong> pipeline is the step that takes RAG from “demo "
        "works” to “maintainable in production” — data changes daily, but only the deltas are recomputed.",
    ))
)
