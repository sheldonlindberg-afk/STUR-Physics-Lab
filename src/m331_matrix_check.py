#!/usr/bin/env python3
"""
An independent route to the 3-3-1 gauge beta-function coefficients (NOTE_331.md, section 3).

src/m331_exact.py gets the one- and two-loop coefficients from tabulated group invariants
(Dynkin indices, Casimirs, dimensions) of each multiplet. This script uses none of those
tables. It builds the explicit generator matrices of U(1)_X x SU(3)_L x SU(N_c) on every
fermion and scalar multiplet and takes the traces numerically:

    S2_i delta^ab = Tr(T_i^a T_i^b),   C_i = sum_a T_i^a T_i^a,   C_A delta^ab = f^acd f^bcd,
    a_i  = -11/3 C_A + 2/3 sum_F S2_i + 1/3 sum_S S2_i
    b_ij = -34/3 C_A^2 delta_ij + sum_F [10/3 C_A S2_i delta_ij + 2 Tr(C_i C_j)/d_i]
                                + sum_S [ 2/3 C_A S2_i delta_ij + 4 Tr(C_i C_j)/d_i]
    Yukawa term per y^2:  sum_a Tr(C_i Y^a Y^a+) / d_i      (Machacek-Vaughn 1984)

with Weyl fermions F, complex scalars S, d_i the number of generators, and Y^a the explicit
symmetric Yukawa matrix of each complex scalar component, checked to be gauge invariant.

M1  The Standard Model: (41/10, -19/6, -7), all nine two-loop coefficients and the top
    Yukawa's (17/10, 3/2, 2), from matrices.
M2  Both 3-3-1 variants, N_c = N_g = 3, 5, 7, and (N_c, N_g) = (2, 4): every one- and
    two-loop coefficient agrees with m331_exact.coefficients.
M3  The top, exotic-quark and heavy-lepton Yukawa matrices are gauge invariant with a scalar
    the model contains, and their two-loop coefficients agree with m331_yukawa.yukawas_331.

What this is and is not. It is a second derivation of every group-theory input: each
index, Casimir, multiplicity and dimension is recomputed from matrices. It shares the
general two-loop formula with m331_exact; that formula's normalisation is fixed by M1. It is
not a comparison with an external package such as PyR@TE or SARAH, which would be a
further, stronger check.
"""
import os
import sys
from fractions import Fraction as F
from itertools import product

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_exact as E
import m331_yukawa as Y

TOL = 1e-10


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def su_generators(N):
    """The N^2 - 1 generalised Gell-Mann matrices over 2: Tr(T^a T^b) = delta^ab / 2."""
    gens = []
    for i, j in product(range(N), repeat=2):
        if i < j:
            s = np.zeros((N, N), complex); s[i, j] = s[j, i] = 0.5
            a = np.zeros((N, N), complex); a[i, j], a[j, i] = -0.5j, 0.5j
            gens += [s, a]
    for k in range(1, N):
        d = np.zeros((N, N), complex)
        d[:k, :k] = np.eye(k)
        d[k, k] = -k
        gens.append(d / np.sqrt(2 * k * (k + 1)))
    assert len(gens) == N * N - 1
    return gens


def adjoint_casimir(gens):
    """C_A from the structure constants f^abc = -2i Tr([T^a, T^b] T^c) of the fundamental."""
    n = len(gens)
    f = np.zeros((n, n, n))
    for a in range(n):
        for b in range(a + 1, n):
            comm = gens[a] @ gens[b] - gens[b] @ gens[a]
            for c in range(n):
                f[a, b, c] = (-2j * np.trace(comm @ gens[c])).real
                f[b, a, c] = -f[a, b, c]
    m = np.einsum("acd,bcd->ab", f, f)
    assert np.allclose(m, m[0, 0] * np.eye(n), atol=TOL)
    return m[0, 0]


def rep(group_gens, dims, q):
    """Generators of each group on one multiplet: [[q 1], SU(3)_L gens, colour gens]."""
    sizes = [d for d in dims[1:]]
    D = int(np.prod(sizes))
    out = [[q * np.eye(D, dtype=complex)]]
    for slot, d in enumerate(sizes):
        if d == 1:
            out.append([np.zeros((D, D), complex) for _ in group_gens[slot]])
            continue
        mats = []
        for t in group_gens[slot]:
            parts = [np.eye(s) for s in sizes]
            parts[slot] = t
            m = parts[0]
            for p in parts[1:]:
                m = np.kron(m, p)
            mats.append(m)
        out.append(mats)
    return out


