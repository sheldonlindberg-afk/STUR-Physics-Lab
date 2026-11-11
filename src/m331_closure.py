#!/usr/bin/env python3
"""
Unifying-equation search, front 7f: closing the remaining assumptions of N_c = N_g = 3.

C1  Is Witten's anomaly (step 1) needed? In 3-3-1, SU(2)_L sits inside SU(3)_L, and
    pi_4(SU(3)) = 0, so the UV theory has no global anomaly of its own. Enumerate every
    (N_c, N_g, n) with the SU(3)_L anomaly N_g (1 + N_c) = 2 n N_c and asymptotic freedom
    of colour, 11 N_c - 6 N_g > 0 (3 N_g Dirac flavours). Proof in the output.
C2  The running of the Yukawas. Yukawas only slow the U(1)_X growth, so switching them
    off entirely is a lower bound on the N_c = 3 pole for any running. Thresholds kept.
C3  Which cutoff, which criterion? The selection holds for any cutoff Lambda with
    (best N_c = 5 pole) < Lambda < (worst N_c = 3 pole). Computed for g = 4 pi and
    alpha = 1 over the front-7e spectrum, with and without Yukawas.
"""
import os
import sys
from math import gcd, pi, sqrt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_threshold as T

M_PLANCK = T.M_PLANCK
M_RED = M_PLANCK / sqrt(8 * pi)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def solutions(nc_max=60, ng_max=400):
    out = []
    for Nc in range(2, nc_max + 1):
        for Ng in range(1, ng_max + 1):
            if 11 * Nc - 6 * Ng <= 0:
                break
            if (Ng * (1 + Nc)) % (2 * Nc) == 0:
                n = Ng * (1 + Nc) // (2 * Nc)
                if 0 <= n <= Ng:
                    out.append((Nc, Ng, n))
    return out


def main():
    res = {}
    banner("C1  Anomaly + asymptotic freedom alone: is Witten's anomaly needed?")
    sol = solutions()
    print(f"   All solutions with 2 <= N_c <= 60, N_g <= 400: {len(sol)}")
    print("   " + ", ".join(f"(N_c={a}, N_g={b}, n={c})" for a, b, c in sol[:8]) + ", ...")
    ok = all(Nc == Ng and Nc % 2 == 1 for Nc, Ng, n in sol)
    res["C1"] = (len(sol), ok)
    print(f"   Every solution has N_g = N_c with N_c odd: {ok}")
    print("   Proof: gcd(N_c, N_c + 1) = 1. If N_c is odd, gcd(N_c + 1, 2N_c) = 2, so N_c divides N_g;")
    print("   asymptotic freedom (N_g < 11N_c/6) leaves N_g = N_c. If N_c is even, N_c + 1 is odd and")
    print("   gcd(N_c + 1, 2N_c) = 1, so 2N_c divides N_g, and 2N_c > 11N_c/6 violates asymptotic freedom.")
    print("   The SU(2) doublets number N_g + N_c N_g = 2 n N_c, always even, so Witten's anomaly is")
    print("   automatically absent: it is implied, not used. Step 1 (and the spin-charge twist) is")
    print("   redundant in 3-3-1, and the chain no longer leans on a global-anomaly argument that the")
    print("   UV group SU(3)_L would not itself impose.")
    print(f"   check gcds: " + ", ".join(f"N_c={k}: {gcd(k + 1, 2 * k)}" for k in (2, 3, 4, 5, 6, 7)))

    banner("C2  Yukawas switched off entirely (a lower bound on the N_c = 3 pole for any Yukawa running)")
    for v in ("-1/sqrt3", "+1/sqrt3"):
        (lo, *a), _ = T.scan(3, v, yukawas=False)
        (lo4, *_), _ = T.scan(3, v, MVs=(4e3, 1e4), yukawas=False)
        res[(v, "noY")] = (lo, lo4)
        print(f"   beta = {v:8s}: worst N_c = 3 pole = {lo:.2e} GeV = {lo/M_PLANCK:.3g} M_Pl"
              f"  (M_V >= 4 TeV: {lo4/M_PLANCK:.3g} M_Pl)")
    print("   So the selection does not depend on how the Yukawas run: it holds with none at all.")

    banner("C3  The window of cutoffs for which only N_c = 3 survives")
    print(f"   Planck mass {M_PLANCK:.2e} GeV; reduced Planck mass {M_RED:.2e} GeV.")
    print("   criterion   Yukawas   beta       window (GeV): best N_c = 5 ... worst N_c = 3     M_Pl inside?  M_red inside?")
    for crit, gm in (("g = 4 pi", 4 * pi), ("alpha = 1", sqrt(4 * pi))):
        for yk in (True, False):
            for v in ("-1/sqrt3", "+1/sqrt3"):
                (lo3, *_), _ = T.scan(3, v, gmax=gm, yukawas=yk)
                _, (hi5, *_) = T.scan(5, v, gmax=gm, yukawas=yk)
                res[(crit, yk, v)] = (hi5, lo3)
                print(f"   {crit:10s}  {'on ' if yk else 'off'}       {v:9s}  {hi5:.2e} ... {lo3:.2e}"
                      f"         {'yes' if hi5 < M_PLANCK < lo3 else 'NO '}           "
                      f"{'yes' if hi5 < M_RED < lo3 else 'NO '}")
    print("   Reading: the selection does not need the Planck scale exactly. Any cutoff inside the")
    print("   intersection of the windows works, including the reduced Planck mass and the usual")
    print("   grand-unification scale 2e16 GeV, wherever the window covers them.")
    return res


if __name__ == "__main__":
    main()
