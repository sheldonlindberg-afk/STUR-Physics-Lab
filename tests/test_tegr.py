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


def test_tip_regular_frame_diverges_at_infinity():
    tau, r, th, ph, M, k = sp.symbols("tau r theta phi M k", positive=True)
    f = 1 - 2 * M / r
    E = sp.diag(sp.sqrt(f), 1 / sp.sqrt(f), r, r * sp.sin(th))
    n = 4
    w = [[[0] * n for _ in range(n)] for _ in range(n)]
    w[2][1][2], w[1][2][2] = 1, -1
    w[3][1][3], w[1][3][3] = sp.sin(th), -sp.sin(th)
    w[3][2][3], w[2][3][3] = sp.cos(th), -sp.cos(th)
    w[0][1][0], w[1][0][0] = k, -k
    Ts, B, g, ginv, e = T.torsion_parts(E, [tau, r, th, ph], sp.eye(4), w, simp=True)
    tail = sp.limit(sp.simplify(e * Ts / sp.sin(th)).diff(k), r, sp.oo)
    assert sp.simplify(tail + 4 * M) == 0     # constant integrand -> divergent radial integral


def test_field_bookkeeping_and_gravitons():
    fld, mat, tot = T.two_mass_bookkeeping(1.0, 1.0, 1.0)
    assert abs(mat + 2 * fld) < 1e-25 and abs(tot - T.G_SI) < 1e-20
    E, N = T.graviton_count(1.5e-14, 721e-6, 1.58, 0.08)
    assert abs(E / 5.78e-93 - 1) < 0.01 and N < 1e-58
