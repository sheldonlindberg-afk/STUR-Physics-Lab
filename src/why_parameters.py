#!/usr/bin/env python3
"""
Why do the Standard Model's 19 parameters have their values? What can be said, and tested.

None of the 19 is derived by anyone (W0). This script collects the published attempts to
explain them and tests each against the measured values. Every row is one of
    MEASURED     no explanation used here; the value is an input;
    RELATION     established physics relates it to other inputs (it does not fix it);
    EMPIRICAL    a numerical regularity with no accepted derivation;
    CONJECTURE   follows only under an unproven assumption, named in the row.
Established physics stops at MEASURED and RELATION. The rest is marked as such.

W0  The ledger: the 19 parameters, where each enters this repository, and its row above.
    (LIT: A. Kronfeld, arXiv:1007.1444, section 5: "The Standard Model has 19 free
    parameters, or 28 if nonzero neutrino masses and mixings are taken into account";
    PDG 2024 review "Electroweak model and constraints on new physics", section 10.2.)
W1  The Higgs mass from a vanishing quartic at the Planck scale. (CONJECTURE)
    If gravity is asymptotically safe and nothing lies between the Fermi and Planck scales,
    lambda(M_Pl) = 0 and M_H follows from M_t and alpha_s (LIT: Shaposhnikov and Wetterich,
    Phys. Lett. B 683, 196 (2010), arXiv:0912.0208, eq. (12): 126.3 GeV at their inputs,
    +- 2.2 GeV theory). Evaluated at the PDG 2024 inputs by three published NNLO formulas:
    their eq. (12); lambda(M_Pl) = 0 in Buttazzo et al., JHEP 12 (2013) 089,
    arXiv:1307.3536, eq. (61e); and the stability bound, eq. (64). Cross-check: the one-loop
    running of src/m331_scalar.py, integrated down from lambda(M_Pl) = 0 (CHECK).
    Two conditions, two masses: adding beta_lambda(M_Pl) = 0 (the quartic's one-loop beta
    function, their eq. (8)) fixes M_t as well, from the gauge couplings alone. Solved with
    the NNLO couplings at M_Pl of Buttazzo et al. eq. (61), and again at one loop throughout.
    The combination is this script's; Buttazzo et al. note that beta_lambda vanishes near
    1e17-1e18 GeV and call it "more like an accidental cancellation" (their section 4.1).
W2  The same boundary condition with the 3-3-1 scalars. (MODEL, one loop)
    All nine quartics of src/m331_scalar.py set to zero at M_Pl and run down to M_V = 4 TeV.
    The self-quartic of a triplet with no large Yukawa is driven by gauge terms alone and is
    negative at M_V: the potential is unbounded below. The condition does not carry over.
W3  The top mass. (RELATION for the bound; CONJECTURE for the value)
    The infrared quasi-fixed point: a large top Yukawa at a high scale is focused to one
    value at low energy (LIT: Pendleton and Ross; Hill; as described in Bardeen, Carena,
    Pokorski and Wagner, arXiv:hep-ph/9309293). Computed here at one loop from M_Pl.
    Asymptotic safety: M_t,pole ~ 171 GeV (LIT: Eichhorn and Held, Phys. Lett. B 777, 217
    (2018), arXiv:1707.01107, abstract). Read the other way, W1 with the measured M_H gives
    M_t < 171.53 +- 0.42 GeV (LIT: Buttazzo et al., eq. (66)).
W4  The strong coupling and the proton's mass scale. (RELATION)
    One-loop running: Lambda = M_Pl exp(-2 pi / (7 alpha_3(M_Pl))). The small proton-to-
    Planck ratio is the exponential of a coupling of order 1/50; the coupling's value is
    not explained. (LIT: g_3(M_Pl) from Buttazzo et al., eq. (61c); "a 10% increase in the
    strong gauge coupling at the Planck scale makes Lambda_QCD larger than the weak scale",
    their Fig. 5; hadron masses from the quark masses and the coupling: Durr et al., Science
    322, 1224 (2008), arXiv:0906.3599.)
W5  The weak mixing angle in 3-3-1. (RELATION: a bound, not a value)
    Rung 1's matching 1/g_Y^2 = beta^2/g^2 + 1/g_X^2 with g_X^2 > 0 gives
    sin^2 theta_W < 1/(1 + beta^2): 3/4 for beta = +-1/sqrt3.
W6  The strong CP angle. (CONJECTURE: needs an axion, not observed)
    In the 3-3-1 model with right-handed neutrinos (this repository's beta = -1/sqrt3
    content) a Peccei-Quinn symmetry follows from a Z_11 x Z_2 symmetry (LIT: Dias, de S.
    Pires and Rodrigues da Silva, Phys. Rev. D 68, 115009 (2003), arXiv:hep-ph/0309058,
    eqs. (6), (14)-(19)). Checked here in exact fractions: every Yukawa term of their eq.
    (6) and the potential term eta rho chi phi are invariant under their charges, and the
    colour anomaly is 2 X_d, not zero, because the exotic quarks (one u', two d') do not
    cancel. A massless up quark, the other way out, is excluded: m_u differs from zero "by
    more than 30 times the quoted error" (LIT: PDG 2024 quark-mass review, after eq. 60.9).
W7  The Cabibbo angle from the quark masses. (EMPIRICAL)
    Gatto-Sartori-Tonin: theta_12 = arctan sqrt(m_d/m_s) (LIT: Gatto, Sartori and Tonin,
    Phys. Lett. B 28, 128 (1968); exact form and the PDG 2024 test in Antusch, Hinze and
    Saad, arXiv:2510.01312, eq. (4.11): 0.2205 +- 0.0012, "not accurate enough").
    Recomputed from the PDG 2024 masses m_d, m_s at 2 GeV (as listed in their eq. (2.2))
    and sin theta_12 (PDG 2024 CKM review, eq. 12.28).
W8  The charged-lepton masses. (EMPIRICAL)
    Koide: K = (m_e + m_mu + m_tau)/(sqrt m_e + sqrt m_mu + sqrt m_tau)^2 = 2/3 (LIT: holds
    for the pole masses, 2/3 x (0.999989 +- 0.000014), and not for the running masses at
    M_Z, 2/3 x 1.00189, although a field-theory derivation would give running masses: "a
    serious theoretical problem", Y. Koide, arXiv:1809.00425, eqs. (0.2), (1.1), with the 1982
    prediction m_tau = 1776.97 MeV; Xing and Zhang, Phys. Lett. B 635, 107 (2006),
    arXiv:hep-ph/0602134).
W9  Quark flavour in 3-3-1: what the model's structure gives. (RELATION, then MODEL)
    F1  One family is an SU(3)_L triplet and two are antitriplets (anomaly cancellation), so
        the two electroweak vevs enter the quark mass matrices by rows (LIT: the Yukawa terms
        of Dias et al., eq. (6), beta = -1/sqrt3): up-type rows (v_rho, v_rho, v_eta),
        down-type rows (v_eta, v_eta, v_rho).
    F2  One vev ratio. With tan b = v_eta/v_rho the top and bottom Yukawas are equal at
        tan b = y_t/y_b. Yukawas at M_Z from the PDG 2024 inputs (LIT: Antusch, Hinze and
        Saad, arXiv:2510.01312, eq. (2.4)). The ratio is a new parameter, traded for m_b/m_t.
    F3  Is the rest structure? Random O(1) complex Yukawas with that row structure (MODEL):
        the triplet family is the heaviest up-type quark and the lightest down-type quark, so
        the top would decay to the lightest down quark. The measured |V_tb| ~ 1 needs a
        hierarchy inside the Yukawas themselves.
    F4  The same ratio is the angle a of the rho parameter (src/m331_rho_bound.py, R1):
        rho - 1 = (v/w)^2 (sin^2 a - sin^2 a0)^2 at the LHC bound on w, against the global
        fit's rho_0 (LIT: Erler, arXiv:1908.07346).
    F5  (LIT) Because the third family's Z' couplings differ, the left-handed rotations are
        separately physical and the Z' changes flavour at tree level; 3-3-1 adds four mixing
        parameters to the CKM matrix's four (Buras, De Fazio, Girrbach and Carlucci, JHEP 02
        (2013) 023, arXiv:1211.1237, eqs. (53)-(56) and abstract).
W10 The tally.
"""
import os
import sys
from fractions import Fraction as F
from itertools import permutations
from math import asin, atan, exp, hypot, log, pi, sqrt

