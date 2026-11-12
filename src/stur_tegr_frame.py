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
  Q5  Exact, nonlinear, pure-frame sector (flat metric, e = Lambda(x), Lambda a finite
      SO(2,1) or SO(3,1) frame field): the symplectic current is omega^mu = d_nu W^{mu nu}
      with W^{mu nu} = (1/8 pi) [theta_1, theta_2]^{mu nu}, theta = Lambda^-1 d Lambda.
      Checked numerically at 60 digits (finite differences, error ~1e-34). So the corner
      form is the Kirillov-Kostant form of the Lorentz group at (1/8 pi G) K_normal per unit
      area. (CHECK)
  Q6  Hence the corner charges of frame rotations, G_X = (1/8 pi) (Lambda^-1 X Lambda)^{tx},
      satisfy d G_X = Omega(delta_X, .) and close exactly: {G_X, G_Y} = Omega(delta_X,
      delta_Y) = G_[X,Y], the Lorentz algebra so(3,1) = sl(2,C). Its sl(2,R) = so(2,1) subalgebras are
      {K_normal, K_A, J_normal-A} for each tangent direction A. The orbit has dimension 4;
      the stabilizer is {K_normal, J_surface}, the two modes Q3 found without a frame
      partner. (CHECK)
  Q7  Consequence for the entropy (KNOWN representation theory; Varrin arXiv:2610.37750,
      eq. 4.14 and 4.20): an orbit through a boost quantizes to principal-series
      representations labelled by the area. The group Plancherel density grows only
      polynomially (k tanh(pi k) for SL(2,R)), giving ln A, not A/4. The exponential
      k sinh(2 pi k), which gives A/4, needs the causal semigroup SL+(2,R) of normal-plane
      maps. For Lorentz boosts the causal condition is automatic (in null coordinates a
      boost is diag(e^eta, e^-eta)), so TEGR's frame does not supply it.
