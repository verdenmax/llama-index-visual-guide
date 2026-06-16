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
LESSON_28 = (
    c.pipeline("retrieve")
    + c.lead(L(
        "到这里，检索一直在做同一件事——“<strong>找相似</strong>”：把问题和文档变成向量、取回最像的片段。可一旦"
        "问题是“<strong>上个月各区域的总销售额、降序排列</strong>”这种要<strong>精确算数字</strong>的，向量就无能为力："
        "答案不在某一段话里现成写着，而要把成千上万行<strong>逐笔加总、按区域分组、再排序</strong>。这一课换一种思路："
        "<strong>别让向量算账，把结构化数据交给天生会精确计算的工具</strong>——用 <strong>text-to-SQL</strong> 让数据库算、"
        "用 <strong>PandasQueryEngine</strong> 让内存表算；同时盯紧一个绕不开的代价：<strong>这些引擎在执行 LLM 生成的"
        "代码</strong>。",
        "Up to here retrieval kept doing one thing — “<strong>find similar</strong>”: turn the question and docs into "
        "vectors and fetch the most alike chunks. But the moment the question is something like “<strong>total sales "
        "per region last month, sorted descending</strong>” that needs an <strong>exact number</strong>, vectors are "
        "helpless: the answer isn't sitting ready in any passage — it requires <strong>summing row by row, grouping by "
        "region and then sorting</strong> thousands of rows. This lesson flips the approach: <strong>don't make vectors "
        "do the accounting; hand structured data to tools born to compute exactly</strong> — use <strong>text-to-SQL"
        "</strong> so the database computes, and <strong>PandasQueryEngine</strong> so an in-memory table computes — "
        "all while watching one unavoidable cost: <strong>these engines execute LLM-generated code</strong>.",
    ))
    + c.section(
        L("痛点：数字、聚合、精确筛选，塞进向量必然不准",
          "The pain: numbers, aggregation, exact filtering — forced into vectors, bound to be wrong"),
        L(
            "向量检索的本事是“<strong>找像的</strong>”：把每段文字编码成语义向量，召回和问题<strong>最相似</strong>的 "
            "top-k 片段。这对“讲了什么”的非结构化文字很灵，碰到“<strong>算出确切数字</strong>”却立刻露馅。问“上个月每个"
            "区域的总销售额、降序排列”，答案不是哪段话里写好的句子，而要把<strong>成千上万行</strong>订单加总、分组、"
            "排序——向量<strong>既不会做加法</strong>，也保证不了“<strong>全</strong>”：top-k 只取几片，漏一行结果就错。"
            "把订单表、财务报表、监控指标这种<strong>结构化数据</strong>硬编码成 embedding，等于让一个擅长“<strong>模糊"
            "联想</strong>”的系统去做“<strong>精确算账</strong>”，结果必然是“看起来差不多、其实算错”。这类问题的正解只有"
            "一个方向：<strong>别让向量算，把精确计算交给本来就为它而生的工具</strong>——数据库与 DataFrame。",
            "Vector search is good at “<strong>finding the alike</strong>”: encode each passage into a semantic vector "
            "and recall the top-k chunks <strong>most similar</strong> to the question. That shines on unstructured text "
            "about “what was said”, but it falls apart the instant you need an <strong>exact number</strong>. Ask “total "
            "sales per region last month, sorted descending” and the answer isn't a ready-made sentence in some passage "
            "— it requires totalling, grouping and sorting <strong>thousands of rows</strong> of orders. Vectors "
            "<strong>can't do arithmetic</strong> and can't guarantee <strong>completeness</strong>: top-k takes a few "
            "chunks, and miss one row and the result is wrong. Hard-coding an orders table, a financial report or a "
            "monitoring metric into embeddings asks a system built for “<strong>fuzzy association</strong>” to do "
            "“<strong>exact accounting</strong>” — the result is bound to “look about right but compute wrong”. There's "
            "only one right direction: <strong>don't make vectors compute; hand exact calculation to the tools born for "
            "it</strong> — databases and DataFrames.",
        ),
    )
    + d.compare2(
        (L("向量检索", "Vector"),
         i18n.render(L("问“各区域总销售额”，只捞回几段<strong>看起来相关</strong>的文字，数字还得你自己凑——<strong>漏行、算错</strong>",
                       "ask “total sales per region” and it just pulls a few <strong>seems-related</strong> snippets; you still patch the numbers yourself — <strong>missed rows, wrong totals</strong>"))),
        (L("text-to-SQL", "text-to-SQL"),
         i18n.render(L("LLM 写 <code>GROUP BY · SUM · ORDER BY</code>，数据库<strong>逐行精确算</strong>，结果<strong>又全又准</strong>",
                       "the LLM writes <code>GROUP BY · SUM · ORDER BY</code>; the database computes <strong>exactly, row by row</strong> — <strong>complete and correct</strong>"))),
        caption=L("同一个数字问题：向量只会“找相似”，text-to-SQL 才能“精确算”",
                  "Same numeric question: vectors only “find similar”, text-to-SQL actually “computes exactly”"),
    )
    + c.section(
        L("text-to-SQL：LLM 写 SQL，数据库做精确计算",
          "text-to-SQL: the LLM writes SQL, the database does the exact compute"),
        L(
            "数据库天生就会“精确算账”：<code>GROUP BY</code> 分组、<code>SUM</code> 求和、<code>ORDER BY</code> 排序，"
            "几十年的引擎优化保证又快又准。text-to-SQL 的思路就是<strong>分工</strong>：把<strong>表结构（schema）</strong>"
            "喂给 LLM，让它据此<strong>写出 SQL</strong>，交数据库<strong>执行</strong>，再把结果用自然语言讲回来——LLM 只"
            "做“<strong>把人话翻成 SQL</strong>”这件它擅长的事，真正的计算落在数据库上。<code>SQLDatabase</code> 包住"
            "数据库连接（<code>include_tables</code> 限定可见表），<code>NLSQLTableQueryEngine</code> 把“自然语言 → SQL → "
            "执行 → 答案”串成一个查询引擎。",
            "A database is born to do “exact accounting”: <code>GROUP BY</code> to group, <code>SUM</code> to total, "
            "<code>ORDER BY</code> to sort — decades of engine optimization make it fast and correct. text-to-SQL is "
            "just a <strong>division of labor</strong>: feed the <strong>schema</strong> to the LLM, have it <strong>"
            "write SQL</strong> from that, hand it to the database to <strong>execute</strong>, then phrase the result "
            "back in natural language — the LLM only does the one thing it's good at, “<strong>translate human words "
            "into SQL</strong>”, while the real computation lands on the database. <code>SQLDatabase</code> wraps the "
            "connection (<code>include_tables</code> limits the visible tables) and <code>NLSQLTableQueryEngine</code> "
            "chains “NL → SQL → execute → answer” into one query engine.",
        ),
        L(
            "可 schema 一大就有新麻烦：库里有<strong>几百张表</strong>时，把所有表结构塞进提示词既<strong>超长又贵</strong>，"
            "还会让 LLM 在无关表里挑花眼、写错 SQL。解法是<strong>先选表、再写 SQL</strong>：把每张表的描述做成对象、建一个 "
            "<code>ObjectIndex</code>，查询时先<strong>检索出与问题最相关的少数几张表</strong>，只把这几张的 schema 交给 "
            "LLM。承担这一步的是 <code>SQLTableRetrieverQueryEngine</code>——它比 <code>NLSQLTableQueryEngine</code> 多了"
            "“<strong>先按问题召回相关表</strong>”的检索器，正是为大库设计：提示词短了，选错表、串错列的概率自然降下来。",
            "But a big schema brings a new problem: with <strong>hundreds of tables</strong>, stuffing every schema into "
            "the prompt is <strong>huge and expensive</strong> and tempts the LLM to pick the wrong table and write "
            "wrong SQL. The fix is <strong>select tables first, then write SQL</strong>: turn each table's description "
            "into an object and build an <code>ObjectIndex</code>; at query time first <strong>retrieve the few tables "
            "most relevant to the question</strong> and give only those schemas to the LLM. That job falls to <code>"
            "SQLTableRetrieverQueryEngine</code> — it adds a “<strong>retrieve relevant tables by the question first"
            "</strong>” retriever on top of <code>NLSQLTableQueryEngine</code>, designed exactly for large databases: a "
            "shorter prompt naturally lowers the odds of the wrong table or a crossed-up column.",
        ),
    )
    + c.code(
        'from llama_index.core import SQLDatabase\n'
        'from llama_index.core.query_engine import NLSQLTableQueryEngine\n\n'
        'sql_db = SQLDatabase(engine, include_tables=["orders"])\n'
        'qe = NLSQLTableQueryEngine(sql_database=sql_db, tables=["orders"])\n'
        'print(qe.query("上个月每个区域的总销售额是多少，降序排列？"))',
        caption=L("自然语言进、SQL 出、数据库算：include_tables 限定可见表，把精确计算交给数据库",
                  "NL in, SQL out, DB computes: include_tables limits the visible tables, hand the exact math to the database"),
    )
    + c.source_ref(
        "indices/struct_store/sql_query.py", "NLSQLTableQueryEngine",
        L("把自然语言转成 SQL 在数据库上执行。", "turns NL into SQL executed on the database."),
    )
    + d.flow([
        ("q", L("自然语言问题", "NL question")),
        ("sql", L("LLM 写 SQL", "LLM writes SQL"), L("据表结构", "from schema")),
        ("run", L("数据库执行", "DB executes"), L("精确计算", "exact compute")),
        ("ans", L("自然语言答案", "NL answer")),
    ], active="run", caption=L("text-to-SQL：把精确计算交给数据库，LLM 只负责翻译",
                               "text-to-SQL: hand exact compute to the DB; the LLM only translates"))
    + c.section(
        L("内存表：交给 PandasQueryEngine",
          "In-memory tables: hand them to PandasQueryEngine"),
        L(
            "不是所有结构化数据都躺在数据库里。很多时候你手上就是一个 <code>pandas.DataFrame</code>——一份刚读进来的 "
            "CSV、一段 API 返回、一张算好的中间表。为这点数据起一个数据库太重，<code>PandasQueryEngine</code> 直接让 "
            "LLM 对 DataFrame 干活：把<strong>列名和样例</strong>给 LLM，让它写一小段 <strong>pandas 代码</strong>（如 "
            "<code>df.groupby(...).sum()</code>），<strong>执行</strong>后把结果讲回来。“销量最高的 3 个产品”这种小分析，"
            "几行就出；<code>verbose=True</code> 还会打印它生成的代码，方便你核对它到底算了什么。它和 text-to-SQL 是<strong>"
            "同一套思路</strong>（LLM 写代码、引擎执行），只是把“数据库 + SQL”换成了“<strong>内存表 + pandas</strong>”。",
            "Not all structured data lives in a database. Often you just hold a <code>pandas.DataFrame</code> — a freshly "
            "read CSV, an API response, a computed intermediate table. Spinning up a database for that is overkill; "
            "<code>PandasQueryEngine</code> lets the LLM work the DataFrame directly: give it the <strong>column names "
            "and a sample</strong>, have it write a small snippet of <strong>pandas code</strong> (e.g. <code>"
            "df.groupby(...).sum()</code>), <strong>execute</strong> it, and phrase the result back. A small analysis "
            "like “the top-3 products by sales” comes out in a few lines; <code>verbose=True</code> also prints the "
            "generated code so you can check what it actually computed. It's the <strong>same idea</strong> as "
            "text-to-SQL (the LLM writes code, an engine runs it), just swapping “database + SQL” for “<strong>"
            "in-memory table + pandas</strong>”.",
        ),
    )
    + c.code(
        '# pip install llama-index-experimental  —— core 0.14.22 仅留会抛弃用警告的占位实现\n'
        'from llama_index.experimental.query_engine import PandasQueryEngine\n\n'
        'qe = PandasQueryEngine(df=df, verbose=True)   # ⚠️ 会 eval LLM 生成的 Python，仅用于可信环境\n'
        'print(qe.query("销量最高的 3 个产品是哪些？"))',
        caption=L("内存 DataFrame 直接问：LLM 写 pandas、引擎执行；verbose 打印生成的代码便于核对",
                  "Ask an in-memory DataFrame directly: the LLM writes pandas, the engine runs it; verbose prints the generated code to check"),
    )
    + d.grid(
        [L("数据形态", "Data shape"), L("最该用", "Best tool"), L("为什么", "Why")],
        [
            [L("非结构化文档", "unstructured docs"), L("向量检索", "vector"), L("语义相似", "semantic similarity")],
            [L("数据库表（大）", "DB tables (large)"), L("text-to-SQL", "text-to-SQL"), L("精确聚合/筛选", "exact aggregation")],
            [L("内存 DataFrame", "in-memory DataFrame"), L("PandasQueryEngine", "PandasQueryEngine"), L("快速表分析", "quick table analysis")],
        ],
        caption=L("按数据形态选工具——数字别硬塞向量", "pick by data shape — don't force numbers into vectors"),
    )
    + c.section(
        L("安全：它们在执行 LLM 生成的代码",
          "Safety: they execute LLM-generated code"),
        L(
            "这两个引擎好用，但有一个<strong>必须正视</strong>的共同前提：它们都在<strong>执行 LLM 生成的代码</strong>。"
            "<code>PandasQueryEngine</code> 会 <code>eval</code> 一段 LLM 写的 Python，<code>NLSQLTableQueryEngine</code> "
            "会把 LLM 写的 SQL <strong>真的跑在你的数据库上</strong>。一旦输入不可信，<strong>提示注入</strong>就能诱导模型"
            "写出 <code>DROP TABLE</code>、<code>DELETE</code>、越权去读别的表，甚至（Pandas 这边）执行任意 Python——这"
            "不是“答错了”，是“<strong>被人借你的手执行命令</strong>”。",
            "These two engines are handy, but they share one premise you <strong>must face</strong>: both <strong>"
            "execute LLM-generated code</strong>. <code>PandasQueryEngine</code> <code>eval</code>s a snippet of "
            "LLM-written Python, and <code>NLSQLTableQueryEngine</code> <strong>actually runs the LLM's SQL on your "
            "database</strong>. The moment input is untrusted, <strong>prompt injection</strong> can coax the model "
            "into <code>DROP TABLE</code>, <code>DELETE</code>, reading other tables it shouldn't, or (on the Pandas "
            "side) running arbitrary Python — that's not “a wrong answer”, it's “<strong>someone executing commands "
            "through your hands</strong>”.",
        ),
        L(
            "所以上线前的第一要务不是跑通，而是<strong>关进笼子</strong>：① 数据库一律用<strong>只读、最小权限</strong>的"
            "账号，能 SELECT 不能写、只看该看的表/视图；② Pandas 这类引擎<strong>放进沙箱/隔离进程/容器</strong>，限制可用"
            "模块与文件系统；③ <strong>只对可信输入开放</strong>，别把这种引擎直接怼到匿名用户面前。事实上，<code>"
            "llama-index-core 0.14.22</code> 已经把 <code>PandasQueryEngine</code> 做成<strong>会抛弃用警告的占位实现"
            "</strong>，把真正能跑的版本挪到了 <code>llama-index-experimental</code>（<code>from "
            "llama_index.experimental.query_engine import PandasQueryEngine</code>），并白纸黑字写明“<strong>会任意执行"
            "代码、请在安全环境使用</strong>”——库本身就用这种“默认不让用”的姿态提醒你：方便和危险是绑在一起的。",
            "So the first priority before shipping isn't getting it to run — it's <strong>caging it</strong>: (1) give "
            "the database a <strong>read-only, least-privilege</strong> account — SELECT but no writes, only the "
            "tables/views it should see; (2) put Pandas-style engines in a <strong>sandbox / isolated process / "
            "container</strong>, restricting modules and filesystem; (3) <strong>expose it only to trusted input"
            "</strong>, never wire such an engine straight to anonymous users. In fact, <code>llama-index-core "
            "0.14.22</code> already ships <code>PandasQueryEngine</code> as a <strong>shim that raises a deprecation "
            "warning</strong>, moving the runnable version to <code>llama-index-experimental</code> (<code>from "
            "llama_index.experimental.query_engine import PandasQueryEngine</code>) and stating in black and white that "
            "it “<strong>allows arbitrary code execution; use in a secure environment</strong>” — the library itself "
            "uses this “off by default” stance to remind you that convenience and danger come bound together.",
        ),
    )
    + c.analogy(L(
        "向量检索像凭“<strong>模糊回忆</strong>”找最像的一段话：问“上个月华东区卖了多少”，它只会捞回几段“看起来相关”"
        "的文字，真要把数字加起来还得靠你自己、还容易漏。text-to-SQL 像“<strong>拿计算器精确算</strong>”：让数据库去 "
        "<code>GROUP BY · SUM · ORDER BY</code>，算出来的数字<strong>又全又准</strong>。要数字，就别问“模糊回忆”，去按"
        "“计算器”。",
        "Vector search is like fishing by “<strong>fuzzy memory</strong>” for the passage that looks most alike: ask "
        "“how much did the East region sell last month” and it pulls back a few “seems-related” snippets, leaving the "
        "actual arithmetic to you — and easy to miss rows. text-to-SQL is like “<strong>reaching for a calculator"
        "</strong>”: let the database <code>GROUP BY · SUM · ORDER BY</code>, and the number comes back <strong>"
        "complete and correct</strong>. When you need a number, don't ask “fuzzy memory” — press the “calculator”.",
    ))
    + c.key_points([
        L("数字 / 聚合 / 精确筛选<strong>别塞向量</strong>——向量只会“找相似”，算不准 <code>SUM/COUNT/排序</code>；"
          "结构化数据交给能<strong>精确计算</strong>的引擎。",
          "<strong>Don't force numbers / aggregation / exact filtering into vectors</strong> — vectors only “find "
          "similar” and can't compute <code>SUM/COUNT/sort</code>; hand structured data to engines that <strong>compute "
          "exactly</strong>."),
        L("<strong>text-to-SQL</strong>：让 LLM 据表结构写 SQL、数据库执行（<code>NLSQLTableQueryEngine</code>）；表多时"
          "先用 <code>ObjectIndex</code> + <code>SQLTableRetrieverQueryEngine</code> <strong>选相关表</strong>再生成 SQL。",
          "<strong>text-to-SQL</strong>: the LLM writes SQL from the schema and the database executes it (<code>"
          "NLSQLTableQueryEngine</code>); with many tables, first <strong>select relevant tables</strong> via <code>"
          "ObjectIndex</code> + <code>SQLTableRetrieverQueryEngine</code>, then generate SQL."),
        L("内存 <code>DataFrame</code> 用 <strong>PandasQueryEngine</strong> 做快速表分析（LLM 写 pandas、引擎执行）。",
          "For an in-memory <code>DataFrame</code>, use <strong>PandasQueryEngine</strong> for quick table analysis (the "
          "LLM writes pandas, the engine runs it)."),
        L("⚠️ <strong>安全</strong>：Pandas/SQL 引擎都在<strong>执行 LLM 生成的代码</strong>——必须<strong>沙箱 / 只读账号 "
          "/ 最小权限 / 限可信输入</strong>；core 0.14.22 已把 <code>PandasQueryEngine</code> 移到 <code>"
          "llama-index-experimental</code> 并要求“安全环境”。",
          "⚠️ <strong>Safety</strong>: Pandas/SQL engines both <strong>execute LLM-generated code</strong> — you must "
          "<strong>sandbox / use a read-only account / least privilege / restrict to trusted input</strong>; core "
          "0.14.22 has moved <code>PandasQueryEngine</code> to <code>llama-index-experimental</code> and requires a "
          "“secure environment”."),
    ])
    + c.design_highlight(L(
        "结构化数据查询的精髓，是把“<strong>该谁来算</strong>”想清楚：向量擅长“<strong>找相似</strong>”，却天生不会"
        "“<strong>精确算数字</strong>”——<code>SUM</code>、<code>COUNT</code>、<code>GROUP BY</code>、环比这些，硬塞进 "
        "embedding 只会得到“看起来差不多”的错答。正确做法是<strong>按数据形态选工具</strong>：非结构化文档走向量，"
        "数据库表走 text-to-SQL，内存表走 Pandas，让<strong>数据库 / 解释器去做它最擅长的精确计算</strong>，LLM 只负责"
        "“把人话翻成查询”。代价也很实在：这些引擎都在<strong>执行 LLM 生成的代码</strong>，把“翻译”的便利和“任意执行”的"
        "风险绑在了一起——所以工程上第一件事不是跑通，而是<strong>关进沙箱、换只读账号、收最小权限</strong>。一句话："
        "<strong>数字别硬塞向量，但给数据库写 SQL 的权力也要锁死</strong>。",
        "The essence of structured-data querying is getting “<strong>who should do the math</strong>” right: vectors are "
        "great at “<strong>finding similar</strong>” but inherently can't “<strong>compute exact numbers</strong>” — "
        "<code>SUM</code>, <code>COUNT</code>, <code>GROUP BY</code>, quarter-over-quarter forced into an embedding only "
        "yield a “close-looking” wrong answer. The fix is to <strong>pick the tool by data shape</strong>: unstructured "
        "docs → vectors, database tables → text-to-SQL, in-memory tables → Pandas, letting the <strong>database / "
        "interpreter do the exact compute it's best at</strong> while the LLM only “translates human questions into a "
        "query”. The cost is real too: these engines all <strong>execute LLM-generated code</strong>, binding the "
        "convenience of “translation” to the risk of “arbitrary execution” — so the first engineering move isn't getting "
        "it to run, it's <strong>caging it: sandbox, swap in a read-only account, cut to least privilege</strong>. In a "
        "line: <strong>don't force numbers into vectors, but lock down the power to write SQL against your database too"
        "</strong>.",
    ))
)
LESSON_29 = (
    c.pipeline("embed")
    + c.lead(L(
        "前面所有检索都是“<strong>文字找文字</strong>”：把问题和文本块塞进同一个向量空间，取回最相似的片段。可现实里"
        "大量知识<strong>长在图里</strong>——架构图、仪表盘截图、产品照、扫描的电路图。只把它们 OCR / 配文字成纯文本，"
        "<strong>视觉细节就丢了</strong>（“这张图里设备有几个接口”光靠文字答不出）。<strong>多模态 RAG</strong> 换一种"
        "存法：用<strong>多模态 embedding</strong> 把图和文映进<strong>同一个向量空间</strong>，于是能“<strong>用文字"
        "查图、用图查图</strong>”；检索时图和文一起召回，再交给一个<strong>看得见图的多模态 LLM</strong> 看着图作答。"
        "一句话：先让图文“<strong>坐标统一</strong>”，再让<strong>会看图的模型</strong>来回答。",
        "Every retrieval so far has been “<strong>text finds text</strong>”: push the question and text chunks into one "
        "vector space and fetch the most similar. But in the real world a lot of knowledge <strong>lives in images"
        "</strong> — architecture diagrams, dashboard screenshots, product photos, scanned schematics. OCR-ing or "
        "captioning them into plain text <strong>throws away the visual detail</strong> (“how many ports does the device "
        "in this picture have” can't be answered from text alone). <strong>Multimodal RAG</strong> stores things "
        "differently: a <strong>multimodal embedding</strong> maps images and text into the <strong>same vector space"
        "</strong>, so you can “<strong>query images with text, or query images with images</strong>”; retrieval recalls "
        "images and text together, then hands them to a <strong>vision-capable multimodal LLM</strong> that answers by "
        "actually looking at the picture. In a line: <strong>unify the coordinates</strong> of image and text first, "
        "then let a <strong>model that can see</strong> answer.",
    ))
    + c.section(
        L("图文进同一向量空间：于是能“用文字查图、用图查图”",
          "Image and text in one vector space: now you can “query images with text, or with images”"),
        L(
            "纯文本 RAG 能成立，靠的是一个前提：问题和文档块被<strong>同一个 embedding 模型</strong>映进<strong>同一个"
            "向量空间</strong>，所以“算两段文字的余弦相似度、取最近邻”才有意义。多模态的关键，是把这个前提<strong>扩展"
            "到图像</strong>：用<strong>图文对</strong>训练出来的<strong>多模态 embedding</strong>（最有名的是 CLIP），会"
            "让“一张猫的照片”和“cat 这个词”落在<strong>彼此邻近的坐标</strong>上——图和文<strong>共用一套坐标系</strong>。"
            "一旦共用，<strong>跨模态的最近邻就有了意义</strong>：拿“文字问题”的向量，去和<strong>图像向量</strong>比距离，"
            "就能召回“画的就是这件事”的图片——这正是“<strong>用文字查图</strong>”的全部底气。反过来，如果图、文各在"
            "<strong>两个互不相干的空间</strong>，跨空间比距离<strong>毫无意义</strong>，就像拿经纬度去和体温比大小。所以"
            "“同一向量空间”不是一句口号，而是跨模态检索<strong>能不能成立的根</strong>。",
            "Text-only RAG works because of one premise: the question and the doc chunks are mapped by the <strong>same "
            "embedding model</strong> into the <strong>same vector space</strong>, so “cosine similarity between two "
            "pieces of text, take the nearest” actually means something. The crux of going multimodal is <strong>"
            "extending that premise to images</strong>: a <strong>multimodal embedding</strong> trained on <strong>"
            "image–text pairs</strong> (the famous one is CLIP) makes “a photo of a cat” and “the word cat” land at "
            "<strong>neighboring coordinates</strong> — image and text <strong>share one coordinate system</strong>. "
            "Once shared, <strong>cross-modal nearest-neighbor becomes meaningful</strong>: take the vector of a "
            "<strong>text question</strong>, measure its distance to <strong>image vectors</strong>, and you recall the "
            "picture that “depicts exactly this” — which is the entire basis of “<strong>querying images with text"
            "</strong>”. Conversely, if image and text sat in <strong>two unrelated spaces</strong>, measuring distance "
            "across them would be <strong>meaningless</strong>, like comparing latitude to body temperature. So “the same "
            "vector space” isn't a slogan; it's the <strong>root of whether cross-modal retrieval can exist at all"
            "</strong>.",
        ),
    )
    + d.compare2(
        (L("文本路径", "Text path"), i18n.render(L("文字 → 文本 embedding", "text → text embedding"))),
        (L("图像路径", "Image path"), i18n.render(L("图片 → 图像 embedding", "image → image embedding"))),
        caption=L("两条路径映到<strong>同一向量空间</strong>，于是能跨模态互相检索",
                  "both map into the <strong>same vector space</strong>, enabling cross-modal retrieval"),
    )
    + c.section(
        L("建多模态索引：文本库、图像库各一，统一检索",
          "Build a multimodal index: a text store and an image store, retrieved together"),
        L(
            "把图文放进同一空间后，索引也要相应地<strong>分两套向量库</strong>。<code>MultiModalVectorStoreIndex</code> "
            "内部维护<strong>两个 store</strong>：一个存<strong>文本节点</strong>（段落，走文本 embedding），一个存"
            "<strong>图像节点</strong>（<code>ImageNode</code>，走图像 embedding）。<code>SimpleDirectoryReader</code> 读"
            "一个混合文件夹时，文本读成普通 <code>Document</code>、图片读成 <code>ImageDocument</code>，<code>"
            "from_documents</code> 自动按类型<strong>分流进各自的 store</strong>。查询时两个 store <strong>都召回</strong>，"
            "再把图、文候选<strong>合并</strong>交给下游——所以一次检索既可能捞回相关段落，也可能捞回相关图片。为什么要分"
            "两套、而不是混成一堆？因为两种模态的<strong>向量来自不同的 embedder</strong>，分库便于各自索引、各自调 "
            "top-k，最后在统一的检索结果里汇合。",
            "Once image and text share a space, the index splits into <strong>two vector stores</strong> to match. "
            "<code>MultiModalVectorStoreIndex</code> keeps <strong>two stores</strong> internally: one for <strong>text "
            "nodes</strong> (passages, via the text embedding) and one for <strong>image nodes</strong> (<code>ImageNode"
            "</code>, via the image embedding). When <code>SimpleDirectoryReader</code> reads a mixed folder, text "
            "becomes ordinary <code>Document</code>s and pictures become <code>ImageDocument</code>s, and <code>"
            "from_documents</code> automatically <strong>routes each type into its own store</strong>. At query time "
            "<strong>both stores are queried</strong> and the image + text candidates are <strong>merged</strong> for the "
            "downstream step — so one retrieval may pull back relevant passages and relevant pictures alike. Why two "
            "stores rather than one mixed pile? Because the two modalities' <strong>vectors come from different embedders"
            "</strong>; separate stores let each be indexed and top-k-tuned independently, then meet in one unified result "
            "set.",
        ),
        c.compare_table(
            [L("子库", "Sub-store"), L("存什么", "Holds"), L("用什么 embedding", "Embedded by")],
            [
                [L("文本 store", "Text store"), L("文本节点（段落）", "text nodes (passages)"),
                 L("文本 embedding（沿用前课的标准文本嵌入，同属集成）", "text embedding (the standard text embedder from L08 — also an integration)")],
                [L("图像 store", "Image store"), L("图像节点 <code>ImageNode</code>", "image nodes <code>ImageNode</code>"),
                 L("图像 embedding（如 CLIP，走集成）", "image embedding (e.g. CLIP, an integration)")],
            ],
        ),
    )
    + c.code(
        'from llama_index.core import SimpleDirectoryReader\n'
        'from llama_index.core.indices import MultiModalVectorStoreIndex\n\n'
        'documents = SimpleDirectoryReader("./mixed_docs").load_data()   # 文本 + 图片\n'
        'index = MultiModalVectorStoreIndex.from_documents(documents)\n'
        'qe = index.as_query_engine(llm=mm_llm)                          # mm_llm：多模态 LLM（走集成）\n'
        'print(qe.query("图里这台设备的型号和接口数量是多少？"))',
        caption=L("读混合文件夹建多模态索引：文本/图像各进一个 store，查询交多模态 LLM 看图作答",
                  "Build a multimodal index from a mixed folder: text/images go to separate stores; the query hands it to a multimodal LLM to read the picture"),
    )
    + c.source_ref(
        "indices/multi_modal/base.py", "MultiModalVectorStoreIndex",
        L("文本与图像各建向量库，统一检索。", "separate text/image vector stores, retrieved together."),
    )
    + c.source_ref(
        "llama-index-embeddings-clip", "ClipEmbedding",
        L("CLIP 图像 embedding 在 core 之外的<strong>集成包</strong>里——core 只给抽象；作答的视觉 LLM 同样是外部集成。",
          "the CLIP image embedding lives in an <strong>integration package</strong> outside core — core only ships the abstractions; the vision LLM is likewise an external integration."),
    )
    + c.section(
        L("检索件 + 生成件，都要换成多模态版",
          "Both the retrieval side and the generation side must go multimodal"),
        L(
            "把一套纯文本 RAG 升级成多模态，要<strong>同时换两个件</strong>，缺一不可。① <strong>检索件</strong>："
            "embedding 必须是<strong>多模态</strong>的，图片才能被编码进那个共享空间、被文字查到——这一步落在<strong>图像 "
            "embedding</strong>（如 CLIP）和索引里的<strong>图像 store</strong> 上。② <strong>生成件</strong>：作答的 LLM "
            "必须<strong>看得见图</strong>——检索召回的是图片节点，得交给一个<strong>多模态 LLM</strong>（视觉模型），它把"
            "图像当输入<strong>直接“看”</strong>着回答；换成纯文本 LLM，召回的图它根本读不了，多模态就白做了。还要分清"
            "<strong>哪是 core、哪是集成</strong>：抽象层是 core 的——<code>MultiModalLLM</code> 基类、<code>"
            "MultiModalVectorStoreIndex</code>、<code>ImageNode</code> 都在核心里；但<strong>具体能跑的模型</strong>——"
            "一个<strong>会看图的多模态 LLM</strong>（如 GPT-4o / Gemini）、CLIP 图像 embedding——都在 core 之外的<strong>集成包</strong>，"
            "要按需另装。core 给“<strong>插槽</strong>”，模型是“<strong>插件</strong>”。",
            "Upgrading a text-only RAG to multimodal means swapping <strong>two components at once</strong>, neither "
            "optional. (1) <strong>Retrieval side</strong>: the embedding must be <strong>multimodal</strong> so images "
            "get encoded into that shared space and become findable by text — this rides on the <strong>image embedding"
            "</strong> (e.g. CLIP) and the index's <strong>image store</strong>. (2) <strong>Generation side</strong>: the "
            "answering LLM must be able to <strong>see the image</strong> — retrieval returns image nodes, which must go "
            "to a <strong>multimodal LLM</strong> (a vision model) that takes the image as input and <strong>actually "
            "“looks”</strong> to answer; swap in a text-only LLM and it simply can't read the recalled pictures, wasting "
            "the whole effort. Keep <strong>what is core vs an integration</strong> straight: the abstraction layer is "
            "core — the <code>MultiModalLLM</code> base class, <code>MultiModalVectorStoreIndex</code> and <code>"
            "ImageNode</code> all live in core; but the <strong>concrete runnable models</strong> — a "
            "<strong>vision-capable multimodal LLM</strong> (e.g. GPT-4o / Gemini), the CLIP image embedding — sit in <strong>integration packages</strong> "
            "outside core and are installed as needed. Core gives the “<strong>sockets</strong>”, the models are the "
            "“<strong>plugins</strong>”.",
        ),
    )
    + d.flow([
        ("q", L("问题（文/图）", "query (text/img)")),
        ("ret", L("跨模态检索", "cross-modal retrieve"), L("图+文都召回", "images + text")),
        ("mm", L("多模态 LLM", "multimodal LLM"), L("看图作答", "reads images")),
        ("ans", L("答案", "answer")),
    ], caption=L("多模态 RAG：检索召回图与文，再交会看图的 LLM 合成",
                 "multimodal RAG: retrieve images+text, then a vision-capable LLM synthesizes"))
    + c.section(
        L("什么时候值得上多模态、什么时候不必",
          "When multimodal is worth it, and when it isn't"),
        L(
            "判断只看一件事：<strong>答案到底在不在“像素里”</strong>。值得上的典型场景，是信息<strong>只长在图里</strong>"
            "且文字旁注补不全的：读<strong>图表 / 仪表盘截图</strong>取趋势与数值、看<strong>产品照</strong>认型号与接口、"
            "查<strong>电路图 / 架构图 / 扫描件</strong>里的连接与标注——这些问题“看图才能答”，纯文本 RAG <strong>结构上"
            "答不了</strong>。反过来，如果图只是<strong>装饰</strong>、或它的信息<strong>本就写在正文 / 标题 / 配文里"
            "</strong>，那纯文本检索<strong>又快又便宜</strong>，没必要上多模态。成本也要算清：多模态 embedding 和视觉 "
            "LLM <strong>更贵更慢</strong>、图像 store 也更占资源。还有一种<strong>降级方案</strong>——先把图 OCR / 配成 "
            "caption 文字、再做纯文本 RAG：便宜，但<strong>丢视觉细节</strong>（布局、颜色、相对位置、图里没写成字的东西）。"
            "实务里的稳妥姿态是<strong>默认文本优先、图像按需启用</strong>：只对“确有图、且要看图”的查询和文档走多模态。",
            "The test is one thing: <strong>does the answer actually live “in the pixels”</strong>. The cases worth it "
            "are where information <strong>exists only in the image</strong> and no text caption fully covers it: reading "
            "<strong>charts / dashboard screenshots</strong> for trends and values, reading a <strong>product photo"
            "</strong> for a model number and ports, checking a <strong>schematic / architecture diagram / scan</strong> "
            "for connections and labels — these need you to “look at the picture”, and text-only RAG <strong>structurally "
            "can't answer</strong> them. Conversely, if the image is merely <strong>decorative</strong>, or its "
            "information is <strong>already written in the body / heading / caption</strong>, then text-only retrieval is "
            "<strong>faster and cheaper</strong> and multimodal isn't needed. Count the cost too: multimodal embeddings "
            "and vision LLMs are <strong>pricier and slower</strong>, and an image store consumes more resources. There's "
            "also a <strong>downgrade path</strong> — OCR/caption the image into text first, then do text-only RAG: "
            "cheap, but it <strong>loses visual detail</strong> (layout, color, relative position, anything not written "
            "out in the picture). The safe production stance is <strong>text-first by default, images enabled on demand"
            "</strong>: route only the queries and documents that “truly have an image and need to look at it” through "
            "the multimodal path.",
        ),
    )
    + c.analogy(L(
        "想象给每张照片和每个词都标上<strong>同一张地图上的坐标</strong>：一旦“猫的照片”和“猫”这个词被放到地图上"
        "<strong>同一个点</strong>，你就能<strong>站在词上、找最近的照片</strong>——这就是“用文字查图”。要是照片用的是"
        "一张地图、文字用的是另一张<strong>互不对齐</strong>的地图，那“谁离谁近”就<strong>无从谈起</strong>。多模态 "
        "embedding 干的就是“<strong>把图和字标到同一张地图上</strong>”这件事；剩下的检索，不过是<strong>在同一张图上找"
        "最近的点</strong>。",
        "Picture giving every photo and every word <strong>coordinates on the same map</strong>: once “a photo of a cat” "
        "and the word “cat” are placed at the <strong>same spot</strong>, you can <strong>stand on the word and find the "
        "nearest photo</strong> — that's “querying images with text”. If photos used one map and words used another, "
        "<strong>misaligned</strong> map, then “who is near whom” is <strong>meaningless</strong>. A multimodal "
        "embedding does exactly the “<strong>plot images and words on one shared map</strong>” part; the retrieval that "
        "follows is just <strong>finding the nearest point on that one map</strong>.",
    ))
    + c.key_points([
        L("多模态 RAG 的根：用<strong>多模态 embedding</strong>（如 CLIP）把图和文映进<strong>同一向量空间</strong>，"
          "跨模态最近邻才有意义，于是能“<strong>用文字查图、用图查图</strong>”。",
          "The root of multimodal RAG: a <strong>multimodal embedding</strong> (e.g. CLIP) maps images and text into the "
          "<strong>same vector space</strong>, making cross-modal nearest-neighbor meaningful — so you can “<strong>query "
          "images with text, or with images</strong>”."),
        L("<code>MultiModalVectorStoreIndex</code> 内部<strong>文本 store + 图像 store 各一</strong>，<code>"
          "from_documents</code> 按类型分流（文本 → <code>Document</code>、图片 → <code>ImageDocument</code>），查询时"
          "<strong>两库都召回再合并</strong>。",
          "<code>MultiModalVectorStoreIndex</code> keeps a <strong>text store and an image store</strong>; <code>"
          "from_documents</code> routes by type (text → <code>Document</code>, image → <code>ImageDocument</code>), and a "
          "query <strong>recalls from both stores and merges</strong>."),
        L("升级要<strong>同时换两个件</strong>：检索件换<strong>多模态 embedding</strong>，生成件换<strong>看得见图的"
          "多模态 LLM</strong>；纯文本 LLM 读不了召回的图。",
          "Upgrading swaps <strong>two components at once</strong>: a <strong>multimodal embedding</strong> on the "
          "retrieval side and a <strong>vision-capable multimodal LLM</strong> on the generation side; a text-only LLM "
          "can't read the recalled images."),
        L("<strong>core 给抽象、集成给模型</strong>：<code>MultiModalVectorStoreIndex</code> / <code>MultiModalLLM"
          "</code> / <code>ImageNode</code> 在 core；<strong>会看图的多模态 LLM</strong>（如 GPT-4o / Gemini）、CLIP embedding 在<strong>集成包"
          "</strong>。按需上多模态——<strong>答案在像素里才值得</strong>，否则文本优先更省。",
          "<strong>Core ships abstractions, integrations ship models</strong>: <code>MultiModalVectorStoreIndex</code> / "
          "<code>MultiModalLLM</code> / <code>ImageNode</code> are in core; a <strong>vision-capable multimodal LLM</strong> (e.g. GPT-4o / Gemini) and the CLIP "
          "embedding are in <strong>integration packages</strong>. Go multimodal on demand — <strong>worth it only when "
          "the answer is in the pixels</strong>, otherwise text-first is cheaper."),
    ])
    + c.design_highlight(L(
        "多模态 RAG 的精髓，是把“<strong>找相似</strong>”从纯文本扩展到图文之间，而这一切的支点只有一个：<strong>图和文"
        "落在同一个向量空间</strong>。有了这层<strong>跨模态对齐</strong>，“用文字查图”才从不可能变成一次普通的最近邻；"
        "没有它，图像向量和文本向量就是两套不能互比的坐标。工程上要记住三件事：① <strong>两个件一起换</strong>——检索端"
        "的多模态 embedding 让图<strong>进得了空间</strong>，生成端的视觉 LLM 让模型<strong>看得懂召回的图</strong>，缺一"
        "边都不成；② <strong>分清 core 与集成</strong>——core 只给 <code>MultiModalVectorStoreIndex</code> / <code>"
        "MultiModalLLM</code> 这层抽象插槽，真正能跑的视觉模型和 CLIP embedding 是外部集成，别把它们当核心内置；③ "
        "<strong>按需启用</strong>——多模态更贵更慢，只有当“<strong>答案确实在像素里</strong>”时才值得，否则文本优先、"
        "必要时再用 caption 降级。一句话：<strong>先让图文坐标统一，再让会看图的模型来回答</strong>。",
        "The essence of multimodal RAG is extending “<strong>find similar</strong>” from pure text to between images and "
        "text, and the whole thing pivots on one fulcrum: <strong>images and text landing in the same vector space"
        "</strong>. With that <strong>cross-modal alignment</strong>, “querying images with text” turns from impossible "
        "into an ordinary nearest-neighbor; without it, image vectors and text vectors are two coordinate systems you "
        "can't compare. Three engineering points: (1) <strong>swap both components together</strong> — the "
        "retrieval-side multimodal embedding lets images <strong>enter the space</strong>, the generation-side vision "
        "LLM lets the model <strong>understand the recalled images</strong>, and neither alone suffices; (2) <strong>keep "
        "core vs integrations straight</strong> — core ships only the abstraction sockets like <code>"
        "MultiModalVectorStoreIndex</code> / <code>MultiModalLLM</code>, while the actual runnable vision models and CLIP "
        "embedding are external integrations, not core built-ins; (3) <strong>enable on demand</strong> — multimodal is "
        "pricier and slower, worth it only when “<strong>the answer is truly in the pixels</strong>”, otherwise go "
        "text-first and fall back to captioning when needed. In a line: <strong>unify the coordinates of image and text "
        "first, then let a model that can see answer</strong>.",
    ))
)
LESSON_30 = _skeleton("retrieve", "查询分解（Sub-Question）", "query decomposition (Sub-Question)")
LESSON_31 = _skeleton("synthesize", "结构化输出", "structured outputs")
