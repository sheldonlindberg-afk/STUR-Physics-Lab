#!/usr/bin/env python3
"""
Unifying-equation search, front 11: does the 3-3-1 content (which selects N_c = N_g = 3) also
fix the Higgs mass via the Planck boundary condition lambda(M_P) = 0?

P1 Parameter count: the 3-3-1 scalar potential with three triplets (eta, rho, chi)
   (KNOWN form): 3 mass terms, 3 self-quartics, 3 (Phi_i^dag Phi_i)(Phi_j^dag Phi_j),
   3 |Phi_i^dag Phi_j|^2, 1 trilinear f eps eta rho chi  vs the SM's mu^2, lambda.
P2 Threshold needed: integrating out heavy scalars that mix with the light doublet shifts
   lambda_SM = lambda - kappa^2 / lambda_S at mu_331 (tree level; KNOWN mechanism,
   Elias-Miro et al. 2012, recalled).  APPROXIMATION: SM one-loop running is used above
   mu_331 too (the 3-3-1 running of the quartics is NOT computed); this isolates how big a
   threshold is needed, not the full 3-3-1 prediction.
P3 Is that size natural?  Scan kappa, lambda_S log-uniform in [0.01, 1] and count how often
   the threshold lands within +-25% of the needed value.
"""
import os
import sys
from math import log
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import search_boundary as B
import search_gaps as G

MU331 = 4e3


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def state_at(mH, mu):
    return solve_ivp(B.rhs, [0, log(mu / G.MT)], B.start(mH), rtol=1e-10, atol=1e-13).y[:, -1]


def lam_MP_from(y331):
    return solve_ivp(B.rhs, [log(MU331 / G.MT), log(G.M_PLANCK / G.MT)], y331,
                     rtol=1e-10, atol=1e-13).y[5, -1]


def main():
    banner("P1  Free parameters added where the Higgs-mass prediction comes from")
    sm = {"mu^2": 1, "lambda": 1}
    t331 = {"mass terms": 3, "self quartics": 3, "(Pi^dag Pi)(Pj^dag Pj)": 3, "|Pi^dag Pj|^2": 3,
            "trilinear f": 1}
    print(f"   SM scalar sector: {sum(sm.values())} parameters;  3-3-1 (3 triplets): {sum(t331.values())}"
          f"  {t331}")
    print("   plus the 3-3-1 vevs' ratio and exotic-quark Yukawas.  lambda(M_P) = 0 no longer has a")
    print("   unique meaning: WHICH quartic(s) vanish, and with what mixing, are new choices.")

    banner("P2  Threshold needed at mu_331 = 4 TeV to reach m_H = 125.20 with lambda(M_P) = 0")
    y_meas = state_at(125.20, MU331)
    lam_crit = brentq(lambda L: lam_MP_from(np.r_[y_meas[:5], L]), 0.0, 0.3)
    delta = lam_crit - y_meas[5]
    print(f"   lambda_SM(4 TeV) from measured m_H = {y_meas[5]:.4f}")
    print(f"   lambda(4 TeV) that runs to 0 at M_P  = {lam_crit:.4f}")
    print(f"   needed tree-level threshold  delta = kappa^2/lambda_S = {delta:.4f}  (positive: the sign")
    print("   the heavy-scalar mixing mechanism gives - it can only LOWER the light quartic)")

    banner("P3  How natural is that threshold?  (kappa, lambda_S log-uniform in [0.01, 1])")
    rng = np.random.default_rng(1)
    k, ls = np.exp(rng.uniform(log(0.01), log(1), (2, 1_000_000)))
    d = k**2 / ls
    hit = np.mean(np.abs(d / delta - 1) < 0.25)
    over = np.mean(d > delta)
    print(f"   fraction of the scan with delta within +-25% of {delta:.4f}: {hit:.1%}")
    print(f"   fraction with delta larger than needed (would overshoot below 125 GeV): {over:.1%}")
    print("   -> a threshold of the needed size is generic: the 3-3-1 sector ACCOMMODATES 125 GeV")
    print("      with ordinary couplings, so it does not PREDICT it.")


if __name__ == "__main__":
    main()
