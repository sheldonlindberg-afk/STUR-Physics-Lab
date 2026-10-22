#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- STUR-B action audit: can the birefringence bridge hypothesis
(A1 + A2 of 'genesis V10 Light Bird') be derived from the STUR Master Action?
================================================================================
Master Action (scripts/stur_master_action_derivation.html, eq. 2.5):

  S = int d^5x sqrt(-g) [ 1/2 |dR|^2 - V(|R|) + chi |R|^2 d_X phi
                          + alpha |R| T + L_matter ],     R = |R| e^{i phi}

STUR-B needs two things:
  (i)  a parity-odd photon coupling, so that a change of the R-phase rotates
       linear polarisation:  beta = (c_g alpha_em / 2 pi) * Delta phi
  (ii) a phase that accrues linearly in log-time,  d phi / d ln t = const  (A2)

This script checks each against the action and computes the consequences on the
same Planck 2018 background and line-of-sight (LOS) reionization tomography
used by the pre-registration, so every accrual law is compared like for like.

  Part A  Noether no-go: the Master Action is U(1) invariant, so the homogeneous
          phase obeys a^3 |R|^2 phi_dot = Q. With |R| = v this gives
          phi_dot ~ a^-3, not 1/t.  (symbolic, sympy)
  Part B  Audit of the repo's Cauchy-Euler equation
          W'' + W'/t + (omega/t)^2 W = 0 (DERIVATION_CHAIN_INFINITY.md 2.3b):
          FRW friction is 3H = 2/t in matter domination, not 1/t.
  Part C  Minimal CP-even extension that does give log-time accrual:
          L_B = (xi/2) T |R|^2 + c_g (alpha_em/4 pi) phi F Ftilde,
          with the radial mode not pinned. Solved exactly on the background.
  Part D  LOS predictions (beta_reio/beta_rec, Delta beta) for each law, plus
          the anomaly coefficient c_g each one requires.

