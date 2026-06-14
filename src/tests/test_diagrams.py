import diagrams as d
from i18n import L


def test_fig_wraps_with_caption():
    h = d.fig("<x>", caption=L("图注", "cap"))
    assert h.startswith('<div class="fig">') and "figcap" in h
    assert 'data-lang="en">cap' in h


def test_flow_boxes_arrows_and_active():
    h = d.flow([("a", L("甲", "A")), ("b", L("乙", "B"), L("注", "note"))], active="b")
    assert h.count('class="fbox') == 2
    assert "fbox on" in h            # active highlighted
    assert "farrow" in h            # arrow between boxes
    assert "fsub" in h              # the note on box b
    assert 'data-lang="en">A' in h and 'data-lang="en">B' in h


def test_vflow_down_arrows_and_produces():
    h = d.vflow([(L("加载", "Load"), L("→Documents", "→Documents")), (L("切块", "Split"),)])
    assert h.count("fvbox") == 2
    assert "fvarrow" in h           # one down-arrow between 2 stages
    assert "fprod" in h             # the 'produces' label


def test_layers_stack():
    h = d.layers([(L("core", "core"), L("抽象", "abstractions")), (L("集成", "integrations"),)])
    assert h.count("flayer") == 2
    assert "fllabel" in h and "flstack" in h


def test_annot_center_and_callouts():
    h = d.annot(L("Node", "Node"), [(L("metadata", "metadata"), L("键值", "key-values"))])
    assert "fcenter" in h and "fcall" in h
    assert 'data-lang="en">metadata' in h


def test_compare2_two_columns():
    h = d.compare2((L("左", "L"), "<p>a</p>"), (L("右", "R"), "<p>b</p>"))
    assert h.count('class="fcol"') == 2 and "fvs" in h
    assert "<p>a</p>" in h and "<p>b</p>" in h


def test_grid_shape():
    h = d.grid([L("h1", "h1"), L("h2", "h2")], [[L("a", "a"), L("b", "b")]])
    assert h.count("fgh") == 2 and h.count("fgc") == 2
    assert "repeat(2,1fr)" in h


def test_scatter_svg_and_legend():
    pts = [(20, 20, L("d1", "d1")), (80, 80, L("d2", "d2")), (25, 30, L("d3", "d3"))]
    h = d.scatter(pts, (22, 22), k=2)
    assert "<svg" in h and h.count("fsdot") == 3
    assert "fsq" in h and "fsknn" in h          # query dot + knn circle
    assert h.count("near") >= 2                 # k nearest highlighted
    assert "fslegend" in h


def test_diagram_css_present():
    assert ".fig" in d.DIAGRAM_CSS and ".fbox" in d.DIAGRAM_CSS and ".fscatter" in d.DIAGRAM_CSS


def test_no_third_party_imports():
    import ast
    import pathlib

    tree = ast.parse(pathlib.Path("diagrams.py").read_text(encoding="utf-8"))
    mods = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            mods += [a.name.split(".")[0] for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            mods.append((n.module or "").split(".")[0])
    assert set(mods) <= {"i18n", "math"}
