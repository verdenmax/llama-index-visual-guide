"""Part 2 (write path): lessons 04-11. Content filled task-by-task."""
import components as c
from i18n import L


def _stub():
    return c.pipeline(None) + c.lead(L("（本课内容建设中）", "(Lesson content coming soon)"))


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
LESSON_07 = _stub()
LESSON_08 = _stub()
LESSON_09 = _stub()
LESSON_10 = _stub()
LESSON_11 = _stub()
