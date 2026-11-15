"""The repository's 3-3-1 beta-function coefficients against PyR@TE 3 (an external package).

tools/pyrate_crosscheck.py ran PyR@TE on model files generated from src/m331_core.py and
stored its output in results/m331/pyrate/pyrate_crosscheck.json. This test compares that
stored output, exactly, with what the repository computes; it does not need PyR@TE."""
import json
import os
import sys
from fractions import Fraction as F

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import numpy as np
import m331_core as C
import m331_three_loop as L

DATA = json.load(open(os.path.join(ROOT, "results", "m331", "pyrate", "pyrate_crosscheck.json")))


def test_covers_both_variants_and_three_colour_cases():
    assert {(r["variant"], r["Nc"], r["Ng"]) for r in DATA["rows"]} == {
        (v, Nc, Ng) for v in C.VARIANTS for Nc, Ng in ((3, 3), (5, 5), (2, 4))}
    assert DATA["pyrate_commit"].startswith("04b219c")


def test_one_and_two_loop_gauge_coefficients_agree_exactly():
    for r in DATA["rows"]:
        a, b = C.coefficients(*C.model(r["Nc"], r["variant"], r["Ng"])[:3])
        assert [F(x) for x in r["a"]] == a
        assert [[F(x) for x in row] for row in r["b"]] == b


def test_two_loop_yukawa_coefficients_agree_exactly():
    for r in DATA["rows"]:
        Nc, v = r["Nc"], r["variant"]
        gs, _, _, (Xt, Xa, Qu, Qd, Ng, nA) = C.model(Nc, v, r["Ng"])
        QT, QD = (Qu, Qd) if v == "-1/sqrt3" else (Qd, Qu)
        Q, S, y = (None, 3, Nc), (None, 1, Nc), r["yukawa"]
        assert [F(x) for x in y["yt2"]] == C.yukawa_coeff(gs, (Q, Xt), (S, -Qu), 3 * Nc)
        assert [F(x) for x in y["yT2"]] == C.yukawa_coeff(gs, (Q, Xt), (S, -QT), 3 * Nc)
        assert [F(x) for x in y["trYD"]] == C.yukawa_coeff(gs, (Q, Xa), (S, -QD), 3 * Nc)
        if v == "+1/sqrt3":
            lep = C.yukawa_coeff(gs, ((None, 3, 1), F(-2, 3)), ((None, 1, 1), F(1)), 3)
            assert [F(x) for x in y["trYE"]] == lep


def test_three_loop_gauge_coefficients_agree():
    for r in DATA["rows"]:
        theirs = np.array([[[float(F(x)) for x in row] for row in m] for m in r["c"]])
        mine = L.c3_tensor(r["Nc"], r["variant"], r["Ng"]) / 2      # m331_three_loop stores twice the coefficient
        assert np.abs(theirs - mine).max() < 1e-12 * np.abs(mine).max()


def test_stored_model_files_are_what_the_tool_writes():
    import pyrate_crosscheck as X
    for r in DATA["rows"]:
        for yuk, suffix in ((True, ""), (False, "_gauge")):
            name = f"m331_{X.TAG[r['variant']]}_Nc{r['Nc']}_Ng{r['Ng']}{suffix}.model"
            assert open(os.path.join(X.OUT_DIR, name)).read() == X.model_file(r["Nc"], r["variant"], r["Ng"], yuk)
