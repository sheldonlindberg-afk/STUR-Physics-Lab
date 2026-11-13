"""Pins src/m331_rho_bound.py: the rho parameter from the 3-3-1 Z-Z' mixing against the global
fit's rho_0 and the LHC Z' bound."""
import math, os, sys
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import m331_rho_bound as R
import m331_breaking as B


def test_b5_coefficient_is_a_perfect_square():
    for v in R.VARIANTS:
        c, closed, ok = R.coefficient(v)
        assert ok, v
    x = sp.Symbol("x", positive=True)
    assert sp.simplify(sum(R.sin2_a0_symbolic(v, x) for v in R.VARIANTS) - 1) == 0


def test_closed_form_matches_exact_diagonalization():
    """B5's own numerical check (exact eigenvalues at v/w = 0.01, a = 0.7) against R1."""
    for v in R.VARIANTS:
        _, rho_num, _ = B.rho_coefficient(v)
        x = 0.79**2 / 0.652**2
        pred = 1 + 0.01**2 * (math.sin(0.7) ** 2 - float(R.sin2_a0_symbolic(v, x))) ** 2
        assert abs(rho_num - pred) < 1e-8, v


def test_where_the_mixing_vanishes():
    assert abs(R.sin2_a0("+1/sqrt3") - 0.3496) < 1e-4 and abs(R.sin2_a0("-1/sqrt3") - 0.6504) < 1e-4
    assert abs(R.s2_tev() - 0.2505) < 1e-4
    assert abs(R.sin2_a0("+1/sqrt3", R.s2_tev()) - 0.333) < 1e-3


def test_rho_bound_is_weaker_than_the_lhc():
    assert abs(R.rho_max() - 7.62e-4) < 1e-6
    for v in R.VARIANTS:
        assert abs(R.w_bound_rho_max(v) / 5.80e3 - 1) < 2e-3
        assert R.w_bound_rho(v, R.sin2_a0(v)) == 0
        wl, MV = R.w_from_zprime(v)
        assert wl / R.w_bound_rho_max(v) > 1.75
    assert abs(R.w_from_zprime("+1/sqrt3")[0] / 11.88e3 - 1) < 3e-3
    assert abs(R.w_from_zprime("-1/sqrt3")[0] / 10.32e3 - 1) < 3e-3
    # same M_V as the 3-3-1 margin scan uses for the LHC bound
    import m331_margin as M
    assert abs(R.w_from_zprime("+1/sqrt3")[1] / M.MV_LHC - 1) < 2e-3


def test_rho_excess_is_only_partly_explained():
    assert abs(R.w_for_central("+1/sqrt3") / 8.1e3 - 1) < 0.01
    assert abs(R.rho_at_lhc("+1/sqrt3") / 1.82e-4 - 1) < 0.01 and abs(R.tension_left("+1/sqrt3") - 1.1) < 0.05
    assert abs(R.rho_at_lhc("-1/sqrt3") / 2.41e-4 - 1) < 0.01 and abs(R.tension_left("-1/sqrt3") - 0.78) < 0.05
