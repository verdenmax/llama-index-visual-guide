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
        L("relationships（SOURCE/PREVIOUS/NEXT）是进阶检索（如自动合并）的基础。",
          "relationships (SOURCE/PREVIOUS/NEXT) underpin advanced retrieval (e.g. auto-merging)."),
    ])
    + c.design_highlight(L(
        "统一的 <strong>Node</strong> 抽象让整条管道“说同一种语言”：无论来源是 PDF 还是数据库，"
        "下游都只面对带元数据与关系的 Node。",
        "A single <strong>Node</strong> abstraction makes the whole pipeline speak one language: whether the source "
        "is a PDF or a database, everything downstream only deals with metadata-and-relationship-bearing Nodes.",
    ))
)
LESSON_05 = _stub()
LESSON_06 = _stub()
LESSON_07 = _stub()
LESSON_08 = _stub()
LESSON_09 = _stub()
LESSON_10 = _stub()
LESSON_11 = _stub()
