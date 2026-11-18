"""Pins src/ladder_links.py: the links between the ladder's rungs (SYMMETRY_LADDER.md).
L1, neutral matter (rung 1 -> rung 4); L2, pi0 -> gamma gamma (rung 1 -> rung 2);
L3, the Planck mass (rung 4 -> rung 1), at the reference spectrum and over the threshold scan."""
import contextlib, io, math, os, sys
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


def test_pion_from_the_weak_and_em_forces():
    fV, f, ferr = LL.fpi_from_weak()
    assert abs(fV * 1e3 - 127.13) < 0.01 and abs(f * 1e3 - 130.57) < 0.01 and abs(ferr * 1e3 - 0.14) < 0.01
    G, pull, m4 = LL.rung2_with_weak_fpi()
    assert abs(G - 7.742) < 2e-3 and abs(pull + 0.51) < 0.02 and abs(m4 * 1e3 - 132.3) < 0.2
    resid, num, (lo, hi), meas, dm, dm_meas = LL.dgmly()
    assert resid == 0 and abs(num - 1604) < 1 and abs(meas - 1261.2) < 0.1 and lo < num < hi


def test_one_coupling_from_mz_to_zero():
    num, clo = LL.dalpha_lep_one_loop()
    assert abs(num / clo - 1) < 1e-7 and abs(clo / LL.DALPHA_LEP_1LOOP_LIT - 1) < 1e-4
    w, frac = LL.dalpha_kedr_window()
    assert abs(w - 1.7425e-3) < 1e-6 and abs(frac - 0.0626) < 1e-3
    a0, d = LL.alpha0_from_mz()
    assert abs(a0 - 1 / LL.ALPHA_0) < 1e-5


def test_de_sitter_gauge_theory_in_the_lab():
    assert LL.weak_field_of_sds() == (0, 0)
    assert LL.lambda_cancels_in_entangling_phase() == 0
    rel, l, rf = LL.lambda_correction_size()
    assert abs(l / 1.647e26 - 1) < 1e-3 and abs(rel / 2.04e-59 - 1) < 0.01


def test_de_sitter_horizon_entropy():
    d_rc, d_k, d_A, d_S, d_S2, fac = LL.de_sitter_entropy_symbolic()
    assert (d_rc, d_k, d_A, d_S, d_S2) == (0, 0, 0, 0, 0) and fac == 3     # A = 12 pi/Lambda, S = 3 pi/Lambda
    assert LL.first_law_every_horizon() == 0
    ident, worst = LL.sds_entropy_bound()
    assert ident == 0 and worst < 1
    l, A, S, T, r1, r2 = LL.de_sitter_numbers()
    assert abs(S / 3.263e122 - 1) < 1e-3 and abs(T / 2.21e-30 - 1) < 1e-2
    assert abs(r1 - 1) < 1e-12 and abs(r2 - 3) < 1e-12


def test_neutrino_mass_from_the_breaking_scale():
    q = LL.lepton_triplets()
    assert q["-1/sqrt3"] == ["0", "-1", "0"] and q["+1/sqrt3"] == ["0", "-1", "-1"]
    prod, resid, inv = LL.seesaw_symbolic()
    assert prod == 0 and resid == 0 and inv == 0
    sn = LL.seesaw_numbers()
    assert abs(sn["slope"] + 1) < 1e-9 and abs(sn["light"] / 0.0501 - 1) < 2e-3
    assert 1.2 < sn["ratio"] < 1.4 and abs(sn["m_with_ye"] / 0.0301 - 1) < 5e-3
    tot, bound = LL.neutrino_data()
    assert 0.058 < tot < 0.060 and tot < bound


def test_first_post_newtonian_correction():
    assert LL.eih_test_mass_limit() == 0
    dn, dp, dq = LL.eih_phase_shift()
    assert abs(dn - 2.1868) < 1e-3
    assert abs(dp / dn) < 1e-23 and abs(dq / dn) < 1e-37 and dp != 0


def test_bekenstein_bound():
    assert LL.bekenstein_saturation() == 0
    R, bek, holo, atoms = LL.diamond_bounds()
    assert bek > 1e3 * atoms and holo > 1e30 * bek


def test_de_sitter_pair_correction_and_vacuum_energy():
    resid, dn, dc = LL.de_sitter_pair_correction()
    assert resid == 0 and abs(dc / dn + 1.92e-60) < 0.05e-60
    assert LL.de_sitter_entropy_identity() == 0
    r4, ratios = LL.vacuum_energy_scales()
    assert abs(r4 / 2.248e-3 - 1) < 2e-3
    vals = list(ratios.values())
    assert abs(vals[3] / (8 * LL.de_sitter_numbers()[2] / 3) - 1) < 1e-3
    assert vals == sorted(vals) and 1e42 < vals[0] < 1e43 and 1e54 < vals[1] < 1e55


def test_quasinormal_modes_and_the_fit_at_zero_spin():
    w0, w1 = LL.leaver_qnm(0), LL.leaver_qnm(1)
    assert abs(w0 - (0.373672 - 0.088962j)) < 2e-6 and abs(w1 - (0.346711 - 0.273915j)) < 2e-6
    fr, er, fq, eq = LL.bcw_at_zero_spin()
    assert abs(fr / er - 1) < 0.02 and abs(fq / eq - 1) < 0.015 and fr / er < 1 < fq / eq


def test_abj_anomaly_derived():
    ok, lam, holds, coef = LL.abj_fujikawa()
    assert ok and holds and abs(lam) == 4 and coef == 1
    assert LL.abj_landau() == (0, 0)
    assert LL.abj_pion_amplitude() == 1


