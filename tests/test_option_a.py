"""Pins option A (area-law gravitational decoherence) numbers."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_option_a as A


def test_area_law_limit():
    assert abs(A.check_profile() - 1) < 1e-4


def test_kovachy_bound_and_magis_signal():
    kmax = 1.0 / ((87 * A.amu / A.hbar) ** 2 * A.A_mz(0.54, 1.04))
    assert 9.4e-19 < kmax < 9.6e-19
    assert abs(A.gamma(87, kmax, A.A_mz(1.0, 2.0)) - 3.56) < 0.01