import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ladder_links as LL
import m331_exact as E
import m331_rho_bound as RB
import m331_scalar as S
import m331_threshold as T
import m331_yukawa as Y

M_T, M_H, M_W = LL.M_T, LL.M_H, LL.M_W           # PDG 2024, GeV
M_T_ERR = 0.29                                   # PDG 2024 (AUDIT.md)
ALPHA_S = 0.1180                                 # PDG 2024, alpha_s(M_Z)
M_PL = E.M_PLANCK

# PDG 2024, MS-bar at 2 GeV, as listed in Antusch, Hinze, Saad, eq. (2.2); CKM review, eq. (12.28)
M_D, M_D_ERR = 4.70, 0.04                        # MeV
M_S, M_S_ERR = 93.5, 0.5                         # MeV
S12, S12_ERR = 0.22501, 0.00068                  # sin(theta_12)
GST_LIT = (0.2205, 0.0012)                       # Antusch, Hinze, Saad, eq. (4.11), from running Yukawas
# MS-bar Yukawa couplings at M_Z from the PDG 2024 inputs: Antusch, Hinze, Saad, eq. (2.4)
YUK_MZ = {"u": 7.04e-6, "c": 3.56e-3, "t": 0.967, "d": 1.54e-5, "s": 3.06e-4, "b": 1.630e-2}
V_TB, V_US, V_CB = 0.999118, 0.22501, 0.04183   # PDG 2024 CKM review, eq. (12.27)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ------------------------------------------------------------------------------ W0
# (parameter, status in this repository, class, what explains it and where)
LEDGER = [
    ("alpha_s", "input 0.1180", "RELATION", "fixes the proton's mass scale exponentially (W4); value unexplained"),
    ("alpha_QED", "input 1/127.930 at M_Z", "MEASURED", "g_X at a gravity fixed point (NOTE_331.md, G1) is a MODEL"),
    ("alpha_W (sin^2 theta_W)", "input 0.23129", "RELATION", "3-3-1 bounds it below 3/4 (W5); value unexplained"),
    ("v (electroweak scale)", "from the measured G_F", "MEASURED", "none"),
    ("lambda (Higgs mass)", "input 125.20 GeV", "CONJECTURE", "lambda(M_Pl) = 0 gives 128.7 GeV (W1); zero quartics fail in 3-3-1 (W2)"),
    ("m_t", "input 172.57 GeV", "CONJECTURE", "with beta_lambda(M_Pl) = 0: 170-174 GeV (W1); asymptotic safety 171 GeV (W3)"),
    ("m_b", "input (threshold)", "RELATION", "3-3-1: y_b = y_t at one vev ratio, a new parameter (W9)"),
    ("m_c", "input (threshold)", "MEASURED", "none"),
    ("m_s", "not used before this script", "MEASURED", "none; enters W7"),
    ("m_d", "input", "MEASURED", "none; enters W7"),
    ("m_u", "input", "MEASURED", "none; m_u = 0 is excluded (W6)"),
    ("m_tau", "input", "EMPIRICAL", "Koide's relation fixes one of the three lepton masses (W8)"),
    ("m_mu", "input", "MEASURED", "none"),
    ("m_e", "input", "MEASURED", "none"),
    ("theta_12 (Cabibbo)", "only |V_ud| is used", "EMPIRICAL", "arctan sqrt(m_d/m_s), 2.8% low, 5 sigma (W7)"),
    ("theta_23", "not used", "MEASURED", "none; 3-3-1's row structure alone gives the wrong pattern (W9)"),
    ("theta_13", "not used", "MEASURED", "none; as theta_23"),
    ("delta_CKM", "not used", "MEASURED", "none"),
    ("theta-bar", "not used", "CONJECTURE", "Peccei-Quinn symmetry in 3-3-1 (W6); needs an axion"),
]
CLASSES = ("MEASURED", "RELATION", "EMPIRICAL", "CONJECTURE")


