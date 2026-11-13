#!/usr/bin/env python3
"""
The gravity rung as a broken gauge theory: MacDowell-Mansouri (1977) and Stelle-West (1980).

Last rung of the symmetry-breaking ladder (SYMMETRY_LADDER.md). Gravity is not produced by
the gauge chain 3-3-1 -> Standard Model -> electromagnetism. But general relativity with a
cosmological constant can itself be written as a gauge theory of the de Sitter group SO(4,1)
whose symmetry is broken to the Lorentz group SO(3,1). This is an established
REFORMULATION (MacDowell and Mansouri, PRL 38 (1977) 739; Stelle and West, PRD 21 (1980)
1466). It gives exactly the predictions of GR + Lambda, and it does not unify gravity with
the other forces.

Conventions: eta_AB = diag(-1, 1, 1, 1, 1), A, B = 0..4; Lorentz indices a, b = 0..3.
Generators (J_AB)^C_D = delta^C_A eta_BD - delta^C_B eta_AD. Connection
    A_mu = (1/2) omega^ab_mu J_ab + (1/l) e^a_mu J_a4,
curvature F_munu = d_mu A_nu - d_nu A_mu + [A_mu, A_nu] (5x5 matrices).

  M1  The algebra. so(4,1) = so(3,1) + 4 "translations" P_a = J_a4 / l, with
      [P_a, P_b] proportional to J_ab / l^2. A de Sitter vector V = (0,0,0,0,l): its
      stabilizer is exactly the 6 Lorentz generators, 4 are broken. In the gauge V = l e_4,
      D V^a = l A^a_4 = e^a: the tetrad is the covariant derivative of the symmetry-breaking
      field (Stelle-West). (CHECK)
  M2  The curvature, on a real spacetime (static, spherical, any f(r)), with the
      Levi-Civita spin connection: F^ab = R^ab + s e^a ^ e^b / l^2 (s computed) and
      F^a4 = T^a / l = 0 (torsion-free). R^ab is checked against the metric's Riemann
      tensor through the Ricci scalar. (CHECK)
  M3  The vacuum: de Sitter space of radius l, f = 1 - r^2/l^2, has F = 0 identically: the
      flat SO(4,1) connection. So R^ab = e^a ^ e^b / l^2 and Lambda = 3 / l^2. (CHECK)
  M4  The action S = N int eps_abcd F^ab ^ F^cd. Pointwise, its density splits into
      eps R^R (Euler) + (2s/l^2) eps R^e^e + (1/l^4) eps e^e^e^e. Each term is computed:
      eps R^e^e = c_R e R, eps e^e^e^e = c_V e; the cosmological constant read off from the
      ratio is 3/l^2, the same as M3; N follows from 1/(16 pi G); and the Euler density is
      a total r-derivative for the static spherical family (it does not change the field
      equations). (CHECK)
  M5  Field equations: Schwarzschild-de Sitter, f = 1 - 2M/r - r^2/l^2, satisfies
      G_munu + Lambda g_munu = 0 with Lambda = 3/l^2. (CHECK)
  M6  Numbers: the measured Lambda (Planck 2018) gives l = sqrt(3/Lambda) ~ 1.6e26 m and the
      dimensionless MacDowell-Mansouri coupling 3/(G Lambda) ~ 1e122 in Planck units: the
      cosmological-constant problem, in this language. (CHECK)
Labels: REFORMULATION, CHECK, LIT (Lambda, G).
"""
import itertools
import math

import sympy as sp

t, r, th, ph = sp.symbols("t r theta phi", real=True)
X = [t, r, th, ph]
N4, N5 = 4, 5
ETA5 = sp.diag(-1, 1, 1, 1, 1)
ETA4 = sp.diag(-1, 1, 1, 1)
l = sp.Symbol("l", positive=True)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def J(A, B):
    """(J_AB)^C_D = delta^C_A eta_BD - delta^C_B eta_AD."""
    M = sp.zeros(N5, N5)
    for C in range(N5):
        for D in range(N5):
            M[C, D] = (1 if C == A else 0) * ETA5[B, D] - (1 if C == B else 0) * ETA5[A, D]
    return M


