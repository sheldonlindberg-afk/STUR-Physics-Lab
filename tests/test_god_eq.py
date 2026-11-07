"""Pins front-1 result: holographic dark energy always has CPL wa > 0."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import god_eq_dark_energy as D


def test_hde_wa_positive_for_all_c():
    for c in [0.5, 1.0, 2.0, 5.0]:
        a, w = D.hde_w_of_a(c)
        assert D.cpl_fit(a, w)[1] > 0


def test_running_vacuum_quadrant_and_cmb_limit():
    import god_eq_running_vacuum as R
    _, _, _, w0, wa = R.rvm_weff(0.01)
    assert w0 > -1 and wa < 0                         # DESI quadrant for nu > 0
    _, _, _, w0, wa = R.rvm_weff(4.8e-4)
    assert abs(w0 + 1) < 1e-3 and abs(wa) < 0.01      # negligible at the CMB-allowed nu


def test_fold_spin_and_baryon_nogo():
    import itertools
    import god_eq_quark_fold as F
    assert abs(F.thomson_J(1.0) - 1 / (4 * 3.141592653589793)) < 1e-9
    assert not [c for c in itertools.product(range(-7, 8, 2), repeat=3) if sum(c) == 0]


def test_spin_charge_twist():
    import numpy as np
    import god_eq_spin_charge as S
    assert S.mismatch(0, 0, 0, 3 * np.pi, S.FIELDS) < 1e-9       # exp(3 pi i (B-L)) = (-1)^2J
    assert S.mismatch(1, 0, 0, np.pi, S.FIELDS) < 1e-9           # colour centre + B-L pi
    sm = [f for f in S.FIELDS if f[0] != "S(B-L=2)"]
    best = min(S.mismatch(a, b, c, 0.0, sm) for a in range(3) for b in range(2)
               for c in np.linspace(0, 6, 6001))
    assert best > 1.9                                            # none without B-L


def test_why_three():
    import god_eq_why_three as W
    import sympy as sp
    Qu, Qd, cub = W.charges(3)
    assert (Qu, Qd, cub) == (sp.Rational(2, 3), sp.Rational(-1, 3), 0)
    Qu5, Qd5, cub5 = W.charges(5)
    assert cub5 == 0 and 5 * (Qu5**2 - Qd5**2) == 1          # pi0 amplitude blind to N_c


def test_three_generations():
    import god_eq_three_generations as T
    from scipy.optimize import brentq
    assert [r[0] for r in T.allowed_Ng(3) if r[2]] == [3]
    assert [r[0] for r in T.allowed_Ng(5) if r[2]] == [5]
    mu = brentq(lambda m: T.sin2_running(m) - 0.25, 100, 1e6)
    assert 3.5e3 < mu < 3.9e3


def test_su3L_and_hypercharge_selection():
    import god_eq_su3L_running as L
    assert L.landau(5)[1] is None and L.landau(7)[1] < L.M_PLANCK      # SU(3)_L cuts N_c >= 7
    from fractions import Fraction
    assert L.bY(3, False) == Fraction(-41, 6)                          # reproduces the SM
    assert L.bY_pole(3)[1] > L.M_PLANCK > L.bY_pole(5)[1]               # hypercharge cuts 5 (estimate)
