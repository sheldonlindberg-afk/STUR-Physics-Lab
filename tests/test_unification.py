"""Pins the unification-candidate checks in src/stur_unification.py."""
import os, sys
import numpy as np
from scipy.linalg import expm
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_unification as U


def test_visibility_is_parity_of_exchanged_quanta():
    N, al = 200, 0.7
    a = np.diag(np.sqrt(np.arange(1, N)), 1)
    p = np.zeros(N); p[:20] = np.random.default_rng(0).random(20); p /= p.sum()
    D = expm(al * (a.T - a))
    dn = np.arange(N)[:, None] - np.arange(N)[None, :]
    assert abs(np.sum(np.abs(D)**2 * p[None, :] * (-1.0)**dn) - np.trace(D @ D @ np.diag(p)).real) < 1e-12


def test_modular_slope_is_two_pi_over_vF():
    L = 30
    h = U.modular_h(L, dps=90)
    c = L // 2
    v = sum(-r * np.sin(np.pi * r / 2) * h[c - (r + 1) // 2, c - (r + 1) // 2 + r]
            for r in range(1, L, 2) if c - (r + 1) // 2 >= 0 and c - (r + 1) // 2 + r < L)
    assert abs(v / (c * (L - c) / L) - np.pi) < 2e-3


def test_srednicki_area_coefficient():
    S = U.srednicki(N=50, n=10)
    assert abs(S / 10.5**2 - 0.3022) < 2e-3
