#!/usr/bin/env python3
"""
Unifying-equation search, front 7d: the three weak spots of 'N_c = N_g = 3' (NOTE_331.md).

Y1  Two-loop Yukawa terms (CHECK + computed). For a Yukawa y phi psi1 psi2 whose
    invariant contraction has n_terms unit entries, the two-loop gauge beta function
    gets  -g_i^3/(16 pi^2)^2 * y^2 * n_terms * [C2_i(psi1) + C2_i(psi2)] / d(G_i)
    (d = 1 and C2 = X^2 for U(1); Machacek-Vaughn, NPB 236, 221 (1984)). Calibrated on the
    Standard Model top quark: (17/10, 3/2, 2), GUT-normalised.
Y2  The verdict with Yukawas held CONSTANT up to the blow-up. Real Yukawas fall with
    energy (QCD), so a constant y overstates how much they slow the U(1)_X growth: the
    N_c = 5 exclusion is then conservative. Exotic-quark Yukawas y_J are unknown
    (m_J = y_J v_chi / sqrt2) and are scanned; the top Yukawa starts at its value at
    the 3-3-1 scale.
Y3  The counterfactual boundary condition, made explicit. All N_c are run from the
    couplings measured at the 3-3-1 scale. In 3-3-1, 1/alpha_X = (1 - 4 s^2/3)/alpha
    (s^2 = sin^2 theta_W), so the selection is a statement about one measured number.
    We find the window of s^2(mu_331) inside which N_c = 3 survives and N_c = 5 does
    not, and where the measured value sits in it.
Y4  The narrow beta = +1/sqrt3 margin, with Y1-Y3 included.
"""
import os
import sys
from fractions import Fraction as F
from math import log, pi, sqrt

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_exact as E

MZ, MT_POLE = 91.1880, 172.57
M_PLANCK = E.M_PLANCK
MU331 = 4e3


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def yukawa_coeff(groups, psi1, psi2, n_terms):
    """psi = (dims tuple, U(1) charge). Returns the per-y^2 coefficient for each group."""
    out = []
    for i, g in enumerate(groups):
        dG = 1 if g.N is None else g.N**2 - 1
        s = 0
        for dims, q in (psi1, psi2):
            s += q**2 if g.N is None else g.C2(dims[i])
        out.append(F(n_terms) * s / dG)
    return out


def sm_top_check():
    gs = [E.Group("Y"), E.Group("SU2", 2), E.Group("SU3", 3)]
    c = yukawa_coeff(gs, ((None, 2, 3), F(1, 6)), ((None, 1, 3), F(-2, 3)), 2 * 3)
    return [c[0] * F(3, 5), c[1], c[2]]


def yukawas_331(Nc, variant):
    """Coefficient vectors (top, one exotic quark) for 3-3-1 at colour number N_c.
    Top: the up quark of a triplet generation. Exotics: one per generation, each
    coupling its quark (anti-)triplet to its exotic singlet; contraction 3 x N_c."""
    gs, ferm, scal, (Xt, Xa, Qu, Qd, Ng, nA) = E.MODELS[variant](Nc)
    nt = 3 * Nc
    top = yukawa_coeff(gs, ((None, 3, Nc), Xt), ((None, 1, Nc), -Qu), nt)
    if variant == "-1/sqrt3":       # triplet exotic T (charge Q_u), anti-triplet exotic D (Q_d)
        ex_t = yukawa_coeff(gs, ((None, 3, Nc), Xt), ((None, 1, Nc), -Qu), nt)
        ex_a = yukawa_coeff(gs, ((None, 3, Nc), Xa), ((None, 1, Nc), -Qd), nt)
    else:                           # triplet exotic J (d-like), anti-triplet exotic J' (u-like)
        ex_t = yukawa_coeff(gs, ((None, 3, Nc), Xt), ((None, 1, Nc), -Qd), nt)
        ex_a = yukawa_coeff(gs, ((None, 3, Nc), Xa), ((None, 1, Nc), -Qu), nt)
    exotic = [(Ng - nA) * x + nA * y for x, y in zip(ex_t, ex_a)]   # all N_g exotics, equal y_J
    if variant == "+1/sqrt3":       # heavy charged leptons E, one per generation
        lep = yukawa_coeff(gs, ((None, 3, 1), F(-2, 3)), ((None, 1, 1), F(1)), 3)
        exotic = [x + Ng * l for x, l in zip(exotic, lep)]
    return np.array([float(x) for x in top]), np.array([float(x) for x in exotic])