def tally():
    return {c: sum(1 for r in LEDGER if r[2] == c) for c in CLASSES}


# ------------------------------------------------------------------------------ W1
def mh_from_planck(mt=M_T, a3=ALPHA_S):
    """M_H (GeV) for which the quartic vanishes at M_Pl, from three published NNLO formulas:
    (Shaposhnikov-Wetterich eq. 12, Buttazzo et al. eq. 61e solved for M_h, their eq. 64)."""
    sw = 126.3 + (mt - 171.2) / 2.1 * 4.1 - (a3 - 0.1176) / 0.002 * 1.5
    b61 = 125.15 + (0.0143 + 0.0066 * (mt - 173.34) - 0.0018 * (a3 - 0.1184) / 0.0007) / 0.0029
    b64 = 129.6 + 2.0 * (mt - 173.34) - 0.5 * (a3 - 0.1184) / 0.0007
    return sw, b61, b64


SW_THEORY_ERR = 2.2          # GeV, Shaposhnikov-Wetterich, below their eq. (13)
SW_DMT = 4.1 / 2.1           # d m_min / d m_t, their eq. (12)


def mh_pull():
    """(prediction - measurement)/error for Shaposhnikov-Wetterich's eq. (12), with their
    theory error and the top-mass error in quadrature. The Higgs mass's own error, about
    0.1 GeV (PDG 2024 electroweak review, eq. 10.66), is negligible beside them."""
    sw = mh_from_planck()[0]
    err = sqrt(SW_THEORY_ERR**2 + (SW_DMT * M_T_ERR) ** 2)
    return sw - M_H, err, (sw - M_H) / err


def mt_stability_pull():
    """Buttazzo et al. eq. (66): M_t < 171.53 +- 0.42 GeV, against the measured top mass."""
    return (M_T - 171.53) / hypot(0.42, M_T_ERR)


def sm_start(mh=M_H):
    """MS-bar (g_Y, g_2, g_3, y_t, lambda) at mu = M_t: Buttazzo et al. eqs. (55)-(60), the
    same formulas and inputs as src/m331_scalar.sm_running (pinned in the test)."""
    lam = 0.12604 + 0.00206 * (mh - 125.15) - 0.00004 * (M_T - 173.34)
    yt = 0.93690 + 0.00556 * (M_T - 173.34) - 0.00042 * (ALPHA_S - 0.1184) / 0.0007
    g3 = 1.1666 + 0.00314 * (ALPHA_S - 0.1184) / 0.0007 - 0.00046 * (M_T - 173.34)
    g2 = 0.64779 + 0.00004 * (M_T - 173.34) + 0.00011 * (M_W - 80.384) / 0.014
    g1 = 0.35830 + 0.00011 * (M_T - 173.34) - 0.00020 * (M_W - 80.384) / 0.014
    return [g1, g2, g3, yt, lam]


def mh_of_lambda(lam):
    """Invert the lambda(M_t) formula of sm_start for M_h."""
    return 125.15 + (lam - 0.12604 + 0.00004 * (M_T - 173.34)) / 0.00206


def sm_rhs(t, s):
    """One-loop SM beta functions, t = ln mu (as in src/m331_scalar.sm_running; the quartic's
    is Shaposhnikov-Wetterich eq. (8))."""
    g1, g2, g3, yt, lam = s
    k = 1 / (16 * pi**2)
    return [k * 41 / 6 * g1**3, -k * 19 / 6 * g2**3, -k * 7 * g3**3,
            k * yt * (4.5 * yt**2 - 8 * g3**2 - 9 / 4 * g2**2 - 17 / 12 * g1**2),
            k * (24 * lam**2 - 6 * yt**4 + 12 * lam * yt**2 - 3 * lam * (3 * g2**2 + g1**2)
                 + 3 / 8 * (2 * g2**4 + (g2**2 + g1**2) ** 2))]


