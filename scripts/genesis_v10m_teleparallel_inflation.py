#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10m: scalarons and scalar perturbations in teleparallel
gravity, computed (replaces the argued claim 'f(T) has no scalaron')
================================================================================
Conventions: metric signature (-,+,+,+); Weitzenboeck torsion T^r_{mn} =
e_A^r (d_m e^A_n - d_n e^A_m); T = T^{rmn}T_{rmn}/4 + T^{rmn}T_{nmr}/2 - T^r_{mr}T^{nm}_n,
which gives T = +6H^2 on flat FRW. GR is L = -e T/2 (M_Pl = 1); R = -T + B with
B = -(2/e) d_m(e T^{r m}_r) (sign fixed by FRW: B = 6(a''/a + 2H^2)).

PART A  minisuperspace (flat FRW, lapse N): differential order of the equations
        and linearised modes, for GR, f(R) = R + R^2/6M^2 and f(T) = T + beta T^2.
        Gate: f(R) must show the Starobinsky scalaron at mass M.
PART B  second-order scalar action, comoving gauge (delta chi = 0), Fourier mode
        along x, for  L = -e[G + S(T-T0) + Q(T-T0)^2/2]/2 + e[chi_dot^2/2N^2 - V]
        with all scalar tetrad fields: lapse, shift, curvature zeta and the local
        Lorentz boost (rapidity d_x lambda). This covers GR (S=1,Q=0), f(T)
        (S=f_T, Q=f_TT) and STUR's F(chi)T (S = F = 2 alpha chi, Q = 0).
        Gates: GR reduces to Mukhanov's action; the boost decouples in GR.
        Then: the boundary-term coupling +e D(chi) B/2, giving the condition for
        a propagating scalar in F(chi)T + D(chi)B theories.
PART C  f(T): exact k-scan of the reduced action on a numerical background.
PART D  counterfactual: if STUR's coupling were alpha|R| R (scalar-curvature),
        n_s and r (Einstein frame, parameter-free for v << chi).

