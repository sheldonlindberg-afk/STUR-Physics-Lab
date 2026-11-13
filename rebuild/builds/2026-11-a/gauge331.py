"""gauge331: SU(3)_L x U(1)_X -> SU(2)_L x U(1)_Y -> U(1)_em (SPEC.md section 2).

Derivations and second routes: DERIVATION_gauge331.md. Numerics via toolkit (eigvalsh,
exact_derivative). Exact quantities are fractions.Fraction.
"""
import math
from fractions import Fraction

import inputs  # noqa: F401  (no measured number is needed in this stage; G_F etc. are arguments)
import toolkit

PROVENANCE = {
    "triplet_charges": ("derived", "Q = T3 + b diag(1,1,-2) + X, b = beta/(2 sqrt3) exact rational parsed from"
                                   " the variant; antitriplet -t^* flips T3, T8 (real diagonal)"),
    "quark_charges": ("derived", "[SU(3)_L]^2 U(1)_X anomaly N_g X_L + N_c[(N_g-n_A)X_t + n_A X_a] affine in Q_u,"
                                 " X_L from Q_e = -1, X_t, X_a from (Q_u, Q_d) = first two components; solved exactly"
                                 " with toolkit.exact_derivative; b cancels: Q_u = (N_c+1)/(2N_c)"),
    "doublet_charge_pairs": ("derived", "first two charges of lepton triplets (X_L), quark triplets (X_t) and"
                                        " antitriplets (X_a = X_t + 2b) via triplet_charges and quark_charges"),
    "mass_matrix": ("derived", "|D<phi>|^2 = (1/2) g_A g_B <phi>^dag{t_A,t_B}<phi> V^A V^B with Gell-Mann t_A,"
                               " t_9 = X; vev components = the Q = 0 ones found from triplet_charges (w: first"
                               " triplet neutral in comp 3; others: neutral comp other than 3, v1 then v2)"),
    "photon_direction": ("derived", "massless direction n_A = q_A/g_A, q = (T3: 1, T8: beta, X: 1) so"
                                    " sum g_A n_A t_A = Q; M n = 0 because Q<phi> = 0 for every vev"),
    "inv_e2": ("derived", "canonical A = n_hat.V couples Q/|n|, so 1/e^2 = |n|^2 = (1+beta^2)/g^2 + 1/gX^2"),
    "neutral_masses": ("derived", "toolkit.eigvalsh of the (W3, W8, B) block, which decouples because diagonal x"
                                  " off-diagonal generators vanish on the diagonal; photon zero mode dropped"),
    "vev_from_GF": ("derived", "G_F/sqrt2 = g^2/(8 M_W^2), M_W^2 = g^2 v^2/4 (mass_matrix) => v = (sqrt2 G_F)^(-1/2)"),
    "mz_tree": ("derived", "e = g s_W, e^2 = 4 pi alpha, M_W^2 = g^2 v^2/4, M_Z = M_W/c_W =>"
                           " M_Z^2 = pi alpha/(sqrt2 G_F s^2 (1-s^2)) (SPEC convention)"),
}


# ------------------------------------------------------------------------------------------
# variant parsing: beta = s k / sqrt(r)
# ------------------------------------------------------------------------------------------
def _parse_variant(variant):
    s = variant.strip()
    sign = -1 if s.startswith("-") else 1
    s = s.lstrip("+-")
    num, den = s.split("/")
    if not den.startswith("sqrt"):
        raise ValueError(f"variant {variant!r}: expected 'k/sqrt r'")
    return sign, int(num), int(den[len("sqrt"):])


def _b(variant):
    """b = beta/(2 sqrt3) as an exact Fraction (beta T8 = b diag(1,1,-2))."""
    sign, k, r = _parse_variant(variant)
    root = math.isqrt(3 * r)
    if root * root != 3 * r:
        raise ValueError(f"variant {variant!r}: beta T8 not rational")
    return Fraction(sign * k, 2 * root)


def _beta(variant):
    sign, k, r = _parse_variant(variant)
    return sign * k / math.sqrt(r)


# ------------------------------------------------------------------------------------------
# charges
# ------------------------------------------------------------------------------------------
_T3 = (Fraction(1, 2), Fraction(-1, 2), Fraction(0))
_T8SHAPE = (1, 1, -2)          # lambda_8 sqrt3 diagonal


def triplet_charges(X, variant, anti=False):
    X = Fraction(X)
    b = _b(variant)
    sg = -1 if anti else 1
    return [sg * (_T3[i] + b * _T8SHAPE[i]) + X for i in range(3)]


def _scalar_X(variant):
    """SPEC.md section 2 postulate: X charges of the three scalar triplets."""
    if _b(variant) < 0:
        return (Fraction(-1, 3), Fraction(2, 3), Fraction(-1, 3))
    return (Fraction(1, 3), Fraction(1, 3), Fraction(-2, 3))


