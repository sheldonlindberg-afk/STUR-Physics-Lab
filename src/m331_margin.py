#!/usr/bin/env python3
"""
The narrow beta = +1/sqrt3 margin, tightened (NOTE_331.md, section 3e).

Section 3d gives the worst case for N_c = 3 at alpha = 1 (three loops) as 1.28 M_Pl. That
number is the minimum over a fixed grid (r_J >= 0.5, r_S >= 1/3, M_V >= 2 TeV), and the
minimum sits on the grid's corner. This module replaces the grid edges with physical
floors and puts an error budget on the result.

M1  The grid corner is not a bound. Below r_J = 0.5 the pole keeps falling: at M_V = 2 TeV
    it drops below M_Pl. The margin is set by how light the exotics may be, so it has to
    be stated against experimental mass floors.
M2  Split spectrum. The scan of section 3a ties the heavy charged leptons E to the exotic
    quarks (one r_J). Their LHC limits differ by a factor of about four, so here the
    masses m_J (exotic quarks), m_E (heavy leptons), m_S (heavy scalars) and M_V run
    independently, each Yukawa set by its own mass (y = sqrt2 m g_L / (2 M_V)). The pole
    rises with every fermion mass and falls with M_V at fixed fermion masses.
M3  The worst case over the allowed spectrum: M_V = 3.755-30 TeV (Z' >= 4.6 TeV, LHC recast,
    section 6), m_J >= 1.3 TeV, m_E >= 0.1 TeV, m_S >= 0.1 TeV. Result: N_c = 3 does not
    reach M_Pl at alpha = 1 when the heavy leptons are light.
    Floors (LIT, approximate): exotic quarks, ATLAS 139 fb^-1 vector-like-quark pair
    searches exclude 1.3-1.6 TeV depending on the decays; 1.3 TeV is the low end. Heavy
    leptons and scalars: LEP's ~0.1 TeV; LHC singlet vector-like lepton limits (0.3-0.4
    TeV for e, mu partners; weaker for tau) are not used, which is conservative.
M4  The condition that replaces the margin: the heavy-lepton mass m_E* above which N_c = 3
    reaches M_Pl at alpha = 1, as a function of M_V; and the criterion a light-lepton
    spectrum would need (outside the convergent region).
M5  Error budget on m_E*: measured inputs (PDG 1 sigma), matching scale
    mu = M_V/2 to 2 M_V, truncation (two- to three-loop shift as the size of the next
    order), and the Yukawa sector (the case without Yukawas is complete at three loops).
"""
import os
import sys
from math import log, pi, sqrt

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_exact as E
import m331_three_loop as L
import m331_threshold as T
import m331_yukawa as Y
import qcd_running as Q

M_PLANCK = E.M_PLANCK
VAR = "+1/sqrt3"
ALPHA1 = sqrt(4 * pi)                               # g_crit for alpha = 1
MV_LHC = 4.6e3 / 1.225                              # Z' >= 4.6 TeV (section 6), as in section 3a
FLOORS = dict(MV=MV_LHC, mJ=1.3e3, mE=0.1e3, mS=0.1e3, n_light=2)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def yukawa_vectors(Nc=3):
    """Two-loop Yukawa coefficient vectors (top, exotic quarks, heavy leptons), per y^2."""
    gs = E.MODELS[VAR](Nc)[0]
    ct, cJ = Y.yukawas_331(Nc, VAR)
    lep = np.array([float(x) for x in Y.yukawa_coeff(gs, ((None, 3, 1), E.F(-2, 3)), ((None, 1, 1), E.F(1)), 3)])
    Ng = Nc
    return ct, cJ - Ng * lep, Ng * lep


def spectrum(Nc, MV, mJ, mE, mS, n_light):
    """m331_threshold.heavy_spectrum with the exotic quarks and heavy leptons split."""
    out, mEs = [], list(np.broadcast_to(np.asarray(mE, float), (Nc,)))   # one m_E or one per E
    for kind, tY, t2, t3, M in T.heavy_spectrum(Nc, VAR, MV, 1.0, 1.0, n_light):
        if kind == "F":
            M = mJ if t3 > 0 else mEs.pop(0)         # quarks carry colour; leptons do not
        elif kind == "S":
            M = mS
        out.append((kind, tY, t2, t3, M))
    return out


def pole(MV=4e3, mJ=4e3, mE=4e3, mS=4e3, n_light=1, Nc=3, loops=3, gmax=ALPHA1, mu=None,
         yukawas=True, s2=None, grav=None, mu_max=1e45):
    mu = MV if mu is None else mu
    lam = T.lambdas(spectrum(Nc, MV, mJ, mE, mS, n_light), mu)
    if yukawas:
        gL = T.gL_at(mu)
        ct, cq, cl = yukawa_vectors(Nc)
        yJ = sqrt(2) * mJ * gL / (2 * MV)
        yE2 = float(np.mean((sqrt(2) * np.asarray(mE, float) * gL / (2 * MV)) ** 2))
        yuk = ct * Y.yt_at(mu) ** 2 + cq * yJ**2 + cl * yE2
    else:
        yuk = np.zeros(3)
    return L.blow_up(Nc, VAR, mu0=mu, gmax=gmax, s2=s2, lam=tuple(lam), n_light=n_light, loops=loops, yuk=yuk,
                     grav=grav, mu_max=mu_max)


