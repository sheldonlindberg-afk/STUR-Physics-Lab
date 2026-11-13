#!/usr/bin/env python3
"""
Gravity above the Planck scale and the 3-3-1 gauge couplings: the asymptotic-safety
estimate (NOTE_331.md asks every coupling to stay perturbative up to M_Pl; this asks what
happens above it if gravity is asymptotically safe).

The model (MODEL; LIT: Eichhorn and Versteegen, JHEP 01 (2018) 030; Eichhorn, Held and
Wetterich, PLB 782 (2018) 198). Above the Planck scale, gravity adds to every gauge beta
function the same term,
    beta_i -> beta_i - f_g(mu) g_i,      f_g(mu) = f* / (1 + G* M_Pl^2 / mu^2),
that is f_g = c G(mu) with the dimensionless Newton coupling G(mu) = G mu^2 below the
transition and its fixed point G* above it (the solution of beta_G = 2 G (1 - G/G*)).
f* > 0 and G* depend on the regulator and on the matter content; neither is computed
here. They are the two parameters of the model, and everything below is stated as a
function of them. The running below is the selection's own: three loops in the gauge and
matter sector, two-loop Yukawas, one-loop thresholds (src/m331_three_loop.py).

G1  Fixed points (CHECK, symbolic). At one loop with constant f, beta = b g^3/16pi^2 - f g.
    With b > 0 there is an interacting fixed point g*^2 = 16 pi^2 f / b; its slope is +2f, so
    it is IR-attractive (irrelevant): the coupling there is predicted. g = 0 has slope -f
    (UV-attractive, relevant). Exactly, u = 1/g^2 obeys u' = 2 f u - 2b/16pi^2, so
    u(t) = u* + (u0 - u*) e^(2ft): below g* the coupling goes to zero in the UV, above it it
    hits a Landau pole. For b < 0 only g = 0 exists. For N_c = 3: b_X = 14 (beta = +1/sqrt3)
    or 26/3 (-1/sqrt3) > 0, while SU(3)_L (-13/2) and colour (-5) are asymptotically free.
    So only g_X can be predicted, and UV completion asks g_X <= g_X* at the transition.
G2  The value of f* that puts the measured couplings exactly on the fixed-point trajectory
    (the separatrix: just above it every coupling stays finite to arbitrarily high scales;
    just below, U(1)_X hits a pole). Reference spectrum M_V = 4 TeV, alpha = 1 criterion:
        G* = 0.5 / 1 / 2:  beta = +1/sqrt3: f* = 0.247 / 0.295 / 0.362
                           beta = -1/sqrt3: f* = 0.0200 / 0.0203 / 0.0206
    With the same profile, the Standard Model's hypercharge (one loop, b_Y = 41/6) needs
    f* = 0.0097-0.0099: the benchmark the published estimates of f_g aim at. So beta =
    -1/sqrt3 needs about twice the SM's gravity contribution, beta = +1/sqrt3 about 30
    times, because its g_X is already close to its pole at M_Pl (2.86 M_Pl at alpha = 1).
    (CHECK, given the model)
G3  The selection is unchanged. f* can be at most b_X/4pi (1.11 and 0.69) for g_X* to stay
    below sqrt(4 pi), the selection's own criterion. At that maximum and G* = 0.5, the
    N_c = 5 and 7 poles do not move (to 1e-6): they sit at 3e8-1e15 GeV, where f_g(mu) is
    suppressed by (mu/M_Pl)^2 to below 1e-7. Gravity above M_Pl cannot rescue the
    excluded N_c. (CHECK, given the model)
G4  Light heavy leptons (NOTE_331.md section 3e): there N_c = 3 fails at 0.61 M_Pl, before
    the transition. Gravity rescues it only with f* >= 0.73 (G* = 0.5) or 1.08 (G* = 1),
    that is with g_X* at 81-98.5% of sqrt(4 pi), the edge of the criterion, and for no
    allowed f* at G* = 2. The heavy-lepton condition stands. (CHECK, given
    the model)
G5  What this does and does not give (FOLLOWS). One irrelevant coupling (g_X) and one
    unknown (f*) give no prediction from the gauge sector alone. The result is conditional:
    if an FRG computation for 3-3-1 matter fixes f* and G*, then G2 turns the measured
    sin^2 theta_W into a test. A value near the SM benchmark would favour beta = -1/sqrt3
    and disfavour beta = +1/sqrt3, which needs 30 times more. The Yukawa and quartic
    couplings, which gravity also shifts (and which make the SM Higgs-mass prediction of
    asymptotic safety), are held at their gauge-sector contributions here and not given
    their own gravity terms.
Labels: CHECK, MODEL, FOLLOWS, LIT.
"""
import os
import sys
from functools import lru_cache
from math import log, pi, sqrt

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_exact as E
import m331_margin as M
import m331_three_loop as L
import m331_yukawa as Y

