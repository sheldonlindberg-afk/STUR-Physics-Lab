"""Pins src/z3_orbifold_audit.py (Z3_ORBIFOLD.md): the Z3 orbifold engine, kept as proposed in
src/z3_orbifold_engine.py, against the Standard Model's 19 parameters."""
import math
import os
import sys

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import z3_orbifold_audit as A
import z3_orbifold_engine as Z


def test_engine_runs_as_given_and_prints_its_numbers():
    out = A.engine_output()
    assert "R*          = 1.04730" in out and "V''(R*)     = +5.65331" in out
    assert "y_t/y_u = 1.36e+07" in out and "y_b/y_d = 1.15e+07" in out
    assert "Nc=3: Qu=2/3, Qd=-1/3 → SURVIVES" in out and "[PASS]" in out


def test_ledger_has_19_rows_and_seven_outputs():
    assert len(A.LEDGER) == 19 and len({r[0] for r in A.LEDGER}) == 19
    assert A.tally() == {"OUTPUT": 7, "FIXED": 1, "INPUT": 2, "SILENT": 9}
    assert len(A.DIALS) == 16 and len(A.OUTPUTS) == 7


def test_radius_is_an_interior_minimum_and_the_grid_is_close():
    Rg, Vg, Vppg = Z.stabilize_radius()
    Rx, Vppx = A.exact_minimum()
    assert abs(Rx - 1.04771) < 1e-5 and abs(Vppx - 5.63145) < 1e-5
    assert abs(Rg - Rx) < 1.4e-3 and Vg > 0 and Vppx > 0


def test_radius_cancels_from_the_yukawa_matrices():
    """The audit's matrices, built from M R and 8 R alone, are the engine's."""
    assert A.radius_cancels() < 1e-15


def test_engine_svd_is_not_orthogonal_and_its_printed_mixing_is_rounding():
    orth, Ve, Vn, s_err = A.svd_check()
    assert orth > 1e-3 and s_err < 1e-4
    assert abs(Ve[1, 2] - 0.0029) < 1e-4 and abs(Ve[2, 1] - 0.0068) < 1e-4      # as printed
    assert abs(Vn[1, 2] / Vn[2, 1] - 1) < 1e-6 and abs(Vn[1, 2] / 1.065e-5 - 1) < 1e-3


def test_outputs_miss_by_two_to_five_decades():
    x0 = A.default_dials()
    d = A.decades(x0)
    expect = [-4.52, -2.00, -5.05, -4.04, -4.32, -3.51, -4.33]
    assert all(abs(a - b) < 0.01 for a, b in zip(d, expect))
    assert abs(A.rms_decades(x0) - 4.07) < 0.01
    obs = A.observables(x0)
    assert abs(obs[0] / obs[1] - 1.53) < 0.01 and abs(obs[2] / obs[3] - 1.95) < 0.01


def test_real_matrices_give_no_cp_violation():
    Yu, Yd = A.matrices(A.default_dials())
    assert np.isrealobj(Yu) and np.isrealobj(Yd)
    assert dict((r[0], r[1]) for r in A.LEDGER)["delta_CKM"] == "FIXED"


def test_cabibbo_angle_moves_by_decades_for_ten_percent():
    rows = dict(A.sensitivity())
    assert abs(rows["bulk-mass scale (sqrt(V'') x 1.8)"][4] + 1.73) < 0.01
    assert abs(rows["Higgs exponent (8 R*)"][1] + 0.71) < 0.01


def test_one_dial_brings_the_miss_below_one_decade():
    s, m, d = A.one_dial_fit()
    assert abs(s - 1.188) < 0.005 and abs(m - 0.69) < 0.01 and max(abs(d)) < 1.3


def test_six_dials_reach_a_factor_three_not_better():
    x, m, d = A.six_dial_fit()
    assert 0.25 < m < 0.5


def test_section_4_coefficients_against_the_exact_ones():
    for Nc in (3, 5, 7):
        e, x = A.engine_coefficients(Nc), A.exact_coefficients(Nc)
        assert abs(e[1] - x[1]) < 1e-12                      # b_L agrees
        assert abs(e[0] - x[0] - 2 / 3) < 1e-12              # b_X is 2/3 larger at every N_c
    assert abs(A.exact_coefficients(3)[3] + 15.0) < 1e-9 and A.engine_coefficients(3)[3] == -32.0


def test_section_4_verdict_survives_every_variant():
    """The engine's integrator reproduces its printed poles, and N_c = 3 alone survives with
    the engine's coefficients, at one loop, and with the exact coefficients."""
    printed = {r["Nc"]: r["pole"] for r in Z.run_331_selection()}
    for Nc in (3, 5, 7):
        e, x = A.engine_coefficients(Nc), A.exact_coefficients(Nc)
        assert A.euler_pole(*e) == printed[Nc]
        for c in (e, (e[0], e[1], 0.0, 0.0), x):
            assert (A.euler_pole(*c) is None) == (Nc == 3)
    ainv, s2 = A.inputs_at_4tev()
    assert abs(ainv - 125.7) < 0.05 and abs(s2 - 0.2504) < 2e-4


def test_stored_output_is_current():
    stored = open(os.path.join(ROOT, "results", "z3_orbifold", "output.txt")).read()
    for needle in ("root-mean-square miss: 4.07 decades", "OUTPUT: 7, FIXED: 1, INPUT: 2, SILENT: 9",
                   "rms miss 4.07 -> 0.69 decades"):
        assert needle in stored
