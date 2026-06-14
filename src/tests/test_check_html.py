import check_html


GOOD = (
    '<html lang="zh-CN" data-uilang="zh"><head><title>x</title>'
    '<meta name="description" content="d"></head><body>'
    '<button data-lang-toggle>EN</button>'
    '<h1>t</h1><div data-lang="zh">中</div><div data-lang="en">en</div>'
    '<div class="card analogy">a</div><div class="card keypts">本课要点</div>'
    '<a href="01-what-is-llamaindex.html">p</a><a href="03-rag-lifecycle.html">n</a>'
    "</body></html>"
)


def test_good_lesson_has_no_errors():
    issues = check_html.check_lesson("02-architecture.html", GOOD)
    errs = [i for i in issues if i[0] == "ERR"]
    assert errs == []


def test_missing_english_is_an_error():
    html = GOOD.replace('<div data-lang="en">en</div>', "")
    issues = check_html.check_lesson("02-architecture.html", html)
    assert any(i[0] == "ERR" and "English" in i[2] for i in issues)


def test_unbalanced_div_is_an_error():
    html = GOOD + "<div>oops"
    issues = check_html.check_lesson("02-architecture.html", html)
    assert any(i[0] == "ERR" and "div" in i[2] for i in issues)


def test_stray_ampersand_is_an_error():
    html = GOOD.replace("<h1>t</h1>", "<h1>t</h1><p>Q&A text</p>")
    issues = check_html.check_lesson("02-architecture.html", html)
    assert any(i[0] == "ERR" and "&amp;" in i[2] for i in issues)


def test_escaped_ampersand_is_ok():
    html = GOOD.replace("<h1>t</h1>", "<h1>t</h1><p>Q&amp;A text</p>")
    issues = check_html.check_lesson("02-architecture.html", html)
    assert [i for i in issues if i[0] == "ERR"] == []


def test_missing_toggle_button_is_an_error():
    html = GOOD.replace("<button data-lang-toggle>EN</button>", "")
    issues = check_html.check_lesson("02-architecture.html", html)
    assert any(i[0] == "ERR" and "toggle" in i[2] for i in issues)


def test_unbalanced_bilingual_blocks_is_an_error():
    html = GOOD.replace('<div data-lang="en">en</div>', '<div data-lang="en">en</div><div data-lang="zh">多</div>')
    issues = check_html.check_lesson("02-architecture.html", html)
    assert any(i[0] == "ERR" and "unbalanced bilingual" in i[2] for i in issues)


def test_fewer_than_two_figures_is_a_warning():
    issues = check_html.check_lesson("02-architecture.html", GOOD)
    assert any(i[0] == "WARN" and "figures" in i[2] for i in issues)


def test_two_figures_clears_the_figure_warning():
    html = GOOD + '<div class="fig">a</div><div class="fig">b</div>'
    issues = check_html.check_lesson("02-architecture.html", html)
    assert not any("figures" in i[2] for i in issues)


def test_glossary_is_exempt_from_figure_warning():
    issues = check_html.check_lesson("21-glossary.html", GOOD)
    assert not any("figures" in i[2] for i in issues)
