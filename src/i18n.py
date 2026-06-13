"""Bilingual content model for the LlamaIndex RAG visual guide.

Author content once with both Chinese and English. Each bilingual fragment is
emitted as a pair of elements tagged ``data-lang="zh"`` / ``data-lang="en"``.
Visibility is driven entirely by CSS keyed on the root element's
``data-uilang`` attribute (baked as ``zh`` at build time), so with JavaScript
disabled exactly one language (Chinese) still shows. The top-bar toggle flips
``data-uilang`` and remembers the choice in ``localStorage``.
"""


class L:
    """A bilingual fragment whose ``zh`` / ``en`` are HTML strings.

    ``en`` falls back to ``zh`` when omitted, so partially-translated content
    never renders an empty block.
    """

    __slots__ = ("zh", "en")

    def __init__(self, zh, en=None):
        self.zh = zh
        self.en = zh if en is None else en

    def render(self, block=True):
        tag = "div" if block else "span"
        return (
            f'<{tag} data-lang="zh">{self.zh}</{tag}>'
            f'<{tag} data-lang="en">{self.en}</{tag}>'
        )


def render(node, block=True):
    """Render an :class:`L`; pass plain strings through unchanged."""
    if isinstance(node, L):
        return node.render(block=block)
    return str(node)


def t(zh, en=None):
    """Inline bilingual span for short labels (nav, pills, buttons)."""
    return L(zh, en).render(block=False)


# CSS: hide all bilingual blocks, reveal the one matching the root data-uilang.
LANG_CSS = (
    "[data-lang]{display:none}\n"
    'html[data-uilang="zh"] [data-lang="zh"]{display:revert}\n'
    'html[data-uilang="en"] [data-lang="en"]{display:revert}\n'
)

# Inline script: restore saved language, wire the toggle button(s), keep
# <html lang>, the toggle label and document.title in sync.
LANG_TOGGLE_JS = r"""
(function () {
  var root = document.documentElement;
  var KEY = 'li-guide-lang';
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  var lang = (saved === 'en' || saved === 'zh') ? saved : 'zh';
  apply(lang);
  function apply(l) {
    root.setAttribute('data-uilang', l);
    root.setAttribute('lang', l === 'en' ? 'en' : 'zh-CN');
    var btns = document.querySelectorAll('[data-lang-toggle]');
    for (var i = 0; i < btns.length; i++) {
      btns[i].textContent = (l === 'zh') ? 'EN' : '中';
      btns[i].setAttribute('aria-label', l === 'zh' ? 'Switch to English' : '切换到中文');
    }
    var ti = root.getAttribute(l === 'en' ? 'data-title-en' : 'data-title-zh');
    if (ti) document.title = ti;
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-lang-toggle]') : null;
    if (!b) return;
    var next = (root.getAttribute('data-uilang') === 'zh') ? 'en' : 'zh';
    try { localStorage.setItem(KEY, next); } catch (e) {}
    apply(next);
  });
})();
"""
