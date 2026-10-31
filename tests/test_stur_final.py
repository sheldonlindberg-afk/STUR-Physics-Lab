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


def test_brane_angle_twist_is_exactly_pi_and_flips_theta():
    # R6: Z2-even periodic V(vartheta) is stationary at 0 and pi; at vartheta = pi
    # with q_psi odd, q_phi even, theta = 0 is the hilltop
    v = np.linspace(-np.pi, np.pi, 4001)
    rng = np.random.default_rng(5)
    for _ in range(200):
        c = rng.normal(0, 1, 4)
        dV = sum(-ck * (k + 1) * np.sin((k + 1) * v) for k, ck in enumerate(c))
        assert abs(dV[2000]) < 1e-12 and abs(dV[0]) < 1e-12
    th = np.linspace(-np.pi, np.pi, 721)
    V = -1.0 * np.cos(th + np.pi) - 0.3 * np.cos(th)
    assert abs(th[V.argmax()]) < 1e-3


def _r7():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "checks"))
    import r7_audit as A
    return A


def test_opposite_domain_rotation_is_alpha_minus_own():
    # R7 A2: an opposite domain rotates reionization light by alpha - beta_own,
    # so a half-and-half shell gives beta_reio = alpha/2 and Delta beta ~ 0
    A = _r7()
    alpha = np.degrees(F.ALPHA)
    assert abs(A.delta_beta(0.05, 0.2, 1.0) - (alpha - 0.05 - 0.2)) < 1e-12
    assert abs(A.delta_beta(0.0, alpha / 2, 0.5)) < 1e-12
    # the round-7 window edge: m = 2e-31 eV, f = 0.085
    assert abs(A.delta_beta(0.0679, 0.2144, 0.085) + 0.1225) < 1e-4


def test_nucleation_window_is_f_over_197():
    # R7 A3: H_nuc < 2 pi f (0.03 pi)/sqrt(60) and H_nuc > 15.06/L
    A = _r7()
    ratio = A.H_C / (2 * np.pi * A.SEED_3PCT / np.sqrt(A.N_EFOLDS))
    assert 196 < ratio < 198


def test_late_potential_has_no_preferred_roll_direction():
    # R7 A1: V = m^2 f^2 (1 + cos theta) is even, so the sign of beta follows
    # theta_i in our region; beta_rec still has one sign on our whole sky
    th = np.linspace(-np.pi, np.pi, 2001)
    V = 1 + np.cos(th)
    assert np.max(np.abs(V - V[::-1])) < 1e-12
    th_i = 1e-3 * np.random.default_rng(0).standard_normal(1000)
    b = F.ALPHA / (2 * np.pi) * (np.pi - th_i)
    assert np.all(b > 0)
