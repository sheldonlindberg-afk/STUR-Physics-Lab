#!/usr/bin/env python3
"""
The frame as a corner degree of freedom: linearized TEGR's corner symplectic form.

First step toward the quantum question of QUANTUM_TEGR.md, section 6: before the frame can
be quantized, one needs to know what it is canonically conjugate to on an entangling
surface. Linearize around Minkowski in the Weitzenboeck gauge (omega = 0, Cartesian):
e^a_mu = delta^a_mu + B^a_mu, B_{rho nu} = s_{rho nu} + a_{rho nu}, s symmetric (metric
perturbation, h = 2 s) and a antisymmetric (the linearized frame: a local Lorentz
rotation). L = -T / 16 pi with T quadratic in the linear torsion
T_{rho mu nu} = d_mu B_{rho nu} - d_nu B_{rho mu}. G = 1.

  Q1  L(s + a) - L(s) has identically vanishing Euler-Lagrange derivatives: the frame is
      pure gauge in the bulk (a total derivative). KNOWN (local Lorentz invariance of
      TEGR up to a boundary term). (CHECK)
  Q2  The frame part of the symplectic current, omega(d1, d2) - omega_s(d1, d2), is
      divergence-free off shell, and equals d_nu W^{mu nu} for a unique covariant corner
      2-form W bilinear in (d1 B, d2 B). W has no s-s part. (CHECK)
  Q3  On the entangling plane t = const, x = 0:
        W^{tx} = (1/8 pi) [ -d a_01 ^ d(s_22 + s_33) + d a_02 ^ d B_12 + d a_03 ^ d B_13
                            - d a_12 ^ d B_02 - d a_13 ^ d B_03 ]
      a_01 = -eta (eta the rapidity of the frame's boost normal to the surface) and
      s_22 + s_33 = delta sqrt(sigma), the linearized area density. So the corner form
      contains (1/8 pi G) int d eta ^ d sqrt(sigma): the frame's normal boost is conjugate
      to area / 8 pi G, the pair of Carlip and Teitelboim (gr-qc/9312002). The rotation in
      the surface, a_23, pairs with nothing. (CHECK; the pairing is KNOWN in metric and
      tetrad variables, found here for TEGR's frame.)
  Q4  Cross-check with stur_tegr_corner K5 (nonlinear, Euclidean): the frame winding at
      rate k shifts the tip term by (A/4)(k/kappa) = (A/8 pi) x (k beta), i.e. A/8 pi times
      the frame's total rotation angle, the same coefficient. (CHECK)
Labels: KNOWN, CHECK (computed here).
"""
import sympy as sp

X = sp.symbols("t x y z", real=True)
N4 = 4
ETA = [-1, 1, 1, 1]


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def fields(tag):
    """Symmetric s and antisymmetric a as arbitrary functions of (t, x, y, z)."""
    s = [[None] * N4 for _ in range(N4)]
    a = [[0] * N4 for _ in range(N4)]
    for i in range(N4):
        for j in range(i, N4):
            s[i][j] = s[j][i] = sp.Function(f"{tag}s{i}{j}")(*X)
        for j in range(i + 1, N4):
            F = sp.Function(f"{tag}a{i}{j}")(*X)
            a[i][j], a[j][i] = F, -F
    return s, a


def add(s, a):
    return [[s[i][j] + a[i][j] for j in range(N4)] for i in range(N4)]


def lagrangian_of_torsion(T):
    """-T_scalar / 16 pi with T_{rho mu nu} all lower (Minkowski, as in stur_tegr)."""
    n, e = N4, ETA
    U = [[[e[r] * e[m] * e[v] * T[r][m][v] for v in range(n)] for m in range(n)] for r in range(n)]
    s1 = sum(U[r][m][v] * T[r][m][v] for r in range(n) for m in range(n) for v in range(n))
    s2 = sum(U[r][m][v] * T[v][m][r] for r in range(n) for m in range(n) for v in range(n))
    V = [sum(e[r] * T[r][r][m] for r in range(n)) for m in range(n)]
    s3 = sum(e[m] * V[m] ** 2 for m in range(n))
    return -(sp.Rational(1, 4) * s1 + sp.Rational(1, 2) * s2 - s3) / (16 * sp.pi)


def torsion(B):
    return [[[sp.diff(B[r][v], X[m]) - sp.diff(B[r][m], X[v]) for v in range(N4)] for m in range(N4)]
            for r in range(N4)]


