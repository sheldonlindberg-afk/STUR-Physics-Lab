#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10o: the ultralight static-mass candidate (U0), and the
hypothesis ranking rebuilt from computed inputs only
================================================================================
Stage 10j found a beta != 0 candidate the earlier ranking did not list: an
R-phase with a small static mass m (H0 < m < H(z*)) that rolls coherently after
recombination (the standard ultralight axion-like birefringence mechanism).
It computed U0 only for c_g = 3 and 8 and only at high l. Stage 10i showed that
c_g = 6 with c_s = 0 is an allowed R-charge assignment (no QCD pinning).

Part 1 computes U0 for c_g = 6 (and c_g = 3 for comparison):
  * full nonlinear dynamics theta'' + 3H theta' + (m^2/3) sin 3 theta = 0
    (Stage 10j's equation and integrator, imported), |theta_i| <= pi/3;
  * exact CAMB EB transfers at low l (reionization) and high l (recombination);
  * for each m, theta_i solved so the EB-weighted high-l angle equals beta_now;
  * predictions: beta_reio/beta_rec, Delta beta, high-l shape;
  * f window: lower edges from ACT DR6 anisotropic birefringence (the field is
    light during inflation, m << H_I) and NGC 1275; upper edge from the
    ultralight-axion density bound Omega h^2 <= 0.006 (Hlozek et al. 2015,
    PRD 91, 103512, valid 1e-32 <= m <= 10^-25.5 eV), applied to the computed
    energy density today.
Part 2 assembles the ranking from the computed results of Stages 10g-10o.

Usage:  python genesis_v10o_u0_and_ranking.py
================================================================================
"""
import importlib.util
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


J = _load("g10j", "genesis_v10j_mass_dynamics.py")
G = J.G
ALPHA = J.ALPHA
BETA_NOW = 0.277
GYR_S = J.GYR_S
HBAR_GEV_S = J.HBAR_GEV_S
EV = 1e-9                                   # GeV
RHO_CRIT_H2 = 8.0992e-47                    # GeV^4
OMEGA_H2_MAX = 0.006                        # Hlozek et al. 2015, 95%
ULA_RANGE_EV = (1e-32, 10 ** -25.5)
H_I = 1.47e13                               # GeV, r = 0.0035
A_CB_MAX = 0.15e-4                          # rad^2 (convention confirmed in Stage 10n)
G_AGG_MAX = 6.3e-13                         # GeV^-1, NGC 1275
gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:56s} {detail:34s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 80 + "\n  " + s + "\n" + "=" * 80)


def part1():
    header("PART 1  U0: ultralight static-mass R-phase, c_g = 6 (c_s = 0 assignment, Stage 10i)")
    src = G.Sources(r=0.0035)
    bg = J.Bg(src.res)
    gate("background age matches Sources", abs(bg.t0 - src.t0) < 1e-3, f"{bg.t0:.4f} Gyr")
    ells = np.concatenate([np.arange(2, 11), [12, 15, 20, 30, 40], [50, 100, 200, 400, 800, 1200]])
    hi, lo = ells >= 50, ells <= 10
    ce0, _ = src.transfers(ells, {"c": lambda z, t: 0 * z})
    nl = G.litebird_noise(ells, 2.2, 30.0)
    wl = (2 * ells + 1) * ce0 ** 2 / ((ce0 + nl) * (src.cl_len[ells, 2] + nl))
    wlo = (2 * ells[lo] + 1) * ce0[lo]

    H0_gyr = bg.H0
    K3 = 3 * ALPHA / (2 * np.pi)
    mt0_grid = np.geomspace(1.0, 3e3, 14)
    thetas_i = np.linspace(0.1, 1.0, 7) * (np.pi / 3) * 0.999
    u_i = np.log(1e-7)
    hist, sols = {}, {}
    for mt0 in mt0_grid:
        m_gyr = mt0 / bg.t0
        for th_i in thetas_i:
            ue, th, thu = J.integrate(bg, u_i, bg.u0, [th_i, 0.0],
                                      lambda u: 3 * bg.Ht_of(u) - 1,
                                      lambda u, m=m_gyr: (m * np.exp(u)) ** 2, nonlin=True,
                                      n=int(min(4e5, 4e4 + 40 * mt0)))
            key = (float(mt0), float(th_i))
            sols[key] = (ue, th, thu)
            # built at the TRUE small angle for c_g = 3 (as Stage 10j); a per-unit-K history would
            # reach tens of degrees, where beta_eff (an arcsin) saturates and is not linear
            hist[key] = (lambda z, t, ue=ue, th=th: np.degrees(
                K3 * (th[-1] - np.interp(np.log(t), ue, th))))
    print(f"  {len(hist)} histories, exact transfers at {len(ells)} multipoles ...")
    cee, ceb = src.transfers(ells, hist)

    # c_g = 6 is obtained by scaling the exact c_g = 3 result by 2; verify on the history with the
    # LARGEST rotation (not a frozen one), where any non-linearity would show
    K6 = 6 * ALPHA / (2 * np.pi)
    probe = max(hist, key=lambda k: abs(np.sum(G.beta_eff(cee, ceb[k])[hi])))
    th_scaled = {"x2": (lambda z, t, f=hist[probe]: 2 * f(z, t))}
    ce_l, cb_l = src.transfers(ells[hi], th_scaled)
    b_exact = G.beta_eff(ce_l, cb_l["x2"])
    b_lin = 2 * G.beta_eff(cee, ceb[probe])[hi]
    gate("c_g = 6 = 2 x exact c_g = 3 (largest-rotation history)", np.max(np.abs(b_exact - b_lin)) < 1e-4,
         f"max dev {np.max(np.abs(b_exact - b_lin)):.1e} deg (max beta {np.max(np.abs(b_exact)):.3f})")

    def stats(key, K):
        b = (K / K3) * G.beta_eff(cee, ceb[key])
        bh = np.sum(wl[hi] * b[hi]) / np.sum(wl[hi])
        br = np.sum(wlo * b[lo]) / np.sum(wlo)
        return bh, br, b
    # gate: reproduce Stage 10j's c_g = 3 plateau (0.20-0.22 deg) at H0 < m < H(z*)
    plateau3 = max(abs(stats(k, K3)[0]) for k in hist if 3 <= k[0] <= 300)
    gate("c_g = 3 plateau reproduces Stage 10j (0.20-0.22 deg)", 0.19 <= plateau3 <= 0.23, f"{plateau3:.4f} deg")

    rows = []
    print(f"\n  {'m [eV]':>9s} {'m/H0':>7s} {'theta_i':>8s} {'beta_rec':>9s} {'beta_reio':>10s} {'ratio':>7s}"
          f" {'Delta beta':>10s} {'f_min':>9s} {'f_max':>9s} {'window':>7s}")
    for mt0 in mt0_grid:
        bh = np.array([stats((float(mt0), float(t)), K6)[0] for t in thetas_i])
        if np.max(bh) < BETA_NOW:
            continue
        j = np.argmax(bh >= BETA_NOW)
        if j == 0:
            th_sol = thetas_i[0] * BETA_NOW / bh[0]
            k_lo = k_hi = (float(mt0), float(thetas_i[0]))
            w = 0.0
        else:
            w = (BETA_NOW - bh[j - 1]) / (bh[j] - bh[j - 1])
            th_sol = thetas_i[j - 1] + w * (thetas_i[j] - thetas_i[j - 1])
            k_lo, k_hi = (float(mt0), float(thetas_i[j - 1])), (float(mt0), float(thetas_i[j]))
        s_lo, s_hi = stats(k_lo, K6), stats(k_hi, K6)
        br = (1 - w) * s_lo[1] + w * s_hi[1]
        bcurve = (1 - w) * s_lo[2] + w * s_hi[2]
        # energy today per unit f^2: theta_dot^2/2 + (m^2/9)(1 - cos 3 theta), from the bracketing solution
        ue, th, thu = sols[k_hi]
        m_gev = mt0 / bg.t0 / GYR_S * HBAR_GEV_S
        thdot = thu[-1] / bg.t0 / GYR_S * HBAR_GEV_S
        eps = (0.5 * thdot ** 2 + m_gev ** 2 * (1 - np.cos(3 * th[-1])) / 9) * (th_sol / thetas_i[min(j, len(thetas_i) - 1)]) ** 2
        m_ev = m_gev / EV
        in_ula = ULA_RANGE_EV[0] <= m_ev <= ULA_RANGE_EV[1]
        f_max = np.sqrt(OMEGA_H2_MAX * RHO_CRIT_H2 / eps) if in_ula else np.inf
        f_min = max(K6 * H_I / (2 * np.pi * np.sqrt(A_CB_MAX)), 6 * ALPHA / (np.pi * G_AGG_MAX))
        ok = f_max > f_min
        shape = np.max(np.abs(bcurve[hi] - BETA_NOW))
        rows.append(dict(m_ev=m_ev, mH0=mt0 / (H0_gyr * bg.t0), th=th_sol, br=br, ratio=br / BETA_NOW,
                         db=br - BETA_NOW, f_min=f_min, f_max=f_max, ok=ok, shape=shape, in_ula=in_ula))
        print(f"  {m_ev:9.2e} {mt0 / (H0_gyr * bg.t0):7.1f} {th_sol:8.3f} {BETA_NOW:8.3f}° {br:9.4f}°"
              f" {br / BETA_NOW:7.3f} {br - BETA_NOW:+9.4f}° {f_min:9.2e} "
              f"{(f'{f_max:9.2e}' if np.isfinite(f_max) else '  (no ULA)'):>9s} {'open' if ok else 'EMPTY':>7s}")
    viable = [r for r in rows if r['ok']]
    gate("U0 (c_g = 6) reaches beta_now for some m", len(rows) > 0, f"{len(rows)} masses")
    if viable:
        print(f"\n  viable (f window open): m = {min(r['m_ev'] for r in viable):.1e} - {max(r['m_ev'] for r in viable):.1e} eV;"
              f" ratio {min(r['ratio'] for r in viable):.3f} - {max(r['ratio'] for r in viable):.3f};"
              f" Delta beta {min(r['db'] for r in viable):+.3f} to {max(r['db'] for r in viable):+.3f} deg;"
              f" high-l |beta_eff - beta_now| <= {max(r['shape'] for r in viable):.4f} deg")
    return rows, viable


def part2(rows, viable):
    header("PART 2  Ranking from computed inputs only (Stages 10g-10o)")
    tab = [
        ("H0  STUR as written", "beta ~ 0 in every consistent reading: |beta| <= 7e-23 deg (QCD-pinned, 10i); "
         "c_g = 0 on the exact flat direction (10i); Higgs-overlap Yukawas force c_g = c_s = 0 (10i)",
         "none", "4.9 / 3.5 / 2.9 sigma from the three beta inputs (10g, 10k)"),
        ("C0  free U(1) rotation", "no f window for any beta input: gap x22-41 (10g, 10k, 10n)",
         "c_s = 0 charges; X-pinned fermions", "EXCLUDED"),
        ("M3a log-time oscillation", "registered curves need F = 0 (no Hubble friction); with FRW friction every mass law "
         "tested misses by >= 0.27 deg, ~ the signal (10j)", "c_s = 0; X-pinning; H1 dynamics",
         "NOT REALISABLE in FRW (pre-registered test still stands as a test)"),
        ("STUR-B log-time rotation", "Part C dynamics computed: f window 5.8e7-2.8e15 GeV (10n); needs ~150x "
         "suppression with no mechanism (beta_from_action); ratio 0.231, LiteBIRD 1.0 sigma (10b, 10k)",
         "c_s = 0; X-pinning; xi T|R|^2 with unpinned |R|; ~150x suppression", "viable, unexplained tuning"),
        ("U0  ultralight static mass (new)", (f"c_g = 6 reaches beta_now for m = {min(r['m_ev'] for r in viable):.1e}-"
                                             f"{max(r['m_ev'] for r in viable):.1e} eV with open f windows; "
                                             f"ratio {min(r['ratio'] for r in viable):.2f}-{max(r['ratio'] for r in viable):.2f}")
         if viable else "no viable mass", "c_s = 0 (c_g = 6 assignment); X-pinning; a free tiny mass m (not computed by STUR)",
         "viable" if viable else "not viable"),
    ]
    for name, evidence, extra, verdict in tab:
        print(f"\n  {name}\n    computed evidence: {evidence}\n    assumptions beyond STUR: {extra}\n    verdict: {verdict}")


def main():
    rows, viable = part1()
    part2(rows, viable)
    header("VERDICT")
    print("""  * STUR's own mathematics predicts no isotropic birefringence (H0), now by calculation in
    every consistent reading; the measured beta disfavours it at 2.9-4.9 sigma.
  * Of the beta != 0 options, C0 is excluded and M3a is not realisable with Hubble friction.
  * STUR-B and U0 remain. U0 uses standard ultralight-axion physics with an O(1) initial angle
    and an allowed c_g = 6 assignment, but its mass is a free parameter STUR does not fix;
    STUR-B needs an extra coupling, an unpinned modulus and a ~150x suppression with no
    mechanism. See the table above for which needs fewer unexplained elements.""")
    print(f"\n  gates: {sum(gates)}/{len(gates)} passed")


if __name__ == "__main__":
    main()
