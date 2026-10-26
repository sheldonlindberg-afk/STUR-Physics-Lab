#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10i: pinning and anomaly claims, computed
================================================================================
Replaces four arguments made in Stages 10f/10g with calculations.

  Part 1  Reading A (c_g = 8, c_s = 3): the R-phase is a QCD axion. Solve its
          equation of motion with V = chi(T)(1 - cos N theta), N = 2 c_s, from
          misalignment initial conditions over the f range (relic abundance), and
          bound kinetic initial conditions by energy. Compute the largest beta any
          admissible history can give, including the CAMB-visibility average of the
          oscillation at recombination.
  Part 2  Same QCD potential added to the STUR-B rotating driver and to M3a's
          oscillation: does it pin them? (Is c_s = 0 really required?)
  Part 3  Reading B: the zero-mode shift theta acting on the repo's localisation
          potential alpha(1 - cos(u + theta - phi_g)) on the circle. Compute the
          ground-state profile, the 4D mass phase arg m_4(theta), the chiral charge
          X_f = d arg m_4 / d theta, and E_0(theta), with and without an
          X-fixed pinning term and the repo's Higgs modulation (eps_H = 0.40).
  Part 4  Charge enumeration: solve U(1)_R invariance of the repo's Yukawas
          (R-Yukawas psibar R^s psi, s = +-1, Z3-allowed; and the Higgs-overlap
          Yukawas) for the fermion charges, and compute the photon and gluon
          anomaly coefficients of every consistent assignment.

Inputs: chi(0)^(1/4) = 75.5(5) MeV (Grilli di Cortona et al. 2016, verified);
high-T exponent b of chi ~ T^-b NOT verified -> scanned over b = 6.68-8.16;
T_c = 150 MeV and the piecewise g_* are approximations (they move the relic
abundance by O(1), not the beta bound, which uses rho <= rho_DM directly).

