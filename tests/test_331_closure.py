"""Pins src/m331_closure.py: Witten redundant; Yukawa-independent; cutoff window."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import m331_closure as C

REF = os.path.join(os.path.dirname(__file__), "..", "results", "m331", "331_closure.txt")


def test_anomaly_plus_asymptotic_freedom_force_odd_nc_and_ng_equals_nc():
    sol = C.solutions(nc_max=80, ng_max=600)
    assert sol and all(Nc == Ng and Nc % 2 == 1 for Nc, Ng, n in sol)
    assert all(n == (Nc + 1) // 2 for Nc, Ng, n in sol)


def test_selection_without_any_yukawa_at_the_worst_spectrum():
    p = C.T.pole(3, "+1/sqrt3", MV=2e3, rJ=0.5, rS=1 / 3, n_light=2, yukawas=False)
    assert 1.4 < p / C.M_PLANCK < 1.7
    ref = open(REF).read()
    for line in ("g = 4 pi    on        +1/sqrt3   3.76e+12 ... 2.00e+19",
                 "alpha = 1   off       +1/sqrt3   2.24e+12 ... 1.38e+19"):
        assert line in ref
    assert "NO" not in ref.split("C3")[1]
