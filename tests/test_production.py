"""Pins production_v2_2.py, the repository's one simulation.

Three kinds of test:
  1. The rule: no non-integer number may appear in the script outside INPUTS,
     COMPARISONS, NUMERICS and LITERATURE (published coefficients, each with its
     source), and measured comparisons never feed a calculation.
  2. The script is standard-library only and every self-check passes.
  3. The headline numbers stay where they are (they move only if an input moves).
"""
import ast
import importlib.util
import math
import os
import re
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
PATH = os.path.join(ROOT, "production_v2_2.py")
EXPECTED = os.path.join(ROOT, "results", "production_v2_2.txt")
TABLES = ("INPUTS", "COMPARISONS", "NUMERICS", "LITERATURE")


def _load():
    spec = importlib.util.spec_from_file_location("production_v2_2", PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = _load()
TREE = ast.parse(open(PATH, encoding="utf-8").read())
RESULT = P.run()


def _table_line_ranges():
    ranges = []
    for node in TREE.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            target = node.targets[0] if isinstance(node, ast.Assign) else node.target
            if getattr(target, "id", None) in TABLES:
                ranges.append((node.lineno, node.end_lineno))
    return ranges


def test_literature_entries_have_sources():
    assert all(e["source"] and "value" in e for e in P.LITERATURE.values())


def test_no_tunable_number_outside_the_input_tables():
    ranges = _table_line_ranges()
    assert len(ranges) == len(TABLES)
    numeric_string = re.compile(r"^[+-]?(\d+\.\d*|\.\d+|\d+)([eE][+-]?\d+)?$")
    bad = []
    for node in ast.walk(TREE):
        if not isinstance(node, ast.Constant):
            continue
        if any(a <= node.lineno <= b for a, b in ranges):
            continue
        v = node.value
        if isinstance(v, float) and not v.is_integer():
            bad.append((node.lineno, v))
        if isinstance(v, complex) and v != 1j:
            bad.append((node.lineno, v))
        if isinstance(v, str) and numeric_string.match(v.strip()) and not v.strip().isdigit():
            bad.append((node.lineno, v))
    assert not bad, f"numbers outside INPUTS/COMPARISONS/NUMERICS/LITERATURE: {bad}"


def test_comparisons_never_feed_a_calculation():
    """COMPARISONS is read only by the functions that judge or print results."""
    readers = set()
    for node in ast.walk(TREE):
        if isinstance(node, ast.FunctionDef):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and sub.id == "COMPARISONS":
                    readers.add(node.name)
    assert readers <= {"_comparison", "_derived_vub_over_vcb", "report", "to_jsonable"}, readers


def test_inputs_are_read_only_through_the_tracer():
    """Every read of a measured input is recorded, so the traced dependency graph is complete:
    only these functions touch INPUTS directly, and each of them records what it reads."""
    readers = set()
    for node in ast.walk(TREE):
        if isinstance(node, ast.FunctionDef):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and sub.id == "INPUTS":
                    readers.add(node.name)
    assert readers <= {"_input_value", "sig", "sig_decimal", "_float_inputs", "run_cosmology",
                       "model_lineage", "report", "to_jsonable", "main"}, readers


def test_standard_library_only():
    mods = set()
    for node in ast.walk(TREE):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            mods.add(node.module.split(".")[0])
    assert mods <= {"__future__", "argparse", "cmath", "decimal", "fractions", "itertools",
                    "json", "math", "multiprocessing", "sys", "time", "typing"}, mods


def test_every_self_check_passes():
    failed = [name for name, ok, _ in RESULT["checks"] if not ok]
    assert not failed, failed


def test_cosmology_numbers():
    c = RESULT["cosmology"]
    assert abs(float(c["age_Gyr"]) - 13.7952) < 1e-3
    assert abs(float(c["Omega_Lambda"]) - 0.68461) < 1e-4
    assert abs(float(c["Omega_r"]) - 9.218e-5) < 1e-8
    assert abs(float(c["z_acc"]) - 0.6310) < 1e-3
    # within 1 sigma of Planck's age, using the script's own (uncorrelated) error
    assert abs(float(c["age_Gyr"]) - 13.787) < c["age_sigma_uncorrelated_Gyr"]


def test_flavour_verdicts():
    """The six-zero texture: V_us, V_ub and J inside their bands; V_cb, V_ub/V_cb, V_td/V_ts outside."""
    for mu in RESULT["scales"]:
        bands = RESULT["flavour"]["scales"][mu]["bands"]
        for k in ("V_us", "V_ub", "J"):
            assert bands[k]["vs_measurement"]["inside"], (mu, k)
        assert bands["V_cb"]["vs_measurement"]["n_sigma"] > 25
        assert bands["V_ub/V_cb"]["vs_measurement"]["n_sigma"] > 10
        assert bands["V_td/V_ts"]["vs_measurement"]["n_sigma"] > 4


def test_leading_order_relations():
    """The exact texture reproduces the textbook leading-order formulas."""
    for mu in RESULT["scales"]:
        blk = RESULT["flavour"]["scales"][mu]
        r, b = blk["ratios"], blk["bands"]
        a, c = math.sqrt(r["r_ds"]), math.sqrt(r["r_uc"])
        assert abs(b["V_us"]["lo"] - abs(a - c)) < 0.01
        assert abs(b["V_us"]["hi"] - (a + c)) < 0.01
        a, c = math.sqrt(r["r_sb"]), math.sqrt(r["r_ct"])
        assert abs(b["V_cb"]["lo"] - abs(a - c)) < 0.01


def test_texture_survey():
    """Part C: every predictive texture pair is tested; the verdicts are the same at every scale."""
    verdicts = None
    for mu in RESULT["scales"]:
        classes = RESULT["survey"][mu]["classes"]
        tested = [r for r in classes if r["status"] == "tested"]
        assert len(classes) == 188 and len(tested) == 83
        survivors = sorted((P.pattern_mask(r["zeros_u"]), P.pattern_mask(r["zeros_d"]))
                           for r in tested if r["survives"])
        verdicts = verdicts or survivors
        assert survivors == verdicts
        fz = ((0, 0), (0, 2), (1, 1))
        key = P.pattern_class(fz, fz)
        rec = [r for r in classes if (r["zeros_u"], r["zeros_d"]) == key][0]
        assert not rec["survives"] and rec["sigma"] > 25
    assert len(verdicts) == 1


def test_331_allows_every_entry():
    """Part D: the gauge symmetry forbids no entry; families split as {1, 2} + {3}."""
    for b in (-1, 1):
        y = RESULT["yukawa_331"][b]
        assert y["all_entries_allowed"]
        assert y["left_blocks"] == [[1, 2], [3]]
    assert len(P.residual_permutations([[1, 2], [3]])) == 2


def test_symmetry_search():
    """Part E: no abelian symmetry on the minimal 3-3-1 fields makes a usable zero; with extra
    scalars Z_6 reproduces the survivor's zeros, but the general (non-Hermitian) version predicts nothing."""
    for b, e in RESULT["symmetry"]["by_beta"].items():
        assert e["common_shift"] and not e["hermitian_possible"]
        assert all(m["with_zeros_and_mixing"] == 0 for m in e["minimal_scan"])
        assert len(e["survivors"]) == 3
        for sv in e["survivors"]:
            assert sv["verified"]
            assert (sv["symmetry"]["N"], sv["symmetry"]["triplets"]) == (6, 6)
            assert sv["general_count"]["predictions"] == -4


def test_general_texture_closure():
    """Part F: every zero pattern of general mass matrices that allows three-family mixing and
    CP violation has exactly 10 physical parameters, so none predicts anything. Every rank is
    certified (exact lower bound meets the symmetry upper bound) and J = 0 is proved symbolically."""
    cl = RESULT["closure"]
    assert cl["ordered_pairs"] == 247 ** 2 and cl["classes"] == 497
    assert cl["rank"] == {10: 470, 8: 2} and cl["cp_impossible"] == 2
    assert cl["rank_certified"] == cl["candidates"] == 472 and cl["rank_open"] == []
    assert cl["predictive_with_cp"] == []


def test_closure_certificates_are_sound():
    """The Part F proof tools on cases with known answers, including ones that must fail."""
    draw = P._IntStream(7)
    full = frozenset((i, a) for i in range(3) for a in range(3))
    diag = frozenset((i, i) for i in range(3))
    tri = frozenset((i, a) for i in range(3) for a in range(i, 3))
    # rank 10 at a point bounds the generic rank from below; the symmetry bound from above
    assert P.invariant_rank(full, full, draw) == 10
    assert 36 - P.stabilizer_rank(full, full, draw) == 10
    assert 12 - P.stabilizer_rank(diag, diag, draw) == 6 == P.invariant_rank(diag, diag, draw)
    # J: zero for diagonal (no mixing), nonzero for a triangular up sector
    assert P.cp_identically_zero(diag, diag)
    assert not P.cp_identically_zero(tri, diag)
    assert P.cp_violation_possible(tri, diag, draw, 2)


def test_model_lineage():
    """The traced graph: pure-mathematics stages read no measured input; M_P is made once and
    reaches Parts J and L without dragging cosmology along; the UV hypotheses conflict."""
    lin = RESULT["lineage"]
    assert lin["registered"] and lin["acyclic"] and lin["in_order"]
    for st in ("general_texture_closure", "gauge_331"):
        assert lin["reads"][st] == [] and lin["uses"][st] == []
    assert lin["uses"]["criticality"] == ["planck_units"]
    assert {"yukawa_relations", "criticality", "quantum_gravity"} <= set(lin["takers"]["planck_units[E_P_GeV]"])
    h0 = [s for s in lin["reaches"]["H0"] if s != "self_checks"]
    assert h0[:2] == ["cosmology", "quantum_gravity"]
    # H0 enters particle physics only through Part P's cosmological neutrino limits (and what reads them)
    assert not {"flavour", "gauge_unification", "yukawa_relations", "criticality", "proton_decay"} & set(h0)
    assert "neutrinos" in h0
    assert "criticality" in lin["reaches"]["M_t"] and "criticality" in lin["reaches"]["G"]
    assert "flavour" in lin["takers"]["gauge_unification[M_S_for_measured_alpha]"]
    assert not lin["uv_consistent"]


def test_uv_joint_test():
    """Part M: the SM up to M_P misses every condition it predicts; the MSSM survives each
    condition alone and in pairs, never predicting anything, and all three together exclude it."""
    jt = RESULT["joint"]
    rows = {(r["hypothesis"], r["conditions"]): r for r in jt["rows"]}
    assert len(rows) == 14
    assert not any(r["survives"] for (h, _), r in rows.items() if h.startswith("SM"))
    assert abs(jt["SM_pulls"]["H"] - 3.27) < 0.05
    mssm = {c: r for (h, c), r in rows.items() if h.startswith("MSSM")}
    assert all(mssm[c]["survives"] for c in mssm if len(c) < 3)
    assert all(mssm[c]["chi2"] < 1e-6 for c in (("U",), ("B",), ("H",), ("U", "B"), ("U", "H")))
    assert not mssm[("U", "B", "H")]["survives"] and mssm[("U", "B", "H")]["n_sigma"] > 20
    assert all(r["dof"] <= 0 for r in mssm.values())
    assert jt["predictive_survivors"] == []
    # theory errors: calculated from the code's own lower orders, never typed in
    th = jt["SM_theory_sigma"]
    # Part L's last orders: running 3 vs 2 loops, matching 3 vs 2, QCD 4 vs 3 (the largest)
    parts = jt["SM_theory_H_parts"]
    assert abs(parts["QCD"]) > max(abs(parts["running"]), abs(parts["matching"]))
    assert 0.3 < th["H"] < 0.6 and abs(th["U"] - 4.80) < 0.05
    assert all(r["with_theory"]["n_sigma"] <= r["n_sigma"] + 1e-9 for r in rows.values())
    # two verdicts depend on the theory errors: SM criticality (3.3 sigma on inputs, just under 3 with
    # the last-order shifts) and the MSSM with all three conditions (through unification)
    assert 2.5 < rows[("SM up to M_P", ("H",))]["with_theory"]["n_sigma"] < 3
    flips = {k for k, r in rows.items() if r["survives"] != r["with_theory"]["survives"]}
    assert flips == {("SM up to M_P", ("H",)), ("MSSM above M_S", ("U", "B", "H"))}
    assert jt["predictive_survivors_theory"] == [("SM up to M_P", ("H",))]


def test_survey_certificates_are_sound():
    """Part C certificates on cases with known answers: two exclusions are proved quickly, and the
    survivor (which has a point that fits) is never 'proved' excluded."""
    mu = RESULT["scales"][0]
    sv = RESULT["survey"][mu]["survey"]
    recs = {(P.pattern_mask(r["zeros_u"]), P.pattern_mask(r["zeros_d"])): r
            for r in RESULT["survey"][mu]["classes"] if r["status"] == "tested"}
    for key in (("00X/0X0/X0X", "00X/0X0/X0X"), ("00X/0XX/XXX", "0XX/XX0/X00")):
        assert not recs[key]["survives"] and P._certify_class((sv, recs[key]))["certified"]
    old = P.NUMERICS["cert_budget"]
    P.NUMERICS["cert_budget"] = 20000
    try:
        assert not P._certify_class((sv, recs[("00X/0XX/XXX", "0X0/X0X/0XX")]))["certified"]
    finally:
        P.NUMERICS["cert_budget"] = old


def test_survivor_prediction():
    """The survivor's prediction: |V_us|, |V_cb|, |V_ub| fix its unknowns at isolated points; two
    distinct solutions, one excluded by |V_td/V_ts| (never used by the survey), one within 3 sigma."""
    for mu in RESULT["scales"]:
        surv = [r for r in RESULT["survey"][mu]["classes"] if r["status"] == "tested" and r["survives"]]
        assert len(surv) == 1
        sols = surv[0]["prediction"]
        assert len(sols) == 2
        pulls = [abs(o["V_td/V_ts"] - 0.207) / math.hypot(o["V_td/V_ts_sigma"], 0.0032) for o in sols]
        assert min(pulls) < 3 < max(pulls)
        assert all(2.5e-5 < o["J"] < 3.5e-5 and o["J_sigma"] < 2e-6 for o in sols)


def test_parallel_textures_excluded():
    """Part G: left-right models give parallel Hermitian textures; every predictive one is excluded."""
    for mu in RESULT["scales"]:
        par = [r for r in RESULT["survey"][mu]["classes"]
               if r["status"] == "tested" and r["zeros_u"] == r["zeros_d"]]
        assert len(par) == 3 and not any(r["survives"] for r in par)


def test_quantum_gravity():
    """Part H: established quantum-gravity numbers, and the two exact identities."""
    qg = RESULT["quantum_gravity"]
    assert abs(qg["planck"]["E_P_GeV"] / 1.22089e19 - 1) < 1e-4
    assert abs(qg["black_holes"]["evaporating_now"]["mass_kg"] / 1.7298e11 - 1) < 1e-3
    assert abs(qg["numbers"]["S_dS_times_rho_ratio"] - 3 / 8) < 1e-12
    alpha_g = qg["numbers"]["alpha_G_proton"]
    assert abs(alpha_g / qg["numbers"]["m_p_over_M_P"] ** 2 - 1) < 1e-12
    en = qg["entanglement"]
    assert abs(en["concurrence"] - 1) < 1e-12 and abs(en["entropy_bits"] - 1) < 1e-12
    assert abs(en["m_min_MeV"] - 89.13) < 0.05
    assert 0.2 < qg["transmutation"]["Lambda5_GeV"] < 0.25


def test_alpha_from_unification():
    """Part I: the SM cannot unify; MSSM unification reproduces alpha only at M_S of a few TeV;
    every closed formula for 1/alpha is excluded."""
    au = RESULT["alpha_unification"]
    sm = [r for r in au["rows"] if not math.isfinite(r["M_S"])][0]
    assert abs(sm["loop2"]["inv_alpha"] - 81.85) < 0.05
    ms = au["M_S_for_measured_alpha"]["M_S_GeV"]
    assert 2000 < ms < 3200
    assert all(c["n_sigma"] > 1000 for c in RESULT["alpha_numerology"])


def test_scales_come_from_the_algorithm():
    """No scale is typed in: Parts B and C run at m_t(m_t) and at Part I's superpartner scale,
    and Part J uses Part I's unification scale."""
    mt = RESULT["flavour"]["runner"].mt_msbar
    ms = RESULT["alpha_unification"]["M_S_for_measured_alpha"]
    assert RESULT["scales"] == sorted([mt, ms["M_S_GeV"]])
    assert RESULT["yukawa"]["M_S"] == ms["M_S_GeV"] and RESULT["yukawa"]["M_GUT"] == ms["M_GUT_GeV"]


def test_yukawa_relations():
    """Part J: SU(5) and Georgi-Jarlskog ratios excluded; SM b-tau fails; MSSM needs tan(beta) ~ 1.3."""
    yk = RESULT["yukawa"]
    assert yk["ratios"]["SU5"]["n_sigma"] > 100 and yk["ratios"]["GJ"]["n_sigma"] > 5
    assert all(p["yb_over_ytau"] < 0.8 for p in yk["btau_SM"])
    assert 1.2 < yk["btau_MSSM_unity"]["tan_beta"] < 1.5
    assert all(1.2 < r["tan_beta"] < 1.5 for r in yk["fixed_point_MSSM"]["runs"])
    assert all(r["mt_msbar"] > 200 for r in yk["fixed_point_SM"]["runs"])


def test_higgs_mass_mssm():
    """Part K: with Part I's M_S and Part J's tan(beta), maximal stop mixing bounds m_h far below 125 GeV."""
    hg = RESULT["higgs"]
    assert hg["M_S"] == RESULT["alpha_unification"]["M_S_for_measured_alpha"]["M_S_GeV"]
    assert min(hg["tan_betas"]) == min(r["tan_beta"] for r in RESULT["yukawa"]["fixed_point_MSSM"]["runs"]
                                       + [RESULT["yukawa"]["btau_MSSM_unity"]])
    assert 95 < hg["mh_upper_bound"] < 110
    assert all(r["mh_no_mixing"] < r["mh_max_mixing"] for r in hg["rows"])


def test_sm_criticality():
    """Part L: lambda(M_P) = 0 at three loops with three-loop matching predicts m_h a few GeV above
    the measurement, reproducing Buttazzo et al.; the measured m_h makes lambda(M_P) slightly negative."""
    cr = RESULT["criticality"]
    two = [r for r in cr["rows"] if r["loops"] == 2]
    assert all(127 < r["m_h"] < 131 for r in two)
    assert max(r["m_h"] for r in two) - min(r["m_h"] for r in two) < 1.5   # Planck mass, matching orders
    assert 127 < cr["central"]["m_h"] < 131 and cr["central"]["matched"]
    assert (cr["central"]["loops"], cr["central"]["matching"]) == (3, "SMDR-anchored")
    # anchoring to SMDR's full two-loop plus leading three-loop matching changes M_h by under 50 MeV
    assert abs(cr["central"]["m_h"] - cr["row"]["3L/three loops"]["m_h"]) < 0.05
    assert abs(cr["smdr"]["lambda"]) < 3e-4 and abs(cr["smdr"]["y_t"]) < 5e-4
    # the higher orders move it by well under a GeV
    assert abs(cr["central"]["m_h"] - cr["two_loop_one_loop"]["m_h"]) < 1
    bz = cr["buttazzo"]
    assert bz["dev_3L"] < 1e-4 < bz["dev_2L"]
    assert bz["dev_lambda"] < bz["lambda_th"] and bz["dev_yt"] < bz["yt_th"]
    assert abs(cr["row"]["3L/two loops, QCD 3"]["m_h"] - bz["mh_linear"]) < bz["mh_linear_tol"]
    qc = cr["qcd_checks"]
    assert qc["dev_alpha_Mb"] < 1e-5 and qc["dev_gamma"] < 1e-5 and qc["dev_B4"] < 1e-6
    assert 0.3 < cr["sigma_total"] < 2
    assert 125 < cr["double"]["m_h"] < 135 and 170 < cr["double"]["M_t"] < 177
    pr = P.sm_lambda_profile(cr, 125.20)
    assert -0.03 < pr["lambda_MP"] < 0 and 1e9 < pr["mu_zero"] < 1e12


def test_four_loop_qcd():
    """Four-loop QCD with three-loop decoupling: the published coefficients reproduce RunDec and
    Chetyrkin; each lower order is the right truncation; the runner's m_t(m_t) moves as expected."""
    x = P._float_inputs()
    runs = {L: P.FlavourRunner(x, int(P.num("rg_steps_per_efold")), L) for L in (2, 3, 4)}
    mts = {L: r.mt_msbar for L, r in runs.items()}
    assert mts[2] > mts[3] > mts[4]                      # each QCD order lowers m_t(m_t)
    assert 0.3 < mts[2] - mts[4] < 1.0
    assert abs(P.qcd_beta_pi(5, 2)[1] - (102 - 38 * 5 / 3) / 16) < 1e-12
    assert P.decoupling_g2(0.2, 4, 2) == 1 and P.decoupling_m(0.2, 4, 2) == 1


def test_mass_formulas():
    """Part N: Koide's Q = 2/3 holds for the charged-lepton pole masses only; at M_Z and for the
    quarks it fails by many sigma."""
    k = RESULT["mass_formulas"]["koide"]
    assert k[0]["n_sigma"] < 2 and abs(k[0]["Q"] - 2 / 3) < 2e-5
    assert all(r["n_sigma"] > 50 for r in k[1:])
    assert abs(RESULT["mass_formulas"]["koide_m_tau_MeV"] - 1776.97) < 0.05


def test_strong_cp():
    """Part O: the chiral log gives d_n ~ 2e-16 theta-bar e cm, so |theta-bar| < 1e-10; m_u = 0 is
    excluded; m_a f_a at leading order is within 2 % of the NLO value; theta-bar = 0 at tree level
    is reachable for the Part C survivor."""
    sc = RESULT["strong_cp"]
    b = sc["bound"]
    assert 1.5e-16 < b["d_n_per_theta"] < 2.5e-16 and 5e-11 < b["theta_max"] < 1.5e-10
    assert abs(b["gbar"] - 15.5e-3) < 1e-3                  # de Vries et al.: (15.5 +- 2.5) 10^-3
    assert sc["massless_up"]["n_sigma"] > 25
    assert abs(sc["axion"]["lo_minus_nlo_rel"]) < 0.02
    assert len(sc["parity"]) == 1 and sc["parity"][0]["arg_det_over_pi"] in (0, 1)
    assert 1e-20 < sc["sm_invariant"]["mass_difference_product"] < 1e-18


def test_neutrinos():
    """Part P: the smallest mass sums; DESI + CMB excludes the inverted ordering; the m_bb bands;
    fixed mixing patterns excluded by theta13; TM1 survives with the known sum rule for delta."""
    nu = RESULT["neutrinos"]["orderings"]
    no, io = nu["NO"], nu["IO"]
    assert abs(no["sum_min"] - 0.0588) < 5e-4 and abs(io["sum_min"] - 0.0989) < 1e-3
    assert no["vs_cosmology"]["sum_mnu_DESI"]["allowed"] and not io["vs_cosmology"]["sum_mnu_DESI"]["allowed"]
    assert io["vs_cosmology"]["sum_mnu_Planck"]["allowed"]
    lo, hi = io["m_bb_at_m0_0"]
    assert 0.017 < lo < 0.020 and 0.047 < hi < 0.050
    c0, c1 = no["m_bb_cancellation_m0"]
    assert 0.001 < c0 < 0.004 and 0.005 < c1 < 0.008 and io["m_bb_cancellation_m0"] is None
    assert abs(RESULT["neutrinos"]["sum_for_omega_h2_1_eV"] - 94.1) < 0.2
    for rec in (no, io):
        rows = {r["pattern"].split(":")[0]: r for r in rec["patterns"]["rows"]}
        assert all(not r["survives"] and abs(r["pulls"]["s13sq"]) > 30 for r in rows.values() if r["unknowns"] == 0)
        assert rows["TM1"]["survives"] and rows["TM1"]["n_sigma"] < 1.5
    # TM1 sum rule: cos delta = -(1 - 5 s13^2) cos 2th23 / (2 sqrt2 s13 sin 2th23 sqrt(1 - 3 s13^2))
    x = P._float_inputs()
    s13s, s23s = x["nu_s13sq_NO"], x["nu_s23sq_NO"]
    want = -(1 - 5 * s13s) * (1 - 2 * s23s) / (2 * math.sqrt(2) * math.sqrt(s13s) * 2 * math.sqrt(s23s * (1 - s23s))
                                               * math.sqrt(1 - 3 * s13s))
    tm1 = [r for r in no["patterns"]["rows"] if r["pattern"].startswith("TM1")][0]
    assert all(abs(math.cos(math.radians(q["delta_deg"])) - want) < 1e-6 for q in tm1["solutions"])
    ss = no["seesaw"]
    assert 5e14 < ss["M_for_y_1"] < 7e14 and ss["M_max_perturbative"] < RESULT["neutrinos"]["M_GUT"]


def test_proton_decay():
    """Part Q: at Part I's M_GUT and alpha_GUT the gauge-boson channel lives longer than the Super-K
    limit (and agrees with Ellis et al.'s scaling formula); the SM's g1 = g2 point is excluded."""
    pq = RESULT["proton_decay"]
    assert abs(pq["A_L"] - pq["A_L_two_loop_quoted"]) < 0.05
    rows = {r["hypothesis"].split(" ")[0].rstrip(","): r for r in pq["rows"]}
    m = rows["MSSM"]
    assert m["allowed"] and 3 < m["ratio_to_limit"] < 30
    # Ellis et al. 2020: tau_flipped = 7.9e35 (M_X/1e16)^4 (0.0378/alpha)^2 yr, unflipped smaller by ~4.8
    ellis = 7.9e35 / 4.8 * (m["M_X"] / 1e16) ** 4 * (0.0378 / m["alpha_GUT"]) ** 2
    assert abs(m["tau_years"] / ellis - 1) < 0.2
    assert not rows["SM"]["allowed"] and rows["SM"]["ratio_to_limit"] < 1e-8
    # dimension five: minimal SUSY SU(5) at Part I's scales is excluded by p -> nubar K+ at every phase
    assert pq["d5"] and all(not r["allowed_somewhere"] for r in pq["d5"])
    for r in pq["d5"]:
        assert r["tau_min"] <= r["tau_max"] < 1e31
        assert abs(r["A_L"] - 0.53) < 0.06                    # Hisano et al., eq. 25 (one-loop alpha_s)


def test_anomalies():
    """Part R: anomaly cancellation plus Yukawas give the SM hypercharges uniquely and quantize charge;
    nu_R opens B - L (neutron charge eps); 3-3-1 needs N_f a multiple of 3, asymptotic freedom leaves 3."""
    from fractions import Fraction as Fr
    an = RESULT["anomalies"]
    hy = an["hypercharge"]
    assert hy["all_cancel"] and len(hy["solutions"]) == 2 and len(hy["with_yukawas"]) == 1
    assert hy["with_yukawas"][0] == {"Q": Fr(1, 6), "u^c": Fr(-2, 3), "d^c": Fr(1, 3), "L": Fr(-1, 2), "e^c": Fr(1)}
    ch = hy["charges"]
    assert (ch["u"], ch["d"], ch["e"], ch["nu"]) == (Fr(2, 3), Fr(-1, 3), Fr(-1), Fr(0))
    assert ch["proton_plus_electron"] == 0 and ch["neutron"] == 0
    assert hy["Y_Q_zero_branch_cancels"] and not hy["Y_Q_zero_branch_has_yukawas"]
    assert hy["nu_R_family_cancels"] and hy["nu_R_hydrogen_charge"] == 0 and hy["nu_R_neutron_charge_per_eps"] == 1
    assert an["witten_doublets_per_family"] % 2 == 0
    assert an["331_part_D"]["SU3L_cubed"] == 0
    assert [a["families"] for a in an["331_allowed"]] == [3, 6, 9] and an["331_families_with_af"] == [3]


def test_baryon_asymmetry():
    """Part S: eta_B from Planck; the SM fails (crossover, CP far too small); the leptogenesis factors
    come out of the field content (28/79, g* = 106.75 + 7/4, 0.96e-2) and need M_1 > ~1e8 GeV."""
    from fractions import Fraction as Fr
    ba = RESULT["baryon_asymmetry"]
    assert abs(ba["eta_B"] / 6.12e-10 - 1) < 0.01
    assert ba["sphaleron"]["B_over_BminusL"] == Fr(28, 79)
    assert ba["transition"]["n_sigma_above"] > 20
    assert ba["cp_measure"]["delta_CP"] < 1e-15
    lg = ba["leptogenesis"]
    assert lg["g_star"] == Fr(427, 4) + Fr(7, 4) and lg["g_s_today"] == Fr(43, 11)
    assert abs(lg["eta_per_epsilon_kappa"] - 0.96e-2) < 0.01e-2           # Buchmuller, Di Bari, Plumacher
    assert all(1e8 < r["M1_min"] < 1e9 and r["window_open"] for r in lg["rows"])
    assert abs(lg["di_example_M1"] / 4e9 - 1) < 0.4                       # Davidson-Ibarra's own example


def test_so10():
    """Part T: B - L needs nu^c; sin^2 theta_W = 3/8 and the 3/5 normalization from the 16; minimal
    Yukawa ratios excluded; non-SUSY Pati-Salam unification at M_I ~ 1e11-1e12 GeV passes proton decay."""
    from fractions import Fraction as Fr
    so = RESULT["so10"]
    assert all(v == 0 for v in so["bl_anomalies_with_nu_c"].values())
    assert any(v != 0 for v in so["bl_anomalies_without_nu_c"].values())
    assert so["weinberg"]["sin2_theta_W"] == Fr(3, 8) and so["weinberg"]["GUT_norm"] == Fr(3, 5) == P.GUT_NORM
    assert so["minimal_10"]["s_over_c"] > 3
    ps = so["pati_salam"]
    assert ps["b_PS"] == {"4": Fr(-23, 3), "2L": Fr(-3), "2R": Fr(11, 3)}
    assert ps["consistent"] and 1e11 < ps["M_I"] < 1e12 and 5e15 < ps["M_GUT"] < 3e16
    assert ps["tau_p_allowed"] and ps["M_I_in_leptogenesis_window"]


def test_scorecard():
    """Part U: SM to M_P fails unification and the baryon asymmetry; minimal SUSY SU(5) fails the Higgs
    mass and proton decay; the D-parity SO(10) chains fail proton decay; Pati-Salam fails nothing."""
    sc = RESULT["scorecard"]
    v = sc["verdict"]
    assert {"U", "A"} <= set(v["SM to M_P"]["fails"])
    assert {"H", "P"} <= set(v["minimal SUSY SU(5)"]["fails"])
    assert "P" in v["SO(10) via PS+D"]["fails"] and "P" in v["SO(10) via LR+D"]["fails"]
    assert v["SO(10) via PS"]["fails"] == [] and "SO(10) via PS" in sc["survivors"]
    ph = sc["chain_higgs"]["PS"]
    assert 125 < ph["m_h"] < 127 and abs(ph["pull"]) < 2


def test_so10_chains():
    """Part T5: chain b from the field content (one loop as published); two loops move M_I but keep
    every chain consistent; the solver reproduces the linear one-loop solution."""
    from fractions import Fraction as Fr
    ch = RESULT["so10"]["chains"]
    assert ch["PS"]["b1"] == [Fr(-23, 3), Fr(-3), Fr(11, 3)]
    assert ch["PS+D"]["b1"] == [Fr(-14, 3), Fr(11, 3), Fr(11, 3)]
    assert ch["LR"]["b1"] == [Fr(-7), Fr(-3), Fr(-7, 3), Fr(11, 2)]
    assert ch["LR+D"]["b1"] == [Fr(-7), Fr(-7, 3), Fr(-7, 3), Fr(7)]
    for c in ch.values():
        assert c["loop1"]["consistent"] and c["loop2"]["consistent"]
        assert c["loop2"]["residual"] < 1e-6
        assert abs(c["two_loop_shift_ln_MI"]) < 2.5
    ps = RESULT["so10"]["pati_salam"]
    assert abs(ch["PS"]["loop1"]["M_I"] / ps["M_I"] - 1) < 1e-4


def test_chain_vacuum():
    """Part T6: the SM's lambda turns negative near 6e10 GeV; chains breaking below it (LR, LR+D) can be
    stabilized by the scalar threshold, PS+D cannot; lambda_SM(M_I) has the sign of mu_0 - M_I."""
    vac = RESULT["so10"]["vacuum"]
    assert 1e10 < vac["mu0"] < 2e11 and vac["mu0_band_Mt"][0] < vac["mu0"] < vac["mu0_band_Mt"][-1]
    rows = vac["rows"]
    assert rows["LR"]["stabilizable"] and rows["LR+D"]["stabilizable"] and not rows["PS+D"]["stabilizable"]
    assert all((r["lambda_SM_at_MI"] > 0) == r["below_mu0"] for r in rows.values())
    assert RESULT["scorecard"]["rows"]["SO(10) via LR"]["V"]["status"] == "pass"


def test_leptogenesis_efficiency():
    """Part S: m_* ~ 1.07e-3 eV; z_B of 6-8 in the natural range (Buchmuller, Di Bari, Plumacher); at full
    efficiency M_1 >= 6.6e8 GeV (their eq. 32); the natural range needs M_1 >~ 1e10 GeV."""
    lg = RESULT["baryon_asymmetry"]["leptogenesis"]
    assert abs(lg["m_star_eV"] / 1.08e-3 - 1) < 0.03
    zs = [e["z_B"] for e in lg["efficiency"]]
    assert 5 < min(zs) and max(zs) < 9
    m1 = min(r["M1_min"] for r in lg["rows"])
    assert abs(m1 / 6.6e8 - 1) < 0.15
    lo, hi = lg["M1_min_natural"]
    assert 5e9 < lo < 5e10 < hi < 5e11
    sc = RESULT["scorecard"]["rows"]
    assert sc["SO(10) via PS"]["A"]["status"] == "trade" and sc["SO(10) via LR"]["A"]["status"] == "open"


def test_dark_matter():
    """Part V: misalignment from its ingredients reproduces eq. 170 of Di Luzio et al.; post-inflation all
    the dark matter needs f_a ~ 2e11 GeV (m_a ~ 28 micro-eV); at Pati-Salam's M_I about two thirds; at the
    left-right M_I no angle suffices."""
    dm = RESULT["dark_matter"]
    assert abs(dm["check_eq170"]["Omega_h2"] / 0.12 - 1) < 0.05
    assert 1.5e11 < dm["f_a_all_dm_post"] < 2.5e11 and 2.4e-5 < dm["m_a_all_dm_post_eV"] < 3.4e-5
    ps, lr = dm["chains"]["PS"], dm["chains"]["LR"]
    assert 0.4 < ps["fraction_post"] < 0.9 and ps["pre_possible"]
    assert lr["fraction_post"] < 0.05 and not lr["pre_possible"]
    assert RESULT["scorecard"]["rows"]["SO(10) via LR"]["D"]["status"] == "open"


def test_website_data_is_current():
    """assets/site-data.js (written by tools/site_data.py) shows the numbers the script computes."""
    import json
    txt = open(os.path.join(ROOT, "assets", "site-data.js"), encoding="utf-8").read()
    data = json.loads(txt[txt.index("{"):txt.rindex("}") + 1])
    assert abs(data["criticality"]["m_h_pred"] - RESULT["criticality"]["central"]["m_h"]) < 1e-6
    assert abs(data["higgs_mssm"]["bound"] - RESULT["higgs"]["mh_upper_bound"]) < 1e-6
    assert data["checks"][0] == len(RESULT["checks"])


def test_report_matches_expected_output():
    got = P.report(RESULT).splitlines()
    want = [ln for ln in open(EXPECTED, encoding="utf-8").read().splitlines() if not ln.startswith("Elapsed")]
    assert got == want


def test_command_line_runs():
    out = subprocess.run([sys.executable, PATH, "--help"], capture_output=True, text=True, timeout=60)
    assert out.returncode == 0 and "--json-out" in out.stdout
