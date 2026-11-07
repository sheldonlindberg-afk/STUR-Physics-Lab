#!/usr/bin/env python3
"""
God-equation search, front 6: why three generations?  (3-3-1 models)

KNOWN framework (Pisano-Pleitez 1992, Frampton 1992): SU(3)_C x SU(3)_L x U(1)_X.
Left-handed leptons: one SU(3)_L triplet per generation (N_g triplets).
Quarks: n generations in the anti-triplet, N_g - n in the triplet, each x N_c colours,
each multiplet holding 3 quark flavours (2 Standard Model + 1 exotic).

G1 SU(3)_L^3 anomaly: #triplets = #anti-triplets  ->  N_g (1 + N_c) = 2 n N_c.
G2 QCD asymptotic freedom with n_f = 3 N_g flavours: 11 N_c/3 - 2 n_f/3 > 0.
G3 Combine with front 5 (N_c odd).
G4 Data for the MINIMAL model (beta = -sqrt3): it needs sin^2 theta_W(mu) < 1/4 at the
   3-3-1 scale.  Running the Standard Model couplings up (one loop) gives the scale
   mu_* where sin^2 theta_W reaches 1/4; the new gauge bosons must lie below it.
   Inputs (LIT, PDG, recalled): 1/alpha(M_Z) = 127.95, sin^2 theta_W(M_Z) = 0.23122 (MS-bar).
   LHC (LIT, retrieved): minimal-model Z' below 5 TeV excluded; beta = +-1/sqrt3: Z' > 3.6-4.2 TeV.
"""
from math import gcd, log, pi, exp
from scipy.optimize import brentq


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def allowed_Ng(Nc, Ng_max=40):
    out = []
    for Ng in range(1, Ng_max + 1):
        num = Ng * (1 + Nc)
        if num % (2 * Nc) == 0 and 0 <= num // (2 * Nc) <= Ng:
            b0 = 11 * Nc / 3 - 2 * (3 * Ng) / 3
            out.append((Ng, num // (2 * Nc), b0 > 0))
    return out


def sin2_running(mu, MZ=91.1876, ainv=127.95, s2=0.23122):
    """One-loop SM running of g' and g (non-GUT normalisation): b_Y = 41/6, b_2 = -19/6."""
    aY, a2 = (1 - s2) * ainv, s2 * ainv               # 1/alpha_Y, 1/alpha_2 at M_Z
    L = log(mu / MZ) / (2 * pi)
    aY_mu, a2_mu = aY - 41 / 6 * L, a2 + 19 / 6 * L
    return (1 / aY_mu) / (1 / aY_mu + 1 / a2_mu)


def main():
    banner("G1+G2  Generations allowed by the SU(3)_L anomaly and QCD asymptotic freedom")
    for Nc in [3, 5, 7]:
        rows = allowed_Ng(Nc)
        anom = [r[0] for r in rows][:6]
        af = [r[0] for r in rows if r[2]]
        print(f"   N_c = {Nc}:  anomaly-free N_g = {anom} ...   + asymptotic freedom: N_g = {af}")
    print("   -> N_g = N_c exactly: the generation number is LOCKED to the colour number.")
    print("      With N_c = 3: n = 2 anti-triplet + 1 triplet quark generations (the standard assignment).")

    banner("G3  Combined with front 5")
    print("   Witten / spin-charge twist: N_c odd.  3-3-1: N_g = N_c.  So the two 'threes' are one number;")
    print("   the measured N_g = 3 (LIT, LEP: N_nu = 2.98 +- 0.01) and the R-ratio (front 5) agree on it.")
    print("   Still open: why that one number is 3 rather than 5 or 7.")

    banner("G4  Minimal 3-3-1 (beta = -sqrt3) vs data: the sin^2 theta_W = 1/4 wall")
    for mu in [91.1876, 1e3, 2e3, 3e3, 4e3, 5e3]:
        print(f"   mu = {mu:8.1f} GeV:  sin^2 theta_W = {sin2_running(mu):.5f}")
    mu_star = brentq(lambda m: sin2_running(m) - 0.25, 100, 1e6)
    print(f"   sin^2 theta_W reaches 1/4 at mu_* = {mu_star/1e3:.2f} TeV (one loop, Standard Model content)")
    print("   The U(1)_X coupling g_X^2 ~ s^2/(1 - 4 s^2) diverges there (Landau pole), so every new")
    print("   gauge boson of the minimal model must lie below mu_*.  LHC (LIT): Z' < 5 TeV excluded.")
    print(f"   -> minimal 3-3-1 needs M_Z' < {mu_star/1e3:.1f} TeV but data require M_Z' > 5 TeV: EXCLUDED")
    print(f"      Two-loop and threshold effects were NOT computed; rescuing the model needs them to")
    print(f"      raise mu_* by {5e3/mu_star*100-100:.0f}% (to 5 TeV).")
    print("   beta = +-1/sqrt3 variants have no such pole: the N_g = N_c result survives there,")
    print("   with Z' > 3.6-4.2 TeV (LIT) - testable, not excluded.")
    return mu_star


if __name__ == "__main__":
    main()
