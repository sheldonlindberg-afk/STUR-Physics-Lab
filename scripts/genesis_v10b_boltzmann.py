#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10b: full-Boltzmann STUR-B tomography + LiteBIRD forecast
================================================================================
Stage 10 ('genesis V10 Light Bird') computed the reionization angle with a
simplified line of sight (free-streamed quadrupole, no ISW) and said:
"A full CLASS tomographic run should replace this before publication."
This stage does that with CAMB, and replaces quoted LiteBIRD sensitivities
with a forecast computed from the instrument model. The hypothesis (A1-A4) is
unchanged and nothing is fitted to anything except kappa to beta_now.

  1. Exact polarisation sources S_E(k, eta) from CAMB's Boltzmann hierarchy.
     The rotation acts at emission:
       Delta_E,l(k) = N_l int deta S_E cos(2 beta(eta)) j_l(k(eta0 - eta))
       Delta_B,l(k) = N_l int deta S_E sin(2 beta(eta)) j_l(k(eta0 - eta))
     N_l = sqrt((l+2)!/(l-2)!). Gates: C_l^EE vs CAMB; constant beta returned.
  2. kappa calibrated to beta_now = 0.277 deg as the measurement sees it: the
     EB-information-weighted beta_eff over l = 50-1500, not beta(z*) itself.
  3. LiteBIRD Fisher forecast on C_l^EB (2 <= l <= lmax), with the
     polarisation-angle miscalibration alpha marginalised:
       sigma(Delta beta), the detection significance of the STUR-B tomographic
       signal, and Delta chi^2 against every competing rotation history.
  4. Robustness of beta_reio/beta_rec to tau, the reionization width, the
     chronomagnetic modulation (eps, phase) and t_c.

Writes genesis_v10b_preregistration.json (canonical JSON) and prints its SHA-256.
The Stage 10 pre-registration file is left untouched: both hashes stand.

