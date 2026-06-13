import i18n
from i18n import L, render, t


def test_render_emits_both_languages_as_div():
    html = L("你好", "hello").render()
    assert '<div data-lang="zh">你好</div>' in html
    assert '<div data-lang="en">hello</div>' in html


def test_render_inline_uses_span():
    html = L("上一课", "Prev").render(block=False)
    assert '<span data-lang="zh">上一课</span>' in html
    assert '<span data-lang="en">Prev</span>' in html


def test_en_falls_back_to_zh_when_omitted():
    node = L("仅中文")
    assert node.en == "仅中文"
    html = node.render()
    assert '<div data-lang="en">仅中文</div>' in html


def test_render_passthrough_for_plain_str():
    assert render("plain text") == "plain text"


def test_render_dispatches_to_L():
    node = L("甲", "A")
    assert render(node) == node.render()
    assert render(node, block=False) == node.render(block=False)


def test_t_is_inline_helper():
    assert t("中", "EN") == L("中", "EN").render(block=False)


def test_html_inside_zh_is_preserved_not_escaped():
    html = L("<b>粗</b>", "<b>bold</b>").render()
    assert "<b>粗</b>" in html


def test_assets_present_and_consistent():
    # default language baked into CSS selectors + toggle script key
    assert '[data-lang]{display:none}' in i18n.LANG_CSS.replace(" ", "")
    assert 'data-uilang="zh"' in i18n.LANG_CSS or "data-uilang='zh'" in i18n.LANG_CSS
    assert "li-guide-lang" in i18n.LANG_TOGGLE_JS
    assert "localStorage" in i18n.LANG_TOGGLE_JS
