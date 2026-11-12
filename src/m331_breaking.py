#!/usr/bin/env python3
"""
Symmetry breaking in 3-3-1, derived: SU(3)_L x U(1)_X -> SU(2)_L x U(1)_Y -> U(1)_em.

First rung of the symmetry-breaking ladder (SYMMETRY_LADDER.md). Nothing here is typed in
from the literature: the gauge-boson masses, the photon, the hypercharge matching and the
electric charges are all computed from the gauge generators and the scalar vevs.

Setup (both variants beta = +-1/sqrt3, the scalar X charges of src/m331_exact.py):
  Q = T3 + beta T8 + X, with T^a = lambda^a / 2 on SU(3)_L triplets.
  Covariant derivative D = d - i g W^a T^a - i g_X X B. With vevs <phi>, the mass term
  sum_phi |D <phi>|^2 = (1/2) M2_AB A^A A^B gives
      M2_AB = g_A g_B sum_phi <phi>^dagger {t_A, t_B} <phi>,
  A = (W^1 ... W^8, B), g_A = (g, ..., g, g_X), t_A = (T^1 ... T^8, X).
  Vevs: w/sqrt2 in the 3-3-1 triplet chi, v1/sqrt2 and v2/sqrt2 in the two electroweak
  triplets, each in the component the charge operator makes neutral (B0).

  B0  For every scalar triplet, the components with Q = 0 (where a vev may sit). (CHECK)
  B1  The mass matrix has rank 8: one of the 9 gauge bosons stays massless, so 8 eat
      Goldstone bosons. (CHECK)
  B2  The massless state is n_A ~ c_A / g_A with Q = sum c_A t_A, i.e. the generator
      T3 + beta T8 + X; its coupling is 1/e^2 = (1 + beta^2)/g^2 + 1/g_X^2. (CHECK)
  B3  First step alone (v1 = v2 = 0): 4 massless states, SU(2)_L and one U(1); that U(1)
      is Y = beta T8 + X with 1/g_Y^2 = beta^2/g^2 + 1/g_X^2, the matching condition that
      src/m331_exact.py uses, now derived. Consistency: 1/e^2 = 1/g^2 + 1/g_Y^2. (CHECK)
  B4  The spectrum: M_W = g v / 2 (v^2 = v1^2 + v2^2); bileptons ~ g w / 2; to leading order
      in v/w, M_Z^2 = (g^2 + g_Y^2) v^2 / 4 and M_Z'^2 = (g^2 + beta^2 g_X^2) w^2 / 3, so
      M_Z'/M_V = sqrt(4/3 (1 + beta^2 t_X^2)) with t_X^2 = s2 / (1 - (1 + beta^2) s2):
      the formula in src/m331_threshold.py, now derived. (CHECK)
  B5  Z-Z' mixing: the rho parameter M_W^2 / (M_Z^2 cos^2 theta_W) = 1 + O(v^2/w^2); the
      leading coefficient, computed. (CHECK)
  B6  Electric charges of every fermion multiplet of the model, for general N_c, from Q: they
      are 0, +-1 for leptons, Q_u = (N_c + 1)/2N_c and Q_d = (1 - N_c)/2N_c for quarks, and
      the exotics as the model states. (CHECK)
  B7  Numbers. v = (sqrt2 G_F)^(-1/2) = 246.22 GeV from the measured Fermi constant; then
      the tree-level M_Z from alpha(M_Z), sin^2 theta_W(M_Z) and G_F, against the measured
      91.1876 GeV (the 0.3% difference is the known radiative correction, not derived
      here); M_Z' and M_V for w set by the LHC bound. (CHECK)
Labels: CHECK (computed here), LIT (measured inputs: PDG).
"""
import os
import sys
from fractions import Fraction as Fr

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_exact as E

g, gX, w, v1, v2 = sp.symbols("g g_X w v_1 v_2", positive=True)
SQ3 = sp.sqrt(3)

