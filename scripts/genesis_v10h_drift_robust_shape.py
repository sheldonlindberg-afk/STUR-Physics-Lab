#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10h: an M3a shape test that an instrumental angle drift
                          cannot fake
================================================================================
Stage 10e found that a beam-like drift of the effective polarisation angle,
alpha(l) = a l(l+1)/2500^2, of ~0.1 deg between l ~ 300 and 2500 is largely
degenerate with STUR-M3a's l-dependent beta_eff(l), cutting the SO-like median
from 3.0 to 1.3 sigma. This stage asks which strategies break that degeneracy.

Basic fact: with a FREE drift amplitude in every channel, a cosmological shape
common to all channels is reproduced exactly by equal drifts, so adding
instruments or frequencies only helps through (i) drift templates whose SHAPE
differs between channels, (ii) priors on the drift amplitudes, or (iii) an
observable in which a rotation at emission and an instrumental angle act
differently. Strategies (all Fisher / Delta chi^2, truth = M3a, over all 49
admissible phases; null = constant rotation + per-channel nuisances):

  (a) several instruments on the same sky (joint covariance, shared cosmic
      variance), independent alpha_c and drift a_c per instrument;
  (b) frequency channels of one instrument, independent per-channel drifts,
      with a quadratic template and with a beam-shaped template
      a_c [1 - exp(-l(l+1) sigma_c^2)] (sigma_c = FWHM_c / sqrt(8 ln 2));
  (c) a Gaussian prior sigma_a on each drift amplitude (external calibrator),
      scanned to find the width giving 3 sigma (SO-like) and 5 sigma (S4-like);
  (d) TB with EB, fully non-parametric drift: an independent angle alpha(l) at
      EVERY multipole. An instrumental angle rotates TE->TB and EE->EB by the
      same alpha(l); a rotation at emission rotates E-mode SOURCES, so TB is
      weighted by Delta_T Delta_E and EB by Delta_E^2 and a time-varying
      rotation gives beta_TB(l) != beta_EB(l). Any pure angle drift is absorbed
      exactly; only the TB/EB inconsistency remains.

(a)-(c) use the lensed EB of Stage 10e; (d) is unlensed (lensing cost EB 5-12%).
Not modelled: T->P leakage and beam ellipticity that are NOT pure angle
rotations (they can produce TB/EB patterns of their own), temperature
foreground residuals beyond the stated toy level, and partial sky overlap.

