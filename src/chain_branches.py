#!/usr/bin/env python3
"""
Branches of the force chain (FORCE_CHAIN.md): seven places where values the chain already
carries meet a measurement the chain did not use. src/force_chain.py calls these functions
with its own values; run on its own, this file uses the same inputs and prints each branch.

B1  The W mass. The chain's tree-level electroweak masses miss by more than the
    measurement's error. Stage 2's running of alpha from zero momentum to M_Z, and the top
    quark's loop, are the two largest corrections:
        M_W^2 (1 - M_W^2/M_Z^2) = pi alpha / (sqrt2 G_F (1 - Delta r)),
        Delta r = Delta alpha - (c^2/s^2) Delta rho,  Delta rho = 3 G_F m_t^2/(8 sqrt2 pi^2) (1 - QCD).
    Not included: the remaining bosonic and two-loop terms (MODEL of Delta r: its two
    leading pieces only).
B2  The neutron lifetime. G_F (the weak force), |V_ud| and the nucleon's axial coupling g_A
    (the strong force's imprint on the weak current) fix how fast a free neutron decays:
        1/tau = G_F^2 |V_ud|^2 m_e^5 f (1 + 3 g_A^2) (1 + RC) / (2 pi^3 hbar).
    The phase-space factor f is computed here from the neutron-proton mass difference, with
    and without the Coulomb attraction of the outgoing electron. The electroweak radiative
    corrections are quoted (LIT: Marciano and Sirlin, PRL 96, 032002 (2006):
    tau (1 + 3 g_A^2) |V_ud|^2 = 4908.7(1.9) s).
B3  Primordial helium. Gravity sets how fast the early universe expands, the weak force how
    fast neutrons and protons interconvert, the strong force when deuterium can survive, and
    electromagnetism the barrier that deuterium must cross to burn. The neutron fraction is
    followed from 10 MeV down with the exact weak rates (normalised to B2's lifetime), the
    expansion rate from Friedmann's equation with photons, electrons, positrons and three
    neutrinos, and then a minimal network: n + p <-> D + gamma, and D + D, after which each
    fusion is taken to end in helium-4 (3 D -> 4He + n + p). MODEL: that network. It has
    two nuclear inputs, and the result barely depends on them (printed).
B4  When matter collapses. A cold star is held up by the Pauli pressure of its fermions.
    Both limits are pure numbers times M_Pl^3 / m_N^2:
        Chandrasekhar (electrons, Lane-Emden n = 3):  3.098 / mu_e^2,
        Oppenheimer-Volkoff (free neutrons, general relativity):  0.384,
    both integrated here. The heaviest neutron star measured is three times the second
    number: the strong force's repulsion, not Pauli pressure, holds neutron stars up.

B5  The electron's magnetic moment. The chain's alpha(0) comes down from M_Z and carries the
    hadronic input's error. The electron's anomaly a_e = (g - 2)/2 is a power series in
    alpha/pi with known coefficients (LIT: the QED series to five loops, plus small
    mass-dependent, hadronic and weak terms), so the measured a_e gives alpha directly.
    CHECK: inverting the series reproduces the published 1/alpha = 137.035999166(15).
B6  The weak mixing angle at low energy. The same fermion loops that run alpha (stage 2)
    mix the photon with the Z, so the weak mixing angle runs too:
        s^2(0) = s^2(M_Z) + sum over sectors (lambda - s^2) Delta alpha,
        lambda = sum N_c Q T_3 / (2 sum N_c Q^2) = 1/4 for leptons, 21/44 for five quarks.
    MODEL: one loop, the hadronic mixing weighted by the quark charges, the W loop left out.
B7  The neutron-proton mass difference. It is not derived: lattice QCD + QED gets it from the
    up-down mass difference and the electromagnetic self-energy (LIT). What is computed is
    what it controls: 3a's lifetime through the phase space, and 4a's helium through the
    freeze-out and the lifetime. Helium pins it far more tightly than the lattice does.

Labels: CHECK = computed here; LIT = quoted with its source; MODEL = named where it enters.
Independent work, not peer reviewed.
"""
import math
import os
import sys
import warnings

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ladder_links as LL

HBAR, C_LIGHT, E_CH = 1.054571817e-34, 2.99792458e8, 1.602176634e-19      # SI, exact or CODATA 2018
HBAR_MEV_S = LL.HBAR_GEV_S * 1e3
HBARC_MEV_CM = 1.973269804e-11                  # CODATA 2018

