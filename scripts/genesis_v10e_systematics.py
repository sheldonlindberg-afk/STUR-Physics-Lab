#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10e: systematics not modelled by the M3a l-shape forecast
================================================================================
genesis_v10c_m3a_lshape.py forecast how well a flat (constant) rotation is
rejected by STUR-M3a's high-l decline of beta_eff(l). It applied the rotation to
the lensed spectra and ignored instrument and foreground EB. This stage adds:

  (a) Lensing. The rotation acts at emission, i.e. on the UNLENSED E/B fields;
      lensing then remaps Q/U. In the curved-sky correlation-function method
      (Challinor & Lewis 2005, CAMB camb.correlations) lensing acts linearly on
        xi_+  <->  C^EE + C^BB,      xi_-  <->  C^EE - C^BB + 2i C^EB,
      with real kernels, so the imaginary part of xi_- transforms exactly like
      its real part:   C~^EB = L_-[C^EB],   C~^EE - C~^BB = L_-[C^EE - C^BB].
      L_-[X] is obtained from CAMB by lensing an input with EE = X, BB = 0 and
      taking lensed EE - lensed BB. Gates: L_-[C^EE] reproduces CAMB's lensed
      EE - BB; a constant rotation stays a constant rotation after lensing.
  (b) l-dependent instrumental EB and foreground EB, as nuisance templates:
        beam-like drift of the polarisation angle  alpha(l) = a l(l+1)/2500^2
        dust EB  C^EB_dust = rho C^EE_dust,  C^EE_dust ~ l^-2.42
      Reported: M3a significance with each nuisance marginalised, and the
      nuisance amplitude that best mimics M3a's decline.
  (c) Faraday rotation across LiteBIRD bands: Galactic (RM ~ few rad/m^2 at high
      latitude) and primordial magnetic field (stochastic, zero mean). Gives the
      frequency-dependence threshold for the achromaticity criterion.