M_PLANCK = E.M_PLANCK
VARIANTS = ("+1/sqrt3", "-1/sqrt3")
G_STARS = (0.5, 1.0, 2.0)
MU_MAX = 1e300               # ~650 e-folds above M_Pl: the separatrix is resolved to ~1e-6
MV_REF = 4e3                 # the reference spectrum of NOTE_331.md section 3d


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def f_profile(f_star, G_star=1.0):
    """f_g(mu) = f* G(mu)/G*, with G(mu) = G* / (1 + G* M_Pl^2 / mu^2)."""
    m2 = G_star * M_PLANCK**2
    return lambda mu: f_star / (1 + m2 / mu / mu)


# --------------------------------------------------------------------------- G1
def fixed_points():
    g, b, f, t, u0 = sp.symbols("g b f t u0", positive=True)
    beta = b * g**3 / (16 * sp.pi**2) - f * g
    fps = sp.solve(sp.Eq(beta, 0), g)
    gstar = [x for x in fps if x != 0][0]
    slope_star = sp.simplify(sp.diff(beta, g).subs(g, gstar))
    slope_zero = sp.diff(beta, g).subs(g, 0)
    # u = 1/g^2: u' = -2 beta / g^3
    u = sp.Function("u")
    ustar = b / (16 * sp.pi**2 * f)
    sol = ustar + (u0 - ustar) * sp.exp(2 * f * t)
    ode_ok = sp.simplify(sp.diff(sol, t) - (2 * f * sol - 2 * b / (16 * sp.pi**2))) == 0
    flow_ok = sp.simplify(-2 * beta / g**3 - (2 * f / g**2 - 2 * b / (16 * sp.pi**2))) == 0
    return sp.simplify(gstar**2), slope_star, slope_zero, ode_ok and flow_ok


def one_loop_b(Nc, variant):
    """(b_X, b_L, b_C) at one loop."""
    gs, ferm, scal, _ = E.MODELS[variant](Nc)
    return tuple(E.coefficients(gs, ferm, scal)[0])


# --------------------------------------------------------------------------- G2
def finite(f_star, G_star=1.0, Nc=3, variant="+1/sqrt3", floors=False):
    """True if every coupling stays below sqrt(4 pi) up to MU_MAX."""
    grav = f_profile(f_star, G_star)
    if floors:
        p = M.pole(**M.FLOORS, Nc=Nc, loops=3, gmax=M.ALPHA1, grav=grav, mu_max=MU_MAX)
    else:
        p = L.pole(Nc, variant, MV=MV_REF, gmax=M.ALPHA1, grav=grav, mu_max=MU_MAX)
    return p >= MU_MAX


@lru_cache(maxsize=None)
def f_separatrix(G_star=1.0, variant="+1/sqrt3", floors=False, hi=None, iters=30):
    """Smallest f* with every coupling finite; None if no f* <= hi works."""
    hi = f_max(3, variant) if hi is None else hi
    if not finite(hi, G_star, variant=variant, floors=floors):
        return None
    lo = 0.0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        lo, hi = (lo, mid) if finite(mid, G_star, variant=variant, floors=floors) else (mid, hi)
    return hi


def f_max(Nc, variant):
    """Largest f* with g_X* = sqrt(16 pi^2 f / b_X) <= sqrt(4 pi): f = b_X / 4 pi."""
    return float(one_loop_b(Nc, variant)[0]) / (4 * pi)