# measured inputs (PDG 2024)
G_F = 1.1663788e-5          # GeV^-2
MZ_MEAS = 91.1876           # GeV
MW_MEAS = 80.3692           # GeV (PDG 2024 average)
ALPHA_MZ_INV = 127.951      # alpha(M_Z) MS-bar, inverse
S2_MZ = 0.23122             # sin^2 theta_W(M_Z) MS-bar


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def gell_mann():
    l = [sp.zeros(3, 3) for _ in range(8)]
    l[0][0, 1] = l[0][1, 0] = 1
    l[1][0, 1], l[1][1, 0] = -sp.I, sp.I
    l[2][0, 0], l[2][1, 1] = 1, -1
    l[3][0, 2] = l[3][2, 0] = 1
    l[4][0, 2], l[4][2, 0] = -sp.I, sp.I
    l[5][1, 2] = l[5][2, 1] = 1
    l[6][1, 2], l[6][2, 1] = -sp.I, sp.I
    l[7] = sp.diag(1, 1, -2) / SQ3
    return [m / 2 for m in l]


T = gell_mann()


def beta_value(variant):
    return -1 / SQ3 if variant == "-1/sqrt3" else 1 / SQ3


def charge_matrix(X, beta):
    return T[2] + beta * T[7] + X * sp.eye(3)


def scalar_triplets(variant):
    """The model's three scalar triplets (X charges from src/m331_exact.py), each with the
    neutral component in which its vev sits, and the vev symbol: w for the 3-3-1 triplet
    (neutral third component), v1, v2 for the electroweak ones."""
    _, _, scal, _ = E.MODELS[variant](3)
    beta = beta_value(variant)
    out, ew = [], [v1, v2]
    used_chi = False
    for _, dims, X in scal:
        Q = charge_matrix(sp.Rational(X.numerator, X.denominator), beta)
        neutral = [k for k in range(3) if Q[k, k] == 0]
        if 2 in neutral and not used_chi:
            out.append((sp.Rational(X.numerator, X.denominator), 2, w, neutral))
            used_chi = True
        else:
            k = [c for c in neutral if c != 2][0]
            out.append((sp.Rational(X.numerator, X.denominator), k, ew.pop(0), neutral))
    return out


def mass_matrix(variant, vw=w, va=v1, vb=v2):
    beta = beta_value(variant)
    trip = scalar_triplets(variant)
    gens = T + [None]
    cs = [g] * 8 + [gX]
    M = sp.zeros(9, 9)
    for X, k, vev, _ in trip:
        vev = {w: vw, v1: va, v2: vb}[vev]
        phi = sp.zeros(3, 1)
        phi[k] = vev / sp.sqrt(2)
        tl = [m for m in T] + [X * sp.eye(3)]
        for A in range(9):
            for B in range(9):
                M[A, B] += cs[A] * cs[B] * (phi.H * (tl[A] * tl[B] + tl[B] * tl[A]) * phi)[0, 0]
    return sp.simplify(M)


def photon_checks(variant):
    """B1, B2: rank, massless direction, and 1/e^2."""
    beta = beta_value(variant)
    M = mass_matrix(variant)
    n = sp.Matrix([0, 0, 1 / g, 0, 0, 0, 0, beta / g, 1 / gX])          # c_A / g_A for Q
    rank = M.subs({g: sp.Rational(7, 10), gX: sp.Rational(9, 10), w: 4000, v1: 150, v2: 190}).rank()
    e_inv2 = sp.simplify(sum(x**2 for x in n))
    return rank, sp.simplify(M * n), e_inv2


def first_step(variant):
    """B3: with v1 = v2 = 0, the number of massless states and the hypercharge matching."""
    beta = beta_value(variant)
    M = mass_matrix(variant, va=0, vb=0)
    num = M.subs({g: sp.Rational(7, 10), gX: sp.Rational(9, 10), w: 4000})
    massless = 9 - num.rank()
    nY = sp.Matrix([0] * 7 + [beta / g, 1 / gX])
    gY_inv2 = sp.simplify(sum(x**2 for x in nY))
    return massless, sp.simplify(M * nY), gY_inv2