# measured inputs of the branches (sources checked against the PDG 2024 text where marked; AUDIT.md)
M_W_MEAS = (LL.M_W, 0.0133)                     # GeV, PDG 2024
M_TOP = 172.57                                  # GeV, PDG 2024
DM_NP = LL.M_N0_MEV - LL.M_P_MEV                # MeV, CODATA 2018 masses
G_A = (1.2754, 0.0013)                          # PDG 2024
MS_CONSTANT = (4908.7, 1.9)                     # s, Marciano-Sirlin 2006: tau (1 + 3 gA^2) |Vud|^2
TAU_N_MEAS = (878.4, 0.5)                       # s, PDG 2024 average (scale factor 1.8)
ETA10 = (6.104, 0.058)                          # PDG 2024 BBN review: CMB (Planck) baryon-to-photon ratio x 1e10
YP_MEAS = (0.245, 0.003)                        # PDG 2024 BBN review, eq. 24.3
DH_MEAS = (25.47e-6, 0.29e-6)                   # PDG 2024 BBN review, eq. 24.2
B_DEUTERON = 2.224566                           # MeV, deuteron binding energy
SIGMA_NP_THERMAL = (0.3326e-24, 2.2e5)          # cm^2 at 2200 m/s = 2.2e5 cm/s: thermal n + p -> D + gamma (1/v law)
S_DD = (0.0508 + 0.0510) * 1e-24                # MeV cm^2: S(0) of D(D,p)T and D(D,n)3He, 50.8 and 51.0 keV b
#                                                 (Viviani et al., arXiv:2207.01433), held constant in energy
M_NS_MEAS = (2.08, 0.07)                        # solar masses, PSR J0740+6620 (Fonseca et al., ApJL 915, L12 (2021))
DR_FULL = 0.03685                               # PDG 2024 electroweak review: the complete Delta r
A_E_MEAS = (1159652180.59e-12, 0.13e-12)        # Fan et al., PRL 130, 071801 (2023)
AINV_FROM_AE = (137.035999166, 0.000000015)     # the same paper: 1/alpha from a_e and the QED series
# QED series for a_e in powers of alpha/pi: one loop (Schwinger), two loops (exact, computed in a_e), then
# three, four and five loops; and the mass-dependent QED, hadronic and weak terms
A_E_C3, A_E_C4, A_E_C5 = 1.181241456587, -1.9122457649, 6.737
A_E_REST = 2.7475e-12 + 1.693e-12 + 0.03053e-12
S2_MZ = (0.23129, 0.00004)                      # PDG 2024, MS-bar
S2_ZERO_PDG = (0.23873, 0.00005)                # PDG 2024 electroweak review, Table 10.2: full calculation
S2_QWEAK = (0.2382, 0.0011)                     # PDG 2024 (Qweak, Nature 557, 207 (2018)), at 157 MeV
DM_NP_LATTICE = {"total": (1.51, 0.28), "QCD": (2.52, 0.29), "QED": (-1.00, 0.16)}   # Borsanyi et al., Science 347, 1452 (2015)
M_U_D = ((2.20, 0.07), (4.69, 0.05))            # MeV, MS-bar at 2 GeV, PDG 2024 quark-mass review eqs. 60.7-60.8


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ------------------------------------------------------------------------------ B1
def w_mass(alpha0, GF, MZ=LL.M_Z, mt=M_TOP, dalpha=None, alpha_s=None):
    """M_W (GeV) at four levels: tree level with alpha(0); with the running of alpha to M_Z;
    with the top quark's Delta rho; with its one-loop QCD correction. Returns a dict."""
    if dalpha is None:
        dalpha = LL.DALPHA_LEP_3LOOP + LL.DALPHA_HAD[0]          # on-shell, leptons + five quark flavours
    if alpha_s is None:
        from qcd_running import alpha_s_run
        alpha_s = alpha_s_run(mt)

    def solve(dr):
        A = math.pi * alpha0 / (math.sqrt(2) * GF * MZ**2 * (1 - dr))
        s2 = (1 - math.sqrt(1 - 4 * A)) / 2
        return MZ * math.sqrt(1 - s2), s2

    def with_top(drho):
        s2 = 0.223
        for _ in range(60):                                      # Delta r depends on s^2: iterate
            m, s2 = solve(dalpha - (1 - s2) / s2 * drho)
        return m

    drho = 3 * GF * mt**2 / (8 * math.sqrt(2) * math.pi**2)
    qcd = 1 - 2 * alpha_s / (3 * math.pi) * (1 + math.pi**2 / 3)
    return {"tree": solve(0.0)[0], "running": solve(dalpha)[0], "top": with_top(drho),
            "top + QCD": with_top(drho * qcd), "Delta alpha": dalpha, "Delta rho": drho, "QCD factor": qcd,
            "full": solve(DR_FULL)[0]}


