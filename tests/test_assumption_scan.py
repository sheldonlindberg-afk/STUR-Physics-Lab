"""Pins the matches found by src/stur_assumption_scan.py (fast subset)."""
import os, sys
import numpy as np
from scipy.optimize import brentq
from scipy.special import zeta
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_assumption_scan as A

PTS = [A.one_mode(a2, T) for a2, T in [(0.05, 0.1), (0.5, 0.8), (0.2, 3.2)]]


def test_visibility_is_twice_quanta_variance():          # IDENTITY, all T
    for r in PTS:
        assert abs(2 * r["VarQ"] / r["Gamma"] - 1) < 1e-6


def test_esposito_record_identity():                     # <Q> = k_B T D(record||rho_beta)
    for r in PTS:
        assert abs(r["Q"] / (r["T"] * r["D_rec"]) - 1) < 1e-6
        assert abs(r["Q"] / (r["T"] * r["D_pm"]) - 0.25) < 1e-6


def test_fidelity_noise_temperature_identity():           # <Q> = k_B T_noise (-ln F)
    for r in PTS:
        assert abs(r["Q"] / (r["Teff"] * r["mlnF"]) - 1) < 1e-5


def test_postulate_itself_not_an_identity():
    ratios = [r["Q"] / (r["T"] * r["Gamma"]) for r in PTS]
    assert max(ratios) / min(ratios) > 10


def test_crossings_are_model_dependent():
    pd = 2 * brentq(lambda x: x * np.tanh(x) - 1, 0.1, 5)
    gad = brentq(lambda x: x * np.tanh(x / 2) - 1, 0.1, 10)
    assert abs(pd - 2.399357) < 1e-5 and abs(gad - 1.543405) < 1e-5


def test_photon_mean_energy():
    assert abs(7 * zeta(8) / zeta(7) - 6.9703) < 1e-4
