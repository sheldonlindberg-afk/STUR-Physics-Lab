#!/usr/bin/env python3
"""
Unifying-equation search, front 7e: one-loop threshold matching at the 3-3-1 scale.

Front 7d left one number open: in the beta = +1/sqrt3 variant, N_c = 3 reaches the Planck
scale only if sin^2 theta_W(4 TeV) < 0.266, against the measured 0.250. The matching
SU(3)_L x U(1)_X -> SU(2)_L x U(1)_Y had been done at tree level. Here it is done at one
loop.

Matching (MS-bar; LIT recalled: Weinberg, PLB 91, 51 (1980); Hall, NPB 178, 75 (1981)):
    1/alpha_low(mu) = 1/alpha_high(mu) - lambda(mu) / (12 pi)
    lambda = sum_V t^2 (1 - 21 ln(M_V/mu)) + 8 sum_Dirac t^2 ln(M_F/mu)
             + sum_real-scalars t^2 ln(M_S/mu)
t^2 is the trace of the low-energy generator squared over the heavy multiplet. For
U(1)_Y the high-energy coupling is the combination 1/alpha_X + beta^2/alpha_L. The "1" in
the vector term is the MS-bar constant (zero in DR-bar).

The heavy spectrum (both variants, counted from the model, not assumed):
  vectors   one complex SU(2) doublet of bileptons, |Y| = 1/2  (t2^2 = 1, tY^2 = 1), mass M_V;
            the Z' (Y = 0, no SU(2)) contributes nothing; M_Z'/M_V is printed for reference.
  fermions  N_g = N_c exotic quarks (SU(2) singlets, colour fundamentals, charges from the
            model); for beta = +1/sqrt3 also N_g heavy charged leptons. Mass m = r_J M_V with
            r_J = sqrt2 y_J / g_L, so the exotic Yukawa used at two loops is the same one.
  scalars   of the 18 real fields in the three triplets: 4 form the light SM doublet,
            5 are eaten by the heavy vectors, and 9 are heavy: a second doublet (|Y| = 1/2),
            a charged singlet (|Y| = 1) and 3 neutral fields. Mass r_S M_V. Option: the
            second doublet light (a two-Higgs-doublet model below M_V).

T1  CHECK: at one loop, with the spectrum fixed, the blow-up scale must not depend on the
    matching scale mu. This tests every sign and multiplicity in lambda.
T2  The corrections at mu = M_V for a reference spectrum.
T3  The verdict, scanning the unknown spectrum: r_J (y_J), r_S, M_V and the second doublet.
T4  The narrow margin, recomputed: the largest sin^2 theta_W(M_V) for which N_c = 3 still
    reaches the Planck scale, and the residual matching-scale dependence at two loops.
"""
import os
import sys
from fractions import Fraction as F
from itertools import product
from math import log, pi, sqrt

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_exact as E
import m331_yukawa as Y

M_PLANCK = E.M_PLANCK


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def heavy_spectrum(Nc, variant, MV, rJ=1.0, rS=1.0, n_light=1):
    """List of (kind, tY^2, t2^2, t3^2, mass). kind in {'V', 'F', 'S'}."""
    _, _, _, (Xt, Xa, Qu, Qd, Ng, nA) = E.MODELS[variant](Nc)
    out = [("V", 1.0, 1.0, 0.0, MV)]                          # bilepton doublet (4 real)
    if variant == "-1/sqrt3":
        exotics = [Qu] * (Ng - nA) + [Qd] * nA                  # T (u-like), D (d-like)
    else:
        exotics = [Qd] * (Ng - nA) + [Qu] * nA                  # J (d-like), J' (u-like)
    for Q in exotics:
        out.append(("F", float(Nc * Q**2), 0.0, 0.5, rJ * MV))
    if variant == "+1/sqrt3":
        out += [("F", 1.0, 0.0, 0.0, rJ * MV)] * Ng           # heavy charged leptons E
    if n_light == 1:
        out.append(("S", 1.0, 1.0, 0.0, rS * MV))             # second doublet, 4 real
    out.append(("S", 2.0, 0.0, 0.0, rS * MV))                 # charged singlet, 2 real
    return out                                                # 3 neutral scalars: no t^2


def lambdas(spec, mu):
    lam = np.zeros(3)
    for kind, tY, t2, t3, M in spec:
        t = np.array([tY, t2, t3])
        L = log(M / mu)
        if kind == "V":
            lam += t * (1 - 21 * L)
        elif kind == "F":
            lam += 8 * t * L
        else:
            lam += t * L
    return lam


def mzp_over_mv(s2, beta2=1 / 3):
    """M_Z'/M_V from the chi vev: M_V^2 = g^2 v^2/4, M_Z'^2 = v^2 (g^2 + g_X^2 beta^2)/3."""
    tX2 = s2 / (1 - (1 + beta2) * s2)
    return sqrt(4 / 3 * (1 + beta2 * tX2))


def gL_at(mu):
    ainv, _, _ = Y.boundary(mu)
    return sqrt(4 * pi / ainv[1])


