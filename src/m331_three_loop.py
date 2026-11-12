#!/usr/bin/env python3
"""
Three-loop gauge running for the 3-3-1 selection (NOTE_331.md, section 3d).

The selection runs the gauge couplings at two loops. The tightest case is beta = +1/sqrt3,
where N_c = 3 reaches the Planck scale with a factor of 1.6-2.2 to spare in the pole
scale. This module adds the three-loop gauge beta functions.

Source (LIT): C. Poole and A. E. Thomsen, JHEP 09 (2019) 055, arXiv:1906.04625: the general
three-loop gauge beta function in MS-bar, eq. (A.9), coefficients eqs. (A.14)-(A.16).
Only the gauge and matter terms g1-g16 are used; the Yukawa and quartic terms g17-g33
are not (see below). With one U(1) there is no kinetic mixing, so every tensor structure
reduces to per-group invariants of each irreducible multiplet (Dynkin index, Casimirs,
adjoint Casimir). Fermion traces include the conjugate fields and complex scalars count
as two real ones, as in that paper.

Validation (CHECK, exact rational arithmetic):
  V1  The two-loop terms of the same code reproduce m331_exact.coefficients exactly, for
      the Standard Model and both 3-3-1 variants.
  V2  The three-loop terms reproduce the Standard Model three-loop gauge beta functions of
      Mihaila, Salomon and Steinhauser, PRL 108 (2012) 151602, arXiv:1201.5868 (all gauge
      terms, n_G = 1-4, random couplings; top Yukawa and quartic set to zero), exactly.

Results:
  C1  Convergence. The U(1)_X beta function term by term along a typical trajectory: the
      three-loop term reaches the size of the two-loop one at g_X ~ sqrt(4 pi)
      (alpha_X = 1), and at g = 4 pi it is about 25 times the one-loop term.
  C2  So the g = 4 pi criterion lies outside the convergent region: the two-loop
      truncation blows up there and the three-loop truncation develops a spurious fixed
      point instead. Numbers read off at g = 4 pi are not stable under higher orders.
  C3  Controlled criteria (g_crit = 1.5 to sqrt(4 pi)): the scale where the largest
      coupling reaches g_crit, at two and three loops, both variants, N_c = 3 and 5.
      Three loops move it by 0.5-6%, upward.
  C4  beta = +1/sqrt3, N_c = 3, the worst case over the threshold scan of NOTE_331 3a, as a
      function of g_crit; and the smallest g_crit for which it reaches M_Pl.
  C5  The largest sin^2 theta_W(M_V) for which N_c = 3 reaches M_Pl, at alpha = 1 and g = 3.

Not included: three-loop Yukawa and quartic terms (g17-g33). The case without Yukawas,
which the note uses as its conservative lower bound (section 3b), contains no Yukawa
terms at any order and is complete at three loops in the gauge and matter sector.
"""
import os
import sys
from fractions import Fraction as F
from itertools import product
from math import log, pi, sqrt

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_exact as E
import m331_threshold as T
import m331_yukawa as Y

M_PLANCK = E.M_PLANCK

# Poole-Thomsen coefficients, MS-bar (A.15), (A.16): gauge and matter terms only
G2C = {1: F(2), 2: F(4), 3: F(-68, 3), 4: F(10, 3), 5: F(2, 3)}
G3C = {1: F(-1), 2: F(29, 2), 3: F(133, 18), 4: F(679, 36), 5: F(-11, 18), 6: F(-25, 18),
       7: F(-23, 36), 8: F(-49, 36), 9: F(4), 10: F(25, 2), 11: F(-2857, 27), 12: F(-79, 108),
       13: F(1, 54), 14: F(1415, 54), 15: F(545, 108), 16: F(-29, 54)}


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def _setup(groups, fermions, scalars, g):
    n = len(groups)

    def S(i, m, dims, q):
        gr, other = groups[i], 1
        for j, d in enumerate(dims):
            if j != i and d is not None:
                other *= d
        return m * other * (q**2 if gr.N is None else gr.T(dims[i]))

    def C(j, dims, q):
        gr = groups[j]
        return q**2 if gr.N is None else gr.C2(dims[j], q)

    CA = [groups[i].CA() if groups[i].N is not None else 0 for i in range(n)]
    S2F = [2 * sum(S(i, *x) for x in fermions) for i in range(n)]
    S2S = [2 * sum(S(i, *x) for x in scalars) for i in range(n)]
    C2F = lambda d, q: sum(g[j] * C(j, d, q) for j in range(n))
    X = {"G": CA, "F": S2F, "S": S2S}
    C2X = lambda d, q, k: sum(g[j] ** 2 * X[k][j] * C(j, d, q) for j in range(n))
    return S, CA, S2F, S2S, C2F, C2X


