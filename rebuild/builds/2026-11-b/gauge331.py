"""Stage `gauge331` (build 2026-11-b): SU(3)_L x U(1)_X -> SM -> electromagnetism.

Everything is derived from SPEC.md section 2; nothing is quoted. Derivations and second routes:
DERIVATION_gauge331.md (same directory), section numbers cited below.
"""
import math
import random
from fractions import Fraction

import inputs
import toolkit

PROVENANCE = {
    "triplet_charges": ("derived", "diagonal of Q = T3 + beta T8 + X with T3 = diag(1/2,-1/2,0), beta T8 ="
                                   " b diag(1,1,-2), b = beta/(2 sqrt3) = -+1/6; antitriplet flips the sign of the"
                                   " SU(3) part only (DERIVATION section 1)"),
    "quark_charges": ("derived", "exact root in Q_u of the affine [SU(3)_L]^2 U(1)_X anomaly N_g X_L + N_c[(N_g-n_A)"
                                 " X_t + n_A X_a], with X_L fixed by the electron charge -1, X_t and X_a by the"
                                 " doublet (Q_u, Q_d = Q_u - 1); slope from toolkit.exact_derivative (section 2)"),
    "doublet_charge_pairs": ("derived", "first two components, via triplet_charges, of the lepton triplet, quark"
                                        " triplet and quark antitriplet with the X charges of section 2 (section 3)"),
    "mass_matrix": ("derived", "M2_AB = g_A g_B sum_phi <phi>^dag {T_A, T_B} <phi> from |D phi|^2, explicit Gell-Mann"
                               " matrices, vevs placed in the neutral components found with triplet_charges"
                               " (sections 4, 5)"),
    "photon_direction": ("derived", "the direction n with sum_A n_A g_A T_A = Q: n_3 = 1/g, n_8 = beta/g, n_9 = 1/g_X;"
                                    " M2 n = 0 because Q annihilates every allowed vev (section 6)"),
    "inv_e2": ("derived", "e = 1/|n| from projecting the gauge field on the unit photon direction, so 1/e^2 = |n|^2 ="
                          " (1 + beta^2)/g^2 + 1/g_X^2 (section 6)"),
    "neutral_masses": ("derived", "two nonzero eigenvalues (toolkit.eigvalsh) of the decoupled (W^3, W^8, B_X) block"
                                  " of mass_matrix; the third is the photon's zero (section 7)"),
    "vev_from_GF": ("derived", "G_F/sqrt2 = g^2/(8 M_W^2) with M_W^2 = g^2 v^2/4 gives v = (sqrt2 G_F)^(-1/2)"
                               " (section 8)"),
    "mz_tree": ("derived", "M_Z^2 = M_W^2/c^2, M_W^2 = g^2 v^2/4, g^2 = 4 pi alpha/s^2, v from vev_from_GF:"
                           " M_Z^2 = pi alpha/(sqrt2 G_F s^2 (1 - s^2)) (section 9)"),
}

VARIANTS = ("-1/sqrt3", "+1/sqrt3")


# ------------------------------------------------------------------------------------------
# charges (exact)
# ------------------------------------------------------------------------------------------
def _sign(variant):
    if variant not in VARIANTS:
        raise ValueError(f"unknown variant {variant!r}")
    return -1 if variant.startswith("-") else 1


def _beta(variant):
    return _sign(variant) / math.sqrt(3)


def _b(variant):
    """b = beta/(2 sqrt3) = sign/6: beta T8 = b diag(1, 1, -2)."""
    return Fraction(_sign(variant), 2 * 3)


def triplet_charges(X, variant, anti=False):
    b = _b(variant)
    half = Fraction(1, 2)
    su3 = [half + b, -half + b, -2 * b]            # diagonal of T3 + beta T8
    if anti:
        su3 = [-q for q in su3]                    # -t^* = -t on the real diagonal generators
    return [q + Fraction(X) for q in su3]


def _lepton_X(variant):
    """Electron = T3 = -1/2 member of the lepton triplet, charge -1: -1/2 + b + X_L = -1."""
    return Fraction(-1) - triplet_charges(0, variant)[1]


def _quark_X(Qu, variant):
    """(X_t, X_a): triplet with first two (Q_u, Q_d); antitriplet with first two (Q_d, Q_u)."""
    Xt = Qu - triplet_charges(0, variant)[0]
    Xa = Qu - triplet_charges(0, variant, anti=True)[1]
    return Xt, Xa


