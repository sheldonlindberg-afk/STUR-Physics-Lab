#!/usr/bin/env python3
"""
Refinement round 5: derive the Lagrangian for the "twist" (see docs/REFINEMENT_R5.md).
Requires numpy. Runs in a few seconds.

  L1. Z2 parities of 5D torsion components on S^1/Z2 (from the geometry):
      the only component that can twist fermions along y (the trace T_y,
      via a non-minimal coupling c T_A psibar Gamma^A psi) is Z2-ODD, so its
      holonomy over the covering circle vanishes identically.
  L2. Positivity: for the orbifold (two equal half-circles), any Z2-even,
      reflection-positive brane term gives a positive transfer-matrix trace,
      so the untwisted birth point stays the minimum. Checked on random terms.
  L3. A Z2-ODD brane coupling to the y-current, Sigma(x) psibar Gamma^y psi,
      acts as a localized twist delta = y_S <Sigma>; the hilltop of theta moves
      to -delta + pi (fermion term), i.e. to theta = 0 when delta = pi.
"""
import itertools

import numpy as np

BAR = "=" * 78
rng = np.random.default_rng(7)
SX = np.array([[0, 1], [1, 0]], float)
SZ = np.array([[1, 0], [0, -1]], float)


def expm_sym(a, b):
    """exp(a sz + b sx) for real a, b (symmetric generator: a 'boost')"""
    r = np.hypot(a, b)
    if r == 0:
        return np.eye(2)
    return np.cosh(r) * np.eye(2) + np.sinh(r) / r * (a * SZ + b * SX)


def l1():
    print(BAR + "\n L1. Torsion on S^1/Z2: which components survive?\n" + BAR)
    print("   Orbifold y -> -y acts on every index equal to y (coordinate or frame)")
    print("   with a sign; a component is Z2-even iff it has an even number of y's.")
    comps = {
        "T_[mu nu rho]  (4D axial torsion)": "mu nu rho",
        "T_[mu nu y]    (axial, one y)": "mu nu y",
        "T_y = T^B_{yB} (trace, y-component)": "y",
        "T_mu = T^B_{muB} (trace, 4D)": "mu",
    }
    for name, idx in comps.items():
        ny = idx.split().count("y")
        print(f"   {name:40s} #y = {ny}  ->  {'even' if ny % 2 == 0 else 'ODD'}")
    print("   Fermion couplings in 5D:")
    print("   * minimal (Cartan): (1/8) T_[ABC] psibar Gamma^ABC psi  -> spin couplings")
    print("     T_[mu nu rho]: 4D axial-vector coupling (no y-momentum shift);")
    print("     T_[mu nu y]: dipole coupling psibar sigma_{mu nu} psi (no shift).")
    print("   * non-minimal: c T_A psibar Gamma^A psi -> c T_y J^y shifts y-momentum")
    print("     (a twist), but T_y is Z2-odd: phase +a on (0, pi R), -a on (pi R, 2 pi R).")
    y = np.linspace(0, 2 * np.pi, 200001)
    Ty = np.sign(np.sin(y)) * (1 + 0.3 * np.cos(y) ** 2)        # any odd profile
    hol = np.trapezoid(Ty, y)
    print(f"   numerical holonomy of an odd profile over the covering circle: {hol:.1e}")
    print("   -> NO torsion twist chi exists in 5D PGT on S^1/Z2 (round 4's chi is")
    print("      not realised); a continuous frame-rotation twist commuting with 4D")
    print("      Lorentz symmetry does not exist in 5D either.")


def l2():
    print("\n" + BAR + "\n L2. Positivity with brane terms (orbifold = two equal half-circles)\n"
          + BAR)
    print("   Euclidean transfer matrix around the covering circle, fixed 4D momentum p:")
    print("   T = e^{G L/2} J_pi e^{G L/2} J_0,  G = M sz + p sx (bulk),")
    print("   J = exp(a sz + b sx): brane mass / kinetic / mixing terms (Z2-even, real).")
    print("   theta-dependence: ln|Tr T - 2 s cos theta|; s = -1 at a smooth birth.")
    neg_orb, neg_gen = 0, 0
    for _ in range(20000):
        M, p, L = rng.uniform(0, 5), rng.uniform(0, 5), rng.uniform(0.1, 3)
        a0, b0, a1, b1 = rng.normal(0, 3, 4)
        Pg = expm_sym(M * L / 2, p * L / 2)
        T = Pg @ expm_sym(a1, b1) @ Pg @ expm_sym(a0, b0)
        neg_orb += np.trace(T) < 0
        u = rng.uniform(0.05, 0.95)                       # unequal segments
        T2 = (expm_sym(M * L * u, p * L * u) @ expm_sym(a1, b1)
              @ expm_sym(M * L * (1 - u), p * L * (1 - u)) @ expm_sym(a0, b0))
        neg_gen += np.trace(T2) < 0
    print(f"   20000 random brane terms, orbifold (equal halves): Tr T < 0 in {neg_orb} cases")
    print(f"   same, unequal segments (not an orbifold):          Tr T < 0 in {neg_gen} cases")
    print("   -> on the orbifold Tr T = Tr(Q e^{J0}) with Q = P^1/2 e^{J_pi} P^1/2 > 0,")
    print("      so Tr T > 0 always: Z2-even brane terms can never turn the birth point")
    print("      into a hilltop. (This is the transfer-matrix form of the positivity")
    print("      theorem in REFINEMENT_R5.md.)")


def vtheta(theta, delta, s, M=2.0, L=1.0):
    """fermion one-loop theta potential with a brane twist delta (per dof, up to +const)"""
    p = np.linspace(1e-3, 40, 4000)
    E = np.sqrt(M ** 2 + p ** 2)
    trT = 2 * np.cosh(E * L)
    w = p ** 3 * np.gradient(p)
    return np.array([-np.sum(w * np.log(np.abs(trT - 2 * s * np.cos(t + delta))))
                     for t in theta])


def l3():
    print("\n" + BAR + "\n L3. Z2-odd brane coupling  y_S Sigma(x) delta(y) psibar Gamma^y psi\n"
          + BAR)
    print("   Z2 parity: Gamma^y-current odd x Sigma odd = even  -> allowed; needs a")
    print("   brane field that is odd under the orbifold parity. <Sigma> != 0 breaks the")
    print("   orbifold parity on the brane: the orbifold 'twists'. Its jump is a pure")
    print("   phase e^{-i delta}, delta = y_S <Sigma>: a localized twist for psi only.")
    th = np.linspace(-np.pi, np.pi, 721)
    print(f"   {'delta':>7s}  {'argmax V(theta)':>16s}  {'theta=0 is':>11s}")
    for d in (0.0, np.pi / 2, 0.9 * np.pi, np.pi):
        v = vtheta(th, d, s=-1)
        amax = th[v.argmax()]
        kind = "maximum" if abs(amax) < 0.01 else ("minimum" if abs(th[v.argmin()]) < 0.01
                                                   else "slope")
        print(f"   {d:7.3f}  {amax:16.3f}  {kind:>11s}")
    print("   -> the hilltop sits at theta = pi - delta: exactly at the birth point")
    print("      only for delta = pi. A 3 % accuracy on beta needs |delta - pi| < 0.094.")


if __name__ == "__main__":
    l1()
    l2()
    l3()
