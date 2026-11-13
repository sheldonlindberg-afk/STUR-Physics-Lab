"""Pins src/m331_zpole.py: the Z-pole fit of Z-Z' mixing, its validation on the E6 Z' bosons,
and the 3-3-1 bound on w against the LHC."""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import m331_zpole as Z
import m331_rho_bound as R
import m331_zprime_recast as ZR


def test_inputs_and_sm_baseline():
    assert len(Z.NAMES) == 14
    assert np.all(np.linalg.eigvalsh(Z.covariance()) > 0)
    assert abs(Z.chi2({}) - 14.19) < 0.01 and abs(Z.chi2({}, Z.names_without("AFB_b")) - 9.59) < 0.01


def test_tree_level_sm_is_close_to_gfitter():
    o = Z.observables(Z.couplings())
    for n in ("GammaZ", "sigma_had", "R_l", "A_l_SLD", "A_b", "A_c", "AFB_l", "AFB_b", "AFB_c"):
        assert abs(o[n] / Z.OBS[n]["sm"][0] - 1) < 0.01, n
    for n in ("R_b", "R_c"):                                           # no top vertex, massless quarks
        assert abs(o[n] / Z.OBS[n]["sm"][0] - 1) < 0.02, n
    assert abs(o["s2eff_QFB"] - Z.S2) < 1e-12


def test_rho_shift_moves_the_weak_angle_as_expected():
    d = 1e-4
    sh = Z.shifts(0.0, d)
    assert abs(sh["s2eff_Tevt"] / (-Z.S2 * (1 - Z.S2) / (1 - 2 * Z.S2) * d) - 1) < 1e-3
    # widths go as rho; the lower s^2 raises the charged-fermion couplings on top of that
    assert 1.0 < sh["GammaZ"] / Z.OBS["GammaZ"]["sm"][0] / d < 1.5


def test_e6_validation_against_erler_et_al():
    r = Z.e6_ranges()
    val = Z.DATA["validation"]
    for key, ref in ((("chi", "one"), val["chi_rho1"]), (("psi", "one"), val["psi_rho1"]),
                     (("psi", "free"), val["psi_rhofree"])):
        lo, hi = r[key]
        assert lo < 0 < hi and abs(lo) > abs(hi)                        # the asymmetry is reproduced
        assert abs(lo - ref[0]) < 5e-4 and abs(hi - ref[1]) < 5e-4, (key, lo, hi)
        assert abs((hi - lo) / (ref[1] - ref[0]) - 1) < 0.15
    assert abs(r[("chi", "one")][0] + 0.00145) < 5e-5 and abs(r[("psi", "one")][0] + 0.0022) < 5e-5


def test_331_mixing_formula_against_exact_diagonalization():
    for v in Z.VARIANTS:
        for a in (0.2, 0.7, 1.3):
            th, dr, mz1, mz2, (g, gX, nZp) = Z.exact_mixing(v, R.v_ew() / 0.04, a)
            th0, dr0 = Z.mixing(v, R.v_ew() / 0.04, math.sin(a) ** 2)
            assert abs(th / th0 - 1) < 5e-3 and abs(dr / dr0 - 1) < 5e-3, (v, a)
        # the Z' direction is the recast's g331 (left-handed electron)
        beta, g, gY, gX = Z.lagrangian_couplings(v)
        nZp = Z.exact_mixing(v, 6e3, 0.3)[4][2]
        T8 = 1 / (2 * math.sqrt(3)); X = -0.5 - beta * T8
        c = (g * nZp[1] * T8 + gX * nZp[2] * X) / math.hypot(g, gY)
        assert abs(c - ZR.g331(T8, -0.5, beta, Z.S2)) < 1e-12


def test_w_bounds_and_the_lhc():
    out = {}
    for v in Z.VARIANTS:
        for label, names in (("all", Z.NAMES), ("noAFBb", Z.names_without("AFB_b"))):
            bd = Z.w_bounds(v, names)
            out[(v, label)] = Z.worst(bd)
            assert max(bd[2]) <= max(max(bd[0]), max(bd[1])) + 1e-9      # odd third generation is weakest here
            assert max(max(b) for b in bd.values()) - min(max(b) for b in bd.values()) < 400
    assert abs(out[("+1/sqrt3", "all")] / 7.5e3 - 1) < 0.02 and abs(out[("-1/sqrt3", "all")] / 7.6e3 - 1) < 0.02
    assert abs(out[("+1/sqrt3", "noAFBb")] / 6.0e3 - 1) < 0.02 and abs(out[("-1/sqrt3", "noAFBb")] / 6.4e3 - 1) < 0.02
    for v in Z.VARIANTS:
        lhc = R.w_from_zprime(v)[0]
        assert R.w_bound_rho_max(v) < out[(v, "noAFBb")] < out[(v, "all")] < lhc   # rho < Z pole < LHC


def test_no_significant_preference_for_mixing():
    for v in Z.VARIANTS:
        for names in (Z.NAMES, Z.names_without("AFB_b")):
            dc = Z.best_fit(v, names)[0]
            assert 0 <= dc < 3.84
