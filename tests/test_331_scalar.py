"""Pins src/rge_engine.py and src/god_eq_331_scalar.py: the 3-3-1 scalar sector to M_Pl."""
import os, sys
from math import log, pi, sqrt
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import rge_engine as R
import god_eq_331_scalar as S

REF = os.path.join(os.path.dirname(__file__), "..", "results", "god_equation", "331_scalar.txt")


def test_engine_reproduces_standard_model():
    for kw in ({}, dict(lam=0.05, g1=0.5, g2=0.3, g3=0.9, yt=1.3)):
        bl, el, rl, by, ey, ry = R.check_sm(**kw)
        assert abs(bl - el) < 1e-9 and abs(by.real - ey) < 1e-9 and rl < 1e-12 and ry < 1e-12


def test_331_basis_closed_and_cached_fit_exact():
    rng = np.random.default_rng(5)
    for v in S.VARIANTS:
        m = S.Model(v)
        m.cached_fit()
        assert m.gauge_invariance() < 1e-12
        l = rng.uniform(-0.5, 0.5, 9); gX, gL = 0.6, 0.63; ys = rng.uniform(0.2, 0.9, m.K)
        c, res = m.beta_lam_exact(l, gX, gL, ys)
        assert res < 1e-12                                    # the 9-quartic basis is RG-closed
        assert np.abs(m.beta_l(l, gX, gL, ys) - c).max() < 1e-9
        cy, resy = m.beta_y_exact(gX, gL, 1.0, ys)
        assert resy < 1e-12
        assert np.abs(np.concatenate([ys**2, [gX**2, gL**2, 1.0]]) @ m.cy * ys - cy.real).max() < 1e-9
        assert abs(m.cy[0, 0] - 5.0) < 1e-9 and abs(m.cy[-1, 0] + 8.0) < 1e-9     # y_t: 5 y_t^2 - 8 g3^2


def test_yukawa_bound_and_survivor():
    sol = S.sm_running(S.M_PLANCK)
    yt_sm = float(sol.sol(log(4e3 / 172.57))[3])
    m = S.Model("+1/sqrt3"); m.cached_fit()
    g0 = np.sqrt(4 * pi / S.Y.boundary(4e3, lam=tuple(S.T.lambdas(S.T.heavy_spectrum(3, "+1/sqrt3", 4e3), 4e3)))[0])
    assert abs(S.yJ_max(m, yt_sm / sqrt(0.9), g0) - 0.624) < 0.005
    l = np.array([0.158, 0.159, 0.130, 0.128, 0.210, 0.184, 0.143, -0.040, -0.278])   # S4 example
    r = S.run_331(m, l, 0.893, 0.166, g0, rng=np.random.default_rng(0))
    assert r["pert"] and r["stable"]
    ref = open(REF).read()
    assert "m_exotic < 1.79 M_V" in ref and "m_exotic < 1.40 M_V" in ref
