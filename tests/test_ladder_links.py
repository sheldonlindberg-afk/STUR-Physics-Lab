"""Pins src/ladder_links.py: the links between the ladder's rungs (SYMMETRY_LADDER.md).
L1, neutral matter (rung 1 -> rung 4); L2, pi0 -> gamma gamma (rung 1 -> rung 2);
L3, the Planck mass (rung 4 -> rung 1), at the reference spectrum and over the threshold scan."""
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
    assert abs(p3 - 2.86) < 0.01 and 3.9e-8 < p5 < 4.5e-8 and abs(1 / lo - 8.2) < 0.1
    p3m, p5m, lom, him = out["-1/sqrt3"]
    assert 1.8e10 < p3m < 2.0e10 and 9.0e-5 < p5m < 9.6e-5
    assert abs(floor - 0.605) < 0.01 and abs(x_floor - 2.73) < 0.05


def test_g_window_over_the_threshold_scan():
    scan, n = LL.g_window_scan()
    assert n == 72
    p3lo, p3hi, s_lo, s_hi = scan["+1/sqrt3", 3]
    assert abs(p3lo - 1.262) < 0.005 and abs(p3hi - 16.0) < 0.2
    assert s_lo == (0.5, 1 / 3, 2000.0, 2) and s_hi == (3.0, 3.0, 10000.0, 1)
    assert abs(1 / p3lo**2 - 0.628) < 0.005            # L3e: G 1.59x weaker excludes N_c = 3
    # the reference spectrum lies inside the scan, and every spectrum keeps the selection
    ref = LL.g_window()[0]
    for v in ("+1/sqrt3", "-1/sqrt3"):
        assert scan[v, 3][0] <= ref[v][0] <= scan[v, 3][1] and scan[v, 3][0] > 1
        assert scan[v, 5][0] <= ref[v][1] <= scan[v, 5][1] and scan[v, 5][1] < 1


def test_gravity_term_shifts_the_pole_by_percent():
    f_sm, rows = LL.gravity_shift()
    assert abs(f_sm - 0.0098) < 2e-4
    p0, pg = rows["reference"]
    assert abs(p0 - 2.859) < 0.005 and abs(pg / p0 - 1.029) < 0.003
    p0, pg = rows["worst"]
    assert abs(p0 - 1.262) < 0.005 and 1.0 < pg / p0 < 1.02


def test_diamond_mass_is_mostly_qcd():
    B, b = LL.carbon12_binding()
    assert abs(B - 92.162) < 1e-3 and abs(b - 7.680) < 1e-3
    f, tot = LL.mass_budget("2+1")
    assert abs(tot - 1) < 1e-12
    assert abs(f["QCD field energy"] - 0.9145) < 5e-4 and abs(f["u, d quark masses"] - 0.0453) < 2e-4
    assert abs(f["s quark mass"] - 0.0482) < 2e-4 and abs(f["electrons"] - 2.74e-4) < 1e-5
    phi, out = LL.phase_without_masses()
    pl, pn = out["2+1"]
    assert abs(pl / phi - (1 - f["u, d quark masses"]) ** 2) < 1e-12 and abs(pl - 1.99) < 0.01 and abs(pn - 1.80) < 0.01


def test_evaporation_counts_the_particles():
    assert abs(LL.hawking_T_gev(1e7) - 1057.26) < 0.05
    assert abs(LL.f_of_T(1e-15) - 1.016) < 1e-9
    assert abs(LL.f_of_T(500.0) - 15.332) < 1e-9 and abs(LL.f_standard_model_unbroken() - 15.332) < 1e-9
    assert abs(LL.f_331("-1/sqrt3")[0] - 25.664) < 1e-6 and abs(LL.f_331("+1/sqrt3")[0] - 26.486) < 1e-6
    assert LL.f_331("-1/sqrt3")[1:] == (66, 17, 18) and LL.f_331("+1/sqrt3")[1] == 69
    assert abs((1e10) ** 3 / (3 * LL.ALPHA_EVAP * 15.35) - 406.66) < 0.05
    ms = LL.m_star()
    assert abs(ms / 5.11e11 - 1) < 0.01 and abs(LL.hawking_T_gev(ms) * 1e3 - 20.7) < 0.2
    rows = LL.evaporation_thresholds()
    Ts = [T for _, T, _, _, _ in rows]
    assert Ts == sorted(Ts) and abs(rows[1][2] / 4.50e22 - 1) < 0.01


def test_reference_output_matches():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        LL.main()
    ref = open(os.path.join(os.path.dirname(__file__), "..", "results", "ladder", "ladder_links.txt")).read()
    assert buf.getvalue() == ref