def algebra():
    """M1."""
    P = [J(a, 4) / l for a in range(4)]
    comm = lambda A_, B_: A_ * B_ - B_ * A_
    pp = all(sp.simplify(comm(P[a], P[b]) + ETA5[4, 4] * J(a, b) / l**2) == sp.zeros(N5, N5)
             for a in range(4) for b in range(4))
    V = sp.Matrix([0, 0, 0, 0, l])
    gens = [(A, B) for A in range(N5) for B in range(A + 1, N5)]
    stab = [(A, B) for A, B in gens if (J(A, B) * V) == sp.zeros(N5, 1)]
    broken = [(A, B) for A, B in gens if (A, B) not in stab]
    return pp, stab, broken


def static_spherical(f):
    E = sp.diag(sp.sqrt(f), 1 / sp.sqrt(f), r, r * sp.sin(th))            # e^a_mu
    g = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th) ** 2)
    return E, g


def christoffel(g):
    gi = g.inv()
    return [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d]))
                              for d in range(N4)) / 2) for c in range(N4)] for b in range(N4)] for a in range(N4)]


def spin_connection(E, g):
    """omega^a_{b mu} = e^a_nu Gamma^nu_{mu lam} e_b^lam - e_b^lam d_mu e^a_lam (Levi-Civita)."""
    Gm = christoffel(g)
    Ei = E.inv()                                                         # Ei[mu, a] = e_a^mu
    w = [[[sp.simplify(sum(E[a, nu] * Gm[nu][mu][lam] * Ei[lam, b] for nu in range(N4) for lam in range(N4))
                       - sum(Ei[lam, b] * sp.diff(E[a, lam], X[mu]) for lam in range(N4)))
           for mu in range(N4)] for b in range(N4)] for a in range(N4)]
    return w


def connection_matrices(E, w, with_e=True):
    """A_mu (5x5) = omega^a_{b mu} (Lorentz block) + (1/l) e^a_mu J_a4."""
    As = []
    for mu in range(N4):
        A = sp.zeros(N5, N5)
        for a in range(N4):
            for b in range(N4):
                A[a, b] = w[a][b][mu]
        if with_e:
            for a in range(N4):
                # from (1/l) e^a J_a4: (J_a4)^C_D = delta^C_a eta_4D - delta^C_4 eta_aD
                for Cc in range(N5):
                    for D in range(N5):
                        A[Cc, D] += E[a, mu] / l * J(a, 4)[Cc, D]
        As.append(A)
    return As


def curvature(As):
    F = [[None] * N4 for _ in range(N4)]
    for m in range(N4):
        for n in range(N4):
            F[m][n] = sp.simplify(sp.diff(As[n], X[m]) - sp.diff(As[m], X[n]) + As[m] * As[n] - As[n] * As[m])
    return F


def ee(E, a, b, m, n):
    return E[a, m] * E[b, n] - E[a, n] * E[b, m]


def curvature_split(f):
    """M2: F^a_b (Lorentz block) minus R^a_b, compared with s (e^a e_b)/l^2; F^a_4."""
    E, g = static_spherical(f)
    w = spin_connection(E, g)
    F = curvature(connection_matrices(E, w, True))
    R = curvature(connection_matrices(E, w, False))
    s_vals, ok, tors = set(), True, True
    for m, n in itertools.combinations(range(N4), 2):
        for a in range(N4):
            for b in range(N4):
                diff = sp.simplify(F[m][n][a, b] - R[m][n][a, b])
                target = sp.simplify(sum(ee(E, a, c, m, n) * ETA4[c, b] for c in range(N4)) / l**2)   # (e^a ^ e_b)/l^2
                if target != 0:
                    s_vals.add(sp.simplify(diff / target))
                elif diff != 0:
                    ok = False
            tors &= all(sp.simplify(F[m][n][a, 4]) == 0 for a in range(N4))
    # Ricci scalar from R^a_b vs from the metric
    Ei = E.inv()
    Rs = sp.simplify(sum(R[m][n][a, b] * Ei[m, a] * Ei[n, c] * ETA4[c, b] for m in range(N4) for n in range(N4)
                         for a in range(N4) for b in range(N4) for c in range(N4) if c == b))
    Rmetric = ricci_scalar(g)
    return s_vals, ok, tors, sp.simplify(Rs - Rmetric), F, R, E, g


