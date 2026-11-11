"""Pins src/m331_threshold.py: one-loop threshold matching at the 3-3-1 scale."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import m331_threshold as T

REF = os.path.join(os.path.dirname(__file__), "..", "results", "m331", "331_threshold.txt")


def test_one_loop_matching_scale_independence():
    for v in ("-1/sqrt3", "+1/sqrt3"):
        ps = [T.pole(3, v, 4e3, 2.0, 0.5, 1, mu=4e3 * k, loops=1) for k in (1 / 3, 1, 3)]
        assert np.ptp(np.log(ps)) < 1e-8                       # thresholds compensate the logs exactly
    ps = [T.pole(3, "+1/sqrt3", 4e3, 2.0, 0.5, 1, mu=4e3 * k, loops=1, thresholds=False) for k in (1 / 3, 3)]
    assert ps[1] / ps[0] > 2                                   # tree-level matching does not


def test_heavy_content_and_constants():
    for v in ("-1/sqrt3", "+1/sqrt3"):
        assert np.allclose(T.lambdas(T.heavy_spectrum(3, v, 4e3), 4e3), [1, 1, 0])   # MS-bar vector constant
    assert abs(T.mzp_over_mv(0.2504) - 1.225) < 1e-3


def test_verdict_at_the_worst_spectrum():
    worst = dict(MV=2e3, rJ=0.5, rS=1 / 3, n_light=2)
    assert T.pole(3, "+1/sqrt3", **worst) / T.M_PLANCK > 1.5
    assert T.pole(3, "+1/sqrt3", MV=4e3, rJ=0.5, rS=1 / 3, n_light=2) / T.M_PLANCK > 2.0
    best5 = max(T.pole(5, "+1/sqrt3", 1e4, 3.0, 3.0, 1, mu=3e4), T.pole(5, "-1/sqrt3", 1e4, 3.0, 3.0, 1, mu=3e4))
    assert best5 < 1e-3 * T.M_PLANCK


def test_margin_and_reference_output():
    u = T.s2_upper_thr("+1/sqrt3", MV=4e3, rJ=0.5, rS=1 / 3, n_light=2)
    assert abs(u - 0.2608) < 5e-4
    ref = open(REF).read()
    assert "Margin range +0.0104 to +0.0347" in ref and "only N_c = 3 survives" in ref