def euler_lagrange(L, F):
    out = sp.diff(L, F)
    for m in range(N4):
        out -= sp.diff(sp.diff(L, sp.Derivative(F, X[m])), X[m])
    return sp.expand(out)


# --------------------------------------------------------------------------- Q1
def frame_is_pure_gauge():
    """Fields whose E-L derivative of L(s + a) - L(s) is nonzero (expect none), and a
    control: the E-L derivative of L(s) with respect to s_00 (expect nonzero)."""
    s, a = fields("")
    dL = sp.expand(lagrangian_of_torsion(torsion(add(s, a))) - lagrangian_of_torsion(torsion(s)))
    allf = [s[i][j] for i in range(N4) for j in range(i, N4)] + [a[i][j] for i in range(N4) for j in range(i + 1, N4)]
    bad = [str(F.func) for F in allf if euler_lagrange(dL, F) != 0]
    control = euler_lagrange(sp.expand(lagrangian_of_torsion(torsion(s))), s[0][0]) != 0
    return bad, control


# --------------------------------------------------------------------------- Q2
def _momentum_map():
    """Pi^{mu, rho nu} = dL / d(d_mu B_{rho nu}) as linear functions of P = dB."""
    P = [[[sp.Symbol(f"P{r}{v}{m}") for m in range(N4)] for v in range(N4)] for r in range(N4)]
    T = [[[P[r][v][m] - P[r][m][v] for v in range(N4)] for m in range(N4)] for r in range(N4)]
    L = sp.expand(lagrangian_of_torsion(T))
    return P, [[[sp.diff(L, P[r][v][m]) for v in range(N4)] for r in range(N4)] for m in range(N4)]


def symplectic_current(B1, B2):
    P, Pi = _momentum_map()

    def at(B):
        sub = {P[r][v][m]: sp.diff(B[r][v], X[m]) for r in range(N4) for v in range(N4) for m in range(N4)}
        return [[[Pi[m][r][v].xreplace(sub) for v in range(N4)] for r in range(N4)] for m in range(N4)]
    P1, P2 = at(B1), at(B2)
    return [sp.expand(sum(P1[m][r][v] * B2[r][v] - P2[m][r][v] * B1[r][v] for r in range(N4) for v in range(N4)))
            for m in range(N4)]


def _structures():
    e = ETA
    UU = lambda B, i, j: e[i] * e[j] * B[i][j]
    UL = lambda B, i, j: e[i] * B[i][j]
    LU = lambda B, i, j: e[j] * B[i][j]
    tr = lambda B: sum(e[i] * B[i][i] for i in range(N4))
    return [
        ("B^{mn} tr B'", lambda P, Q, m, v: UU(P, m, v) * tr(Q)),
        ("B^{nm} tr B'", lambda P, Q, m, v: UU(P, v, m) * tr(Q)),
        ("B^{ma} B'^n_a", lambda P, Q, m, v: sum(UU(P, m, k) * UL(Q, v, k) for k in range(N4))),
        ("B^{am} B'_a^n", lambda P, Q, m, v: sum(UU(P, k, m) * LU(Q, k, v) for k in range(N4))),
        ("B^{ma} B'_a^n", lambda P, Q, m, v: sum(UU(P, m, k) * LU(Q, k, v) for k in range(N4))),
        ("B^{am} B'^n_a", lambda P, Q, m, v: sum(UU(P, k, m) * UL(Q, v, k) for k in range(N4))),
    ]


