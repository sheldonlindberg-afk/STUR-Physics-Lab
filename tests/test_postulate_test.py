"""Pins the key numbers of src/stur_postulate_test.py (fast subset, no plots)."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_postulate_test as P


def test_crossing_mode():
    assert abs(2 * P.x_star() - 2.399357) < 1e-5


def test_simulation_matches_exact_formulas():
    ws, gs = [0.7, 1.3], [0.25, 0.35]
    r = P.simulate(ws, gs, 1.0, 2.0)
    G, E = P.analytic_discrete(ws, gs, 1.0, 2.0)
    assert abs(r["Gamma"] - G) < 1e-6 and abs(r["dEB"] - E) < 1e-6
    assert abs(r["Sigma"] - (r["I"] + r["D"])) < 1e-9          # Esposito identity
    assert abs(r["Gamma"] - 2.200749) < 1e-5
    assert 1.0 * r["Gamma"] > 4 * r["dEB"]   # k_B T * Gamma vs dE_B: P2 off by >4x here


def test_bath_energy_is_temperature_independent():
    ws, gs = [0.7, 1.3], [0.25, 0.35]
    E1 = P.analytic_discrete(ws, gs, 0.3, 2.0)[1]
    E2 = P.analytic_discrete(ws, gs, 3.0, 2.0)[1]
    assert E1 == E2


def test_high_T_scaling_opposite_to_postulate():
    eta, t = 0.05, 3.0
    g1, g2 = P.Gamma_ohmic(t, 10.0, eta), P.Gamma_ohmic(t, 20.0, eta)
    assert abs(np.log(g2 / g1) / np.log(2) - 1.0) < 0.01         # Gamma ∝ T, postulate ∝ 1/T


def test_cl_ratio_is_dx_over_lambda_squared():
    r = P.cl_numbers(86.909 * P.amu, 1e-6, 1e-5, 1.0, 1e-3)
    assert abs(r["E_post"] / r["E_in"] - (1e-6 / r["lam"]) ** 2) < 1e-9 * r["E_post"] / r["E_in"]