Registered files are imported only, never modified.
Usage:  python genesis_v10e_systematics.py [--cache FILE.npz]
================================================================================
"""
import argparse
import importlib.util
import os

import camb
import numpy as np
from camb import correlations

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


G = _load("g10b", "genesis_v10b_boltzmann.py")
M = _load("g10c", "genesis_v10c_m3a.py")
LS = _load("g10c_ls", "genesis_v10c_m3a_lshape.py")

LMAX_IN = 4000          # lensing input band limit
LMAX = 3000             # analysis range (as in the lshape forecast)
C_LIGHT = 2.99792458e8
LITEBIRD_BANDS = [40, 50, 60, 68, 78, 89, 100, 119, 140, 166, 195, 235, 280, 337, 402]  # GHz
gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:56s} {detail:32s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 80 + "\n  " + s + "\n" + "=" * 80)


# ------------------------------------------------------------------------------
# beta_eff(l) curves: exactly the lshape pipeline (M3a, 49 phases, + STUR-B)
# ------------------------------------------------------------------------------
def compute_curves():
    src = G.Sources(r=0.0035)
    t0 = src.t0
    noise, fwhm = 2.2, 30.0
    ells_hi = np.unique(np.round(np.geomspace(45, 1500, 40)).astype(int))
    nl_h = G.litebird_noise(ells_hi, noise, fwhm)
    deltas = np.linspace(0, 2 * np.pi, 145)[:-1]
    H1 = {float(d): (lambda z, t, th=M.theta_fn(1.0, d, t0): np.degrees(M.K * (th(t0) - th(t))))
          for d in deltas}
    ce1, cb1 = src.transfers(ells_hi, H1)
    hh = ells_hi >= 50
    wl1 = (2 * ells_hi + 1) * ce1 ** 2 / ((ce1 + nl_h) * (src.cl_len[ells_hi, 2] + nl_h))
    sols = {}
    for d in H1:
        b1 = G.beta_eff(ce1, cb1[d])
        bh1 = np.sum(wl1[hh] * b1[hh]) / np.sum(wl1[hh])
        if bh1 > 0 and M.BETA_NOW / bh1 <= M.A_MAX:
            sols[d] = M.BETA_NOW / bh1
    ds = sorted(sols)
    LS.extend_hi_grid(src)
    LS.extend_spectra(src)
    ells = np.unique(np.concatenate([np.arange(2, 41), np.round(np.geomspace(45, 3000, 70)).astype(int)]))
    H = {d: (lambda z, t, th=M.theta_fn(sols[d], d, t0): np.degrees(M.K * (th(t0) - th(t)))) for d in ds}
    H["STUR-B"] = G.histories(src)["STUR-B (ln t)"]
    cee, ceb = src.transfers(ells, H)
    hi = ells >= 50
    nl = G.litebird_noise(ells, noise, fwhm)
    wl = (2 * ells + 1) * cee ** 2 / ((cee + nl) * (src.cl_len[ells, 2] + nl))
    curves = np.array([G.beta_eff(cee, ceb[d]) for d in ds])
    bsb = G.beta_eff(cee, ceb["STUR-B"])
    sturb = bsb * M.BETA_NOW / (np.sum(wl[hi] * bsb[hi]) / np.sum(wl[hi]))
    return ells, np.array(ds), curves, sturb


# ------------------------------------------------------------------------------
# spectra and the lensing operator L_-
# ------------------------------------------------------------------------------
def spectra():
    pars = camb.set_params(**G.COSMO, tau=G.DATA['tau'][0], lmax=LMAX_IN + 300, lens_potential_accuracy=1)
    res = camb.get_results(pars)
    unl = res.get_unlensed_scalar_cls(CMB_unit='muK', lmax=LMAX_IN)            # D_l
    lens = res.get_lensed_scalar_cls(CMB_unit='muK', lmax=LMAX_IN)
    pp = res.get_lens_potential_cls(lmax=LMAX_IN)[:, 0]
    pt = camb.set_params(**G.COSMO, tau=G.DATA['tau'][0], r=0.0035, lmax=LMAX_IN, WantTensors=True)
    tot = camb.get_results(pt).get_total_cls(CMB_unit='muK', raw_cl=True, lmax=LMAX_IN)
    return unl, lens, pp, tot


def make_Lminus(pp):
    def Lminus(X_D):
        """lensed EB (D_l) of an unlensed EB X_D (D_l), via xi_- linearity"""
        inp = np.zeros((LMAX_IN + 1, 4))
        inp[:, 1] = X_D[:LMAX_IN + 1]
        out = correlations.lensed_cls(inp, pp, lmax=LMAX_IN)
        return out[:, 1] - out[:, 2]
    return Lminus


def d2c(D):
    ell = np.arange(len(D))
    C = np.zeros_like(D)
    C[2:] = 2 * np.pi * D[2:] / (ell[2:] * (ell[2:] + 1))
    return C


def beta_on_grid(ells, b):
    """beta_eff(l) interpolated to 0..LMAX_IN, held at its l = 3000 value above (input band limit)"""
    L = np.arange(LMAX_IN + 1)
    return np.interp(L, ells, b)


# ------------------------------------------------------------------------------
# shape test with optional nuisance templates
# ------------------------------------------------------------------------------
def shape_sigma(data, basis, var, ell, extra=()):
    """sqrt(Delta chi^2) of the best fit of (flat basis + extra templates) to data"""
    X = np.vstack([basis[ell]] + [e[ell] for e in extra]).T / np.sqrt(var)[:, None]
    y = data[ell] / np.sqrt(var)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(np.sqrt(np.sum((y - X @ coef) ** 2))), coef


def main(cache):
    print("\n=== Stage 10e: systematics for the STUR-M3a / STUR-B tests ===")
    if cache and os.path.exists(cache):
        z = np.load(cache)
        ells, ds, curves, sturb = z['ells'], z['ds'], z['curves'], z['sturb']
        print(f"  beta_eff curves loaded from cache ({len(ds)} M3a phases + STUR-B)")
    else:
        print("  computing beta_eff curves (lshape pipeline, ~10 min) ...")
        ells, ds, curves, sturb = compute_curves()
        if cache:
            np.savez(cache, ells=ells, ds=ds, curves=curves, sturb=sturb)
    gate("49 admissible M3a phases (as registered)", len(ds) == 49, f"{len(ds)}")

    unl, lens, pp, tot = spectra()
    Lm = make_Lminus(pp)
    L = np.arange(LMAX_IN + 1)

    # ---------------- (a) lensing gates
    header("(a) Lensing of an l-dependent EB rotation")
    LEE = Lm(unl[:, 1])
    ref = lens[:, 1] - lens[:, 2]
    sel = (L >= 30) & (L <= LMAX)
    dev = np.max(np.abs(LEE[sel] / ref[sel] - 1))
    gate("L_-[EE] reproduces CAMB lensed EE - BB (l = 30-3000)", dev < 0.01, f"max dev {dev:.1e}")
    b0 = np.radians(0.3)
    lhs = Lm(0.5 * np.sin(4 * b0) * unl[:, 1])
    rhs = 0.5 * np.sin(4 * b0) * LEE
    dev_c = np.max(np.abs(lhs[sel] - rhs[sel]) / np.abs(rhs[sel]))
    gate("constant rotation stays constant after lensing", dev_c < 1e-8, f"max rel dev {dev_c:.1e}")

    # rotated unlensed EB and its lensed counterpart, raw C_l
    def eb_lensed(bcurve):
        bl = beta_on_grid(ells, bcurve)
        return d2c(Lm(0.5 * np.sin(4 * np.radians(bl)) * unl[:, 1]))

    def eb_unlensed_lshape(bcurve):
        """the lshape forecast's construction: rotation applied to the lensed total spectra"""
        bl = np.interp(np.arange(LMAX + 1), ells, bcurve)
        return 0.5 * np.sin(4 * np.radians(bl)) * (tot[:LMAX + 1, 1] - tot[:LMAX + 1, 2])

    flat_len = 0.5 * np.sin(4 * np.radians(1.0)) * d2c(LEE)
    flat_ls = 0.5 * np.sin(4 * np.radians(1.0)) * (tot[:LMAX + 1, 1] - tot[:LMAX + 1, 2])
    beam_t = lambda flat: flat * (L[:len(flat)] * (L[:len(flat)] + 1) / 2500.0 ** 2)
    dust_C = np.zeros(LMAX_IN + 1)
    dust_C[2:] = (L[2:] / 80.0) ** -2.42                                      # shape only

    imed = len(ds) // 2
    print(f"  M3a median phase delta = {ds[imed]:.3f} rad")
    rows = {}
    for name, (nz, fw, fsky, lmin, lmax) in LS.EXPERIMENTS.items():
        ell = np.arange(lmin, lmax + 1)
        n_ = G.litebird_noise(ell, nz, fw)
        var = (tot[ell, 1] + n_) * (tot[ell, 2] + n_) / ((2 * ell + 1) * fsky)
        s_ls, s_len, s_beam, s_dust, a_mimic, rho_mimic = [], [], [], [], [], []
        for c in curves:
            s_ls.append(shape_sigma(eb_unlensed_lshape(c), flat_ls, var, ell)[0])
            d = eb_lensed(c)
            s_len.append(shape_sigma(d, flat_len, var, ell)[0])
            sb, cb = shape_sigma(d, flat_len, var, ell, extra=(beam_t(flat_len),))
            s_beam.append(sb)
            a_mimic.append(cb[1])                                             # deg of drift at l = 2500
            sd, cd = shape_sigma(d, flat_len, var, ell, extra=(dust_C,))
            s_dust.append(sd)
            rho_mimic.append(cd[1])                                           # rho * C^EE_dust(80) [uK^2]
        d_sb = eb_lensed(sturb)
        rows[name] = dict(
            ls=np.array(s_ls), len=np.array(s_len), beam=np.array(s_beam), dust=np.array(s_dust),
            a=np.array(a_mimic), rho=np.array(rho_mimic),
            sturb_len=shape_sigma(d_sb, flat_len, var, ell)[0],
            sturb_ls=shape_sigma(eb_unlensed_lshape(sturb), flat_ls, var, ell)[0])

    ref_ls = {"LiteBIRD": 0.38, "ACT DR6-like": 1.19, "Simons Obs. LAT-like": 3.18, "CMB-S4-like (wide)": 11.31}
    devr = max(abs(np.median(rows[n]['ls']) / ref_ls[n] - 1) for n in ref_ls)
    gate("reproduces the lshape forecast medians (unlensed construction)", devr < 0.02, f"max rel dev {devr:.1e}")

    fmt = lambda a: f"{a.min():5.2f} /{np.median(a):6.2f} /{a.max():6.2f}"
    print(f"\n  significance at which a flat rotation is rejected (min / median / max over 49 phases)")
    print(f"  {'experiment':22s} {'lshape (no lensing)':>22s} {'lensed':>22s} {'STUR-B lensed':>14s}")
    for n, r in rows.items():
        print(f"  {n:22s} {fmt(r['ls']):>22s} {fmt(r['len']):>22s} {r['sturb_len']:13.2f}σ")

    # ---------------- (b) instrumental and foreground nuisances
    header("(b) l-dependent instrumental EB and dust EB, marginalised")
    print(f"  {'experiment':22s} {'+beam drift':>22s} {'+dust EB':>22s}"
          f" {'mimicking drift a(l=2500)':>26s} {'mimicking rho*C_dust(80)':>25s}")
    for n, r in rows.items():
        print(f"  {n:22s} {fmt(r['beam']):>22s} {fmt(r['dust']):>22s}"
              f" {np.median(r['a']):+21.3f} deg {np.median(r['rho']):+20.2e} uK^2")
    print("""
  Reading: 'mimicking' amplitudes are the best-fit nuisance amplitudes that absorb the M3a
  decline (median phase). A beam-like drift of the effective polarisation angle of order
  the printed a(l = 2500) between l ~ 300 and 2500 is degenerate with M3a. Published
  detector-angle systematics are at the ~0.1 deg level (ACT optical modelling, arXiv:2403.00763;
  CMB-S4 budget >0.1 deg, unrefereed talk), and SO reports cross-polar beams raise EB mainly at
  high l (arXiv:2503.01791). The M3a shape test therefore requires the l-dependence of the
  angle calibration to be known to well below the printed a, not just its mean.""")

    # ---------------- (c) Faraday rotation
    header("(c) Faraday rotation across LiteBIRD bands")
    lam2 = (C_LIGHT / (np.array(LITEBIRD_BANDS) * 1e9)) ** 2
    print(f"  {'band [GHz]':>10s} {'RM = 1':>9s} {'RM = 6.3':>9s} {'RM = 10':>9s}   PMF rms (B = 4.4 nG)  [deg]")
    pmf = 1.6 * 4.4 * (np.array(LITEBIRD_BANDS) / 30.0) ** -2
    for nu, l2, p in zip(LITEBIRD_BANDS, lam2, pmf):
        print(f"  {nu:10d} {np.degrees(1 * l2):9.5f} {np.degrees(6.3 * l2):9.5f} {np.degrees(10 * l2):9.5f}   {p:9.4f}")
    gal_max = np.degrees(10 * (lam2.max() - lam2.min()))
    cmb_bands = [i for i, nu in enumerate(LITEBIRD_BANDS) if 68 <= nu <= 235]
    gal_cmb = np.degrees(10 * (lam2[cmb_bands].max() - lam2[cmb_bands].min()))
    print(f"""
  Galactic: |RM| at high latitude ~ 0-6 rad/m^2 (median), scatter ~9 rad/m^2 (Mitra et al. 2010;
  Akahori et al. 2013). For an effective sky-averaged |RM| <= 10 rad/m^2 the expected isotropic
  rotation differs between 40 and 402 GHz by <= {gal_max:.3f} deg, and between the CMB channels
  68-235 GHz by <= {gal_cmb:.4f} deg, with a nu^-2 shape.
  Primordial fields: stochastic and zero-mean, so they add anisotropic, not isotropic, rotation;
  rms 1.6 deg B_nG (nu/30 GHz)^-2 (review rescaling of Kosowsky & Loeb 1996; KL quote ~1 deg)
  with B_1Mpc < 4.4 nG (Planck 2015 XIX).""")
    gate("Galactic Faraday difference across CMB channels < LiteBIRD sigma(beta) = 0.02 deg",
         gal_cmb < 0.02, f"{gal_cmb:.4f} deg")
    print(f"""
  Quantitative achromaticity criterion (both STUR-B and M3a predict achromatic beta):
    fit beta(nu) = beta_0 + beta_F (nu / 40 GHz)^-2 across bands; any nu-dependence that is
    not of nu^-2 form, or a nu^-2 term with |beta_F| > {np.degrees(10 * lam2[0]):.3f} deg (|RM_eff| > 10 rad/m^2)
    after subtracting the Galactic RM map, excludes the achromatic hypotheses at the stated
    significance; differences between 68-235 GHz channels above 3 sigma_combined + {gal_cmb:.4f} deg
    cannot be attributed to Faraday rotation.""")

    print(f"\n  gates: {sum(gates)}/{len(gates)} passed")
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None, help="npz cache for the beta_eff curves")
    main(ap.parse_args().cache)