def _vev_slots(variant):
    """[(X, component index 0..2, which vev 'w'|'v1'|'v2')], derived from Q = 0."""
    Xs = _scalar_X(variant)
    neutral = [[k for k, q in enumerate(triplet_charges(X, variant)) if q == 0] for X in Xs]
    iw = next(i for i, nl in enumerate(neutral) if 2 in nl)
    slots, light = [], iter(("v1", "v2"))
    for i, X in enumerate(Xs):
        if i == iw:
            slots.append((X, 2, "w"))
            continue
        rest = [k for k in neutral[i] if k != 2]
        if len(rest) != 1:
            raise ValueError(f"triplet {i} (X = {X}): neutral components {neutral[i]} do not fix a vev slot")
        slots.append((X, rest[0], next(light)))
    return slots


def _lepton_X(b):
    """Q_e = -1/2 + b + X_L = -1 (second component of the lepton triplet)."""
    return Fraction(-1) - (_T3[1] + b * _T8SHAPE[1])


def _anomaly(Nc, b, Qu):
    """[SU(3)_L]^2 U(1)_X / (common Dynkin index) for the SPEC content; Qu may be a Dual."""
    Ng, nA = Nc, (1 + Nc) // 2
    XL = _lepton_X(b)
    Xt = Qu - (_T3[0] + b * _T8SHAPE[0])                 # triplet comp 1 = Q_u
    Qd = Qu - 1
    Xa = Qd - (-_T3[0] - b * _T8SHAPE[0])                # antitriplet comp 1 = Q_d
    return Ng * XL + Nc * ((Ng - nA) * Xt + nA * Xa)


def quark_charges(Nc):
    if Nc < 1 or Nc % 2 == 0:
        raise ValueError("N_c must be a positive odd integer (n_A = (1+N_c)/2 families)")
    sols = set()
    for var in ("-1/sqrt3", "+1/sqrt3"):
        b = _b(var)
        f = lambda q, b=b: _anomaly(Nc, b, q)
        q0 = Fraction(0)
        slope = toolkit.exact_derivative(f, q0)
        Qu = q0 - f(q0) / slope
        assert f(Qu) == 0
        sols.add(Qu)
    if len(sols) != 1:
        raise ArithmeticError(f"anomaly solution depends on beta: {sols}")
    Qu = sols.pop()
    return Qu, Qu - 1


def doublet_charge_pairs(Nc, variant):
    b = _b(variant)
    Qu, Qd = quark_charges(Nc)
    nA = (1 + Nc) // 2
    XL = _lepton_X(b)
    Xt = Qu - (_T3[0] + b * _T8SHAPE[0])
    Xa = Xt + 2 * b
    pairs = {frozenset(triplet_charges(XL, variant)[:2])}
    quark = []
    if Nc - nA >= 1:
        quark.append(frozenset(triplet_charges(Xt, variant)[:2]))
    if nA >= 1:
        quark.append(frozenset(triplet_charges(Xa, variant, anti=True)[:2]))
    for p in quark:
        assert p == frozenset({Qu, Qd}), (p, Qu, Qd)
    return pairs | set(quark)


# ------------------------------------------------------------------------------------------
# gauge-boson mass matrix
# ------------------------------------------------------------------------------------------
def _gell_mann():
    i = 1j
    r3 = math.sqrt(3)
    z = lambda: [[0j] * 3 for _ in range(3)]
    L = [z() for _ in range(8)]
    L[0][0][1] = L[0][1][0] = 1
    L[1][0][1], L[1][1][0] = -i, i
    L[2][0][0], L[2][1][1] = 1, -1
    L[3][0][2] = L[3][2][0] = 1
    L[4][0][2], L[4][2][0] = -i, i
    L[5][1][2] = L[5][2][1] = 1
    L[6][1][2], L[6][2][1] = -i, i
    L[7][0][0] = L[7][1][1] = 1 / r3
    L[7][2][2] = -2 / r3
    return [[[x / 2 for x in row] for row in lam] for lam in L]


def _gens(X):
    t = _gell_mann()
    t.append([[complex(X) if a == c else 0j for c in range(3)] for a in range(3)])
    return t


def mass_matrix(variant, g, gX, w, v1, v2):
    vev = {"w": w, "v1": v1, "v2": v2}
    gA = [g] * 8 + [gX]
    M = [[0.0] * 9 for _ in range(9)]
    for X, k, name in _vev_slots(variant):
        t = _gens(X)
        phi = [0.0] * 3
        phi[k] = vev[name] / math.sqrt(2)
        for A in range(9):
            for B in range(9):
                s = 0j
                for a in range(3):
                    for c in range(3):
                        anti = sum(t[A][a][d] * t[B][d][c] + t[B][a][d] * t[A][d][c] for d in range(3))
                        s += phi[a] * anti * phi[c]
                M[A][B] += gA[A] * gA[B] * s.real
    return M


def photon_direction(variant, g, gX):
    n = [0.0] * 9
    n[2] = 1 / g
    n[7] = _beta(variant) / g
    n[8] = 1 / gX
    return n


def inv_e2(variant, g, gX):
    return math.fsum(x * x for x in photon_direction(variant, g, gX))