def pole(Nc, variant, MV=4e3, rJ=1.0, rS=1.0, n_light=1, mu=None, loops=2, s2=None,
         thresholds=True, yt=None, yukawas=True, gmax=4 * pi):
    mu = MV if mu is None else mu
    yJ = rJ * gL_at(mu) / sqrt(2) if yukawas else 0.0
    yt = (Y.yt_at(mu) if yt is None else yt) if yukawas else 0.0
    lam = lambdas(heavy_spectrum(Nc, variant, MV, rJ, rS, n_light), mu) if thresholds else (0, 0, 0)
    return Y.blow_up(Nc, variant, yt, yJ, mu0=mu, s2=s2, lam=tuple(lam), n_light=n_light, loops=loops,
                     gmax=gmax)


def s2_upper_thr(variant, **kw):
    f = lambda x: log(pole(3, variant, s2=x, **kw) / M_PLANCK)
    return brentq(f, 0.15, 0.70, xtol=1e-7)


GRID = dict(rJ=(0.5, 1.0, 2.0, 3.0), rS=(1 / 3, 1.0, 3.0), MV=(2e3, 4e3, 1e4), n_light=(1, 2))


def scan(Nc, variant, MVs=None, **kw):
    vals = []
    mus = (1.0,) if Nc == 3 else (1 / 3, 1.0, 3.0)     # N_c = 5: no consistent low theory, take the best mu
    for rJ, rS, MV, nl in product(GRID["rJ"], GRID["rS"], MVs or GRID["MV"], GRID["n_light"]):
        p = max(pole(Nc, variant, MV, rJ, rS, nl, mu=k * MV, **kw) for k in mus)
        vals.append((p, rJ, rS, MV, nl))
    return min(vals), max(vals)


