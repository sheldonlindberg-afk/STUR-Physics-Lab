"""Pins the numbers of src/stur_measurement.py (measurement, double slit, entanglement)."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_measurement as M


def test_standard_hydrogen_reproduced():
    r = M.hydrogen_scf(self_interaction=False)
    assert abs(r["E"] + 0.5) < 1e-4 and abs(r["rmean"] - 1.5) < 1e-3


def test_real_charge_cloud_binds_too_weakly():
    r = M.hydrogen_scf(self_interaction=True)
    assert abs(r["E"] * M.HARTREE_EV + 6.638) < 0.01
    assert r["E"] < -121 / 512                     # below the exponential variational bound
    assert M.H_IONIZATION_EV / (-r["E"] * M.HARTREE_EV) > 2.0


def test_strong_force_and_positronium():
    rng, x = M.yukawa_exponent()
    assert abs(rng - 1.4138) < 1e-3 and x > 37000
    f = M.positronium_1s2s_mhz()
    assert abs(f - M.PS_1S2S_MHZ) / M.PS_1S2S_MHZ < 1e-4


def test_complementarity_and_cloud():
    for th in np.linspace(0, np.pi / 2, 7):
        _, _, V, D = M.double_slit(th)
        assert abs(V - abs(np.cos(th))) < 1e-5 and abs(D * D + V * V - 1) < 1e-5
    assert M.double_slit(0.0, model="cloud")[2] < 1e-12
    assert abs(M.electron_wavelength_pm(50.0) - 5.355) < 1e-3


def test_bell_and_swapping():
    assert abs(M.chsh(lambda a, b: -np.cos(a - b)) - 2 * np.sqrt(2)) < 1e-12
    def mc(model):
        return lambda a, b: np.mean(np.prod(model(a, b), axis=0))
    assert abs(M.chsh(mc(M.stretched_instant)) - 2 * np.sqrt(2)) < 0.02
    assert abs(M.chsh(mc(M.stretched_local)) - 2.0) < 0.02
    S, p = M.swap_chsh()
    assert abs(S - 2 * np.sqrt(2)) < 1e-12 and abs(p - 0.25) < 1e-12
