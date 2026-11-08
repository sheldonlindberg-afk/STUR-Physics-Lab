#!/usr/bin/env python3
"""
God-equation search, front 13: is dark energy a measurement artifact?
Timescape cosmology vs flat LCDM on the Pantheon+ supernovae.

Question.  "Dark energy" is the name for one measurement: supernovae look fainter than a
matter-only universe predicts.  Timescape (Wiltshire 2007-2009) says the faintness is an
averaging artifact: we live in a gravitationally bound region whose clocks run slow relative
to the voids that fill most of the volume, and fitting a smooth (FLRW) model to that lumpy
universe invents an acceleration.  It has NO dark energy and ONE parameter, the present void
volume fraction f_v0.  Flat LCDM has one parameter, Omega_m.  Same data, same likelihood:
which fits better?

Timescape tracker solution (KNOWN, Wiltshire 2009 PRD 80 123512; recalled, then checked
below).  Units: bare Hubble constant Hbar0 = 1, c = 1, volume-average time t.
    f_v(t)    = 3 f t / [3 f t + (1-f)(2+f)]                      void fraction
    t0        = (2+f)/3                                           (from f_v(t0) = f)
    abar/abar0 = (3t)^(2/3) [3 f t + (1-f)(2+f)]^(1/3) / (2+f)
    gamma(t)  = 1 + f_v/2 = 3(t+b) / (2t+3b),  b = 2(1-f)(2+f)/(9f)  (clock-rate lapse)
    1 + z     = (abar0/abar) (gamma/gamma0)                       (wall-observer redshift)
    D_A       = t^(2/3) [F(t0) - F(t)],  F' = 1/(gamma t^(2/3))   (closed form for F below)
    D_L       = (1+z)^2 D_A                                       (Etherington)
Dressed (what we measure) H0 = (4f^2 + f + 4) / (2(2+f)) * Hbar0.

Data (LIT, retrieved): Pantheon+ (Scolnic et al. 2022; Brout et al. 2022), the public
release github.com/PantheonPlusSH0ES/DataRelease: m_b_corr (standardized, bias-corrected
magnitudes) and the full 1701 x 1701 STAT+SYS covariance.  Downloaded on first run into
data/pantheon_plus/ (git-ignored, 34 MB).
    mu_model = 5 log10[ (1+z_hel)/(1+z) * D_L(z) ] + const   (Pantheon+ convention)
The absolute magnitude / H0 offset is marginalized analytically (flat prior), so only the
SHAPE of D_L(z) is tested -- which is exactly what dark energy is inferred from.

Comparison (LIT, retrieved, Seifert, Lane, Galoppo, Ridden-Harper & Wiltshire 2024,
MNRAS Lett., arXiv:2412.15143): with their OWN Tripp standardization of the Pantheon+
light curves and NO cosmology-dependent bias corrections, timescape is preferred,
ln B > 5 (whole sample) and ln B > 1 (z > 0.075), with f_v0 = 0.737 +- 0.029.  Their
priors are reused here: f_v0 in [0.500, 0.799], Omega_m in [0.143, 0.487].
Independent f_v0 values (LIT, as quoted there): Planck CMB 0.695 (+0.041 -0.051).
"""
import os
import urllib.request

import numpy as np
from scipy.integrate import quad, trapezoid

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "..", "data", "pantheon_plus")
URL = ("https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/"
       "Pantheon%2B_Data/4_DISTANCES_AND_COVAR/")
FILES = {"pp.dat": "Pantheon%2BSH0ES.dat", "pp.cov": "Pantheon%2BSH0ES_STAT%2BSYS.cov"}

PRIOR_OM = (0.143, 0.487)          # Seifert et al. 2024 priors (uniform)
PRIOR_FV = (0.500, 0.799)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# --------------------------------------------------------------------------- models
def ts_params(f):
    b = 2 * (1 - f) * (2 + f) / (9 * f)
    t0 = (2 + f) / 3
    return b, t0


def ts_F(t, b):
    """Closed-form antiderivative of 1/(gamma t^(2/3)) (Wiltshire 2009, recalled)."""
    u, c = np.cbrt(t), np.cbrt(b)
    return (2 * u + c / 6 * np.log((u + c) ** 2 / (u * u - u * c + c * c))
            + c / np.sqrt(3) * np.arctan((2 * u - c) / (np.sqrt(3) * c)))


def ts_gamma(t, b):
    return 3 * (t + b) / (2 * t + 3 * b)


def ts_abar(t, f):
    return (3 * t) ** (2 / 3) * np.cbrt(3 * f * t + (1 - f) * (2 + f)) / (2 + f)


def ts_z(t, f):
    b, t0 = ts_params(f)
    return ts_gamma(t, b) / (ts_abar(t, f) * ts_gamma(t0, b)) - 1