# ------------------------------------------------------------------------------ B2
def phase_space(Q=DM_NP, me=LL.M_E_MEV, coulomb=True, alpha=1 / 137.035999084, n=20001):
    """f = integral of F(E) p E (Q - E)^2 dE / m_e^5 over the electron's energy, with the
    non-relativistic Fermi function F = x/(1 - e^-x), x = 2 pi alpha E/p (or F = 1)."""
    E = np.linspace(me, Q, n)[1:-1]
    p = np.sqrt(E * E - me * me)
    x = 2 * math.pi * alpha * E / p
    F = x / (1 - np.exp(-x)) if coulomb else 1.0
    return float(np.trapezoid(F * p * E * (Q - E) ** 2, E)) / me**5


def neutron_lifetime(GF, Vud, gA=G_A[0]):
    """(tree-level lifetime with the phase space computed here, lifetime with the quoted
    radiative corrections, its error from g_A, |V_ud| and the constant), in seconds."""
    f = phase_space()
    tree = 2 * math.pi**3 * HBAR_MEV_S / ((GF * 1e-6) ** 2 * Vud**2 * LL.M_E_MEV**5 * f * (1 + 3 * gA**2))
    tau = MS_CONSTANT[0] / (Vud**2 * (1 + 3 * gA**2))
    err = tau * math.sqrt((6 * gA * G_A[1] / (1 + 3 * gA**2)) ** 2 + (2 * LL.V_UD[1] / Vud) ** 2
                          + (MS_CONSTANT[1] / MS_CONSTANT[0]) ** 2)
    return tree, tau, err


# ------------------------------------------------------------------------------ B3
def _thermal_history(mpl_mev, me, n=260):
    """Photon temperature T (MeV, falling), neutrino temperature, and time (s)."""
    T = np.geomspace(10.0, 4e-3, n)
    x = np.linspace(1e-4, 45.0, 3000)[:, None]                   # p / T
    E = np.sqrt(x * x + (me / T) ** 2)
    occ = 1 / (np.exp(E) + 1)
    rho_e = 2 / math.pi**2 * np.trapezoid(x * x * E * occ, x[:, 0], axis=0) * T**4       # e- and e+, 2 spins
    p_e = 2 / math.pi**2 * np.trapezoid(x**4 / (3 * E) * occ, x[:, 0], axis=0) * T**4
    s_gamma = 4 * math.pi**2 / 45 * T**3
    Tnu = T * ((s_gamma + (rho_e + p_e) / T) / (s_gamma * 11 / 4)) ** (1 / 3)            # entropy conservation
    rho = math.pi**2 / 15 * T**4 + rho_e + 3 * 7 / 4 * math.pi**2 / 30 * Tnu**4
    H = np.sqrt(8 * math.pi / 3 * rho) / mpl_mev / HBAR_MEV_S                             # Friedmann, 1/s
    dlna = -np.diff(np.log(Tnu))                                                          # a ~ 1/T_nu
    t = np.concatenate([[0.0], np.cumsum(dlna * 0.5 * (1 / H[1:] + 1 / H[:-1]))]) + 1 / (2 * H[0])
    return T, Tnu, t


