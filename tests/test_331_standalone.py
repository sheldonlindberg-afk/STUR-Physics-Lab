"""Pins src/m331_standalone.py: the copy-paste script must stay standard-library-only
and agree with the repository's own 3-3-1 modules."""
import ast
import os
import subprocess
import sys

SRC = os.path.join(os.path.dirname(__file__), "..", "src")
PATH = os.path.join(SRC, "m331_standalone.py")
sys.path.insert(0, SRC)
import m331_standalone as S
import m331_exact as E
import m331_threshold as T
import m331_yukawa as Y
from qcd_running import alpha_s_run


def test_imports_only_the_standard_library():
    allowed = {"fractions", "itertools", "math", "time"}
    tree = ast.parse(open(PATH).read())
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            mods.add(node.module.split(".")[0])
    assert mods <= allowed, mods


def test_exact_coefficients_match_the_repository():
    for v in ("-1/sqrt3", "+1/sqrt3"):
        for Nc in (3, 5, 7):
            assert S.coefficients(*S.model(Nc, v)[:3]) == E.coefficients(*E.MODELS[v](Nc)[:3])
            assert S.anomalies(Nc, v) == {k.replace(" (3 - 3bar)", ""): x
                                          for k, x in E.anomalies(Nc, E.MODELS[v]).items()}
            assert [list(x) for x in S.yukawas_331(Nc, v)] == [[float(c) for c in x] for x in Y.yukawas_331(Nc, v)]


def test_running_matches_the_repository():
    for mu in (2.45, 91.1876, 4e3, 3e4):
        assert abs(S.alpha_s(mu) / alpha_s_run(mu) - 1) < 1e-6
    assert abs(S.yt_at(4e3) / Y.yt_at(4e3) - 1) < 1e-5
    yt = Y.yt_at(4e3)
    for v in ("-1/sqrt3", "+1/sqrt3"):
        for Nc in (3, 5):
            assert abs(S.blow_up(Nc, v, yt, 1.0) / Y.blow_up(Nc, v, yt, 1.0) - 1) < 2e-3
    worst = dict(MV=2e3, rJ=0.5, rS=1 / 3, n_light=2)
    assert abs(S.pole(3, "+1/sqrt3", **worst) / T.pole(3, "+1/sqrt3", **worst) - 1) < 2e-3


def test_mass_floor_section_matches_the_repository():
    # S6b (split spectrum, alpha = 1, two loops) against src/m331_margin.py
    import m331_margin as M
    f = S.FLOORS
    for mE in (100.0, 684.0):
        mine = S.pole_split(3, f["MV"], f["mJ"], mE, f["mS"], f["n_light"])
        ref = M.pole(MV=f["MV"], mJ=f["mJ"], mE=mE, mS=f["mS"], n_light=f["n_light"], loops=2)
        assert abs(mine / ref - 1) < 3e-3


def test_runs_isolated_and_every_check_passes():
    code = open(PATH).read().replace("FULL_SCAN = True", "FULL_SCAN = False", 1)
    out = subprocess.run([sys.executable, "-I", "-S", "-c", code], capture_output=True, text=True,
                         timeout=300).stdout
    assert "ALL CHECKS PASS" in out and "FAIL" not in out
    ref = open(os.path.join(os.path.dirname(__file__), "..", "results", "m331", "standalone.txt")).read()
    assert "Checks passed: 23/23" in ref and "ALL CHECKS PASS" in ref
