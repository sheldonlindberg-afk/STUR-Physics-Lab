"""Pins src/triangle_orbifold.py (TRIANGLE.md): SU(6) on the triangle T^2/Z_3, the unification test,
and Yukawa couplings from zero modes in magnetic flux. Failures of the construction are pinned too."""
import os
import sys
from fractions import Fraction as F

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import triangle_orbifold as T
import m331_standalone as E
import why_parameters as W


def test_twist_leaves_331_and_no_other_twist_does():
    assert T.surviving_generators() == 17
    tw = T.all_twists()
    # (3,3,0) is SU(3) x SU(3) x U(1); (4,1,1) has the same dimension but is SU(4) x U(1)^2
    assert tw == {(6, 0, 0): 35, (3, 3, 0): 17, (4, 1, 1): 17, (2, 2, 2): 11}


def test_every_331_fermion_sits_in_su6():
    assert [T.dimension(T.fragments(r)) for r in ("6", "6bar", "15", "20", "21", "35")] == [6, 6, 15, 20, 21, 35]
    emb = T.embedding()
    assert all(rep is not None for *_, rep in emb)
    assert sum(m * dl * dc for m, dl, dc, _, _ in emb) == 66                 # Weyl fermions, exotic quarks included
    reps = {(dl, dc, q): rep for _, dl, dc, q, rep in emb}
    assert reps[(3, 3, F(1, 3))] == "20" and reps[(3, 3, F(0))] == "15" and reps[(3, 1, F(-1, 3))] == "6bar"


def test_weak_mixing_angle_at_the_orbifold_scale():
    assert T.sin2_at_orbifold() == (F(3, 4), F(3, 8))


def test_coefficients_agree_with_the_note():
    """One-loop a_X = 26/3, b_L = 13/2 (NOTE_331.md, steps 3 and 4), colour 5."""
    a, _ = T.coeffs(())
    assert np.allclose(a, [26 / 3, -13 / 2, -5])
    a8, _ = T.coeffs((T.candidates()[0],))
    assert T.Group("c", 3).T(8) == 3 and T.Group("c", 3).C2(6) == F(10, 3) and a8.shape == (3,)


def test_minimal_content_fails_to_unify():
    for loops in (1, 2):
        u = T.unify((), loops=loops)
        assert 1e10 < u["Mc"] < 2e10 and abs(u["alpha_s_MZ"] - 0.0325) < 0.001
    assert abs(T.unify((T.ORBIFOLD_SCALAR,), loops=2)["alpha_s_MZ"] - 0.0326) < 0.001
    assert T.unify((), mu331=1e11, loops=2)["alpha_s_MZ"] < 0.07 < E.ALPHA_S_MZ


def test_completion_is_a_fit_with_one_freed_mass():
    cand, n_screen, sols = T.completions()
    assert len(cand) == 22 and n_screen == 5 and len(sols) == 4
    assert not [t for t in sols if abs(t[2]["alpha_s_MZ"] - E.ALPHA_S_MZ) < T.ALPHA_S_TOL]
    extra, u1, u2 = sols[0]
    assert sorted(e[0] for e in extra) == ["Weyl fermion (1,8) X=0"] * 3 + ["real scalar (8,1) X=0"]
    assert u1["alpha_s_MZ"] < E.ALPHA_S_MZ < u2["alpha_s_MZ"]            # one and two loops bracket it
    m8, u = T.best_completion_with_one_mass()
    assert abs(m8 / 7.08e3 - 1) < 0.02 and abs(u["Mc"] / 1.11e16 - 1) < 0.03
    assert abs(u["alpha_s_MZ"] - E.ALPHA_S_MZ) < 1e-6 and u["tau_p"] > T.TAU_P_LIMIT


