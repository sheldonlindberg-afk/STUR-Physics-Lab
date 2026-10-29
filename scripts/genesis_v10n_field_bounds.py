#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10n: field-normalisation bounds by calculation
================================================================================
Replaces three argued steps of genesis_v10d / genesis_v10g with computations:

  [10] Isocurvature. Inflationary fluctuations of the phase are evolved through
       each hypothesis's own dynamics (mode equations in de Sitter, then the
       hypothesis's equation of motion), and the resulting energy-density
       isocurvature is compared with the Planck bound.
  [11] Energy-density history. rho_theta(z) is computed from each hypothesis's
       own dynamics and added to CAMB as an extra component (Lambda + component
       folded into a tabulated w(a) fluid, c_s^2 = 1). A Planck-like Fisher
       forecast (TT/TE/EE, l = 30-2500, tau prior), marginalised over the six
       LCDM parameters, gives the f upper bound. BBN is computed separately.
  [13] Bound conventions: the ACT DR6 A_CB unit convention is fixed by
       requiring its own quoted g < 4.9e-2/H_I to follow.

Hypotheses and the dynamics used (theta = phase, f = decay constant, M = reduced Planck mass)
  C0       free rotation, theta_dot = q/a^3, c_g = 3 (genesis_v10g_hypothesis_ranking.py)
  M3a      theta = A0 sin(omega ln(t/t0) + delta), constant A0 (registered, genesis_v10c_m3a.py),
           c_g = 3. Restoring term (omega/t)^2: during inflation its H^2-scaled form
           m = (3/2) omega H (matching (omega/t)^2 in matter domination) makes it heavy;
           the 'light during inflation' case of genesis_v10d is also kept.
  STUR-B   (Part C, genesis_v10_sturb_action_audit.py) complex mode W with xi T |W|^2,
           W'' + 3H W' + 6 xi H^2 W = 0, xi = 146.2, |W| unpinned (f = |W| today),
           c_g = 0.0201. Gravity sees M^2 -> M^2 + xi|W|^2 (sympy-derived below).
  STUR-B-A2 the pre-registered A2 rotation at constant f (theta_dot = omega/t), c_g = 0.0201,
           kept for comparison with genesis_v10d.

