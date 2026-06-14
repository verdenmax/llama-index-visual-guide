"""Part 5 (capstone): lesson 20. Content filled task-by-task."""
import components as c
import diagrams as d
import i18n
from i18n import L


def _lessons(*pairs):
    """Render clickable lesson-number links (identical in both languages)."""
    links = " · ".join(f'<a href="{fname}">{num}</a>' for num, fname in pairs)
    return L(links, links)


LESSON_20 = (
    c.pipeline(None)
    + c.lead(L(
        "把前面每一站拼成一个<strong>可运行的本地 RAG 应用</strong>：加载 → 摄取/切块 → 建索引 → 持久化 → 检索 → 后处理 → "
        "合成 → 问答/多轮 → 评估。这一课就是“总装车间”。",
        "Assemble every stop into a <strong>runnable local RAG app</strong>: load → ingest/split → index → persist → "
        "retrieve → post-process → synthesize → Q&amp;A/chat → evaluate. This lesson is the final assembly line.",
    ))
    + d.flow([
        ("load", L("加载", "Load"), L("Reader", "Reader")),
        ("ingest", L("摄取/切块", "Ingest/Split"), L("IngestionPipeline", "IngestionPipeline")),
        ("index", L("建索引", "Index"), L("VectorStoreIndex", "VectorStoreIndex")),
        ("persist", L("持久化", "Persist"), L("StorageContext", "StorageContext")),
        ("retrieve", L("检索", "Retrieve"), L("Retriever", "Retriever")),
        ("postproc", L("后处理", "Post-process"), L("Postprocessor", "Postprocessor")),
        ("synth", L("合成", "Synthesize"), L("ResponseSynthesizer", "ResponseSynthesizer")),
        ("chat", L("问答/多轮", "Query/Chat"), L("Query/Chat Engine", "Query/Chat Engine")),
        ("eval", L("评估", "Evaluate"), L("Evaluator", "Evaluator")),
    ], caption=L(
        "端到端架构：每一站都可替换",
        "End-to-end architecture: every stop is swappable",
    ))
    + c.analogy(L(
        "前面学的每个零件，现在装成一台完整的<strong>“知识问答机”</strong>——拧上电源就能跑。",
        "Every part you've learned now snaps together into a complete <strong>“knowledge answering machine”</strong> — "
        "plug it in and it runs.",
    ))
    + c.section(
        L("总装清单（每步都可点回对应课）", "Assembly checklist (every step links back to its lessons)"),
        c.compare_table(
            [L("阶段", "Stage"), L("对应课（可点）", "Lessons (clickable)")],
            [
                [L("加载 → 文档/节点 → 切块 → 抽取", "load → docs/nodes → split → extract"),
                 _lessons(("04", "04-documents-nodes.html"), ("05", "05-readers.html"),
                          ("06", "06-node-parsers.html"), ("07", "07-metadata-extractors.html"))],
                [L("向量化 → 索引 → 向量库 → 持久化", "embed → index → vector store → persist"),
                 _lessons(("08", "08-embeddings.html"), ("09", "09-vector-stores.html"),
                          ("10", "10-index-abstraction.html"), ("11", "11-ingestion-storage.html"))],
                [L("检索 → 后处理 → 合成", "retrieve → post-process → synthesize"),
                 _lessons(("12", "12-retrievers.html"), ("13", "13-postprocessors.html"),
                          ("14", "14-response-synthesizers.html"))],
                [L("查询引擎 / 多轮聊天", "query engine / multi-turn chat"),
                 _lessons(("15", "15-query-engine.html"), ("16", "16-chat-engine.html"))],
                [L("全局配置 &amp; Prompt（贯穿全程）", "global Settings &amp; prompts (throughout)"),
                 _lessons(("17", "17-settings-prompts.html"))],
                [L("进阶检索（可选升级）", "advanced retrieval (optional upgrade)"),
                 _lessons(("18", "18-advanced-retrieval.html"))],
                [L("评估闭环", "evaluation loop"),
                 _lessons(("19", "19-evaluation.html"))],
            ],
        ),
    )
    + c.section(
        L("把整本书拼成一个应用", "Assembling the whole guide into one app"),
        L(
            "前 19 课每一课都拆开了管道上的一站；这一课把它们按同一套接口拼回去。整条链路只有两个阶段："
            "<strong>写入路径</strong>把数据变成可复用、可落盘的索引，<strong>查询路径</strong>在索引之上反复检索、合成、作答。"
            "因为每一站都遵守统一抽象，你可以只替换其中一件（换向量库、换检索器、加一道评估），而不动其余结构。"
            "举例：想要更强的召回，把 <code>as_retriever</code> 换成第 18 课的 <code>QueryFusionRetriever</code> 即可，主流程一行不改；"
            "而全局 <code>Settings</code>（第 17 课）从一开始就在背后统一着 LLM 与 embedding。",
            "Each of the first 19 lessons opened up one stop on the pipeline; this one snaps them back together behind "
            "one shared interface. The whole chain has just two phases: the <strong>write path</strong> turns data into "
            "a reusable, persistable index, and the <strong>query path</strong> retrieves, synthesizes and answers on "
            "top of it — over and over. Because every stop obeys the same abstraction, you can swap a single part (a "
            "different vector store, a different retriever, an added evaluator) without disturbing the rest. For "
            "example, to boost recall just swap <code>as_retriever</code> for Lesson 18's <code>QueryFusionRetriever</code> "
            "— the main flow doesn't change a line; meanwhile the global <code>Settings</code> (Lesson 17) has been "
            "unifying the LLM and embedding behind the scenes all along.",
        ),
        d.compare2(
            (L("首次建库（load → ingest → persist）", "First build (load → ingest → persist)"), i18n.render(L(
                "首次运行：<code>SimpleDirectoryReader</code> 加载 → <code>IngestionPipeline</code> 切块/抽取 → "
                "<code>VectorStoreIndex</code> 向量化建索引 → <code>persist('./storage')</code> 落盘。较重，但只做一次。",
                "First run: <code>SimpleDirectoryReader</code> loads → <code>IngestionPipeline</code> splits/extracts → "
                "<code>VectorStoreIndex</code> embeds &amp; indexes → <code>persist('./storage')</code> to disk. "
                "Heavy, but one-off.",
            ))),
            (L("复用（load_index_from_storage）", "Reuse (load_index_from_storage)"), i18n.render(L(
                "以后启动：<code>StorageContext.from_defaults(persist_dir='./storage')</code> + "
                "<code>load_index_from_storage</code> 直接复活索引，跳过重新切块与向量化，秒级就绪。",
                "Later starts: <code>StorageContext.from_defaults(persist_dir='./storage')</code> + "
                "<code>load_index_from_storage</code> revive the index directly — skip re-splitting and re-embedding, "
                "ready in seconds.",
            ))),
            caption=L(
                "第一次建库较重；之后用 load_index_from_storage 秒级复用",
                "The first build is heavy; afterwards load_index_from_storage reuses it in seconds",
            ),
        ),
    )
    + c.source_ref("(综合 / integrates)", "VectorStoreIndex · IngestionPipeline · RetrieverQueryEngine · FaithfulnessEvaluator",
                   L("把全书组件拼到一起", "wires the whole guide's components together"))
    + c.accordion(
        L("深入：端到端组装", "Deep dive: end-to-end assembly"),
        c.qa_item(
            L("🧪 示例", "🧪 Example"),
            L(
                "capstone 的核心是一个 <code>if os.path.exists(PERSIST)</code> 分支：存在就 "
                "<code>load_index_from_storage</code> 秒级复活，否则跑一遍 <code>IngestionPipeline</code> → "
                "<code>VectorStoreIndex</code> 再 <code>persist</code>。其余几行只是把检索器、后处理、合成器、"
                "评估器装到同一个 <code>RetrieverQueryEngine</code> 上。",
                "The heart of the capstone is one <code>if os.path.exists(PERSIST)</code> branch: if it exists, "
                "<code>load_index_from_storage</code> revives it in seconds; otherwise run <code>IngestionPipeline</code> "
                "→ <code>VectorStoreIndex</code> once, then <code>persist</code>. The remaining lines just bolt a "
                "retriever, postprocessor, synthesizer and evaluator onto one <code>RetrieverQueryEngine</code>.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "因为每一站都是实现同一接口的<strong>标准件</strong>，整台应用才能像搭积木一样拼装。换一个向量库或"
                "检索策略时，你不必重写主流程——只把对应那块换掉，<code>RetrieverQueryEngine</code> 的骨架原封不动。",
                "Because every stop is a <strong>standard part</strong> implementing the same interface, the whole app "
                "assembles like building blocks. To change a vector store or retrieval strategy you never rewrite the "
                "main flow — just swap that one block while the <code>RetrieverQueryEngine</code> skeleton stays intact.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "运行分两支：首次走<strong>写入路径</strong>（摄取 → 建索引 → <code>persist</code>），之后走"
                "<strong>复用路径</strong>（<code>load_index_from_storage</code>）。关键时序："
                "<code>Settings.embed_model</code> 必须在<strong>建索引之前</strong>设好——落盘的向量由它决定，"
                "加载后必须用同一个 embedding 才能对齐检索。",
                "It runs in two branches: the first time takes the <strong>write path</strong> (ingest → index → "
                "<code>persist</code>); later runs take the <strong>reuse path</strong> "
                "(<code>load_index_from_storage</code>). Critical ordering: <code>Settings.embed_model</code> must be "
                "set <strong>before building the index</strong> — it determines the vectors written to disk, and after "
                "loading you must use the same embedding for retrieval to line up.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "想把这台问答机改造成<strong>“带脚注的客服机器人”</strong>？只需替换三件：把 query engine 换成 "
                "<code>chat_mode='condense_plus_context'</code> 的 <strong>chat engine</strong>（多轮记忆）、加一道"
                "<strong>引用后处理</strong>把 <code>source_nodes</code> 渲染成脚注、再挂上<strong>评估</strong>当上线前的"
                "质量闸。骨架不变，只换这几块。",
                "Want to turn this answering machine into a <strong>“support bot with footnotes”</strong>? Swap just "
                "three parts: replace the query engine with a <strong>chat engine</strong> "
                "(<code>chat_mode='condense_plus_context'</code>) for multi-turn memory, add a <strong>citation "
                "postprocessor</strong> that renders <code>source_nodes</code> as footnotes, and attach "
                "<strong>evaluation</strong> as a pre-launch quality gate. The skeleton stays; only these blocks change.",
            ),
        ),
    )
    + c.code(
        "from llama_index.core import (\n"
        "    SimpleDirectoryReader, VectorStoreIndex, StorageContext,\n"
        "    load_index_from_storage, Settings, get_response_synthesizer,\n"
        ")\n"
        "from llama_index.core.node_parser import SentenceSplitter\n"
        "from llama_index.core.ingestion import IngestionPipeline\n"
        "from llama_index.core.postprocessor import SimilarityPostprocessor\n"
        "from llama_index.core.query_engine import RetrieverQueryEngine\n"
        "from llama_index.core.evaluation import FaithfulnessEvaluator\n"
        "from llama_index.llms.openai import OpenAI\n"
        "from llama_index.embeddings.openai import OpenAIEmbedding\n"
        "import os\n\n"
        "Settings.llm = OpenAI(model='gpt-4o-mini')\n"
        "Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')\n\n"
        "PERSIST = './storage'\n"
        "if os.path.exists(PERSIST):                      # 已建过就秒加载\n"
        "    index = load_index_from_storage(StorageContext.from_defaults(persist_dir=PERSIST))\n"
        "else:                                            # 首次：摄取 -&gt; 建索引 -&gt; 落盘\n"
        "    docs = SimpleDirectoryReader('./data').load_data()\n"
        "    nodes = IngestionPipeline(transformations=[SentenceSplitter(chunk_size=512, chunk_overlap=50)]).run(documents=docs)\n"
        "    index = VectorStoreIndex(nodes)\n"
        "    index.storage_context.persist(persist_dir=PERSIST)\n\n"
        "engine = RetrieverQueryEngine.from_args(\n"
        "    retriever=index.as_retriever(similarity_top_k=4),\n"
        "    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.4)],  # \u9608\u503c\u968f\u6570\u636e\u800c\u5b9a\n"
        "    response_synthesizer=get_response_synthesizer(response_mode='compact'),\n"
        ")\n"
        "resp = engine.query('退款政策是什么？')\n"
        "print('答案:', resp)\n"
        "print('忠实度:', FaithfulnessEvaluator().evaluate_response(response=resp).passing)\n\n"
        "chat = index.as_chat_engine(chat_mode='condense_plus_context')\n"
        "print(chat.chat('那国际订单也一样吗？'))",
        caption=L("一个文件跑通完整 RAG（含持久化、后处理、评估、多轮）", "one file, full RAG: persistence, post-processing, eval, chat"),
    )
    + c.code(
        "from llama_index.core.evaluation import FaithfulnessEvaluator, RelevancyEvaluator\n\n"
        "# 在 capstone 的 engine 之上：把单次评估扩成可回归的质量闸\n"
        "faith = FaithfulnessEvaluator()        # 答案是否忠于检索到的上下文\n"
        "relev = RelevancyEvaluator()           # 检索到的上下文是否切题\n\n"
        "eval_set = ['退款要多久到账？', '国际订单能退吗？', '怎么申请换货？']\n"
        "passed = 0\n"
        "for q in eval_set:\n"
        "    resp = engine.query(q)\n"
        "    ok = (faith.evaluate_response(response=resp).passing\n"
        "          and relev.evaluate_response(query=q, response=resp).passing)\n"
        "    passed += int(ok)\n"
        "    print(q, 'PASS' if ok else 'FAIL')\n"
        "print(f'通过率 pass-rate: {passed}/{len(eval_set)}')",
        caption=L("批量评估当回归测试：改完管道就重跑这套用例", "Batch eval as a regression test: re-run this set after every pipeline change"),
    )
    + c.key_points([
        L("完整 RAG = 写入路径（建一次、落盘）+ 查询路径（反复问）。",
          "A full RAG = write path (build once, persist) + query path (ask repeatedly)."),
        L("每一站都是<strong>可替换</strong>组件：换库、换检索、换合成都不动主结构。",
          "Every stop is a <strong>swappable</strong> component: change store/retrieval/synthesis without touching the skeleton."),
        L("持久化 + 评估让它从 demo 走向<strong>可维护、可回归</strong>。",
          "Persistence + evaluation take it from demo to <strong>maintainable and regression-safe</strong>."),
    ])
    + c.design_highlight(L(
        "整条管道每一站都能独立替换，却共享统一接口——这正是 LlamaIndex 的核心思想：<strong>用可组合的标准件搭出你自己的 RAG</strong>。",
        "Every stop swaps independently yet shares one interface — that's LlamaIndex's core idea: <strong>compose your own "
        "RAG from standard, interchangeable parts</strong>.",
    ))
)
