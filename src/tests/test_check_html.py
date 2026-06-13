import check_html


GOOD = (
    '<html lang="zh-CN" data-uilang="zh"><head><title>x</title>'
    '<meta name="description" content="d"></head><body>'
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