Usage:  python genesis_v10n_field_bounds.py
================================================================================
"""
import importlib.util
import os

import camb
import numpy as np
import sympy as sp
from camb.dark_energy import DarkEnergyFluid, DarkEnergyPPF
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
M_RED = 2.435e18                       # GeV
ALPHA = 1 / 137.035999
OMEGA = 2 * np.pi ** 2
XI = (OMEGA ** 2 + 0.25) / (6 * (2 / 3) ** 2)
HBAR_GEV_S = 6.582119569e-25
AS, R_GENESIS = 2.1e-9, 0.0035
H_I = np.pi * M_RED * np.sqrt(R_GENESIS * AS / 2)          # GeV
COSMO = dict(H0=67.36, ombh2=0.02237, omch2=0.1200, mnu=0.06, tau=0.0544, As=2.1e-9, ns=0.9649)
BETA_NOW = 0.277
A0_RANGE = (1.4352, 2.9311)                                  # Stage 10c registered
CG = {"C0": 3.0, "M3a": 3.0, "STUR-B": 0.0201, "STUR-B-A2": 0.0201}

# external bounds (sources in docs/GENESIS_V10N_FIELD_BOUNDS.md)
ACB_ACT = 0.15                       # ACT DR6, 95%: C_L = A_CB 2pi/(L(L+1)) x 1e-4 rad^2 (Eq. 7)
G_ACT_QUOTED = 4.9e-2                # ACT DR6 quoted g < 4.9e-2 / H_I
G_NGC1275 = (6.3e-13, 8.0e-13)       # GeV^-1, Chandra, 99.7%, B-model dependent
DNEFF_BBN = (0.3, 1.0)               # BBN Delta N_eff 95%: 0.3 (BBN+BK18 analysis), 1.0 (conservative)
P_ISO_MAX = 8.7e-11                  # uncorrelated CDM isocurvature, Planck 2015 (k = 0.05/Mpc)
T_BBN, GSTAR_BBN = 1e-3, 10.75

gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:56s} {detail:32s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 82 + "\n  " + s + "\n" + "=" * 82)


# ------------------------------------------------------------------------------
# background
# ------------------------------------------------------------------------------
class Bg:
    def __init__(self):
        self.res = camb.get_results(camb.set_params(**COSMO))
        self.H0 = self.res.hubble_parameter(0) * 1e3 / 3.0856776e22          # s^-1
        self.lna = np.linspace(np.log(1e-11), 0, 60001)
        z = np.exp(-self.lna) - 1
        Hs = np.array([self.res.hubble_parameter(zz) for zz in z[::300]]) * 1e3 / 3.0856776e22
        self.H = np.exp(np.interp(self.lna, self.lna[::300], np.log(Hs)))
        # cosmic time t(a) = int da/(a H)
        integ = 1 / self.H
        t = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(self.lna))])
        self.t = t + 1 / (2 * self.H[0])                                      # radiation era: t = 1/(2H)
        self.t0 = self.t[-1]
        self.Om_r = self.res.get_Omega('photon', z=0) + self.res.get_Omega('neutrino', z=0)
        self.Om_c = COSMO['omch2'] / (COSMO['H0'] / 100) ** 2
        self.Om_m = self.res.get_Omega('cdm', z=0) + self.res.get_Omega('baryon', z=0)

    def t_of(self, a):
        return np.exp(np.interp(np.log(a), self.lna, np.log(self.t)))

    def H_of(self, a):
        return np.exp(np.interp(np.log(a), self.lna, np.log(self.H)))


def a_bbn():
    return (2.348e-13 / T_BBN) * (3.91 / GSTAR_BBN) ** (1 / 3)


# ------------------------------------------------------------------------------
# 1. hypothesis dynamics -> rho(a)/rho_crit0 per unit x^2 = (f/M)^2
# ------------------------------------------------------------------------------
def c0_q(bg):
    """C0 normalisation: theta_dot = q/a^3 with visibility-weighted rotation = beta_now (as v10g)"""
    lna = bg.lna
    integrand = np.exp(lna) ** -3 / bg.H
    I_from = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(lna))])
    I_to = I_from[-1] - I_from
    eta = np.linspace(150, 600, 1801)
    vis = bg.res.get_background_time_evolution(eta, ['visibility'])['visibility']
    zv = bg.res.redshift_at_conformal_time(eta)
    Iv = np.interp(-np.log1p(zv), lna, I_to)
    K = CG["C0"] * ALPHA / (2 * np.pi)
    return np.radians(BETA_NOW) / K / (np.sum(vis * Iv) / np.sum(vis))


def rho_templates(bg):
    """rho_theta / rho_crit0 at x = f/M = 1, as functions of a"""
    q = c0_q(bg)
    T = {}
    T["C0"] = lambda a: (q / bg.H0) ** 2 / (6 * a ** 6)
    for lab, W in (("M3a (A0 min)", A0_RANGE[0] * OMEGA), ("M3a (A0 max)", A0_RANGE[1] * OMEGA),
                   ("STUR-B-A2", OMEGA)):
        T[lab] = (lambda a, W=W: W ** 2 / (6 * (bg.H0 * bg.t_of(a)) ** 2))
    return T, q


def sympy_part_c():
    """minisuperspace for TEGR + (xi/2) T |W|^2 with T = -6 H^2: Hamiltonian constraint and W equation"""
    t = sp.symbols('t', positive=True)
    N, xi, M = sp.symbols('N xi M', positive=True)
    a = sp.Function('a', positive=True)(t)
    W = sp.Function('W', real=True)(t)            # one real component suffices (|W|^2 -> W^2)
    adot, Wdot = a.diff(t), W.diff(t)
    L = -3 * M ** 2 * a * adot ** 2 / N + a ** 3 * (Wdot ** 2 / (2 * N)) \
        + N * a ** 3 * (xi / 2) * (-6 * adot ** 2 / (N ** 2 * a ** 2)) * W ** 2
    ham = sp.simplify(sp.diff(L, N).subs(N, 1))
    EL = sp.diff(sp.diff(L, Wdot), t) - sp.diff(L, W)
    EL = sp.simplify((EL / a ** 3).subs(N, 1))
    H = adot / a
    target = W.diff(t, 2) + 3 * H * Wdot + 6 * xi * H ** 2 * W
    ok_eom = sp.simplify(EL - target) == 0
    # ham = 0  <=>  3 (M^2 + xi W^2) H^2 = Wdot^2/2
    ok_ham = sp.simplify(ham / a ** 3 - (3 * (M ** 2 + xi * W ** 2) * H ** 2 - Wdot ** 2 / 2)) == 0
    return ok_eom, ok_ham


def part_c_history(bg, ell=0.0, rtol=1e-12):
    """Part C mode from a = 1e-11 (radiation-era eigenmode, plus an admixture `ell` of the
    counter-rotating mode). Returns a, |W|/|W(today)| and the expansion residual
    R = (|dW/dN|^2/6 - xi |W|^2) / (xi |W|^2), which sets H^2/H_std^2 - 1 = xi x^2 |W|^2 R."""
    lna = np.linspace(np.log(1e-11), 0, 400001)
    dlnH = np.gradient(np.log(bg.H_of(np.exp(lna))), lna)
    dl = lambda x: np.interp(x, lna, dlnH)
    Om_r = np.sqrt(6 * XI * 0.25 - (3 * 0.5 - 1) ** 2 / 4)
    rp, rm = 2 * (-0.25 + 1j * Om_r), 2 * (-0.25 - 1j * Om_r)
    W0, Wp0 = 1.0 + ell, rp + ell * rm

    def rhs(x, y):
        Wc, Wp = y[0] + 1j * y[1], y[2] + 1j * y[3]
        Wpp = -(3 + dl(x)) * Wp - 6 * XI * Wc
        return [Wp.real, Wp.imag, Wpp.real, Wpp.imag]
    s = solve_ivp(rhs, [lna[0], 0.0], [W0.real, W0.imag, Wp0.real, Wp0.imag], t_eval=lna[::20], rtol=rtol,
                  atol=1e-15, method='DOP853')
    Wc = s.y[0] + 1j * s.y[1]
    Wp = s.y[2] + 1j * s.y[3]
    R = (np.abs(Wp) ** 2 / 6 - XI * np.abs(Wc) ** 2) / (XI * np.abs(Wc) ** 2)
    return np.exp(s.t), np.abs(Wc) / abs(Wc[-1]), R


def circular_identity():
    """roots r of r^2 + c r + 6 xi = 0 (any constant friction c < sqrt(24 xi)): |r|^2 = 6 xi exactly"""
    r, c, xi = sp.symbols('r c xi', positive=True)
    roots = sp.solve(r ** 2 + c * r + 6 * xi, r)
    prod = sp.simplify(sp.expand(roots[0] * roots[1]))
    return prod


# ------------------------------------------------------------------------------
# 2. CAMB extra component and Planck-like Fisher
# ------------------------------------------------------------------------------
PLANCK = dict(nT=33.0, nP=70.0, fwhm=7.3, fsky=0.6, lmin=30, lmax=2500, tau_sigma=0.007)


def camb_cls(params, rho_x=None, s=0.0, ppf=False):
    p = camb.set_params(**params, lmax=PLANCK['lmax'] + 200)
    if rho_x is not None and s > 0:
        r0 = camb.get_results(camb.set_params(**params))           # closure Omega_de for these params
        OL = r0.get_Omega('de', z=0)
        a = np.logspace(-9, 0, 1200)
        rx = s * rho_x(a)
        OLam = OL - s * rho_x(1.0)
        dlr = np.gradient(np.log(rx), np.log(a))
        wx = -1 - dlr / 3
        w = (-OLam + wx * rx) / (OLam + rx)
        # a constant-c_s^2 fluid cannot cross w = -1; use CAMB's PPF dark energy when the table does
        if w.min() < -1.0 or ppf:
            de = DarkEnergyPPF()
        else:
            de = DarkEnergyFluid()
        de.set_w_a_table(a, w)
        p.DarkEnergy = de
    # linear lensing in every Fisher run (HMCode does not converge for some tables; derivatives
    # are taken consistently either way)
    p.NonLinear = camb.model.NonLinear_none
    r = camb.get_results(p)
    return r.get_total_cls(CMB_unit='muK', raw_cl=True), r


def noise(ell):
    th = np.radians(PLANCK['fwhm'] / 60)
    b = np.exp(ell * (ell + 1) * th ** 2 / (8 * np.log(2)))
    return (np.radians(PLANCK['nT'] / 60)) ** 2 * b, (np.radians(PLANCK['nP'] / 60)) ** 2 * b


def fisher(derivs, cl):
    ell = np.arange(PLANCK['lmin'], PLANCK['lmax'] + 1)
    nT, nP = noise(ell)
    C = np.zeros((len(ell), 2, 2))
    C[:, 0, 0] = cl[ell, 0] + nT
    C[:, 1, 1] = cl[ell, 1] + nP
    C[:, 0, 1] = C[:, 1, 0] = cl[ell, 3]
    Ci = np.linalg.inv(C)
    names = list(derivs)
    D = {n: np.zeros((len(ell), 2, 2)) for n in names}
    for n in names:
        d = derivs[n]
        D[n][:, 0, 0], D[n][:, 1, 1] = d[ell, 0], d[ell, 1]
        D[n][:, 0, 1] = D[n][:, 1, 0] = d[ell, 3]
    F = np.zeros((len(names), len(names)))
    w = (2 * ell + 1) * PLANCK['fsky'] / 2
    for i, a in enumerate(names):
        A = Ci @ D[a]
        for j, b in enumerate(names[i:], start=i):
            Bm = Ci @ D[b]
            F[i, j] = F[j, i] = np.sum(w * np.einsum('lij,lji->l', A, Bm))
    if 'tau' in names:
        k = names.index('tau')
        F[k, k] += 1 / PLANCK['tau_sigma'] ** 2
    return names, F


STEPS = dict(ombh2=0.0003, omch2=0.002, H0=0.5, tau=0.005, As=0.03e-9, ns=0.01)


def lcdm_derivs():
    out = {}
    for n, h in STEPS.items():
        pp, pm = dict(COSMO), dict(COSMO)
        pp[n] += h
        pm[n] -= h
        out[n] = (camb_cls(pp)[0] - camb_cls(pm)[0]) / (2 * h)
    return out


def bound_x2(rho_x, s_test, lcd, cl0, ppf=False):
    """95% upper bound on s = (f/M)^2 from Planck-like TT/TE/EE, LCDM marginalised"""
    c1 = camb_cls(COSMO, rho_x, s_test, ppf)[0]
    c2 = camb_cls(COSMO, rho_x, 2 * s_test, ppf)[0]
    d1 = (c1 - cl0) / s_test
    d2 = (c2 - cl0) / (2 * s_test)
    ell = np.arange(PLANCK['lmin'], PLANCK['lmax'] + 1)
    lin = np.max(np.abs(d2[ell, 0] - d1[ell, 0])) / np.max(np.abs(d1[ell, 0]))
    derivs = dict(lcd)
    derivs['s'] = d1
    names, F = fisher(derivs, cl0)
    Finv = np.linalg.inv(F)
    k = names.index('s')
    sig_marg = np.sqrt(Finv[k, k])
    sig_fixed = 1 / np.sqrt(F[k, k])
    return 1.96 * sig_marg, sig_marg, sig_fixed, lin


# ------------------------------------------------------------------------------
# 3. inflationary fluctuations: de Sitter mode functions
# ------------------------------------------------------------------------------
def ds_mode(mu, n_after=12.0):
    """|delta phi_k|^2 (H/2pi)^-2 versus e-folds after horizon exit, for mass m = mu H"""
    # conformal: v = a delta phi, v'' + (k^2 - (2 - mu^2)/tau^2) v = 0; integrate in N with k = 1, H = 1
    Ni, Nf = -np.log(200.0), n_after                  # N = ln(a H / k)

    def rhs(N, y):
        d, dd = y[0] + 1j * y[1], y[2] + 1j * y[3]
        ka = np.exp(-N)                               # k/(aH)
        ddd = -3 * dd - (ka ** 2 + mu ** 2) * d
        return [dd.real, dd.imag, ddd.real, ddd.imag]
    a_i = np.exp(Ni)                                  # a with k = H = 1
    d0 = np.exp(-1j * (-1 / a_i)) / (a_i * np.sqrt(2.0))           # BD: delta phi = e^{-ik tau}/(a sqrt(2k))
    tau = -1 / a_i
    # d/dN [e^{-i tau}/a] with dtau/dN = -tau (de Sitter, k = H = 1) = (e^{-i tau}/a)(-1 + i tau)
    dd0 = d0 * (-1 + 1j * tau)
    s = solve_ivp(rhs, [Ni, Nf], [d0.real, d0.imag, dd0.real, dd0.imag], rtol=1e-10, atol=1e-16,
                  dense_output=True, method='DOP853', max_step=0.01)
    NN = np.linspace(0, Nf, 400)
    d = s.sol(NN)
    P = 2 * (d[0] ** 2 + d[1] ** 2)                  # [k^3/(2pi^2)|dphi|^2] / (H/2pi)^2 with k = H = 1
    Pdot = 2 * (d[2] ** 2 + d[3] ** 2)
    return NN, P, Pdot


# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------
def main():
    header("[13] bound conventions")
    g_rad = 4 * np.pi * np.sqrt(ACB_ACT * 1e-4)                    # g H_I < 4 pi sqrt(A) [rad^2 convention]
    g_deg = 4 * np.pi * np.sqrt(ACB_ACT * 1e-4 * np.radians(1) ** 2)
    print(f"  A_CB < {ACB_ACT} x 1e-4: rad^2 gives g < {g_rad:.3e}/H_I; deg^2 gives g < {g_deg:.3e}/H_I;"
          f" ACT quotes {G_ACT_QUOTED}/H_I")
    gate("ACT's quoted g bound follows from the rad^2 convention", abs(g_rad / G_ACT_QUOTED - 1) < 0.03,
         f"{g_rad:.4f} vs {G_ACT_QUOTED}")
    gate("ACT's quoted g bound does NOT follow from deg^2", abs(g_deg / G_ACT_QUOTED - 1) > 0.5,
         f"{g_deg:.4f} vs {G_ACT_QUOTED}")
    acb_rad2 = ACB_ACT * 1e-4

    header("Part C gravity coupling (sympy minisuperspace)")
    ok_eom, ok_ham = sympy_part_c()
    gate("W EOM = W'' + 3H W' + 6 xi H^2 W (Part C)", ok_eom, "")
    gate("Friedmann: 3(M^2 + xi|W|^2) H^2 = |W_dot|^2/2 + rho", ok_ham, "")

    bg = Bg()
    gate("background age vs Planck", abs(bg.t0 / 3.15576e16 - 13.797) < 0.05, f"{bg.t0 / 3.15576e16:.3f} Gyr")
    T, q = rho_templates(bg)
    print(f"  C0: theta_dot = q/a^3, q = {q:.3e} s^-1;  M3a/STUR-B-A2 trackers rho ~ 1/t^2;  xi = {XI:.1f}")

    # --------------------------------------------------------------------- [11]
    header("[11] energy-density history -> CAMB, Planck-like Fisher (LCDM marginalised)")
    lcd = lcdm_derivs()
    cl0 = camb_cls(COSMO)[0]
    names, F = fisher(lcd, cl0)
    sig = np.sqrt(np.diag(np.linalg.inv(F)))
    sd = dict(zip(names, sig))
    print("  LCDM forecast: " + ", ".join(f"s({n}) = {sd[n]:.2e}" for n in names))
    gate("Planck-like forecast within 1.6x of Planck 2018 (ns, ombh2, H0)",
         all(0.6 < sd[n] / ref < 1.6 for n, ref in (("ns", 0.0042), ("ombh2", 0.00015), ("H0", 0.54))),
         f"ns {sd['ns'] / 0.0042:.2f}, wb {sd['ombh2'] / 0.00015:.2f}, H0 {sd['H0'] / 0.54:.2f}")
    # gate: fluid Delta N_eff-like component vs CAMB's own N_eff (background)
    og = camb.get_results(camb.set_params(**COSMO)).get_Omega('photon', z=0)
    onu1 = og * (7 / 8) * (4 / 11) ** (4 / 3)
    r_fl = camb_cls(COSMO, lambda a: onu1 * a ** -4, 0.3)[1]
    r_ne = camb.get_results(camb.set_params(**dict(COSMO, nnu=3.046 + 0.3)))
    dth = abs(r_fl.get_derived_params()['thetastar'] / r_ne.get_derived_params()['thetastar'] - 1)
    gate("fluid with Delta N_eff = 0.3 reproduces CAMB theta* (N_eff + 0.3)", dth < 5e-4, f"rel diff {dth:.1e}")

    results = {}
    # trackers: choose s_test so the component is ~0.3% of rho_tot at recombination
    for lab in ("M3a (A0 min)", "M3a (A0 max)", "STUR-B-A2"):
        rho = T[lab]
        a_rec = 1 / 1090.0
        rho_tot_rec = bg.H_of(a_rec) ** 2 / bg.H0 ** 2
        s_test = 0.003 * rho_tot_rec / rho(a_rec)
        s95, sm, sf, lin = bound_x2(rho, s_test, lcd, cl0)
        f_cmb = M_RED * np.sqrt(s95)
        frac = rho(a_rec) * s95 / rho_tot_rec
        results[lab] = dict(f_cmb=f_cmb, frac_rec=frac, lin=lin, degrade=sm / sf)
        print(f"  {lab:14s} f < {f_cmb:.2e} GeV (CMB, 95%)  -> Omega_theta(z=1090) = {frac:.2e};"
              f" marginalisation x{sm / sf:.1f}; derivative nonlinearity {lin:.1e}")
    gate("Fisher derivatives linear (< 5%) for every component", all(r['lin'] < 0.05 for r in results.values()),
         f"max {max(r['lin'] for r in results.values()):.1e}")
    # PPF vs fluid on the same tracker (PPF is needed below for a table that crosses w = -1)
    rho = T["M3a (A0 min)"]
    rho_tot_rec = bg.H_of(1 / 1090.0) ** 2 / bg.H0 ** 2
    s95p = bound_x2(rho, 0.003 * rho_tot_rec / rho(1 / 1090.0), lcd, cl0, ppf=True)[0]
    f_ppf = M_RED * np.sqrt(s95p)
    gate("PPF reproduces the fluid tracker bound (< 5%)", abs(f_ppf / results["M3a (A0 min)"]["f_cmb"] - 1) < 0.05,
         f"{f_ppf:.3e} vs {results['M3a (A0 min)']['f_cmb']:.3e}")

    # BBN for trackers and C0
    header("[11] BBN (T = 1 MeV) from the same histories")
    ab = a_bbn()
    rho_1nu = (7 / 4) * (np.pi ** 2 / 30) * T_BBN ** 4                     # GeV^4
    Hbbn = np.sqrt((np.pi ** 2 / 30) * GSTAR_BBN * T_BBN ** 4 / (3 * M_RED ** 2))   # GeV
    t_gev = 1 / (2 * Hbbn)                                                 # GeV^-1 (radiation era)
    rho_c0_GeV4 = 3 * M_RED ** 2 * (bg.H0 * HBAR_GEV_S) ** 2
    for lab in ("M3a (A0 min)", "M3a (A0 max)", "STUR-B-A2", "C0"):
        if lab == "C0":
            rho_x1 = T[lab](ab) * rho_c0_GeV4
        else:
            W = {"M3a (A0 min)": A0_RANGE[0] * OMEGA, "M3a (A0 max)": A0_RANGE[1] * OMEGA, "STUR-B-A2": OMEGA}[lab]
            rho_x1 = 0.5 * M_RED ** 2 * W ** 2 / t_gev ** 2                  # rho at f = M
        # rho_x1 = rho at x = 1; Delta N_eff = rho / rho_1nu  ->  x^2 < DNeff rho_1nu / rho_x1
        results.setdefault(lab, {})["f_bbn"] = [M_RED * np.sqrt(d * rho_1nu / rho_x1) for d in DNEFF_BBN]
        print(f"  {lab:14s} f < {results[lab]['f_bbn'][0]:.2e} GeV (dN<0.3), < {results[lab]['f_bbn'][1]:.2e} (dN<1)")
    # C0 at recombination when saturating BBN: kination fraction falls as a^2 relative to radiation
    fr_bbn = DNEFF_BBN[0] * rho_1nu / ((np.pi ** 2 / 30) * GSTAR_BBN * T_BBN ** 4)
    rho_rad = lambda a: bg.H_of(a) ** 2 / bg.H0 ** 2
    fr_rec = fr_bbn * (T["C0"](1 / 1090.0) / rho_rad(1 / 1090.0)) / (T["C0"](ab) / ((np.pi ** 2 / 30) * GSTAR_BBN * T_BBN ** 4 / rho_c0_GeV4))
    print(f"  C0 at the BBN bound: Omega_theta(BBN) = {fr_bbn:.2e} -> Omega_theta(z=1090) = {fr_rec:.1e}"
          " (CMB-irrelevant; BBN sets C0's upper edge)")
    # check: C0 BBN bound against v10g's analytic value 5.15e10 (dN < 0.3)
    gate("C0 BBN bound reproduces genesis_v10g (5.15e10 GeV)", abs(results["C0"]["f_bbn"][0] / 5.15e10 - 1) < 0.05,
         f"{results['C0']['f_bbn'][0]:.3e}")
    # tracker BBN cross-check with the radiation-era formula Omega = (2/3) W^2 x^2
    W = A0_RANGE[0] * OMEGA
    x2 = DNEFF_BBN[0] * rho_1nu / ((np.pi ** 2 / 30) * GSTAR_BBN * T_BBN ** 4) / ((2 / 3) * W ** 2)
    gate("tracker BBN bound = radiation-era formula (2/3)W^2 x^2", abs(M_RED * np.sqrt(x2) / results["M3a (A0 min)"]["f_bbn"][0] - 1) < 0.02,
         f"{M_RED * np.sqrt(x2):.3e}")

    # STUR-B Part C: G_eff and kinetic energy at BBN and recombination
    header("[11] STUR-B (Part C): kinetic energy vs xi T|W|^2 in the Friedmann equation")
    # From the sympy constraint: H^2 = rho / (3 M^2 [1 + xi x^2|W|^2 (1 - |W'|^2/(6 xi |W|^2))])
    # = rho/(3M^2) (1 + xi x^2 |W|^2 R + ...),  R = (|W'|^2/6 - xi|W|^2)/(xi|W|^2), W' = dW/dN.
    prod = circular_identity()
    gate("circular mode: |r|^2 = 6 xi for any constant friction (sympy)", sp.simplify(prod - 6 * sp.Symbol('xi', positive=True)) == 0,
         f"r+ r- = {prod}")
    a_w, Wabs, R = part_c_history(bg)
    a_w2, _, R2 = part_c_history(bg, rtol=1e-10)
    lnw = np.log(a_w)

    def smooth(y, width=0.25):
        dx = lnw[1] - lnw[0]
        n = max(int(width / dx), 1)
        return np.convolve(y, np.ones(2 * n + 1) / (2 * n + 1), mode='same')
    Rbar = smooth(R)
    Rbar2 = smooth(np.interp(lnw, np.log(a_w2), R2))
    at = lambda arr, aa: np.interp(np.log(aa), lnw, arr)
    Wat = lambda aa: np.exp(np.interp(np.log(aa), lnw, np.log(Wabs)))
    for lab, aa in (("BBN", ab), ("z = 1e5", 1e-5), ("recombination", 1 / 1090.0), ("z = 10", 1 / 11.0), ("today", 1.0)):
        print(f"  {lab:14s} |W|/f = {Wat(aa):.3e}  R_bar = {at(Rbar, aa):+.2e} (rtol 1e-10: {at(Rbar2, aa):+.2e})"
              f"  xi|W|^2 R_bar = {XI * Wat(aa) ** 2 * at(Rbar, aa):+.2e} per x^2")
    # D(a) = xi |W|^2 R_bar = (H^2/H_std^2 - 1)/x^2. The constant-friction identity makes R vanish
    # in an exact power-law era; the real background is not exactly power-law (matter admixture in
    # the radiation era), and R ~ a while |W|^2 ~ 1/a, so D plateaus through the radiation era.
    Dsm = XI * Wabs ** 2 * smooth(R, 0.5)
    Dsm2 = XI * np.interp(lnw, np.log(a_w2), Wabs) ** 2 * smooth(np.interp(lnw, np.log(a_w2), R2), 0.5)
    conv = [abs(at(Dsm, aa) / at(Dsm2, aa) - 1) for aa in (1e-7, 1e-6, 1e-5, 1 / 1090.0)]
    gate("D(a) converged across rtol 1e-10 / 1e-12 for a >= 1e-7 (< 2%)", max(conv) < 0.02, f"max {max(conv):.1e}")
    cmb = a_w > 1e-7
    neg = np.mean(Dsm[cmb] < 0)
    gate("D(a) single-signed for a >= 1e-7 (H^2 lowered)", neg > 0.999, f"fraction D<0 = {neg:.4f}")
    D_bbn = at(Dsm, ab)
    D_bbn2 = at(Dsm2, ab)
    print(f"  D = (H^2/H_std^2 - 1)/x^2: BBN {D_bbn:+.2e} (rtol 1e-10: {D_bbn2:+.2e}), z = 1e5 {at(Dsm, 1e-5):+.2e},"
          f" recombination {at(Dsm, 1 / 1090.0):+.2e}, today {at(Dsm, 1.0):+.2e}")
    # CMB: smooth template |D(a)| rho_tot(a) in rho_crit0 units per x^2; constant |D| below a = 1e-7
    from scipy.interpolate import UnivariateSpline
    gl = np.linspace(np.log(1e-7), np.log(0.02), 300)
    lnD = np.log(np.abs(np.interp(gl, lnw, Dsm)))
    spl = UnivariateSpline(gl, lnD, k=3, s=len(gl) * 4e-4)
    slope_end = float(spl.derivative()(gl[-1]))

    def Dfun(a):
        la = np.log(a)
        return np.exp(np.where(la > gl[-1], spl(gl[-1]) + slope_end * (la - gl[-1]), spl(np.clip(la, gl[0], gl[-1]))))
    tmpl = lambda a: Dfun(a) * (bg.H_of(a) / bg.H0) ** 2
    fit_err = np.max(np.abs(spl(gl) - lnD))
    gate("spline template reproduces ln|D| over a = 1e-7-0.02 (< 0.05)", fit_err < 0.05, f"max dev {fit_err:.1e}")
    late = abs(at(Dsm, 1 / 51.0)) / abs(at(Dsm, 1e-5))
    gate("late times (z < 50) carry < 1e-3 of the effect at z = 1e5", late < 1e-3, f"{late:.1e}")
    a_rec = 1 / 1090.0
    s_test = 0.003 / Dfun(1e-5)
    # (i) spline template: its residual ripples cross w = -1, so it runs through PPF
    s95, sm, sf, lin = bound_x2(tmpl, s_test, lcd, cl0)
    f_cmb_ppf = M_RED * np.sqrt(s95)
    # (ii) smooth envelope: low-order polynomial in ln a for ln|D|, representable as a c_s^2 = 1 fluid
    cfit = None
    for deg in (2, 3, 4):
        c = np.polyfit(gl, lnD, deg)
        Dp = lambda a, c=c: np.exp(np.polyval(c, np.clip(np.log(a), gl[0], gl[-1]))
                                   + np.where(np.log(a) > gl[-1], np.polyval(np.polyder(c), gl[-1]) * (np.log(a) - gl[-1]), 0))
        aa = np.logspace(-9, 0, 1200)
        rx = Dp(aa) * (bg.H_of(aa) / bg.H0) ** 2
        wxp = -1 - np.gradient(np.log(rx), np.log(aa)) / 3
        if wxp.min() >= -1.0:
            cfit = (deg, c, Dp, np.max(np.abs(np.polyval(c, gl) - lnD)))
            break
    if cfit is None:
        gate("smooth envelope representable as a fluid (w >= -1)", False, "no degree <= 4 works")
        f_cmb_B = f_cmb_ppf
    else:
        deg, c, Dp, env_err = cfit
        gate("smooth envelope representable as a fluid (w >= -1)", True, f"degree {deg}, |dln D| <= {env_err:.2f}")
        tmpl_env = lambda a: Dp(a) * (bg.H_of(a) / bg.H0) ** 2
        s95e, _, _, line = bound_x2(tmpl_env, 0.003 / Dp(1e-5), lcd, cl0)
        f_cmb_B = M_RED * np.sqrt(s95e)
        print(f"  CMB, smooth envelope (fluid, degree {deg}, max |ln-residual| {env_err:.2f}): f < {f_cmb_B:.2e} GeV;"
              f" nonlinearity {line:.1e}")
    print(f"  CMB, rippled spline (PPF): f < {f_cmb_ppf:.2e} GeV  -> template/DE-model spread"
          f" {abs(f_cmb_ppf / f_cmb_B - 1) * 100:.0f}% (cf. PPF-vs-fluid gate above)")
    # BBN: Delta N_eff = (rho_tot/rho_1nu) |D| x^2 (H^2 lowered -> negative Delta N_eff)
    rho_tot_over_1nu = GSTAR_BBN / (7 / 4)
    Dmax = max(abs(D_bbn), abs(D_bbn2))
    f_bbn_B = [M_RED * np.sqrt(d / rho_tot_over_1nu / Dmax) for d in DNEFF_BBN]
    print(f"  BBN: |Delta N_eff| = {rho_tot_over_1nu * Dmax:.2e} x^2 -> f < {f_bbn_B[0]:.2e} GeV (|dN|<0.3),"
          f" < {f_bbn_B[1]:.2e} (|dN|<1)")
    # sensitivity to a counter-rotating admixture (the registered STUR-B has eps = 0)
    ell_b = {}
    for ell in (1e-3, 1e-2):
        a_e2, W_e, R_e = part_c_history(bg, ell=ell)
        i = np.argmin(np.abs(a_e2 - ab))
        win = slice(max(i - 2000, 0), i + 2000)
        Dm = abs(np.mean(XI * W_e[win] ** 2 * R_e[win]))
        ell_b[ell] = M_RED * np.sqrt(DNEFF_BBN[0] / rho_tot_over_1nu / max(Dm, Dmax))
        print(f"  counter-rotating admixture {ell:.0e}: mean |D(BBN)| = {Dm:.2e} -> f < {ell_b[ell]:.2e} GeV (|dN|<0.3)")
    # G_dot/G today if local G_eff = 1/(8 pi M^2 (1 + xi x^2 |W|^2))   [stated model assumption]
    dlnW2 = 2 * np.gradient(np.log(Wabs), lnw)[-200:].mean()
    H0_yr = bg.H0 * 3.15576e7
    GDOT_MAX = 0.7e-13 + 2 * 3.8e-13                      # LLR (Hofmann et al. 2010), 2 sigma, per yr
    x2_g = GDOT_MAX / (XI * abs(dlnW2) * H0_yr)
    f_gdot = M_RED * np.sqrt(x2_g)
    print(f"  today d ln|W|^2/dN = {dlnW2:.2f}; |G_dot/G| = xi x^2 |dln|W|^2/dN| H0 < {GDOT_MAX:.1e}/yr"
          f" -> f < {f_gdot:.2e} GeV (if local G_eff = 1/F)")
    results["STUR-B"] = dict(f_cmb=f_cmb_B, f_cmb_ppf=f_cmb_ppf, f_bbn=f_bbn_B, f_gdot=f_gdot, ell=ell_b)

    # --------------------------------------------------------------------- [10]
    header("[10] inflationary fluctuations: mode functions in de Sitter")
    NN, P0, _ = ds_mode(0.0)
    gate("massless mode freezes at (H/2pi)^2", abs(P0[-1] - 1) < 2e-3, f"P/(H/2pi)^2 = {P0[-1]:.4f}")
    mu_m3a = 1.5 * OMEGA
    mu_b = np.sqrt(6 * XI)
    supp = {}
    for lab, mu in (("M3a heavy (m = 1.5 omega H)", mu_m3a), ("STUR-B Part C (m^2 = 6 xi H^2)", mu_b)):
        NNm, Pm, _ = ds_mode(mu, n_after=8.0)
        sl = np.polyfit(NNm[200:], np.log(Pm[200:]), 1)[0]
        log10_55 = (np.log(Pm[-1]) + sl * (55 - NNm[-1])) / np.log(10)
        supp[lab] = log10_55
        print(f"  {lab:32s} mu = {mu:.1f}: d ln P/dN = {sl:.3f} (expect -3); P(55 e-folds) ~ 10^{log10_55:.0f} (H/2pi)^2")
        gate(f"{lab}: superhorizon decay rate -3", abs(sl + 3) < 0.05, f"{sl:.3f}")

    # light fields: superhorizon S for shift-symmetric histories (C0, STUR-B-A2)
    header("[10] isocurvature for each hypothesis")
    # Shift-symmetric (light) histories, C0 and STUR-B-A2: rho depends on theta_dot only, so a
    # superhorizon delta theta changes rho only through delta theta_dot. Solve the massless mode
    # delta theta'' + (3 + dlnH/dN) delta theta' + (k/aH)^2 delta theta = 0 in N from deep superhorizon
    # (frozen initial condition from inflation) and measure S = 2 delta theta_dot / theta_dot.
    def S_shift(kMpc, a_end, thdot_of_a):
        k = kMpc / 3.0856776e22 * 2.99792458e8
        Ni, Ne = np.log(1e-11), np.log(a_end)
        lnHgrid = lambda N: np.log(bg.H_of(np.exp(N)))
        sol = solve_ivp(lambda N, y: [y[1], -(3 + (lnHgrid(N + 1e-4) - lnHgrid(N - 1e-4)) / 2e-4) * y[1]
                                      - (k / (np.exp(N) * bg.H_of(np.exp(N)))) ** 2 * y[0]],
                        [Ni, Ne], [1.0, 0.0], rtol=1e-10, atol=1e-16, method='DOP853')
        dth_dN = sol.y[1, -1]
        return 2 * dth_dN * bg.H_of(a_end) / thdot_of_a(a_end)     # per unit delta theta
    thdot_c0 = lambda a: q / a ** 3
    thdot_b2 = lambda a: OMEGA / bg.t_of(a)
    a_e = 1e-6
    for lab, thd, Om_at in (("C0", thdot_c0, None), ("STUR-B-A2", thdot_b2, None)):
        S1, S2 = S_shift(0.05, a_e, thd), S_shift(0.10, a_e, thd)
        print(f"  {lab:10s} superhorizon S(k=0.05/Mpc, a=1e-6) = {S1:+.2e} x delta theta;"
              f" S(0.1)/S(0.05) = {S2 / S1:.3f}")
        gate(f"{lab}: S ~ k^2 (vanishes on superhorizon scales)", abs(S2 / S1 - 4) < 0.08, f"ratio {S2 / S1:.3f}")
    # size at the light-field window edges: P_iso ~ (Omega_theta/f_c S)^2 with delta theta = H_I/(2 pi f)
    fc = COSMO['omch2'] / (COSMO['omch2'] + COSMO['ombh2'])
    S_b2_e = abs(S_shift(0.05, a_e, thdot_b2))
    f_e = 1.41e10                                    # STUR-B-A2 lower edge (anisotropy)
    Om_b2 = (3 / 8) * OMEGA ** 2 * (f_e / M_RED) ** 2
    P_b2 = (Om_b2 / fc * S_b2_e * H_I / (2 * np.pi * f_e)) ** 2
    print(f"  STUR-B-A2 at f = {f_e:.1e} GeV: P_iso ~ {P_b2:.1e} (bound {P_ISO_MAX:.1e}); negligible")
    gate("STUR-B-A2 isocurvature negligible at the window edge", P_b2 < 1e-3 * P_ISO_MAX, f"{P_b2:.1e}")
    # M3a light: perturb the amplitude in the registered linear equation and measure delta rho/rho
    def m3a_energy(theta_i, t_i, t_e):
        sol = solve_ivp(lambda tt, y: [y[1], -y[1] / tt - (OMEGA / tt) ** 2 * y[0]], [t_i, t_e],
                        [theta_i, 0.0], rtol=1e-11, atol=1e-14, method='DOP853')
        th, thd = sol.y[0, -1], sol.y[1, -1]
        return (thd * t_e) ** 2 + OMEGA ** 2 * th ** 2
    t_i, t_e = 1.0, np.exp(20.0)
    e0 = m3a_energy(1.0, t_i, t_e)
    e1 = m3a_energy(1.0 + 1e-6, t_i, t_e)
    S_per = (e1 / e0 - 1) / 1e-6                    # delta rho/rho per unit (delta theta / theta_i)
    gate("M3a light: delta rho/rho = 2 delta theta/A0 (computed)", abs(S_per - 2) < 1e-3, f"{S_per:.5f}")
    # CDM-equivalent isocurvature in matter domination: S_eff = (rho_theta/rho_c) S
    for lab, A0 in (("M3a light (A0 min)", A0_RANGE[0]), ("M3a light (A0 max)", A0_RANGE[1])):
        Wm = A0 * OMEGA
        # rho_theta/rho_tot in matter era = (3/8) W^2 x^2 ; rho_c/rho_m = omch2/(omch2+ombh2)
        fc = COSMO['omch2'] / (COSMO['omch2'] + COSMO['ombh2'])
        # P_S = [(3/8) W^2 x^2 / fc]^2 * (S_per^2) * (H_I/(2 pi x M))^2 / A0^2
        coef = ((3 / 8) * Wm ** 2 / fc) ** 2 * S_per ** 2 * (H_I / (2 * np.pi * M_RED)) ** 2 / A0 ** 2
        x2max = P_ISO_MAX / coef                    # P_S = coef * x^2
        results[lab] = dict(f_iso=M_RED * np.sqrt(x2max))
        print(f"  {lab:20s} isocurvature: f < {results[lab]['f_iso']:.2e} GeV (P_iso < {P_ISO_MAX:.1e})")

    # anisotropic birefringence (light fields only) with the confirmed convention
    header("windows (all bounds 95% unless noted; NGC 1275 is 99.7%)")
    def f_aniso(cg):
        return cg * ALPHA / (2 * np.pi) * H_I / (2 * np.pi * np.sqrt(acb_rad2))
    def f_gag(cg, g):
        return cg * ALPHA / (np.pi * g)
    rows = []
    # C0
    lo = max(f_aniso(3.0), f_gag(3.0, G_NGC1275[1]))
    hi = results["C0"]["f_bbn"][0]
    rows.append(("C0 (light)", lo, hi, results["C0"]["f_bbn"][1]))
    # M3a heavy / light
    for A in ("min", "max"):
        cmb = results[f"M3a (A0 {A})"]["f_cmb"]
        bbn = results[f"M3a (A0 {A})"]["f_bbn"]
        lo_h = f_gag(3.0, G_NGC1275[1])
        rows.append((f"M3a heavy, A0 {A}", lo_h, min(cmb, bbn[0]), min(cmb, bbn[1])))
        lo_l = max(f_aniso(3.0), lo_h)
        hi_l = min(cmb, bbn[0], results[f"M3a light (A0 {A})"]["f_iso"])
        rows.append((f"M3a light, A0 {A}", lo_l, hi_l, min(cmb, bbn[1], results[f"M3a light (A0 {A})"]["f_iso"])))
    # STUR-B Part C (heavy during inflation) and A2 (light)
    hiB = min(results["STUR-B"]["f_cmb"], results["STUR-B"]["f_cmb_ppf"], results["STUR-B"]["f_bbn"][0])  # most conservative
    rows.append(("STUR-B Part C (heavy)", f_gag(CG['STUR-B'], G_NGC1275[1]), hiB, hiB))
    rows.append(("  + G_dot/G (if G_eff=1/F)", f_gag(CG['STUR-B'], G_NGC1275[1]), min(hiB, results["STUR-B"]["f_gdot"]),
                 min(hiB, results["STUR-B"]["f_gdot"])))
    rows.append(("  + 1e-2 counter-rotating", f_gag(CG['STUR-B'], G_NGC1275[1]), min(hiB, results["STUR-B"]["ell"][1e-2]),
                 min(hiB, results["STUR-B"]["ell"][1e-2])))
    rows.append(("STUR-B-A2 (light)", max(f_aniso(CG['STUR-B-A2']), f_gag(CG['STUR-B-A2'], G_NGC1275[1])),
                 min(results["STUR-B-A2"]["f_cmb"], results["STUR-B-A2"]["f_bbn"][0]),
                 min(results["STUR-B-A2"]["f_cmb"], results["STUR-B-A2"]["f_bbn"][1])))
    print(f"  {'hypothesis':26s} {'f_min':>10s} {'f_max(dN<0.3)':>14s} {'f_max(dN<1)':>12s}  window")
    for lab, lo, hi, hi2 in rows:
        st = "OPEN" if hi > lo else ("open only with dN<1" if hi2 > lo else "EMPTY")
        print(f"  {lab:26s} {lo:10.2e} {hi:14.2e} {hi2:12.2e}  {st}")
    print(f"\n  f_min sources: anisotropy (light) c_g=3 -> {f_aniso(3.0):.2e}, c_g=0.0201 -> {f_aniso(0.0201):.2e};"
          f" NGC 1275 (8e-13) c_g=3 -> {f_gag(3.0, 8e-13):.2e}, c_g=0.0201 -> {f_gag(0.0201, 8e-13):.2e} GeV")
    print(f"  M3a heavy / STUR-B Part C: inflationary fluctuations suppressed to 10^{min(supp.values()):.0f}"
          " (H/2pi)^2: no anisotropy or isocurvature bound")
    print(f"\n  gates: {sum(gates)}/{len(gates)} passed")
    return rows


if __name__ == "__main__":
    main()
