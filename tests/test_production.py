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
import json
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
    # every result handed across field contents has a stated reason (CROSS_EDGES), and the SO(10) and 3-3-1 stages
    # carry their field content
    assert lin["cross_edges"] and not lin["cross_unexplained"], lin["cross_unexplained"]
    for st in ("so10", "so10_yukawa", "dark_matter", "gauge_331", "w_mass"):
        assert "uv" in P.STAGES[st]


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
    assert an["331_full_ok"] and all(v == 0 for d in an["331_full"].values() for v in d.values())
    assert all(d["SU3L^3"] != 0 and d["X^3"] != 0 for d in an["331_full_no_leptons"].values())


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
    mass and proton decay; the D-parity SO(10) chains fail proton decay; PS and LR fail one condition each."""
    sc = RESULT["scorecard"]
    v = sc["verdict"]
    assert {"U", "A"} <= set(v["SM to M_P"]["fails"])
    assert {"H", "P"} <= set(v["minimal SUSY SU(5)"]["fails"])
    assert "P" in v["SO(10) via PS+D"]["fails"] and "P" in v["SO(10) via LR+D"]["fails"]
    # Pati-Salam fails the fermion masses, left-right the neutrinos (SO(10)'s v_R): no complete hypothesis survives
    assert v["SO(10) via PS"]["fails"] == ["F"] and v["SO(10) via LR"]["fails"] == ["N"] and sc["survivors"] == []
    # the closest chains are those with the fewest fails, ties carried (not broken by counting trades)
    assert sorted(sc["closest_chains"]) == ["LR", "PS"]
    # the labels follow the definitions: no chain "passes" unification (three unknowns, three conditions) or the
    # Higgs mass (lambda(M_I) = 0 is not imposed, Part T6)
    for h, r in sc["rows"].items():
        if h.startswith("SO(10) via "):
            assert r["U"]["status"] in ("trade", "fail") and r["H"]["status"] == "open"
            assert r["N"]["status"] != "pass" and r["V"]["status"] != "pass"
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
    # a stabilizing threshold of unknown size absorbs the condition: a trade, not a pass
    assert RESULT["scorecard"]["rows"]["SO(10) via LR"]["V"]["status"] == "trade"


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
    # one B - L ceiling for every stage: M_1 <= 2 sqrt(4 pi) M_I/g_R (Parts T7, U, Y4 agree)
    sc = RESULT["scorecard"]["rows"]
    lr2 = RESULT["so10"]["chains"]["LR"]["loop2"]
    assert abs(P.m_r_ceiling(lr2) / lr2["M_I"] - RESULT["so10_yukawa"]["LR"]["M_R_max_over_M_I"]) < 1e-9
    assert (sc["SO(10) via LR"]["A"]["status"] == "trade") == (P.m_r_ceiling(lr2) >= lo)
    assert sc["SO(10) via PS"]["A"]["status"] == "trade"


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


def test_chain_thresholds():
    """Part T7: with thresholds up to the band, PS+D stays excluded by proton decay (robust), while the
    LR+D exclusion and the PS and LR verdicts can flip; the zero-threshold point lies inside every range."""
    th = RESULT["so10"]["thresholds"]
    ch = RESULT["so10"]["chains"]
    assert not th["PS+D"]["proton_flips"] and th["LR+D"]["proton_flips"]
    for nm, t in th.items():
        assert t["corners"] >= 8
        assert t["M_I"][0] <= ch[nm]["loop2"]["M_I"] <= t["M_I"][1]
        assert t["tau_p"][0] <= ch[nm]["loop2"]["tau_p_years"] <= t["tau_p"][1]


def test_w_mass():
    """Part W: the SM's two-loop M_W reproduces the PDG global fit within its error and agrees with the
    measurements within 2 sigma; the Higgs-mass choice moves it by about a MeV."""
    wm = RESULT["w_mass"]
    c = wm["comparisons"]
    assert abs(c["PDG 2024 global-fit prediction"]["pull"]) < 1
    assert all(abs(v["pull"]) < 2 for v in c.values())
    assert abs(wm["shift_to_measured_m_h"]) < 0.003 and 0.003 < wm["sigma"] < 0.01


def test_heavy_spectrum():
    """Part T8: the SU(2)_L triplets (10,3,1) of the 126 and (15,3,1) of the 210 dominate; proton decay flips
    if either is lighter than M_GUT by a factor of a few; within a factor 10 the spectrum decides everything."""
    hs = RESULT["so10"]["heavy_spectrum_PS"]
    rows = {r["multiplet"]: r for r in hs["rows"]}
    assert len(rows) == 8
    big = sorted(rows.values(), key=lambda r: -abs(r["dlntau"]))[:2]
    assert {r["multiplet"] for r in big} == {"126: (10,3,1)", "210: (15,3,1)"}
    assert 0.2 < rows["126: (10,3,1)"]["proton_flip_ratio"] < 1
    assert hs["tau_p"][1] / hs["tau_p"][0] > 1e5
    assert all(P.so10_decomposition_index(r) == [P.SO10_INDEX[r]] * 3 for r in P.SO10_TO_PS)


def test_z_pole_and_closed_cosmology():
    """Part W's Z pole: sin^2 theta_eff within 2 sigma of LEP+SLC. Part X: with misalignment alone at
    Pati-Salam's M_I the universe is too old; all of Omega_c reproduces Part A's age."""
    zp = RESULT["w_mass"]["z_pole"]
    assert 0.2314 < zp["sin2_eff"] < 0.2318 and all(abs(c["pull"]) < 2 for c in zp["comparisons"].values())
    cc = RESULT["closed_cosmology"]
    # Part X follows every surviving chain, or every closest one (fewest fails, ties carried) when none survives
    surv = [h.replace("SO(10) via ", "") for h in RESULT["scorecard"]["survivors"] if h.startswith("SO(10) via ")]
    assert set(cc["tied"]) == set(surv or RESULT["scorecard"]["closest_chains"])
    assert cc["chain"] == ("LR" if "LR" in cc["tied"] else list(cc["tied"])[0])
    assert all(c_["age_pull"] > 10 for c_ in cc["tied"].values())
    frac = RESULT["dark_matter"]["chains"][cc["chain"]]["fraction_post"]
    assert abs(cc["string_fraction_needed"] - (1 - frac)) < 1e-9 and cc["age_pull"] > 10
    assert abs(cc["age_with_all_dm_Gyr"] / float(RESULT["cosmology"]["age_Gyr"]) - 1) < 5e-3


def test_potential_210():
    """Part T9: the 210 potential's Goldstones are massless, (15,3,1) and (15,1,3) differ only by the cubic;
    a few percent of the coupling box is viable, and most viable potentials pass proton decay."""
    pz = RESULT["so10"]["potential_210"]
    cv = pz["curvatures"]
    assert all(abs(v) < 1e-9 for v in cv["(6,2,2)"].values())
    assert all(abs(cv["(15,3,1)"][q] - cv["(15,1,3)"][q]) < 1e-9 for q in ("Q1", "Q2", "Q3", "Q4"))
    assert abs(cv["(15,3,1)"]["eta"] + cv["(15,1,3)"]["eta"]) < 1e-9 and cv["(15,3,1)"]["eta"] > 0
    assert 50 < pz["viable"] < pz["tried"] / 5
    assert 0.5 < pz["frac_proton_ok"] <= 1 and 0.5 < pz["frac_leptogenesis_ok"] <= 1
    lo, mid, hi = pz["tau_p_quantiles"]
    assert lo < mid < hi
    # T10: the 126 from its couplings to <210>; (10,3,1) and (10bar,1,3) differ only by the cubic
    c6 = pz["with_126"]["coefficients_126"]
    assert abs(c6["(10,3,1)"]["cubic"] + c6["(10bar,1,3)"]["cubic"]) < 1e-9 and c6["(10,3,1)"]["cubic"] > 0
    assert all(abs(c6["(10,3,1)"][k] - c6["(10bar,1,3)"][k]) < 1e-9 for k in ("norm", "D", "E", "F"))
    w6 = pz["with_126"]
    assert w6["viable"] > 50 and w6["frac_proton_ok"] > 0.5
    # T11: the 10: only A_ij splits doublet from triplet; with the light doublet the triplet is heavy
    w10 = pz["with_10"]
    assert (w10["A_SO4"], w10["A_SO6"]) == (6, 0) and w10["split_per_kappa"] == -1
    assert w10["viable"] > 50 and w10["frac_proton_ok"] > 0.5
    assert 0.3 < w10["triplet_light_quantiles"][1] < 5


def test_so10_yukawa():
    """Part Y: the minimal Pati-Salam chain's light Higgs lies in one SU(4) irrep, so M_e = M_d or -3 M_d:
    excluded by tens of sigma; the general 10 + 126 sum rule reaches the charged leptons at the LR M_GUT."""
    yy = RESULT["so10_yukawa"]
    ps = yy["PS"]
    assert ps["excluded"] and min(ps["worst_pull_10"], ps["worst_pull_126"]) > 10
    ratios = {g["pair"]: g["ratio"] for g in ps["generations"]}
    assert 3 < ratios["m_mu/m_s"] < 5 and 1 < ratios["m_tau/m_b"] < 2 and ratios["m_e/m_d"] < 1
    lr = yy["LR"]
    assert lr["reaches"] and lr["worst_rel_miss"] < 0.01
    sc = RESULT["scorecard"]["rows"]
    assert sc["SO(10) via PS"]["F"]["status"] == "fail" and sc["SO(10) via LR"]["F"]["status"] == "trade"


def test_type2_and_ledger():
    """Part Y3: type-II neutrinos from the 10 + 126 sum rule fail without supersymmetry (b and tau do not
    converge). Part Z: every free number carries a status; only discrete ones are calculated."""
    t2 = RESULT["so10_yukawa"]["LR"]["type2"]
    assert not t2["reaches"] and t2["n_sigma_worst"] > 5 and t2["b_tau_mismatch"] < -0.2
    lg = RESULT["ledger"]
    st = {r["quantity"]: r["status"] for r in lg["rows"]}
    assert st["hypercharges and electric charge"] == "calculated" and st["weak mixing angle at unification"] == "calculated"
    assert st["neutrino masses and mixing"] == "open" and st["cosmological constant"] == "open"
    assert set(st.values()) <= {"calculated", "related", "traded", "bounded", "open", "input"}
    assert sum(lg["counts"].values()) == len(lg["rows"]) == 15
    # nothing from a framework that is not the closest hypothesis is credited: 3-3-1 is not on the scorecard, and
    # the Hermitian texture of Part C belongs to no framework tested here
    assert st["number of families"] == "open" and st["quark mixing (CKM)"] == "input"
    assert set(lg["tied"]) == set(RESULT["closed_cosmology"]["tied"])


def test_heavy_spectrum_lr():
    """Part T12: the 3221 decompositions add up to the SO(10) indices (B - L included); SU(2)_L-triplet coloured
    states lower M_I when heavy and SU(2)_R ones raise it; the spectrum can lift M_I to where the neutrino fits put
    B - L breaking, within a small factor of M_GUT, keeping the proton."""
    from fractions import Fraction as Fr
    assert all(P.so10_decomposition_index_3221(r) == [Fr(P.SO10_INDEX[r])] * 4 for r in P.SO10_TO_3221)
    rows = {r["multiplet"]: r for r in RESULT["so10"]["heavy_spectrum_LR"]["rows"]}
    assert rows["126: (6,3,1)"]["dlnMI"] < -1 < 1 < rows["126: (6,1,3)"]["dlnMI"]
    lf = RESULT["so10_yukawa"]["lift"]
    assert lf["reached"] and 1 < lf["spread"] < 3 and lf["proton_ok"]
    # with the sharpened bound (2 sqrt(4 pi) M_I / g_R) the target lies below mu_0: the vacuum stays stabilizable
    assert lf["vacuum_ok"] == (lf["target_M_I"] < RESULT["so10"]["vacuum"]["mu0"])
    assert abs(lf["M_I"] / lf["target_M_I"] - 1) < 0.05


def test_lr_potential():
    """Part T13: the left-right chain's 210 vacuum with both vevs and the 126 at it. The highest weights reproduce
    the decompositions; the Pati-Salam limit equals T9 and T10; the Goldstones are massless. Most viable potentials
    keep the proton and lower M_I; almost none gives the lift the neutrino fits need."""
    pl = RESULT["so10"]["potential_lr"]
    ck = pl["checks"]
    assert ck["decompositions"] == 0 and max(ck[k] for k in ("PS_limit_210", "PS_limit_126", "goldstones", "unbroken")) < 1e-9
    w2, w6 = pl["with_210"], pl["with_126"]
    assert w2["viable"] > 100 and w6["viable"] > 500 and w6["frac_proton_ok"] > 0.8
    assert w6["M_I_quantiles"][1] < RESULT["so10"]["chains"]["LR"]["loop2"]["M_I"]
    assert ck["PS_limit_10"] < 1e-9                       # the 10's couplings reduce to T11's at the Pati-Salam vev
    w10 = pl["with_10"]
    assert w10["viable"] > 300 and w10["frac_proton_ok"] > 0.8
    lo, mid, hi = w10["higgs_126_fraction_quantiles"]
    assert 0 < lo < mid < hi < 1                            # the light Higgs is a genuine 10-126 mixture
    assert 0.2 < w10["triplet_light_quantiles"][1] < 5
    lf = RESULT["so10_yukawa"]["lift"]
    assert lf["potential_n"] == w10["viable"] and lf["potential_hits"] < 0.01 * lf["potential_n"]


def test_v_r_prediction():
    """Neutrino tension: with M_R = Y126 v_R and Y126 fixed by the charged fermions, the type I + II fits put v_R
    orders of magnitude above the left-right chain's, beyond anything the thresholds (Part T7) can move."""
    vr = RESULT["so10_yukawa"]["v_R"]
    lift_max = RESULT["so10"]["thresholds"]["LR"]["M_I"][1] / RESULT["so10"]["chains"]["LR"]["loop2"]["M_I"]
    # 5b: the fits' |b/d| ~ 30 cut d, and the margin, about 30-fold (it was > 100 x lift_max before)
    assert vr["ratio"][0] > 10 * lift_max and 1e12 < vr["v_R_needed"][0] < vr["v_R_needed"][1] < 1e17
    assert RESULT["scorecard"]["rows"]["SO(10) via LR"]["N"]["status"] == "fail"


