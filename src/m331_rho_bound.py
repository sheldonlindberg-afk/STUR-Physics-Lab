#!/usr/bin/env python3
"""
The rho parameter and the 3-3-1 scale: what electroweak precision says about w, from the
tree-level Z-Z' mixing of rung 1 (src/m331_breaking.py B5), against the LHC Z' search.

The Standard Model's loop corrections, the +0.35% of B7, are not a test of 3-3-1: they are
known Standard Model physics. What is left after them is the global fit's rho_0, the
tree-level rho parameter beyond the Standard Model, with the Standard Model's loops (top,
Higgs) already taken out: rho_0 = 1.00039 +- 0.00019 (LIT: J. Erler, arXiv:1908.07346,
Frascati Phys. Ser. 69 (2019), from the global fit of that time; 2 sigma above 1). A newer
fit, with the 2022-2024 W-mass measurements, is not used here.

R1  rho - 1 = (v/w)^2 (sin^2 a - sin^2 a0)^2 exactly at leading order in v/w, with
    tan a = v2/v1 and x = g_X^2/g^2 = s2 / (1 - (1 + beta^2) s2):
        beta = +1/sqrt3:  sin^2 a0 = (3 - 2x) / (2(3 + x))
        beta = -1/sqrt3:  sin^2 a0 = (3 + 4x) / (2(3 + x))
    B5's coefficient, refactored: a perfect square in sin^2 a, so rho >= 1 and the
    mixing vanishes at one ratio of the two electroweak vacuum values. The two values add
    to 1: the variants are mirror images under v1 <-> v2 (in B0's labelling the vevs sit
    in different triplets). (CHECK, symbolic)
R2  Numbers. With s2 at M_Z (0.23122): sin^2 a0 = 0.350 (+1/sqrt3) and 0.650 (-1/sqrt3);
    with s2 at 4 TeV (0.2504): 0.333 and 0.667. (CHECK)
R3  The bound. rho_0 - 1 < 7.6e-4 (95% CL, two-sided) gives
        w > v |sin^2 a - sin^2 a0| / sqrt(7.6e-4),
    at most 5.8 TeV (at a = 0 or pi/2, whichever is farther from a0), and no bound at
    a = a0. The LHC Z' recast (NOTE_331.md section 6; Z' > 4.6 TeV for +1/sqrt3, > 4.0 TeV
    for -1/sqrt3, the low ends of its ranges) gives w > 11.9 and 10.3 TeV for every a. So
    rho is weaker than the LHC by at least a factor 1.8-2.0 in w, for every a. (CHECK; LIT rho_0)
R4  The 2 sigma excess. rho_0 - 1 = 3.9e-4 asks for w < 8.1 TeV at the most favourable
    a. At the LHC bound, the 3-3-1 tree-level mixing gives at most rho - 1 = 1.8e-4
    (+1/sqrt3) or 2.4e-4 (-1/sqrt3), 47% (62%) of the central excess: 3-3-1 at the LHC
    bound can reduce the tension to 1.1 sigma (0.8 sigma), not remove it. (CHECK)
R5  What is left out (FOLLOWS). One-loop 3-3-1 contributions to T (the bilepton doublet's
    mass splitting, of order M_W^2 in M^2) are suppressed by alpha/4pi next to the tree
    term and are not computed; S and U, and the Z' couplings to fermions at the Z pole, are
    not used. With a newer rho_0, the R3 and R4 numbers move but the comparison with the
    LHC does not reverse unless the rho_0 upper limit tightens by a factor of 3-4
    (w goes as its inverse square root).
Labels: CHECK, LIT, FOLLOWS.
"""
import math
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_breaking as B
import m331_threshold as T

RHO0, RHO0_ERR = 1.00039, 0.00019          # Erler, arXiv:1908.07346 (global fit, 2019)
Z95 = 1.96
ZP_BOUND = {"+1/sqrt3": 4.6e3, "-1/sqrt3": 4.0e3}   # GeV, LHC recast, NOTE_331.md section 6
MV_REF = 4e3                               # where sin^2 theta_W is taken for M_Z'/M_V
VARIANTS = ("+1/sqrt3", "-1/sqrt3")


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# --------------------------------------------------------------------------- R1
def coefficient(variant):
    """(rho - 1)/(v/w)^2 from B5, the closed form, and whether they agree."""
    t, a = sp.symbols("t a", positive=True)
    ser = B.rho_parameter(variant)
    c_b5 = sp.expand(ser - 1).coeff(t, 2)
    x = sp.symbols("x", positive=True)
    s0 = sin2_a0_symbolic(variant, x)
    closed = (sp.sin(a) ** 2 - s0) ** 2
    diff = sp.simplify(c_b5.subs(B.gX, sp.sqrt(x) * B.g) - closed)
    return c_b5, closed, diff == 0


def sin2_a0_symbolic(variant, x):
    c = 2 if variant == "+1/sqrt3" else -4
    return (3 - c * x) / (2 * (3 + x))


