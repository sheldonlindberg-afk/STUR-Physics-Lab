"""Pins src/ladder_links.py: the links between the ladder's rungs (SYMMETRY_LADDER.md).
L1, neutral matter (rung 1 -> rung 4); L2, pi0 -> gamma gamma (rung 1 -> rung 2)."""
import contextlib, io, os, sys
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import ladder_links as LL
import stur_gravity_full as GF


def test_neutrality_is_the_mixed_anomaly():
    d1, d2, same = LL.neutrality_identity()
    assert d1 == 0 and d2 == 0 and same == (0, 0)
    s1, s2 = LL.neutrality_identity_sm()
    assert s1 == 0 and s2 == 0


def test_rung1_charges_make_matter_neutral_for_every_Nc():
    res = LL.rung1_matter_charges()
    assert len(res) == 6
    for (qp, qn, qe, qnu, ok) in res.values():
        assert (qp, qn, qe, qnu) == (1, 0, -1, 0) and ok


def test_neutrality_requirement_and_margin():
    c = LL.coulomb_vs_gravity()
    assert abs(c["dphi_grav"] - 2.1868) < 1e-3
    assert abs(c["delta_max"] / 2.82e-19 - 1) < 2e-3
    assert abs(c["delta_max"] / c["size_independent"] - 1) < 1e-3       # design A: m = 12 u x atoms
    assert abs(c["Qmax_e"] / 2.50e-6 - 1) < 5e-3
    assert 270 < c["margin"] < 290 and c["residual_total_e"] < 1e-8
    # one stray electron: the same number as src/stur_gravity_full.py H6
    m, dx, gap = c["m"], 720.8e-6, 181.2e-6
    h6 = GF.em_entangling_ratio(m, dx, gap, 3.24, q=GF.E_CH)
    assert abs(c["one_electron"] / h6 - 1) < 1e-6 and abs(c["one_electron"] / 1.60e10 - 1) < 0.01


def test_pi0_anomaly_factor_is_one_for_every_Nc():
    out, general, agree = LL.anomaly_factor()
    assert set(out.values()) == {1} and general == 1 and agree


def test_two_photon_width_formula():
    msq, width, A, m = LL.two_photon_width()
    assert sp.simplify(msq - A**2 * m**4 / 2) == 0
    assert sp.simplify(width - A**2 * m**3 / (64 * sp.pi)) == 0


def test_pi0_width_against_primex():
    G, pull, fpi, fixed = LL.pi0_width()
    assert abs(G - 7.785) < 2e-3 and abs(pull) < 0.5
    assert abs(fixed[5] / G - 25 / 9) < 1e-12


def test_planck_mass_is_rung4s_gravity():
    mpl, mpl331, _ = LL.planck_mass()
    assert abs(mpl / mpl331 - 1) < 1e-6
    out, floor, x_floor = LL.g_window()
    p3, p5, lo, hi = out["+1/sqrt3"]
    assert abs(p3 - 2.89) < 0.01 and 3.9e-8 < p5 < 4.5e-8 and abs(1 / lo - 8.4) < 0.1
    p3m, p5m, lom, him = out["-1/sqrt3"]
    assert 1.8e10 < p3m < 2.0e10 and 9.0e-5 < p5m < 9.6e-5
    assert abs(floor - 0.61) < 0.01 and abs(x_floor - 2.7) < 0.05


def test_reference_output_matches():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        LL.main()
    ref = open(os.path.join(os.path.dirname(__file__), "..", "results", "ladder", "ladder_links.txt")).read()
    assert buf.getvalue() == ref
