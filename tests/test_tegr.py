"""Pins src/stur_tegr.py: TEGR identity, Newtonian limit, Schwarzschild flux, gravitons."""
import os, sys
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_tegr as T


def test_identity_T_equals_minus_R_plus_B():
    for d, t, r in T.identity_check(points=1):
        assert abs(d) < 1e-20 and abs(t) > 1e-3 and abs(r) > 1e-3


def test_newtonian_limit():
    a, b, c = T.grad_form(*T.newtonian_lagrangian())
    assert (a, b, c) == (0, 4, -2)
    assert a + b + c == 2          # Psi = Phi: (e T)_2 = 2 (grad Phi)^2 -> Newton, G coefficient 1


def test_schwarzschild_flux():
    Tref, flux, I_inf, I_tip, M = T.schwarzschild_tegr_action()
    assert Tref == 0
    assert sp.simplify(I_inf - 4 * sp.pi * M**2) == 0
    assert sp.simplify(I_tip - 4 * sp.pi * M**2) == 0
    assert sp.simplify(8 * sp.pi * M**2 - I_inf - sp.Rational(1, 4) * 16 * sp.pi * M**2) == 0


# The tip-regular frame check moved to tests/test_tegr_corner.py: the connection used here
# before (static reference + k d tau) was not flat. See stur_tegr_corner K5.


def test_field_bookkeeping_and_gravitons():
    fld, mat, tot = T.two_mass_bookkeeping(1.0, 1.0, 1.0)
    assert abs(mat + 2 * fld) < 1e-25 and abs(tot - T.G_SI) < 1e-20
    import stur_gravity_full as GF
    A = GF.design_a()
    E, N = T.graviton_count(A["m"], A["dx"], A["ramp"], A["hold"])
    assert abs(E / 5.5e-93 - 1) < 0.01 and abs(N / 1.3e-59 - 1) < 0.05


def test_reissner_nordstrom_and_horizon_term():
    rn = T.reissner_nordstrom_tegr()
    assert rn["flux_inf"] == 0                                         # Q^2 terms fall off
    assert sp.simplify(rn["I_inf"] - rn["beta_M_half"]) == 0           # beta M / 2, no subtraction
    assert sp.simplify(rn["S"] - rn["area_quarter"]) == 0              # S = A/4 = pi r+^2
    assert sp.simplify(rn["I_tip"] - rn["area_quarter"]) == 0          # horizon term = A/4
    fp, r = sp.Symbol("fp"), sp.Symbol("r", positive=True)
    assert sp.simplify(rn["tip_general"] + fp * r**2 / 2) == 0         # any f with f(r+) = 0
