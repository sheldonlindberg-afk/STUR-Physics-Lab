"""Pins src/stur_lab_test.py: the trapped-ion kill test for STUR's corollary P2."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_lab_test as L


def test_fock_space_identity():
    for nbar in (0.0, 1.0, 5.0):
        for a2 in (0.02, 0.5):
            V, m, v = L.fock_space(np.sqrt(a2), nbar)
            g = -np.log(V)
            assert abs(g / (2 * a2 * (2 * nbar + 1)) - 1) < 1e-8
            assert abs(2 * v / g - 1) < 1e-8 and abs(m / a2 - 1) < 1e-8


def test_opposite_temperature_dependence():
    for nbar in (0.05, 0.5, 5.0):
        x = np.log(1 + 1 / nbar)
        assert 0 < L.slope_standard(x) <= 1
    x1, x2 = np.log(1 + 1 / 0.1), np.log(1 + 1 / 5.0)
    assert L.gamma_standard(0.1, x2) / L.gamma_standard(0.1, x1) > 9
    assert L.gamma_P2(0.1, x2) / L.gamma_P2(0.1, x1) < 0.08


def test_reference_output_matches():
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        L.main()
    ref = open(os.path.join(os.path.dirname(__file__), "..", "results", "lab_test", "output.txt")).read()
    assert buf.getvalue() == ref
