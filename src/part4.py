"""Part 4 (advanced): lessons 17-19. Content filled task-by-task."""
import components as c
import diagrams as d
import i18n
from i18n import L


LESSON_17 = (
    c.pipeline(None)
    + c.lead(L(
        "<strong>Settings</strong> 是全局默认配置（llm / embed_model / node_parser / chunk_size…），"
        "取代了旧的 <code>ServiceContext</code>。<strong>Prompt 模板</strong>则控制“到底怎么问 LLM”，可按领域定制语气与约束。",
        "<strong>Settings</strong> holds global defaults (llm / embed_model / node_parser / chunk_size…), replacing the "
        "old <code>ServiceContext</code>. <strong>Prompt templates</strong> control “how exactly we ask the LLM”, "
        "customizable per domain for tone and constraints.",
    ))
    + c.analogy(L(
        "Settings 像项目的<strong>默认设置面板</strong>：定一次，处处生效，单处仍可覆盖。Prompt 模板像<strong>填空式提问公式</strong>，"
        "把检索到的上下文和用户问题填进固定结构。",
        "Settings is the project's <strong>defaults panel</strong>: set once, applies everywhere, still overridable "
        "locally. A prompt template is a <strong>fill-in-the-blank question form</strong> that slots the retrieved "
        "context and the user's question into a fixed structure.",
    ))
    + c.section(
        L("Settings 常用项 + Prompt 占位符", "Common Settings + prompt placeholders"),
        c.compare_table(
            [L("项 / 占位符", "Item / placeholder"), L("含义", "Meaning")],
            [
                [L("<code>Settings.llm</code>", "<code>Settings.llm</code>"), L("默认生成模型", "default generation model")],
                [L("<code>Settings.embed_model</code>", "<code>Settings.embed_model</code>"), L("默认向量化模型", "default embedding model")],
                [L("<code>Settings.chunk_size</code>", "<code>Settings.chunk_size</code>"), L("默认切块大小", "default chunk size")],
                [L("<code>{context_str}</code> / <code>{query_str}</code>", "<code>{context_str}</code> / <code>{query_str}</code>"), L("Prompt 里填入检索上下文 / 用户问题", "where context / question are injected")],
            ],
        ),
        d.annot(
            L("PromptTemplate（问答模板）", "PromptTemplate (the QA template)"),
            [
                (L("<code>{context_str}</code>", "<code>{context_str}</code>"),
                 L("检索到的片段在此注入——答案的“依据”", "retrieved snippets are injected here — the answer's evidence")),
                (L("<code>{query_str}</code>", "<code>{query_str}</code>"),
                 L("用户问题在此注入——要回答的“题目”", "the user's question is injected here — the task to answer")),
                (L("固定指令", "Fixed instructions"),
                 L("语气、边界、“无据就说不知道”等约束写死在模板里", "tone, limits and rules like “say you don't know” live in the template")),
            ],
            caption=L(
                "Prompt 模板是一张填空卷：两个占位符到运行时才被真实内容填满",
                "A prompt template is a fill-in-the-blank form: both placeholders are filled with real content only at run time",
            ),
        ),
    )
    + c.section(
        L("全局默认 + 局部覆盖；Prompt 决定“最后一公里”", "Global defaults + local overrides; the prompt owns the “last mile”"),
        L(
            "<code>Settings</code> 给全管道一份<strong>默认值</strong>，省去到处传配置对象；但任何一处都能在构造时"
            "就地覆盖，不影响全局。检索决定“拿到哪些上下文”，<strong>Prompt</strong> 决定“拿同一份上下文怎么问”——"
            "检索结果一字不变，换一个语气、约束或输出格式的模板，答案就大不相同。这一步正是 RAG 的“最后一公里”。",
            "<code>Settings</code> hands the whole pipeline a set of <strong>defaults</strong>, sparing you from "
            "threading a config object everywhere; yet any call site can override locally at construction without "
            "touching the global. Retrieval decides “which context you get”; the <strong>prompt</strong> decides "
            "“how to ask with that same context” — with identical retrieved snippets, swapping the template's tone, "
            "constraints or output format yields a very different answer. That step is RAG's “last mile”.",
        ),
        d.compare2(
            (L("全局 Settings（基线）", "Global Settings (baseline)"), i18n.render(L(
                "一处设定，<code>llm</code> / <code>embed_model</code> / <code>chunk_size</code> 成为全管道默认，适合统一基线。",
                "Set once and <code>llm</code> / <code>embed_model</code> / <code>chunk_size</code> become pipeline-wide defaults — ideal for a uniform baseline.",
            ))),
            (L("局部覆盖（特例）", "Local override (special case)"), i18n.render(L(
                "构造某个组件时显式传参，如 <code>as_query_engine(llm=…, text_qa_template=…)</code>，只改这一处而不动全局。",
                "Pass arguments explicitly when building one component, e.g. <code>as_query_engine(llm=…, text_qa_template=…)</code> — changes this spot only, leaving the global intact.",
            ))),
            caption=L(
                "同一套 RAG：全局定基线，局部按需特例化",
                "One RAG setup: set a global baseline, then special-case locally on demand",
            ),
        ),
        d.compare2(
            (L("Prompt A · 宽松", "Prompt A · loose"), i18n.render(L(
                "模板只说“根据资料回答”。检索到的同一份上下文里其实<strong>没提保修期</strong>，"
                "宽松的措辞却纵容 LLM 顺嘴补一句<strong>“一般为一年”</strong>——看似贴心，实为编造、无出处。",
                "The template merely says “answer from the materials”. The retrieved context never actually "
                "<strong>mentions the warranty period</strong>, yet the loose wording lets the LLM blurt out "
                "<strong>“usually one year”</strong> — helpful-looking, but fabricated and unsourced.",
            ))),
            (L("Prompt B · 严格", "Prompt B · strict"), i18n.render(L(
                "模板写死“只用资料回答；未提及就说‘资料未提及’”。<strong>检索结果一字未变</strong>、"
                "问题也一样，这次 LLM <strong>老实回答“资料未提及”</strong>——不编、可追溯。",
                "The template hard-codes “answer only from the materials; if not mentioned, say ‘not in the "
                "materials’”. With the <strong>retrieved snippets byte-for-byte identical</strong> and the same "
                "question, the LLM now <strong>honestly says “not in the materials”</strong> — no fabrication, "
                "fully traceable.",
            ))),
            caption=L(
                "同一份上下文、同一个问题，只换 Prompt：答案从“编造”翻转为“老实说不知道”——这就是 RAG 的最后一公里",
                "Same context, same question, only the prompt changes: the answer flips from fabrication to an honest "
                "“I don't know” — RAG's last mile",
            ),
        ),
    )
    + c.source_ref("settings.py", "Settings", L("全局配置单例（取代 ServiceContext）", "the global config singleton (replaces ServiceContext)"))
    + c.source_ref("prompts/base.py", "PromptTemplate", L("提示词模板", "the prompt template type"))
    + c.accordion(
        L("深入：全局配置与 Prompt 模板", "Deep dive: global config and prompt templates"),
        c.qa_item(
            L("🧪 示例：设默认 + 定制模板", "🧪 Example: set defaults + a custom template"),
            L(
                "<code>Settings.llm = OpenAI(...)</code> 与 <code>Settings.embed_model = OpenAIEmbedding(...)</code> 设好全局默认；"
                "再用 <code>PromptTemplate('…{context_str}…{query_str}…')</code> 为某个 query engine 定制问答语气与约束。",
                "<code>Settings.llm = OpenAI(...)</code> and <code>Settings.embed_model = OpenAIEmbedding(...)</code> set "
                "the global defaults; then a <code>PromptTemplate('…{context_str}…{query_str}…')</code> customizes the "
                "answering tone and constraints for a given query engine.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "全局默认<strong>去样板</strong>：不必把 llm / embed_model 一路当参数传给每个组件；把 Prompt 显式成模板，"
                "则让“最后一公里”的措辞<strong>集中、可审、可版本化</strong>，而不是散落在代码里的隐式字符串。",
                "Global defaults <strong>kill boilerplate</strong>: you no longer thread llm / embed_model as arguments "
                "into every component. Making the prompt an explicit template keeps the “last-mile” wording "
                "<strong>centralized, auditable and versionable</strong> instead of buried as implicit strings.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "<code>Settings</code> 是一个进程内<strong>单例</strong>（<code>_Settings</code>）；组件构造时若没收到显式参数，"
                "就回退到它的字段。问答模板（<code>text_qa_template</code>）最终流向<strong>响应合成器</strong>，"
                "在合成阶段用检索到的上下文填满占位符，再交给 LLM。",
                "<code>Settings</code> is an in-process <strong>singleton</strong> (<code>_Settings</code>); when a "
                "component is built without explicit arguments, it falls back to these fields. The QA template "
                "(<code>text_qa_template</code>) ultimately flows into the <strong>response synthesizer</strong>, which "
                "fills the placeholders with retrieved context at synthesis time before calling the LLM.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "想要全局一致就用 <code>Settings</code>；只想在<strong>某一处</strong>用不同模型或模板，就在构造时"
                "<strong>局部传参</strong>（如 <code>as_query_engine(llm=…, text_qa_template=…)</code>），覆盖全局而不污染其它链路。",
                "Use <code>Settings</code> for global consistency; when only <strong>one spot</strong> needs a different "
                "model or template, <strong>pass it locally</strong> at construction (e.g. "
                "<code>as_query_engine(llm=…, text_qa_template=…)</code>), overriding the global without polluting other paths.",
            ),
        ),
    )
    + c.code(
        "from llama_index.core import Settings, PromptTemplate\n"
        "from llama_index.llms.openai import OpenAI\n\n"
        "Settings.llm = OpenAI(model='gpt-4o-mini')   # 全局默认，一处生效\n"
        "Settings.chunk_size = 512\n\n"
        "qa = PromptTemplate(\n"
        "    '只根据下面的上下文回答，未提及就说不知道，不要编造。\\n'\n"
        "    '上下文:\\n{context_str}\\n问题: {query_str}\\n答案: '\n"
        ")\n"
        "engine = index.as_query_engine(text_qa_template=qa)   # 定制问答 Prompt\n"
        "print(engine.query('退款政策？'))",
        caption=L("全局配一次 + 局部定制 Prompt", "configure globally + customize the prompt locally"),
    )
    + c.code(
        "from llama_index.core import PromptTemplate\n"
        "from llama_index.llms.openai import OpenAI\n\n"
        "# 全局 Settings 保持不变；只在这个 query engine 上局部覆盖\n"
        "strict = PromptTemplate(\n"
        "    '只依据下面的上下文回答；若上下文未提及，请回答“资料中未提及”。\\n'\n"
        "    '上下文:\\n{context_str}\\n问题: {query_str}\\n答案: '\n"
        ")\n"
        "engine = index.as_query_engine(\n"
        "    llm=OpenAI(model='gpt-4o', temperature=0),   # 这一处换更强的模型\n"
        "    text_qa_template=strict,                     # 这一处换更严格的模板\n"
        ")\n"
        "print(engine.query('保修期是多久？'))",
        caption=L("局部覆盖：换掉这一处的 llm 与模板，全局 Settings 原封不动", "Local override: swap this engine's llm and template; global Settings untouched"),
    )
    + c.key_points([
        L("<code>Settings</code> 取代 <code>ServiceContext</code>，集中管理默认 llm/embed/切块等。",
          "<code>Settings</code> replaces <code>ServiceContext</code>, centralizing default llm/embed/chunking."),
        L("Prompt 模板用 <code>{context_str}</code> / <code>{query_str}</code> 注入上下文与问题。",
          "Prompt templates inject context and question via <code>{context_str}</code> / <code>{query_str}</code>."),
        L("全局默认 + 局部覆盖：既省事又灵活。",
          "Global defaults + local overrides: convenient yet flexible."),
    ])
    + c.design_highlight(L(
        "“全局 Settings + 局部覆盖”避免了到处传配置对象的样板；而把 Prompt 显式成模板，让 RAG 的“最后一公里语气与约束”可控可审。",
        "“Global Settings + local overrides” kills the boilerplate of threading a config object everywhere; making the "
        "prompt an explicit template keeps RAG's “last-mile tone and constraints” controllable and auditable.",
    ))
)
LESSON_18 = (
    c.pipeline("retrieve")
    + c.lead(L(
        "基础 top-k 不够用时，进阶检索登场：<strong>融合多查询</strong>（QueryFusionRetriever）、"
        "<strong>自动合并相邻块</strong>（AutoMergingRetriever）、<strong>递归</strong>（RecursiveRetriever）、"
        "<strong>按问题路由到不同库</strong>（RouterRetriever）。它们都实现同一个 BaseRetriever 接口。",
        "When plain top-k isn't enough, advanced retrieval steps in: <strong>fuse multiple queries</strong> "
        "(QueryFusionRetriever), <strong>merge adjacent chunks</strong> (AutoMergingRetriever), <strong>recurse</strong> "
        "(RecursiveRetriever), and <strong>route by question</strong> (RouterRetriever). All implement the same "
        "BaseRetriever interface.",
    ))
    + d.flow([
        ("q", L("一个问题", "One question")),
        ("rewrite", L("改写成多版", "Rephrase to N"), L("LLM 生成 n-1 个", "LLM writes n-1 more")),
        ("retrieve", L("各自检索", "Retrieve each"), L("每版取 top-k", "top-k per variant")),
        ("fuse", L("倒数排名融合", "Reciprocal rerank"), L("跨多个排名累加", "summed across rankings")),
        ("merge", L("合并结果", "Merged set"), L("去重后的统一列表", "one deduped list")),
    ], caption=L(
        "Query Fusion：一题多问、分别检索，再用 reciprocal rerank 融合成一份结果",
        "Query Fusion: ask one question many ways, retrieve each, then reciprocal-rerank into a single result set",
    ))
    + c.analogy(L(
        "不只问一次、不只取一处：<strong>多角度改写再合并</strong>、把碎片<strong>拼回完整段落</strong>、"
        "按问题<strong>选对资料库</strong>。",
        "Don't ask once or look in one place: <strong>rephrase from several angles and merge</strong>, <strong>stitch "
        "fragments back into a passage</strong>, and <strong>pick the right corpus</strong> per question.",
    ))
    + c.section(
        L("基础 top-k 的三类短板，进阶检索逐一补齐", "Top-k's three weak spots — advanced retrieval patches each"),
        L(
            "把这些进阶检索当成一堆零散“高级技巧”去记，很容易迷失。换个视角：它们都在补朴素 top-k 相似度检索的"
            "<strong>三类典型短板</strong>——<strong>召回不全</strong>（换个问法本能命中的内容被漏掉）、"
            "<strong>命中碎片</strong>（块切得太碎，单个 Node 只剩半句上下文）、<strong>多库分流</strong>"
            "（不同问题其实该查不同索引）。看清这三道缺口，下面四种检索器就各有归属——其中“命中碎片”有"
            "横向合并、纵向递归两种补法；而且它们都实现同一个 <code>BaseRetriever</code>，可即插即换、互相嵌套。",
            "Memorizing advanced retrieval as a pile of scattered “tricks” gets you lost. Flip the view: they all "
            "patch plain top-k's <strong>three classic weak spots</strong> — <strong>missed recall</strong> (a "
            "different phrasing would have hit, but it's dropped), <strong>fragmented hits</strong> (chunks so small "
            "a single Node holds half a thought), and <strong>multiple corpora</strong> (different questions belong "
            "to different indexes). Name those three gaps and the four retrievers below each find their place — "
            "“fragmented hits” gets two cures, merging sideways and recursing down — and since all implement one "
            "<code>BaseRetriever</code>, you swap or nest them freely.",
        ),
        d.grid(
            [L("基础 top-k 的短板", "Top-k's weak spot"), L("进阶检索器", "Advanced retriever"), L("怎么补", "How it patches")],
            [
                [L("召回不全", "Missed recall"),
                 L("<code>QueryFusionRetriever</code>", "<code>QueryFusionRetriever</code>"),
                 L("一题多版改写再融合，覆盖更多说法", "multi-rephrase then fuse to cover more phrasings")],
                [L("命中碎片", "Fragmented hits"),
                 L("<code>AutoMergingRetriever</code>", "<code>AutoMergingRetriever</code>"),
                 L("相邻子块自动合并回父块", "merge adjacent child chunks back into the parent")],
                [L("命中碎片", "Fragmented hits"),
                 L("<code>RecursiveRetriever</code>", "<code>RecursiveRetriever</code>"),
                 L("从摘要/索引节点递归到完整原文", "recurse from summary/index nodes to the full source")],
                [L("多库分流", "Multiple corpora"),
                 L("<code>RouterRetriever</code>", "<code>RouterRetriever</code>"),
                 L("由 LLM 选择该查哪个索引/工具", "an LLM picks which index/tool to query")],
            ],
            caption=L(
                "三类短板组织起四种检索器：“命中碎片”有合并与递归两解，其余各对一招——接口统一，可单用也可叠加",
                "Three weak spots organize four retrievers: “fragmented hits” has two cures (merge, recurse), the rest map one-to-one — one interface, used alone or stacked",
            ),
        ),
    )
    + c.source_ref("retrievers/fusion_retriever.py", "QueryFusionRetriever", L("多查询融合（含 reciprocal rerank）", "multi-query fusion (with reciprocal rerank)"))
    + c.source_ref("retrievers/auto_merging_retriever.py", "AutoMergingRetriever", L("相邻块自动合并", "auto-merging adjacent chunks"))
    + c.accordion(
        L("深入：融合检索与可插拔接口", "Deep dive: fusion retrieval and the pluggable interface"),
        c.qa_item(
            L("🧪 示例：一题改写成 4 版", "🧪 Example: rephrase one question into 4"),
            L(
                "<code>QueryFusionRetriever(retrievers=[base], num_queries=4)</code>：原问题加上 LLM 生成的 3 个改写"
                "各自检索，再用 reciprocal rerank 融合成一份去重结果，召回通常明显高于单版 top-k。",
                "<code>QueryFusionRetriever(retrievers=[base], num_queries=4)</code>: the original question plus 3 "
                "LLM-generated rewrites each retrieve, then reciprocal rerank fuses them into one deduped result set — "
                "recall usually beats single-query top-k by a clear margin.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "所有检索器都实现同一个 <code>BaseRetriever</code>，统一返回 <code>list[NodeWithScore]</code>，"
                "于是它们能<strong>互相嵌套、随意替换</strong>，并直接塞进任何 QueryEngine——上层完全无感。",
                "Every retriever implements the same <code>BaseRetriever</code> and returns "
                "<code>list[NodeWithScore]</code>, so they <strong>nest and swap freely</strong> and drop straight into "
                "any QueryEngine — the layer above never notices.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "<code>num_queries=n</code> 让 LLM 额外生成 <strong>n-1</strong> 个改写（原问题也算一版）；"
                "融合方式由 <code>FUSION_MODES</code> 决定，<strong>默认 <code>simple</code></strong>，常显式设 "
                "<code>reciprocal_rerank</code>（RRF）——按每条结果在多个排名中的倒数位次累加打分，再统一排序。",
                "<code>num_queries=n</code> makes the LLM generate <strong>n-1</strong> extra rewrites (the original "
                "counts as one); fusion is governed by <code>FUSION_MODES</code> (<strong>default <code>simple</code>"
                "</strong>), and you commonly set <code>reciprocal_rerank</code> (RRF) — it sums each result's reciprocal "
                "rank across the several rankings, then sorts once.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "不是每个问题都靠“多问几遍”：碎片化严重就用 <code>AutoMergingRetriever</code> 合并回父块；"
                "知识有层级或引用就用 <code>RecursiveRetriever</code> 跟随引用到原文；面对多个索引就用 "
                "<code>RouterRetriever</code> 让 LLM 选库。它们可单用，也能叠在 fusion 之上。",
                "Not every problem yields to “asking more times”: for heavy fragmentation use "
                "<code>AutoMergingRetriever</code> to merge back into parents; for hierarchical or cited knowledge use "
                "<code>RecursiveRetriever</code> to follow references to the source; for multiple indexes use "
                "<code>RouterRetriever</code> to let an LLM pick the corpus. Each works alone or stacked atop fusion.",
            ),
        ),
    )
    + c.code(
        "from llama_index.core.retrievers import QueryFusionRetriever\n\n"
        "# 把一个问题改写成多版、分别检索，再用 reciprocal rerank 融合\n"
        "fusion = QueryFusionRetriever(\n"
        "    retrievers=[index.as_retriever(similarity_top_k=5)],\n"
        "    num_queries=4,\n"
        "    mode='reciprocal_rerank',\n"
        ")\n"
        "nodes = fusion.retrieve('退款和换货政策有何不同？')\n"
        "print(len(nodes))",
        caption=L("进阶检索器仍是 BaseRetriever，可直接塞进 QueryEngine", "still a BaseRetriever — drops into any QueryEngine"),
    )
    + c.code(
        "from llama_index.core.retrievers import AutoMergingRetriever\n"
        "from llama_index.core.node_parser import HierarchicalNodeParser\n\n"
        "# 层级切块：同一段文本切成大/中/小三层父子块\n"
        "parser = HierarchicalNodeParser.from_defaults()\n"
        "nodes = parser.get_nodes_from_documents(docs)\n"
        "# ...把叶子块建进 index，得到一个基础 base_retriever...\n"
        "retriever = AutoMergingRetriever(\n"
        "    base_retriever,                  # 任意 BaseRetriever（这里检索叶子块）\n"
        "    storage_context=storage_context,\n"
        ")\n"
        "# 命中同一父块的多个叶子，会被自动合并成更完整的父块\n"
        "merged = retriever.retrieve('保修条款有哪些例外情况？')\n"
        "print(len(merged))",
        caption=L("另一种思路：AutoMerging 把命中的碎片拼回完整父块", "A different angle: AutoMerging stitches hit fragments back into a whole parent"),
    )
    + c.key_points([
        L("进阶检索针对“召回不全/碎片化/多库”等基础 top-k 的短板。",
          "Advanced retrieval targets top-k's weak spots: missed recall, fragmentation, multiple corpora."),
        L("它们都实现 <code>BaseRetriever</code>，可<strong>无缝</strong>接入现有 QueryEngine。",
          "All implement <code>BaseRetriever</code>, so they <strong>drop into</strong> an existing QueryEngine."),
        L("Fusion 用改写+融合提升召回；AutoMerging 用关系合并提升上下文完整度。",
          "Fusion lifts recall via rephrase+merge; AutoMerging lifts context completeness via relationships."),
    ])
    + c.design_highlight(L(
        "进阶检索没有免费的午餐：fusion 多跑几轮检索来提召回，但更慢更贵；auto-merging 合并父块补上下文，"
        "却可能引入冗余。每一种都是在用更多计算换更好结果。",
        "Advanced retrieval is no free lunch: fusion runs extra retrieval passes to lift recall but costs more and "
        "runs slower; auto-merging merges parent blocks to restore context but can add redundancy. Each trades more "
        "compute for better results.",
    ))
)
LESSON_19 = (
    c.pipeline(None)
    + c.lead(L(
        "RAG 到底好不好，不能只凭“感觉还行”。<strong>评估器（Evaluator）</strong>把答案质量"
        "<strong>量化成分数</strong>，让“好”与“坏”有据可比——下面这张表把核心的几把尺子摆在一起。",
        "Is the RAG any good? “Feels fine” isn't an answer. <strong>Evaluators</strong> <strong>quantify</strong> "
        "answer quality into scores so “good” and “bad” become comparable — the grid below lays out the core rulers.",
    ))
    + d.grid(
        [L("评估器", "Evaluator"), L("衡量什么", "Measures"), L("需要的输入", "Needs")],
        [
            [L("<code>FaithfulnessEvaluator</code>", "<code>FaithfulnessEvaluator</code>"),
             L("答案是否被检索上下文支撑（防幻觉）", "is the answer grounded in retrieved context (anti-hallucination)"),
             L("答案 + source_nodes", "answer + source_nodes")],
            [L("<code>RelevancyEvaluator</code>", "<code>RelevancyEvaluator</code>"),
             L("检索与答案是否切合该问题", "are the context and answer on-topic for the query"),
             L("问题 + 答案 + source_nodes", "query + answer + source_nodes")],
            [L("<code>CorrectnessEvaluator</code>", "<code>CorrectnessEvaluator</code>"),
             L("对照参考答案是否正确（1–5 分）", "is the answer correct vs a reference (scored 1–5)"),
             L("问题 + 答案 + 参考答案", "query + answer + reference answer")],
        ],
        caption=L(
            "三把尺子量不同侧面：忠实看“有没有据”，相关看“切不切题”，正确看“对不对”",
            "Three rulers, three facets: faithfulness checks grounding, relevancy checks on-topic, correctness checks rightness",
        ),
    )
    + c.analogy(L(
        "评估器就像给作文判卷的<strong>老师</strong>：不是一句“感觉不错”，而是拿固定的几把尺子逐项打分——"
        "分数能横向比较、也能复算。",
        "An evaluator is like a <strong>teacher grading essays</strong>: not a vague “seems good” but scoring against "
        "a fixed set of rulers — numbers you can compare across runs and recompute.",
    ))
    + c.section(
        L("把调优变成可度量的闭环", "Turn tuning into a measurable loop"),
        L(
            "没有评估，调 RAG 就是“凭感觉”：改了切块、换了检索、调了 Prompt，到底变好还是变坏，全靠主观印象。"
            "评估把它变成一个<strong>闭环</strong>：每次改动后，用<strong>同一套问题和指标</strong>跑一遍，"
            "对比分数再决定保留还是回退。于是每一步优化都有据可依，也能挡住“修好一个、悄悄弄坏一批”的回归。"
            "下面用一组真实感的分数，看这个闭环跑起来是什么样。",
            "Without evaluation, tuning RAG is “by feel”: after changing chunking, retrieval or the prompt, whether it "
            "improved is a subjective impression. Evaluation turns it into a <strong>closed loop</strong>: after each "
            "change, run the <strong>same questions and metrics</strong>, compare the scores, then decide to keep or "
            "revert. Every optimization becomes evidence-based, and you catch the “fix one, silently break a batch” "
            "regressions. The numbers below show one turn of that loop in action.",
        ),
        d.flow([
            ("baseline", L("基线", "Baseline"), L("Faithfulness 0.82", "Faithfulness 0.82")),
            ("change", L("改一处", "Change one"), L("chunk_size 512 → 1024", "chunk_size 512 → 1024")),
            ("retest", L("重测", "Re-measure"), L("同一批问题", "same question set")),
            ("compare", L("对比", "Compare"), L("0.82 → 0.71，↓ 变差", "0.82 → 0.71, worse ↓")),
            ("decide", L("决定", "Decide"), L("回退，守住基线", "revert, keep the baseline")),
        ], caption=L(
            "一次真实的闭环：基线 0.82 → 把 chunk_size 改大反降到 0.71 → 回退；倘若改成加一道 rerank 升到 0.91，就予以保留——分数让去留有据，再回到第一步",
            "One real turn of the loop: baseline 0.82 → enlarging chunk_size drops it to 0.71 → revert; had a rerank lifted it to 0.91 you'd keep it — the score makes the call, then back to step one",
        )),
    )
    + c.source_ref("evaluation/faithfulness.py", "FaithfulnessEvaluator", L("忠实度评估（防幻觉）", "faithfulness (anti-hallucination)"))
    + c.source_ref("evaluation/base.py", "BaseEvaluator.evaluate_response", L("统一评估入口", "the unified evaluation entry"))
    + c.accordion(
        L("深入：评估器怎么打分", "Deep dive: how evaluators score"),
        c.qa_item(
            L("🧪 示例：评一个回答", "🧪 Example: grade one answer"),
            L(
                "<code>FaithfulnessEvaluator().evaluate_response(response=resp)</code> 直接吃 QueryEngine 的返回"
                "（已含 <code>source_nodes</code>）；结果里 <code>passing</code> 表示是否“有据可依”，<code>score</code> 给出分值。",
                "<code>FaithfulnessEvaluator().evaluate_response(response=resp)</code> consumes the QueryEngine "
                "response directly (it already carries <code>source_nodes</code>); the result's <code>passing</code> "
                "says whether it is “grounded”, and <code>score</code> gives the value.",
            ),
        ),
        c.qa_item(
            L("❓ 为什么这么设计", "❓ Why designed this way"),
            L(
                "把质量<strong>量化</strong>，调优才能<strong>回归测试</strong>：同一套问题在每次改动后复跑，"
                "分数升降一目了然，避免“改好一个、悄悄弄坏一批”。",
                "<strong>Quantifying</strong> quality makes tuning <strong>regression-testable</strong>: rerun the same "
                "question set after each change and the score moves are obvious, so you don't “fix one and silently "
                "break a batch”.",
            ),
        ),
        c.qa_item(
            L("⚙️ 内部怎么跑", "⚙️ How it runs inside"),
            L(
                "多数评估器是 <strong>LLM-as-judge</strong>：把问题、答案、上下文（或参考答案）塞进一个评判 Prompt，"
                "让 LLM 给判断。<code>Faithfulness</code> / <code>Relevancy</code> 多为<strong>二值</strong>"
                "（<code>passing</code> 是/否），<code>Correctness</code> 则给 <strong>1–5 分</strong>的 <code>score</code>。",
                "Most evaluators are <strong>LLM-as-judge</strong>: the question, answer and context (or reference) go "
                "into a judging prompt and an LLM rules on it. <code>Faithfulness</code> / <code>Relevancy</code> are "
                "usually <strong>binary</strong> (<code>passing</code> yes/no), while <code>Correctness</code> returns "
                "a <strong>1–5</strong> <code>score</code>.",
            ),
        ),
        c.qa_item(
            L("🔀 替代方案", "🔀 Alternatives"),
            L(
                "<strong>人工评估</strong>最准但慢且贵，适合做小规模“金标准”；<strong>LLM 评估</strong>快且可自动化，"
                "适合每次改动的回归。实践中两者结合：维护一个固定的<strong>回归问题集</strong>，平时用 LLM 评，"
                "定期抽样人评来校准。",
                "<strong>Human evaluation</strong> is most accurate but slow and costly — good for a small “gold "
                "standard”; <strong>LLM evaluation</strong> is fast and automatable — good for per-change regressions. "
                "In practice combine both: keep a fixed <strong>regression question set</strong>, judge with an LLM "
                "routinely, and sample human checks periodically to calibrate.",
            ),
        ),
    )
    + c.code(
        "from llama_index.core.evaluation import FaithfulnessEvaluator\n\n"
        "resp = index.as_query_engine().query('退款政策是什么？')\n"
        "ev = FaithfulnessEvaluator()\n"
        "result = ev.evaluate_response(response=resp)\n"
        "print(result.passing, result.score)   # 答案是否有据可依",
        caption=L("把“感觉还行”变成“可度量”", "turn “feels fine” into “measurable”"),
    )
    + c.code(
        "from llama_index.core.evaluation import (\n"
        "    FaithfulnessEvaluator, RelevancyEvaluator, BatchEvalRunner)\n\n"
        "# 用一小批问题跑回归：每题同时算忠实度与相关性\n"
        "runner = BatchEvalRunner(\n"
        "    {'faith': FaithfulnessEvaluator(), 'rel': RelevancyEvaluator()},\n"
        "    workers=4,\n"
        ")\n"
        "questions = ['退款政策是什么？', '保修期多久？', '支持哪些支付方式？']\n"
        "results = await runner.aevaluate_queries(\n"
        "    index.as_query_engine(), queries=questions)\n\n"
        "# 汇总通过率，作为本次改动的基线指标\n"
        "passed = sum(bool(r.passing) for r in results['faith'])\n"
        "print(f'faithfulness: {passed}/{len(questions)} passed')",
        caption=L("用 BatchEvalRunner 跑一小批问题，得到可对比的基线", "Run a small batch with BatchEvalRunner for a comparable baseline"),
    )
    + c.key_points([
        L("三类评估：<strong>忠实</strong>（防幻觉）、<strong>相关</strong>（切题）、<strong>正确</strong>（对参考）。",
          "Three checks: <strong>faithful</strong> (anti-hallucination), <strong>relevant</strong> (on-topic), <strong>correct</strong> (vs reference)."),
        L("<code>evaluate_response</code> 直接吃 QueryEngine 的返回（含 source_nodes）。",
          "<code>evaluate_response</code> consumes the QueryEngine's response directly (with source_nodes)."),
        L("评估通常由一个 LLM 充当“裁判”。",
          "Evaluation is usually done by an LLM acting as judge."),
    ])
    + c.design_highlight(L(
        "评估把 RAG 调优从“凭感觉”变成“<strong>可度量的闭环</strong>”：改切块、换检索、调 Prompt 后，用同一套指标对比，才知道是真变好了。",
        "Evaluation turns RAG tuning from gut feeling into a <strong>measurable loop</strong>: after changing chunking, "
        "retrieval or prompts, compare on the same metrics to know it actually improved.",
    ))
)
