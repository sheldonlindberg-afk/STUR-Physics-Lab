#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10k: sensitivity of every prediction to the beta input
================================================================================
Replaces the argued statement "a lower beta only rescales the amplitudes; the
shapes are unchanged" with a computation. The full prediction chains are rerun
for three inputs:

  registered      0.277 +/- 0.057 deg  (ACT+Planck joint, arXiv:2608.06480)
  dust-mitigated  0.277 +/- 0.079 deg  (same value, 3.5 sigma significance)
  ACT DR6 alone   0.215 +/- 0.074 deg  (arXiv:2509.13654)

This is a SENSITIVITY ANALYSIS, not a pre-registration: the registered files are
imported, never modified, and their predictions stand as registered.

Method. Within each hypothesis only the amplitude depends on the input (kappa for
STUR-B; A0(delta) for M3a, solved per phase by the registered rule). The
transfers are therefore computed once per unit amplitude and multiplied by each
input's amplitude, and that linearity is NOT assumed: it is gated with exact
transfers at the solved amplitudes. Every row is gated against the registered
numbers at the registered input.

  STUR-B   kappa, ratio, Delta beta +/- sigma, LiteBIRD sigma(Delta beta) and
           detection significance (r = 0.0035, alpha marginalised), Delta chi^2
           of the competing histories (Stage 10b machinery).
  M3a      admissible phases under the registered rule (A0 <= 3 rad, A0 from the
           exact EB-weighted l = 50-1500 angle), delta and A0 ranges, ratio and
           Delta beta ranges, beta_eff(l = 3000) range, and the drift-robust joint
           EB+TB significance (Stage 10h estimator) for SO-like and S4-like.
  windows  C0, STUR-B (c_g ~ 0.02) and M3a f-windows (Stage 10g / 10d formulas).

