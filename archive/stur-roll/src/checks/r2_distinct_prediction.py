#!/usr/bin/env python3
"""
Refinement round 2, item 1: is there an observable that distinguishes
STUR-ROLL from the hilltop domain-wall scenario of Lee, Murai, Takahashi &
Yin (LMTY, PRD 112, 043538, 2025)?  See docs/R2_DISTINCT_PREDICTION.md.

Both models: L = (c alpha/4 pi) theta F Ftilde, theta starts at a hilltop and
rolls by pi after recombination, beta = c alpha/2.  So any discriminator must
come from what STUR-ROLL FIXES that LMTY leaves free. Checks:

  D1  the theta-mass window that STUR-ROLL's derived amplitude requires
      (lands at pi by today; still at the hilltop at recombination)
  D2  the tomographic difference Delta beta = beta_reio - beta_rec across
      that window, versus a late-rolling (dark-energy-like) hilltop axion
  D3  energy budget: can theta contribute to late-time evolving dark energy?
  D4  seed spectrum: theta mass during nucleation versus H_nuc
  D5  gravitational waves from the T_c sign flip
Requires numpy, scipy. Runs in ~1 min (the reionization projection).
"""
import os
import sys

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import stur_final as F  # noqa: E402

BAR = "=" * 78
KFAC = F.ALPHA / (2 * np.pi)                      # k = 1
HALF = np.degrees(F.ALPHA) / 2                    # alpha/2 in degrees
MPL = 2.435e27                                    # reduced Planck mass, eV
RHO_DE = F.OL * 3 * MPL ** 2 * F.H0_EV ** 2       # eV^4
H0 = F.H0_EV


def theta_of_z(m, seed):
    frac, b_rec, hist = F.roll(m, seed)
    th0 = frac * np.pi
    th = lambda z: th0 - np.radians(hist(z)) / KFAC
    return frac, b_rec, th


def z_cross(th, level):
    """redshift at which theta(z) first exceeds `level` (None if never)"""
    if th(0.0) < level:
        return None
    return brentq(lambda z: th(z) - level, 0.0, 9.9e3)


def d1_d2(R):
    print(BAR + "\n D1/D2  STUR-ROLL theta-mass window and tomography (seed 1e-4)\n"
          + BAR)
    print("   beta_reio: reionization-only projection of stur_final (Reion, l = 2;")
    print("   agrees with CLASS to <= 0.004 deg for l <= 5)")
    print(f"   {'m [eV]':>8s} {'lands/pi':>9s} {'theta(z*)':>10s} {'z_roll':>8s}"
          f" {'beta_rec':>9s} {'beta_reio':>10s} {'Delta beta':>11s}  alpha/2 derived?")
    rows = []
    for m in (3e-33, 1e-32, 3e-32, 1e-31, 2e-31, 3e-31, 1e-30, 3e-30, 1e-29, 3e-29,
              1e-28):
        frac, b_rec, th = theta_of_z(m, 1e-4)
        th_star = th(F.Z_STAR)
        zr = z_cross(th, np.pi / 2)
        _, _, hist = F.roll(m, 1e-4)
        b_reio = R.beta_l(hist)[2]
        db = b_reio - b_rec
        ok = abs(b_rec - HALF) / HALF < 0.03 and abs(th_star) < 0.05
        rows.append((m, frac, th_star, zr, b_rec, b_reio, db, ok))
        zs = f"{zr:8.1f}" if zr is not None else "  > now"
        print(f"   {m:8.0e} {frac:9.4f} {th_star:10.2e} {zs} {b_rec:9.4f}"
              f" {b_reio:10.4f} {db:+11.4f}  {'yes' if ok else 'no'}")
    win = [r for r in rows if r[7]]
    print(f"   -> derived-amplitude window (|beta_rec - alpha/2| < 3%, theta(z*) < 0.05):")
    print(f"      m from {win[0][0]:.0e} to {win[-1][0]:.0e} eV on this grid;"
          f" z_roll from {win[0][3]:.0f} to {win[-1][3]:.0f}")
    dbs = [r[6] for r in win]
    print(f"      Delta beta in [{min(dbs):+.3f}, {max(dbs):+.3f}] deg"
          f" = [{min(dbs) / HALF:+.2f}, {max(dbs) / HALF:+.2f}] x alpha/2")
    print("   -> a hilltop axion that rolls after reionization (m <~ 1e-32 eV,")
    print("      the dark-energy-like regime) has Delta beta ~ 0 but has NOT")
    print("      reached pi today, so its beta is below alpha/2 for c = 1.")
    print("   LiteBIRD: sigma(Delta beta) ~ 0.05 deg (Sherwin & Namikawa 2023).")
    print(f"      STUR-ROLL Delta beta / sigma ~ {max(dbs) / 0.05:+.1f} to"
          f" {min(dbs) / 0.05:+.1f} sigma from zero.")
    return win


