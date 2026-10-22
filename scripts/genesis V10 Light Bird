#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10: LiteBIRD pre-registration
================================================================================
Turns GENESIS, plus a minimal STUR coupling, into dated, hashed predictions for
quantities LiteBIRD is designed to measure:

  (1) isotropic cosmic birefringence beta         [LiteBIRD total error ~0.02 deg]
  (2) the calibration-free tomographic difference
      Delta beta = beta_reio - beta_rec            [LiteBIRD forecast ~0.05 deg]
  (3) the tensor-to-scalar ratio r                 [LiteBIRD design sigma(r) ~0.001]

STUR-B, the birefringence sector. This is a BRIDGE HYPOTHESIS: it is not yet
derived from the STUR action. Every assumption is listed here and stored in the
pre-registration file.
  A1  CMB photon polarisation is rotated by the resistance holonomy accumulated
      along its path: beta = kappa * Phi_R, with Phi_R = integral J_a dx^a.
  A2  Phi_R accrues in chronomagnetic log-time u = ln((t + t_c)/t_0), with
      modulation M(u) = 1 + eps cos(2 pi u / ln lambda + phase),
      lambda = 3722/2705:   d beta / du = kappa M(u).
  A3  The rotation is isotropic and achromatic (geometric, not Faraday).
  A4  t_c << t_rec (default t_c = 0; sensitivity reported).

ONE parameter (kappa) is fixed by today's measured beta (ACT DR6 + Planck).
Everything else is then a PREDICTION:
  * beta_reio / beta_rec, set by log-time geometry
  * Delta beta, which is immune to instrumental polarisation-angle miscalibration
  * no frequency dependence across LiteBIRD's 34-448 GHz bands
Competing explanations predict different Delta beta: rotation acting only after
reionization (a late-rolling field, or an instrument miscalibration) gives
Delta beta = 0; rotation completed before reionization gives beta_reio = 0.

Reionization-bump angle: simplified line-of-sight calculation (Zaldarriaga 1997).
The reionization E-mode source is g(chi) * Theta_2(k, chi), with the quadrupole
free-streamed from last scattering, Theta_2 ~ j_2(k (chi_* - chi)), projected
with eps_l(x) = sqrt((l+2)!/(l-2)!) j_l(x)/x^2. The rotation at emission time
enters the B source, so beta_eff(l) = C_l^EB / (2 C_l^EE). ISW contributions to
the late quadrupole are neglected. Gate: a constant beta must come back exactly
at every l. A full CLASS tomographic run should replace this before publication.

Pre-registration: predictions, inputs, assumptions and the SHA-256 of this
source file are written as canonical JSON; the SHA-256 of that file is printed.
Post the hash somewhere with an independent timestamp (a public GitHub commit,
a Zenodo DOI, OSF) BEFORE the data being predicted are released. Anyone can
check it later with:  sha256sum genesis_v10_preregistration.json

Usage
  python genesis_v10_litebird.py
  python genesis_v10_litebird.py --nstar 54.3 --nstar-lo 46 --nstar-hi 57.5
  inside v9:  from genesis_v10_litebird import run_stage10;  run_stage10(reh)
