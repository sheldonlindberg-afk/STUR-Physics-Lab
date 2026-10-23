#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10c forecast: is STUR-M3a's l-dependent beta_eff detectable?
================================================================================
STUR-M3a (scripts/genesis_v10c_m3a_preregistration.json) rotates polarisation by
an R-phase that oscillates in ln t with period ln(lambda) = 1/pi, comparable to
the width of the recombination visibility window. Different multipoles weight
different parts of that window, so beta_eff(l) is not flat at high l. A constant
rotation (any true isotropic beta plus instrument miscalibration alpha) is flat,
so the SHAPE is calibration-free.

  1. Reproduce the registered model: re-solve A0(delta) with the registered rule
     (exact EB-weighted high-l angle, l = 50-1500, equals beta_now) and gate the
     result against the per-phase beta_eff(l) curves stored in the pre-registration.
  2. Extend exact CAMB transfers to l = 3000 (wider k grid).
  3. For each experiment, Delta chi^2 of the best-fit FLAT rotation (free angle)
     against M3a data, for every admissible phase. STUR-B is run as a control.

The registered scripts (genesis_v10b_boltzmann.py, genesis_v10c_m3a.py) are only
imported, never modified, so their pre-registration code hashes stay valid.
Instrument parameters are approximate and stated in EXPERIMENTS. Not modelled:
lensing remapping of the EB pattern, foreground residuals, and l-dependent
instrumental EB (beam ellipticity), which could mimic or mask a shape.