def ts_DL(z, f, n=4000):
    """Timescape luminosity distance in units c/Hbar0, at redshifts z (array)."""
    b, t0 = ts_params(f)
    t = t0 * np.logspace(-4.5, 0, n)          # z up to ~ 10^3; plenty for SNe
    zt = ts_z(t, f)                           # decreasing in t
    DA = np.cbrt(t) ** 2 * (ts_F(t0, b) - ts_F(t, b))
    DL = (1 + zt) ** 2 * DA
    return np.interp(z, zt[::-1], DL[::-1])


def ts_H0_dressed(f):
    return (4 * f * f + f + 4) / (2 * (2 + f))


def ts_dressed_metric_H_q(f, h=1e-3):
    """H0 and q0 of the dressed scale factor a = abar/gamma in wall time (dtau = dt/gamma)."""
    b, t0 = ts_params(f)
    tau = lambda t: quad(lambda s: 1 / ts_gamma(s, b), 0, t, epsabs=1e-14, limit=200)[0]
    ts = t0 * (1 + h * np.arange(-2, 3))
    ta = np.array([tau(t) for t in ts])
    lna = np.log(ts_abar(ts, f) / ts_gamma(ts, b))
    p = np.polyfit(ta - ta[2], lna, 4)
    H = p[3]
    return H, -(2 * p[2] + H * H) / H ** 2


def lcdm_DL(z, Om, n=4000):
    """Flat LCDM luminosity distance in units c/H0."""
    zz = np.linspace(0, max(np.max(z), 1e-3) * 1.001, n)
    Einv = 1 / np.sqrt(Om * (1 + zz) ** 3 + 1 - Om)
    chi = np.concatenate([[0], np.cumsum(0.5 * (Einv[1:] + Einv[:-1]) * np.diff(zz))])
    return (1 + z) * np.interp(z, zz, chi)


def milne_DL(z):
    return z * (1 + z / 2)


def eds_DL(z):
    return 2 * (1 + z) * (1 - 1 / np.sqrt(1 + z))


def q0_from_DL(DLfun):
    """Deceleration parameter from D_L = (z + (1-q0) z^2/2 + ...)/H0, by finite differences."""
    h = 1e-3
    d1, d2 = DLfun(h), DLfun(2 * h)
    a1 = (4 * d1 - d2) / (2 * h)               # D_L'(0)
    a2 = (d2 - 2 * d1) / (h * h)               # D_L''(0)  (D_L(0) = 0)
    return 1 - a2 / a1, a1


# --------------------------------------------------------------------------- data
def load_pantheon():
    os.makedirs(DATA_DIR, exist_ok=True)
    for local, remote in FILES.items():
        p = os.path.join(DATA_DIR, local)
        if not os.path.exists(p):
            print(f"   downloading {remote} ...")
            urllib.request.urlretrieve(URL + remote, p)
    names = open(os.path.join(DATA_DIR, "pp.dat")).readline().split()
    raw = np.genfromtxt(os.path.join(DATA_DIR, "pp.dat"), skip_header=1, dtype=None,
                        encoding=None)
    col = {n: np.array([r[i] for r in raw]) for i, n in enumerate(names)}
    flat = np.loadtxt(os.path.join(DATA_DIR, "pp.cov"))
    N = int(flat[0])
    C = flat[1:].reshape(N, N)
    return col, C


def have_data():
    return all(os.path.exists(os.path.join(DATA_DIR, k)) for k in FILES)


class Likelihood:
    """chi^2 with the magnitude offset marginalized analytically (flat prior)."""

    def __init__(self, col, C, zmin, zkey="zHD", debias=False):
        s = (col[zkey] > zmin) & (col["IS_CALIBRATOR"] == 0)
        self.z = col[zkey][s].astype(float)
        self.zhel = col["zHEL"][s].astype(float)
        self.m = col["m_b_corr"][s].astype(float)
        if debias:   # undo delta_bias (Brout et al. 2022 eq. 1: mu = ... - delta_bias + ...)
            self.m = self.m + col["biasCor_m_b"][s].astype(float)
        self.N = int(s.sum())
        Ci = np.linalg.inv(C[np.ix_(s, s)])
        self.Ci = Ci
        self.e = Ci.sum(axis=0)
        self.E = self.e.sum()

    def chi2(self, DL):
        r = self.m - 5 * np.log10((1 + self.zhel) / (1 + self.z) * DL)
        A = r @ self.Ci @ r
        B = self.e @ r
        return A - B * B / self.E

    def scan(self, DLfun, grid):
        return np.array([self.chi2(DLfun(self.z, p)) for p in grid])