Usage:  python genesis_v10_sturb_action_audit.py
================================================================================
"""
import importlib.util
import os
from importlib.machinery import SourceFileLoader

import numpy as np
import sympy as sp
from scipy.integrate import cumulative_trapezoid, solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
_lb_path = os.path.join(HERE, "genesis V10 Light Bird")
_loader = SourceFileLoader("genesis_v10_litebird", _lb_path)
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
LB = importlib.util.module_from_spec(_spec)
_loader.exec_module(LB)

ALPHA_EM = 1 / 137.035999
OMEGA_CHRONO = 2 * np.pi ** 2        # repo v7.0 exact value (stur_chronomagnetics_omega.html)
BETA_REC, S_BETA = LB.DATA['beta_now'][0], LB.DATA['beta_now'][1]
SIG_DB_LB = LB.DATA['LB_sigma_dbeta'][0]
PREREG_DBETA = -0.21802718458621612  # from scripts/genesis V10 preregistration

gates = []


def gate(name, ok, detail):
    gates.append((name, bool(ok)))
    print(f"  gate: {name:52s} {detail:40s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 80 + "\n  " + s + "\n" + "=" * 80)


# ------------------------------------------------------------------------------
# Part A: Noether no-go for the Master Action as written
# ------------------------------------------------------------------------------
def part_A():
    header("PART A  Master Action, homogeneous FRW zero mode: Noether charge")
    t = sp.symbols('t', positive=True)
    chi, alpha, k, lam, v = sp.symbols('chi alpha k lambda v', real=True)
    a = sp.Function('a', positive=True)(t)
    rho = sp.Function('rho', positive=True)(t)       # |R|
    th = sp.Function('theta', real=True)(t)          # 4D zero mode of phi
    H = a.diff(t) / a
    Tsc = -6 * H ** 2                                # TEGR torsion scalar, flat FRW, diagonal tetrad
    V = lam / 4 * (rho ** 2 - v ** 2) ** 2
    # phi(t, X) = k X + theta(t): the XCRM density chi rho^2 d_X phi = chi k rho^2
    L = a ** 3 * (sp.Rational(1, 2) * (rho.diff(t) ** 2 + rho ** 2 * th.diff(t) ** 2)
                  - V + chi * k * rho ** 2 + alpha * rho * Tsc)
    EL_th = sp.diff(sp.diff(L, th.diff(t)), t) - sp.diff(L, th)
    p_th = sp.simplify(sp.diff(L, th.diff(t)))
    print(f"  L_eff/a^3 depends on theta only through theta_dot: dL/dtheta = {sp.diff(L, th)}")
    print(f"  conjugate momentum  p_theta = {p_th}")
    print(f"  Euler-Lagrange      d/dt p_theta = 0   (EL residual = {sp.simplify(EL_th - sp.diff(p_th, t))})")
    gate("U(1): theta is cyclic in the Master Action", sp.diff(L, th) == 0, "dL/dtheta = 0")
    # if theta_dot = w/t (log-time accrual) with rho = v, p_theta must be constant
    w = sp.symbols('w', positive=True)
    pp = sp.symbols('p', positive=True)
    test = (p_th.subs({th.diff(t): w / t, rho: v}).subs(a, t ** pp))
    dp = sp.simplify(sp.diff(test, t))
    print(f"  with |R| = v, theta_dot = w/t, a = t^p:  d p_theta/dt = {sp.factor(dp)}")
    sol_p = sp.solve(sp.Eq(dp, 0), pp)
    print(f"  vanishes only for p = {sol_p}  (a ~ t^(1/3): stiff/kination, never realised after BBN)")
    gate("log-time accrual incompatible with U(1) at |R| = v", sol_p == [sp.Rational(1, 3)],
         f"requires a ~ t^{sol_p}")
    print("\n  => With |R| pinned at v, theta_dot = Q / (v^2 a^3): the phase freezes out.")
    print("     The chi term is a total derivative for constant |R| and cannot source it;")
    print("     alpha|R|T couples only to |R|. The Master Action alone does not give A2.")


# ------------------------------------------------------------------------------
# Part B: audit of the Cauchy-Euler equation used for chronomagnetics
# ------------------------------------------------------------------------------
def part_B():
    header("PART B  Cauchy-Euler equation of DERIVATION_CHAIN_INFINITY.md 2.3b")
    r, p, xi, om = sp.symbols('r p xi omega', positive=True)
    # repo:  W'' + (1/t) W' + (omega/t)^2 W = 0  ->  r^2 + omega^2 = 0
    print("  repo equation: W'' + (1/t)W' + (w/t)^2 W = 0  -> indicial r^2 + w^2 = 0 -> W = sin(w ln t)")
    # FRW zero mode: W'' + 3H W' + m^2 W, H = p/t
    ind = sp.expand(r * (r - 1) + 3 * p * r + om ** 2)
    print(f"  FRW zero mode, a ~ t^p:  W'' + (3p/t)W' + (w/t)^2 W = 0 -> indicial {ind} = 0")
    roots = sp.solve(ind.subs(p, sp.Rational(2, 3)), r)
    print(f"  matter era p = 2/3: r = {roots}")
    print("    -> W = t^(-1/2) sin(sqrt(w^2 - 1/4) ln t): amplitude decays, frequency shifted")
    fr = sp.solve(sp.Eq(3 * p - 1, 0), p)
    print(f"  the repo's 1/t friction needs 3p = 1, i.e. p = {fr}, not matter domination (p = 2/3)")
    gate("repo friction coefficient matches FRW matter era", False, "1/t vs 3H = 2/t")
    print("  The restoring term (w/t)^2 = 6 xi H^2 is a non-minimal coupling xi T |R|^2;")
    print("  it is not in the Master Action (which has the non-analytic alpha |R| T).")
    print("  Note also: W(t) is a real amplitude; its oscillation phase w ln t is not the")
    print("  R-field angle phi. Only a *complex* (rotating) doublet mode turns w ln t into phi.")
    # the 'triangle vs exact' mismatch inside the pre-registration
    print(f"\n  pre-registration uses ln(lambda) = ln(3722/2705) = {np.log(3722/2705):.5f};"
          f" repo v7.0 exact value is 1/pi = {1/np.pi:.5f} (0.27% apart).")
    print("  Irrelevant at eps = 0, but the eps-modulation period should use the v7.0 value.")


# ------------------------------------------------------------------------------
# Part C: minimal CP-even extension, solved exactly on the Planck background
# ------------------------------------------------------------------------------
def xi_for_matter_frequency(Om):
    """xi such that the rotating mode has d phi/d ln t = Om in pure matter domination"""
    # r = -(3p-1)/2 + i Om_p,  Om_p^2 = 6 xi p^2 - (3p-1)^2/4,  p = 2/3
    return (Om ** 2 + 0.25) / (6 * (2 / 3) ** 2)


def era_frequency(xi, p):
    return np.sqrt(6 * xi * p ** 2 - (3 * p - 1) ** 2 / 4)


def solve_rotating_mode(bg, xi, Ni=np.log(1e-6), n=200001):
    """W'' + (3 + dlnH/dN) W' + 6 xi W = 0 in N = ln a; complex W, radiation-era circular IC"""
    N = np.linspace(Ni, 0.0, n)
    z = np.exp(-N) - 1
    lnH = np.log(bg.H(z))
    dlnH = np.gradient(lnH, N)
    dl = lambda x: np.interp(x, N, dlnH)
    Om_r = era_frequency(xi, 0.5)
    rN = 2 * (-0.25 + 1j * Om_r)             # radiation: t ~ a^2, W = t^r = a^(2r)

    def rhs(x, y):
        W, Wp = y[0] + 1j * y[1], y[2] + 1j * y[3]
        Wpp = -(3 + dl(x)) * Wp - 6 * xi * W
        return [Wp.real, Wp.imag, Wpp.real, Wpp.imag]
    s = solve_ivp(rhs, [Ni, 0.0], [1.0, 0.0, rN.real, rN.imag], t_eval=N, rtol=1e-10,
                  atol=1e-14, method='DOP853')
    W = s.y[0] + 1j * s.y[1]
    phi = np.unwrap(np.angle(W))
    return N, z, phi, np.abs(W)