def _families(Nc):
    """(N_g, n_A, N_g - n_A)."""
    Ng = Fraction(Nc)
    nA = Fraction(1 + Nc, 2)
    return Ng, nA, Ng - nA


def _anomaly(Qu, Nc, variant):
    """[SU(3)_L]^2 U(1)_X anomaly, sum of X over triplets and antitriplets (T(3) = T(3bar))."""
    Ng, nA, nT = _families(Nc)
    Xt, Xa = _quark_X(Qu, variant)
    return Ng * _lepton_X(variant) + Nc * (nT * Xt + nA * Xa)


def quark_charges(Nc):
    sols = []
    for variant in VARIANTS:
        A = lambda Qu: _anomaly(Qu, Nc, variant)
        slope = toolkit.exact_derivative(A, Fraction(0))
        sols.append(-A(Fraction(0)) / slope)       # root of an affine function
    if sols[0] != sols[1]:
        raise ArithmeticError("anomaly cancellation gives variant-dependent quark charges")
    Qu = sols[0]
    return Qu, Qu - 1


def doublet_charge_pairs(Nc, variant):
    Qu, _ = quark_charges(Nc)
    Ng, nA, nT = _families(Nc)
    Xt, Xa = _quark_X(Qu, variant)
    multiplets = [(Ng, _lepton_X(variant), False), (nT, Xt, False), (nA, Xa, True)]
    return {frozenset(triplet_charges(X, variant, anti=anti)[:2]) for n, X, anti in multiplets if n != 0}


# ------------------------------------------------------------------------------------------
# scalars and the mass matrix
# ------------------------------------------------------------------------------------------
def _scalar_X(variant):
    third = Fraction(1, 3)
    return (-third, 2 * third, -third) if _sign(variant) < 0 else (third, third, -2 * third)


def _vev_slots(variant):
    """[(X, component index 0..2, which vev: 0 = w, 1 = v1, 2 = v2)], from SPEC.md's placement rule."""
    Xs = _scalar_X(variant)
    neutral = [[k for k, q in enumerate(triplet_charges(X, variant)) if q == 0] for X in Xs]
    iw = next(i for i, nk in enumerate(neutral) if 2 in nk)
    slots, nxt = [], 1
    for i, X in enumerate(Xs):
        if i == iw:
            slots.append((X, 2, 0))
            continue
        rest = [k for k in neutral[i] if k != 2]
        if len(rest) != 1:
            raise ValueError("vev placement rule is ambiguous for this scalar content")
        slots.append((X, rest[0], nxt))
        nxt += 1
    return slots


def _gell_mann_half():
    """t_a = lambda_a/2, a = 1..8, as 3x3 complex lists."""
    def mat(entries):
        m = [[0j] * 3 for _ in range(3)]
        for (i, j), val in entries.items():
            m[i][j] = complex(val)
        return m
    lam = []
    for (i, j) in ((0, 1),):
        lam += [mat({(i, j): 1, (j, i): 1}), mat({(i, j): -1j, (j, i): 1j}), mat({(0, 0): 1, (1, 1): -1})]
    for (i, j) in ((0, 2), (1, 2)):
        lam += [mat({(i, j): 1, (j, i): 1}), mat({(i, j): -1j, (j, i): 1j})]
    s = 1 / math.sqrt(3)
    lam.append(mat({(0, 0): s, (1, 1): s, (2, 2): -2 * s}))
    return [[[x / 2 for x in row] for row in m] for m in lam]


def _matvec(m, v):
    return [sum(m[i][k] * v[k] for k in range(3)) for i in range(3)]


def mass_matrix(variant, g, gX, w, v1, v2):
    vevs = (w, v1, v2)
    ts = _gell_mann_half()
    M = [[0.0] * 9 for _ in range(9)]
    for X, comp, which in _vev_slots(variant):
        phi = [0j] * 3
        phi[comp] = vevs[which] / math.sqrt(2)
        ident = [[complex(float(X)) if i == j else 0j for j in range(3)] for i in range(3)]
        gens = ts + [ident]
        coup = [g] * 8 + [gX]
        Tphi = [_matvec(T, phi) for T in gens]     # T_A <phi>
        for A in range(9):
            for B in range(9):
                # <phi>^dag {T_A, T_B} <phi> = (T_A phi)^dag (T_B phi) + (T_B phi)^dag (T_A phi)
                val = sum((Tphi[A][k].conjugate() * Tphi[B][k]).real for k in range(3))
                M[A][B] += 2 * coup[A] * coup[B] * val
    return M


