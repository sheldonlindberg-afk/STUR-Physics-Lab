"""desitter: gravity as a broken SO(4,1) gauge theory, MacDowell-Mansouri (SPEC.md section 6).

Derivations and second routes: DERIVATION_desitter.md. Epsilon symbols go through
toolkit.levi_civita. rung 6 (blackholes) calls spin_connection and ell_from_lambda.
"""
import math
from fractions import Fraction
from itertools import permutations

import inputs  # noqa: F401  (stage reads no measured inputs; kept for the self-check)
import toolkit

PROVENANCE = {
    "so41_generator": ("derived", "(J_AB)^C_D = delta^C_A eta_BD - delta^C_B eta_AD built entrywise as a 5x5 matrix;"
                                  " [P_a, P_b] = -J_ab checked by matrix commutators"),
    "spin_connection": ("derived", "Cartan de^a = -omega^a_b ^ e^b on the diagonal tetrad: omega^0_1 = f'/2 dt,"
                                   " omega^2_1 = sqrt f dth, omega^3_1 = sqrt f sin th dph, omega^3_2 = cos th dph,"
                                   " the rest by omega_ab = -omega_ba; torsion proved ~0 by finite differences"),
    "unbroken_generators": ("derived", "computes J_AB V for every A < B and keeps those with J_AB V = 0"
                                       " (stabilizer of V; so(3,1) for V = e_4)"),
    "curvature_split_residual": ("derived", "A = omega^a_b block + e/l column/row from so41_generator; F = dA + [A, A]"
                                            " by central differences + matrix commutators; R from omega alone;"
                                            " max |F^ab - R^ab + e^a^e^b/l^2|, |F^a4| (= torsion/l)"),
    "ds_curvature_max": ("derived", "same F with f = 1 - r^2/l^2: R^ab = e^a^e^b/l^2 so F = 0 (flat connection)"),
    "action_coefficients": ("derived", "literal wedge contractions eps_abcd eps~^{mu nu rho sig} R^ab_{mu nu} e^c_rho"
                                       " e^d_sig / 2 and eps eps~ e e e e (toolkit.levi_civita), divided by e R and e;"
                                       " exact values 2 and 24 from the epsilon identities"),
    "ell_from_lambda": ("derived", "eps F^F = Euler - (2 cR/l^2) e (R - cV/(2 cR l^2)) vs e (R - 2 Lambda):"
                                   " Lambda = cV/(4 cR l^2) with exact cR, cV from levi_civita -> l = sqrt(3/Lambda)"),
    "mm_coupling": ("derived", "l^2/lP^2 with l from ell_from_lambda, = cV/(4 cR lP^2 Lambda) = 3/(lP^2 Lambda)"),
}

_N = 5
_ETA = (-1, 1, 1, 1, 1)
_H = 1e-5                     # finite-difference step (coordinate units)


# ------------------------------------------------------------------------------------------ algebra
def so41_generator(A, B):
    """(J_AB)^C_D = delta^C_A eta_BD - delta^C_B eta_AD."""
    return [[(1 if C == A else 0) * (_ETA[B] if B == D else 0) - (1 if C == B else 0) * (_ETA[A] if A == D else 0)
             for D in range(_N)] for C in range(_N)]


