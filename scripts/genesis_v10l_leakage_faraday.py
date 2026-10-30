#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10l: T->P leakage / beam ellipticity in the EB+TB test, and
primordial-magnetic-field Faraday rotation (Monte Carlo)
================================================================================
Replaces two argued claims with calculations.

PART 1 (claim 8). Stage 10h's joint EB+TB test absorbs any l-dependent instrumental
angle alpha(l). It was then *said* to remain vulnerable to T->P leakage and beam
ellipticity. Here they are modelled and marginalised.

  Leakage model (harmonic "leakage beam", as used by ACT DR6, arXiv:2503.14452):
      E_obs = E + gE_l T,   B_obs = B + gB_l T
  To first order in (alpha, gE, gB):
      EB_obs = EB + 2 alpha EE + gB TE + gE TB
      TB_obs = TB + 2 alpha TE + gB TT
      TE_obs = TE + gE TT,  EE_obs = EE + 2 gE TE,  BB_obs = BB + 2 gB TB + gB^2 TT
  gB therefore adds the template [TE, TT] to [EB, TB] -- a different direction from
  alpha's [EE, TE]. gE enters [EB, TB] only through gE * TB_signal (second order).
  The l-shape of gB is modelled four ways:
    (i)   free at every l (like alpha),
    (ii)  free in bins of width dl,
    (iii) HHZ-type parametric forms: monopole (const), dipole (l/2500) and
          quadrupole / differential ellipticity (l(l+1)/2500^2), one amplitude each
          (Hu, Hedman & Zaldarriaga 2003 scalings: leakage of order (l sigma_b)^n),
    (iv)  binned with a Gaussian calibration prior sigma_g per bin.
  For each: M3a-vs-flat significance (min / median / max over the 49 admissible
  phases) for SO-like and S4-like, and the leakage amplitude that fakes M3a.
  Null information on the leakage from TE/EE (gE) and BB (gB, second order).
  Gate: with leakage switched off, Stage 10h (d) is reproduced exactly.

PART 2 (claim 12). Faraday rotation by a stochastic primordial magnetic field:
  alpha(n) = C lambda0^2 int d chi w(chi) B0(chi n) . n,
  C from RM = 0.812 rad m^-2 / (cm^-3 uG pc) with comoving B0 (B ~ a^-2), physical
  wavelength lambda0 a, n_e ~ x_e a^-3, dl = a d chi: d alpha = C' lambda0^2 B0 d tau.
  w(chi) = tau_dot(chi) x (fraction of the polarisation already emitted), from CAMB.
  The field is a sum of transverse Fourier modes (k . e = 0) drawn from
  P_B ~ k^n_B (n_B = -2.9 nearly scale-invariant; n_B = +2 blue, with cutoff scan),
  normalised to B_lambda (1 Mpc Gaussian smoothing) = 4.4 nG (Planck 2015 XIX,
  power-spectrum bound). The monopole is computed per mode with the exact angular
  integral, the anisotropic rms by direct evaluation on a sphere of directions, and
  an n_e-modulation (B . grad n_e) term is included as the only route to a monopole.