def test_proton_running_and_triplets():
    """Item 4: the operators' anomalous dimensions from the bilinear rule reproduce Ellis et al.; above M_I each chain
    runs them with its own group, a modest change; the colour triplets with the fitted Yukawas are negligible."""
    from fractions import Fraction as Fr
    for op in ("S1", "S2"):
        assert [-g / 4 for g in P.operator_gamma("SM", op)] == [Fr(v) for v in P.LITERATURE["proton_decay_d6"]["value"]["SM"][op]]
    assert P.operator_gamma("SU3", "S1") == [Fr(-4), Fr(-9, 2), Fr(-9, 2), Fr(-1, 2)]
    x = P._float_inputs()
    for nm, ch in P.so10_chains().items():
        sol = RESULT["so10"]["chains"][nm]["loop2"]
        a_ch, a_sm = P.proton_short_distance_chain(x, ch, sol, "S1"), P.proton_short_distance(x, sol["M_GUT"], None, "S1")
        assert 1 < a_ch / a_sm < 1.5
    tp = RESULT["so10_yukawa"]["triplet"]
    # 5b: the split of the 10 and 126 shares by |a/c|, |b/d| raises the triplet Yukawas ~ 50-fold (bounds loosened with it)
    assert tp["tau_p_years"] > 1e43 and tp["M_T_min_GeV"] < 1e-2 * RESULT["so10"]["chains"]["LR"]["loop2"]["M_GUT"]


