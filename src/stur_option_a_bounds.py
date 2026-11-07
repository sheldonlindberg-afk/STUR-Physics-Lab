#!/usr/bin/env python3
"""
Option A confronted with stronger bounds.  Model (STUR POSTULATE, see stur_option_a.py):
potential noise white in time with variogram V(r) = 2 kappa (sqrt(r^2 + xi^2) - xi).

FOLLOWS: acceleration noise g = -grad Phi has
    <g_i(x,t) g_j(y,t')> = delta(t-t') H_ij(x-y),   H_ij(r) = kappa [delta_ij/s - r_i r_j/s^3],
    s = sqrt(r^2 + xi^2)      (long-range ~1/r: the 'string' variogram).

Bounds (inputs LIT, network-limited session: two inputs are scanned, not fixed):
 1. Kovachy et al. Nature 528, 530 (2015): Rb-87, max separation 0.54 m, ~1 s timescale,
    observed contrast 28%  ->  model may not remove more:  Gamma <= -ln 0.28 = 1.27.
    Pulse spacing T scanned 0.9-1.1 s (exact value not retrieved).
 2. LISA Pathfinder, Armano et al. PRL 120, 061101 (2018): differential acceleration noise
    ASD 1.74 fm s^-2 / sqrt(Hz) above 2 mHz; test masses 46 mm cubes.  Centre separation
    d scanned 0.30-0.45 m (nominal ~0.38 m; exact value not retrieved).
    White differential noise <da(t)da(t')> = Q delta(t-t') has one-sided PSD 2Q, so
    2Q <= (1.74e-15)^2,  Q = 2 (<H_xx>_self - <H_xx>_cross)  averaged over the cubes.
 3. Earth's heat flow 47 TW / 5.97e24 kg  ->  3 kappa / (2 xi) per kg below it.
 4. X-ray emission (Donadi et al. Nat. Phys. 17, 74 (2021)) - NOT binding here: for
    xi >> atomic size the noise accelerates each neutral atom uniformly, and a uniformly
    accelerated neutral system has no dipole radiation (FOLLOWS, Larmor).
"""
import numpy as np

hbar, amu = 1.054571817e-34, 1.66053906660e-27
rng = np.random.default_rng(7)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def Hxx(dx, dy, dz, xi):
    s2 = dx * dx + dy * dy + dz * dz + xi * xi
    return 1 / np.sqrt(s2) - dx * dx / s2**1.5           # per unit kappa


def lpf_Q_per_kappa(xi, d, L=0.046, n=400000):
    p = rng.uniform(-L / 2, L / 2, (4, n, 3))
    self_ = Hxx(*(p[0] - p[1]).T, xi).mean()
    cross = Hxx(*(p[2] - p[3] + np.array([d, 0, 0])).T, xi).mean()
    return 2 * (self_ - cross)


def gamma_per_kappa(m_amu, dxm, T, xi, n=20001):
    t = np.linspace(0, 2 * T, n)
    dx = dxm * (1 - abs(t - T) / T)
    return 0.5 * (m_amu * amu / hbar) ** 2 * np.trapezoid(2 * (np.sqrt(dx**2 + xi**2) - xi), t)


# ESTIMATE (not retrieved, network-limited): ground-based GW detector, arm 3995 m,
# strain ASD ~1e-23 /sqrt(Hz) near 100 Hz -> differential acceleration ASD = h L (2 pi f)^2.
LIGO_A = 1e-23 * 3995 * (2 * np.pi * 100) ** 2
R_EARTH = 6.371e6


def kappa_max(xi, d=0.38, TK=1.04):
    k_kov = 1.27 / gamma_per_kappa(87, 0.54, TK, xi)
    k_lpf = (1.74e-15) ** 2 / 2 / lpf_Q_per_kappa(xi, d)
    k_heat = 7.873e-12 * 2 * xi / 3
    k_ligo = LIGO_A**2 / 2 / lpf_Q_per_kappa(xi, 3995.0, L=0.2)
    return k_kov, k_lpf, k_heat, k_ligo


def main():
    global LIGO_A
    banner("B1  Joint bounds on (kappa, xi) and the best-case MAGIS/AION-class signal")
    geos = [("1 m x 2 s", 1.0, 2.0), ("3 m x 4 s", 3.0, 4.0), ("10 m x 10 s", 10.0, 10.0)]
    print(f"   LIGO-type differential acceleration ASD used (ESTIMATE): {LIGO_A:.2e} m s^-2/sqrt(Hz)")
    print("   Scan stops at xi = R_Earth: beyond it the apparatus co-moves with the noise and only")
    print("   the tidal part is observable (equivalence principle) - the formula below would be wrong.")
    print("   xi [m]    kappa_Kovachy  kappa_LPF    kappa_heat   kappa_LIGO   binding   " +
          "  ".join(f"Gamma({g[0]})" for g in geos))
    best = {g[0]: (0, None) for g in geos}
    for xi in np.r_[np.logspace(-7, 6.5, 28), R_EARTH]:
        kk, kl, kh, kg = kappa_max(xi)
        k = min(kk, kl, kh, kg)
        which = ["Kovachy", "LPF", "heat", "LIGO"][int(np.argmin([kk, kl, kh, kg]))]
        Gs = [k * gamma_per_kappa(87, dxm, T, xi) for _, dxm, T in geos]
        for (name, _, _), G in zip(geos, Gs):
            if G > best[name][0]:
                best[name] = (G, xi)
        print(f"   {xi:8.1e}  {kk:11.2e}  {kl:11.2e}  {kh:11.2e}  {kg:11.2e}  {which:8s}  " +
              "  ".join(f"{G:14.2e}" for G in Gs))
    print("\n   Best case over xi (Sr-87, illustrative geometries):")
    for name, (G, xi) in best.items():
        print(f"     {name:12s} max Gamma = {G:.2e}  at xi = {xi:.1e} m")

    print("\n   Sensitivity to the LIGO ESTIMATE (best Gamma, 3 m x 4 s, over xi <= R_Earth):")
    base = LIGO_A
    for f in [0.1, 1.0, 10.0, 100.0]:
        LIGO_A = base * f
        G = max(min(kappa_max(xi)) * gamma_per_kappa(87, 3.0, 4.0, xi)
                for xi in np.r_[np.logspace(-7, 6.5, 28), R_EARTH])
        print(f"     LIGO acceleration ASD x {f:6.1f}:  best Gamma = {G:.2e}")
    LIGO_A = base

    banner("B2  Robustness to the two inputs not retrieved (LPF separation, Kovachy T)")
    for d in [0.30, 0.38, 0.45]:
        for TK in [0.9, 1.1]:
            G = max(min(kappa_max(xi, d, TK)) * gamma_per_kappa(87, 3.0, 4.0, xi)
                    for xi in np.r_[np.logspace(-7, 6.5, 28), R_EARTH])
            print(f"   d = {d:.2f} m, T_Kovachy = {TK} s:  best Gamma(3 m x 4 s) = {G:.2e}")


if __name__ == "__main__":
    main()