def rel(**kw):
    return pole(**kw) / M_PLANCK


def grid_edge(MV=2e3):
    """M1: the section 3a parametrization (m_J = m_E = r_J M_V, m_S = r_S M_V), r_J below the grid."""
    return [(rJ, rel(MV=MV, mJ=rJ * MV, mE=rJ * MV, mS=MV / 3, n_light=2)) for rJ in (0.5, 0.4, 0.3)]


def sensitivity():
    """M2: d ln(pole) / d ln(mass) at the floor point (M_V = 3.755 TeV), by finite difference."""
    base = dict(FLOORS)
    p0 = log(pole(**base))
    out = {}
    for k in ("MV", "mJ", "mE", "mS"):
        up = dict(base, **{k: base[k] * 1.1})
        out[k] = (log(pole(**up)) - p0) / log(1.1)
    up = dict(base, n_light=1)
    out["n_light=1"] = log(pole(**up)) - p0
    return out


MV_RANGE = (MV_LHC, 6e3, 10e3, 20e3, 30e3)           # 3-3-1 scales up to 30 TeV, as in the README


def worst(loops=3, gmax=ALPHA1, yukawas=True, **floors):
    """M3: minimum over M_V in MV_RANGE and over a grid at and above the other floors."""
    f = dict(FLOORS, **floors)
    vals = []
    for MV in MV_RANGE:
        for kJ in (1, 1.5):
            for kE in (1, 3):
                for kS in (1, 3):
                    for nl in (1, 2):
                        p = pole(MV=MV, mJ=f["mJ"] * kJ, mE=f["mE"] * kE, mS=f["mS"] * kS,
                                 n_light=nl, loops=loops, gmax=gmax, yukawas=yukawas)
                        vals.append((p / M_PLANCK, (MV, kJ, kE, kS, nl)))
    return min(vals)


def mE_critical(MV=MV_LHC, mJ=FLOORS["mJ"], tied=False, gmax=ALPHA1, yukawas=True, loops=3):
    """M4: the heavy-lepton mass at which N_c = 3 reaches exactly M_Pl (other masses at
    their floors). tied = True sets m_J = m_E, the section 3a parametrization."""
    def f(m):
        kw = dict(FLOORS, MV=MV, mE=m, mJ=m if tied else mJ)
        return log(pole(**kw, gmax=gmax, yukawas=yukawas, loops=loops) / M_PLANCK)
    return brentq(f, 30.0, 3e4, xtol=0.5)


def g_needed(mE):
    """M4: the criterion g_crit needed for N_c = 3 to reach M_Pl at the floors with this m_E."""
    f = lambda gc: log(pole(**dict(FLOORS, mE=mE), gmax=gc) / M_PLANCK)
    return brentq(f, 2.0, 7.9, xtol=1e-4)


class _inputs:
    """Temporarily shift a measured input (sin^2 theta_W(M_Z), 1/alpha(M_Z), alpha_s(M_Z), m_t)."""
    def __init__(self, name, value):
        self.name, self.value = name, value

    def __enter__(self):
        n = self.name
        if n == "s2":
            self.old, E.s2 = E.s2, self.value
        elif n == "ainv":
            self.old, E.ainv = E.ainv, self.value
        elif n == "as":
            self.old = Q.alpha_s_run.__defaults__
            d = list(self.old); d[1] = self.value
            Q.alpha_s_run.__defaults__ = tuple(d)
        elif n == "mt":
            self.old, Y.MT_POLE = Y.MT_POLE, self.value

    def __exit__(self, *a):
        n = self.name
        if n == "s2":
            E.s2 = self.old
        elif n == "ainv":
            E.ainv = self.old
        elif n == "as":
            Q.alpha_s_run.__defaults__ = self.old
        elif n == "mt":
            Y.MT_POLE = self.old


# PDG 2024 central values and 1 sigma (LIT recalled; centrals as used throughout the repo)
INPUTS = {"s2": (0.23122, 0.00004), "ainv": (127.95, 0.01), "as": (0.1180, 0.0009), "mt": (172.57, 0.29)}


def error_budget():
    """M5: the uncertainty on the M4 threshold m_E* (M_V and m_J at their floors, alpha = 1,
    three loops). Each source shifts ln(pole) at m_E*; dividing by d ln(pole)/d ln(m_E)
    converts that into a shift of m_E*."""
    mE0 = mE_critical()
    pt = dict(FLOORS, mE=mE0)
    p0 = pole(**pt)
    slope = (log(pole(**dict(pt, mE=mE0 * 1.05))) - log(p0)) / log(1.05)
    out = {}
    for k, (c, s) in INPUTS.items():
        sh = []
        for v in (c - s, c + s):
            with _inputs(k, v):
                sh.append(abs(log(pole(**pt) / p0)))
        out[k] = max(sh) / slope
    out["mu"] = max(abs(log(pole(**pt, mu=k * pt["MV"]) / p0)) for k in (0.5, 2.0)) / slope
    out["truncation"] = abs(log(pole(**pt, loops=2) / p0)) / slope
    out["yukawas_off"] = mE_critical(yukawas=False) / mE0 - 1
    return mE0, slope, out