def test_left_right_running():
    """Part Y: matrix running SM -> M_I -> left-right -> M_GUT. The reduced RGEs equal the general formula; the
    left-right running brings b and tau closer than SM running does, whatever the unknown Takagi phases."""
    rn = RESULT["so10_yukawa"]["running"]
    assert max(P.matrix_rge_checks(11).values()) < 1e-12
    assert rn["SM"]["b_tau"] < rn["b_tau_dirac_like_up"] < rn["LR"]["b_tau"] < 0
    lo, hi = rn["b_tau_phase_range"]
    assert hi - lo < 1e-3 and lo - 1e-3 < rn["LR"]["b_tau"] < hi + 1e-3
    vc = P.vector_threshold_constants(P.so10_chains()["LR"])["M_GUT"]
    inv = [i + float(c) / (12 * math.pi) for i, c in zip(rn["LR"]["inv_alpha_M_GUT"], vc)]
    assert max(inv) - min(inv) < 1e-5
    va = rn["LR"]["V_abs"]
    assert 0.2 < va[0][1] < 0.23 and 0.03 < va[1][2] < 0.045


def test_complex_10_potential():
    """The complex 10's own potential: the light complex bidoublet fixes its doublet masses (Schur complement zero);
    viable points pass proton decay; the fits' |a/c|, |b/d| are matched per point by two circles, and every match is
    reported against that point's own v_R."""
    wc = RESULT["so10"]["potential_lr"]["with_complex_10"]
    assert wc["viable"] > 100 and wc["frac_proton_ok"] > 0.5 and len(wc["points"]) == wc["viable"]
    cx = RESULT["so10_yukawa"]["v_R"]["complex_10"]
    assert cx["points"] == wc["viable"]
    if cx["matches"]:
        assert cx["ratio_quantiles"][0] <= cx["ratio_quantiles"][2] <= cx["ratio_quantiles"][4]