def ricci_scalar(g):
    Gm = christoffel(g)
    gi = g.inv()
    Ric = lambda b, c: sum(sp.diff(Gm[a][b][c], X[a]) - sp.diff(Gm[a][b][a], X[c])
                           + sum(Gm[a][a][d] * Gm[d][b][c] - Gm[a][c][d] * Gm[d][b][a] for d in range(N4))
                           for a in range(N4))
    return sp.simplify(sum(gi[b, c] * Ric(b, c) for b in range(N4) for c in range(N4)))


def einstein_tensor(g):
    Gm = christoffel(g)
    gi = g.inv()
    Ric = sp.Matrix(N4, N4, lambda b, c: sp.simplify(sum(sp.diff(Gm[a][b][c], X[a]) - sp.diff(Gm[a][b][a], X[c])
                                                          + sum(Gm[a][a][d] * Gm[d][b][c] - Gm[a][c][d] * Gm[d][b][a] for d in range(N4))
                                                          for a in range(N4))))
    Rs = sp.simplify(sum(gi[b, c] * Ric[b, c] for b in range(N4) for c in range(N4)))
    return sp.simplify(Ric - Rs * g / 2)


def de_sitter_vacuum():
    """M3: F = 0 for f = 1 - r^2/l^2."""
    E, g = static_spherical(1 - r**2 / l**2)
    w = spin_connection(E, g)
    F = curvature(connection_matrices(E, w, True))
    return all(F[m][n] == sp.zeros(N5, N5) for m in range(N4) for n in range(N4))


def eps4(p):
    if len(set(p)) < 4:
        return 0
    s = 1
    for i in range(4):
        for j in range(i + 1, 4):
            if p[i] > p[j]:
                s = -s
    return s


def wedge_density(X2, Y2):
    """eps_abcd X^ab ^ Y^cd as the coefficient of dt dr dth dph: (1/4) eps^{mnrs} eps_abcd X^ab_mn Y^cd_rs.
    X2[(a,b)] -> 4x4 matrix in (mu, nu)."""
    tot = 0
    for a, b, c, d in itertools.permutations(range(4)):
        e_ = eps4([a, b, c, d])
        for m, n, p, q in itertools.permutations(range(4)):
            tot += e_ * eps4([m, n, p, q]) * X2[(a, b)][m, n] * Y2[(c, d)][p, q]
    return sp.simplify(tot / 4)


def action_terms(f):
    """M4: the three densities for static spherical f, upper Lorentz indices X^ab."""
    E, g = static_spherical(f)
    w = spin_connection(E, g)
    R = curvature(connection_matrices(E, w, False))
    Rup = {(a, b): sp.Matrix(N4, N4, lambda m, n: sum(R[m][n][a, c] * ETA4[c, b] for c in range(N4)))
           for a in range(4) for b in range(4)}
    EE = {(a, b): sp.Matrix(N4, N4, lambda m, n: ee(E, a, b, m, n)) for a in range(4) for b in range(4)}
    RR = wedge_density(Rup, Rup)
    REE = wedge_density(Rup, EE)
    EEEE = wedge_density(EE, EE)
    e = sp.simplify(E.det())
    Rs = ricci_scalar(g)
    cR = sp.simplify(REE / (e * Rs)) if Rs != 0 else None
    cV = sp.simplify(EEEE / e)
    return RR, REE, EEEE, cR, cV, e, Rs


