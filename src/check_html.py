"""Structural / consistency regression guard for the generated HTML.

Run after ``build.py``::

    cd src && python check_html.py

Exits non-zero if any ERROR-level issue is found (used by CI). WARN/INFO are
printed but do not fail the build. Checks performed on every lesson + index:

* balanced tags (div / details / table / pre / summary) and details<->summary
* exactly one <h1> (WARN), a <title>, and a meta description
* every lesson carries English content (data-lang="en") — bilingual guard
* no unescaped '<' inside <pre> code blocks (would eat content)
* nav prev/next chain matches shell.PAGES order
* index TOC lists every page and shows the correct lesson/part counts
* (WARN only) every lesson has a "本课要点" and a "card analogy"
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

import shell  # noqa: E402

PAGES = shell.PAGES
ORDER = [p[0] for p in PAGES]
TOTAL = len(PAGES)

STALE = []
SOFT_EXEMPT = {"21-glossary.html"}


def check_lesson(fname, html):
    issues = []

    def add(sev, msg):
        issues.append((sev, fname, msg))

    for tag in ("div", "details", "table", "pre", "summary"):
        o = len(re.findall(rf"<{tag}[\s>]", html))
        c = len(re.findall(rf"</{tag}>", html))
        if o != c:
            add("ERR", f"<{tag}> unbalanced: {o} open / {c} close")
    nd, ns = len(re.findall(r"<details", html)), len(re.findall(r"<summary", html))
    if nd != ns:
        add("ERR", f"details({nd}) != summary({ns})")
    if len(re.findall(r"<h1", html)) != 1:
        add("WARN", "expected exactly one <h1>")
    if "<title>" not in html:
        add("ERR", "missing <title>")
    if 'name="description"' not in html:
        add("ERR", "missing meta description")
    # bilingual: every lesson must carry English content
    if 'data-lang="en"' not in html:
        add("ERR", "no English content (data-lang=\"en\") — page is not bilingual")
    if fname not in SOFT_EXEMPT:
        if "本课要点" not in html:
            add("WARN", "no 本课要点 / key-points card")
        if "card analogy" not in html:
            add("WARN", "no analogy card")
    # unescaped '<' inside <pre>
    for pre in re.findall(r"<pre[^>]*>(.*?)</pre>", html, re.S):
        cleaned = re.sub(r"</?(?:span|strong|b|em|u|a)\b[^>]*>", "", pre)
        if re.search(r"<(?!/)", cleaned):
            add("ERR", "unescaped '<' in <pre> code block")
            break
    # stray '&' in body content (must be &amp;) — ignore <style>/<script>/data: URIs
    body = re.sub(
        r"<style[^>]*>.*?</style>|<script[^>]*>.*?</script>|data:[^\"')\s]+", "", html, flags=re.S
    )
    body = re.sub(r"&(?:amp|lt|gt|quot|apos|nbsp|#\d+|#x[0-9a-fA-F]+);", "", body)
    if "&" in body:
        m = re.search(r".{0,15}&.{0,15}", body)
        add("ERR", f"unescaped '&' (use &amp;): {m.group(0)!r}")
    # nav chain matches PAGES order
    if fname in ORDER:
        idx = ORDER.index(fname)
        if idx + 1 < TOTAL and f'href="{ORDER[idx + 1]}"' not in html:
            add("ERR", f"next link missing -> {ORDER[idx + 1]}")
        if idx > 0 and f'href="{ORDER[idx - 1]}"' not in html:
            add("ERR", f"prev link missing -> {ORDER[idx - 1]}")
    return issues


def main():
    issues = []
    for fname, _title, _part in PAGES:
        path = os.path.join(ROOT, "lessons", fname)
        if not os.path.exists(path):
            issues.append(("ERR", fname, "lesson file missing (run build.py)"))
            continue
        issues += check_lesson(fname, open(path, encoding="utf-8").read())

    idx_html = open(os.path.join(ROOT, shell.INDEX_FILE), encoding="utf-8").read()
    for fname, _title, _part in PAGES:
        if f"lessons/{fname}" not in idx_html:
            issues.append(("ERR", "index.html", f"TOC missing entry {fname}"))
    m = re.search(r"共 (\d+) 课 · (\d+) 个部分", idx_html)
    if m:
        if int(m.group(1)) != TOTAL:
            issues.append(("ERR", "index.html", f"count says {m.group(1)} but PAGES has {TOTAL}"))
        nparts = len({p[2].zh for p in PAGES})
        if int(m.group(2)) != nparts:
            issues.append(("ERR", "index.html", f"parts says {m.group(2)} but PAGES has {nparts}"))
    else:
        issues.append(("WARN", "index.html", "missing '共 N 课 · N 个部分' pill"))

    errs = [i for i in issues if i[0] == "ERR"]
    order = {"ERR": 0, "WARN": 1}
    for sev, f, msg in sorted(issues, key=lambda x: order.get(x[0], 2)):
        print(f"  [{sev}] {f}: {msg}")
    print(f"\nChecked {TOTAL} lessons + index — {len(errs)} error(s), {len(issues) - len(errs)} warning(s).")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