Usage:  python genesis_v10b_boltzmann.py [--fsky 0.6] [--noise 2.2] [--fwhm 30]
================================================================================
"""
import argparse
import datetime
import hashlib
import json
import os

import camb
import numpy as np
from scipy.special import gammaln, spherical_jn

LN_LAMBDA_PREREG = np.log(3722 / 2705)   # value used by Stage 10 (eps-modulation period)
DATA = {
    'beta_now': (0.277, 0.057, "ACT DR6 + Planck joint analysis, arXiv:2608.06480 (4.8 sigma)"),
    'tau': (0.0544, 0.0073, "Planck 2018 VI"),
    'age': (13.797, 0.023, "Planck 2018 VI [Gyr]"),
    'stage10_ratio': 0.21289825059127768,
    'stage10_dbeta': -0.21802718458621612,
}
COSMO = dict(H0=67.36, ombh2=0.02237, omch2=0.1200, mnu=0.06, As=2.1e-9, ns=0.9649)
TCMB_UK = 2.7255e6


# ------------------------------------------------------------------------------
# CAMB sources
# ------------------------------------------------------------------------------
class Sources:
    """S_E(k, eta) on a low-l grid (full history) and a high-l grid (recombination)."""

    def __init__(self, tau=0.0544, dz_reion=0.5, r=0.0):
        # scalar-only run for the sources: with WantTensors on, get_time_evolution does not
        # return the scalar E source (C_EE gate fails by 100%); tensors go in a separate run
        p = camb.set_params(**COSMO, tau=tau, lmax=2500)
        p.Reion.delta_redshift = dz_reion
        self.pars = p
        self.res = camb.get_results(p)
        if r > 0:
            pt = camb.set_params(**COSMO, tau=tau, r=r, lmax=2500, WantTensors=True)
            pt.Reion.delta_redshift = dz_reion
            self.res_tot = camb.get_results(pt)
        else:
            self.res_tot = self.res
        self.eta0 = self.res.tau0
        self.zre = self.res.Params.Reion.redshift
        # low l: k <= 0.03, whole history (reionization needs it)
        self.k_lo = np.logspace(-5, np.log10(0.03), 800)
        e_lo = np.unique(np.concatenate([np.linspace(150, 1500, 2701),
                                         np.linspace(1500, self.eta0 - 5, 4500)]))
        # high l: recombination window, k linear (Delta_l(k) oscillates with period 2pi/eta0)
        self.k_hi = np.arange(2e-4, 0.25, 2e-4)
        e_hi = np.linspace(150, 800, 1301)
        self.grids = {}
        for key, k, e in (("lo", self.k_lo, e_lo), ("hi", self.k_hi, e_hi)):
            S = self.res.get_time_evolution(k, e, ['E_source'])[:, :, 0]
            z = self.res.redshift_at_conformal_time(e)
            t = np.array([self.res.physical_time(zz) for zz in z[::25]])
            t = np.exp(np.interp(z, z[::25][::-1], np.log(t)[::-1]))
            self.grids[key] = dict(k=k, eta=e, S=S, w=np.gradient(e), z=z, t=t)
        self.t0 = self.res.physical_time(0.0)
        self.zstar = self.res.get_derived_params()['zstar']
        self.tstar = self.res.physical_time(self.zstar)
        self.cl_unl = self.res.get_unlensed_scalar_cls(CMB_unit='muK', raw_cl=True)
        self.cl_len = self.res_tot.get_total_cls(CMB_unit='muK', raw_cl=True)

    def transfers(self, ells, betas):
        """C_EE (unrotated) and C_EB for each rotation history beta(z, t) [deg], per l"""
        out_ee, out_eb = [], {n: [] for n in betas}
        for l in ells:
            g = self.grids["lo" if l <= 40 else "hi"]
            k = g['k']
            J = spherical_jn(l, np.outer(k, self.eta0 - g['eta']))
            SJ = g['S'] * J * g['w']
            Nl = np.exp(0.5 * (gammaln(l + 3) - gammaln(l - 1)))
            P = COSMO['As'] * (k / 0.05) ** (COSMO['ns'] - 1)
            wk = 4 * np.pi * P * np.gradient(np.log(k)) * TCMB_UK ** 2 * Nl ** 2
            dE0 = SJ.sum(1)
            out_ee.append(np.sum(wk * dE0 * dE0))
            for n, bf in betas.items():
                b = np.radians(bf(g['z'], g['t']))
                dE = (SJ * np.cos(2 * b)).sum(1)
                dB = (SJ * np.sin(2 * b)).sum(1)
                out_eb[n].append(np.sum(wk * dE * dB))
        return np.array(out_ee), {n: np.array(v) for n, v in out_eb.items()}


def beta_eff(cee, ceb):
    return 0.25 * np.degrees(np.arcsin(np.clip(2 * ceb / cee, -1, 1)))


# ------------------------------------------------------------------------------
# rotation histories (all in degrees, normalised later)
# ------------------------------------------------------------------------------
def histories(src, eps=0.0, phase=0.0, t_c=0.0, z_split=50.0):
    t0 = src.t0

    def stur(z, t, eps=eps, phase=phase, t_c=t_c):
        U = lambda tt: (np.log((tt + t_c) / (t0 + t_c)) + eps * LN_LAMBDA_PREREG / (2 * np.pi)
                        * np.sin(2 * np.pi * np.log((tt + t_c) / (t0 + t_c)) / LN_LAMBDA_PREREG + phase))
        return U(t0) - U(t)
    return {
        "STUR-B (ln t)": stur,
        "ln a accrual": lambda z, t: np.log1p(z),
        "early-only (U(1) Master Action)": lambda z, t: (z > z_split) * 1.0,
        "late-only / miscalibration": lambda z, t: 1.0 + 0 * z,   # rotates rec and reio photons alike
    }


# ------------------------------------------------------------------------------
# Fisher forecast on C_l^EB with miscalibration alpha
# ------------------------------------------------------------------------------
def litebird_noise(ell, noise_uk_arcmin, fwhm_arcmin):
    th = np.radians(fwhm_arcmin / 60.0)
    return (np.radians(noise_uk_arcmin / 60.0)) ** 2 * np.exp(ell * (ell + 1) * th ** 2 / (8 * np.log(2)))


def eb_forecast(src, L, templ, fid_name, fsky, noise, fwhm, lmax, cl=None):
    """templ[name](l) = C_EB per unit amplitude on the full l range; alpha template = 2(C_EE - C_BB).
    cl: total (lensed + tensor) spectra; primordial B-modes are irreducible variance for EB"""
    cl = src.cl_len if cl is None else cl
    ell = np.arange(2, lmax + 1)
    cee = cl[ell, 1]
    cbb = cl[ell, 2]
    nl = litebird_noise(ell, noise, fwhm)
    var = ((cee + nl) * (cbb + nl)) / ((2 * ell + 1) * fsky)
    t_alpha = 2 * np.radians(1.0) * (cee - cbb)          # dC_EB / d alpha [per deg]
    tf = templ[fid_name][ell]
    data = tf                                            # fiducial: amplitude 1 (beta_now-calibrated), alpha = 0

    def fit(T):
        X = np.vstack([T, t_alpha]).T / np.sqrt(var)[:, None]
        y = data / np.sqrt(var)
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
        return float(np.sum((y - X @ coef) ** 2)), coef

    # detection of the STUR-B signal beyond a pure miscalibration (alpha absorbs any constant angle)
    chi_const, _ = fit(np.zeros_like(tf))
    F = np.array([[np.sum(tf * tf / var), np.sum(tf * t_alpha / var)],
                  [np.sum(tf * t_alpha / var), np.sum(t_alpha * t_alpha / var)]])
    Finv = np.linalg.inv(F)
    out = dict(sigma_A_fixed_alpha=float(1 / np.sqrt(F[0, 0])),
               sigma_A_marg_alpha=float(np.sqrt(Finv[0, 0])),
               delta_chi2={})
    for n, T in templ.items():
        if n == fid_name:
            continue
        out['delta_chi2'][n] = fit(T[ell])[0]
    return out


# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------
def run(fsky=0.6, noise=2.2, fwhm=30.0, lmax=1000, out_json="genesis_v10b_preregistration.json"):
    gates = []

    def gate(name, ok, detail):
        gates.append(dict(name=name, passed=bool(ok), detail=detail))
        print(f"  gate: {name:50s} {detail:42s} {'PASS' if ok else 'FAIL'}")

    print("\n=== Stage 10b: full-Boltzmann STUR-B tomography (CAMB) + LiteBIRD forecast ===")
    src = Sources(r=0.0035)
    gate("age vs Planck 2018", abs(src.t0 - DATA['age'][0]) < 2 * DATA['age'][1],
         f"{src.t0:.3f} Gyr")
    ells_lo = np.arange(2, 41)
    ells_hi = np.unique(np.round(np.geomspace(45, 1500, 40)).astype(int))
    ells = np.concatenate([ells_lo, ells_hi])
    H = histories(src)
    print(f"  computing transfers at {len(ells)} multipoles for {len(H)} histories ...")
    cee, ceb = src.transfers(ells, H)

    ratio_ee = cee / src.cl_unl[ells, 1]
    dev_lo, dev_hi = np.max(np.abs(ratio_ee[:39] - 1)), np.max(np.abs(ratio_ee[39:] - 1))
    gate("C_EE vs CAMB, l = 2-40", dev_lo < 0.01, f"max |ratio - 1| = {dev_lo:.1e}")
    gate("C_EE vs CAMB, l = 45-1500", dev_hi < 0.03, f"max |ratio - 1| = {dev_hi:.1e}")
    be_const = beta_eff(cee, ceb["late-only / miscalibration"])
    gate("constant beta = 1 deg returned at every l", np.max(np.abs(be_const - 1)) < 1e-3,
         f"max |beta_eff - 1| = {np.max(np.abs(be_const - 1)):.1e}")

    # kappa calibration: EB-information-weighted beta_eff at l = 50-1500
    hi = ells >= 50
    nl = litebird_noise(ells, noise, fwhm)
    wl = (2 * ells + 1) * cee ** 2 / ((cee + nl) * (src.cl_len[ells, 2] + nl))
    be1 = beta_eff(cee, ceb["STUR-B (ln t)"])                 # kappa = 1 deg per unit ln t
    per_k = float(np.sum(wl[hi] * be1[hi]) / np.sum(wl[hi]))
    per_k_star = np.log(src.t0 / src.tstar)
    kappa = DATA['beta_now'][0] / per_k
    s_kappa = DATA['beta_now'][1] / per_k
    print(f"\n  beta_eff(high l) per unit kappa = {per_k:.4f} deg; ln(t0/t*) = {per_k_star:.4f}"
          f" (Stage 10 used the latter)")
    print(f"  kappa = {kappa:.5f} +/- {s_kappa:.5f} deg per unit ln t   (Stage 10: 0.02632)")

    # predictions, every history normalised to the same high-l beta_now
    def norm(name):
        b = beta_eff(cee, ceb[name])
        return b * DATA['beta_now'][0] / (np.sum(wl[hi] * b[hi]) / np.sum(wl[hi]))
    lo = ells <= 10
    wlo = (2 * ells[lo] + 1) * cee[lo]
    preds = {}
    print(f"\n  {'history':34s} {'beta_reio':>9s} {'ratio':>7s} {'Delta beta':>11s}")
    for n in H:
        b = norm(n)
        breio = float(np.sum(wlo * b[lo]) / np.sum(wlo))
        preds[n] = dict(beta_reio=breio, ratio=breio / DATA['beta_now'][0],
                        delta_beta=breio - DATA['beta_now'][0], beta_eff_by_ell=b)
        print(f"  {n:34s} {breio:8.4f}° {breio / DATA['beta_now'][0]:7.3f} {breio - DATA['beta_now'][0]:+10.4f}°")
    P = preds["STUR-B (ln t)"]
    s_db = abs(P['delta_beta']) * DATA['beta_now'][1] / DATA['beta_now'][0]
    print(f"\n  STUR-B full Boltzmann: ratio = {P['ratio']:.3f} (Stage 10 simplified LOS: "
          f"{DATA['stage10_ratio']:.3f}); Delta beta = {P['delta_beta']:+.3f} +/- {s_db:.3f} deg")
    print("  beta_eff(l): " + " ".join(f"{l}:{b:.3f}" for l, b in zip(ells[:12], P['beta_eff_by_ell'][:12])))
    print("  high l:      " + " ".join(f"{l}:{b:.3f}" for l, b in
                                       zip(ells[39::6], P['beta_eff_by_ell'][39::6])))

    # ---- robustness
    print("\n  robustness of beta_reio/beta_rec:")
    rob = {}

    # every history only reweights the same S_E j_l products, so all variants on one source
    # set are evaluated in a single pass, on l = 2-10 plus a subset of the flat high-l plateau
    rsel = (ells <= 10) | ((ells >= 50) & (np.arange(len(ells)) % 3 == 0))
    er, wlr, hir, lor = ells[rsel], wl[rsel], hi[rsel], lo[rsel]
    wlor = (2 * er[lor] + 1) * cee[rsel][lor]

    def ratios(srcx, variants):
        Hs = {lab: histories(srcx, **kw)["STUR-B (ln t)"] for lab, kw in variants.items()}
        ce, cb = srcx.transfers(er, Hs)
        out = {}
        for lab in variants:
            b = beta_eff(ce, cb[lab])
            bh = np.sum(wlr[hir] * b[hir]) / np.sum(wlr[hir])
            out[lab] = float(np.sum(wlor * b[lor]) / np.sum(wlor) / bh)
        return out
    phases = np.linspace(0, 2 * np.pi, 7)[:-1]
    variants = {"eps = 0 (baseline)": {}, "t_c = 1e5 yr": dict(t_c=1e-4), "t_c = 1 Myr": dict(t_c=1e-3)}
    for e_ in (0.5, 1.0):
        for i, ph in enumerate(phases):
            variants[f"eps={e_} ph{i}"] = dict(eps=e_, phase=ph)
    rr = ratios(src, variants)
    for lab in ("eps = 0 (baseline)", "t_c = 1e5 yr", "t_c = 1 Myr"):
        rob[lab] = rr[lab]
        print(f"    {lab:28s} {rob[lab]:.3f}")
    for e_ in (0.5, 1.0):
        v = [rr[f"eps={e_} ph{i}"] for i in range(len(phases))]
        rob[f"eps = {e_}, phases"] = [min(v), max(v)]
        print(f"    {'eps = ' + str(e_) + ', 6 phases':28s} [{min(v):.3f}, {max(v):.3f}]")
    for lab, kw in [("tau - 1 sigma", dict(tau=DATA['tau'][0] - DATA['tau'][1])),
                    ("tau + 1 sigma", dict(tau=DATA['tau'][0] + DATA['tau'][1])),
                    ("reion width dz = 1.5", dict(dz_reion=1.5))]:
        rob[lab] = ratios(Sources(**kw), {lab: {}})[lab]
        print(f"    {lab:28s} {rob[lab]:.3f}")
    spread = max(abs(v - rob["eps = 0 (baseline)"]) if not isinstance(v, list)
                 else max(abs(x - rob["eps = 0 (baseline)"]) for x in v) for v in rob.values())
    gate("ratio robust to unknowns (max shift < 0.05)", spread < 0.05, f"max shift = {spread:.3f}")

    # ---- LiteBIRD forecast: interpolate beta_eff(l) to all l, C_EB = 1/2 sin(4 beta)(C_EE - C_BB)
    L = np.arange(0, lmax + 1)
    templ = {}
    for n, p_ in preds.items():
        b = np.interp(L, ells, p_['beta_eff_by_ell'])
        cl = src.cl_len[:lmax + 1]
        templ[n] = 0.5 * np.sin(4 * np.radians(b)) * (cl[:, 1] - cl[:, 2])
    fc = eb_forecast(src, L, templ, "STUR-B (ln t)", fsky, noise, fwhm, lmax)
    det = 1 / fc['sigma_A_marg_alpha']
    print(f"\n  LiteBIRD EB forecast (f_sky = {fsky}, {noise} uK-arcmin, {fwhm}' FWHM, l <= {lmax}):")
    print(f"    sigma(A) with alpha known : {fc['sigma_A_fixed_alpha']:.4f}  -> {1 / fc['sigma_A_fixed_alpha']:.0f} sigma")
    print(f"    sigma(A) alpha marginalised: {fc['sigma_A_marg_alpha']:.4f}  -> tomographic signal at {det:.1f} sigma")
    s_db_lb = abs(P['delta_beta']) / det
    print(f"    => computed sigma(Delta beta) = {s_db_lb:.3f} deg  (Stage 10 quoted 0.05, Sherwin & Namikawa 2021)")
    print("    Delta chi^2 of competing histories against STUR-B data (amplitude and alpha free):")
    for n, d in fc['delta_chi2'].items():
        print(f"      {n:34s} Delta chi^2 = {d:7.2f}  ({np.sqrt(d):.1f} sigma)")

    # ---- primordial B-modes are cosmic variance for the l = 2-10 EB measurement
    print("\n  sigma(Delta beta) vs tensor amplitude (the GENESIS r prediction degrades its own test):")
    r_scan = {}
    for r_, lab in ((0.0, "r = 0 (Sherwin & Namikawa-like)"), (0.001, "r = 0.001"),
                    (0.0035, "r = 0.0035 (GENESIS R^2, used above)"), (0.0139, "r = 0.0139 (stur_inflation.py)")):
        pr_ = camb.set_params(**COSMO, tau=DATA['tau'][0], r=r_, lmax=2500, WantTensors=r_ > 0)
        clr = camb.get_results(pr_).get_total_cls(CMB_unit='muK', raw_cl=True)
        f_ = eb_forecast(src, L, templ, "STUR-B (ln t)", fsky, noise, fwhm, lmax, cl=clr)
        sdb = abs(P['delta_beta']) * f_['sigma_A_marg_alpha']
        r_scan[str(r_)] = dict(sigma_delta_beta_deg=sdb, signal_sigma=1 / f_['sigma_A_marg_alpha'])
        print(f"    {lab:38s} sigma(Delta beta) = {sdb:.3f} deg   STUR-B Delta beta at {1 / f_['sigma_A_marg_alpha']:.1f} sigma")

    crit = [
        f"LiteBIRD finds Delta beta inconsistent with {P['delta_beta']:+.3f} deg at > 3 sigma (combined, computed sigma "
        f"{s_db_lb:.3f} deg at r = 0.0035): STUR-B log-time accrual excluded. NOTE: at this sigma the test is weak "
        f"(late-only rotation sits {np.sqrt(fc['delta_chi2']['late-only / miscalibration']):.1f} sigma away); it is a "
        f"consistency check, not a decisive test, unless r is small",
        "LiteBIRD measures r < 0.0010 at 95%: GENESIS R^2 inflation (any reheating) excluded",
        "LiteBIRD finds |beta| < 3 x 0.02 deg at high l: STUR-B coupling kappa excluded",
        "beta varies with frequency across LiteBIRD bands beyond Faraday/foreground expectations: STUR-B (achromatic) excluded",
        f"beta_eff(l) at l = 2-10 inconsistent with the stored curve at > 3 sigma for every eps, phase in the robustness scan",
    ]
    payload = dict(
        pipeline="GENESIS v10 Stage 10b (full Boltzmann, CAMB %s)" % camb.__version__,
        supersedes_method_of="GENESIS v10 Stage 10 (simplified LOS); Stage 10 pre-registration retained",
        authors="Sheldon Lindberg",
        hypothesis="STUR-B: CMB polarisation rotated by resistance holonomy accrued in chronomagnetic log-time",
        assumptions={"A1-A4": "unchanged from Stage 10", "status": "bridge hypothesis; not derived from the STUR action",
                     "kappa_calibration": "EB-weighted beta_eff over l = 50-1500 equals beta_now",
                     "method": "exact CAMB E-mode sources, rotation applied at emission"},
        inputs=dict(beta_now=DATA['beta_now'], tau=DATA['tau'], cosmology=COSMO, z_re=src.zre),
        fitted=dict(kappa_deg=kappa, s_kappa_deg=s_kappa),
        predictions=dict(
            ratio_reio_over_rec=P['ratio'], beta_reio_deg=P['beta_reio'], delta_beta_deg=P['delta_beta'],
            s_delta_beta_deg=s_db,
            beta_eff_by_ell={int(l): float(b) for l, b in zip(ells, P['beta_eff_by_ell'])},
            ratio_robustness=rob,
            competing={n: dict(ratio=p_['ratio'], delta_beta=p_['delta_beta']) for n, p_ in preds.items()
                       if n != "STUR-B (ln t)"},
        ),
        litebird_forecast=dict(fsky=fsky, noise_uK_arcmin=noise, fwhm_arcmin=fwhm, lmax=lmax,
                               detection_sigma_alpha_marg=det, sigma_delta_beta_deg=s_db_lb,
                               delta_chi2=fc['delta_chi2'], sigma_delta_beta_vs_r=r_scan),
        falsification=crit,
        gates=gates,
    )
    h = preregister(payload, out_json)
    print(f"\n  gates: {sum(g['passed'] for g in gates)}/{len(gates)} passed")
    print(f"  pre-registration written to {out_json}\n  SHA-256 = {h}")
    return payload, h


def _clean(x):
    if isinstance(x, dict):
        return {str(k): _clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_clean(v) for v in x]
    if isinstance(x, np.ndarray):
        return [_clean(v) for v in x.tolist()]
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        return x.item()
    return x


def preregister(payload, path):
    payload = _clean(payload)
    with open(os.path.abspath(__file__), 'rb') as fh:
        payload['code_sha256'] = hashlib.sha256(fh.read()).hexdigest()
    payload['generated_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    canon = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=True)
    with open(path, 'w') as fh:
        fh.write(canon)
    return hashlib.sha256(canon.encode()).hexdigest()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="GENESIS v10 Stage 10b")
    ap.add_argument("--fsky", type=float, default=0.6)
    ap.add_argument("--noise", type=float, default=2.2, help="polarisation noise [uK-arcmin]")
    ap.add_argument("--fwhm", type=float, default=30.0, help="beam FWHM [arcmin]")
    ap.add_argument("--lmax", type=int, default=1000)
    ap.add_argument("--out", default="genesis_v10b_preregistration.json")
    a = ap.parse_args()
    run(a.fsky, a.noise, a.fwhm, a.lmax, a.out)