def _weak_rates(T, Tnu, tau_n, Q, me, n=40001):
    """n -> p and p -> n rates (1/s) on the temperature grid, normalised to the free lifetime."""
    lnp, lpn = np.empty_like(T), np.empty_like(T)
    qf = np.linspace(-Q + me, 0.0, 4001)                          # free decay: q = -E_nu
    f0 = np.trapezoid(np.sqrt(np.maximum(1 - me * me / (Q + qf) ** 2, 0)) * (Q + qf) ** 2 * qf * qf, qf)
    for i, (t, tn) in enumerate(zip(T, Tnu)):
        L = 45 * max(t, tn) + Q + me
        q = np.linspace(-L, L, n)
        E = Q + q
        ok = np.abs(E) > me
        w = np.where(ok, np.sqrt(np.where(ok, 1 - me * me / E**2, 0.0)) * E * E * q * q, 0.0)
        a, b = np.clip(q / tn, -600, 600), np.clip(E / t, -600, 600)
        lnp[i] = np.trapezoid(w / ((1 + np.exp(a)) * (1 + np.exp(-b))), q)
        lpn[i] = np.trapezoid(w / ((1 + np.exp(-a)) * (1 + np.exp(b))), q)
    return lnp / (tau_n * f0), lpn / (tau_n * f0)


def helium(tau_n, mpl_gev, alpha0, eta10=ETA10[0], Q=DM_NP, me=LL.M_E_MEV, s_dd=S_DD,
           sv_np=SIGMA_NP_THERMAL[0] * SIGMA_NP_THERMAL[1], network=True):
    """Primordial helium-4 mass fraction and what leads to it. Returns a dict with the
    neutron fraction at freeze-out (no decay), Y_p, D/H, and when the helium forms."""
    mN = (LL.M_P_MEV + LL.M_N0_MEV) / 2
    T, Tnu, t = _thermal_history(mpl_gev * 1e3, me)
    lnp, lpn = _weak_rates(T, Tnu, tau_n, Q, me)
    lt = np.log(t)
    f_T = lambda u: float(np.exp(np.interp(u, lt, np.log(T))))
    f_np = lambda u: float(np.exp(np.interp(u, lt, np.log(lnp))))
    f_pn = lambda u: float(np.exp(np.interp(u, lt, np.log(np.maximum(lpn, 1e-300)))))
    x0 = 1 / (1 + math.exp(Q / T[0]))

    def neutrons(u, y, decay):
        tt = math.exp(u)
        return [tt * (-(f_np(u) - (0 if decay else 1 / tau_n)) * y[0] + f_pn(u) * (1 - y[0]))]
    frozen = solve_ivp(neutrons, [lt[0], lt[-1]], [x0], args=(False,), method="LSODA", rtol=1e-8, atol=1e-12).y[0, -1]
    alone = solve_ivp(neutrons, [lt[0], lt[-1]], [x0], args=(True,), method="LSODA", rtol=1e-8, atol=1e-12,
                      dense_output=True)
    out = {"X_n at freeze-out": float(frozen), "t(T = 1 MeV)": float(np.interp(-1.0, -T, t)),
           "t(T = 0.1 MeV)": float(np.interp(-0.1, -T, t)), "T_nu/T": float(Tnu[-1] / T[-1])}
    if not network:
        return out
    eta = eta10 * 1e-10
    b_gamow = math.pi * alpha0 * math.sqrt(2 * mN)                # D + D: reduced mass m_D/2 ~ m_N

    def sv_dd(temp):
        """<sigma v> for D + D (cm^3/s) from a constant S-factor through the Coulomb barrier."""
        e0 = (b_gamow * temp / 2) ** (2 / 3)                      # Gamow peak
        Eg = np.linspace(1e-6, e0 * 12 + 30 * temp, 4000)
        g = np.trapezoid(np.exp(-Eg / temp - b_gamow / np.sqrt(Eg)), Eg)
        return math.sqrt(8 / (math.pi * mN)) * temp**-1.5 * s_dd * g * C_LIGHT * 100

    Tg = np.geomspace(1.0, T[-1], 200)
    svg = np.log(np.array([sv_dd(x) for x in Tg]))

    def net(u, y):
        xn, xp, xd, xa = y
        tt, temp = math.exp(u), f_T(u)
        nb = eta * 2 * 1.2020569031595942 / math.pi**2 * (temp / HBARC_MEV_CM) ** 3      # baryons per cm^3
        # Saha: (n_D / n_n n_p) n_b, with g_D = 3 and g_n = g_p = 2
        K = nb * HBARC_MEV_CM**3 * 0.75 * 2**1.5 * (2 * math.pi / (mN * temp)) ** 1.5 * math.exp(min(B_DEUTERON / temp, 600))
        form = sv_np * nb * (xn * xp - xd / K)
        burn = math.exp(float(np.interp(-temp, -Tg, svg))) * nb * xd * xd / 2             # D + D reactions per baryon
        l1, l2 = f_np(u), f_pn(u)
        return [tt * (-l1 * xn + l2 * xp - form + burn), tt * (l1 * xn - l2 * xp - form + burn),
                tt * (form - 3 * burn), tt * burn]
    u0 = float(np.interp(-1.0, -T, lt))                           # start the network at T = 1 MeV
    xn0 = float(alone.sol(u0)[0])
    with warnings.catch_warnings():                               # scipy's Jacobian step-size bookkeeping overflows harmlessly
        warnings.simplefilter("ignore", RuntimeWarning)
        s = solve_ivp(net, [u0, lt[-1]], [xn0, 1 - xn0, 0.0, 0.0], method="Radau", rtol=1e-7, atol=1e-16)
    xn, xp, xd, xa = s.y[:, -1]
    half = int(np.searchsorted(s.y[3], 0.5 * xa))
    out.update({"Y_p": float(4 * xa), "D/H": float(xd / xp), "baryons": float(xn + xp + 2 * xd + 4 * xa),
                "T at half helium": f_T(s.t[half]), "t at half helium": math.exp(s.t[half]),
                "X_n when helium forms": float(alone.sol(s.t[half])[0])})
    return out


