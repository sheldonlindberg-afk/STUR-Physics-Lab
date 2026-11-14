"""running: one-loop running of the SM and 3-3-1 couplings to the Planck scale (SPEC.md section 9).

Derivations and second routes: DERIVATION_running.md. Coefficients are exact Fractions computed
from the field content; every 3-3-1 charge comes from rung 1 (gauge331.triplet_charges,
gauge331.quark_charges) at call time.
"""
import math
from fractions import Fraction

import inputs
import toolkit
import gauge331

PROVENANCE = {
    "sm_coefficients": ("derived", "b = -(11/3)C2 + (2/3) sum_Weyl T + (1/3) sum_scalar T summed over SPEC 9's SM"
                                   " table (3 gens of Q, u^c, d^c, L, e^c; one Higgs doublet), U(1): Y^2 per"
                                   " component, SU(2): T = 1/2 per doublet times colour"),
    "b_331": ("derived", "same formula over SPEC 2/9 content: N_c lepton triplets, n_A = (1+N_c)/2 antitriplet and"
                         " N_c - n_A triplet quark families (N_c colours), singlet partners X = -Q for each charged"
                         " component, 3 complex scalar triplets; X_L from Q_e = -1, X_t, X_a from (Q_u, Q_d), all"
                         " via gauge331.triplet_charges and gauge331.quark_charges"),
    "couplings_at": ("derived", "1/alpha_i(mu) = 1/alpha_i(M_Z) - b_i/(2 pi) ln(mu/M_Z) with b_i = sm_coefficients"
                                " and boundary 1/alpha_Y = (1-s^2)/alpha, 1/alpha_2 = s^2/alpha (inputs)"),
    "matching_331": ("derived", "1/alpha_L = 1/alpha_2; 1/alpha_X from gauge331.inv_e2(g_L, g_X) = (1/alpha_Y +"
                                " 1/alpha_2)/(4 pi), solved for u = 1/g_X^2 (inv_e2 affine in u, two-point solve);"
                                " closed form 1/alpha_Y - beta^2/alpha_2"),
    "landau_pole": ("derived", "1/alpha_X(mu) = 1/alpha_X(mu0) - b_X/(2 pi) ln(mu/mu0) = 1 with mu0 = MU_331,"
                               " matching_331 and b_331: mu = mu0 exp(2 pi (1/alpha_X0 - 1)/b_X)"),
}

# SPEC 9 group-theory weights (postulates, exact)
_W_GAUGE, _W_WEYL, _W_SCALAR = Fraction(-11, 3), Fraction(2, 3), Fraction(1, 3)
_T_FUND = Fraction(1, 2)


def _b_coeff(C2, weyl_T, scalar_T):
    return _W_GAUGE * C2 + _W_WEYL * weyl_T + _W_SCALAR * scalar_T


# ------------------------------------------------------------------------------------------
# Standard Model
# ------------------------------------------------------------------------------------------
def _sm_table():
    """(name, SU(2) dim, colour dim, Y) per generation, left-handed Weyl (SPEC 9)."""
    return [("Q", 2, 3, Fraction(1, 6)), ("u^c", 1, 3, Fraction(-2, 3)), ("d^c", 1, 3, Fraction(1, 3)),
            ("L", 2, 1, Fraction(-1, 2)), ("e^c", 1, 1, Fraction(1))]


_SM_GENS, _SM_COLOURS = 3, 3
_HIGGS_Y = Fraction(1, 2)


def sm_coefficients():
    ferm_Y = ferm_2 = Fraction(0)
    for _, d2, dc, Y in _sm_table():
        ferm_Y += _SM_GENS * d2 * dc * Y * Y
        if d2 == 2:
            ferm_2 += _SM_GENS * dc * _T_FUND
    scal_Y = 2 * _HIGGS_Y * _HIGGS_Y          # one complex doublet: 2 components
    scal_2 = _T_FUND
    bY = _b_coeff(0, ferm_Y, scal_Y)
    b2 = _b_coeff(2, ferm_2, scal_2)
    return bY, b2


# ------------------------------------------------------------------------------------------
# 3-3-1 content (charges from rung 1)
# ------------------------------------------------------------------------------------------
def _b_of(variant):
    """b = beta/(2 sqrt3) read off rung 1: triplet comp 1 at X = 0 is 1/2 + b."""
    return gauge331.triplet_charges(0, variant)[0] - Fraction(1, 2)


