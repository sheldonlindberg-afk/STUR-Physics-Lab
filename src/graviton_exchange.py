#!/usr/bin/env python3
"""
The gravity rung of the ladder (SYMMETRY_LADDER.md): from linearized GR to the entangling
phase of the two-diamond experiment.

Gravity does not come out of the gauge chain (3-3-1 -> Standard Model -> electromagnetism);
it sits beside it, with Newton's G as its own input. Its low-energy quantum description is
general relativity as an effective field theory (the graviton), which is what the diamond
test probes. TEGR gives the same results (TEGR.md, E1-E2).

  N1  Linearized GR, g = eta + h, de Donder gauge: box hbar_munu = -16 pi G T_munu. For a
      static point mass, hbar_00 = 4GM/r; then h_00 = 2GM/r and h_ij = 2GM/r delta_ij, so
      g_00 = -(1 - 2GM/r) (Newton's potential -GM/r) and g_ij = (1 + 2GM/r) delta_ij
      (PPN gamma = 1). (CHECK, symbolic)
  N2  One-graviton exchange between two sources: h(q) = (16 pi G / q^2) P.T1 with
      P_munurhosigma = (eta_murho eta_nusigma + eta_musigma eta_nurho - eta_munu eta_rhosigma)/2,
      and U(q) = -(1/2) T2.h = -(8 pi G / q^2) T2.P.T1. Static masses: T2.P.T1 = m1 m2 / 2, so
      U(q) = -4 pi G m1 m2 / q^2 and, by the Fourier transform (chiral_breaking S4 at m = 0),
      U(r) = -G m1 m2 / r. (CHECK)
  N3  The same contraction with a photon's (traceless) stress tensor is twice as large: the
      origin of the factor 2 in light bending, 4GM/(c^2 b) against the Newtonian 2GM/(c^2 b).
      (CHECK)
  N4  If the field of each diamond follows each branch, every branch pair (i, j) acquires
      phi_ij = -(1/hbar) int U(r_ij(t)) dt. The entangling phase
      Delta phi = phi_LL + phi_RR - phi_LR - phi_RL for design A (1.47e-14 kg, dx = 721 um,
      gap 181 um, ramps 2 x 1.58 s and hold 0.08 s, parallel), from N2's potential along
      the trajectories: 2.19 rad, against src/stur_gravity_full.trajectory_dphi. (CHECK)
  N5  What a positive result would and would not establish (FOLLOWS; see SYMMETRY_LADDER.md).
Labels: CHECK, FOLLOWS, LIT (G).
"""
import os
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ETA = sp.diag(-1, 1, 1, 1)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def linearized_point_mass():
    """N1: solve nabla^2 hbar_00 = -16 pi G M delta^3 (static box -> nabla^2) by Gauss's law,
    then h = hbar - (1/2) eta hbar_trace."""
    G, M, r = sp.symbols("G M r", positive=True)
    hb00 = sp.Function("f")(r)
    # radial Laplacian of f(r) with the source: flux through a sphere = -16 pi G M
    sol = sp.dsolve(sp.Eq(sp.diff(r**2 * sp.diff(hb00, r), r), 0), hb00)
    C1, C2 = sp.symbols("C1 C2")
    f = sol.rhs.subs({C1: 0}) if sol.rhs.has(C1) else sol.rhs     # vanish at infinity
    f = f.subs({sp.Symbol("C1"): 0})
    # fix the 1/r coefficient by Gauss: 4 pi r^2 f'(r) = -16 pi G M
    coeff = [s for s in f.free_symbols if s.name.startswith("C")]
    c = coeff[0] if coeff else None
    csol = sp.solve(sp.Eq(4 * sp.pi * r**2 * sp.diff(f, r), -16 * sp.pi * G * M), c)[0]
    hbar00 = sp.simplify(f.subs(c, csol))
    hbar = sp.zeros(4, 4)
    hbar[0, 0] = hbar00
    trace = sum(ETA[i, i] * hbar[i, i] for i in range(4))                 # eta^munu hbar_munu (eta diagonal, self-inverse)
    h = sp.simplify(hbar - ETA * trace / 2)
    g = ETA + h
    Phi = sp.simplify(-(g[0, 0] + 1) / 2)                                 # g_00 = -(1 + 2 Phi)
    gamma = sp.simplify(h[1, 1] / h[0, 0])
    return hbar00, h, Phi, gamma


def contraction(T1, T2):
    """T2.P.T1 with P = (eta eta + eta eta - eta eta)/2, indices lowered with eta."""
    low = lambda T: ETA * T * ETA
    tr = lambda T: sum(ETA[i, i] * T[i, i] for i in range(4))
    full = sum(low(T1)[a, b] * T2[a, b] for a in range(4) for b in range(4))
    return sp.simplify((2 * full - tr(T1) * tr(T2)) / 2)