def main():
    banner("M1  so(4,1) -> so(3,1): the algebra and the breaking (CHECK)")
    pp, stab, broken = algebra()
    print(f"   [P_a, P_b] = -eta_44 J_ab / l^2 for all a, b: {pp}")
    print(f"   Stabilizer of V = (0,0,0,0,l): {len(stab)} generators J_ab with a, b < 4: {stab}")
    print(f"   Broken: {len(broken)} generators {broken} (the 'translations')")
    print("   In the gauge V = l e_4, D V^a = l A^a_4 = e^a: the tetrad is the broken direction.")

    banner("M2  The curvature splits into Riemann + (e ^ e)/l^2 + torsion/l (CHECK)")
    f = sp.Function("f")(r)
    s_vals, ok, tors, dR, F, R, E, g = curvature_split(f)
    print(f"   F^ab - R^ab = s (e^a ^ e^b)/l^2 with s = {s_vals}  (all components consistent: {ok})")
    print(f"   F^a4 = 0 (Levi-Civita: no torsion): {tors}")
    print(f"   Ricci scalar from R^ab minus from the metric: {dR}")

    banner("M3  The vacuum: de Sitter space of radius l is the flat SO(4,1) connection (CHECK)")
    print(f"   F = 0 identically for f = 1 - r^2/l^2: {de_sitter_vacuum()}  ->  Lambda = 3/l^2")

    banner("M4  The MacDowell-Mansouri action (CHECK)")
    RR, REE, EEEE, cR, cV, e, Rs = action_terms(f)
    s = list(s_vals)[0]
    print(f"   eps R^e^e = c_R e R with c_R = {cR};  eps e^e^e^e = c_V e with c_V = {cV}")
    LamB = sp.simplify(-(s**2 / l**4 * cV) / (2 * (2 * s / l**2) * cR))   # match N[(2s/l^2) c_R R + (s^2/l^4) c_V] to R - 2 Lambda
    print(f"   eps F^F = eps R^R + (2s/l^2) c_R e R + (s^2/l^4) c_V e  ->  e (R - 2 Lambda) with Lambda = {LamB}")
    G = sp.Symbol("G", positive=True)
    Nn = sp.simplify(1 / (16 * sp.pi * G) / (2 * s / l**2 * cR))
    Lam = sp.Symbol("Lambda", positive=True)
    print(f"   Normalization for 1/(16 pi G): N = {Nn} = {sp.simplify(Nn.subs(l, sp.sqrt(3 / Lam)))}")
    print(f"   Euler density eps R^R = {sp.factor(RR)}")
    prim = 4 * (f * sp.diff(f, r) - sp.diff(f, r))
    print(f"   = sin(theta) d/dr[{prim}]: {sp.simplify(sp.diff(prim, r) * sp.sin(th) - RR) == 0}"
          "  (a total derivative; KNOWN in general: the Chern-Gauss-Bonnet density)")

    banner("M5  Schwarzschild-de Sitter solves G + Lambda g = 0 with Lambda = 3/l^2 (CHECK)")
    M = sp.Symbol("M", positive=True)
    _, gS = static_spherical(1 - 2 * M / r - r**2 / l**2)
    Gt = einstein_tensor(gS)
    print(f"   G_munu + (3/l^2) g_munu = 0: {sp.simplify(Gt + 3 / l**2 * gS) == sp.zeros(4, 4)}")

    banner("M6  Numbers (LIT: Lambda from Planck 2018, G from CODATA)")
    Lam_si = 1.1056e-52          # m^-2: Planck 2018 with BAO, 3 H0^2 Omega_L / c^2 (H0 = 67.66, Omega_L = 0.6889);
                                 # Planck's own quoted Lambda, without BAO, is 1.089e-52 (see AUDIT.md)
    lP2 = 1.616255e-35 ** 2
    ell = math.sqrt(3 / Lam_si)
    print(f"   l = sqrt(3/Lambda) = {ell:.3e} m = {ell / 9.4607e15 / 1e9:.1f} billion light years")
    print(f"   MacDowell-Mansouri coupling 3/(G Lambda) in Planck units = 3/(l_P^2 Lambda) = {3 / (lP2 * Lam_si):.2e}")
    print("   REFORMULATION: the same predictions as GR + Lambda; it does not unify gravity with 3-3-1.")


if __name__ == "__main__":
    main()
