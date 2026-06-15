"""Part 6 (production-advanced): lessons 21-26. Content filled task-by-task."""
import components as c
import diagrams as d
import i18n
from i18n import L


def _skeleton(zh_topic, en_topic):
    return (
        c.pipeline(None)
        + c.lead(L(f"本课讲生产阶段的 <strong>{zh_topic}</strong>（内容完善中）。",
                   f"This lesson covers <strong>{en_topic}</strong> for production (being written)."))
        + d.flow([("a", L("场景", "Scenario")), ("b", L("做法", "Approach")), ("c", L("评测", "Evaluate"))],
                 caption=L("占位流程图", "placeholder flow"))
        + d.compare2((L("不做", "Without"), i18n.render(L("有什么问题", "what breaks"))),
                     (L("做了", "With"), i18n.render(L("解决什么", "what it fixes"))),
                     caption=L("占位对照", "placeholder compare"))
        + c.analogy(L("占位类比。", "Placeholder analogy."))
        + c.key_points([L("本课要点占位。", "Key-points placeholder.")])
    )


LESSON_21 = _skeleton("生产级检索", "production retrieval")
LESSON_22 = _skeleton("规模化评估与 CI 回归闸", "evaluation at scale &amp; CI gating")
LESSON_23 = _skeleton("可观测与追踪", "observability &amp; tracing")
LESSON_24 = _skeleton("成本与延迟工程", "cost &amp; latency engineering")
LESSON_25 = _skeleton("安全与防护", "security &amp; guardrails")
LESSON_26 = _skeleton("Agent 与 Workflows", "agents &amp; workflows")
