"""Per-lesson "interviewer" questions (面试官提问).

Realistic, interview-style drills — each gives a scenario and probes design,
rationale ("why / how did you arrive at it") and evaluation ("how do you
measure it works"). Answers lead with a bold "🔑 重点" key-point and may carry
an optional diagram via the ``fig`` key (any ``diagrams`` primitive).

Schema, keyed by lesson filename::

    "NN-file.html": [
        {"q": L("场景 + 追问…", "scenario + probes…"),
         "answer": L("🔑 重点：… <strong>关键</strong> …", "🔑 Key: …"),
         "fig": d.flow(...)},      # optional
        ...
    ]

``render(fname)`` in ``quizzes.py`` pulls from ``INTERVIEW.get(fname)``. Keep
2–3 deep questions per lesson; escape literal ``&`` as ``&amp;`` (text is raw
HTML, not inside ``<pre>``).
"""

import diagrams as d
from i18n import L


INTERVIEW = {
    "01-what-is-llamaindex.html": [
        {"q": L(
            "你要给公司 1 万份内部文档做问答助手。为什么选 RAG，而不是直接微调一个模型、或把文档全塞进长上下文？"
            "你当初怎么权衡的？上线后又怎么<strong>用数据证明</strong>这条路是对的？",
            "You're building a Q&amp;A assistant over 10,000 internal docs. Why RAG rather than fine-tuning a model or "
            "stuffing everything into long context? How did you weigh it — and after launch, how would you "
            "<strong>prove with data</strong> it was the right call?"),
         "answer": L(
            "🔑 <strong>重点：RAG 把知识外置成可检索、可更新、可溯源的索引</strong>，是“大 / 私有 / 时效 / 要出处”场景的默认解。"
            "① 不微调：微调把知识焊进权重，更新一次要重训、贵且难溯源，更适合改<strong>风格</strong>而非加<strong>事实</strong>；"
            "② 不长上下文全塞：1 万份装不进窗口，贵且会“迷失在中间”；"
            "③ 怎么验证：建一组带标准答案的问题，对比 RAG vs 纯 LLM 基线的 <strong>Faithfulness（答案是否忠于检索）</strong>与<strong>命中率</strong>，用数字而非感觉下结论。",
            "🔑 <strong>Key: RAG externalizes knowledge into a searchable, refreshable, citable index</strong> — the default for "
            "large / private / time-sensitive knowledge that needs sources. (1) Not fine-tuning: it welds knowledge into "
            "weights, costly to update and hard to cite — better for <strong>style</strong> than <strong>facts</strong>; "
            "(2) not long-context dumping: 10k docs don't fit, it's expensive and 'lost in the middle'; "
            "(3) validate by comparing RAG vs a plain-LLM baseline on a labeled question set — <strong>Faithfulness</strong> "
            "and hit-rate — concluding from numbers, not vibes."),
         "fig": d.grid(
            [L("方案", "Approach"), L("更新知识", "Updating knowledge"), L("可溯源", "Citable"), L("适合", "Best for")],
            [
                [L("微调 Fine-tune", "Fine-tune"), L("重训，贵", "retrain, costly"), L("难", "hard"), L("改风格/格式", "style/format")],
                [L("长上下文 Long-ctx", "Long context"), L("每次全塞", "stuff every call"), L("部分", "partial"), L("小而短的语料", "tiny/short corpus")],
                [L("RAG", "RAG"), L("重建索引", "re-index"), L("是", "yes"), L("大/私有/时效", "large/private/fresh")],
            ],
            caption=L("三条路线的权衡：RAG 在“可更新 + 可溯源 + 规模”上取胜", "Trade-offs: RAG wins on refreshable + citable + scale")),
        },
        {"q": L(
            "用户反馈助手“还是会编”。在 RAG 框架下，你会<strong>按什么顺序</strong>排查？每一步怎么<strong>用数据验证</strong>而不是猜？",
            "Users say the assistant 'still makes things up'. In what <strong>order</strong> would you investigate, and how "
            "would you <strong>verify each step with data</strong> rather than guess?"),
         "answer": L(
            "🔑 <strong>重点：先看 <code>source_nodes</code>，把问题定位到“检索”还是“生成”，再分而治之。</strong>"
            "① 检索：<code>retrieve()</code> 有没有命中正确依据？没有→召回问题（调 top_k / 换 embedding / 改切块），用<strong>命中率</strong>量化；"
            "② 生成：依据对但答案越界→收紧 prompt（只依据资料、给出处），用 <strong>Faithfulness 评估</strong>对比改前改后；"
            "③ 建一个小<strong>回归集</strong>，每次改动重测，挡住“修好一个、悄悄弄坏一批”。",
            "🔑 <strong>Key: look at <code>source_nodes</code> first to localize whether it's retrieval or generation, then "
            "divide and conquer.</strong> (1) Retrieval: did <code>retrieve()</code> surface the right evidence? If not → "
            "recall problem (tune top_k / swap embedding / re-chunk), quantified by <strong>hit-rate</strong>; "
            "(2) generation: right evidence but the answer over-reaches → tighten the prompt (cite-only), compare before/after "
            "with a <strong>Faithfulness evaluator</strong>; (3) keep a small <strong>regression set</strong> and re-test every "
            "change to block 'fix one, silently break many'."),
         "fig": d.flow([
            ("src", L("看 source_nodes", "check source_nodes")),
            ("ret", L("检索命中对吗？", "retrieval right?"), L("否→调召回", "no → fix recall")),
            ("gen", L("生成越界吗？", "generation over-reach?"), L("是→收紧 prompt", "yes → tighten prompt")),
            ("eval", L("回归集复测", "re-test on regression set")),
         ], active="src", caption=L("先定位再修：每一步都用指标验证", "Localize, then fix — verify each step with a metric")),
        },
    ],
    "02-architecture.html": [
        {"q": L(
            "你要给团队定规范：什么时候用现成集成包、什么时候自己封装。core/集成分层怎么帮你做这个决定？"
            "你又怎么<strong>验证</strong>“换厂商真的低成本”？",
            "You're setting a team rule: when to use an off-the-shelf integration vs roll your own. How does the "
            "core/integration split inform that, and how would you <strong>verify</strong> that 'swapping vendors is "
            "really cheap'?"),
         "answer": L(
            "🔑 <strong>重点：路径含 <code>core</code>=抽象，不含=集成实现；优先用现成集成，只有专有需求才自封装。</strong>"
            "现成集成久经测试、独立发版；自写要实现 core 的接口。验证：写一个“换 LLM 只改 <code>Settings.llm</code> 一行”的冒烟测试，"
            "跑同一组问题看链路不崩——但注意<strong>换 Embedding 要重建索引</strong>，那一项并非零成本。",
            "🔑 <strong>Key: a path with <code>core</code> = abstraction, without = integration; prefer existing "
            "integrations, roll your own only for proprietary needs.</strong> Existing ones are battle-tested and ship "
            "independently; custom ones implement the core interface. Verify with a smoke test that swaps the LLM via one "
            "<code>Settings.llm</code> line and re-runs a question set — but note <strong>swapping the embedding forces a "
            "re-index</strong>, which isn't free."),
        },
        {"q": L(
            "本地用 Ollama 跑通的 RAG 要上线换 OpenAI。你的迁移清单是什么？<strong>哪一步最容易出事</strong>，怎么提前验证？",
            "A local Ollama RAG goes live on OpenAI. What's your migration checklist, <strong>which step is most "
            "dangerous</strong>, and how do you de-risk it ahead of time?"),
         "answer": L(
            "🔑 <strong>重点：换 LLM 是一行；最容易出事的是换 Embedding——必须重建索引。</strong>"
            "迁移清单：改 <code>Settings.llm</code>；retriever / index / query engine 不动；若也换 embedding，则在 staging "
            "<strong>用新模型重建一遍索引</strong>、跑回归集对比分数，确认召回没退化再切流量——直接热切会让旧向量与新查询坐标系不可比。",
            "🔑 <strong>Key: swapping the LLM is one line; the dangerous step is swapping the embedding — it forces a "
            "re-index.</strong> Checklist: change <code>Settings.llm</code>; leave retriever / index / query engine; if the "
            "embedding also changes, <strong>rebuild the index with the new model in staging</strong> and compare a "
            "regression set before shifting traffic — a hot swap leaves old vectors incomparable to new queries."),
        },
    ],
    "03-rag-lifecycle.html": [
        {"q": L(
            "你要把这套 5 行 demo 变成能扛 1000 QPS 的服务。写入路径和查询路径<strong>分别部署在哪</strong>？"
            "为什么不能每次提问都 <code>from_documents</code>？你怎么验证扩容方案？",
            "You're turning the 5-line demo into a 1000-QPS service. <strong>Where does each of the write path and query "
            "path run</strong>, why can't you call <code>from_documents</code> per question, and how do you validate the "
            "scaling plan?"),
         "answer": L(
            "🔑 <strong>重点：写入路径离线做一次并落盘，查询路径在线、无状态、复用索引。</strong>"
            "每次提问都 <code>from_documents</code> 等于把 O(语料) 的切块+向量化塞进每个请求——又慢又烧钱、还没法水平扩展。"
            "做法：建索引放批处理/后台任务，<code>persist</code> 后查询侧只 <code>load</code> + <code>query</code>。"
            "验证：压测查询 QPS / p95 延迟，并确认建索引不在请求热路径上。",
            "🔑 <strong>Key: the write path runs once offline and is persisted; the query path is online, stateless, and "
            "reuses the index.</strong> Calling <code>from_documents</code> per question forces O(corpus) split+embed into "
            "every request — slow, costly, unscalable. Build in a batch/background job, <code>persist</code>, then the query "
            "side only <code>load</code>s + <code>query</code>s. Validate by load-testing query QPS / p95 latency and "
            "confirming indexing is off the hot path."),
         "fig": d.compare2(
            (L("写入路径（做一次）", "Write path (once)"), L("加载→切块→向量化→建索引→<strong>persist</strong>；重，离线/批处理。", "load→split→embed→index→<strong>persist</strong>; heavy, offline/batch.").render(False)),
            (L("查询路径（做很多次）", "Query path (many times)"), L("load→检索→后处理→合成；轻，在线、无状态、可水平扩展。", "load→retrieve→post-process→synthesize; light, online, stateless, scales out.").render(False)),
            caption=L("把“建一次”和“问多次”分开部署，才能各自扩容", "Deploy 'build once' and 'ask many' separately so each scales on its own")),
        },
        {"q": L(
            "高层 API 把细节藏了起来。你怎么判断“什么时候该拆开用低层 <code>from_args</code>”？举一个<strong>必须下沉</strong>的例子。",
            "The high-level API hides the details. How do you decide when to drop to low-level <code>from_args</code>? Give "
            "an example that <strong>forces</strong> it."),
         "answer": L(
            "🔑 <strong>重点：默认装配够用就用高层；要替换/插入某一站就下沉到 <code>from_args</code>。</strong>"
            "二者产出同一种对象、共享同一套抽象，只是装配深度不同。必须下沉的例子：要做“句窗检索 + 相似度过滤 + rerank + 自定义 "
            "<code>text_qa_template</code>”的客服引擎——默认 <code>as_query_engine</code> 装不出来，得用 <code>from_args</code> 逐件装。",
            "🔑 <strong>Key: use the high-level API when default wiring suffices; drop to <code>from_args</code> to "
            "replace/insert a stop.</strong> Both yield the same object and share the abstractions, differing only in wiring "
            "depth. Forcing example: a support engine with sentence-window retrieval + similarity cutoff + rerank + a custom "
            "<code>text_qa_template</code> — the default <code>as_query_engine</code> can't assemble that, so you wire it "
            "with <code>from_args</code>."),
        },
    ],
    "04-documents-nodes.html": [
        {"q": L(
            "你要做一个能“<strong>精确引用到第几页第几段</strong>”的合同问答。为什么检索单位用 Node 而不是整篇 Document？"
            "你会怎么设计 Node 的 metadata 与 relationships？怎么<strong>验证引用准确</strong>？",
            "You're building contract Q&amp;A that must <strong>cite the exact page and paragraph</strong>. Why retrieve "
            "Nodes, not whole Documents? How would you design the Node metadata and relationships, and how do you "
            "<strong>verify citation accuracy</strong>?"),
         "answer": L(
            "🔑 <strong>重点：Node 让检索精准且可溯源；整篇 Document 的向量会被无关内容稀释、还没法定位。</strong>"
            "设计：metadata 存 page / section / contract_id 供过滤与溯源，relationships（PREVIOUS/NEXT）串前后文做上下文扩展。"
            "验证：抽一批问题，人工核对引用的 page/段落是否<strong>真的包含答案</strong>，统计引用准确率，而不是只看答案读起来对不对。",
            "🔑 <strong>Key: Nodes make retrieval precise and citable; a whole-Document vector is diluted by irrelevant "
            "text and can't localize.</strong> Design: metadata holds page / section / contract_id for filtering and "
            "provenance; relationships (PREVIOUS/NEXT) chain neighbors for context expansion. Verify by manually checking, "
            "on a sample, whether the cited page/paragraph <strong>actually contains the answer</strong> — a citation-"
            "accuracy rate, not just whether the prose reads right."),
        },
        {"q": L(
            "检索老返回“相关但不对”的段落——查 2024 年退款却返回 2022 年的条款。你会怎么用 Node 的 metadata 解决？",
            "Retrieval keeps returning related-but-wrong chunks — asking about 2024 refunds returns the 2022 clause. How "
            "would you use Node metadata to fix it?"),
         "answer": L(
            "🔑 <strong>重点：把年份/版本写进 metadata，用 <code>MetadataFilters</code> 先过滤、再语义排序（检索第二通道）。</strong>"
            "纯向量只懂语义、不懂“限定 2024”这种结构化约束。前提是建索引时就把这些字段抽进每个 Node 的 metadata；否则过滤无从谈起。",
            "🔑 <strong>Key: put year/version into metadata and use <code>MetadataFilters</code> to filter first, then rank "
            "semantically (retrieval's second channel).</strong> Pure vectors capture meaning but not structured constraints "
            "like 'restrict to 2024'. It works only if those fields were extracted into each Node's metadata at index time."),
        },
    ],
    "05-readers.html": [
        {"q": L(
            "你的数据来自 PDF、网页、Confluence 三种源，还会不断加新源。你怎么设计加载层让“<strong>加新源不影响后面任何一站</strong>”？"
            "一个 PDF 常常每页一个 Document，这对你估成本和做引用有什么影响？",
            "Your data comes from PDFs, web pages and Confluence, with more sources coming. How do you design the loading "
            "layer so <strong>adding a source disturbs no later stage</strong>? A PDF often yields one Document per page — "
            "what does that do to your cost estimates and citations?"),
         "answer": L(
            "🔑 <strong>重点：Reader 统一产出 Document，把“来源差异”挡在管道之外；加新源 = 再接一个 Reader。</strong>"
            "因为下游只认 Document，换/加来源不动切块、向量化、检索任何一站。一个 PDF→多个 Document（每页），"
            "<code>len(docs) ≠ 文件数</code>：按 Document/Node 数估 embedding 成本，引用靠每个 Document 的 page metadata。"
            "验证：抽样检查每种源加载出的 Document 数与 metadata 是否齐全。",
            "🔑 <strong>Key: Readers all output Documents, keeping source quirks out of the pipeline; adding a source = "
            "plugging in another Reader.</strong> Since downstream only sees Documents, adding/swapping a source touches no "
            "later stage. One PDF → many Documents (per page), so <code>len(docs) ≠ file count</code>: estimate embedding "
            "cost by Document/Node count and cite via each Document's page metadata. Verify by spot-checking the Document "
            "count and metadata per source."),
        },
        {"q": L(
            "自己写一个 Reader vs 用 LlamaHub 现成集成，你怎么定？什么时候<strong>自写更划算</strong>？",
            "Writing your own Reader vs using a LlamaHub integration — how do you decide, and when is rolling your own "
            "<strong>worth it</strong>?"),
         "answer": L(
            "🔑 <strong>重点：常见格式/源优先用现成集成；只有专有格式或要特殊清洗/分块时才自写。</strong>"
            "现成集成久经测试、省事；自写只需实现 <code>BaseReader.load_data</code> 返回 Document 即可无缝接入管道。"
            "权衡点：维护成本 vs 控制力——别为一个一次性 CSV 重造轮子。",
            "🔑 <strong>Key: prefer existing integrations for common formats/sources; roll your own only for proprietary "
            "formats or special cleaning/splitting.</strong> Existing ones are tested and quick; a custom one just implements "
            "<code>BaseReader.load_data</code> to return Documents and plugs straight in. The trade-off is maintenance vs "
            "control — don't reinvent a wheel for a one-off CSV."),
        },
    ],
    "06-node-parsers.html": [
        {"q": L(
            "你接手一个“答不全 / 跑偏”的 RAG，怀疑是切块。请你来定 <code>chunk_size</code> 与 <code>chunk_overlap</code>："
            "① 依据什么信号、为什么；② 考虑过哪些<strong>替代切法</strong>、各自取舍；③ 定完用<strong>什么指标</strong>证明更好？",
            "You inherit a RAG that 'under-answers / drifts' and suspect chunking. Set <code>chunk_size</code> and "
            "<code>chunk_overlap</code>: (1) by what signal and why; (2) which <strong>alternative splitters</strong> did you "
            "weigh; (3) what <strong>metric</strong> proves the new split is better?"),
         "answer": L(
            "🔑 <strong>重点：按内容结构定大小、受 embedding token 上限约束，并用“改前改后命中率/Faithfulness”证明。</strong>"
            "① 手册偏小、叙事偏大；太大→噪声多还挤占上下文，太小→语义被切碎；多数 embedding 上限 ~512 token。"
            "② 替代：SentenceSplitter(通用)、TokenTextSplitter(严格控长)、SemanticSplitter(按语义断点、贵)、SentenceWindow(检索/上下文解耦)。"
            "③ 固定一组带 gold 块的查询，比较改前/改后的<strong>检索命中率</strong>与<strong>Faithfulness</strong>，看趋势而非单点。",
            "🔑 <strong>Key: size by content structure, bounded by the embedding token limit, and prove it with before/after "
            "hit-rate / Faithfulness.</strong> (1) manuals smaller, narrative larger; too large → noise + context bloat, too "
            "small → shredded meaning; most embeddings cap ~512 tokens. (2) Alternatives: SentenceSplitter (general), "
            "TokenTextSplitter (strict length), SemanticSplitter (semantic breakpoints, costly), SentenceWindow (decouples "
            "retrieval from context). (3) On a fixed gold-chunk query set, compare <strong>hit-rate</strong> and "
            "<strong>Faithfulness</strong> before vs after — trends, not a single point."),
         "fig": d.compare2(
            (L("无重叠 overlap=0", "No overlap"), L("句子被边界切断：块A“…7 个工作” | 块B“日内到账…”，两边都答不全。", "A sentence cut at the boundary: chunk A '…7 business' | chunk B 'days…' — neither answers fully.").render(False)),
            (L("有重叠 overlap=50", "With overlap"), L("相邻块共享边界句，“7 个工作日内到账”完整落在某块，命中即拿到完整语义。", "Adjacent chunks share boundary sentences, so the full thought lands in one chunk.").render(False)),
            caption=L("overlap 用少量冗余换“不把一句话切两半”", "Overlap trades a little redundancy for 'don't cut a thought in half'")),
        },
        {"q": L(
            "sentence-window 怎么同时做到“检索精准”和“上下文完整”？什么场景值得用、代价是什么？",
            "How does sentence-window get both precise retrieval and full context at once — and when is it worth the cost?"),
         "answer": L(
            "🔑 <strong>重点：它把“检索单位”和“喂给 LLM 的单位”解耦。</strong>"
            "以单句为 Node 检索(足够精准)，命中后用 <code>MetadataReplacementPostProcessor</code> 把单句换成前后句组成的 window 再交 LLM(补回上下文)。"
            "适合“答案靠一句话命中、但要上下文才说得清”的场景；代价是 metadata 变大、要配合特定后处理。",
            "🔑 <strong>Key: it decouples the retrieval unit from the unit fed to the LLM.</strong> Retrieve on single "
            "sentences (precise), then on a hit swap the sentence for its surrounding window via "
            "<code>MetadataReplacementPostProcessor</code> (restores context). Great when the answer is pinpointed by one "
            "sentence but needs context to explain; the cost is larger metadata and a required postprocessor."),
        },
    ],
    "07-metadata-extractors.html": [
        {"q": L(
            "你想让“用户的问句”更容易命中“陈述句的块”。你会怎么用元数据抽取做到？LLM 抽取成本怎么控？怎么<strong>验证召回真的提升</strong>？",
            "You want users' <em>questions</em> to better hit <em>statement</em>-style chunks. How would metadata extraction "
            "help, how do you control LLM cost, and how do you <strong>verify recall actually improves</strong>?"),
         "answer": L(
            "🔑 <strong>重点：用 <code>QuestionsAnsweredExtractor</code> 预生成“这个块能回答的问题”并一并 embedding，把“问”与“答”在语义空间对齐。</strong>"
            "成本控制：只对值得的块抽、文档级字段用文档级抽取器(不按块乘)、把确定字段留给 Reader 手写。验证：用真实问句集比较加抽取前后的<strong>命中率</strong>，确认提升大于成本。",
            "🔑 <strong>Key: use <code>QuestionsAnsweredExtractor</code> to pre-generate 'questions this chunk answers' and "
            "embed them too, aligning question with answer in semantic space.</strong> Control cost by extracting only where "
            "it pays, using document-level extractors for document-level fields (not multiplied per chunk), and hand-writing "
            "deterministic fields at the Reader. Verify by comparing <strong>hit-rate</strong> on a real question set before "
            "vs after, confirming the lift beats the cost."),
        },
        {"q": L(
            "哪些 metadata 值得用 LLM 抽、哪些直接在 Reader 阶段手写就够？<code>excluded_embed_metadata_keys</code> 什么时候<strong>必须</strong>用、为什么？",
            "Which metadata is worth an LLM vs hand-writing at the Reader stage, and when <strong>must</strong> you use "
            "<code>excluded_embed_metadata_keys</code>, and why?"),
         "answer": L(
            "🔑 <strong>重点：确定性字段(文件名/页码/日期/部门)手写、零成本；只有需要“理解内容”的(摘要/关键词/可回答问题)才花 LLM。</strong>"
            "<code>excluded_embed_metadata_keys</code>：当某些字段(长 URL、内部 ID、时间戳)会污染语义向量、拉偏相似度时，把它们排除出 embedding——保留用于过滤/展示，但不进向量。",
            "🔑 <strong>Key: hand-write deterministic fields (filename/page/date/dept) for free; spend an LLM only on fields "
            "that require understanding (summary/keywords/answerable questions).</strong> Use "
            "<code>excluded_embed_metadata_keys</code> when fields (long URLs, internal IDs, timestamps) would pollute the "
            "semantic vector and skew similarity — keep them for filtering/display but out of the embedding."),
        },
    ],
    "08-embeddings.html": [
        {"q": L(
            "你要给<strong>法律合同库</strong>选 embedding 模型。你会怎么选、为什么不直接用“最大最强”的那个？选定后怎么<strong>验证它在这个领域真的好用</strong>？",
            "Pick an embedding model for a <strong>legal-contract</strong> corpus. How do you choose, why not just the "
            "'biggest/strongest', and how do you <strong>verify it's actually good in this domain</strong>?"),
         "answer": L(
            "🔑 <strong>重点：领域贴合度 &gt; 通用强度——用你自己的评测集选，而不是默认“更大=更好”。</strong>"
            "通用最强模型未必懂法律术语；领域/微调模型常反超，还要权衡维度、成本、延迟、是否可私有部署(合同涉密)。"
            "验证：建一组带 gold 块的法律问句，比较候选模型的<strong>检索命中率/MRR</strong>，再看端到端 Faithfulness——用数字选型。",
            "🔑 <strong>Key: domain fit &gt; raw strength — choose with your own eval set, not 'bigger = better'.</strong> The "
            "strongest general model may not grasp legal terms; domain/fine-tuned models often win, and you must weigh "
            "dimensions, cost, latency, and on-prem deploy (contracts are sensitive). Verify with a legal gold-chunk query "
            "set, comparing candidates on <strong>hit-rate/MRR</strong> and end-to-end Faithfulness — pick by numbers."),
         "fig": d.grid(
            [L("候选", "Candidate"), L("领域贴合", "Domain fit"), L("代价", "Cost"), L("怎么定", "How to decide")],
            [
                [L("通用最强", "Top general"), L("未必懂法律术语", "may miss legal terms"), L("贵/可能云端", "pricey/cloud"), L("别默认选它", "don't default to it")],
                [L("领域/微调", "Domain/fine-tuned"), L("常更准", "often sharper"), L("需数据/训练", "needs data"), L("评测集胜出才用", "use if it wins evals")],
                [L("小而可私有部署", "Small, on-prem"), L("看评测", "depends"), L("便宜/合规", "cheap/compliant"), L("敏感数据优先", "prefer for sensitive")],
            ],
            caption=L("选型用评测集说话，不是参数最大就好", "Pick by an eval set, not by who has the most parameters")),
        },
        {"q": L(
            "用户搜精确条款编号“X-2000”搜不到——字面明明就在文档里。为什么向量会漏？怎么补救？",
            "Users search the exact clause id 'X-2000' and miss it — though it's literally in the docs. Why does the vector "
            "miss, and how do you fix it?"),
         "answer": L(
            "🔑 <strong>重点：向量偏“语义”，对精确符号/罕见 token/编号不敏感，语义上“X-2000”与别的编号很近、可能排不进 top-k。</strong>"
            "补救：<strong>混合检索</strong>(向量 + BM25/关键词把精确匹配召回回来)、把编号存进 metadata 做精确过滤、或对这类查询加 rerank。",
            "🔑 <strong>Key: embeddings capture meaning and are weak on exact symbols/rare tokens/ids — semantically 'X-2000' "
            "sits near other ids and may miss top-k.</strong> Fixes: <strong>hybrid retrieval</strong> (vector + BM25/keyword "
            "to recover exact matches), store the id in metadata for exact filtering, or add a reranker for such queries."),
        },
        {"q": L(
            "你想把 embedding 模型从 A 升级到 B。怎么评估“值不值得升”、怎么<strong>安全上线</strong>？",
            "You want to upgrade the embedding model from A to B. How do you assess whether it's worth it, and how do you "
            "<strong>roll it out safely</strong>?"),
         "answer": L(
            "🔑 <strong>重点：升级 embedding ＝ 全量重算向量、坐标系不可比，必须重建索引后再切——不能热替换。</strong>"
            "评估：在 staging 用 B <strong>重建一份索引</strong>，对同一回归集比较命中率/Faithfulness 与延迟成本；只有提升明显才升。"
            "上线：双索引灰度，确认 B 不退化再切流量；切换期间查询必须用与建索引相同的模型。",
            "🔑 <strong>Key: upgrading the embedding means recomputing all vectors into an incomparable space — you must "
            "re-index, then cut over; never hot-swap.</strong> Assess by <strong>rebuilding an index with B</strong> in "
            "staging and comparing hit-rate/Faithfulness and latency/cost on the same regression set; upgrade only on a clear "
            "win. Roll out with dual indexes and a gradual cutover; during the switch, queries must use the same model the "
            "index was built with."),
        },
    ],
    "09-vector-stores.html": [
        {"q": L(
            "你要从内存版 <code>SimpleVectorStore</code> 迁到生产向量库。按什么标准选？“百万级毫秒查询”靠什么、代价是什么？"
            "怎么<strong>验证召回没因近似而垮</strong>？",
            "You're moving from the in-memory <code>SimpleVectorStore</code> to a production store. By what criteria? How do "
            "you get 'millisecond queries at million-scale', at what cost, and how do you <strong>verify recall didn't "
            "collapse from the approximation</strong>?"),
         "answer": L(
            "🔑 <strong>重点：靠 ANN(近似最近邻)换速度，召回率可调、并非 100%——要用评测把召回卡在可接受线。</strong>"
            "选型标准：规模/持久化、metadata 过滤、库 vs 服务、事务一致性、运维成本(FAISS 快但偏库；pgvector 复用 Postgres+事务；Chroma 开箱)。"
            "验证：对一组 gold 查询比较 ANN 与精确扫描的命中率差，调 ANN 参数把召回拉回阈值，再看延迟是否仍达标。",
            "🔑 <strong>Key: speed comes from ANN (approximate NN); recall is tunable, not 100% — pin it above an "
            "acceptable line with evals.</strong> Criteria: scale/persistence, metadata filtering, library-vs-service, "
            "transactions, ops (FAISS fast but library-ish; pgvector reuses Postgres + transactions; Chroma batteries-"
            "included). Verify by comparing ANN vs exact-scan hit-rate on gold queries, tuning ANN params back to threshold, "
            "then checking latency still holds."),
        },
        {"q": L(
            "既要语义检索、又要“只在某部门 / 某年份里找”，你会怎么实现？",
            "You need semantic search AND 'only within a dept / year' — how do you implement it?"),
         "answer": L(
            "🔑 <strong>重点：用 <code>MetadataFilters</code> 先把范围约束到对的子集，再在子集里做向量近邻——“先按标签筛、再按语义排”。</strong>"
            "前提是建索引时就把部门/年份写进每个 Node 的 metadata，且所选向量库支持过滤下推(否则要先取再过滤、效率差)。",
            "🔑 <strong>Key: use <code>MetadataFilters</code> to constrain to the right subset, then do vector NN within it — "
            "'filter by tag, then rank by meaning'.</strong> It requires writing dept/year into each Node's metadata at index "
            "time, and a store that supports filter push-down (else you fetch-then-filter, which is inefficient)."),
        },
    ],
    "10-index-abstraction.html": [
        {"q": L(
            "一个库里既有定点 FAQ、又要“整库总结”。你会怎么组织 Index？为什么一个 Index 难兼顾两种范式？怎么<strong>验证路由把问题送对了</strong>？",
            "One base needs both pinpoint FAQ and 'summarize the whole base'. How do you organize the Index, why can't one "
            "Index do both, and how do you <strong>verify routing sends each question to the right one</strong>?"),
         "answer": L(
            "🔑 <strong>重点：建多个 Index(向量索引 + 摘要索引)，用 <code>RouterQueryEngine</code> 按问题路由。</strong>"
            "因为“Index = 怎么找”：向量索引按相似度定点召回，摘要索引遍历全部——一个结构难同时擅长两种检索行为。"
            "验证：构造“定点类 vs 总结类”问题各一批，检查路由选择的命中率(选错就调 selector/描述)，再看各自端到端答案质量。",
            "🔑 <strong>Key: build multiple indices (vector + summary) and route by question with a "
            "<code>RouterQueryEngine</code>.</strong> Because 'Index = how you find': a vector index pinpoints by similarity, "
            "a summary index walks everything — one structure can't excel at both. Verify with a batch of pinpoint vs "
            "summary questions, checking routing accuracy (tune the selector/descriptions on mistakes), then each path's "
            "end-to-end answer quality."),
         "fig": d.grid(
            [L("Index", "Index"), L("组织方式", "Organizes by"), L("适合", "Best for")],
            [
                [L("VectorStoreIndex", "VectorStoreIndex"), L("按相似度", "by similarity"), L("定点问答", "pinpoint Q&amp;A")],
                [L("SummaryIndex", "SummaryIndex"), L("遍历全部", "walk all"), L("整库总结", "whole-base summary")],
                [L("DocumentSummaryIndex", "DocumentSummaryIndex"), L("先摘要再定位", "summary then locate"), L("先粗后精", "coarse→fine")],
                [L("PropertyGraphIndex", "PropertyGraphIndex"), L("实体/关系图", "entity/relation graph"), L("多跳推理", "multi-hop")],
            ],
            caption=L("选 Index = 选检索范式：按“怎么找”而不是“存哪儿”", "Choosing an Index = choosing how you find, not where it lives")),
        },
        {"q": L(
            "需求从“单库 FAQ”演进到“跨 5 条产品线、还要多跳推理（A 依赖 B、B 依赖 C）”。你会怎么调整 Index 选型？"
            "为什么纯向量检索在多跳上吃力、怎么<strong>验证</strong>？",
            "Requirements grow from 'single-base FAQ' to 'across 5 product lines with multi-hop reasoning (A depends on B "
            "depends on C)'. How do you adjust your Index choice, why does pure vector retrieval struggle with multi-hop, and "
            "how would you <strong>verify</strong>?"),
         "answer": L(
            "🔑 <strong>重点：多跳/关系推理超出“按相似度取 top-k”的能力——考虑 <code>PropertyGraphIndex</code>（实体-关系图）或多 Index + Router 分流。</strong>"
            "纯向量把每跳当独立检索，难把 A→B→C 串成链路；跨产品线则用 metadata 过滤或按线建多个 Index。"
            "验证：构造需要 2+ 跳才能答对的问题集，比较向量索引 vs 图索引的<strong>正确率</strong>。",
            "🔑 <strong>Key: multi-hop/relational reasoning exceeds 'top-k by similarity' — consider a "
            "<code>PropertyGraphIndex</code> (entity-relation graph) or multiple indices + a Router.</strong> Pure vectors "
            "treat each hop as independent retrieval and can't chain A→B→C; across product lines, use metadata filters or "
            "per-line indices. Verify with a question set needing 2+ hops, comparing the <strong>correctness</strong> of the "
            "vector index vs the graph index."),
        },
    ],
    "11-ingestion-storage.html": [
        {"q": L(
            "知识库每天只变 1%。你怎么把建索引做成<strong>增量、幂等、可缓存</strong>的管道？怎么<strong>验证“只重算了变化的那部分”</strong>？",
            "Your base changes 1% a day. How do you make indexing an <strong>incremental, idempotent, cacheable</strong> "
            "pipeline, and how do you <strong>verify only the changed part was recomputed</strong>?"),
         "answer": L(
            "🔑 <strong>重点：用 <code>IngestionPipeline</code> + docstore + <code>DocstoreStrategy</code>，让代价正比于“变化量”而非总量。</strong>"
            "未变的块按内容哈希命中缓存、被去重，只有变化的文档触发重新切块/向量化；前提是文档有稳定 <code>ref_doc_id</code>。"
            "验证：改一篇文档再 run，看日志/计数确认只处理了那一篇、其余命中缓存(耗时与变更量成正比)。",
            "🔑 <strong>Key: use <code>IngestionPipeline</code> + a docstore + <code>DocstoreStrategy</code> so cost is "
            "proportional to the delta, not the total.</strong> Unchanged chunks hit the content-hash cache and are deduped; "
            "only changed docs trigger re-split/re-embed — given stable <code>ref_doc_id</code>s. Verify by editing one doc, "
            "re-running, and checking logs/counts that only that doc was processed while the rest hit cache (time scales with "
            "the change)."),
         "fig": d.flow([
            ("docs", L("文档", "Docs")),
            ("hash", L("内容哈希比对", "content-hash check"), L("未变→命中缓存", "unchanged → cache hit")),
            ("split", L("切块+抽取", "split+extract"), L("仅变化的", "changed only")),
            ("embed", L("向量化", "embed")),
            ("store", L("写入索引", "write index")),
         ], active="hash", caption=L("幂等摄取：只重算变化的文档，其余去重命中缓存", "Idempotent ingestion: recompute only changed docs, dedup the rest")),
        },
        {"q": L(
            "<code>persist</code> 到底存了哪三件？换成生产向量库(Chroma/pgvector)后有什么不同、加载时要注意什么？",
            "What three things does <code>persist</code> write, and how does that change with a production store "
            "(Chroma/pgvector) — what must you watch on load?"),
         "answer": L(
            "🔑 <strong>重点：默认三件套——docstore(Node 内容)、index store(索引结构)、vector store(向量)。</strong>"
            "换生产库后，向量由<strong>外部数据库托管</strong>，本地不再是 vector_store.json；加载时 <code>StorageContext</code> 必须连回<strong>同一个</strong>库，且查询用与建索引相同的 embedding 模型。",
            "🔑 <strong>Key: by default three pieces — docstore (Node content), index store (index structure), vector store "
            "(vectors).</strong> With a production store the vectors live in an <strong>external DB</strong>, not a local "
            "vector_store.json; on load the <code>StorageContext</code> must reconnect to the <strong>same</strong> store, and "
            "queries must use the same embedding model the index was built with."),
        },
    ],
    "12-retrievers.html": [
        {"q": L(
            "检索分数普遍偏低。你按<strong>什么顺序</strong>排查(top_k / embedding / 切块)？每一步怎么用<strong>数据</strong>验证而不是猜？",
            "Retrieval scores are uniformly low. In what <strong>order</strong> do you investigate (top_k / embedding / "
            "chunking), and how do you verify each step with <strong>data</strong> rather than guessing?"),
         "answer": L(
            "🔑 <strong>重点：先看正确块是否进了 top-k——top_k 只改数量不改分，不是第一手。</strong>"
            "正确块没进→切块太碎/太粗或 embedding 不贴领域(用命中率/MRR 量化、逐一替换变量验证)；进了但分低→query 与 doc 表述差距大(考虑改写/HyDE/rerank)。"
            "始终用一组带 gold 块的查询做对照，避免凭感觉。",
            "🔑 <strong>Key: first check whether the right chunk is even in top-k — top_k changes count, not scores, so it's "
            "not the first move.</strong> Not there → bad chunking or off-domain embedding (quantify with hit-rate/MRR, swap "
            "one variable at a time); there but low → query/doc phrasing gap (consider rewriting/HyDE/rerank). Always compare "
            "against a gold-chunk query set, not vibes."),
         "fig": d.compare2(
            (L("好召回", "Good recall"), L("top-k 全相关、分数高，正确依据在列——retrieve() 一看便知。", "top-k all relevant, high scores, the right evidence present — visible from retrieve() alone.").render(False)),
            (L("坏召回", "Bad recall"), L("混入噪声或正确块没进 top-k、分数偏低——问题在检索，不必怪 LLM。", "noise mixed in or the right chunk missing / low score — the fault is retrieval, not the LLM.").render(False)),
            caption=L("不调用 LLM，只看 retrieve() 的结果就能判断召回好坏", "Judge recall from retrieve() alone, without ever calling the LLM")),
        },
        {"q": L(
            "为什么要把检索独立成一等公民？这让你能脱离 LLM 单独做什么评估、有什么工程好处？",
            "Why make retrieval a first-class citizen? What can you evaluate without the LLM, and what's the engineering "
            "payoff?"),
         "answer": L(
            "🔑 <strong>重点：检索与生成解耦后，“召回对不对”可脱离 LLM 单独度量与优化。</strong>"
            "直接看 <code>retrieve()</code> 的 Node 是否含正确依据，用命中率/MRR 量化；于是调 top_k/embedding/切块都能秒级验证、不必每次跑昂贵生成，两类问题(召回 vs 生成)也不再纠缠。",
            "🔑 <strong>Key: decoupling retrieval from generation lets you measure and optimize 'is recall right' without the "
            "LLM.</strong> Inspect whether <code>retrieve()</code>'s Nodes hold the right evidence (hit-rate/MRR), so tuning "
            "top_k/embedding/chunking is verified in seconds without paying for generation — and the two problems (recall vs "
            "generation) stop entangling."),
        },
    ],
    "13-postprocessors.html": [
        {"q": L(
            "你想用<strong>最低成本</strong>提升答案质量。为什么后处理是性价比最高的一环？<code>similarity_cutoff</code> 怎么定？"
            "怎么<strong>证明它真的提升了</strong>——要看“答案”而不只是节点数？",
            "You want the <strong>cheapest</strong> quality lift. Why is post-processing the best bang-for-buck, how do you "
            "set <code>similarity_cutoff</code>, and how do you <strong>prove it actually helped</strong> — looking at "
            "answers, not just node counts?"),
         "answer": L(
            "🔑 <strong>重点：后处理在“检索后/生成前”，多为非 LLM 的轻量操作，不重训不换模型就能去噪提质。</strong>"
            "<code>similarity_cutoff</code> 看相关/不相关块的分数分布、卡在两者之间的谷，且分数尺度因 embedding 而异、要按模型重标。"
            "证明：同一组问题比较<strong>答案</strong>的 Faithfulness/正确率 before vs after，而不是只看“过滤掉几个节点”。",
            "🔑 <strong>Key: post-processing sits after retrieval / before generation, mostly lightweight non-LLM work that "
            "denoises and lifts quality with no retraining or model swap.</strong> Set <code>similarity_cutoff</code> from the "
            "score distribution of relevant vs irrelevant chunks (the valley between them); scales differ per embedding, so "
            "re-calibrate. Prove it by comparing <strong>answer</strong> Faithfulness/correctness before vs after on a fixed "
            "set — not just 'how many nodes got dropped'."),
         "fig": d.compare2(
            (L("过滤前", "Before cutoff"), L("混入“配送时效”低分块 → 答案被带偏、答非所问。", "a low-score 'shipping' chunk slips in → the answer drifts off-topic.").render(False)),
            (L("过滤后", "After cutoff"), L("只剩“退款”高分块 → 答案正确、切题。", "only the high-score 'refund' chunk remains → the answer is correct.").render(False)),
            caption=L("看答案的 before/after，才能坐实“显著提升”的主张", "Compare answers before/after to substantiate the 'big lift' claim")),
        },
        {"q": L(
            "阈值过滤 vs 交叉编码器 rerank 分别什么时候用？句窗 + <code>MetadataReplacementPostProcessor</code> 解决什么矛盾？",
            "When do you use threshold filtering vs cross-encoder reranking, and what tension do sentence-window + "
            "<code>MetadataReplacementPostProcessor</code> resolve?"),
         "answer": L(
            "🔑 <strong>重点：阈值便宜但粗糙(先砍明显低分)；rerank 准但贵一次调用(用更强模型纠正向量排序)。常组合：多取→cutoff→rerank。</strong>"
            "句窗+替换解决“检索要精准(小块) vs 生成要上下文(大块)”的矛盾：单句检索保证精准，命中后替换成前后句的 window 再喂 LLM——检索粒度与喂入粒度解耦。",
            "🔑 <strong>Key: thresholds are cheap but blunt (cut obvious low scores); reranking is accurate but costs an extra "
            "call (a stronger model fixes vector ordering). Often combined: fetch wide → cutoff → rerank.</strong> "
            "Sentence-window + replacement resolves 'retrieve precisely (small) vs generate with context (large)': retrieve "
            "single sentences for precision, then replace with the surrounding window before generation — decoupling "
            "retrieval granularity from what the LLM reads."),
        },
    ],
    "14-response-synthesizers.html": [
        {"q": L(
            "片段很多但上下文窗口很小。你怎么选 ResponseMode？compact 和 refine 的<strong>代价对比</strong>？怎么验证选对了？",
            "Many chunks but a small context window. How do you choose a ResponseMode, what's the <strong>cost difference</strong> "
            "between compact and refine, and how do you verify you chose right?"),
         "answer": L(
            "🔑 <strong>重点：选 mode 是“上下文窗口 vs 片段数量”的取舍——窗口小+片段多时矛盾最尖锐。</strong>"
            "refine 对每片段各调一次 LLM(多/慢/贵，但都读到)；compact 尽量合并(调用少，但小窗能塞的有限、可能漏或频繁退化为 refine)。"
            "验证：比较各 mode 的<strong>答案质量(Faithfulness/完整度)与成本/延迟</strong>，按预算取平衡。",
            "🔑 <strong>Key: choosing a mode trades context window against number of chunks — the tension peaks with a small "
            "window and many chunks.</strong> refine calls the LLM once per chunk (more/slower/costly, but reads all); compact "
            "merges to cut calls (but a small window limits what fits, risking misses or falling back to refine). Verify by "
            "comparing each mode's <strong>answer quality (Faithfulness/completeness) and cost/latency</strong>, balancing to "
            "budget."),
        },
        {"q": L(
            "“多片段→单答案”的核心矛盾是什么？<code>compact</code> 实际是什么、为什么把它做默认？",
            "What's the core tension of 'many chunks → one answer', what is <code>compact</code> really, and why is it the "
            "default?"),
         "answer": L(
            "🔑 <strong>重点：核心矛盾是检索片段可能装不进一次上下文窗口。</strong>"
            "<code>compact</code> 其实是 compact_and_refine：先把尽量多的片段塞满一个 prompt(减少调用)，装不下时再退回 refine 逐块迭代——兼顾省钱与不丢信息，所以适合做通用默认。",
            "🔑 <strong>Key: the core tension is that retrieved chunks may not fit in one context window.</strong> "
            "<code>compact</code> is really compact_and_refine: pack as many chunks as fit into one prompt (fewer calls), "
            "falling back to refine's chunk-by-chunk iteration when they don't — balancing cost and completeness, which makes "
            "it a sensible default."),
        },
        {"q": L(
            "你要“把整库逐点总结成一页纪要”。你选哪个 mode、为什么不是 compact？",
            "You must 'summarize the whole base into a one-page brief'. Which mode, and why not compact?"),
         "answer": L(
            "🔑 <strong>重点：用 tree_summarize——它要求看“全部”内容、分组逐层合并，正合“全局总结”。</strong>"
            "compact 以“尽量塞满+少调用”为目标，面对超出窗口的大量片段会塞不下、易漏；总结类问题宁可多调用也要覆盖全。",
            "🔑 <strong>Key: use tree_summarize — it sees <em>all</em> content and merges in layers, exactly fitting a global "
            "summary.</strong> compact aims to pack-and-minimize-calls and, with chunks exceeding the window, can't fit "
            "everything and risks missing parts; for summaries you'd rather pay more calls to cover all."),
         "fig": d.vflow([
            (L("8 个检索片段", "8 retrieved chunks"), L("装不进一次上下文", "too many for one window")),
            (L("分组各自总结", "summarize each group"), L("→ 几个小结", "→ partial summaries")),
            (L("再总结这些小结", "summarize the summaries"), L("→ 更少中间结果", "→ fewer intermediates")),
            (L("单个最终答案", "one final answer"), None),
         ], caption=L("tree_summarize：像锦标赛逐层向上合并，适合“看全部再总结”", "tree_summarize merges upward, round by round — for 'see all, then summarize'")),
        },
    ],
    "15-query-engine.html": [
        {"q": L(
            "你要把 demo 问答升级成“<strong>只引用、不编造、可灰度替换检索策略</strong>”的客服引擎。你会怎么用 QueryEngine 装配？"
            "为什么拆成三件而不是写死一个函数？怎么<strong>验证改造没把效果搞差</strong>？",
            "You're upgrading demo Q&amp;A into a support engine that is <strong>cite-only, never-invent, with swappable "
            "retrieval</strong>. How do you assemble it via the QueryEngine, why split into three parts instead of one "
            "hard-coded function, and how do you <strong>verify the rebuild didn't regress</strong>?"),
         "answer": L(
            "🔑 <strong>重点：QueryEngine 是“组合根”，把检索器/后处理/合成器三件正交组件装在一起，可独立替换。</strong>"
            "拆三件→换检索器不影响合成、加后处理不影响检索，灰度某一件不动其余；写死一个函数则牵一发动全身。"
            "装配：retriever + [cutoff/rerank] + 严格 <code>text_qa_template</code>(只引用/给出处)。验证：用回归集比较改造前后的 Faithfulness/正确率，确认没退化再上。",
            "🔑 <strong>Key: the QueryEngine is a composition root assembling three orthogonal parts — retriever / "
            "postprocessors / synthesizer — each independently swappable.</strong> Splitting them means swapping the retriever "
            "doesn't touch synthesis and adding postprocessing doesn't touch retrieval, so you can canary one part; a "
            "hard-coded function couples everything. Assemble retriever + [cutoff/rerank] + a strict "
            "<code>text_qa_template</code> (cite-only). Verify with a regression set comparing Faithfulness/correctness before "
            "vs after, shipping only on no regression."),
        },
        {"q": L(
            "什么时候从 <code>as_query_engine</code> 下沉到 <code>from_args</code>？这个取舍你怎么向团队解释？",
            "When do you drop from <code>as_query_engine</code> to <code>from_args</code>, and how do you explain the "
            "trade-off to your team?"),
         "answer": L(
            "🔑 <strong>重点：二者产出同一种 QueryEngine，只是装配深度不同——默认够用就用快捷方式，要定制某一站才下沉。</strong>"
            "向团队解释：<code>as_query_engine</code> 一行起步、维护省心；<code>from_args</code> 给最大控制力(自定义 retriever/后处理/合成/prompt)。"
            "规范：默认走快捷方式，确有定制需求再下沉，避免无谓的样板。",
            "🔑 <strong>Key: both yield the same QueryEngine, differing only in wiring depth — use the shortcut when defaults "
            "suffice, drop down to customize a stop.</strong> Explain it as: <code>as_query_engine</code> is one-line and "
            "low-maintenance; <code>from_args</code> gives maximum control (custom retriever/postproc/synth/prompt). "
            "Convention: default to the shortcut, drop down only on a real customization need, avoiding needless boilerplate."),
        },
        {"q": L(
            "一次 <code>.query()</code> 内部时序是什么、为什么是这个顺序？",
            "What's the internal sequence of one <code>.query()</code>, and why this order?"),
         "answer": L(
            "🔑 <strong>重点：retrieve() 取 top-k → node_postprocessors 过滤/重排/替换 → synthesize() 合成 → Response(answer + source_nodes)。</strong>"
            "顺序有因：必须先取回候选才能后处理，必须先精选再合成(否则把噪声喂给 LLM)；source_nodes 一路保留，保证答案可溯源。",
            "🔑 <strong>Key: retrieve() fetches top-k → node_postprocessors filter/rerank/replace → synthesize() fuses → "
            "Response (answer + source_nodes).</strong> The order is principled: you must fetch candidates before "
            "post-processing them, and curate before synthesis (else you feed the LLM noise); source_nodes are carried "
            "throughout to keep the answer traceable."),
        },
    ],
    "16-chat-engine.html": [
        {"q": L(
            "你要做多轮客服。<strong>两个真正的难点</strong>是什么？condense_question 和 context 都每轮检索吗？“要不要检索”由谁决定？"
            "你会选哪种 mode、怎么<strong>验证多轮效果</strong>？",
            "You're building multi-turn support. What are the <strong>two real hard parts</strong>? Do condense_question and "
            "context both retrieve every turn? Who decides 'whether to retrieve'? Which mode would you pick, and how do you "
            "<strong>evaluate multi-turn quality</strong>?"),
         "answer": L(
            "🔑 <strong>重点：难点是“指代消解 + 用哪个问题去检索”；两种 mode 都每轮检索，“要不要检索”是 agent/router 的事，不是这两个 mode。</strong>"
            "选择：condense_plus_context 通用性最好(先消解再检索注入)。验证：用<strong>多轮</strong>对话集，看带指代的追问是否被正确消解、答案是否仍忠于检索——单轮指标不够。",
            "🔑 <strong>Key: the hard parts are coreference + which question to retrieve with; both modes retrieve every turn, "
            "and deciding 'whether to retrieve' is agent/router territory, not these modes.</strong> Pick condense_plus_context "
            "as the most general (condense, then retrieve + inject). Evaluate with a <strong>multi-turn</strong> dialogue set, "
            "checking whether pronoun-laden follow-ups resolve correctly and answers stay grounded — single-turn metrics "
            "aren't enough."),
         "fig": d.flow([
            ("u", L("“那它呢？”", "“and its …?”"), L("含指代", "has a pronoun")),
            ("co", L("指代消解", "Coreference"), L("→“国际订单的退款呢？”", "→ “refund for intl orders?”")),
            ("ret", L("检索", "Retrieve")),
            ("ans", L("作答", "Answer")),
            ("mem", L("写入记忆", "Update memory")),
         ], active="co", caption=L("多轮关键：先把“它/那”解析成具体所指，再检索作答", "The crux of multi-turn: resolve 'it/that' to a referent, then retrieve and answer")),
        },
        {"q": L(
            "用户追问“那国际订单呢”被解析错、检索跑偏。你怎么排查和改善？",
            "On 'and intl orders?', the engine resolves it wrong and retrieval derails. How do you debug and improve it?"),
         "answer": L(
            "🔑 <strong>重点：先打印 condense 之后生成的“独立问题”——很多实现可看改写后的 query。</strong>"
            "若改写错→优化 condense 的 prompt、保留更多对话历史、或换 condense_plus_context；指代实在复杂时，上 agent 做更强的对话状态管理，或在 UI 端引导用户把指代说明确。",
            "🔑 <strong>Key: first print the standalone question produced after condensing — many implementations expose the "
            "rewritten query.</strong> If the rewrite is wrong → improve the condense prompt, keep more history, or switch to "
            "condense_plus_context; for genuinely hard references, move to an agent with stronger dialogue-state management, "
            "or guide users to disambiguate in the UI."),
        },
    ],
    "17-settings-prompts.html": [
        {"q": L(
            "同样的检索结果，换一句 prompt 答案就不同。质量责任更多压在<strong>检索</strong>还是 <strong>prompt</strong>？"
            "你怎么分工调优、分别用什么指标？",
            "Same retrieved context, different prompt, different answer. Does quality rest more on <strong>retrieval</strong> "
            "or the <strong>prompt</strong>? How do you split the tuning, and with what metrics each?"),
         "answer": L(
            "🔑 <strong>重点：检索决定“依据对不对”、prompt 决定“依据用得对不对”——先把召回调达标，再用 prompt 调忠实度/格式。</strong>"
            "召回不到，prompt 再好也是巧妇难为无米之炊；指标上，检索看<strong>命中率/MRR</strong>，prompt 看 <strong>Faithfulness</strong> 与格式/约束达成率。别把两类问题混在一起调。",
            "🔑 <strong>Key: retrieval decides whether the evidence is right, the prompt decides whether it's used right — "
            "get recall to target first, then tune faithfulness/format with the prompt.</strong> No recall, no prompt can "
            "save it; measure retrieval by <strong>hit-rate/MRR</strong> and the prompt by <strong>Faithfulness</strong> plus "
            "format/constraint adherence. Don't conflate the two while tuning."),
         "fig": d.compare2(
            (L("Prompt A（宽松）", "Prompt A (loose)"), L("“根据资料回答” → 资料没提保修期，却补一句“一般为一年”(编造)。", "'answer from the context' → the warranty isn't there, yet it adds 'usually one year' (invented).").render(False)),
            (L("Prompt B（严格）", "Prompt B (strict)"), L("“只用资料、未提及就说不知道” → 老实回答“资料未提及”。", "'use only the context, say unknown otherwise' → honestly says 'not in the sources'.").render(False)),
            caption=L("检索一字不变，换 prompt 就改变忠实度——这是“最后一公里”", "Same retrieval, a different prompt changes faithfulness — the 'last mile'")),
        },
        {"q": L(
            "有人到处用全局 <code>Settings</code>、有人坚持显式传参。各自利弊？你怎么定团队规范？",
            "Some use the global <code>Settings</code> everywhere; others pass config explicitly. Trade-offs, and what "
            "team convention would you set?"),
         "answer": L(
            "🔑 <strong>重点：全局少样板但隐式依赖、难追踪、测试易串味；显式可读可测、可多配置共存但啰嗦。</strong>"
            "规范：<strong>全局设默认值</strong>，关键/差异化组件(评估用的 judge、特殊 query engine)<strong>显式覆盖并就近声明</strong>——既省样板又可追踪。",
            "🔑 <strong>Key: global means less boilerplate but an implicit, hard-to-trace dependency that can leak state in "
            "tests; explicit is readable/testable and lets configs coexist but is verbose.</strong> Convention: <strong>set "
            "sane global defaults</strong>, and <strong>explicitly override</strong> key/divergent components (an eval judge, "
            "a special query engine) declared close to use — boilerplate saved, traceability kept."),
        },
    ],
    "18-advanced-retrieval.html": [
        {"q": L(
            "基础 top-k 召回不全。<strong>三类典型短板</strong>分别用哪种进阶检索器补？对延迟敏感的线上问答你会上 query fusion 吗？"
            "怎么权衡、怎么<strong>验证召回真提升</strong>？",
            "Naive top-k under-recalls. Which advanced retriever fixes each of the <strong>three typical weaknesses</strong>? "
            "Would you use query fusion in latency-sensitive live Q&amp;A? How do you weigh it and <strong>verify recall "
            "actually improves</strong>?"),
         "answer": L(
            "🔑 <strong>重点：召回不全→Query Fusion、命中碎片→AutoMerging/Recursive、多库分流→Router；进阶检索是“用更多计算换更好结果”，没有免费午餐。</strong>"
            "延迟敏感时先量化：fusion 多跑几轮检索+一次改写，提升值不值这点延迟？高价值可容忍几百 ms 才上，否则用更便宜手段(更好 embedding/轻量 rerank/缓存)。"
            "验证：对 gold 集比较加 fusion 前后的命中率与端到端质量，再核延迟预算。",
            "🔑 <strong>Key: under-recall → Query Fusion, fragmented hits → AutoMerging/Recursive, multi-source → Router; "
            "advanced retrieval trades more compute for better results — no free lunch.</strong> Under latency pressure, "
            "quantify first: fusion adds retrieval passes + a rewrite — is the lift worth the latency? Adopt only for "
            "high-value, few-hundred-ms-tolerant flows; else use cheaper levers (better embedding/light rerank/caching). Verify "
            "by comparing hit-rate and end-to-end quality with/without fusion on a gold set, then re-check the latency budget."),
         "fig": d.flow([
            ("q", L("一个问题", "One question")),
            ("rw", L("改写成多版", "rewrite to N variants")),
            ("ret", L("各自检索", "retrieve each")),
            ("rrf", L("RRF 融合", "fuse via RRF")),
            ("out", L("更全的候选", "fuller candidate set")),
         ], active="rrf", caption=L("Query Fusion：改写多版各自检索，再把多路结果融合（默认 simple，可选 RRF）", "Query Fusion: rewrite, retrieve each, then fuse the lists (default simple; RRF optional)")),
        },
        {"q": L(
            "AutoMerging 检索和“直接调大 chunk_size”有何不同？什么时候用 Router？",
            "How is AutoMerging retrieval different from 'just use a bigger chunk_size', and when do you use a Router?"),
         "answer": L(
            "🔑 <strong>重点：AutoMerging 用小块检索(精准)，命中同一父块的多个小块时再合并成父块喂 LLM(补上下文)——兼得精准与上下文。</strong>"
            "直接调大 chunk_size 则全程用大块，检索更糊、噪声更多。Router 用于<strong>多个 Index/数据源分流</strong>：用 selector 把问题路由到最合适的那个。",
            "🔑 <strong>Key: AutoMerging retrieves with small chunks (precise), then merges small chunks under the same parent "
            "into the parent for the LLM (context) — precision and context together.</strong> A bigger chunk_size uses large "
            "chunks throughout, blurring retrieval and adding noise. A Router is for <strong>routing across multiple "
            "indices/sources</strong>: a selector sends each question to the best one."),
        },
    ],
    "19-evaluation.html": [
        {"q": L(
            "你要把调优从“凭感觉”变“<strong>可度量闭环</strong>”。你会搭什么评估、三把尺子各查什么、各需什么输入？"
            "怎么防止“修好一个、悄悄弄坏一批”？",
            "You want to turn tuning from 'vibes' into a <strong>measurable loop</strong>. What evaluation do you set up, what "
            "does each of the three rulers measure and need as input, and how do you prevent 'fix one, silently break many'?"),
         "answer": L(
            "🔑 <strong>重点：Faithfulness(答案是否忠于检索，需 response+source_nodes)、Relevancy(是否切题，需 query+response+检索上下文)、Correctness(对不对，需参考答案，1–5 分)。</strong>"
            "闭环：改一处→重测→对比→保留/回退；防回归靠一个固定<strong>回归集</strong>，每次改动都重跑、看趋势而非单点。",
            "🔑 <strong>Key: Faithfulness (is the answer grounded in retrieval — needs response + source_nodes), Relevancy (is "
            "it on-topic — needs query + response + the retrieved contexts), Correctness (is it right — needs a reference answer, 1–5).</strong> The "
            "loop: change one thing → re-test → compare → keep/revert; prevent regressions with a fixed <strong>regression "
            "set</strong> re-run on every change, watching trends over single points."),
         "fig": d.flow([
            ("base", L("基线 0.82", "baseline 0.82")),
            ("change", L("改 chunk_size", "change chunk_size")),
            ("retest", L("重测", "re-test")),
            ("cmp", L("0.71 变差", "0.71 worse"), L("→ 回退", "→ revert")),
            ("keep", L("达标才保留", "keep only if it holds")),
         ], active="cmp", caption=L("可度量闭环：用数字决定保留还是回退，挡住悄悄的退化", "Measurable loop: numbers decide keep-or-revert, blocking silent regressions")),
        },
        {"q": L(
            "评估用 LLM-as-judge，有哪些局限？怎么缓解、怎么让分数<strong>可信</strong>？",
            "Evaluation uses LLM-as-judge. What are its limits, and how do you mitigate them to make scores "
            "<strong>trustworthy</strong>?"),
         "answer": L(
            "🔑 <strong>重点：judge 本身有噪声/偏见、可能偏向某种风格、成本高、边界判断不稳。</strong>"
            "缓解：固定 judge 模型与 prompt、用二值/明确 rubric、对关键集做<strong>人评校准</strong>、看<strong>趋势</strong>而非单点分数、维护回归集比较相对变化——把它当“相对尺”而非“绝对真值”。",
            "🔑 <strong>Key: the judge is noisy/biased, may favor a style, costs money, and is shaky on edge cases.</strong> "
            "Mitigate by pinning the judge model and prompt, using binary/explicit rubrics, <strong>calibrating with human "
            "review</strong> on a key set, watching <strong>trends</strong> over single scores, and comparing relative change "
            "on a fixed set — treat it as a relative ruler, not absolute truth."),
        },
        {"q": L(
            "你只有 200 条历史问答、<strong>没有标准答案</strong>。怎么起步做评估？",
            "You have 200 historical Q&amp;A pairs but <strong>no reference answers</strong>. How do you start evaluating?"),
         "answer": L(
            "🔑 <strong>重点：先做不需要参考答案的 Faithfulness 与 Relevancy——它们只看 response/source_nodes/query。</strong>"
            "Correctness 才需要 reference，可后续对高价值子集人工标注少量 gold 再补。先用前两把尺子建立基线和回归集，立刻就能挡住明显退化。",
            "🔑 <strong>Key: start with Faithfulness and Relevancy, which need no reference — they look only at "
            "response/source_nodes/query.</strong> Correctness needs a reference, so hand-label a small gold subset on "
            "high-value cases later. The first two rulers establish a baseline and regression set immediately, catching "
            "obvious regressions right away."),
        },
    ],
    "20-capstone.html": [
        {"q": L(
            "你要把整套书拼成<strong>生产级</strong>本地 RAG。首次建库 vs 复用怎么分支？为什么 <code>Settings.embed_model</code> 必须<strong>先于建索引</strong>？"
            "怎么验证整条链路？",
            "You're assembling everything into a <strong>production-grade</strong> local RAG. How do you branch first-build vs "
            "reuse, why must <code>Settings.embed_model</code> be set <strong>before</strong> building the index, and how do "
            "you validate the whole chain?"),
         "answer": L(
            "🔑 <strong>重点：用 <code>if os.path.exists(PERSIST)</code> 分支(存在→load_index_from_storage，否则建+persist)；embed_model 必须先设，因为落盘向量由它决定、加载后必须同模型才能对齐。</strong>"
            "设晚或设错→向量在错坐标系，查询报错或相似度全错，只能重建。验证：端到端跑一组问题 + 用 <code>FaithfulnessEvaluator</code> 批量打分，作上线前质量闸。",
            "🔑 <strong>Key: branch on <code>if os.path.exists(PERSIST)</code> (exists → load_index_from_storage, else build + "
            "persist); embed_model must be set first because persisted vectors depend on it and loading must use the same "
            "model to line up.</strong> Set it late or wrong → vectors in the wrong space, queries error or score "
            "nonsensically, fixable only by re-indexing. Validate by running a question set end-to-end plus batch "
            "<code>FaithfulnessEvaluator</code> scoring as a pre-launch gate."),
         "fig": d.flow([
            ("load", L("加载", "Load")),
            ("ingest", L("摄取/切块", "Ingest")),
            ("index", L("建索引", "Index")),
            ("persist", L("持久化", "Persist")),
            ("retrieve", L("检索", "Retrieve")),
            ("postproc", L("后处理", "Post-proc")),
            ("synth", L("合成", "Synthesize")),
            ("eval", L("评估", "Evaluate")),
         ], caption=L("端到端：写入路径建好可复用索引，查询路径据此作答，评估守门", "End-to-end: the write path builds a reusable index, the query path answers, evaluation guards the gate")),
        },
        {"q": L(
            "把它改造成“带引用脚注的客服机器人”，你换 / 加哪几件？为什么<strong>骨架不用动</strong>？",
            "To reshape it into a 'support bot with citation footnotes', which parts do you swap or add, and why does the "
            "<strong>skeleton stay</strong>?"),
         "answer": L(
            "🔑 <strong>重点：只换/加四件——chat engine(多轮记忆)、引用后处理(把 source_nodes 渲染成脚注)、收紧 prompt(只引用)、评估闸。</strong>"
            "因为每一站都遵守统一接口、正交可替换，写入/查询主干(QueryEngine 装配)原封不动——这正是“可组合标准件”的红利。",
            "🔑 <strong>Key: swap/add just four — a chat engine (memory), a citation postprocessor (render source_nodes as "
            "footnotes), a tightened cite-only prompt, and an evaluation gate.</strong> Because every stop obeys one interface "
            "and is orthogonally swappable, the write/query backbone (the QueryEngine assembly) stays untouched — exactly the "
            "dividend of 'composable standard parts'."),
        },
        {"q": L(
            "面试官说“一句话讲清 LlamaIndex 的 RAG 核心思想”。你会怎么答？",
            "The interviewer asks: 'in one sentence, the core idea of LlamaIndex RAG'. What's your answer?"),
         "answer": L(
            "🔑 <strong>重点：RAG 是一条由可组合标准件搭成的数据管道——写入路径把知识外置成可检索、可更新、可溯源的索引，查询路径在其上据此作答，每一站都遵守统一接口、可独立替换与评估。</strong>"
            "加分点：能顺势举一个“替换某一站”的例子(换向量库/加 rerank/接 chat)说明它的可组合性。",
            "🔑 <strong>Key: RAG is a data pipeline of composable standard parts — the write path externalizes knowledge into "
            "a searchable, refreshable, citable index, and the query path answers from it, with every stop sharing one "
            "interface and independently swappable and measurable.</strong> Bonus: follow up with a 'swap one stop' example "
            "(change the vector store / add a reranker / attach chat) to show the composability."),
        },
    ],
    "21-production-retrieval.html": [
        {"q": L(
            "线上客服 RAG 要加一道 <strong>rerank 精排</strong>。你会在 <strong>Cohere 托管</strong>、"
            "<strong>本地 SentenceTransformer 交叉编码器</strong>、<strong>LLMRerank</strong> 之间怎么选？"
            "数据合规、延迟、成本各自怎么权衡，又怎么<strong>验证 rerank 真的有用</strong>？",
            "Your live support RAG needs a <strong>rerank</strong> step. How do you choose among <strong>hosted "
            "Cohere</strong>, a <strong>local SentenceTransformer cross-encoder</strong>, and <strong>LLMRerank</strong>? "
            "How do you weigh data compliance, latency and cost, and how do you <strong>verify rerank actually "
            "helps</strong>?"),
         "answer": L(
            "🔑 <strong>重点：三者是“准确 / 成本 / 是否本地”的取舍——Cohere 最省事最准，但数据出网且按调用计费；"
            "本地 SentenceTransformer 数据不出网、免调用费，但要 GPU；LLMRerank 最灵活却最慢最贵。</strong>"
            "合规敏感（医疗/金融）优先本地；要开箱即用且数据可外发选 Cohere；只在高价值、可容忍延迟的少量查询上才考虑 "
            "LLMRerank。验证：固定一组 gold 查询，比较“仅向量 / 混合 / 混合+rerank”三档的命中率与端到端答案质量，"
            "再核对每条新增的延迟与单价是否值得。",
            "🔑 <strong>Key: the three trade off accuracy / cost / on-prem — Cohere is easiest and most accurate but data "
            "leaves the network and is billed per call; a local SentenceTransformer keeps data in and is fee-free but "
            "needs a GPU; LLMRerank is most flexible yet slowest and priciest.</strong> For compliance-sensitive domains "
            "(health/finance) prefer local; for plug-and-play with data allowed to egress pick Cohere; reserve LLMRerank "
            "for a few high-value, latency-tolerant queries. Verify on a fixed gold set: compare hit-rate and end-to-end "
            "answer quality across vector-only / hybrid / hybrid+rerank, then check whether the added latency and "
            "per-call cost are worth it."),
         "fig": d.grid(
            [L("Rerank 方案", "Reranker"), L("准确", "Accuracy"), L("成本", "Cost"), L("是否本地", "On-prem?")],
            [
                [L("CohereRerank（托管 API）", "CohereRerank (hosted API)"), L("高", "high"),
                 L("按调用计费", "per-call fee"), L("否（数据出网）", "no (data egress)")],
                [L("SentenceTransformer 交叉编码器", "SentenceTransformer cross-encoder"), L("中–高", "mid–high"),
                 L("免调用费 · 需 GPU", "no fee · needs GPU"), L("是", "yes")],
                [L("LLMRerank", "LLMRerank"), L("高（看模型）", "high (model-dependent)"),
                 L("最贵 · 最慢", "priciest · slowest"), L("可本地（用本地 LLM）", "can be (local LLM)")],
            ],
            caption=L("三种 rerank 的取舍：准确 / 成本 / 是否本地——按数据合规与延迟预算选",
                      "Three rerankers traded off on accuracy / cost / on-prem — choose by data compliance and latency budget")),
        },
        {"q": L(
            "用户报“问产品编号 <code>X-2000</code> 的保修期，答得驴唇不对马嘴”。纯向量为什么会漏？你会怎么修，"
            "<strong>为什么不是直接把 top_k 调大</strong>？",
            "Users report “asking the warranty for product id <code>X-2000</code> gives a nonsense answer”. Why does "
            "pure vector miss it, how would you fix it, and <strong>why not just raise top_k</strong>?"),
         "answer": L(
            "🔑 <strong>重点：embedding 偏语义，对精确符号/罕见 token（如 <code>X-2000</code>）不敏感，相关条款可能排在"
            "很后面、进不了 top-k——这是“字面匹配”问题，不是“召回量”问题。</strong>调大 top_k 只是把噪声一起拉进来、"
            "更慢更贵，真正该补的是<strong>字面那一路</strong>：加 BM25 做混合检索，让精确编号被直接命中，再用 RRF 融合 + "
            "rerank 精排；或把编号写进 metadata 做精确过滤。验证：在含编号的 gold 查询上比较修复前后的命中率。",
            "🔑 <strong>Key: embeddings capture meaning and are weak on exact symbols/rare tokens (like "
            "<code>X-2000</code>), so the right clause can rank far down and never enter top-k — a literal-match "
            "problem, not a recall-volume one.</strong> Raising top_k just drags in noise, slower and pricier; the real "
            "fix is the <strong>literal path</strong>: add BM25 for hybrid retrieval so the exact id is hit directly, "
            "fuse via RRF and rerank; or write the id into metadata for exact filtering. Verify by comparing hit-rate "
            "before/after on id-bearing gold queries."),
        },
        {"q": L(
            "有人提议给检索加 <strong>HyDE</strong>。它的原理是什么、什么场景最有效、又有什么<strong>风险</strong>？"
            "你怎么决定上不上？",
            "Someone proposes adding <strong>HyDE</strong> to retrieval. How does it work, when does it help most, "
            "what's the <strong>risk</strong>, and how do you decide whether to adopt it?"),
         "answer": L(
            "🔑 <strong>重点：HyDE 先让 LLM 写一个“假设答案”，用这段更像文档的文本的向量去检索——当问句很短、措辞和"
            "文档差距大时，召回往往明显变好。</strong>风险：多一次 LLM 调用（更慢更贵），且假设答案若跑偏会把检索带偏"
            "（垃圾进、垃圾出）；所以 <code>include_original=True</code> 保留原问句一起检索更稳。决定上不上：在 gold 集上"
            "对比 HyDE 前后的命中率与端到端质量，再权衡多出的延迟/成本是否值得。",
            "🔑 <strong>Key: HyDE first has the LLM draft a “hypothetical answer”, then retrieves with that doc-like "
            "text's vector — when questions are terse and worded unlike the documents, recall often improves "
            "clearly.</strong> Risks: an extra LLM call (slower, pricier) and, if the hypothetical drifts, it can steer "
            "retrieval astray (garbage in, garbage out) — so <code>include_original=True</code> keeps the raw question "
            "in the mix for safety. Decide by comparing hit-rate and end-to-end quality with/without HyDE on a gold "
            "set, then weigh the added latency/cost."),
        },
    ],
    "22-eval-scale.html": [
        {"q": L(
            "你要给一套上线的 RAG 建 <strong>CI 质量闸</strong>。金标集<strong>怎么造</strong>、阈值<strong>怎么定</strong>、"
            "judge <strong>误判</strong>了怎么办？又怎么<strong>验证这道闸本身有效</strong>（不是摆设、也不会动不动误杀）？",
            "You're building a <strong>CI quality gate</strong> for a live RAG. How do you <strong>build the gold "
            "set</strong>, <strong>set the threshold</strong>, handle <strong>judge misfires</strong>, and how do you "
            "<strong>verify the gate itself works</strong> (neither a rubber stamp nor a flaky blocker)?"),
         "answer": L(
            "🔑 <strong>重点：金标集先自动生成起量、再人工策展高价值子集；阈值用基线分布定、且只卡“相对回退”；"
            "judge 误判靠固定 judge+rubric、看趋势、留容忍带；闸的有效性要拿“已知好/坏改动”去回归测试它。</strong>"
            "① 造集：<code>DatasetGenerator</code> 自动铺几十上百题，人工挑高价值、易回归的场景补参考答案，沉淀成固定回归集；"
            "② 定阈值：先跑基线得到通过率分布，阈值卡在“比基线明显下降”（如低于基线 5 个点就 fail），而非拍一个绝对数；"
            "③ 误判：固定 judge 模型与 prompt、用二值 rubric、对边界样本人评校准，关注<strong>整体通过率趋势</strong>而非单题抖动；"
            "④ 验证闸本身：故意提交一个<strong>已知会变差</strong>的改动（把 chunk 改坏 / 砍掉 rerank），闸必须变红；"
            "再提交一个<strong>已知无害</strong>的改动，闸必须放行——闸也要回归测试，否则它只是个绿灯摆设。",
            "🔑 <strong>Key: auto-generate the gold set for volume then human-curate a high-value subset; set the threshold "
            "from the baseline distribution and gate on <em>relative</em> regression; tame judge misfires with a pinned "
            "judge+rubric, trends and a tolerance band; and prove the gate works by regression-testing it with "
            "known-good/known-bad changes.</strong> (1) Build: <code>DatasetGenerator</code> lays down dozens-to-hundreds, "
            "then hand-pick high-value, regression-prone cases and add reference answers, hardening a fixed regression set; "
            "(2) threshold: run a baseline for the pass-rate distribution and gate on “clearly below baseline” (e.g. fail "
            "if it drops 5 points), not an arbitrary absolute number; (3) misfires: pin the judge model and prompt, use a "
            "binary rubric, calibrate edge cases with human review, and watch the <strong>overall pass-rate trend</strong> "
            "rather than single-question jitter; (4) verify the gate: deliberately submit a <strong>known-bad</strong> "
            "change (break chunking / drop the reranker) and the gate must go red, then a <strong>known-harmless</strong> "
            "one and it must pass — the gate itself needs regression testing, or it's just a green rubber stamp."),
         "fig": d.flow([
            ("pr", L("提 PR", "Open PR"), L("改了切块/检索", "changed chunking/retrieval")),
            ("rerun", L("CI 重跑金标集", "CI re-runs gold set"), L("50 题并发", "50 Qs, concurrent")),
            ("rate", L("通过率 0.86", "pass-rate 0.86"), L("基线 0.93", "baseline 0.93")),
            ("gate", L("跌破阈值 0.90", "below the 0.90 bar"), L("闸变红", "gate goes red")),
            ("block", L("拦回 / 回退", "block / revert"), L("合不进主干", "can't reach main")),
         ], active="gate", caption=L(
            "一次 CI 闸触发：通过率从基线 0.93 跌到 0.86、低于 0.90 阈值，PR 被自动拦回",
            "One gate trip: pass-rate falls from baseline 0.93 to 0.86, under the 0.90 bar — the PR is auto-blocked")),
        },
        {"q": L(
            "有同事说“金标集直接用 <code>DatasetGenerator</code> 自动生成就行，省得人工标注”。你<strong>同意吗</strong>？"
            "自动题有什么<strong>坑</strong>，你会怎么把这套金标做得<strong>可信、可长期当闸用</strong>？",
            "A teammate says “just auto-generate the gold set with <code>DatasetGenerator</code> — skip human labeling”. Do "
            "you <strong>agree</strong>? What are the <strong>pitfalls</strong> of auto-generated gold, and how would you "
            "make the set <strong>trustworthy enough to gate on long-term</strong>?"),
         "answer": L(
            "🔑 <strong>重点：自动生成适合“快速起量”，但不能直接当唯一金标——它问得浅、可能脱离真实分布，"
            "还无法支撑需要参考答案的 Correctness。</strong>坑：① 题目多是“文档里直接抄得到”的浅问，测不出真实难例；"
            "② 分布偏向文档密集处，真实高频问法反而漏；③ 没有人工核对的参考答案，Correctness 用不了，"
            "且自动题里混着噪声会让闸“误判”。做可信：自动生成只当<strong>草稿池</strong>，人工<strong>挑选 + 改写 + 标注</strong>"
            "出一个高价值子集，再掺入<strong>线上真实问题</strong>（点踩/转人工的会话）补真实长尾；CI 闸主要用免参考的忠实/相关"
            "跑全量草稿、用人工金标子集跑 Correctness。怎么验证金标本身够好：让它能<strong>区分</strong>已知的好坏配置"
            "（好配置分明显更高），区分不出就说明题目没区分度，得继续提纯。",
            "🔑 <strong>Key: auto-generation is great for fast volume but can't be the sole gold — it asks shallow "
            "questions, can drift from the real distribution, and can't support reference-needing Correctness.</strong> "
            "Pitfalls: (1) questions are mostly “copy-able straight from the doc”, missing real hard cases; (2) the "
            "distribution skews to doc-dense areas while real high-frequency phrasings are missed; (3) without "
            "human-checked references Correctness is unusable, and noise in auto questions makes the gate “misfire”. To "
            "make it trustworthy: treat auto-generation as a <strong>draft pool</strong>, have humans <strong>select + "
            "rewrite + label</strong> a high-value subset, and mix in <strong>real production questions</strong> "
            "(thumbs-down / handed-off chats) for the true long tail; the CI gate runs reference-free faithfulness/relevancy "
            "over the full draft and Correctness over the human subset. How to check the gold itself is good: it should "
            "<strong>discriminate</strong> known good vs bad configs (good scores clearly higher); if it can't, the "
            "questions lack discriminative power and need more curation."),
        },
        {"q": L(
            "评估是 <strong>LLM-as-judge</strong>，搬进 CI 后同一个 PR 重跑两次<strong>分数会抖</strong>，"
            "构建一会儿红一会儿绿（flaky）。这种“闸不稳定”你怎么<strong>定位和治理</strong>？还要不要把它当硬性合并条件？",
            "Evaluation is <strong>LLM-as-judge</strong>; in CI the same PR re-run twice gives <strong>jittery "
            "scores</strong> and a flaky red/green build. How do you <strong>diagnose and tame</strong> this instability — "
            "and should it still be a hard merge requirement?"),
         "answer": L(
            "🔑 <strong>重点：抖动来自 judge 的随机性和小样本噪声；靠“降随机 + 增样本 + 留容忍带 + 看趋势”治理，"
            "硬闸只卡明显回退、细微抖动转为告警。</strong>① 降随机：judge 用 <code>temperature=0</code>、固定模型版本与评判 prompt、"
            "二值 rubric，减少不确定性；② 增样本：题太少则单题翻转就让通过率大跳，扩大回归集让比例稳定；"
            "③ 容忍带：阈值不卡“等于基线”，而是“低于基线一个明显幅度”才 fail，给噪声留缓冲；"
            "④ 分层：把昂贵/不稳的 Correctness 放夜间离线跑，CI 硬闸只用稳定、免参考的忠实/相关；"
            "⑤ 看趋势：连续多次低于阈值才阻断，单点抖动只告警。验证治理是否见效：固定一个不动的 PR 重跑 N 次，"
            "统计通过率方差，方差落进容忍带以内才算稳。",
            "🔑 <strong>Key: jitter comes from judge randomness and small-sample noise; tame it with “less randomness + more "
            "samples + a tolerance band + trend-watching”, and let the hard gate fire only on clear regressions while small "
            "jitter becomes a warning.</strong> (1) Less randomness: run the judge at <code>temperature=0</code>, pin the "
            "model version and judging prompt, use a binary rubric; (2) more samples: with too few questions one flip "
            "swings the pass-rate, so enlarge the regression set to stabilize the ratio; (3) tolerance band: gate on "
            "“clearly below baseline”, not “equal to baseline”, leaving room for noise; (4) tiering: run the "
            "costly/unstable Correctness offline nightly and keep only stable, reference-free faithfulness/relevancy as the "
            "hard CI gate; (5) trend: block only after several consecutive sub-threshold runs, warn on a single dip. Verify "
            "the fix by re-running one unchanged PR N times and measuring pass-rate variance — stable once it falls within "
            "the tolerance band."),
        },
    ],
}