Usage:  python genesis_v10l_leakage_faraday.py [--cache-dir DIR]
================================================================================
"""
import argparse
import importlib.util
import os

import camb
import numpy as np
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = "/tmp/claude-0/-home-user-STUR-Physics-Lab/d24fad38-4807-5bed-b0ba-60837fc14853/scratchpad/forkI"


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load("g10h", "genesis_v10h_drift_robust_shape.py")
E, G = H.E, H.G
LMAX = H.LMAX
DEG = np.radians(1.0)
gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:58s} {detail:30s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 80 + "\n  " + s + "\n" + "=" * 80)


def stats(a):
    a = np.asarray(a)
    return a.min(), np.median(a), a.max()


def fmt(s):
    return f"{s[0]:5.2f} / {s[1]:5.2f} / {s[2]:5.2f}"


# ------------------------------------------------------------------------------
# PART 1 -- generalised per-l GLS: local (per-l) params profiled out analytically,
# global params (bins / parametric amplitudes) by accumulated normal equations
# ------------------------------------------------------------------------------
class JointFit:
    def __init__(self, cl, inst):
        nz, fw, fsky, lmin, lmax = inst
        l = np.arange(lmin, min(lmax, LMAX) + 1)
        nP = G.litebird_noise(l, nz, fw)
        nT = nP / 2
        TT, TE, EE, BB = cl[0][l] + nT, cl[1][l], cl[2][l] + nP, cl[3][l] + nP
        nu = (2 * l + 1) * fsky
        C = np.empty((len(l), 2, 2))
        C[:, 0, 0], C[:, 0, 1], C[:, 1, 1] = EE * BB / nu, TE * BB / nu, TT * BB / nu
        C[:, 1, 0] = C[:, 0, 1]
        self.l, self.Ci = l, np.linalg.inv(C)
        self.xa = np.stack([2 * DEG * cl[2][l], 2 * DEG * cl[1][l]], -1)     # alpha template
        self.xg = np.stack([cl[1][l], cl[0][l]], -1)                       # gB template [TE, TT]
        self.cl, self.inst = cl, inst
        self.nu, self.N = nu, (nP, nT)

    def projector(self, local):
        """P = Ci - Ci X (X^T Ci X)^-1 X^T Ci for the per-l local templates"""
        cols = [self.xa] + ([self.xg] if local == "alpha+gB" else [])
        X = np.stack(cols, -1)                                             # (nl, 2, k)
        CiX = self.Ci @ X
        M = np.swapaxes(X, 1, 2) @ CiX
        if X.shape[-1] == 2:                                               # full rank in 2D -> P = 0 up to rounding
            Minv = np.linalg.pinv(M)
        else:
            Minv = 1.0 / M
        return self.Ci - CiX @ Minv @ np.swapaxes(CiX, 1, 2)

    def sig(self, ys, local="alpha", Z=None, prior=None):
        """ys: (nphase, nl, 2) data; Z: (nl, 2, nG) global templates; prior: (nG,) sigmas"""
        P = self.projector(local)
        Py = np.einsum('lij,plj->pli', P, ys)
        chi = np.einsum('pli,pli->p', ys, Py)
        if Z is not None and Z.shape[-1]:
            A = np.einsum('lia,lij,ljb->ab', Z, P, Z)
            if prior is not None:
                A = A + np.diag(1.0 / np.asarray(prior) ** 2)
            b = np.einsum('lia,pli->pa', Z, Py)
            sol = np.linalg.lstsq(A, b.T, rcond=None)[0]
            chi = chi - np.einsum('pa,ap->p', b, sol)
            self.last_amp = sol                                            # (nG, nphase)
        return np.sqrt(np.maximum(chi, 0.0))

    def Z_param(self, which):
        l = self.l
        shapes = {"monopole": np.ones_like(l, float), "dipole": l / 2500.0,
                  "quadrupole/ellipticity": l * (l + 1) / 2500.0 ** 2}
        cols = [shapes[w][:, None] * self.xg for w in which]
        return np.stack(cols, -1)

    def Z_bins(self, dl):
        l = self.l
        edges = np.arange(l[0], l[-1] + dl, dl)
        cols = []
        for a, b in zip(edges[:-1], edges[1:]):
            m = ((l >= a) & (l < b)).astype(float)
            if m.sum():
                cols.append(m[:, None] * self.xg)
        return np.stack(cols, -1)

    def fake_gamma(self, y):
        """exact per-l (alpha, gB) that reproduce y (nl, 2): returns gB(l)"""
        X = np.stack([self.xa, self.xg], -1)
        return np.linalg.solve(X, y[..., None])[..., 1, 0]


def part1(cache_dir):
    header("PART 1  T->P leakage and beam ellipticity in the joint EB+TB test")
    zc = np.load(os.path.join(cache_dir, "curves.npz"))
    ells, ds = zc['ells'], zc['ds']
    zt = np.load(os.path.join(cache_dir, "curves_tb.npz"), allow_pickle=True)
    TT, TE, EE = zt['TT'], zt['TE'], zt['EE']
    EB, TB = zt['EB'].item(), zt['TB'].item()
    lgrid = np.unique(np.concatenate([np.arange(275, 3001, 25), [3000]]))
    chk = [int(l) for l in ells if 300 <= l <= 3000][::12]
    lt = np.unique(np.concatenate([lgrid, chk]))
    gate("Stage 10h cache: 49 phases, 114 multipoles, STUR-B at registered kappa",
         len(ds) == 49 and len(lt) == len(TT) == 114 and
         abs(0.25 * np.degrees(np.arcsin(2 * EB["STUR-B"][0] / EE[0])) - 0.276) < 0.005,
         f"{len(ds)} / {len(TT)}")
    unl, lens, pp, tot = E.spectra()
    L = np.arange(LMAX + 1)

    def spl(y):
        return CubicSpline(lt, y)(L)
    cl = (spl(TT), spl(TE), spl(EE), tot[:LMAX + 1, 2])
    data = {float(d): (spl(EB[float(d)]), spl(TB[float(d)])) for d in ds}
    insts = {"ACT": H.ACT, "SO": H.SO_COMB, "S4": H.S4_COMB}
    fits = {k: JointFit(cl, v) for k, v in insts.items()}

    def ys_for(fit):
        return np.stack([np.stack([data[float(d)][0][fit.l], data[float(d)][1][fit.l]], -1) for d in ds])

    # ---- gate: leakage off reproduces Stage 10h (d)
    ref = {"ACT": (0.45, 0.69, 1.68), "SO": (1.14, 1.74, 4.27), "S4": (4.18, 6.48, 16.53)}
    dev, devref = 0.0, 0.0
    base = {}
    for k, f in fits.items():
        mine = f.sig(ys_for(f))
        theirs = np.array([H.tbeb_dchi2(data[float(d)][0], data[float(d)][1], cl, insts[k]) for d in ds])
        dev = max(dev, np.max(np.abs(mine - theirs)))
        base[k] = stats(mine)
        devref = max(devref, max(abs(a - b) for a, b in zip(base[k], ref[k])))
    gate("leakage off: identical to genesis_v10h tbeb_dchi2 (all phases)", dev < 1e-6, f"max |d sigma| = {dev:.1e}")
    gate("leakage off: Stage 10h (d) table reproduced (2 dp)", devref < 0.006, f"max dev {devref:.3f}")
    const = np.stack([np.stack([spl(EB["const"])[fits['S4'].l], spl(TB["const"])[fits['S4'].l]], -1)])
    raw = np.sqrt(np.einsum('li,lij,lj->', const[0], fits['S4'].Ci, const[0]))
    rc = fits['S4'].sig(const, "alpha+gB")[0] / raw
    gate("constant rotation absorbed with gB free per l (residual / raw chi)", rc < 1e-6, f"{rc:.1e}")

    rows = {}
    print(f"\n  Flat rotation rejected, M3a true (min / median / max over 49 phases), sigma")
    print(f"  {'treatment of gB (T->B leakage)':44s} {'SO-like':>22s} {'S4-like':>22s}")

    def row(lab, fn):
        rows[lab] = {k: stats(fn(fits[k], ys_for(fits[k]))) for k in ("SO", "S4")}
        print(f"  {lab:44s} {fmt(rows[lab]['SO']):>22s} {fmt(rows[lab]['S4']):>22s}")
    row("none (Stage 10h (d))", lambda f, y: f.sig(y))
    row("free at every l", lambda f, y: f.sig(y, "alpha+gB"))
    for dl in (50, 200, 500):
        row(f"free per bin, dl = {dl}", lambda f, y, dl=dl: f.sig(y, Z=f.Z_bins(dl)))
    row("single constant (one global amplitude)", lambda f, y: f.sig(y, Z=f.Z_bins(4000)))
    for w in ("monopole", "dipole", "quadrupole/ellipticity"):
        row(f"HHZ {w}", lambda f, y, w=w: f.sig(y, Z=f.Z_param([w])))
    row("HHZ all three together", lambda f, y: f.sig(y, Z=f.Z_param(["monopole", "dipole", "quadrupole/ellipticity"])))
    for sg in (1e-2, 3e-3, 1e-3, 3e-4):
        row(f"bins dl = 200, prior sigma_g = {100 * sg:.2f}%",
            lambda f, y, sg=sg: f.sig(y, Z=f.Z_bins(200), prior=np.full(f.Z_bins(200).shape[-1], sg)))
    gate("gB free at every l absorbs M3a completely (2 params per 2-vector)",
         rows["free at every l"]["S4"][2] < 1e-3, f"S4 max {rows['free at every l']['S4'][2]:.1e}")

    # ---- prior width needed (bins dl = 200)
    print("\n  calibration prior on gB (bins dl = 200) needed for the test:")
    need = {}
    for k, target in (("SO", 3.0), ("S4", 5.0)):
        f = fits[k]
        y = ys_for(f)
        Zb = f.Z_bins(200)
        for which, idx in (("median phase", 1), ("every phase", 0)):
            lo, hi = 1e-6, 1e-1
            ok = stats(f.sig(y, Z=Zb, prior=np.full(Zb.shape[-1], lo)))[idx] >= target
            if not ok:
                need[(k, which)] = None
                print(f"    {k}-like {target:.0f} sigma, {which}: not reached even with sigma_g -> 0")
                continue
            for _ in range(60):
                mid = np.sqrt(lo * hi)
                if stats(f.sig(y, Z=Zb, prior=np.full(Zb.shape[-1], mid)))[idx] >= target:
                    lo = mid
                else:
                    hi = mid
            need[(k, which)] = lo
            print(f"    {k}-like {target:.0f} sigma, {which}: sigma_g <= {100 * lo:.4f}%")

    # ---- faking amplitudes
    print("\n  leakage that fakes M3a (S4-like range, l = 300-3000):")
    f = fits["S4"]
    y = ys_for(f)
    g = np.array([f.fake_gamma(y[i]) for i in range(len(ds))])            # exact per-l fake
    gr = np.sqrt(np.mean(g ** 2, axis=1))
    gm = np.max(np.abs(g), axis=1)
    print(f"    exact per-l gB(l): rms {100 * np.median(gr):.4f}% (median phase), max |gB| {100 * np.median(gm):.4f}%;"
          f" over phases rms {100 * gr.min():.4f}-{100 * gr.max():.4f}%")
    fakes = {}
    for w in ("monopole", "dipole", "quadrupole/ellipticity"):
        f.sig(y, Z=f.Z_param([w]))
        a = np.abs(f.last_amp[0])
        fakes[w] = stats(a)
        print(f"    best-fit HHZ {w:24s} amplitude at l = 2500: {100 * np.median(a):.4f}% (median phase),"
              f" {100 * a.min():.4f}-{100 * a.max():.4f}% over phases")
    print("    reference: ACT DR6 residual T->P leakage ~0.3% (power-spectrum level, varies by array-band;"
          " arXiv:2503.14452); main-beam leakage <= 1% (150 GHz), 2.5% (98 GHz)")

    # ---- second-order gE term and null information
    fS = fits["S4"]
    tbsig = np.array([data[float(d)][1][fS.l] for d in ds])
    ebres = np.array([fS.sig(ys_for(fS)[i:i + 1])[0] for i in range(len(ds))])
    def sE_of(gE):
        yE = np.stack([gE * tbsig, np.zeros_like(tbsig)], -1)            # gE * TB_signal in EB
        return fS.sig(yE)
    s3, s6 = sE_of(3e-3), sE_of(6e-3)
    gate("gE*TB term is linear in gE (validity of first-order expansion)", np.max(np.abs(s6 / s3 - 2)) < 1e-9, "")
    l = fS.l
    nP, nT = fS.N
    TTo, TEo, EEo, BBo = cl[0][l] + nT, cl[1][l], cl[2][l] + nP, cl[3][l] + nP
    s_gE = 1 / np.sqrt(np.sum(cl[0][l] ** 2 * fS.nu / (TTo * EEo + TEo ** 2)))
    s_gB2 = 1 / np.sqrt(np.sum(cl[0][l] ** 2 * fS.nu / (2 * BBo ** 2)))
    print(f"  null information (S4-like, constant leakage, LCDM fixed):")
    print(f"    TE constrains gE to {100 * s_gE:.4f}% (1 sigma); it carries no first-order gB information")
    print(f"    BB constrains gB only at second order: gB^2 TT detectable for |gB| > {100 * np.sqrt(s_gB2):.3f}% (1 sigma)")
    print("    TB/EB: with gB free per l the 2-vector [EB, TB] is fully absorbed (computed above)")
    sEte = sE_of(3 * s_gE)
    print(f"\n  gE (T->E) enters [EB, TB] as gE * TB_signal (first order in gE, times beta):")
    print(f"    gE = 0.3% (ACT-like residual): spurious non-flat signal {np.median(s3):.2f} sigma (S4 median),"
          f" {100 * np.median(s3 / ebres):.0f}% of M3a's {np.median(ebres):.2f} sigma (max {100 * np.max(s3 / ebres):.0f}%)")
    print(f"    gE = 3 x TE limit ({100 * 3 * s_gE:.4f}%): {np.median(sEte):.3f} sigma ({100 * np.median(sEte / ebres):.1f}% of M3a)")
    return dict(gE_03=stats(s3), gE_03_frac=stats(s3 / ebres), gE_te=stats(sEte),
                rows=rows, need=need, fakes=fakes, fake_rms=stats(gr), s_gE=s_gE, s_gB_BB=np.sqrt(s_gB2))


# ------------------------------------------------------------------------------
# PART 2 -- primordial magnetic field Faraday rotation, Monte Carlo
# ------------------------------------------------------------------------------
RM_CONST = 0.812                      # rad m^-2 per (cm^-3 uG pc)
SIGT_CM2 = 6.6524587e-25
PC_CM = 3.0856776e18
C_FAR = RM_CONST / (SIGT_CM2 * PC_CM)  # rad m^-2 uG^-1 per unit optical depth
C_LIGHT = 2.99792458e8
LB_BANDS = [40, 50, 60, 68, 78, 89, 100, 119, 140, 166, 195, 235, 280, 337, 402]   # GHz (intermediate centres unverified)


def los_weight():
    """rotation weight w = d tau x (fraction of polarisation already emitted), on a fine
    recombination grid (0.1 Mpc) and a coarser reionization grid (2 Mpc)"""
    res = camb.get_results(camb.set_params(**G.COSMO, tau=G.DATA['tau'][0]))
    eta0 = res.tau0
    e_rec = np.arange(100.0, 1500.0, 0.1)
    e_rei = np.arange(1500.0, eta0 - 1.0, 2.0)
    out = []
    for e_ in (e_rec, e_rei):
        ev = res.get_background_time_evolution(e_, ['opacity', 'visibility'])
        out.append((ev['opacity'], ev['visibility'], np.gradient(e_)))
    emitted = np.cumsum(np.concatenate([o[1] * o[2] for o in out]))
    emitted /= emitted[-1]
    n1 = len(e_rec)
    w_rec = out[0][0] * out[0][2] * emitted[:n1]
    w_rei = out[1][0] * out[1][2] * emitted[n1:]
    keep = w_rec > 1e-8 * w_rec.max()
    return (eta0 - e_rec[keep], w_rec[keep]), (eta0 - e_rei, w_rei)


def draw_modes(rng, n, nB, kmin, kmax, Blam_nG, lam=1.0):
    lk = rng.uniform(np.log(kmin), np.log(kmax), n)
    k = np.exp(lk)
    khat = rng.normal(size=(n, 3))
    khat /= np.linalg.norm(khat, axis=1)[:, None]
    e = np.cross(khat, rng.normal(size=(n, 3)))                         # transverse: e . khat = 0
    e /= np.linalg.norm(e, axis=1)[:, None]
    phi = rng.uniform(0, 2 * np.pi, n)
    # weight per log k ~ k^3 P_B ~ k^(nB+3); variance of a mode A^2/2; smoothed var = B_lam^2
    wgt = k ** (nB + 3)
    var_s = np.sum(wgt * np.exp(-(k * lam) ** 2)) / 2
    A = np.sqrt(wgt / var_s) * Blam_nG * 1e-3                            # uG
    return k, khat, e, phi, A


def monopole_exact(k, khat, e, phi, A, chi, w, dvec=None):
    """(1/4pi) oint d Omega n.B(chi n) for B = sum A e cos(k khat.x + phi):
    = - sum A (e.khat) j1(k chi) sin(phi);  with a direction dvec replacing khat
    (for the n_e-modulated term) the same formula holds with q = |dvec|."""
    from scipy.special import spherical_jn
    if dvec is None:
        proj = np.einsum('ij,ij->i', e, khat)
        kk = k
    else:
        kk = np.linalg.norm(dvec, axis=1)
        proj = np.einsum('ij,ij->i', e, dvec / kk[:, None])
    coef = A * proj * np.sin(phi)
    tot = 0.0
    for i in range(0, len(kk), 2000):                                   # chunked: memory
        tot -= np.sum(coef[i:i + 2000, None] * spherical_jn(1, np.outer(kk[i:i + 2000], chi)) * w[None, :])
    return tot


def part2(seed=1):
    header("PART 2  primordial magnetic field Faraday rotation (Monte Carlo)")
    (cr, wr), (ci, wi) = los_weight()
    rng = np.random.default_rng(seed)
    lam30 = C_LIGHT / 30e9
    kfac = C_FAR * lam30 ** 2                                           # rad per (uG x d tau)
    tau_rec, tau_rei = wr.sum(), wi.sum()
    print(f"  C' = {C_FAR:.4e} rad m^-2 uG^-1 per unit tau; at 30 GHz {np.degrees(kfac * 1e-3):.3f} deg"
          " per nG (field along the line of sight) per unit optical depth")
    print(f"  rotation-weighted optical depth: recombination {tau_rec:.4f}, reionization {tau_rei:.4f}")
    # gate: a uniform field B0 z-hat evaluated through the same LOS machinery as the modes
    # (a single mode with k -> 0, e = z-hat, phi = 0) must give alpha = kfac B0 cos(theta) tau_eff
    th = np.linspace(0, np.pi, 7)
    n_u = np.stack([np.sin(th), 0 * th, np.cos(th)], -1)
    k0 = 1e-9 * np.array([[1.0, 0, 0]])
    cc = np.concatenate([cr, ci])
    ww = np.concatenate([wr, wi])
    W0 = np.exp(1j * (k0 @ n_u.T)[..., None] * cc) @ ww                  # (1, ndir)
    num = kfac * 1e-3 * (n_u[:, 2] * np.real(W0[0]))
    ana = kfac * 1e-3 * np.cos(th) * (tau_rec + tau_rei)
    gate("uniform field through the LOS machinery: C' lambda^2 B cos(theta) tau_eff",
         np.max(np.abs(num - ana)) < 1e-9 * np.max(np.abs(ana)),
         f"max rel dev {np.max(np.abs(num - ana)) / np.max(np.abs(ana)):.1e}")
    # reionization window transform: it averages any mode with |k.n| >= KC away
    KC = 0.05
    qq = np.linspace(KC, 1.0, 200)
    ci_f = np.arange(ci.min(), ci.max(), 0.1)
    wi_f = np.interp(ci_f, ci[::-1], wi[::-1]) * (0.1 / 2.0)             # same density on the 0.1 Mpc grid
    Wq = np.abs(np.exp(1j * np.outer(qq, ci_f)) @ wi_f)
    rel_rei = Wq.max() / wi_f.sum()
    gate("reionization window: |W(|k.n| >= 0.05 Mpc^-1)| / W(0) < 1e-2", rel_rei < 1e-2, f"{rel_rei:.1e}")
    dirs = rng.normal(size=(800, 3))
    dirs /= np.linalg.norm(dirs, axis=1)[:, None]
    beams = {"pointwise": 0.0, "30' (LiteBIRD)": 30.0, "1.4' (SO/S4)": 1.4}
    chi_s = np.sum(wr * cr) / tau_rec
    results = {}
    cases = [("nearly scale-invariant, n_B = -2.9", -2.9, 1e-4, 1.0),
             ("blue, n_B = +2, cutoff 1 Mpc^-1", 2.0, 1e-4, 1.0),
             ("blue, n_B = +2, cutoff 10 Mpc^-1", 2.0, 1e-4, 10.0)]
    for lab, nB, kmin, kmax in cases:
        k, khat, e, phi, A = draw_modes(rng, 1200, nB, kmin, kmax, 4.4)
        # gate on the estimator: longitudinal (unphysical) field does give a monopole
        mono = monopole_exact(k, khat, e, phi, A, cc, ww)
        mono_long = monopole_exact(k, khat, khat, phi, A, cc, ww)
        # anisotropic part: exact LOS transform per (mode, direction)
        kv = k[:, None] * khat
        kn = kv @ dirs.T                                                 # k . n   (modes, dirs)
        en = e @ dirs.T
        kperp = np.sqrt(np.maximum((k ** 2)[:, None] - kn ** 2, 0.0))
        Wt = np.zeros(kn.shape, complex)
        for c_, w_ in zip(cr, wr):                                       # recombination: fine grid, all modes
            Wt += w_ * np.exp(1j * kn * c_)
        msk = np.abs(kn) < KC                                            # reionization: resolved modes only
        for c_, w_ in zip(ci, wi):
            Wt[msk] += w_ * np.exp(1j * kn[msk] * c_)
        rms = {}
        for bl, fwhm in beams.items():
            sb = np.radians(fwhm / 60.0) / np.sqrt(8 * np.log(2))
            bf = np.exp(-0.5 * (kperp * chi_s * sb) ** 2)                # Gaussian beam on l ~ k_perp chi
            a = kfac * np.sum(A[:, None] * en * bf * np.real(np.exp(1j * phi)[:, None] * Wt), axis=0)
            rms[bl] = np.sqrt(np.mean(a ** 2))
        # n_e-modulated monopole: (1 + delta) with delta = sum d_j cos(q_j . x + psi_j), rms delta_e
        nd = 40
        q = np.exp(rng.uniform(np.log(1e-3), np.log(1.0), nd))
        qh = rng.normal(size=(nd, 3))
        qh /= np.linalg.norm(qh, axis=1)[:, None]
        psi = rng.uniform(0, 2 * np.pi, nd)
        d_rms = 1e-3
        dj = np.full(nd, d_rms * np.sqrt(2.0 / nd))
        # product of cosines -> waves at k +/- q with amplitude A d / 2
        m_mod = 0.0
        for s in (+1, -1):
            dvec = (k[:, None] * khat)[:, None, :] + s * (q[:, None] * qh)[None, :, :]
            dv = dvec.reshape(-1, 3)
            ee = np.repeat(e, nd, axis=0)
            amp = (A[:, None] * dj[None, :] / 2).reshape(-1)
            ph = (phi[:, None] + s * psi[None, :]).reshape(-1)
            m_mod += monopole_exact(None, None, ee, ph, amp, cr, wr, dvec=dv)
        results[lab] = dict(mono=kfac * mono, mono_long=kfac * mono_long, rms=rms, mono_mod=kfac * m_mod)
        print(f"\n  {lab}, B_1Mpc = 4.4 nG, 30 GHz:")
        for bl in beams:
            print(f"    anisotropic rms alpha, {bl:16s} = {np.degrees(rms[bl]):.3e} deg")
        print(f"    monopole, divergence-free field (exact) = {np.degrees(kfac * mono):.2e} deg")
        print(f"    monopole if the field were longitudinal = {np.degrees(kfac * mono_long):.2e} deg  (estimator check)")
        print(f"    monopole from n_e modulation (delta_e rms {d_rms:g}) = {np.degrees(kfac * m_mod):.2e} deg")
    sc = results[cases[0][0]]
    gate("divergence-free field: monopole vanishes (< 1e-12 of rms)",
         all(abs(r['mono']) < 1e-12 * r['rms']['pointwise'] for r in results.values()), "div B = 0")
    gate("estimator detects a monopole when div B != 0",
         all(abs(r['mono_long']) > 1e3 * abs(r['mono']) for r in results.values()), "")
    lb = "30' (LiteBIRD)"
    print(f"\n  scale-invariant, 30 GHz: {np.degrees(sc['rms'][lb]) / 4.4:.2f} deg rms per nG (30' beam);"
          " literature quotes ~1-1.6 deg per nG at 30 GHz (Kosowsky & Loeb 1996; not verified here)")
    worst = max(abs(r['mono_mod']) for r in results.values())
    print("  frequency dependence (alpha ~ nu^-2): worst-case monopole incl. n_e modulation,"
          " and 30'-beam anisotropic rms for n_B = -2.9:")
    for nu in (40, 68, 119, 235, 402):
        f2 = (30.0 / nu) ** 2
        print(f"    {nu:4d} GHz: monopole <= {np.degrees(worst) * f2:.2e} deg;"
              f" anisotropic rms {np.degrees(sc['rms'][lb]) * f2:.3e} deg")
    m40 = np.degrees(worst) * (30.0 / 40) ** 2
    gate("PMF monopole at 40 GHz below the 0.032 deg achromaticity threshold", m40 < 0.032, f"{m40:.1e} deg")
    return results


def main(cache_dir):
    print("\n=== Stage 10l: leakage / ellipticity in the EB+TB test, and PMF Faraday Monte Carlo ===")
    p1 = part1(cache_dir)
    p2 = part2()
    print(f"\n  gates: {sum(gates)}/{len(gates)} passed")
    return p1, p2


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-dir", default=SCR)
    main(ap.parse_args().cache_dir)
