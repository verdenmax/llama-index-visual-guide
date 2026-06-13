import os

import build_print
import shell


def test_print_html_written_and_chinese_default():
    out = build_print.build_print()
    assert os.path.exists(out)
    html = open(out, encoding="utf-8").read()
    assert 'data-uilang="zh"' in html                 # PDF shows Chinese
    assert '<details class="accordion" open>' in html or "accordion" not in html
    assert '<details class="accordion">' not in html   # every accordion forced open
    for _f, title, _p in shell.PAGES:
        assert title.zh in html                        # every lesson title present
