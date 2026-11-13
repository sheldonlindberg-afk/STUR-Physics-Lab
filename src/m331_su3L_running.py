#!/usr/bin/env python3
"""
Unifying-equation search, front 7: can SU(3)_L running remove N_c = 5 (and 7, 9, ...)?

With N_g = N_c (front 6), the SU(3)_L-charged left-handed fermions are
N_g lepton triplets + N_g x N_c quark (anti)triplets = N_c (1 + N_c) Weyl triplets.
One-loop coefficient (d alpha^-1 / d ln mu = -b / 2 pi; b > 0 = asymptotically free):
    b_L = (11/3) C_A - (2/3) sum_Weyl T(R) - (1/3) sum_complex-scalars T(R)
        = 11 - N_c (1 + N_c) / 3 - scalars,      T(3) = 1/2, T(6) = 5/2
Scalar content (KNOWN): beta = +-1/sqrt3 models: 3 triplets (eta, rho, chi) -> 1/2;
minimal model adds a sextet -> + 5/6.
ASSUMPTION (labelled): the theory must stay perturbative (no Landau pole) up to the
Planck scale.  Matching: g_L = g_2 at the 3-3-1 scale (SU(2)_L inside SU(3)_L), taken as
mu_331 = 4 TeV with g_2 from one-loop Standard Model running (front 6 inputs).
"""
from math import log, pi, exp

MZ, ainv, s2 = 91.1880, 127.930, 0.23129      # PDG 2024 (MS-bar)
M_PLANCK = 1.22089e19


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def alpha2_inv(mu):
    return s2 * ainv + 19 / 6 * log(mu / MZ) / (2 * pi)


def b_L(Nc, sextet=False):
    return 11 - Nc * (1 + Nc) / 3 - 0.5 - (5 / 6 if sextet else 0)


def landau(Nc, mu0=4e3, sextet=False):
    b = b_L(Nc, sextet)
    a0 = alpha2_inv(mu0)
    if b >= 0:
        return b, None
    return b, mu0 * exp(2 * pi * a0 / (-b))


def main():
    banner("L1  SU(3)_L one-loop coefficient with N_g = N_c generations")
    print(f"   1/alpha_L at 4 TeV (= 1/alpha_2) = {alpha2_inv(4e3):.2f}")
    print("   N_c   N_g   triplets   b_L (3 triplets)   Landau pole        b_L (+sextet)   Landau pole")
    for Nc in [1, 3, 5, 7, 9]:
        b, mp = landau(Nc)
        bs, mps = landau(Nc, sextet=True)
        f = lambda m: "none (AF)" if m is None else f"{m:.1e} GeV"
        print(f"   {Nc:3d}   {Nc:3d}   {Nc*(1+Nc):8d}   {b:15.3f}   {f(mp):17s} {bs:14.3f}   {f(mps)}")
    print(f"   Planck scale = {M_PLANCK:.2e} GeV")

    banner("L2  Which odd N_c survive perturbativity up to the Planck scale?")
    for sextet in [False, True]:
        ok = [Nc for Nc in range(1, 16, 2)
              if (landau(Nc, sextet=sextet)[1] is None or landau(Nc, sextet=sextet)[1] > M_PLANCK)]
        print(f"   scalars = 3 triplets{' + sextet' if sextet else '':9s}: surviving odd N_c = {ok}")
    print("   (N_c = 1 has no strong force: front 5 excludes it.)")
    print("   -> THEORY now allows N_c = N_g in {3, 5}.  Five survives: b_L = +1/2 (barely")
    print("      asymptotically free) with triplets, and a far-away pole with the sextet.")

    banner("L3  How far is 5 from the edge?")
    for sextet in [False, True]:
        b, mp = landau(5, sextet=sextet)
        print(f"   N_c = 5{' + sextet' if sextet else '':9s}: b_L = {b:+.3f}  pole: "
              f"{'none' if mp is None else f'{mp:.1e} GeV (log10 = {log(mp, 10):.0f})'}")
    print("   One extra complex scalar triplet costs 1/6 in b_L; with 3 triplets, N_c = 5 loses")
    print("   asymptotic freedom after 3 more scalar triplets, but its pole would still sit far")
    print("   beyond the Planck scale.  Two-loop terms were NOT computed.")


def bY(Nc, exotics=True):
    """ESTIMATE: hypercharge-equivalent one-loop coefficient above the 3-3-1 scale.
    SM fermions with front-5 N_c-dependent charges, N_g = N_c generations, plus (if exotics)
    one exotic Dirac quark per generation (SU(2) singlet, Y = Q): u-like in the (N_g - n)
    triplet generations, d-like in the n anti-triplet ones, n = (1 + N_c)/2 (beta = -1/sqrt3
    pattern); neutral heavy leptons add nothing; only the SM Higgs doublet among scalars."""
    from fractions import Fraction as F
    Qu, Qd = F(Nc + 1, 2 * Nc), F(1 - Nc, 2 * Nc)
    YQ = F(1, 2 * Nc)
    per_gen = 2 * Nc * YQ**2 + Nc * Qu**2 + Nc * Qd**2 + 2 * F(1, 4) + 1
    Ng = Nc
    tot = Ng * per_gen
    if exotics:
        n = (1 + Nc) // 2
        tot += (Ng - n) * 2 * Nc * Qu**2 + n * 2 * Nc * Qd**2
    return -(F(2, 3) * tot + F(1, 3) * 2 * F(1, 4))


def bY_pole(Nc, exotics=True, mu0=4e3):
    b = float(bY(Nc, exotics))
    aY0 = (1 - s2) * ainv - 41 / 6 * log(mu0 / MZ) / (2 * pi)
    return b, mu0 * exp(2 * pi * aY0 / (-b))


def hypercharge():
    banner("L4  Hypercharge-equivalent Landau pole (ESTIMATE, see bY docstring)")
    print(f"   check: N_c = 3 without exotics gives b_Y = {bY(3, False)} (SM: -41/6)")
    for Nc in [3, 5, 7]:
        for ex in [False, True]:
            b, mp = bY_pole(Nc, ex)
            print(f"   N_c = N_g = {Nc}, {'with' if ex else 'no  '} exotic quarks:  b_Y = {b:7.2f}   pole ~ {mp:.1e} GeV"
                  f"   {'BELOW' if mp < M_PLANCK else 'above'} Planck")
    mu0 = 4e3
    aY0 = (1 - s2) * ainv - 41 / 6 * log(mu0 / MZ) / (2 * pi)
    b_crit = 2 * pi * aY0 / log(M_PLANCK / mu0)
    print(f"   critical |b_Y| for a pole exactly at the Planck scale: {b_crit:.2f}")
    for Nc in [3, 5]:
        b = -float(bY(Nc, True))
        print(f"   N_c = {Nc} with exotics: |b_Y| = {b:.2f}  ->  margin to flip the verdict = {b_crit - b:+.2f}")
    print("   (the three 3-3-1 scalar triplets add roughly 1-2 to |b_Y| - NOT computed exactly;")
    print("    both margins, 7.1 and 5.6, exceed that)")
    print("   1/alpha_Y = 1/alpha_X + beta^2/alpha_L with alpha_L perturbative: a pole in the Y")
    print("   combination implies the U(1)_X pole comes no later - so the estimate is indicative,")
    print("   not exact (true X charges and scalar content shift b by O(1)).")


if __name__ == "__main__":
    main()
    hypercharge()