def yt_at(mu, loops=1):
    """SM top Yukawa run from m_t to mu (one loop, with gauge couplings; MSbar y_t(m_t) from
    the pole mass with the one-loop QCD conversion). Inputs: m_t = 172.57 GeV, alpha_s(M_Z) =
    0.1180 (PDG 2024, checked)."""
    from qcd_running import alpha_s_run
    v = 246.22
    as_mt = alpha_s_run(MT_POLE)
    mt_ms = MT_POLE * (1 - 4 * as_mt / (3 * pi))
    y0 = sqrt(2) * mt_ms / v
    ainv, s2 = E.ainv, E.s2

    def gauge(t_mu):
        L = log(t_mu / MZ) / (2 * pi)
        a1 = 1 / ((1 - s2) * ainv * 3 / 5 - 41 / 10 * L)
        a2 = 1 / (s2 * ainv + 19 / 6 * L)
        return a1, a2, alpha_s_run(t_mu)

    def rhs(t, y):
        a1, a2, a3 = gauge(MT_POLE * np.exp(t))
        g1s, g2s, g3s = 4 * pi * a1, 4 * pi * a2, 4 * pi * a3
        return y / (16 * pi**2) * (4.5 * y**2 - 17 / 20 * g1s - 9 / 4 * g2s - 8 * g3s)

    sol = solve_ivp(rhs, [0, log(mu / MT_POLE)], [y0], rtol=1e-10)
    return float(sol.y[0, -1])


def boundary(mu0, s2_override=None, aem_inv_override=None, lam=(0.0, 0.0, 0.0), n_light=1):
    """Couplings (1/alpha_X, 1/alpha_L, 1/alpha_3) at the 3-3-1 scale. With s2_override,
    keep alpha_em(mu0) and alpha_s fixed and impose sin^2 theta_W(mu0) = s2_override.
    lam = (lambda_Y, lambda_2, lambda_3): one-loop threshold corrections at mu0,
    1/alpha_high = 1/alpha_low + lambda / (12 pi)  (src/m331_threshold.py).
    n_light: number of Higgs doublets below mu0 (each adds 1/6 to b_Y and b_2)."""
    from qcd_running import alpha_s_run
    L0 = log(mu0 / MZ) / (2 * pi)
    extra = (n_light - 1) / 6
    aY_inv = (1 - E.s2) * E.ainv - (41 / 6 + extra) * L0
    a2_inv = E.s2 * E.ainv + (19 / 6 - extra) * L0
    a3_inv = 1 / alpha_s_run(mu0)
    aem_inv = aY_inv + a2_inv
    s2_mu = a2_inv / aem_inv
    if aem_inv_override is not None:
        aem_inv = aem_inv_override
        if s2_override is None:
            s2_override = s2_mu
    if s2_override is not None:
        a2_inv = s2_override * aem_inv
        aY_inv = aem_inv - a2_inv
        s2_mu = s2_override
    aY_inv += lam[0] / (12 * pi)
    a2_inv += lam[1] / (12 * pi)
    a3_inv += lam[2] / (12 * pi)
    aX_inv = aY_inv - a2_inv / 3                 # 1/g_Y^2 = 1/g_X^2 + beta^2/g_L^2, beta^2 = 1/3
    return np.array([aX_inv, a2_inv, a3_inv]), s2_mu, aem_inv


def blow_up(Nc, variant="-1/sqrt3", yt=0.0, yJ=0.0, mu0=MU331, gmax=4 * pi, s2=None, aem_inv=None,
            lam=(0.0, 0.0, 0.0), n_light=1, loops=2):
    gs, ferm, scal, _ = E.MODELS[variant](Nc)
    a, b = E.coefficients(gs, ferm, scal)
    a = np.array([float(x) for x in a]); b = np.array([[float(x) for x in r] for r in b])
    ct, cJ = yukawas_331(Nc, variant)
    yuk = ct * yt**2 + cJ * yJ**2
    ainv0, _, _ = boundary(mu0, s2, aem_inv, lam, n_light)
    if loops == 1:
        b, yuk = 0 * b, 0 * yuk
    if min(ainv0) <= 0:
        return mu0
    g0 = np.sqrt(4 * pi / ainv0)

    def rhs(t, g):
        return g**3 / (16 * pi**2) * (a + (b @ g**2 - yuk) / (16 * pi**2))

    def ev(t, g):
        return gmax - max(g)
    ev.terminal = True
    sol = solve_ivp(rhs, [0, log(1e45 / mu0)], g0, events=ev, rtol=1e-9, atol=1e-12, max_step=0.5)
    return mu0 * np.exp(sol.t_events[0][0]) if sol.t_events[0].size else 1e45