def sm_run(s0, mu0, mu1):
    return solve_ivp(sm_rhs, [log(mu0), log(mu1)], s0, rtol=1e-10, atol=1e-12, dense_output=True,
                     max_step=0.2)


_UP = {}


def sm_up():
    """The measured couplings run from M_t to M_Pl at one loop."""
    if "up" not in _UP:
        _UP["up"] = sm_run(sm_start(), M_T, M_PL)
    return _UP["up"]


def mh_one_loop_zero_quartic():
    """One loop: the quartic set to zero at M_Pl, run down to M_t, converted to M_h. (The gauge
    and top couplings do not depend on the quartic at one loop.)"""
    top = sm_up().y[:, -1]
    down = sm_run(list(top[:4]) + [0.0], M_PL, M_T)
    return float(down.y[4, -1]), mh_of_lambda(float(down.y[4, -1]))


def planck_couplings(mt, mh):
    """(g_Y, g_2, y_t, lambda) at M_Pl: Buttazzo et al. eq. (61a,b,d,e), NNLO, linearised in
    M_t, M_h, alpha_s, M_W. Their g_1 is GUT-normalised: g_Y = sqrt(3/5) g_1."""
    a = (ALPHA_S - 0.1184) / 0.0007
    g1 = 0.6154 + 0.0003 * (mt - 173.34) - 0.0006 * (M_W - 80.384) / 0.014
    yt = 0.3825 + 0.0051 * (mt - 173.34) - 0.0021 * a
    lam = -0.0143 - 0.0066 * (mt - 173.34) + 0.0018 * a + 0.0029 * (mh - 125.15)
    return g1 * sqrt(3 / 5), 0.5055, yt, lam


def yt_for_flat_quartic(gY, g2):
    """The top Yukawa at which beta_lambda = 0 when lambda = 0 (one loop, sm_rhs):
    6 y^4 = (3/8)(2 g_2^4 + (g_2^2 + g_Y^2)^2)."""
    return ((2 * g2**4 + (g2**2 + gY**2) ** 2) / 16) ** 0.25


def two_conditions_nnlo():
    """Solve lambda(M_Pl) = 0 and beta_lambda(M_Pl) = 0 for (M_t, M_h) with planck_couplings.
    Returns (M_t, M_h, y_t(M_Pl))."""
    mt = M_T
    for _ in range(60):
        gY, g2, _, _ = planck_couplings(mt, M_H)
        y = yt_for_flat_quartic(gY, g2)
        mt = 173.34 + (y - 0.3825 + 0.0021 * (ALPHA_S - 0.1184) / 0.0007) / 0.0051
    return mt, mh_from_planck(mt)[1], y


def two_conditions_one_loop():
    """The same at one loop throughout: the measured gauge couplings run to M_Pl, y_t(M_Pl) set by
    beta_lambda = 0 at lambda = 0, both run down to M_t. Returns (y_t(M_t), M_t, lambda(M_t), M_h),
    the masses by inverting the formulas of sm_start (M_h at the measured M_t)."""
    top = sm_up().y[:, -1]
    y = yt_for_flat_quartic(top[0], top[1])
    d = sm_run([top[0], top[1], top[2], y, 0.0], M_PL, M_T)
    yt0, lam0 = float(d.y[3, -1]), float(d.y[4, -1])
    mt = 173.34 + (yt0 - 0.93690 + 0.00042 * (ALPHA_S - 0.1184) / 0.0007) / 0.00556
    return yt0, mt, lam0, mh_of_lambda(lam0)


# ------------------------------------------------------------------------------ W2
def quartics_331_from_planck(variant, c2, yJ):
    """All nine 3-3-1 quartics zero at M_Pl, run down to M_V at one loop (two-loop gauge), for a
    top-doublet vev fraction c2 and a common exotic Yukawa yJ at M_V.
    Returns None if the gauge or Yukawa couplings are not perturbative up to M_Pl; otherwise
    (quartics at M_V or None if they diverge on the way down, scale reached)."""
    m = _model(variant)
    ainv, _, _ = Y.boundary(S.MV, lam=tuple(T.lambdas(T.heavy_spectrum(S.NC, variant, S.MV), S.MV)))
    g0 = np.sqrt(4 * pi / np.array(ainv))
    gs, ferm, scal, _ = E.MODELS[variant](S.NC)
    a, b = E.coefficients(gs, ferm, scal)
    a = np.array([float(x) for x in a])
    b = np.array([[float(x) for x in r] for r in b])
    cg, k, K = m.gauge_yukawa_coeffs(), 1 / (16 * pi**2), m.K

    def rhs(t, s):
        g, ys, l = s[:3], s[3:3 + K], s[3 + K:]
        dg = g**3 * k * (a + (b @ g**2 - cg @ ys**2) * k)
        dy = k * ys * (np.concatenate([ys**2, g**2]) @ m.cy)
        return np.concatenate([dg, dy, k * m.beta_l(l, g[0], g[1], ys)])

    def blow(t, s):
        return 4 * pi - np.abs(s[3:]).max()
    blow.terminal = True
    tend = log(M_PL / S.MV)
    yt_sm = float(sm_up().sol(log(S.MV))[3])
    s0 = np.concatenate([g0, [yt_sm / sqrt(c2)] + [yJ] * (K - 1), np.zeros(9)])
    up = solve_ivp(rhs, [0, tend], s0, events=blow, rtol=1e-9, atol=1e-11, max_step=0.5)
    if up.t[-1] < tend - 1e-9:
        return None
    top = up.y[:, -1].copy()
    top[3 + K:] = 0.0
    down = solve_ivp(rhs, [tend, 0], top, events=blow, rtol=1e-9, atol=1e-11, max_step=0.5)
    mu = S.MV * exp(down.t[-1])
    if down.t[-1] > 1e-9:
        return None, mu
    return down.y[3 + K:, -1], mu


