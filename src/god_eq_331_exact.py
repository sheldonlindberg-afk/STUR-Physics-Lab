#!/usr/bin/env python3
"""
God-equation search, front 7b: firming up 'N_c = N_g = 3' with exact charges and
two-loop gauge running.

Model: 3-3-1 with beta = -1/sqrt3 (Q = T3 + beta T8 + X), N_g = N_c generations, quark
charges from anomaly cancellation for general N_c (front 5):
    Q_u = (N_c+1)/(2N_c), Q_d = (1-N_c)/(2N_c).
Left-handed Weyl content:
    leptons   L   = (1, 3, -1/3) x N_g,       e^c = (1, 1, +1) x N_g
    quarks    Q_t = (N_c, 3,  Q_u - 1/3) x (N_g - n)     [u, d, T]
              Q_a = (N_c, 3b, Q_d + 1/3) x n             [d, -u, D],   n = (1+N_c)/2
              u^c, d^c (Nb_c, 1, -Q_u / -Q_d) per generation, plus T^c (-Q_u) or D^c (-Q_d)
    scalars   eta = (1, 3, -1/3), rho = (1, 3, +2/3), chi = (1, 3, -1/3)   (complex;
              X fixed by the Yukawa couplings, N_c-independent)
Checks: every gauge anomaly vanishes for general N_c; the two-loop machinery reproduces
the Standard Model's known one- and two-loop gauge coefficients (GUT-normalised):
    a = (41/10, -19/6, -7),  b = [[199/50, 27/10, 44/5], [9/10, 35/6, 12], [11/10, 9/2, -26]].
Yukawa contributions to the two-loop running are NOT included (they slow the growth of
U(1) couplings in the SM; labelled).
"""
from fractions import Fraction as F
from math import log, pi, sqrt
import numpy as np
from scipy.integrate import solve_ivp

MZ, ainv, s2 = 91.1876, 127.95, 0.23122
M_PLANCK = 1.22089e19


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


class Group:
    def __init__(self, name, N=None):        # N=None -> U(1)
        self.name, self.N = name, N

    def CA(self):
        return 0 if self.N is None else self.N

    def T(self, d):                          # Dynkin index of irrep of dimension d
        if self.N is None or d == 1:
            return 0
        if d == self.N:
            return F(1, 2)
        if self.N == 3 and d == 6:
            return F(5, 2)
        raise ValueError(d)

    def C2(self, d, charge=None):
        if self.N is None:
            return charge**2
        if d == 1:
            return 0
        if d == self.N:
            return F(self.N**2 - 1, 2 * self.N)
        raise ValueError(d)


def coefficients(groups, fermions, scalars, kappa=F(1, 2), sigma=F(2)):
    # sigma = 2 (complex scalar = 2 real d.o.f.) is FIXED by the SM two-loop check (E1)
    """fermions/scalars: list of (multiplicity, dims tuple (None for U(1)), U(1) charge or None).
    Returns one-loop a_i and two-loop b_ij for d g_i/dt = g_i^3/(16pi^2) [a_i + sum_j b_ij g_j^2/(16pi^2)]."""
    n = len(groups)

    def S(i, mult, dims, q):
        g = groups[i]
        other = 1
        for j, d in enumerate(dims):
            if j != i and d is not None:
                other *= d
        if g.N is None:
            return mult * other * q**2
        return mult * other * g.T(dims[i])

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


def sm_check():
    gs = [Group("Y"), Group("SU2", 2), Group("SU3", 3)]
    ferm = []
    for _ in range(3):
        ferm += [(1, (None, 2, 3), F(1, 6)), (1, (None, 1, 3), F(-2, 3)), (1, (None, 1, 3), F(1, 3)),
                 (1, (None, 2, 1), F(-1, 2)), (1, (None, 1, 1), F(1))]
    scal = [(1, (None, 2, 1), F(1, 2))]
    a, b = coefficients(gs, ferm, scal)
    # GUT normalisation g1 = sqrt(5/3) g_Y:  a1 = 3/5 a_Y, b11 = 9/25 b_YY, b1j = 3/5 b_Yj, bj1 = 3/5 b_jY
    a = [a[0] * F(3, 5), a[1], a[2]]
    b = [[b[0][0] * F(9, 25), b[0][1] * F(3, 5), b[0][2] * F(3, 5)],
         [b[1][0] * F(3, 5), b[1][1], b[1][2]],
         [b[2][0] * F(3, 5), b[2][1], b[2][2]]]
    return a, b


