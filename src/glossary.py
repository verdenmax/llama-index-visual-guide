"""Part 6 (reference): lesson 21 glossary. Content filled task-by-task."""
import components as c
from i18n import L


def _stub():
    return c.pipeline(None) + c.lead(L("（本课内容建设中）", "(Lesson content coming soon)"))


def _term(zh, en):
    return L(zh, en)


LESSON_21 = (
    c.lead(L(
        "全书术语一句话速查，点“课”跳到对应讲解。", "One-line lookups for every term; click “Lesson” to jump to it.",
    ))
    + c.compare_table(
        [L("术语 Term", "术语 Term"), L("一句话 In a line", "一句话 In a line"), L("课 Lesson", "课 Lesson")],
        [
            [L("<code>RAG</code>", "<code>RAG</code>"), _term("检索增强生成：先检索相关片段再让 LLM 生成", "retrieve relevant chunks, then let the LLM generate"), L('<a href="01-what-is-llamaindex.html">01</a>', '<a href="01-what-is-llamaindex.html">01</a>')],
            [L("<code>Document</code>", "<code>Document</code>"), _term("一整份原始资料", "one whole raw source"), L('<a href="04-documents-nodes.html">04</a>', '<a href="04-documents-nodes.html">04</a>')],
            [L("<code>Node</code>", "<code>Node</code>"), _term("切块后带元数据/关系的检索单位", "a chunked, metadata-bearing unit of retrieval"), L('<a href="04-documents-nodes.html">04</a>', '<a href="04-documents-nodes.html">04</a>')],
            [L("Reader", "Reader"), _term("把来源加载成 Document", "loads a source into Documents"), L('<a href="05-readers.html">05</a>', '<a href="05-readers.html">05</a>')],
            [L("Node Parser", "Node Parser"), _term("把 Document 切成 Node（chunking）", "splits Documents into Nodes (chunking)"), L('<a href="06-node-parsers.html">06</a>', '<a href="06-node-parsers.html">06</a>')],
            [L("<code>chunk_size/overlap</code>", "<code>chunk_size/overlap</code>"), _term("切块大小与相邻重叠", "chunk length and adjacent overlap"), L('<a href="06-node-parsers.html">06</a>', '<a href="06-node-parsers.html">06</a>')],
            [L("Extractor", "Extractor"), _term("用 LLM 为 Node 生成元数据", "LLM-generates metadata for Nodes"), L('<a href="07-metadata-extractors.html">07</a>', '<a href="07-metadata-extractors.html">07</a>')],
            [L("Embedding", "Embedding"), _term("文本→向量，使语义相近=距离近", "text→vector so similar=close"), L('<a href="08-embeddings.html">08</a>', '<a href="08-embeddings.html">08</a>')],
            [L("Vector Store", "Vector Store"), _term("存向量+元数据并做近邻查询", "stores vectors+metadata, does NN search"), L('<a href="09-vector-stores.html">09</a>', '<a href="09-vector-stores.html">09</a>')],
            [L("Index", "Index"), _term("为某种检索方式组织 Node 的结构", "structure organizing Nodes for a retrieval style"), L('<a href="10-index-abstraction.html">10</a>', '<a href="10-index-abstraction.html">10</a>')],
            [L("Ingestion Pipeline", "Ingestion Pipeline"), _term("可缓存/去重的摄取管道", "cacheable, dedup-aware ingestion"), L('<a href="11-ingestion-storage.html">11</a>', '<a href="11-ingestion-storage.html">11</a>')],
            [L("<code>persist/load</code>", "<code>persist/load</code>"), _term("索引落盘与恢复", "persist an index and reload it"), L('<a href="11-ingestion-storage.html">11</a>', '<a href="11-ingestion-storage.html">11</a>')],
            [L("Retriever", "Retriever"), _term("取回 top-k 相关 Node", "fetches the top-k relevant Nodes"), L('<a href="12-retrievers.html">12</a>', '<a href="12-retrievers.html">12</a>')],
            [L("Postprocessor", "Postprocessor"), _term("生成前过滤/重排/替换 Node", "filter/rerank/replace Nodes before generation"), L('<a href="13-postprocessors.html">13</a>', '<a href="13-postprocessors.html">13</a>')],
            [L("Response Synthesizer", "Response Synthesizer"), _term("多片段→单答案的策略", "the many-chunks→one-answer strategy"), L('<a href="14-response-synthesizers.html">14</a>', '<a href="14-response-synthesizers.html">14</a>')],
            [L("Query Engine", "Query Engine"), _term("检索+后处理+合成的组合根", "composition root: retrieve+postproc+synth"), L('<a href="15-query-engine.html">15</a>', '<a href="15-query-engine.html">15</a>')],
            [L("Chat Engine", "Chat Engine"), _term("带记忆的多轮 RAG", "multi-turn RAG with memory"), L('<a href="16-chat-engine.html">16</a>', '<a href="16-chat-engine.html">16</a>')],
            [L("<code>Settings</code>", "<code>Settings</code>"), _term("全局默认配置（取代 ServiceContext）", "global defaults (replaces ServiceContext)"), L('<a href="17-settings-prompts.html">17</a>', '<a href="17-settings-prompts.html">17</a>')],
            [L("Evaluation", "Evaluation"), _term("忠实/相关/正确三类打分", "faithful/relevant/correct scoring"), L('<a href="19-evaluation.html">19</a>', '<a href="19-evaluation.html">19</a>')],
        ],
    )
)
