"""Stage `running` (build 2026-11-b): the 3-3-1 couplings at one loop, to the scale where alpha_X = 1.

Everything is derived from SPEC.md sections 9 and 2; nothing is quoted (inputs.POLES_331 is not used).
Derivations and second routes: DERIVATION_running.md (same directory), section numbers cited below.
"""
import math
from fractions import Fraction

import inputs
import toolkit
import gauge331

PROVENANCE = {
    "sm_coefficients": ("derived", "b = -(11/3) C2 + (2/3) sum_Weyl T + (1/3) sum_scalar T summed over the multiplet"
                                   " list of SPEC section 9 (3 colours, 3 generations, one Higgs doublet), T = 1/2 per"
                                   " doublet, dim * Y^2 for U(1)_Y; exact Fractions (DERIVATION section 1)"),
    "b_331": ("derived", "same master formula over the 3-3-1 content: X charges solved from rung 1's"
                         " gauge331.triplet_charges and gauge331.quark_charges (electron charge -1, doublet"
                         " (Q_u, Q_d)), one singlet of X = -q per charged component, three complex scalar"
                         " triplets; exact Fractions (section 2)"),
    "couplings_at": ("derived", "exact one-loop solution 1/alpha_i(mu) = 1/alpha_i(M_Z) - b_i ln(mu/M_Z)/(2 pi) with"
                                " SPEC's boundary values at inputs.MZ_MEAS and b_i from sm_coefficients (section 3)"),
    "matching_331": ("derived", "1/alpha_L = 1/alpha_2; g_X solved from gauge331.inv_e2(g_L, g_X) = (1/alpha_Y +"
                                " 1/alpha_2)/(4 pi), using that inv_e2 is affine in 1/g_X^2 (slope and intercept"
                                " measured from two calls) (section 4)"),
    "landau_pole": ("derived", "mu0 exp(2 pi (1/alpha_X(mu0) - 1)/b_X): the one-loop solution run from"
                               " matching_331(inputs.MU_331) with b_331's b_X to alpha_X = 1 (section 5)"),
}

_WEYL, _SCALAR = "weyl", "scalar"


# ------------------------------------------------------------------------------------------
# the master formula on a multiplet list (DERIVATION section 0)
# ------------------------------------------------------------------------------------------
def _weight(kind):
    """Coefficient of T(R) in b: 2/3 per Weyl fermion, 1/3 per complex scalar."""
    return Fraction(2, 3) if kind == _WEYL else Fraction(1, 3)


def _b_nonabelian(N, fields):
    """fields: (kind, mult, dim, charge); dim == N marks a (anti)fundamental of SU(N), index 1/2."""
    b = -Fraction(11, 3) * N
    for kind, mult, dim, _ in fields:
        if dim == N:
            b += _weight(kind) * mult * Fraction(1, 2)
        elif dim != 1:
            raise ValueError("only singlets and fundamentals are supported")
    return b


def _b_abelian(fields):
    return sum((_weight(kind) * mult * dim * Fraction(q) ** 2 for kind, mult, dim, q in fields), Fraction(0))


# ------------------------------------------------------------------------------------------
# Standard Model (section 1)
# ------------------------------------------------------------------------------------------
def _sm_fields(Ng=3, Nc=3):
    """(kind, mult, dim under SU(2), Y) of SPEC section 9; colour multiplicity folded into mult."""
    Y = lambda p, q: Fraction(p, q)
    return [
        (_WEYL, Ng * Nc, 2, Y(1, 6)),      # quark doublet
        (_WEYL, Ng * Nc, 1, Y(-2, 3)),     # u^c
        (_WEYL, Ng * Nc, 1, Y(1, 3)),      # d^c
        (_WEYL, Ng, 2, Y(-1, 2)),          # lepton doublet
        (_WEYL, Ng, 1, Y(1, 1)),           # e^c
        (_SCALAR, 1, 2, Y(1, 2)),          # Higgs doublet
    ]


def sm_coefficients():
    fields = _sm_fields()
    return _b_abelian(fields), _b_nonabelian(2, fields)


# ------------------------------------------------------------------------------------------
# 3-3-1 content (section 2)
# ------------------------------------------------------------------------------------------
def _scalar_X(variant):
    """SPEC section 2's scalar X charges (postulates)."""
    third = Fraction(1, 3)
    if variant == "-1/sqrt3":
        return (-third, 2 * third, -third)
    if variant == "+1/sqrt3":
        return (third, third, -2 * third)
    raise ValueError(f"unknown variant {variant!r}")


