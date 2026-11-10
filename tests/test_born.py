"""Pins src/stur_born.py: the Born rule from envariance, additivity, no-signaling, frequencies."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_born as B


def test_envariance():
    a, b, c = B.envariance_equal()
    assert abs(a - np.sqrt(2)) < 1e-12 and b < 1e-12 and c < 1e-12
    for m, M in [(1, 3), (3, 7)]:
        nz, worst, p0, c2 = B.fine_grain(m, M)
        assert np.allclose(nz, 1 / np.sqrt(M)) and worst < 1e-12 and abs(p0 - c2) < 1e-12


def test_rival_rules_inconsistent():
    for q in (0.5, 2.0):
        coarse, fine = B.rival_rule_inconsistency(2, 5, q)
        assert abs(coarse - fine) > 0.04


def test_only_x_is_additive():
    assert B.additivity_violation(1.0, trials=2000) < 1e-12
    assert B.additivity_violation(0.9, trials=2000) > 0.05


def test_no_signaling_only_for_born():
    assert B.signaling(1.0, trials=100) < 1e-12
    assert B.signaling(2.0, trials=100) > 0.05


def test_frequencies():
    w = [B.atypical_weight(N, 0.4) for N in (100, 1000, 10000)]
    assert w[0] > w[1] > w[2] and w[2] < 1e-20