Labels: KNOWN, CHECK (computed here).
"""
import itertools
import random

import mpmath as mp
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


# --------------------------------------------------------------------------- Q5-Q7
_GENS = [(0, 1, True), (0, 2, True), (1, 2, False), (0, 3, True), (1, 3, False), (2, 3, False)]


def _mp_rot(i, j, ang, is_boost):
    M = mp.eye(4)
    if is_boost:
        M[i, i] = M[j, j] = mp.cosh(ang)
        M[i, j] = M[j, i] = mp.sinh(ang)
    else:
        M[i, i] = M[j, j] = mp.cos(ang)
        M[i, j], M[j, i] = -mp.sin(ang), mp.sin(ang)
    return M


def _mp_eta():
    return mp.diag(ETA)


def _random_frame(ngen, rng):
    """A finite Lorentz frame field Lambda(x; e1, e2) built from ngen generators, with
    random quadratic polynomials for the angles and for the two variations."""
    def rpoly():
        c = [mp.mpf(rng.randint(-9, 9)) / 17 for _ in range(15)]

        def f(x):
            out, k = c[0] + sum(c[1 + i] * x[i] for i in range(4)), 5
            for i in range(4):
                for j in range(i, 4):
                    if k < 15:
                        out += c[k] * x[i] * x[j]
                        k += 1
            return out
        return f
    gens = _GENS[:ngen]
    q, u, v = ([rpoly() for _ in gens] for _ in range(3))

    def Lam(x, e1=0, e2=0):
        M = mp.eye(4)
        for (i, j, b), qq, uu, vv in zip(gens, q, u, v):
            M = M * _mp_rot(i, j, qq(x) / 3 + e1 * uu(x) + e2 * vv(x), b)
        return M
    return Lam


def _cd(f, h):
    """4th-order central difference of s -> f(s) at 0."""
    return (-f(2 * h) + 8 * f(h) - 8 * f(-h) + f(-2 * h)) / (12 * h)


def _mp_lag(Linv, P):
    n = N4
    Tl = [[[sum(Linv[r, a] * (P[a][w][m] - P[a][m][w]) for a in range(n)) for w in range(n)] for m in range(n)]
          for r in range(n)]
    s1 = s2 = 0
    for r, m, w in itertools.product(range(n), repeat=3):
        up = ETA[m] * ETA[w] * Tl[r][m][w]
        s1 += up * ETA[r] * Tl[r][m][w]
        s2 += up * ETA[w] * Tl[w][m][r]
    V = [sum(Tl[r][r][m] for r in range(n)) for m in range(n)]
    return -(s1 / 4 + s2 / 2 - sum(ETA[m] * V[m] ** 2 for m in range(n))) / (16 * mp.pi)


def _mp_momentum(Linv, P):
    """Gradient of the quadratic form: exact by central difference with step 1."""
    out = [[[0] * N4 for _ in range(N4)] for _ in range(N4)]
    for a, w, m in itertools.product(range(N4), repeat=3):
        Pp = [[[P[i][j][k] for k in range(N4)] for j in range(N4)] for i in range(N4)]
        Pm = [[[P[i][j][k] for k in range(N4)] for j in range(N4)] for i in range(N4)]
        Pp[a][w][m] += 1
        Pm[a][w][m] -= 1
        out[m][a][w] = (_mp_lag(Linv, Pp) - _mp_lag(Linv, Pm)) / 2
    return out


def kks_exact_check(ngen=6, points=2, seed=11, dps=60):
    """Q5: max |omega - div W|, max |omega + div W| (control), max |omega| over points."""
    mp.mp.dps = dps
    h = mp.mpf("1e-14")
    rng = random.Random(seed)
    Lam = _random_frame(ngen, rng)
    E = _mp_eta()

    def theta(x, e1, e2, which):
        L = Lam(x, e1, e2)
        Linv = E * L.T * E
        dL = [_cd(lambda s, m=m: Lam([x[k] + (s if k == m else 0) for k in range(4)], e1, e2), h) for m in range(4)]
        P = [[[dL[m][a, w] for m in range(4)] for w in range(4)] for a in range(4)]
        Pm = _mp_momentum(Linv, P)
        dLe = _cd(lambda s: Lam(x, e1 + s, e2) if which == 1 else Lam(x, e1, e2 + s), h)
        return mp.matrix([sum(Pm[mu][a][w] * dLe[a, w] for a in range(4) for w in range(4)) for mu in range(4)])

    def W(x):
        L = Lam(x)
        Linv = E * L.T * E
        t1 = Linv * _cd(lambda s: Lam(x, s, 0), h)
        t2 = Linv * _cd(lambda s: Lam(x, 0, s), h)
        return (t1 * t2 - t2 * t1) * E / (8 * mp.pi)

    worst = ctrl = size = mp.mpf(0)
    for _ in range(points):
        x = [mp.mpf(rng.randint(-20, 20)) / 23 for _ in range(4)]
        om = _cd(lambda s: theta(x, s, 0, 2), h) - _cd(lambda s: theta(x, 0, s, 1), h)
        div = mp.matrix(4, 1)
        for nu in range(4):
            div += _cd(lambda s, nu=nu: W([x[k] + (s if k == nu else 0) for k in range(4)])[:, nu], h)
        worst = max(worst, mp.norm(om - div))
        ctrl = max(ctrl, mp.norm(om + div))
        size = max(size, mp.norm(om))
    return worst, ctrl, size


def lorentz_generator(i, j):
    """J_ij in the frame representation, (J_ij)^a_b = delta^a_i eta_jb - delta^a_j eta_ib."""
    M = mp.matrix(4, 4)
    M[i, j] += ETA[j]
    M[j, i] -= ETA[i]
    return M


def charge_closure_check(seed=5, dps=40):
    """Q6: at a random finite frame Lambda, with Omega(d1, d2) = (1/8 pi)[th1, th2]^{tx}
    (th = Lambda^-1 dLambda) and G_X = (1/8 pi)(Lambda^-1 X Lambda eta)^{tx}:
    worst |Omega(delta_X, d) - d G_X| over random d, and worst
    |Omega(delta_X, delta_Y) - G_[X,Y]| over all generator pairs."""
    mp.mp.dps = dps
    rng = random.Random(seed)
    E = _mp_eta()
    Lam = mp.eye(4)
    for (i, j, b) in _GENS:
        Lam = Lam * _mp_rot(i, j, mp.mpf(rng.randint(-9, 9)) / 7, b)
    Linv = E * Lam.T * E
    tx = lambda M: (M * E)[0, 1] / (8 * mp.pi)
    Omega = lambda dA, dB: tx((Linv * dA) * (Linv * dB) - (Linv * dB) * (Linv * dA))
    G = lambda Xg, L: tx((E * L.T * E) * Xg * L)
    gens = [lorentz_generator(i, j) for (i, j, b) in _GENS]
    ham = mp.mpf(0)
    for Xg in gens:
        for _ in range(3):
            Y = sum((mp.mpf(rng.randint(-9, 9)) / 11 * g for g in gens), mp.matrix(4, 4))
            dLam = Y * Lam                                                  # a random variation
            dG = _cd(lambda s: G(Xg, Lam + s * dLam), mp.mpf("1e-12"))
            ham = max(ham, abs(Omega(Xg * Lam, dLam) - dG))
    alg = mp.mpf(0)
    for A, B in itertools.product(gens, repeat=2):
        alg = max(alg, abs(Omega(A * Lam, B * Lam) - G(A * B - B * A, Lam)))
    # stabilizer at the identity: generators X with Omega(delta_X, .) = 0
    stab = [(i, j) for (i, j, b), Xg in zip(_GENS, gens)
            if all(abs(tx(Xg * Yg - Yg * Xg)) < mp.mpf("1e-30") for Yg in gens)]
    return ham, alg, stab


def plancherel_entropy(area):
    """Q7: leading edge entropy, two powers of the Plancherel density at k = A / 16 pi
    (Varrin: 2 Phi_h = A / 8 pi G, k = Phi_h): group SL(2,R), mu = k tanh(pi k); semigroup
    SL+(2,R), mu = k sinh(2 pi k). Returns (S_group, S_semigroup, A/4)."""
    k = mp.mpf(area) / (16 * mp.pi)
    return (2 * mp.log(k * mp.tanh(mp.pi * k)), 2 * mp.log(k * mp.sinh(2 * mp.pi * k)), mp.mpf(area) / 4)


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

    banner("Q5  Exact, nonlinear: the frame's corner form is Kirillov-Kostant (CHECK)")
    for ng, label in ((3, "SO(2,1)"), (6, "SO(3,1)")):
        w, c, sz = kks_exact_check(ngen=ng)
        print(f"   {label} frame field: |omega - div W| = {mp.nstr(w, 2)},  control |omega + div W| ="
              f" {mp.nstr(c, 3)},  |omega| = {mp.nstr(sz, 3)}")
    print("   W^{mu nu} = (1/8 pi) [Lambda^-1 d1 Lambda, Lambda^-1 d2 Lambda]^{mu nu}, flat metric, finite frames.")

    banner("Q6  The corner charges close into the Lorentz algebra (CHECK)")
    ham, alg, stab = charge_closure_check()
    print(f"   Omega(delta_X, d) = d G_X:          worst error {mp.nstr(ham, 2)}")
    print(f"   Omega(delta_X, delta_Y) = G_[X,Y]:  worst error {mp.nstr(alg, 2)} over all 36 pairs")
    print(f"   Stabilizer of the orbit point (generators with no partner): J{stab}")
    print("   so(3,1) = sl(2,C) closes exactly. sl(2,R) = so(2,1) subalgebras: {J01, J0A, J1A}.")
    print("   This sl(2,R) mixes the normal with a tangent direction; Varrin's acts on the normal")
    print("   plane. They share only the boost J01, the area pair of Q3.")

    banner("Q7  What this quantizes to (KNOWN: Varrin 2610.37750, eqs. 4.14, 4.20)")
    for A in (100, 1000):
        sg, ss, q4 = plancherel_entropy(A)
        print(f"   A = {A}: group SL(2,R) 2 ln mu = {mp.nstr(sg, 4)};  semigroup SL+(2,R) = {mp.nstr(ss, 6)};  A/4 = {q4}")
    print("   The group measure gives ln A; only the causal semigroup gives A/4. For Lorentz boosts")
    print("   the causal condition is automatic, so TEGR's frame alone does not give A/4. The")
    print("   exponential needs the normal-plane edge modes, which the frame does not supply.")


if __name__ == "__main__":
    main()