def test_zero_modes_and_three_generations():
    assert T.zero_mode_table() == {2: (1, 0, 1), 4: (1, 2, 1), 6: (3, 2, 1), 8: (3, 2, 3), 10: (3, 4, 3), 12: (5, 4, 3)}
    assert all(T.unitarity_error(M) < 1e-10 for M in (6, 12))
    assert T.corner_charges(6, 0) == [0, 1, 2] and T.corner_charges(12, 0) == [0, 1, 1, 2, 2]


def test_symmetric_higgs_gives_no_hierarchy():
    h, parity = T.symmetric_higgs()
    assert abs(parity - 1) < 1e-9
    assert np.allclose(T.masses(h), [1, 2 ** (-1 / 3), 2 ** (-1 / 3)], atol=1e-6)


def test_point_higgs_gives_one_massive_generation():
    s, err = T.point_higgs_check()
    assert s[1] < 1e-10 and err < 1e-10
    s, err = T.point_higgs_check(0.4 + 0.77 * T.TAU)
    assert s[1] < 1e-10 and err < 1e-10


def test_quartic_is_minimised_by_the_vortex_lattice():
    h, bmin = T.vacuum(0.0, n=6)
    assert abs(T.abrikosov() - 1.159595) < 1e-5 and abs(bmin - T.abrikosov()) < 1e-5
    s = T.masses(h)
    assert abs(s[1] - 1) < 1e-3 and s[2] < 1e-3                           # 1 : 1 : 0
    hk = T.point_higgs(T.CORNERS[0])
    assert abs(T.B(hk) - 6) < 1e-6 and abs(T.loop_term(hk) - 12.005) < 0.01


def test_fermion_loops_do_not_concentrate_the_higgs():
    hk = T.point_higgs(T.CORNERS[0])
    xc = T.B(hk) / T.loop_term(hk)
    h, g = T.vacuum(0.9 * xc, n=6)
    assert 0 < g < T.B(hk) - 0.9 * xc * T.loop_term(hk)                  # the vacuum is not the corner state
    assert T.masses(h)[2] > 0.3                                           # and has no hierarchy


def test_light_higgs_from_unequal_corners():
    cn = T.corner_numbers()
    assert abs(cn["K"] - 12 / T.AREA) < 1e-6 and abs(cn["g"] - 0.00212) < 2e-5 and abs(cn["kappa_L"] - 0.07973) < 2e-5
    s, _, ev = T.light_higgs([1, 0.9, 0.5])
    assert abs(s[1] / 1.90e-2 - 1) < 0.01 and abs(s[2] / 2.13e-3 - 1) < 0.01
    assert abs(ev[1] - 0.9) < 1e-3 and abs(ev[2] - 0.5) < 1e-3


def test_mixing_prediction_fails():
    m = T.mixing()
    assert m["resid"] < 1e-6
    assert abs(m["ku"][2] - 0.00345) < 1e-4 and abs(m["kd"][1] - 0.899) < 2e-3
    assert abs(m["Vus"] - 0.0038) < 3e-4 and abs(m["Vcb"] - 0.0012) < 2e-4
    assert W.V_US / m["Vus"] > 30 and W.V_CB / m["Vcb"] > 30


def test_triangle_form():
    r, th = T.triangle_form((T.LL.M_EL, T.LL.M_MU, T.LL.M_TAU))
    assert abs(r / 2 ** 0.5 - 1) < 2e-5 and abs(th - 2 / 9) < 2e-5
    y = W.YUK_MZ
    assert abs(T.triangle_form((y["u"], y["c"], y["t"]))[0] / 2 ** 0.5 - 1.2895) < 1e-3
    assert abs(T.triangle_form((y["d"], y["s"], y["b"]))[0] / 2 ** 0.5 - 1.1151) < 1e-3


def test_saved_output_has_every_section():
    text = open(os.path.join(ROOT, "results", "triangle", "output.txt"), encoding="utf8").read()
    for tag in ("G1 ", "G2 ", "G3 ", "G4 ", "T1 ", "T2 ", "T3 ", "T4 ", "T5 ", "T6 ", "None of the 19 is derived"):
        assert tag in text, tag