def _fermion_triplets(Nc, variant):
    """[(mult, X, anti)] for the lepton triplets, quark triplets and quark antitriplets; X solved from rung 1."""
    s = gauge331.triplet_charges(0, variant)                 # T3 + beta T8 on a triplet
    sa = gauge331.triplet_charges(0, variant, anti=True)
    Qu, Qd = gauge331.quark_charges(Nc)
    XL = Fraction(-1) - s[1]                                 # electron: T3 = -1/2 component, charge -1
    Xt = Qu - s[0]                                           # first two components (Q_u, Q_d)
    if s[1] + Xt != Qd:
        raise ArithmeticError("quark triplet does not contain the (Q_u, Q_d) doublet")
    cands = [X for X in (Qu - sa[0], Qu - sa[1])             # (Q_u, Q_d) in either order
             if {sa[0] + X, sa[1] + X} == {Qu, Qd}]
    if len(set(cands)) != 1:
        raise ArithmeticError("antitriplet X is not uniquely fixed")
    Xa = cands[0]
    Ng = Fraction(Nc)
    nA = Fraction(1 + Nc, 2)
    nT = Ng - nA
    return [(Ng, XL, False), (nT * Nc, Xt, False), (nA * Nc, Xa, True)]


def _fields_331(Nc, variant):
    """(kind, mult, dim under SU(3)_L, X) of everything above the 3-3-1 scale."""
    fields = []
    for mult, X, anti in _fermion_triplets(Nc, variant):
        fields.append((_WEYL, mult, 3, X))
        for q in gauge331.triplet_charges(X, variant, anti=anti):
            if q != 0:
                fields.append((_WEYL, mult, 1, -q))          # singlet partner of the opposite charge
    for X in _scalar_X(variant):
        fields.append((_SCALAR, Fraction(1), 3, X))
    return fields


def b_331(Nc, variant):
    fields = _fields_331(Nc, variant)
    return _b_abelian(fields), _b_nonabelian(3, fields)


# ------------------------------------------------------------------------------------------
# running and matching (sections 3-5)
# ------------------------------------------------------------------------------------------
def _run(inv_alpha0, b, t):
    """1/alpha after t = ln(mu/mu0): the exact solution of d(1/alpha)/dt = -b/(2 pi)."""
    return inv_alpha0 - float(b) * t / (2 * math.pi)


def couplings_at(mu):
    s2, ainv = inputs.S2_MZ, inputs.ALPHA_MZ_INV
    bY, b2 = sm_coefficients()
    t = math.log(mu / inputs.MZ_MEAS)
    return _run((1 - s2) * ainv, bY, t), _run(s2 * ainv, b2, t)


def matching_331(mu, variant):
    aY, a2 = couplings_at(mu)
    gL = math.sqrt(4 * math.pi / a2)                         # g_L = g_2
    target = (aY + a2) / (4 * math.pi)                       # the Standard Model's 1/e^2
    E = lambda u: gauge331.inv_e2(variant, gL, 1 / math.sqrt(u))   # affine in u = 1/g_X^2
    u1, u2 = 1.0, 4.0
    E1, E2 = E(u1), E(u2)
    slope = (E2 - E1) / (u2 - u1)
    intercept = E1 - slope * u1
    u = (target - intercept) / slope
    if not u > 0:
        raise ValueError("matching has no real g_X at this scale")
    return 4 * math.pi * u, a2


def landau_pole(Nc, variant):
    mu0 = inputs.MU_331
    aX0 = matching_331(mu0, variant)[0]
    bX = b_331(Nc, variant)[0]
    if not (bX > 0 and aX0 > 1):
        raise ValueError("alpha_X does not reach 1 above the matching scale")
    return mu0 * math.exp(2 * math.pi * (aX0 - 1) / float(bX))


# ------------------------------------------------------------------------------------------
# second routes (DERIVATION_running.md)
# ------------------------------------------------------------------------------------------
def _rk4_alpha(alpha0, b, t, n=4000):
    """Integrate d alpha/dt = b alpha^2/(2 pi) from 0 to t (the non-linear form of the same equation)."""
    f = lambda a: float(b) * a * a / (2 * math.pi)
    h, a = t / n, alpha0
    for _ in range(n):
        k1 = f(a)
        k2 = f(a + h * k1 / 2)
        k3 = f(a + h * k2 / 2)
        k4 = f(a + h * k3)
        a += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return a


