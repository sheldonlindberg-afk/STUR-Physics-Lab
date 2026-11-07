#!/usr/bin/env python3
"""
God-equation search, front 10: Planck-scale boundary conditions (asymptotic-safety
gravity) as a source of CONTINUOUS parameters.

A. Shaposhnikov-Wetterich (2010, KNOWN): gravity makes lambda irrelevant above the
   Planck scale, so lambda(mu*) ~ 0 at the transition scale mu*  ->  predicts m_H.
B. Eichhorn-Held (2018, KNOWN mechanism): one universal gravitational term -f_y y in
   every Yukawa beta function.  Fixed points for y_t and y_b (one loop, FOLLOWS):
        beta_yt/y_t = beta_yb/y_b  =>  3 (y_t^2 - y_b^2) - g1^2 = 0   (g2, g3 terms cancel)
   i.e. y_t^2 - y_b^2 = g1^2/3 at mu*  ->  predicts m_t with no free gravity parameter.

One-loop SM RGEs with y_t, y_b (tau neglected).  Inputs: as in god_eq_gaps.py plus
y_b(m_t) ~ 0.0158 (m_b(m_t) ~ 2.75 GeV, recalled, approximate).  mu* scanned between the
reduced Planck mass 2.435e18 GeV and M_P = 1.221e19 GeV.
Calibration: one loop overestimates the stability bound (front 9: 133.1 GeV) relative to
the NNLO literature value ~129.5 GeV (recalled; Buttazzo et al. 2013) - the offset is used
as a labelled systematic correction, not as data.
"""
import os
import sys
from math import log, pi, sqrt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import god_eq_gaps as G
from stur_open_problems import alpha_s_run

YB_MT = 0.0158
MU_STAR = [2.435e18, 1.22089e19]
NNLO_STABILITY = 129.5            # GeV, recalled literature anchor (approximate)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def rhs(t, y):
    g1, g2, g3, yt, yb, lam = y
    k = 1 / (16 * pi**2)
    Y2 = 3 * (yt**2 + yb**2)
    return k * np.array([
        41 / 6 * g1**3, -19 / 6 * g2**3, -7 * g3**3,
        yt * (1.5 * (yt**2 - yb**2) + Y2 - 8 * g3**2 - 2.25 * g2**2 - 17 / 12 * g1**2),
        yb * (1.5 * (yb**2 - yt**2) + Y2 - 8 * g3**2 - 2.25 * g2**2 - 5 / 12 * g1**2),
        24 * lam**2 + 4 * lam * Y2 - 6 * (yt**4 + yb**4) - 3 * lam * (3 * g2**2 + g1**2)
        + 3 / 8 * (2 * g2**4 + (g2**2 + g1**2) ** 2)])


def start(mH, mt_pole=G.MT):
    y0, _ = G.initial(mH)
    a = alpha_s_run(mt_pole) / pi
    yt = sqrt(2) * mt_pole / (1 + 4 / 3 * a + 10.9 * a**2 + 107 * a**3) / G.V
    return np.array([y0[0], y0[1], y0[2], yt, YB_MT, y0[4]])


def up(y0, mu):
    return solve_ivp(rhs, [0, log(mu / G.MT)], y0, rtol=1e-10, atol=1e-13).y[:, -1]


def lam_at(mH, mt, mu):
    return up(start(mH, mt), mu)[5]


def mt_from_yt(yt):
    a = alpha_s_run(G.MT) / pi
    return yt * G.V / sqrt(2) * (1 + 4 / 3 * a + 10.9 * a**2 + 107 * a**3)


def main():
    offset = None
    banner("A  Shaposhnikov-Wetterich: lambda(mu*) = 0")
    for mu in MU_STAR:
        mH = brentq(lambda m: lam_at(m, G.MT, mu), 100, 200)
        yP = up(start(mH), mu)
        beta_lam = rhs(0, yP)[5]
        mt_req = brentq(lambda m: lam_at(125.20, m, mu), 160, 180)
        print(f"   mu* = {mu:.2e} GeV:  predicted m_H = {mH:6.1f} GeV (one loop, m_t = {G.MT})"
              f"   beta_lambda(mu*) = {beta_lam:+.1e}")
        print(f"                         m_t needed for m_H = 125.20:  {mt_req:6.2f} GeV   (measured 172.57 +- 0.29)")
    stab = brentq(lambda m: min(solve_ivp(rhs, [0, log(G.M_PLANCK / G.MT)], start(m), rtol=1e-10,
                                           dense_output=True).sol(np.linspace(0, log(G.M_PLANCK / G.MT), 300))[5]), 100, 200)
    offset = stab - NNLO_STABILITY
    print(f"\n   calibration: one-loop stability bound {stab:.1f} GeV vs NNLO ~{NNLO_STABILITY} (recalled)"
          f" -> one-loop offset ~{offset:+.1f} GeV")
    for mu in MU_STAR:
        mH = brentq(lambda m: lam_at(m, G.MT, mu), 100, 200)
        print(f"   corrected SW prediction (mu* = {mu:.1e}): m_H ~ {mH - offset:.1f} GeV  vs measured 125.20")
    print("   -> lambda ~ 0 near M_P is near-critical: beta_lambda is small there too, so the")
    print("      condition is natural - but at face value it predicts m_H ~ 129-130, not 125.")

    banner("B  Eichhorn-Held: y_t^2 - y_b^2 = g1^2/3 at mu*  ->  m_t")
    y0 = start(125.20)
    for mu in MU_STAR:
        yP = up(y0, mu)
        g1P, ybP = yP[0], yP[4]
        ytP_meas = yP[3]
        ytP_fp = sqrt(g1P**2 / 3 + ybP**2)
        yinit = yP.copy(); yinit[3] = ytP_fp
        down = solve_ivp(rhs, [log(mu / G.MT), 0], yinit, rtol=1e-10, atol=1e-13).y[:, -1]
        print(f"   mu* = {mu:.2e}:  g1 = {g1P:.4f}, y_t(fixed point) = {ytP_fp:.4f}"
              f"  (measured y_t runs to {ytP_meas:.4f})")
        print(f"                     predicted m_t = {mt_from_yt(down[3]):6.1f} GeV   measured 172.57")
    print("   LIT (retrieved via search, not read in full): Eichhorn-Held 2017 (arXiv 1707.01107 v3):")
    print("   M_t ~ 171 GeV for a RANGE of gravity couplings (not parameter-free) and M_h ~ 132 GeV.")
    print("   Their 2018 top/bottom-from-hypercharge paper (1803.04027) could not be read here (network")
    print("   block); this parameter-free one-loop version gives m_t ~ 136-140 GeV - UNRECONCILED.")


if __name__ == "__main__":
    main()