# ------------------------------------------------------------------------------ B4
def lane_emden(n=3):
    """(xi_1, omega = -xi_1^2 theta'(xi_1)) of the Lane-Emden equation of index n."""
    def rhs(x, y):
        return [y[1], -max(y[0], 0.0) ** n - 2 * y[1] / x]
    ev = lambda x, y: y[0]
    ev.terminal = True
    s = solve_ivp(rhs, [1e-6, 30.0], [1 - 1e-12 / 6, -1e-6 / 3], events=ev, rtol=1e-11, atol=1e-13)
    x1 = s.t_events[0][0]
    return x1, -x1 * x1 * s.y_events[0][0][1]


def chandrasekhar_number():
    """M_Ch mu_e^2 / (M_Pl^3 / m_u^2): the relativistic electron gas, a polytrope of index 3."""
    return lane_emden(3)[1] * math.sqrt(3 * math.pi) / 2


def _fermi_gas(xf):
    """Energy density and pressure of a cold free Fermi gas, in units of m^4 c^5 / hbar^3."""
    r = math.sqrt(1 + xf * xf)
    eps = (xf * r * (2 * xf * xf + 1) - math.asinh(xf)) / (8 * math.pi**2)
    P = (xf * r * (2 * xf * xf / 3 - 1) + math.asinh(xf)) / (8 * math.pi**2)
    return eps, P


def ov_star(xc):
    """A star of free neutrons with central Fermi momentum xc m_n c, from the
    Tolman-Oppenheimer-Volkoff equation. Returns (mass in M_Pl^3/m_n^2, radius in
    hbar M_Pl / (m_n^2 c)): in those units the equations contain no constants."""
    def rhs(r, y):
        m, xf = y
        xf = max(xf, 1e-9)
        eps, P = _fermi_gas(xf)
        dP = -(eps + P) * (m + 4 * math.pi * r**3 * P) / (r * r * (1 - 2 * m / r))
        return [4 * math.pi * r * r * eps, dP * 3 * math.pi**2 * math.sqrt(1 + xf * xf) / xf**4]
    ev = lambda r, y: y[1] - 1e-3
    ev.terminal = True
    s = solve_ivp(rhs, [1e-6, 50.0], [0.0, xc], events=ev, rtol=1e-9, atol=1e-12, max_step=0.02)
    return s.y[0, -1], s.t[-1]


def oppenheimer_volkoff_number():
    """(largest mass, its radius, central x_F), in the units of ov_star."""
    r = minimize_scalar(lambda x: -ov_star(x)[0], bounds=(0.4, 1.6), method="bounded", options={"xatol": 1e-4})
    m, rad = ov_star(r.x)
    return m, rad, r.x


