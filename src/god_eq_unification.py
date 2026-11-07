#!/usr/bin/env python3
"""
God-equation search, front 12: gauge-coupling unification in 3-3-1 (N_c = N_g = 3).

Embedding-independent test: SU(3)_C and SU(3)_L have the same (standard) normalisation, so
in ANY unified group containing both they must meet: alpha_L^-1 = alpha_3^-1.  U(1)_X
normalisation depends on the embedding and is only examined if they meet.
Machinery: the calibrated two-loop gauge RGEs of god_eq_331_exact.py (reproduces all SM
coefficients exactly).  Matching at mu_331: g_L = g_2, 1/g_Y^2 = 1/g_X^2 + beta^2/g_L^2.
Reference: the Standard Model 'near-miss triangle' (KNOWN): GUT-normalised couplings meet
pairwise at three different scales.
"""
import os
import sys
from math import log, pi
import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import god_eq_331_exact as E
from stur_open_problems import alpha_s_run

MZ, ainv, s2 = 91.1876, 127.95, 0.23122


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def run_inv_alpha(a, b, g0, mu0, mu1, n=2000):
    a = np.array([float(x) for x in a]); b = np.array([[float(x) for x in r] for r in b])
    rhs = lambda t, g: g**3 / (16 * pi**2) * (a + b @ (g**2) / (16 * pi**2))
    ts = np.linspace(0, log(mu1 / mu0), n)
    s = solve_ivp(rhs, [0, ts[-1]], g0, t_eval=ts, rtol=1e-10, atol=1e-12)
    return mu0 * np.exp(s.t), 4 * pi / s.y**2


def crossing(mu, x, y):
    d = x - y
    i = np.where(np.diff(np.sign(d)) != 0)[0]
    return mu[i[0]] if i.size else None


def sm_triangle():
    a, b = E.sm_check()                                      # GUT-normalised g1
    a3 = 1 / alpha_s_run(MZ)
    inv = np.array([(1 - s2) * ainv * 3 / 5, s2 * ainv, a3])
    mu, ia = run_inv_alpha(a, b, np.sqrt(4 * pi / inv), MZ, 1e19)
    return mu, ia


def main():
    banner("U0  Reference: Standard Model (two loop, GUT-normalised U(1))")
    mu, ia = sm_triangle()
    for (i, j, nm) in [(0, 1, "g1-g2"), (1, 2, "g2-g3"), (0, 2, "g1-g3")]:
        c = crossing(mu, ia[i], ia[j])
        print(f"   {nm} meet at {c:.1e} GeV" if c else f"   {nm} never meet")
    print("   -> three different scales: the KNOWN near miss (no SM unification)")

    for name, model in E.MODELS.items():
        banner(f"U1  3-3-1 (beta = {name}), N_c = N_g = 3: do SU(3)_C and SU(3)_L meet?")
        gs, ferm, scal, _ = model(3)
        a, b = E.coefficients(gs, ferm, scal)
        print(f"   one-loop a = (X {float(a[0]):.2f}, L {float(a[1]):.2f}, C {float(a[2]):.2f})")
        for mu0 in [2e3, 4e3, 1e5, 1e10, 1e15]:
            L0 = log(mu0 / MZ) / (2 * pi)
            aY = (1 - s2) * ainv - 41 / 6 * L0
            a2 = s2 * ainv + 19 / 6 * L0
            a3 = 1 / alpha_s_run(mu0)
            inv0 = np.array([aY - a2 / 3, a2, a3])
            mu, ia = run_inv_alpha(a, b, np.sqrt(4 * pi / inv0), mu0, 1e19)
            c = crossing(mu, ia[1], ia[2])
            gap = ia[1, -1] - ia[2, -1]
            print(f"   mu_331 = {mu0:.0e} GeV: 1/alpha_L - 1/alpha_3 = {a2 - a3:6.2f} at mu_331,"
                  f" {gap:6.2f} at M_P  ->  {'meet at %.1e GeV' % c if c else 'NEVER meet below M_P'}")

    banner("U2  What it would take: extra SU(3)_L-charged matter")
    gs, ferm, scal, _ = E.model_331(3)
    a, _ = E.coefficients(gs, ferm, scal)
    gap0 = (s2 * ainv + 19 / 6 * log(4e3 / MZ) / (2 * pi)) - 1 / alpha_s_run(4e3)
    for muU in [1e15, 1e16, 1e17, 1.2e19]:
        need = 2 * pi * gap0 / log(muU / 4e3)                 # a_L - a_3 required (one loop)
        dL = need - float(a[1] - a[2])
        print(f"   meet at {muU:.0e} GeV needs a_L - a_3 = {need:+.2f} (now {float(a[1]-a[2]):+.2f}):"
              f"  +{dL:.2f} = {dL/(1/3):.0f} extra colourless Weyl triplets (or {dL/(1/6):.0f} complex scalar triplets)")
    print(f"   Adding that much SU(3)_L matter moves a_L(N_c = 3) from {float(a[1]):.2f} to about"
          f" {float(a[1]) + 5.6:.1f} (fermions), and")
    print("   a_L(N_c = 5) from -0.5 to about +5: front 7's N_c-selection chain would have to be")
    print("   redone with the new content (not done here).")


if __name__ == "__main__":
    main()