def x_of(s2):
    """g_X^2/g^2 = s2 / (1 - (1 + beta^2) s2), beta^2 = 1/3 (B4)."""
    return s2 / (1 - (4 / 3) * s2)


def s2_tev():
    """sin^2 theta_W at 4 TeV from the selection's own boundary (0.2504)."""
    import m331_yukawa as Y
    ainv = Y.boundary(MV_REF)[0]
    aY_inv = ainv[0] + ainv[1] / 3                 # 1/g_Y^2 = 1/g_X^2 + (1/3)/g_L^2
    return ainv[1] / (aY_inv + ainv[1])


def sin2_a0(variant, s2=B.S2_MZ):
    return float(sin2_a0_symbolic(variant, x_of(s2)))


# --------------------------------------------------------------------------- R3
def v_ew():
    return B.numbers()[0]


def rho_max():
    return RHO0 - 1 + Z95 * RHO0_ERR


def rho_min():
    return RHO0 - 1 - Z95 * RHO0_ERR


def w_bound_rho(variant, sin2a):
    """Lower bound on w from rho (95% CL) at a given sin^2 a."""
    return v_ew() * abs(sin2a - sin2_a0(variant)) / math.sqrt(rho_max())


def w_bound_rho_max(variant):
    s0 = sin2_a0(variant)
    return v_ew() * max(s0, 1 - s0) / math.sqrt(rho_max())


def w_from_zprime(variant):
    """w from the LHC Z' bound: M_V = M_Z' / (M_Z'/M_V) with sin^2 theta_W at 4 TeV (B4, as
    the 3-3-1 scans use it), and M_V = g w / 2 with g at M_V."""
    MV = ZP_BOUND[variant] / T.mzp_over_mv(s2_tev())
    return 2 * MV / T.gL_at(MV), MV


# --------------------------------------------------------------------------- R4
def rho_at_lhc(variant):
    """Largest tree-level rho - 1 allowed by the LHC bound (most favourable a)."""
    s0 = sin2_a0(variant)
    w, _ = w_from_zprime(variant)
    return (v_ew() / w) ** 2 * max(s0, 1 - s0) ** 2


def w_for_central(variant):
    s0 = sin2_a0(variant)
    return v_ew() * max(s0, 1 - s0) / math.sqrt(RHO0 - 1)


def tension_left(variant):
    return (RHO0 - 1 - rho_at_lhc(variant)) / RHO0_ERR


# --------------------------------------------------------------------------- main
def main():
    banner("R1  rho - 1 = (v/w)^2 (sin^2 a - sin^2 a0)^2  (CHECK, symbolic, from B5)")
    for v in VARIANTS:
        c, closed, ok = coefficient(v)
        print(f"   beta = {v}: sin^2 a0 = {sin2_a0_symbolic(v, sp.Symbol('x'))};  B5 coefficient = closed form: {ok}")
    print(f"   sum of the two sin^2 a0 = {sp.simplify(sum(sin2_a0_symbolic(v, sp.Symbol('x')) for v in VARIANTS))}")
    print(f"   vevs (X charge, component, vev) per triplet: "
          + "; ".join(f"{v}: {B.scalar_triplets(v)}" for v in VARIANTS))

    banner("R2  Where the mixing vanishes")
    for v in VARIANTS:
        print(f"   beta = {v}: sin^2 a0 = {sin2_a0(v):.3f} (s2 at M_Z), {sin2_a0(v, s2_tev()):.3f} (s2 at 4 TeV);"
              f"  tan a0 = {math.sqrt(sin2_a0(v) / (1 - sin2_a0(v))):.3f}")

    banner("R3  The bound on w (LIT: rho_0 = 1.00039 +- 0.00019, Erler 2019)")
    print(f"   v = {v_ew():.2f} GeV;  rho_0 - 1 < {rho_max():.2e} at 95% CL")
    for v in VARIANTS:
        wl, MV = w_from_zprime(v)
        print(f"   beta = {v}: rho: w > {w_bound_rho_max(v) / 1e3:.2f} TeV at most (a = 0 or pi/2), none at a = a0;"
              f"  LHC Z' > {ZP_BOUND[v] / 1e3:.1f} TeV: M_V > {MV / 1e3:.2f} TeV, w > {wl / 1e3:.2f} TeV;"
              f"  ratio {wl / w_bound_rho_max(v):.1f}")
    for v in VARIANTS:
        print(f"   beta = {v}, w bound from rho vs sin^2 a: " + ", ".join(
            f"{s:.2f}: {w_bound_rho(v, s) / 1e3:.2f}" for s in (0.0, 0.25, 0.5, 0.75, 1.0)) + " TeV")

    banner("R4  Can 3-3-1 explain the 2 sigma excess in rho_0?")
    for v in VARIANTS:
        print(f"   beta = {v}: central value needs w < {w_for_central(v) / 1e3:.1f} TeV; at the LHC bound "
              f"rho - 1 <= {rho_at_lhc(v):.2e} ({rho_at_lhc(v) / (RHO0 - 1):.0%} of the excess), "
              f"leaving {tension_left(v):.1f} sigma")


if __name__ == "__main__":
    main()
