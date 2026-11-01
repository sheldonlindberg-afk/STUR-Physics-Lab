#!/usr/bin/env python3
"""
Refinement round 8, module 8B: can a second holonomy theta_2 be the dark energy?
Preregistered in docs/R8_PREREGISTRATION.md; results in docs/REFINEMENT_R8.md.
Requires numpy, scipy. Runs in about 1 min.

Assumptions (preregistered): D-B1 a second Z2-odd U(1)_B' on the same circle
L, V2 = m2^2 f2^2 (1 + cos theta_2) with m2^2 f2^2 ~ e^(-M2 L)/L^4; D-B2 no
bare cosmological constant; D-B3 theta_2 born at 0, made a hilltop by the
brane twist, offset theta_2i from the inflationary random walk; D-B4 photon
coupling at integer level k2.

  Q1  background: Omega_DE = 0.685 today; w0, wa (CPL fit, 0 < z < 2.5)
  Q2  electric weak gravity conjecture for U(1)_B'
  Q3  extra late-time rotation (k2 alpha / 2 pi) Delta theta_2
  Q4  the predicted (w0, wa) locus for the random-walk theta_2i
  dS  refined de Sitter conjecture at the hilltop (reported, not a kill)
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

BAR = "=" * 78
H_LITTLE = 0.6736
OM, OR = 0.1430 / H_LITTLE ** 2, 4.18e-5 / H_LITTLE ** 2
ODE = 1 - OM - OR                                   # 0.685
ALPHA = 1 / 137.035999
MPL_EV = 2.435e27
H0_EV = 2.1332e-33 * H_LITTLE
RHO_DE_EV4 = 3 * ODE * MPL_EV ** 2 * H0_EV ** 2


def evolve(m2, f2, th_i, a0=1e-4):
    """Units: H0 = 1, M_Pl = 1. phi = f2 theta. Returns a, theta(a), w(a), Omega_DE(a=1)."""
    def rhs(N, y):
        th, dth = y                                  # dth = dtheta/dN
        a = np.exp(N)
        V = m2 ** 2 * f2 ** 2 * (1 + np.cos(th))
        rho_bg = 3 * (OM / a ** 3 + OR / a ** 4)
        # H^2 = (rho_bg + V) / (3 - f2^2 dth^2 / 2)
        H2 = (rho_bg + V) / (3 - 0.5 * f2 ** 2 * dth ** 2)
        p_bg = 3 * OR / a ** 4 / 3
        kin = 0.5 * f2 ** 2 * H2 * dth ** 2
        Hdot_over_H2 = -0.5 * (rho_bg + p_bg + 2 * kin) / H2
        ddth = -(3 + Hdot_over_H2) * dth + m2 ** 2 * np.sin(th) / H2
        return [dth, ddth]

    Ns = np.linspace(np.log(a0), 0, 2000)
    s = solve_ivp(rhs, [Ns[0], 0], [th_i, 0.0], t_eval=Ns, method="DOP853",
                  rtol=1e-10, atol=1e-14)
    a = np.exp(s.t)
    th, dth = s.y
    V = m2 ** 2 * f2 ** 2 * (1 + np.cos(th))
    rho_bg = 3 * (OM / a ** 3 + OR / a ** 4)
    H2 = (rho_bg + V) / (3 - 0.5 * f2 ** 2 * dth ** 2)
    kin = 0.5 * f2 ** 2 * H2 * dth ** 2
    w = (kin - V) / (kin + V)
    ode = (kin + V) / (3 * H2)
    return a, th, w, ode[-1], H2[-1]


def solve_f2(m2, th_i):
    """f2 such that the field gives Omega_DE = 0.685 with H(today) = H0"""
    g = lambda lf: evolve(m2, np.exp(lf), th_i)[4] - 1.0
    return np.exp(brentq(g, np.log(0.05), np.log(50), xtol=1e-10))


def cpl(a, w):
    """least-squares w(a) = w0 + wa (1 - a) over 0 < z < 2.5"""
    sel = a >= 1 / 3.5
    A = np.vstack([np.ones(sel.sum()), 1 - a[sel]]).T
    return np.linalg.lstsq(A, w[sel], rcond=None)[0]


def q1_q4():
    print(BAR + "\n Q1/Q4  Hilltop holonomy as the whole dark energy (no Lambda)\n" + BAR)
    print("   theta_2i from the inflationary random walk, s0 sqrt(60) with s0 = H/(2 pi f2):")
    print("   for f2 ~ M_Pl and H_nuc <= 4.7e13 GeV (r < 0.036): theta_2i <~ 3e-5.")
    print(f"   {'m2/H0':>6s} {'theta_2i':>9s} {'f2/M_Pl':>8s} {'w0':>7s} {'wa':>7s}"
          f" {'Om_DE':>6s} {'dtheta':>7s}")
    rows = []
    for m2 in (1.0, 3.0, 6.0, 10.0, 15.0, 20.0, 30.0):
        for th_i in (1e-15, 1e-10, 3e-5, 1e-2):
            try:
                f2 = solve_f2(m2, th_i)
            except ValueError:
                print(f"   {m2:6.1f} {th_i:9.0e}   no solution")
                continue
            a, th, w, ode, _ = evolve(m2, f2, th_i)
            w0, wa = cpl(a, w)
            d_th = th[-1] - th_i
            rows.append((m2, th_i, f2, w0, wa, d_th))
            print(f"   {m2:6.1f} {th_i:9.0e} {f2:8.3f} {w0:7.3f} {wa:7.3f} {ode:6.3f} {d_th:7.3f}")
    return rows


def q4_locus():
    print("\n" + BAR + "\n Q4  Predicted (w0, wa) locus (random-walk offset, not fitted)\n" + BAR)
    print("   theta_2i = H_nuc sqrt(60)/(2 pi f2) at its largest (H_nuc = 4.7e13 GeV),")
    print("   iterated with f2; one free input remains: m2.")
    for m2 in (11.0, 12.0, 12.5, 13.0, 13.5, 14.0, 15.0):
        f2 = 0.09
        for _ in range(3):
            th_i = 4.7e13 * np.sqrt(60) / (2 * np.pi * f2 * 2.435e18)
            f2 = solve_f2(m2, th_i)
        a, th, w, ode, _ = evolve(m2, f2, th_i)
        w0, wa = cpl(a, w)
        print(f"   m2 = {m2:5.1f} H0: theta_2i = {th_i:.1e}, f2 = {f2:.3f} M_Pl,"
              f" w0 = {w0:+.3f}, wa = {wa:+.3f}")
    print("   -> a one-parameter curve from (w0, wa) = (-1, 0) toward (-0.5, -0.9):")
    print("      thawing hilltop quintessence. Reaching w0 > -0.95 needs m2 within")
    print("      ~10% of 12-14 H0: the coincidence problem, restated as a mass.")


def q2_wgc(rows):
    print("\n" + BAR + "\n Q2  Weak gravity conjecture for U(1)_B' on STUR's circle L\n" + BAR)
    print("   electric WGC: a charged state with M_c <= sqrt(2) g4' M_Pl, g4' = 1/(f2 L)")
    print("   i.e. M_c L <= sqrt(2) M_Pl / f2.  A charged bulk state of mass M_c")
    print("   contributes ~ e^(-M_c L)/L^4 to V2, so V2 = rho_DE needs every charged")
    print("   state to have M_c L >= -ln(rho_DE L^4):")
    for linv_gev in (875.0, 1e6, 1e10, 4e12):
        L4 = (1 / (linv_gev * 1e9)) ** 4
        need = -np.log(RHO_DE_EV4 * L4)
        print(f"     1/L = {linv_gev:8.0e} GeV: M_c L >= {need:5.1f}")
    f_typ = [r[2] for r in rows if r[3] < -0.7]
    print(f"   rows with w0 < -0.7 have f2 = {min(f_typ):.2f}-{max(f_typ):.2f} M_Pl, so WGC")
    print(f"   allows M_c L <= {np.sqrt(2) / max(f_typ):.2f}-{np.sqrt(2) / min(f_typ):.2f}.")
    print("   -> the WGC state would have M_c L ~ 1 and add ~1/L^4 to V2, more than")
    print(f"      rho_DE by a factor >= {1 / (RHO_DE_EV4 * (1 / 875e9) ** 4):.0e}. Q2 FAILS.")
    print("   Escape: a WGC multiplet with exact Bose-Fermi degeneracy cancels in V2;")
    print("   it must be degenerate to ~1 part in 1e58, i.e. unbroken bulk")
    print("   supersymmetry for that multiplet. Recorded as a loophole, not a pass.")
    print("   Conversely f2 small enough for the WGC (f2 <~ sqrt(2)/135 ~ 0.01 M_Pl)")
    for f2 in (0.01, 0.03):
        m2 = np.sqrt(1.5 * ODE) / f2
        print(f"   f2 = {f2} M_Pl -> m2 = {m2:.0f} H0: the field rolled long ago.")
    for m2 in (34.0, 100.0):
        th_i = 4.7e13 * np.sqrt(60) / (2 * np.pi * np.sqrt(1.5 * ODE) / m2 * 2.435e18)
        f2 = solve_f2(m2, th_i)
        a, th, w, ode, _ = evolve(m2, f2, th_i)
        w0, wa = cpl(a, w)
        print(f"   m2 = {m2:.0f} H0 (theta_2i = {th_i:.0e}): Omega_DE = 0.685 needs f2 = {f2:.3f},"
              f" but w(today) = {w[-1]:+.2f}, CPL w0 = {w0:+.2f}")
    print("   -> the field has rolled and oscillates (matter-like): Q1 fails.")
    print("   -> Q1 (w0 < -0.7) and Q2 (WGC) cannot hold together.")


def q3_rotation(rows):
    print("\n" + BAR + "\n Q3  Extra late-time rotation if theta_2 couples to photons\n" + BAR)
    print("   Delta beta_DE = (k2 alpha / 2 pi) Delta theta_2 since recombination;")
    print("   it adds to beta at every l (Delta beta_tomography unchanged).")
    worst = None
    for (m2, th_i, f2, w0, wa, d_th) in rows:
        if th_i == 3e-5:
            db = np.degrees(ALPHA / (2 * np.pi) * d_th)
            print(f"   m2 = {m2:4.0f} H0, w0 = {w0:+.3f}: k2 = 1 adds {db:.4f} deg"
                  f" ({100 * db / 0.20905:.1f}% of alpha/2)")
            if w0 > -0.95 and (worst is None or db < worst):
                worst = db
    if worst is None:
        print("   -> no random-walk row departs visibly from w = -1; where theta_2 stays")
        print("      frozen the extra rotation is negligible, so Q3 passes trivially there.")
    else:
        print(f"   -> wherever w0 > -0.95 the extra rotation is >= {worst:.3f} deg: then k2 = 0")
        print("      is required (a new discrete choice), else |beta| != alpha/2.")


def ds_conjecture(rows):
    print("\n" + BAR + "\n dS  Refined de Sitter conjecture at the hilltop\n" + BAR)
    f_typ = sorted({round(r[2], 3) for r in rows if r[3] < -0.7})
    for f2 in (f_typ[0], f_typ[-1]):
        print(f"   f2 = {f2:.2f} M_Pl: M_Pl^2 |V''|/V = 1/(2 f2^2) = {1 / (2 * f2 ** 2):.2f}")
    print("   The conjecture asks for >= c' = O(1): mild tension, reported only.")


def main():
    rows = q1_q4()
    q4_locus()
    q2_wgc(rows)
    q3_rotation(rows)
    ds_conjecture(rows)


if __name__ == "__main__":
    main()