def part_C(bg):
    header("PART C  Minimal CP-even extension: L_B = (xi/2) T |R|^2 + c_g (alpha/4pi) phi F Ftilde")
    print("  CP check: |R|^2 T even; phi odd (R -> R*), F Ftilde odd -> phi F Ftilde even.")
    print("  Both terms respect the ∞3 x CP symmetry used for theta_QCD = 0; the sign of the")
    print("  rotation (sign of the Noether charge Q) is set spontaneously by initial conditions.")
    print("  (A derivative coupling d_mu phi T^mu would give phi ~ ln a, but it is CP-odd.)")
    xi = xi_for_matter_frequency(OMEGA_CHRONO)
    print(f"\n  identify the matter-era log-time frequency with omega = 2 pi^2 = {OMEGA_CHRONO:.4f}")
    print(f"  -> xi = (omega^2 + 1/4) / (6 p^2) = {xi:.2f}   (large non-minimal coupling)")
    print(f"     era rates d phi/d ln t: radiation {era_frequency(xi, .5):.3f}, matter {OMEGA_CHRONO:.3f};"
          f" Lambda era: d phi/d ln a = {np.sqrt(24 * xi - 9) / 2:.3f}")
    N, z, phi, amp = solve_rotating_mode(bg, xi)
    t = bg.age(z)
    lnt = np.log(t)
    dphidlnt = np.gradient(phi, lnt)
    # solver check against the local WKB rate  d phi/dN = sqrt(6 xi - ((3 + dlnH/dN)/2)^2)
    dlnH = np.gradient(np.log(bg.H(z)), N)
    wkb = np.sqrt(6 * xi - ((3 + dlnH) / 2) ** 2)
    m = (z > 30) & (z < 300)
    rel = np.median(np.abs(np.gradient(phi, N)[m] / wkb[m] - 1))
    gate("rotating mode follows local WKB rate (z = 30-300)", rel < 1e-3, f"median |rel err| = {rel:.1e}")
    print(f"  d phi/d ln t at z = 30-300: {np.median(dphidlnt[m]):.3f} (-> {OMEGA_CHRONO:.3f} only as"
          f" radiation -> 0; H t = {np.median((bg.H(z) * t)[m]):.4f} vs 2/3)")
    print(f"  d phi/d ln a is nearly era-independent: radiation {np.median(np.gradient(phi, N)[z > 1e4]):.2f},"
          f" matter {np.median(np.gradient(phi, N)[m]):.2f}, today {np.gradient(phi, N)[-1]:.2f}"
          f"  (sqrt(6 xi) = {np.sqrt(6 * xi):.2f})")
    print("  => for xi >> 1 the derived accrual is phi ~ sqrt(6 xi) ln a, i.e. log-SCALE-FACTOR, not log-time.")
    gate("|R| ~ t^-1/2 in matter era (not pinned at v)",
         abs(np.polyfit(lnt[m], np.log(amp[m]), 1)[0] + 0.5) < 0.03,
         f"slope {np.polyfit(lnt[m], np.log(amp[m]), 1)[0]:+.3f}")
    # residual modulation (the eps of A2) produced by the radiation -> matter transition
    mm = (z > 20) & (z < 600)
    eps_eff = np.std(dphidlnt[mm] / np.polyval(np.polyfit(lnt[mm], dphidlnt[mm], 3), lnt[mm]) - 1) * np.sqrt(2)
    print(f"  log-periodic modulation left after radiation->matter: eps_eff ~ {eps_eff:.1e}"
          f" (at 2x the rotation frequency, not 1x as A2 assumes)")
    return xi, N, z, phi


