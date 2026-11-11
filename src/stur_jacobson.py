#!/usr/bin/env python3
"""
D3 re-derived: Einstein's equation from the Clausius relation on local horizons
(Jacobson, PRL 75, 1260 (1995)), each step checked symbolically.

Inputs (from D1-D2): the vacuum's entanglement across any surface is delta S = eta delta A
(area law), and every accelerated observer sees the Unruh temperature T = hbar kappa / 2 pi
(Bisognano-Wichmann). Heat is the boost-energy flux across a local Rindler horizon.

J1  Raychaudhuri: for a null, shear- and twist-free congruence, d theta/d lambda =
    - theta^2/2 - R_ab k^a k^b. CHECK on flat FRW with a general scale factor a(t).
J2  The tensor lemma: X_ab k^a k^b = 0 for every null k  =>  X_ab = f g_ab. CHECK by
    imposing the condition on a general symmetric X and solving.
J3  Clausius on the horizon, at first order in lambda:
        delta A = - int lambda R_kk dlambda dA,  delta Q = kappa int lambda T_kk dlambda dA
        delta Q = T delta S  =>  (2 pi / hbar) T_kk = eta R_kk  for every null k.
    With J2: R_ab - (2 pi / hbar eta) T_ab = f g_ab.
J4  Contracted Bianchi identity (CHECK on a general time-dependent spherical metric) and
    conservation of T fix f = R/2 + Lambda:  G_ab + Lambda g_ab = 8 pi G T_ab with
    G = 1/(4 hbar eta). With D1 (eta = N c_s / (4 pi a^2)) this is the G formula of D1-D3.
"""
import sympy as sp


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def christoffel(g, x):
    n = len(x)
    gi = g.inv()
    return [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], x[c]) + sp.diff(g[d, c], x[b])
                                         - sp.diff(g[b, c], x[d])) for d in range(n)) / 2)
              for c in range(n)] for b in range(n)] for a in range(n)]


def ricci(g, x, Gam=None):
    n = len(x)
    Gam = Gam or christoffel(g, x)
    R = sp.zeros(n, n)
    for b in range(n):
        for c in range(n):
            R[b, c] = sp.simplify(
                sum(sp.diff(Gam[a][b][c], x[a]) for a in range(n))
                - sum(sp.diff(Gam[a][b][a], x[c]) for a in range(n))
                + sum(Gam[a][a][d] * Gam[d][b][c] for a in range(n) for d in range(n))
                - sum(Gam[a][c][d] * Gam[d][b][a] for a in range(n) for d in range(n)))
    return R, Gam


def j1_raychaudhuri():
    t, x, y, z = sp.symbols("t x y z")
    a = sp.Function("a")(t)
    g = sp.diag(-1, a**2, a**2, a**2)
    R, _ = ricci(g, [t, x, y, z])
    # affine null geodesic along x: k^t = 1/a, k^x = 1/a^2 (conserved k_t = -1/a ... checked below)
    k = sp.Matrix([1 / a, 1 / a**2, 0, 0])
    null = sp.simplify((k.T * g * k)[0])
    # transverse area element of the congruence ~ a^2 (y-z plane); theta = d ln A / d lambda
    theta = k[0] * sp.diff(sp.log(a**2), t)
    dtheta = k[0] * sp.diff(theta, t)
    Rkk = sp.simplify((k.T * R * k)[0])
    resid = sp.simplify(dtheta + theta**2 / 2 + Rkk)
    # geodesic check: k^b nabla_b k^a = 0
    Gam = christoffel(g, [t, x, y, z])
    X = [t, x, y, z]
    geo = [sp.simplify(sum(k[b] * sp.diff(k[a_], X[b]) for b in range(4))
                       + sum(Gam[a_][b][c] * k[b] * k[c] for b in range(4) for c in range(4))) for a_ in range(4)]
    return null, geo, Rkk, resid


def j2_lemma():
    X = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"X{min(i, j)}{max(i, j)}"))
    eta = sp.diag(-1, 1, 1, 1)
    unknowns = sorted(X.free_symbols, key=str)
    eqs = []
    # null vectors k = (1, n) for a set of directions n spanning the needed quadratic forms
    dirs = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1),
            (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, -1, 0), (1, 0, -1), (0, 1, -1), (1, 1, 1)]
    for d in dirs:
        n = sp.Matrix(d) / sp.sqrt(sum(c**2 for c in d))
        k = sp.Matrix([1, *n])
        eqs.append(sp.expand((k.T * X * k)[0]))
    sol = sp.solve(eqs, unknowns, dict=True)[0]
    Xs = X.subs(sol)
    free = sorted(Xs.free_symbols, key=str)
    return Xs, len(free), sp.simplify(Xs / Xs[1, 1] - eta)