Registered files are imported only, never modified.
Usage:  python genesis_v10h_drift_robust_shape.py [--cache FILE.npz]
================================================================================
"""
import argparse
import importlib.util
import os

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.special import gammaln, spherical_jn

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


E = _load("g10e", "genesis_v10e_systematics.py")
G, M, LS = E.G, E.M, E.LS
LMAX = E.LMAX
DEG = np.radians(1.0)
gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:56s} {detail:30s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 80 + "\n  " + s + "\n" + "=" * 80)


# ------------------------------------------------------------------------------
# instruments. (noise_pol uK-arcmin, FWHM arcmin, f_sky, lmin, lmax). The SO LAT
# channel noise follows the 8.2 : 8.9 : 21 ratio of arXiv:2405.01621 (93/145/225
# GHz, 2.2'/1.4'/1.0'), rescaled so the combination equals the 8 uK' SO-like
# level of the lshape and 10e forecasts; S4-like channels are the same scaled to
# 2 uK' combined. Approximate by construction.
# ------------------------------------------------------------------------------
def _scaled(ratios, target):
    comb = 1 / np.sqrt(sum(1 / r ** 2 for r in ratios))
    return [r * target / comb for r in ratios]


SO_N = _scaled([8.2, 8.9, 21.0], 8.0)
S4_N = _scaled([8.2, 8.9, 21.0], 2.0)
BEAMS = [2.2, 1.4, 1.0]
SO_CH = [(n, b, 0.4, 300, 3000) for n, b in zip(SO_N, BEAMS)]
S4_CH = [(n, b, 0.4, 300, 3000) for n, b in zip(S4_N, BEAMS)]
ACT = (18.0, 1.4, 0.4, 300, 3000)
SO_COMB = (8.0, 1.4, 0.4, 300, 3000)
S4_COMB = (2.0, 1.4, 0.4, 300, 3000)
SO_SAT = (2.6, 30.0, 0.1, 30, 300)            # illustrative SAT-like (low-l only)


def quad_template(flat, L):
    return flat * L * (L + 1) / 2500.0 ** 2


def beam_template(flat, L, fwhm):
    s2 = (np.radians(fwhm / 60.0)) ** 2 / (8 * np.log(2))
    shape = 1 - np.exp(-L * (L + 1) * s2)
    return flat * shape / (1 - np.exp(-2500 * 2501 * s2))


# ------------------------------------------------------------------------------
# multi-channel EB Fisher, same sky: per-channel alpha_c (free) and drift a_c
# (free or Gaussian prior sigma_a, in deg of angle at l = 2500)
# ------------------------------------------------------------------------------
class MultiChannel:
    """Same-sky EB Fisher for a channel set: per-channel alpha_c (free) and drift a_c
    (free or Gaussian prior sigma_a, in deg of angle at l = 2500), optional common
    null-model template. Template projections are precomputed once, so every
    phase is evaluated with a few matrix products (data enter linearly)."""

    def __init__(self, chans, flat, tot, template="quad", null_extra=None):
        nc = len(chans)
        self.nc = nc
        npar = 2 * nc + (1 if null_extra is not None else 0)
        lo = min(ch[3] for ch in chans)
        hi = min(max(ch[4] for ch in chans), LMAX)
        self.ls = np.arange(lo, hi + 1)
        F = np.zeros((npar, npar))
        V = np.zeros((npar, len(self.ls)))
        W = np.zeros(len(self.ls))
        for j, l in enumerate(self.ls):
            act = [i for i, ch in enumerate(chans) if ch[3] <= l <= ch[4]]
            if not act:
                continue
            fsky = min(chans[i][2] for i in act)
            nu = (2 * l + 1) * fsky
            nl = np.array([G.litebird_noise(np.array([l]), chans[i][0], chans[i][1])[0] for i in act])
            n = len(act)
            ee = tot[l, 1] * np.ones((n, n)) + np.diag(nl)      # shared cosmic variance, independent noise
            bb = tot[l, 2] * np.ones((n, n)) + np.diag(nl)
            ci = np.linalg.inv(ee * bb / nu)
            T = np.zeros((n, npar))
            for r, i in enumerate(act):
                T[r, 2 * i] = flat[l]
                T[r, 2 * i + 1] = (quad_template(flat[l], l) if template == "quad"
                                   else beam_template(flat[l], l, chans[i][1]))
                if null_extra is not None:
                    T[r, -1] = null_extra[l]
            one = np.ones(n)
            F += T.T @ ci @ T
            V[:, j] = T.T @ ci @ one
            W[j] = one @ ci @ one
        self.F, self.V, self.W = F, V, W

    def sigma(self, datas, sigma_a=None):
        F = self.F.copy()
        if sigma_a is not None:
            for i in range(self.nc):
                F[2 * i + 1, 2 * i + 1] += 1.0 / sigma_a ** 2
        D = np.array([d[self.ls] for d in datas])           # (nphase, nl)
        bvec = D @ self.V.T                                  # (nphase, npar)
        c = (D ** 2) @ self.W
        sol = np.linalg.lstsq(F, bvec.T, rcond=None)[0]      # (npar, nphase)
        chi2 = c - np.einsum('ij,ji->i', bvec, sol)
        return np.sqrt(np.maximum(chi2, 0.0))


# ------------------------------------------------------------------------------
# (d) T and E sources, EB and TB for every history
# ------------------------------------------------------------------------------
def solve_A0(src, ds):
    """registered pass-1 rule (genesis_v10c_m3a.py), restricted to the given phases"""
    t0 = src.t0
    ells_hi = np.unique(np.round(np.geomspace(45, 1500, 40)).astype(int))
    nl_h = G.litebird_noise(ells_hi, 2.2, 30.0)
    H1 = {float(d): (lambda z, t, th=M.theta_fn(1.0, d, t0): np.degrees(M.K * (th(t0) - th(t)))) for d in ds}
    ce1, cb1 = src.transfers(ells_hi, H1)
    hh = ells_hi >= 50
    wl1 = (2 * ells_hi + 1) * ce1 ** 2 / ((ce1 + nl_h) * (src.cl_len[ells_hi, 2] + nl_h))
    out = {}
    for d in H1:
        b1 = G.beta_eff(ce1, cb1[d])
        out[d] = M.BETA_NOW / (np.sum(wl1[hh] * b1[hh]) / np.sum(wl1[hh]))
    return out


def te_transfers(src, ells, hist, kmax=0.40):
    """unlensed C_TT, C_TE, C_EE and, per history, C_EB, C_TB at multipoles `ells` (raw uK^2)"""
    k = np.arange(2e-4, kmax, 2e-4)
    eta = np.linspace(150, 800, 1301)
    ST = src.res.get_time_evolution(k, eta, ['T_source'])[:, :, 0]
    SE = src.res.get_time_evolution(k, eta, ['E_source'])[:, :, 0]
    z = src.res.redshift_at_conformal_time(eta)
    tt_ = np.array([src.res.physical_time(zz) for zz in z[::25]])
    t = np.exp(np.interp(z, z[::25][::-1], np.log(tt_)[::-1]))
    w = np.gradient(eta)
    P = G.COSMO['As'] * (k / 0.05) ** (G.COSMO['ns'] - 1)
    base = 4 * np.pi * P * np.gradient(np.log(k)) * G.TCMB_UK ** 2
    s2 = {n: np.sin(2 * np.radians(f(z, t))) for n, f in hist.items()}
    c2 = {n: np.cos(2 * np.radians(f(z, t))) for n, f in hist.items()}
    TT, TE, EE = [], [], []
    EB = {n: [] for n in hist}
    TB = {n: [] for n in hist}
    for l in ells:
        J = spherical_jn(l, np.outer(k, src.eta0 - eta))
        Nl = np.exp(0.5 * (gammaln(l + 3) - gammaln(l - 1)))
        SEJ = SE * J * w
        dT = (ST * J * w).sum(1)
        dE0 = SEJ.sum(1) * Nl
        TT.append(np.sum(base * dT * dT))
        TE.append(np.sum(base * dT * dE0))
        EE.append(np.sum(base * dE0 * dE0))
        for n in hist:
            dE = (SEJ * c2[n]).sum(1) * Nl
            dB = (SEJ * s2[n]).sum(1) * Nl
            EB[n].append(np.sum(base * dE * dB))
            TB[n].append(np.sum(base * dT * dB))
    return (np.array(TT), np.array(TE), np.array(EE),
            {n: np.array(v) for n, v in EB.items()}, {n: np.array(v) for n, v in TB.items()})


def tbeb_dchi2(eb, tb, cl, inst, null_eb=None, null_tb=None, fg_tt=0.0):
    """Free instrumental angle alpha(l) at EVERY l, acting on [EB, TB] as
    2 alpha [EE, TE] (small angle; the unlensed signal rotates E only, B_scalar = 0).
    Returns sqrt(chi^2) of what no l-by-l common angle can absorb.
    cl = (TT, TE, EE, BB_var): unlensed TT/TE/EE for templates and variance, lensed+tensor
    BB for the variance; fg_tt: toy TT foreground residual, D_l at l = 3000 [uK^2]."""
    nz, fw, fsky, lmin, lmax = inst
    l = np.arange(lmin, min(lmax, LMAX) + 1)
    nP = G.litebird_noise(l, nz, fw)
    nT = nP / 2 + fg_tt * 2 * np.pi / (l * (l + 1)) * (l / 3000.0) ** 2
    TT, TE, EE, BB = cl[0][l] + nT, cl[1][l], cl[2][l] + nP, cl[3][l] + nP
    nu = (2 * l + 1) * fsky
    # 2x2 covariance [[EE BB, TE BB], [TE BB, TT BB]] / nu and its inverse
    c11, c12, c22 = EE * BB / nu, TE * BB / nu, TT * BB / nu
    det = c11 * c22 - c12 ** 2
    i11, i12, i22 = c22 / det, -c12 / det, c11 / det
    y1, y2 = eb[l].copy(), tb[l].copy()
    if null_eb is not None:
        y1 -= null_eb[l]
        y2 -= null_tb[l]
    x1, x2 = 2 * DEG * cl[2][l], 2 * DEG * cl[1][l]
    yy = y1 * (i11 * y1 + i12 * y2) + y2 * (i12 * y1 + i22 * y2)
    xy = x1 * (i11 * y1 + i12 * y2) + x2 * (i12 * y1 + i22 * y2)
    xx = x1 * (i11 * x1 + i12 * x2) + x2 * (i12 * x1 + i22 * x2)
    return float(np.sqrt(max(np.sum(yy - xy ** 2 / xx), 0.0)))


# ------------------------------------------------------------------------------
def main(cache):
    print("\n=== Stage 10h: drift-robust test of STUR-M3a's l-dependent beta_eff ===")
    if cache and os.path.exists(cache):
        zc = np.load(cache)
        ells, ds, curves, sturb = zc['ells'], zc['ds'], zc['curves'], zc['sturb']
        print(f"  beta_eff curves loaded from cache ({len(ds)} phases + STUR-B)")
    else:
        print("  computing beta_eff curves (10e pipeline, ~10 min) ...")
        ells, ds, curves, sturb = E.compute_curves()
        if cache:
            np.savez(cache, ells=ells, ds=ds, curves=curves, sturb=sturb)
    gate("49 admissible M3a phases", len(ds) == 49, f"{len(ds)}")

    unl, lens, pp, tot = E.spectra()
    Lm = E.make_Lminus(pp)
    LEE = Lm(unl[:, 1])
    flat = 0.5 * np.sin(4 * DEG) * E.d2c(LEE)

    def eb_lensed(bc):
        return E.d2c(Lm(0.5 * np.sin(4 * np.radians(E.beta_on_grid(ells, bc))) * unl[:, 1]))
    data = [eb_lensed(c) for c in curves]
    d_sb = eb_lensed(sturb)

    def stats(vals):
        a = np.array(vals)
        return a.min(), np.median(a), a.max()

    _mc = {}

    def run(chans, template="quad", sigma_a=None, null_extra=None, datas=None):
        key = (tuple(chans), template, null_extra is not None)
        if key not in _mc:
            _mc[key] = MultiChannel(chans, flat, tot, template, null_extra)
        return stats(_mc[key].sigma(data if datas is None else datas, sigma_a))

    # ---- gate: single-instrument limit reproduces Stage 10e (lensed, + beam drift)
    ref10e = {"SO": (2.38, 3.03, 6.03, 0.86, 1.30, 3.27), "S4": (7.11, 10.49, 24.65, 3.58, 5.06, 12.15)}
    rows = {}
    for lab, inst in (("SO", SO_COMB), ("S4", S4_COMB)):
        nod = stats([E.shape_sigma(d, flat, (tot[np.arange(inst[3], inst[4] + 1), 1]
                                             + G.litebird_noise(np.arange(inst[3], inst[4] + 1), inst[0], inst[1]))
                                    * (tot[np.arange(inst[3], inst[4] + 1), 2]
                                       + G.litebird_noise(np.arange(inst[3], inst[4] + 1), inst[0], inst[1]))
                                    / ((2 * np.arange(inst[3], inst[4] + 1) + 1) * inst[2]),
                                    np.arange(inst[3], inst[4] + 1))[0] for d in data])
        drift = run([inst], template="quad")
        rows[lab] = (nod, drift)
        dev = max(abs(np.median(drift[1]) / ref10e[lab][4] - 1), abs(nod[1] / ref10e[lab][1] - 1))
        gate(f"single {lab}-like: reproduces Stage 10e medians (no drift / drift)", dev < 0.05,
             f"{nod[1]:.2f}/{drift[1]:.2f} vs {ref10e[lab][1]}/{ref10e[lab][4]}")

    fmt = lambda s: f"{s[0]:5.2f} / {s[1]:5.2f} / {s[2]:5.2f}"
    res = {}
    header("(a)/(b) independent per-channel drifts, no prior")
    cases = {
        "SO LAT, combined (10e baseline)": ([SO_COMB], "quad"),
        "SO LAT 3 bands, quadratic drift": (SO_CH, "quad"),
        "SO LAT 3 bands, beam-shaped drift": (SO_CH, "beam"),
        "SO LAT + ACT DR6, quadratic": ([SO_COMB, ACT], "quad"),
        "SO LAT + SO SAT, quadratic": ([SO_COMB, SO_SAT], "quad"),
        "S4, combined": ([S4_COMB], "quad"),
        "S4 3 bands, beam-shaped drift": (S4_CH, "beam"),
        "SO LAT + S4, quadratic": ([SO_COMB, S4_COMB], "quad"),
    }
    print(f"  {'strategy':40s} {'min / median / max  (sigma)':>30s}")
    for name, (ch, tpl) in cases.items():
        res[name] = run(ch, template=tpl)
        print(f"  {name:40s} {fmt(res[name]):>30s}")
    # nested null models: free per-band drifts contain the equal-drift (combined) case, so
    # splitting into bands with the same template shape cannot raise the significance
    gate("3 bands, free same-shape drifts <= combined (no free lunch)",
         res["SO LAT 3 bands, quadratic drift"][1] <= res["SO LAT, combined (10e baseline)"][1] * 1.05,
         f"{res['SO LAT 3 bands, quadratic drift'][1]:.2f} <= {res['SO LAT, combined (10e baseline)'][1]:.2f}")

    header("(c) prior sigma_a on each drift amplitude (deg at l = 2500)")
    grid = np.geomspace(0.002, 1.0, 40)
    prior = {}
    for lab, inst, target in (("SO", SO_COMB, 3.0), ("S4", S4_COMB, 5.0)):
        meds, mins = [], []
        for sa in grid:
            s = run([inst], template="quad", sigma_a=sa)
            mins.append(s[0])
            meds.append(s[1])
        meds, mins = np.array(meds), np.array(mins)
        def width(arr):
            """largest scanned sigma_a reaching the target; inf if reached with no prior, nan if never"""
            ok = np.where(arr >= target)[0]
            if not len(ok):
                return float('nan')
            return float('inf') if ok.max() == len(grid) - 1 else float(grid[ok.max()])
        prior[lab] = dict(median=width(meds), worst=width(mins), target=target,
                          at_020=run([inst], template="quad", sigma_a=0.20),
                          at_008=run([inst], template="quad", sigma_a=0.08),
                          at_002=run([inst], template="quad", sigma_a=0.02))
        def say(w):
            if np.isinf(w):
                return "any prior (reached with the drift free)"
            if np.isnan(w):
                return "never (not even with the drift fixed at 0)"
            return f"sigma_a <= {w:.3f} deg"
        print(f"  {lab}-like, {target:.0f} sigma: median phase {say(prior[lab]['median'])};"
              f" every phase {say(prior[lab]['worst'])}")
        for k_, sa in (("at_020", 0.20), ("at_008", 0.08), ("at_002", 0.02)):
            print(f"      sigma_a = {sa:.2f} deg: {fmt(prior[lab][k_])}")
    gate("prior -> 0 recovers the no-drift significance (SO)",
         abs(run([SO_COMB], template="quad", sigma_a=1e-6)[1] / rows["SO"][0][1] - 1) < 0.02,
         f"{run([SO_COMB], template='quad', sigma_a=1e-6)[1]:.2f} vs {rows['SO'][0][1]:.2f}")

    header("(d) EB + TB with a free instrumental angle at every multipole (unlensed)")
    src = G.Sources(r=0.0035)
    A0 = solve_A0(src, ds)
    t0 = src.t0
    hist = {float(d): (lambda z, t, th=M.theta_fn(A0[float(d)], d, t0): np.degrees(M.K * (th(t0) - th(t)))) for d in ds}
    # G.histories returns STUR-B at kappa = 1 deg per unit ln t (beta ~ 10 deg at recombination);
    # earlier stages rescaled the resulting EB, valid only at small angle. Here the angle enters
    # non-linearly (sin 2b, sin 4b), so build it at the registered Stage 10b kappa.
    KAPPA_10B = 0.026742209957093272
    _sb = G.histories(src)["STUR-B (ln t)"]
    hist["STUR-B"] = lambda z, t, f=_sb: KAPPA_10B * f(z, t)
    hist["const"] = lambda z, t: 0.277 + 0 * z
    lgrid = np.unique(np.concatenate([np.arange(275, 3001, 25), [3000]]))
    chk = [int(l) for l in ells if 300 <= l <= 3000][::12]
    lt = np.unique(np.concatenate([lgrid, chk]))
    tbc = cache.replace('.npz', '_tb.npz') if cache else None
    if tbc and os.path.exists(tbc):
        zt = np.load(tbc, allow_pickle=True)
        TT, TE, EE = zt['TT'], zt['TE'], zt['EE']
        EB, TB = zt['EB'].item(), zt['TB'].item()
        print(f"  T+E transfers loaded from cache ({len(lt)} multipoles)")
    else:
        print(f"  T+E transfers at {len(lt)} multipoles for {len(hist)} histories (~45 min) ...")
        TT, TE, EE, EB, TB = te_transfers(src, lt, hist)
        if tbc:
            np.savez(tbc, TT=TT, TE=TE, EE=EE, EB=np.array(EB, dtype=object), TB=np.array(TB, dtype=object))
    LS.extend_spectra(src)
    dev_tt = np.max(np.abs(TT / src.cl_unl[lt, 0] - 1))
    dev_te = np.max(np.abs(TE - src.cl_unl[lt, 3]) / np.sqrt(src.cl_unl[lt, 0] * src.cl_unl[lt, 1]))
    gate("C_TT vs CAMB unlensed (l = 275-3000)", dev_tt < 0.03, f"max dev {dev_tt:.1e}")
    gate("C_TE vs CAMB (relative to sqrt(TT EE))", dev_te < 0.01, f"max dev {dev_te:.1e}")
    b0 = np.radians(0.277)
    dev_c = max(np.max(np.abs(EB["const"] / EE / (0.5 * np.sin(4 * b0)) - 1)),
                np.max(np.abs(TB["const"] / TE / np.sin(2 * b0) - 1)))
    gate("constant rotation: EB = sin4b/2 EE and TB = sin2b TE", dev_c < 1e-8, f"max rel dev {dev_c:.1e}")
    # EB angle reproduces the cached curves at the check multipoles
    dev_eb = 0.0
    for i, d in enumerate(ds):
        b = G.beta_eff(EE, EB[float(d)])
        for l in chk:
            j = list(lt).index(l)
            dev_eb = max(dev_eb, abs(b[j] - curves[i][list(ells).index(l)]))
    gate("EB angle reproduces the cached beta_eff curves (A0 re-solved)", dev_eb < 5e-4, f"max dev {dev_eb:.1e} deg")

    L = np.arange(LMAX + 1)

    def spl(y):
        return CubicSpline(lt, y)(L)
    cl = (spl(TT), spl(TE), spl(EE), tot[:LMAX + 1, 2])
    # use the measured/lensed BB (incl. r) for the variance, unlensed T/E for signal
    sig = {}
    for lab, inst in (("SO", SO_COMB), ("S4", S4_COMB), ("ACT", ACT)):
        for fg in (0.0, 10.0):
            vals = [tbeb_dchi2(spl(EB[float(d)]), spl(TB[float(d)]), cl, inst, fg_tt=fg) for d in ds]
            sig[(lab, fg)] = stats(vals)
        sig[(lab, "sturb")] = tbeb_dchi2(spl(EB["STUR-B"]), spl(TB["STUR-B"]), cl, inst)
        sig[(lab, "vsB")] = stats([tbeb_dchi2(spl(EB[float(d)]), spl(TB[float(d)]), cl, inst,
                                              null_eb=spl(EB["STUR-B"]), null_tb=spl(TB["STUR-B"])) for d in ds])
    gate("constant rotation gives zero TB/EB inconsistency",
         tbeb_dchi2(spl(EB["const"]), spl(TB["const"]), cl, S4_COMB) < 0.01, "S4-like, < 0.01 sigma")
    print(f"  {'experiment':10s} {'M3a (no T fg)':>24s} {'M3a (T fg 10 uK^2)':>24s}"
          f" {'STUR-B control':>15s} {'M3a vs STUR-B':>24s}")
    for lab in ("ACT", "SO", "S4"):
        print(f"  {lab:10s} {fmt(sig[(lab, 0.0)]):>24s} {fmt(sig[(lab, 10.0)]):>24s}"
              f" {sig[(lab, 'sturb')]:14.2f}σ {fmt(sig[(lab, 'vsB')]):>24s}")

    header("STUR-B vs M3a under the drift treatment (EB, lensed)")
    for lab, inst in (("SO", SO_COMB), ("S4", S4_COMB)):
        s = run([inst], template="quad", null_extra=d_sb)
        ctrl = run([inst], template="quad", datas=[d_sb])[1]
        print(f"  {lab}-like: M3a vs (STUR-B + alpha + drift) {fmt(s)};  STUR-B vs (flat + drift) {ctrl:.2f} sigma")

    print(f"\n  gates: {sum(gates)}/{len(gates)} passed")
    return dict(rows=rows, res=res, prior=prior, sig=sig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None)
    main(ap.parse_args().cache)