def neutral_invariants(variant):
    """The neutral block N (W3, W8, B): its trace S and sum of principal 2x2 minors P. With
    the photon's zero removed, lambda_Z + lambda_Z' = S and lambda_Z lambda_Z' = P, so
    exactly lambda_Z = 2P / (S + sqrt(S^2 - 4P)) and lambda_Z' = S - lambda_Z."""
    M = mass_matrix(variant)
    N = M.extract([2, 7, 8], [2, 7, 8])
    S = sp.expand(N.trace())
    P = sp.expand(sum(N.extract([i, j], [i, j]).det() for i in range(3) for j in range(i + 1, 3)))
    return M, N, S, P


def leading_masses(variant):
    beta = beta_value(variant)
    M, N, S, P = neutral_invariants(variant)
    gY2 = 1 / (beta**2 / g**2 + 1 / gX**2)
    v2s = v1**2 + v2**2
    t, a = sp.symbols("t a", positive=True)
    sub = {v1: t * w * sp.cos(a), v2: t * w * sp.sin(a)}
    # leading order: lambda_Z = P/S + O(t^4 w^2), lambda_Z' = S + O(t^2 w^2)
    zlead = sp.simplify(sp.limit((P / S).subs(sub) / (t**2 * w**2), t, 0))
    zplead = sp.simplify(S.subs({v1: 0, v2: 0}) / w**2)
    return {
        "MW2": sp.simplify((M[0, 0] + M[1, 1]) / 2), "MW2_expected": g**2 * v2s / 4,
        "MV2": [sp.simplify(M[3, 3]), sp.simplify(M[5, 5])],
        "MZ2_lead_over_v2": zlead, "MZ2_expected": sp.simplify((g**2 + gY2) / 4),
        "MZp2_lead_over_w2": zplead, "MZp2_expected": (g**2 + beta**2 * gX**2) / 3,
        "S": S, "P": P, "gY2": gY2}


def mzp_over_mv_check(variant):
    """B4: M_Z'^2 / M_V^2 at v = 0 vs (4/3)(1 + beta^2 t_X^2), t_X^2 = s2/(1-(1+beta^2)s2)."""
    beta = beta_value(variant)
    lm = leading_masses(variant)
    mv2_lead = sp.simplify(lm["MV2"][1].subs({v1: 0, v2: 0}) / w**2)
    ratio = sp.simplify(lm["MZp2_lead_over_w2"] / mv2_lead)
    s2 = sp.Symbol("s2", positive=True)
    gx_s2 = sp.sqrt(s2 * g**2 / (1 - s2 - beta**2 * s2))        # from s2 = gY^2/(g^2 + gY^2)
    check_s2 = sp.simplify((lm["gY2"] / (g**2 + lm["gY2"])).subs(gX, gx_s2) - s2)
    tX2 = s2 / (1 - (1 + beta**2) * s2)
    return sp.simplify(ratio.subs(gX, gx_s2) - sp.Rational(4, 3) * (1 + beta**2 * tX2)), check_s2


def rho_parameter(variant):
    """B5: rho = M_W^2 / (M_Z^2 cos^2 theta_W) with the exact lambda_Z, expanded in t = v/w;
    cos^2 theta_W = g^2/(g^2 + g_Y^2). v1 = v cos a, v2 = v sin a."""
    lm = leading_masses(variant)
    S, P = lm["S"], lm["P"]
    t, a = sp.symbols("t a", positive=True)
    sub = {v1: t * w * sp.cos(a), v2: t * w * sp.sin(a)}
    lamZ = 2 * P / (S + sp.sqrt(S**2 - 4 * P))
    cw2 = g**2 / (g**2 + lm["gY2"])
    rho = (lm["MW2"] / (lamZ * cw2)).subs(sub)
    ser = sp.series(rho, t, 0, 3).removeO()
    return sp.simplify(sp.trigsimp(ser))


