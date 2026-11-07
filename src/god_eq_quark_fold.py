#!/usr/bin/env python3
"""
God-equation search, front 3: a quark as a folded, twisted area of spacetime.

THE FOLD EQUATION (STUR claim, built on KNOWN physics):
  A fold = a closed surface S threaded by flux Phi = oint_S B.dA ('the twist').
  A charge q bound to it stores field angular momentum (Thomson 1904, KNOWN):
        J = q Phi / (4 pi)            (Heaviside-Lorentz, hbar = c = 1)
  Single-valuedness (Dirac 1931, KNOWN):  q Phi = 2 pi n   =>   J = n / 2.
  STUR claim: a quark IS such a fold; its spin 1/2 is the n = 1 twist.

Tests (quark checklist):
  F1 CHECK   J = q Phi / 4 pi numerically, independent of separation.
  F2         which twist gives spin 1/2, for each possible kind of flux.
  F3         baryons: three folds must cancel their flux (no magnetic hadrons).
  F4         colour-magnetic folds: is the spin the same for all three colours?
  F5         fractional charge 1/3 vs spin 1/2: can ONE twist give both?
  F6         generations: do higher twists give heavier spin-1/2 copies?
  F7         mass: core size and fine-tuning vs compositeness bounds.
"""
import itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.integrate import dblquad

alpha = 1 / 137.035999
hbarc_MeV_fm = 197.3269804


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def thomson_J(d, q=1.0, g=1.0):
    def f(z, rho):
        r = np.array([rho, 0.0, z])
        a, b = r - np.array([0, 0, -d / 2]), r - np.array([0, 0, d / 2])
        E = q * a / (4 * np.pi * np.linalg.norm(a) ** 3)
        B = g * b / (4 * np.pi * np.linalg.norm(b) ** 3)
        return np.cross(r, np.cross(E, B))[2] * 2 * np.pi * rho
    return dblquad(f, 0, np.inf, -np.inf, np.inf, epsabs=1e-10, epsrel=1e-8)[0]


def triplet_weights():
    """Weights of the SU(3) fundamental in the Cartan basis (T3, T8), tr(T^a T^b) = delta/2."""
    return np.array([[0.5, 1 / (2 * np.sqrt(3))], [-0.5, 1 / (2 * np.sqrt(3))], [0.0, -1 / np.sqrt(3)]])


def main():
    banner("F1  CHECK: field angular momentum of a charge + flux fold")
    for d in [0.5, 1.0, 3.0]:
        J = thomson_J(d)
        print(f"   separation {d}:  J_numeric = {J:.12f}   q Phi / 4 pi = {1/(4*np.pi):.12f}")
    print("   -> J = q Phi/4pi exactly, independent of size: the twist, not the geometry, sets the spin.")

    banner("F2  Spin from each kind of twist (J = q Phi / 4 pi)")
    print("   (a) electromagnetic flux, Dirac-quantised q Phi = 2 pi n:  J = n/2")
    for n in [1, 2, 3]:
        print(f"       n = {n}:  J = {Fr(n, 2)}")
    print("   (b) colour-centre (Z3) flux, phase q Phi = 2 pi k / 3 seen by a quark:  J = k/6")
    for k in [1, 2]:
        print(f"       k = {k}:  J = {Fr(k, 6)}   (not a multiple of 1/2: forbidden for an isolated object)")
    print("   -> spin 1/2 needs a FULL Dirac twist (odd n), not a 1/3 twist.")

    banner("F3  Baryons: three spin-1/2 folds must carry odd n each and cancel (no magnetic proton)")
    found = [c for c in itertools.product(range(-7, 8, 2), repeat=3) if sum(c) == 0]
    print(f"   triples of odd n in [-7, 7] with total flux 0: {len(found)}  (sum of three odd numbers is odd)")
    print("   -> NO-GO: with electromagnetic flux, every baryon would be a magnetic monopole.")

    banner("F4  Colour-magnetic folds (Cartan / GNO): is spin colour-blind?")
    w = triplet_weights()
    print("   weights w_i . w_j:\n" + "\n".join("     " + "  ".join(f"{x:+.4f}" for x in row) for row in w @ w.T))
    # magnetic charge along colour-1 weight, minimal value making exp(i w_j . m) = 1 for all j
    lam = None
    for L in np.arange(1, 200) * np.pi / 3:
        m = L * w[0]
        if np.allclose(np.mod(w @ m / (2 * np.pi) + 1e-12, 1), 0, atol=1e-9):
            lam = L
            break
    m = lam * w[0]
    J = w @ m / (4 * np.pi)
    print(f"   minimal Dirac-consistent fold along colour 1: J seen by colours 1,2,3 = "
          + ", ".join(str(Fr(x).limit_denominator(12)) for x in J))
    print("   -> the 'spin' depends on the quark's colour: breaks exact SU(3) colour. NO-GO for the")
    print("      minimal colour fold. (Spin-from-isospin, Jackiw-Rebbi 1976, needs an adjoint Higgs")
    print("      that breaks the gauge group - QCD has none.)")

    banner("F5  One twist for both fractional charge and spin 1/2?")
    print("   Standard Model global structure (KNOWN): Q = (2/3) x triality (mod 1). Check:")
    for name, Q, t in [("u", Fr(2, 3), 1), ("d", Fr(-1, 3), 1), ("anti-u", Fr(-2, 3), 2), ("e", Fr(-1), 0),
                       ("nu", Fr(0), 0), ("gluon", Fr(0), 0), ("W", Fr(1), 0)]:
        print(f"     {name:7s} Q = {str(Q):5s} triality {t}:  Q - 2t/3 mod 1 = {(Q - Fr(2*t, 3)) % 1}")
    print("   The 1/3 comes from a Z3 (colour-centre) twist; F2 shows that twist gives J = 1/6, not 1/2.")
    print("   -> the twist that makes charge 1/3 cannot be the twist that makes spin 1/2.")

    banner("F6  Generations from higher twists?")
    for n in [1, 3, 5]:
        print(f"   n = {n}:  J = {Fr(n, 2)}")
    print("   -> higher twists raise the SPIN, not the mass at fixed spin: no c, s, t, b copies.")

    banner("F7  Mass: how small and how fine-tuned must the fold be?")
    gsq = np.pi / alpha                                   # g^2 for n = 1, q = e, HL units: g = 2 pi / e
    coef = gsq / (4 * np.pi) / 2                          # E_core = (g^2/4pi) / (2 r_c)
    print(f"   EM fold self-energy E = (g^2/4pi)/(2 r_c) = {coef:.2f} hbar c / r_c")
    for q, mq in [("u", 2.16), ("d", 4.70)]:                # PDG MS-bar masses at 2 GeV (LIT)
        print(f"   {q} quark ({mq} MeV): fold radius r_c = {coef*hbarc_MeV_fm/mq:.0f} fm "
              "(vs proton radius 0.84 fm)")
    Lam = 20e6                                            # MeV; ~20 TeV compositeness scale (APPROX LIT)
    print(f"   Compositeness (APPROX LIT: contact-interaction scale >~ 20 TeV): r_c <~ hbar c/Lambda,")
    print(f"   so E_core >~ {coef*Lam/1e6:.0f} TeV and the up mass needs cancellation to {2.16/(coef*Lam):.0e}")
    EP = 1.22089e22
    print(f"   Pure-spacetime fold (spinorial geon, Friedman-Sorkin 1980, KNOWN): core ~ l_P, E ~ E_P;")
    print(f"   up-quark mass / E_P = {2.16/EP:.1e}")


if __name__ == "__main__":
    main()
