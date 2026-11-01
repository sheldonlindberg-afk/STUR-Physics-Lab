"""Pins front-1 result: holographic dark energy always has CPL wa > 0."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import god_eq_dark_energy as D


def test_hde_wa_positive_for_all_c():
    for c in [0.5, 1.0, 2.0, 5.0]:
        a, w = D.hde_w_of_a(c)
        assert D.cpl_fit(a, w)[1] > 0
