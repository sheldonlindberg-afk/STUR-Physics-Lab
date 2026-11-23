"""Pins production_v2_2.py, the repository's one simulation.

Three kinds of test:
  1. The rule: no non-integer number may appear in the script outside INPUTS,
     COMPARISONS and NUMERICS, and measured comparisons never feed a calculation.
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
TABLES = ("INPUTS", "COMPARISONS", "NUMERICS")


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
    assert not bad, f"numbers outside INPUTS/COMPARISONS/NUMERICS: {bad}"


def test_comparisons_never_feed_a_calculation():
    """COMPARISONS is read only by the functions that judge or print results."""
    readers = set()
    for node in ast.walk(TREE):
        if isinstance(node, ast.FunctionDef):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and sub.id == "COMPARISONS":
                    readers.add(node.name)
    assert readers <= {"_comparison", "_derived_vub_over_vcb", "report", "to_jsonable"}, readers


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
    CP violation has exactly 10 physical parameters, so none predicts anything."""
    cl = RESULT["closure"]
    assert cl["ordered_pairs"] == 247 ** 2 and cl["classes"] == 497
    assert cl["rank"] == {10: 470, 8: 2} and cl["cp_impossible"] == 2
    assert cl["predictive_with_cp"] == []


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


def test_report_matches_expected_output():
    got = P.report(RESULT).splitlines()
    want = [ln for ln in open(EXPECTED, encoding="utf-8").read().splitlines() if not ln.startswith("Elapsed")]
    assert got == want


def test_command_line_runs():
    out = subprocess.run([sys.executable, PATH, "--help"], capture_output=True, text=True, timeout=60)
    assert out.returncode == 0 and "--json-out" in out.stdout
