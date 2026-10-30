#!/usr/bin/env python3
"""
================================================================================
STUR / GENESIS full birefringence simulation: TEGR + Chronomagnetics + R-phase
================================================================================
One self-contained file. Requirements: numpy, scipy. Optional: camb (pip install
camb) switches on the exact Boltzmann mode (C_l^EE-sourced EB transfers, beta_eff(l),
and a LiteBIRD forecast). Without camb, a fast line-of-sight approximation is used.

  python stur_genesis_simulation.py                     # defaults below
  python stur_genesis_simulation.py --model U0 --mass 2e-32
  python stur_genesis_simulation.py --model STUR-B --eps 0.5 --phase 1.0
  python stur_genesis_simulation.py --model M3a --friction FRW
  python stur_genesis_simulation.py --model all --fast

WHAT IS IN IT
  1. TEGR background. Gravity is the teleparallel torsion scalar T = -6 H^2. The
     action f(T)/16 pi G gives the Friedmann equation 12 H^2 f_T + f = 16 pi G rho.
     f(T) = T is TEGR, which is exactly GR on FRW (gated). f(T) = T + b T^2 is
     offered as an option (b in units of 1/H0^2); it rescales H at early times.
  2. Chronomagnetics. Log-periodic modulation in u = ln(t/t0):
       M(u) = 1 + eps cos(omega u + phase),  omega = 2 pi^2 (repo v7.0) or
       2 pi / ln(3722/2705) (integer triangle). Phase-lock epochs are printed.
  3. R-phase models (theta = R-field phase zero mode; beta = K [theta(t0) - theta(t)],
     K = c_g alpha / 2 pi, c_g = photon anomaly coefficient):
       H0      STUR as written: beta = 0
       STUR-B  log-time accrual d beta/du = kappa M(u)  (GENESIS Stage 10 hypothesis)
       M3a     log-time oscillation theta = A0 sin(omega u + delta), solved from
               theta_uu + F theta_u + omega^2 theta = 0 with F = 0 (repo) or the
               FRW friction F = 3 H t - 1
       U0      ultralight static mass: theta'' + 3H theta' + (m^2/3) sin 3 theta = 0
       C0      free U(1) rotation: theta_dot = q / a^3
     Each model's amplitude is fitted so the recombination angle equals beta_now,
     unless --no-fit (then STUR-B uses kappa = c_g alpha omega_eff / 2 pi).
  4. Projection: recombination angle (visibility-weighted) and reionization angle
     (line-of-sight E-mode source, or exact CAMB sources), ratio, Delta beta.

STATUS (from the GENESIS v10 audit; nothing here should be read as derived unless
listed as such):
  * TEGR with constant |R| is GR on FRW: derived.
  * STUR's own scalar (alpha |R| T) has no propagating scalar perturbation, so
    STUR has no inflation of its own; r is an external input.
  * STUR as written predicts beta ~ 0 (H0).
  * STUR-B, M3a, U0, C0 are bridge hypotheses. M3a's constant-amplitude form needs
    F = 0 (no Hubble friction); with FRW friction it is not reproduced. C0 has no
    allowed field-size window. omega = pi * S (chronomagnetics) is an ansatz.
================================================================================
"""
import argparse

import numpy as np
from scipy.integrate import cumulative_trapezoid, quad, solve_ivp
from scipy.optimize import brentq
from scipy.special import gammaln, spherical_jn

try:
    import camb
    HAVE_CAMB = True
except Exception:
    HAVE_CAMB = False

# ------------------------------------------------------------------------------
# constants and inputs
# ------------------------------------------------------------------------------
C_SI, SIGT, MPC, GYR = 2.99792458e8, 6.6524587e-29, 3.0856776e22, 3.15576e16
M_H, RHO_C_H2 = 1.6735575e-27, 1.87834e-26
ALPHA = 1 / 137.035999
HBAR_EV_S = 6.582119569e-16
OMEGA_V7 = 2 * np.pi ** 2                          # chronomagnetic frequency (v7.0)
OMEGA_TRI = 2 * np.pi / np.log(3722 / 2705)        # integer-triangle value
BETA_NOW = (0.277, 0.057)   # deg, Eskilt (ACT+Planck), arXiv:2608.06480 / PRD 114, 043553
TAU = (0.0544, 0.0073)      # Planck 2018
ZSTAR = 1089.92
COSMO = dict(h=0.6736, obh2=0.02237, och2=0.1200, mnu=0.06, Tcmb=2.7255, Neff=3.046, Yp=0.2454)