Runtime ~15 min (the two symbolic tetrad expansions dominate).
Usage:  python genesis_v10m_teleparallel_inflation.py
================================================================================
"""
import time

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:58s} {detail:38s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 84 + "\n  " + s + "\n" + "=" * 84)


t = sp.symbols('t', real=True)
x, y, z, k, eps = sp.symbols('x y z k epsilon', real=True)
X = [t, x, y, z]
ETA = sp.diag(-1, 1, 1, 1)


# ------------------------------------------------------------------------------
# PART A
# ------------------------------------------------------------------------------
def ricci_frw(N, a):
    g = sp.diag(-N ** 2, a ** 2, a ** 2, a ** 2)
    gi = g.inv()
    Gam = [[[sum(gi[r, q] * (sp.diff(g[q, m], X[n]) + sp.diff(g[q, n], X[m]) - sp.diff(g[m, n], X[q])) / 2
                 for q in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]
    Ric = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            Ric[m, n] = sum(sp.diff(Gam[r][m][n], X[r]) - sp.diff(Gam[r][m][r], X[n])
                            + sum(Gam[r][r][q] * Gam[q][m][n] - Gam[r][n][q] * Gam[q][m][r] for q in range(4))
                            for r in range(4))
    return sp.simplify(sum(gi[m, n] * Ric[m, n] for m in range(4) for n in range(4)))


def max_order(expr, f):
    o = 0
    for d in expr.atoms(sp.Derivative):
        if d.expr == f:
            o = max(o, sum(c for _, c in d.variable_count))
    return o


def part_A():
    header("PART A  minisuperspace: differential order and linearised modes")
    M, beta, Lam, H0 = sp.symbols('M beta Lambda H0', positive=True)
    s = sp.Symbol('s')          # mode exponent: complex, unrestricted
    a, N, u, n = [sp.Function(q)(t) for q in ('a', 'N', 'u', 'n')]
    R = ricci_frw(N, a)
    Tsc = 6 * sp.diff(a, t) ** 2 / (a ** 2 * N ** 2)
    th = {"GR": N * a ** 3 * R / 2, "f(R)": N * a ** 3 * (R + R ** 2 / (6 * M ** 2)) / 2,
          "f(T)": -N * a ** 3 * (Tsc + beta * Tsc ** 2) / 2}
    orders, mink, dsroots = {}, {}, {}
    for name, L in th.items():
        Ea, EN = [sp.simplify(e.lhs) for e in sp.euler_equations(L, [a, N], t)]
        orders[name] = (max_order(Ea, a), max_order(EN, a))
        la = sp.simplify(sp.diff(Ea.subs({a: 1 + eps * u, N: 1 + eps * n}).doit(), eps).subs(eps, 0))
        ex = sp.exp(s * t)
        mink[name] = set(sp.solve(sp.factor(sp.simplify(la.subs(u, ex).doit() / ex)), s))
        # de Sitter with a cosmological constant, synchronous gauge n = 0 (the full 2x2
        # determinant vanishes identically: time reparametrisation)
        Ld = L - N * a ** 3 * Lam
        Ea, EN = [sp.simplify(e.lhs) for e in sp.euler_equations(Ld, [a, N], t)]
        LamS = sp.solve(sp.simplify(EN.subs({a: sp.exp(H0 * t), N: 1}).doit()), Lam)[0]
        lN = sp.diff(EN.subs({a: sp.exp(H0 * t) * (1 + eps * u), N: 1}).doit(), eps).subs(eps, 0).subs(Lam, LamS)
        cN = sp.factor(sp.simplify(lN.subs(u, ex).doit() / ex * sp.exp(-3 * H0 * t)))
        dsroots[name] = sp.solve(cN, s)
        print(f"  {name:5s}: order(a-eq) = {orders[name][0]}, order(constraint) = {orders[name][1]};"
              f"  Minkowski roots {sorted(mink[name], key=str)};  de Sitter constraint roots {dsroots[name]}")
    gate("f(R): scalaron at s = +/- i M about Minkowski", mink["f(R)"] == {0, sp.I * M, -sp.I * M},
         str(sorted(mink["f(R)"], key=str)))
    gate("f(R): extra de Sitter pair -3H/2 +/- sqrt(9H^2/4 - M^2)", len(dsroots["f(R)"]) == 3, f"{len(dsroots['f(R)'])} roots")
    gate("f(T): same differential order as GR (2, 1)", orders["f(T)"] == orders["GR"] == (2, 1), str(orders["f(T)"]))
    gate("f(T): no mode beyond GR's (Minkowski and de Sitter)",
         mink["f(T)"] == mink["GR"] and dsroots["f(T)"] == dsroots["GR"], f"{dsroots['f(T)']}")
    return orders


# ------------------------------------------------------------------------------
# PART B: tetrad perturbation engine
# ------------------------------------------------------------------------------
a = sp.Function('a')(t)
Sf, Qf, Gf, P, V0, Df = [sp.Function(q)(t) for q in ('S', 'Q', 'G', 'P', 'V0', 'D')]
a1, b1, z1, l1 = [sp.Function(q)(t) for q in ('a1', 'b1', 'z1', 'l1')]
cx, sx = sp.cos(k * x), sp.sin(k * x)


def torsion(E):
    Einv = E.inv()
    g = E.T * ETA * E
    gi = g.inv()
    T = [[[sum(Einv[r, A] * (sp.diff(E[A, n], X[m]) - sp.diff(E[A, m], X[n])) for A in range(4))
           for n in range(4)] for m in range(4)] for r in range(4)]
    return T, g, gi


def torsion_scalar(E):
    T, g, gi = torsion(E)
    Tl = [[[sum(g[r, q] * T[q][m][n] for q in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]
    Tu = [[[sum(gi[m, p] * gi[n, q] * T[r][p][q] for p in range(4) for q in range(4))
            for n in range(4)] for m in range(4)] for r in range(4)]
    s1 = sum(Tl[r][m][n] * Tu[r][m][n] for r in range(4) for m in range(4) for n in range(4)) / 4
    s2 = sum(T[r][m][n] * sum(gi[n, p] * gi[m, q] * Tl[p][q][r] for p in range(4) for q in range(4))
             for r in range(4) for m in range(4) for n in range(4)) / 2
    v = [sum(T[r][m][r] for r in range(4)) for m in range(4)]
    return s1 + s2 - sum(v[m] * gi[m, n] * v[n] for m in range(4) for n in range(4))


def boundary_B(E):
    T, g, gi = torsion(E)
    v = [sum(T[r][m][r] for r in range(4)) for m in range(4)]
    vu = [sum(gi[m, n] * v[n] for n in range(4)) for m in range(4)]
    e = E.det()
    return -2 * sum(sp.diff(e * vu[m], X[m]) for m in range(4)) / e


def scalar_tetrad():
    """comoving gauge: lapse 1+alpha, shift N_x = d_x B, h_ij = a^2 e^{2 zeta}, boost rapidity d_x lambda.
    Scalars ~ cos(kx), their x-gradients ~ sin(kx)."""
    Nl = 1 + eps * a1 * cx
    sc = a * sp.exp(eps * z1 * cx)
    E = sp.zeros(4, 4)
    E[0, 0] = Nl
    E[1, 0] = sc * (eps * b1 * sx) / sc ** 2
    E[1, 1] = E[2, 2] = E[3, 3] = sc
    r = eps * l1 * sx
    Bst = sp.eye(4)
    Bst[0, 0] = Bst[1, 1] = sp.cosh(r)
    Bst[0, 1] = Bst[1, 0] = sp.sinh(r)
    return Bst * E, Nl


def second_order(expr):
    e2 = sp.expand(sp.diff(expr, eps, 2).subs(eps, 0) / 2)
    cc, ss = sp.symbols('cc ss')
    poly = sp.Poly(e2.subs({sx: ss, cx: cc}), cc, ss)
    avg = {(2, 0): sp.Rational(1, 2), (0, 2): sp.Rational(1, 2)}
    return sp.simplify(sum(coef * avg.get(mon, 0 if sum(mon) else 1) for mon, coef in poly.terms()))


def ibp_linear(L, f):
    """remove f', f'' by parts: c0 f + c1 f' + c2 f'' -> (c0 - c1' + c2'') f (exact up to total derivatives)"""
    L = sp.expand(L)
    c2 = L.coeff(sp.diff(f, t, 2))
    L = sp.expand(L - c2 * sp.diff(f, t, 2) + sp.diff(c2, t, 2) * f)
    c1 = L.coeff(sp.diff(f, t))
    return sp.expand(L - c1 * sp.diff(f, t) - sp.diff(c1, t) * f)


def part_B():
    header("PART B  second-order scalar action (comoving gauge, all scalar tetrad modes)")
    t0 = time.time()
    E, Nl = scalar_tetrad()
    T0 = 6 * sp.diff(a, t) ** 2 / a ** 2
    dT = torsion_scalar(E) - T0
    e = E.det()
    L2 = second_order(-e * (Gf + Sf * dT + Qf * dT ** 2 / 2) / 2 + e * (P ** 2 / (2 * Nl ** 2) - V0))
    print(f"  L2 built in {time.time() - t0:.0f} s")
    L2 = ibp_linear(L2, l1)
    A1, B1, Z, Zd, L1 = sp.symbols('A1 B1 Z Zd L1')
    Ls = sp.expand(L2.subs({sp.diff(z1, t): Zd, z1: Z, a1: A1, b1: B1, l1: L1}))
    lin_l = sp.simplify(Ls.subs(Qf, 0).coeff(L1, 1))
    print("  boost-mode coupling for Q = 0 (after IBP):", lin_l)
    gate("boost appears for Q = 0 only as -k a^2 S' zeta lambda",
         sp.simplify(lin_l + k * a ** 2 * sp.diff(Sf, t) * Z) == 0 and sp.simplify(Ls.subs(Qf, 0).coeff(L1, 2)) == 0,
         "linear multiplier, no lambda^2")

    # background equations from the same Lagrangian (minisuperspace with lapse; see doc):
    #  (i) S T0 - G/2 = P^2/2 + V0;  (ii) gives P^2 = 2[a'^2 S - a(S a'' + S' a')]/a^2
    ad, add = sp.diff(a, t), sp.diff(a, t, 2)
    V0s = Sf * T0 - Gf / 2 - P ** 2 / 2
    P2 = 2 * (Sf * ad ** 2 - a * (Sf * add + sp.diff(Sf, t) * ad)) / a ** 2

    # GR gate
    LGR = sp.expand(Ls.subs({Qf: 0, Sf: 1}).doit())
    gate("GR: boost decouples completely", sp.simplify(LGR.coeff(L1)) == 0, "coeff = 0")
    A1s = sp.solve(LGR.coeff(B1, 1), A1)[0]
    LGR = sp.expand(LGR.subs(A1, A1s).subs(L1, 0))
    zt = sp.Function('zt')(t)
    LGR = sp.expand(LGR.subs({Zd: sp.diff(zt, t), Z: zt}))
    Kc = LGR.coeff(sp.diff(zt, t), 2)
    Bc = sp.expand(LGR.coeff(sp.diff(zt, t), 1)).coeff(zt, 1)
    Mt = sp.expand(sp.expand(LGR - Kc * sp.diff(zt, t) ** 2 - Bc * zt * sp.diff(zt, t)).coeff(zt, 2) - sp.diff(Bc, t) / 2)
    grad = Mt.coeff(k, 2)
    m0 = sp.expand(Mt - grad * k ** 2)
    bgGR = lambda q: sp.simplify(q.subs(V0, V0s.subs(Sf, 1)).subs(Gf, T0).doit().subs(P ** 2, P2.subs(Sf, 1).doit()))
    Kg, gg, mg = bgGR(Kc), bgGR(grad), bgGR(m0)
    muk = P ** 2 * a ** 3 / (4 * sp.diff(a, t) ** 2 / a ** 2)
    gate("GR: kinetic term = a^3 chi'^2/(4H^2) (Mukhanov, x-averaged)",
         sp.simplify(Kg - bgGR(muk)) == 0, "exact")
    gate("GR: gradient term = -a chi'^2/(4H^2) k^2 (c_s^2 = 1)",
         sp.simplify(gg + bgGR(muk) / a ** 2) == 0, "exact")
    gate("GR: superhorizon mass of zeta vanishes", mg == 0, "exact")

    # STUR F(chi) T: Q = 0, S' != 0 -> Euler-Lagrange system
    fz, fa, fb, fl = [sp.Function(q)(t) for q in ('fz', 'fa', 'fb', 'fl')]
    LF = sp.expand(Ls.subs(Qf, 0).doit()).subs({Zd: sp.diff(fz, t), Z: fz, A1: fa, B1: fb, L1: fl})
    EL = [sp.simplify(q.lhs) for q in sp.euler_equations(LF, [fz, fa, fb, fl], t)]
    print("  F(chi)T  EL(lambda):", EL[3], "\n           EL(shift): ", EL[2])
    s_a = sp.solve(EL[2].subs(fz, 0).doit(), fa)
    s_b = sp.solve(EL[1].subs({fz: 0, fa: 0}).doit(), fb)
    s_l = sp.solve(EL[0].subs({fz: 0, fa: 0, fb: 0}).doit(), fl)
    print(f"           EL(lambda) forces zeta = 0 (S' != 0); then lapse = {s_a}, shift = {s_b}, lambda = {s_l}")
    gate("STUR F(chi)T: only the trivial solution -> 0 scalar dof",
         sp.simplify(EL[3] + k * a ** 2 * fz * sp.diff(Sf, t)) == 0 and s_a == [0] and s_b == [0] and s_l == [0],
         "zeta = lapse = shift = lambda = 0")

    # f(T): Q != 0 -> lapse, shift, boost all auxiliary
    sol = sp.solve([sp.diff(Ls, v) for v in (A1, B1, L1)], [A1, B1, L1], dict=True)
    gate("f(T): lapse, shift, boost all auxiliary (unique algebraic solution)", len(sol) == 1, "1 solution")
    LQr = sp.expand(Ls.subs(sol[0]))
    gate("f(T): reduced action depends on zeta only -> 1 scalar dof", not any(LQr.has(v) for v in (A1, B1, L1)), "")

    # boundary-term coupling +e D B/2
    t0 = time.time()
    E, _ = scalar_tetrad()
    LB = second_order(E.det() * Df * boundary_B(E) / 2)
    print(f"  L2(+e D B/2) built in {time.time() - t0:.0f} s")
    LB = ibp_linear(sp.expand(sum(q for q in sp.Add.make_args(sp.expand(LB)) if q.has(l1))), l1)
    lB = sp.simplify(LB.coeff(l1, 1))
    print("  boost coupling from +e D B/2:", lB)
    gate("boundary term adds +k a^2 D' zeta lambda (no lambda^2)",
         sp.simplify(lB - k * a ** 2 * sp.diff(Df, t) * z1) == 0 and sp.simplify(LB.coeff(l1, 2)) == 0, "")
    print("  => total boost coupling -k a^2 (S' - D') zeta lambda: a scalar propagates only if D' = S',")
    print("     i.e. -e S T/2 + e S B/2 = e S R/2 (scalar-curvature). STUR: D = 0, S' = 2 alpha chi' != 0.")
    return LQr


# ------------------------------------------------------------------------------
# PART C: f(T) k-scan on a numerical background, f = T + beta T^2, V = chi^2/2
# ------------------------------------------------------------------------------
def part_C(LQr):
    header("PART C  f(T) = T + beta T^2: exact k-scan of the reduced scalar action")
    Z, Zd = sp.symbols('Z Zd')
    K = sp.diff(LQr, Zd, 2) / 2
    M = sp.diff(LQr, Z, 2) / 2 - sp.diff(sp.diff(LQr, Zd, Z), t) / 2
    names = ['a', 'a1', 'a2', 'a3', 'S', 'Sd', 'Sdd', 'Q', 'Qd', 'G', 'Gd', 'P', 'Pd', 'V', 'Vd']
    sy = sp.symbols(names)
    rep = [(sp.diff(Sf, t, 2), sy[6]), (sp.diff(Gf, t), sy[10]), (sp.diff(V0, t), sy[14]),
           (sp.diff(a, t, 3), sy[3]), (sp.diff(a, t, 2), sy[2]), (sp.diff(a, t), sy[1]),
           (sp.diff(Sf, t), sy[5]), (sp.diff(Qf, t), sy[8]), (sp.diff(P, t), sy[12]),
           (a, sy[0]), (Sf, sy[4]), (Qf, sy[7]), (Gf, sy[9]), (P, sy[11]), (V0, sy[13])]

    def lam(e):
        for o, nn in rep:
            e = e.subs(o, nn)
        assert not e.has(t)
        return sp.lambdify(list(sy) + [k], e, 'numpy')
    fK, fM = lam(K), lam(M)

    def background(beta):
        T_of = lambda rho: 4 * rho / (1 + np.sqrt(1 + 24 * beta * rho))      # T/2 + 3 beta T^2/2 = rho
        rhs = lambda tt, y: [y[1], -3 * np.sqrt(T_of(0.5 * y[1] ** 2 + 0.5 * y[0] ** 2) / 6) * y[1] - y[0],
                             np.sqrt(T_of(0.5 * y[1] ** 2 + 0.5 * y[0] ** 2) / 6)]
        so = solve_ivp(rhs, [0, 30], [8.0, -0.3, 0.0], rtol=1e-12, atol=1e-14, dense_output=True)
        Hf = lambda tt: np.sqrt(T_of(0.5 * so.sol(tt)[1] ** 2 + 0.5 * so.sol(tt)[0] ** 2) / 6)

        def vals(tt, h=1e-3):
            chi, dchi, lna = so.sol(tt)
            A, H = np.exp(lna), Hf(tt)
            Hd = (Hf(tt + h) - Hf(tt - h)) / (2 * h)
            Hdd = (Hf(tt + h) - 2 * H + Hf(tt - h)) / h ** 2
            T0, T0d, T0dd = 6 * H ** 2, 12 * H * Hd, 12 * (Hd ** 2 + H * Hdd)
            dd = -3 * H * dchi - chi
            res = (-6 * (A ** 2 * H ** 2 * (1 + 2 * beta * T0) + A * A * (Hd + H ** 2) * (1 + 2 * beta * T0)
                         + A * A * H * 2 * beta * T0d) + 1.5 * A ** 2 * (T0 + beta * T0 ** 2)
                   - 6 * A ** 2 * H ** 2 * (1 + 2 * beta * T0) - 3 * A ** 2 * (dchi ** 2 / 2 - chi ** 2 / 2))
            return dict(a=A, a1=A * H, a2=A * (Hd + H ** 2), a3=A * (Hdd + 3 * H * Hd + H ** 3),
                        S=1 + 2 * beta * T0, Sd=2 * beta * T0d, Sdd=2 * beta * T0dd, Q=2 * beta, Qd=0.0,
                        G=T0 + beta * T0 ** 2, Gd=(1 + 2 * beta * T0) * T0d, P=dchi, Pd=dd,
                        V=chi ** 2 / 2, Vd=chi * dchi, H=H, Hd=Hd, res=res / (6 * A ** 2 * H ** 2))
        return vals

    vals = background(0.05)
    b = vals(5.0)
    gate("numerical f(T) background satisfies both Friedmann equations", abs(b['res']) < 1e-6, f"eq (ii) residual {b['res']:.1e}")
    args = [b[q] for q in names]
    aH = b['a'] * b['H']
    Kexp = b['a'] ** 3 * (b['S'] + 12 * b['Q'] * b['H'] ** 2) * (-b['Hd']) / (2 * b['H'] ** 2)
    rat, cs2, msh = [], None, None
    for q in (1e-3, 1e-1, 1, 10, 1e3):
        kk = q * aH
        Kv, Mv = fK(*args, kk), fM(*args, kk)
        rat.append(Kv / Kexp)
        print(f"   k/aH = {q:7.0e}: K/[a^3 (f_T + 2T f_TT)(-H')/2H^2] = {Kv / Kexp:.7f},  M/(K H^2) = {Mv / (Kv * b['H'] ** 2): .4e}")
        if q == 1e3:
            cs2 = -Mv / (Kv * kk ** 2 / b['a'] ** 2)
        if q == 1e-3:
            msh = Mv / (Kv * b['H'] ** 2)
    gate("f(T): K = a^3 (f_T + 2T f_TT)(-H')/(2H^2) at all k (no ghost)", max(abs(r - 1) for r in rat) < 1e-5,
         f"max dev {max(abs(r - 1) for r in rat):.1e}")
    gate("f(T): c_s^2 -> 1 for k >> aH", abs(cs2 - 1) < 1e-4, f"c_s^2(k = 1e3 aH) = {cs2:.6f}")
    print(f"   superhorizon: M/(K H^2) = {msh:.3f} (GR: 0) -> zeta is NOT conserved for k << aH")
    scan = []
    for beta in (0.05, 0.01, 0.002, 0.0004):
        vb = background(beta)(5.0)
        ab = [vb[q] for q in names]
        kk = 1e-3 * vb['a'] * vb['H']
        m = fM(*ab, kk) / (fK(*ab, kk) * vb['H'] ** 2)
        scan.append((beta, m, beta * 6 * vb['H'] ** 2))
        print(f"   beta = {beta:7.4f}: superhorizon M/(K H^2) = {m:.4e}   (ratio to beta T0: {m / (beta * 6 * vb['H'] ** 2):.2f})")
    gate("f(T): superhorizon mass -> 0 continuously as f_TT -> 0", scan[-1][1] / scan[0][1] < 0.05,
         f"{scan[-1][1]:.1e} at beta = 4e-4")
    return dict(Kratio=rat, cs2=cs2, m_superhorizon=msh, scan=scan)


# ------------------------------------------------------------------------------
# PART D: counterfactual scalar-curvature coupling alpha|R| R
# ------------------------------------------------------------------------------
def part_D():
    header("PART D  counterfactual: STUR's coupling as alpha|R| R (Einstein frame, v << chi)")
    # L = F(chi) R/2 - (d chi)^2/2 - V,  F = 2 alpha chi, V = lambda chi^4/4 (v << chi)
    # Einstein frame (M_Pl = 1): (d sigma/d chi)^2 = 1/F + (3/2)(F'/F)^2, U = V/F^2.
    # With x = chi/alpha: (d sigma/dx)^2 = 1/(2x) + 3/(2x^2), U ~ x^2: no free parameter.
    dsdx = lambda q: np.sqrt(1 / (2 * q) + 1.5 / q ** 2)
    lnU_x = lambda q: 2 / q
    eps_x = lambda q: 0.5 * (lnU_x(q) / dsdx(q)) ** 2

    def eta_x(q, h=1e-6):
        # U_ss/U with U ~ x^2:  U_s = U_x / s_x, U_ss = (U_xx s_x - U_x s_xx)/s_x^3
        sx_ = dsdx(q)
        sxx = (dsdx(q + h) - dsdx(q - h)) / (2 * h)
        return (2 * sx_ - 2 * q * sxx) / (q ** 2 * sx_ ** 3)
    x_end = brentq(lambda q: eps_x(q) - 1, 1e-6, 1e6)
    Nof = lambda q: quad(lambda s_: dsdx(s_) ** 2 / lnU_x(s_), x_end, q)[0]   # N = int U/U_s ds
    out = {}
    for Nst in (50, 55, 60):
        xs = brentq(lambda q: Nof(q) - Nst, x_end * 1.0001, 1e7)
        e, h = eps_x(xs), eta_x(xs)
        out[Nst] = (1 - 6 * e + 2 * h, 16 * e)
        print(f"   N* = {Nst}: n_s = {out[Nst][0]:.4f}, r = {out[Nst][1]:.4f}   (quartic chaotic: 1 - 3/N = {1 - 3 / Nst:.4f}, 16/N = {16 / Nst:.3f})")
    gate("counterfactual alpha|R| R inflation excluded (r > 0.036 BICEP/Keck)", out[60][1] > 0.036, f"r(60) = {out[60][1]:.3f}")
    return out


def main():
    part_A()
    LQr = part_B()
    part_C(LQr)
    part_D()
    header("VERDICT")
    print("""  (a) Computed: f(T) has the same differential order and the same linear modes as GR
      (Minkowski and de Sitter); f(R) has the extra Starobinsky pair at mass M. In the full
      scalar sector f(T) propagates exactly one scalar, with no ghost, K = a^3 (f_T + 2T f_TT)
      (-H')/2H^2 and c_s^2 -> 1, so there is no scalaron: R^2/Starobinsky inflation is not in
      a TEGR-based STUR action. (New: the integrated-out Lorentz mode gives zeta a
      superhorizon mass ~ 3 f_TT T, so zeta is not conserved in f(T) beyond GR.)
  (b) Computed: STUR's own F(chi)T coupling (F = 2 alpha |R|) has ZERO propagating scalar
      modes at linear order: the local-Lorentz mode is a Lagrange multiplier enforcing
      F' chi' zeta = 0. A scalar propagates only if a boundary-term coupling D(chi)B with
      D' = F' is added, i.e. only for the scalar-curvature theory F(chi)R. So n_s and r are
      not computable for STUR's inflation as written (linear theory is degenerate / strongly
      coupled). Counterfactual alpha|R| R gives quartic-like chaotic inflation, excluded.""")
    print(f"\n  gates: {sum(gates)}/{len(gates)} passed")


if __name__ == "__main__":
    main()