_NEUTRAL = (2, 7, 8)


def _neutral_block(variant, g, gX, w, v1, v2):
    M = mass_matrix(variant, g, gX, w, v1, v2)
    return [[M[i][j] for j in _NEUTRAL] for i in _NEUTRAL]


def neutral_masses(variant, g, gX, w, v1, v2):
    ev = toolkit.eigvalsh(_neutral_block(variant, g, gX, w, v1, v2))
    ev.sort(key=abs)
    return tuple(sorted(ev[1:]))


def vev_from_GF(G_F):
    return (math.sqrt(2) * G_F) ** -0.5


def mz_tree(G_F, alpha_inv, s2):
    alpha = 1 / alpha_inv
    return math.sqrt(math.pi * alpha / (math.sqrt(2) * G_F * s2 * (1 - s2)))


# ------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("== triplet charges (second route: trace 3X, spacing, conjugate) ==")
    for var in ("-1/sqrt3", "+1/sqrt3"):
        for X in (Fraction(-1, 3), Fraction(2, 3), Fraction(1, 3), Fraction(-2, 3)):
            q, qa = triplet_charges(X, var), triplet_charges(X, var, anti=True)
            conj = [-x for x in triplet_charges(-X, var)]
            print(var, X, q, qa, sum(q) == 3 * X, q[0] - q[1] == 1, qa == conj)
        print("  vev slots:", [(str(X), k + 1, n) for X, k, n in _vev_slots(var)])

    print("== quark charges vs proton route ==")
    for Nc in (1, 3, 5, 7, 9):
        Qu, Qd = quark_charges(Nc)
        qp = Fraction(Nc + 1, 2) * Qu + Fraction(Nc - 1, 2) * Qd
        print(Nc, Qu, Qd, "closed form", Fraction(Nc + 1, 2 * Nc), "q_p + q_e =", qp - 1)
        print("   pairs", {v: doublet_charge_pairs(Nc, v) for v in ("-1/sqrt3", "+1/sqrt3")})

    g, gX, w, v1, v2 = 0.65, 0.8, 4000.0, 150.0, 190.0
    for var in ("-1/sqrt3", "+1/sqrt3"):
        beta = _beta(var)
        print(f"== {var} ==")
        M = mass_matrix(var, g, gX, w, v1, v2)
        n = photon_direction(var, g, gX)
        print(" |M n| =", max(abs(sum(M[i][k] * n[k] for k in range(9))) for i in range(9)))
        M0 = mass_matrix(var, g, gX, w, 0.0, 0.0)
        ev0 = toolkit.eigvalsh(M0)
        print(" massless at v = 0:", sum(abs(x) < 1e-12 * max(ev0) for x in ev0))
        gY2 = 1 / (beta ** 2 / g ** 2 + 1 / gX ** 2)
        print(" 1/e^2:", inv_e2(var, g, gX), "SM route 1/g^2 + 1/gY^2:", 1 / g ** 2 + 1 / gY2)
        N = _neutral_block(var, g, gX, w, v1, v2)
        tr = N[0][0] + N[1][1] + N[2][2]
        c2 = sum(N[i][i] * N[j][j] - N[i][j] * N[j][i] for i in range(3) for j in range(i + 1, 3))
        disc = math.sqrt(tr * tr - 4 * c2)
        print(" eigvalsh:", neutral_masses(var, g, gX, w, v1, v2),
              " char. poly:", (2 * c2 / (tr + disc), (tr + disc) / 2))
        vs = v1 * v1 + v2 * v2
        print(" LO: MZ^2", (g * g + gY2) * vs / 4, " MZ'^2", (g * g + beta ** 2 * gX ** 2) * w * w / 3)
        cw2 = g * g / (g * g + gY2)
        rho = lambda W: (g * g * vs / 4) / (neutral_masses(var, g, gX, W, v1, v2)[0] * cw2)
        print(" rho-1:", rho(w) - 1, " ratio on doubling w:", (rho(w) - 1) / (rho(2 * w) - 1))

        # vev and M_Z second routes
        GF, ainv, s2 = inputs.G_F, inputs.ALPHA_MZ_INV, inputs.S2_MZ
        v = vev_from_GF(GF)
        th = 0.6
        Mv = mass_matrix(var, g, gX, w, v * math.cos(th), v * math.sin(th))
        print(" G_F from M_W:", math.sqrt(2) * g * g / (8 * Mv[0][0]), "input", GF)
        e = math.sqrt(4 * math.pi / ainv)
        gg, gy = e / math.sqrt(s2), e / math.sqrt(1 - s2)
        gx = (1 / gy ** 2 - beta ** 2 / gg ** 2) ** -0.5
        for W in (1e4, 1e5, 1e6):
            mz = math.sqrt(neutral_masses(var, gg, gx, W, v * math.cos(th), v * math.sin(th))[0])
            print(f"  w = {W:.0e}: M_Z from matrix {mz:.9f}  mz_tree {mz_tree(GF, ainv, s2):.9f}")
