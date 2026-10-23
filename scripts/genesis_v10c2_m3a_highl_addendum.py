#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10c2: STUR-M3a high-l addendum pre-registration
================================================================================
Addendum to scripts/genesis_v10c_m3a_preregistration.json (Stage 10c). That file
stores beta_eff(l) only to l = 1500, but M3a's decisive signature, the decline
of beta_eff(l) below beta_now, is strongest at l = 1500-3000. This addendum:

  1. Re-derives the 49 admissible phases and their A0 with the REGISTERED rule
     (exact EB-weighted l = 50-1500 angle equals beta_now, LiteBIRD weights).
     Gate: the stored Stage 10c curves are reproduced to < 1e-4 deg (l <= 1500).
  2. Pre-registers beta_eff(l) for l = 45-3000 for every admissible phase.
  3. Records the calibration-free shape test (flat rotation with a free angle vs
     M3a) for LiteBIRD, ACT DR6-like, SO LAT-like and CMB-S4-like surveys, with
     its falsification criterion.
  4. KNOWN LIMITATION of the registered calibration: beta_now = 0.277 deg comes
     from an ACT DR6 + Planck EB analysis, which weights l up to ~3000, while the
     registered rule weights l = 50-1500 with LiteBIRD noise. With the registered
     A0 (NOT re-solved), this computes the angle an ACT DR6 + Planck-like
     analysis would measure. The registered predictions are not altered.

Nothing here modifies a registered script; genesis_v10b_boltzmann.py,
genesis_v10c_m3a.py and genesis_v10c_m3a_lshape.py are imported only.
Instrument models are approximate and stated in ACT_PLANCK and LS.EXPERIMENTS.
Not modelled: lensing remapping of the EB pattern, foreground residuals,
l-dependent instrumental EB (beam ellipticity).

