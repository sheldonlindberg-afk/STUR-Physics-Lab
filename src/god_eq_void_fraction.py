#!/usr/bin/env python3
"""
God-equation search, front 14: is timescape's void fraction the real cosmic web's?

Front 13 left timescape (dark energy as an averaging artifact) with an internal question:
the Pantheon+ supernovae want a present void volume fraction f_v0 = 0.853 +- 0.039
(official standardization) or 0.737 +- 0.029 (Seifert et al. 2024), and the Planck CMB
wants 0.695 (+0.041 -0.051).  The void fraction is not a free number: it is how much of
space is empty.  Galaxy surveys measure it.  Does the real cosmic web agree?

Timescape's own definition (LIT, retrieved, Wiltshire 2007 NJP 9 377, gr-qc/0702082):
voids are the DOMINANT voids, diameters ~30 h^-1 Mpc and larger; "minivoids" (~1 Mpc)
inside the filamentary walls "contribute to the expansion of the bubble walls", i.e. they
count as WALL.  In the tracker solution the voids are taken as empty and the walls hold
the matter.

Measurements (LIT, retrieved), SDSS DR7 volume-limited sample (M_r < -20.09, z < 0.107):
  Pan et al. 2012 (arXiv:1103.4156), VoidFinder, voids r > 10 h^-1 Mpc:
      62% of volume, 7% of galaxies; interiors delta < -0.85.  LCDM mocks: "similar".
  Douglass et al. 2023 (arXiv:2202.01226), VAST, Planck-2018 distances:
      VoidFinder        61% of volume, ~18% of galaxies
      V2/VIDE           63-68% of volume, ~64% of galaxies
      V2/REVOLVER       86-90% of volume, ~82% of galaxies
  (V2 = watershed/Voronoi zones; every point is in some basin, walls included.)
  64 Horizon Run 4 LCDM mocks agree with the data (Douglass et al.).

Computed here:
  V1  how empty each algorithm's "voids" are: mean galaxy density contrast
      delta_v = (galaxy fraction / volume fraction) - 1.
  V2  redshift: the survey sees f_v at z_eff ~ 0.085, not today; the tracker f_v(t)
      (front 13 / Wiltshire 2009, retrieved) maps it to f_v0.
  V3  what a void phase of volume 0.695 / 0.737 / 0.853 would have to contain.  Model:
      lognormal density field (Coles & Jones 1991, KNOWN), whose "Lorenz curve" (volume
      fraction V of the emptiest regions holding mass fraction m) is exact:
          V(m) = Phi( Phi^-1(m) + s ),   s^2 = Var ln(1 + delta)          (FOLLOWS)
      s is calibrated on each VoidFinder (volume, galaxy) pair, so the extrapolation is
      anchored to the data, in GALAXIES (a biased tracer; see caveats).
"""
import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

import god_eq_timescape as T

# (label, volume fraction (lo, hi), galaxy fraction)   LIT, retrieved
CATALOGS = [
    ("Pan+2012 VoidFinder", (0.62, 0.62), 0.07),
    ("Douglass+2023 VoidFinder", (0.61, 0.61), 0.18),
    ("Douglass+2023 V2/VIDE", (0.63, 0.68), 0.64),
    ("Douglass+2023 V2/REVOLVER", (0.86, 0.90), 0.82),
]
TARGETS = [("Planck CMB (Duley+2013)", 0.695), ("SNe, Seifert+2024", 0.737),
           ("SNe, official Pantheon+ (front 13)", 0.853)]
Z_MAX = 0.107


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# --------------------------------------------------------------------------- V2
def z_eff_volume_median(zmax=Z_MAX, n=20001):
    """Redshift that splits the comoving survey volume in half (flat LCDM Om=0.315)."""
    z = np.linspace(0, zmax, n)
    chi = T.lcdm_DL(z, 0.315) / (1 + z)
    V = chi ** 3
    return np.interp(0.5 * V[-1], V, z)


def fv_at_z(f0, z):
    """Tracker void fraction seen at redshift z, for present value f0."""
    b, t0 = T.ts_params(f0)
    t = brentq(lambda t: T.ts_z(t, f0) - z, 1e-6 * t0, t0)
    return 3 * f0 * t / (3 * f0 * t + (1 - f0) * (2 + f0))


def f0_from_fv_at_z(fv, z):
    return brentq(lambda f0: fv_at_z(f0, z) - fv, 0.05, 0.99)


# --------------------------------------------------------------------------- V3
def lorenz_V(m, s):
    """Volume fraction of the emptiest lognormal regions holding mass fraction m."""
    return norm.cdf(norm.ppf(m) + s)


def lorenz_m(V, s):
    return norm.cdf(norm.ppf(V) - s)


def s_from_pair(V, m):
    return norm.ppf(V) - norm.ppf(m)