def collapse_limits(mpl_gev, G, gm_sun, m_u_kg=LL.U_AMU, m_n_mev=LL.M_N0_MEV):
    """Chandrasekhar (mu_e = 2) and Oppenheimer-Volkoff masses in solar masses, with the two
    pure numbers and the natural mass M_Pl^3/m_n^2."""
    msun = gm_sun / G
    mpl_kg = mpl_gev * 1e9 * E_CH / C_LIGHT**2
    m_n_kg = m_n_mev * 1e6 * E_CH / C_LIGHT**2
    ch, (ov, rad, xc) = chandrasekhar_number(), oppenheimer_volkoff_number()
    return {"Chandrasekhar number": ch, "OV number": ov, "M_Pl^3/m_n^2": mpl_kg**3 / m_n_kg**2 / msun,
            "M_Ch": ch / 4 * mpl_kg**3 / m_u_kg**2 / msun, "M_OV": ov * mpl_kg**3 / m_n_kg**2 / msun,
            "R_OV km": rad * HBAR * mpl_kg / (m_n_kg**2 * C_LIGHT) / 1e3,
            "nucleons": (mpl_kg / m_n_kg) ** 3}


# ------------------------------------------------------------------------------ B5
def a_e(ainv):
    """The electron's anomaly from 1/alpha: the QED series plus the small non-QED terms."""
    x = 1 / (ainv * math.pi)
    z3 = 1.2020569031595942
    c2 = 197 / 144 + math.pi**2 / 12 + 3 * z3 / 4 - math.pi**2 / 2 * math.log(2)     # Petermann, Sommerfield 1957
    return 0.5 * x + c2 * x**2 + A_E_C3 * x**3 + A_E_C4 * x**4 + A_E_C5 * x**5 + A_E_REST


def alpha_from_a_e(ae=A_E_MEAS[0]):
    """1/alpha that reproduces a measured anomaly (bisection on the series)."""
    lo, hi = 136.0, 138.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if a_e(mid) > ae else (lo, mid)
    return (lo + hi) / 2


# ------------------------------------------------------------------------------ B6
def mixing_lambda(fermions):
    """lambda = sum N_c Q T_3 / (2 sum N_c Q^2) for a set of (N_c, Q, T_3): the value s^2 would
    run to if only these fermions' loops acted."""
    return sum(n * q * t for n, q, t in fermions) / (2 * sum(n * q * q for n, q, t in fermions))


LEPTONS = [(1, -1.0, -0.5)] * 3
QUARKS5 = [(3, 2 / 3, 0.5)] * 2 + [(3, -1 / 3, -0.5)] * 3            # u, c and d, s, b


def weak_angle_at_zero(dalpha_lep, dalpha_had, s2_mz=S2_MZ[0]):
    """MS-bar sin^2 theta_W at zero momentum from its value at M_Z and the running of alpha
    in each sector. Returns (s^2(0), lepton shift, hadron shift)."""
    lep = (mixing_lambda(LEPTONS) - s2_mz) * dalpha_lep
    had = (mixing_lambda(QUARKS5) - s2_mz) * dalpha_had
    return s2_mz + lep + had, lep, had


# ------------------------------------------------------------------------------ B7
def splitting_consequences(GF, Vud, mpl_gev, alpha0, deltas):
    """For each neutron-proton mass difference (MeV): (phase space, lifetime in s, Y_p). The
    radiative corrections are taken unchanged, so the lifetime scales as 1/f(delta)."""
    _, tau0, _ = neutron_lifetime(GF, Vud)
    f0 = phase_space()
    out = []
    for d in deltas:
        f = phase_space(Q=d)
        tau = tau0 * f0 / f
        out.append((d, f, tau, helium(tau, mpl_gev, alpha0, Q=d)["Y_p"]))
    return out