def yJ_to_rescue(Nc, variant, yt, mu0=MU331, gmax=4 * pi):
    """Constant exotic Yukawa that pushes N_c's blow-up to the Planck scale (None if > 6)."""
    f = lambda y: log(blow_up(Nc, variant, yt, y, mu0, gmax) / M_PLANCK)
    if f(0.0) > 0:
        return 0.0
    if f(6.0) < 0:
        return None
    return brentq(f, 0.0, 6.0, xtol=1e-6)


def best_over_s2(Nc, variant, yt=0.0, yJ=0.0, aem_inv=None):
    """Largest blow-up scale over every weak mixing angle at the 3-3-1 scale."""
    from scipy.optimize import minimize_scalar
    grid = np.linspace(0.01, 0.74, 74)
    vals = [blow_up(Nc, variant, yt, yJ, s2=x, aem_inv=aem_inv) for x in grid]
    i = int(np.argmax(vals))
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    r = minimize_scalar(lambda x: -log(blow_up(Nc, variant, yt, yJ, s2=x, aem_inv=aem_inv)),
                        bounds=(lo, hi), method="bounded", options={"xatol": 1e-6})
    return float(np.exp(-r.fun)), float(r.x)


def s2_upper(Nc, variant, yt=0.0, yJ=0.0):
    """Largest sin^2 theta_W(mu0) for which N_c still reaches M_Pl (alpha_em fixed)."""
    f = lambda x: log(blow_up(Nc, variant, yt, yJ, s2=x) / M_PLANCK)
    return brentq(f, 0.15, 0.70, xtol=1e-7)


def s2_band(Nc, variant, yt=0.0, yJ=0.0):
    """Range of sin^2 theta_W(mu0) in which N_c reaches M_Pl (None if empty)."""
    best, xb = best_over_s2(Nc, variant, yt, yJ)
    if best < M_PLANCK:
        return None
    f = lambda x: log(blow_up(Nc, variant, yt, yJ, s2=x) / M_PLANCK)
    return brentq(f, 0.005, xb, xtol=1e-7), brentq(f, xb, 0.74, xtol=1e-7)


def aem_inv_to_rescue(Nc, variant, yt=0.0, yJ=0.0):
    """Smallest 1/alpha_em(mu0) letting N_c reach M_Pl at the MEASURED weak angle."""
    _, s2m, _ = boundary(MU331)
    f = lambda ai: log(blow_up(Nc, variant, yt, yJ, s2=s2m, aem_inv=ai) / M_PLANCK)
    return brentq(f, 100.0, 2000.0, xtol=1e-4)