def _scalar_X(variant):
    """SPEC 2 postulate: the three scalar triplets' X charges."""
    if _b_of(variant) < 0:
        return (Fraction(-1, 3), Fraction(2, 3), Fraction(-1, 3))
    return (Fraction(1, 3), Fraction(1, 3), Fraction(-2, 3))


def _content(Nc, variant):
    """List of fermion SU(3)_L (anti)triplets: (X, charges[3], colour multiplicity, number of copies)."""
    if Nc < 1 or Nc % 2 == 0:
        raise ValueError("N_c must be a positive odd integer")
    Qu, Qd = gauge331.quark_charges(Nc)
    Ng, nA = Nc, (1 + Nc) // 2
    nT = Ng - nA
    # lepton triplet: Q_e = -1 in component 2
    XL = Fraction(-1) - gauge331.triplet_charges(0, variant)[1]
    qL = gauge331.triplet_charges(XL, variant)
    assert qL[1] == -1 and qL[0] == 0
    assert XL == (Fraction(-1, 3) if _b_of(variant) < 0 else Fraction(-2, 3))     # SPEC 2's stated X_L
    # quark triplet: first two = (Q_u, Q_d)
    Xt = Qu - gauge331.triplet_charges(0, variant)[0]
    qT = gauge331.triplet_charges(Xt, variant)
    assert qT[:2] == [Qu, Qd]
    # antitriplet: first two = {Q_u, Q_d} in some order
    c1 = gauge331.triplet_charges(0, variant, anti=True)[0]
    Xa = None
    for cand in (Qu - c1, Qd - c1):
        if set(gauge331.triplet_charges(cand, variant, anti=True)[:2]) == {Qu, Qd}:
            Xa = cand
            break
    if Xa is None:
        raise ArithmeticError("no antitriplet X reproduces (Q_u, Q_d)")
    qA = gauge331.triplet_charges(Xa, variant, anti=True)
    return [(XL, qL, 1, Ng), (Xt, qT, Nc, nT), (Xa, qA, Nc, nA)]


def b_331(Nc, variant):
    multiplets = _content(Nc, variant)
    weyl_X = weyl_L = Fraction(0)
    for X, q, col, copies in multiplets:
        weyl_X += copies * col * 3 * X * X                              # the (anti)triplet itself
        weyl_X += copies * col * sum(c * c for c in q if c != 0)        # singlet partners, X = -Q
        weyl_L += copies * col * _T_FUND
    Xs = _scalar_X(variant)
    scal_X = sum(3 * X * X for X in Xs)
    scal_L = len(Xs) * _T_FUND
    bX = _b_coeff(0, weyl_X, scal_X)
    bL = _b_coeff(3, weyl_L, scal_L)
    return bX, bL


# ------------------------------------------------------------------------------------------
# running and matching
# ------------------------------------------------------------------------------------------
def couplings_at(mu):
    mz, ainv, s2 = inputs.MZ_MEAS, inputs.ALPHA_MZ_INV, inputs.S2_MZ
    bY, b2 = sm_coefficients()
    t = math.log(mu / mz) / (2 * math.pi)
    return (1 - s2) * ainv - float(bY) * t, s2 * ainv - float(b2) * t


def matching_331(mu, variant):
    aY, a2 = couplings_at(mu)
    aL = a2
    gL = math.sqrt(4 * math.pi / aL)
    target = (aY + a2) / (4 * math.pi)
    F = lambda u: gauge331.inv_e2(variant, gL, u ** -0.5)
    u1, u2 = 1 / gL ** 2, 2 / gL ** 2
    f1, f2 = F(u1), F(u2)
    u = u1 + (target - f1) * (u2 - u1) / (f2 - f1)
    if not u > 0:
        raise ArithmeticError(f"no real g_X at mu = {mu}: 1/g_X^2 = {u}")
    resid = abs(F(u) - target) / target
    if resid > 1e-12:
        raise ArithmeticError(f"inv_e2 not affine in 1/g_X^2: residual {resid}")
    return 4 * math.pi * u, aL


def landau_pole(Nc, variant):
    mu0 = inputs.MU_331
    aX0 = matching_331(mu0, variant)[0]
    bX = float(b_331(Nc, variant)[0])
    return mu0 * math.exp(2 * math.pi * (aX0 - 1) / bX)