_MODELS = {}


def _model(variant):
    if variant not in _MODELS:
        m = S.Model(variant)
        m.cached_fit()
        _MODELS[variant] = m
    return _MODELS[variant]


W2_GRID = [(c2, yJ) for c2 in (0.5, 0.9) for yJ in (0.1, 0.3, 0.5)]


def w2_scan():
    """For each variant and grid point: (c2, yJ, outcome, self-quartic of the triplet without a
    large Yukawa, smallest self-quartic). outcome: 'unbounded' (a self-quartic is negative at
    M_V), 'diverges' (a quartic passes 4 pi before M_V), 'non-perturbative' (the gauge or Yukawa
    couplings do not reach M_Pl), 'bounded' (all three self-quartics positive)."""
    out = {}
    for v in S.VARIANTS:
        other = S.VARIANTS[v]["other"]
        rows = []
        for c2, yJ in W2_GRID:
            r = quartics_331_from_planck(v, c2, yJ)
            if r is None:
                rows.append((c2, yJ, "non-perturbative", None, None))
            elif r[0] is None:
                rows.append((c2, yJ, "diverges", None, r[1]))
            else:
                l = r[0]
                rows.append((c2, yJ, "unbounded" if min(l[:3]) < 0 else "bounded", float(l[other]),
                             float(min(l[:3]))))
        out[v] = rows
    return out


# ------------------------------------------------------------------------------ W3
def top_quasi_fixed_point(y_planck=(1.0, 2.0, 3.0, sqrt(4 * pi))):
    """y_t(M_t) at one loop for a top Yukawa y_planck at M_Pl, with the measured gauge couplings.
    Returns [(y(M_Pl), y(M_t))] and the measured y_t(M_t)."""
    top = sm_up().y[:, -1]
    rows = [(y0, float(sm_run(list(top[:3]) + [y0, 0.0], M_PL, M_T).y[3, -1])) for y0 in y_planck]
    return rows, sm_start()[3]


# ------------------------------------------------------------------------------ W4
def qcd_scale():
    """alpha_3(M_Pl) from Buttazzo et al. eq. (61c); the one-loop, six-flavour scale
    Lambda = M_Pl exp(-2 pi/(7 alpha_3)); d ln Lambda / d ln alpha_3; and Lambda with g_3(M_Pl)
    raised by 10%."""
    g3 = 0.4873 + 0.0002 * (ALPHA_S - 0.1184) / 0.0007
    a3 = g3**2 / (4 * pi)
    lam = lambda a: M_PL * exp(-2 * pi / (7 * a))
    return a3, lam(a3), 2 * pi / (7 * a3), lam(a3 * 1.1**2)


# ------------------------------------------------------------------------------ W5
def s2_bound(beta2):
    """sin^2 theta_W < 1/(1 + beta^2) from 1/g_X^2 = 1/g_Y^2 - beta^2/g^2 > 0 (rung 1's matching;
    src/m331_breaking.py B4), with tan^2 theta_W = g_Y^2/g^2."""
    return 1 / (1 + F(beta2))


# ------------------------------------------------------------------------------ W6
def pq_charges(xd=F(1)):
    """Peccei-Quinn charges q (field -> exp(i alpha q) field) of Dias et al., eqs. (14)-(18),
    with X_d = X_d' = -X_u = -X_u' = -X_e = X_eR = X_nu = -X_nuR (their eq. 17)."""
    xu, xe, xeR, xnu, xnuR = -xd, -xd, xd, xd, -xd
    q = {"uL": -xu, "uR": xu, "dL": -xd, "dR": xd, "u'L": -xu, "u'R": xu, "d'L": -xd, "d'R": xd,
         "eL": xe, "eR": xeR, "nuL": xnu, "nuRc": -xnuR, "phi": -2 * xd}
    q["Q3"] = (q["uL"], q["dL"], q["u'L"])          # triplet (u3, d3, u'3)
    q["Qi"] = (q["dL"], q["uL"], q["d'L"])          # antitriplet (d_i, -u_i, d'_i)
    q["f"] = (q["nuL"], q["eL"], q["nuRc"])         # (nu, e, nu_R^c)
    q["chi"] = (2 * xd, F(0), 2 * xd)               # (chi0, chi-, chi'0)
    q["eta"] = (2 * xd, F(0), 2 * xd)               # (eta0, eta-, eta'0)
    q["rho"] = (F(0), -2 * xd, F(0))                # (rho+, rho0, rho'+)
    return q


