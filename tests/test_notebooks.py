"""The study notebooks run against the current code and reproduce the headline numbers."""
import json, os, glob, contextlib, io
ROOT = os.path.join(os.path.dirname(__file__), "..")
NB = os.path.join(ROOT, "notebooks")


def run(name):
    cells = json.load(open(os.path.join(NB, name), encoding="utf8"))["cells"]
    ns, out, cwd = {"display": print}, io.StringIO(), os.getcwd()
    os.chdir(NB)
    try:
        with contextlib.redirect_stdout(out):
            for c in cells:
                if c["cell_type"] == "code":
                    exec("".join(c["source"]), ns)
    finally:
        os.chdir(cwd)
    return out.getvalue()


def test_every_notebook_is_listed():
    assert len(glob.glob(os.path.join(NB, "*.ipynb"))) == 5


def test_tegr_notebook():
    out = run("01_tegr_classic_tests.ipynb")
    assert "42.98 arcsec/century" in out and "1.7512 arcsec" in out and "net 38.54" in out


def test_decoherence_notebook():
    out = run("02_complementarity_and_decoherence.ipynb")
    assert out.count("V^2 + D^2 = 1.000000") == 7 and "-ln V = 0.6000   2 Var(dN) = 0.6000" in out


def test_bmv_notebook():
    assert "entangling phase = -0.3139 rad" in run("03_gravity_mediated_entanglement.ipynb")


def test_area_law_notebook():
    assert "fitted slope c_s = 0.30" in run("04_area_law.ipynb")


def test_teleparallel_3d_notebook():
    out = run("05_teleparallel_3d_quantum.ipynb")
    assert out.count("T + R - B = 0  (exact)") == 2
    assert "exact +3.982143e-04" in out and "40 random spin sets" in out
