"""Pins rebuild/campaigns/induced_g: both accepted builds pass the verifier gate with the hidden oracle and the
audit's checks, agree with each other, and the chain embeds build a's exports unchanged."""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(__file__), "..")
CAMP = os.path.join(ROOT, "rebuild", "campaigns")
BUILDS = os.path.join(CAMP, "induced_g", "builds")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_both_builds_pass_the_verifier_gate():
    for b in ("a", "b"):
        d = os.path.join(tempfile.mkdtemp(), b)
        shutil.copytree(os.path.join(BUILDS, b), d)        # the gate writes its report into the build directory
        r = subprocess.run([sys.executable, "gate.py", d, "--mode", "verifier", "--campaign", "induced_g",
                            "--oracle", os.path.join("induced_g", "oracle.py")], cwd=CAMP, capture_output=True, text=True)
        assert r.returncode == 0 and "GATE PASSED" in r.stdout, r.stdout[-2000:]


def test_builds_agree():
    a = load(os.path.join(BUILDS, "a", "induced_g.py"), "ig_a")
    b = load(os.path.join(BUILDS, "b", "induced_g.py"), "ig_b")
    for d in range(2, 13):
        for kind in ("scalar", "dirac", "vector", "vector_no_ghosts") + (("weyl",) if d % 2 == 0 else ()):
            assert abs(a.k1(kind, d, 0.3) - b.k1(kind, d, 0.3)) < 1e-14
    for p in ((1e19, 18, 69, 17, 0.0), (1e19, 18, 69, 17, 1 / 6), (2.0, 18, 66, 17, 1 / 6)):
        ga, gb = a.inv_G(*p), b.inv_G(*p)
        assert abs(ga - gb) <= 1e-14 * abs(ga) and (a.mpl(*p) is None) == (b.mpl(*p) is None)


def test_chain_embeds_build_a():
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import chain_first_principles as C
    a = load(os.path.join(BUILDS, "a", "induced_g.py"), "ig_a2")
    for p in ((5.3355e19, 18, 69, 17, 0.0), (3.49103e19, 18, 69, 17, 1 / 6)):
        assert C.induced_g.mpl(*p) == a.mpl(*p)
    assert "numpy" not in open(os.path.join(ROOT, "src", "chain_first_principles.py")).read().replace("need numpy", "")
