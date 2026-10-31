"""Regression and sanity tests for src/stur_final.py.

Run from the repository root:  python -m pytest tests/ -q
The full-output test reruns the whole pipeline (~30 s).
"""
import contextlib
import io
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_final as F  # noqa: E402


def test_coupling_normalisation_is_one_half():
    # Section A: one charge-1 Dirac fermion's KK tower gives c_g = 1/2 sgn M
    assert abs(F.kk_coupling(2.0) - 0.5) < 1e-4


def test_headline_prediction_is_alpha_over_two():
    ideal = np.degrees(F.ALPHA) / 2
    assert abs(ideal - 0.2091) < 5e-5
    frac, beta_rec, _ = F.roll(1e-30, 1e-4)
    assert abs(frac - 1) < 0.01          # theta lands at pi
    assert abs(beta_rec - ideal) / ideal < 0.01


def test_prediction_within_two_sigma_of_joint_measurement():
    _, beta_rec, _ = F.roll(1e-30, 1e-4)
    b0, s0 = F.BETA_DATA["joint2026 (ACT DR6+Planck)"]
    assert abs(beta_rec - b0) < 2 * s0


def test_full_output_matches_expected():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        F.main()
    got = [line.rstrip() for line in buf.getvalue().strip().splitlines()]
    exp = [line.rstrip() for line in F.EXPECTED_OUTPUT.strip().splitlines()]
    assert got == exp
