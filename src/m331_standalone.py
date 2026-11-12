#!/usr/bin/env python3
"""
Three colours and three generations from perturbativity in 3-3-1 models.
A single-file, standard-library-only reproduction of the selection N_c = N_g = 3.

HOW TO RUN
    Paste this whole file into any Python 3.8+ runner (a terminal, an online
    interpreter, Jupyter, Pyodide, or an AI assistant's code tool) and run it.
    No packages to install: it uses only the Python standard library.
    It runs in roughly 10-60 seconds, depending on the machine; set FULL_SCAN = False
    below for a run of a few seconds that skips the threshold-spectrum scan.

FOR AI ASSISTANTS
    Execute the file as-is and report the printed results. Every section ends with
    PASS/FAIL checks against the numbers pinned in the source repository, and the last
    lines give the overall verdict. Explain the physics from the section headers and the
    comments; do not change the inputs unless the user asks to.

WHAT IT COMPUTES
    Model: SU(N_c)_C x SU(3)_L x U(1)_X with Q = T3 + beta T8 + X, beta = -1/sqrt3 or
    +1/sqrt3, N_g generations, n of the quark generations in the SU(3)_L anti-triplet.
    The number of colours N_c is kept general; nothing about generations or neutrinos is
    taken from experiment. The one added requirement: every gauge coupling stays
    perturbative (g < 4 pi) up to the Planck scale, 1.22e19 GeV.

      S1  Charges for general N_c from anomaly cancellation; all gauge anomalies vanish.
      S2  SU(3)_L anomaly + asymptotic freedom of colour  =>  N_c odd and N_g = N_c.
      S3  Calibration: the two-loop machinery reproduces the Standard Model coefficients.
      S4  SU(3)_L one-loop running excludes N_c >= 7.
      S5  U(1)_X two-loop running excludes N_c = 5, in both variants, with Yukawas.
      S6  One-loop threshold matching at the 3-3-1 scale, scanning the heavy spectrum.
      S6b The beta = +1/sqrt3 variant against mass floors at alpha = 1: a condition on
          the heavy-lepton mass.
      S7  Cross-check with data: R = sigma(ee -> hadrons)/sigma(ee -> mu mu) vs KEDR.

    Result (conditional on the 3-3-1 framework, Planck-scale perturbativity, and the
    measured electroweak couplings at the TeV scale used as input): only N_c = N_g = 3
    survives, with quark charges 2/3 and -1/3. In the beta = +1/sqrt3 variant this also
    needs the three heavy charged leptons heavy enough (S6b).

SOURCE
    Repository: https://github.com/sheldonlindberg-afk/STUR-Physics-Lab
    Note:       paper/note331.pdf  (extended notes: NOTE_331.md)
    This file condenses src/m331_exact.py, m331_three_generations.py, m331_closure.py,
    m331_su3L_running.py, m331_yukawa.py, m331_threshold.py, m331_margin.py,
    m331_why_three.py and qcd_running.py; tests/test_331_standalone.py checks that it agrees with them.
    Independent work, not peer reviewed. License: CC0 1.0 (public domain).
"""
from fractions import Fraction as F
from itertools import product
from math import exp, gcd, log, pi, sqrt
import time

FULL_SCAN = True          # S6: scan the whole heavy spectrum (False: only its two extremes)

# ----------------------------------------------------------------------------------------
# Inputs (PDG; MS-bar at M_Z)
# ----------------------------------------------------------------------------------------
MZ = 91.1876              # GeV
AINV_MZ = 127.95          # 1/alpha_em(M_Z)
S2_MZ = 0.23122           # sin^2 theta_W(M_Z)
ALPHA_S_MZ = 0.1180
QUARK_THRESHOLDS = (1.27, 4.18, 172.69)    # m_c, m_b, m_t for alpha_s flavour matching
MT_POLE = 172.57
V_EW = 246.22
M_PLANCK = 1.22089e19     # GeV
MU331 = 4e3               # reference 3-3-1 scale, GeV
VARIANTS = ("-1/sqrt3", "+1/sqrt3")

CHECKS = []               # (label, passed)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def check(label, ok):
    CHECKS.append((label, bool(ok)))
    print(f"   [{'PASS' if ok else 'FAIL'}] {label}")


def close(x, ref, rel=0.03):
    return abs(x / ref - 1) < rel


# ----------------------------------------------------------------------------------------
# A small ODE integrator (classical RK4 with step control and event location),
# replacing scipy's solve_ivp so the file needs nothing beyond the standard library.
# ----------------------------------------------------------------------------------------
def _rk4(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + h / 2, [a + h / 2 * b for a, b in zip(y, k1)])
    k3 = f(t + h / 2, [a + h / 2 * b for a, b in zip(y, k2)])
    k4 = f(t + h, [a + h * b for a, b in zip(y, k3)])
    return [a + h / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(y, k1, k2, k3, k4)]


