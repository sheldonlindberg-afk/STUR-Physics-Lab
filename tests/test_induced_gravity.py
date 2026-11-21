"""Pins src/induced_gravity.py: the test registered in INDUCED_GRAVITY_PREREG.md, as computed."""
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


def test_visser_sign_convention():
    """Visser eq. (29): str[k1] ~ -1 gives positive 1/G; the formula used here agrees."""
    k = 1e19
    assert I.str_for_kappa(k) < 0 and abs(I.kappa_needed(I.str_for_kappa(k)) / k - 1) < 1e-12


def test_xi_moves_the_supertrace_as_registered():
    assert I.str_k1("+1/sqrt3", F(1, 6)) - I.str_k1("+1/sqrt3", F(1, 3)) == F(18, 6)


def test_verdict():
    assert RES["verdict"].startswith("FAIL")
    assert all(not ok for *_, ok in RES[("verdict", "+1/sqrt3")])
    assert all(not ok for *_, ok in RES[("verdict", "-1/sqrt3")])
    assert 0.17 < RES[("xi_fit", "+1/sqrt3", "one loop")] < 0.23
