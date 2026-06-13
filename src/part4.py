"""Part 4 (advanced): lessons 17-19. Content filled task-by-task."""
import components as c
from i18n import L


def _stub():
    return c.pipeline(None) + c.lead(L("（本课内容建设中）", "(Lesson content coming soon)"))


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
LESSON_18 = _stub()
LESSON_19 = _stub()