# ------------------------------------------------------------------------------------------
if __name__ == "__main__":
    bY, b2 = sm_coefficients()
    print("== SM ==  b_Y, b_2 =", bY, b2, "  GUT-normalised (3/5) b_Y =", Fraction(3, 5) * bY)
    s3 = s1 = s2Y = Fraction(0)
    for name, d2, dc, Y in _sm_table():
        s3 += d2 * dc * Y ** 3
        s1 += d2 * dc * Y
        if d2 == 2:
            s2Y += dc * Y
            print(f"  {name}: Q = {Fraction(1, 2) + Y}, {Fraction(-1, 2) + Y}")
        else:
            print(f"  {name}: Q = {Y}")
    print("  anomalies Y^3, grav, SU2^2 Y:", s3, s1, s2Y)

    print("== b_331: enumeration vs closed form (DERIVATION 2.3) ==")
    for var in ("-1/sqrt3", "+1/sqrt3"):
        b = _b_of(var)
        for Nc in (1, 3, 5, 7, 9):
            eps = Fraction(1, 2 * Nc)
            Qu, Qd = Fraction(Nc + 1, 2 * Nc), Fraction(1 - Nc, 2 * Nc)
            nA, nT = (1 + Nc) // 2, (Nc - 1) // 2
            XL, Xt, Xa = -Fraction(1, 2) - b, eps - b, eps + b
            Ft = 3 * Nc * XL ** 2 + 3 * Nc * (nT * Xt ** 2 + nA * Xa ** 2)
            Fs = (Nc * (1 + (Fraction(1, 2) + 3 * b) ** 2) + Nc * nT * (Qu ** 2 + Qd ** 2 + (eps - 3 * b) ** 2)
                  + Nc * nA * (Qu ** 2 + Qd ** 2 + (eps + 3 * b) ** 2))
            bXc = Fraction(2, 3) * (Ft + Fs) + Fraction(2, 3)
            bLc = -11 + Fraction(Nc * (Nc + 1), 3) + Fraction(1, 2)
            bX, bL = b_331(Nc, var)
            print(f"  {var} Nc={Nc}: b_X = {bX} (closed {bXc})  b_L = {bL} (closed {bLc})",
                  bX == bXc and bL == bLc)
        # Y-identity per triplet: sum X^2 = sum Y^2 - 6 b^2
        for X, q, col, n in _content(3, var):
            sgn = 1 if q[0] - q[1] == 1 else -1
            Ys = [qq - sgn * t3 for qq, t3 in zip(q, (Fraction(1, 2), Fraction(-1, 2), 0))]
            print("   triplet X", X, "sum X^2 == sum Y^2 - 6b^2:", 3 * X * X == sum(y * y for y in Ys) - 6 * b * b)

    print("== couplings: closed form vs step-wise Euler integration in ln mu ==")
    mz = inputs.MZ_MEAS
    y0, w0 = couplings_at(mz)
    print("  1/aY + 1/a2 at M_Z:", y0 + w0, " input", inputs.ALPHA_MZ_INV)
    for mu in (300.0, 4000.0, 1e16):
        T = math.log(mu / mz)
        n = 100
        h = T / n
        y, w = y0, w0
        for _ in range(n):
            ky = -float(bY) / (2 * math.pi)
            kw = -float(b2) / (2 * math.pi)
            y += h * ky
            w += h * kw
        print(f"  mu={mu:.3g}: {couplings_at(mu)}  Euler {(y, w)}")

    print("== matching: two-point solve vs closed form 1/aY - beta^2/a2 ==")
    for var in ("-1/sqrt3", "+1/sqrt3"):
        beta2 = 12 * _b_of(var) ** 2
        for mu in (2000.0, 4000.0, 3e4):
            aX, aL = matching_331(mu, var)
            aY, a2 = couplings_at(mu)
            print(f"  {var} mu={mu:g}: 1/aX = {aX:.12f}  closed {aY - float(beta2) * a2:.12f}  1/aL = {aL:.6f}")

    print("== Landau pole: closed form vs toolkit.bisect in ln mu ==")
    for var in ("-1/sqrt3", "+1/sqrt3"):
        for Nc in (3, 5):
            p = landau_pole(Nc, var)
            aX0 = matching_331(inputs.MU_331, var)[0]
            bX = float(b_331(Nc, var)[0])
            g = lambda t: aX0 - bX / (2 * math.pi) * t - 1
            t = toolkit.bisect(g, 0.0, 400.0)
            print(f"  {var} Nc={Nc}: pole {p:.6e} GeV  bisect {inputs.MU_331 * math.exp(t):.6e}"
                  f"  (quoted 3-loop {inputs.POLES_331[var][(Nc - 3) // 2]:.3e})")
