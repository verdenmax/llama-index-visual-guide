"""Part 7 (beyond plain-text RAG): lessons 27-31. Content filled task-by-task."""
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


LESSON_27 = _skeleton("index", "图谱 RAG", "Graph RAG")
LESSON_28 = _skeleton("retrieve", "结构化数据查询（SQL &amp; Pandas）", "querying structured data (SQL &amp; Pandas)")
LESSON_29 = _skeleton("embed", "多模态 RAG", "multimodal RAG")
LESSON_30 = _skeleton("retrieve", "查询分解（Sub-Question）", "query decomposition (Sub-Question)")
LESSON_31 = _skeleton("synthesize", "结构化输出", "structured outputs")
