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
