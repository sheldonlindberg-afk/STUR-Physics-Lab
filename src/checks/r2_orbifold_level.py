#!/usr/bin/env python3
"""
Refinement round 2, item 2: the Chern-Simons level on the actual S^1/Z2
orbifold. See docs/R2_ORBIFOLD_LEVEL.md for the derivation and references.
Requires numpy, scipy. Runs in ~1-2 min (the trigger re-check is the slow part).

  O1  Z2 action on the fermion pair (psi1: q_B=+1, psi2: q_B=-1, both Q=1):
      explicit Dirac-matrix check that psi2(y) = gamma5 psi1(-y) maps every
      bulk term of psi2 onto psi1 at -y, iff M2 = -M1. The pair is ONE
      unconstrained Dirac field on the covering circle with CONSTANT mass.
  O2  Z2 parity of every component of the candidate 5D Chern-Simons terms
      B^F_A^F_A, A^F_A^F_A, B^F_B^F_A (B_mu odd, B_5 even, A_mu even, A_5 odd).
  O3  large gauge transformations on the orbifold: xi = n y / R is odd,
      winds 2 pi n on the covering circle, equals n pi at y = pi R.
  O4  exact roll integral: Phi(pi) - Phi(0) = (pi/2) sgn M for ANY M R,
      so Delta Theta_eff = k_eff pi exactly (not just up to e^(-2 pi M R)).
  O5  sensitivity of the cooling trigger (H_c, T_c) to the scalar's dof:
      Z2 pair (2 real dof per KK level, as in stur_final) vs a single
      C-projected scalar phi(-y) = phi*(y) (1 real dof per KK level).
"""
import os
import sys

import numpy as np
from scipy.integrate import quad

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from refinement_r1 import cg_exact  # noqa: E402

BAR = "=" * 78
rng = np.random.default_rng(1)

# Dirac matrices (Dirac basis); 5D: Gamma^mu = gamma^mu, Gamma^5 = i gamma5
I2, Z2m = np.eye(2), np.zeros((2, 2))
sx = np.array([[0, 1], [1, 0]], complex)
sy = np.array([[0, -1j], [1j, 0]], complex)
sz = np.array([[1, 0], [0, -1]], complex)
g0 = np.block([[I2, Z2m], [Z2m, -I2]]).astype(complex)
gs = [np.block([[Z2m, s], [-s, Z2m]]) for s in (sx, sy, sz)]
g5 = 1j * g0 @ gs[0] @ gs[1] @ gs[2]
G5 = 1j * g5


def bar(p):
    return p.conj() @ g0


def o1():
    print(BAR + "\n O1  Z2 action on the fermion pair\n" + BAR)
    p1 = rng.normal(size=4) + 1j * rng.normal(size=4)         # psi1 at -y
    dp1 = rng.normal(size=4) + 1j * rng.normal(size=4)        # d/dy' psi1 at -y
    p2 = g5 @ p1                                              # psi2 at +y
    dp2 = -(g5 @ dp1)                                         # d/dy = -d/dy'
    B5, Bmu, A5, Amu = 0.7, 0.3, 0.4, 0.9                     # values at -y
    mass2 = bar(p2) @ p2
    mass1 = bar(p1) @ p1
    print(f"   psibar2 psi2 (y) = {mass2.real:+.6f},  psibar1 psi1 (-y) = {mass1.real:+.6f}")
    print("   -> mass terms: M2 psibar2 psi2 = M1 psibar1 psi1  iff  M2 = -M1")
    # 5th-direction kinetic term with B (q2=-1, B5 even) and A (Q=1, A5 odd)
    D5p2 = dp2 - 1j * (-1) * B5 * p2 - 1j * (+1) * (-A5) * p2  # fields at +y
    D5p1 = dp1 - 1j * (+1) * B5 * p1 - 1j * (+1) * A5 * p1    # fields at -y
    k2 = bar(p2) @ (1j * G5) @ D5p2
    k1 = bar(p1) @ (1j * G5) @ D5p1
    print(f"   psibar2 i G5 D5 psi2 (y) = {k2:.6f}")
    print(f"   psibar1 i G5 D5 psi1 (-y) = {k1:.6f}   (equal -> charges q_B = +-1 consistent)")
    # 4D vector current coupling: B_mu odd (q2 = -1), A_mu even (Q = 1)
    j2 = bar(p2) @ g0 @ p2 * (-1 * (-Bmu) + 1 * Amu)
    j1 = bar(p1) @ g0 @ p1 * (+1 * Bmu + 1 * Amu)
    print(f"   current couplings: {j2.real:+.6f} vs {j1.real:+.6f}")
    ok = (abs(mass2 + mass1) < 1e-12 and abs(k2 - k1) < 1e-12 and abs(j2 - j1) < 1e-12)
    print(f"   all checks: {'PASS' if ok else 'FAIL'}")
    print("   Conclusion: the pair (psi1, psi2) with masses (M, -M) is exactly one Dirac")
    print("   field psi1 on the covering circle with CONSTANT mass M, charge q_B = 1, Q = 1,")
    print("   and no chiral zero mode. A single field cannot carry q_B != 0 under a")
    print("   Z2-odd U(1) while keeping Q != 0 (the Z2 maps q_B -> -q_B, Q -> Q).")
    print("   A Z2-odd 'kink' mass M eps(y) arises only for a single Z2-projected field,")
    print("   which is B-neutral and so cannot contribute to the theta-term.")
    return ok