def model_331(Nc):
    Qu, Qd = F(Nc + 1, 2 * Nc), F(1 - Nc, 2 * Nc)
    Ng, nA = Nc, (1 + Nc) // 2
    Xt, Xa = Qu - F(1, 3), Qd + F(1, 3)
    gs = [Group("X"), Group("SU3L", 3), Group("SUNc", Nc)]
    ferm = [(Ng, (None, 3, 1), F(-1, 3)), (Ng, (None, 1, 1), F(1)),
            (Ng - nA, (None, 3, Nc), Xt), (nA, (None, 3, Nc), Xa)]
    ferm += [(Ng, (None, 1, Nc), -Qu), (Ng, (None, 1, Nc), -Qd),
             (Ng - nA, (None, 1, Nc), -Qu), (nA, (None, 1, Nc), -Qd)]
    scal = [(1, (None, 3, 1), F(-1, 3)), (1, (None, 3, 1), F(2, 3)), (1, (None, 3, 1), F(-1, 3))]
    return gs, ferm, scal, (Xt, Xa, Qu, Qd, Ng, nA)


def model_331_plus(Nc):
    """beta = +1/sqrt3: Q = T3 + T8/sqrt3 + X.  Leptons (nu, e, E-) triplets X = -2/3 with
    heavy charged lepton E; quark triplet (u, d, J) X = Q_u - 2/3 (J d-like); anti-triplet
    (d, -u, J') X = Q_d + 2/3 (J' u-like).  Scalars from the Yukawas: X = 1/3, 1/3, -2/3."""
    Qu, Qd = F(Nc + 1, 2 * Nc), F(1 - Nc, 2 * Nc)
    Ng, nA = Nc, (1 + Nc) // 2
    Xt, Xa = Qu - F(2, 3), Qd + F(2, 3)
    gs = [Group("X"), Group("SU3L", 3), Group("SUNc", Nc)]
    ferm = [(Ng, (None, 3, 1), F(-2, 3)), (Ng, (None, 1, 1), F(1)), (Ng, (None, 1, 1), F(1)),
            (Ng - nA, (None, 3, Nc), Xt), (nA, (None, 3, Nc), Xa)]
    ferm += [(Ng, (None, 1, Nc), -Qu), (Ng, (None, 1, Nc), -Qd),
             (Ng - nA, (None, 1, Nc), -Qd), (nA, (None, 1, Nc), -Qu)]
    scal = [(1, (None, 3, 1), F(1, 3)), (1, (None, 3, 1), F(1, 3)), (1, (None, 3, 1), F(-2, 3))]
    return gs, ferm, scal, (Xt, Xa, Qu, Qd, Ng, nA)


MODELS = {"-1/sqrt3": model_331, "+1/sqrt3": model_331_plus}


def anomalies(Nc, model=model_331):
    gs, ferm, scal, (Xt, Xa, Qu, Qd, Ng, nA) = model(Nc)
    def dim(d):
        p = 1
        for x in d[1:]:
            p *= x
        return p
    A = {}
    A["X^3"] = sum(m * dim(d) * q**3 for m, d, q in ferm)
    A["grav^2 X"] = sum(m * dim(d) * q for m, d, q in ferm)
    A["SU3L^2 X"] = sum(m * d[2] * q for m, d, q in ferm if d[1] == 3)
    A["SUNc^2 X"] = sum(m * d[1] * q for m, d, q in ferm if d[2] == Nc and Nc > 1)
    trip = Ng + Nc * (Ng - nA)
    A["SU3L^3 (3 - 3bar)"] = F(trip - Nc * nA)
    return A


def run_two_loop(Nc, mu0=4e3, loops=2, model=model_331, gmax=4 * pi):
    gs, ferm, scal, _ = model(Nc)
    a, b = coefficients(gs, ferm, scal)
    a = np.array([float(x) for x in a]); b = np.array([[float(x) for x in r] for r in b])
    L0 = log(mu0 / MZ) / (2 * pi)
    aY_inv = (1 - s2) * ainv - 41 / 6 * L0
    a2_inv = s2 * ainv + 19 / 6 * L0
    from stur_open_problems import alpha_s_run
    a3_inv = 1 / alpha_s_run(mu0)
    aL_inv = a2_inv
    aX_inv = aY_inv - (1 / 3) * aL_inv                        # 1/g_Y^2 = 1/g_X^2 + beta^2/g_L^2
    g0 = np.sqrt(4 * pi / np.array([aX_inv, aL_inv, a3_inv]))

    def rhs(t, g):
        two = (b @ (g**2)) / (16 * pi**2) if loops == 2 else 0
        return g**3 / (16 * pi**2) * (a + two)

    def blow(t, g):
        return gmax - max(g)                                   # default g = 4 pi: non-perturbative
    blow.terminal = True
    tmax = log(1e40 / mu0)
    sol = solve_ivp(rhs, [0, tmax], g0, events=blow, rtol=1e-9, atol=1e-12, max_step=0.5)
    if sol.t_events[0].size:
        return mu0 * np.exp(sol.t_events[0][0]), a, b, aX_inv
    return None, a, b, aX_inv


