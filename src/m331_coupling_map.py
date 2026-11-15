#!/usr/bin/env python3
"""
The 3-3-1 selection without the measured couplings: a map of coupling space
(NOTE_331.md, section 4a).

The selection runs every N_c from the electroweak couplings measured in our three-colour
world. That boundary condition is counterfactual for N_c other than 3. Here it is dropped.
The couplings at the 3-3-1 scale (4 TeV) are free:

    1/alpha_L = s^2/alpha_em,   1/alpha_X = (1 - 4 s^2/3)/alpha_em,   alpha_3,

with s^2 = sin^2 theta_W in (0, 3/4) (the range where alpha_X > 0) and 1/alpha_em from 20 to
400, uniform in s^2 and in log(1/alpha_em). For each point and each model the gauge couplings
are run at two loops (no Yukawas) and the model is kept if every coupling stays below the
criterion up to M_Pl.

P1  The region of each (N_c, N_g), as a fraction of the box, and whether it holds the
    measured point (s^2 = 0.2505, 1/alpha_em = 125.7).
P2  Nesting. Wherever any model with N_c odd and >= 3 is perturbative to M_Pl, N_c = N_g = 3
    is too. No choice of couplings selects 5, 7 or 9 instead of 3.
P3  The fraction of N_c = 3's region in which it is the only odd N_c >= 3 that survives.
P4  The same with alpha_3 halved and doubled, and with the criterion alpha = 1.
P5  A character map for each variant.

The box is a convention, so the fractions are descriptive; P2 does not depend on it.
"""
import os
import sys
from math import log, pi, sqrt

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_exact as E

MU = 4e3
S2_RANGE, AINV_RANGE = (0.0, 0.75), (20.0, 400.0)
MODELS = [(3, 3), (5, 5), (7, 7), (9, 9), (3, 6), (2, 4), (4, 8)]
ODD = [(3, 3), (5, 5), (7, 7), (9, 9), (3, 6)]


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def measured():
    """(s^2, 1/alpha_em, 1/alpha_3) at 4 TeV from the measured couplings (one-loop SM running)."""
    L0 = log(MU / E.MZ) / (2 * pi)
    aY, a2 = (1 - E.s2) * E.ainv - 41 / 6 * L0, E.s2 * E.ainv + 19 / 6 * L0
    from qcd_running import alpha_s_run
    return a2 / (aY + a2), aY + a2, 1 / alpha_s_run(MU)


def grid(n):
    """Cell centres: n values of s^2 and n of 1/alpha_em (log-spaced)."""
    s = S2_RANGE[0] + (np.arange(n) + 0.5) / n * (S2_RANGE[1] - S2_RANGE[0])
    a = np.exp(log(AINV_RANGE[0]) + (np.arange(n) + 0.5) / n * log(AINV_RANGE[1] / AINV_RANGE[0]))
    return s, a


def survives(Nc, Ng, variant, s2, ainv_em, ainv3, gmax=4 * pi):
    ainv0 = ((1 - 4 * s2 / 3) * ainv_em, s2 * ainv_em, ainv3)
    if min(ainv0) <= 0:
        return False
    p = E.run_two_loop(Nc, mu0=MU, model=E.MODELS[variant], gmax=gmax, Ng=Ng, ainv0=ainv0, rtol=1e-6)[0]
    return p is None or p > E.M_PLANCK


def region(variant, n=24, a3_scale=1.0, gmax=4 * pi, models=MODELS):
    """{(N_c, N_g): boolean n x n array [s^2 index, 1/alpha_em index]}."""
    s, a = grid(n)
    ainv3 = measured()[2] / a3_scale
    return {m: np.array([[survives(m[0], m[1], variant, x, y, ainv3, gmax) for y in a] for x in s])
            for m in models}


def summary(reg):
    """(fractions, nested, share of N_c = 3's region where it is the only odd N_c >= 3)."""
    frac = {m: float(r.mean()) for m, r in reg.items()}
    three = reg[(3, 3)]
    others = np.zeros_like(three)
    for m in ODD[1:]:
        if m in reg:
            others |= reg[m]
    nested = not bool((others & ~three).any())
    alone = float((three & ~others).sum() / max(three.sum(), 1))
    return frac, nested, alone


def draw(reg, n):
    s, a = grid(n)
    sm, am, _ = measured()
    i0, j0 = int(np.argmin(abs(s - sm))), int(np.argmin(abs(np.log(a / am))))
    rows = []
    for j in reversed(range(n)):
        line = ""
        for i in range(n):
            c = "."
            if reg[(3, 3)][i, j]:
                c = "3"
            if reg[(5, 5)][i, j]:
                c = "5"
            if reg[(7, 7)][i, j]:
                c = "7"
            if (i, j) == (i0, j0):
                c = "M"
            line += c
        rows.append(f"   {a[j]:6.1f} |{line}|")
    rows.append("          " + "-" * n)
    rows.append(f"   1/alpha_em ^   s^2 from {S2_RANGE[0]} to {S2_RANGE[1]} ->")
    return "\n".join(rows)


def main(n=24):
    sm, am, a3 = measured()
    banner("P1-P3  Regions of coupling space that are perturbative to M_Pl (two loops, g = 4 pi)")
    print(f"   Box: s^2 in {S2_RANGE}, 1/alpha_em in {AINV_RANGE} (log), {n} x {n} cells, alpha_3 measured.")
    print(f"   Measured point at 4 TeV: s^2 = {sm:.4f}, 1/alpha_em = {am:.1f}, 1/alpha_3 = {a3:.2f}")
    regs = {}
    for v in E.MODELS:
        reg = regs[v] = region(v, n)
        frac, nested, alone = summary(reg)
        print(f"   beta = {v}")
        for m in MODELS:
            here = survives(m[0], m[1], v, sm, am, a3)
            print(f"     (N_c, N_g) = {m}: {100 * frac[m]:5.1f}% of the box;  measured point "
                  f"{'inside' if here else 'outside'}")
        print(f"     nested (every point where 5, 7, 9 or (3, 6) survives, 3 survives): {nested}")
        print(f"     N_c = 3 is the only odd N_c >= 3 in {100 * alone:.0f}% of its own region")

    banner("P4  The same with alpha_3 halved and doubled, and with the criterion alpha = 1")
    m4 = n // 2
    for v in E.MODELS:
        for label, kw in (("alpha_3 x 1/2", dict(a3_scale=0.5)), ("alpha_3 x 2", dict(a3_scale=2.0)),
                          ("alpha = 1", dict(gmax=sqrt(4 * pi)))):
            frac, nested, alone = summary(region(v, m4, **kw))
            print(f"   beta = {v:8s} {label:14s} N_c = 3: {100 * frac[(3, 3)]:5.1f}%  N_c = 5: "
                  f"{100 * frac[(5, 5)]:5.1f}%  (2, 4): {100 * frac[(2, 4)]:5.1f}%  nested: {nested}  "
                  f"3 alone in {100 * alone:.0f}%")

    banner("P5  Maps: 3 = only N_c = 3 of the odd N_c;  5, 7 = that N_c survives too (so does 3);")
    print("   . = none;  M = the cell holding the measured point (the point itself is in region 3")
    print("   for both variants, P1; for beta = +1/sqrt3 it sits near the edge of its cell's region)")
    for v in E.MODELS:
        print(f"   beta = {v}")
        print(draw(regs[v], n))
    return regs


if __name__ == "__main__":
    main()