def charges(variant, Nc):
    """B6: component charges of every fermion multiplet from Q. Anti-triplets carry -T^*:
    Q = -T3 - beta T8 + X. The model lists both as SU(3)_L dimension 3; the anti-triplet is
    the quark multiplet with X = Xa. Returns rows (kind, X, charges) and the checks that
    each SU(2)_L doublet part is (Q_u, Q_d) for quarks or (0, -1) for leptons, up to order."""
    beta = beta_value(variant)
    gs, ferm, scal, (Xt, Xa, Qu, Qd, Ng, nA) = E.MODELS[variant](Nc)
    R = lambda f: sp.Rational(f.numerator, f.denominator)
    Qu, Qd, Xt, Xa = R(Qu), R(Qd), R(Xt), R(Xa)
    rows, ok = [], True
    for m, dims, X in ferm:
        Xs = R(X)
        if dims[1] != 3:
            rows.append(("singlet", Xs, [Xs]))
            continue
        anti = dims[2] == Nc and Xs == Xa and Xa != Xt
        Qm = (-T[2] - beta * T[7] if anti else T[2] + beta * T[7]) + Xs * sp.eye(3)
        q = [sp.nsimplify(Qm[k, k]) for k in range(3)]
        kind = ("quark anti-triplet" if anti else "quark triplet") if dims[2] == Nc else "lepton triplet"
        rows.append((kind, Xs, q))
        pair = set(q[:2])
        if kind == "lepton triplet":
            ok &= pair == {0, -1}
        else:
            ok &= pair == {Qu, Qd}
    return rows, ok, (Qu, Qd)


def rho_coefficient(variant):
    """B5: (rho - 1) / (v/w)^2 at leading order, and a numerical check by exact diagonalization."""
    import numpy as np
    ser = rho_parameter(variant)
    t, a = sp.symbols("t a", positive=True)
    coeff = sp.simplify(sp.expand(ser - 1).coeff(t, 2))
    vals = {g: 0.652, gX: 0.79, w: 4000.0}
    M = mass_matrix(variant)
    lm = leading_masses(variant)
    tv, av = 0.01, 0.7
    num = np.array(M.subs(vals).subs({v1: tv * 4000 * np.cos(av), v2: tv * 4000 * np.sin(av)}).evalf(), dtype=float)
    ev = sorted(np.linalg.eigvalsh(num))
    mW2 = float(lm["MW2"].subs(vals).subs({v1: tv * 4000 * np.cos(av), v2: tv * 4000 * np.sin(av)}))
    gY2 = float(lm["gY2"].subs(vals))
    cw2 = 0.652**2 / (0.652**2 + gY2)
    neutral = [x for x in ev if abs(x - mW2) > 1e-6 * mW2 and x > 1e-9]
    mz2 = min(neutral)
    rho_num = mW2 / (mz2 * cw2)
    rho_ser = float((1 + coeff * t**2).subs(vals).subs({t: tv, a: av}))
    return coeff, rho_num, rho_ser


def numbers(variant="+1/sqrt3", MZp_bound=4.6e3):
    """B7: v from G_F; tree-level M_Z; M_Z' and M_V at the LHC bound."""
    import math
    v = (math.sqrt(2) * G_F) ** -0.5
    a = 1 / ALPHA_MZ_INV
    mz_tree = math.sqrt(math.pi * a / (math.sqrt(2) * G_F) / (S2_MZ * (1 - S2_MZ)))
    beta2 = 1 / 3
    tX2 = S2_MZ / (1 - (1 + beta2) * S2_MZ)
    ratio = math.sqrt(4 / 3 * (1 + beta2 * tX2))
    return v, mz_tree, ratio, MZp_bound / ratio


