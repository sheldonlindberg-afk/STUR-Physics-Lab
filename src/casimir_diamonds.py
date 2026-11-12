#!/usr/bin/env python3
"""
The electromagnetic rung of the ladder (SYMMETRY_LADDER.md): why electromagnetism is the
background in the diamond experiment, and its strength, derived.

U(1)_em is never broken, so the photon stays massless and electromagnetism is long-range.
Between two neutral, unpolarized diamonds what remains is the Casimir-Polder force, from
correlated zero-point fluctuations of the field and the induced dipoles. It is derived here
from classical electrostatics, the dipole field and one quantum step (the fluctuation sum
over imaginary frequencies, Casimir and Polder 1948).

  P1  Polarizability of a dielectric sphere (radius R, permittivity eps) in a uniform field,
      from Laplace's equation with the boundary conditions at r = R:
      alpha / (4 pi eps0) = K R^3, K = (eps - 1)/(eps + 2). (CHECK, symbolic)
  P2  The dipole field Green tensor at imaginary frequency xi (u = xi r / c):
      G_ij = e^{-u} / r^3 [(1 + u + u^2) delta_ij - (3 + 3u + u^2) rhat_i rhat_j],
      checked to satisfy the Helmholtz equation (nabla^2 - xi^2/c^2) away from the source;
      Tr G.G = 2 e^{-2u} (3 + 6u + 5u^2 + 2u^3 + u^4) / r^6. (CHECK, symbolic)
  P3  The interaction of two polarizable particles, U = -(hbar / 2 pi) int_0^oo dxi
      alpha1 alpha2 Tr G.G (Gaussian units for alpha = K R^3). For constant alpha (the
      retarded regime, r much larger than the wavelengths where alpha varies):
      int_0^oo e^{-2u}(3 + 6u + 5u^2 + 2u^3 + u^4) du = 23/4, so
      U = -(23 hbar c / 4 pi) alpha1 alpha2 / r^7. (CHECK, exact)
  P4  This is the formula used in src/stur_gravity_entanglement.py (then quoted as KNOWN), and
      at the design gap Casimir's entangling phase against gravity's: the gap that src/
      stur_gravity_full.py chose, 181 um, is where Casimir is 10% of gravity. (CHECK)
Labels: CHECK, LIT (eps of diamond, 5.7).
"""
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def sphere_polarizability():
    """P1: potential inside A r cos(th), outside -E0 r cos(th) + B cos(th)/r^2; continuity of
    the potential and of eps * d(phi)/dr at r = R. Dipole moment p = 4 pi eps0 B."""
    A, B = sp.symbols("A B", real=True)
    R, E0, eps = sp.symbols("R E0 epsilon", positive=True)
    r = sp.Symbol("r", positive=True)
    phin = A * r
    phout = -E0 * r + B / r**2
    sol = sp.solve([sp.Eq(phin.subs(r, R), phout.subs(r, R)),
                    sp.Eq(eps * sp.diff(phin, r).subs(r, R), sp.diff(phout, r).subs(r, R))], [A, B])
    alpha_over_4pieps0 = sp.simplify(sol[B] / E0)
    return alpha_over_4pieps0, sp.simplify(alpha_over_4pieps0 - (eps - 1) / (eps + 2) * R**3)