def test_dark_sector():
    """Part AA: every field of the minimal theory is R-even (no candidate but the axion); minimal phi^4 and phi^2
    inflation are excluded by r, the plateau is allowed; SM Higgs inflation is excluded by lambda < 0 above mu_0."""
    ds = RESULT["dark_sector"]
    assert ds["r_odd"] == [] and ds["scalar_16_odd"] and ds["fermion_10_odd"]
    inf = ds["inflation"]
    assert inf["plateau (Higgs, or xi phi^2 R)"]["allowed"]
    assert not inf["phi^4 (minimal)"]["allowed"] and not inf["phi^2 (minimal)"]["allowed"]
    assert ds["higgs"]["excluded"] and ds["higgs"]["lambda_needed"] > 1


def test_d5_eq19():
    """7b: the full higgsino term has eq. 19's scaling exactly; with Hisano et al.'s alpha_p their constant follows."""
    d5 = RESULT["proton_decay"]["d5"]
    cs = [r["eq19_constant"] for r in d5]
    assert (max(cs) - min(cs)) / cs[0] < 1e-9
    assert 1 < 4e35 / d5[0]["eq19_constant_hisano_alpha_p"] < 1.5


def test_second_vev_and_delta_r():
    """5c: neither the second bidoublet vev (|k2/k1| <= m_b/m_t) nor a perturbative Delta_R coupling makes b and tau
    meet at the left-right M_GUT; f only pushes tau up. The MS-bar vector constants move M_I and M_GUT by a few %."""
    rn = RESULT["so10_yukawa"]["running"]
    assert rn["b_tau_k2_range"][1] < -0.2 and rn["b_tau_f_max"] < rn["LR"]["b_tau"] < 0
    assert 0 < rn["f3_max_M_I"] < P.PERTURBATIVE_LIMIT
    for c in RESULT["so10"]["chains"].values():
        assert 1 < c["loop2"]["M_I"] / c["loop2_tree_matching"]["M_I"] < 1.2