@lru_cache(maxsize=None)
def f_separatrix_sm(G_star=1.0, iters=40):
    """The same separatrix for the Standard Model's hypercharge g' at one loop, b = 41/6,
    from its measured value at M_Z."""
    aY_inv = (1 - E.s2) * E.ainv
    g0 = sqrt(4 * pi / aY_inv)
    b = 41 / 6

    def blows(f_star):
        grav = f_profile(f_star, G_star)
        rhs = lambda t, g: b * g**3 / (16 * pi**2) - grav(Y.MZ * np.exp(t)) * g
        ev = lambda t, g: M.ALPHA1 - g[0]
        ev.terminal = True
        sol = solve_ivp(rhs, [0, log(MU_MAX / Y.MZ)], [g0], events=ev, rtol=1e-10, atol=1e-13, max_step=0.5)
        return sol.t_events[0].size > 0

    lo, hi = 0.0, 0.1
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if blows(mid) else (lo, mid)
    return hi


# --------------------------------------------------------------------------- G3
def excluded_poles():
    """Poles of N_c = 5 and N_c = 7, without gravity and with the largest f* the criterion
    allows, at G* = 0.5 (the lowest transition scanned, so the strongest gravity there)."""
    out = {}
    for v in VARIANTS:
        for Nc in (5, 7):
            p0 = L.pole(Nc, v, MV=MV_REF, gmax=M.ALPHA1)
            pg = L.pole(Nc, v, MV=MV_REF, gmax=M.ALPHA1, grav=f_profile(f_max(3, v), 0.5))
            out[(v, Nc)] = (p0, pg)
    return out


# --------------------------------------------------------------------------- main
def main():
    banner("G1  Fixed points with the gravity term (CHECK, symbolic)")
    g2s, s_star, s_zero, ok = fixed_points()
    print(f"   beta = b g^3/16pi^2 - f g:  g*^2 = {g2s},  slope at g* = {s_star},  at 0 = {s_zero}")
    print(f"   u = 1/g^2 solves u' = 2 f u - 2b/16pi^2 with u = u* + (u0 - u*) e^(2ft): {ok}")
    for v in VARIANTS:
        bX, bL, bC = one_loop_b(3, v)
        print(f"   beta = {v}, N_c = 3: b_X = {bX}, b_L = {bL}, b_C = {bC}  ->  only g_X is predicted")

    banner("G2  f* that puts the measured couplings on the fixed-point trajectory (MODEL)")
    print(f"   {'G*':>5} " + " ".join(f"{v:>12}" for v in VARIANTS) + f" {'SM g_Y':>10}")
    for Gs in G_STARS:
        fs = [f_separatrix(Gs, v) for v in VARIANTS]
        print(f"   {Gs:5.1f} " + " ".join(f"{x:12.4f}" for x in fs) + f" {f_separatrix_sm(Gs):10.4f}")
    print(f"   ratio to the SM at G* = 1: +1/sqrt3 {f_separatrix(1.0, '+1/sqrt3') / f_separatrix_sm(1.0):.1f}, "
          f"-1/sqrt3 {f_separatrix(1.0, '-1/sqrt3') / f_separatrix_sm(1.0):.2f}")

    banner("G3  The excluded N_c stay excluded (largest allowed f*, G* = 0.5)")
    for v in VARIANTS:
        print(f"   beta = {v}: f*_max = b_X / 4pi = {f_max(3, v):.3f}")
    for (v, Nc), (p0, pg) in excluded_poles().items():
        print(f"   beta = {v}, N_c = {Nc}: pole {p0:.3e} GeV without gravity, {pg:.3e} GeV with "
              f"(f_g there ~ {f_max(3, v) * (p0 / M_PLANCK) ** 2 / 0.5:.0e})")

    banner("G4  Light heavy leptons (NOTE_331.md 3e: N_c = 3 fails at 0.61 M_Pl)")
    for Gs in G_STARS:
        fs = f_separatrix(Gs, "+1/sqrt3", floors=True)
        print(f"   G* = {Gs}: " + (f"rescued for f* >= {fs:.3f}" if fs else
                                   f"no f* <= {f_max(3, '+1/sqrt3'):.2f} rescues it"))


if __name__ == "__main__":
    main()