GATES = []


def gate(name, ok, detail=""):
    GATES.append(bool(ok))
    print(f"  gate: {name:54s} {detail:32s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 80 + "\n  " + s + "\n" + "=" * 80)


# ------------------------------------------------------------------------------
# 1. TEGR background:  12 H^2 f_T + f = 16 pi G rho,  T = -6 H^2
# ------------------------------------------------------------------------------
class TEGRBackground:
    """flat FRW in teleparallel gravity; f(T) = T + b T^2 with b in units of 1/H0^2"""

    def __init__(self, b=0.0):
        c = COSMO
        self.h, self.b = c['h'], b
        self.omh2 = c['obh2'] + c['och2'] + c['mnu'] / 93.14
        self.orh2 = 2.4728e-5 * (c['Tcmb'] / 2.7255) ** 4 * (1 + 0.2271 * c['Neff'])
        self.olh2 = self.h ** 2 - self.omh2 - self.orh2
        self.H100 = 100e3 / MPC
        self.H0 = self.h * self.H100
        self.nH0 = (1 - c['Yp']) * c['obh2'] * RHO_C_H2 / M_H
        self.fHe = c['Yp'] / (3.9715 * (1 - c['Yp']))
        lna = np.linspace(-30.0, 0.0, 60001)
        z = np.exp(-lna) - 1
        H = self.H(z)
        t = cumulative_trapezoid(1.0 / H, lna, initial=0.0) + 1 / (2 * H[0])
        self.lna, self.z_grid, self.H_grid, self.t_grid = lna, z, H, t
        self.t0 = t[-1]
        zc = np.linspace(0, 1200, 120001)
        self._zc, self._chi = zc, cumulative_trapezoid(C_SI / self.H(zc), zc, initial=0.0) / MPC

    def H_GR(self, z):
        return self.H100 * np.sqrt(self.omh2 * (1 + z) ** 3 + self.orh2 * (1 + z) ** 4 + self.olh2)

    def H(self, z):
        """TEGR (b = 0) gives H_GR. For f = T + b T^2:  H^2 (1 - 18 b H^2) = H_GR^2 (H in H0 units)."""
        HGR = self.H_GR(np.asarray(z, float))
        if self.b == 0.0:
            return HGR
        x = (HGR / self.H0) ** 2
        disc = 1 - 72 * self.b * x
        if np.any(disc < 0):
            bmax = 1 / (72 * np.max(x))
            raise ValueError(f"f(T) = T + b T^2: no real H at the earliest times for b = {self.b:g}/H0^2. "
                             f"The b T^2 term grows as H^2, so positive b must satisfy b < {bmax:.2e}/H0^2 "
                             f"(back to z = {np.max(np.atleast_1d(z)):.1e}); negative b is always real.")
        # GR-continuous branch y = (1 - sqrt(D)) / (36 b), rationalised to avoid cancellation
        # (the direct form returns 0 for small |b| x):  y = 2 x / (1 + sqrt(D))
        y = 2 * x / (1 + np.sqrt(disc))
        return self.H0 * np.sqrt(y)

    def age(self, z):
        return np.interp(-np.log1p(z), self.lna, self.t_grid)

    def a_of_t(self, t):
        return np.exp(np.interp(np.log(t), np.log(self.t_grid), self.lna))

    def H_of_t(self, t):
        return np.exp(np.interp(np.log(t), np.log(self.t_grid), np.log(self.H_grid)))

    def chi(self, z):
        return np.interp(z, self._zc, self._chi)

    # tanh reionization (CAMB convention) + helium at z = 3.5
    def xe(self, z, zre, dz=0.5, zhe=3.5, dzhe=0.5):
        y, yre = (1 + z) ** 1.5, (1 + zre) ** 1.5
        dy = 1.5 * np.sqrt(1 + zre) * dz
        return ((1 + self.fHe) / 2 * (1 + np.tanh((yre - y) / dy))
                + self.fHe / 2 * (1 + np.tanh((zhe - z) / dzhe)))

    def dtau_dz(self, z, zre):
        return C_SI * SIGT * self.nH0 * (1 + z) ** 2 * self.xe(z, zre) / self.H(z)

    def tau(self, zre):
        return quad(self.dtau_dz, 0, 50, args=(zre,), limit=400, points=[3.5, zre])[0]

    def zre_for_tau(self, tau):
        return brentq(lambda z: self.tau(z) - tau, 2.0, 30.0, xtol=1e-6)


# ------------------------------------------------------------------------------
# 2. Chronomagnetics
# ------------------------------------------------------------------------------
class Chronomagnetics:
    def __init__(self, omega=OMEGA_V7, eps=0.0, phase=0.0, t_c=0.0):
        self.omega, self.eps, self.phase, self.t_c = omega, eps, phase, t_c

    def u(self, t, t0):
        return np.log((t + self.t_c) / (t0 + self.t_c))

    def M(self, t, t0):
        return 1 + self.eps * np.cos(self.omega * self.u(t, t0) + self.phase)

    def U(self, t, t0):
        """integral of M du (the accrued log-time)"""
        u = self.u(t, t0)
        return u + self.eps / self.omega * np.sin(self.omega * u + self.phase)

    def phase_locks(self, t_lo, t0, n=5):
        """epochs where cos(omega u + phase) = 1, counting back from today"""
        out = []
        k = np.floor(-self.phase / (2 * np.pi))
        while len(out) < n:
            u = (2 * np.pi * k - self.phase) / self.omega
            t = t0 * np.exp(u)
            if t <= t0 and t >= t_lo:
                out.append(t)
            k -= 1
            if t < t_lo:
                break
        return out


# ------------------------------------------------------------------------------
# 3. R-phase models: each returns beta(t) in degrees for photons emitted at t
# ------------------------------------------------------------------------------
def model_history(name, bg, chrono, args, amp=1.0):
    t0 = bg.t0
    K = args.cg * ALPHA / (2 * np.pi)
    if name == "H0":
        return lambda t: 0.0 * t
    if name == "STUR-B":
        # d beta/du = kappa M(u); amp = kappa [deg per unit ln t]
        return lambda t: amp * (chrono.U(t0, t0) - chrono.U(t, t0))
    if name == "M3a":
        # theta_uu + F theta_u + omega^2 theta = 0, matched today to A0 sin(delta)
        w, d = chrono.omega, args.delta
        F = (lambda u: 0.0) if args.friction == "repo" else \
            (lambda u: 3 * bg.H_of_t(t0 * np.exp(u)) * t0 * np.exp(u) - 1)
        rhs = lambda u, y: [y[1], -F(u) * y[1] - w ** 2 * y[0]]
        uu = np.linspace(0.0, np.log(1e-7 / (t0 / GYR)), 200001)
        s = solve_ivp(rhs, [0.0, uu[-1]], [np.sin(d), w * np.cos(d)], t_eval=uu,
                      rtol=1e-10, atol=1e-13, method='DOP853')
        uu_r, th_r = s.t[::-1], s.y[0][::-1]
        th0 = np.sin(d)
        return lambda t: amp * np.degrees(K * (th0 - np.interp(np.log(t / t0), uu_r, th_r)))
    if name == "U0":
        # theta'' + 3 H theta' + (m^2/3) sin 3 theta = 0 in u = ln t ; amp = theta_i
        m = args.mass / HBAR_EV_S                                 # s^-1
        th_i = np.clip(amp, -np.pi / 3, np.pi / 3)

        def rhs(u, y):
            t = np.exp(u)
            Ht = bg.H_of_t(t) * t
            return [y[1], -(3 * Ht - 1) * y[1] - (m * t) ** 2 * np.sin(3 * y[0]) / 3]
        ui, uf = np.log(1e-7 * GYR), np.log(t0)
        n = int(min(4e5, 4e4 + 40 * m * t0))
        s = solve_ivp(rhs, [ui, uf], [th_i, 0.0], t_eval=np.linspace(ui, uf, n),
                      rtol=1e-10, atol=1e-13, method='DOP853')
        uu, th = s.t, s.y[0]
        return lambda t: np.degrees(K * (th[-1] - np.interp(np.log(t), uu, th)))
    if name == "C0":
        # theta_dot = q / a^3 ; amp = q [s^-1]
        tt = bg.t_grid
        integ = bg.a_of_t(tt) ** -3
        I = cumulative_trapezoid(integ, tt, initial=0.0)
        return lambda t: amp * np.degrees(K * (I[-1] - np.interp(t, tt, I)))
    raise ValueError(name)


# ------------------------------------------------------------------------------
# 4a. fast projection (no camb): visibility-weighted recombination + LOS reionization
# ------------------------------------------------------------------------------
class FastProjection:
    def __init__(self, bg, zre, ns=0.9649):
        self.bg = bg
        # recombination: Gaussian visibility in z (z* = 1089.9, sigma_z ~ 80)
        self.zr = np.linspace(800, 1400, 1201)
        self.wr = np.exp(-0.5 * ((self.zr - ZSTAR) / 80.0) ** 2)
        self.wr /= self.wr.sum()
        self.tr = bg.age(self.zr)
        # reionization: free-streamed quadrupole x E projection (Zaldarriaga 1997), l = 2-10
        chi = np.linspace(1e-3, bg.chi(30.0), 2500)
        zg = np.interp(chi, bg._chi, bg._zc)
        dtz = bg.dtau_dz(zg, zre)
        g = dtz * bg.H(zg) / C_SI * MPC * np.exp(-cumulative_trapezoid(dtz, zg, initial=0.0))
        k = np.logspace(-5, np.log10(0.02), 320)
        self.wk = k ** (ns - 1) * np.gradient(np.log(k))
        Q = spherical_jn(2, np.outer(k, bg.chi(ZSTAR) - chi))
        self.S = Q * (g * np.gradient(chi))[None, :]
        x = np.maximum(np.outer(k, chi), 1e-6)
        self.ells = np.arange(2, 11)
        self.proj = {l: np.exp(0.5 * (gammaln(l + 3) - gammaln(l - 1))) * spherical_jn(l, x) / x ** 2
                     for l in self.ells}
        self.tz = bg.age(zg)

    def beta_rec(self, hist):
        return float(0.5 * np.degrees(np.angle(np.sum(self.wr * np.exp(2j * np.radians(hist(self.tr)))))))

    def beta_reio(self, hist):
        s2b = np.sin(2 * np.radians(hist(self.tz)))
        num = den = 0.0
        for l in self.ells:
            SP = self.S * self.proj[l]
            dE, dB = SP.sum(1), (SP * s2b[None, :]).sum(1)
            cee, ceb = np.sum(self.wk * dE * dE), np.sum(self.wk * dE * dB)
            b = 0.5 * np.degrees(np.arcsin(np.clip(ceb / cee, -1, 1)))
            w = (2 * l + 1) * cee
            num += w * b
            den += w
        return float(num / den)


# ------------------------------------------------------------------------------
# 4b. exact projection (camb): rotation applied at emission to CAMB E-mode sources
# ------------------------------------------------------------------------------
class ExactProjection:
    def __init__(self, bg, tau=TAU[0], r=0.0035):
        p = camb.set_params(H0=100 * COSMO['h'], ombh2=COSMO['obh2'], omch2=COSMO['och2'],
                            mnu=COSMO['mnu'], tau=tau, As=2.1e-9, ns=0.9649, lmax=2500)
        self.res = camb.get_results(p)
        pt = camb.set_params(H0=100 * COSMO['h'], ombh2=COSMO['obh2'], omch2=COSMO['och2'],
                             mnu=COSMO['mnu'], tau=tau, As=2.1e-9, ns=0.9649, r=r, lmax=2500,
                             WantTensors=r > 0)
        self.cl = camb.get_results(pt).get_total_cls(CMB_unit='muK', raw_cl=True)
        self.cl_unl = self.res.get_unlensed_scalar_cls(CMB_unit='muK', raw_cl=True)
        self.eta0 = self.res.tau0
        self.grids = {}
        for key, k, e in (("lo", np.logspace(-5, np.log10(0.03), 600),
                           np.unique(np.concatenate([np.linspace(150, 1500, 2701),
                                                     np.linspace(1500, self.eta0 - 5, 4000)]))),
                          ("hi", np.arange(2e-4, 0.25, 2e-4), np.linspace(150, 800, 1301))):
            S = self.res.get_time_evolution(k, e, ['E_source'])[:, :, 0]
            z = self.res.redshift_at_conformal_time(e)
            t = np.array([self.res.physical_time(zz) for zz in z[::25]]) * GYR
            t = np.exp(np.interp(z, z[::25][::-1], np.log(t)[::-1]))
            self.grids[key] = dict(k=k, eta=e, S=S, w=np.gradient(e), t=t)
        self.ells = np.concatenate([np.arange(2, 41), np.unique(np.round(np.geomspace(45, 1500, 25)).astype(int))])

    def beta_eff(self, hists):
        out_ee, out = [], {n: [] for n in hists}
        for l in self.ells:
            g = self.grids["lo" if l <= 40 else "hi"]
            J = spherical_jn(l, np.outer(g['k'], self.eta0 - g['eta']))
            SJ = g['S'] * J * g['w']
            Nl = np.exp(0.5 * (gammaln(l + 3) - gammaln(l - 1)))
            wk = 4 * np.pi * 2.1e-9 * (g['k'] / 0.05) ** (0.9649 - 1) * np.gradient(np.log(g['k'])) * Nl ** 2
            dE0 = SJ.sum(1)
            out_ee.append(np.sum(wk * dE0 * dE0))
            for n, h in hists.items():
                b = np.radians(h(g['t']))
                dE, dB = (SJ * np.cos(2 * b)).sum(1), (SJ * np.sin(2 * b)).sum(1)
                out[n].append(np.sum(wk * dE * dB))
        cee = np.array(out_ee) * 2.7255e6 ** 2
        return cee, {n: 0.25 * np.degrees(np.arcsin(np.clip(2 * np.array(v) * 2.7255e6 ** 2 / cee, -1, 1)))
                     for n, v in out.items()}

    def split(self, be):
        hi, lo = self.ells >= 50, self.ells <= 10
        ce = self.cl_unl[self.ells, 1]
        wlo = (2 * self.ells[lo] + 1) * ce[lo]
        w_hi = (2 * self.ells[hi] + 1)
        return float(np.sum(w_hi * be[hi]) / np.sum(w_hi)), float(np.sum(wlo * be[lo]) / np.sum(wlo))

    def sigma_dbeta(self, be, fsky=0.6, noise=2.2, fwhm=30.0, lmax=1000):
        """LiteBIRD-like sigma on the tomographic amplitude, miscalibration marginalised"""
        L = np.arange(2, lmax + 1)
        th = np.radians(fwhm / 60)
        nl = np.radians(noise / 60) ** 2 * np.exp(L * (L + 1) * th ** 2 / (8 * np.log(2)))
        cee, cbb = self.cl[L, 1], self.cl[L, 2]
        var = (cee + nl) * (cbb + nl) / ((2 * L + 1) * fsky)
        T = 0.5 * np.sin(4 * np.radians(np.interp(L, self.ells, be))) * (cee - cbb)
        Ta = 2 * np.radians(1.0) * (cee - cbb)
        F = np.array([[np.sum(T * T / var), np.sum(T * Ta / var)], [np.sum(T * Ta / var), np.sum(Ta * Ta / var)]])
        return float(np.sqrt(np.linalg.inv(F)[0, 0]))


# ------------------------------------------------------------------------------
# fitting the model amplitude to beta_now at recombination (linear for small angles)
# ------------------------------------------------------------------------------
def fit_amplitude(name, bg, chrono, args, beta_rec_of):
    if name == "H0":
        return 0.0, True
    if name == "U0":
        ths = np.linspace(0.02, 1.0, 50) * np.pi / 3 * 0.999
        br = np.array([abs(beta_rec_of(model_history(name, bg, chrono, args, th))) for th in ths])
        if br.max() < BETA_NOW[0]:
            return ths[np.argmax(br)], False
        j = int(np.argmax(br >= BETA_NOW[0]))
        if j == 0:
            return ths[0], True
        th = brentq(lambda x: abs(beta_rec_of(model_history(name, bg, chrono, args, x))) - BETA_NOW[0],
                    ths[j - 1], ths[j], xtol=1e-6)
        # the sign of theta_i is free: choose it so beta_rec is positive
        if beta_rec_of(model_history(name, bg, chrono, args, th)) < 0:
            th = -th
        return th, True
    # start small (linear regime) and iterate: with FRW friction M3a's amplitude grows ~186x back
    # to recombination, so a one-step rescaling from an O(1) reference is far from linear
    amp = {"STUR-B": 0.02, "M3a": 1e-4, "C0": 1e-24}[name]
    for _ in range(8):
        b = beta_rec_of(model_history(name, bg, chrono, args, amp))
        if b == 0:
            return amp, False
        amp *= BETA_NOW[0] / b
        if abs(b / BETA_NOW[0] - 1) < 1e-6:
            break
    b = beta_rec_of(model_history(name, bg, chrono, args, amp))
    return amp, abs(b / BETA_NOW[0] - 1) < 1e-3


# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------
def run_model(name, bg, chrono, proj, args, exact):
    if name == "STUR-B" and args.no_fit:
        amp, ok = np.degrees(args.cg * ALPHA * args.omega_eff / (2 * np.pi)), True
    elif exact is not None:
        def brec(h):
            return exact.split(exact.beta_eff({"x": h})[1]["x"])[0]
        amp, ok = fit_amplitude(name, bg, chrono, args, proj.beta_rec)      # fast pre-fit
        if name not in ("H0", "U0"):
            h = model_history(name, bg, chrono, args, amp)
            amp *= BETA_NOW[0] / brec(h) if brec(h) != 0 else 1.0           # exact (linear) refit
    else:
        amp, ok = fit_amplitude(name, bg, chrono, args, proj.beta_rec)
    h = model_history(name, bg, chrono, args, amp)
    out = dict(model=name, amp=amp, reached=ok)
    if exact is not None:
        be = exact.beta_eff({"x": h})[1]["x"]
        out["beta_rec"], out["beta_reio"] = exact.split(be)
        out["beta_eff"] = be
        if abs(out["beta_rec"]) > 0:
            s = exact.sigma_dbeta(be)
            out["sigma_dbeta_LiteBIRD"] = abs(out["beta_reio"] - out["beta_rec"]) * s
    else:
        out["beta_rec"], out["beta_reio"] = proj.beta_rec(h), proj.beta_reio(h)
    out["ratio"] = out["beta_reio"] / out["beta_rec"] if out["beta_rec"] else float("nan")
    out["dbeta"] = out["beta_reio"] - out["beta_rec"]
    return out


def main():
    ap = argparse.ArgumentParser(description="STUR/GENESIS birefringence simulation (TEGR + Chronomagnetics)")
    ap.add_argument("--model", default="all", choices=["all", "H0", "STUR-B", "M3a", "U0", "C0"])
    ap.add_argument("--fT-b", type=float, default=0.0, help="f(T) = T + b T^2, b in 1/H0^2 (0 = TEGR)")
    ap.add_argument("--omega", default="v7", choices=["v7", "triangle"], help="chronomagnetic frequency")
    ap.add_argument("--eps", type=float, default=0.0, help="chronomagnetic modulation amplitude")
    ap.add_argument("--phase", type=float, default=0.0, help="chronomagnetic phase [rad]")
    ap.add_argument("--tc", type=float, default=0.0, help="chronomagnetic t_c [s]")
    ap.add_argument("--cg", type=float, default=6.0, help="photon anomaly coefficient c_g")
    ap.add_argument("--friction", default="FRW", choices=["FRW", "repo"], help="M3a mode equation")
    ap.add_argument("--delta", type=float, default=np.pi / 2, help="M3a phase today [rad]")
    ap.add_argument("--mass", type=float, default=2.0e-32, help="U0 mass [eV]")
    ap.add_argument("--no-fit", action="store_true", help="STUR-B: kappa from c_g and --omega-eff")
    ap.add_argument("--omega-eff", type=float, default=OMEGA_V7, help="STUR-B phase rate per unit ln t")
    ap.add_argument("--fast", action="store_true", help="skip camb even if installed")
    args = ap.parse_args()

    header("1. TEGR background")
    bg = TEGRBackground(b=args.fT_b)
    gr = TEGRBackground(b=0.0)
    print(f"  f(T) = T + b T^2 with b = {args.fT_b} / H0^2;  t0 = {bg.t0 / GYR:.4f} Gyr")
    gate("TEGR (b = 0) is GR on FRW", np.max(np.abs(gr.H(gr.z_grid[::997]) / gr.H_GR(gr.z_grid[::997]) - 1)) < 1e-14,
         "H_TEGR / H_GR = 1")
    tiny = TEGRBackground.__new__(TEGRBackground)
    tiny.__dict__.update(gr.__dict__)
    tiny.b = 1e-60
    gate("f(T) branch continuous with GR as b -> 0", np.max(np.abs(tiny.H(gr.z_grid[::997]) / gr.H_GR(gr.z_grid[::997]) - 1)) < 1e-9,
         "b = 1e-60")
    if args.fT_b != 0:
        dz = bg.H(np.array([0.0, ZSTAR, 1e9])) / gr.H_GR(np.array([0.0, ZSTAR, 1e9])) - 1
        print(f"  f(T) correction to H: today {dz[0]:+.2e}, recombination {dz[1]:+.2e}, z = 1e9 {dz[2]:+.2e}")
    gate("age vs Planck 2018 (13.797 +/- 0.023 Gyr)", abs(gr.t0 / GYR - 13.797) < 0.07, f"{gr.t0 / GYR:.3f} Gyr")
    zre = bg.zre_for_tau(TAU[0])
    gate("z_re from tau = 0.0544 vs Planck (7.67 +/- 0.73)", abs(zre - 7.67) < 0.73, f"z_re = {zre:.2f}")

    header("2. Chronomagnetics")
    omega = OMEGA_V7 if args.omega == "v7" else OMEGA_TRI
    chrono = Chronomagnetics(omega=omega, eps=args.eps, phase=args.phase, t_c=args.tc)
    t_rec, t_re = bg.age(ZSTAR), bg.age(zre)
    print(f"  omega = {omega:.4f} ({args.omega}); lambda = e^(2 pi/omega) = {np.exp(2 * np.pi / omega):.5f};"
          f" eps = {args.eps}, phase = {args.phase}")
    print(f"  log-time span recombination -> today: {np.log(bg.t0 / t_rec):.3f} = "
          f"{np.log(bg.t0 / t_rec) * omega / (2 * np.pi):.1f} chronomagnetic cycles")
    print(f"  M(t) at recombination {chrono.M(t_rec, bg.t0):.3f}, reionization {chrono.M(t_re, bg.t0):.3f},"
          f" today {chrono.M(bg.t0, bg.t0):.3f}")
    locks = chrono.phase_locks(t_re, bg.t0, n=4)
    print("  most recent phase-lock epochs (M max): " + ", ".join(f"{t / GYR:.3f} Gyr" for t in locks))
    gate("accrued log-time U = u when eps = 0", abs(Chronomagnetics(omega).U(t_rec, bg.t0) - np.log(t_rec / bg.t0)) < 1e-12)

    header("3. Projection")
    proj = FastProjection(bg, zre)
    exact = None
    if HAVE_CAMB and not args.fast:
        print("  camb found: exact Boltzmann mode (building E-mode sources, ~1-2 min) ...")
        exact = ExactProjection(bg)
    else:
        print("  fast line-of-sight mode" + (" (camb not installed)" if not HAVE_CAMB else " (--fast)"))
    const = lambda t: 0.3 + 0 * t
    gate("constant beta returned at recombination", abs(proj.beta_rec(const) - 0.3) < 1e-9, "fast")
    gate("constant beta returned at reionization", abs(proj.beta_reio(const) - 0.3) < 1e-6, "fast")
    if exact is not None:
        ce, be = exact.beta_eff({"c": const})
        gate("constant beta returned at every l (exact)", np.max(np.abs(be["c"] - 0.3)) < 1e-6, "camb")
        dev = np.max(np.abs(ce[exact.ells <= 40] / exact.cl_unl[exact.ells[exact.ells <= 40], 1] - 1))
        gate("C_l^EE vs CAMB, l = 2-40", dev < 0.02, f"max dev {dev:.1e}")

    header("4. Models")
    models = ["H0", "STUR-B", "M3a", "U0", "C0"] if args.model == "all" else [args.model]
    rows = []
    for m in models:
        r = run_model(m, bg, chrono, proj, args, exact)
        rows.append(r)
    print(f"\n  {'model':8s} {'amplitude':>12s} {'beta_rec':>9s} {'beta_reio':>10s} {'ratio':>7s} {'Delta beta':>11s}"
          + ("   LiteBIRD sigma(Db)" if exact is not None else ""))
    for r in rows:
        note = "" if r['reached'] else "  (beta_now not reachable)"
        extra = f"   {r.get('sigma_dbeta_LiteBIRD', float('nan')):.3f} deg" if exact is not None else ""
        print(f"  {r['model']:8s} {r['amp']:12.4e} {r['beta_rec']:8.4f}° {r['beta_reio']:9.4f}° "
              f"{r['ratio']:7.3f} {r['dbeta']:+10.4f}°{extra}{note}")
    if exact is not None:
        print("\n  beta_eff(l) [deg]:")
        sel = [2, 5, 10, 20, 40, 100, 300, 1000, 1500]
        idx = [int(np.argmin(np.abs(exact.ells - l))) for l in sel]
        print("    " + "model".ljust(8) + "".join(f"{exact.ells[i]:>8d}" for i in idx))
        for r in rows:
            print("    " + r['model'].ljust(8) + "".join(f"{r['beta_eff'][i]:8.4f}" for i in idx))
    sb = [r for r in rows if r['model'] == "STUR-B"]
    if sb and exact is None and args.eps == 0 and args.tc == 0 and args.omega == "v7" and args.fT_b == 0 and not args.no_fit:
        gate("STUR-B reproduces the GENESIS Stage 10 pre-registration", abs(sb[0]['ratio'] - 0.21290) < 2e-4
             and abs(sb[0]['dbeta'] + 0.21803) < 2e-4, f"ratio {sb[0]['ratio']:.4f}, Db {sb[0]['dbeta']:+.4f}")
    h0 = [r for r in rows if r['model'] == "H0"]
    if h0:
        gate("H0 gives no rotation", abs(h0[0]['beta_rec']) < 1e-12 and abs(h0[0]['beta_reio']) < 1e-12)
    print(f"\n  beta_now = {BETA_NOW[0]} +/- {BETA_NOW[1]} deg; H0 (beta = 0) is {BETA_NOW[0] / BETA_NOW[1]:.1f} sigma away.")
    print("  Notes: M3a with --friction FRW is not the registered M3a (which needs F = 0); C0 has no allowed")
    print("  field-size window; U0's mass is a free parameter STUR does not fix.")
    print(f"\n  gates: {sum(GATES)}/{len(GATES)} passed")


if __name__ == "__main__":
    main()
