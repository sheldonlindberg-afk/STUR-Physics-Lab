"""Pins ckm_from_331_overlaps.py, the repository's copy-paste script.

It must stay standard-library-only, its eigensolvers must agree with numpy, the
self-consistent loop must converge, and its output must match results/ckm_331/output.txt.
"""
import ast, os, subprocess, sys
import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..")
PATH = os.path.join(ROOT, "ckm_from_331_overlaps.py")
sys.path.insert(0, ROOT)
import ckm_from_331_overlaps as C


def test_standard_library_only():
    allowed = {"__future__", "cmath", "dataclasses", "math", "typing"}
    tree = ast.parse(open(PATH, encoding="utf8").read())
    mods = {a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    mods |= {n.module.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
    assert mods <= allowed, mods - allowed


def test_eigensolver_matches_numpy():
    rng = np.random.default_rng(7)
    for _ in range(25):
        a = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
        h = a @ a.conj().T
        ev, u = C.jacobi_hermitian_eig(h.tolist())
        u = np.array(u)
        assert np.allclose(ev, np.linalg.eigvalsh(h), rtol=1e-12, atol=1e-12)
        assert np.allclose(u @ np.diag(ev) @ u.conj().T, h, atol=1e-12)
        assert np.allclose(u.conj().T @ u, np.eye(3), atol=1e-12)


def test_mode_solver_matches_numpy():
    grid = [-6.0 + 12.0 * i / 200 for i in range(201)]
    pot = [y * y + 0.3 * y for y in grid]
    ev, modes = C.lowest_modes(grid, pot, 4)
    h = grid[1] - grid[0]
    m = np.diag([2 / h**2 + v for v in pot]) + np.diag([-1 / h**2] * 200, 1) + np.diag([-1 / h**2] * 200, -1)
    ref = np.linalg.eigvalsh(m)[:4]
    assert np.allclose(ev, ref, rtol=1e-10)
    for k, psi in enumerate(modes):
        assert np.allclose(m @ np.array(psi), ref[k] * np.array(psi), atol=1e-6 * max(1.0, ref[k]))


def test_self_consistent_solution():
    sol = C.solve_self_consistent()
    assert sol["converged"] and sol["net_x_charge"] == 0.0
    a = sol["A"]
    assert max(abs(a[i] - a[-1 - i]) for i in range(len(a))) < 1e-10   # parity-even attractor
    res = C.light_ckm(*C.build_mass_matrices(sol))
    assert res["J"] == 0.0                                                # no complex input


def test_demo_output_is_pinned():
    out = subprocess.run([sys.executable, PATH], capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stdout + out.stderr
    expected = open(os.path.join(ROOT, "results", "ckm_331", "output.txt"), encoding="utf8").read()
    assert out.stdout == expected
    assert "7/7 checks passed" in out.stdout and "no fitted inputs" in out.stdout
