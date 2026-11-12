"""Pins src/stur_tegr_frame.py: the frame's corner symplectic form in linearized TEGR."""
import os, sys
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_tegr_frame as F


def test_frame_is_pure_gauge_in_bulk():
    bad, control = F.frame_is_pure_gauge()
    assert bad == [] and control


def test_corner_form_pairs_boost_with_area():
    div_zero, sol, fixed, names, Wtx, flds = F.corner_form()
    assert div_zero
    pi = sp.pi
    c = sp.symbols("c0:6")
    assert sp.simplify(fixed[c[0]] - 1 / (16 * pi)) == 0 and sp.simplify(fixed[c[2]] + 3 / (64 * pi)) == 0
    assert sp.simplify(fixed[c[3]] - 1 / (64 * pi)) == 0 and sp.simplify(fixed[c[4]] - 1 / (32 * pi)) == 0
    pr, ss = F.pairings(Wtx, flds)
    s1, a1, s2, a2 = flds
    assert ss == 0                                                   # no metric-metric part
    assert sp.expand(pr["a01"] + s2[2][2] + s2[3][3]) == 0           # boost <-> area density
    assert sp.expand(pr["a02"] - (a2[1][2] + s2[1][2])) == 0
    assert sp.expand(pr["a12"] + (a2[0][2] + s2[0][2])) == 0
    assert pr["a23"] == 0                                            # in-surface rotation: gauge


def test_k5_gives_the_same_coefficient():
    assert sp.simplify(F.k5_coefficient() - 1 / (8 * sp.pi)) == 0