def B2(groups, fermions, scalars, g):
    """Two-loop: dg_i^2/dt = g_i^4 B2_i / (16 pi^2)^2, g = squared couplings."""
    S, CA, S2F, S2S, C2F, C2X = _setup(groups, fermions, scalars, g)
    out = []
    for i in range(len(groups)):
        f = 2 * sum(S(i, m, d, q) * C2F(d, q) for m, d, q in fermions)
        s = 2 * sum(S(i, m, d, q) * C2F(d, q) for m, d, q in scalars)
        out.append(G2C[1] * f + G2C[2] * s + g[i] * CA[i] * (G2C[3] * CA[i] + G2C[4] * S2F[i] + G2C[5] * S2S[i]))
    return out


def B3(groups, fermions, scalars, g):
    """Three-loop gauge and matter terms: dg_i^2/dt = g_i^4 B3_i / (16 pi^2)^3."""
    S, CA, S2F, S2S, C2F, C2X = _setup(groups, fermions, scalars, g)
    n = len(groups)
    S2FCF = [2 * sum(S(j, m, d, q) * C2F(d, q) for m, d, q in fermions) for j in range(n)]
    S2SCS = [2 * sum(S(j, m, d, q) * C2F(d, q) for m, d, q in scalars) for j in range(n)]
    out = []
    for i in range(n):
        tF = lambda fn: 2 * sum(S(i, m, d, q) * fn(d, q) for m, d, q in fermions)
        tS = lambda fn: 2 * sum(S(i, m, d, q) * fn(d, q) for m, d, q in scalars)
        c = G3C
        b = (c[1] * tF(lambda d, q: C2F(d, q) ** 2) + c[2] * tS(lambda d, q: C2F(d, q) ** 2)
             + c[3] * tF(lambda d, q: C2X(d, q, "G")) + c[4] * tS(lambda d, q: C2X(d, q, "G"))
             + c[5] * tF(lambda d, q: C2X(d, q, "F")) + c[6] * tS(lambda d, q: C2X(d, q, "F"))
             + c[7] * tF(lambda d, q: C2X(d, q, "S")) + c[8] * tS(lambda d, q: C2X(d, q, "S"))
             + c[9] * CA[i] * g[i] * S2FCF[i] + c[10] * CA[i] * g[i] * S2SCS[i]
             + g[i] ** 2 * (c[11] * CA[i] ** 3 + c[12] * CA[i] * S2F[i] ** 2 + c[13] * CA[i] * S2S[i] ** 2
                            + c[14] * CA[i] ** 2 * S2F[i] + c[15] * CA[i] ** 2 * S2S[i]
                            + c[16] * CA[i] * S2F[i] * S2S[i]))
        out.append(b)
    return out


# --------------------------------------------------------------------------- validation
def _sm(nG):
    gs = [E.Group("Y"), E.Group("SU2", 2), E.Group("SU3", 3)]
    ferm = []
    for _ in range(nG):
        ferm += [(1, (None, 2, 3), F(1, 6)), (1, (None, 1, 3), F(-2, 3)), (1, (None, 1, 3), F(1, 3)),
                 (1, (None, 2, 1), F(-1, 2)), (1, (None, 1, 1), F(1))]
    return gs, ferm, [(1, (None, 2, 1), F(1, 2))]


