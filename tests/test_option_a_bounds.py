"""Pins the LISA Pathfinder bound on option A at small xi (Monte Carlo, seeded)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_option_a_bounds as B


def test_lpf_bound_small_xi():
    k = (1.74e-15) ** 2 / 2 / B.lpf_Q_per_kappa(1e-6, 0.38, n=200000)
    assert 2.5e-32 < k < 3.1e-32
    G = k * B.gamma_per_kappa(87, 3.0, 4.0, 1e-6)
    assert G < 1e-11                                       # unobservable
