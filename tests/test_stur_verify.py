"""Regression tests for src/stur_verify.py.

Run from the repository root:  python -m pytest tests/ -q
The script prints every number quoted in the derivation record; its full
output must match results/stur_verify_output.txt exactly (~20 s).
"""
import os
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")


def test_output_matches_reference_exactly():
    out = subprocess.run(
        [sys.executable, os.path.join(ROOT, "src", "stur_verify.py")],
        capture_output=True, text=True, check=True,
    ).stdout
    with open(os.path.join(ROOT, "results", "stur_verify_output.txt")) as f:
        expected = f.read()
    assert out == expected


def test_smarr_half_is_analytic():
    # E_R = T_H * S_BH = Mc^2 / 2 independently of M (Smarr: Mc^2 = 2TS)
    G, c, hbar, kB = 6.67430e-11, 2.99792458e8, 1.054571817e-34, 1.380649e-23
    for m in (1e27, 2e30, 1e40):
        T = hbar * c**3 / (8 * 3.141592653589793 * G * m * kB)
        S = kB * 4 * 3.141592653589793 * G * m**2 / (hbar * c)
        assert abs(T * S / (m * c**2) - 0.5) < 1e-12