def check_two_loop():
    """V1: max |B2 - 2 sum_j b_ij g_j| over models and random couplings (exact)."""
    import random
    rng = random.Random(1)
    cases = [_sm(3)] + [E.MODELS[v](3)[:3] for v in ("-1/sqrt3", "+1/sqrt3")] + [E.MODELS[v](5)[:3] for v in ("-1/sqrt3", "+1/sqrt3")]
    worst = F(0)
    for gs, ferm, scal in cases:
        a, b = E.coefficients(gs, ferm, scal)
        for _ in range(4):
            g = [F(rng.randint(1, 30), 17) for _ in range(3)]
            mine = B2(gs, ferm, scal, g)
            worst = max(worst, max(abs(mine[i] - 2 * sum(b[i][j] * g[j] for j in range(3))) for i in range(3)))
    return worst


def _mss(i, x, n):
    """Mihaila-Salomon-Steinhauser three-loop gauge terms, x_j = alpha_j/pi (GUT-normalized
    alpha_1), alpha_t = lambda = 0; coefficient of (alpha_i/pi)^2 in mu^2 d(alpha_i/pi)/dmu^2."""
    x1, x2, x3 = x
    if i == 0:
        return (x1**2 * (F(489, 512000) - F(29, 2400) * n - F(209, 8640) * n * n) + x1 * x2 * (F(783, 51200) - F(7, 6400) * n)
                - x1 * x3 * F(137, 14400) * n + x2**2 * (F(3401, 20480) + F(83, 1920) * n - F(11, 960) * n * n)
                - x2 * x3 * F(1, 320) * n + x3**2 * (F(275, 576) * n - F(121, 2160) * n * n))
    if i == 1:
        return (x1**2 * (F(163, 102400) - F(7, 960) * n - F(11, 2880) * n * n) + x1 * x2 * (F(561, 10240) + F(13, 1280) * n)
                - x1 * x3 * F(1, 960) * n + x2**2 * (F(-667111, 110592) + F(1603, 432) * n - F(415, 1728) * n * n)
                + x2 * x3 * F(13, 64) * n + x3**2 * (F(125, 192) * n - F(11, 144) * n * n))
    return (x1**2 * (-F(13, 7680) * n - F(121, 17280) * n * n) - x1 * x2 * F(1, 2560) * n + x1 * x3 * F(77, 2880) * n
            + x2**2 * (F(241, 1536) * n - F(11, 384) * n * n) + x2 * x3 * F(7, 64) * n
            + x3**2 * (F(-2857, 128) + F(5033, 576) * n - F(325, 864) * n * n))


def check_three_loop_sm():
    """V2: max |B3 - 128 P_MSS| (exact), in units where dg_i^2/dt = g_i^4 B/(16 pi^2)^3.
    (mu^2 d(a/pi)/dmu^2 = (a/pi)^2 P with x = g^2/4pi^2 gives B = 128 P(g^2).)"""
    import random
    rng = random.Random(2)
    worst = F(0)
    for nG in (1, 2, 3, 4):
        gs, ferm, scal = _sm(nG)
        for _ in range(3):
            g = [F(rng.randint(1, 30), 11) for _ in range(3)]
            B = B3(gs, ferm, scal, g)
            gg = [F(5, 3) * g[0], g[1], g[2]]
            for i in range(3):
                mine = B[i] * (F(3, 5) if i == 0 else 1)
                worst = max(worst, abs(mine - 128 * _mss(i, gg, nG)))
    return worst


# --------------------------------------------------------------------------- running
def c3_tensor(Nc, variant):
    """B3_i(g) = sum_{j<=k} c[i][j][k] g_j g_k, extracted exactly from the quadratic form."""
    gs, ferm, scal, _ = E.MODELS[variant](Nc)
    e = [[F(int(a == b)) for b in range(3)] for a in range(3)]
    c = np.zeros((3, 3, 3))
    diag = [B3(gs, ferm, scal, e[j]) for j in range(3)]
    for i in range(3):
        for j in range(3):
            c[i][j][j] = float(diag[j][i])
            for k in range(j + 1, 3):
                both = B3(gs, ferm, scal, [e[j][m] + e[k][m] for m in range(3)])
                c[i][j][k] = float(both[i] - diag[j][i] - diag[k][i])
    return c