def invariants(gens_i):
    """(S2, C) for one group on one multiplet, checking Tr(T^a T^b) is proportional to delta."""
    n = len(gens_i)
    tr = np.array([[np.trace(gens_i[a] @ gens_i[b]).real for b in range(n)] for a in range(n)])
    assert np.allclose(tr, tr[0, 0] * np.eye(n), atol=TOL)
    return tr[0, 0], sum(t @ t for t in gens_i)


def coefficients(Ns, fermions, scalars):
    """One- and two-loop coefficients from explicit matrices. Ns: N of each non-abelian
    group (the U(1) comes first); fields as in m331_exact: (multiplicity, dims, charge)."""
    group_gens = [su_generators(N) if N > 1 else [] for N in Ns]
    CA = [0.0] + [adjoint_casimir(g) if g else 0.0 for g in group_gens]
    dG = [1] + [max(len(g), 1) for g in group_gens]
    n = len(Ns) + 1
    a = np.array([-11 / 3 * c for c in CA])
    b = np.diag([-34 / 3 * c * c for c in CA])
    for fields, c1, c2self, c2mix in ((fermions, 2 / 3, 10 / 3, 2.0), (scalars, 1 / 3, 2 / 3, 4.0)):
        for mult, dims, q in fields:
            gens = rep(group_gens, dims, float(q))
            inv = [invariants(g) if g else (0.0, 0.0 * gens[0][0]) for g in gens]
            for i in range(n):
                a[i] += c1 * mult * inv[i][0]
                b[i, i] += c2self * CA[i] * mult * inv[i][0]
                for j in range(n):
                    b[i, j] += c2mix * mult * np.trace(inv[i][1] @ inv[j][1]).real / dG[i]
    return a, b


def yukawa(Ns, psi1, psi2, scalar_charges):
    """Two-loop coefficient per y^2 of the Yukawa psi1 psi2 phi, built explicitly.
    psi = (dims, charge). psi1 carries the SU(3)_L (or SU(2)) index, contracted with the
    scalar's; colour is contracted between psi1 and psi2. Checks gauge invariance, and
    that the model has a scalar of the charge the coupling needs."""
    group_gens = [su_generators(N) if N > 1 else [] for N in Ns]
    (d1, q1), (d2, q2) = psi1, psi2
    qs = -(q1 + q2)
    assert any(qs == x or qs == -x for x in scalar_charges), (qs, scalar_charges)
    nL, nC = d1[1], d1[2]
    assert d2[1] == 1 and d2[2] == nC
    g1 = rep(group_gens, d1, float(q1))
    # psi2 in the conjugate colour representation, so that colour contracts with a delta
    g2 = [[-m.T for m in g] for g in rep(group_gens, d2, -float(q2))]
    D1, D2 = nL * nC, nC
    T = [[np.block([[m1, np.zeros((D1, D2))], [np.zeros((D2, D1)), m2]]) for m1, m2 in zip(x, y)]
         for x, y in zip(g1, g2)]
    Ys = []
    for al in range(nL):                                   # one matrix per complex scalar component
        y = np.zeros((D1 + D2, D1 + D2), complex)
        for c in range(nC):
            y[al * nC + c, D1 + c] = y[D1 + c, al * nC + c] = 1.0
        Ys.append(y)
    # invariance: T^T Y^a + Y^a T + sum_b (T_S)_ba Y^b = 0, the scalar in the conjugate of psi1's
    # SU(3)_L representation with U(1) charge qs
    TS = [[qs * np.eye(nL, dtype=complex)], [-t.T for t in group_gens[0]], [0 * np.eye(nL)] * len(group_gens[1])]
    for gi in range(3):
        for k, t in enumerate(T[gi]):
            for al in range(nL):
                res = t.T @ Ys[al] + Ys[al] @ t + sum(TS[gi][k][be, al] * Ys[be] for be in range(nL))
                assert np.allclose(res, 0, atol=TOL), (gi, k, al)
    out = []
    for gi in range(3):
        C = sum(t @ t for t in T[gi])
        out.append(sum(np.trace(C @ y @ y.conj().T).real for y in Ys) / max(len(T[gi]) if gi else 1, 1))
    return np.array(out)


