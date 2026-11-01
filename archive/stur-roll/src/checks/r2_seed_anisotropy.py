#!/usr/bin/env python3
"""
Refinement round 2, item 4: seed statistics of theta, domain walls, and
anisotropic / time-dependent birefringence.  See docs/R2_SEED_ANISOTROPY.md.
Requires numpy, scipy. Runs in ~1 min.

Model (stated, not derived from the 5D action):
  * During the de Sitter phase (Hubble H) theta is effectively massless
    (curvature of the scalar-dominated potential ~ m^2 << H^2), so it
    random-walks: P_theta(k) = s0^2 per ln k, s0 = H / (2 pi f).
  * N_extra = number of e-folds of that phase BEFORE our present horizon
    scale exited.  It sets the patch mean theta_bar ~ s0 sqrt(N_extra).
  * theta is frozen (m << H) until H ~ m; modes inside the horizon at the
    roll have decayed, so the sign pattern is the seed field smoothed on
    R_s = comoving Hubble radius when H = m (Gaussian window).
  * After the roll a domain of sign s sits at s * Theta(z), Theta = roll
    profile (>= 0).  Reionization photon from direction n:
        beta_re(n) = (alpha/2pi) [ s_obs theta_0 - s(n) Theta(z_re) ]
    so the anisotropic part is -(alpha/2pi) Theta(z_re) s(n).
    For a partially rolled (linear) field this is an UPPER bound.
"""
import os
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
from scipy.special import eval_legendre

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import stur_final as F  # noqa: E402

BAR = "=" * 78
KF = F.ALPHA / (2 * np.pi)            # beta = KF * Delta theta  (k = 1)
DEG = 180 / np.pi
C_H0_MPC = 299792.458 / 67.36         # c / H0 in Mpc
Z_RE = 7.69                           # tanh reionization for tau = 0.0544 (stur_final)
HBAR_EV_S = 6.582119569e-16
MPL_EV = 2.435e27                     # reduced Planck mass, eV

# --- verified bounds (see docs/R2_SEED_ANISOTROPY.md for status) ----------
# D_L = L(L+1) C_L^aa / 2pi = A_CB x 1e-4 rad^2  (BICEP/Keck XVII convention)
A_CB_ACT_DR6 = 0.15        # 95% upper limit, ACT DR6 (2608.27458); convention assumed
A_PLANCK_DEG2 = 0.104      # Planck 2018 (Gruppuso et al.), deg^2, 95%


def E(z):
    return F.hubble(-np.log1p(z)) / F.H0_EV


def chi(z):                                    # comoving distance, Mpc
    return C_H0_MPC * quad(lambda x: 1 / E(x), 0, z, limit=200)[0]


def z_of_H(m):                                 # redshift where H = m
    return brentq(lambda z: F.hubble(-np.log1p(z)) - m, 0.0, 1e6)


def theta_profile(m, seed):
    """same equation as stur_final.roll; returns theta(z) and amplitude today"""
    def rhs(N, y):
        H = F.hubble(N)
        dlnH = (F.hubble(N + 1e-5) - F.hubble(N - 1e-5)) / (2e-5 * H)
        return [y[1], -(3 + dlnH) * y[1] + (m / H) ** 2 * np.sin(y[0])]
    sol = solve_ivp(rhs, [np.log(1e-4), 0.0], [seed, 0.0], method="DOP853",
                    rtol=1e-10, atol=min(1e-13, 1e-3 * seed), dense_output=True)
    th = lambda z: sol.sol(-np.log1p(z))[0]
    th0, dth0 = sol.sol(0.0)
    # oscillation amplitude about pi today: theta' = H dtheta/dN, omega ~ m
    amp = np.hypot(th0 - np.pi, F.H0_EV * dth0 / m)
    return th, th0, amp


def corr_fn(r, Rs, N_extra, k0):
    """rho(r) = xi(r)/xi(0) for P = const per ln k, k in [k0 e^-N, inf), W^2 = exp(-k^2 Rs^2)"""
    lo = k0 * 1e-3
    hi = 8.0 / Rs
    u = np.linspace(np.log(lo), np.log(hi), 3000)
    k = np.exp(u)
    w = np.exp(-(k * Rs) ** 2)
    du = u[1] - u[0]
    base = max(N_extra + np.log(k0 / lo), 0.0) if N_extra > -np.log(1e-3) else None
    if base is None:                           # k_min above lo: start there
        kmin = k0 * np.exp(-N_extra)
        u = np.linspace(np.log(kmin), np.log(hi), 3000)
        k = np.exp(u)
        w = np.exp(-(k * Rs) ** 2)
        du = u[1] - u[0]
        base = 0.0
    xi0 = base + np.sum(w) * du
    r = np.atleast_1d(r)
    kr = np.outer(r, k)
    sinc = np.sinc(kr / np.pi)
    xi = base + (sinc * w).sum(1) * du
    return np.clip(xi / xi0, -1, 1)