def blow_up(Nc, variant, yt=0.0, yJ=0.0, mu0=Y.MU331, gmax=4 * pi, s2=None, lam=(0.0, 0.0, 0.0),
            n_light=1, loops=3, yuk=None):
    """As m331_yukawa.blow_up (same boundary, two-loop and Yukawa terms), plus the
    three-loop gauge and matter terms when loops = 3. yuk: an explicit two-loop Yukawa
    vector, overriding the one built from yt and yJ (used by m331_margin.py)."""
    gs, ferm, scal, _ = E.MODELS[variant](Nc)
    a, b = E.coefficients(gs, ferm, scal)
    a = np.array([float(x) for x in a])
    b = np.array([[float(x) for x in r] for r in b])
    ct, cJ = Y.yukawas_331(Nc, variant)
    yuk = ct * yt**2 + cJ * yJ**2 if yuk is None else np.asarray(yuk, float)
    c3 = c3_tensor(Nc, variant) if loops == 3 else np.zeros((3, 3, 3))
    if loops == 1:
        b, yuk = 0 * b, 0 * yuk
    ainv0, _, _ = Y.boundary(mu0, s2, None, lam, n_light)
    if min(ainv0) <= 0:
        return mu0
    g0 = np.sqrt(4 * pi / ainv0)

    def rhs(t, g):
        g2 = g**2
        three = np.array([g2 @ c3[i] @ g2 for i in range(3)])     # sum_{j<=k} c_ijk g_j^2 g_k^2
        return g**3 / (16 * pi**2) * (a + (b @ g2 - yuk) / (16 * pi**2) + three / (2 * (16 * pi**2) ** 2))

    def ev(t, g):
        return gmax - max(g)
    ev.terminal = True
    sol = solve_ivp(rhs, [0, log(1e45 / mu0)], g0, events=ev, rtol=1e-9, atol=1e-12, max_step=0.5)
    return mu0 * np.exp(sol.t_events[0][0]) if sol.t_events[0].size else 1e45


def pole(Nc, variant, MV=4e3, rJ=1.0, rS=1.0, n_light=1, mu=None, loops=3, s2=None,
         thresholds=True, yukawas=True, gmax=4 * pi):
    """As m331_threshold.pole, with loops = 3 available."""
    mu = MV if mu is None else mu
    yJ = rJ * T.gL_at(mu) / sqrt(2) if yukawas else 0.0
    yt = Y.yt_at(mu) if yukawas else 0.0
    lam = T.lambdas(T.heavy_spectrum(Nc, variant, MV, rJ, rS, n_light), mu) if thresholds else (0, 0, 0)
    return blow_up(Nc, variant, yt, yJ, mu0=mu, s2=s2, lam=tuple(lam), n_light=n_light, loops=loops, gmax=gmax)


def worst_case(loops, gmax, yukawas=True, MVs=None):
    """N_c = 3, beta = +1/sqrt3: lowest scale over the threshold scan grid of NOTE_331 3a."""
    vals = []
    for rJ, rS, MV, nl in product(T.GRID["rJ"], T.GRID["rS"], MVs or T.GRID["MV"], T.GRID["n_light"]):
        vals.append((pole(3, "+1/sqrt3", MV, rJ, rS, nl, loops=loops, yukawas=yukawas, gmax=gmax), rJ, rS, MV, nl))
    return min(vals)


WORST = dict(MV=2000.0, rJ=0.5, rS=1 / 3, n_light=2)      # the scan's worst point at every g_crit (C4)


def g_crit_min(loops):
    """Smallest g_crit for which the worst-case spectrum still reaches M_Pl."""
    f = lambda gc: log(pole(3, "+1/sqrt3", loops=loops, gmax=gc, **WORST) / M_PLANCK)
    return brentq(f, 1.5, 6.0, xtol=1e-6)


def s2_upper(loops, gmax):
    f = lambda x: log(pole(3, "+1/sqrt3", s2=x, loops=loops, gmax=gmax) / M_PLANCK)
    return brentq(f, 0.15, 0.40, xtol=1e-7)


def convergence_table(gXs=(1.0, 2.0, 3.0, sqrt(4 * pi), 5.0, 4 * pi), g2s=(0.42, 0.5)):
    """C1: the one-, two- and three-loop terms of the U(1)_X beta function (beta = +1/sqrt3,
    N_c = 3) at g_L^2, g_3^2 = g2s, in units of g_X^3/(16 pi^2)."""
    gs, ferm, scal, _ = E.MODELS["+1/sqrt3"](3)
    a, b = E.coefficients(gs, ferm, scal)
    a = np.array([float(x) for x in a])
    b = np.array([[float(x) for x in r] for r in b])
    c3 = c3_tensor(3, "+1/sqrt3")
    rows = []
    for gX in gXs:
        g2 = np.array([gX**2, *g2s])
        rows.append((gX, a[0], (b @ g2)[0] / (16 * pi**2), (g2 @ c3[0] @ g2) / (2 * (16 * pi**2) ** 2)))
    return rows