# ------------------------------------------------------------------------------
# Part D: LOS predictions for each accrual law
# ------------------------------------------------------------------------------
def part_D(bg, N, z, phi_C):
    header("PART D  LOS tomography for each accrual law (same machinery as the pre-registration)")
    zre = bg.zre_for_tau(LB.DATA['tau'][0])
    tomo = LB.ReioTomography(bg, zre)
    zs = LB.DATA['zstar']
    zg = z[::-1]                                      # increasing z for interpolation

    def law(phi_of_z):
        p0 = phi_of_z(0.0)
        return lambda zz: p0 - phi_of_z(zz)           # accumulated phase from emission to today

    # C0: Master Action as written (U(1), |R| = v): phi_dot = Q/(v^2 a^3)
    a = np.exp(N)
    dt_dN = 1 / bg.H(z)
    phi0 = cumulative_trapezoid(a ** -3 * dt_dN, N, initial=0.0)
    # C1: STUR-B as pre-registered: phi ~ ln t
    # C2: rotating mode with xi T |R|^2 (Part C)
    # C3: CP-odd derivative coupling: phi ~ ln a
    laws = {
        "C0 Master Action (U(1), |R|=v)": (lambda zz: np.interp(zz, zg, phi0[::-1])),
        "C1 STUR-B pre-registered (ln t)": (lambda zz: np.log(bg.age(zz))),
        "C2 xi T|R|^2 rotating mode": (lambda zz: np.interp(zz, zg, phi_C[::-1])),
        "C3 d phi . T^mu (ln a, CP-odd)": (lambda zz: -np.log1p(zz)),
    }
    print(f"  normalisation: beta_rec = {BETA_REC} +/- {S_BETA} deg in every case;"
          f" LiteBIRD sigma(Delta beta) = {SIG_DB_LB} deg\n")
    print(f"  {'accrual law':34s} {'ratio':>7s} {'beta_reio':>10s} {'Delta beta':>11s}"
          f" {'vs 0':>6s} {'vs prereg':>9s} {'c_g needed':>11s}")
    out = {}
    for name, pz in laws.items():
        acc = law(pz)
        per = float(acc(zs))
        bfun = lambda zz, per=per, acc=acc: BETA_REC * acc(zz) / per
        breio = tomo.beta_reio(bfun)[0]
        ratio = breio / BETA_REC
        db = breio - BETA_REC
        sdb = abs(db) * S_BETA / BETA_REC
        s0 = abs(db) / np.hypot(SIG_DB_LB, sdb)
        sp_ = abs(db - PREREG_DBETA) / np.hypot(SIG_DB_LB, sdb)
        if name.startswith("C0"):
            cg = "free (Q)"
        elif name.startswith("C3"):
            cg = "free (g)"
        else:
            dphi = per if not name.startswith("C1") else per * OMEGA_CHRONO
            cg = f"{np.radians(BETA_REC) * 2 * np.pi / (ALPHA_EM * dphi):.4f}"
        out[name] = (ratio, db)
        print(f"  {name:34s} {ratio:7.3f} {breio:9.4f}° {db:+10.4f}° {s0:5.1f}σ {sp_:8.1f}σ {cg:>11s}")
    print("\n  c_g for C1 assumes the phase rotates at the chronomagnetic rate omega per unit ln t.")
    print("  Anomaly matching gives c_g = E/2, E = sum_f X_f N_c Q_f^2 over R-charged chiral fermions;")
    print("  the smallest natural value is c_g = 1/2 (one charged lepton). c_g ~ 0.02 is ~25x below")
    print("  it: with c_g = 1/2 and phase rate omega, beta_rec would be ~ 7 deg, excluded.")
    r1 = out["C1 STUR-B pre-registered (ln t)"][0]
    gate("C1 reproduces the pre-registered ratio 0.2129", abs(r1 - 0.21289825) < 1e-4, f"{r1:.4f}")
    return out