def test_rho_parameter_and_w_mass():
    ward, pole, s2dep, diff, lim = LL.rho_parameter_loop()
    assert ward == 0 and not pole and not s2dep and diff == 0 and lim == sp.Symbol("m_t", positive=True) ** 2
    drho, dal, steps, rest = LL.w_mass_steps()
    assert abs(drho / 9.256e-3 - 1) < 2e-3
    mws = [m for m, _ in steps]
    assert abs(mws[0] - 80.939) < 2e-3 and mws[1] < mws[0] and mws[2] > mws[1] and abs(mws[3] - 80.495) < 3e-3
    assert 0.005 < rest < 0.009 and abs(steps[3][1] + rest - 0.0356) < 1e-3     # total Delta r of the SM


def test_hawking_spectrum_from_bogoliubov_coefficients():
    de, dg, rat, ex = LL.bogoliubov_checks()
    assert de < 1e-15 and dg < 1e-15 and abs(rat / ex - 1) < 1e-12
    assert LL.bogoliubov_symbolic() == (0, 0, 0)
    de2, dg2, rat2, ex2 = LL.bogoliubov_checks(y=1.9, Om=0.4)         # other frequency and Omega: still thermal
    assert abs(rat2 / ex2 - 1) < 1e-12


def test_kerr_modes_and_the_fit_at_the_spin_gw250114_uses():
    assert LL.kerr_table_check() < 6e-5
    ef, eq = LL.kerr_fit_errors()
    assert abs(ef - 0.0185) < 5e-4 and abs(eq - 0.0088) < 5e-4           # BCW's stated maxima, 1.85% and 0.88%
    mf, chif, a_f, a_min = LL.area_law_exact()
    assert abs(mf - 66.48) < 0.02 and abs(chif - 0.7444) < 5e-4 and abs(a_f / 4.039e5 - 1) < 1e-3
    import black_holes as BH
    a_i, a_fit, a_i_max, a_fit_min, _ = BH.area_law()
    assert a_min > a_i_max and abs(a_min / 3.360e5 - 1) < 2e-3 and abs(a_f / a_fit - 1) < 0.01


def test_retarded_casimir_polder_step():
    res = LL.retarded_pair_energy()
    for r, (ex, fo, st) in res.items():
        assert abs(fo / ex - 1) < 1e-8                      # normal modes against the retarded ln det
        assert abs(st / ex - 1) > 1.0 or r > 4              # the static kernel is wrong
    assert abs(res[4][2] / res[4][0] - 3.06) < 0.05
    x, x2 = LL.casimir_polder_order()
    assert 5e-8 < x < 2e-7 and x2 < 1e-13


def test_mz_bookkeeping():
    b = LL.mz_bookkeeping()
    assert abs(b["tree"] - 91.5065) < 1e-3 and abs(b["dr0"] - 0.066450) < 1e-5
    assert abs(b["pred"] - 91.1880) < 2e-3 and abs(b["gap"] - b["measured_gap"]) < 5e-5
    assert abs(b["parts"][0] + 0.010058) < 1e-5 and abs(b["parts"][1] - 0.003138) < 1e-5
    assert abs(b["ratio2"] ** 0.5 - 1 + 0.0035) < 1e-4
    assert abs(b["frac"] - 0.912) < 2e-3 and abs(b["pred_one_loop"] - 91.229) < 2e-3


def test_qed_cp_accepted_builds():
    worst, cross, far, near = LL.qed_cp_accepted(rhos=(0.05, 1.0, 20.0))
    assert worst < 1e-9 and cross < 1e-9
    assert abs(far - 23 / (4 * math.pi)) < 1e-10 and abs(near - 0.75) < 1e-10


def test_grey_body_weights_derived():
    gw = LL.grey_weights()
    for s, (d, q) in gw.items():
        assert abs(d / q - 1) < 0.02                    # within the digits Carr et al. quote (0.007 has one)
    assert abs(gw[0][0] - 0.26638) < 1e-4 and abs(gw[0.5][0] - 0.14652) < 1e-4 and abs(gw[1][0] - 0.06023) < 1e-4 and abs(gw[2][0] - 0.006870) < 1e-5
    fq, fd, fall = LL.grey_f_standard_model()
    assert abs(fq - 15.332) < 1e-3 and abs(fd - 15.332) < 2e-3 and abs(fall - 15.712) < 2e-3
    assert LL.grey_gamma_against_reference(6) < 1e-6


def test_collapsing_shell_map_and_thermal_ratio():
    resid, kinv, kh1 = LL.null_shell_map()
    M = LL.sp.Symbol("M", positive=True)
    assert resid == 0 and LL.sp.simplify(kinv - 4 * M) == 0 and LL.sp.simplify(kh1 - 1 / (4 * M)) == 0
    for w, wp in ((0.05, 0.4), (0.05, 5.0), (0.1, 50.0), (0.1, 0.12)):
        num, closed = LL.shell_bogoliubov_ratio(w, wp)
        assert abs(num / closed - 1) < 1e-12
    num, _ = LL.shell_bogoliubov_ratio(0.1, 1e4)
    assert abs(num / math.exp(-8 * math.pi * 0.1) - 1) < 1e-3                    # w' >> w: the Planck factor of L19


def test_reference_output_matches():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        LL.main()
    ref = open(os.path.join(os.path.dirname(__file__), "..", "results", "ladder", "ladder_links.txt")).read()
    assert buf.getvalue() == ref
