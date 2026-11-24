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
                    "json", "math", "sys", "time", "typing"}, mods


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
    assert [s for s in lin["reaches"]["H0"] if s != "self_checks"] == ["cosmology", "quantum_gravity"]
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
    """The survivor's prediction: with |V_us|, |V_cb|, |V_ub| at their measured values (1 sigma),
    J and |V_td/V_ts| follow; both ranges contain the measured values."""
    for mu in RESULT["scales"]:
        surv = [r for r in RESULT["survey"][mu]["classes"] if r["status"] == "tested" and r["survives"]]
        assert len(surv) == 1
        pr = surv[0]["prediction"]
        lo, hi = pr["J"]
        assert lo <= 3.12e-5 <= hi and hi - lo < 1e-5
        lo, hi = pr["V_td/V_ts"]
        assert 0.15 < lo <= hi < 0.3


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