def _mm(X, Y):
    n = len(X)
    return [[sum(X[i][k] * Y[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def _comm(X, Y):
    P, Q = _mm(X, Y), _mm(Y, X)
    return [[P[i][j] - Q[i][j] for j in range(len(X))] for i in range(len(X))]


def unbroken_generators(V):
    scale = max(1.0, max(abs(v) for v in V))
    out = []
    for A in range(_N):
        for B in range(A + 1, _N):
            J = so41_generator(A, B)
            JV = [sum(J[C][D] * V[D] for D in range(_N)) for C in range(_N)]
            if max(abs(v) for v in JV) <= 1e-12 * scale:
                out.append((A, B))
    return out


# ------------------------------------------------------------------------------------------ geometry
def spin_connection(x, f, fp):
    """Diagonal tetrad E[a][mu] and Levi-Civita omega^a_{b mu} (w[a][b][mu]) for -f dt^2 + dr^2/f + r^2 dOmega^2."""
    t, r, th, ph = x
    fv, fpv = f(r), fp(r)
    sf = math.sqrt(fv)
    E = [[0.0] * 4 for _ in range(4)]
    E[0][0], E[1][1], E[2][2], E[3][3] = sf, 1 / sf, r, r * math.sin(th)
    w = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
    w[0][1][0] = w[1][0][0] = fpv / 2              # boost: omega^0_1 = omega^1_0 = f'/2 dt
    w[2][1][2], w[1][2][2] = sf, -sf               # omega^2_1 = sqrt f dth
    w[3][1][3], w[1][3][3] = sf * math.sin(th), -sf * math.sin(th)
    w[3][2][3], w[2][3][3] = math.cos(th), -math.cos(th)
    return E, w


def _d(fn, x, mu):
    """Central difference d_mu of fn(x) (a nested list structure of floats)."""
    xp, xm = list(x), list(x)
    xp[mu] += _H
    xm[mu] -= _H
    return _sub(fn(xp), fn(xm), 1 / (2 * _H))


def _sub(a, b, s=1.0):
    if isinstance(a, list):
        return [_sub(u, v, s) for u, v in zip(a, b)]
    return (a - b) * s


def _torsion(x, f, fp):
    """T^a_{mu nu} = d_mu e^a_nu - d_nu e^a_mu + omega^a_{b mu} e^b_nu - omega^a_{b nu} e^b_mu."""
    E, w = spin_connection(x, f, fp)
    dE = [_d(lambda y: spin_connection(y, f, fp)[0], x, mu) for mu in range(4)]   # dE[mu][a][nu]
    return [[[dE[mu][a][nu] - dE[nu][a][mu]
              + sum(w[a][b][mu] * E[b][nu] - w[a][b][nu] * E[b][mu] for b in range(4))
              for nu in range(4)] for mu in range(4)] for a in range(4)]


def _riemann(x, f, fp):
    """R^a_{b mu nu} from omega alone: d omega + omega ^ omega."""
    _, w = spin_connection(x, f, fp)
    dw = [_d(lambda y: spin_connection(y, f, fp)[1], x, mu) for mu in range(4)]   # dw[mu][a][b][nu]
    return [[[[dw[mu][a][b][nu] - dw[nu][a][b][mu]
               + sum(w[a][c][mu] * w[c][b][nu] - w[a][c][nu] * w[c][b][mu] for c in range(4))
               for nu in range(4)] for mu in range(4)] for b in range(4)] for a in range(4)]


def _riemann_up(x, f, fp):
    """R^{ab}_{mu nu} = R^a_{c mu nu} eta^{cb}."""
    R = _riemann(x, f, fp)
    return [[[[R[a][b][mu][nu] * _ETA[b] for nu in range(4)] for mu in range(4)] for b in range(4)] for a in range(4)]


def _inverse_tetrad(E):
    """E_a^mu for the diagonal tetrad (checked: E . Einv = 1)."""
    return [[(1 / E[a][a] if mu == a else 0.0) for mu in range(4)] for a in range(4)]


def _ricci_scalar(Rup, E):
    Ei = _inverse_tetrad(E)
    return sum(Rup[a][b][mu][nu] * Ei[a][mu] * Ei[b][nu]
               for a in range(4) for b in range(4) for mu in range(4) for nu in range(4))


# ------------------------------------------------------------------------------------------ SO(4,1) connection
def _gauge_field(x, f, fp, l):
    """A_mu = 1/2 omega^{ab}_mu J_ab + (1/l) e^a_mu J_a4, as a list of four 5x5 matrices."""
    E, w = spin_connection(x, f, fp)
    J = {(A, B): so41_generator(A, B) for A in range(_N) for B in range(_N)}
    out = []
    for mu in range(4):
        M = [[0.0] * _N for _ in range(_N)]
        for a in range(4):
            for b in range(4):
                wab = w[a][b][mu] * _ETA[b]          # omega^{ab}_mu
                for C in range(_N):
                    for D in range(_N):
                        M[C][D] += 0.5 * wab * J[(a, b)][C][D]
            for C in range(_N):
                for D in range(_N):
                    M[C][D] += E[a][mu] / l * J[(a, 4)][C][D]
        out.append(M)
    return out


def _field_strength(x, f, fp, l):
    """F_{mu nu} = d_mu A_nu - d_nu A_mu + [A_mu, A_nu] (5x5 matrices)."""
    A = _gauge_field(x, f, fp, l)
    dA = [_d(lambda y: _gauge_field(y, f, fp, l), x, mu) for mu in range(4)]     # dA[mu][nu]
    F = [[None] * 4 for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            c = _comm(A[mu], A[nu])
            F[mu][nu] = [[dA[mu][nu][i][j] - dA[nu][mu][i][j] + c[i][j] for j in range(_N)] for i in range(_N)]
    return F


def _so41_components(Fm):
    """Coefficients F^{AB} (A < B) with Fm = sum_{A<B} F^{AB} J_AB, read off the matrix, plus the reconstruction
    residual (zero iff Fm lies in so(4,1))."""
    comp = {}
    for A in range(_N):
        for B in range(A + 1, _N):
            comp[(A, B)] = Fm[A][B] * _ETA[B]          # (J_AB)^A_B = eta_BB; other generators vanish there
    rec = [[0.0] * _N for _ in range(_N)]
    for (A, B), v in comp.items():
        J = so41_generator(A, B)
        for C in range(_N):
            for D in range(_N):
                rec[C][D] += v * J[C][D]
    res = max(abs(rec[i][j] - Fm[i][j]) for i in range(_N) for j in range(_N))
    return comp, res


def _sds(M, l):
    return (lambda r: 1 - 2 * M / r - r * r / (l * l)), (lambda r: 2 * M / (r * r) - 2 * r / (l * l))


def _split(M, l, x):
    f, fp = _sds(M, l)
    E, _ = spin_connection(x, f, fp)
    F = _field_strength(x, f, fp, l)
    Rup = _riemann_up(x, f, fp)
    worst = 0.0
    for mu in range(4):
        for nu in range(4):
            comp, rec = _so41_components(F[mu][nu])
            worst = max(worst, rec)
            for a in range(4):
                for b in range(a + 1, 4):
                    ee = (E[a][mu] * E[b][nu] - E[a][nu] * E[b][mu]) / (l * l)
                    worst = max(worst, abs(comp[(a, b)] - Rup[a][b][mu][nu] + ee))
                worst = max(worst, abs(comp[(a, 4)]))
    return worst


def curvature_split_residual(M, l, x):
    return _split(M, l, x)


def ds_curvature_max(l, x):
    f, fp = _sds(0.0, l)
    F = _field_strength(x, f, fp, l)
    return max(abs(F[mu][nu][i][j]) for mu in range(4) for nu in range(4) for i in range(_N) for j in range(_N))


# ------------------------------------------------------------------------------------------ action
def _eps4(p):
    return toolkit.levi_civita(list(p))


def action_coefficients(M, l, x):
    """(cR, cV): [eps_abcd R^ab^e^c^e^d]_{0123} = cR e R and [eps_abcd e^a^e^b^e^c^e^d]_{0123} = cV e."""
    f, fp = _sds(M, l)
    E, _ = spin_connection(x, f, fp)
    Rup = _riemann_up(x, f, fp)
    perms = list(permutations(range(4)))
    det = sum(_eps4(p) * E[0][p[0]] * E[1][p[1]] * E[2][p[2]] * E[3][p[3]] for p in perms)
    vol, rterm = 0.0, 0.0
    for lor in perms:                                  # (a, b, c, d) with eps_abcd != 0
        s = _eps4(lor)
        a, b, c, d = lor
        for co in perms:                               # (mu, nu, rho, sig)
            sc = _eps4(co)
            mu, nu, rho, sig = co
            vol += s * sc * E[a][mu] * E[b][nu] * E[c][rho] * E[d][sig]
            rterm += 0.5 * s * sc * Rup[a][b][mu][nu] * E[c][rho] * E[d][sig]
    R = _ricci_scalar(Rup, E)
    return rterm / (det * R), vol / det


def _exact_coefficients():
    """cR, cV as exact Fractions from the epsilon contractions alone (DERIVATION section 6)."""
    perms = list(permutations(range(4)))
    cV = Fraction(sum(_eps4(p) * _eps4(p) for p in perms))
    k = lambda e, f_, a, b: sum(_eps4((e, f_, c, d)) * _eps4((a, b, c, d)) for c in range(4) for d in range(4))
    cR = Fraction(k(0, 1, 0, 1) - k(1, 0, 0, 1), 2)
    return cR, cV


def ell_from_lambda(Lam):
    cR, cV = _exact_coefficients()
    lam_l2 = cV / (4 * cR)                           # Lambda l^2, from the ratio of the MM action's terms
    return math.sqrt(float(lam_l2) / Lam)


def mm_coupling(Lam, lP):
    return ell_from_lambda(Lam) ** 2 / lP ** 2


# ------------------------------------------------------------------------------------------ self-check
if __name__ == "__main__":
    x = [0.2, 2.3, 1.1, 0.4]
    # algebra: general commutator vs the matrices
    worst = 0.0
    for A in range(_N):
        for B in range(_N):
            for C in range(_N):
                for D in range(_N):
                    lhs = _comm(so41_generator(A, B), so41_generator(C, D))
                    rhs = [[(_ETA[B] if B == C else 0) * so41_generator(A, D)[i][j]
                            - (_ETA[A] if A == C else 0) * so41_generator(B, D)[i][j]
                            - (_ETA[B] if B == D else 0) * so41_generator(A, C)[i][j]
                            + (_ETA[A] if A == D else 0) * so41_generator(B, C)[i][j]
                            for j in range(_N)] for i in range(_N)]
                    worst = max(worst, max(abs(lhs[i][j] - rhs[i][j]) for i in range(_N) for j in range(_N)))
    print("so(4,1) commutator formula residual:", worst)
    print("unbroken by (0,0,0,0,1):", unbroken_generators([0, 0, 0, 0, 1]))
    print("unbroken by (1,0,0,0,0) (timelike):", unbroken_generators([1, 0, 0, 0, 0]))

    M, l = 0.3, 7.0
    f, fp = _sds(M, l)
    T = _torsion(x, f, fp)
    print("SdS torsion max:", max(abs(v) for a in T for row in a for v in row))
    for name, (MM, ll) in (("de Sitter", (0.0, l)), ("SdS", (M, l))):
        ff, ffp = _sds(MM, ll)
        E, _ = spin_connection(x, ff, ffp)
        Rup = _riemann_up(x, ff, ffp)
        print(f"{name}: Ricci scalar from R^ab = {_ricci_scalar(Rup, E):.10f}, 12/l^2 = {12 / ll ** 2:.10f};"
              f" R^01_01 = {Rup[0][1][0][1] / (E[0][0] * E[1][1]):.10f}, -f''/2 = 2M/r^3 + 1/l^2 = {2 * MM / x[1] ** 3 + 1 / ll**2:.10f}")
    print("split residual SdS:", curvature_split_residual(M, l, x))
    print("de Sitter max |F|:", ds_curvature_max(l, x))

    def ricci_of_F(fr, fpr, ll):
        E, _ = spin_connection(x, fr, fpr)
        Ei = _inverse_tetrad(E)
        F = _field_strength(x, fr, fpr, ll)
        out = 0.0
        for a in range(4):
            for c in range(4):
                s = 0.0
                for b in range(4):
                    for mu in range(4):
                        for nu in range(4):
                            Fab = F[mu][nu][a][b] * _ETA[b]          # F^{ab}_{mu nu}
                            s += Fab * Ei[c][mu] * Ei[b][nu]
                out = max(out, abs(s))
        return out
    print("max |Ric(F)| SdS:", ricci_of_F(f, fp, l))
    fs = lambda r: 1 - 2 * M / r
    fsp = lambda r: 2 * M / r ** 2
    print("max |Ric(F)| Schwarzschild (expect 3/l^2 =", 3 / l ** 2, "):", ricci_of_F(fs, fsp, l))

    print("action coefficients numerical (0.3, 7):", action_coefficients(M, l, x))
    print("action coefficients numerical (0.1, 4):", action_coefficients(0.1, 4.0, [0.0, 1.7, 0.5, 2.0]))
    print("action coefficients exact:", _exact_coefficients())
    cR, cV = action_coefficients(0.2, 5.0, [0.0, 1.9, 0.8, 0.3])
    print("Lambda l^2 from numerical ratio cV/(4 cR):", cV / (4 * cR), " exact:", _exact_coefficients()[1] / (4 * _exact_coefficients()[0]))
    fd, fdp = _sds(0.0, l)
    Ed, _ = spin_connection(x, fd, fdp)
    print("Lambda l^2 from de Sitter R = 4 Lambda:", _ricci_scalar(_riemann_up(x, fd, fdp), Ed) * l ** 2 / 4)
    print("ell_from_lambda(LAMBDA_SI) [m]:", ell_from_lambda(inputs.LAMBDA_SI))
    print("mm_coupling(LAMBDA_SI, L_PLANCK):", mm_coupling(inputs.LAMBDA_SI, inputs.L_PLANCK))
