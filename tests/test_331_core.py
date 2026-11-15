"""Pins src/m331_core.py: one definition of the 3-3-1 group theory and field content, used by
the repository's scripts and copied verbatim into the one-paste script."""
import ast
import os
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import m331_core as C
import m331_exact as E
import m331_standalone as S
import m331_yukawa as Y


def test_core_is_standard_library_only():
    tree = ast.parse(open(os.path.join(ROOT, "src", "m331_core.py")).read())
    mods = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    mods |= {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
    assert mods == {"fractions"}


def test_standalone_copy_is_current():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build_m331_standalone.py"), "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout


def test_the_repository_scripts_use_the_core():
    assert E.Group is C.Group and E.coefficients is C.coefficients and Y.yukawa_coeff is C.yukawa_coeff
    for v in C.VARIANTS:
        for Nc, Ng in ((3, 3), (5, 5), (2, 4), (1, 2)):
            assert E.MODELS[v](Nc, Ng)[1:] == C.model(Nc, v, Ng)[1:]
            assert S.coefficients(*S.model(Nc, v, Ng)[:3]) == C.coefficients(*C.model(Nc, v, Ng)[:3])


def test_models_refuse_an_anomalous_generation_count():
    import pytest
    for bad in ((3, 4), (2, 2), (5, 7)):
        with pytest.raises(ValueError):
            C.model(*bad[:1], "-1/sqrt3", bad[1])
