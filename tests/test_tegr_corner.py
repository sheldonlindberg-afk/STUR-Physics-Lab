"""Pins src/stur_tegr_corner.py: TEGR vs GR Noether charges, the corner term, and the frame."""
import os, sys
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_tegr_corner as C

r = C.r


def test_pure_gauge_reproduces_e3_reference_connection():
    w = C.pure_gauge(C.spherical_rotation())
    assert w[2][1][2] == 1 and w[1][2][2] == -1
    assert w[3][1][3] == sp.sin(C.th) and w[3][2][3] == sp.cos(C.th)
    assert C.curvature(w) == {}


def test_static_charges_and_corner_term():
    res = C.charges_static()
    f = res["f"]
    assert sp.simplify(res["Q_tegr"] - r * (sp.sqrt(f) - f)) == 0          # N * E_BY
    assert sp.simplify(res["Pi0"] - r * (1 - sp.sqrt(f))) == 0             # E_BY
    assert sp.simplify(res["Q_gr"] - r**2 * sp.diff(f, r) / 4) == 0       # Iyer-Wald
    assert res["diff"] == 0                                                # = corner term
    lim = C.limits_schwarzschild_rn(res)
    assert sp.simplify(lim["Q_tegr_inf"] - lim["M"]) == 0 and lim["Q_tegr_hor"] == 0
    assert sp.simplify(lim["Q_gr_hor"] - lim["kappaA8pi"]) == 0
    assert sp.simplify(lim["corner_hor"] - lim["kappaA8pi"]) == 0
    assert sp.simplify(lim["wald_gr"] - lim["area_quarter"]) == 0


def test_boosted_frame():
    b = C.boosted_frame()
    f, kap = b["f"], b["kappa"]
    assert b["flat"]
    assert sp.simplify(b["Q"] - r * (sp.sqrt(f) - f)) == 0
    assert sp.simplify(b["J_volume"] - kap * r * (1 / sp.sqrt(f) - 1)) == 0


def test_euclidean_winding_replaces_nonflat_e3_test():
    e5 = C.euclidean_winding()
    assert e5["flat"] and len(e5["old_curvature"]) == 4                   # old test: not flat
    tip = C.winding_tip_term(e5)
    M, k = tip["M"], e5["k"]
    assert sp.simplify(tip["ratio"] - (1 + 4 * M * k)) == 0               # (A/4)(1 + k/kappa)
    assert tip["regular_k"] == [-1 / (4 * M)]
    assert tip["flux_inf_k0"] == M and tip["flux_inf_regular"] == sp.oo
