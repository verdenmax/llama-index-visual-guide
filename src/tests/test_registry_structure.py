import registry
import shell


def test_27_lessons_and_glossary_last():
    keys = list(registry.CONTENT.keys())
    assert len(keys) == 27
    assert keys[-1] == "27-glossary.html"          # glossary renumbered + last
    assert "21-production-retrieval.html" in keys   # first production lesson
    assert "26-agents-workflows.html" in keys       # last production lesson


def test_pages_has_seven_parts():
    parts = {p[2].zh for p in shell.PAGES}
    assert len(parts) == 7                          # was 6 → +Production part
    assert len(shell.PAGES) == 27
