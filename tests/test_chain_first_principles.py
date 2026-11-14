"""Pins src/chain_first_principles.py, the copy-paste force chain on blind build 2026-11-b, and
src/first_principles_standalone.py, that build's stages alone.

Each must be exactly what tools/build_chain_standalone.py writes, use only the standard library, run
clean, and give the same numbers as the build it embeds and as src/force_chain.py where they overlap."""
import ast
import contextlib
import io
import math
import os
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PATH = os.path.join(ROOT, "src", "chain_first_principles.py")
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "rebuild"))

import build_chain_standalone as gen  # noqa: E402
import chain_first_principles as C    # noqa: E402
import contract                       # noqa: E402
import harness                        # noqa: E402


def test_are_what_the_generator_writes():
    for kind in gen.OUTPUTS:
        assert open(gen.out_path(kind), encoding="utf-8").read() == gen.render(kind), kind


def test_import_only_the_standard_library():
    for kind in gen.OUTPUTS:
        mods = set()
        for node in ast.walk(ast.parse(open(gen.out_path(kind), encoding="utf-8").read())):
            if isinstance(node, ast.Import):
                mods |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                mods.add(node.module.split(".")[0])
        assert mods <= harness.STDLIB_ALLOWED | {"sys", "types"}, (kind, mods)


def test_stages_file_runs_and_matches_the_saved_output():
    r = subprocess.run([sys.executable, gen.out_path("stages")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-2000:]
    assert r.stdout == open(os.path.join(ROOT, "results", "first_principles_standalone.txt"), encoding="utf-8").read()
    import first_principles_standalone as S
    ledger = harness.ledger(os.path.join(ROOT, "rebuild", "builds", gen.BUILD_ID))
    assert sum(len(m.PROVENANCE) for _, m in S.STAGES) == sum(len(s["exports"]) for s in contract.STAGES)
    assert S.casimir.cp_integral() == C.casimir.cp_integral() and ledger


def test_runs_clean_and_matches_the_saved_output():
    r = subprocess.run([sys.executable, PATH], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:]
    assert "FAIL" not in r.stdout and "VERDICT: every hand-off checks" in r.stdout
    assert r.stdout == open(os.path.join(ROOT, "results", "chain_first_principles.txt"), encoding="utf-8").read()


def test_embedded_stages_equal_the_build():
    """The indentation into functions changed nothing: every probe of the harness agrees exactly."""
    build = os.path.join(ROOT, "rebuild", "builds", gen.BUILD_ID)
    want = harness.probe_values(build)
    harness.unload(build)
    got = {f"{st}.{fn}": harness._flat(getattr(getattr(C, contract.stage(st)["module"]), fn)(*args))
           for st, fn, args in harness.PROBES}
    assert got.keys() == want.keys() and len(got) >= 20
    for k in want:
        assert got[k] == want[k], k


def test_agrees_with_the_force_chain():
    """Same quantities as src/force_chain.py's ledger, within the differences rebuild/chain_compare.py records."""
    import force_chain
    with contextlib.redirect_stdout(io.StringIO()):
        ledger, _ = force_chain.run()
        C.LEDGER.clear(), C.CHECKS.clear(), C.FIT.clear(), C.REPLACED.clear()
        assert C.run() == 0
    theirs = {name: value for name, value, _, _ in ledger}
    mine = {name: value for name, value, _, _ in C.LEDGER}
    assert (mine["Q_u"], mine["Q_d"], mine["N_c"], mine["q_p + q_e"]) == \
        (theirs["Q_u"], theirs["Q_d"], theirs["N_c"], theirs["q_p + q_e"])
    for name, rtol in (("M_Pl", 1e-12), ("f_pi", 1e-9), ("pi0 width", 2e-9), ("m_pi O(p^4)", 1e-9), ("alpha(0)", 1e-9),
                       ("neutrality needed", 1e-9), ("gap", 3e-4), ("phase", 5e-4), ("l", 1e-12),
                       ("Sgr A* T_H", 1e-12), ("end temperature", 1e-9)):
        assert math.isclose(float(mine[name]), float(theirs[name]), rel_tol=rtol), name


def test_every_step_after_the_first_uses_an_earlier_one():
    with contextlib.redirect_stdout(io.StringIO()):
        C.LEDGER.clear(), C.CHECKS.clear(), C.FIT.clear(), C.REPLACED.clear()
        C.run()
    used_by = {u for _, _, _, used in C.LEDGER for u in used}
    assert used_by == set(range(3, 9)), used_by      # step 2 produces alpha(0) and takes nothing
    assert all(made < u for _, _, made, used in C.LEDGER for u in used)
    assert len(C.FIT) >= 8 and max(abs(row[4]) for row in C.FIT) <= 2