# Their eq. (6): (left multiplet, right singlet, scalar, scalar enters conjugated)
YUKAWAS = [("Q3", "u'R", "chi", False), ("Qi", "d'R", "chi", True), ("Q3", "uR", "eta", False),
           ("Qi", "dR", "eta", True), ("Q3", "dR", "rho", False), ("Qi", "uR", "rho", True),
           ("f", "eR", "rho", False)]


def pq_check(xd=F(1), n_c=3):
    """Exact: the net PQ charge of every component of every Yukawa term and of eta rho chi phi
    (all zero if invariant), and the colour anomaly sum over quarks of (q_R - q_L), with
    N_g = N_c families, (N_c + 1)/2 of them antitriplets (one d' each), the rest triplets (one u'
    each)."""
    q = pq_charges(xd)
    terms = [-q[L][k] + q[R] + (-1 if conj else 1) * q[s][k]
             for L, R, s, conj in YUKAWAS for k in range(3)]
    terms += [q["eta"][a] + q["rho"][b] + q["chi"][c] + q["phi"] for a, b, c in permutations(range(3))]
    n_anti = (n_c + 1) // 2
    count = {"u": n_c, "d": n_c, "u'": n_c - n_anti, "d'": n_anti}
    anomaly = sum(n * (q[f + "R"] - q[f + "L"]) for f, n in count.items())
    ordinary = sum(count[f] * (q[f + "R"] - q[f + "L"]) for f in ("u", "d"))
    return terms, anomaly, ordinary


# ------------------------------------------------------------------------------ W7
def gst():
    """arctan sqrt(m_d/m_s) and its error, theta_12 = arcsin(s12) and its error, and the pull."""
    r = M_D / M_S
    th = atan(sqrt(r))
    dth = 0.5 * sqrt(r) / (1 + r) * hypot(M_D_ERR / M_D, M_S_ERR / M_S)
    t12 = asin(S12)
    dt12 = S12_ERR / sqrt(1 - S12**2)
    return th, dth, t12, dt12, (th - t12) / hypot(dth, dt12)


# ------------------------------------------------------------------------------ W8
def koide(masses=None):
    """K = sum m / (sum sqrt m)^2 for the charged leptons (pole masses), and the tau mass (GeV)
    that would make K = 2/3 exactly with the measured m_e and m_mu."""
    me, mmu, mtau = masses or (LL.M_EL, LL.M_MU, LL.M_TAU)
    K = (me + mmu + mtau) / (sqrt(me) + sqrt(mmu) + sqrt(mtau)) ** 2
    # K = 2/3: with s = sqrt(me) + sqrt(mmu), p = me + mmu, x = sqrt(mtau):  x^2 - 4 s x + 3p - 2s^2 = 0
    s, p = sqrt(me) + sqrt(mmu), me + mmu
    x = 2 * s + sqrt(6 * s**2 - 3 * p)
    return K, x**2


# ------------------------------------------------------------------------------ W9
def tan_b_equal_tb():
    """F2: the vev ratio v_eta/v_rho at which the top and bottom Yukawas are equal, and the six
    3-3-1 quark Yukawas there. Up-type: t from v_eta, u and c from v_rho; down-type: b from v_rho,
    d and s from v_eta (F1). SM Yukawa y means mass = y v/sqrt2 with v^2 = v_eta^2 + v_rho^2."""
    tb = YUK_MZ["t"] / YUK_MZ["b"]
    sb, cb = tb / sqrt(1 + tb**2), 1 / sqrt(1 + tb**2)
    y = {q: YUK_MZ[q] / (sb if q in "tds" else cb) for q in YUK_MZ}
    return tb, y


def yukawa_spread(y):
    return max(y.values()) / min(y.values())


def anarchy(tb, n=4000, seed=7):
    """F3: n draws of complex Gaussian Yukawa matrices with the row structure of F1 at vev ratio tb.
    Returns the medians of |V_tb|, |V_us|, |V_cb| (mass-ordered) and the fraction with |V_tb| > 0.9."""
    rng = np.random.default_rng(seed)
    sb, cb = tb / sqrt(1 + tb**2), 1 / sqrt(1 + tb**2)
    Du, Dd = np.diag([cb, cb, sb]), np.diag([sb, sb, cb])
    out = np.empty((n, 3))
    for i in range(n):
        G = rng.normal(size=(2, 3, 3)) + 1j * rng.normal(size=(2, 3, 3))
        Uu, su, _ = np.linalg.svd(Du @ G[0])
        Ud, sd, _ = np.linalg.svd(Dd @ G[1])
        V = np.abs(Uu[:, ::-1].conj().T @ Ud[:, ::-1])          # rows u, c, t; columns d, s, b
        out[i] = V[2, 2], V[0, 1], V[1, 2]
    med = np.median(out, axis=0)
    return float(med[0]), float(med[1]), float(med[2]), float((out[:, 0] > 0.9).mean())


def rho_from_flavour(tb, variant="-1/sqrt3"):
    """F4: rho - 1 = (v/w)^2 (sin^2 a - sin^2 a0)^2 (src/m331_rho_bound.py R1) at the LHC bound on w,
    with tan a = v_2/v_1 = v_eta/v_rho = tb (for beta = -1/sqrt3, v_1 sits in the X = 2/3 triplet,
    rho, and v_2 in an X = -1/3 triplet, eta: results/m331/331_rho_bound.txt, R1)."""
    w = RB.w_from_zprime(variant)[0]
    s2a = tb**2 / (1 + tb**2)
    return (RB.v_ew() / w) ** 2 * (s2a - RB.sin2_a0(variant)) ** 2, w