def photon_direction(variant, g, gX):
    n = [0.0] * 9
    n[2] = 1 / g                    # T3
    n[7] = _beta(variant) / g       # beta T8
    n[8] = 1 / gX                   # X
    return n


def inv_e2(variant, g, gX):
    return sum(x * x for x in photon_direction(variant, g, gX))


_NEUTRAL = (2, 7, 8)


def neutral_masses(variant, g, gX, w, v1, v2):
    M = mass_matrix(variant, g, gX, w, v1, v2)
    block = [[M[i][j] for j in _NEUTRAL] for i in _NEUTRAL]
    ev = toolkit.eigvalsh(block)
    return ev[1], ev[2]


def vev_from_GF(G_F):
    return 1 / math.sqrt(math.sqrt(2) * G_F)


def mz_tree(G_F, alpha_inv, s2):
    g = math.sqrt(4 * math.pi / (alpha_inv * s2))          # e = g s
    return g * vev_from_GF(G_F) / (2 * math.sqrt(1 - s2))  # M_Z = M_W / c, M_W = g v / 2


# ------------------------------------------------------------------------------------------
# second routes
# ------------------------------------------------------------------------------------------
def _q_vectors(variant, g, gX, w, v1, v2):
    """[(u, q)]: vev and neutral charge vector q = (g t3_kk, g t8_kk, gX X), closed form of section 5."""
    b = float(_b(variant))
    t3 = (1 / 2, -1 / 2, 0.0)
    t8 = tuple(x / (2 * math.sqrt(3)) for x in (1, 1, -2))
    vevs = (w, v1, v2)
    return [(vevs[which], (g * t3[k], g * t8[k], gX * float(X))) for X, k, which in _vev_slots(variant)]


def _closed_form_matrix(variant, g, gX, w, v1, v2):
    M = [[0.0] * 9 for _ in range(9)]
    for u, q in _q_vectors(variant, g, gX, w, v1, v2):
        for a, A in enumerate(_NEUTRAL):
            for c, B in enumerate(_NEUTRAL):
                M[A][B] += u * u * q[a] * q[c]
    M[0][0] = M[1][1] = g * g * (v1 * v1 + v2 * v2) / 4
    M[3][3] = M[4][4] = g * g * (w * w + v2 * v2) / 4
    M[5][5] = M[6][6] = g * g * (w * w + v1 * v1) / 4
    return M


def _closed_form_neutral(variant, g, gX, w, v1, v2):
    uq = _q_vectors(variant, g, gX, w, v1, v2)
    dot = lambda a, c: sum(x * y for x, y in zip(a, c))
    T = sum(u * u * dot(q, q) for u, q in uq)
    P = sum(uq[i][0] ** 2 * uq[j][0] ** 2 * (dot(uq[i][1], uq[i][1]) * dot(uq[j][1], uq[j][1])
                                           - dot(uq[i][1], uq[j][1]) ** 2)
            for i in range(3) for j in range(i + 1, 3))
    disc = math.sqrt(T * T - 4 * P)
    hi = (T + disc) / 2
    return P / hi, hi                                   # stable form of (T - disc)/2


