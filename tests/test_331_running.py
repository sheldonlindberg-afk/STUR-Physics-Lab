"""Pins the 3-3-1 selection steps of NOTE_331.md: charges, generations, SU(3)_L and U(1)_X running, two loops."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_why_three():
    import m331_why_three as W
    import sympy as sp
    Qu, Qd, cub = W.charges(3)
    assert (Qu, Qd, cub) == (sp.Rational(2, 3), sp.Rational(-1, 3), 0)
    Qu5, Qd5, cub5 = W.charges(5)
    assert cub5 == 0 and 5 * (Qu5**2 - Qd5**2) == 1          # pi0 amplitude blind to N_c


def test_three_generations():
    import m331_three_generations as T
    from scipy.optimize import brentq
    assert [r[0] for r in T.allowed_Ng(3) if r[2]] == [3]
    assert [r[0] for r in T.allowed_Ng(5) if r[2]] == [5]
    mu = brentq(lambda m: T.sin2_running(m) - 0.25, 100, 1e6)
    assert 3.5e3 < mu < 3.9e3


def test_su3L_and_hypercharge_selection():
    import m331_su3L_running as L
    assert L.landau(5)[1] is None and L.landau(7)[1] < L.M_PLANCK      # SU(3)_L cuts N_c >= 7
    from fractions import Fraction
    assert L.bY(3, False) == Fraction(-41, 6)                          # reproduces the SM
    assert L.bY_pole(3)[1] > L.M_PLANCK > L.bY_pole(5)[1]               # hypercharge cuts 5 (estimate)


def test_331_exact_two_loop():
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
    from fractions import Fraction as F
    import m331_exact as E
    a, b = E.sm_check()
    assert a == [F(41, 10), F(-19, 6), F(-7)]
    assert b == [[F(199, 50), F(27, 10), F(44, 5)], [F(9, 10), F(35, 6), F(12)], [F(11, 10), F(9, 2), F(-26)]]
    for Nc in (3, 5, 7):
        assert all(v == 0 for v in E.anomalies(Nc).values())
    assert E.run_two_loop(3)[0] > E.M_PLANCK > E.run_two_loop(5)[0]


def test_331_plus_variant():
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
    import m331_exact as E
    for Nc in (3, 5, 7):
        assert all(v == 0 for v in E.anomalies(Nc, E.model_331_plus).values())
    assert E.run_two_loop(3, model=E.model_331_plus)[0] > E.M_PLANCK > E.run_two_loop(5, model=E.model_331_plus)[0]
