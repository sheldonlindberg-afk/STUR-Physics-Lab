"""Pins src/m331_coupling_map.py: the selection as a map of coupling space (NOTE_331.md, 4a)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import m331_coupling_map as C
import m331_exact as E


def test_measured_point():
    s2, ainv, a3 = C.measured()
    assert abs(s2 - 0.2505) < 2e-4 and abs(ainv - 125.7) < 0.1
    for v in E.MODELS:
        assert C.survives(3, 3, v, s2, ainv, a3) and not C.survives(5, 5, v, s2, ainv, a3)
    assert C.survives(2, 4, "-1/sqrt3", s2, ainv, a3) and not C.survives(2, 4, "+1/sqrt3", s2, ainv, a3)


def test_regions_are_nested_and_three_is_largest():
    for v in E.MODELS:
        reg = C.region(v, n=8, models=[(3, 3), (5, 5), (7, 7), (3, 6)])
        frac, nested, alone = C.summary(reg)
        assert nested and frac[(3, 3)] > frac[(5, 5)] > frac[(7, 7)] >= frac[(3, 6)] == 0
        assert 0.4 < alone < 0.8


def test_weaker_alpha_em_lets_five_colours_through():
    s2, ainv, a3 = C.measured()
    assert C.survives(5, 5, "-1/sqrt3", s2, 1.5 * ainv, a3)       # NOTE_331 section 4: needs 1.33 x weaker
    assert not C.survives(5, 5, "-1/sqrt3", s2, 1.2 * ainv, a3)
