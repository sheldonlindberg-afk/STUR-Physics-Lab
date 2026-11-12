"""Pins src/stur_tegr3d.py: 3D TEGR identity, exact 6j, Ponzano-Regge, Biedenharn-Elliott."""
import os, sys
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_tegr3d as U


def test_identity_3d_exact():
    for d, t, r in U.identity_3d():
        assert d == 0 and abs(t) > 1e-4 and abs(r) > 1e-2


def test_sixj_exact_values():
    assert abs(U.sixj(1, 1, 1, 1, 1, 1) - 1 / 6) < 1e-15
    assert U.sixj(1, 1, 3, 1, 1, 1) == 0.0                       # triangle fails
    assert U.check_against_sympy() < 1e-14


def test_ponzano_regge_asymptotics():
    rows = U.pr_scan()
    assert abs(rows[0][3] - 1.0e-2) < 1e-3                       # k = 2: 1% of the envelope
    assert all(r[3] < 1.2e-3 for r in rows[1:])                  # k >= 5
    assert abs(rows[3][1] - 3.982143e-04) < 1e-9                 # exact 6j at k = 20, pinned
    rms, n = U.pr_rms()
    assert n == 49 and rms < 1e-3


def test_biedenharn_elliott_and_orthogonality():
    worst, hits = U.be_check()
    assert hits == 40 and worst < 1e-14
    ps, M = U.orthogonality(1, F(3, 2), 1, F(3, 2))
    assert len(ps) == 3 and np.abs(M - np.eye(3)).max() < 1e-13
