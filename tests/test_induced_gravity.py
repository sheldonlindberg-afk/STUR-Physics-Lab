"""Pins src/induced_gravity.py: Newton's constant induced by stage 1's matter at its U(1)_X pole."""
import math
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import induced_gravity as I

RES = I.main()


def test_counts_from_stage1():
    assert RES[("counts", "-1/sqrt3")] == (17, 66, 18)
    assert RES[("counts", "+1/sqrt3")] == (17, 69, 18)


def test_supertrace_exact():
    assert RES[("str", "-1/sqrt3", F(0))] == F(8, 3)
    assert RES[("str", "-1/sqrt3", F(1, 6))] == F(-1, 3)
    assert RES[("str", "+1/sqrt3", F(0))] == F(19, 6)
    assert RES[("str", "+1/sqrt3", F(1, 6))] == F(1, 6)


def test_sign_matches_larsen_wilczek():
    """Larsen-Wilczek sec. 3.3: one minimal scalar gives 1/G = +(1/2 pi)(1/6) kappa^2."""
    assert abs(I.kappa_needed(F(1, 6)) / (I.mpl() * math.sqrt(12 * math.pi)) - 1) < 1e-12
    k = 1e19
    assert I.str_for_kappa(k) > 0 and abs(I.kappa_needed(I.str_for_kappa(k)) / k - 1) < 1e-12


def test_xi_moves_the_supertrace():
    assert I.str_k1("+1/sqrt3", F(1, 6)) - I.str_k1("+1/sqrt3", F(1, 3)) == F(18, 6)


def test_verdict():
    assert RES["verdict"] == "PASS (prediction)"
    sel = RES[("verdict", "+1/sqrt3")]
    assert all(ok for *_, ok in sel)
    ratios = sel[0][2]
    assert 0.32 < ratios["one loop"] < 0.33 and 0.49 < ratios["three loops"] < 0.50   # xi = 0: the 3-loop pole in band
    assert not any(ok for *_, ok in RES[("verdict", "-1/sqrt3")])


def test_prediction_range():
    lo, hi = RES["mpl_range"]
    assert 0.46 < lo < 0.48 and 3.0 < hi < 3.2


def test_beyond_the_test():
    assert RES[("str_k0", "+1/sqrt3")] == -86
    n5, s5, m5 = RES["nc5"]
    assert n5 == (33, 175, 18) and m5 / I.mpl() < 1e-6