def main():
    bg = LB.Background()
    part_A()
    part_B()
    xi, N, z, phi_C = part_C(bg)
    part_D(bg, N, z, phi_C)
    header("SUMMARY")
    print("""  1. The Master Action as written cannot produce STUR-B: its exact U(1) forces
     phi_dot ~ a^-3 at |R| = v; the phase freezes after the hot big bang and nearly all
     rotation happens before reionization (Delta beta ~ -beta_rec).
  2. The repo's Cauchy-Euler 'log-time' equation is not the FRW equation of any zero mode
     in matter domination (friction 1/t vs 2/t) and its restoring term is not in the action.
  3. Log-time accrual CAN be derived from a minimal CP-even extension
       (xi/2) T |R|^2 + c_g (alpha/4pi) phi F Ftilde
     for a rotating, unpinned doublet mode. For xi >> 1 the phase accrues as ln a (not
     ln t); the LOS ratio moves 0.213 -> 0.234, a 0.1 sigma shift LiteBIRD cannot resolve.
  3b. LiteBIRD's Delta beta separates STUR-B from late-only rotation (ratio 1, 3.2 sigma)
     but NOT from the Master Action as written (ratio ~ 0): only 0.8 sigma apart.
  4. Costs of that extension: xi ~ 146; |R| decays as t^-1/2 (conflicts with |R| = v used
     for Lambda_tree = 0); c_g ~ 0.02 is unnaturally small for an anomaly coefficient; and
     the R-charged fermions must be colour-neutral or phi becomes a rolling QCD theta.""")
    npass = sum(ok for _, ok in gates)
    print(f"\n  gates: {npass}/{len(gates)} passed (the Part B FAIL is the audit finding, expected)")


if __name__ == "__main__":
    main()
