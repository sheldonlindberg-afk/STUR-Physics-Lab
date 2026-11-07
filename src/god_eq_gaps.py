#!/usr/bin/env python3
"""
God-equation search, front 9: WHY the equation has not produced continuous parameters.

So far every result is DISCRETE (N_c, N_g, charges in thirds, spin 1/2): anomalies and
topology fix integers.  The Standard Model's 19 parameters are continuous.  The only
continuous-valued criterion used was 'consistent up to the Planck scale' (front 7).
Test it on a continuous parameter: the Higgs self-coupling lambda must stay >= 0 up to
M_P (vacuum stability).  Does that predict m_H = 125 GeV?

One-loop SM RGEs (KNOWN; V = lambda (H^dag H)^2, m_H^2 = 2 lambda v^2, g1 = g'):
 16pi^2 dg_i/dt = b_i g_i^3,  b = (41/6, -19/6, -7)
 16pi^2 dy_t/dt = y_t [9/2 y_t^2 - 8 g3^2 - 9/4 g2^2 - 17/12 g1^2]
 16pi^2 dlam/dt = 24 lam^2 + 12 lam y_t^2 - 6 y_t^4 - 3 lam (3 g2^2 + g1^2)
                  + 3/8 [2 g2^4 + (g2^2 + g1^2)^2]
Inputs (LIT, recalled - not retrieved this session): m_H = 125.20 GeV, m_t(pole) = 172.57
+- 0.29 GeV, v = 246.22 GeV, alpha_s(M_Z) = 0.1180.  Matching (APPROXIMATE): tree-level
lambda = m_H^2/2v^2; m_t(MS-bar) from the 3-loop QCD pole relation, no electroweak terms.
These approximations shift lambda and y_t by ~1-3 %, which matters - see the y_t scan.
"""
import os
import sys
from math import log, pi, sqrt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stur_open_problems import alpha_s_run

MZ, ainv, s2 = 91.1876, 127.95, 0.23122
MT, V = 172.57, 246.22
M_PLANCK = 1.22089e19


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def initial(mH, yt_scale=1.0):
    L = log(MT / MZ) / (2 * pi)
    a1 = (1 - s2) * ainv - 41 / 6 * L
    a2 = s2 * ainv + 19 / 6 * L
    a3 = 1 / alpha_s_run(MT)
    g1, g2, g3 = sqrt(4 * pi / a1), sqrt(4 * pi / a2), sqrt(4 * pi / a3)
    a = alpha_s_run(MT) / pi
    mt_ms = MT / (1 + 4 / 3 * a + 10.9 * a**2 + 107 * a**3)
    yt = sqrt(2) * mt_ms / V * yt_scale
    lam = mH**2 / (2 * V**2)
    return np.array([g1, g2, g3, yt, lam]), mt_ms


def rhs(t, y):
    g1, g2, g3, yt, lam = y
    k = 1 / (16 * pi**2)
    return k * np.array([
        41 / 6 * g1**3, -19 / 6 * g2**3, -7 * g3**3,
        yt * (4.5 * yt**2 - 8 * g3**2 - 2.25 * g2**2 - 17 / 12 * g1**2),
        24 * lam**2 + 12 * lam * yt**2 - 6 * yt**4 - 3 * lam * (3 * g2**2 + g1**2)
        + 3 / 8 * (2 * g2**4 + (g2**2 + g1**2) ** 2)])


def run(mH, yt_scale=1.0, mu=M_PLANCK):
    y0, _ = initial(mH, yt_scale)
    s = solve_ivp(rhs, [0, log(mu / MT)], y0, rtol=1e-10, atol=1e-12, dense_output=True)
    return s


def main():
    banner("H1  Inputs at mu = m_t")
    y0, mtms = initial(125.20)
    print(f"   m_t(MS-bar) = {mtms:.2f} GeV   y_t = {y0[3]:.4f}   lambda(tree) = {y0[4]:.4f}   g3 = {y0[2]:.4f}")

    banner("H2  Run the measured Higgs up to the Planck scale (one loop)")
    s = run(125.20)
    ts = np.linspace(0, log(M_PLANCK / MT), 400)
    lam = s.sol(ts)[4]
    mu = MT * np.exp(ts)
    i0 = np.argmax(lam < 0) if np.any(lam < 0) else None
    print(f"   lambda(M_P) = {lam[-1]:+.4f};   min lambda = {lam.min():+.4f} at mu = {mu[np.argmin(lam)]:.1e} GeV")
    if i0:
        print(f"   lambda turns negative at mu = {mu[i0]:.1e} GeV  ->  the SM vacuum is NOT absolutely stable")

    banner("H3  The Planck-consistency criterion as a PREDICTION: m_H with lambda >= 0 up to M_P")
    def min_lam(mH, ys=1.0):
        return run(mH, ys).sol(ts)[4].min()
    mH_min = brentq(lambda m: min_lam(m), 100, 200)
    print(f"   one loop: lambda stays >= 0 up to M_P only if m_H >= {mH_min:.1f} GeV   (measured 125.20)")
    for ys in [0.98, 0.99, 1.0, 1.01, 1.02]:
        print(f"     y_t x {ys:.2f}:  m_H(min) = {brentq(lambda m: min_lam(m, ys), 80, 250):6.1f} GeV")
    print("   LIT (recalled, two-loop NNLO: Degrassi et al. 2012; Buttazzo et al. 2013): stability needs")
    print("   m_H >~ 129-130 GeV; measured 125 GeV -> metastable vacuum, lifetime >> age of universe.")

    banner("H4  What this means for the search")
    print("   * The criterion behind front 7 ('consistent to M_P') does NOT produce the Higgs mass:")
    print("     applied as stability it misses 125 GeV by several GeV (one loop here; ~4-5 GeV at NNLO).")
    print("   * A Landau pole (front 7) is a breakdown of the theory; metastability is not - the vacuum")
    print("     simply decays far in the future.  The two criteria are different; front 7's survives,")
    print("     but its power to fix CONTINUOUS parameters fails at the first test.")
    print("   * Continuous parameters need dynamics with a boundary condition (e.g. asymptotic-safety")
    print("     gravity: Shaposhnikov-Wetterich 2010 predicted m_H ~ 126 GeV - LIT, recalled).")


if __name__ == "__main__":
    main()
