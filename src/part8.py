"""Part 8 (agentic depth & shipping): lessons 32-35. Content filled task-by-task."""
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


LESSON_32 = _skeleton("answer", "多智能体与工作流控制流", "multi-agent &amp; workflow control flow")
LESSON_33 = _skeleton("answer", "人在回路（HITL）", "human-in-the-loop")
LESSON_34 = _skeleton("answer", "把 RAG 上线成服务", "serving your RAG")
LESSON_35 = _skeleton("embed", "微调 embedding", "fine-tuning embeddings")
