#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10c: pre-registration of STUR-M3a (oscillating R-phase)
================================================================================
Registered ALONGSIDE STUR-B (Stage 10, Stage 10b). Neither replaces the other;
LiteBIRD data decide. Origin: scripts/genesis_v10_phase_suppression.py, the only
STUR-internal mechanism found that gives a natural birefringence amplitude.

Hypothesis STUR-M3a
  H1  The R-field phase zero mode OSCILLATES in log-time with the chronomagnetic
      frequency and constant amplitude (the repo's own equation,
      DERIVATION_CHAIN_INFINITY.md 2.3b, friction 1/t):
          theta(t) = A0 sin(omega ln(t/t0) + delta),   omega = 2 pi^2 (v7.0 exact)
  H2  Only leptons carry R-charge (X = 1 each, 3 generations): photon anomaly
      c_g = 3, colour anomaly c_s = 0 (keeps theta_QCD = 0; no QCD axion).
  H3  Photon polarisation rotates by beta = (c_g alpha/2pi)[theta(t0) - theta(t_emit)].
  Status: H1 needs a restoring force that explicitly breaks the Master Action's
  U(1), and H2 is not derived; both are stated assumptions.

Rules fixed before computing
  * A0 <= 3 rad (the bound used in the suppression scan); 0 <= delta < 2 pi.
  * At each delta, A0 is solved so that the recombination (high-l) angle equals
    beta_now. Every delta with a solution counts; the predictions are the full
    ranges over those delta. Nothing is selected afterwards.
  * Same CAMB sources, LiteBIRD model and r = 0.0035 as Stage 10b.

Writes genesis_v10c_m3a_preregistration.json (canonical JSON) + SHA-256.
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
_spec = importlib.util.spec_from_file_location("g10b", os.path.join(HERE, "genesis_v10b_boltzmann.py"))
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)

ALPHA = 1 / 137.035999
OMEGA = 2 * np.pi ** 2
C_G, C_S = 3, 0
K = C_G * ALPHA / (2 * np.pi)
A_MAX = 3.0
BETA_NOW, S_BETA_NOW = G.DATA['beta_now'][0], G.DATA['beta_now'][1]
PRIOR = {
    "stage10_STUR-B": "c05406dd94c6ea596166a9e2121e895975ca4fb7e06e579cf42092f95d265bb3",
    "stage10b_STUR-B": "8dde755844ca7c2416a6618f4565bce815ea3fd8d9e9268492e509ebb2663018",
}
STURB_STAGE10B = dict(ratio=0.2307, delta_beta=-0.2131)


def theta_fn(A0, delta, t0):
    return lambda t: A0 * np.sin(OMEGA * np.log(t / t0) + delta)