def fit_1d(grid, chi2, prior):
    """Best fit on the full grid (unconstrained), sigma from the curvature, and ln(evidence)
    over the uniform prior window only (up to a constant common to both models)."""
    i = np.argmin(chi2)
    w = (grid >= prior[0]) & (grid <= prior[1])
    L = np.exp(-0.5 * (chi2[w] - chi2[i]))
    lnZ = -0.5 * chi2[i] + np.log(trapezoid(L, grid[w]) / (prior[1] - prior[0]))
    # parabolic refinement + Gaussian sigma from local curvature
    j = min(max(i, 1), len(grid) - 2)
    y0, y1, y2 = chi2[j - 1:j + 2]
    h = grid[1] - grid[0]
    curv = (y0 - 2 * y1 + y2) / h ** 2
    xb = grid[j] - h * (y2 - y0) / (2 * (y0 - 2 * y1 + y2)) if curv > 0 else grid[i]
    sig = np.sqrt(2 / curv) if curv > 0 else np.nan
    return xb, sig, chi2[i], lnZ


# --------------------------------------------------------------------------- main
def checks():
    banner("T1  CHECKS on the timescape distance (recalled formulas, verified here)")
    f = 0.695
    b, t0 = ts_params(f)
    num = quad(lambda t: 1 / (ts_gamma(t, b) * t ** (2 / 3)), 0.05, t0, epsabs=1e-13)[0]
    cf = ts_F(t0, b) - ts_F(0.05, b)
    print(f"   closed-form F vs numerical integral of 1/(gamma t^2/3):  {cf:.12f} vs {num:.12f}")
    print(f"   z(t0) = {ts_z(t0, f):.2e}  (must be 0);  f_v(t0) = "
          f"{3*f*t0/(3*f*t0+(1-f)*(2+f)):.12f}  (must be f = {f})")
    q0DL, slope = q0_from_DL(lambda z: ts_DL(np.array([z]), f, n=20000)[0])
    H0 = ts_H0_dressed(f)
    H0m, q0m = ts_dressed_metric_H_q(f)
    q0_lit = -(1 - f) * (8 * f ** 3 + 39 * f ** 2 - 12 * f - 8) / (4 + f + 4 * f * f) ** 2
    print(f"   low-z slope D_L'(0) = {slope:.6f}  vs  1/H0_dressed = {1/H0:.6f}")
    print(f"   dressed a(tau) = abar/gamma in wall time:  H0 = {H0m:.9f} vs {H0:.9f};"
          f"  q0 = {q0m:+.6f} vs closed form (Wiltshire, recalled) {q0_lit:+.6f}")
    print(f"   q0 read off D_L(z) as if FLRW: {q0DL:+.4f}.  FOLLOWS: differs from the metric q0")
    print("   because the dressed geometry is not FLRW (the areal radius carries extra z-")
    print("   dependence), so 'q0 from supernovae' is model-dependent in timescape.")
    print("   Either way q0 < 0: apparent acceleration with NO dark energy; the bare (volume-")
    print("   average) expansion always decelerates.")
    q0L, _ = q0_from_DL(lambda z: lcdm_DL(np.array([z]), 0.3, n=20000)[0])
    print(f"   CHECK flat LCDM Om=0.3: q0 = {q0L:+.4f}  vs  Om*3/2 - 1 = {0.3*1.5-1:+.4f}")
    return dict(cf=cf, num=num, slope=slope, H0inv=1 / H0, q0m=q0m, q0_lit=q0_lit, q0DL=q0DL)


