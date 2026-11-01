"""Pins the key numbers of src/stur_open_problems.py."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_open_problems as O


def test_u1_wilson_loop_is_perimeter_law():
    Ls = np.array([10, 20, 40.0])
    W = np.array([O.wilson_u1_square(L, 1.0, 4 * np.pi / 137.036) for L in Ls])
    # per-unit-perimeter roughly constant, per-unit-area falls ~1/L
    assert W[2] / W[1] < 2.3 and (W[2] / Ls[2]**2) / (W[1] / Ls[1]**2) < 0.6


def test_immirzi_values():
    abck, me, gm = O.immirzi()
    assert abs(abck - 0.127384) < 1e-6 and abs(me - 0.237533) < 1e-6 and abs(gm - 0.274067) < 1e-6


def test_alpha_s_at_planck():
    assert abs(O.alpha_s_run(91.1876) - 0.1180) < 1e-9
    assert abs(O.alpha_s_run(O.EP_GeV) - 0.01886) < 2e-4


def test_skyrmion_reproduces_anw():
    E, Lt = O.skyrme_profile()
    assert abs(E / (12 * np.pi**2) - 1.23145) < 2e-5
    assert abs(Lt - 50.98) < 0.05


def test_bounce_in_phi_units():
    rc = np.sqrt(3) / (32 * np.pi**2 * 0.2375329579659206**3)
    assert abs(0.75 / rc - 1.8328) < 1e-3


def test_page_time():
    r = 1.4847
    assert abs(1 - (r / (1 + r)) ** 1.5 - 0.5381) < 2e-4
