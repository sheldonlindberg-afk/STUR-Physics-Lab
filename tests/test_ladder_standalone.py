"""Pins src/ladder_standalone.py: the copy-paste ladder script must stay standard-library-only
and agree with the repository's own ladder modules."""
import ast, os, subprocess, sys
SRC = os.path.join(os.path.dirname(__file__), "..", "src")
PATH = os.path.join(SRC, "ladder_standalone.py")
sys.path.insert(0, SRC)
import ladder_standalone as S
import m331_breaking as B
import chiral_breaking as CB
import graviton_exchange as GX
import stur_gravity_entanglement as GE


def test_imports_only_the_standard_library():
    allowed = {"fractions", "itertools", "math", "random", "textwrap", "time"}
    mods = set()
    for node in ast.walk(ast.parse(open(PATH).read())):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            mods.add(node.module.split(".")[0])
    assert mods <= allowed, mods


def test_agrees_with_the_repository():
    vals = dict(g=0.652, gX=0.79, w=4000.0, v1=150.0, v2=190.0)
    for v in ("-1/sqrt3", "+1/sqrt3"):
        mine = S.mass_matrix(v, *vals.values())
        theirs = B.mass_matrix(v).subs({B.g: vals["g"], B.gX: vals["gX"], B.w: vals["w"], B.v1: vals["v1"], B.v2: vals["v2"]})
        assert max(abs(mine[i][j] - float(theirs[i, j])) for i in range(9) for j in range(9)) < 1e-6
    assert abs(S.casimir_safe_gap() - GE.casimir_vs_gravity_gap(GE.BASE["m"], GE.BASE["dx"], GE.BASE["tau"], "parallel")) < 1e-12
    assert abs(S.sqrt(S.MU_PLUS_MD * S.COND_13**3) / S.F_PI - CB.gmor_numbers()[0]) < 1e-12
    mine_dphi = GX.branch_phases()[0]
    assert abs(mine_dphi - 2.1868) < 1e-3


def test_links_agree_with_the_repository():
    import ladder_links as LL
    assert (S.U_AMU, S.K_COUL, S.E_CH, S.ALPHA_0) == (LL.U_AMU, LL.K_COUL, LL.E_CH, LL.ALPHA_0)
    assert S.EPS_PE_BOUND == LL.EPS_PE_BOUND
    assert all(abs(x - y) < 1e-12 for x, y in zip(S.GAMMA_PI0, LL.GAMMA_PI0_MEAS))
    import chiral_breaking as CB
    assert S.F_PI == CB.F_PI and S.M_PI0 == CB.M_PI0


def test_planck_window_poles_agree_with_the_three_loop_running():
    import ladder_links as LL
    import m331_exact as E
    window = LL.g_window()[0]
    for v, (p3, p5) in S.POLES_331.items():
        assert abs(p3 / (window[v][0] * E.M_PLANCK) - 1) < 1e-4
        assert abs(p5 / (window[v][1] * E.M_PLANCK) - 1) < 1e-4


def test_runs_isolated_and_every_check_passes():
    out = subprocess.run([sys.executable, "-I", "-S", PATH], capture_output=True, text=True, timeout=300).stdout
    assert "ALL CHECKS PASS" in out and "FAIL" not in out
    ref = open(os.path.join(os.path.dirname(__file__), "..", "results", "ladder", "standalone.txt")).read()
    assert "Checks passed: 45/45" in ref and "ALL CHECKS PASS" in ref
    assert "Checks passed: 45/45" in out


def test_exit_status_is_nonzero_when_a_check_fails():
    ok = subprocess.run([sys.executable, "-I", "-S", PATH], capture_output=True, timeout=300)
    assert ok.returncode == 0
    code = open(PATH).read().replace("ok = abs(gpinn / G_PINN_EMP - 1) < 0.02", "ok = False")
    code = code.replace("abs(gpinn / G_PINN_EMP - 1) < 0.02, \"data\"", "False, \"data\"")
    assert code != open(PATH).read()
    bad = subprocess.run([sys.executable, "-I", "-S", "-c", code], capture_output=True, text=True, timeout=300)
    assert bad.returncode == 1 and "SOME CHECKS FAILED" in bad.stdout