def main():
    banner("M1  The section 3a grid corner is not a bound (alpha = 1, three loops, M_V = 2 TeV)")
    for rJ, r in grid_edge():
        print(f"   r_J = {rJ:.1f} (m_J = m_E = {rJ * 2:.1f} TeV), r_S = 1/3, light 2nd doublet: pole = {r:.3f} M_Pl")
    print("   The 1.28 M_Pl of section 3d is the value at the grid's corner, not a minimum. The")
    print("   margin is set by the lightest allowed exotics, so it is stated against mass floors.")

    banner("M2  Which masses matter: d ln(pole)/d ln(mass) at the floors, M_V = 3.755 TeV")
    s = sensitivity()
    for k, lab in (("MV", "M_V (vectors)"), ("mJ", "m_J (exotic quarks)"), ("mE", "m_E (heavy leptons)"),
                   ("mS", "m_S (heavy scalars)")):
        print(f"   {lab:22s}: {s[k]:+.3f}")
    print(f"   second doublet heavy instead of light: ln(pole) shifts by {s['n_light=1']:+.3f}")
    print("   Heavier exotic fermions raise the pole; the scalars barely matter. A heavier M_V at")
    print("   fixed fermion masses lowers it: the light fermions then run longer below M_V.")

    banner("M3  Worst case over the allowed spectrum (beta = +1/sqrt3, N_c = 3, alpha = 1)")
    print(f"   floors: M_V >= {MV_LHC / 1e3:.3f} TeV (Z' >= 4.6 TeV), m_J >= 1.3 TeV, m_E >= 0.1 TeV,"
          f" m_S >= 0.1 TeV; M_V up to 30 TeV")
    for lab, kw in (("three loops, Yukawas", {}), ("three loops, no Yukawas", dict(yukawas=False)),
                    ("two loops, Yukawas", dict(loops=2))):
        r, where = worst(**kw)
        print(f"   {lab:24s}: {r:.3f} M_Pl   (at M_V = {where[0] / 1e3:.1f} TeV, floor multiples"
              f" m_J, m_E, m_S = {where[1]}, {where[2]}, {where[3]}, n_light = {where[4]})")
    print(f"   at M_V = {MV_LHC / 1e3:.3f} TeV, all other masses at their floors: {rel(**FLOORS):.3f} M_Pl")
    print("   With light heavy leptons, N_c = 3 does NOT reach M_Pl in this variant. Heavier M_V")
    print("   at fixed fermion masses makes it worse: the light fermions run longer below M_V.")

    banner("M4  The condition: how heavy the heavy leptons must be (alpha = 1, three loops)")
    for MV in (MV_LHC, 10e3, 30e3):
        a = mE_critical(MV=MV)
        b = mE_critical(MV=MV, tied=True)
        print(f"   M_V = {MV / 1e3:6.3f} TeV: N_c = 3 reaches M_Pl iff m_E >= {a / 1e3:.3f} TeV (m_J = 1.3 TeV);"
              f"  with m_J = m_E tied: m >= {b / 1e3:.3f} TeV")
    for mE in (100.0, 300.0):
        g = g_needed(mE)
        print(f"   m_E = {mE / 1e3:.1f} TeV at the floors needs g_crit = {g:.2f} (alpha = {g * g / (4 * pi):.2f}),"
              f" outside the convergent region (section 3d)")
    print(f"   N_c = 5 at the same floors: {rel(Nc=5, **FLOORS):.1e} M_Pl (still excluded)")

    banner("M5  Error budget on the threshold m_E* (M_V = 3.755 TeV, m_J = 1.3 TeV, alpha = 1, three loops)")
    mE0, slope, b = error_budget()
    print(f"   m_E* = {mE0:.0f} GeV;  d ln(pole)/d ln(m_E) there = {slope:.3f}")
    for k, lab in (("s2", "sin^2 theta_W(M_Z) +- 0.00004"), ("ainv", "1/alpha(M_Z) +- 0.01"),
                   ("as", "alpha_s(M_Z) +- 0.0009"), ("mt", "m_t +- 0.29 GeV"),
                   ("mu", "matching scale M_V/2 - 2 M_V"), ("truncation", "next order (2 -> 3 loop shift)")):
        print(f"   {lab:34s}: {100 * b[k]:5.2f}% of m_E*")
    quad = sqrt(sum(b[k] ** 2 for k in ("s2", "ainv", "as", "mt", "mu", "truncation")))
    print(f"   combined in quadrature: {100 * quad:.1f}%  ->  m_E* = {mE0:.0f} +- {mE0 * quad:.0f} GeV")
    print(f"   Yukawas off (complete at three loops): m_E* {100 * b['yukawas_off']:+.1f}%"
          f"  ->  {mE0 * (1 + b['yukawas_off']):.0f} GeV")


if __name__ == "__main__":
    main()