def _sm_closed(Ng, Nc):
    Ng, Nc = Fraction(Ng), Fraction(Nc)
    bY = Fraction(2, 3) * Ng * (11 * Nc / 18 + Fraction(3, 2)) + Fraction(1, 3) * 2 * Fraction(1, 4)
    b2 = -Fraction(11, 3) * 2 + Fraction(1, 3) * Ng * (Nc + 1) + Fraction(1, 6)
    return bY, b2


def _sm_anomalies():
    f = [x for x in _sm_fields() if x[0] == _WEYL]
    coloured = f[:3]
    return (sum(m * d * y for _, m, d, y in f), sum(m * d * y ** 3 for _, m, d, y in f),
            sum(m * y for _, m, d, y in f if d == 2), sum(d * y for _, m, d, y in coloured))


def _closed_331(Nc, variant):
    """Closed forms (2.4), (2.5), coded separately from the multiplet list."""
    trip = _fermion_triplets(Nc, variant)
    ferm = Fraction(0)
    for mult, X, anti in trip:
        S = sum(q * q for q in gauge331.triplet_charges(X, variant, anti=anti))   # neutral ones add 0
        ferm += mult * (3 * X * X + S)
    bX = Fraction(2, 3) * ferm + sum(X * X for X in _scalar_X(variant))
    bL = -11 + Fraction(1, 3) * Nc * (1 + Nc) + Fraction(1, 2)
    return bX, bL


def _anomalies_331(Nc, variant):
    trip = _fermion_triplets(Nc, variant)
    f = [x for x in _fields_331(Nc, variant) if x[0] == _WEYL]
    a_LLX = sum(m * X for m, X, _ in trip)
    a_LLL = sum(-m if anti else m for m, X, anti in trip)
    a_grav = sum(m * d * X for _, m, d, X in f)
    a_XXX = sum(m * d * X ** 3 for _, m, d, X in f)
    # colour: the quark (anti)triplets (colour N_c) against their singlet partners (colour N_c-bar), per colour
    a_CCX = Fraction(0)
    for m, X, anti in trip[1:]:
        qs = gauge331.triplet_charges(X, variant, anti=anti)
        a_CCX += (m / Nc) * (3 * X + sum(-q for q in qs if q != 0))
    return a_LLX, a_LLL, a_grav, a_XXX, a_CCX


def _bY_of_331_matter(Nc, variant):
    """Route C: sum of w mult (Q - T3)^2 over every component, from electric charges only."""
    half = Fraction(1, 2)
    t3 = (half, -half, Fraction(0))
    tot = Fraction(0)
    for mult, X, anti in _fermion_triplets(Nc, variant):
        for q, t in zip(gauge331.triplet_charges(X, variant, anti=anti), t3):
            tot += _weight(_WEYL) * mult * (q - (-t if anti else t)) ** 2
            if q != 0:
                tot += _weight(_WEYL) * mult * q ** 2            # singlet: Y = Q = -q, T3 = 0
    for X in _scalar_X(variant):
        for q, t in zip(gauge331.triplet_charges(X, variant), t3):
            tot += _weight(_SCALAR) * (q - t) ** 2
    return tot


