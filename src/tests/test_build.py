import os

import build
import shell


def test_build_writes_all_pages_and_index():
    written = build.build()
    assert len(written) == len(shell.PAGES) + 1
    assert os.path.exists(os.path.join(build.ROOT, "index.html"))
    for fname, _t, _p in shell.PAGES:
        assert os.path.exists(os.path.join(build.LESSONS_DIR, fname))


def test_built_lesson_has_shell_and_bilingual_default():
    build.build()
    html = open(os.path.join(build.LESSONS_DIR, "01-what-is-llamaindex.html"), encoding="utf-8").read()
    assert 'data-uilang="zh"' in html
    assert 'data-lang="en"' in html
    assert 'href="02-architecture.html"' in html


def test_built_index_lists_every_lesson():
    build.build()
    idx = open(os.path.join(build.ROOT, "index.html"), encoding="utf-8").read()
    for fname, _t, _p in shell.PAGES:
        assert f'href="lessons/{fname}"' in idx
    assert "共 36 课 · 9 个部分" in idx