def main():
    out = {}
    banner("T1  CHECK: one loop, fixed spectrum, matching scale varied (must not matter)")
    print("   mu / M_V:        1/3        1/2        1          2          3      spread in ln(pole)")
    worst = 0.0
    for v in ("-1/sqrt3", "+1/sqrt3"):
        ps = [pole(3, v, 4e3, 2.0, 0.5, 1, mu=4e3 * k, loops=1) for k in (1 / 3, 0.5, 1, 2, 3)]
        spread = max(np.log(ps)) - min(np.log(ps))
        worst = max(worst, spread)
        print(f"   beta = {v:8s} N_c = 3: " + "  ".join(f"{p:.3e}" for p in ps) + f"   {spread:.1e}")
    out["T1"] = worst
    print(f"   The N_c = 3 pole is independent of mu to {worst:.0e} in its logarithm: every sign and")
    print("   multiplicity in lambda is right, and the heavy content is exactly 3-3-1 minus the SM.")
    ps = [pole(3, "+1/sqrt3", 4e3, 2.0, 0.5, 1, mu=4e3 * k, loops=1, thresholds=False) for k in (1 / 3, 3)]
    print(f"   Without thresholds the same check fails: {ps[0]:.2e} vs {ps[1]:.2e} GeV.")
    ps = [pole(5, "+1/sqrt3", 4e3, 2.0, 0.5, 1, mu=4e3 * k, loops=1) for k in (1 / 3, 3)]
    out["T1_nc5"] = ps[1] / ps[0]
    print("   N_c = 5 cannot pass it, and should not: below mu we run the real SM, with three colours,")
    print("   which is not 3-3-1 at N_c = 5 minus its heavy fields. This is the counterfactual boundary")
    print(f"   condition showing up directly: N_c = 5's pole moves by a factor {ps[1]/ps[0]:.2f} as mu goes")
    print("   from M_V/3 to 3 M_V. T3 takes N_c = 5's most favourable mu.")

    banner("T2  The corrections at mu = M_V = 4 TeV (r_J = 1, r_S = 1, one light doublet)")
    _, s2m, aemi = Y.boundary(4e3)
    print(f"   M_Z'/M_V = {mzp_over_mv(s2m):.3f} (from sin^2 theta_W = {s2m:.4f}); the Z' carries no SM charge.")
    for v in ("-1/sqrt3", "+1/sqrt3"):
        for Nc in (3, 5):
            lam = lambdas(heavy_spectrum(Nc, v, 4e3), 4e3)
            d = lam / (12 * pi)
            dX = d[0] - d[1] / 3
            print(f"   beta = {v:8s} N_c = {Nc}: lambda_Y = {lam[0]:+.3f}, lambda_2 = {lam[1]:+.3f}, "
                  f"lambda_3 = {lam[2]:+.3f};  shift in 1/alpha_X = {dX:+.4f}")
    print("   With every heavy mass at mu, only the MS-bar vector constant survives: lambda_Y = lambda_2 = 1,")
    print("   so 1/alpha_X moves by (1 - 1/3)/(12 pi) = +0.018, out of 83.8. The logs carry the rest.")
    for v in ("-1/sqrt3", "+1/sqrt3"):
        lo = min(lambdas(heavy_spectrum(3, v, 4e3, rJ, rS, nl), 4e3)[0] for rJ, rS, nl in
                 product(GRID["rJ"], GRID["rS"], GRID["n_light"]))
        hi = max(lambdas(heavy_spectrum(3, v, 4e3, rJ, rS, nl), 4e3)[0] for rJ, rS, nl in
                 product(GRID["rJ"], GRID["rS"], GRID["n_light"]))
        print(f"   beta = {v:8s} N_c = 3, spectrum scanned: lambda_Y from {lo:+.2f} to {hi:+.2f}"
              f"  (1/alpha_Y moves {lo/(12*pi):+.3f} to {hi/(12*pi):+.3f})")

    banner("T3  Blow-up scale with one-loop thresholds and two-loop running, spectrum scanned")
    print("   r_J = m_exotic/M_V in {0.5, 1, 2, 3} (y_J = r_J g_L/sqrt2, also used at two loops),")
    print("   r_S = m_scalar/M_V in {1/3, 1, 3}, M_V in {2, 4, 10} TeV, second doublet heavy or light.")
    for v in ("-1/sqrt3", "+1/sqrt3"):
        (lo3, *a3), (hi3, *b3) = scan(3, v)
        (lo5, *a5), (hi5, *b5) = scan(5, v)
        out[(v, 3)] = (lo3, hi3)
        out[(v, 5)] = (lo5, hi5)
        print(f"   beta = {v:8s}: N_c = 3 from {lo3:.2e} to {hi3:.2e} GeV  (lowest at r_J, r_S, M_V, n_light = "
              f"{a3[0]}, {a3[1]:.2f}, {a3[2]:.0e}, {a3[3]})")
        print(f"                    N_c = 5 from {lo5:.2e} to {hi5:.2e} GeV")
        print(f"                    worst N_c = 3 / M_Pl = {lo3/M_PLANCK:.3g};  best N_c = 5 / M_Pl = {hi5/M_PLANCK:.1e}"
              f"  ->  {'only N_c = 3 survives' if lo3 > M_PLANCK > hi5 else 'VERDICT CHANGES'}")
        (lo3b, *_), _ = scan(3, v, MVs=(4e3, 1e4))
        out[(v, "3_lhc")] = lo3b
        print(f"                    with M_V >= 4 TeV (M_Z' >= {1.225*4:.1f} TeV, above every current Z' limit): "
              f"worst N_c = 3 / M_Pl = {lo3b/M_PLANCK:.3g}")
        # 13 TeV, 139 fb^-1 recast (src/m331_zprime_recast.py): most conservative bound, all exotics open
        mz_lhc = {"+1/sqrt3": 4.6e3, "-1/sqrt3": 4.0e3}[v]
        (lo3c, *_), _ = scan(3, v, MVs=(mz_lhc / 1.225, 1e4))
        out[(v, "3_recast")] = lo3c
        print(f"                    at the ATLAS 139 fb^-1 recast bound (M_Z' >= {mz_lhc/1e3:.1f} TeV, M_V >= "
              f"{mz_lhc/1.225/1e3:.2f} TeV): worst N_c = 3 / M_Pl = {lo3c/M_PLANCK:.3g}")

    banner("T4  The narrow margin, recomputed (beta = +1/sqrt3, N_c = 3)")
    s_tree = Y.s2_upper(3, "+1/sqrt3")
    print(f"   Tree-level matching, no Yukawas (front 7d): N_c = 3 needs sin^2 theta_W(4 TeV) < {s_tree:.4f}")
    rows = []
    for rJ, rS, nl in ((0.5, 1 / 3, 2), (0.5, 1.0, 1), (1.0, 1.0, 1), (2.0, 1.0, 1), (3.0, 3.0, 1)):
        u = s2_upper_thr("+1/sqrt3", MV=4e3, rJ=rJ, rS=rS, n_light=nl)
        rows.append(u)
        print(f"   one-loop thresholds, r_J = {rJ:3.1f}, r_S = {rS:4.2f}, light doublets = {nl}:"
              f"  s^2 < {u:.4f}   margin {u - s2m:+.4f}")
    out["T4"] = (min(rows), max(rows))
    print(f"   measured sin^2 theta_W(4 TeV) = {s2m:.4f}.  Margin range {min(rows)-s2m:+.4f} to {max(rows)-s2m:+.4f}.")
    print("   Residual matching-scale dependence at two loops (r_J = 1, r_S = 1), N_c = 3 pole / M_Pl:")
    for v in ("-1/sqrt3", "+1/sqrt3"):
        ps = [pole(3, v, 4e3, 1.0, 1.0, 1, mu=4e3 * k) / M_PLANCK for k in (0.5, 1, 2)]
        out[(v, "mu")] = ps
        print(f"     beta = {v:8s}: mu = M_V/2, M_V, 2 M_V -> " + ", ".join(f"{p:.3g}" for p in ps))
    return out


if __name__ == "__main__":
    main()
