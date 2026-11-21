"""Pins src/gravity_from_331.py: it is what tools/build_gravity_standalone.py writes, it runs as pasted (standard
library, outside the repository), its output is the committed one, and its numbers are the repository's."""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "src"))
import build_gravity_standalone as BG  # noqa: E402

SRC = os.path.join(ROOT, "src", "gravity_from_331.py")


def run_isolated():
    d = tempfile.mkdtemp()
    shutil.copy(SRC, os.path.join(d, "pasted.py"))
    return subprocess.run([sys.executable, "-I", "pasted.py"], cwd=d, capture_output=True, text=True, timeout=120)


def test_file_is_current():
    assert open(SRC, encoding="utf-8").read() == BG.render(), "run python3 tools/build_gravity_standalone.py"


def test_runs_as_pasted_and_matches_committed_output():
    r = run_isolated()
    assert r.returncode == 0, r.stderr[-2000:]
    assert r.stdout == open(os.path.join(ROOT, "results", "gravity", "output.txt"), encoding="utf-8").read()
    assert "[math] 9/9 pass" in r.stdout and "[model] 3/3 pass" in r.stdout and "FAIL" not in r.stdout


def test_no_dependencies_outside_the_standard_library():
    src = open(SRC, encoding="utf-8").read()
    for mod in ("numpy", "scipy", "sympy", "mpmath"):
        assert f"import {mod}" not in src


def test_numbers_are_the_repositorys():
    import induced_gravity as I
    out = open(os.path.join(ROOT, "results", "gravity", "output.txt"), encoding="utf-8").read()
    lo, hi = I.main()["mpl_range"]
    assert f"M_Pl {lo:.2f} to {hi:.2f} x measured" in out
    assert "115 embeddings, 0 matches, at least 49 chiral exotics" in out
