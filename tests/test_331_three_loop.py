"""Pins src/m331_three_loop.py: validation, convergence, and the beta = +1/sqrt3 margin at three loops."""
import os, sys
from math import pi, sqrt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import m331_three_loop as L


def test_validation_exact():
    assert L.check_two_loop() == 0          # reproduces the note's two-loop coefficients
    assert L.check_three_loop_sm() == 0     # reproduces the SM three-loop gauge beta functions


def test_convergence_breaks_down_before_4pi():
    rows = {round(r[0], 3): r for r in L.convergence_table()}
    g, one, two, three = rows[round(sqrt(4 * pi), 3)]
    assert 0.9 < abs(three / two) < 1.1                       # three-loop ~ two-loop at alpha = 1
    g, one, two, three = rows[round(4 * pi, 3)]
    assert abs(three / one) > 20                              # series useless at g = 4 pi
    assert L.pole(5, "+1/sqrt3", loops=3, gmax=4 * pi) >= 1e45  # spurious fixed point


def test_narrow_variant_margin_three_loop():
    assert abs(L.g_crit_min(3) - 2.870) < 0.01 and abs(L.g_crit_min(2) - 2.954) < 0.01
    assert abs(L.s2_upper(3, sqrt(4 * pi)) - 0.2647) < 0.001


def test_nc5_stays_excluded():
    MPL = L.M_PLANCK
    for variant in ("+1/sqrt3", "-1/sqrt3"):
        assert L.pole(5, variant, loops=3, gmax=sqrt(4 * pi)) < 1e-3 * MPL
