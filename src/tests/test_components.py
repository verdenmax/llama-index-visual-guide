import components as c
from i18n import L


def test_lead_wraps_paragraph_with_both_languages():
    html = c.lead(L("一段话", "a sentence"))
    assert html.startswith('<p class="lead">')
    assert 'data-lang="zh">一段话' in html
    assert 'data-lang="en">a sentence' in html


def test_analogy_card_has_tag_and_class():
    html = c.analogy(L("像便利贴", "like sticky notes"))
    assert "card analogy" in html
    assert "🧩" in html


def test_section_title_is_inline_not_block_div():
    html = c.section(L("标题", "Title"), "<p>body</p>")
    assert "<h2><span" in html  # inline title, no <div> inside <h2>
    assert "<p>body</p>" in html


def test_key_points_emits_one_li_per_item():
    html = c.key_points([L("甲", "A"), L("乙", "B"), "丙"])
    assert html.count("<li>") == 3
    assert "✅" in html


def test_compare_table_shapes_rows_and_cols():
    html = c.compare_table(
        [L("特性", "Feature"), L("说明", "Note")],
        [[L("a", "a"), L("b", "b")], ["c", "d"]],
    )
    assert html.count("<th>") == 2
    assert html.count("<tr>") == 3  # header + 2 rows
    assert html.count("<td>") == 4


def test_source_ref_cites_file_and_symbol():
    html = c.source_ref("schema.py", "Document")
    assert "schema.py" in html and "Document" in html
    assert "🔬" in html


def test_code_block_wraps_pre():
    html = c.code('<span class="kw">from</span> llama_index')
    assert '<pre class="code">' in html
    assert "llama_index" in html


def test_design_highlight_card():
    assert "card highlight" in c.design_highlight(L("精妙", "elegant"))
    assert "💡" in c.design_highlight(L("精妙", "elegant"))


def test_pipeline_highlights_requested_stage_only():
    html = c.pipeline("embed")
    assert "stage on" in html
    assert html.count("stage on") == 1
    # both path labels present
    assert "写入路径" in html and "查询路径" in html


def test_pipeline_none_has_no_active_stage():
    assert "stage on" not in c.pipeline(None)


def test_accordion_has_details_and_summary_and_qa():
    html = c.accordion(L("详解", "Details"), c.qa_item(L("示例", "Example"), L("代码", "code")))
    assert "<details" in html and "<summary>" in html
    assert 'class="qa"' in html