def green_tensor():
    """P2: the Green tensor, the Helmholtz check and Tr G.G."""
    x, y, z, k = sp.symbols("x y z k", positive=True)                  # k = xi / c
    X = [x, y, z]
    r = sp.sqrt(x**2 + y**2 + z**2)
    u = k * r
    G = sp.Matrix(3, 3, lambda i, j: sp.exp(-u) / r**3 * ((1 + u + u**2) * (1 if i == j else 0)
                                                          - (3 + 3 * u + u**2) * X[i] * X[j] / r**2))
    # Helmholtz: each component of the field of a fixed dipole p_j solves (lap - k^2) E = 0 off the source
    lapm = lambda f: sum(sp.diff(f, v, 2) for v in X) - k**2 * f
    pt = {x: sp.Rational(3, 7), y: sp.Rational(-2, 5), z: sp.Rational(5, 11), k: sp.Rational(4, 3)}
    helm = max(abs(sp.N(lapm(G[i, j]).subs(pt), 30)) for i in range(3) for j in range(3))
    # divergence-free (transverse) off the source, like a radiation field
    div = max(abs(sp.N(sum(sp.diff(G[i, j], X[i]) for i in range(3)).subs(pt), 30)) for j in range(3))
    tr = sp.simplify((G * G).trace())
    uu, rr = sp.symbols("u r", positive=True)
    target = 2 * sp.exp(-2 * uu) * (3 + 6 * uu + 5 * uu**2 + 2 * uu**3 + uu**4) / rr**6
    trcheck = sp.simplify(tr.subs({x: rr, y: 0, z: 0}).subs(k, uu / rr) - target)
    return helm, div, trcheck


def frequency_integral():
    """P3: the integral, exactly."""
    u = sp.Symbol("u", positive=True)
    return sp.integrate(sp.exp(-2 * u) * (3 + 6 * u + 5 * u**2 + 2 * u**3 + u**4), (u, 0, sp.oo))


def casimir_coefficient():
    """U = -(hbar/2pi) int dxi a1 a2 Tr G.G = -(hbar/2pi)(c/r) a1 a2 (2/r^6) * I, I = 23/4."""
    I = frequency_integral()
    return sp.Rational(1, 2) / sp.pi * 2 * I                            # U = -coef hbar c a1 a2 / r^7


def compare_with_experiment_code():
    import stur_gravity_entanglement as GE
    import numpy as np
    m, r = 1.5e-14, 200e-6
    R = GE.radius(m)
    K = (GE.EPS_DIAMOND - 1) / (GE.EPS_DIAMOND + 2)
    coef = float(casimir_coefficient())
    mine = -coef * GE.HBAR * GE.C * (K * R**3) ** 2 / r**7
    theirs = GE.casimir_energy(m, r)
    grav = -GE.G * m * m / r
    return mine, theirs, grav, R


def main():
    banner("P1  Polarizability of a dielectric sphere, from electrostatics (CHECK)")
    a, resid = sphere_polarizability()
    print(f"   alpha / (4 pi eps0) = {a};  minus K R^3 with K = (eps-1)/(eps+2): {resid}")

    banner("P2  The dipole Green tensor at imaginary frequency (CHECK)")
    helm, div, trc = green_tensor()
    print(f"   (nabla^2 - xi^2/c^2) G = 0 off the source: max residual {helm:.1e}")
    print(f"   div G = 0 off the source: max residual {div:.1e}")
    print(f"   Tr G.G - 2 e^(-2u)(3 + 6u + 5u^2 + 2u^3 + u^4)/r^6 = {trc}")

    banner("P3  The Casimir-Polder coefficient (CHECK, exact)")
    I = frequency_integral()
    print(f"   int_0^oo e^(-2u)(3 + 6u + 5u^2 + 2u^3 + u^4) du = {I}")
    print(f"   U = -({casimir_coefficient()}) hbar c alpha1 alpha2 / r^7 = -(23/(4 pi)) hbar c alpha1 alpha2 / r^7")

    banner("P4  In the diamond experiment")
    mine, theirs, grav, R = compare_with_experiment_code()
    print(f"   m = 1.5e-14 kg (R = {R * 1e6:.2f} um), r = 200 um: derived U = {mine:.4e} J,"
          f" src/stur_gravity_entanglement.py {theirs:.4e} J (ratio {mine / theirs:.12f})")
    print(f"   Gravity at the same r: {grav:.4e} J; Casimir/gravity = {mine / grav:.3e}")
    print("   Casimir ~ R^6/r^7 and gravity ~ R^6/r, so the safe gap does not depend on the mass:")
    print("   181 um is where Casimir's entangling phase is 10% of gravity's (src/stur_gravity_full.py, H0).")


if __name__ == "__main__":
    main()
