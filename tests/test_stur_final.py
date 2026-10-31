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


def test_kk_coupling_closed_form():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "checks"))
    import refinement_r1 as R
    for Mr in (0.2, 2.0):
        assert abs(R.cg_sum(1.0, Mr, 20000000) - R.cg_exact(1.0, Mr)) < 1e-7
    # one full period of theta shifts the theta-term by exactly pi
    t = np.linspace(0, 2 * np.pi, 20001)
    per = np.trapezoid([R.cg_exact(x, 0.3) for x in t], t)
    assert abs(per / np.pi - 1) < 1e-6


def test_roll_integral_is_exactly_half_pi():
    # R2.2: Phi(pi) - Phi(0) = (pi/2) sgn M for any M r -> beta = k alpha/2 exactly
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "checks"))
    import refinement_r1 as R
    t = np.linspace(0, np.pi, 40001)
    for Mr in (0.05, 0.3, 2.0):
        val = np.trapezoid([R.cg_exact(x, Mr) for x in t], t)
        assert abs(val / (np.pi / 2) - 1) < 1e-6


def test_birth_point_is_one_loop_minimum():
    # R4.A: smooth-cap birth (bosons periodic, fermions antiperiodic) is the
    # minimum of every one-loop Wilson-line contribution
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "checks"))
    import r4_torsion as T
    x = np.linspace(-np.pi, np.pi, 241)
    for a in (0.0, 1.0, 5.0):
        assert np.argmin(T.one_loop(x, a, 0, 0.0)) == 120
        assert np.argmin(T.one_loop(x, a, 1, np.pi)) == 120


def test_orbifold_positivity_of_brane_terms():
    # R5.L2: Z2-even brane terms on the orbifold keep Tr T > 0
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "checks"))
    import r5_lagrangian as L5
    rng = np.random.default_rng(3)
    for _ in range(2000):
        M, p, L = rng.uniform(0, 5), rng.uniform(0, 5), rng.uniform(0.1, 3)
        a0, b0, a1, b1 = rng.normal(0, 3, 4)
        P = L5.expm_sym(M * L / 2, p * L / 2)
        T = P @ L5.expm_sym(a1, b1) @ P @ L5.expm_sym(a0, b0)
        assert np.trace(T) > 0