def main():
    banner("E1  CHECK: general two-loop machinery vs the Standard Model")
    a, b = sm_check()
    print("   one-loop a  =", [str(x) for x in a], "  (expected 41/10, -19/6, -7)")
    for row in b:
        print("   two-loop b  =", [str(x) for x in row])
    print("   expected    = [199/50, 27/10, 44/5] [9/10, 35/6, 12] [11/10, 9/2, -26]")
    exp = [[F(199, 50), F(27, 10), F(44, 5)], [F(9, 10), F(35, 6), F(12)], [F(11, 10), F(9, 2), F(-26)]]
    print(f"   all 9 two-loop entries exact: {b == exp}")

    banner("E2  CHECK: all gauge anomalies vanish for general N_c (exact charges)")
    for Nc in [3, 5, 7]:
        A = anomalies(Nc)
        print(f"   N_c = {Nc}: " + ", ".join(f"{k} = {v}" for k, v in A.items()))

    banner("E3  Two-loop gauge running from 4 TeV: where does a coupling reach g = 4 pi?")
    for Nc in [3, 5, 7]:
        for loops in [1, 2]:
            mp, a, b, aXi = run_two_loop(Nc, loops=loops)
            print(f"   N_c = N_g = {Nc}, {loops}-loop: a = ({a[0]:.2f}, {a[1]:.2f}, {a[2]:.2f})  "
                  f"1/alpha_X(4 TeV) = {aXi:.2f}  ->  "
                  f"{'no blow-up below 1e40 GeV' if mp is None else f'blow-up at {mp:.1e} GeV'}"
                  f"  {'' if mp is None else ('BELOW' if mp < M_PLANCK else 'above') + ' Planck'}")
    aXi = run_two_loop(3)[3]
    a_crit = 2 * pi * aXi / log(M_PLANCK / 4e3)
    print(f"\n   one-loop U(1)_X coefficient that puts the pole exactly at the Planck scale: {a_crit:.2f}")
    for Nc in (3, 5):
        aX = float(coefficients(*model_331(Nc)[:3])[0][0])
        print(f"   N_c = {Nc}: a_X = {aX:.2f}  ->  margin {a_crit - aX:+.2f}")
    print("   (charges and scalar content exact; two-loop Yukawa terms NOT included - they enter only")
    print("    at two loops, while the verdict is already set at one loop with margins of 4.6 and 6.1)")
    print("\n   3-3-1 scale dependence (two-loop):")
    for mu0 in [2e3, 4e3, 1e4, 3e4]:
        res = [run_two_loop(Nc, mu0=mu0)[0] for Nc in (3, 5)]
        print(f"     mu_331 = {mu0/1e3:5.0f} TeV:  N_c = 3 -> "
              f"{'none' if res[0] is None else f'{res[0]:.1e}'}   N_c = 5 -> "
              f"{'none' if res[1] is None else f'{res[1]:.1e}'}")


def variant_plus():
    banner("E4  The other viable variant: beta = +1/sqrt3 (exact charges, two loops)")
    for Nc in [3, 5, 7]:
        A = anomalies(Nc, model_331_plus)
        print(f"   N_c = {Nc} anomalies: " + ", ".join(f"{k} = {v}" for k, v in A.items()))
    for Nc in [3, 5, 7]:
        mp, a, b, aXi = run_two_loop(Nc, model=model_331_plus)
        print(f"   N_c = N_g = {Nc}: a = ({a[0]:.2f}, {a[1]:.2f}, {a[2]:.2f})  ->  "
              f"{'no blow-up below 1e40 GeV' if mp is None else f'blow-up at {mp:.1e} GeV'}"
              f"  {'' if mp is None else ('BELOW' if mp < M_PLANCK else 'above') + ' Planck'}")
    print("   criterion for 'non-perturbative' (blow-up scale, GeV; Planck = 1.2e19):")
    for name, m in MODELS.items():
        for crit, gm in [("g = 4 pi", 4 * pi), ("alpha = 1", sqrt(4 * pi)), ("g = 1 (alpha = 0.08)", 1.0)]:
            r = [run_two_loop(Nc, model=m, gmax=gm)[0] for Nc in (3, 5)]
            print(f"     beta = {name:8s} {crit:22s} N_c = 3: {r[0]:.1e}   N_c = 5: {r[1]:.1e}")
    for mu0 in [2e3, 1e4, 3e4]:
        res = [run_two_loop(Nc, mu0=mu0, model=model_331_plus)[0] for Nc in (3, 5)]
        print(f"     mu_331 = {mu0/1e3:5.0f} TeV:  N_c = 3 -> "
              f"{'none' if res[0] is None else f'{res[0]:.1e}'}   N_c = 5 -> "
              f"{'none' if res[1] is None else f'{res[1]:.1e}'}")


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
    variant_plus()