def main():
    out = checks()
    col, C = load_pantheon()

    gOm = np.linspace(0.05, 0.70, 651)          # wide grids: best fits unconstrained,
    gfv = np.linspace(0.30, 0.97, 671)          # evidence uses the prior windows only

    banner("T2  Pantheon+ (official standardization, STAT+SYS covariance): LCDM vs timescape")
    print("   chi^2 with the magnitude/H0 offset marginalized.  Delta = chi2(TS) - chi2(LCDM):")
    print("   negative favours timescape.  ln B = ln Z_TS - ln Z_LCDM (Seifert et al. priors).")
    print("   Milne (empty) and Einstein-de Sitter (matter only, no averaging) for scale.\n")
    print("   z key  z_min    N    Om (LCDM)        f_v0 (TS)        chi2_LCDM  Delta   "
          "ln B    dEdS     dMilne")
    rows = []
    for zkey in ["zHD", "zCMB"]:
        for zmin in [0.01, 0.023, 0.033, 0.05, 0.075, 0.1]:
            Lk = Likelihood(col, C, zmin, zkey)
            cL = Lk.scan(lcdm_DL, gOm)
            cT = Lk.scan(ts_DL, gfv)
            Om, sOm, chiL, lnZL = fit_1d(gOm, cL, PRIOR_OM)
            fv, sfv, chiT, lnZT = fit_1d(gfv, cT, PRIOR_FV)
            dEdS = Lk.chi2(eds_DL(Lk.z)) - chiL
            dMil = Lk.chi2(milne_DL(Lk.z)) - chiL
            rows.append(dict(zkey=zkey, zmin=zmin, N=Lk.N, Om=Om, sOm=sOm, fv=fv, sfv=sfv,
                             chiL=chiL, chiT=chiT, lnB=lnZT - lnZL, dEdS=dEdS, dMil=dMil))
            print(f"   {zkey:5s} {zmin:5.3f} {Lk.N:5d}   {Om:.3f} +- {sOm:.3f}   "
                  f"{fv:.3f} +- {sfv:.3f}   {chiL:8.1f}  {chiT-chiL:+6.2f}  {lnZT-lnZL:+6.2f}"
                  f"  {dEdS:+7.1f}  {dMil:+7.1f}")

    banner("T2b DIAGNOSTIC: undo the Pantheon+ bias correction (simulated in a FLRW model)")
    print("   Seifert et al. omit cosmology-dependent bias corrections.  Adding delta_bias back")
    print("   (covariance unchanged, so this is approximate) isolates that one difference.\n")
    print("   z key  z_min    N    Om (LCDM)        f_v0 (TS)        Delta   ln B")
    diag = []
    for zkey in ["zHD", "zCMB"]:
        for zmin in [0.01, 0.033, 0.075]:
            Lk = Likelihood(col, C, zmin, zkey, debias=True)
            Om, sOm, chiL, lnZL = fit_1d(gOm, Lk.scan(lcdm_DL, gOm), PRIOR_OM)
            fv, sfv, chiT, lnZT = fit_1d(gfv, Lk.scan(ts_DL, gfv), PRIOR_FV)
            diag.append(dict(zkey=zkey, zmin=zmin, Om=Om, fv=fv, d=chiT - chiL, lnB=lnZT - lnZL))
            print(f"   {zkey:5s} {zmin:5.3f} {Lk.N:5d}   {Om:.3f} +- {sOm:.3f}   "
                  f"{fv:.3f} +- {sfv:.3f}   {chiT-chiL:+6.2f}  {lnZT-lnZL:+6.2f}")

    banner("T3  Verdict")
    r0 = rows[0]
    print(f"   Reference CHECK: LCDM, zHD, z > 0.01: Om = {r0['Om']:.3f} +- {r0['sOm']:.3f}"
          "  (Brout et al. 2022, retrieved: 0.334 +- 0.018).")
    print(f"   1. Matter only, smooth (EdS): worse by Delta chi^2 = {r0['dEdS']:+.0f}.  In an FLRW")
    print("      universe the supernovae DO demand acceleration; that part is not an artifact.")
    print(f"   2. Timescape (no dark energy) fits nearly as well: Delta chi^2 = "
          f"{r0['chiT']-r0['chiL']:+.1f} (official")
    print(f"      analysis, z > 0.01), ln B = {r0['lnB']:+.1f}.  Over all 12 cuts/redshift "
          f"choices Delta chi^2 spans")
    ds = [r["chiT"] - r["chiL"] for r in rows]
    lb = [r["lnB"] for r in rows]
    print(f"      {min(ds):+.1f} .. {max(ds):+.1f} and ln B spans {min(lb):+.1f} .. {max(lb):+.1f}:"
          " LCDM mildly preferred or a tie.")
    hi = [r for r in rows if r["zmin"] >= 0.075]
    print(f"      Beyond the homogeneity scale (z > 0.075): |ln B| <= "
          f"{max(abs(r['lnB']) for r in hi):.1f} -> inconclusive.")
    print("   3. Seifert et al. 2024 (own Tripp standardization, same light curves): ln B > +5.")
    print("      The SIGN of the preference is set by the light-curve standardization.  Undoing")
    print(f"      the FLRW-simulated bias correction moves it the other way (ln B -> "
          f"{diag[0]['lnB']:+.1f}), so that")
    print("      correction is not what hides timescape here.")
    sig_pl = 0.041 if r0["fv"] > 0.695 else 0.051   # asymmetric Planck error, side of the fit
    t = (r0["fv"] - 0.695) / np.hypot(r0["sfv"], sig_pl)
    print(f"   4. Fitted f_v0 = {r0['fv']:.3f} +- {r0['sfv']:.3f} vs Planck-CMB timescape 0.695"
          f" (+0.041 -0.051): {t:.1f} sigma apart.")
    print("   VERDICT: supernovae alone cannot tell 'dark energy' from 'averaging artifact'.")
    print("   The difference is a few chi^2 units and flips sign with the analysis choices.")
    out.update(tension=t)
    return out, rows, diag


if __name__ == "__main__":
    main()