def main():
    for variant in ("-1/sqrt3", "+1/sqrt3"):
        banner(f"beta = {variant}")
        print("   B0  scalar triplets: X charge, vev component, vev, neutral components")
        for X, k, vev, neutral in scalar_triplets(variant):
            print(f"       X = {str(X):5s}  vev in component {k + 1} ({vev}); Q = 0 in components {[c + 1 for c in neutral]}")
        rank, Mn, einv2 = photon_checks(variant)
        print(f"   B1  rank of the 9x9 mass matrix: {rank}  (8 massive, 1 massless)")
        print(f"   B2  M2 . n_Q = {list(Mn)}  -> n_Q ~ (T3 + beta T8 + X)/g_A is massless")
        print(f"       1/e^2 = {einv2}")
        massless, MnY, gYinv2 = first_step(variant)
        print(f"   B3  v1 = v2 = 0: {massless} massless states; M2 . n_Y = 0: {all(x == 0 for x in MnY)}")
        print(f"       1/g_Y^2 = {gYinv2}   and 1/e^2 - (1/g^2 + 1/g_Y^2) = {sp.simplify(einv2 - 1 / g**2 - gYinv2)}")
        lm = leading_masses(variant)
        print(f"   B4  M_W^2 = {lm['MW2']}  (= g^2 v^2 / 4: {sp.simplify(lm['MW2'] - lm['MW2_expected']) == 0})")
        print(f"       bileptons: M^2 = {lm['MV2'][0]} and {lm['MV2'][1]}")
        print(f"       M_Z^2 / v^2 -> {lm['MZ2_lead_over_v2']}  (= (g^2 + g_Y^2)/4: {sp.simplify(lm['MZ2_lead_over_v2'] - lm['MZ2_expected']) == 0})")
        print(f"       M_Z'^2 / w^2 -> {lm['MZp2_lead_over_w2']}  (= (g^2 + beta^2 g_X^2)/3: {sp.simplify(lm['MZp2_lead_over_w2'] - lm['MZp2_expected']) == 0})")
        diff, chk = mzp_over_mv_check(variant)
        print(f"       M_Z'/M_V formula of src/m331_threshold.py reproduced: residual {diff} (s2 inversion check {chk})")
        coeff, rn, rs = rho_coefficient(variant)
        print(f"   B5  rho - 1 = (v/w)^2 x [{coeff}]  (v1 = v cos a, v2 = v sin a)")
        print(f"       check at v/w = 0.01: exact diagonalization {rn:.10f}, series {rs:.10f}")
        for Nc in (3, 5):
            rows, ok, (Qu, Qd) = charges(variant, Nc)
            print(f"   B6  N_c = {Nc} (Q_u = {Qu}, Q_d = {Qd}): doublet parts as in the Standard Model: {ok}")
            seen = set()
            for kind, X, q in rows:
                key = (kind, X)
                if key in seen:
                    continue
                seen.add(key)
                print(f"         {kind:18s} X = {str(X):6s} charges {[str(x) for x in q]}")
    banner("B7  Numbers (tree level; measured inputs: G_F, alpha(M_Z), sin^2 theta_W(M_Z))")
    v, mz, ratio, mv = numbers()
    print(f"   v = (sqrt2 G_F)^(-1/2) = {v:.2f} GeV")
    print(f"   M_Z (tree) = sqrt(pi alpha / (sqrt2 G_F s^2 c^2)) = {mz:.2f} GeV, measured {MZ_MEAS} GeV"
          f" ({100 * (mz / MZ_MEAS - 1):+.2f}%: the radiative correction, not derived here)")
    print(f"   beta = +1/sqrt3: M_Z'/M_V = {ratio:.4f}; at the LHC bound M_Z' = 4.6 TeV, M_V = {mv / 1e3:.2f} TeV")


if __name__ == "__main__":
    main()