def lorenz_mc(s, m, n=2_000_000, seed=1):
    """CHECK: Monte-Carlo lognormal cells (equal volume), sort by density."""
    rng = np.random.default_rng(seed)
    rho = np.exp(rng.normal(-s * s / 2, s, n))
    rho.sort()
    cm = np.cumsum(rho) / rho.sum()
    return np.searchsorted(cm, m) / n


# --------------------------------------------------------------------------- main
def main():
    banner("V1  How empty are the measured 'voids'?  (mean galaxy density contrast)")
    print("   catalog                        volume    galaxies   delta_v (galaxies)")
    v1 = []
    for lab, (vlo, vhi), g in CATALOGS:
        d = [g / v - 1 for v in (vlo, vhi)]
        v1.append((lab, vlo, vhi, g, min(d), max(d)))
        vs = f"{vlo:.2f}" if vlo == vhi else f"{vlo:.2f}-{vhi:.2f}"
        ds = f"{d[0]:+.2f}" if vlo == vhi else f"{max(d):+.2f} .. {min(d):+.2f}"
        print(f"   {lab:30s} {vs:9s}  {g:5.2f}      {ds}")
    print("   -> only VoidFinder's voids are underdense (delta_v = -0.70 to -0.89).  The V2")
    print("      watershed 'voids' sit at 0.93-1.02 of the MEAN galaxy density: they are")
    print("      basins that include walls, not empty regions.  Their 0.86-0.90 is not a")
    print("      timescape void fraction.")

    banner("V2  Redshift: survey value -> present-day f_v0 (timescape tracker)")
    zeff = z_eff_volume_median()
    print(f"   volume-median redshift of the z < {Z_MAX} sample: z_eff = {zeff:.4f}")
    for f0 in (0.695, 0.853):
        print(f"   f_v0 = {f0:.3f}  ->  f_v(z_eff) = {fv_at_z(f0, zeff):.4f}")
    meas = 0.615
    f0m = f0_from_fv_at_z(meas, zeff)
    print(f"   measured underdense-void fraction 0.61-0.62 (take {meas}) -> f_v0 = {f0m:.3f}")
    print("   The correction is ~+0.01: redshift does not close any gap.")

    banner("V3  What would a void phase of the required size have to contain?")
    mc_err = 0.0
    for lab, (v, _), g in CATALOGS[:2]:
        s = s_from_pair(v, g)
        chk = lorenz_mc(s, g)
        mc_err = max(mc_err, abs(chk - v))
        print(f"   calibration {lab}: s = {s:.3f}   (CHECK Monte Carlo V(m) = {chk:.4f}"
              f" vs {v:.4f})")
    print("\n   target f_v0                           galaxy fraction in voids   delta_v")
    v3 = []
    for lab, f in TARGETS:
        fz = fv_at_z(f, zeff)
        ms = [lorenz_m(fz, s_from_pair(v, g)) for _, (v, _), g in CATALOGS[:2]]
        ds = [m / fz - 1 for m in ms]
        v3.append((lab, f, min(ms), max(ms), min(ds), max(ds)))
        print(f"   {lab:36s} {f:.3f}   {min(ms):.2f} - {max(ms):.2f}"
              f"               {min(ds):+.2f} .. {max(ds):+.2f}")
    print("   (Evaluated at f_v(z_eff), i.e. what the SDSS volume would show.)")

    banner("V4  Verdict")
    print(f"   Census of underdense voids: 0.61-0.62 of the volume -> f_v0 = {f0m:.2f} today.")
    print("   Definitional systematic, both directions: VoidFinder keeps voids down to r = 10")
    print("   h^-1 Mpc, below Wiltshire's dominant ~30 Mpc-diameter scale (pushes f_v0 DOWN);")
    print("   it counts only galaxy-free spheres, missing low-density volume at void edges")
    print("   (pushes f_v0 UP).  The two VoidFinder runs disagree on the galaxy content (7%")
    print("   vs 18%), which sets the spread of the extrapolation in V3.")
    for lab, f in TARGETS:
        print(f"   {lab:36s} needs {f:.3f}: {f - f0m:+.3f} above the census")
    sn, cm = v3[2], v3[0]
    print(f"   A void phase of 0.853 would sit at delta_v = {sn[4]:+.2f} .. {sn[5]:+.2f}:"
          " from 'as empty as")
    print("   VoidFinder's voids' (Pan anchor) to 'half the mean density' (Douglass anchor).")
    print(f"   A void phase of 0.695 sits at {cm[4]:+.2f} .. {cm[5]:+.2f}: as empty as the "
          "measured voids.")
    print("   VERDICT: the cosmic web supports f_v0 ~ 0.64-0.70, consistent with timescape's")
    print("   CMB value; Seifert et al.'s 0.737 is marginal; the official-Pantheon+ 0.853 is")
    print("   strained (needs voids much fuller than measured on one anchor), not excluded.")
    print("   LCDM mocks reproduce the same census, so this is a consistency test OF")
    print("   timescape, not evidence FOR it over LCDM.")
    return dict(v1=v1, zeff=zeff, f0m=f0m, v3=v3, mc_err=mc_err)


if __name__ == "__main__":
    main()
