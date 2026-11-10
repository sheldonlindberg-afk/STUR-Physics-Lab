"""Pins src/stur_derivation.py: the chain from the quantum level up."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_derivation as D


def test_area_law_and_modular_structure():
    k, pts = D.area_law_coefficient(ns=(10, 14, 18))
    assert abs(k - 0.3047) < 5e-4
    assert abs(D.modular_slope(20) - 1) < 1e-3


def test_G_from_entanglement_round_trip():
    a = D.K.cutoff_for_G(1, 0.3046)
    assert abs(D.G_from_entanglement(a, 1, 0.3046) / D.G_SI - 1) < 1e-12
    # G scales as a^2 / N
    assert abs(D.G_from_entanglement(2 * a, 4, 0.3046) / D.G_SI - 1) < 1e-12


def test_two_diamond_phase_from_actions():
    b = D.ge.BASE
    rij = D.ge.branch_distances(b["dx"], b["gap"], "parallel")
    R = D.ge.radius(b["m"])
    S = np.array([[-D.F.interaction_energy_tegr(b["m"], R, rij[i, j])[2] * b["tau"]
                   for j in range(2)] for i in range(2)]) / D.HBAR
    assert abs(S[0, 0] + S[1, 1] - S[0, 1] - S[1, 0] - 0.59382) < 1e-4