def main():
    import black_holes as BH
    G = LL.G_NEWTON
    mpl = math.sqrt(HBAR * C_LIGHT / G) * C_LIGHT**2 / E_CH / 1e9
    a0 = 1 / 137.035999084                          # CODATA 2018; the chain passes its own stage 2 value

    banner("B1  The W mass from G_F, M_Z and alpha: what the running of alpha and the top quark do")
    w = w_mass(a0, LL.G_F_GEV)
    print(f"   Delta alpha (zero momentum -> M_Z) = {w['Delta alpha']:.5f};  Delta rho (top) = {w['Delta rho']:.5f},"
          f" x {w['QCD factor']:.3f} with QCD")
    for k, lab in (("tree", "tree level, alpha(0)"), ("running", "with alpha run to M_Z"),
                   ("top", "with the top quark's loop"), ("top + QCD", "and its QCD correction")):
        print(f"   {lab:28s}: M_W = {w[k]:.3f} GeV  ({100 * (w[k] / M_W_MEAS[0] - 1):+.2f}%)")
    print(f"   measured: {M_W_MEAS[0]} +- {M_W_MEAS[1]} GeV. The two leading corrections leave"
          f" {100 * (w['top + QCD'] / M_W_MEAS[0] - 1):+.2f}%;")
    print("   the remaining bosonic and two-loop terms are not computed (MODEL).")
    print(f"   LIT check: with the PDG's complete Delta r = {DR_FULL} the same relation gives {w['full']:.3f} GeV.")

    banner("B2  The neutron lifetime from G_F, |V_ud| and g_A")
    tree, tau, err = neutron_lifetime(LL.G_F_GEV, LL.V_UD[0])
    print(f"   phase space f = {phase_space(coulomb=False):.4f} (no Coulomb), {phase_space():.4f} with the Fermi function")
    print(f"   tree level with that f: {tree:.1f} s;  with the quoted radiative corrections: {tau:.1f} +- {err:.1f} s")
    print(f"   measured: {TAU_N_MEAS[0]} +- {TAU_N_MEAS[1]} s  (pull {(tau - TAU_N_MEAS[0]) / math.hypot(err, TAU_N_MEAS[1]):+.1f} sigma)")

    banner("B3  Primordial helium: all four forces in one number")
    h = helium(tau, mpl, a0)
    print(f"   expansion (gravity): t = {h['t(T = 1 MeV)']:.2f} s at 1 MeV, {h['t(T = 0.1 MeV)']:.0f} s at 0.1 MeV;"
          f" T_nu/T -> {h['T_nu/T']:.4f} ((4/11)^(1/3) = {(4 / 11) ** (1 / 3):.4f})")
    print(f"   weak freeze-out: neutron fraction {h['X_n at freeze-out']:.4f} if neutrons did not decay")
    print(f"   deuterium survives and burns at T = {h['T at half helium'] * 1e3:.0f} keV, t = {h['t at half helium']:.0f} s,"
          f" when the neutron fraction has decayed to {h['X_n when helium forms']:.4f}")
    print(f"   Y_p = {h['Y_p']:.4f}  (measured {YP_MEAS[0]} +- {YP_MEAS[1]});  baryons conserved to {abs(h['baryons'] - 1):.0e}")
    print(f"   D/H left over = {h['D/H']:.1e} (measured {DH_MEAS[0]:.2e}): the minimal network leaves twice the")
    print("   measured deuterium, since it has no D + p -> 3He. Helium is insensitive to that:")
    for lab, kw in (("D + D S-factor x 2", dict(s_dd=2 * S_DD)), ("D + D S-factor / 2", dict(s_dd=S_DD / 2)),
                    ("n + p capture x 1.3", dict(sv_np=1.3 * SIGMA_NP_THERMAL[0] * SIGMA_NP_THERMAL[1])),
                    ("baryon density + 10%", dict(eta10=1.1 * ETA10[0])), ("lifetime + 5 s", dict())):
        hh = helium(tau + 5 if lab.startswith("lifetime") else tau, mpl, a0, **kw)
        print(f"      {lab:22s}: Y_p = {hh['Y_p']:.4f}")
    print("   and to the force that sets the clock: with G 10% larger, "
          f"Y_p = {helium(tau, mpl / math.sqrt(1.1), a0)['Y_p']:.4f}")

    banner("B4  When matter collapses: two pure numbers times M_Pl^3 / m_N^2")
    s = collapse_limits(mpl, G, BH.GM_SUN)
    x1, om = lane_emden(3)
    print(f"   M_Pl^3 / m_n^2 = {s['M_Pl^3/m_n^2']:.3f} solar masses = {s['nucleons']:.2e} nucleons")
    print(f"   Lane-Emden n = 3: xi_1 = {x1:.5f}, omega = {om:.5f} (tabulated 6.89685, 2.01824)")
    print(f"   Chandrasekhar: {s['Chandrasekhar number']:.4f} / mu_e^2  ->  {s['M_Ch']:.3f} solar masses for carbon"
          f" (mu_e = 2), such as the diamonds")
    print(f"   Oppenheimer-Volkoff, free neutrons: {s['OV number']:.4f}  ->  {s['M_OV']:.3f} solar masses,"
          f" R = {s['R_OV km']:.1f} km (1939: 0.71, 9.6 km)")
    print(f"   heaviest neutron star measured: {M_NS_MEAS[0]} +- {M_NS_MEAS[1]} solar masses ="
          f" {M_NS_MEAS[0] / s['M_OV']:.1f} x the free-neutron limit: the nuclear force's repulsion carries the rest")
    print(f"   GW250114's black holes, {BH.GW_M1:.1f} and {BH.GW_M2:.1f} solar masses, are above every such limit")

    banner("B5  The electron's magnetic moment and alpha")
    d = LL.DALPHA_LEP_3LOOP + LL.DALPHA_HAD[0] + LL.DALPHA_CONV
    chain = LL.AINV_MZ_MSBAR / (1 - d)
    err = chain * LL.DALPHA_HAD[1] / (1 - d)
    print(f"   the chain's route, down from M_Z: 1/alpha(0) = {chain:.4f} +- {err:.4f} (the hadronic input's error)")
    print(f"   a_e from that alpha: {a_e(chain):.8f} +- {a_e(chain) * err / chain:.8f};  measured {A_E_MEAS[0]:.14f}")
    inv = alpha_from_a_e()
    print(f"   the measured a_e inverted through the QED series: 1/alpha = {inv:.9f}"
          f"  (published {AINV_FROM_AE[0]} +- {AINV_FROM_AE[1]})")
    print(f"   they differ by {abs(chain - inv):.1e}, far inside the chain's error; the electron's moment is"
          f" {err / AINV_FROM_AE[1]:.0e} times more precise")
    print("   This is a return trip, not an independent test: the alpha-hat(M_Z) that stage 1 takes as input")
    print("   was itself obtained from alpha(0). What the branch shows is where the chain's alpha comes from.")

    banner("B6  The weak mixing angle at low energy, from the loops that run alpha")
    s0, lep, had = weak_angle_at_zero(LL.DALPHA_LEP_3LOOP, LL.DALPHA_HAD[0])
    print(f"   lambda = {mixing_lambda(LEPTONS):.4f} (leptons), {mixing_lambda(QUARKS5):.4f} = 21/44 (five quarks),"
          f" {mixing_lambda(LEPTONS + QUARKS5 + [(3, 2 / 3, 0.5)]):.4f} = 3/8 (all fermions)")
    print(f"   sin^2 theta_W(M_Z) = {S2_MZ[0]};  leptons {lep:+.5f}, hadrons {had:+.5f}  ->  sin^2 theta_W(0) = {s0:.5f}")
    print(f"   full calculation (PDG): {S2_ZERO_PDG[0]} +- {S2_ZERO_PDG[1]};  measured at 157 MeV (Qweak):"
          f" {S2_QWEAK[0]} +- {S2_QWEAK[1]}  (pull {(s0 - S2_QWEAK[0]) / S2_QWEAK[1]:+.1f} sigma)")
    print(f"   the angle rises by {100 * (s0 / S2_MZ[0] - 1):.1f}% between M_Z and zero; the measurement sees the rise at"
          f" {(S2_QWEAK[0] - S2_MZ[0]) / S2_QWEAK[1]:.1f} sigma")

    banner("B7  The neutron-proton mass difference: quoted, and what it controls")
    (mu, _), (md, _) = M_U_D
    L = DM_NP_LATTICE
    print(f"   m_d - m_u = {md - mu:.2f} MeV (lattice averages);  lattice QCD + QED: {L['QCD'][0]} (quark masses)"
          f" {L['QED'][0]:+} (electromagnetism) = {L['total'][0]} +- {L['total'][1]} MeV;  measured {DM_NP:.4f}")
    rows = splitting_consequences(LL.G_F_GEV, LL.V_UD[0], mpl, a0, (DM_NP, 1.01 * DM_NP, L["total"][0]))
    for dlt, f, t_, y in rows:
        print(f"   delta = {dlt:.4f} MeV: phase space {f:.3f}, lifetime {t_:6.1f} s, Y_p = {y:.4f}")
    slope = (rows[1][3] - rows[0][3]) / (0.01 * DM_NP)
    print(f"   dY_p/d delta = {slope:+.3f} per MeV: the measured helium (+- {YP_MEAS[1]}) fixes delta to"
          f" +- {abs(YP_MEAS[1] / slope) * 1e3:.0f} keV, the lattice to +- {L['total'][1] * 1e3:.0f} keV")
    print(f"   with electromagnetism alone ({L['QED'][0]} MeV) the proton would be the heavier one and hydrogen would decay")


if __name__ == "__main__":
    main()
