"""Pins src/stur_emergent.py: gravity as a consequence of the quantum level."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_emergent as K


def test_cutoff_for_G():
    assert abs(K.cutoff_for_G(1) / K.L_P - 0.311) < 1e-3
    assert abs(K.cutoff_for_G(100) / K.L_P - 3.114) < 2e-3


def test_emergent_one_over_r():
    prof = K.green_profile(L=61, r_ref=10, rs=(4, 6))
    ratios = [g / c for _, g, c in prof]
    assert all(abs(x - 1) < 0.04 for x in ratios) and ratios[1] < ratios[0]


def test_collective_medium_entangles_mean_field_does_not():
    slow = K.medium_evolution(L=10, t_ramp=30.0, t_hold=60.0, nt=3000)
    assert abs(slow["dphi"] / slow["static"] - 1) < 0.02
    assert slow["neg"] > 0.01 and slow["record"] > 0.999
    mf = K.medium_evolution(L=10, t_ramp=30.0, t_hold=60.0, nt=3000, mean_field=True)
    assert abs(mf["dphi"]) < 1e-12 and mf["neg"] < 1e-12
    sud = K.medium_evolution(L=10, t_hold=60.0, nt=3000, sudden=True)
    assert sud["record"] < slow["record"]


def test_dp_rate():
    m = 1.5e-14
    R = K.ge.radius(m)
    assert abs(K.dp_rate(m, R, 721e-6) - 170) < 2
    assert K.dp_crystal_extra(m) < 1e-4