def one_graviton():
    """N2, N3."""
    G, m1, m2, E, q = sp.symbols("G m1 m2 E q", positive=True)
    T1 = sp.diag(m1, 0, 0, 0)
    T2 = sp.diag(m2, 0, 0, 0)
    Tph = sp.zeros(4, 4)
    Tph[0, 0] = Tph[3, 3] = E
    TPT = contraction(T1, T2)
    Uq = sp.simplify(-8 * sp.pi * G / q**2 * TPT)
    # Fourier transform: the Yukawa transform of chiral_breaking at m -> 0
    r, mu = sp.symbols("r mu", positive=True)
    import chiral_breaking as CB
    Y, _ = CB.yukawa()
    ft_massless = sp.limit(Y.subs(sp.Symbol("m", positive=True), mu), mu, 0)  # FT[1/q^2] = 1/(4 pi r)
    Ur = sp.simplify(sp.factor(Uq * q**2) * ft_massless.subs(sp.Symbol("r", positive=True), r))
    ratio_photon = sp.simplify(contraction(T1, Tph) / contraction(T1, sp.diag(E, 0, 0, 0)))
    return TPT, Uq, Ur, ratio_photon


def branch_phases(n=4001):
    """N4: design A (1.468e-14 kg, dx = 720.8 um, Casimir-safe gap 181.2 um, ramps 2 x 1.581 s,
    hold 0.082 s: 3.24 s in total), parallel geometry, symmetric splitting. The phase is the time integral
    of the N2 potential along the branch trajectories, -int U_ij dt / hbar, against
    src/stur_gravity_full.trajectory_dphi."""
    import stur_gravity_entanglement as GE
    import stur_gravity_full as GF
    # design A is a point of the design-search grids of src/stur_gravity_full.py (H5)
    m = float(np.geomspace(1e-16, 1e-12, 25)[13])                          # 1.468e-14 kg
    dx = float(np.geomspace(10e-6, 3e-3, 25)[18])                          # 720.8 um
    hold = float(np.geomspace(0.05, 20, 25)[2])                            # 0.0824 s
    ramp = float(np.geomspace(0.05, 5, 17)[12])                            # 1.581 s
    gap = GE.casimir_vs_gravity_gap(GE.BASE["m"], GE.BASE["dx"], GE.BASE["tau"], "parallel")   # 181.2 um
    t = np.linspace(0, hold + 2 * ramp, n)
    y = 0.5 * dx * GF.ramp_profile(t, hold, ramp)                         # each branch at +-y
    r_same = np.full_like(t, gap)                                         # (L,L) and (R,R)
    r_cross = np.sqrt(gap**2 + (2 * y) ** 2)                              # (L,R) and (R,L)
    U = lambda r: -GE.G * m * m / r                                        # N2 potential
    phi = lambda r: -np.trapezoid(U(r), t) / GE.HBAR
    mine = 2 * phi(r_same) - 2 * phi(r_cross)
    theirs = GF.trajectory_dphi(m, dx, gap, hold, ramp, n)
    return mine, theirs, (gap, float(np.sqrt(gap**2 + dx**2))), (m, dx, gap, hold, ramp)


def main():
    banner("N1  Linearized GR for a point mass (CHECK, symbolic)")
    hb, h, Phi, gamma = linearized_point_mass()
    print(f"   hbar_00 = {hb};  h_00 = {h[0, 0]},  h_ij = {h[1, 1]} delta_ij")
    print(f"   Newtonian potential Phi = {Phi};  PPN gamma = h_ii / h_00 = {gamma}")

    banner("N2-N3  One-graviton exchange (CHECK)")
    TPT, Uq, Ur, rp = one_graviton()
    print(f"   T2.P.T1 for two static masses = {TPT}")
    print(f"   U(q) = {Uq};  U(r) = {Ur}  (Newton's law)")
    print(f"   Photon vs a static mass of the same energy: coupling ratio {rp} -> light bends twice"
          " as much as a Newtonian particle (4GM/c^2 b)")

    banner("N4  The entangling phase of design A, from the graviton-exchange potential (CHECK)")
    mine, theirs, (rs, rc), (m, dx, gap, hold, ramp) = branch_phases()
    print(f"   design A: m = {m:.4e} kg, dx = {dx * 1e6:.1f} um, gap = {gap * 1e6:.2f} um, hold {hold:.4f} s, ramps 2 x {ramp:.4f} s")
    print(f"   branch distances during the hold: same-side {rs * 1e6:.0f} um, cross {rc * 1e6:.1f} um")
    print(f"   Delta phi = {mine:.4f} rad (time integral of the N2 potential);"
          f" src/stur_gravity_full.trajectory_dphi {theirs:.4f} rad")

    banner("N5  What a positive diamond result would establish (FOLLOWS)")
    print("   - The phase needs the field sourced by each branch to act on each branch: gravity's")
    print("     field in superposition. Under the experiment's assumptions (locality, LOCC), a")
    print("     classical field cannot entangle, so a positive result rules out classical gravity.")
    print("   - It is what linearized quantum gravity (N2, a graviton field) predicts; it does")
    print("     not test the Planck scale, distinguish GR from TEGR, or link gravity to 3-3-1.")


if __name__ == "__main__":
    main()