if __name__ == "__main__":
    two_pi = 2 * math.pi
    print("== Standard Model coefficients ==")
    bY, b2 = sm_coefficients()
    print(f"multiplet sum (b_Y, b_2) = ({bY}, {b2}); closed forms (1.1), (1.2) = {_sm_closed(3, 3)};"
          f" equal: {(bY, b2) == _sm_closed(3, 3)}")
    Qu, Qd = gauge331.quark_charges(3)
    half = Fraction(1, 2)
    ys = [y for _, _, _, y in _sm_fields()]
    emb = (half + ys[0] == Qu and -half + ys[0] == Qd and ys[1] == -Qu and ys[2] == -Qd
           and half + ys[3] == 0 and -half + ys[3] == -1 and ys[4] == 1)
    print(f"Q = T3 + Y reproduces rung 1's (Q_u, Q_d) = ({Qu}, {Qd}) and leptons (0, -1): {emb}")
    print(f"anomaly sums (Y, Y^3, doublet Y, coloured Y) = {tuple(str(x) for x in _sm_anomalies())} (all 0)")
    gen = [x for x in _sm_fields(1, 3) if x[0] == _WEYL]
    print(f"one generation: (3/5) sum Y^2 = {Fraction(3, 5) * sum(m * d * y * y for _, m, d, y in gen)};"
          f" SU(2) index sum = {sum(m * half for _, m, d, y in gen if d == 2)}")

    print("== 3-3-1 coefficients ==")
    for var in gauge331.VARIANTS:
        trip = _fermion_triplets(3, var)
        print(f"{var}: N_c = 3 (mult, X, anti) = {[(str(m), str(X), a) for m, X, a in trip]}")
        for Nc in (1, 3, 5, 7):
            b = b_331(Nc, var)
            c = _closed_331(Nc, var)
            an = _anomalies_331(Nc, var)
            lhs = _bY_of_331_matter(Nc, var)
            rhs = Fraction(1, 3) * (b[1] + 11) + b[0]
            print(f"   N_c = {Nc}: (b_X, b_L) = ({b[0]}, {b[1]}); closed form equal: {b == c};"
                  f" anomalies (LLX, LLL, grav, XXX, CCX) = {tuple(str(x) for x in an)};"
                  f" embedding route {lhs} vs beta^2 b_L(matter) + b_X = {rhs}: {lhs == rhs}")
    print(f"hand value (3, -1/sqrt3): (26/3, -13/2); code: {b_331(3, '-1/sqrt3')}")

    print("== Standard Model running ==")
    mz = inputs.MZ_MEAS
    y0, w0 = couplings_at(mz)
    print(f"at M_Z: 1/alpha_Y = {y0:.6f}, 1/alpha_2 = {w0:.6f}, sum = {y0 + w0:.6f} (1/alpha-hat ="
          f" {inputs.ALPHA_MZ_INV})")
    for mu in (1e3, inputs.MU_331, 1e5):
        y, w = couplings_at(mu)
        t = math.log(mu / mz)
        yr, wr = 1 / _rk4_alpha(1 / y0, bY, t), 1 / _rk4_alpha(1 / w0, b2, t)
        n = 11
        dt = t / (n - 1)
        yt = y0 + toolkit.trapezoid([-float(bY) / two_pi] * n, dt)
        print(f"mu = {mu:.0f}: closed form ({y:.9f}, {w:.9f}); RK4 of d alpha/dt = b alpha^2/2pi ({yr:.9f},"
              f" {wr:.9f}); trapezoid of the slope, 1/alpha_Y = {yt:.9f}")

    print("== matching ==")
    for var in gauge331.VARIANTS:
        for mu in (inputs.MU_331, 3e4):
            aX, aL = matching_331(mu, var)
            aY, a2 = couplings_at(mu)
            gL = math.sqrt(4 * math.pi / aL)
            target = (aY + a2) / (4 * math.pi)
            gXb = toolkit.bisect(lambda g: gauge331.inv_e2(var, gL, g) - target, 1e-2, 1e2)
            back = 4 * math.pi * gauge331.inv_e2(var, gL, math.sqrt(4 * math.pi / aX))
            print(f"{var}, mu = {mu:.0f}: 1/alpha_X = {aX:.9f}; closed form 1/alpha_Y - (1/3)/alpha_2 ="
                  f" {aY - a2 / 3:.9f}; bisection on g_X: {4 * math.pi / gXb ** 2:.9f};"
                  f" 4 pi inv_e2 = {back:.9f} vs 1/alpha_Y + 1/alpha_2 = {aY + a2:.9f}")

    print("== scale where alpha_X = 1 ==")
    mu0 = inputs.MU_331
    for var in gauge331.VARIANTS:
        for Nc in (3, 5):
            p = landau_pole(Nc, var)
            aX0 = matching_331(mu0, var)[0]
            bX = b_331(Nc, var)[0]
            F = lambda t: _run(aX0, bX, t) - 1
            tb = toolkit.bisect(F, 0.0, 1e3)
            arK = _rk4_alpha(1 / aX0, bX, math.log(p / mu0))
            y1, w1 = couplings_at(mu0)
            y2, w2 = couplings_at(2 * mu0)
            pred = 2 * math.exp(two_pi * ((y2 - w2 / 3) - (y1 - w1 / 3)) / float(bX))
            print(f"{var}, N_c = {Nc}: b_X = {bX}; closed form {p:.6e} GeV; bisection in ln mu"
                  f" {mu0 * math.exp(tb):.6e} GeV; RK4 alpha_X at the pole = {arK:.9f};"
                  f" doubling mu0 scales the pole by {pred:.6f} = 2^(1 - (b_Y - b_2/3)/b_X) ="
                  f" {2 ** (1 - float((bY - b2 / 3) / bX)):.6f}")