def theta_reio(th):
    """|theta| averaged over the reionization visibility g = dtau/dz e^-tau (z < 30)"""
    z = np.linspace(0.0, 30.0, 3001)
    d = F.dtau_dz(z, Z_RE)
    tau = np.concatenate([[0], np.cumsum(0.5 * (d[1:] + d[:-1]) * np.diff(z))])
    g = d * np.exp(-tau)
    return abs(np.sum(g * th(z)) / np.sum(g))


def sign_cl(Rs, chi_re, N_extra, k0, Lmax=100, nq=2000):
    x, wq = leggauss(nq)
    gam = np.arccos(x)
    r = 2 * chi_re * np.sin(gam / 2)
    rho = corr_fn(r, Rs, N_extra, k0)
    ss = 2 / np.pi * np.arcsin(rho)            # <s s'> for sign of a Gaussian field
    Ls = np.arange(0, Lmax + 1)
    cl = np.array([2 * np.pi * np.sum(wq * eval_legendre(L, x) * ss) for L in Ls])
    return Ls, cl


def main():
    print(BAR + "\n R2.4  Seed statistics, walls, anisotropic and time-dependent beta\n" + BAR)
    chi_re, chi_st = chi(Z_RE), chi(F.Z_STAR)
    k0 = 1 / C_H0_MPC                          # present horizon scale (a0 H0 / c)
    print(f"   chi(z_re = {Z_RE}) = {chi_re:.0f} Mpc,  chi(z*) = {chi_st:.0f} Mpc,"
          f"  c/H0 = {C_H0_MPC:.0f} Mpc")

    # ---- 1. seed magnitude and the hilltop requirement -------------------
    print("\n 1. Seed and hilltop requirement")
    print("   theta frozen at theta_i until H ~ m; Delta theta = pi - |theta_i|, so")
    print("   beta = (alpha/2)(1 - |theta_i|/pi).  theta_i ~ s0 sqrt(N_tot) (random walk).")
    print(f"   {'s0 = H/2pi f':>14s} {'N_tot max for |dbeta| < 1%':>28s} {'< 3%':>10s}")
    for s0 in (3e-1, 3e-2, 4e-3, 1e-4, 1e-8):
        n1, n3 = (0.01 * np.pi / s0) ** 2, (0.03 * np.pi / s0) ** 2
        print(f"   {s0:14.0e} {n1:28.2e} {n3:10.2e}")
    print("   -> the top of stur_final's seed window (s0 ~ 0.3) is excluded for any")
    print("      de Sitter phase longer than ~1e-3 e-folds; with >= 60 e-folds one")
    print(f"      needs s0 <~ {0.03 * np.pi / np.sqrt(60):.1e} (3%) or"
          f" {0.01 * np.pi / np.sqrt(60):.1e} (1%).")
    # GENESIS v10 (archived) R^2 inflation: r = 0.00355 at N* = 55
    As, r = 2.1e-9, 0.00355
    Hinf = np.pi * 2.435e18 * np.sqrt(As * r / 2)
    fmin = Hinf * np.sqrt(55) / (2 * np.pi * 0.03 * np.pi)
    print(f"   Scenario: if the de Sitter phase is the archived GENESIS R^2 inflation")
    print(f"   (r = {r}, A_s = {As}), H_inf = {Hinf:.2e} GeV and N >= 55 requires")
    print(f"   f >~ {fmin:.1e} GeV (3%), vs section C upper limits 6.5e14 / 3.5e14 /")
    print("   1.1e14 GeV for m = 3e-31 / 1e-30 / 1e-29 eV.")
    print("   (Separately: the de Sitter minimum at theta = 0 does NOT pin theta,")
    print("    because its curvature ~ m^2 << H^2; the equilibrium spread")
    print("    3 H^4/(8 pi^2 m^2 f^2) would be enormous. Only finite N_tot keeps")
    print("    theta near 0.)")

    # ---- 2a. recombination anisotropy -----------------------------------
    print("\n 2a. Recombination photons: anisotropy from theta_i(n) at emission")
    print("   D_L = (alpha/2pi)^2 s0^2   (scale-invariant field on the sphere)")
    for s0 in (3e-1, 4e-3, 1e-4):
        D = KF ** 2 * s0 ** 2
        print(f"   s0 = {s0:6.0e}: D_L = {D:.1e} rad^2 = A_CB {D / 1e-4:.1e}"
              f"   (ACT DR6: A_CB < {A_CB_ACT_DR6})")
    print("   -> claim 'recombination rotation is isotropic' holds: <= 1e-3 of the bound.")

    # ---- 2b. reionization photons ---------------------------------------
    print("\n 2b. Reionization photons: sign domains (random-sign model, upper bound)")
    hdr = (f"   {'m [eV]':>8s} {'z(H=m)':>7s} {'R_s[Mpc]':>9s} {'Theta_re/pi':>11s}"
           f" {'N_extra':>7s} {'P_opp':>6s} {'rms[deg]':>8s} {'D_2':>8s} {'D_10':>8s}"
           f" {'D_30':>8s}  [D in 1e-4 rad^2]")
    print(hdr)
    rows = []
    for m in (1e-31, 3e-31, 1e-30, 3e-30, 1e-29):
        zr = z_of_H(m)
        Rs = (1 + zr) * C_H0_MPC / E(zr)
        th, _, _ = theta_profile(m, 1e-4)
        Th = min(theta_reio(th), np.pi)      # visibility-weighted, see header
        for Nx in (0, 60, 1e4):
            Ls, cl = sign_cl(Rs, chi_re, Nx, k0)
            D = Ls * (Ls + 1) * cl / (2 * np.pi) * (KF * Th) ** 2 / 1e-4
            var_sky = np.sum((2 * Ls[1:] + 1) * cl[1:]) / (4 * np.pi)
            rms = KF * Th * np.sqrt(var_sky) * DEG
            p_opp = np.arccos(corr_fn(chi_re, Rs, Nx, k0)[0]) / np.pi
            rows.append((m, Nx, D[10]))
            print(f"   {m:8.0e} {zr:7.1f} {Rs:9.0f} {Th / np.pi:11.3f} {Nx:7.0f}"
                  f" {p_opp:6.3f} {rms:8.4f} {D[2]:8.2e} {D[10]:8.2e} {D[30]:8.2e}")
    print("   Theta_re = |theta| averaged over the reionization visibility function;")
    print("   for m >= 1e-30 eV theta already oscillates about pi there, so the")
    print("   observer-domain rotation of reionization photons is ~0 (as stur_final")
    print("   states) and an opposite domain sits near -pi.")
    print("   P_opp = probability a reionization scattering point is in a domain of")
    print("   opposite sign to ours; rms = sky rms of the reionization-photon angle.")
    print("   Maximum possible: D_L <= (alpha/2)^2 = 1.3e-5 rad^2 = A_CB 0.13 at the")
    print("   very largest scales, falling with L.  Reionization E modes only")
    print("   carry l <~ 10, while ACT/SPT A_CB estimators use small-scale")
    print("   (recombination) E/B modes: they do NOT probe this signal.")
    print("   -> no part of the mass window is excluded by current A_CB limits.")
    print("   Note: for m >= 1e-30 eV a reionization point in an opposite domain")
    print("   is rotated by alpha = 0.418 deg (Delta theta = 2 pi), not ~0.")

    # ---- 3. walls today ---------------------------------------------------
    print("\n 3. Walls today (only if a sign change lies inside our horizon)")
    H0 = F.H0_EV
    for m in (3e-31, 1e-30, 1e-29):
        fmax = np.sqrt(1e18 / (8 * m))         # eV, section C
        for f_gev in (3e9, fmax / 1e9):
            sig = 8 * m * (f_gev * 1e9) ** 2   # eV^3
            om = sig * H0 / (3 * MPL_EV ** 2 * H0 ** 2)
            dT = sig / (4 * MPL_EV ** 2 * H0)  # 2 pi G sigma / H0
            print(f"   m = {m:.0e}, f = {f_gev:.1e} GeV: sigma = {sig:.1e} eV^3,"
                  f" Omega_wall ~ {om:.0e}, dT/T ~ {dT:.0e}")
    print("   -> at the section C upper edge dT/T ~ 3e-5: marginal, consistent with")
    print("      the order-of-magnitude bound sigma <~ (1 MeV)^3.  If no sign change")
    print("      lies inside our horizon (large N_extra) there is no wall bound.")

    # ---- 4. time-dependent beta today ------------------------------------
    print("\n 4. Time-dependent birefringence today (residual oscillation about pi)")
    yr = 3.15576e7
    for m in (3e-31, 1e-30, 3e-30):
        _, th0, amp = theta_profile(m, 1e-4)
        P = 2 * np.pi * HBAR_EV_S / m / yr
        A = KF * amp * DEG
        drift = A * 2 * np.pi * 5 / P          # max change over a 5-year baseline
        print(f"   m = {m:.0e} eV: period {P:.2e} yr, amplitude {A:.1e} deg,"
              f" max change in 5 yr {drift:.1e} deg")
    print("   -> unobservable (periods ~1e8 yr); the ACT DR6 time-dependent search")
    print("      targets oscillations within the 2017-2022 observing span.")


if __name__ == "__main__":
    main()