def main():
    banner("W0  The ledger: 19 parameters (LIT: Kronfeld, arXiv:1007.1444, section 5)")
    for name, status, cls, why in LEDGER:
        print(f"   {name:24s} {cls:10s} {status:28s} {why}")

    banner("W1  The Higgs mass from lambda(M_Pl) = 0 (CONJECTURE: asymptotic safety, no new scale)")
    sw, b61, b64 = mh_from_planck()
    d, err, pull = mh_pull()
    lam0, mh1 = mh_one_loop_zero_quartic()
    print(f"   inputs: M_t = {M_T} +- {M_T_ERR} GeV, alpha_s = {ALPHA_S}; measured M_H = {M_H} GeV")
    print(f"   Shaposhnikov-Wetterich eq. (12):          {sw:.1f} GeV (theory +- {SW_THEORY_ERR})")
    print(f"   Buttazzo et al. eq. (61e), lambda(M_Pl)=0: {b61:.1f} GeV")
    print(f"   Buttazzo et al. eq. (64), stability:       {b64:.1f} GeV")
    print(f"   prediction - measurement = {d:+.1f} GeV = {d / M_H:+.1%}; error {err:.1f} GeV; pull {pull:+.1f} sigma")
    print(f"   read the other way, eq. (66): M_t < 171.53 +- 0.42 GeV; measured {M_T}: {mt_stability_pull():+.1f} sigma")
    print(f"   one-loop cross-check (CHECK): lambda(M_t) = {lam0:.4f} -> M_H = {mh1:.1f} GeV;"
          f" one loop is {mh1 - b61:+.1f} GeV from NNLO")
    print(f"   measured couplings at M_Pl, one loop: lambda = {sm_up().y[4, -1]:+.4f} (NNLO, eq. 61e: "
          f"{-0.0143 - 0.0066 * (M_T - 173.34) + 0.0018 * (ALPHA_S - 0.1184) / 0.0007 + 0.0029 * (M_H - 125.15):+.4f})")

    mt2, mh2, y2 = two_conditions_nnlo()
    yt1, mt1, lam1, mh1b = two_conditions_one_loop()
    print("   two conditions, lambda(M_Pl) = 0 and beta_lambda(M_Pl) = 0, solved for M_t and M_H together:")
    print(f"     NNLO couplings at M_Pl (eq. 61): y_t(M_Pl) = {y2:.4f} -> M_t = {mt2:.1f} GeV ({mt2 / M_T - 1:+.1%}),"
          f" M_H = {mh2:.1f} GeV ({mh2 / M_H - 1:+.1%})")
    print(f"     one loop throughout:             y_t(M_t) = {yt1:.4f} -> M_t = {mt1:.1f} GeV ({mt1 / M_T - 1:+.1%}),"
          f" M_H = {mh1b:.1f} GeV ({mh1b / M_H - 1:+.1%})")
    print("     the spread between the two lines is the size of the method's error")

    banner("W2  The same condition with the 3-3-1 scalars (MODEL, one loop, M_V = 4 TeV)")
    print("   all nine quartics zero at M_Pl, run down to M_V; c^2 = top-doublet vev fraction")
    for v, rows in w2_scan().items():
        for c2, yJ, outcome, l_other, l_min in rows:
            tail = ("" if l_other is None and l_min is None else
                    f"; a quartic passes 4 pi at {l_min:.1e} GeV, above M_V" if l_other is None else
                    f"; self-quartic of the triplet without a large Yukawa = {l_other:+.3f}")
            print(f"   beta = {v}, c^2 = {c2}, y_J = {yJ}: {outcome}{tail}")
    print("   A negative self-quartic l_i (Phi_i+ Phi_i)^2 makes the potential unbounded below along Phi_i.")

    banner("W3  The top mass")
    rows, y_meas = top_quasi_fixed_point()
    for y0, y in rows:
        print(f"   y_t(M_Pl) = {y0:.2f} -> y_t(M_t) = {y:.3f}  ({y / y_meas - 1:+.0%} against the measured {y_meas:.4f})")
    print(f"   quasi-fixed point (RELATION): y_t(M_t) <= {rows[-1][1]:.3f}; a factor {rows[-1][0] / rows[0][0]:.1f} in y_t(M_Pl)"
          f" is focused to {rows[-1][1] / rows[0][1] - 1:.1%}")
    print(f"   asymptotic safety (CONJECTURE; LIT Eichhorn-Held): M_t,pole ~ 171 GeV; measured {M_T} +- {M_T_ERR}"
          f" ({171 / M_T - 1:+.1%}; no error is quoted)")

    banner("W4  The strong coupling and the proton's mass scale (RELATION)")
    a3, lam, sens, lam10 = qcd_scale()
    print(f"   alpha_3(M_Pl) = {a3:.4f} = 1/{1 / a3:.1f} (LIT: Buttazzo et al. eq. 61c)")
    print(f"   one loop, six flavours: Lambda = M_Pl exp(-2 pi/(7 alpha_3)) = {lam:.3f} GeV = {lam / M_PL:.1e} M_Pl")
    print(f"   d ln Lambda / d ln alpha_3 = {sens:.1f}; with g_3(M_Pl) 10% larger, Lambda = {lam10:.0f} GeV")

    banner("W5  The weak mixing angle in 3-3-1 (RELATION: a bound)")
    print(f"   sin^2 theta_W < 1/(1 + beta^2) = {s2_bound(F(1, 3))} for beta = +-1/sqrt3; measured {E.s2} at M_Z")
    print(f"   (the same formula gives {s2_bound(3)} for beta = sqrt3, a variant this repository does not use)")

    banner("W6  The strong CP angle (CONJECTURE: Peccei-Quinn in 3-3-1; LIT Dias et al.)")
    terms, anomaly, ordinary = pq_check()
    print(f"   {len(terms)} components of the 7 Yukawa terms and of eta rho chi phi: all invariant: {all(t == 0 for t in terms)}")
    print(f"   colour anomaly, sum over quarks of (q_R - q_L): {anomaly} X_d  (u and d alone: {ordinary});"
          f" for N_c = 5, 7: {pq_check(n_c=5)[1]}, {pq_check(n_c=7)[1]}")
    print("   non-zero, so theta-bar can be rotated away; the price is an axion, which is not observed")

    banner("W7  The Cabibbo angle (EMPIRICAL: Gatto-Sartori-Tonin)")
    th, dth, t12, dt12, pull = gst()
    print(f"   arctan sqrt(m_d/m_s) = {th:.4f} +- {dth:.4f}  (m_d = {M_D} +- {M_D_ERR}, m_s = {M_S} +- {M_S_ERR} MeV)")
    print(f"   theta_12 = arcsin({S12}) = {t12:.4f} +- {dt12:.4f};  difference {th / t12 - 1:+.1%}, {pull:+.1f} sigma")
    print(f"   (LIT, Antusch et al. eq. 4.11, from running Yukawas: {GST_LIT[0]} +- {GST_LIT[1]}; 'the uncertainty")
    print("    intervals only overlap at the 3 sigma level')")

    banner("W8  The charged-lepton masses (EMPIRICAL: Koide)")
    K, mtau = koide()
    print(f"   K = {K:.7f};  K/(2/3) - 1 = {K / (2 / 3) - 1:+.1e}")
    print(f"   K = 2/3 exactly needs m_tau = {mtau * 1e3:.2f} MeV; measured {LL.M_TAU * 1e3:.2f} MeV ({mtau / LL.M_TAU - 1:+.1e})")

    banner("W9  Quark flavour in 3-3-1 (beta = -1/sqrt3; LIT Dias et al. eq. 6, Antusch et al. eq. 2.4)")
    print("   F1  up-type mass rows (v_rho, v_rho, v_eta); down-type rows (v_eta, v_eta, v_rho): the triplet")
    print("       family's up quark and the antitriplet families' down quarks take the same vev")
    tb, y = tan_b_equal_tb()
    print(f"   F2  y_t = y_b at tan b = v_eta/v_rho = {tb:.1f}; the 3-3-1 Yukawas there:")
    print("       " + ", ".join(f"y_{q} = {y[q]:.2e}" for q in "tbcsud"))
    print(f"       largest/smallest Yukawa: {yukawa_spread(YUK_MZ):.2e} in the Standard Model, {yukawa_spread(y):.2e} here;"
          f" y_c/y_t = {y['c'] / y['t']:.2f}")
    print("       tan b is a new parameter: it is traded for m_b/m_t, not derived")
    for t in (1.0, tb):
        vtb, vus, vcb, frac = anarchy(t)
        print(f"   F3  random O(1) Yukawas, tan b = {t:.1f}: median |V_tb| = {vtb:.2f}, |V_us| = {vus:.2f}, |V_cb| = {vcb:.2f};"
              f" |V_tb| > 0.9 in {frac:.1%} of draws")
    print(f"       measured: |V_tb| = {V_TB:.3f}, |V_us| = {V_US:.3f}, |V_cb| = {V_CB:.3f} (PDG 2024 CKM review, eq. 12.27)")
    for t in (1.0, tb):
        r, w = rho_from_flavour(t)
        print(f"   F4  tan b = {t:.1f}: rho - 1 = {r:.2e} at w = {w / 1e3:.1f} TeV (the LHC bound);"
              f" global fit rho_0 - 1 = {RB.RHO0 - 1:.2e} +- {RB.RHO0_ERR:.1e}: {(r - (RB.RHO0 - 1)) / RB.RHO0_ERR:+.1f} sigma")
    print("   F5  (LIT Buras et al.) the third family's different Z' coupling makes the left-handed rotations")
    print("       physical: four new mixing parameters, and flavour change at tree level through the Z'")

    banner("W10 The tally")
    t = tally()
    print("   " + ", ".join(f"{c}: {t[c]}" for c in CLASSES) + f"  (of {len(LEDGER)})")
    print("   No parameter's value is derived. Established physics gives relations for "
          f"{t['RELATION']}; {t['EMPIRICAL']} have a numerical regularity;")
    print(f"   {t['CONJECTURE']} have a conjectured explanation; {t['MEASURED']} have none.")


if __name__ == "__main__":
    main()