def corner_form():
    """Solve d_nu W^{mu nu} = (frame part of omega) for a covariant W. Returns
    (divergence check, solution dict, W^{tx} expression, fields used)."""
    s1, a1 = fields("A")
    s2, a2 = fields("C")
    B1, B2 = add(s1, a1), add(s2, a2)
    w = symplectic_current(B1, B2)
    ws = symplectic_current(s1, s2)
    wa = [sp.expand(w[m] - ws[m]) for m in range(N4)]
    div_zero = sp.expand(sum(sp.diff(wa[m], X[m]) for m in range(N4))) == 0
    st = _structures()
    c = sp.symbols(f"c0:{len(st)}")

    def Wk(k, m, v):
        S = st[k][1]
        return S(B1, B2, m, v) - S(B1, B2, v, m) - S(B2, B1, m, v) + S(B2, B1, v, m)
    W = [[sum(c[k] * Wk(k, m, v) for k in range(len(st))) for v in range(N4)] for m in range(N4)]
    resid = [sp.expand(sum(sp.diff(W[m][v], X[v]) for v in range(N4)) - wa[m]) for m in range(N4)]
    atoms = set()
    for R in resid:
        atoms |= R.atoms(sp.Derivative) | {f for f in R.atoms(sp.Function)}
    order = sorted(atoms, key=lambda q: -len(str(q)))                 # derivatives first
    syms = {q: sp.Symbol(f"j{i}") for i, q in enumerate(order)}
    eqs = []
    for R in resid:
        eqs += sp.Poly(R.xreplace(syms), *syms.values()).coeffs()
    sol = sp.solve(eqs, c, dict=True)
    if len(sol) != 1:
        raise RuntimeError("corner form not found")
    fixed = {k: sp.sympify(sol[0].get(k, 0)).subs({q: 0 for q in c}) for k in c}   # free -> 0
    Wtx = sp.expand(W[0][1].subs(fixed))
    return div_zero, sol[0], fixed, [st[k][0] for k in range(len(st))], Wtx, (s1, a1, s2, a2)


def pairings(Wtx, flds):
    """Coefficient (times 8 pi) of each frame component of variation 1 in W^{tx}."""
    s1, a1, s2, a2 = flds
    out = {}
    for (i, j) in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
        out[f"a{i}{j}"] = sp.expand(sp.diff(Wtx, a1[i][j]) * 8 * sp.pi)
    ss = sp.expand(Wtx.xreplace({f: 0 for f in Wtx.atoms(sp.Function) if "a" in f.func.__name__[1:]}))
    return out, ss


# --------------------------------------------------------------------------- Q4
def k5_coefficient():
    """From stur_tegr_corner K5: tip term / (A/4) = 1 + k/kappa. The shift per unit total
    frame angle (k beta) in units of A: (A/4)(k/kappa) / (A k beta) with beta = 2 pi/kappa."""
    k, kappa = sp.symbols("k kappa", positive=True)
    beta = 2 * sp.pi / kappa
    return sp.simplify(sp.Rational(1, 4) * (k / kappa) / (k * beta))


# --------------------------------------------------------------------------- main
def main():
    banner("Q1  The frame is pure gauge in the bulk of linearized TEGR (CHECK)")
    bad, control = frame_is_pure_gauge()
    print(f"   Fields with nonzero E-L derivative of L(s + a) - L(s): {bad or 'none'}")
    print(f"   Control, E-L of L(s) w.r.t. s_00 nonzero: {control}")
    print("   KNOWN: TEGR is locally Lorentz invariant up to a boundary term.")

    banner("Q2  The frame's part of the symplectic current is a corner term (CHECK)")
    div_zero, sol, fixed, names, Wtx, flds = corner_form()
    print(f"   Off-shell divergence of the frame part of omega vanishes: {div_zero}")
    print("   Covariant fit d_nu W^{mu nu} = omega_frame^mu, W antisymmetric in mu nu and in 1 <-> 2:")
    for nm, k in zip(names, sp.symbols(f"c0:{len(names)}")):
        print(f"      {nm:16s} {sol.get(k, 'free')}")
    print("   The free parameters multiply structures that coincide after antisymmetrizing,")
    print("   so W is unique.")

    banner("Q3  On the plane t = const, x = 0: what the frame is conjugate to (CHECK)")
    pr, ss = pairings(Wtx, flds)
    print(f"   s-s part of W^(tx): {ss}")
    for kk, v in pr.items():
        print(f"   8 pi x coefficient of d1 {kk}: {v}")
    print("   a_01 = -eta (normal boost rapidity); s_22 + s_33 = delta sqrt(sigma) (area density).")
    print("   So W^(tx) contains (1/8 pi) d eta ^ d sqrt(sigma): the frame's normal boost is")
    print("   conjugate to area / 8 pi G (Carlip and Teitelboim, gr-qc/9312002, in metric")
    print("   variables). The in-surface rotation a_23 pairs with nothing: still gauge.")

    banner("Q4  Same coefficient from the nonlinear Euclidean action (stur_tegr_corner K5)")
    print(f"   Tip-term shift per unit area per unit frame angle: {k5_coefficient()} = 1/(8 pi)")


if __name__ == "__main__":
    main()