def main():
    banner("V1-V2  Validation of the three-loop implementation (CHECK, exact arithmetic)")
    print(f"   V1 two-loop terms vs m331_exact.coefficients (SM, both variants, N_c = 3, 5): max |diff| = {check_two_loop()}")
    print(f"   V2 three-loop gauge terms vs Mihaila-Salomon-Steinhauser SM (n_G = 1-4): max |diff| = {check_three_loop_sm()}")

    banner("C1  Convergence of the U(1)_X beta function (beta = +1/sqrt3, N_c = 3)")
    for gX, one, two, three in convergence_table():
        print(f"   g_X = {gX:6.3f}: 1-loop {one:+8.3f}  2-loop {two:+8.3f}  3-loop {three:+9.3f}"
              f"   |3/2| = {abs(three / two):6.2f}   |3/1| = {abs(three / one):6.2f}")

    banner("C2  The g = 4 pi criterion is outside the convergent region")
    for variant, Nc in (("+1/sqrt3", 3), ("+1/sqrt3", 5)):
        p2 = pole(Nc, variant, loops=2, gmax=4 * pi)
        p3 = pole(Nc, variant, loops=3, gmax=4 * pi)
        print(f"   beta = {variant}, N_c = {Nc}: reaches g = 4 pi at 2 loops at {p2:.2e} GeV;"
              f" at 3 loops {'never (below 1e45 GeV)' if p3 >= 1e45 else f'{p3:.2e} GeV'}")
    print("   Even N_c = 5, excluded by eight orders of magnitude at any controlled criterion,")
    print("   never reaches 4 pi at three loops: the truncated series has a spurious fixed point.")

    banner("C3  Controlled criteria: scale where the largest coupling reaches g_crit (M_V = 4 TeV)")
    for variant in ("+1/sqrt3", "-1/sqrt3"):
        for Nc in (3, 5):
            cells = []
            for gc in (1.5, 2.0, 3.0, sqrt(4 * pi)):
                p2, p3 = pole(Nc, variant, loops=2, gmax=gc), pole(Nc, variant, loops=3, gmax=gc)
                cells.append(f"g={gc:.2f}: {p2 / M_PLANCK:.3g} -> {p3 / M_PLANCK:.3g}")
            print(f"   beta = {variant:8s} N_c = {Nc} (M_Pl units, 2 -> 3 loops): " + ";  ".join(cells))

    banner("C4  beta = +1/sqrt3, N_c = 3: worst case over the threshold scan vs the criterion")
    for gc in (2.0, 2.5, 3.0, sqrt(4 * pi)):
        w2, w3 = worst_case(2, gc), worst_case(3, gc)
        print(f"   g_crit = {gc:5.3f} (alpha = {gc**2 / (4 * pi):.2f}): 2-loop {w2[0] / M_PLANCK:.3f} M_Pl,"
              f" 3-loop {w3[0] / M_PLANCK:.3f} M_Pl   (worst at r_J={w3[1]}, r_S={w3[2]:.3g}, M_V={w3[3]:.0f}, n_light={w3[4]})")
    for lp in (2, 3):
        gm = g_crit_min(lp)
        print(f"   {lp}-loop: the worst case reaches M_Pl for g_crit >= {gm:.3f} (alpha >= {gm**2 / (4 * pi):.3f})")

    banner("C5  Largest sin^2 theta_W(M_V) for N_c = 3 to reach M_Pl (beta = +1/sqrt3, reference spectrum)")
    for gc, lab in ((sqrt(4 * pi), "alpha = 1"), (3.0, "g = 3   ")):
        print(f"   {lab}: 2-loop {s2_upper(2, gc):.4f}, 3-loop {s2_upper(3, gc):.4f}  (measured 0.250)")


if __name__ == "__main__":
    main()
