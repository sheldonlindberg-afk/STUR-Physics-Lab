"""The adjacent sims in sims/: each is production_v2_2.py with one piece changed, and each obeys the same rules.

  1. The rule, as for the production script: no non-integer number outside INPUTS, COMPARISONS, NUMERICS and
     LITERATURE; COMPARISONS never feed a calculation; INPUTS are read only through the tracer; standard library only.
  2. The published diff (sims/<name>.diff) is the real difference from production_v2_2.py, so the change can be
     audited line by line; the expected output exists; every number the website shows for a sim is in it.
  3. With STUR_SIM=<name> (one CI job per sim), the sim runs, every self-check passes, the report equals
     results/sims/<name>.txt and --json-out's conversion works.
"""
import ast
import difflib
import glob
import importlib.util
import json
import os
import re

import pytest

ROOT = os.path.join(os.path.dirname(__file__), "..")
BASE = os.path.join(ROOT, "production_v2_2.py")
SIMS = sorted(glob.glob(os.path.join(ROOT, "sims", "*.py")))
TABLES = ("INPUTS", "COMPARISONS", "NUMERICS", "LITERATURE")
NAMES = [os.path.splitext(os.path.basename(p))[0] for p in SIMS]


def _tree(path):
    return ast.parse(open(path, encoding="utf-8").read())


def _readers(tree, name):
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and sub.id == name:
                    out.add(node.name)
    return out


def sim_diff(name):
    """The unified diff of sims/<name>.py against production_v2_2.py (what sims/<name>.diff must contain)."""
    base = open(BASE, encoding="utf-8").read().splitlines(keepends=True)
    sim = open(os.path.join(ROOT, "sims", f"{name}.py"), encoding="utf-8").read().splitlines(keepends=True)
    return "".join(difflib.unified_diff(base, sim, "production_v2_2.py", f"sims/{name}.py"))


def test_there_is_a_sim():
    assert SIMS


@pytest.mark.parametrize("path", SIMS, ids=NAMES)
def test_no_tunable_number_outside_the_input_tables(path):
    tree = _tree(path)
    ranges = []
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            target = node.targets[0] if isinstance(node, ast.Assign) else node.target
            if getattr(target, "id", None) in TABLES:
                ranges.append((node.lineno, node.end_lineno))
    assert len(ranges) == len(TABLES)
    numeric_string = re.compile(r"^[+-]?(\d+\.\d*|\.\d+|\d+)([eE][+-]?\d+)?$")
    bad = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or any(a <= node.lineno <= b for a, b in ranges):
            continue
        v = node.value
        if isinstance(v, float) and not v.is_integer():
            bad.append((node.lineno, v))
        if isinstance(v, complex) and v != 1j:
            bad.append((node.lineno, v))
        if isinstance(v, str) and numeric_string.match(v.strip()) and not v.strip().isdigit():
            bad.append((node.lineno, v))
    assert not bad, bad


@pytest.mark.parametrize("path", SIMS, ids=NAMES)
def test_comparisons_and_inputs_are_read_only_where_allowed(path):
    tree = _tree(path)
    assert _readers(tree, "COMPARISONS") <= {"_comparison", "_derived_vub_over_vcb", "report", "to_jsonable"}
    assert _readers(tree, "INPUTS") <= {"_input_value", "sig", "sig_decimal", "_float_inputs", "run_cosmology",
                                        "model_lineage", "report", "to_jsonable", "main"}


@pytest.mark.parametrize("path", SIMS, ids=NAMES)
def test_standard_library_only(path):
    mods = set()
    for node in ast.walk(_tree(path)):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            mods.add(node.module.split(".")[0])
    assert mods <= {"__future__", "argparse", "cmath", "decimal", "fractions", "itertools",
                    "json", "math", "multiprocessing", "sys", "time", "typing"}, mods


@pytest.mark.parametrize("name", NAMES)
def test_published_diff_is_current(name):
    path = os.path.join(ROOT, "sims", f"{name}.diff")
    assert open(path, encoding="utf-8").read() == sim_diff(name), "run: python tools/sim_diff.py"


@pytest.mark.parametrize("name", NAMES)
def test_website_numbers_are_in_the_expected_output(name):
    """Every number index.html shows for a sim (marked data-sim="<name>") appears in its expected output."""
    expected = open(os.path.join(ROOT, "results", "sims", f"{name}.txt"), encoding="utf-8").read()
    html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    assert f'data-src="sims/{name}.py"' in html, "the sim has no Copy button on the website"
    shown = re.findall(rf'<span data-sim="{name}">([^<]+)</span>', html)
    missing = [v for v in shown if v not in expected]
    assert not missing, missing


FULL = os.environ.get("STUR_SIM")


@pytest.mark.skipif(not FULL, reason="set STUR_SIM=<name> to run a sim in full (about 25 minutes)")
def test_full_run():
    path = os.path.join(ROOT, "sims", f"{FULL}.py")
    spec = importlib.util.spec_from_file_location(FULL, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    res = mod.run()
    failed = [n for n, ok, _ in res["checks"] if not ok]
    assert not failed, failed
    want = [ln for ln in open(os.path.join(ROOT, "results", "sims", f"{FULL}.txt"), encoding="utf-8").read().splitlines()
            if not ln.startswith("Elapsed")]
    assert mod.report(res).splitlines() == want
    json.dumps(mod.to_jsonable(res))
