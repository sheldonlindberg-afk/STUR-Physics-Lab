"""Pins src/stur_thermo_gravity.py: statistical gravity's minimum noise and its consequences."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_thermo_gravity as T


def test_minimum_is_diosi_penrose_kernel():
    for q in (1e2, 1e8, 1e14):
        val, kk = T.min_total_kernel(q)
        assert abs(val / (4 * np.pi * T.G / (T.hbar * q**2)) - 1) < 1e-9
        assert abs(kk - 1) < 1e-4


def test_diamond_rate_limits():
    exact = T.G * T.M_A**2 / T.hbar * (6 / (5 * T.R_A) - 1 / T.D_A)
    assert abs(T.rate(0.0) / exact - 1) < 1e-3 and abs(exact - 169.5) < 0.1
    for R0 in (2e-4, 1e-3):
        assert abs(T.rate(R0) / T.rate_point_gauss(R0) - 1) < 1e-3


def test_cutoff_heating_and_required_smearing():
    assert abs(T.cutoff(1) / T.lP - 0.311) < 0.001
    assert 1e60 < T.heating_per_kg(T.cutoff(1)) < 1e61
    assert 5e-15 < T.heating_per_kg(T.R0_DONADI) < 8e-15
    assert T.R0_DONADI / T.cutoff(1000) > 1e23


def test_reference_output_matches():
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        R_need = T.main()
    assert 440e-6 < R_need < 470e-6 and R_need > 8 * T.L_ISL
    ref = open(os.path.join(os.path.dirname(__file__), "..", "results", "thermo_gravity", "output.txt")).read()
    assert buf.getvalue() == ref