def close(x, ref):
    return np.allclose(np.array(x, float), np.array([[float(v) for v in r] for r in ref] if isinstance(ref[0], list)
                                                    else [float(v) for v in ref], float), atol=1e-9)


def sm():
    ferm = []
    for _ in range(3):
        ferm += [(1, (None, 2, 3), F(1, 6)), (1, (None, 1, 3), F(-2, 3)), (1, (None, 1, 3), F(1, 3)),
                 (1, (None, 2, 1), F(-1, 2)), (1, (None, 1, 1), F(1))]
    a, b = coefficients((2, 3), ferm, [(1, (None, 2, 1), F(1, 2))])
    r = np.array([3 / 5, 1, 1])                            # GUT normalisation of the U(1)
    top = yukawa((2, 3), ((None, 2, 3), F(1, 6)), ((None, 1, 3), F(-2, 3)), [F(1, 2)])
    return a * r, b * np.outer(r, r), top * r


def compare(Nc, variant, Ng=None):
    """Largest absolute difference from m331_exact (gauge) and m331_yukawa (Yukawa terms)."""
    gs, ferm, scal, (Xt, Xa, Qu, Qd, Ng, nA) = E.MODELS[variant](Nc, Ng)
    a, b = coefficients((3, Nc), ferm, scal)
    a0, b0 = E.coefficients(gs, ferm, scal)
    d_gauge = max(np.abs(a - [float(x) for x in a0]).max(),
                  np.abs(b - [[float(x) for x in r] for r in b0]).max())
    xs = [x[2] for x in scal]
    Q, S = (None, 3, Nc), (None, 1, Nc)
    top = yukawa((3, Nc), (Q, Xt), (S, -Qu), xs)
    if variant == "-1/sqrt3":
        ex = (Ng - nA) * yukawa((3, Nc), (Q, Xt), (S, -Qu), xs) + nA * yukawa((3, Nc), (Q, Xa), (S, -Qd), xs)
    else:
        ex = (Ng - nA) * yukawa((3, Nc), (Q, Xt), (S, -Qd), xs) + nA * yukawa((3, Nc), (Q, Xa), (S, -Qu), xs)
        ex = ex + Ng * yukawa((3, Nc), ((None, 3, 1), F(-2, 3)), ((None, 1, 1), F(1)), xs)
    d_yuk = 0.0
    if Ng == Nc:                                           # m331_yukawa is written for N_g = N_c
        ct, cJ = Y.yukawas_331(Nc, variant)
        d_yuk = max(np.abs(top - [float(x) for x in ct]).max(), np.abs(ex - [float(x) for x in cJ]).max())
    return d_gauge, d_yuk


def main():
    banner("M1  The Standard Model from explicit generator matrices")
    a, b, top = sm()
    print("   one-loop a =", np.round(a, 10), "  (41/10, -19/6, -7)")
    for row in b:
        print("   two-loop b =", np.round(row, 10))
    print("   top Yukawa =", np.round(top, 10), "  (17/10, 3/2, 2)")
    ok = (close(a, [F(41, 10), F(-19, 6), F(-7)]) and close(top, [F(17, 10), F(3, 2), F(2)])
          and close(b, [[F(199, 50), F(27, 10), F(44, 5)], [F(9, 10), F(35, 6), F(12)], [F(11, 10), F(9, 2), F(-26)]]))
    print(f"   all 15 Standard Model coefficients reproduced: {ok}")

    banner("M2 + M3  3-3-1 models: matrices against the tabulated group invariants")
    print("   largest |difference| in the 3 one-loop and 9 two-loop gauge coefficients, and in the")
    print("   6 two-loop Yukawa coefficients (top; all exotics); Yukawa matrices checked invariant")
    worst = 0.0
    for variant in E.MODELS:
        for Nc, Ng in ((3, 3), (5, 5), (7, 7), (2, 4)):
            dg, dy = compare(Nc, variant, Ng)
            worst = max(worst, dg, dy)
            print(f"   beta = {variant}, N_c = {Nc}, N_g = {Ng}: gauge {dg:.1e}   Yukawa "
                  + (f"{dy:.1e}" if Ng == Nc else "(invariance only)"))
    print(f"   -> every coefficient agrees to {worst:.0e}: the group-theory inputs of the selection are")
    print("      confirmed by a route that uses no tabulated index, Casimir or dimension.")
    return ok, worst


if __name__ == "__main__":
    main()
