import shell
from i18n import L


def test_pages_count_and_endpoints():
    assert len(shell.PAGES) == 27
    assert shell.PAGES[0][0] == "01-what-is-llamaindex.html"
    assert shell.PAGES[-1][0] == "27-glossary.html"


def test_pages_titles_and_parts_are_bilingual():
    for fname, title, part in shell.PAGES:
        assert isinstance(title, L) and isinstance(part, L)
    assert len({p[2].zh for p in shell.PAGES}) == 7  # seven parts


def test_page_has_language_toggle_and_assets():
    html = shell.page("01-what-is-llamaindex.html", "<p>body</p>")
    assert "data-lang-toggle" in html
    assert 'data-uilang="zh"' in html
    assert "li-guide-lang" in html
    assert "[data-lang]{display:none}" in html.replace(" ", "")


def test_page_title_uses_chinese_and_sets_data_titles():
    html = shell.page("01-what-is-llamaindex.html", "x")
    assert "<title>01 · LlamaIndex 与 RAG 是什么 — LlamaIndex RAG 图解教程</title>" in html
    assert 'data-title-en="01 · ' in html


def test_page_nav_chain_links_siblings():
    html = shell.page("02-architecture.html", "x")
    assert 'href="01-what-is-llamaindex.html"' in html
    assert 'href="03-rag-lifecycle.html"' in html


def test_first_page_prev_goes_home_last_page_next_goes_home():
    first = shell.page("01-what-is-llamaindex.html", "x")
    last = shell.page("27-glossary.html", "x")
    assert 'href="../index.html"' in first
    assert 'href="../index.html"' in last


def test_index_lists_all_pages_and_counts():
    html = shell.index_page(lesson_prefix="lessons/")
    for fname, _t, _p in shell.PAGES:
        assert f'href="lessons/{fname}"' in html
    assert "共 27 课 · 7 个部分" in html
    assert "data-lang-toggle" in html