Writes genesis_v10c2_m3a_highl_addendum.json (canonical JSON) + SHA-256.
================================================================================
"""
import datetime
import hashlib
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


LS = _load("g10c_lshape", "genesis_v10c_m3a_lshape.py")
G, M = LS.G, LS.M
PREREG = os.path.join(HERE, "genesis_v10c_m3a_preregistration.json")
PRIOR = {
    "stage10_STUR-B": "c05406dd94c6ea596166a9e2121e895975ca4fb7e06e579cf42092f95d265bb3",
    "stage10b_STUR-B": "8dde755844ca7c2416a6618f4565bce815ea3fd8d9e9268492e509ebb2663018",
    "stage10c_STUR-M3a": "d3008ee624930ae356f4cfe3c89f331d7cbae8628346c895a4dba37f44224638",
}
# approximate noise models of the analysis that produced beta_now (polarisation noise
# uK-arcmin, FWHM arcmin, f_sky, lmin, lmax); combined by inverse variance per l
ACT_PLANCK = {
    "ACT DR6-like": (18.0, 1.4, 0.4, 300, 3000),
    "Planck PR4-like": (60.0, 7.0, 0.6, 30, 1500),
}


def file_sha256(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run(out_json="genesis_v10c2_m3a_highl_addendum.json"):
    gates = []

    def gate(name, ok, detail):
        gates.append(dict(name=name, passed=bool(ok), detail=detail))
        print(f"  gate: {name:54s} {detail:34s} {'PASS' if ok else 'FAIL'}")

    print("\n=== Stage 10c2: STUR-M3a high-l addendum pre-registration ===")
    gate("Stage 10c pre-registration file unchanged", file_sha256(PREREG) == PRIOR["stage10c_STUR-M3a"],
         "SHA-256 matches")
    reg = json.load(open(PREREG))
    stored = reg["predictions"]["beta_eff_by_ell_per_phase"]
    src = G.Sources(r=0.0035)
    t0 = src.t0

    # ---- 1. registered A0 rule, exactly as genesis_v10c_m3a.py
    ells_hi = np.unique(np.round(np.geomspace(45, 1500, 40)).astype(int))
    nl_h = G.litebird_noise(ells_hi, 2.2, 30.0)
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
    gate("same admissible phases as Stage 10c", len(ds) == reg["fitted"]["n_admissible_phases"],
         f"{len(ds)} vs {reg['fitted']['n_admissible_phases']}")
    a_lo, a_hi = reg["fitted"]["A0_range_rad"]
    gate("same A0 range as Stage 10c", abs(min(sols.values()) - a_lo) < 1e-9 and abs(max(sols.values()) - a_hi) < 1e-9,
         f"{min(sols.values()):.4f}-{max(sols.values()):.4f} rad")

    # ---- 2. exact transfers to l = 3000 at the registered A0
    LS.extend_hi_grid(src)
    LS.extend_spectra(src)
    ells = np.unique(np.concatenate([ells_hi, np.round(np.geomspace(1500, 3000, 30)).astype(int)]))
    H = {d: (lambda z, t, th=M.theta_fn(sols[d], d, t0): np.degrees(M.K * (th(t0) - th(t)))) for d in ds}
    print(f"  exact transfers l = 45-3000: {len(ells)} multipoles x {len(H)} phases ...")
    cee, ceb = src.transfers(ells, H)
    curves = {d: G.beta_eff(cee, ceb[d]) for d in ds}
    dev = 0.0
    for d in ds:
        ref = stored[f"{d:.4f}"]
        dev = max(dev, max(abs(curves[d][i] - ref[str(int(l))]) for i, l in enumerate(ells) if str(int(l)) in ref))
    gate("reproduces stored Stage 10c curves (l <= 1500)", dev < 1e-4, f"max dev {dev:.1e} deg")
    hiL = ells >= 1500
    gate("C_EE vs CAMB at l = 1500-3000",
         np.max(np.abs(cee[hiL] / src.cl_unl[ells[hiL], 1] - 1)) < 0.05,
         f"max dev {np.max(np.abs(cee[hiL] / src.cl_unl[ells[hiL], 1] - 1)):.1e}")
    b3000 = np.array([curves[d][-1] for d in ds])
    print(f"  beta_eff(l = {ells[-1]}) over admissible phases: {b3000.min():.3f} - {b3000.max():.3f} deg")

    # ---- 3. calibration-free shape test (same method as genesis_v10c_m3a_lshape.py)
    L = np.arange(0, 3001)
    cl = src.cl_len[:3001]
    diff = cl[:, 1] - cl[:, 2]

    def eb(b_by_ell):
        return 0.5 * np.sin(4 * np.radians(np.interp(L, ells, b_by_ell))) * diff

    def var_for(nz, fw, fsky, lmin, lmax):
        ell = np.arange(lmin, lmax + 1)
        n_ = G.litebird_noise(ell, nz, fw)
        return ell, (cl[ell, 1] + n_) * (cl[ell, 2] + n_) / ((2 * ell + 1) * fsky)

    shape = {}
    print(f"\n  shape test (flat rotation with free angle rejected if M3a true), over {len(ds)} phases:")
    for name, cfg in LS.EXPERIMENTS.items():
        ell, var = var_for(*cfg)
        x = (0.5 * np.sin(4 * np.radians(1.0)) * diff[ell]) / np.sqrt(var)
        sig = []
        for d in ds:
            y = eb(curves[d])[ell] / np.sqrt(var)
            a = np.sum(x * y) / np.sum(x * x)
            sig.append(np.sqrt(np.sum((y - a * x) ** 2)))
        sig = np.array(sig)
        shape[name] = dict(config=cfg, sigma_min=float(sig.min()), sigma_median=float(np.median(sig)),
                           sigma_max=float(sig.max()))
        print(f"    {name:22s} {sig.min():6.2f} / {np.median(sig):6.2f} / {sig.max():6.2f} sigma (min/median/max)")

    # ---- 4. known limitation: the angle an ACT DR6 + Planck-like analysis would measure
    Ld = np.arange(2, 3001)
    w_tot = np.zeros(len(Ld))
    for name, (nz, fw, fsky, lmin, lmax) in ACT_PLANCK.items():
        m = (Ld >= lmin) & (Ld <= lmax)
        n_ = G.litebird_noise(Ld[m], nz, fw)
        w_tot[m] += (2 * Ld[m] + 1) * fsky * cl[Ld[m], 1] ** 2 / ((cl[Ld[m], 1] + n_) * (cl[Ld[m], 2] + n_))
    b_act = np.array([np.sum(w_tot * np.interp(Ld, ells, curves[d])) / np.sum(w_tot) for d in ds])
    wmean_l = float(np.sum(w_tot * Ld) / np.sum(w_tot))
    print(f"\n  ACT DR6 + Planck-like weighted beta at the REGISTERED A0 (information-weighted mean l = {wmean_l:.0f}):")
    print(f"    {b_act.min():.4f} - {b_act.max():.4f} deg  (registered calibration target {M.BETA_NOW} deg;"
          f" shift {b_act.min() - M.BETA_NOW:+.4f} to {b_act.max() - M.BETA_NOW:+.4f} deg,"
          f" = {(b_act.min() - M.BETA_NOW) / M.S_BETA_NOW:+.2f} to {(b_act.max() - M.BETA_NOW) / M.S_BETA_NOW:+.2f} sigma of beta_now)")

    crit = [
        "A calibration-free EB shape analysis over l = 300-3000 at SO-LAT-like or better sensitivity finds beta_eff(l) "
        "consistent with flat where the stored curves predict rejection of a flat rotation at > 3 sigma for every "
        "admissible phase (CMB-S4-like: min %.1f sigma): STUR-M3a excluded" % shape["CMB-S4-like (wide)"]["sigma_min"],
        "The measured beta_eff(l) is inconsistent at > 3 sigma with the stored curve of every admissible phase: STUR-M3a excluded",
        "A flat rotation is rejected and the decline matches a stored curve: consistent with STUR-M3a (not proof; "
        "l-dependent instrumental EB and lensing remapping must be excluded first)",
    ]
    payload = dict(
        pipeline="GENESIS v10 Stage 10c2 (STUR-M3a high-l addendum, CAMB %s)" % camb.__version__,
        addendum_to=PRIOR["stage10c_STUR-M3a"],
        registered_alongside=PRIOR,
        authors="Sheldon Lindberg",
        hypothesis="STUR-M3a (unchanged from Stage 10c)",
        rules="A0(delta) by the registered Stage 10c rule; no re-solving, nothing fitted",
        predictions=dict(
            beta_eff_by_ell_per_phase_l45_3000={f"{d:.4f}": {int(l): float(b) for l, b in zip(ells, curves[d])}
                                                for d in ds},
            beta_eff_at_lmax_range_deg=[float(b3000.min()), float(b3000.max())],
        ),
        shape_test=dict(method="Delta chi^2 of best-fit flat rotation (free angle) against M3a EB; sigma = sqrt(Delta chi^2)",
                        experiments=shape),
        known_limitation=dict(
            issue="registered calibration weights l = 50-1500 with LiteBIRD noise, but beta_now comes from ACT DR6 + Planck "
                  "(l up to ~3000); M3a's beta_eff declines at high l, so the angle such an analysis would report differs",
            noise_models=ACT_PLANCK,
            information_weighted_mean_l=wmean_l,
            act_planck_weighted_beta_deg=[float(b_act.min()), float(b_act.max())],
            shift_from_beta_now_deg=[float(b_act.min() - M.BETA_NOW), float(b_act.max() - M.BETA_NOW)],
            registered_predictions_altered=False,
        ),
        falsification=crit,
        not_modelled=["lensing remapping of the EB pattern", "foreground residuals",
                      "l-dependent instrumental EB (beam ellipticity)"],
        gates=gates,
    )
    payload = G._clean(payload)
    payload['code_sha256'] = file_sha256(os.path.abspath(__file__))
    payload['generated_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    canon = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=True)
    with open(out_json, 'w') as fh:
        fh.write(canon)
    h = hashlib.sha256(canon.encode()).hexdigest()
    print(f"\n  gates: {sum(g['passed'] for g in gates)}/{len(gates)} passed")
    print(f"  addendum written to {out_json}\n  SHA-256 = {h}")
    return payload, h


if __name__ == "__main__":
    run()
