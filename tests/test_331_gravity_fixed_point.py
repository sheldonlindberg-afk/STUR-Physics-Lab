"""Pins src/m331_gravity_fixed_point.py: the asymptotic-safety gravity term above M_Pl and
the 3-3-1 gauge couplings."""
import os, sys
from math import pi
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import m331_gravity_fixed_point as GFP
import m331_three_loop as L
import m331_margin as M


def test_fixed_point_structure():
    g2s, s_star, s_zero, ok = GFP.fixed_points()
    b, f = sp.symbols("b f", positive=True)
    assert sp.simplify(g2s - 16 * sp.pi**2 * f / b) == 0
    assert sp.simplify(s_star - 2 * f) == 0 and sp.simplify(s_zero + f) == 0 and ok


def test_only_gX_is_predicted_for_three_colours():
    for v in GFP.VARIANTS:
        bX, bL, bC = GFP.one_loop_b(3, v)
        assert bX > 0 and bL < 0 and bC < 0
    assert GFP.one_loop_b(3, "+1/sqrt3")[0] == 14 and GFP.one_loop_b(3, "-1/sqrt3")[0] == sp.Rational(26, 3)


def test_gravity_off_is_the_selection():
    """With f* = 0 the new code path gives the selection's own pole (2.89 M_Pl, L3b)."""
    p = L.pole(3, "+1/sqrt3", MV=GFP.MV_REF, gmax=M.ALPHA1, grav=GFP.f_profile(0.0))
    assert abs(p / L.pole(3, "+1/sqrt3", MV=GFP.MV_REF, gmax=M.ALPHA1) - 1) < 1e-9
    assert abs(p / GFP.M_PLANCK - 2.89) < 0.01


def test_separatrix_values():
    fp, fm, fsm = GFP.f_separatrix(1.0, "+1/sqrt3"), GFP.f_separatrix(1.0, "-1/sqrt3"), GFP.f_separatrix_sm(1.0)
    assert abs(fp - 0.2929) < 5e-4 and abs(fm - 0.0203) < 2e-4 and abs(fsm - 0.0098) < 1e-4
    assert 29 < fp / fsm < 31 and 2.0 < fm / fsm < 2.15
    # just above the separatrix everything is finite; just below, U(1)_X hits a pole
    assert GFP.finite(1.01 * fp, 1.0, variant="+1/sqrt3") and not GFP.finite(0.99 * fp, 1.0, variant="+1/sqrt3")
    # the fixed point stays inside the criterion
    assert fp < GFP.f_max(3, "+1/sqrt3") and abs(GFP.f_max(3, "+1/sqrt3") - 14 / (4 * pi)) < 1e-12


def test_excluded_colours_stay_excluded():
    out = GFP.excluded_poles()
    for (v, Nc), (p0, pg) in out.items():
        assert p0 < 1e-3 * GFP.M_PLANCK and abs(pg / p0 - 1) < 1e-6, (v, Nc)


def test_light_heavy_leptons():
    assert GFP.f_separatrix(2.0, "+1/sqrt3", floors=True) is None
    assert GFP.finite(0.73, 0.5, floors=True) and not GFP.finite(0.71, 0.5, floors=True)
