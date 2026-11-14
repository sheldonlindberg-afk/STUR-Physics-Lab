"""Pins src/why_parameters.py (WHY.md): the Standard Model's 19 parameters, the published attempts
to explain them, and quark flavour in 3-3-1; and step 9 of the merged simulation against it."""
import contextlib
import io
import math
import os
import re
import sys
from fractions import Fraction as F

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import why_parameters as W
import m331_scalar as S


def test_ledger_has_19_rows_and_none_is_called_derived():
    assert len(W.LEDGER) == 19 and len({r[0] for r in W.LEDGER}) == 19
    assert {r[2] for r in W.LEDGER} <= set(W.CLASSES) and "DERIVED" not in W.CLASSES
    assert W.tally() == {"MEASURED": 11, "RELATION": 3, "EMPIRICAL": 2, "CONJECTURE": 3}


def test_higgs_mass_from_a_vanishing_quartic():
    sw, b61, b64 = W.mh_from_planck()
    assert abs(sw - 128.67) < 0.01 and abs(b61 - 128.68) < 0.01 and abs(b64 - 128.35) < 0.01
    # at their own inputs the formulas return the published numbers
    assert abs(W.mh_from_planck(171.2, 0.1176)[0] - 126.3) < 1e-9
    assert abs(W.mh_from_planck(173.34, 0.1184)[2] - 129.6) < 1e-9
    d, err, pull = W.mh_pull()
    assert abs(d - 3.47) < 0.01 and abs(pull - 1.5) < 0.05
    assert abs(W.mt_stability_pull() - 2.04) < 0.02


def test_one_loop_running_is_the_scalar_script_s():
    """sm_start and sm_rhs reproduce src/m331_scalar.sm_running exactly."""
    ref = S.sm_running(W.M_PL)
    assert all(abs(a - b) < 1e-12 for a, b in zip(W.sm_start(), ref.y[:, 0]))
    assert all(abs(a - b) < 1e-6 for a, b in zip(W.sm_up().y[:, -1], ref.y[:, -1]))
    lam0, mh = W.mh_one_loop_zero_quartic()
    assert abs(lam0 - 0.1458) < 1e-4 and abs(mh - 134.7) < 0.1
    assert abs(W.mh_of_lambda(W.sm_start()[4]) - W.M_H) < 1e-9


def test_two_conditions_fix_both_masses():
    mt, mh, y = W.two_conditions_nnlo()
    gY, g2, yt, lam = W.planck_couplings(mt, mh)
    assert abs(lam) < 1e-12 and abs(yt - y) < 1e-12
    assert abs(W.sm_rhs(0, [gY, g2, 0.5, yt, 0.0])[4]) < 1e-15          # beta_lambda = 0 at lambda = 0
    assert abs(mt - 174.27) < 0.02 and abs(mh - 132.56) < 0.02
    yt1, mt1, lam1, mh1 = W.two_conditions_one_loop()
    assert abs(mt1 - 169.6) < 0.1 and abs(mh1 - 128.6) < 0.1
    # both within 2% (top) and 6% (Higgs) of the measured values
    assert all(abs(m / W.M_T - 1) < 0.02 for m in (mt, mt1)) and all(abs(m / W.M_H - 1) < 0.06 for m in (mh, mh1))


def test_zero_quartics_at_the_planck_scale_fail_in_331():
    scan = W.w2_scan()
    assert set(scan) == set(S.VARIANTS)
    for v, rows in scan.items():
        assert len(rows) == len(W.W2_GRID)
        assert all(o in ("unbounded", "diverges") for _, _, o, _, _ in rows), (v, rows)
        assert all(l < -0.1 for _, _, o, l, _ in rows if o == "unbounded")
    assert sum(o == "unbounded" for rows in scan.values() for _, _, o, _, _ in rows) == 9


def test_top_quasi_fixed_point_overshoots():
    rows, y_meas = W.top_quasi_fixed_point()
    assert abs(y_meas - 0.9329) < 1e-4
    assert abs(rows[0][1] - 1.192) < 2e-3 and abs(rows[-1][1] - 1.265) < 2e-3
    assert all(y > 1.25 * y_meas for _, y in rows)


def test_qcd_scale_is_exponentially_sensitive():
    a3, lam, sens, lam10 = W.qcd_scale()
    assert abs(1 / a3 - 52.9) < 0.1 and abs(lam - 0.028) < 0.001 and abs(sens - 47.5) < 0.1
    assert 80 < lam10 < 250                                           # above the weak scale's order


def test_weak_angle_bound():
    assert W.s2_bound(F(1, 3)) == F(3, 4) and W.s2_bound(3) == F(1, 4)


