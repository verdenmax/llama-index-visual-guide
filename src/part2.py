"""Part 2 (write path): lessons 04-11. Content filled task-by-task."""
import components as c
import diagrams as d
import i18n
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
    + d.annot(
        L("Node", "Node"),
        [
            (L("text 文本", "text"),
             L("用于 embedding 的正文内容", "the body content that gets embedded")),
            (L("metadata 元数据", "metadata"),
             L("键值对，可用于过滤与溯源", "key-value pairs, usable for filtering and provenance")),
            (L("relationships 关系", "relationships"),
             L("SOURCE · PREVIOUS · NEXT，把 Node 串成链", "SOURCE · PREVIOUS · NEXT, chaining Nodes together")),
        ],
        caption=L(
            "一个 Node = 文本 + 元数据 + 关系，三者一起流经整条管道",
            "One Node = text + metadata + relationships, flowing together through the whole pipeline",
        ),
    )
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
    + c.section(
        L("为什么以 Node 为检索单位", "Why the Node is the unit of retrieval"),
        L(
            "检索、排序、返回、合成全部以 Node 为单位，是为了让下游组件“说同一种语言”：向量库存的是 Node、"
            "检索器返回的是 Node、合成器读的也是 Node，无论原始来源是 PDF、网页还是数据库。Document 太粗——"
            "一篇上万字里真正相关的常常只有一两段，整篇压成<strong>一个</strong>向量时，相关内容会被大量无关文字"
            "<strong>稀释</strong>，命中既不准也不稳；Node 把粒度收敛到“一次讲清一件事”的片段，既适配 embedding "
            "的长度上限，又让命中更准、引用更细。",
            "Retrieval, ranking, results and synthesis all operate on Nodes so that every downstream component "
            "“speaks one language”: the vector store holds Nodes, the retriever returns Nodes, the synthesizer reads "
            "Nodes — whatever the original source. A Document is too coarse — in a 10k-word file usually only a "
            "paragraph or two is relevant, and squeezing the whole thing into <strong>one</strong> vector "
            "<strong>dilutes</strong> that signal with unrelated text, so hits are neither precise nor stable; "
            "a Node narrows granularity to “one idea at a time”, fitting the embedding's length limit while making "
            "hits sharper and citations finer.",
        ),
        d.compare2(
            (L("整篇 Document = 一个向量", "Whole Document = one vector"), i18n.render(L(
                "上万字压成<strong>单个</strong>向量，真正相关的一两段被大量无关文字<strong>稀释</strong>——命中既不准也不稳。",
                "Tens of thousands of words squeezed into <strong>one</strong> vector; the relevant paragraph or two gets "
                "<strong>diluted</strong> by unrelated text — hits are neither precise nor stable.",
            ))),
            (L("切成多个 Node = 各一个向量", "Split into Nodes = one vector each"), i18n.render(L(
                "每个 Node 只讲<strong>一件事</strong>、单独成向量；相关片段独立命中，<strong>更准、引用更细</strong>，也合 embedding 的长度上限。",
                "Each Node says <strong>one thing</strong> and is embedded on its own; the relevant chunk is hit "
                "independently — <strong>sharper, with finer citations</strong> — and fits the embedding's length limit.",
            ))),
            caption=L(
                "为什么以 Node 为检索单位：粒度决定信噪比——整篇会稀释信号，Node 让相关内容单独被命中",
                "Why the Node is the unit of retrieval: granularity sets the signal-to-noise ratio — a whole doc "
                "dilutes the signal, while a Node lets the relevant piece be hit on its own",
            ),
        ),
        d.flow(
            [
                ("doc", L("Document", "Document"), L("一整份原始资料", "one whole source")),
                ("split", L("切块 split", "split"), L("按 chunk_size 拆分", "split by chunk_size")),
                ("n1", L("Node", "Node"), L("片段 + 元数据", "chunk + metadata")),
                ("n2", L("Node", "Node"), L("PREVIOUS ↔ NEXT 相连", "linked PREVIOUS ↔ NEXT")),
                ("n3", L("Node", "Node"), L("SOURCE 指回 Document", "SOURCE points back to the Document")),
            ],
            caption=L(
                "一份 Document 切成多个 Node；relationships 让它们彼此相连、并各自指回来源",
                "One Document becomes many Nodes; relationships link them to one another and back to the source",
            ),
        ),
    )
    + c.source_ref(
        "schema.py", "Document · TextNode · NodeRelationship · RelatedNodeInfo",
        L("数据模型与节点关系都定义在这里", "the data model and node relationships live here"),
    )
    + c.accordion(
        L("深入：Node 作为检索单位", "Deep dive: the Node as the unit of retrieval"),
        c.qa_item(
            L("🧪 示例：构造 Node 并连上关系", "🧪 Example: build a Node and wire its relationships"),
            L(
                "手动建两个 TextNode，把第二个的 SOURCE 指回 Document、PREVIOUS 指向第一个，"
                "就得到一条可前后扩展、可溯源的链：检索命中某个 Node 后，能顺着 NEXT 取下一段补全上下文。",
                "Create two TextNodes by hand, point the second's SOURCE back to the Document and its PREVIOUS to the "
                "first, and you get a chain you can expand and trace: after a Node is hit you can follow NEXT to pull "
                "the next chunk for fuller context.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "把“检索/溯源的单位”固定为 Node，整条管道就只需理解一种对象。粒度统一后，过滤、排序、引用、"
                "前后文扩展都有了共同的承载体，组件之间也能自由替换而不必翻译彼此的数据结构。",
                "Fixing the Node as the unit of retrieval and provenance means the whole pipeline only ever reasons "
                "about one kind of object. With uniform granularity, filtering, ranking, citation and context "
                "expansion share one carrier, and components stay swappable without translating each other's data.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "关系存在 <code>node.relationships</code> 字典里，键是 <code>NodeRelationship</code> 枚举"
                "（SOURCE / PREVIOUS / NEXT / PARENT / CHILD），值是 <code>RelatedNodeInfo</code>；"
                "<code>node.ref_doc_id</code> 就是顺着 SOURCE 找到的来源文档 id。",
                "Relationships live in the <code>node.relationships</code> dict, keyed by the "
                "<code>NodeRelationship</code> enum (SOURCE / PREVIOUS / NEXT / PARENT / CHILD) with "
                "<code>RelatedNodeInfo</code> values; <code>node.ref_doc_id</code> is simply the source document id "
                "reached via SOURCE.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "直接拿整篇 Document 去检索看似省事，却粒度太粗：长文里相关的只有一两段，整篇的向量被无关内容"
                "稀释，命中不准、还浪费上下文。以 Node 为单位，才能既命中精准、又能按需向前后扩展。",
                "Retrieving whole Documents looks simpler but is too coarse: only a paragraph or two is relevant, the "
                "whole-doc vector gets diluted by unrelated text, hits are imprecise and context is wasted. Working "
                "per Node is what makes hits precise while still allowing on-demand prev/next expansion.",
            ),
        ),
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
    + c.code(
        "from llama_index.core import VectorStoreIndex\n"
        "from llama_index.core.schema import NodeRelationship\n"
        "from llama_index.core.vector_stores import MetadataFilters, MetadataFilter\n\n"
        "index = VectorStoreIndex(nodes)\n\n"
        "# 只在 metadata['page'] == 2 的 Node 里检索（元数据过滤）\n"
        "flt = MetadataFilters(filters=[MetadataFilter(key='page', value=2)])\n"
        "engine = index.as_query_engine(filters=flt)\n"
        "print(engine.query('第二页讲了什么？'))\n\n"
        "# 顺着 SOURCE 关系溯源：命中的 Node 来自哪个 Document\n"
        "src = nodes[1].relationships.get(NodeRelationship.SOURCE)\n"
        "print(src.node_id if src else None)",
        caption=L("用 metadata 过滤检索，用 relationships 溯源", "filter retrieval by metadata, trace provenance via relationships"),
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
    + d.flow(
        [
            ("src", L("多来源", "Many sources"), L("文件夹 · PDF · 网页 · 数据库", "folder · PDF · web · DB")),
            ("reader", L("Reader", "Reader"), L("按来源选解析器", "pick a parser per source")),
            ("doc", L("Document 列表", "List of Documents"), L("统一结构，下游通用", "one structure, used by everything downstream")),
        ],
        caption=L(
            "千奇百怪的来源，经 Reader 收敛成同一种 Document",
            "Wildly different sources, collapsed by a Reader into one Document type",
        ),
    )
    + c.analogy(L(
        "Reader 像一排<strong>不同接口的扫描仪</strong>：无论纸张、幻灯片还是网页，扫出来都是同一种标准的 Document。",
        "Readers are like a row of <strong>scanners with different ports</strong>: paper, slides or web pages all "
        "come out as the same standard Document.",
    ))
    + d.grid(
        [L("来源", "Source"), L("用哪个 Reader", "Which Reader"), L("产出", "Output")],
        [
            [L("本地文件夹", "Local folder"), L("SimpleDirectoryReader（内置）", "SimpleDirectoryReader (built-in)"),
             L("Document 列表", "List of Documents")],
            [L("PDF 文件", "PDF file"), L("内置 PDF 解析器，按页切", "built-in PDF parser, per page"),
             L("Document / 每页", "Document / page")],
            [L("网页", "Web page"), L("SimpleWebPageReader（readers-web）", "SimpleWebPageReader (readers-web)"),
             L("Document", "Document")],
            [L("Notion · 数据库 …", "Notion · DB …"), L("LlamaHub 集成包（按需装）", "LlamaHub package (install on demand)"),
             L("Document", "Document")],
        ],
        caption=L(
            "来源各异、Reader 各不相同，产出却都收敛成 Document——按来源装对应包即可，下游一律不变",
            "Different sources, different Readers — yet the output always converges to a Document; install the matching "
            "package per source and everything downstream stays the same",
        ),
    )
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
    + c.section(
        L("一个文件可能产出多个 Document", "One file can yield many Documents"),
        L(
            "容易以为“读 N 个文件就得到 N 个 Document”，其实不一定：很多解析器按<strong>自然边界</strong>切分，"
            "一个 PDF 通常<strong>每页一个 Document</strong>，于是 <code>len(docs)</code> 往往大于文件数。"
            "这个粒度会一路向下传导——Document 越多，切出的 Node 越多；而每个 Document 自带的 <code>page_label</code> "
            "等元数据，正是日后“引用到第几页”溯源的依据。所以加载完先 <code>print(len(docs))</code>、"
            "看一眼 <code>docs[0].metadata</code>，对后面的切块数量与引用粒度都心里有数。",
            "It's tempting to assume “N files in, N Documents out”, but not necessarily: many parsers split on "
            "<strong>natural boundaries</strong> — a PDF usually yields <strong>one Document per page</strong> — so "
            "<code>len(docs)</code> is often larger than the file count. That granularity propagates downstream: more "
            "Documents means more Nodes after chunking, and the <code>page_label</code> each Document carries is "
            "exactly what later lets you cite “which page”. So after loading, <code>print(len(docs))</code> and peek "
            "at <code>docs[0].metadata</code> — it tells you a lot about downstream chunk counts and citation granularity.",
        ),
        d.annot(
            L("report.pdf（1 个文件）", "report.pdf (1 file)"),
            [
                (L("Document(page=1)", "Document(page=1)"),
                 L("第 1 页正文 + page_label", "page 1's text + page_label")),
                (L("Document(page=2)", "Document(page=2)"),
                 L("第 2 页正文 + page_label", "page 2's text + page_label")),
                (L("Document(page=3) …", "Document(page=3) …"),
                 L("逐页扇出，依此类推", "fanned out page by page, and so on")),
            ],
            caption=L(
                "一个文件按页扇出多个 Document：所以 len(docs) ≠ 文件数，且每个 Document 自带页码供日后溯源",
                "One file fans out into many Documents by page — so len(docs) ≠ the file count, and each Document "
                "carries its page number for later provenance",
            ),
        ),
    )
    + c.source_ref("readers/file/base.py", "SimpleDirectoryReader", L("内置目录读取器", "the built-in directory reader"))
    + c.source_ref("readers/base.py", "BaseReader.load_data", L("所有 Reader 的统一接口", "the interface every Reader implements"))
    + c.accordion(
        L("深入：Reader 与统一 Document", "Deep dive: Readers and the unified Document"),
        c.qa_item(
            L("🧪 示例：递归读目录、只取特定扩展名", "🧪 Example: recurse a folder, keep only some extensions"),
            L(
                "<code>SimpleDirectoryReader(input_dir='./data', recursive=True, required_exts=['.md', '.pdf'])</code> "
                "会递归扫描子目录、只读 .md 与 .pdf，并按扩展名分别用平文本与 PDF 解析器，最后统一产出 Document。",
                "<code>SimpleDirectoryReader(input_dir='./data', recursive=True, required_exts=['.md', '.pdf'])</code> "
                "recurses subfolders, keeps only .md and .pdf, parses each with the plain-text or PDF parser by "
                "extension, and emits Documents uniformly.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "把来源解析与下游处理解耦：管道只认 Document，不关心它来自文件、网页还是数据库。换数据源是"
                "“换一个 Reader”，主链路一行不改。",
                "It decouples source parsing from downstream processing: the pipeline only knows Documents, not whether "
                "they came from a file, a web page or a database. Changing sources means “swap a Reader” — the "
                "pipeline stays untouched.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "<code>SimpleDirectoryReader</code> 内部维护一张扩展名→解析器类的映射"
                "（<code>default_file_reader_cls</code>）：遍历文件时按后缀查表、实例化对应解析器、调用其 "
                "<code>load_data</code>，把结果汇成一个 Document 列表。",
                "Inside, <code>SimpleDirectoryReader</code> keeps an extension→parser-class map "
                "(<code>default_file_reader_cls</code>): it walks files, looks up the suffix, instantiates the "
                "matching parser, calls its <code>load_data</code>, and gathers everything into one list of Documents.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "内置解析器覆盖常见文件；更多来源（网页、Notion、Slack、数据库、Google Drive……）在 "
                "<strong>LlamaHub</strong> 上以独立集成包提供，<code>pip install</code> 后即插即用，产出同样是 Document。",
                "Built-in parsers cover common files; more sources (web, Notion, Slack, databases, Google Drive…) live "
                "on <strong>LlamaHub</strong> as separate integration packages — <code>pip install</code> and plug in, "
                "still emitting Documents.",
            ),
        ),
    )
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
    + c.code(
        "# pip install llama-index-readers-web\n"
        "from llama_index.core import VectorStoreIndex\n"
        "from llama_index.readers.web import SimpleWebPageReader\n\n"
        "docs = SimpleWebPageReader(html_to_text=True).load_data(\n"
        "    ['https://docs.llamaindex.ai/en/stable/'])\n"
        "print(len(docs), docs[0].text[:80])\n\n"
        "# 网页同样产出 Document —— 与本地文件走完全一样的下游管道\n"
        "index = VectorStoreIndex.from_documents(docs)",
        caption=L("LlamaHub：一个网页也是一份 Document", "LlamaHub: a web page is a Document too"),
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
    + d.compare2(
        (L("无重叠 chunk_overlap=0", "No overlap (chunk_overlap=0)"), i18n.render(L(
            "块 A 结尾是“……退款将在 7 个工作”，块 B 开头是“日内原路退回……”——一句话被从中间切断，"
            "两个块单独看都答不全。",
            "Chunk A ends with “…refunds arrive within 7 business” and Chunk B starts with “days, to the original "
            "method…” — one sentence cut in half; neither chunk answers fully on its own.",
        ))),
        (L("有重叠 chunk_overlap=50", "With overlap (chunk_overlap=50)"), i18n.render(L(
            "块 A 末尾与块 B 开头共享几句，“7 个工作日内原路退回”完整落在某一个块里——检索命中即拿到完整语义。",
            "Chunk A's tail and Chunk B's head share a few sentences, so “within 7 business days to the original "
            "method” lands intact in one chunk — hit it and you get the whole thought.",
        ))),
        caption=L(
            "chunk_overlap 让相邻块共享边界句，避免把一句话从中间切断",
            "chunk_overlap makes adjacent chunks share boundary sentences, so a thought isn't cut in half",
        ),
    )
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
    + c.section(
        L("chunk_size / chunk_overlap 的权衡", "The chunk_size / chunk_overlap trade-off"),
        L(
            "chunk_size 太大，块里混入大量无关内容，检索噪声多、还挤占 LLM 上下文；而且块再大也不能超过 "
            "<strong>embedding 模型的 token 上限</strong>——常见模型大多在 <strong>512 token</strong> 左右"
            "（详见第 8 课），超出的部分会被悄悄截断、白白丢失。太小，完整语义被切碎，"
            "块与块之间断裂、读不成句。chunk_overlap 用少量冗余换“不把一句话切两半”。这对“精准命中 vs 保留上下文”"
            "的张力，sentence-window 给了一个漂亮的折中：用单句去检索（足够精准），却把前后句组成的窗口喂给 "
            "LLM（补回上下文）。",
            "Too large a chunk_size mixes in lots of irrelevant text — noisy retrieval that also hogs LLM context; and "
            "a chunk can never exceed the <strong>embedding model's token limit</strong> either — most models cap "
            "around <strong>512 tokens</strong> (see Lesson 8), and anything past that is silently truncated and lost. "
            "Too small and a complete thought is shredded, with chunks that break mid-sentence. chunk_overlap trades a "
            "little redundancy for “never cut a sentence in half”. For the tension between “precise hits vs. retained "
            "context”, sentence-window offers an elegant compromise: retrieve on a single sentence (precise enough), "
            "yet feed the LLM the window of surrounding sentences (context restored).",
        ),
        d.vflow(
            [
                (L("原文按句切分", "Split text into sentences"), L("每个 Node = 一句", "each Node = one sentence")),
                (L("节点正文 = 单句", "Node text = a single sentence"), L("检索只匹配这一句 → 命中精准", "retrieval matches just this sentence → precise")),
                (L("metadata['window'] = 前后各 N 句", "metadata['window'] = ±N sentences"), L("查询时替换为窗口 → 补回上下文", "swapped in at query time → context restored")),
            ],
            caption=L(
                "句窗把“精准检索”和“完整上下文”解耦：检索靠单句，喂给 LLM 靠窗口",
                "Sentence-window decouples precise retrieval from full context: retrieve by sentence, feed the window to the LLM",
            ),
        ),
    )
    + c.source_ref("node_parser/text/sentence.py", "SentenceSplitter", L("默认切块器", "the default splitter"))
    + c.source_ref("node_parser/text/sentence_window.py", "SentenceWindowNodeParser.from_defaults", L("句窗切块", "sentence-window parsing"))
    + c.accordion(
        L("深入：切块策略与旋钮", "Deep dive: chunking strategies and knobs"),
        c.qa_item(
            L("🧪 示例：SentenceSplitter(chunk_size=512, chunk_overlap=50)", "🧪 Example: SentenceSplitter(chunk_size=512, chunk_overlap=50)"),
            L(
                "默认切块器按句子把文本凑到约 512 token 一块、相邻块重叠 50 token。这组数值是通用起点："
                "块够大能容下完整语义，重叠又能护住边界句，适合大多数问答场景。",
                "The default splitter packs text into ~512-token chunks along sentence boundaries, with 50 tokens of "
                "overlap between neighbours. These values are a solid starting point: chunks large enough to hold a "
                "complete thought, with overlap guarding the boundary sentences — good for most Q&amp;A.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "切块本质是在“召回精度”和“上下文完整”之间找平衡：小块检索更准但易断章，大块语义更全但召回更糊。"
                "把 chunk_size / chunk_overlap 暴露成旋钮，就是把这个平衡权交给你按数据来调。",
                "Chunking is fundamentally a balance between recall precision and contextual completeness: small chunks "
                "retrieve more sharply but fragment meaning; large chunks keep meaning whole but blur recall. Exposing "
                "chunk_size / chunk_overlap as knobs hands that balance to you, to tune against your data.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "所有切块器都实现同一个 <code>get_nodes_from_documents</code> 接口。SentenceSplitter 先把文本拆成句子，"
                "再贪心地把句子凑到接近 chunk_size，遇到下一块时回退 chunk_overlap 个 token 作为重叠起点。",
                "Every splitter implements the same <code>get_nodes_from_documents</code> interface. SentenceSplitter "
                "first breaks text into sentences, then greedily packs sentences up to near chunk_size, backing off by "
                "chunk_overlap tokens as the overlapping start of the next chunk.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "<code>TokenTextSplitter</code> 按 token 数硬切，控长最严但可能切断句子；"
                "<code>SemanticSplitterNodeParser</code> 在语义断点处下刀，适合主题多变的长文；"
                "<code>SentenceWindowNodeParser</code> 用单句检索 + 窗口补上下文，兼顾精准与完整。",
                "<code>TokenTextSplitter</code> cuts strictly by token count — tightest length control but may split "
                "sentences; <code>SemanticSplitterNodeParser</code> cuts at semantic breakpoints, good for topically "
                "varied text; <code>SentenceWindowNodeParser</code> retrieves by single sentence then restores context "
                "via a window — precise and complete at once.",
            ),
        ),
    )
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
    + c.code(
        "from llama_index.core import VectorStoreIndex\n"
        "from llama_index.core.node_parser import SentenceWindowNodeParser\n"
        "from llama_index.core.postprocessor import MetadataReplacementPostProcessor\n\n"
        "parser = SentenceWindowNodeParser.from_defaults(\n"
        "    window_size=3, window_metadata_key='window',\n"
        "    original_text_metadata_key='original_text')\n"
        "index = VectorStoreIndex(parser.get_nodes_from_documents(docs))\n\n"
        "# 检索靠单句命中，喂给 LLM 前再用 window 把上下文换回来\n"
        "engine = index.as_query_engine(\n"
        "    similarity_top_k=2,\n"
        "    node_postprocessors=[MetadataReplacementPostProcessor(target_metadata_key='window')])\n"
        "print(engine.query('退款多久到账？'))",
        caption=L("句窗的完整用法：检索靠单句，喂给 LLM 时再换回窗口", "Full sentence-window flow: retrieve by sentence, swap the window back before the LLM sees it"),
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
    + d.compare2(
        (L("抽取前 Node.metadata", "Before — Node.metadata"), i18n.render(L(
            "检索只能靠正文向量。此刻元数据很<strong>稀</strong>：<code>{'page': 3}</code>——只有加载时带进来的页码。",
            "Retrieval can only ride on the body vector. Right now the metadata is <strong>sparse</strong>: "
            "<code>{'page': 3}</code> — just the page number carried in at load time.",
        ))),
        (L("抽取后 Node.metadata", "After — Node.metadata"), i18n.render(L(
            "抽取器补上三个键：<code>document_title='退款政策'</code>、"
            "<code>excerpt_keywords='退款,时效,原路'</code>、"
            "<code>questions_this_excerpt_can_answer='退款多久到账？'</code>。"
            "这些就是向量之外的<strong>第二检索通道</strong>：可按字段过滤，也让问句更易对齐。",
            "Extractors add three keys: <code>document_title='Refund policy'</code>, "
            "<code>excerpt_keywords='refund,timing,original'</code>, "
            "<code>questions_this_excerpt_can_answer='How long do refunds take?'</code>. That's the "
            "<strong>second retrieval channel</strong> beyond the vector: filterable by field, and far easier to "
            "align with a user's question.",
        ))),
        caption=L(
            "抽取前后对照同一个 Node.metadata：抽取器把它从一个页码，填成可过滤、可对齐问句的第二检索通道",
            "The same Node.metadata, before and after: extractors grow it from a lone page number into a filterable, "
            "question-aligned second retrieval channel",
        ),
    )
    + c.analogy(L(
        "给每张便利贴贴上<strong>标签和一句摘要</strong>：日后既能按主题筛，也能让“问题↔片段”更容易对上。",
        "Put a <strong>label and one-line summary</strong> on every sticky note: later you can filter by topic and "
        "match “question ↔ snippet” far more easily.",
    ))
    + d.flow([
        ("node", L("原始 Node", "Raw Node"), L("只有正文 + 少量元数据", "body + a little metadata")),
        ("llm", L("LLM 抽取", "LLM extraction"), L("读内容、按提示生成", "reads content, prompts the LLM")),
        ("meta", L("+标题 / 关键词 / 问题 / 摘要", "+title / keywords / questions / summary"), L("写进 metadata 键", "written into metadata keys")),
        ("hit", L("更易被检索到", "Easier to retrieve"), L("向量之外再加一条命中通道", "a hit channel beyond the vector")),
    ], caption=L(
        "抽取的意义在结果：Node 经 LLM 补齐元数据后，除了向量相似，还能靠字段过滤与问句对齐被命中",
        "Why extraction pays off: once an LLM fills in a Node's metadata, it can be hit not only by vector similarity "
        "but also by field filters and question alignment",
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
    + c.section(
        L("元数据 = 检索的第二通道", "Metadata: retrieval's second channel"),
        L(
            "向量相似度是第一检索通道，元数据是第二条。一方面，标题、来源、日期这类字段可做精确过滤"
            "（“只在某产品手册里检索”）；另一方面，像 questions_this_excerpt_can_answer 这样的字段，把"
            "“用户会怎么问”预先写进块里，让“问句”和“片段”在语义空间里更容易对齐、召回更稳。",
            "Vector similarity is the first retrieval channel; metadata is the second. On one hand, fields like title, "
            "source and date enable exact filtering (“search only this product manual”); on the other, fields like "
            "questions_this_excerpt_can_answer bake “how users would ask” into the chunk itself, aligning “question ↔ "
            "chunk” in semantic space for steadier recall.",
        ),
        d.flow(
            [
                ("split", L("SentenceSplitter", "SentenceSplitter"), L("切块 → Node", "split → Nodes")),
                ("title", L("TitleExtractor", "TitleExtractor"), L("写入 document_title", "writes document_title")),
                ("qa", L("QuestionsAnsweredExtractor", "QuestionsAnsweredExtractor"), L("写入 questions_…", "writes questions_…")),
            ],
            caption=L(
                "transformations 是一条流水线：切块器与抽取器依次加工同一批 Node",
                "transformations form one assembly line: splitter then extractors process the same Nodes in turn",
            ),
        ),
        c.alert(L(
            "抽取器都要<strong>调用 LLM</strong>，是有成本的一步：<strong>逐块</strong>抽取器（关键词 / 问题 / 摘要）"
            "开销随块数线性增长，<strong>按需选字段、别全开</strong>；确定性字段（来源 / 日期）在 Reader 阶段手写即可，零成本。",
            "Extractors <strong>call the LLM</strong> — a step that costs tokens: <strong>per-node</strong> ones "
            "(keywords / questions / summary) scale linearly with the chunk count, so <strong>pick fields on demand, "
            "don't enable them all</strong>; deterministic fields (source / date) are best hand-written at the Reader "
            "stage, for free.",
        ), kind="warn"),
    )
    + c.source_ref("extractors/metadata_extractors.py", "TitleExtractor · QuestionsAnsweredExtractor · KeywordExtractor · SummaryExtractor",
                   L("都作为 transformation 接入管道", "all plug in as pipeline transformations"))
    + c.accordion(
        L("深入：元数据抽取", "Deep dive: metadata extraction"),
        c.qa_item(
            L("🧪 示例：用 IngestionPipeline 串起抽取器", "🧪 Example: chain extractors in an IngestionPipeline"),
            L(
                "把 <code>SentenceSplitter</code> 与 <code>TitleExtractor</code>、<code>QuestionsAnsweredExtractor</code> "
                "放进 <code>IngestionPipeline(transformations=[...])</code>，<code>run</code> 一次就得到带标题与问题元数据的 Node。",
                "Put <code>SentenceSplitter</code> together with <code>TitleExtractor</code> and "
                "<code>QuestionsAnsweredExtractor</code> into <code>IngestionPipeline(transformations=[...])</code>; one "
                "<code>run</code> yields Nodes carrying title and question metadata.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "纯向量检索只会“按相似度”召回，遇到同义改写或宽泛提问容易漏。补上元数据这条第二通道，既能按字段"
                "过滤缩小范围，又能用“该块能回答的问题”把用户问句和片段对齐，召回更稳、更可控。",
                "Pure vector search only recalls “by similarity” and can miss paraphrases or broad questions. Adding "
                "metadata as a second channel lets you both filter by field to narrow scope and align user questions "
                "with chunks via “questions this chunk answers” — steadier, more controllable recall.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "每个 extractor 都是一个 transformation：按提示词生成内容、写进固定的 metadata 键"
                "（如 document_title / questions_this_excerpt_can_answer）。调用次数分两类："
                "<strong>逐块</strong>抽取器（Keyword / QuestionsAnswered / Summary）对每个 Node 各调一次 LLM，"
                "随块数 N 线性增长；<strong>文档级</strong>抽取器（如 TitleExtractor）大致每篇文档只推断一次再共享。"
                "所以总开销并非简单的 N×M。",
                "Each extractor is a transformation: it generates content from a prompt and writes it to a fixed "
                "metadata key (e.g. document_title / questions_this_excerpt_can_answer). The call count splits in two: "
                "<strong>per-node</strong> extractors (Keyword / QuestionsAnswered / Summary) make one LLM call per "
                "Node, growing linearly with the chunk count N; <strong>document-level</strong> ones (e.g. "
                "TitleExtractor) infer roughly once per document and share the result. So the total is not simply N×M.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "确定性的字段（来源、路径、日期、作者）直接在 Reader 阶段手工写入 metadata，零成本也零误差；"
                "只有需要“理解内容”才能得到的字段（标题、关键词、能回答的问题）才值得花 LLM 去抽取。两者常常混用。",
                "Deterministic fields (source, path, date, author) are best written by hand at the Reader stage — free "
                "and exact; only fields that require “understanding the content” (title, keywords, answerable "
                "questions) are worth an LLM extraction. In practice you mix both.",
            ),
        ),
    )
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
    + c.code(
        "from llama_index.core import Document\n"
        "from llama_index.core.schema import MetadataMode\n\n"
        "# 手工写入业务元数据（零 LLM 成本）\n"
        "doc = Document(\n"
        "    text='退款将在 7 个工作日内原路退回。',\n"
        "    metadata={'source': 'faq.md', 'product': 'wallet', 'internal_id': 'X-92'})\n\n"
        "# 控制元数据可见性：哪些不进 embedding、哪些不进给 LLM 的 prompt\n"
        "doc.excluded_embed_metadata_keys = ['internal_id']\n"
        "doc.excluded_llm_metadata_keys = ['internal_id']\n"
        "print(doc.get_content(metadata_mode=MetadataMode.EMBED))  # internal_id 不污染向量",
        caption=L("手工元数据 + excluded_embed_metadata_keys：让 ID 之类字段不污染向量", "Hand-written metadata + excluded_embed_metadata_keys: keep fields like IDs out of the vector"),
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
    + d.scatter(
        [
            (18, 24, L("退款政策", "refund policy")),
            (70, 72, L("配送时效", "shipping")),
            (28, 30, L("退货流程", "returns")),
            (80, 30, L("账号注册", "signup")),
            (22, 68, L("发票", "invoice")),
        ],
        (24, 28),
        k=2,
        caption=L(
            "查询（黄点）落在“退款/退货”一带，top-2 圈出语义最近的退款政策与退货流程，而非字面相同的块。"
            "注意：2D 散点只是直觉示意，真正的度量是两个向量的夹角（余弦相似度），而非图上的平面距离",
            "The query (amber) lands among “refund / returns”; top-2 circles the two nearest in meaning — refund "
            "policy and returns — not literally matching ones. Note: the 2D scatter is only an intuition; the real "
            "metric is the angle between the two vectors (cosine similarity), not flat distance on the plane",
        ),
    )
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
    + c.section(
        L("同一个 embedding 模型，才有可比的坐标系", "One embedding model, one comparable space"),
        L(
            "既然检索靠“向量够不够近”，那“用什么尺子量近”就至关重要。LlamaIndex 默认用<strong>余弦相似度</strong>，"
            "量的是两个向量的<strong>夹角</strong>——夹角越小越相关。由此引出一个硬约束：查询和文档"
            "<strong>必须用同一个 embedding 模型</strong>。反例很直接——文档用模型 A 向量化、查询却用模型 B，"
            "两者落在<strong>互不相通的坐标系</strong>里，算出来的相似度只是两堆无关数字的巧合，毫无意义。"
            "至于换“更强”的模型：通用榜单更高未必在<strong>你的领域</strong>里召回更好，领域专用或微调过的小模型"
            "常常胜过更大的通用模型；而且一旦更换，整个索引都得<strong>重新向量化</strong>。",
            "Since retrieval hinges on “are the vectors close enough”, what you measure closeness with matters. By "
            "default LlamaIndex uses <strong>cosine similarity</strong>, measuring the <strong>angle</strong> between "
            "two vectors — the smaller the angle, the more related. That implies a hard constraint: the query and the "
            "documents <strong>must use the same embedding model</strong>. The counter-example is stark — embed the "
            "documents with model A but the query with model B, and the two live in <strong>incompatible coordinate "
            "systems</strong>; any similarity you compute is a coincidence of unrelated numbers, meaningless. As for "
            "switching to a “stronger” model: a higher general-leaderboard score doesn't guarantee better recall in "
            "<strong>your</strong> domain — a domain-specific or fine-tuned smaller model often beats a bigger general "
            "one — and any switch forces a full <strong>re-embedding</strong> of the index.",
        ),
        d.flow(
            [
                ("text", L("文本", "text"), L("一段话或一个问题", "a passage or a question")),
                ("model", L("embed_model", "embed_model"), L("查询与文档共用同一个", "same one for query and docs")),
                ("vec", L("向量 [1536]", "vector [1536]"), L("语义的坐标，按余弦比近邻", "semantic coordinates, compared by cosine")),
            ],
            caption=L(
                "embedding 把文本映射成定长向量；只有查询与文档共用同一个模型，向量才落在同一个坐标系里、夹角才可比",
                "Embedding maps text to a fixed-length vector; only when query and documents share one model do the "
                "vectors live in the same space and their angle becomes comparable",
            ),
        ),
    )
    + c.source_ref("base/embeddings/base.py", "BaseEmbedding · similarity · SimilarityMode",
                   L("统一接口 + 相似度计算", "the unified interface + similarity"))
    + c.accordion(
        L("深入：embedding 与相似度", "Deep dive: embeddings and similarity"),
        c.qa_item(
            L("🧪 示例：把一句话变成向量", "🧪 Example: turn a sentence into a vector"),
            L(
                "<code>Settings.embed_model.get_text_embedding('退款政策是什么？')</code> 返回一个定长浮点数组"
                "（如 1536 维）。同一模型对“退款要多久”给出的向量，会和它在空间里靠得很近。",
                "<code>Settings.embed_model.get_text_embedding('What is the refund policy?')</code> returns a "
                "fixed-length float array (e.g. 1536 dims). The same model's vector for “how long do refunds take” lands "
                "right next to it in space.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "关键词匹配只认字面，换个说法就失灵。把文本投射到语义向量空间，让“意思相近”而非“用词相同”决定距离，"
                "才是语义检索的地基——这也是 RAG 能听懂同义改写的根本原因。",
                "Keyword matching only sees the literal words and breaks on paraphrase. Projecting text into a semantic "
                "vector space lets “similar meaning”, not “same wording”, set the distance — the bedrock of semantic "
                "search and the reason RAG understands rephrasings at all.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "所有 embedding 实现都遵循 <code>BaseEmbedding</code> 接口：<code>get_text_embedding</code> 给文档用、"
                "<code>get_query_embedding</code> 给查询用；检索时用 <code>similarity</code>（默认余弦）给候选打分排序，"
                "取分数最高的 top-k。",
                "Every embedding implementation follows the <code>BaseEmbedding</code> interface: "
                "<code>get_text_embedding</code> for documents, <code>get_query_embedding</code> for queries; at "
                "retrieval time <code>similarity</code> (cosine by default) scores and ranks candidates, keeping the "
                "top-k.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "关键词检索（如 BM25）按词频精确命中，擅长专有名词与代码符号，但不懂同义。向量检索懂语义却可能漏掉"
                "确切关键词。生产里常把两者<strong>混合检索</strong>（hybrid）再融合排序，兼得字面精确与语义召回。",
                "Keyword search (e.g. BM25) matches exactly by term frequency — great for proper nouns and code symbols "
                "but blind to synonyms. Vector search grasps meaning but may miss an exact keyword. In production you "
                "often combine them in <strong>hybrid retrieval</strong> and fuse the rankings — exact and semantic at "
                "once.",
            ),
        ),
    )
    + c.code(
        "from llama_index.core import Settings\n"
        "from llama_index.embeddings.openai import OpenAIEmbedding\n\n"
        "Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')\n"
        "v = Settings.embed_model.get_text_embedding('退款政策是什么？')\n"
        "print(len(v))   # 向量维度，如 1536\n\n"
        "# 语义越近，余弦相似度越高（检索就按它排序取 top-k）",
        caption=L("一次向量化，多次检索复用", "embed once, reuse across many queries"),
    )
    + c.code(
        "from llama_index.core import Settings\n"
        "from llama_index.embeddings.openai import OpenAIEmbedding\n\n"
        "emb = Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')\n"
        "a = emb.get_text_embedding('退款多久到账？')\n"
        "b = emb.get_text_embedding('退款需要几天？')      # 近义、不同词\n"
        "c = emb.get_text_embedding('如何注册新账号？')    # 另一主题\n\n"
        "print(round(emb.similarity(a, b), 3))   # 高：语义相近\n"
        "print(round(emb.similarity(a, c), 3))   # 低：语义无关",
        caption=L("同义不同词也能算出高相似度——这正是向量检索强于关键词的地方", "Paraphrases score high even with different words — exactly why vectors beat keywords"),
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
        "embedding 模型是管道里最“牵一发而动全身”的一环：它定义了整套语义坐标系，所以换 LLM、换切块器都只是局部调整，"
        "唯独换 embedding 模型必须把<strong>全部向量重算一遍</strong>——选型要趁早，更要贴合你的领域。",
        "The embedding model is the pipeline's most load-bearing link: it defines the entire semantic coordinate "
        "system, so swapping the LLM or the splitter is a local change — but swapping the embedding model forces you "
        "to <strong>re-embed every vector</strong>. Choose it early, and choose it for your domain.",
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
    + d.flow(
        [
            ("q", L("查询向量", "Query vector"), L("问题经 embedding 得到", "the question, embedded")),
            ("store", L("VectorStore", "VectorStore"), L("近邻搜索 + 元数据过滤", "nearest-neighbor + metadata filter")),
            ("topk", L("top-k Node", "top-k Nodes"), L("最相关的若干片段", "the most relevant chunks")),
        ],
        caption=L(
            "向量库的核心动作：拿查询向量，毫秒级返回最近邻的 top-k 个 Node",
            "A vector store's core move: take a query vector, return the top-k nearest Nodes in milliseconds",
        ),
    )
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
    + c.section(
        L("VectorStore 的职责与可替换性", "What a VectorStore owns, and why it's swappable"),
        d.annot(
            L("VectorStore", "VectorStore"),
            [
                (L("存向量", "store vectors"), L("每个 Node 一条", "one per Node")),
                (L("存元数据", "store metadata"), L("随向量一起存", "stored alongside")),
                (L("近邻查询", "nearest-neighbor"), L("返回 top-k，可按元数据过滤", "top-k, filterable by metadata")),
            ],
            caption=L("VectorStore 干三件事：存向量、存元数据、做近邻查询（可按元数据过滤）",
                      "a VectorStore does three things: store vectors, store metadata, run nearest-neighbor search (filterable by metadata)"),
        ),
        L(
            "VectorStore 干三件事：保存每个 Node 的向量、保存其元数据、并支持“给定一个查询向量、返回最近邻”。"
            "LlamaIndex 把这三件事抽象成统一契约，于是笔记本上的内存库和生产级引擎对上层看起来一模一样。你按 "
            "SimpleVectorStore 写通的代码，换成 Chroma 只动注入 StorageContext 的那几行，检索逻辑、索引、查询引擎全都不变。",
            "A VectorStore does three things: store each Node's vector, store its metadata, and answer “given a query "
            "vector, return the nearest neighbours”. LlamaIndex abstracts these into one contract, so a laptop's "
            "in-memory store and a production engine look identical upstream. Code you got working on SimpleVectorStore "
            "moves to Chroma by changing only the few lines that inject the StorageContext — retrieval, index and query "
            "engine all stay the same.",
        ),
        d.compare2(
            (L("内存 SimpleVectorStore", "In-memory SimpleVectorStore"), i18n.render(L(
                "零依赖，随进程而生灭；<strong>线性扫描</strong>全部向量，返回的是<strong>精确</strong>最近邻。"
                "适合学习、原型与小数据。",
                "Zero-dependency, lives and dies with the process; a <strong>linear scan</strong> over every vector "
                "returns the <strong>exact</strong> nearest neighbours. Great for learning, prototypes and small data.",
            ))),
            (L("生产向量库 Chroma · FAISS · pgvector", "Production store: Chroma · FAISS · pgvector"), i18n.render(L(
                "持久化、可扩展，用 <strong>ANN（近似最近邻）</strong>索引和元数据过滤，百万级向量也能毫秒级返回。"
                "代价是“近似”：用一点召回率换巨大的速度，命中率<strong>可调但并非 100%</strong>。",
                "Persistent and scalable; an <strong>ANN (approximate nearest-neighbor)</strong> index plus metadata "
                "filters answer in milliseconds even at millions of vectors. The catch is “approximate”: it trades a "
                "little recall for huge speed, so hit rate is <strong>tunable, not a guaranteed 100%</strong>.",
            ))),
            caption=L(
                "同一个 VectorStore 接口，两种实现：上线只是换实现，不是重写",
                "One VectorStore interface, two impls: going live is a swap, not a rewrite",
            ),
        ),
    )
    + c.source_ref("vector_stores/simple.py", "SimpleVectorStore", L("默认内存向量库", "the default in-memory store"))
    + c.source_ref("vector_stores/types.py", "VectorStoreQuery", L("统一的相似度查询契约", "the unified similarity-query contract"))
    + c.accordion(
        L("深入：向量库的统一契约", "Deep dive: the vector store's unified contract"),
        c.qa_item(
            L("🧪 示例：默认内存库 vs 注入 Chroma", "🧪 Example: in-memory default vs injecting Chroma"),
            L(
                "<code>VectorStoreIndex.from_documents(docs)</code> 默认用内存 SimpleVectorStore；要换 Chroma，只需"
                "构造 <code>ChromaVectorStore</code>、用 <code>StorageContext.from_defaults(vector_store=...)</code> 注入，"
                "其余代码原样不动。",
                "<code>VectorStoreIndex.from_documents(docs)</code> uses the in-memory SimpleVectorStore by default; to "
                "switch to Chroma you only build a <code>ChromaVectorStore</code> and inject it via "
                "<code>StorageContext.from_defaults(vector_store=...)</code> — everything else stays put.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "把“近邻搜索”收敛成一个统一接口，意味着你能在不重写检索逻辑的前提下，从笔记本无缝升级到生产引擎——"
                "选向量库变成一个纯运维/规模问题，而非代码架构问题。",
                "Collapsing nearest-neighbor search into one interface lets you upgrade from laptop to production engine "
                "without rewriting retrieval logic — picking a store becomes an ops/scale decision, not an "
                "architectural one.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "上层把查询打包成 <code>VectorStoreQuery</code>（含 <code>query_embedding</code>、"
                "<code>similarity_top_k</code> 与可选 <code>filters</code>），交给具体向量库执行，返回命中的 Node 与分数。"
                "各家库实现各异，但都满足这同一份契约。",
                "The layer above packs a query into a <code>VectorStoreQuery</code> (carrying "
                "<code>query_embedding</code>, <code>similarity_top_k</code> and optional <code>filters</code>) and "
                "hands it to the concrete store, which returns matching Nodes with scores. Each store implements it "
                "differently but all honour the same contract.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "Chroma 上手简单、本地友好；FAISS 极快但偏库而非服务；pgvector 复用现成 Postgres、便于事务与运维；"
                "Qdrant / Weaviate 等是云原生向量服务。取舍点在规模、过滤能力、运维成本与是否需要持久化。",
                "Chroma is easy and local-friendly; FAISS is blazingly fast but a library, not a service; pgvector "
                "reuses your existing Postgres for transactions and ops; Qdrant / Weaviate are cloud-native vector "
                "services. You trade off scale, filtering, ops cost and whether you need persistence.",
            ),
        ),
    )
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
    + c.code(
        "from llama_index.core import VectorStoreIndex\n"
        "from llama_index.core.vector_stores import (\n"
        "    MetadataFilters, MetadataFilter, FilterOperator)\n\n"
        "index = VectorStoreIndex.from_documents(docs)\n\n"
        "# 近邻搜索 + 元数据过滤：只在 source='faq' 且 year &gt;= 2024 的块里找\n"
        "flt = MetadataFilters(filters=[\n"
        "    MetadataFilter(key='source', value='faq'),\n"
        "    MetadataFilter(key='year', value=2024, operator=FilterOperator.GTE),\n"
        "])\n"
        "engine = index.as_query_engine(similarity_top_k=3, filters=flt)\n"
        "print(engine.query('最新的退款政策？'))",
        caption=L("把近邻搜索和元数据过滤组合，检索更准也更可控", "Combine nearest-neighbor with metadata filters for tighter, more controllable retrieval"),
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
    + d.grid(
        [L("Index", "Index"), L("组织方式", "Organizes by"), L("适合", "Best for")],
        [
            [L("VectorStoreIndex", "VectorStoreIndex"), L("向量空间近邻", "nearest-neighbor in vector space"), L("相似问答", "similarity Q&amp;A")],
            [L("SummaryIndex", "SummaryIndex"), L("线性 Node 列表", "a linear list of Nodes"), L("整库总结", "whole-corpus summary")],
            [L("DocumentSummaryIndex", "DocumentSummaryIndex"), L("每篇文档一份摘要", "one summary per document"), L("多文档路由", "routing across docs")],
            [L("PropertyGraphIndex", "PropertyGraphIndex"), L("实体-关系图", "an entity-relation graph"), L("多跳/关系推理", "multi-hop / relations")],
        ],
        caption=L(
            "四种 Index = 四种组织 Node 的方式，各自擅长一类问题",
            "Four Indexes = four ways to organize Nodes, each best at one kind of question",
        ),
    )
    + c.analogy(L(
        "同一堆资料的不同<strong>组织法</strong>：词典（按相似度近邻）、章节大纲（逐条遍历总结）、知识图谱（按实体关系跳转）。",
        "Different <strong>organizations</strong> of the same pile: a dictionary (nearest-neighbor), a chapter outline "
        "(walk every entry to summarize), a knowledge graph (hop by entity relations).",
    ))
    + c.section(
        L("同一个问题，两种 Index 两种答案", "One question, two Indexes, two answers"),
        L(
            "选错 Index，再好的数据也答非所问。拿同一句问题分别问两种最常见的索引，差别一目了然：",
            "Pick the wrong Index and even great data answers the wrong question. Put the same question to the two "
            "most common Indexes and the difference is obvious:",
        ),
        d.compare2(
            (L("VectorStoreIndex", "VectorStoreIndex"), i18n.render(L(
                "把问题向量化，只<strong>定点召回</strong>最相关的 top-k 段再作答：回答“退款多久到账？”这类具体细节"
                "又快又准；但问“整份资料讲了什么”时，只看几段容易<strong>以偏概全</strong>。",
                "Embeds the question and answers from just the <strong>top-k</strong> most similar chunks: fast and "
                "precise for specifics like “how long do refunds take?”, but asked “what does the whole corpus cover?” "
                "it sees only a few chunks and tends to <strong>generalize from a fragment</strong>.",
            ))),
            (L("SummaryIndex", "SummaryIndex"), i18n.render(L(
                "不挑不选，<strong>遍历全部</strong> Node 逐步归纳：天生适合“总结全库”“这批文档讲了什么”；"
                "代价是每次都读全量，问具体细节时既慢又贵。",
                "Picks nothing — it <strong>walks every</strong> Node and synthesizes: a natural fit for “summarize the "
                "whole corpus” / “what do these docs cover”; the cost is reading everything each time, so it's slow "
                "and pricey for narrow questions.",
            ))),
            caption=L(
                "同一句问题，两种 Index 给出不同答案：向量索引定点召回最相关几段，摘要索引遍历全库做归纳",
                "Same question, two Indexes, two answers: the vector index pinpoints the most relevant chunks; the "
                "summary index walks the whole corpus to synthesize",
            ),
        ),
    )
    + c.section(
        L("选 Index = 选检索范式", "Choosing an Index = choosing a retrieval paradigm"),
        L(
            "Index 决定的不是“存哪儿”，而是“怎么找”。VectorStoreIndex 把 Node 摆进向量空间、按相似度近邻召回；"
            "SummaryIndex 把 Node 排成一列、逐条遍历做全局总结；PropertyGraphIndex 把 Node 连成实体关系图、"
            "按边跳转做多跳推理。同一堆资料，选不同 Index 就得到不同的检索范式——而它们都用 from_documents / "
            "as_query_engine 的同款入口，让你能用同一套代码切换甚至组合。",
            "An Index decides not “where things live” but “how you find them”. VectorStoreIndex places Nodes in vector "
            "space and recalls by similarity; SummaryIndex lines Nodes up and walks them all for a global summary; "
            "PropertyGraphIndex links Nodes into an entity-relation graph and hops along edges for multi-hop "
            "reasoning. Same pile of data, different Index, different retrieval paradigm — yet all share the "
            "from_documents / as_query_engine entry points, so you switch or even combine them with the same code.",
        ),
        d.flow(
            [
                ("index", L("任意 Index", "Any Index"), L("from_documents 建好", "built via from_documents")),
                ("engine", L("as_query_engine()", "as_query_engine()"), L("统一的问答入口", "one uniform Q&amp;A entry")),
                ("router", L("RouterQueryEngine", "RouterQueryEngine"), L("按问题自动选 Index", "auto-pick an Index per question")),
            ],
            caption=L(
                "不同 Index 共用同一个 as_query_engine 入口，还能用 Router 在它们之间分流",
                "Every Index shares the same as_query_engine entry; a Router can even dispatch between them",
            ),
        ),
    )
    + c.source_ref("indices/vector_store/base.py", "VectorStoreIndex", L("最常用的相似检索索引", "the common similarity index"))
    + c.source_ref("indices/list/base.py", "SummaryIndex", L("遍历式索引（原 ListIndex）", "the iterate-all index (formerly ListIndex)"))
    + c.accordion(
        L("深入：Index 抽象", "Deep dive: the Index abstraction"),
        c.qa_item(
            L("🧪 示例：VectorStoreIndex vs SummaryIndex", "🧪 Example: VectorStoreIndex vs SummaryIndex"),
            L(
                "同一批 docs，<code>VectorStoreIndex</code> 适合“退款政策是什么”这类定点问答（按相似度取 top-k）；"
                "<code>SummaryIndex</code> 适合“全文讲了什么”这类整库总结（遍历所有 Node 再归纳）。",
                "On the same docs, <code>VectorStoreIndex</code> suits pinpoint questions like “what's the refund "
                "policy” (top-k by similarity), while <code>SummaryIndex</code> suits whole-corpus asks like “what does "
                "the text cover” (walk every Node, then summarize).",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "不同问题需要不同的“组织 + 检索”策略：定点问答要近邻、全局总结要遍历、关系推理要图。把它们做成可互换的 "
                "Index，就能用同一套上层代码服务截然不同的问法。",
                "Different questions need different “organize + retrieve” strategies: pinpoint Q&amp;A wants "
                "nearest-neighbor, global summary wants iteration, relational reasoning wants a graph. Making them "
                "interchangeable Indexes lets one upper layer serve very different question shapes.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "所有 Index 都继承 <code>BaseIndex</code>，共享 <code>from_documents</code>（建索引）与 "
                "<code>as_query_engine</code> / <code>as_retriever</code>（装配查询）。差异只在于内部如何组织 Node、"
                "以及默认配哪种 retriever 与 response 合成策略。",
                "Every Index inherits <code>BaseIndex</code>, sharing <code>from_documents</code> (build) and "
                "<code>as_query_engine</code> / <code>as_retriever</code> (assemble queries). They differ only in how "
                "they organize Nodes internally and which default retriever and response strategy they wire up.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "当一个库里既有定点问答又有整库总结时，可建多个 Index，再用 <code>RouterQueryEngine</code> 按问题"
                "自动路由到合适的那个；也可以组合检索器、做多 Index 融合。单一 Index 简单，多 Index + Router 更全能。",
                "When a corpus needs both pinpoint Q&amp;A and global summaries, build several Indexes and let a "
                "<code>RouterQueryEngine</code> auto-route each question to the right one; you can also compose "
                "retrievers and fuse multiple Indexes. One Index is simpler; many Indexes + a Router is more capable.",
            ),
        ),
    )
    + c.code(
        "from llama_index.core import VectorStoreIndex, SummaryIndex\n\n"
        "vindex = VectorStoreIndex.from_documents(docs)   # 相似问答\n"
        "print(vindex.as_query_engine().query('退款政策？'))\n\n"
        "sindex = SummaryIndex.from_documents(docs)        # 整库总结\n"
        "print(sindex.as_query_engine(response_mode='tree_summarize').query('全文讲了什么？'))",
        caption=L("选 Index 就是选检索范式", "choosing an Index = choosing a retrieval style"),
    )
    + c.code(
        "from llama_index.core import VectorStoreIndex, SummaryIndex\n"
        "from llama_index.core.tools import QueryEngineTool\n"
        "from llama_index.core.query_engine import RouterQueryEngine\n\n"
        "vector_tool = QueryEngineTool.from_defaults(\n"
        "    VectorStoreIndex.from_documents(docs).as_query_engine(),\n"
        "    description='按相似度回答具体细节问题')\n"
        "summary_tool = QueryEngineTool.from_defaults(\n"
        "    SummaryIndex.from_documents(docs).as_query_engine(response_mode='tree_summarize'),\n"
        "    description='对全文做整体总结')\n\n"
        "# Router 读 description，自动把问题分给合适的 Index\n"
        "engine = RouterQueryEngine.from_defaults([vector_tool, summary_tool])\n"
        "print(engine.query('全文主要讲了什么？'))",
        caption=L("多 Index + Router：让框架按问题自动选检索范式", "Many Indexes + a Router: let the framework auto-pick the retrieval paradigm per question"),
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
        "<strong>IngestionPipeline</strong> 把切块、抽取、向量化串成一条<strong>可缓存、可去重</strong>的管道，"
        "重复运行只处理变化的部分。索引建好后，用 <code>storage_context.persist</code> 整体落盘，"
        "下次用顶层函数 <code>load_index_from_storage</code>（传入 StorageContext）秒开，免去每次重建。",
        "An <strong>IngestionPipeline</strong> chains splitting, extraction and embedding into a "
        "<strong>cacheable, dedup-aware</strong> pipeline, so re-runs only touch what changed. Once the index is "
        "built, <code>storage_context.persist</code> writes it to disk, and the top-level "
        "<code>load_index_from_storage</code> (given a StorageContext) reloads it instantly — no rebuild next time.",
    ))
    + d.flow(
        [
            ("split", L("split 切块", "split"), L("SentenceSplitter", "SentenceSplitter")),
            ("extract", L("extract 抽取", "extract"), L("TitleExtractor …", "TitleExtractor …")),
            ("embed", L("embed 向量化", "embed"), L("embed_model", "embed_model")),
            ("cache", L("cache 缓存", "cache"), L("相同输入命中、不重算", "same input hits cache, skips recompute")),
            ("docstore", L("docstore 去重", "docstore dedup"), L("按内容哈希增量更新", "incremental by content hash")),
        ],
        caption=L(
            "一条摄取管道：transformations 依次加工，cache 跳过重复计算，docstore 按文档去重",
            "One ingestion pipeline: transformations process in turn, the cache skips repeats, the docstore dedups by document",
        ),
    )
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
    + c.section(
        L("把建索引做成幂等、可缓存的管道", "Make indexing an idempotent, cacheable pipeline"),
        L(
            "demo 里“每次重跑都全量重建”尚可忍受，生产里却致命：数据天天变，全量重算既慢又贵。IngestionPipeline "
            "把摄取做成幂等管道——run 时对每个转换的输入算内容哈希，命中缓存就跳过；配上 docstore，相同文档不重复"
            "处理，只有变化的文档才走完整流程。再用 persist / load 把成品索引落盘，重启免重建。这三件事合起来，"
            "才让 RAG 从“能跑通”走到“可维护”。",
            "“Rebuild everything on every run” is tolerable in a demo but fatal in production: data changes daily and "
            "full recomputation is slow and costly. IngestionPipeline makes ingestion idempotent — on run it hashes "
            "each transformation's input and skips on a cache hit; paired with a docstore, identical documents aren't "
            "reprocessed and only changed docs run the full path. Then persist / load put the finished index on disk "
            "so restarts skip the rebuild. Together these three take RAG from “it runs” to “it's maintainable”.",
        ),
        d.layers(
            [
                (L("persist(persist_dir)", "persist(persist_dir)"), L("把内存中的索引整体写到磁盘", "writes the in-memory index to disk")),
                (L("docstore.json", "docstore.json"), L("Node 正文与元数据", "Node text and metadata")),
                (L("index_store.json", "index_store.json"), L("索引结构（谁指向谁）", "the index structure (what points to what)")),
                (L("vector_store.json", "vector_store.json"), L("向量数据", "the vectors")),
                (L("load_index_from_storage", "load_index_from_storage"), L("从三件套重建索引，秒级开门", "rebuilds the index from the three — open in seconds")),
            ],
            caption=L(
                "persist 把索引拆成磁盘上的三件套，load 再把它们拼回可查询的索引；"
                "不过生产里若向量交给外部库（Chroma / pgvector）托管，向量就不在本地，落盘的往往只剩 docstore 与 index_store",
                "persist splits the index into three local files; load stitches them back into a queryable index. In "
                "production, though, if the vectors live in an external store (Chroma / pgvector) they aren't local — "
                "often only the docstore and index_store hit disk",
            ),
        ),
    )
    + c.source_ref("ingestion/pipeline.py", "IngestionPipeline.run", L("可缓存/去重的摄取管道", "the cacheable, dedup-aware pipeline"))
    + c.source_ref("storage/storage_context.py", "StorageContext.persist", L("把 docstore/index/vector 一起落盘", "persists docstore/index/vector together"))
    + c.source_ref("indices/loading.py", "load_index_from_storage", L("从磁盘恢复索引", "reload an index from disk"))
    + c.accordion(
        L("深入：摄取管道与持久化", "Deep dive: the ingestion pipeline and persistence"),
        c.qa_item(
            L("🧪 示例：带 docstore 的 IngestionPipeline", "🧪 Example: an IngestionPipeline with a docstore"),
            L(
                "<code>IngestionPipeline(transformations=[...], docstore=SimpleDocumentStore())</code> 第一次 run 会"
                "完整处理所有文档；之后再 run，未变化的文档直接命中缓存/去重，只有新增或改动的文档才重新加工。",
                "<code>IngestionPipeline(transformations=[...], docstore=SimpleDocumentStore())</code> processes every "
                "document on the first run; on later runs unchanged documents hit the cache/dedup, and only new or "
                "modified documents are reprocessed.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "生产数据是活的：每天只有一小部分变化。幂等 + 缓存 + 去重让“重建索引”的代价正比于<strong>变化量</strong>"
                "而非总量，既省钱又省时，还保证重复运行结果一致。",
                "Production data is alive: only a small slice changes each day. Idempotency + cache + dedup make the "
                "cost of “rebuilding the index” proportional to the <strong>delta</strong>, not the total — cheaper, "
                "faster, and consistent across repeated runs.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "<code>run</code> 时，管道对每个转换的（输入 Node + 转换配置）算一个哈希作为缓存键，命中就复用上次结果；"
                "docstore 则按 doc_id 记录每个文档的内容哈希，配合 <code>DocstoreStrategy</code> 决定是 UPSERT 还是跳过。",
                "On <code>run</code>, the pipeline hashes each transformation's (input Nodes + config) into a cache key "
                "and reuses last time's output on a hit; the docstore records each document's content hash by doc_id "
                "and, via a <code>DocstoreStrategy</code>, decides whether to UPSERT or skip.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "不用管道也能跑：每次都 <code>from_documents</code> 全量重建。小数据时无所谓，但随着库变大，"
                "全量重算的时间和 embedding 费用会线性膨胀——这正是增量摄取存在的理由。",
                "You can skip the pipeline and just <code>from_documents</code> from scratch every time. Fine for small "
                "data, but as the corpus grows the recompute time and embedding bill scale linearly — exactly why "
                "incremental ingestion exists.",
            ),
        ),
    )
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
    + c.code(
        "from llama_index.core import Document\n"
        "from llama_index.core.ingestion import IngestionPipeline, IngestionCache\n"
        "from llama_index.core.node_parser import SentenceSplitter\n"
        "from llama_index.core.storage.docstore import SimpleDocumentStore\n\n"
        "pipeline = IngestionPipeline(\n"
        "    transformations=[SentenceSplitter(chunk_size=512)],\n"
        "    docstore=SimpleDocumentStore(),   # 去重：按 doc_id + 内容哈希判断是否变化\n"
        "    cache=IngestionCache(),           # 缓存：相同输入直接复用上次结果\n"
        ")\n\n"
        "docs = [Document(text='退款政策……', doc_id='faq-1')]\n"
        "print(len(pipeline.run(documents=docs)))   # 首次：完整处理\n\n"
        "docs = [Document(text='退款政策（已更新）……', doc_id='faq-1')]   # 同一 doc_id、内容已更新\n"
        "print(len(pipeline.run(documents=docs)))   # 再跑：仅这篇重算，其余命中缓存",
        caption=L("第二次 run 只处理变化的文档，其余命中缓存/去重——这就是增量摄取", "The second run touches only changed docs; the rest hit cache/dedup — that's incremental ingestion"),
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