def integrate(f, t0, t1, y0, hmax=0.1, rel=0.002, stop=None):
    """Integrate dy/dt = f(t, y) from t0 to t1 (either direction).
    Steps are capped so no component changes by more than `rel` of itself per step.
    If stop(y) > 0 is given, return (t_event, y) at the first crossing, else (None, y)."""
    t, y = t0, list(y0)
    sgn = 1 if t1 >= t0 else -1
    while sgn * (t1 - t) > 1e-14:
        d = f(t, y)
        h = hmax
        for a, b in zip(y, d):
            if b != 0 and a != 0:
                h = min(h, rel * abs(a / b))
        h = sgn * min(h, abs(t1 - t))
        yn = _rk4(f, t, y, h)
        if stop is not None and stop(yn) > 0:
            lo, hi = 0.0, h                       # bisect the step to locate the event
            for _ in range(60):
                mid = (lo + hi) / 2
                if stop(_rk4(f, t, y, mid)) > 0:
                    hi = mid
                else:
                    lo = mid
            return t + hi, _rk4(f, t, y, hi)
        t, y = t + h, yn
    return None, y


def bisect(f, a, b, tol=1e-7):
    fa = f(a)
    for _ in range(200):
        m = (a + b) / 2
        fm = f(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
        if b - a < tol:
            break
    return (a + b) / 2


# ----------------------------------------------------------------------------------------
# QCD: two-loop MS-bar running of alpha_s with flavour thresholds
# ----------------------------------------------------------------------------------------
def _nf(mu):
    return 3 + sum(mu > m for m in QUARK_THRESHOLDS)


def _as_rhs(lnmu2, y):
    n = _nf(exp(lnmu2 / 2))
    b0, b1 = 11 - 2 * n / 3, 102 - 38 * n / 3
    a = y[0]
    return [-(b0 / (4 * pi)) * a**2 - (b1 / (16 * pi**2)) * a**3]


_AS_CACHE = {}


def alpha_s(mu):
    if mu not in _AS_CACHE:
        # integrate piecewise so each segment has a fixed number of flavours
        pts = sorted({MZ, mu} | {m for m in QUARK_THRESHOLDS if min(MZ, mu) < m < max(MZ, mu)},
                     reverse=mu < MZ)
        y = [ALPHA_S_MZ]
        for p, q in zip(pts, pts[1:]):
            lnmid2 = 2 * log(sqrt(p * q))                    # nf fixed on each segment
            f = lambda t, yy, c=lnmid2: _as_rhs(c, yy)
            _, y = integrate(f, 2 * log(p), 2 * log(q), y, hmax=0.05)
        _AS_CACHE[mu] = y[0]
    return _AS_CACHE[mu]


# ----------------------------------------------------------------------------------------
# Group theory and the general one- and two-loop gauge beta functions
# ----------------------------------------------------------------------------------------
class Group:
    def __init__(self, name, N=None):            # N = None -> U(1)
        self.name, self.N = name, N

    def CA(self):
        return 0 if self.N is None else self.N

    def T(self, d):                              # Dynkin index of the irrep of dimension d
        if self.N is None or d == 1:
            return 0
        if d == self.N:
            return F(1, 2)
        if self.N == 3 and d == 6:
            return F(5, 2)
        raise ValueError(d)

    def C2(self, d, charge=None):                # quadratic Casimir
        if self.N is None:
            return charge**2
        if d == 1:
            return 0
        if d == self.N:
            return F(self.N**2 - 1, 2 * self.N)
        raise ValueError(d)


def coefficients(groups, fermions, scalars, kappa=F(1, 2), sigma=F(2)):
    """Fields: (multiplicity, dims tuple with None in the U(1) slot, U(1) charge).
    Fermions are left-handed Weyl (kappa = 1/2), scalars complex (sigma = 2).
    Returns exact a_i, b_ij for dg_i/dt = g_i^3/(16 pi^2) [a_i + sum_j b_ij g_j^2/(16 pi^2)]."""
    n = len(groups)

    def S(i, mult, dims, q):
        other = 1
        for j, d in enumerate(dims):
            if j != i and d is not None:
                other *= d
        g = groups[i]
        return mult * other * (q**2 if g.N is None else g.T(dims[i]))

    def C(j, dims, q):
        g = groups[j]
        return g.C2(dims[j], q) if g.N is not None else q**2

    a = [F(0)] * n
    b = [[F(0)] * n for _ in range(n)]
    for i, g in enumerate(groups):
        a[i] = -F(11, 3) * g.CA()
        b[i][i] = -F(34, 3) * g.CA()**2
        for mult, dims, q in fermions:
            s = S(i, mult, dims, q)
            a[i] += F(4, 3) * kappa * s
            b[i][i] += kappa * F(20, 3) * g.CA() * s
            for j in range(n):
                b[i][j] += kappa * 4 * s * C(j, dims, q)
        for mult, dims, q in scalars:
            s = S(i, mult, dims, q)
            a[i] += F(1, 3) * s
            b[i][i] += sigma * F(1, 3) * g.CA() * s
            for j in range(n):
                b[i][j] += sigma * 2 * s * C(j, dims, q)
    return a, b


def yukawa_coeff(groups, psi1, psi2, n_terms):
    """Two-loop Yukawa term per y^2: n_terms [C2(psi1) + C2(psi2)] / d(G) for each group."""
    out = []
    for i, g in enumerate(groups):
        dG = 1 if g.N is None else g.N**2 - 1
        s = sum(q**2 if g.N is None else g.C2(dims[i]) for dims, q in (psi1, psi2))
        out.append(F(n_terms) * s / dG)
    return out


# ----------------------------------------------------------------------------------------
# The 3-3-1 models for general N_c (groups ordered X, SU(3)_L, SU(N_c))
# ----------------------------------------------------------------------------------------
def charges(Nc):
    """Quark charges fixed by anomaly cancellation with Yukawas, for general N_c."""
    return F(Nc + 1, 2 * Nc), F(1 - Nc, 2 * Nc)


def model(Nc, variant):
    Qu, Qd = charges(Nc)
    Ng, nA = Nc, (1 + Nc) // 2               # N_g = N_c (S2); n anti-triplet generations
    gs = [Group("X"), Group("SU3L", 3), Group("SUNc", Nc)]
    if variant == "-1/sqrt3":
        # leptons (nu, e, N) X = -1/3; quark triplet (u, d, T) X = Q_u - 1/3;
        # anti-triplet (d, -u, D) X = Q_d + 1/3; scalars eta, rho, chi X = -1/3, 2/3, -1/3
        Xt, Xa = Qu - F(1, 3), Qd + F(1, 3)
        ferm = [(Ng, (None, 3, 1), F(-1, 3)), (Ng, (None, 1, 1), F(1)),
                (Ng - nA, (None, 3, Nc), Xt), (nA, (None, 3, Nc), Xa),
                (Ng, (None, 1, Nc), -Qu), (Ng, (None, 1, Nc), -Qd),
                (Ng - nA, (None, 1, Nc), -Qu), (nA, (None, 1, Nc), -Qd)]
        scal = [(1, (None, 3, 1), F(-1, 3)), (1, (None, 3, 1), F(2, 3)), (1, (None, 3, 1), F(-1, 3))]
    else:
        # leptons (nu, e, E-) X = -2/3 with a heavy charged lepton E; quark triplet (u, d, J)
        # X = Q_u - 2/3 (J d-like); anti-triplet (d, -u, J') X = Q_d + 2/3 (J' u-like);
        # scalars X = 1/3, 1/3, -2/3
        Xt, Xa = Qu - F(2, 3), Qd + F(2, 3)
        ferm = [(Ng, (None, 3, 1), F(-2, 3)), (Ng, (None, 1, 1), F(1)), (Ng, (None, 1, 1), F(1)),
                (Ng - nA, (None, 3, Nc), Xt), (nA, (None, 3, Nc), Xa),
                (Ng, (None, 1, Nc), -Qu), (Ng, (None, 1, Nc), -Qd),
                (Ng - nA, (None, 1, Nc), -Qd), (nA, (None, 1, Nc), -Qu)]
        scal = [(1, (None, 3, 1), F(1, 3)), (1, (None, 3, 1), F(1, 3)), (1, (None, 3, 1), F(-2, 3))]
    return gs, ferm, scal, (Xt, Xa, Qu, Qd, Ng, nA)


def anomalies(Nc, variant):
    gs, ferm, scal, (Xt, Xa, Qu, Qd, Ng, nA) = model(Nc, variant)
    dim = lambda d: d[1] * d[2]
    return {
        "X^3": sum(m * dim(d) * q**3 for m, d, q in ferm),
        "grav^2 X": sum(m * dim(d) * q for m, d, q in ferm),
        "SU3L^2 X": sum(m * d[2] * q for m, d, q in ferm if d[1] == 3),
        "SUNc^2 X": sum(m * d[1] * q for m, d, q in ferm if d[2] == Nc),
        "SU3L^3": F(Ng + Nc * (Ng - nA) - Nc * nA),       # triplets minus anti-triplets
    }


def yukawas_331(Nc, variant):
    """Two-loop Yukawa coefficient vectors (top quark; all exotic fermions at one common y_J)."""
    gs, ferm, scal, (Xt, Xa, Qu, Qd, Ng, nA) = model(Nc, variant)
    nt = 3 * Nc
    top = yukawa_coeff(gs, ((None, 3, Nc), Xt), ((None, 1, Nc), -Qu), nt)
    if variant == "-1/sqrt3":
        ex_t = yukawa_coeff(gs, ((None, 3, Nc), Xt), ((None, 1, Nc), -Qu), nt)
        ex_a = yukawa_coeff(gs, ((None, 3, Nc), Xa), ((None, 1, Nc), -Qd), nt)
    else:
        ex_t = yukawa_coeff(gs, ((None, 3, Nc), Xt), ((None, 1, Nc), -Qd), nt)
        ex_a = yukawa_coeff(gs, ((None, 3, Nc), Xa), ((None, 1, Nc), -Qu), nt)
    exotic = [(Ng - nA) * x + nA * y for x, y in zip(ex_t, ex_a)]
    if variant == "+1/sqrt3":                              # heavy charged leptons
        lep = yukawa_coeff(gs, ((None, 3, 1), F(-2, 3)), ((None, 1, 1), F(1)), 3)
        exotic = [x + Ng * l for x, l in zip(exotic, lep)]
    return [float(x) for x in top], [float(x) for x in exotic]


# ----------------------------------------------------------------------------------------
# Boundary conditions at the 3-3-1 scale and the running to the blow-up
# ----------------------------------------------------------------------------------------
_YT_CACHE = {}


def yt_at(mu):
    """SM top Yukawa run (one loop, with the gauge couplings) from m_t to mu."""
    if mu not in _YT_CACHE:
        as_mt = alpha_s(MT_POLE)
        y0 = sqrt(2) * MT_POLE * (1 - 4 * as_mt / (3 * pi)) / V_EW

        def rhs(t, v):
            y, a3 = v
            m = MT_POLE * exp(t)
            L = log(m / MZ) / (2 * pi)
            a1 = 1 / ((1 - S2_MZ) * AINV_MZ * 3 / 5 - 41 / 10 * L)
            a2 = 1 / (S2_MZ * AINV_MZ + 19 / 6 * L)
            g1s, g2s, g3s = 4 * pi * a1, 4 * pi * a2, 4 * pi * a3
            dy = y / (16 * pi**2) * (4.5 * y**2 - 17 / 20 * g1s - 9 / 4 * g2s - 8 * g3s)
            return [dy, 2 * _as_rhs(2 * log(m), [a3])[0]]
        _, v = integrate(rhs, 0.0, log(mu / MT_POLE), [y0, as_mt], hmax=0.05)
        _YT_CACHE[mu] = v[0]
    return _YT_CACHE[mu]


def boundary(mu0, lam=(0.0, 0.0, 0.0), n_light=1, s2=None):
    """(1/alpha_X, 1/alpha_L, 1/alpha_3) at mu0 from one-loop SM running of the measured
    couplings; tree-level matching 1/alpha_Y = 1/alpha_X + beta^2/alpha_L (beta^2 = 1/3),
    plus one-loop thresholds lam. n_light: Higgs doublets below mu0. s2: impose a weak
    mixing angle at mu0 with alpha_em fixed (to measure the margin)."""
    L0 = log(mu0 / MZ) / (2 * pi)
    extra = (n_light - 1) / 6
    aY = (1 - S2_MZ) * AINV_MZ - (41 / 6 + extra) * L0
    a2 = S2_MZ * AINV_MZ + (19 / 6 - extra) * L0
    if s2 is not None:
        aem = aY + a2
        a2, aY = s2 * aem, (1 - s2) * aem
    aY += lam[0] / (12 * pi)
    a2 += lam[1] / (12 * pi)
    a3 = 1 / alpha_s(mu0) + lam[2] / (12 * pi)
    return [aY - a2 / 3, a2, a3]


def blow_up(Nc, variant, yt=0.0, yJ=0.0, mu0=MU331, gmax=4 * pi, lam=(0.0, 0.0, 0.0),
            n_light=1, loops=2, s2=None, yuk=None):
    """Scale (GeV) where the first gauge coupling reaches gmax; 1e45 if none below 1e45 GeV.
    yuk: an explicit two-loop Yukawa vector, overriding the one built from yt and yJ (S6b)."""
    gs, ferm, scal, _ = model(Nc, variant)
    a, b = coefficients(gs, ferm, scal)
    a = [float(x) for x in a]
    b = [[float(x) for x in r] for r in b] if loops == 2 else [[0.0] * 3 for _ in range(3)]
    ct, cJ = yukawas_331(Nc, variant)
    if yuk is None:
        yuk = [ct[i] * yt**2 + cJ[i] * yJ**2 for i in range(3)]
    yuk = [x if loops == 2 else 0.0 for x in yuk]
    ainv0 = boundary(mu0, lam, n_light, s2)
    if min(ainv0) <= 0:
        return mu0
    g0 = [sqrt(4 * pi / x) for x in ainv0]
    k = 16 * pi**2

    def rhs(t, g):
        g2 = [x * x for x in g]
        return [g[i]**3 / k * (a[i] + (sum(b[i][j] * g2[j] for j in range(3)) - yuk[i]) / k)
                for i in range(3)]
    te, _ = integrate(rhs, 0.0, log(1e45 / mu0), g0, hmax=0.25, stop=lambda g: max(g) - gmax)
    return mu0 * exp(te) if te is not None else 1e45


def fmt(x):
    return "none below 1e45" if x >= 1e45 else f"{x:.2e} GeV"


# ----------------------------------------------------------------------------------------
# S1  Charges and anomalies
# ----------------------------------------------------------------------------------------
def s1():
    banner("S1  Charges for general N_c, and every gauge anomaly")
    print("   Anomaly cancellation with Yukawas fixes Q_u = (N_c + 1)/(2 N_c), Q_d = (1 - N_c)/(2 N_c):")
    for Nc in (3, 5, 7):
        Qu, Qd = charges(Nc)
        print(f"     N_c = {Nc}: Q_u = {Qu}, Q_d = {Qd}")
    ok = True
    for v in VARIANTS:
        for Nc in (3, 5, 7, 9):
            A = anomalies(Nc, v)
            ok &= all(x == 0 for x in A.values())
        print(f"   beta = {v}: X^3, grav^2 X, SU3L^2 X, SUNc^2 X, SU3L^3 all vanish for N_c = 3, 5, 7, 9")
    print("   -> perturbative anomalies fix the CHARGES given N_c, but not N_c itself.")
    check("Q_u, Q_d = 2/3, -1/3 at N_c = 3", charges(3) == (F(2, 3), F(-1, 3)))
    check("all gauge anomalies vanish exactly, both variants, N_c = 3..9", ok)


# ----------------------------------------------------------------------------------------
# S2  N_c odd and N_g = N_c
# ----------------------------------------------------------------------------------------
def s2():
    banner("S2  SU(3)_L anomaly + asymptotic freedom of colour  =>  N_c odd, N_g = N_c")
    print("   SU(3)_L anomaly: #triplets = #anti-triplets  ->  N_g (1 + N_c) = 2 n N_c")
    print("   Asymptotic freedom with 3 N_g quark flavours: 11 N_c - 6 N_g > 0")
    sol = []
    for Nc in range(2, 61):
        for Ng in range(1, 401):
            if 11 * Nc - 6 * Ng <= 0:
                break
            if (Ng * (1 + Nc)) % (2 * Nc) == 0 and 0 <= Ng * (1 + Nc) // (2 * Nc) <= Ng:
                sol.append((Nc, Ng, Ng * (1 + Nc) // (2 * Nc)))
    print(f"   All solutions for 2 <= N_c <= 60: {len(sol)}; first: "
          + ", ".join(f"(N_c={a}, N_g={b}, n={c})" for a, b, c in sol[:4]) + ", ...")
    print("   Proof: if N_c is odd, gcd(N_c + 1, 2 N_c) = 2, so N_c | N_g, and N_g < 11 N_c/6 leaves")
    print("   N_g = N_c. If N_c is even, gcd = 1, so 2 N_c | N_g, which violates asymptotic freedom.")
    print("   SU(2) doublets then number 2 n N_c, always even: Witten's anomaly is automatic.")
    check("every solution has N_c odd and N_g = N_c (29 solutions)",
          len(sol) == 29 and all(a == b and a % 2 == 1 for a, b, c in sol))
    check("gcd(N_c + 1, 2 N_c) = 2 for odd, 1 for even N_c",
          all(gcd(k + 1, 2 * k) == (2 if k % 2 else 1) for k in range(2, 60)))


# ----------------------------------------------------------------------------------------
# S3  Calibration on the Standard Model
# ----------------------------------------------------------------------------------------
def s3():
    banner("S3  Calibration: the general machinery reproduces the Standard Model")
    gs = [Group("Y"), Group("SU2", 2), Group("SU3", 3)]
    ferm = []
    for _ in range(3):
        ferm += [(1, (None, 2, 3), F(1, 6)), (1, (None, 1, 3), F(-2, 3)), (1, (None, 1, 3), F(1, 3)),
                 (1, (None, 2, 1), F(-1, 2)), (1, (None, 1, 1), F(1))]
    a, b = coefficients(gs, ferm, [(1, (None, 2, 1), F(1, 2))])
    r = F(3, 5)                                            # GUT normalisation g1^2 = (5/3) g_Y^2
    a = [a[0] * r, a[1], a[2]]
    b = [[b[0][0] * r * r, b[0][1] * r, b[0][2] * r], [b[1][0] * r, b[1][1], b[1][2]],
         [b[2][0] * r, b[2][1], b[2][2]]]
    print("   one-loop a =", [str(x) for x in a])
    for row in b:
        print("   two-loop b =", [str(x) for x in row])
    top = yukawa_coeff(gs, ((None, 2, 3), F(1, 6)), ((None, 1, 3), F(-2, 3)), 6)
    top = [top[0] * r, top[1], top[2]]
    print("   top Yukawa two-loop coefficients =", [str(x) for x in top])
    check("SM one-loop (41/10, -19/6, -7)", a == [F(41, 10), F(-19, 6), F(-7)])
    check("all nine SM two-loop coefficients",
          b == [[F(199, 50), F(27, 10), F(44, 5)], [F(9, 10), F(35, 6), F(12)], [F(11, 10), F(9, 2), F(-26)]])
    check("SM top-Yukawa coefficients (17/10, 3/2, 2)", top == [F(17, 10), F(3, 2), F(2)])


# ----------------------------------------------------------------------------------------
# S4  SU(3)_L running excludes N_c >= 7
# ----------------------------------------------------------------------------------------
def s4():
    banner("S4  SU(3)_L one-loop running (g_L = g_2 at 4 TeV)  =>  N_c >= 7 excluded")
    a0 = S2_MZ * AINV_MZ + 19 / 6 * log(MU331 / MZ) / (2 * pi)
    print(f"   1/alpha_L(4 TeV) = {a0:.2f};  b_L = 11 - N_c (1 + N_c)/3 - 1/2 (three scalar triplets)")
    poles = {}
    for Nc in (3, 5, 7, 9):
        bL = 11 - Nc * (1 + Nc) / 3 - 0.5
        p = None if bL >= 0 else MU331 * exp(2 * pi * a0 / (-bL))
        poles[Nc] = p
        print(f"     N_c = {Nc}: b_L = {bL:+7.3f}   Landau pole: "
              f"{'none (asymptotically free)' if p is None else f'{p:.1e} GeV'}")
    check("N_c = 3, 5 asymptotically free in SU(3)_L", poles[3] is None and poles[5] is None)
    check("N_c = 7 SU(3)_L pole at 1.3e14 GeV, below M_Pl", close(poles[7], 1.3e14, 0.05))


# ----------------------------------------------------------------------------------------
# S5  U(1)_X running excludes N_c = 5
# ----------------------------------------------------------------------------------------
def s5():
    banner("S5  U(1)_X two-loop running from 4 TeV: where does a coupling reach g = 4 pi?")
    print(f"   1/alpha_X(4 TeV) = {boundary(MU331)[0]:.2f};  Planck scale = {M_PLANCK:.2e} GeV")
    yt = yt_at(MU331)
    print(f"   SM top Yukawa at 4 TeV: y_t = {yt:.3f}")
    ref = {("-1/sqrt3", 0): (2.95e29, 1.29e15, 9.7e9), ("+1/sqrt3", 0): (3.98e19, 5.50e11, 3.1e8),
           ("-1/sqrt3", 1): (4.65e29, 1.60e15, 1.10e10), ("+1/sqrt3", 1): (6.21e19, 6.82e11, 3.46e8)}
    rows_ok = []
    for v in VARIANTS:
        print(f"   beta = {v}")
        for Nc in (3, 5, 7):
            a, _ = coefficients(*model(Nc, v)[:3])
            p0 = blow_up(Nc, v)
            p1 = blow_up(Nc, v, yt=yt, yJ=1.0)
            print(f"     N_c = N_g = {Nc}: a = ({float(a[0]):5.2f}, {float(a[1]):5.2f}, {float(a[2]):6.2f})"
                  f"  blow-up {fmt(p0)} (no Yukawas), {fmt(p1)} (y_t, y_J = 1)"
                  f"  -> {'above' if p0 > M_PLANCK else 'BELOW'} Planck")
            i = Nc // 2 - 1
            rows_ok.append(close(p0, ref[(v, 0)][i]) and close(p1, ref[(v, 1)][i]))
    aX, aL, _ = boundary(MU331)
    s_meas = aL / (aX + aL / 3 + aL)                     # 1/alpha_em = 1/alpha_Y + 1/alpha_2
    s_up = bisect(lambda x: log(blow_up(3, "+1/sqrt3", s2=x) / M_PLANCK), 0.15, 0.70)
    print(f"   beta = +1/sqrt3 margin: N_c = 3 reaches M_Pl for sin^2 theta_W(4 TeV) < {s_up:.4f}"
          f" (measured {s_meas:.4f})")
    check("y_t(4 TeV) = 0.827", abs(yt - 0.827) < 1.5e-3)
    check("two-loop blow-ups for N_c = 3, 5, 7, both variants, with and without Yukawas, match",
          all(rows_ok))
    check("only N_c = 3 reaches the Planck scale (both variants)",
          all(blow_up(3, v) > M_PLANCK > blow_up(5, v) for v in VARIANTS))
    check("beta = +1/sqrt3 tree-level margin: sin^2 theta_W < 0.2663", abs(s_up - 0.2663) < 5e-4)


# ----------------------------------------------------------------------------------------
# S6  One-loop threshold matching at the 3-3-1 scale
# ----------------------------------------------------------------------------------------
def heavy_spectrum(Nc, variant, MV, rJ=1.0, rS=1.0, n_light=1):
    """(kind, tY^2, t2^2, t3^2, mass): bilepton vector doublet; exotic quarks (and heavy
    leptons for beta = +1/sqrt3) at r_J M_V; heavy scalars at r_S M_V."""
    _, _, _, (Xt, Xa, Qu, Qd, Ng, nA) = model(Nc, variant)
    out = [("V", 1.0, 1.0, 0.0, MV)]
    exotics = [Qu] * (Ng - nA) + [Qd] * nA if variant == "-1/sqrt3" else [Qd] * (Ng - nA) + [Qu] * nA
    out += [("F", float(Nc * Q**2), 0.0, 0.5, rJ * MV) for Q in exotics]
    if variant == "+1/sqrt3":
        out += [("F", 1.0, 0.0, 0.0, rJ * MV)] * Ng
    if n_light == 1:
        out.append(("S", 1.0, 1.0, 0.0, rS * MV))         # second Higgs doublet, heavy
    out.append(("S", 2.0, 0.0, 0.0, rS * MV))             # charged singlet
    return out


def lambdas(spec, mu):
    """MS-bar matching: lambda = sum_V t^2 (1 - 21 ln M/mu) + 8 sum_F t^2 ln M/mu + sum_S t^2 ln M/mu."""
    lam = [0.0, 0.0, 0.0]
    for kind, tY, t2, t3, M in spec:
        L = log(M / mu)
        w = (1 - 21 * L) if kind == "V" else (8 * L if kind == "F" else L)
        lam = [l + w * t for l, t in zip(lam, (tY, t2, t3))]
    return lam


def pole(Nc, variant, MV=4e3, rJ=1.0, rS=1.0, n_light=1, mu=None, loops=2, s2=None):
    mu = MV if mu is None else mu
    gL = sqrt(4 * pi / boundary(mu)[1])
    lam = lambdas(heavy_spectrum(Nc, variant, MV, rJ, rS, n_light), mu)
    return blow_up(Nc, variant, yt_at(mu), rJ * gL / sqrt(2), mu0=mu, lam=lam,
                   n_light=n_light, loops=loops, s2=s2)


def s6():
    banner("S6  One-loop threshold matching at the 3-3-1 scale, two-loop running, Yukawas on")
    print("   Check: at one loop the N_c = 3 pole must not depend on the matching scale mu.")
    spread = 0.0
    for v in VARIANTS:
        ps = [pole(3, v, 4e3, 2.0, 0.5, 1, mu=4e3 * k, loops=1) for k in (1 / 3, 1, 3)]
        spread = max(spread, max(map(log, ps)) - min(map(log, ps)))
    print(f"   spread in ln(pole) for mu = M_V/3 ... 3 M_V: {spread:.1e}")
    check("thresholds make the one-loop pole independent of the matching scale", spread < 1e-5)

    if FULL_SCAN:
        grid = list(product((0.5, 1.0, 2.0, 3.0), (1 / 3, 1.0, 3.0), (2e3, 4e3, 1e4), (1, 2)))
        print(f"   Scanning {len(grid)} spectra per variant: r_J = m_exotic/M_V in {{0.5, 1, 2, 3}},"
              " r_S in {1/3, 1, 3},\n   M_V in {2, 4, 10} TeV, second doublet heavy or light"
              " (N_c = 5 at its best mu of M_V/3, M_V, 3 M_V).")
    else:
        print("   FULL_SCAN = False: only the extremes of the scan in src/m331_threshold.py.")
    ref = {"-1/sqrt3": (2.44e29, 7.17e15), "+1/sqrt3": (2.00e19, 3.76e12)}
    for v in VARIANTS:
        if FULL_SCAN:
            worst3 = min(pole(3, v, MV, rJ, rS, nl) for rJ, rS, MV, nl in grid)
            best5 = max(pole(5, v, MV, rJ, rS, nl, mu=k * MV)
                        for rJ, rS, MV, nl in grid for k in (1 / 3, 1.0, 3.0))
        else:
            worst3 = pole(3, v, 2e3, 0.5, 1 / 3, 2)
            best5 = max(pole(5, v, 1e4, 3.0, rS, 1, mu=3e4) for rS in (1 / 3, 1.0, 3.0))
        print(f"   beta = {v}: worst N_c = 3 pole = {worst3:.2e} GeV = {worst3 / M_PLANCK:.3g} M_Pl;"
              f"  best N_c = 5 pole = {best5:.2e} GeV")
        check(f"beta = {v}: worst N_c = 3 > M_Pl > best N_c = 5, values match the repository",
              worst3 > M_PLANCK > best5 and close(worst3, ref[v][0]) and close(best5, ref[v][1]))
    p_lhc = pole(3, "+1/sqrt3", 4.6e3 / 1.225, 0.5, 1 / 3, 2)
    print(f"   beta = +1/sqrt3 at the LHC Z' bound (M_Z' >= 4.6 TeV, M_V >= 3.76 TeV), worst spectrum:"
          f" {p_lhc / M_PLANCK:.3g} M_Pl")
    u = bisect(lambda x: log(pole(3, "+1/sqrt3", 4e3, 0.5, 1 / 3, 2, s2=x) / M_PLANCK), 0.15, 0.70)
    print(f"   beta = +1/sqrt3, worst spectrum: N_c = 3 needs sin^2 theta_W(4 TeV) < {u:.4f} (measured 0.2504)")
    check("beta = +1/sqrt3 at the LHC bound: 2.17 M_Pl", close(p_lhc / M_PLANCK, 2.17))
    check("beta = +1/sqrt3 threshold margin: sin^2 theta_W < 0.2608", abs(u - 0.2608) < 5e-4)


# ----------------------------------------------------------------------------------------
# S6b  The narrow variant (beta = +1/sqrt3) against physical mass floors
# ----------------------------------------------------------------------------------------
# The worst case of S6 sits on the corner of its grid, and the grid ties the heavy charged
# leptons E to the exotic quarks (one r_J). Here every mass runs on its own, against
# experimental floors, with the controlled criterion alpha = 1 (g = sqrt(4 pi)) instead of
# g = 4 pi, where the loop expansion has already broken down (NOTE_331.md, section 3d).
FLOORS = dict(MV=4.6e3 / 1.225, mJ=1.3e3, mE=100.0, mS=100.0, n_light=2)   # GeV
G_ALPHA1 = sqrt(4 * pi)


def pole_split(Nc, MV, mJ, mE, mS, n_light=2, gmax=G_ALPHA1):
    """Blow-up scale for beta = +1/sqrt3 with the exotic quarks (m_J), heavy leptons (m_E)
    and heavy scalars (m_S) at their own masses; each Yukawa set by its own mass."""
    v = "+1/sqrt3"
    out = []
    for kind, tY, t2, t3, M in heavy_spectrum(Nc, v, MV, 1.0, 1.0, n_light):
        if kind == "F":
            M = mJ if t3 > 0 else mE                       # quarks carry colour; leptons do not
        elif kind == "S":
            M = mS
        out.append((kind, tY, t2, t3, M))
    gs = model(Nc, v)[0]
    ct, cJ = yukawas_331(Nc, v)
    lep = [Nc * float(x) for x in yukawa_coeff(gs, ((None, 3, 1), F(-2, 3)), ((None, 1, 1), F(1)), 3)]
    cq = [x - l for x, l in zip(cJ, lep)]                  # exotic quarks alone
    gL = sqrt(4 * pi / boundary(MV)[1])
    yJ2, yE2 = (mJ * gL / (sqrt(2) * MV)) ** 2, (mE * gL / (sqrt(2) * MV)) ** 2
    yt2 = yt_at(MV) ** 2
    yuk = [ct[i] * yt2 + cq[i] * yJ2 + lep[i] * yE2 for i in range(3)]
    return blow_up(Nc, v, mu0=MV, gmax=gmax, lam=lambdas(out, MV), n_light=n_light, yuk=yuk)


def s6b():
    banner("S6b The narrow variant (beta = +1/sqrt3) against mass floors, criterion alpha = 1")
    f = FLOORS
    print(f"   Floors: M_V >= {f['MV'] / 1e3:.3f} TeV (Z' >= 4.6 TeV), exotic quarks m_J >= 1.3 TeV,")
    print("   heavy charged leptons m_E >= 0.1 TeV (LEP), heavy scalars >= 0.1 TeV. Two loops.")
    p3 = pole_split(3, **f) / M_PLANCK
    p5 = pole_split(5, **f) / M_PLANCK
    print(f"   all masses at the floors: N_c = 3 pole = {p3:.3f} M_Pl;  N_c = 5 pole = {p5:.1e} M_Pl")
    g = lambda lm: log(pole_split(3, f["MV"], f["mJ"], exp(lm), f["mS"], f["n_light"]) / M_PLANCK)
    m_star = exp(bisect(g, log(100.0), log(3000.0), tol=1e-4))
    print(f"   N_c = 3 reaches M_Pl only if m_E >= {m_star:.0f} GeV (two loops; the repository's three-loop")
    print("   value is 561 +- 113 GeV, src/m331_margin.py). With three E the condition is on their")
    print("   geometric mean. Run 2 allows that mean down to ~0.24 TeV, so the LHC has not tested it;")
    print("   the HL-LHC reaches about the threshold (src/m331_heavy_lepton.py).")
    check("beta = +1/sqrt3, light heavy leptons: N_c = 3 falls below M_Pl at alpha = 1 (0.579 M_Pl)",
          p3 < 1 and close(p3, 0.579, 0.01))
    check("beta = +1/sqrt3: N_c = 5 stays excluded at the same floors", p5 < 1e-6)
    check("beta = +1/sqrt3: N_c = 3 needs m_E >= 684 GeV at two loops", close(m_star, 684.0, 0.01))


# ----------------------------------------------------------------------------------------
# S7  Cross-check with data: the R-ratio
# ----------------------------------------------------------------------------------------
def s7():
    banner("S7  Data cross-check: R(e+e- -> hadrons) below charm vs KEDR 2.225 +- 0.051")
    a_s = alpha_s(2.45)
    print(f"   alpha_s(2.45 GeV) = {a_s:.3f}.  R = N_c (Q_u^2 + 2 Q_d^2)(1 + 3 C_F alpha_s / 4 pi)")
    R3 = None
    for Nc in (1, 3, 5, 7):
        Qu, Qd = charges(Nc)
        CF = (Nc**2 - 1) / (2 * Nc)
        R = float(Nc * (Qu**2 + 2 * Qd**2)) * (1 + 3 * CF * a_s / (4 * pi))
        R3 = R if Nc == 3 else R3
        print(f"     N_c = {Nc}: R = {R:6.3f}   ({(R - 2.225) / 0.051:+6.1f} sigma)")
    check("alpha_s(2.45 GeV) = 0.272", abs(a_s - 0.272) < 1.5e-3)
    check("N_c = 3 fits the measured R-ratio (R = 2.173, within 1.1 sigma)", abs(R3 - 2.173) < 2e-3)


def main():
    t0 = time.time()
    for section in (s1, s2, s3, s4, s5, s6, s6b, s7):
        section()
    banner("VERDICT")
    n_ok = sum(ok for _, ok in CHECKS)
    print("   Perturbative anomalies fix the charges for any N_c; the SU(3)_L anomaly and asymptotic")
    print("   freedom force N_c odd with N_g = N_c; SU(3)_L running excludes N_c >= 7 and U(1)_X")
    print("   running excludes N_c = 5. Only N_c = N_g = 3 stays perturbative to the Planck scale,")
    print("   with quark charges 2/3 and -1/3.")
    print("   Conditional on the 3-3-1 framework, Planck-scale perturbativity, and the measured")
    print("   TeV-scale electroweak couplings (an input, not a prediction). In the beta = -1/sqrt3")
    print("   variant the margins are wide. In the beta = +1/sqrt3 variant the selection is a")
    print("   condition, not a margin: N_c = 3 reaches M_Pl at alpha = 1 only if the three heavy")
    print("   charged leptons are heavy enough (geometric mean >= 561 +- 113 GeV at three loops,")
    print("   S6b at two loops). The LHC has not tested this; the HL-LHC reaches about the threshold.")
    print(f"\n   Checks passed: {n_ok}/{len(CHECKS)}   ({time.time() - t0:.0f} s)")
    for label, ok in CHECKS:
        if not ok:
            print(f"   FAILED: {label}")
    print("   ALL CHECKS PASS" if n_ok == len(CHECKS) else "   SOME CHECKS FAILED")
    return n_ok == len(CHECKS)


if __name__ == "__main__":
    main()