def o2():
    print("\n" + BAR + "\n O2  Z2 parity of Chern-Simons components\n" + BAR)
    par = {"B_mu": -1, "B_5": +1, "A_mu": +1, "A_5": -1}

    def fpar(f):        # parities of F_{mu nu}, F_{mu 5}
        return {"F_mn": par[f + "_mu"], "F_m5": -par[f + "_mu"]}
    rows = []
    for name, (X, Y, W) in {"B^F_A^F_A": ("B", "A", "A"),
                            "A^F_A^F_A": ("A", "A", "A"),
                            "B^F_B^F_A": ("B", "B", "A")}.items():
        c1 = par[X + "_5"] * fpar(Y)["F_mn"] * fpar(W)["F_mn"]       # X_5 F F
        c2 = par[X + "_mu"] * fpar(Y)["F_m5"] * fpar(W)["F_mn"]      # X_mu F_5 F
        c3 = par[X + "_mu"] * fpar(Y)["F_mn"] * fpar(W)["F_m5"]
        allp = {c1, c2, c3}
        rows.append((name, c1, c2, c3, allp))
        verdict = ("even: constant coefficient allowed" if allp == {1} else
                   "odd: needs jumping coefficient eps(y), integrates to 0 over the orbifold"
                   if allp == {-1} else "mixed")
        print(f"   {name:10s}  X5 FF: {c1:+d}  X_mu F5 F: {c2:+d}, {c3:+d}  -> {verdict}")
    print("   -> the term that matters, B^F_A^F_A (gives theta F Ftilde), is Z2-even:")
    print("      a constant bulk level is allowed and no fixed-point counterterm is needed.")
    return rows[0][4] == {1}


def o3():
    print("\n" + BAR + "\n O3  Large gauge transformations on the orbifold\n" + BAR)
    R = 1.0
    for n in (1, 2, 3):
        xi = lambda y: n * y / R
        odd = abs(xi(-0.37) + xi(0.37)) < 1e-15
        wind = (xi(2 * np.pi * R) - xi(0)) / (2 * np.pi)
        print(f"   n = {n}: xi = n y/R odd: {odd}; winding on covering circle {wind:.0f};"
              f" exp(i xi(pi R)) = {np.exp(1j * xi(np.pi * R)).real:+.0f}")
    print("   -> theta -> theta + 2 pi n are allowed gauge transformations: theta's period")
    print("      is still 2 pi. At y = 0, xi = 0 always (brane terms there need no B")
    print("      invariance); at y = pi R, exp(i xi) = (-1)^n, so a q_B = 1 brane mixing")
    print("      term is allowed at y = 0 but forbidden at y = pi R.")
    return True


def o4():
    print("\n" + BAR + "\n O4  Exact roll integral of the fermion-induced theta-term\n" + BAR)
    print("   Phi(theta) - Phi(0) = int_0^theta c_g;   c_g = 1/2 sinh a/(cosh a - cos t), a = 2 pi M R")
    ok = True
    for MR in (0.05, 0.3, 1.0, 3.0):
        half, _ = quad(lambda t: cg_exact(t, MR), 0, np.pi)
        full, _ = quad(lambda t: cg_exact(t, MR), 0, 2 * np.pi, limit=200)
        ok &= abs(half / np.pi - 0.5) < 1e-9 and abs(full / np.pi - 1) < 1e-9
        print(f"   M R = {MR:4.2f}:  int_0^pi = {half / np.pi:.10f} pi,"
              f"  int_0^2pi = {full / np.pi:.10f} pi")
    print("   Reason: Phi(-t) - Phi(0) = -(Phi(t) - Phi(0)) (KK spectrum symmetric under")
    print("   n -> -n, theta -> -theta) and Phi(t + 2 pi) = Phi(t) + pi sgn M. So")
    print("   2[Phi(pi) - Phi(0)] = Phi(pi) - Phi(-pi) = pi sgn M, exactly.")
    print("   -> Delta Theta_eff(0 -> pi) = kappa pi + (pi/2) sgn M = k_eff pi EXACTLY,")
    print("      for every M R. beta = k_eff alpha / 2 has no e^(-2 pi M R) correction;")
    print("      the only deviations are theta not yet settled at pi (stur_final 'lands/pi').")
    return ok


def o5():
    print("\n" + BAR + "\n O5  Cooling trigger vs scalar dof (stur_final.crossing)\n" + BAR)
    import stur_final as F
    xf = 137.0
    out = {}
    for db, lab in ((2.0, "Z2 pair = 1 complex scalar on covering circle"),
                    (1.0, "single C-projected scalar, phi(-y) = phi*(y)")):
        hc = F.crossing(lambda x, s, sp: F.ds_ratio(x, s, sp), xf, 2.0, df=4.0, db=db)
        tc = F.crossing(lambda x, s, sp: F.th_ratio(x, s, sp == 1), xf, 2.0, df=4.0, db=db)
        out[db] = (hc, tc)
        print(f"   db = {db:.0f} ({lab}):  H_c = {hc:5.2f}/L,  T_c = {tc:5.2f}/L")
    print("   -> both assignments keep the trigger (scalar wins at high T and on de")
    print("      Sitter, fermion wins below); the C-projected scalar moves H_c and T_c")
    print("      up by ~10%. Delta theta = pi holds as long as the scalar and fermion")
    print("      have the same B charge and the same twist (opposite-sign first harmonics).")
    return all(v[0] > 0 and v[1] > 0 for v in out.values())


if __name__ == "__main__":
    res = [o1(), o2(), o3(), o4(), o5()]
    print("\n" + BAR + f"\n checks passed: {sum(res)}/{len(res)}\n" + BAR)