if __name__ == "__main__":
    g, gX, w, v1, v2 = 0.65, 0.8, 4000.0, 150.0, 190.0
    print("== charges ==")
    for var in VARIANTS:
        ts = _gell_mann_half()
        X = _lepton_X(var)
        diag = [(ts[2][k][k] + _beta(var) * ts[7][k][k]).real + float(X) for k in range(3)]
        print(f"{var}: X_L = {X} (SPEC: {Fraction(-1, 3) if _sign(var) < 0 else Fraction(-2, 3)});"
              f" lepton triplet {triplet_charges(X, var)}; float route from Gell-Mann matrices {diag}")
        print(f"   scalar charges {[triplet_charges(Xs, var) for Xs in _scalar_X(var)]}, vev slots"
              f" (X, component, vev#) {_vev_slots(var)}")
    for Nc in (1, 3, 5, 7):
        Qu, Qd = quark_charges(Nc)
        Qu2 = Fraction(Nc + 1, 2 * Nc)                 # route 2: proton neutrality q_p + q_e = 0
        pairs_ok = all(doublet_charge_pairs(Nc, var) == {frozenset({Fraction(0), Fraction(-1)}),
                                                         frozenset({Qu2, Qu2 - 1})} for var in VARIANTS)
        print(f"N_c = {Nc}: anomaly route (Q_u, Q_d) = ({Qu}, {Qd}); proton route ({Qu2}, {Qu2 - 1});"
              f" equal: {Qu == Qu2}; doublet pairs as expected: {pairs_ok}")
    print("== bosons ==")
    rng = random.Random(7)
    for var in VARIANTS:
        M = mass_matrix(var, g, gX, w, v1, v2)
        C = _closed_form_matrix(var, g, gX, w, v1, v2)
        sc = max(abs(x) for row in M for x in row)
        d = max(abs(M[i][j] - C[i][j]) for i in range(9) for j in range(9)) / sc
        print(f"{var}: anticommutator build vs closed form, max relative difference {d:.2e}")
        n = photon_direction(var, g, gX)
        (_, qa), (_, qb), _ = _q_vectors(var, g, gX, w, v1, v2)
        cr = [qa[1] * qb[2] - qa[2] * qb[1], qa[2] * qb[0] - qa[0] * qb[2], qa[0] * qb[1] - qa[1] * qb[0]]
        n3 = [n[i] for i in _NEUTRAL]
        ratio = [c / x for c, x in zip(cr, n3)]
        worst = 0.0
        for _ in range(5):
            R = mass_matrix(var, g, gX, rng.uniform(500, 9000), rng.uniform(10, 200), rng.uniform(10, 200))
            worst = max(worst, max(abs(sum(R[i][k] * n[k] for k in range(9))) for i in range(9))
                        / max(abs(x) for row in R for x in row))
        print(f"   photon n = {n3}; null vector q_w x q_1 / n = {ratio} (constant = parallel);"
              f" |M n|/|M| on random vevs {worst:.1e}")
        print(f"   1/e^2 = |n|^2 = {inv_e2(var, g, gX):.12g}; formula (1+beta^2)/g^2 + 1/gX^2 ="
              f" {(1 + _beta(var) ** 2) / g ** 2 + 1 / gX ** 2:.12g}")
        print(f"   neutral masses: eigvalsh {neutral_masses(var, g, gX, w, v1, v2)};"
              f" closed form {_closed_form_neutral(var, g, gX, w, v1, v2)}")
        ev0 = toolkit.eigvalsh(mass_matrix(var, g, gX, w, 0.0, 0.0))
        print(f"   v1 = v2 = 0: massless states {sum(abs(x) < 1e-12 * max(ev0) for x in ev0)}")
        gY2 = 1 / (_beta(var) ** 2 / g ** 2 + 1 / gX ** 2)
        big = 1e3 * w
        r = g * g * (v1 * v1 + v2 * v2) / 4 / neutral_masses(var, g, gX, big, v1, v2)[0]
        r0 = g * g * (v1 * v1 + v2 * v2) / 4 / neutral_masses(var, g, gX, w, v1, v2)[0]
        c2 = g * g / (g * g + gY2)
        print(f"   M_W^2/M_Z^2 at w = {big:.0e}: {r:.10f}; cos^2 theta_W = g^2/(g^2+g_Y^2) = {c2:.10f};"
              f" rho - 1 at w = {w:.0f}: {r0 / c2 - 1:.3e} (v^2/w^2 = {(v1 * v1 + v2 * v2) / w ** 2:.3e})")
    print("== Fermi scale ==")
    v = vev_from_GF(inputs.G_F)
    mz = mz_tree(inputs.G_F, inputs.ALPHA_MZ_INV, inputs.S2_MZ)
    s2 = inputs.S2_MZ
    mz2 = math.sqrt(math.pi / inputs.ALPHA_MZ_INV / (math.sqrt(2) * inputs.G_F * s2 * (1 - s2)))
    print(f"v = {v:.6f} GeV; sqrt2 G_F v^2 = {math.sqrt(2) * inputs.G_F * v * v:.15f}")
    print(f"M_Z tree: via g v/(2c) = {mz:.6f} GeV; one-line formula = {mz2:.6f} GeV; measured {inputs.MZ_MEAS} GeV")
