"""Pins src/stur_tegr_gr.py: GR's results derived from TEGR."""
import os, sys
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_tegr_gr as F
import stur_gravity_entanglement as ge


def test_birkhoff_from_tegr():
    L, eA, eB, Ap, ode, sols = F.solve_spherical()
    r = sp.symbols("r", positive=True)
    C1 = sp.Symbol("C1")
    assert any(sp.simplify(s.rhs**2 - (1 + C1 / r)) == 0 for s in sols)
    # Schwarzschild satisfies both TEGR equations
    M = sp.symbols("M", positive=True)
    A, B = sp.Function("A")(r), sp.Function("B")(r)
    sub = {A: sp.log(1 - 2 * M / r) / 2, B: -sp.log(1 - 2 * M / r) / 2}
    assert sp.simplify(eA.subs(sub).doit()) == 0 and sp.simplify(eB.subs(sub).doit()) == 0


def test_classic_tests():
    dp = F.perihelion_shift(F.GM_SUN, F.MERCURY_A, F.MERCURY_E)
    assert abs(dp * (36525 / F.MERCURY_P) * 180 / np.pi * 3600 - 42.98) < 0.01
    assert abs(F.light_deflection(F.GM_SUN, F.R_SUN) * 180 / np.pi * 3600 - 1.7512) < 2e-4
    assert F.ppn_gamma() == 1
    gps, grav = F.gps_offset_us_per_day()
    assert abs(gps - 38.54) < 0.02 and abs(grav - 45.65) < 0.02


def test_field_energy_shell_theorem():
    import stur_gravity_full as GF
    A = GF.design_a()
    m, R = A["m"], A["R"]
    for d in (A["gap"], 3e-6):
        fld, mat, tot = F.interaction_energy_tegr(m, R, d)
        assert abs(fld / (F.G * m * m / d) - 1) < 1e-7
        assert abs(tot / (-F.G * m * m / d) - 1) < 1e-7