def main():
    banner("Y1  Two-loop Yukawa coefficients: CHECK on the Standard Model top quark")
    c = sm_top_check()
    print(f"   computed (GUT-normalised U(1), SU(2), SU(3)): {[str(x) for x in c]}   expected 17/10, 3/2, 2")
    print(f"   exact: {c == [F(17, 10), F(3, 2), F(2)]}")
    yt = yt_at(MU331)
    print(f"   SM top Yukawa run to the 3-3-1 scale (4 TeV, one loop): y_t = {yt:.3f}")
    for v in ("-1/sqrt3", "+1/sqrt3"):
        for Nc in (3, 5):
            ct, cJ = yukawas_331(Nc, v)
            print(f"   beta = {v:8s} N_c = {Nc}: U(1)_X coefficient per y_t^2 = {ct[0]:.3f}, "
                  f"per y_J^2 (all {Nc} exotics{' + heavy leptons' if v[0] == '+' else ''}) = {cJ[0]:.3f}")

    banner("Y2  Blow-up scale (GeV, g = 4 pi) with Yukawas held constant (overstates their effect)")
    print("   Planck = 1.2e19 GeV.  y_t at its 4-TeV value; exotic Yukawas y_J scanned.")
    res = {}
    for v in ("-1/sqrt3", "+1/sqrt3"):
        print(f"   beta = {v}")
        print("     y_J      N_c = 3        N_c = 5        N_c = 7")
        for yJ in (0.0, 0.5, 1.0, 1.5, 2.0):
            r = [blow_up(Nc, v, yt, yJ) for Nc in (3, 5, 7)]
            res[(v, yJ)] = r
            print(f"     {yJ:4.1f}     {r[0]:9.2e}      {r[1]:9.2e}      {r[2]:9.2e}")
        r0 = [blow_up(Nc, v) for Nc in (3, 5)]
        print(f"     (no Yukawas at all: N_c = 3 -> {r0[0]:.2e}, N_c = 5 -> {r0[1]:.2e}; front 7b/7c)")
        need = yJ_to_rescue(5, v, yt)
        print(f"     Constant exotic Yukawa needed to lift N_c = 5 to the Planck scale: "
              f"{'> 6' if need is None else f'{need:.2f}'}"
              f"  (sqrt(4 pi) = {sqrt(4*pi):.2f} is the edge of perturbativity)")
        res[(v, "need")] = need

    banner("Y3  The boundary condition: which measured inputs the selection depends on")
    bc, s2_meas, aem_inv = boundary(MU331)
    print(f"   At 4 TeV (SM running from M_Z): sin^2 theta_W = {s2_meas:.4f}, 1/alpha_em = {aem_inv:.2f},")
    print(f"   so 1/alpha_X = (1 - 4 s^2/3)/alpha_em = {bc[0]:.2f}.")
    print("   All N_c are run from these measured couplings: the selection is conditional on them.")
    print("   Which s^2(4 TeV) would let each N_c reach the Planck scale (alpha_em, alpha_s fixed)?")
    print("   (a) Vary sin^2 theta_W(4 TeV) freely, keeping alpha_em and alpha_s at their measured values:")
    for v in ("-1/sqrt3", "+1/sqrt3"):
        for label, (a, bJ) in (("no Yukawas", (0.0, 0.0)), ("y_t, y_J = 1", (yt, 1.0))):
            b5, s5 = best_over_s2(5, v, a, bJ)
            band = s2_band(5, v, a, bJ)
            u3 = s2_upper(3, v, a, bJ)
            res[(v, label)] = (b5, s5, band, u3)
            print(f"   beta = {v:8s} {label:12s}: N_c = 3 reaches Planck for every s^2 < {u3:.4f} "
                  f"(measured {s2_meas:.4f}, margin {u3 - s2_meas:+.4f})")
            if band is None:
                print(f"        N_c = 5 fails for every s^2 (at best {b5:.1e} GeV, at s^2 = {s5:.3f})")
            else:
                print(f"        N_c = 5 reaches Planck only for {band[0]:.4f} < s^2 < {band[1]:.4f}"
                      f" (at best {b5:.1e} GeV): {s2_meas/band[1]:.1f}x below the measured value")
    print("   Lowering s^2 relieves U(1)_X but makes SU(3)_L stronger, so N_c = 5 has at most a")
    print("   narrow band, far from the measured angle (beta = -1/sqrt3) or none at all (+1/sqrt3).")
    print("   (b) At the measured weak angle, what would rescue N_c = 5: a weaker electromagnetism.")
    for v in ("-1/sqrt3", "+1/sqrt3"):
        ai = aem_inv_to_rescue(5, v, yt, 1.0)
        res[(v, "aem")] = ai
        print(f"   beta = {v:8s}: N_c = 5 needs 1/alpha_em(4 TeV) > {ai:.1f} (y_t and y_J = 1);"
              f" ours is {aem_inv:.1f}: alpha_em {ai/aem_inv:.2f}x weaker")
    print("   Reading: the selection is conditional on the measured electroweak couplings at the TeV")
    print("   scale. It does not predict them. Given them, only N_c = 3 stays perturbative to the")
    print("   Planck scale. In the beta = -1/sqrt3 variant, a world whose weak angle at the TeV")
    print("   scale were about three times smaller than ours would also allow N_c = 5.")

    banner("Y4  The narrow beta = +1/sqrt3 margin, all effects included")
    print("   N_c = 3 blow-up / M_Pl, beta = +1/sqrt3:")
    print("     criterion       no Yukawas    y_t only    y_t + y_J = 1   (mu_331 = 2 / 4 / 30 TeV, y_t + y_J = 1)")
    for crit, gm in (("g = 4 pi", 4 * pi), ("alpha = 1", sqrt(4 * pi)), ("g = 1", 1.0)):
        r = [blow_up(3, "+1/sqrt3", y1, y2, gmax=gm) / M_PLANCK for y1, y2 in ((0, 0), (yt, 0), (yt, 1.0))]
        rs = [blow_up(3, "+1/sqrt3", yt, 1.0, mu0=m, gmax=gm) / M_PLANCK for m in (2e3, 4e3, 3e4)]
        res[("+", crit)] = r
        print(f"     {crit:12s}    {r[0]:8.2f}      {r[1]:8.2f}     {r[2]:8.2f}        "
              + " / ".join(f"{x:.2f}" for x in rs))
    print("   Yukawas raise the N_c = 3 pole (they only slow the U(1)_X growth), so the margin can only")
    print("   widen from the no-Yukawa value; with y_t alone the top Yukawa's real decrease with energy")
    print("   makes the true value lie between the first two columns.")
    return res


if __name__ == "__main__":
    main()