def run(fsky=0.6, noise=2.2, fwhm=30.0, lmax=1000, out_json="genesis_v10c_m3a_preregistration.json"):
    gates = []

    def gate(name, ok, detail):
        gates.append(dict(name=name, passed=bool(ok), detail=detail))
        print(f"  gate: {name:52s} {detail:36s} {'PASS' if ok else 'FAIL'}")

    print("\n=== Stage 10c: STUR-M3a pre-registration (oscillating R-phase, leptons only) ===")
    src = G.Sources(r=0.0035)
    t0 = src.t0
    gh = src.grids["hi"]
    vis = src.res.get_background_time_evolution(gh['eta'], ['visibility'])['visibility'] * gh['w']
    wv = vis / vis.sum()

    def rec_angle(A0, d):
        th = theta_fn(A0, d, t0)
        z2 = np.sum(wv * np.exp(2j * K * (th(t0) - th(gh['t']))))
        return np.degrees(np.angle(z2) / 2), abs(z2)

    # ---- exact calibration. beta ~ 0.3 deg, so beta_eff(l) is linear in A0: compute the
    # exact high-l angle per unit A0 at every phase, solve A0 = beta_now / beta_high, then
    # verify with a second exact pass at the solved amplitudes.
    ells_lo = np.arange(2, 41)
    ells_hi = np.unique(np.round(np.geomspace(45, 1500, 40)).astype(int))
    ells = np.concatenate([ells_lo, ells_hi])
    nl_h = G.litebird_noise(ells_hi, noise, fwhm)
    deltas = np.linspace(0, 2 * np.pi, 145)[:-1]
    H1 = {float(d): (lambda z, t, th=theta_fn(1.0, d, t0): np.degrees(K * (th(t0) - th(t)))) for d in deltas}
    print(f"  pass 1: exact high-l angle per unit A0 at {len(deltas)} phases ...")
    ce1, cb1 = src.transfers(ells_hi, H1)
    hh = ells_hi >= 50
    wl1 = (2 * ells_hi + 1) * ce1 ** 2 / ((ce1 + nl_h) * (src.cl_len[ells_hi, 2] + nl_h))
    sols = {}
    for d in H1:
        b1 = G.beta_eff(ce1, cb1[d])
        bh1 = np.sum(wl1[hh] * b1[hh]) / np.sum(wl1[hh])
        if bh1 > 0 and BETA_NOW / bh1 <= A_MAX:
            sols[d] = BETA_NOW / bh1
    ds = np.array(sorted(sols))
    print(f"  phases with a solution (A0 <= {A_MAX} rad): {len(ds)}/{len(deltas)};"
          f" delta in [{ds.min():.3f}, {ds.max():.3f}] rad")
    print(f"  A0 range: {min(sols.values()):.3f} - {max(sols.values()):.3f} rad")

    # ---- pass 2: exact transfers at the solved amplitudes (+ STUR-B and miscalibration)
    H = {d: (lambda z, t, th=theta_fn(sols[d], d, t0): np.degrees(K * (th(t0) - th(t)))) for d in ds}
    H["STUR-B"] = G.histories(src)["STUR-B (ln t)"]
    H["late-only / miscalibration"] = lambda z, t: 1.0 + 0 * z
    print(f"  pass 2: exact transfers at {len(ells)} multipoles for {len(H)} histories ...")
    cee, ceb = src.transfers(ells, H)
    gate("C_EE vs CAMB, l = 2-40", np.max(np.abs(cee[:39] / src.cl_unl[ells_lo, 1] - 1)) < 0.01,
         f"max dev {np.max(np.abs(cee[:39] / src.cl_unl[ells_lo, 1] - 1)):.1e}")
    hi, lo = ells >= 50, ells <= 10
    nl = G.litebird_noise(ells, noise, fwhm)
    wl = (2 * ells + 1) * cee ** 2 / ((cee + nl) * (src.cl_len[ells, 2] + nl))
    wlo = (2 * ells[lo] + 1) * cee[lo]

    preds = {}
    for d in ds:
        b = G.beta_eff(cee, ceb[d])
        bh = float(np.sum(wl[hi] * b[hi]) / np.sum(wl[hi]))
        br = float(np.sum(wlo * b[lo]) / np.sum(wlo))
        preds[d] = dict(A0=sols[d], beta_high=bh, beta_reio=br, ratio=br / bh, delta_beta=br - bh,
                        pol=rec_angle(sols[d], d)[1], beta_eff_by_ell=b)
    bh_all = [p['beta_high'] for p in preds.values()]
    gate("exact high-l angle = beta_now at solved A0 (linearity)",
         max(abs(x - BETA_NOW) for x in bh_all) < 1e-3, f"range {min(bh_all):.5f}-{max(bh_all):.5f} deg")
    ratios = np.array([p['ratio'] for p in preds.values()])
    dbs = np.array([p['delta_beta'] for p in preds.values()])
    pols = np.array([p['pol'] for p in preds.values()])
    print(f"\n  PREDICTIONS (STUR-M3a), full range over all {len(ds)} admissible phases:")
    print(f"    beta_reio/beta_rec = {ratios.min():.3f} to {ratios.max():.3f}")
    print(f"    Delta beta         = {dbs.min():+.4f} to {dbs.max():+.4f} deg")
    print(f"    recombination polarisation fraction >= {pols.min():.5f}")
    hdev = max(np.max(np.abs(p['beta_eff_by_ell'][hi] - BETA_NOW)) for p in preds.values())
    print(f"    high-l structure: max |beta_eff(l) - beta_now| over l = 50-1500 is {hdev:.4f} deg"
          " (oscillation period in ln t ~ visibility width; stored per phase)")
    pm = preds[ds[len(ds) // 2]]['beta_eff_by_ell']
    print("    median phase, high l: " + " ".join(f"{l}:{b:.3f}" for l, b in zip(ells[hi][::4], pm[hi][::4])))
    print(f"    d beta/dt today <= {np.degrees(K * max(sols.values()) * OMEGA / (t0 * 1e9)):.1e} deg/yr")
    print(f"    (STUR-B, Stage 10b: ratio {STURB_STAGE10B['ratio']}, Delta beta {STURB_STAGE10B['delta_beta']} deg)")

    # ---- robustness to tau and reionization width (median-phase solution)
    dmed = ds[len(ds) // 2]
    rob = {}
    for lab, kw in [("tau - 1 sigma", dict(tau=G.DATA['tau'][0] - G.DATA['tau'][1])),
                    ("tau + 1 sigma", dict(tau=G.DATA['tau'][0] + G.DATA['tau'][1])),
                    ("reion width dz = 1.5", dict(dz_reion=1.5))]:
        sx = G.Sources(**kw)
        th = theta_fn(sols[dmed], dmed, t0)
        e2 = np.concatenate([np.arange(2, 11), [100, 400, 1000]])
        ce, cb = sx.transfers(e2, {"m": lambda z, t, th=th: np.degrees(K * (th(t0) - th(t)))})
        b = G.beta_eff(ce, cb["m"])
        w2 = (2 * e2[:9] + 1) * ce[:9]
        rob[lab] = float(np.sum(w2 * b[:9]) / np.sum(w2) / np.mean(b[9:]))
        print(f"    robustness {lab:24s} ratio = {rob[lab]:.3f}")

    # ---- LiteBIRD: can it tell M3a from STUR-B, and from miscalibration?
    L = np.arange(0, lmax + 1)
    cl = src.cl_len[:lmax + 1]

    def templ(b_by_ell):
        b = np.interp(L, ells, b_by_ell)
        return 0.5 * np.sin(4 * np.radians(b)) * (cl[:, 1] - cl[:, 2])
    T = {"M3a": templ(preds[dmed]['beta_eff_by_ell']),
         "STUR-B": templ(G.beta_eff(cee, ceb["STUR-B"]) * BETA_NOW /
                         (np.sum(wl[hi] * G.beta_eff(cee, ceb["STUR-B"])[hi]) / np.sum(wl[hi]))),
         "late-only / miscalibration": templ(G.beta_eff(cee, ceb["late-only / miscalibration"]) * BETA_NOW)}
    f_m3 = G.eb_forecast(src, L, T, "M3a", fsky, noise, fwhm, lmax)
    f_sb = G.eb_forecast(src, L, T, "STUR-B", fsky, noise, fwhm, lmax)
    d_sb_given_m3 = f_m3['delta_chi2']["STUR-B"]
    d_m3_given_sb = f_sb['delta_chi2']["M3a"]
    print(f"\n  LiteBIRD (alpha marginalised, r = 0.0035): if M3a is true, STUR-B is disfavoured at"
          f" {np.sqrt(d_sb_given_m3):.1f} sigma;")
    print(f"    if STUR-B is true, M3a is disfavoured at {np.sqrt(d_m3_given_sb):.1f} sigma."
          f" M3a vs miscalibration: {np.sqrt(f_m3['delta_chi2']['late-only / miscalibration']):.2f} sigma.")

    crit = [
        "LiteBIRD finds |beta| < 3 x 0.02 deg at high l (absolute calibration): STUR-M3a excluded (it requires beta = beta_now != 0)",
        f"LiteBIRD finds Delta beta inconsistent with [{dbs.min():+.3f}, {dbs.max():+.3f}] deg at > 3 sigma (combined): STUR-M3a excluded",
        "beta varies with frequency across LiteBIRD bands beyond Faraday/foreground expectations: STUR-M3a (achromatic) excluded",
        "beta_eff(l) inconsistent at > 3 sigma with the stored curve of every admissible phase: STUR-M3a excluded",
        "a QCD axion is detected, or quarks are shown to carry R-charge: assumption H2 (c_s = 0) fails, STUR-M3a excluded",
    ]
    payload = dict(
        pipeline="GENESIS v10 Stage 10c (STUR-M3a, full Boltzmann, CAMB %s)" % camb.__version__,
        registered_alongside=PRIOR,
        authors="Sheldon Lindberg",
        hypothesis="STUR-M3a: CMB polarisation rotated by an oscillating (not rotating) R-field phase, leptons-only R-charge",
        assumptions=dict(
            H1="theta(t) = A0 sin(omega ln(t/t0) + delta), omega = 2 pi^2, constant amplitude (repo friction 1/t)",
            H2="only leptons carry R-charge: c_g = 3, c_s = 0",
            H3="beta = (c_g alpha / 2 pi)[theta(t0) - theta(t_emit)]",
            status="H1 needs an explicit U(1)-breaking restoring force; H1 and H2 are not derived from the Master Action",
            rules="A0 <= 3 rad; A0 solved per delta so the exact EB-weighted high-l (l = 50-1500) angle equals beta_now; predictions are full ranges over all admissible delta",
        ),
        inputs=dict(beta_now=G.DATA['beta_now'], tau=G.DATA['tau'], cosmology=G.COSMO, r=0.0035,
                    c_g=C_G, c_s=C_S, omega=OMEGA, A_max=A_MAX),
        fitted=dict(A0_range_rad=[min(sols.values()), max(sols.values())],
                    delta_range_rad=[float(ds.min()), float(ds.max())], n_admissible_phases=len(ds)),
        predictions=dict(
            ratio_reio_over_rec=[float(ratios.min()), float(ratios.max())],
            delta_beta_deg=[float(dbs.min()), float(dbs.max())],
            recombination_pol_fraction_min=float(pols.min()),
            achromatic=True,
            beta_eff_by_ell_per_phase={f"{d:.4f}": {int(l): float(b) for l, b in zip(ells, preds[d]['beta_eff_by_ell'])}
                                       for d in ds},
            ratio_robustness_median_phase=rob,
            no_qcd_axion=True,
        ),
        litebird_forecast=dict(fsky=fsky, noise_uK_arcmin=noise, fwhm_arcmin=fwhm, lmax=lmax,
                               sigma_STURB_disfavoured_if_M3a_true=float(np.sqrt(d_sb_given_m3)),
                               sigma_M3a_disfavoured_if_STURB_true=float(np.sqrt(d_m3_given_sb)),
                               sigma_M3a_vs_miscalibration=float(np.sqrt(f_m3['delta_chi2']['late-only / miscalibration']))),
        falsification=crit,
        gates=gates,
    )
    h = preregister(payload, out_json)
    print(f"\n  gates: {sum(g['passed'] for g in gates)}/{len(gates)} passed")
    print(f"  pre-registration written to {out_json}\n  SHA-256 = {h}")
    return payload, h


def preregister(payload, path):
    payload = G._clean(payload)
    with open(os.path.abspath(__file__), 'rb') as fh:
        payload['code_sha256'] = hashlib.sha256(fh.read()).hexdigest()
    payload['generated_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    canon = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=True)
    with open(path, 'w') as fh:
        fh.write(canon)
    return hashlib.sha256(canon.encode()).hexdigest()


if __name__ == "__main__":
    run()
