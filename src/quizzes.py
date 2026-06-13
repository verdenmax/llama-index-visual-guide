"""Per-lesson self-test (自测题): bilingual multiple-choice + open prompts.

Questions probe *why a thing is designed the way it is*, not rote syntax.
Content lives here as data (``L`` for bilingual text) keyed by filename;
``render(fname)`` turns it into HTML appended to each lesson by build.py /
build_print.py. Options are deterministically shuffled so the correct answer
isn't always first. No third-party dependencies.
"""

import hashlib

import i18n
from i18n import L


def _shuffle(opts, answer, seed):
    order = sorted(
        range(len(opts)),
        key=lambda i: hashlib.md5(f"{seed}:{i}".encode("utf-8")).hexdigest(),
    )
    return [opts[i] for i in order], order.index(answer)


QUIZZES = {
    "01-what-is-llamaindex.html": {
        "mcq": [
            {
                "q": L("RAG（检索增强生成）的核心思想是？", "What is the core idea of RAG?"),
                "opts": [
                    L("重新训练模型以记住新知识", "Retrain the model to memorize new knowledge"),
                    L("回答前先检索相关外部片段、塞进上下文再生成",
                      "Retrieve relevant external snippets first, put them in context, then generate"),
                    L("把全部数据塞进一个超大提示词", "Stuff all data into one giant prompt"),
                    L("换一个更大的模型", "Switch to a bigger model"),
                ],
                "answer": 1,
                "why": L(
                    "RAG = 先检索后生成：用检索到的相关片段作为上下文，让模型据此回答，避免重训成本与知识幻觉。",
                    "RAG retrieves first, then generates: relevant snippets become context so the model answers "
                    "from them, avoiding retraining cost and hallucination.",
                ),
            },
            {
                "q": L("LlamaIndex 在 RAG 里主要负责什么？", "What does LlamaIndex mainly provide for RAG?"),
                "opts": [
                    L("训练 embedding 模型", "Training embedding models"),
                    L("把加载→切块→索引→检索→合成这条管道标准化、可编排",
                      "Standardizing and orchestrating the load→split→index→retrieve→synthesize pipeline"),
                    L("托管一个向量数据库服务", "Hosting a vector database service"),
                    L("提供 GPU 推理", "Providing GPU inference"),
                ],
                "answer": 1,
                "why": L(
                    "LlamaIndex 是 RAG 的“数据与编排框架”：统一各阶段接口，底层换 LLM / 向量库 / embedding 都不改主链路。",
                    "LlamaIndex is the data + orchestration framework for RAG: it unifies each stage so swapping the "
                    "LLM / vector store / embedding doesn't change the main pipeline.",
                ),
            },
        ],
        "open": [
            L("如果你的文档每天都在更新，你会如何设计“增量重新索引”的策略？",
              "If your documents change daily, how would you design an incremental re-indexing strategy?"),
        ],
    },
}


def render(fname):
    data = QUIZZES.get(fname)
    if not data:
        return ""
    head = i18n.t("🧪 自测 · 想一想为什么这么设计", "🧪 Self-check · think about the design")
    out = ['<div class="selftest">', f"<h2>{head}</h2>"]
    for i, item in enumerate(data.get("mcq", []), 1):
        shuffled, ans = _shuffle(item["opts"], item["answer"], f"{fname}:{i}")
        opts = "\n".join(f"    <li>{i18n.render(o, block=False)}</li>" for o in shuffled)
        letter = chr(65 + ans)
        reveal = i18n.t("看答案与解析", "Show answer & explanation")
        hint = i18n.t("点击展开", "expand")
        ans_label = i18n.t(f"答案：{letter}", f"Answer: {letter}")
        out.append(
            f'<div class="quiz">\n'
            f'  <div class="qn">{i}. {i18n.render(item["q"], block=False)}</div>\n'
            f'  <ol class="opts">\n{opts}\n  </ol>\n'
            f'  <details class="accordion">\n'
            f'    <summary>{reveal} <span class="hint">{hint}</span></summary>\n'
            f'    <div class="acc-body"><div class="qa"><div class="a">'
            f'<strong>{ans_label}</strong> {i18n.render(item.get("why", ""), block=False)}'
            f"</div></div></div>\n"
            f"  </details>\n"
            f"</div>"
        )
    opens = data.get("open", [])
    if opens:
        spark = i18n.t("💭 发散思考（没有标准答案）", "💭 Open questions (no single right answer)")
        lis = "\n".join(f"    <li>{i18n.render(o, block=False)}</li>" for o in opens)
        out.append(
            f'<div class="card spark">\n  <div class="tag">{spark}</div>\n  <ul>\n{lis}\n  </ul>\n</div>'
        )
    out.append("</div>")
    return "\n".join(out)
