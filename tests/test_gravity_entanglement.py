"""Pins the numbers of src/stur_gravity_entanglement.py."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_gravity_entanglement as g

B = g.BASE


def test_baseline_phases():
    lin = g.phases(**B, geometry="linear")
    par = g.phases(**B, geometry="parallel")
    assert abs(lin[1, 0] - 0.7911) < 1e-4
    assert abs(g.entangling_phase(lin) + 0.3139) < 1e-4
    assert abs(g.entangling_phase(par) - 0.5938) < 1e-4
    assert abs(g.concurrence_pure(par) - 0.2926) < 1e-4


def test_split_field_never_entangles():
    for geo in ("linear", "parallel"):
        for m in (1e-15, 1e-14, 1e-13):
            ph = g.phases(m, B["dx"], B["gap"], 10.0, geometry=geo, lam=0.0)
            assert abs(g.entangling_phase(ph)) < 1e-9
            assert g.negativity(g.state(ph)) < 1e-12


def test_entangling_phase_linear_in_lambda():
    full = g.entangling_phase(g.phases(**B, geometry="parallel"))
    for lam in (0.1, 0.5, 0.9):
        assert abs(g.entangling_phase(g.phases(**B, geometry="parallel", lam=lam)) - lam * full) < 1e-12


def test_pure_state_negativity_is_half_concurrence():
    ph = g.phases(**B, geometry="parallel")
    assert abs(g.negativity(g.state(ph)) - g.concurrence_pure(ph) / 2) < 1e-12


def test_witness_and_runs():
    rho = g.state(g.phases(**B, geometry="parallel"))
    W = g.witness_for(rho)
    assert abs(np.real(np.trace(rho @ W)) + 0.1463) < 1e-4
    assert 400 < g.runs_for_witness(W, rho) < 470
    prod = g.state(g.phases(**B, geometry="parallel", lam=0.0))
    assert np.real(np.trace(prod @ W)) > -1e-12


def test_dephasing_floor_and_threshold():
    assert abs(g.lambda_floor(0.05, **B) - 0.169) < 2e-3
    ph = g.phases(**B, geometry="parallel")
    assert g.negativity(g.state(ph, 0.28)) > 0 and g.negativity(g.state(ph, 0.30)) < 1e-12


def test_backgrounds():
    assert abs(g.gas_decoherence_rate(B["m"], 1e-15, 0.15) - 0.105) < 0.005
    gap = g.casimir_vs_gravity_gap(B["m"], B["dx"], B["tau"], "parallel")
    assert 170e-6 < gap < 190e-6
    assert g.self_gravity_shift(B["m"], B["dx"], B["tau"]) < 1e-16
