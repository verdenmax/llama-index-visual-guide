import registry
import shell


def test_36_lessons_and_glossary_last():
    keys = list(registry.CONTENT.keys())
    assert len(keys) == 36
    assert keys[-1] == "36-glossary.html"            # glossary renumbered + last
    assert "27-graph-rag.html" in keys               # first beyond-text lesson
    assert "31-structured-outputs.html" in keys      # last Part 7 lesson
    assert "32-multi-agent.html" in keys             # first Part 8 lesson
    assert "35-finetuning-embeddings.html" in keys   # last Part 8 lesson


def test_pages_has_nine_parts():
    parts = {p[2].zh for p in shell.PAGES}
    assert len(parts) == 9                            # was 7 → +Beyond-text +Agentic
    assert len(shell.PAGES) == 36