def test_peccei_quinn_charges_exactly():
    for xd in (F(1), F(-3, 7)):
        terms, anomaly, ordinary = W.pq_check(xd)
        assert len(terms) == 27 and all(t == 0 for t in terms)
        assert anomaly == 2 * xd and ordinary == 0
    assert W.pq_check(n_c=5)[1] == 2 and W.pq_check(n_c=7)[1] == 2
    # a wrong charge is caught: flip the sign of the exotic u' and a Yukawa term is no longer invariant
    q = W.pq_charges()
    assert -q["Q3"][2] + (-q["u'R"]) + q["chi"][2] != 0


def test_cabibbo_relation_misses():
    th, dth, t12, dt12, pull = W.gst()
    assert abs(th - 0.2206) < 1e-4 and abs(t12 - 0.2270) < 1e-4 and abs(pull + 5.0) < 0.1
    assert abs(th - W.GST_LIT[0]) < W.GST_LIT[1]                      # agrees with the published evaluation


def test_koide():
    K, mtau = W.koide()
    assert abs(K / (2 / 3) - 1) < 1e-5 and abs(mtau * 1e3 - 1776.97) < 0.01     # Koide's 1982 prediction
    assert abs(W.koide((W.LL.M_EL, W.LL.M_MU, mtau))[0] - 2 / 3) < 1e-12


def test_flavour_in_331():
    tb, y = W.tan_b_equal_tb()
    assert abs(tb - 59.3) < 0.05 and abs(y["t"] - y["b"]) < 1e-12 and abs(y["c"] / y["t"] - 0.22) < 0.005
    assert abs(W.yukawa_spread(W.YUK_MZ) / 1.37e5 - 1) < 0.01 and abs(W.yukawa_spread(y) / 6.28e4 - 1) < 0.01
    vtb, vus, vcb, frac = W.anarchy(tb, n=1500)
    assert vtb < 0.05 and frac == 0.0                                 # the top pairs with the lightest down quark
    assert W.anarchy(1.0, n=1500)[3] < 0.1
    r1, w = W.rho_from_flavour(1.0)
    rb, _ = W.rho_from_flavour(tb)
    assert abs(r1 / 1.29e-5 - 1) < 0.01 and abs(rb / 6.94e-5 - 1) < 0.01 and abs(w / 10.3e3 - 1) < 0.01


def test_saved_output_is_current():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        W.main()
    assert buf.getvalue() == open(os.path.join(ROOT, "results", "why", "output.txt"), encoding="utf8").read()


def test_merged_simulation_step_9_agrees():
    """Step 9 of src/chain_first_principles.py is this script restated with the standard library."""
    out = open(os.path.join(ROOT, "results", "chain_first_principles.txt"), encoding="utf8").read()
    step9 = out[out.index("9  Why these inputs?"):]

    def num(pattern):
        return float(re.search(pattern, step9).group(1))
    mt, mh, _ = W.two_conditions_nnlo()
    _, mt1, _, mh1 = W.two_conditions_one_loop()
    assert abs(num(r"Higgs mass from lambda\(M_Pl\) = 0: ([0-9.]+) GeV") - W.mh_from_planck()[0]) < 1e-3
    assert abs(num(r"top mass, NNLO couplings at M_Pl: ([0-9.]+) GeV") - mt) < 1e-3
    assert abs(num(r"Higgs mass, NNLO couplings at M_Pl: ([0-9.]+) GeV") - mh) < 1e-3
    assert abs(num(r"top mass, one loop throughout: ([0-9.]+) GeV") - mt1) < 2e-3
    assert abs(num(r"Higgs mass, one loop throughout: ([0-9.]+) GeV") - mh1) < 2e-3
    assert abs(num(r"Gatto-Sartori-Tonin\): ([0-9.]+) rad") - W.gst()[0]) < 1e-6
    assert abs(num(r"Koide's relation K = 2/3: ([0-9.]+) MeV") - 1e3 * W.koide()[1]) < 1e-2
    assert abs(num(r"\(tan b = ([0-9.]+)\)") - W.tan_b_equal_tb()[0]) < 0.05
    t = W.tally()
    assert f"{t['MEASURED']} measured" in step9 and f"{t['CONJECTURE']} with a" in step9.replace("\n", " ").replace("  ", " ")
    assert "median |V_tb| = 0.01" in step9 and f"{W.anarchy(W.tan_b_equal_tb()[0])[0]:.2f}" == "0.01"
    assert math.isclose(num(r"rho - 1 = ([0-9.]+) times"), W.rho_from_flavour(59.3)[0] / W.rho_from_flavour(1.0)[0], rel_tol=0.02)
