"""Pins src/induced_gravity_finite.py: the computation registered in INDUCED_GRAVITY_FINITE.md (commit c1beae2)."""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import induced_gravity_finite as F

RES = F.main()


def test_every_registered_item_as_registered():
    assert all(RES["verdict"].values()), RES["verdict"]


def test_stage1_counts():
    assert RES["str1"] == -86
    assert abs(RES["xi_S1"] - (1 / 6 + (1 / 6) / 18)) < 1e-12


def test_bound_needs_planck_scale_states():
    assert 2e18 < RES["w_needed"] < 4e18


def test_two_level_theorem_exact():
    n, worst, signs = RES["B"]
    assert n == 600 and worst < 1e-10 and signs
    # degenerate limit: r -> 1 gives the proper-time formula with kappa = M
    assert abs(F.formula_B(2.0, 1e19, 1e19 * (1 + 1e-7)) / (2.0 / (2 * math.pi) * 1e38) - 1) < 1e-6


def test_three_levels_can_flip():
    K1, t, K3, M, g = RES["C"]
    S = F.str_k1(F.light_fields(F.SELECTED, 0.0))
    assert S > 0 and g < 0
    assert abs(K1 + t + K3 + S) < 1e-9 * abs(S) and abs(K1 * M[0] ** 2 + t * M[1] ** 2 + K3 * M[2] ** 2) < 1e-9 * abs(t) * M[2] ** 2


def test_integral_asymptotics():
    assert RES["I"] < 1e-6
