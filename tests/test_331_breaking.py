"""Pins src/m331_breaking.py: the photon, hypercharge matching, spectrum and charges, derived."""
import os, sys
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import m331_breaking as B

g, gX = B.g, B.gX
V = ("-1/sqrt3", "+1/sqrt3")


def test_photon_and_hypercharge_derived():
    for v in V:
        rank, Mn, einv2 = B.photon_checks(v)
        assert rank == 8 and all(x == 0 for x in Mn)
        assert sp.simplify(einv2 - (sp.Rational(4, 3) / g**2 + 1 / gX**2)) == 0
        massless, MnY, gYinv2 = B.first_step(v)
        assert massless == 4 and all(x == 0 for x in MnY)
        assert sp.simplify(gYinv2 - (sp.Rational(1, 3) / g**2 + 1 / gX**2)) == 0   # the matching condition


def test_spectrum_and_threshold_formula():
    for v in V:
        lm = B.leading_masses(v)
        assert sp.simplify(lm["MW2"] - lm["MW2_expected"]) == 0
        assert sp.simplify(lm["MZ2_lead_over_v2"] - lm["MZ2_expected"]) == 0
        assert sp.simplify(lm["MZp2_lead_over_w2"] - lm["MZp2_expected"]) == 0
        diff, chk = B.mzp_over_mv_check(v)
        assert diff == 0 and chk == 0                          # src/m331_threshold.py formula derived
        coeff, rn, rs = B.rho_coefficient(v)
        assert abs(rn - rs) < 1e-8 and rn > 1                  # rho >= 1 at tree level


def test_charges_general_nc():
    for v in V:
        for Nc in (3, 5, 7):
            rows, ok, _ = B.charges(v, Nc)
            assert ok


def test_numbers():
    vv, mz, ratio, mv = B.numbers()
    assert abs(vv - 246.22) < 0.01 and abs(mz / B.MZ_MEAS - 1) < 0.005
    assert abs(ratio - 1.2173) < 1e-3