Usage:  python genesis_v10i_pinning_anomalies.py
================================================================================
"""
import itertools
from fractions import Fraction

import camb
import numpy as np
from scipy.integrate import solve_ivp

ALPHA = 1 / 137.035999
MP_RED = 2.435e18          # GeV
HBAR = 6.582119569e-25     # GeV s
CHI0 = 0.0755 ** 4         # GeV^4
TC = 0.150                 # GeV
RHO_CRIT_H2 = 8.096e-47    # GeV^4
RHO_DM = 0.120 * RHO_CRIT_H2
RHO_CRIT = RHO_CRIT_H2 * 0.6736 ** 2
T0 = 2.348e-13             # GeV (2.7255 K)
COSMO = dict(H0=67.36, ombh2=0.02237, omch2=0.1200, mnu=0.06, tau=0.0544, As=2.1e-9, ns=0.9649)
BETA_OBS = 0.277
OMEGA = 2 * np.pi ** 2

gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:58s} {detail:36s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 84 + "\n  " + s + "\n" + "=" * 84)


def gstar(T):
    return 61.75 if T > TC else 10.75 if T > 1e-3 else 3.36


def gstar_s(T):
    return 61.75 if T > TC else 10.75 if T > 1e-3 else 3.91


def chi(T, b):
    return CHI0 if T <= TC else CHI0 * (T / TC) ** (-b)


def hubble_rad(T):
    return np.sqrt(np.pi ** 2 / 30 * gstar(T) * T ** 4 / 3) / MP_RED


# ------------------------------------------------------------------------------
# Part 1: QCD-axion R-phase (reading A)
# ------------------------------------------------------------------------------
def misalignment_relic(f, theta_i, N, b):
    """theta amplitude today and Omega h^2 from misalignment; radiation era to m/H = 300, then WKB"""
    # integrate in x = ln(T_hi / T) with radiation-era H(T), dt = dx / H
    m = lambda T: N * np.sqrt(chi(T, b)) / f
    T_hi = 50.0
    while m(T_hi) > 0.01 * hubble_rad(T_hi):
        T_hi *= 3
    def rhs(x, y):
        T = T_hi * np.exp(-x)
        H = hubble_rad(T)
        th, thd = y                              # thd = d theta / dt
        dth_dx = thd / H
        dthd_dx = (-3 * H * thd - (N * chi(T, b) / f ** 2) * np.sin(N * th)) / H
        return [dth_dx, dthd_dx]
    def stop(x, y):
        T = T_hi * np.exp(-x)
        return m(T) / hubble_rad(T) - 300
    stop.terminal = True
    s = solve_ivp(rhs, [0, 80], [theta_i, 0.0], events=stop, rtol=1e-9, atol=1e-14, max_step=0.02)
    if s.t_events[0].size == 0:
        return None
    x1 = s.t_events[0][0]
    T1 = T_hi * np.exp(-x1)
    th, thd = s.y_events[0][0]
    m1 = m(T1)
    dth = th - np.round(N * th / (2 * np.pi)) * 2 * np.pi / N      # offset from the nearest minimum
    amp1 = np.sqrt(dth ** 2 + (thd / m1) ** 2)
    # WKB: n = m theta_amp^2 a^3 conserved, a ~ 1/(g_s^(1/3) T)
    a = lambda T: 1 / (gstar_s(T) ** (1 / 3) * T)
    amp_today = amp1 * np.sqrt(m1 * a(T1) ** 3 / (m(T0) * a(T0) ** 3))
    rho_today = 0.5 * f ** 2 * m(T0) ** 2 * amp_today ** 2
    return dict(T_osc=T1, amp_today=amp_today, omega_h2=rho_today / RHO_CRIT_H2, m0=m(T0))


def visibility_suppression(res, m_eV_s):
    """|<exp(i m t)>_vis| <= TV(g) / (m * int g): integration-by-parts bound, computed"""
    eta = np.linspace(150, 600, 4001)
    vis = res.get_background_time_evolution(eta, ['visibility'])['visibility']
    z = res.redshift_at_conformal_time(eta)
    t = np.array([res.physical_time(zz) for zz in z]) * 3.15576e16     # s
    g_t = vis * np.gradient(eta) / np.gradient(t)                      # visibility per unit t
    norm = np.trapezoid(g_t, t)
    tv = np.sum(np.abs(np.diff(g_t)))
    return tv / (m_eV_s * norm), (t[np.argmax(g_t)], t)


def part1(res):
    header("PART 1  Reading A: c_g = 8, c_s = 3 -> the R-phase is a QCD axion (N = 6)")
    c_g, c_s = 8, 3
    N = 2 * c_s
    K = c_g * ALPHA / (2 * np.pi)
    print(f"  theta_QCD,eff = 2 c_s theta = {N} theta; m(T=0) = N sqrt(chi0)/f;"
          f" chi0^(1/4) = {CHI0 ** 0.25 * 1e3:.1f} MeV")
    fs = np.logspace(9, np.log10(1.2e19), 12)
    rows = []
    for b in (6.68, 8.16):
        for f in fs:
            r = misalignment_relic(f, 1.0 / N, N, b)            # theta_QCD,i = N theta_i = 1
            if r:
                rows.append((b, f, r))
    print(f"\n  misalignment, theta_QCD,i = 1 (relic; T_osc; theta amplitude today):")
    print(f"  {'b':>5s} {'f [GeV]':>10s} {'T_osc [GeV]':>12s} {'Omega h^2':>11s} {'theta_amp(0)':>13s} {'m0 [eV]':>10s}")
    for b, f, r in rows[::2]:
        print(f"  {b:5.2f} {f:10.2e} {r['T_osc']:12.3e} {r['omega_h2']:11.2e} {r['amp_today']:13.2e} {r['m0'] * 1e9:10.2e}")
    allowed = [(b, f, r) for b, f, r in rows if r['omega_h2'] <= 0.12]
    gate("misalignment relic computed for every f (oscillation onset found)", len(rows) == 2 * len(fs),
         f"{len(rows)}/{2 * len(fs)}")
    # energy bound, any initial condition: trapped field with rho <= rho_DM
    amp_max_today = np.sqrt(2 * RHO_DM / (N ** 2 * CHI0))
    rho_untrapped = 2 * CHI0                     # kinetic energy needed to still rotate over the barrier
    print(f"\n  any initial condition (misalignment or kinetic):")
    print(f"    still rotating today needs rho >= 2 chi0 = {rho_untrapped:.2e} GeV^4"
          f" = {rho_untrapped / RHO_CRIT:.1e} rho_crit -> impossible")
    print(f"    trapped: rho = (N^2 chi0/2) theta_amp^2 <= rho_DM -> theta_amp(0) <= {amp_max_today:.2e} (independent of f)")
    gate("no history can still be rotating today (rho >= 2 chi0 >> rho_crit)", rho_untrapped / RHO_CRIT > 1e30,
         f"ratio {rho_untrapped / RHO_CRIT:.1e}")
    # recombination: amplitude there, and visibility averaging of the fast oscillation
    amp_rec = amp_max_today * (1090.0) ** 1.5
    worst_m = N * np.sqrt(CHI0) / 1.2e19 / HBAR          # s^-1, slowest (largest f)
    S, _ = visibility_suppression(res, worst_m)
    beta_max = K * (amp_max_today + amp_rec * S)
    print(f"    at recombination theta_amp <= {amp_rec:.2e}; slowest oscillation m = {worst_m:.2e} s^-1 (f = M_Pl)")
    print(f"    visibility average |<e^(imt)>| <= TV(g)/(m int g) = {S:.2e}")
    print(f"    => |beta| <= K [theta_amp(0) + theta_amp(t*) S] = {np.degrees(beta_max):.2e} deg"
          f"   (observed {BETA_OBS} deg)")
    gate("reading A cannot give beta ~ 0.277 deg for any f or initial condition",
         np.degrees(beta_max) < 1e-6, f"|beta| <= {np.degrees(beta_max):.1e} deg")
    # theta_QCD today and nEDM
    print(f"    theta_QCD,eff today <= N theta_amp = {N * amp_max_today:.1e} (nEDM bound 1e-10): satisfied")
    return dict(amp_max_today=amp_max_today, beta_max_deg=float(np.degrees(beta_max)),
                n_allowed_f=len(allowed))


# ------------------------------------------------------------------------------
# Part 2: QCD potential vs STUR-B and M3a drivers
# ------------------------------------------------------------------------------
def part2(res):
    header("PART 2  Does a QCD potential (c_s != 0) pin the STUR-B / M3a dynamics?")
    t0 = res.physical_time(0.0) * 3.15576e16
    tstar = res.physical_time(1090.0) * 3.15576e16
    out = {}
    for c_s in (3,):
        N = 2 * c_s
        for f in (1e10, 1e12, 1e14, 1e16, 1.2e19):
            m0 = N * np.sqrt(CHI0) / f / HBAR                      # s^-1
            # M3a: log-time restoring frequency omega/t vs QCD frequency
            r_today, r_rec = m0 * t0 / OMEGA, m0 * tstar / OMEGA
            # STUR-B: rotating at d theta/dt = omega_eff/t needs kinetic energy over the barrier
            w_eff = 0.1319                                          # per unit ln t (c_g = 3) from beta_from_action
            thdot0 = w_eff / t0 * HBAR                              # GeV
            rho_rot = 0.5 * f ** 2 * thdot0 ** 2
            out[f] = (r_today, r_rec, rho_rot / (2 * CHI0))
            print(f"  f = {f:8.1e} GeV: m_QCD t / omega today {r_today:8.1e}, at t* {r_rec:8.1e};"
                  f" STUR-B rotation energy / barrier = {rho_rot / (2 * CHI0):8.1e}")
    # once m_QCD >> H the dynamics is a trapped oscillation about a minimum, with energy
    # (N^2 chi0 / 2) amp^2 that cannot exceed the total density: amplitude bound, any driver
    amp_cap = np.sqrt(2 * RHO_CRIT / ((2 * 3) ** 2 * CHI0))
    print(f"\n  trapped amplitude today, any driver: amp <= sqrt(2 rho_crit / (N^2 chi0)) = {amp_cap:.2e} rad")
    print("  M3a needs A0 = 1.44-2.93 rad (c_g = 3) or 0.54-1.10 rad (c_g = 8); STUR-B needs ~1.4 rad of"
          " winding after recombination")
    gate("with c_s != 0 neither M3a's A0 nor STUR-B's winding fits under rho_crit", amp_cap < 1e-10,
         f"amp cap {amp_cap:.1e} rad vs ~1 rad")
    rmin = min(v[1] for v in out.values())
    gate("QCD mass dominates the log-time frequency at t* for every f <= M_Pl", rmin > 1e10, f"min m t*/omega = {rmin:.1e}")
    rot = max(v[2] for v in out.values())
    gate("STUR-B rotation cannot overcome the QCD barrier today (any f <= M_Pl)", rot < 1, f"max energy/barrier = {rot:.1e}")
    return dict(min_ratio_rec=rmin, max_rot_over_barrier=rot)


# ------------------------------------------------------------------------------
# Part 3: reading B, the shift theta on the repo's localisation potential
# ------------------------------------------------------------------------------
def ground_state(alpha, theta, eta=0.0, n=2048):
    from scipy.sparse import diags
    from scipy.sparse.linalg import eigsh
    u = np.linspace(-np.pi, np.pi, n, endpoint=False)
    du = u[1] - u[0]
    V = alpha * (1 - np.cos(u + theta)) + eta * (1 - np.cos(3 * u))
    H = diags([2 / du ** 2 + V, -np.ones(n - 1) / du ** 2, -np.ones(n - 1) / du ** 2], [0, 1, -1]).tolil()
    H[0, n - 1] = H[n - 1, 0] = -1 / du ** 2
    w, v = eigsh(H.tocsc(), k=1, sigma=V.min() - 1, which='LM', tol=0)
    psi = v[:, 0] / np.sqrt(np.sum(v[:, 0] ** 2) * du)
    return u, du, psi, w[0]


def mass_phase(alpha, theta, eta=0.0, eps_h=0.0):
    u, du, psi, E = ground_state(alpha, theta, eta)
    h = 1 + eps_h * np.cos(3 * u)                        # Higgs modulation fixed in X (if pinned)
    m4 = np.sum(psi ** 2 * h * np.exp(1j * (u + theta))) * du   # chiral phase at u is phi = u + theta
    return np.angle(m4), abs(m4), E


def part3():
    header("PART 3  Reading B: does shifting theta rotate the 4D mass phases? (chiral charge X_f)")
    out = {}
    for alpha, lab in ((1.48, "quark brane alpha = 1.48"), (1.38, "lepton brane alpha = 1.38")):
        ths = np.linspace(-0.3, 0.3, 7)
        for eta, eps, case in ((0.0, 0.0, "comoving (repo potential only)"),
                               (0.0, 0.40, "+ X-fixed Higgs modulation eps_H = 0.40"),
                               (1.0, 0.0, "+ X-fixed pinning eta = 1"),
                               (10.0, 0.0, "+ X-fixed pinning eta = 10"),
                               (100.0, 0.0, "+ X-fixed pinning eta = 100")):
            ph = np.unwrap([mass_phase(alpha, t, eta, eps)[0] for t in ths])
            Es = [mass_phase(alpha, t, eta, eps)[2] for t in ths]
            X = np.polyfit(ths, ph, 1)[0]
            out[(alpha, case)] = (X, max(Es) - min(Es))
            print(f"  {lab:26s} {case:42s} X_f = {X:+.6f}   E_0 range over theta = {max(Es) - min(Es):.2e}")
    X0 = out[(1.48, "comoving (repo potential only)")]
    gate("comoving localisation: X_f = 0 and E_0(theta) flat", abs(X0[0]) < 1e-8 and X0[1] < 1e-8,
         f"X_f = {X0[0]:.1e}, dE = {X0[1]:.1e}")
    Xh = out[(1.48, "+ X-fixed Higgs modulation eps_H = 0.40")][0]
    print(f"\n  with the repo's comoving potential, c_g = sum X_f N_c Q^2 = 0 (no theta F Ftilde at all);"
          f" an X-fixed Higgs modulation gives X_f = {Xh:+.4f}, i.e. c_g = {8 * Xh:+.3f} if every species has it")
    Xp = out[(1.48, "+ X-fixed pinning eta = 100")][0]
    gate("strong X-fixed pinning recovers X_f -> 1 (reading A)", abs(Xp - 1) < 0.05, f"X_f(eta=100) = {Xp:.3f}")
    # does the repo's Z3 action have fixed points that could pin?  X -> X + L/3 on a circle of length L
    L = 1.0
    xs = np.linspace(0, L, 100001)
    d = np.min(np.abs(((xs + L / 3) - xs + L / 2) % L - L / 2))
    print(f"\n  Z3 action X -> X + L/3: min_X |shift mod L| = {d:.4f} L > 0 -> no fixed points (freely acting)")
    # S1/Z2 (Master Action sec 1.3) requires R(-X) = R(X); test with the winding background
    kX = np.linspace(0, 2 * np.pi / 3, 1001)
    viol = np.max(np.abs(np.exp(1j * kX) - np.exp(-1j * kX)))
    print(f"  S1/Z2 with R Z2-even vs winding R = v e^(ikX): max |R(X) - R(-X)|/v = {viol:.3f} (not Z2-even)")
    gate("Z3 action has no fixed points (cannot pin positions)", d > 0.3, f"min shift {d:.3f} L")
    return dict(X_comoving=X0[0], X_higgs=Xh, X_pinned=Xp, z2_violation=viol)


# ------------------------------------------------------------------------------
# Part 4: charges from U(1)_R invariance of the repo's Yukawas, and anomalies
# ------------------------------------------------------------------------------
SPECIES = {  # Dirac fermion: (N_c, Q, T for colour)
    'u': (3, Fraction(2, 3)), 'd': (3, Fraction(-1, 3)), 'e': (1, Fraction(-1)),
}


def anomalies(chiral):
    """chiral[f] = X_L - X_R for species f (common to the 3 generations)"""
    cg = 3 * sum(chiral[f] * SPECIES[f][0] * SPECIES[f][1] ** 2 for f in SPECIES)
    cs = 3 * sum(chiral[f] * Fraction(1, 2) for f in ('u', 'd'))
    return cg, cs


def part4():
    header("PART 4  Charge assignments allowed by the repo's Yukawas, and their anomalies")
    # (i) generation-dependent signs inside a sector are excluded when all Y_ij != 0
    sig = 0.862
    Xg = np.array([0, 2 * np.pi / 3, 4 * np.pi / 3])
    Y = np.exp(-np.minimum(np.abs(Xg[:, None] - Xg[None, :]), 2 * np.pi - np.abs(Xg[:, None] - Xg[None, :])) ** 2
               / (4 * sig ** 2))
    print(f"  repo overlap Yukawa matrix (sigma = {sig}): min |Y_ij| = {Y.min():.3f} (all nonzero)")
    # all Y_ij != 0: X_L,i - X_R,j = s_j for every i,j -> X_L,i all equal, X_R,j = X_L - s_j.
    # A generation-dependent sign carried by the right-handed field is therefore consistent.
    A, rhs = [], []
    sj = (1, -1, 1)
    for i in range(3):
        for j in range(3):
            row = np.zeros(6); row[i] = 1; row[3 + j] = -1
            A.append(row); rhs.append(sj[j])
    sol = np.linalg.lstsq(np.array(A), np.array(rhs, float), rcond=None)[0]
    err = np.max(np.abs(np.array(A) @ sol - rhs))
    print(f"  R-Yukawas only, generation-dependent signs s_j = {sj}: residual {err:.1e} -> consistent"
          " (X_L common, X_R,j = X_L - s_j)")
    gate("R-Yukawas alone permit generation-dependent R-signs (computed)", err < 1e-9, f"residual {err:.1e}")
    allsets = set()
    for su in itertools.product((1, -1), repeat=3):
        for sd in itertools.product((1, -1), repeat=3):
            for se in itertools.product((1, -1), repeat=3):
                cg = sum(Fraction(4, 3) * a + Fraction(1, 3) * b + c for a, b, c in zip(su, sd, se))
                cs = sum(Fraction(1, 2) * (a + b) for a, b in zip(su, sd))
                allsets.add((cg, cs))
    cs0 = sorted({cg for cg, cs in allsets if cs == 0})
    print(f"  all 512 per-generation assignments: c_s = 0 occurs with c_g in {[str(x) for x in cs0]}")
    # (ii) R-Yukawas only: s_u, s_d, s_e in {+1, -1}
    print("\n  (ii) R-Yukawas only, psibar_L R^s psi_R with s = +-1 per sector (Z3 allows R and R* ~ R^2):")
    table = []
    for su, sd, se in itertools.product((1, -1), repeat=3):
        cg, cs = anomalies({'u': su, 'd': sd, 'e': se})
        table.append(((su, sd, se), cg, cs))
        print(f"     s_u = {su:+d}, s_d = {sd:+d}, s_e = {se:+d}:  c_g = {str(cg):>3s}, c_s = {str(cs):>4s}")
    have_cs0 = [(s, cg) for s, cg, cs in table if cs == 0]
    gate("an assignment with c_s = 0 and c_g != 0 exists with quarks R-charged",
         any(cg != 0 for _, cg in have_cs0), f"{[(s, str(cg)) for s, cg in have_cs0 if cg != 0][:1]}")
    # (iii) R-Yukawas AND the Higgs-overlap Yukawas (repo masses), U(1)_R exact -> H charged
    print("\n  (iii) R-Yukawas plus Higgs Yukawas Qbar Htilde u, Qbar H d, Lbar H e (repo mass overlaps):")
    print("       invariance: X_Q - X_u = s_u = -X_H,  X_Q - X_d = s_d = X_H,  X_L - X_e = s_e = X_H")
    res3 = []
    for XH in (1, -1):
        cg, cs = anomalies({'u': -XH, 'd': XH, 'e': XH})
        res3.append((XH, cg, cs))
        print(f"       X_H = {XH:+d}: c_g = {cg}, c_s = {cs}")
    gate("with both Yukawa structures U(1)_R is anomaly-free (c_g = c_s = 0)",
         all(cg == 0 and cs == 0 for _, cg, cs in res3), "c_g = c_s = 0 for X_H = +-1")
    print("       X_H = 0 (Higgs R-neutral): requires s = 0, contradicting s = +-1 -> U(1)_R explicitly broken")
    return dict(table=[(s, str(cg), str(cs)) for s, cg, cs in table], with_higgs=[(x, str(a), str(b)) for x, a, b in res3])


def main():
    res = camb.get_results(camb.set_params(**COSMO))
    p1 = part1(res)
    p2 = part2(res)
    p3 = part3()
    p4 = part4()
    header("SUMMARY")
    print(f"""  1. Reading A (c_g = 8, c_s = 3): QCD pins the phase for every f <= M_Pl and every initial
     condition; |beta| <= {p1['beta_max_deg']:.0e} deg. Confirmed: no birefringence.
  2. A QCD potential dominates the STUR-B and M3a dynamics (m t*/omega >= {p2['min_ratio_rec']:.0e}); STUR-B's
     rotation energy is <= {p2['max_rot_over_barrier']:.0e} of the barrier. Confirmed: both need c_s = 0.
  3. Reading B: with the repo's own (comoving) localisation potential, X_f = {p3['X_comoving']:.0e}: the zero
     mode does not rotate any 4D mass phase, so c_g = c_s = 0 exactly. X_f -> 1 only with an X-fixed
     pinning that the repo does not have (its Z3 action has no fixed points).
  4. R-Yukawas alone allow c_s = 0 with c_g != 0 (e.g. s_u = -s_d gives +-6), so quarks may carry R-charge:
     the earlier 'forces c_g = 8, c_s = 3 / leptons only' is refuted. With the repo's Higgs Yukawas
     as well, U(1)_R invariance forces c_g = c_s = 0.""")
    print(f"\n  gates: {sum(gates)}/{len(gates)} passed")


if __name__ == "__main__":
    main()