Usage:  python genesis_v10k_beta_input_sensitivity.py [--cache DIR]
================================================================================
"""
import argparse
import contextlib
import importlib.util
import io
import json
import os

import numpy as np
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


G = _load("g10b", "genesis_v10b_boltzmann.py")
M = _load("g10c", "genesis_v10c_m3a.py")
LS = _load("g10c_ls", "genesis_v10c_m3a_lshape.py")
Hh = _load("g10h", "genesis_v10h_drift_robust_shape.py")
R = _load("g10g", "genesis_v10g_hypothesis_ranking.py")
D = _load("g10d", "genesis_v10d_field_constraints.py")

INPUTS = {
    "registered (0.277 +/- 0.057)": (0.277, 0.057),
    "dust-mitigated (0.277 +/- 0.079)": (0.277, 0.277 / 3.5),
    "ACT DR6 alone (0.215 +/- 0.074)": (0.215, 0.074),
}
REG = "registered (0.277 +/- 0.057)"
NOISE, FWHM, FSKY, LMAX_LB = 2.2, 30.0, 0.6, 1000
A_MAX = M.A_MAX
OMEGA = M.OMEGA

gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:58s} {detail:40s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 92 + "\n  " + s + "\n" + "=" * 92)


def load_json(fname):
    with open(os.path.join(HERE, fname)) as fh:
        return json.load(fh)


# ------------------------------------------------------------------------------
# STUR-B (Stage 10b machinery)
# ------------------------------------------------------------------------------
def sturb(src, cache):
    header("STUR-B: Stage 10b chain per beta input")
    ells = np.concatenate([np.arange(2, 41), np.unique(np.round(np.geomspace(45, 1500, 40)).astype(int))])
    Hs = G.histories(src)                                    # STUR-B at kappa = 1 deg per unit ln t
    fn = os.path.join(cache, "sturb_unit.npz") if cache else None
    if fn and os.path.exists(fn):
        z = np.load(fn, allow_pickle=True)
        cee, ceb = z['cee'], z['ceb'].item()
    else:
        cee, ceb = src.transfers(ells, Hs)
        if fn:
            np.savez(fn, cee=cee, ceb=np.array(ceb, dtype=object))
    hi, lo = ells >= 50, ells <= 10
    nl = G.litebird_noise(ells, NOISE, FWHM)
    wl = (2 * ells + 1) * cee ** 2 / ((cee + nl) * (src.cl_len[ells, 2] + nl))
    wlo = (2 * ells[lo] + 1) * cee[lo]
    hiw = lambda b: float(np.sum(wl[hi] * b[hi]) / np.sum(wl[hi]))
    per_k = hiw(G.beta_eff(cee, ceb["STUR-B (ln t)"]))

    # exact transfers at the solved kappa of each input (linearity gate, not assumed)
    kap = {k: b / per_k for k, (b, s) in INPUTS.items()}
    fe = os.path.join(cache, "sturb_exact.npz") if cache else None
    if fe and os.path.exists(fe):
        z = np.load(fe, allow_pickle=True)
        ceb_x = z['ceb'].item()
    else:
        f1 = Hs["STUR-B (ln t)"]
        Hx = {k: (lambda zz, tt, kk=kk: kk * f1(zz, tt)) for k, kk in kap.items()}
        _, ceb_x = src.transfers(ells, Hx)
        if fe:
            np.savez(fe, ceb=np.array(ceb_x, dtype=object))

    L = np.arange(0, LMAX_LB + 1)
    cl = src.cl_len[:LMAX_LB + 1]
    out = {}
    for k, (b0, s0) in INPUTS.items():
        def norm(name):
            b = G.beta_eff(cee, ceb[name])
            return b * b0 / hiw(b)
        preds = {}
        for n in Hs:
            b = norm(n)
            br = float(np.sum(wlo * b[lo]) / np.sum(wlo))
            preds[n] = dict(beta_reio=br, ratio=br / b0, delta_beta=br - b0, curve=b)
        P = preds["STUR-B (ln t)"]
        # exact (no small-angle rescaling): history built at this input's kappa
        bx = G.beta_eff(cee, ceb_x[k])
        brx = float(np.sum(wlo * bx[lo]) / np.sum(wlo))
        ratio_x = brx / hiw(bx)
        templ = {n: 0.5 * np.sin(4 * np.radians(np.interp(L, ells, p['curve']))) * (cl[:, 1] - cl[:, 2])
                 for n, p in preds.items()}
        fc = G.eb_forecast(src, L, templ, "STUR-B (ln t)", FSKY, NOISE, FWHM, LMAX_LB)
        det = 1 / fc['sigma_A_marg_alpha']
        out[k] = dict(kappa=kap[k], s_kappa=s0 / per_k, ratio=P['ratio'], ratio_exact=ratio_x,
                      delta_beta=P['delta_beta'], s_delta_beta=abs(P['delta_beta']) * s0 / b0,
                      lb_sigma_dbeta=abs(P['delta_beta']) / det, lb_signal_sigma=det,
                      dchi2=fc['delta_chi2'], curve=P['curve'])
    ref = load_json("genesis_v10b_preregistration.json")
    r = out[REG]
    gate("registered row: kappa, ratio, Delta beta, sigma reproduce Stage 10b",
         max(abs(r['kappa'] / ref['fitted']['kappa_deg'] - 1),
             abs(r['ratio'] / ref['predictions']['ratio_reio_over_rec'] - 1),
             abs(r['delta_beta'] / ref['predictions']['delta_beta_deg'] - 1),
             abs(r['lb_sigma_dbeta'] / ref['litebird_forecast']['sigma_delta_beta_deg'] - 1)) < 1e-3,
         f"ratio {r['ratio']:.4f}, Delta beta {r['delta_beta']:+.4f}")
    gate("registered row: competitor Delta chi^2 reproduce Stage 10b",
         max(abs(r['dchi2'][n] - v) for n, v in ref['litebird_forecast']['delta_chi2'].items()) < 1e-3,
         "max |diff| < 1e-3")
    lin = max(abs(o['ratio_exact'] / o['ratio'] - 1) for o in out.values())
    gate("linearity: exact-kappa ratio = rescaled ratio, every input", lin < 1e-3, f"max rel dev {lin:.1e}")
    print(f"\n  {'input':34s} {'kappa [deg]':>12s} {'ratio':>7s} {'Delta beta':>18s} {'LB sigma(Db)':>13s}"
          f" {'LB signal':>9s} {'chi2 early':>10s} {'chi2 late':>9s}")
    for k, o in out.items():
        print(f"  {k:34s} {o['kappa']:7.5f}±{o['s_kappa']:.5f} {o['ratio']:7.4f}"
              f" {o['delta_beta']:+8.4f}±{o['s_delta_beta']:.4f}° {o['lb_sigma_dbeta']:12.4f}°"
              f" {o['lb_signal_sigma']:8.3f}σ {o['dchi2']['early-only (U(1) Master Action)']:10.4f}"
              f" {o['dchi2']['late-only / miscalibration']:9.4f}")
    return out


# ------------------------------------------------------------------------------
# M3a (Stage 10c rule)
# ------------------------------------------------------------------------------
def m3a(src, cache):
    header("M3a: Stage 10c rule per beta input")
    t0 = src.t0
    unit = lambda d: (lambda z, t, th=M.theta_fn(1.0, d, t0): np.degrees(M.K * (th(t0) - th(t))))
    # pass 1, exactly as genesis_v10c_m3a.py: per-unit high-l angle at 144 phases
    ells_h = np.unique(np.round(np.geomspace(45, 1500, 40)).astype(int))
    deltas = np.linspace(0, 2 * np.pi, 145)[:-1]
    f1 = os.path.join(cache, "m3a_pass1.npz") if cache else None
    if f1 and os.path.exists(f1):
        z = np.load(f1, allow_pickle=True)
        ce1, cb1 = z['ce'], z['cb'].item()
    else:
        ce1, cb1 = src.transfers(ells_h, {float(d): unit(d) for d in deltas})
        if f1:
            np.savez(f1, ce=ce1, cb=np.array(cb1, dtype=object))
    nl_h = G.litebird_noise(ells_h, NOISE, FWHM)
    hh = ells_h >= 50
    wl1 = (2 * ells_h + 1) * ce1 ** 2 / ((ce1 + nl_h) * (src.cl_len[ells_h, 2] + nl_h))
    bh1 = {float(d): float(np.sum(wl1[hh] * G.beta_eff(ce1, cb1[float(d)])[hh]) / np.sum(wl1[hh]))
           for d in deltas}
    sol = {}
    for k, (b0, _) in INPUTS.items():
        sol[k] = {d: b0 / v for d, v in bh1.items() if v > 0 and b0 / v <= A_MAX}
    ref = load_json("genesis_v10c_m3a_preregistration.json")
    rs = sol[REG]
    gate("registered row: 49 admissible phases, A0 range of Stage 10c",
         len(rs) == ref['fitted']['n_admissible_phases']
         and abs(min(rs.values()) - ref['fitted']['A0_range_rad'][0]) < 1e-6
         and abs(max(rs.values()) - ref['fitted']['A0_range_rad'][1]) < 1e-6,
         f"{len(rs)} phases, A0 {min(rs.values()):.4f}-{max(rs.values()):.4f}")
    union = sorted(set().union(*[set(s) for s in sol.values()]))
    print(f"  admissible-phase union over inputs: {len(union)} phases")

    # pass 2: per-unit transfers at the registered multipoles (l <= 1500) for the union
    ells = np.concatenate([np.arange(2, 41), ells_h])
    f2 = os.path.join(cache, "m3a_pass2.npz") if cache else None
    if f2 and os.path.exists(f2):
        z = np.load(f2, allow_pickle=True)
        cee, ceb = z['ce'], z['cb'].item()
    else:
        cee, ceb = src.transfers(ells, {d: unit(d) for d in union})
        if f2:
            np.savez(f2, ce=cee, cb=np.array(ceb, dtype=object))
    hi, lo = ells >= 50, ells <= 10
    nl = G.litebird_noise(ells, NOISE, FWHM)
    wl = (2 * ells + 1) * cee ** 2 / ((cee + nl) * (src.cl_len[ells, 2] + nl))
    wlo = (2 * ells[lo] + 1) * cee[lo]
    unit_curve = {d: G.beta_eff(cee, ceb[d]) for d in union}

    # gate: per-unit x registered A0 reproduces the curves stored in the Stage 10c pre-registration
    stored = ref['predictions']['beta_eff_by_ell_per_phase']
    dev = max(abs(unit_curve[d][i] * rs[d] - stored[f"{d:.4f}"][str(int(l))])
              for d in rs for i, l in enumerate(ells))
    gate("registered row: per-unit x A0 reproduces stored Stage 10c curves", dev < 1e-4, f"max dev {dev:.1e} deg")

    # linearity gate: exact transfers at the solved A0 for three phases x every input
    probe = [union[0], union[len(union) // 2], union[-1]]
    ells_p = np.concatenate([np.arange(2, 11), ells_h[[10, 20, 30, len(ells_h) - 1]]])   # on the registered grid
    fp = os.path.join(cache, "m3a_probe.npz") if cache else None
    Hp = {}
    for k in INPUTS:
        for d in probe:
            if d in sol[k]:
                Hp[(k, d)] = (lambda z, t, th=M.theta_fn(sol[k][d], d, t0): np.degrees(M.K * (th(t0) - th(t))))
    if fp and os.path.exists(fp):
        z = np.load(fp, allow_pickle=True)
        cep, cbp = z['ce'], z['cb'].item()
    else:
        cep, cbp = src.transfers(ells_p, Hp)
        if fp:
            np.savez(fp, ce=cep, cb=np.array(cbp, dtype=object))
    idx = [list(ells).index(int(l)) for l in ells_p]
    ldev = max(np.max(np.abs(G.beta_eff(cep, cbp[key]) - unit_curve[key[1]][idx] * sol[key[0]][key[1]]))
               for key in Hp)
    gate("linearity: exact transfers at solved A0 = per-unit x A0", ldev < 1e-4, f"max dev {ldev:.1e} deg ({len(Hp)} cases)")

    # high-l extension to l = 3000 (as genesis_v10c2): per-unit, union phases
    ells_x = np.unique(np.round(np.geomspace(1500, 3000, 20)).astype(int))
    fx = os.path.join(cache, "m3a_highl.npz") if cache else None
    if fx and os.path.exists(fx):
        z = np.load(fx, allow_pickle=True)
        cbx, cex = z['cb'].item(), z['ce']
    else:
        LS.extend_hi_grid(src)
        cex, cbx = src.transfers(ells_x, {d: unit(d) for d in union})
        if fx:
            np.savez(fx, ce=cex, cb=np.array(cbx, dtype=object))
    b3000 = {d: float(G.beta_eff(cex, cbx[d])[-1]) for d in union}
    reg3k = load_json("genesis_v10c2_m3a_highl_addendum.json")['predictions']['beta_eff_at_lmax_range_deg']
    r3 = [b3000[d] * rs[d] for d in rs]
    gate("registered row: beta_eff(3000) range reproduces Stage 10c2",
         abs(min(r3) - reg3k[0]) < 2e-3 and abs(max(r3) - reg3k[1]) < 2e-3,
         f"{min(r3):.4f}-{max(r3):.4f} vs {reg3k[0]:.4f}-{reg3k[1]:.4f}")

    out = {}
    for k, (b0, _) in INPUTS.items():
        s = sol[k]
        rat, dbs = [], []
        for d, A0 in s.items():
            b = unit_curve[d] * A0
            bh = float(np.sum(wl[hi] * b[hi]) / np.sum(wl[hi]))
            br = float(np.sum(wlo * b[lo]) / np.sum(wlo))
            rat.append(br / bh)
            dbs.append(br - bh)
        ds_ = sorted(s)
        out[k] = dict(n=len(s), delta=(min(ds_), max(ds_)), A0=(min(s.values()), max(s.values())),
                      ratio=(min(rat), max(rat)), dbeta=(min(dbs), max(dbs)),
                      b3000=(min(b3000[d] * s[d] for d in s), max(b3000[d] * s[d] for d in s)),
                      new_phases=sorted(set(s) - set(rs)))
    ro = out[REG]
    gate("registered row: ratio and Delta beta ranges reproduce Stage 10c",
         max(abs(ro['ratio'][0] - ref['predictions']['ratio_reio_over_rec'][0]),
             abs(ro['ratio'][1] - ref['predictions']['ratio_reio_over_rec'][1]),
             abs(ro['dbeta'][0] - ref['predictions']['delta_beta_deg'][0]),
             abs(ro['dbeta'][1] - ref['predictions']['delta_beta_deg'][1])) < 1e-4,
         f"ratio {ro['ratio'][0]:.4f}-{ro['ratio'][1]:.4f}")
    print(f"\n  {'input':34s} {'phases':>6s} {'delta [rad]':>13s} {'A0 [rad]':>13s} {'ratio':>15s}"
          f" {'Delta beta [deg]':>18s} {'beta_eff(3000) [deg]':>21s}")
    for k, o in out.items():
        print(f"  {k:34s} {o['n']:6d} {o['delta'][0]:5.3f}-{o['delta'][1]:5.3f} {o['A0'][0]:5.3f}-{o['A0'][1]:5.3f}"
              f"   {o['ratio'][0]:.3f}-{o['ratio'][1]:.3f}   {o['dbeta'][0]:+.4f}-{o['dbeta'][1]:+.4f}"
              f"      {o['b3000'][0]:.3f}-{o['b3000'][1]:.3f}")
        if o['new_phases']:
            print(f"      phases admitted only at this input: {len(o['new_phases'])}"
                  f" (delta {min(o['new_phases']):.3f}-{max(o['new_phases']):.3f})")
    return out, sol, union, unit


# ------------------------------------------------------------------------------
# drift-robust joint EB+TB (Stage 10h estimator), per-unit transfers x A0
# ------------------------------------------------------------------------------
def tbeb(src, sol, union, unit, cache):
    header("M3a: drift-robust joint EB+TB significance per beta input (Stage 10h estimator, unlensed)")
    t0 = src.t0
    lt = np.unique(np.concatenate([np.arange(275, 3001, 25), [3000]]))
    hist = {d: unit(d) for d in union}
    dprobe = sorted(sol[REG])[len(sol[REG]) // 2]           # admissible at the registered input
    hist["probe_reg"] = (lambda z, t, th=M.theta_fn(sol[REG][dprobe], dprobe, t0): np.degrees(M.K * (th(t0) - th(t))))
    hist["const"] = lambda z, t: 0.277 + 0 * z
    ft = os.path.join(cache, "m3a_tbeb.npz") if cache else None
    if ft and os.path.exists(ft):
        z = np.load(ft, allow_pickle=True)
        TT, TE, EE, EB, TB = z['TT'], z['TE'], z['EE'], z['EB'].item(), z['TB'].item()
    else:
        print(f"  T+E transfers at {len(lt)} multipoles for {len(hist)} histories (long) ...")
        TT, TE, EE, EB, TB = Hh.te_transfers(src, lt, hist)
        if ft:
            np.savez(ft, TT=TT, TE=TE, EE=EE, EB=np.array(EB, dtype=object), TB=np.array(TB, dtype=object))
    LS.extend_spectra(src)
    tot = src.cl_len
    Lmax = Hh.LMAX
    L = np.arange(Lmax + 1)
    spl = lambda y: CubicSpline(lt, y)(L)
    cl = (spl(TT), spl(TE), spl(EE), tot[:Lmax + 1, 2])
    gate("constant rotation gives zero TB/EB inconsistency (S4-like)",
         Hh.tbeb_dchi2(spl(EB["const"]), spl(TB["const"]), cl, Hh.S4_COMB) < 0.01, "< 0.01 sigma")
    # linearity of the estimator in amplitude: exact registered-A0 probe vs per-unit x A0
    s_exact = Hh.tbeb_dchi2(spl(EB["probe_reg"]), spl(TB["probe_reg"]), cl, Hh.S4_COMB)
    s_scaled = sol[REG][dprobe] * Hh.tbeb_dchi2(spl(EB[dprobe]), spl(TB[dprobe]), cl, Hh.S4_COMB)
    gate("estimator homogeneity: exact probe = A0 x per-unit (S4-like)",
         abs(s_exact / s_scaled - 1) < 1e-3, f"{s_exact:.4f} vs {s_scaled:.4f}")
    unit_sig = {lab: {d: Hh.tbeb_dchi2(spl(EB[d]), spl(TB[d]), cl, inst) for d in union}
                for lab, inst in (("SO", Hh.SO_COMB), ("S4", Hh.S4_COMB))}
    out = {}
    for k in INPUTS:
        out[k] = {}
        for lab in ("SO", "S4"):
            v = np.array([sol[k][d] * unit_sig[lab][d] for d in sol[k]])
            out[k][lab] = (float(v.min()), float(np.median(v)), float(v.max()))
    ref = {"SO": (1.14, 1.74, 4.27), "S4": (4.18, 6.48, 16.53)}      # Stage 10h report (2 d.p.)
    dev = max(abs(out[REG][lab][i] - ref[lab][i]) for lab in ref for i in range(3))
    gate("registered row: reproduces Stage 10h EB+TB min/median/max (to 0.01)", dev < 0.011, f"max dev {dev:.3f}")
    print(f"\n  {'input':34s} {'SO-like min/median/max':>26s} {'S4-like min/median/max':>26s}")
    for k, o in out.items():
        f = lambda s: f"{s[0]:5.2f} / {s[1]:5.2f} / {s[2]:5.2f}"
        print(f"  {k:34s} {f(o['SO']):>26s} {f(o['S4']):>26s}")
    return out


# ------------------------------------------------------------------------------
# f windows
# ------------------------------------------------------------------------------
def window(cg, cs, Ws, light):
    """Stage 10d window logic: [f_lo, f_up] or None"""
    H_I = np.pi * D.M_RED * np.sqrt(D.R_GENESIS * D.AS / 2)
    f_up = min(min(D.M_RED * np.sqrt(D.OMEGA_EDE_MATTER / (3 / 8)) / W,
                   D.M_RED * np.sqrt(D.OMEGA_EDE_RAD / (2 / 3)) / W) for W in Ws)
    f_ngc = cg * D.ALPHA / (np.pi * D.G_NGC1275)
    f_act = cg * D.ALPHA * H_I / (np.pi * 4 * np.pi * np.sqrt(D.ACB_ACT))
    lo = max(f_ngc, f_act) if light else f_ngc
    return (lo, f_up) if (lo < f_up and not cs) else None


def windows(m3):
    header("f windows per beta input (Stage 10d / 10g formulas)")
    # gate: the registered Stage 10d hypotheses reproduce 10d's own printed windows
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        D.main()
    txt = buf.getvalue()
    ok = True
    for name, h in D.HYP.items():
        for light in h['light_inflation']:
            w = window(h['cg'], h['cs'], h['W'], light)
            tag = "light during inflation" if light else "heavy during inflation"
            line = [s for s in txt.splitlines() if f"allowed f ({tag})" in s]
            ok &= any(((f"[{w[0]:.1e}, {w[1]:.1e}] GeV" in s) if w else ("NONE" in s)) for s in line)
    gate("window() reproduces Stage 10d's printed windows", ok, "all hypotheses")
    c0r = R.c0_window(3.0, 0.277)
    gate("C0 at the registered input reproduces Stage 10g",
         abs(c0r['f_max_bbn'] / 5.15e10 - 1) < 0.01 and abs(c0r['f_min_aniso'] / 2.10e12 - 1) < 0.01,
         f"{c0r['f_max_bbn']:.2e} / {c0r['f_min_aniso']:.2e}")
    out = {}
    for k, (b0, _) in INPUTS.items():
        need = D.NEED * b0 / 0.277
        c0 = R.c0_window(3.0, b0)
        lo = max(c0['f_min_aniso'], c0['f_min_gag'])
        sb = window(need / (OMEGA * D.LN_T0_TSTAR), 0, [OMEGA], True)
        A0 = m3[k]['A0']
        ml = window(3, 0, [A0[0] * OMEGA, A0[1] * OMEGA], True)
        mh = window(3, 0, [A0[0] * OMEGA, A0[1] * OMEGA], False)
        out[k] = dict(c0=(lo, c0['f_max_bbn'], c0['f_max_bbn'] > lo), sturb=sb, m3a_light=ml, m3a_heavy=mh)
    fmtw = lambda w: f"[{w[0]:.1e}, {w[1]:.1e}]" if w else "none"
    print(f"\n  {'input':34s} {'C0 (lo / up)':>26s} {'STUR-B c_g~0.02':>22s} {'M3a light':>22s} {'M3a heavy':>22s}")
    for k, o in out.items():
        c0 = o['c0']
        print(f"  {k:34s} {c0[0]:.1e} / {c0[1]:.1e} {'(none)' if not c0[2] else '(open)':>6s}"
              f" {fmtw(o['sturb']):>22s} {fmtw(o['m3a_light']):>22s} {fmtw(o['m3a_heavy']):>22s}")
    return out


def main(cache):
    if cache:
        os.makedirs(cache, exist_ok=True)
    print("\n=== Stage 10k: sensitivity of the predictions to the beta input ===")
    src = G.Sources(r=0.0035)
    sb = sturb(src, cache)
    m3, sol, union, unit = m3a(src, cache)
    tb = tbeb(src, sol, union, unit, cache)
    win = windows(m3)

    header("WHAT IS INVARIANT AND WHAT CHANGES (computed above)")
    keys = list(INPUTS)
    rel = lambda a, b: abs(a / b - 1)
    inv = {
        "STUR-B ratio": max(rel(sb[k]['ratio'], sb[REG]['ratio']) for k in keys),
        "STUR-B LiteBIRD sigma(Delta beta) [deg]": max(rel(sb[k]['lb_sigma_dbeta'], sb[REG]['lb_sigma_dbeta']) for k in keys),
        "STUR-B Delta beta / beta": max(rel(sb[k]['delta_beta'] / INPUTS[k][0], sb[REG]['delta_beta'] / INPUTS[REG][0]) for k in keys),
    }
    for n, v in inv.items():
        print(f"  {n:46s} max relative change across inputs: {v:.1e}")
    print(f"  {'M3a admissible phases':46s} " + ", ".join(f"{m3[k]['n']}" for k in keys))
    print(f"  {'M3a ratio range':46s} " + ", ".join(f"{m3[k]['ratio'][0]:.3f}-{m3[k]['ratio'][1]:.3f}" for k in keys))
    print(f"  {'M3a S4-like EB+TB min sigma':46s} " + ", ".join(f"{tb[k]['S4'][0]:.2f}" for k in keys))
    shapes_ok = (inv["STUR-B ratio"] < 1e-3 and
                 all(m3[k]['n'] == m3[REG]['n'] for k in keys))
    print(f"\n  'a lower beta only rescales amplitudes; shapes are unchanged': "
          f"{'HOLDS' if shapes_ok else 'HOLDS FOR STUR-B ONLY; FAILS FOR M3a (the A0 <= 3 cap admits a different phase set)'}")
    print(f"\n  gates: {sum(gates)}/{len(gates)} passed")
    return dict(sturb=sb, m3a=m3, tbeb=tb, windows=win)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None)
    main(ap.parse_args().cache)