================================================================================
"""
import argparse
import datetime
import hashlib
import json
import os

import numpy as np
from scipy.integrate import cumulative_trapezoid, quad, solve_ivp
from scipy.optimize import brentq
from scipy.special import gammaln, spherical_jn

C_SI = 2.99792458e8
SIGT = 6.6524587e-29
MPC = 3.0856776e22
GYR = 3.15576e16
M_H = 1.6735575e-27
RHO_C_H2 = 1.87834e-26             # critical density / h^2 [kg m^-3]
LN_LAMBDA = np.log(3722 / 2705)    # chronomagnetic invariant

DATA = {
    'beta_now': (0.277, 0.057, "ACT DR6 + Planck joint analysis, arXiv:2608.06480 (4.8 sigma)"),
    'beta_planck': (0.30, 0.05, "Planck legacy, Ballardini et al. 2025, JCAP 09, 075 (stat only)"),
    'LB_sigma_beta': (0.02, "LiteBIRD total error budget, de la Hoz et al. 2025, JCAP 07, 083"),
    'LB_sigma_dbeta': (0.05, "Sherwin & Namikawa 2021, arXiv:2108.09287"),
    'LB_sigma_r': (0.001, "LiteBIRD design goal, total"),
    'tau': (0.0544, 0.0073, "Planck 2018 VI"),
    'age': (13.797, 0.023, "Planck 2018 VI [Gyr]"),
    'z_re': (7.67, 0.73, "Planck 2018 VI"),
    'zstar': 1089.92,
}


# ------------------------------------------------------------------------------
# background: flat LCDM at the Planck 2018 best fit
# ------------------------------------------------------------------------------
class Background:
    def __init__(self, h=0.6736, obh2=0.02237, och2=0.1200, mnu=0.06, Tcmb=2.7255,
                 Neff=3.046, Yp=0.2454):
        self.h = h
        self.omh2 = obh2 + och2 + mnu / 93.14
        self.orh2 = 2.4728e-5 * (Tcmb / 2.7255) ** 4 * (1 + 0.2271 * Neff)
        self.olh2 = h * h - self.omh2 - self.orh2
        self.H100 = 100e3 / MPC
        self.nH0 = (1 - Yp) * obh2 * RHO_C_H2 / M_H
        self.fHe = Yp / (3.9715 * (1 - Yp))
        lna = np.linspace(-30.0, 0.0, 60001)
        t = cumulative_trapezoid(1.0 / self.H(np.exp(-lna) - 1), lna, initial=0.0)
        t += np.exp(lna[0]) ** 2 / (2 * self.H100 * np.sqrt(self.orh2))
        self._lna, self._t = lna, t
        self.t0 = t[-1]
        zc = np.linspace(0, 1200, 120001)
        self._zc = zc
        self._chi = cumulative_trapezoid(C_SI / self.H(zc), zc, initial=0.0) / MPC

    def H(self, z):
        return self.H100 * np.sqrt(self.omh2 * (1 + z) ** 3 + self.orh2 * (1 + z) ** 4 + self.olh2)

    def age(self, z):
        return np.interp(-np.log1p(z), self._lna, self._t)

    def chi(self, z):
        return np.interp(z, self._zc, self._chi)

    # tanh reionization (CAMB convention), helium second reionization at z = 3.5
    def xe(self, z, zre, dz=0.5, zhe=3.5, dzhe=0.5):
        y, yre = (1 + z) ** 1.5, (1 + zre) ** 1.5
        dy = 1.5 * np.sqrt(1 + zre) * dz
        return ((1 + self.fHe) / 2 * (1 + np.tanh((yre - y) / dy))
                + self.fHe / 2 * (1 + np.tanh((zhe - z) / dzhe)))

    def dtau_dz(self, z, zre):
        return C_SI * SIGT * self.nH0 * (1 + z) ** 2 * self.xe(z, zre) / self.H(z)

    def tau(self, zre, zmax=50.0):
        return quad(self.dtau_dz, 0, zmax, args=(zre,), limit=400, points=[3.5, zre])[0]

    def zre_for_tau(self, tau):
        return brentq(lambda z: self.tau(z) - tau, 2.0, 30.0, xtol=1e-6)


# ------------------------------------------------------------------------------
# STUR-B: rotation accrued in chronomagnetic log-time
# ------------------------------------------------------------------------------
def U_of_t(t, t0, eps=0.0, phase=0.0, t_c=0.0):
    u = np.log((t + t_c) / (t0 + t_c))      # the t_0 normalisation is absorbed in `phase`
    return u + eps * LN_LAMBDA / (2 * np.pi) * np.sin(2 * np.pi * u / LN_LAMBDA + phase)


def stur_beta(bg, z, kappa, eps=0.0, phase=0.0, t_c=0.0):
    """rotation [deg] of polarisation emitted at redshift z and observed today"""
    t0 = bg.t0
    return kappa * (U_of_t(t0, t0, eps, phase, t_c) - U_of_t(bg.age(z), t0, eps, phase, t_c))


# ------------------------------------------------------------------------------
# line-of-sight reionization tomography
# ------------------------------------------------------------------------------
class ReioTomography:
    def __init__(self, bg, zre, ells=range(2, 31), nchi=2500, nk=320, ns=0.9649, zmax=30.0):
        self.bg, self.zre, self.ells = bg, zre, np.array(list(ells))
        chi = np.linspace(1e-3, bg.chi(zmax), nchi)
        zg = np.interp(chi, bg._chi, bg._zc)
        dtz = bg.dtau_dz(zg, zre)
        tau_cum = cumulative_trapezoid(dtz, zg, initial=0.0)
        g = dtz * bg.H(zg) / C_SI * MPC * np.exp(-tau_cum)      # visibility per Mpc
        self.chi, self.z, self.g = chi, zg, g
        dchi = np.gradient(chi)
        chis = bg.chi(DATA['zstar'])
        k = np.logspace(-5, np.log10(0.02), nk)
        self.k = k
        self.wk = k ** (ns - 1) * np.gradient(np.log(k))
        Q = spherical_jn(2, np.outer(k, chis - chi))           # free-streamed quadrupole
        self.S = Q * (g * dchi)[None, :]
        x = np.maximum(np.outer(k, chi), 1e-6)
        self._proj = {}
        for ell in self.ells:
            pref = np.exp(0.5 * (gammaln(ell + 3) - gammaln(ell - 1)))
            self._proj[ell] = pref * spherical_jn(ell, x) / x ** 2

    def beta_eff(self, beta_of_z):
        """beta_eff(l) = C_EB / (2 C_EE), and C_EE (arbitrary normalisation), for the reio bump"""
        s2b = np.sin(2 * np.radians(beta_of_z(self.z)))
        out_b, out_c = [], []
        for ell in self.ells:
            SP = self.S * self._proj[ell]
            dE = SP.sum(axis=1)
            dB = (SP * s2b[None, :]).sum(axis=1)
            cee = np.sum(self.wk * dE * dE)
            ceb = np.sum(self.wk * dE * dB)
            out_b.append(0.5 * np.degrees(np.arcsin(np.clip(ceb / cee, -1, 1))))
            out_c.append(cee * ell * (ell + 1))
        return np.array(out_b), np.array(out_c)

    def beta_reio(self, beta_of_z, lmax=10):
        be, cee = self.beta_eff(beta_of_z)
        m = self.ells <= lmax
        w = (2 * self.ells[m] + 1) * cee[m] / (self.ells[m] * (self.ells[m] + 1))
        return float(np.sum(w * be[m]) / np.sum(w)), be, cee


# ------------------------------------------------------------------------------
# inflation fingerprint: exact Mukhanov-Sasaki for Starobinsky R^2
# (same method as GENESIS Stage 2; standalone so this file runs without v9)
# ------------------------------------------------------------------------------
def starobinsky_fingerprint(Nstars, dlnk=(-0.3, -0.15, 0.0, 0.15, 0.3)):
    b = np.sqrt(2 / 3)
    V = lambda p: (1 - np.exp(-b * p)) ** 2
    dV = lambda p: 2 * (1 - np.exp(-b * p)) * b * np.exp(-b * p)

    def rhs(N, y):
        p, pN = y
        return [pN, -(3 - 0.5 * pN ** 2) * (pN + dV(p) / V(p))]
    end = lambda N, y: 0.5 * y[1] ** 2 - 1
    end.terminal = True
    p0 = 6.5
    bg = solve_ivp(rhs, [0, 500], [p0, -dV(p0) / V(p0)], events=end, rtol=1e-11, atol=1e-13,
                   dense_output=True)
    Nend = bg.t_events[0][0]
    H = lambda N: np.sqrt(V(bg.sol(N)[0]) / (3 - 0.5 * bg.sol(N)[1] ** 2))
    eps = lambda N: 0.5 * bg.sol(N)[1] ** 2
    deps = lambda N, d=1e-4: (np.log(eps(N + d)) - np.log(eps(N - d))) / (2 * d)

    out = {}
    for Ns in Nstars:
        Nx = Nend - Ns
        rows = []
        for dl in dlnk:
            Nc = Nx + dl
            k = np.exp(Nc - Nx) * H(Nc)
            Ni = brentq(lambda N: np.exp(N - Nx) * H(N) - k / 200, 0, Nc)
            Nf = brentq(lambda N: np.exp(N - Nx) * H(N) - k * 1e4, Nc, Nend)
            Pk = []
            for tensor in (False, True):
                def ms(N, y, tensor=tensor):
                    R, Rd = y[0] + 1j * y[1], y[2] + 1j * y[3]
                    fr = 0.0 if tensor else deps(N)
                    Rdd = -(3 - eps(N) + fr) * Rd - (k / (np.exp(N - Nx) * H(N))) ** 2 * R
                    return [Rd.real, Rd.imag, Rdd.real, Rdd.imag]
                aH = np.exp(Ni - Nx) * H(Ni)
                z = np.exp(Ni - Nx) * (1.0 if tensor else np.sqrt(2 * eps(Ni)))
                R0 = 1 / (z * np.sqrt(2 * k))
                zp = 1 if tensor else 1 + 0.5 * deps(Ni)
                Rd0 = R0 * (-1j * k / aH - zp)
                s = solve_ivp(ms, [Ni, Nf], [R0, 0, Rd0.real, Rd0.imag], rtol=1e-10,
                              atol=abs(R0) * 1e-13, method='DOP853')
                P = k ** 3 * (s.y[0, -1] ** 2 + s.y[1, -1] ** 2) / (2 * np.pi ** 2)
                Pk.append(8 * P if tensor else P)
            rows.append((np.log(k), Pk[0], Pk[1]))
        lk = np.array([r[0] for r in rows])
        lk -= lk[len(lk) // 2]
        cs = np.polyfit(lk, np.log([r[1] for r in rows]), 2)
        ct = np.polyfit(lk, np.log([r[2] for r in rows]), 1)
        mid = rows[len(rows) // 2]
        out[Ns] = dict(n_s=1 + cs[1], alpha_s=2 * cs[0], n_t=ct[0], r=mid[2] / mid[1])
    return out


# ------------------------------------------------------------------------------
# Stage 10 driver
# ------------------------------------------------------------------------------
def run_stage10(reh=None, nstar=55.0, nstar_lo=50.0, nstar_hi=60.0, eps=0.0, phase=0.0,
                t_c=0.0, out_json="genesis_v10_preregistration.json", verbose=True):
    pr = print if verbose else (lambda *a, **k: None)
    if reh is not None:     # take N* from GENESIS Stage 2.5 when run inside v9
        nstar, nstar_lo, nstar_hi = reh['higgs']['N'], reh['bbn']['N'], reh['instant']['N']
    pr("\n\n=== Stage 10: LiteBIRD pre-registration (STUR-B birefringence + R^2 tensors) ===")
    bg = Background()
    gates = []

    def gate(name, ok, detail):
        gates.append(dict(name=name, passed=bool(ok), detail=detail))
        pr(f"  gate: {name:44s} {detail:46s} {'PASS' if ok else 'FAIL'}")

    # ---- background gates
    age = bg.t0 / GYR
    a_ref, a_err, _ = DATA['age']
    gate("age of universe vs Planck 2018", abs(age - a_ref) < 2 * a_err + 0.02,
         f"{age:.3f} vs {a_ref} +/- {a_err} Gyr")
    tau_ref, tau_err, _ = DATA['tau']
    zre = bg.zre_for_tau(tau_ref)
    zr_ref, zr_err, _ = DATA['z_re']
    gate("z_re from tau = 0.0544 vs Planck 2018", abs(zre - zr_ref) < zr_err,
         f"{zre:.2f} vs {zr_ref} +/- {zr_err}")
    zs = DATA['zstar']
    t_rec, t_re = bg.age(zs), bg.age(zre)
    pr(f"  t0 = {age:.3f} Gyr, t(z*) = {t_rec / GYR * 1e6:.0f} kyr, t(z_re = {zre:.2f}) = "
       f"{t_re / GYR * 1e3:.0f} Myr")
    pr(f"  log-time spans: ln(t0/t*) = {np.log(bg.t0 / t_rec):.3f}, "
       f"ln(t0/t_re) = {np.log(bg.t0 / t_re):.3f}, ln(lambda) = {LN_LAMBDA:.4f}")

    # ---- tomography + gates
    tomo = ReioTomography(bg, zre)
    _, be_c, _ = tomo.beta_reio(lambda z: 0.3 + 0 * z)
    gate("constant beta returned at every l", np.max(np.abs(be_c - 0.3)) < 1e-9,
         f"max |beta_eff - 0.3| = {np.max(np.abs(be_c - 0.3)):.1e}")
    b0, _, _ = tomo.beta_reio(lambda z: 0 * z)
    gate("kappa = 0 gives no rotation", abs(b0) < 1e-12, f"beta_reio = {b0:.1e}")
    br_an = np.log((bg.t0 + t_c) / (t_rec + t_c))
    gate("beta_rec(eps=0) = kappa ln((t0+tc)/(t*+tc))",
         abs(stur_beta(bg, zs, 1.0, 0.0, 0.0, t_c) - br_an) < 1e-12, f"{br_an:.6f} deg per kappa")

    # ---- fit kappa to today's beta (dominated by recombination-era multipoles)
    bv, be_, bref = DATA['beta_now']
    per_k = float(stur_beta(bg, zs, 1.0, eps, phase, t_c))
    kappa, s_kappa = bv / per_k, be_ / per_k
    bfun = lambda z: stur_beta(bg, z, kappa, eps, phase, t_c)
    beta_rec = float(bfun(zs))
    beta_reio, be_l, _ = tomo.beta_reio(bfun)
    ratio = beta_reio / beta_rec
    dbeta = beta_reio - beta_rec
    s_dbeta = abs(dbeta) * be_ / bv
    pr(f"\n  kappa fixed by beta = {bv} +/- {be_} deg [{bref}]")
    pr(f"  kappa = {kappa:.5f} +/- {s_kappa:.5f} deg per unit log-time (eps = {eps}, t_c = {t_c} s)")
    pr("  PREDICTIONS (STUR-B):")
    pr(f"    beta_rec   = {beta_rec:.3f} deg (input, l >~ 30)")
    pr(f"    beta_reio  = {beta_reio:.3f} +/- {abs(beta_reio) * be_ / bv:.3f} deg (l = 2-10, LOS-weighted)")
    pr(f"    ratio      = {ratio:.3f}   (late-only rotation: 1; pre-reionization rotation: 0)")
    pr(f"    Delta beta = {dbeta:+.3f} +/- {s_dbeta:.3f} deg (calibration-free)")
    sLB = DATA['LB_sigma_dbeta'][0]
    sig_vs0 = abs(dbeta) / np.hypot(sLB, s_dbeta)
    pr(f"    vs LiteBIRD sigma(Delta beta) ~ {sLB} deg -> distinguishable from 0 at {sig_vs0:.1f} sigma")
    pr("    beta_eff(l): " + " ".join(f"{l}:{b:.3f}" for l, b in zip(tomo.ells[:12], be_l[:12])))

    # ---- robustness of the ratio to the unknowns
    pr("\n  robustness of beta_reio/beta_rec (the prediction must not hinge on unknowns):")
    rob = {}
    for lab, tc_ in [("eps = 0 (baseline)", 0.0), ("t_c = 1e4 yr", 1e4 * GYR * 1e-9),
                     ("t_c = 1e5 yr", 1e5 * GYR * 1e-9), ("t_c = 1 Myr", 1e6 * GYR * 1e-9)]:
        f = lambda z, tc_=tc_: stur_beta(bg, z, 1.0, 0.0, 0.0, tc_)
        r_ = tomo.beta_reio(f)[0] / float(f(zs))
        rob[lab] = float(r_)
        pr(f"    {lab:24s} ratio = {r_:.3f}")
    for e_ in (0.5, 1.0):
        rr = []
        for ph in np.linspace(0, 2 * np.pi, 13)[:-1]:
            f = lambda z, ph=ph: stur_beta(bg, z, 1.0, e_, ph, 0.0)
            rr.append(tomo.beta_reio(f)[0] / float(f(zs)))
        rob[f"eps = {e_}, all phases"] = [float(min(rr)), float(max(rr))]
        pr(f"    {'eps = ' + str(e_) + ', all phases':24s} ratio in [{min(rr):.3f}, {max(rr):.3f}]")
    rz = []
    for tz in (tau_ref - tau_err, tau_ref + tau_err):
        tm = ReioTomography(bg, bg.zre_for_tau(tz))
        f = lambda z: stur_beta(bg, z, 1.0)
        rz.append(tm.beta_reio(f)[0] / float(f(zs)))
    rob["tau +/- 1 sigma"] = [float(min(rz)), float(max(rz))]
    pr(f"    {'tau +/- 1 sigma':24s} ratio in [{min(rz):.3f}, {max(rz):.3f}]")
    inst = float(stur_beta(bg, zre, 1.0) / stur_beta(bg, zs, 1.0))
    rob["instantaneous at z_re (crude)"] = inst
    pr(f"    {'instantaneous z_re':24s} ratio = {inst:.3f} (crude; the LOS value is the one used)")

    # ---- tensors
    pr("\n  GENESIS R^2 tensor prediction (exact Mukhanov-Sasaki):")
    fp = starobinsky_fingerprint([nstar_lo, nstar, nstar_hi])
    for N, o in fp.items():
        pr(f"    N* = {N:5.1f}: r = {o['r']:.5f}, n_t = {o['n_t']:+.5f}, n_s = {o['n_s']:.4f}, "
           f"alpha_s = {o['alpha_s']:+.5f}")
    o = fp[nstar]
    gate("consistency n_t = -r/8 (single-field)", abs(o['n_t'] + o['r'] / 8) < 0.1 * o['r'] / 8,
         f"n_t = {o['n_t']:+.5f}, -r/8 = {-o['r'] / 8:+.5f}")
    gate("n_s vs slow-roll 1 - 2/N*", abs(o['n_s'] - (1 - 2 / nstar)) < 0.003,
         f"{o['n_s']:.4f} vs {1 - 2 / nstar:.4f}")
    sr = DATA['LB_sigma_r'][0]
    pr(f"    LiteBIRD sigma(r) ~ {sr}: r = {o['r']:.4f} would be a {o['r'] / sr:.1f} sigma detection")

    # ---- falsification criteria
    crit = [
        "LiteBIRD finds |beta| < 3 x 0.02 deg (consistent with 0): STUR-B coupling kappa excluded",
        f"LiteBIRD Delta beta differs from {dbeta:+.3f} deg by > 3 sigma (combined): STUR-B log-time accrual excluded",
        "beta varies with frequency across LiteBIRD bands beyond Faraday/foreground expectations: STUR-B (achromatic) excluded",
        f"r < {min(v['r'] for v in fp.values()) / 3:.4f} at 95%: GENESIS R^2 inflation (any reheating) excluded",
    ]
    pr("\n  falsification criteria (stored in the pre-registration):")
    for c in crit:
        pr("    - " + c)

    payload = dict(
        pipeline="GENESIS v10 Stage 10",
        authors="Sheldon Lindberg",
        target_experiment="LiteBIRD (JAXA); beta also testable by Simons Observatory",
        hypothesis="STUR-B: CMB polarisation rotated by resistance holonomy accrued in chronomagnetic log-time",
        assumptions={
            "A1": "beta = kappa * Phi_R, Phi_R = integral J_a dx^a along the photon path",
            "A2": "d beta/du = kappa [1 + eps cos(2 pi u/ln lambda + phase)], u = ln((t+t_c)/t0), lambda = 3722/2705",
            "A3": "isotropic and achromatic rotation",
            "A4": f"t_c = {t_c} s",
            "status": "bridge hypothesis; not derived from the STUR action",
            "method": "reionization angle from simplified LOS (free-streamed quadrupole, no ISW)",
        },
        inputs=dict(beta_now=DATA['beta_now'], tau=DATA['tau'], z_star=zs, z_re=zre, eps=eps,
                    phase=phase,
                    cosmology="Planck 2018 flat LCDM, h = 0.6736, omega_b = 0.02237, omega_c = 0.1200"),
        fitted=dict(kappa_deg=kappa, s_kappa_deg=s_kappa),
        predictions=dict(
            beta_rec_deg=beta_rec, beta_reio_deg=beta_reio, ratio_reio_over_rec=ratio,
            delta_beta_deg=dbeta, s_delta_beta_deg=s_dbeta,
            beta_eff_by_ell={int(l): float(b) for l, b in zip(tomo.ells, be_l)},
            achromatic=True,
            ratio_robustness=rob,
            R2_fingerprint={f"{N:.2f}": v for N, v in fp.items()},
            r_R2_headline=o['r'],
        ),
        litebird_sensitivity=dict(beta=DATA['LB_sigma_beta'], delta_beta=DATA['LB_sigma_dbeta'],
                                  r=DATA['LB_sigma_r']),
        falsification=crit,
        gates=gates,
    )
    h = preregister(payload, out_json)
    npass = sum(g['passed'] for g in gates)
    pr(f"\n  gates: {npass}/{len(gates)} passed")
    pr(f"  pre-registration written to {out_json}")
    pr(f"  SHA-256 = {h}")
    pr("  Post this hash publicly (GitHub commit / Zenodo / OSF) to timestamp it.")
    return payload, h


def _clean(x):
    if isinstance(x, dict):
        return {str(k): _clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_clean(v) for v in x]
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
    ap = argparse.ArgumentParser(description="GENESIS v10 Stage 10: LiteBIRD pre-registration")
    ap.add_argument("--nstar", type=float, default=55.0, help="N* from Stage 2.5 (Higgs decay)")
    ap.add_argument("--nstar-lo", type=float, default=50.0, help="lowest N* (BBN-floor reheating)")
    ap.add_argument("--nstar-hi", type=float, default=60.0, help="highest N* (instant reheating)")
    ap.add_argument("--eps", type=float, default=0.0, help="chronomagnetic modulation amplitude")
    ap.add_argument("--phase", type=float, default=0.0, help="chronomagnetic phase [rad]")
    ap.add_argument("--tc", type=float, default=0.0, help="chronomagnetic t_c [s]")
    ap.add_argument("--out", default="genesis_v10_preregistration.json")
    a = ap.parse_args()
    run_stage10(None, a.nstar, a.nstar_lo, a.nstar_hi, a.eps, a.phase, a.tc, a.out)
