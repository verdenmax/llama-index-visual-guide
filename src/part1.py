"""Part 1 (macro overview): lessons 01-03. Content filled task-by-task."""
import components as c
from i18n import L


def _stub():
    return c.pipeline(None) + c.lead(L("（本课内容建设中）", "(Lesson content coming soon)"))


LESSON_01 = (
    c.pipeline(None)
    + c.lead(L(
        "<strong>LlamaIndex</strong> 是一个把<strong>检索增强生成（RAG）</strong>这条数据管道"
        "标准化、可编排的框架。它不训练模型，只负责模型<strong>周边的全部管道</strong>："
        "把你的数据加载、切块、向量化、建索引，再在提问时检索相关片段、喂给 LLM 生成<strong>有依据</strong>的回答。",
        "<strong>LlamaIndex</strong> is a framework that standardizes and orchestrates the "
        "<strong>Retrieval-Augmented Generation (RAG)</strong> pipeline. It doesn't train models — it owns "
        "everything <em>around</em> them: loading, chunking, embedding and indexing your data, then at query "
        "time retrieving the relevant pieces and feeding them to the LLM for a <strong>grounded</strong> answer.",
    ))
    + c.analogy(L(
        "把 LLM 想成一个聪明但在<strong>闭卷</strong>考试的学生：只能凭记忆答题，记不住就开始编。"
        "RAG 让它<strong>开卷</strong>——先翻到相关页（检索），再据此作答（生成）。"
        "LlamaIndex 就是帮你建好这座图书馆和索书系统的工具。",
        "Picture an LLM as a smart student in a <strong>closed-book</strong> exam: it answers from memory and "
        "invents things it can't recall. RAG makes it <strong>open-book</strong> — find the relevant pages first "
        "(retrieve), then answer from them (generate). LlamaIndex builds that library and its call-number system.",
    ))
    + c.section(
        L("RAG 解决什么问题？", "What problem does RAG solve?"),
        c.compare_table(
            [L("痛点", "Pain point"), L("只用 LLM", "LLM alone"), L("用 RAG", "With RAG")],
            [
                [L("知识截止", "Knowledge cutoff"), L("训练后的新知识一概不知", "Blind to anything after training"),
                 L("先检索实时/私有资料再答", "Retrieves fresh/private data first")],
                [L("幻觉", "Hallucination"), L("不确定也答得很自信", "Confidently makes things up"),
                 L("答案有检索到的出处支撑", "Answers grounded in retrieved sources")],
                [L("私有数据", "Private data"), L("没见过你的文档", "Never saw your documents"),
                 L("把你的文档建成可检索索引", "Indexes your docs for retrieval")],
            ],
        ),
    )
    + c.source_ref(
        "llama_index/core/__init__.py", "VectorStoreIndex · SimpleDirectoryReader",
        L("RAG 的高层入口都从这里导出", "the high-level RAG entry points are exported here"),
    )
    + c.code(
        "pip install llama-index\n\n"
        "from llama_index.core import VectorStoreIndex, SimpleDirectoryReader\n\n"
        "# 写入路径：加载 -&gt; 切块 -&gt; 向量化 -&gt; 建索引（一行搞定）\n"
        "docs = SimpleDirectoryReader('./data').load_data()\n"
        "index = VectorStoreIndex.from_documents(docs)\n\n"
        "# 查询路径：检索 -&gt; 合成 -&gt; 有依据的回答\n"
        "engine = index.as_query_engine()\n"
        "print(engine.query('这些文档讲了什么？'))",
        caption=L("最小可运行 RAG：5 行", "A minimal runnable RAG in 5 lines"),
    )
    + c.key_points([
        L("RAG = 先<strong>检索</strong>相关片段，再让 LLM 据此<strong>生成</strong>，避免重训与幻觉。",
          "RAG = <strong>retrieve</strong> relevant snippets, then <strong>generate</strong> from them — no "
          "retraining, fewer hallucinations."),
        L("LlamaIndex 负责 RAG 的<strong>数据与编排</strong>，不做训练或推理本身。",
          "LlamaIndex owns the <strong>data + orchestration</strong> of RAG, not training or inference."),
        L("两条主线贯穿全书：<strong>写入路径</strong>（建索引）与<strong>查询路径</strong>（问答）。",
          "Two through-lines: the <strong>write path</strong> (build the index) and the <strong>query path</strong> (ask)."),
    ])
    + c.design_highlight(L(
        "RAG 的精妙在于把模型的“记忆”<strong>外置</strong>为一个可随时更新、可检索的索引——"
        "更新知识只需重建索引，模型本身原封不动。",
        "RAG's elegance: it <strong>externalizes</strong> the model's “memory” into a searchable index you can "
        "refresh anytime — update knowledge by rebuilding the index, never touching the model.",
    ))
)
LESSON_02 = (
    c.pipeline(None)
    + c.lead(L(
        "LlamaIndex 分两层：<strong>core</strong>（稳定的抽象与编排）+ <strong>300+ 集成包</strong>"
        "（具体的 LLM / Embedding / 向量库实现）。命名约定一眼区分：导入路径带 <code>core</code> 的是核心抽象，"
        "不带的是某个第三方集成。",
        "LlamaIndex has two layers: <strong>core</strong> (stable abstractions + orchestration) and "
        "<strong>300+ integration packages</strong> (concrete LLM / embedding / vector-store implementations). "
        "The import path tells them apart: paths with <code>core</code> are core abstractions; those without are a "
        "specific third-party integration.",
    ))
    + c.analogy(L(
        "core 像主板上的<strong>标准插槽</strong>，集成包像各品牌的内存条/显卡：只要符合插槽规范，"
        "插上即用，换品牌不用换主板。",
        "core is the <strong>standard slots</strong> on a motherboard; integrations are branded RAM/GPUs: anything "
        "that fits the slot just works, and swapping brands never means swapping the board.",
    ))
    + c.section(
        L("命名约定：一眼看出是核心还是集成", "Naming: spot core vs integration at a glance"),
        c.compare_table(
            [L("导入", "Import"), L("含义", "Meaning")],
            [
                [L("<code>from llama_index.core import VectorStoreIndex</code>", "<code>from llama_index.core import VectorStoreIndex</code>"),
                 L("核心抽象（稳定接口）", "core abstraction (stable interface)")],
                [L("<code>from llama_index.llms.openai import OpenAI</code>", "<code>from llama_index.llms.openai import OpenAI</code>"),
                 L("OpenAI LLM 集成实现", "the OpenAI LLM integration")],
                [L("<code>from llama_index.embeddings.huggingface import ...</code>", "<code>from llama_index.embeddings.huggingface import ...</code>"),
                 L("HuggingFace Embedding 集成", "the HuggingFace embedding integration")],
                [L("<code>from llama_index.vector_stores.chroma import ...</code>", "<code>from llama_index.vector_stores.chroma import ...</code>"),
                 L("Chroma 向量库集成", "the Chroma vector-store integration")],
            ],
        ),
    )
    + c.source_ref(
        "llama_index/core/__init__.py", "(package root)",
        L("core 导出所有稳定抽象；集成包各自独立发版", "core exports the stable abstractions; integrations ship as separate packages"),
    )
    + c.code(
        "# 核心 + 按需安装集成（每个集成是独立的 pip 包）\n"
        "pip install llama-index-core\n"
        "pip install llama-index-llms-openai llama-index-embeddings-openai\n\n"
        "from llama_index.core import Settings           # 核心：全局配置\n"
        "from llama_index.llms.openai import OpenAI       # 集成：换成别家只改这一行\n"
        "from llama_index.embeddings.openai import OpenAIEmbedding\n\n"
        "Settings.llm = OpenAI(model='gpt-4o-mini')\n"
        "Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')",
        caption=L("core 定接口，集成填实现", "core defines interfaces, integrations fill them in"),
    )
    + c.key_points([
        L("导入路径带 <code>core</code> = 核心抽象；不带 = 第三方集成实现。",
          "Import path with <code>core</code> = core abstraction; without = a third-party integration."),
        L("集成是<strong>独立 pip 包</strong>，按需安装，互不绑定版本。",
          "Integrations are <strong>separate pip packages</strong>, installed à la carte."),
        L("换 LLM / Embedding / 向量库只改导入与一行配置，主链路不动。",
          "Swapping the LLM / embedding / vector store is an import + one config line; the pipeline stays."),
    ])
    + c.design_highlight(L(
        "“接口在 core、实现在 integration”的分层，让生态可以<strong>独立演进</strong>："
        "新增一个向量库只需发一个集成包，core 不必改动也不必发版。",
        "Putting “interfaces in core, implementations in integrations” lets the ecosystem <strong>evolve "
        "independently</strong>: adding a vector store is just a new integration package — core never changes.",
    ))
)
LESSON_03 = (
    c.pipeline(None)
    + c.lead(L(
        "那 5 行代码背后是<strong>两个阶段</strong>：<strong>写入路径</strong>（建索引，做一次）和"
        "<strong>查询路径</strong>（问答，做很多次）。高层 API 把每个阶段的细节藏了起来——本课先看全景，后面逐站拆解。",
        "Those 5 lines hide <strong>two phases</strong>: the <strong>write path</strong> (build the index, once) and "
        "the <strong>query path</strong> (ask, many times). The high-level API hides each stage's detail — this "
        "lesson is the map; later lessons visit each stop.",
    ))
    + c.analogy(L(
        "写入路径像<strong>建图书馆</strong>：收书、拆章节、编索书号、上架。查询路径像<strong>借阅问答</strong>："
        "按主题找到相关几页，读完再用自己的话回答你。",
        "The write path is like <strong>building a library</strong>: collect books, split chapters, assign call "
        "numbers, shelve. The query path is like <strong>asking the librarian</strong>: find the few relevant "
        "pages, read them, answer in their own words.",
    ))
    + c.section(
        L("把 5 行代码映射到流水线", "Mapping the 5 lines onto the pipeline"),
        c.compare_table(
            [L("代码", "Code"), L("阶段", "Stage"), L("幕后发生了什么", "What happens under the hood")],
            [
                [L("<code>SimpleDirectoryReader(...).load_data()</code>", "<code>SimpleDirectoryReader(...).load_data()</code>"),
                 L("加载", "Load"), L("文件 → <code>Document</code> 列表", "files → list of <code>Document</code>")],
                [L("<code>VectorStoreIndex.from_documents(docs)</code>", "<code>VectorStoreIndex.from_documents(docs)</code>"),
                 L("切块+向量化+索引", "Split + embed + index"), L("Document → Node → 向量 → 存入索引", "Document → Node → vectors → stored in the index")],
                [L("<code>index.as_query_engine()</code>", "<code>index.as_query_engine()</code>"),
                 L("装配查询", "Assemble query"), L("检索器 + 后处理 + 响应合成器 组装好", "wires retriever + postprocessors + synthesizer")],
                [L("<code>engine.query('...')</code>", "<code>engine.query('...')</code>"),
                 L("检索→合成→回答", "Retrieve→synthesize→answer"), L("取相关 Node，交 LLM 生成有依据回答", "fetch relevant Nodes, LLM answers from them")],
            ],
        ),
    )
    + c.source_ref(
        "indices/base.py", "BaseIndex.from_documents",
        L("写入路径的“快捷方式”（VectorStoreIndex 继承自 BaseIndex），内部串起 split→embed→store",
          "the write-path shortcut (VectorStoreIndex inherits it from BaseIndex); chains split→embed→store inside"),
    )
    + c.source_ref(
        "base/base_query_engine.py", "BaseQueryEngine.query",
        L("查询路径的统一入口", "the unified entry point of the query path"),
    )
    + c.code(
        "from llama_index.core import VectorStoreIndex, SimpleDirectoryReader\n\n"
        "# —— 写入路径（建一次索引）——\n"
        "docs = SimpleDirectoryReader('./data').load_data()   # 加载\n"
        "index = VectorStoreIndex.from_documents(docs)        # 切块+向量化+索引\n\n"
        "# —— 查询路径（可反复问）——\n"
        "engine = index.as_query_engine(similarity_top_k=3)   # 装配\n"
        "resp = engine.query('退款政策是什么？')              # 检索→合成→回答\n"
        "print(resp)                  # 答案\n"
        "print(resp.source_nodes)     # 依据：检索到的片段",
        caption=L("同一个 index，写一次、问多次", "one index: write once, query many times"),
    )
    + c.key_points([
        L("写入路径做一次、查询路径做多次；二者共享同一个 <code>index</code>。",
          "Write path runs once, query path many times; both share one <code>index</code>."),
        L("<code>from_documents</code> 隐藏了 split→embed→store；<code>as_query_engine</code> 隐藏了 retrieve→synthesize。",
          "<code>from_documents</code> hides split→embed→store; <code>as_query_engine</code> hides retrieve→synthesize."),
        L("<code>response.source_nodes</code> 让答案<strong>可溯源</strong>。",
          "<code>response.source_nodes</code> makes every answer <strong>traceable</strong>."),
    ])
    + c.design_highlight(L(
        "高层 API 是低层管道的“快捷方式”：新手用一行跑通，进阶者拆开每一站替换组件——"
        "<strong>同一套抽象，两种使用深度</strong>。",
        "The high-level API is a shortcut over the low-level pipeline: beginners get it running in one line; "
        "experts open each stop to swap components — <strong>one set of abstractions, two depths of use</strong>.",
    ))
)
