"""Pins src/m331_yukawa.py: the three weak spots of N_c = N_g = 3 (NOTE_331.md)."""
import os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import m331_yukawa as Y

REF = os.path.join(os.path.dirname(__file__), "..", "results", "unifying_search", "331_yukawa.txt")


def test_yukawa_coefficients_reproduce_sm_top():
    assert Y.sm_top_check() == [F(17, 10), F(3, 2), F(2)]
    assert 0.80 < Y.yt_at(4e3) < 0.85


def test_yukawas_cannot_rescue_nc5():
    yt = Y.yt_at(4e3)
    for v in ("-1/sqrt3", "+1/sqrt3"):
        for yJ in (0.0, 2.0):
            assert Y.blow_up(3, v, yt, yJ) > Y.M_PLANCK > Y.blow_up(5, v, yt, yJ)
        assert Y.blow_up(3, v, yt, 1.0) > Y.blow_up(3, v)          # Yukawas only widen N_c = 3's margin
        assert Y.yJ_to_rescue(5, v, yt) is None                    # not even a constant y_J = 6


def test_weak_angle_dependence():
    lo, hi = Y.s2_band(5, "-1/sqrt3")
    assert abs(lo - 0.0662) < 5e-4 and abs(hi - 0.0742) < 5e-4    # N_c = 5's only band, far from 0.25
    assert Y.s2_band(5, "+1/sqrt3") is None                        # no band at all
    _, s2m, _ = Y.boundary(4e3)
    assert abs(s2m - 0.2504) < 2e-4
    assert abs(Y.s2_upper(3, "+1/sqrt3") - 0.2663) < 5e-4          # the narrow variant's margin
    assert Y.s2_upper(3, "-1/sqrt3") > 0.44


def test_alpha_em_needed_and_reference_output():
    yt = Y.yt_at(4e3)
    assert 1.30 < Y.aem_inv_to_rescue(5, "-1/sqrt3", yt, 1.0) / 125.74 < 1.36
    ref = open(REF).read()
    assert "N_c = 5 reaches Planck only for 0.0662 < s^2 < 0.0742" in ref
    assert "exact: True" in ref
