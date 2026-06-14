"""Part 1 (macro overview): lessons 01-03. Content filled task-by-task."""
import components as c
import diagrams as d
import i18n
from i18n import L


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
    + d.flow([
        ("load", L("加载", "Load")),
        ("split", L("切块", "Split")),
        ("embed", L("向量化", "Embed")),
        ("store", L("存储", "Store")),
        ("index", L("索引", "Index")),
        ("retrieve", L("检索", "Retrieve")),
        ("synth", L("合成", "Synthesize")),
        ("answer", L("回答", "Answer")),
    ], caption=L(
        "RAG 全景：左半是写入路径（建好索引，做一次），右半是查询路径（据此作答，做很多次）",
        "The RAG pipeline at a glance: the left half (write path) builds the index once; "
        "the right half (query path) answers from it, many times",
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
    + c.section(
        L("三个痛点，同一个根因", "Three pains, one root cause"),
        L(
            "知识截止、幻觉、私有数据看似三件事，根因只有一个：模型的知识在训练时就被<strong>冻结</strong>"
            "在参数里，既无法更新，也说不清依据。RAG 不去改这套被冻结的参数，而是在提问时临时<strong>挂载</strong>"
            "一份可检索的外部资料，让答案有据可查、随时可换。",
            "Knowledge cutoff, hallucination and private data look like three problems but share one root cause: the "
            "model's knowledge is <strong>frozen</strong> into its weights at training time — it can neither refresh "
            "nor cite. RAG doesn't touch those frozen weights; it <strong>mounts</strong> a searchable external "
            "corpus at query time so answers stay grounded and the knowledge stays swappable.",
        ),
        d.compare2(
            (L("闭卷 LLM", "Closed-book LLM"), i18n.render(L(
                "只凭参数里的记忆作答；遇到没学过或已过时的内容就开始“编”，且给不出处。",
                "Answers only from memory baked into its weights; for anything unseen or stale it makes things up, "
                "with no sources.",
            ))),
            (L("开卷 RAG", "Open-book RAG"), i18n.render(L(
                "先检索相关资料，再据此作答，每句话都能逐条追溯到出处。",
                "Retrieves relevant material first, then answers from it — every claim traceable to a source.",
            ))),
            caption=L(
                "同一个问题：闭卷靠脆弱的记忆，开卷靠可核对的检索",
                "Same question: closed-book leans on fragile memory, open-book on checkable retrieval",
            ),
        ),
    )
    + c.source_ref(
        "llama_index/core/__init__.py", "VectorStoreIndex · SimpleDirectoryReader",
        L("RAG 的高层入口都从这里导出", "the high-level RAG entry points are exported here"),
    )
    + c.accordion(
        L("深入：RAG 的来龙去脉", "Deep dive: the why and how of RAG"),
        c.qa_item(
            L("🧪 示例：直接塞进 prompt 会怎样", "🧪 Example: what if you just stuff the prompt"),
            L(
                "把整本手册粘进 prompt 看似省事，但会撞上上下文长度上限、推理更慢更贵，且模型容易“迷失在中间”"
                "而漏掉关键句。RAG 只挑最相关的几段进 prompt，既省 token 又更准。",
                "Pasting a whole manual into the prompt seems easy, but you hit the context-length ceiling, pay more "
                "for slower inference, and the model tends to get “lost in the middle” and miss key lines. RAG feeds "
                "only the few most relevant snippets — cheaper and more accurate.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "把知识<strong>外置</strong>成可检索索引，意味着更新知识只需重建索引、模型零改动；"
                "同一个模型可服务无数套互不相同的私有库。",
                "<strong>Externalizing</strong> knowledge into a searchable index means updating knowledge is just "
                "rebuilding the index — the model never changes, and one model can serve countless private corpora.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "<code>from_documents</code> 在写入路径里把文档切块、向量化、写进索引；"
                "<code>query</code> 在查询路径里把问题向量化、取最近邻、再交给 LLM 据此作答——两行 API 各藏了一条管道。",
                "<code>from_documents</code> runs the write path (split → embed → store); <code>query</code> runs the "
                "query path (embed the question → nearest-neighbor search → LLM answers from them) — each one-liner "
                "hides a pipeline.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "微调把知识焊进参数（更新贵、难溯源）；超长上下文直接全塞（贵且会“迷失在中间”）；"
                "RAG 取两者之间——外置、可更新、可溯源，是私有或时效性知识的默认选择。",
                "Fine-tuning welds knowledge into weights (costly to update, hard to cite); ultra-long context just "
                "dumps everything in (expensive, “lost in the middle”); RAG sits in between — external, refreshable, "
                "citable — the default for private or time-sensitive knowledge.",
            ),
        ),
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
    + c.code(
        "from llama_index.core import VectorStoreIndex, SimpleDirectoryReader\n\n"
        "index = VectorStoreIndex.from_documents(\n"
        "    SimpleDirectoryReader('./data').load_data())\n\n"
        "engine = index.as_query_engine(similarity_top_k=3)\n"
        "resp = engine.query('退款要多久到账？')\n\n"
        "print(resp)                      # 有依据的回答\n"
        "for n in resp.source_nodes:      # 答案的出处，可逐条核对\n"
        "    print(round(n.score, 3), n.node.get_content()[:60])",
        caption=L("可溯源查询：每个答案都能追到检索片段", "Traceable query: trace every answer back to its retrieved snippets"),
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
    + d.layers([
        (L("应用 / 你的代码", "Your app / your code"),
         L("只调用统一抽象，几乎不感知底层换没换", "calls the unified abstractions, barely notices swaps below")),
        (L("llama-index-core", "llama-index-core"),
         L("稳定的抽象与编排：Index / Retriever / QueryEngine …", "stable abstractions + orchestration: Index / Retriever / QueryEngine …")),
        (L("300+ 集成包", "300+ integration packages"),
         L("各家 LLM / Embedding / 向量库 的具体实现", "concrete LLM / embedding / vector-store implementations")),
    ], caption=L(
        "两层结构：core 定接口、集成填实现，应用只依赖 core",
        "Two layers: core defines the interfaces, integrations fill them in, and your app depends only on core",
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
    + c.section(
        L("为什么把接口和实现拆开", "Why split interfaces from implementations"),
        L(
            "core 只定义“能做什么”的抽象接口，具体“怎么做”交给独立集成包。于是新增一个 LLM 或向量库厂商，"
            "只需发布一个集成包，core 不必改动、也不必跟着发版；你的应用只依赖 core 的稳定接口，换厂商几乎零成本。",
            "core defines only the abstract “what”; each concrete “how” lives in a separate integration. So adding a "
            "new LLM or vector-store vendor is just publishing one integration package — core never changes or "
            "re-releases, and because your app depends only on core's stable interface, swapping vendors is near-free.",
        ),
        d.annot(
            L("BaseLLM 接口（core）", "BaseLLM interface (core)"),
            [
                (L("OpenAI", "OpenAI"), L("llama-index-llms-openai", "llama-index-llms-openai")),
                (L("Anthropic", "Anthropic"), L("llama-index-llms-anthropic", "llama-index-llms-anthropic")),
                (L("HuggingFace", "HuggingFace"), L("llama-index-llms-huggingface", "llama-index-llms-huggingface")),
                (L("Ollama（本地）", "Ollama (local)"), L("llama-index-llms-ollama", "llama-index-llms-ollama")),
            ],
            caption=L(
                "一个 core 接口，多份集成实现：插上即用、按需安装",
                "One core interface, many integration impls: plug in à la carte",
            ),
        ),
    )
    + c.source_ref(
        "llama_index/core/__init__.py", "(package root)",
        L("core 导出所有稳定抽象；集成包各自独立发版", "core exports the stable abstractions; integrations ship as separate packages"),
    )
    + c.accordion(
        L("深入：分层架构的取舍", "Deep dive: the trade-offs of the layered architecture"),
        c.qa_item(
            L("🧪 示例：一次装三个包", "🧪 Example: installing three packages"),
            L(
                "一个典型项目会装 <code>llama-index-core</code> + <code>llama-index-llms-openai</code> + "
                "<code>llama-index-embeddings-openai</code>：核心一份，其余按需各取所需。",
                "A typical project installs <code>llama-index-core</code> + <code>llama-index-llms-openai</code> + "
                "<code>llama-index-embeddings-openai</code>: one core, the rest à la carte.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "让生态可<strong>独立演进</strong>：300+ 厂商各自迭代发版，不被 core 的节奏绑死，也不会把彼此的依赖互相拖进来。",
                "It lets the ecosystem <strong>evolve independently</strong>: 300+ vendors iterate and release on their "
                "own cadence, unshackled from core's schedule and from each other's dependencies.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "命名空间约定是关键：<code>llama_index.core.*</code> 是抽象，<code>llama_index.llms.x</code> / "
                "<code>llama_index.vector_stores.y</code> 是实现，导入路径一眼可辨。",
                "The namespace convention is the key: <code>llama_index.core.*</code> is abstractions, while "
                "<code>llama_index.llms.x</code> / <code>llama_index.vector_stores.y</code> are implementations — the "
                "import path tells you which at a glance.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "单体框架（所有实现塞进一个包）安装简单，但依赖臃肿、升级互相牵制；插件式分层用多装几个小包，"
                "换来灵活与可维护。",
                "A monolith (all implementations in one package) is simpler to install but bloats dependencies and "
                "couples upgrades; the plugin-style split trades a few extra small installs for flexibility and "
                "maintainability.",
            ),
        ),
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
    + c.code(
        "# 同一套链路，换一家 LLM 只动这一块\n"
        "from llama_index.core import Settings\n\n"
        "# A) OpenAI\n"
        "from llama_index.llms.openai import OpenAI\n"
        "Settings.llm = OpenAI(model='gpt-4o-mini')\n\n"
        "# B) 换成 Anthropic：只改导入 + 这一行，其余代码原封不动\n"
        "from llama_index.llms.anthropic import Anthropic\n"
        "Settings.llm = Anthropic(model='claude-3-5-sonnet-latest')",
        caption=L("换 provider 只改一行：core 之上的代码完全不变", "Swap provider in one line: everything above core stays the same"),
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
    + d.vflow([
        (L("SimpleDirectoryReader(...).load_data()", "SimpleDirectoryReader(...).load_data()"),
         L("→ Document 列表", "→ a list of Document")),
        (L("VectorStoreIndex.from_documents(docs)", "VectorStoreIndex.from_documents(docs)"),
         L("→ Node → 向量 → 写入索引", "→ Node → vectors → stored in the index")),
        (L("index.as_query_engine()", "index.as_query_engine()"),
         L("→ 装配 检索 / 后处理 / 合成", "→ wires retrieve / post-process / synthesize")),
        (L("engine.query('…')", "engine.query('…')"),
         L("→ 检索 → 合成 → 答案 + source_nodes", "→ retrieve → synthesize → answer + source_nodes")),
    ], caption=L(
        "四行 API，每一行的产出正好喂给下一行",
        "Four API lines — each line's output is exactly the next line's input",
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
    + c.section(
        L("高层 API 只是低层管道的快捷方式", "The high-level API is just a shortcut over the low-level pipeline"),
        L(
            "那几行高层 API 并没有发明新东西，它们只是把底层管道的默认装配“一键化”。新手用一行跑通，"
            "进阶者可以拆开任意一站、替换其中的组件——同一套抽象，支持两种使用深度。",
            "Those few high-level lines invent nothing new; they merely package the low-level pipeline's default "
            "wiring into one click. Beginners get it running in a line; experts open any stop and swap its "
            "components — one set of abstractions, two depths of use.",
        ),
        d.compare2(
            (L("写入路径（做一次）", "Write path (run once)"), i18n.render(L(
                "加载 → 切块 → 向量化 → 建索引。较重但只需一次，产物是可复用的索引。",
                "Load → split → embed → index. Heavier, but one-off; the product is a reusable index.",
            ))),
            (L("查询路径（做很多次）", "Query path (run many times)"), i18n.render(L(
                "检索 → 后处理 → 合成。每次提问都走一遍，复用同一个索引，秒级返回。",
                "Retrieve → post-process → synthesize. Runs on every question, reusing the same index, in seconds.",
            ))),
            caption=L("建一次索引，问无数次", "Build the index once, query it countless times"),
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
    + c.accordion(
        L("深入：两行 API 各藏了什么", "Deep dive: what the two one-liners hide"),
        c.qa_item(
            L("🧪 示例：还是那 5 行", "🧪 Example: those same 5 lines"),
            L(
                "<code>load_data → from_documents → as_query_engine → query</code> 四步，就是一个完整 RAG 的最短写法；"
                "本书后面每一课，都是在拆开其中的某一步。",
                "<code>load_data → from_documents → as_query_engine → query</code> is the shortest complete RAG; every "
                "later lesson in this guide simply opens up one of those steps.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "快捷方式降低上手门槛，又不牺牲可定制性：默认装配开箱即用，需要时再逐站替换，二者共用同一套对象。",
                "Shortcuts lower the barrier to entry without sacrificing customizability: the default wiring works out "
                "of the box, and you can replace any stop when needed — both share the very same objects.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "<code>from_documents</code> 内部依次跑 split → embed → store，把 Document 变成带向量的 Node 存进索引；"
                "<code>query</code> 内部跑 retrieve → synthesize，把问题变成答案。",
                "<code>from_documents</code> internally runs split → embed → store, turning Documents into vector-bearing "
                "Nodes in the index; <code>query</code> internally runs retrieve → synthesize, turning a question into an "
                "answer.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "你完全可以手动逐站装配（自建 node_parser / embed_model / retriever / synthesizer），换取最大控制力；"
                "高层 API 只是把这套装配的常见默认值替你填好。",
                "You can always wire each stop by hand (your own node_parser / embed_model / retriever / synthesizer) for "
                "maximum control; the high-level API just fills in that wiring's common defaults for you.",
            ),
        ),
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
    + c.code(
        "from llama_index.core import (\n"
        "    VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage)\n\n"
        "# —— 首次：建好索引并落盘 ——\n"
        "docs = SimpleDirectoryReader('./data').load_data()\n"
        "index = VectorStoreIndex.from_documents(docs)\n"
        "index.storage_context.persist('./storage')\n\n"
        "# —— 以后：直接从磁盘加载，跳过重新建索引 ——\n"
        "ctx = StorageContext.from_defaults(persist_dir='./storage')\n"
        "index = load_index_from_storage(ctx)\n"
        "engine = index.as_query_engine()",
        caption=L("把“写一次”落盘，之后秒级复用", "Persist the “write once” to disk, then reuse it in seconds"),
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
