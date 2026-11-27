"""Writes sims/<name>.diff for every sim: its unified diff against production_v2_2.py (tests/test_sims.py checks it)."""
import glob
import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "tests"))
from test_sims import sim_diff  # noqa: E402

for path in sorted(glob.glob(os.path.join(ROOT, "sims", "*.py"))):
    name = os.path.splitext(os.path.basename(path))[0]
    with open(os.path.join(ROOT, "sims", f"{name}.diff"), "w", encoding="utf-8") as fh:
        fh.write(sim_diff(name))
    print(f"sims/{name}.diff")
