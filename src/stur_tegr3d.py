#!/usr/bin/env python3
"""
Teleparallel gravity in three dimensions, and the quantum amplitude it shares with
loop quantum gravity there (worked example; every result here is KNOWN).

3D Euclidean gravity is a BF theory, S = (1/16 pi G) int tr(e ^ F(omega)), with two
equations of motion: flatness F(omega) = 0 and zero torsion d_omega e = 0. It has no local
degrees of freedom. Its standard loop quantization imposes the torsion (Gauss) constraint
first; the dual quantization imposes flatness first, which is the teleparallel choice
(Delcamp, Freidel, Girelli, arXiv:1803.03246; Shoshany, arXiv:1904.06386). The physical
amplitude of the Ponzano-Regge model is built from Wigner 6j symbols.

  U1  The TEGR identity T = -R + B holds in 3D as in 4D (CHECK, reusing stur_tegr).
  U2  An exact 6j symbol (Racah's formula, rational arithmetic), checked against sympy.
  U3  Ponzano-Regge (1968): for large spins the 6j symbol is
          {6j} ~ cos(sum_e (j_e + 1/2) theta_e + pi/4) / sqrt(12 pi V),
      where the tetrahedron has edge lengths j_e + 1/2, volume V and exterior dihedral
      angles theta_e. The phase is the Regge action of discrete 3D gravity. (CHECK)
  U4  Biedenharn-Elliott identity = invariance under the 2-3 Pachner move: the amplitude
      does not depend on the triangulation, so there are no local degrees of freedom.
      Orthogonality of the 6j symbols = the 1-4 move up to a divergent factor. (CHECK)
Labels: KNOWN, CHECK (computed here).
"""
import math
import random
from fractions import Fraction as F
from math import factorial as fa

import numpy as np
import sympy as sp

import stur_tegr


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# --------------------------------------------------------------------------- U1
def identity_3d(points=2):
    """T + R - B, exactly, at rational points for a non-diagonal 3D Euclidean tetrad with
    rational entries (so the check is exact arithmetic, not floating point).
    Returns rows (T + R - B, T, R)."""
    x, y, z = sp.symbols("x y z", real=True)
    X = [x, y, z]
    E = sp.Matrix([[1 + x * y / 3, z / 13, 0], [0, 2 + x * z / 5, x / 17], [y / 7, 0, 1 + y**2 / 11]])
    T, Bd, g, ginv, e = stur_tegr.torsion_parts(E, X, sp.eye(3))
    R = stur_tegr.ricci_scalar(g, ginv, X)
    pts = [{x: sp.Rational(1, 3), y: sp.Rational(-2, 5), z: sp.Rational(4, 7)},
           {x: -1, y: sp.Rational(1, 2), z: sp.Rational(1, 3)}][:points]
    return [(sp.simplify((T + R - Bd).subs(p)), float(T.subs(p)), float(R.subs(p))) for p in pts]


# --------------------------------------------------------------------------- U2
def _tri(a, b, c):
    """Triangle condition on doubled spins."""
    return (a + b + c) % 2 == 0 and abs(a - b) <= c <= a + b


