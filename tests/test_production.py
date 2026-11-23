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


def test_report_matches_expected_output():
    got = P.report(RESULT).splitlines()
    want = [ln for ln in open(EXPECTED, encoding="utf-8").read().splitlines() if not ln.startswith("Elapsed")]
    assert got == want


def test_command_line_runs():
    out = subprocess.run([sys.executable, PATH, "--help"], capture_output=True, text=True, timeout=60)
    assert out.returncode == 0 and "--json-out" in out.stdout
