"""Part 4 (advanced): lessons 17-19. Content filled task-by-task."""
import components as c
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
    )
    + c.source_ref("settings.py", "Settings", L("全局配置单例（取代 ServiceContext）", "the global config singleton (replaces ServiceContext)"))
    + c.source_ref("prompts/base.py", "PromptTemplate", L("提示词模板", "the prompt template type"))
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
    + c.analogy(L(
        "不只问一次、不只取一处：<strong>多角度改写再合并</strong>、把碎片<strong>拼回完整段落</strong>、"
        "按问题<strong>选对资料库</strong>。",
        "Don't ask once or look in one place: <strong>rephrase from several angles and merge</strong>, <strong>stitch "
        "fragments back into a passage</strong>, and <strong>pick the right corpus</strong> per question.",
    ))
    + c.section(
        L("四种进阶检索器", "Four advanced retrievers"),
        c.compare_table(
            [L("检索器", "Retriever"), L("解决的问题", "What it solves")],
            [
                [L("QueryFusionRetriever", "QueryFusionRetriever"), L("一问改写多版、结果融合排序", "multi-rephrase + fused ranking")],
                [L("AutoMergingRetriever", "AutoMergingRetriever"), L("命中多个小块时合并成父块", "merge small hits into a parent block")],
                [L("RecursiveRetriever", "RecursiveRetriever"), L("从摘要/引用跳转到原文", "hop from summaries/refs to source")],
                [L("RouterRetriever", "RouterRetriever"), L("按问题选择不同索引/工具", "route to different indexes/tools")],
            ],
        ),
    )
    + c.source_ref("retrievers/fusion_retriever.py", "QueryFusionRetriever", L("多查询融合（含 reciprocal rerank）", "multi-query fusion (with reciprocal rerank)"))
    + c.source_ref("retrievers/auto_merging_retriever.py", "AutoMergingRetriever", L("相邻块自动合并", "auto-merging adjacent chunks"))
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
    + c.key_points([
        L("进阶检索针对“召回不全/碎片化/多库”等基础 top-k 的短板。",
          "Advanced retrieval targets top-k's weak spots: missed recall, fragmentation, multiple corpora."),
        L("它们都实现 <code>BaseRetriever</code>，可<strong>无缝</strong>接入现有 QueryEngine。",
          "All implement <code>BaseRetriever</code>, so they <strong>drop into</strong> an existing QueryEngine."),
        L("Fusion 用改写+融合提升召回；AutoMerging 用关系合并提升上下文完整度。",
          "Fusion lifts recall via rephrase+merge; AutoMerging lifts context completeness via relationships."),
    ])
    + c.design_highlight(L(
        "因为“检索”早就被抽象成统一接口，这些聪明策略才能像<strong>乐高</strong>一样替换基础检索器，而 QueryEngine 完全无感。",
        "Because “retrieval” was abstracted to one interface early, these clever strategies swap in like <strong>Lego</strong> "
        "for the basic retriever — the QueryEngine never notices.",
    ))
)
LESSON_19 = (
    c.pipeline(None)
    + c.lead(L(
        "RAG 到底好不好？用<strong>评估器</strong>量化：<strong>忠实度</strong>（Faithfulness：答案有没有被检索内容支撑）、"
        "<strong>相关性</strong>（Relevancy：检索与答案是否切题）、<strong>正确性</strong>（Correctness：对照参考答案打分）。",
        "Is the RAG any good? Quantify it with <strong>evaluators</strong>: <strong>Faithfulness</strong> (is the answer "
        "grounded in retrieved content?), <strong>Relevancy</strong> (are retrieval and answer on-topic?), and "
        "<strong>Correctness</strong> (score against a reference answer).",
    ))
    + c.analogy(L(
        "给答案打分的<strong>三把尺子</strong>：有没有瞎编（忠实）、答没答到点（相关）、对不对（正确）。",
        "Three rulers for grading an answer: did it make things up (faithful), did it stay on point (relevant), and is "
        "it right (correct).",
    ))
    + c.section(
        L("三类评估器", "Three evaluators"),
        c.compare_table(
            [L("评估器", "Evaluator"), L("回答的问题", "Question it answers")],
            [
                [L("FaithfulnessEvaluator", "FaithfulnessEvaluator"), L("答案是否被检索到的上下文支撑？", "is the answer supported by retrieved context?")],
                [L("RelevancyEvaluator", "RelevancyEvaluator"), L("检索 + 答案是否切题？", "are retrieval + answer relevant?")],
                [L("CorrectnessEvaluator", "CorrectnessEvaluator"), L("对照参考答案对不对？", "is it correct vs a reference?")],
            ],
        ),
    )
    + c.source_ref("evaluation/faithfulness.py", "FaithfulnessEvaluator", L("忠实度评估（防幻觉）", "faithfulness (anti-hallucination)"))
    + c.source_ref("evaluation/base.py", "BaseEvaluator.evaluate_response", L("统一评估入口", "the unified evaluation entry"))
    + c.code(
        "from llama_index.core.evaluation import FaithfulnessEvaluator\n\n"
        "resp = index.as_query_engine().query('退款政策是什么？')\n"
        "ev = FaithfulnessEvaluator()\n"
        "result = ev.evaluate_response(response=resp)\n"
        "print(result.passing, result.score)   # 答案是否有据可依",
        caption=L("把“感觉还行”变成“可度量”", "turn “feels fine” into “measurable”"),
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