def _delta2(a, b, c):
    """Squared triangle coefficient, doubled spins."""
    return F(fa((a + b - c) // 2) * fa((a - b + c) // 2) * fa((-a + b + c) // 2),
             fa((a + b + c) // 2 + 1))


def sixj(j1, j2, j3, j4, j5, j6):
    """Wigner 6j symbol {j1 j2 j3; j4 j5 j6} by Racah's formula, exact until the final
    square root. Spins are ints or Fractions; returns 0.0 if a triangle fails."""
    a, b, c, d, e, f = (int(2 * F(j)) for j in (j1, j2, j3, j4, j5, j6))
    tris = [(a, b, c), (a, e, f), (d, b, f), (d, e, c)]
    if not all(_tri(*t) for t in tris):
        return 0.0
    pref2 = F(1)
    for t in tris:
        pref2 *= _delta2(*t)
    s = [sum(t) // 2 for t in tris]
    p = [(a + b + d + e) // 2, (a + c + d + f) // 2, (b + c + e + f) // 2]
    tot = F(0)
    for zz in range(max(s), min(p) + 1):
        den = 1
        for v in s:
            den *= fa(zz - v)
        for v in p:
            den *= fa(v - zz)
        tot += F((-1) ** zz * fa(zz + 1), den)
    if tot == 0:
        return 0.0
    return math.copysign(math.sqrt(float(tot * tot * pref2)), 1 if tot > 0 else -1)


def check_against_sympy(n=30, seed=1):
    """Largest |difference| from sympy's wigner_6j over n admissible random cases."""
    from sympy.physics.wigner import wigner_6j
    rng, worst, done = random.Random(seed), 0.0, 0
    while done < n:
        v = [F(rng.randint(0, 8), 2) for _ in range(6)]
        mine = sixj(*v)
        if mine:
            worst = max(worst, abs(mine - float(sp.N(wigner_6j(*v), 20))))
            done += 1
    return worst


# --------------------------------------------------------------------------- U3
EDGES = [(0, 1), (1, 2), (0, 2), (2, 3), (0, 3), (1, 3)]   # j1..j6 as edges P_i P_k


def tetrahedron(lengths):
    """Volume and exterior dihedral angles of the Euclidean tetrahedron with the given
    edge lengths, in the order of the 6j symbol: j1, j2, j3 bound one face and j4, j5, j6
    are their opposite edges. Returns None if no Euclidean tetrahedron exists."""
    D = np.zeros((4, 4))
    for (i, k), l in zip(EDGES, lengths):
        D[i, k] = D[k, i] = l * l
    G = np.array([[(D[0, i] + D[0, k] - D[i, k]) / 2 for k in (1, 2, 3)] for i in (1, 2, 3)])
    V2 = np.linalg.det(G) / 36
    if V2 <= 0:
        return None
    P = np.zeros((4, 3))
    P[1:] = np.linalg.cholesky(G)
    cen = P.mean(0)
    theta = []
    for i, k in EDGES:
        normals = []
        for m in (q for q in range(4) if q not in (i, k)):
            nv = np.cross(P[k] - P[i], P[m] - P[i])
            if np.dot(nv, P[i] - cen) < 0:
                nv = -nv                                   # outward
            normals.append(nv / np.linalg.norm(nv))
        theta.append(math.acos(max(-1.0, min(1.0, float(np.dot(*normals))))))
    return math.sqrt(V2), theta


def ponzano_regge(js):
    """(asymptotic value, envelope 1/sqrt(12 pi V), Regge action) for spins js."""
    L = [float(j) + 0.5 for j in js]
    V, th = tetrahedron(L)
    S = sum(l * t for l, t in zip(L, th))
    env = 1 / math.sqrt(12 * math.pi * V)
    return env * math.cos(S + math.pi / 4), env, S


def pr_scan(base=(5, 6, 7, 6, 5, 6), scales=(2, 5, 10, 20, 40)):
    """Exact 6j vs Ponzano-Regge along k * base. Rows (k, exact, asymptotic, err/envelope)."""
    rows = []
    for k in scales:
        js = [k * b for b in base]
        ex = sixj(*js)
        a, env, _ = ponzano_regge(js)
        rows.append((k, ex, a, abs(ex - a) / env))
    return rows


def pr_rms(k=20, base=(5, 6, 7, 6, 5, 6), spread=3):
    """RMS of (exact - asymptotic)/envelope over spins within +-spread of k * base, varying
    j1 and j4 together (keeps the triangle conditions)."""
    errs = []
    for d1 in range(-spread, spread + 1):
        for d4 in range(-spread, spread + 1):
            js = [k * b for b in base]
            js[0] += d1
            js[3] += d4
            if sixj(*js) == 0:
                continue
            a, env, _ = ponzano_regge(js)
            errs.append(((sixj(*js) - a) / env) ** 2)
    return math.sqrt(sum(errs) / len(errs)), len(errs)


# --------------------------------------------------------------------------- U4
def biedenharn_elliott(a, b, c, d, e, f, p, q, r):
    """(LHS, RHS) of
       sum_x (-1)^(S+x) (2x+1) {a b x; c d p}{c d x; e f q}{e f x; b a r}
           = {p q r; e a d}{p q r; f b c},     S = a+b+c+d+e+f+p+q+r."""
    S = a + b + c + d + e + f + p + q + r
    lhs = 0.0
    top = int(2 * max(a + b, c + d, e + f)) + 1
    for x2 in range(top + 1):
        x = F(x2, 2)
        t = sixj(a, b, x, c, d, p) * sixj(c, d, x, e, f, q) * sixj(e, f, x, b, a, r)
        if t:
            lhs += (-1) ** int(S + x) * (2 * x + 1) * t
    return lhs, sixj(p, q, r, e, a, d) * sixj(p, q, r, f, b, c)


def be_check(n_nonzero=40, jmax2=6, seed=3):
    """Worst |LHS - RHS| over n random spin sets with RHS != 0 (spins up to jmax2/2)."""
    rng, worst, hits, tries = random.Random(seed), 0.0, 0, 0
    while hits < n_nonzero:
        tries += 1
        v = [F(rng.randint(0, jmax2), 2) for _ in range(9)]
        if sixj(v[6], v[7], v[8], v[4], v[0], v[3]) == 0 or sixj(v[6], v[7], v[8], v[5], v[1], v[2]) == 0:
            continue
        lhs, rhs = biedenharn_elliott(*v)
        worst = max(worst, abs(lhs - rhs))
        hits += 1
    return worst, hits


def orthogonality(a, b, c, d):
    """Matrix M_pq = sum_x (2x+1)(2p+1) {a b x; c d p}{a b x; c d q}: the identity on the
    admissible p, q."""
    ps = [F(k, 2) for k in range(int(2 * max(abs(a - d), abs(b - c))), int(2 * min(a + d, b + c)) + 1, 2)]
    xs = [F(k, 2) for k in range(0, int(2 * (a + b)) + 1)]
    M = np.zeros((len(ps), len(ps)))
    for i, p in enumerate(ps):
        for k, q in enumerate(ps):
            M[i, k] = sum(float(2 * x + 1) * float(2 * p + 1) * sixj(a, b, x, c, d, p) * sixj(a, b, x, c, d, q)
                          for x in xs)
    return ps, M


# --------------------------------------------------------------------------- main
def main():
    banner("U1  The TEGR identity in 3D: T = -R + B (CHECK)")
    for dlt, T, R in identity_3d():
        print(f"   T = {T:+.6e}   R = {R:+.6e}   T + R - B = {dlt}  (exact)")
    print("   FOLLOWS: as in 4D, 3D TEGR and 3D GR differ by a boundary term.")

    banner("U2  Exact 6j symbols (Racah's formula)")
    print(f"   Worst difference from sympy.physics.wigner over 30 cases: {check_against_sympy():.1e}")
    print(f"   {{1 1 1; 1 1 1}} = {sixj(1, 1, 1, 1, 1, 1):+.10f}   (exact: 1/6)")

    banner("U3  Ponzano-Regge asymptotics: the 6j symbol knows the Regge action (CHECK)")
    for k, ex, a, err in pr_scan():
        js = [k * b for b in (5, 6, 7, 6, 5, 6)]
        print(f"   j = {js}:  exact {ex:+.6e}   asymptotic {a:+.6e}   |diff|/envelope {err:.1e}")
    rms, n = pr_rms()
    print(f"   RMS |diff|/envelope over {n} spins near k = 20: {rms:.1e}")
    print("   KNOWN (Ponzano-Regge 1968; proved by Roberts 1999): the phase is the Regge")
    print("   action sum (j + 1/2) theta of a flat tetrahedron, so the large-spin limit of the")
    print("   quantum amplitude is classical 3D gravity.")

    banner("U4  Triangulation independence: the 2-3 move and orthogonality (CHECK)")
    worst, hits = be_check()
    print(f"   Biedenharn-Elliott identity, {hits} random spin sets: worst |LHS - RHS| = {worst:.1e}")
    ps, M = orthogonality(1, F(3, 2), 1, F(3, 2))
    print(f"   Orthogonality for (a, b, c, d) = (1, 3/2, 1, 3/2), p in {[str(p) for p in ps]}:"
          f" max |M - 1| = {np.abs(M - np.eye(len(ps))).max():.1e}")
    print("   KNOWN: the 2-3 move leaves the Ponzano-Regge amplitude unchanged, so it does not")
    print("   depend on how space is cut into tetrahedra. That is the quantum statement that")
    print("   3D gravity has no local degrees of freedom. The Ponzano-Regge model is the")
    print("   amplitude of the standard loop quantization; Delcamp, Freidel and Girelli")
    print("   (1803.03246) construct the dual, flat-first (teleparallel) quantization of the")
    print("   same BF theory. This notebook does not reproduce their construction.")


if __name__ == "__main__":
    main()