def d3(win):
    print("\n" + BAR + "\n D3  Energy budget: can theta act as late-time dark energy?\n"
          + BAR)
    print(f"   rho_DE today = {RHO_DE:.2e} eV^4")
    print("   hilltop energy 2 m^2 f^2, f at the wall bound f_max = sqrt(1e18/(8m)) eV")
    print(f"   {'m [eV]':>8s} {'f_max [GeV]':>12s} {'2m^2f^2/rho_DE':>15s}"
          f" {'z_roll':>8s} {'Omega_theta today':>18s}")
    for m, *_r in win:
        fmax = np.sqrt(1e18 / (8 * m))
        vh = 2 * m ** 2 * fmax ** 2
        zr = _r[2]
        rho_m0 = F.OM * 3 * MPL ** 2 * H0 ** 2
        # after the roll theta oscillates (matter-like); fraction of total today
        om_today = vh / (1 + zr) ** 3 / (3 * MPL ** 2 * H0 ** 2)
        print(f"   {m:8.0e} {fmax / 1e9:12.1e} {vh / RHO_DE:15.1e} {zr:8.1f}"
              f" {om_today:18.1e}")
    print("   -> in the derived-amplitude window theta rolls at z ~ 4-300, above")
    print("      the DESI redshift range (z < 2.3), holding <~ 1% of rho_DE before")
    print("      the roll; today it is matter-like with Omega_theta <~ 1e-5. theta")
    print("      CANNOT be (part of) the evolving dark energy suggested by DESI.")
    print("   NOTE: the hilltop delay (roll at H ~ m/20, not m/3) makes Omega_theta")
    print("      ~40-60x larger than stur_final section C's 6 (f/M_Pl)^2 estimate;")
    print("      still <~ 1e-5, so the 'invisible except through beta' claim holds.")


def d4():
    print("\n" + BAR + "\n D4  Seed spectrum: theta mass during nucleation\n" + BAR)
    print("   In de Sitter the scalar dominates and V''(0) ~ m^2 x O(1) (same")
    print("   e^-ML suppression), while H_nuc > H_c ~ 15/L >= 7.5e4 GeV.")
    for m in (3e-31, 1e-29):
        print(f"   m = {m:.0e} eV: m / H_nuc <~ {m / 7.5e13:.0e}  -> massless spectrum")
    print("   -> delta theta = H_nuc/(2 pi f) per e-fold, scale invariant: the")
    print("      same seed statistics as an exact-hilltop start with inflationary")
    print("      fluctuations (Gonzalez, Kitajima, Takahashi, Yin 2023).")
    print("   Difference in the MEAN: STUR-ROLL starts exactly at theta = 0 (the")
    print("   minimum), so the patch mean is pure fluctuation; LMTY 'near a")
    print("   hilltop' allows a classical offset theta_bar. Probability that our")
    print("   Hubble volume contains a wall ~ sqrt(2/pi) sqrt(dN / N_early):")
    m = 1e-30
    _, _, th = theta_of_z(m, 1e-4)
    zr = z_cross(th, np.pi / 2)
    hr = F.hubble(-np.log1p(zr))
    dN = np.log(hr / (1 + zr) / H0)
    for ne in (10, 30, 60):
        p = np.sqrt(2 / np.pi) * np.sqrt(dN / ne)
        print(f"   m = 1e-30, dN = ln(a H|roll / a0 H0) = {dN:.2f}, N_early = {ne:2d}:"
              f"  P ~ {p:.2f}")
    print("   -> probabilistic, depends on the unknown N_early; with theta_bar = 0")
    print("      exactly it equals the exact-hilltop LMTY case. Not a discriminator.")


def d5():
    print("\n" + BAR + "\n D5  Gravitational waves from the T_c sign flip\n" + BAR)
    for linv, m, f in ((5e12, 1e-30, 3.5e23), (1e22, 3e-31, 6.5e23)):
        tc = 9.8 * linv
        rho_r = np.pi ** 2 / 30 * 106.75 * tc ** 4
        a_pt = 2 * m ** 2 * f ** 2 / rho_r
        print(f"   1/L = {linv / 1e9:.0e} GeV: T_c = {tc / 1e9:.1e} GeV,"
              f" Delta V / rho_rad <= {a_pt:.0e}")
    print("   -> only the theta-dependent part flips sign; the heavy-field free")
    print("      energy is smooth. No phase transition strength, no GW signal.")


if __name__ == "__main__":
    R = F.Reion()
    win = d1_d2(R)
    d3(win)
    d4()
    d5()
