#!/usr/bin/env python3
"""
The shared core of the 3-3-1 selection (NOTE_331.md): group invariants, the general one-
and two-loop gauge beta-function coefficients, the two-loop Yukawa coefficient, and the
3-3-1 field content, charges and anomalies for general N_c and N_g, in both variants.

Standard library only. src/m331_exact.py and src/m331_yukawa.py import it; the one-paste
script src/m331_standalone.py carries a copy written by tools/build_m331_standalone.py,
and tests/test_331_core.py fails if that copy is stale. Edit this file, not the copy.
"""
from fractions import Fraction as F

VARIANTS = ("-1/sqrt3", "+1/sqrt3")


# >>> core
class Group:
    def __init__(self, name, N=None):            # N = None -> U(1)
        self.name, self.N = name, N

    def CA(self):
        return 0 if self.N in (None, 1) else self.N         # N = 1: no colour group (N_c = 1)

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
        dG = 1 if g.N in (None, 1) else g.N**2 - 1
        s = sum(q**2 if g.N is None else g.C2(dims[i]) for dims, q in (psi1, psi2))
        out.append(F(n_terms) * s / dG)
    return out


# The 3-3-1 models for general N_c (groups ordered X, SU(3)_L, SU(N_c))
def charges(Nc):
    """Quark charges fixed by anomaly cancellation with Yukawas, for general N_c."""
    return F(Nc + 1, 2 * Nc), F(1 - Nc, 2 * Nc)


def model(Nc, variant, Ng=None):
    Qu, Qd = charges(Nc)
    Ng = Nc if Ng is None else Ng            # N_g = N_c unless given
    if (Ng * (1 + Nc)) % (2 * Nc):
        raise ValueError(f"N_c = {Nc}, N_g = {Ng}: the SU(3)_L anomaly does not cancel")
    nA = Ng * (1 + Nc) // (2 * Nc)           # n anti-triplet generations: N_g (1 + N_c) = 2 n N_c
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


def anomalies(Nc, variant, Ng=None):
    gs, ferm, scal, (Xt, Xa, Qu, Qd, Ng, nA) = model(Nc, variant, Ng)
    dim = lambda d: d[1] * d[2]
    return {
        "X^3": sum(m * dim(d) * q**3 for m, d, q in ferm),
        "grav^2 X": sum(m * dim(d) * q for m, d, q in ferm),
        "SU3L^2 X": sum(m * d[2] * q for m, d, q in ferm if d[1] == 3),
        "SUNc^2 X": sum(m * d[1] * q for m, d, q in ferm if d[2] == Nc and Nc > 1),
        "SU3L^3": F(Ng + Nc * (Ng - nA) - Nc * nA),       # triplets minus anti-triplets
    }
# <<< core
