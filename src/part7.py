"""Part 7 (beyond plain-text RAG): lessons 27-31. Content filled task-by-task."""
import components as c
import diagrams as d
import i18n
from i18n import L


def _skeleton(stage, zh_topic, en_topic):
    return (
        c.pipeline(stage)
        + c.lead(L(f"本课讲 <strong>{zh_topic}</strong>（内容完善中）。",
                   f"This lesson covers <strong>{en_topic}</strong> (being written)."))
        + d.flow([("a", L("场景", "Scenario")), ("b", L("做法", "Approach")), ("c", L("权衡", "Trade-off"))],
                 caption=L("占位流程图", "placeholder flow"))
        + d.compare2((L("不做", "Without"), i18n.render(L("有什么问题", "what breaks"))),
                     (L("做了", "With"), i18n.render(L("解决什么", "what it fixes"))),
                     caption=L("占位对照", "placeholder compare"))
        + c.analogy(L("占位类比。", "Placeholder analogy."))
        + c.key_points([L("本课要点占位。", "Key-points placeholder.")])
    )


LESSON_27 = (
    c.pipeline("index")
    + c.lead(L(
        "前面 26 课的检索都在做同一件事：把问题和文档块都变成向量，取回<strong>最相似的 top-k 片段</strong>。"
        "可“相似”召不回“<strong>连起来的事实</strong>”——当答案要顺着“<strong>A 的供应商 → 供应商的总部 → "
        "总部所在国</strong>”这样的<strong>多跳关系</strong>走时，没有任何单个片段同时写着这三件事，纯向量自然"
        "答不出。<strong>图谱 RAG</strong> 换一种存法：用 LLM 把文档抽成<strong>实体—关系—实体</strong>的三元组、"
        "连成一张图；查询时从问题里的实体出发，<strong>顺着边一跳跳走</strong>，把分散在多处、却被关系串起来的"
        "事实收集起来。一句话：向量问“<strong>像不像</strong>”，图谱问“<strong>连不连</strong>”。",
        "The first 26 lessons' retrieval all did the same thing: turn the question and the doc chunks into vectors and "
        "fetch the <strong>top-k most similar chunks</strong>. But “similar” can't recall “<strong>connected facts"
        "</strong>” — when an answer must follow a <strong>multi-hop chain</strong> like “<strong>A's supplier → the "
        "supplier's HQ → the HQ's country</strong>”, no single chunk states all three at once, so pure vectors simply "
        "can't answer. <strong>Graph RAG</strong> stores things differently: an LLM extracts documents into "
        "<strong>entity—relation—entity</strong> triples wired into a graph; at query time it starts from the entities "
        "in the question and <strong>walks edge by edge, hop by hop</strong>, gathering facts that sit in different "
        "places yet are strung together by relations. In a line: vectors ask “<strong>similar?</strong>”, a graph asks "
        "“<strong>connected?</strong>”.",
    ))
    + d.compare2(
        (L("向量检索", "Vector"), i18n.render(L("取回 top-k <strong>相似</strong>片段；跨片段的关系丢失",
                                               "fetches top-k <strong>similar</strong> chunks; cross-chunk relations are lost"))),
        (L("图谱检索", "Graph"), i18n.render(L("沿 实体→关系→实体 <strong>多跳</strong>找到连起来的事实",
                                              "walks entity→relation→entity to find <strong>connected</strong> facts"))),
        caption=L("同一问题：向量看“像不像”，图谱看“连不连”", "Same question: vector asks ‘similar?’, graph asks ‘connected?’"),
    )
    + c.section(
        L("为什么要图谱：向量召回“相似”，图谱召回“连起来”",
          "Why a graph: vectors recall the “similar”, a graph recalls the “connected”"),
        L(
            "纯向量检索把每个文档块<strong>独立</strong>编码成一个语义向量，召回的是和问题<strong>最像</strong>的片段。"
            "这对“换种问法、近义改写”很在行，但它有个结构性盲区：<strong>跨片段的关系会丢</strong>。问“X-2000 的供应商"
            "总部在哪个国家”，答案要顺着“<strong>X-2000 → 供应商 → 总部 → 国家</strong>”连走三跳，而这三段事实往往"
            "<strong>分散在不同文档</strong>里、没有任何一个片段同时写全——于是无论 top-k 取多大，都召不回那条<strong>"
            "把它们串起来的链</strong>。图谱把事实存成<strong>实体—关系—实体</strong>的三元组（如 X-2000 —替代→ "
            "X-1000），查询时<strong>顺着边一跳跳遍历</strong>，正好把“连起来的事实”找回来。这就是图谱补的那块：不是"
            "“更像”，而是“<strong>能连</strong>”。",
            "Pure vector search encodes each doc chunk <strong>independently</strong> into one semantic vector and "
            "recalls the chunks <strong>most similar</strong> to the question. That's great for “rephrasings and "
            "synonyms”, but it has a structural blind spot: <strong>cross-chunk relations are lost</strong>. Ask “which "
            "country is the HQ of X-2000's supplier in” and the answer must follow “<strong>X-2000 → supplier → HQ → "
            "country</strong>” across three hops, yet those three facts usually <strong>sit in different documents"
            "</strong> with no single chunk stating them all — so however large top-k is, the <strong>chain that "
            "strings them together</strong> is never recalled. A graph stores facts as <strong>entity—relation—entity"
            "</strong> triples (e.g. X-2000 —replaces→ X-1000) and at query time <strong>traverses edge by edge, hop "
            "by hop</strong>, recovering exactly those “connected facts”. That's the gap a graph fills: not “more "
            "similar”, but “<strong>can connect</strong>”.",
        ),
    )
    + d.annot(
        L("实体：X-2000", "Entity: X-2000"),
        [
            (L("属于 → 产品线 A", "belongs to → line A"), L("一跳", "1 hop")),
            (L("兼容 → 配件 B", "compatible with → part B"), L("一跳", "1 hop")),
            (L("替代 → 旧款 X-1000", "replaces → old X-1000"), L("可继续多跳", "hop again")),
        ],
        caption=L("图谱把事实存成 实体—关系—实体 三元组，可顺着边多跳遍历",
                  "a graph stores facts as entity—relation—entity triples you can traverse hop by hop"),
    )
    + c.section(
        L("怎么建：PropertyGraphIndex 用 LLM 抽三元组",
          "How to build: PropertyGraphIndex extracts triples with an LLM"),
        L(
            "建图的核心是<strong>抽取</strong>：把自然语言里的事实变成结构化的<strong>实体—关系—实体</strong>三元组。"
            "<code>PropertyGraphIndex.from_documents(...)</code> 接受一组 <code>kg_extractors</code>（知识图谱抽取器），"
            "逐个文档跑 LLM，把“X-2000 兼容配件 B”这样的句子抽成 <code>(X-2000, 兼容, 配件 B)</code> 的边。其中 "
            "<strong>SchemaLLMPathExtractor</strong> 是最常用的一种：你<strong>预先声明</strong>允许的实体类型（产品 / "
            "配件 / 厂商）和关系类型（兼容 / 替代 / 属于），抽取被<strong>约束在 schema 内</strong>——LLM 不会乱造"
            "关系，图更干净、更可控。代价是抽取要花 LLM 调用，<strong>建库比纯向量贵且慢</strong>，但这是一次性成本，"
            "换来的是可多跳的结构。",
            "The heart of building a graph is <strong>extraction</strong>: turning facts in natural language into "
            "structured <strong>entity—relation—entity</strong> triples. <code>PropertyGraphIndex.from_documents(...)"
            "</code> takes a list of <code>kg_extractors</code> (knowledge-graph extractors) and runs an LLM over each "
            "document, turning a sentence like “X-2000 is compatible with part B” into a <code>(X-2000, compatible-with, "
            "part B)</code> edge. The most common one is <strong>SchemaLLMPathExtractor</strong>: you <strong>declare in "
            "advance</strong> the allowed entity types (product / part / vendor) and relation types (compatible / "
            "replaces / belongs-to), and extraction is <strong>constrained to that schema</strong> — the LLM won't "
            "invent stray relations, so the graph is cleaner and more controllable. The cost is the extraction LLM "
            "calls, making <strong>indexing pricier and slower than plain vectors</strong>, but it's a one-time cost "
            "that buys a multi-hop structure.",
        ),
    )
    + c.code(
        'from llama_index.core import PropertyGraphIndex\n'
        'from llama_index.core.indices.property_graph import SchemaLLMPathExtractor\n\n'
        'index = PropertyGraphIndex.from_documents(\n'
        '    documents,\n'
        '    kg_extractors=[SchemaLLMPathExtractor(llm=llm)],   # 可传 possible_entities / possible_relations 声明 schema\n'
        ')\n'
        'qe = index.as_query_engine(include_text=True)\n'
        'print(qe.query("X-2000 和它的替代型号有什么兼容差异？"))',
        caption=L("用 PropertyGraphIndex 抽三元组建图，再 include_text 查询：既给关系骨架又附原文证据",
                  "Build a triple graph with PropertyGraphIndex, then query with include_text: relation skeleton plus source evidence"),
    )
    + c.source_ref(
        "indices/property_graph/base.py", "PropertyGraphIndex",
        L("从文档抽取实体/关系建成属性图，可多跳检索。",
          "builds a property graph of entities/relations from docs for multi-hop retrieval."),
    )
    + c.section(
        L("怎么查：同义词扩展找种子 + 向量上下文，再顺边多跳",
          "How to query: synonym seeds + vector context, then multi-hop"),
        L(
            "查询分两步：<strong>先找种子节点，再顺边遍历</strong>。<code>as_query_engine()</code> 默认挂两路<strong>"
            "子检索器</strong>：<strong>LLMSynonymRetriever</strong>（同义词扩展）把问题里的词扩成若干近义说法，去"
            "<strong>匹配图里的实体名</strong>，解决“用户叫‘旧款’、图里存的是‘X-1000’”这种对不上；<strong>"
            "VectorContextRetriever</strong>（向量上下文）则用 embedding 给问题找<strong>语义最近的种子节点</strong>，"
            "并捎回节点周边的原文。拿到种子实体后，检索器<strong>顺着边多跳</strong>，把连起来的三元组收集成上下文。"
            "<code>include_text=True</code> 还会把每个命中节点对应的<strong>原始段落</strong>一并带上——这样 LLM 既看到"
            "<strong>关系骨架</strong>（谁连着谁），又有<strong>原文证据</strong>，答案能溯源、不靠编。",
            "Querying is two steps: <strong>find seed nodes, then traverse edges</strong>. <code>as_query_engine()</code> "
            "attaches two default <strong>sub-retrievers</strong>: <strong>LLMSynonymRetriever</strong> (synonym "
            "expansion) expands the question's words into several near-synonyms to <strong>match entity names in the "
            "graph</strong>, fixing the “user says ‘the old model’ but the graph stores ‘X-1000’” mismatch; <strong>"
            "VectorContextRetriever</strong> (vector context) uses embeddings to find the <strong>semantically nearest "
            "seed nodes</strong> and brings back the text around them. With seed entities in hand, the retriever "
            "<strong>walks the edges hop by hop</strong>, gathering the connected triples into context. <code>"
            "include_text=True</code> also attaches each hit node's <strong>original passage</strong> — so the LLM sees "
            "both the <strong>relation skeleton</strong> (who connects to whom) and the <strong>source evidence</strong>, "
            "keeping answers traceable rather than made up.",
        ),
    )
    + d.flow(
        [
            ("q", L("问题", "Question"), L("“X-2000 与替代型号的兼容差异？”", "“compat diff vs its replacement?”")),
            ("seed", L("定位种子实体", "Locate seed entities"),
             L("同义词扩展 + 向量找到 X-2000 节点", "synonym + vector find the X-2000 node")),
            ("walk", L("顺边多跳", "Walk edges (multi-hop)"),
             L("替代 → X-1000，X-1000 兼容 → 配件 B", "replaces → X-1000, X-1000 compatible → part B")),
            ("text", L("带回原文", "Attach source text"),
             L("include_text 附上证据段落", "include_text adds the evidence passages")),
            ("ans", L("综合作答", "Synthesize answer"),
             L("关系骨架 + 原文一起喂给 LLM", "feed relation skeleton + text to the LLM")),
        ],
        active="walk",
        caption=L(
            "图谱查询四步：找种子 → 顺边多跳 → 带回原文 → 综合；“顺边多跳”这一步正是向量做不到的",
            "Graph query in four steps: seed → multi-hop walk → attach text → synthesize; the “multi-hop walk” is exactly what vectors can't do",
        ),
    )
    + c.source_ref(
        "indices/property_graph/sub_retrievers/", "LLMSynonymRetriever · VectorContextRetriever",
        L("默认两路子检索器：同义词扩展找种子节点 + 向量上下文召回相邻文本，再顺边多跳。",
          "the two default sub-retrievers: synonym expansion seeds nodes + vector context pulls neighboring text, then traversal hops along edges."),
    )
    + c.section(
        L("何时用图、何时用向量", "When a graph, when vectors"),
        L(
            "不是所有 RAG 都该上图谱，判断只看一件事：<strong>问题靠不靠“关系”</strong>。当知识本身是一张<strong>"
            "关系网</strong>（产品-配件-兼容、人物-公司-职位、论文-引用），问题又要<strong>多跳推理</strong>（A 的 B "
            "的 C），图谱的“顺边遍历”几乎是唯一能答全的方式。反过来，如果问题只是<strong>找一段语义相近的话</strong>"
            "（“退款政策怎么写的”），或关系<strong>稀疏、一跳就够</strong>，那纯向量更<strong>便宜、更快、够用</strong>，"
            "花 LLM 抽一整张图并不划算。实务里两者常<strong>互补</strong>：向量管“找到相关段落”，图谱管“把相关事实连"
            "起来”，按问题类型路由（回想 L18 的 Router）。",
            "Not every RAG needs a graph; the test is one thing: <strong>does the question hinge on “relations”</strong>. "
            "When the knowledge is itself a <strong>web of relations</strong> (product-part-compatibility, "
            "person-company-role, paper-citation) and the question needs <strong>multi-hop reasoning</strong> (A's B's "
            "C), a graph's edge traversal is almost the only way to answer it fully. Conversely, if the question just "
            "<strong>finds a semantically close passage</strong> (“what does the refund policy say”) or relations are "
            "<strong>sparse and one hop suffices</strong>, plain vectors are <strong>cheaper, faster, and enough"
            "</strong> — paying an LLM to extract a whole graph isn't worth it. In practice the two often <strong>"
            "complement</strong>: vectors “find the relevant passage”, a graph “connects the relevant facts”, routed by "
            "question type (recall L18's Router).",
        ),
        c.compare_table(
            [L("对比项", "Aspect"), L("图谱 RAG", "Graph RAG"), L("向量 RAG", "Vector RAG")],
            [
                [L("召回的是", "Recalls"), L("连起来的事实（实体-关系-实体）", "connected facts (entity-relation-entity)"),
                 L("相似的片段（top-k 近邻）", "similar chunks (top-k neighbors)")],
                [L("最擅长", "Best at"), L("多跳 / 关系密集问答", "multi-hop / relation-dense Q&amp;A"),
                 L("语义相似 / 换种问法", "semantic similarity / rephrasings")],
                [L("构建成本", "Build cost"), L("高：LLM 逐文档抽三元组", "high: LLM extracts triples per doc"),
                 L("低：切块 + embedding", "low: chunk + embedding")],
                [L("盲区", "Blind spot"), L("关系稀疏时性价比低", "poor ROI when relations are sparse"),
                 L("跨片段的关系会丢", "loses cross-chunk relations")],
            ],
        ),
    )
    + c.analogy(L(
        "纯向量检索像在一摞书里<strong>翻找长得像的书页</strong>：哪一页和你手里的纸<strong>看起来最像</strong>就抽"
        "出来——换种说法也能找到，但它<strong>不知道页与页之间的关系</strong>。图谱像<strong>顺着引用链一页页翻"
        "下去</strong>：从这一页的脚注找到它<strong>引用</strong>的那一页，再顺着那一页的引用接着翻，把<strong>"
        "一条线索串起来的内容</strong>都找齐——这正是多跳问题需要的。",
        "Pure vector search is like <strong>thumbing through a stack for the page that looks alike</strong>: pull out "
        "whichever page <strong>looks most like</strong> the sheet in your hand — rephrasings still match, but it "
        "<strong>knows nothing about how pages relate</strong>. A graph is like <strong>following a citation chain "
        "page by page</strong>: from this page's footnote you reach the page it <strong>cites</strong>, then follow "
        "that page's citations onward, collecting everything <strong>strung along one thread</strong> — exactly what a "
        "multi-hop question needs.",
    ))
    + c.key_points([
        L("向量召回“相似片段”，图谱召回“连起来的事实”；<strong>多跳关系（A→B→C）</strong>纯向量答不出。",
          "Vectors recall “similar chunks”, a graph recalls “connected facts”; <strong>multi-hop relations (A→B→C)"
          "</strong> are beyond pure vectors."),
        L("用 <code>PropertyGraphIndex.from_documents(kg_extractors=[...])</code> 建图；<strong>SchemaLLMPathExtractor"
          "</strong> 用 schema 约束 LLM 抽出的实体/关系，图更干净。",
          "Build with <code>PropertyGraphIndex.from_documents(kg_extractors=[...])</code>; <strong>"
          "SchemaLLMPathExtractor</strong> constrains the LLM's entities/relations to a schema for a cleaner graph."),
        L("查询默认两路子检索器：<strong>LLMSynonymRetriever</strong>（同义词扩展找种子）+ <strong>"
          "VectorContextRetriever</strong>（向量上下文），再<strong>顺边多跳</strong>；<code>include_text=True</code> "
          "带回原文。",
          "Querying uses two default sub-retrievers: <strong>LLMSynonymRetriever</strong> (synonym seeds) + <strong>"
          "VectorContextRetriever</strong> (vector context), then <strong>multi-hop traversal</strong>; <code>"
          "include_text=True</code> brings back source text."),
        L("关系密集 / 多跳问答用<strong>图谱</strong>，普通相似检索用<strong>向量</strong>；图的代价是<strong>抽取贵、"
          "构建慢</strong>。",
          "Relation-dense / multi-hop Q&amp;A → <strong>graph</strong>, ordinary similarity → <strong>vectors</strong>; "
          "a graph's cost is <strong>pricey extraction, slow build</strong>."),
    ])
    + c.design_highlight(L(
        "图谱 RAG 的精髓，是把检索的问题从“<strong>哪段话最像</strong>”换成“<strong>哪些事实连得上</strong>”。"
        "向量把文档压成一堆<strong>互不相连的点</strong>，只能按距离取近邻；图谱先用 LLM 把文档<strong>还原成实体"
        "与关系的网</strong>，于是“A 的供应商的总部在哪国”这种<strong>跨多跳</strong>的问题，能顺着边一步步走到"
        "答案——这是纯相似度<strong>结构上做不到</strong>的。代价也很实在：<strong>抽取要烧 LLM、建库更慢</strong>，"
        "图的质量取决于抽取的质量。所以工程判断不是“图谱更高级所以要上”，而是“<strong>我的问题到底靠不靠多跳"
        "关系</strong>”：靠，就为那张图付抽取的钱；不靠，向量又快又省，别为用不上的关系买单。",
        "The essence of Graph RAG is turning retrieval's question from “<strong>which passage looks most alike</strong>” "
        "into “<strong>which facts can be connected</strong>”. Vectors squash documents into a cloud of <strong>"
        "unconnected points</strong> and can only take nearest neighbors by distance; a graph first has an LLM "
        "<strong>reconstruct documents into a web of entities and relations</strong>, so a <strong>multi-hop</strong> "
        "question like “which country is the HQ of A's supplier in” can be walked edge by edge to the answer — "
        "something pure similarity <strong>structurally cannot do</strong>. The cost is real: <strong>extraction burns "
        "LLM calls and indexing is slower</strong>, and graph quality rides on extraction quality. So the engineering "
        "call isn't “a graph is fancier, so use it” but “<strong>does my question actually hinge on multi-hop "
        "relations</strong>”: if it does, pay the extraction price for that graph; if it doesn't, vectors are fast and "
        "cheap — don't pay for relations you'll never traverse.",
    ))
)
LESSON_28 = _skeleton("retrieve", "结构化数据查询（SQL &amp; Pandas）", "querying structured data (SQL &amp; Pandas)")
LESSON_29 = _skeleton("embed", "多模态 RAG", "multimodal RAG")
LESSON_30 = _skeleton("retrieve", "查询分解（Sub-Question）", "query decomposition (Sub-Question)")
LESSON_31 = _skeleton("synthesize", "结构化输出", "structured outputs")