def test_complex_10():
    """5b: a real 10 forces |a/c| = 1 (|c2| = |1 - c1|) and then cannot give the charged leptons; with the complex 10 the
    fits fix |b/d|, which lowers the predicted v_R, but perturbativity alone keeps it above the chain's."""
    lr = RESULT["so10_yukawa"]["LR"]
    assert lr["real_10"]["chi2_min"] > 9 > lr["chi2_min"]
    vr = RESULT["so10_yukawa"]["v_R"]
    assert vr["r126_range"][0] > 1 and vr["v_R_needed"][1] < vr["v_R_whole_share_to_d"][1]
    assert vr["floor_ratio"] > 1


def test_one_running():
    """Item 6: one matrix running for every coupling. The MSSM matrix RGE equals the superpotential formula; on the
    third generation the engine is Part J's right-hand side; at m_t(m_t) it starts from Part J's couplings and the
    QCD-run ratios; the light generations move Part J's third-generation results by under a percent."""
    flav = RESULT["flavour"]
    assert set(P.matrix_rge_checks(5)) == {"SM", "LR", "LR_Delta", "MSSM"}
    mt, st = P.couplings_at_mt(flav)
    m0 = P.masses_at_scale(flav, mt)
    kap = flav["runner"].v / math.sqrt(2)
    base = flav["ratios"][mt]
    assert all(abs(m0[k][2] / (st[3 + i] * kap) - 1) < 1e-12 for i, k in enumerate("ude"))
    assert abs(m0["u"][1] / m0["u"][2] / base["r_ct"] - 1) < 1e-9 and abs(m0["d"][0] / m0["d"][1] / base["r_ds"] - 1) < 1e-9
    chk = P.matrix_running_checks(flav, 3, RESULT["yukawa"])
    assert chk["rhs_SM"] < 1e-12 and chk["rhs_MSSM"] < 1e-12
    assert 0 < chk["light_SM"] < 1e-2 and 0 < chk["light_MSSM_btau"] < 1e-2
    hi = max(flav["ratios"])
    assert flav["ratios"][hi]["r_uc"] != base["r_uc"]           # the light ratios run now (they were held fixed)


