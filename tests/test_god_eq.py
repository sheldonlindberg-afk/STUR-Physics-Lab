"""Pins front-1 result: holographic dark energy always has CPL wa > 0."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import god_eq_dark_energy as D


def test_hde_wa_positive_for_all_c():
    for c in [0.5, 1.0, 2.0, 5.0]:
        a, w = D.hde_w_of_a(c)
        assert D.cpl_fit(a, w)[1] > 0


def test_running_vacuum_quadrant_and_cmb_limit():
    import god_eq_running_vacuum as R
    _, _, _, w0, wa = R.rvm_weff(0.01)
    assert w0 > -1 and wa < 0                         # DESI quadrant for nu > 0
    _, _, _, w0, wa = R.rvm_weff(4.8e-4)
    assert abs(w0 + 1) < 1e-3 and abs(wa) < 0.01      # negligible at the CMB-allowed nu
