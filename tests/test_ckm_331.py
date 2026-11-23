"""Pins ckm_from_331_overlaps.py, the repository's copy-paste script.

It must stay standard-library-only, its Hermitian eigensolver must agree with numpy,
and its demo output must match results/ckm_331/output.txt.
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


def test_u1x_selection_in_demo():
    grid, left, ur, dr, us, ds = C._demo_inputs()
    _, info = C.build_derived_yukawa_331(grid, left, ur, us)
    assert info["allowed_couplings"] == 9 and info["forbidden_by_u1x_or_rep"] == 9


def test_demo_output_is_pinned():
    out = subprocess.run([sys.executable, PATH], capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stdout + out.stderr
    expected = open(os.path.join(ROOT, "results", "ckm_331", "output.txt"), encoding="utf8").read()
    assert out.stdout == expected
    assert "7/7 checks passed" in out.stdout