Usage:  python genesis_v10c_m3a_lshape.py
================================================================================
"""
import importlib.util
import json
import os

import camb
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


G = _load("g10b", "genesis_v10b_boltzmann.py")
M = _load("g10c", "genesis_v10c_m3a.py")
PREREG = os.path.join(HERE, "genesis_v10c_m3a_preregistration.json")

# name: (noise uK-arcmin in polarisation, FWHM arcmin, f_sky, lmin, lmax)  -- approximate
EXPERIMENTS = {
    "LiteBIRD": (2.2, 30.0, 0.6, 2, 1000),
    "ACT DR6-like": (18.0, 1.4, 0.4, 300, 3000),
    "Simons Obs. LAT-like": (8.0, 1.4, 0.4, 300, 3000),
    "CMB-S4-like (wide)": (2.0, 1.4, 0.4, 300, 3000),
}
gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:54s} {detail:34s} {'PASS' if ok else 'FAIL'}")


def extend_spectra(src, lmax=3500):
    """CAMB spectra to l = 3500 (Sources stops near 2700); same cosmology and r = 0.0035"""
    p = camb.set_params(**G.COSMO, tau=G.DATA['tau'][0], lmax=lmax)
    src.cl_unl = camb.get_results(p).get_unlensed_scalar_cls(CMB_unit='muK', raw_cl=True)
    pt = camb.set_params(**G.COSMO, tau=G.DATA['tau'][0], r=0.0035, lmax=lmax, WantTensors=True)
    src.cl_len = camb.get_results(pt).get_total_cls(CMB_unit='muK', raw_cl=True)


def extend_hi_grid(src, kmax=0.40):
    """replace the high-l grid with a wider k range (needed to l = 3000)"""
    k = np.arange(2e-4, kmax, 2e-4)
    e = np.linspace(150, 800, 1301)
    S = src.res.get_time_evolution(k, e, ['E_source'])[:, :, 0]
    z = src.res.redshift_at_conformal_time(e)
    t = np.array([src.res.physical_time(zz) for zz in z[::25]])
    t = np.exp(np.interp(z, z[::25][::-1], np.log(t)[::-1]))
    src.grids["hi"] = dict(k=k, eta=e, S=S, w=np.gradient(e), z=z, t=t)


def main():
    print("\n=== Stage 10c forecast: STUR-M3a high-l beta_eff(l) shape ===")
    reg = json.load(open(PREREG))
    stored = reg["predictions"]["beta_eff_by_ell_per_phase"]
    src = G.Sources(r=0.0035)
    t0 = src.t0
    noise, fwhm = 2.2, 30.0          # registered calibration weights (Stage 10c defaults)

    # ---- 1. reproduce the registered A0(delta), exactly as genesis_v10c_m3a.py does
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
    gate("same admissible phases as the registration", len(ds) == reg["fitted"]["n_admissible_phases"],
         f"{len(ds)} vs {reg['fitted']['n_admissible_phases']}")
    dev = 0.0
    for d in ds:
        b = G.beta_eff(ce1, cb1[d]) * sols[d]
        ref = stored[f"{d:.4f}"]
        dev = max(dev, max(abs(b[i] - ref[str(l)]) for i, l in enumerate(ells_hi)))
    gate("beta_eff(l) reproduces the stored curves (l = 45-1500)", dev < 1e-4, f"max dev {dev:.1e} deg")

    # ---- 2. extend to l = 3000
    extend_hi_grid(src)
    extend_spectra(src)
    ells = np.unique(np.concatenate([np.arange(2, 41), np.round(np.geomspace(45, 3000, 70)).astype(int)]))
    H = {d: (lambda z, t, th=M.theta_fn(sols[d], d, t0): np.degrees(M.K * (th(t0) - th(t)))) for d in ds}
    H["STUR-B"] = G.histories(src)["STUR-B (ln t)"]
    print(f"  exact transfers to l = 3000: {len(ells)} multipoles x {len(H)} histories ...")
    cee, ceb = src.transfers(ells, H)
    gate("C_EE vs CAMB at l = 1500-3000 (extended grid)",
         np.max(np.abs(cee[ells >= 1500] / src.cl_unl[ells[ells >= 1500], 1] - 1)) < 0.05,
         f"max dev {np.max(np.abs(cee[ells >= 1500] / src.cl_unl[ells[ells >= 1500], 1] - 1)):.1e}")
    hi = ells >= 50
    nl = G.litebird_noise(ells, noise, fwhm)
    wl = (2 * ells + 1) * cee ** 2 / ((cee + nl) * (src.cl_len[ells, 2] + nl))
    curves = {}
    for d in ds:
        curves[d] = G.beta_eff(cee, ceb[d])
    bsb = G.beta_eff(cee, ceb["STUR-B"])
    curves["STUR-B"] = bsb * M.BETA_NOW / (np.sum(wl[hi] * bsb[hi]) / np.sum(wl[hi]))
    dmed = ds[len(ds) // 2]
    print("  M3a median phase, beta_eff(l): " + " ".join(
        f"{l}:{b:.3f}" for l, b in zip(ells[hi][::8], curves[dmed][hi][::8])))
    print("  STUR-B (control),  beta_eff(l): " + " ".join(
        f"{l}:{b:.3f}" for l, b in zip(ells[hi][::8], curves["STUR-B"][hi][::8])))

    # ---- 3. shape-only Delta chi^2: flat rotation with free angle vs the model
    L = np.arange(0, 3001)
    cl = src.cl_len[:3001]
    diff = cl[:, 1] - cl[:, 2]

    def eb(b_by_ell):
        return 0.5 * np.sin(4 * np.radians(np.interp(L, ells, b_by_ell))) * diff
    out = {}
    print(f"\n  {'experiment':22s} {'M3a min':>9s} {'median':>8s} {'max':>8s}   {'STUR-B control':>14s}   (sigma, flat rejected)")
    for name, (nz, fw, fsky, lmin, lmax) in EXPERIMENTS.items():
        ell = np.arange(lmin, lmax + 1)
        n_ = G.litebird_noise(ell, nz, fw)
        var = (cl[ell, 1] + n_) * (cl[ell, 2] + n_) / ((2 * ell + 1) * fsky)
        flat = 0.5 * np.sin(4 * np.radians(1.0)) * diff[ell]      # shape of a constant 1 deg rotation

        def dchi2(model):
            y = model[ell] / np.sqrt(var)
            x = flat / np.sqrt(var)
            a = np.sum(x * y) / np.sum(x * x)
            return float(np.sum((y - a * x) ** 2))
        sig = np.sqrt([dchi2(eb(curves[d])) for d in ds])
        ctrl = np.sqrt(dchi2(eb(curves["STUR-B"])))
        out[name] = dict(m3a_min=float(sig.min()), m3a_median=float(np.median(sig)),
                         m3a_max=float(sig.max()), sturb=float(ctrl))
        print(f"  {name:22s} {sig.min():8.2f}σ {np.median(sig):7.2f}σ {sig.max():7.2f}σ   {ctrl:13.2f}σ")

    best = max(out, key=lambda n: out[n]['m3a_median'])
    print(f"\n  most sensitive: {best} (median {out[best]['m3a_median']:.1f} sigma over admissible phases)")
    print("  Caveats: lensing remapping, foregrounds and l-dependent instrumental EB are not modelled;")
    print("  noise levels are approximate. Treat these as order-of-magnitude detectability estimates.")
    print(f"\n  gates: {sum(gates)}/{len(gates)} passed")
    return out


if __name__ == "__main__":
    main()