def test_type1_seesaw():
    """Part Y4: type I adds no unknown (M_D is fixed by the sum rule's c1, c2), types I + II one complex ratio;
    each fit does at least as well as type II, and its right-handed scale is computed without the 126's vevs."""
    lr = RESULT["so10_yukawa"]["LR"]
    t2, t1, t12 = lr["type2"], lr["type1"], lr["type12"]
    assert (t2["unknowns"], t1["unknowns"], t12["unknowns"]) == (15, 15, 17)
    assert t12["chi2_min"] <= t1["chi2_min"] < t2["chi2_min"]
    assert t12["starts"] > t1["starts"]                          # I + II also starts from the best I and II points
    for t_ in (t1, t12):
        mr = t_["scales"]["M_R_GeV"]
        assert mr[0] <= mr[1] <= mr[2] and abs(t_["scales"]["M_R_over_M_I"] - mr[2] / lr["M_I"]) < 1e-9 * mr[2] / lr["M_I"]
    assert abs(lr["M_R_max_over_M_I"] - 2 * math.sqrt(4 * math.pi) / lr["g_R"]) < 1e-12 and 0.4 < lr["g_R"] < 0.8
    # the search finds the mixed fits, and every one needs the right-handed scale far above the chain's M_I
    assert t12["fits_found"] > 0 and t12["chi2_min"] < 9
    assert t12["M_R_over_M_I_range"][0] > 10 * lr["M_R_max_over_M_I"]
    lo, hi = t12["delta_deg_range"]
    assert 0 <= lo <= hi < 360
    assert P.so10_dirac_identity(3) < 1e-12


def test_website_data_is_current():
    """assets/site-data.js (written by tools/site_data.py) shows the numbers the script computes."""
    import json
    txt = open(os.path.join(ROOT, "assets", "site-data.js"), encoding="utf-8").read()
    data = json.loads(txt[txt.index("{"):txt.rindex("}") + 1])
    assert abs(data["criticality"]["m_h_pred"] - RESULT["criticality"]["central"]["m_h"]) < 1e-6
    assert abs(data["higgs_mssm"]["bound"] - RESULT["higgs"]["mh_upper_bound"]) < 1e-6
    assert data["checks"][0] == len(RESULT["checks"])
    # the scorecard and ledger the page renders are the ones this run computed
    sc = RESULT["scorecard"]
    assert data["scorecard"]["survivors"] == list(sc["survivors"])
    assert {h: {c: e["status"] for c, e in r.items()} for h, r in data["scorecard"]["rows"].items()} == \
        {h: {c: e["status"] for c, e in r.items()} for h, r in sc["rows"].items()}
    assert [(r["quantity"], r["status"]) for r in data["ledger"]["rows"]] == \
        [(r["quantity"], r["status"]) for r in RESULT["ledger"]["rows"]]
    lr = RESULT["so10_yukawa"]["LR"]
    for k in ("type2", "type1", "type12"):
        assert abs(data["yukawa"]["seesaw"][k]["chi2"] - lr[k]["chi2_min"]) < 1e-9 * max(1, lr[k]["chi2_min"])
    assert data["survivor"]["chain"] == RESULT["closed_cosmology"]["chain"]


def test_every_page_value_is_filled():
    """Every number index.html marks with data-v is filled from assets/site-data.js, so no stale typed-in
    value can survive a rerun; README states the current number of self-checks."""
    html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    script = html[html.index('<script src="assets/site-data.js"></script>'):]
    keys = set(re.findall(r'data-v="([^"]+)"', html))
    filled = set(re.findall(r'"([a-z]+\.?[A-Za-z0-9]*)":', script)) | set(re.findall(r'vals\["([^"]+)"\]', script))
    suffixes = re.findall(r'\[\["(\w+)", "type2"\], \["(\w+)", "type1"\], \["(\w+)", "type12"\]\]', script)
    for pre in re.findall(r'vals\["([^"]+)" \+ k\[0\]\]', script):
        filled |= {pre + s_ for s_ in (suffixes[0] if suffixes else ())}
    assert keys and keys <= filled, sorted(keys - filled)
    readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    assert f"It ends with {len(RESULT['checks'])} self-checks" in readme.replace("\n", " ")


def test_report_matches_expected_output():
    got = P.report(RESULT).splitlines()
    want = [ln for ln in open(EXPECTED, encoding="utf-8").read().splitlines() if not ln.startswith("Elapsed")]
    assert got == want


def test_json_export():
    """--json-out writes every number: the whole result must convert to JSON."""
    json.dumps(P.to_jsonable(RESULT))


def test_command_line_runs():
    out = subprocess.run([sys.executable, PATH, "--help"], capture_output=True, text=True, timeout=60)
    assert out.returncode == 0 and "--json-out" in out.stdout
