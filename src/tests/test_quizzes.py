import quizzes
from i18n import L


def test_render_unknown_is_empty():
    assert quizzes.render("does-not-exist.html") == ""


def test_render_seeded_lesson_has_question_and_options():
    html = quizzes.render("01-what-is-llamaindex.html")
    assert 'class="selftest"' in html
    assert html.count('<li>') >= 4            # >=1 MCQ with >=4 options
    assert "<details" in html                  # answer reveal
    assert 'data-lang="en"' in html            # bilingual content present


def test_shuffle_is_deterministic_and_preserves_answer():
    opts = [L("a"), L("b"), L("c"), L("d")]
    s1, a1 = quizzes._shuffle(opts, 2, "seed-x")
    s2, a2 = quizzes._shuffle(opts, 2, "seed-x")
    assert [o.zh for o in s1] == [o.zh for o in s2]   # stable
    assert s1[a1].zh == opts[2].zh                      # answer tracks option


def test_render_interview_block_with_collapsible_answer():
    quizzes.QUIZZES["__t-iv.html"] = {
        "interview": [
            {"q": L("为什么用 Node 而不是整篇 Document？", "Why Node, not the whole Document?"),
             "answer": L("要点：① 检索粒度；② 溯源。", "Key points: (1) retrieval granularity; (2) provenance.")},
        ],
    }
    try:
        html = quizzes.render("__t-iv.html")
    finally:
        del quizzes.QUIZZES["__t-iv.html"]
    assert 'class="quiz interview"' in html              # the interview block
    assert "面试官提问" in html                            # group heading
    assert "为什么用 Node" in html                         # the question
    assert "<details" in html                             # collapsible answer
    assert "检索粒度" in html                              # the answer key-points
    assert 'data-lang="en"' in html                       # bilingual


def test_render_without_interview_omits_block():
    quizzes.QUIZZES["__t-noiv.html"] = {
        "mcq": [{"q": L("问", "q"), "opts": [L("甲", "a"), L("乙", "b")], "answer": 0, "why": L("因", "w")}],
    }
    try:
        html = quizzes.render("__t-noiv.html")
    finally:
        del quizzes.QUIZZES["__t-noiv.html"]
    assert 'class="selftest"' in html                     # still renders
    assert 'class="quiz interview"' not in html           # no interview block
    assert "面试官提问" not in html