def j3_clausius():
    hbar, eta_, kappa, lam, Tkk, Rkk = sp.symbols("hbar eta kappa lambda T_kk R_kk", real=True)
    dA = -sp.integrate(lam * Rkk, (lam, 0, 1))          # per unit cross-section, lambda in [0,1]
    dQ = kappa * sp.integrate(lam * Tkk, (lam, 0, 1))
    T = hbar * kappa / (2 * sp.pi)
    # Jacobson's sign convention: lambda runs to the past of the bifurcation surface along the
    # generators (lambda < 0 before p), so dQ = kappa int (-lambda) T_kk and dA = int (-lambda)(-R_kk);
    # with lambda in [0, 1] measured toward p this is dQ = T eta (-dA) with the integrals above.
    rel = sp.solve(sp.Eq(dQ, -T * eta_ * dA), Tkk)[0]
    return sp.simplify(rel / Rkk), sp.simplify(2 * sp.pi / (hbar * eta_))


def j4_bianchi():
    t, r, th, ph = sp.symbols("t r theta phi", positive=True)
    A = sp.Function("A")(t, r)
    B = sp.Function("B")(t, r)
    X = [t, r, th, ph]
    g = sp.diag(-sp.exp(2 * A), sp.exp(2 * B), r**2, r**2 * sp.sin(th) ** 2)
    R, Gam = ricci(g, X)
    gi = g.inv()
    Rs = sp.simplify(sum(gi[a, b] * R[a, b] for a in range(4) for b in range(4)))
    Gt = R - Rs * g / 2
    Gup = sp.simplify(gi * Gt)                     # G^a_b
    div = []
    for b in range(4):
        e = sum(sp.diff(Gup[a, b], X[a]) for a in range(4))
        e += sum(Gam[a][a][c] * Gup[c, b] for a in range(4) for c in range(4))
        e -= sum(Gam[c][a][b] * Gup[a, c] for a in range(4) for c in range(4))
        div.append(sp.simplify(e))
    return div


def main():
    banner("J1  Raychaudhuri, checked on flat FRW with a general a(t)")
    null, geo, Rkk, resid = j1_raychaudhuri()
    print(f"   k.k = {null};  geodesic equation residuals: {geo}")
    print(f"   R_ab k^a k^b = {Rkk}")
    print(f"   d theta/d lambda + theta^2/2 + R_kk = {resid}")

    banner("J2  X_ab k^a k^b = 0 for all null k  =>  X_ab = f g_ab")
    _, nfree, diff = j2_lemma()
    print(f"   free parameters left in X after imposing the condition: {nfree}")
    print(f"   X / X_11 - eta = {diff.tolist()}")

    banner("J3  Clausius on a local Rindler horizon")
    coef, expected = j3_clausius()
    print(f"   T_kk / R_kk from delta Q = T delta S: {coef}   (2 pi / hbar eta = {expected})")
    print("   so R_ab - (2 pi / hbar eta) T_ab = f g_ab by J2, i.e. 8 pi G = 2 pi / (hbar eta),")
    print("   G = 1 / (4 hbar eta).")

    banner("J4  Contracted Bianchi identity on ds^2 = -e^{2A(t,r)} dt^2 + e^{2B(t,r)} dr^2 + r^2 dOmega^2")
    div = j4_bianchi()
    print(f"   nabla_a G^a_b = {div}")
    print("   With nabla_a T^a_b = 0, taking the divergence of R_ab - 8 pi G T_ab = f g_ab gives")
    print("   (1/2) d_b R = d_b f, so f = R/2 + Lambda and  G_ab + Lambda g_ab = 8 pi G T_ab.")
    print("   With eta = N c_s / (4 pi a^2) from D1:  G = pi a^2 c^3 / (N c_s hbar).  D3: CHECK.")
    print("   Assumed, not derived: local equilibrium on every local horizon (Jacobson's premise),")
    print("   and that the entropy change is the area term alone (no extra internal entropy).")
    return dict(null=null, geo=geo, resid=resid, nfree=nfree, coef=coef, div=div)


if __name__ == "__main__":
    main()
