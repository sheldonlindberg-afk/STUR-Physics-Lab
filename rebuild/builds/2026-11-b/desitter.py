"""Stage `desitter` (build 2026-11-b): gravity as a broken SO(4,1) gauge theory.

so(4,1) generators, the Levi-Civita spin connection of a static metric, the SO(4,1) curvature
F = R - e^e/l^2 (+ torsion), the MacDowell-Mansouri action's coefficients, and the de Sitter radius.
Derivations and second routes: DERIVATION_desitter.md (same directory); section numbers are cited below.
Geometry in G = c = 1 (M, l lengths); x = (t, r, theta, phi); eta = diag(-1, 1, 1, 1, 1).
"""
import math
import itertools

import inputs
import toolkit

PROVENANCE = {
    "so41_generator": ("derived", "the postulated formula (J_AB)^C_D = delta^C_A eta_BD - delta^C_B eta_AD,"
                                  " eta = diag(-1,1,1,1,1), filled in as an integer 5x5 matrix; algebra"
                                  " [J_AB, J_CD] = eta_BC J_AD - ... derived and checked (section 1)"),
    "spin_connection": ("derived", "solved de^a + omega^a_b ^ e^b = 0 with omega_ab = -omega_ba for the diagonal"
                                   " tetrad (sqrt f, 1/sqrt f, r, r sin th): omega^0_1 = f'/2 dt, omega^1_2 ="
                                   " -sqrt f dth, omega^1_3 = -sqrt f sin th dph, omega^2_3 = -cos th dph"
                                   " (section 3)"),
    "unbroken_generators": ("derived", "applies each so41_generator(A, B) to V and keeps those giving zero;"
                                       " equivalent to V^A = V^B = 0 (section 2)"),
    "curvature_split_residual": ("derived", "F = dA + [A, A] from 5x5 matrices A = omega^ab J_ab/2 + e^a J_a4/l"
                                            " with a numerical derivative, compared with the analytic"
                                            " R^ab = d omega + omega ^ omega minus e^a ^ e^b/l^2, and the"
                                            " torsion part F^a4 (section 4)"),
    "ds_curvature_max": ("derived", "max |F| of the same matrix construction for f = 1 - r^2/l^2: de Sitter is"
                                    " a flat SO(4,1) connection (section 6)"),
    "action_coefficients": ("derived", "4-form components of eps_abcd R^ab ^ e^c ^ e^d and eps_abcd e^a ^ e^b ^"
                                       " e^c ^ e^d by explicit sums over permutations (toolkit.levi_civita),"
                                       " divided by e R and e (section 7)"),
    "ell_from_lambda": ("derived", "the MacDowell-Mansouri action reduces to -(4N/l^2) e (R - 6/l^2), so"
                                   " Lambda = 3/l^2 and l = sqrt(3/Lambda); cross-checked by R = 4 Lambda ="
                                   " 12/l^2 (sections 7, 8)"),
    "mm_coupling": ("derived", "l^2/lP^2 with l from ell_from_lambda: the only dimensionless parameter of the"
                               " action, N = -l^2/(64 pi lP^2) (sections 7, 9)"),
    "ricci_scalar": ("derived", "E_a^mu E_b^nu R^ab_{mu nu} with R^ab = d omega^ab + omega^a_c ^ omega^cb, the"
                                " same array action_coefficients contracts; closed form 12/l^2 (section 5)"),
}

_ETA5 = (-1, 1, 1, 1, 1)


# ------------------------------------------------------------------------------------------
# 1. the algebra
# ------------------------------------------------------------------------------------------
def so41_generator(A, B):
    """(J_AB)^C_D = delta^C_A eta_BD - delta^C_B eta_AD as a 5x5 list of ints (row C, column D)."""
    if A not in range(5) or B not in range(5):
        raise ValueError("so(4,1) indices run over 0..4")
    J = [[0] * 5 for _ in range(5)]
    J[A][B] += _ETA5[B]
    J[B][A] -= _ETA5[A]
    return J


def unbroken_generators(V):
    """The pairs (A, B), A < B, whose generator J_AB annihilates the 5-vector V (section 2)."""
    V = list(V)
    if len(V) != 5:
        raise ValueError("V must have 5 components")
    tol = 1e-12 * max(abs(v) for v in V)
    out = []
    for A in range(5):
        for B in range(A + 1, 5):
            J = so41_generator(A, B)
            JV = [sum(J[C][D] * V[D] for D in range(5)) for C in range(5)]
            if all(abs(c) <= tol for c in JV):
                out.append((A, B))
    return out


# ------------------------------------------------------------------------------------------
# 2. tetrad and spin connection
# ------------------------------------------------------------------------------------------
def spin_connection(x, f, fp):
    """(E, w) at x = (t, r, th, ph) for -f dt^2 + dr^2/f + r^2 dOmega^2: E[a][mu] the diagonal tetrad,
    w[a][b][mu] = omega^a_{b mu} (a up, b down), with de^a + omega^a_b ^ e^b = 0 (section 3)."""
    r, th = x[1], x[2]
    fv = f(r)
    if not fv > 0:
        raise ValueError("spin_connection needs f(r) > 0 (static region)")
    s = math.sqrt(fv)
    E = [[0.0] * 4 for _ in range(4)]
    E[0][0], E[1][1], E[2][2], E[3][3] = s, 1 / s, r, r * math.sin(th)
    w = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
    boost = fp(r) / 2
    w[0][1][0] = w[1][0][0] = boost                    # omega^0_1 = omega^1_0 = (f'/2) dt
    w[1][2][2], w[2][1][2] = -s, s                     # omega^1_2 = -sqrt(f) dtheta
    w[1][3][3], w[3][1][3] = -s * math.sin(th), s * math.sin(th)
    w[2][3][3], w[3][2][3] = -math.cos(th), math.cos(th)
    return E, w


def _dspin(x, f, fp, fpp):
    """Analytic derivatives dw[mu][a][b][nu] = d_mu omega^a_{b nu} of section 3's table (section 5)."""
    r, th = x[1], x[2]
    s = math.sqrt(f(r))
    ds = fp(r) / (2 * s)                               # d sqrt(f)/dr
    dw = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    dw[1][0][1][0] = dw[1][1][0][0] = fpp(r) / 2
    dw[1][1][2][2], dw[1][2][1][2] = -ds, ds
    dw[1][1][3][3], dw[1][3][1][3] = -ds * math.sin(th), ds * math.sin(th)
    dw[2][1][3][3], dw[2][3][1][3] = -s * math.cos(th), s * math.cos(th)
    dw[2][2][3][3], dw[2][3][2][3] = math.sin(th), -math.sin(th)
    return dw


def _riemann(w, dw):
    """R[a][b][mu][nu] = R^{ab}_{mu nu}, both Lorentz indices up, from omega^a_{b mu} and its derivatives:
    R^a_b = d omega^a_b + omega^a_c ^ omega^c_b, second index raised with eta (section 5)."""
    R = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for mu in range(4):
                for nu in range(4):
                    v = dw[mu][a][b][nu] - dw[nu][a][b][mu] + sum(
                        w[a][c][mu] * w[c][b][nu] - w[a][c][nu] * w[c][b][mu] for c in range(4))
                    R[a][b][mu][nu] = v * _ETA5[b]
    return R


def _sds(M, l):
    """f, f', f'' of Schwarzschild-de Sitter, f = 1 - 2M/r - r^2/l^2."""
    f = lambda r: 1 - 2 * M / r - r * r / l ** 2
    fp = lambda r: 2 * M / r ** 2 - 2 * r / l ** 2
    fpp = lambda r: -4 * M / r ** 3 - 2 / l ** 2
    return f, fp, fpp


def _sds_curvature(M, l, x):
    """(E, R^{ab}_{mu nu}) on Schwarzschild-de Sitter at x: the one curvature used by ricci_scalar,
    action_coefficients and curvature_split_residual."""
    f, fp, fpp = _sds(M, l)
    E, w = spin_connection(x, f, fp)
    return E, _riemann(w, _dspin(x, f, fp, fpp))


# ------------------------------------------------------------------------------------------
# 3. the SO(4,1) connection and its curvature
# ------------------------------------------------------------------------------------------
def _gauge_field(x, f, fp, l):
    """A[mu] = (1/2) omega^{ab}_mu J_ab + (1/l) e^a_mu J_a4 as four 5x5 matrices (section 4)."""
    E, w = spin_connection(x, f, fp)
    A = [[[0.0] * 5 for _ in range(5)] for _ in range(4)]
    for a in range(4):
        for b in range(a + 1, 4):                      # (1/2) sum over all a, b = sum over a < b
            J = so41_generator(a, b)
            for mu in range(4):
                c = w[a][b][mu] * _ETA5[b]             # omega^{ab}_mu
                if c:
                    for i in range(5):
                        for j in range(5):
                            A[mu][i][j] += c * J[i][j]
        J = so41_generator(a, 4)
        for mu in range(4):
            c = E[a][mu] / l
            if c:
                for i in range(5):
                    for j in range(5):
                        A[mu][i][j] += c * J[i][j]
    return A


def _field_strength(x, f, fp, l):
    """F[mu][nu] = d_mu A_nu - d_nu A_mu + [A_mu, A_nu], 5x5 matrices; derivatives by a 5-point central
    stencil (4th order) of _gauge_field (section 4, route F)."""
    A = _gauge_field(x, f, fp, l)
    dA = []
    for mu in range(4):
        h = 1e-3 * (abs(x[1]) if mu == 1 else 1)
        if mu == 1:
            for _ in range(60):                        # keep the stencil inside the static region
                if all(f(x[1] + k * h) > 0 for k in (-2, -1, 1, 2)):
                    break
                h /= 2
        pts = []
        for k in (-2, -1, 1, 2):
            y = list(x)
            y[mu] += k * h
            pts.append(_gauge_field(y, f, fp, l))
        m2, m1, p1, p2 = pts
        dA.append([[[(m2[nu][i][j] - 8 * m1[nu][i][j] + 8 * p1[nu][i][j] - p2[nu][i][j]) / (12 * h)
                     for j in range(5)] for i in range(5)] for nu in range(4)])
    F = [[None] * 4 for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            F[mu][nu] = [[dA[mu][nu][i][j] - dA[nu][mu][i][j]
                          + sum(A[mu][i][k] * A[nu][k][j] - A[nu][i][k] * A[mu][k][j] for k in range(5))
                          for j in range(5)] for i in range(5)]
    return F


def curvature_split_residual(M, l, x):
    """max of |F^{ab} - R^{ab} + e^a ^ e^b/l^2| and |F^{a4}| (coordinate components) on SdS at x (section 4)."""
    f, fp, _ = _sds(M, l)
    F = _field_strength(x, f, fp, l)
    E, R = _sds_curvature(M, l, x)
    worst = 0.0
    for mu in range(4):
        for nu in range(4):
            for a in range(4):
                worst = max(worst, abs(F[mu][nu][a][4]))                       # F^{a4} = T^a/l
                for b in range(4):
                    Fab = F[mu][nu][a][b] * _ETA5[b]                           # F^{ab}
                    ee = (E[a][mu] * E[b][nu] - E[a][nu] * E[b][mu]) / l ** 2
                    worst = max(worst, abs(Fab - R[a][b][mu][nu] + ee))
    return worst


def ds_curvature_max(l, x):
    """max |F^C_{D mu nu}| for de Sitter space f = 1 - r^2/l^2 at x (section 6): zero up to stencil noise."""
    f, fp, _ = _sds(0, l)
    F = _field_strength(x, f, fp, l)
    return max(abs(F[mu][nu][i][j]) for mu in range(4) for nu in range(4) for i in range(5) for j in range(5))


# ------------------------------------------------------------------------------------------
# 4. curvature scalar and the action's coefficients
# ------------------------------------------------------------------------------------------
def _contract(E, R):
    """E_a^mu E_b^nu R^{ab}_{mu nu} for a diagonal tetrad."""
    return sum(R[a][b][a][b] / (E[a][a] * E[b][b]) for a in range(4) for b in range(4))


def ricci_scalar(M, l, x):
    """E_a^mu E_b^nu R^{ab}_{mu nu} on Schwarzschild-de Sitter at x (section 5)."""
    E, R = _sds_curvature(M, l, x)
    return _contract(E, R)


def action_coefficients(M, l, x):
    """(cR, cV): eps_abcd R^{ab} ^ e^c ^ e^d = cR e R d^4x and eps_abcd e^a ^ e^b ^ e^c ^ e^d = cV e d^4x,
    eps_0123 = +1, 4-form component read on dt ^ dr ^ dtheta ^ dphi (section 7)."""
    E, R = _sds_curvature(M, l, x)
    perms = [(p, toolkit.levi_civita(p)) for p in itertools.permutations(range(4))]
    ree = eeee = 0.0
    for (a, b, c, d), s1 in perms:
        for (mu, nu, rho, sig), s2 in perms:
            # R^{ab} = (1/2) R^{ab}_{mu nu} dx^mu ^ dx^nu
            ree += s1 * s2 * R[a][b][mu][nu] / 2 * E[c][rho] * E[d][sig]
            eeee += s1 * s2 * E[a][mu] * E[b][nu] * E[c][rho] * E[d][sig]
    e = E[0][0] * E[1][1] * E[2][2] * E[3][3]           # det of the diagonal tetrad
    return ree / (e * _contract(E, R)), eeee / e


# ------------------------------------------------------------------------------------------
# 5. the de Sitter radius and the coupling
# ------------------------------------------------------------------------------------------
def ell_from_lambda(Lam):
    """de Sitter radius l = sqrt(3/Lambda) in m for Lambda in m^-2 (section 8)."""
    if not Lam > 0:
        raise ValueError("a de Sitter radius needs Lambda > 0")
    return math.sqrt(3 / Lam)


def mm_coupling(Lam, lP):
    """The dimensionless MacDowell-Mansouri coupling l^2/lP^2, l = ell_from_lambda(Lam) (section 9)."""
    return (ell_from_lambda(Lam) / lP) ** 2


# ------------------------------------------------------------------------------------------
# self-check: the second routes of DERIVATION_desitter.md
# ------------------------------------------------------------------------------------------
def _matmul(P, Q):
    return [[sum(P[i][k] * Q[k][j] for k in range(5)) for j in range(5)] for i in range(5)]


if __name__ == "__main__":
    J = so41_generator
    eta = _ETA5

    # section 1: the full commutation relations, by matrix multiplication
    bad = 0
    for A in range(5):
        for B in range(5):
            for C in range(5):
                for D in range(5):
                    PQ, QP = _matmul(J(A, B), J(C, D)), _matmul(J(C, D), J(A, B))
                    JAD, JBD, JAC, JBC = J(A, D), J(B, D), J(A, C), J(B, C)
                    for i in range(5):
                        for j in range(5):
                            rhs = (eta[B] * (B == C) * JAD[i][j] - eta[A] * (A == C) * JBD[i][j]
                                   - eta[B] * (B == D) * JAC[i][j] + eta[A] * (A == D) * JBC[i][j])
                            bad += (PQ[i][j] - QP[i][j]) != rhs
    asym = sum(eta[i] * J(A, B)[i][j] + eta[j] * J(A, B)[j][i] != 0
               for A in range(5) for B in range(5) for i in range(5) for j in range(5))
    print(f"so(4,1): violations of [J_AB,J_CD] = eta_BC J_AD - eta_AC J_BD - eta_BD J_AC + eta_AD J_BC: {bad};"
          f" eta J not antisymmetric: {asym}")

    # section 2: matrix route vs the index criterion V^A = V^B = 0
    for V in ([0, 0, 0, 0, 1], [1, 0, 0, 0, 0], [0, 0, 1, 0, 1], [1, 2, 3, 4, 5], [0, 0, 0, 0, 0]):
        got = unbroken_generators(V)
        rule = [(A, B) for A in range(5) for B in range(A + 1, 5) if V[A] == 0 and V[B] == 0]
        print(f"unbroken for V = {V}: {len(got)} (matrix route) vs {len(rule)} (index rule), equal: {got == rule}")

    M, l, x = 0.3, 7.0, [0.2, 2.3, 1.1, 0.4]
    f, fp, fpp = _sds(M, l)
    E, w = spin_connection(x, f, fp)

    # section 3: torsion by an independent finite difference of the tetrad
    def d_num(fn, mu, h=1e-3):
        vals = []
        for k in (-2, -1, 1, 2):
            y = list(x)
            y[mu] += k * h
            vals.append(fn(y))
        return (vals[0] - 8 * vals[1] + 8 * vals[2] - vals[3]) / (12 * h)

    tors = 0.0
    for a in range(4):
        for mu in range(4):
            for nu in range(4):
                de = (d_num(lambda y: spin_connection(y, f, fp)[0][a][nu], mu)
                      - d_num(lambda y: spin_connection(y, f, fp)[0][a][mu], nu))
                tors = max(tors, abs(de + sum(w[a][b][mu] * E[b][nu] - w[a][b][nu] * E[b][mu] for b in range(4))))
    metr = max(abs(eta[a] * w[a][b][mu] + eta[b] * w[b][a][mu]) for a in range(4) for b in range(4) for mu in range(4))
    print(f"spin connection: max torsion {tors:.2e}, max |omega_ab + omega_ba| {metr:.2e}")

    # section 5: analytic d omega vs finite differences; Ricci scalar vs closed forms
    dw_an = _dspin(x, f, fp, fpp)
    dw_fd = [[[[d_num(lambda y: spin_connection(y, f, fp)[1][a][b][nu], mu) for nu in range(4)]
               for b in range(4)] for a in range(4)] for mu in range(4)]
    ddiff = max(abs(dw_an[mu][a][b][nu] - dw_fd[mu][a][b][nu])
                for mu in range(4) for a in range(4) for b in range(4) for nu in range(4))
    R_fd = _contract(E, _riemann(w, dw_fd))
    r = x[1]
    R_closed = -fpp(r) - 4 * fp(r) / r + 2 * (1 - f(r)) / r ** 2
    print(f"d omega analytic vs finite difference: max diff {ddiff:.2e}")
    print(f"ricci_scalar = {ricci_scalar(M, l, x):.12f};  finite-difference route {R_fd:.12f};"
          f"  -f'' - 4f'/r + 2(1-f)/r^2 = {R_closed:.12f};  12/l^2 = {12 / l ** 2:.12f}")

    # sections 4, 6: F against R - e^e/l^2; F is so(4,1) valued; de Sitter flat only for matching l
    F = _field_strength(x, f, fp, l)
    alg = max(max(abs(F[mu][nu][4][4]) for mu in range(4) for nu in range(4)),
              max(abs(eta[i] * F[mu][nu][i][j] + eta[j] * F[mu][nu][j][i])
                  for mu in range(4) for nu in range(4) for i in range(5) for j in range(5)))
    print(f"curvature_split_residual = {curvature_split_residual(M, l, x):.2e};"
          f"  F outside so(4,1): {alg:.2e}")
    f0, fp0, _ = _sds(0, l)
    mismatch = _field_strength(x, f0, fp0, 2 * l)
    mm = max(abs(mismatch[mu][nu][i][j]) for mu in range(4) for nu in range(4) for i in range(5) for j in range(5))
    print(f"ds_curvature_max = {ds_curvature_max(l, x):.2e} (analytic: 0);"
          f"  with the connection's l doubled: {mm:.3e} (nonzero)")

    # section 7: coefficients vs the index identities
    cR, cV = action_coefficients(M, l, x)
    cR2, cV2 = action_coefficients(0.1, 4.0, [0.0, 1.7, 0.5, 2.0])
    print(f"action_coefficients = ({cR:.12f}, {cV:.12f}), ({cR2:.12f}, {cV2:.12f});  identities: (2, 24)")

    # sections 8, 9: l from the action vs from R = 4 Lambda
    Lam, lP = inputs.LAMBDA_SI, inputs.L_PLANCK
    ell = ell_from_lambda(Lam)
    print(f"ell_from_lambda(LAMBDA_SI) = {ell:.6e} m;  R l^2/4 on SdS = {ricci_scalar(M, l, x) * l ** 2 / 4:.12f}"
          f" (action route: 3)")
    print(f"mm_coupling = {mm_coupling(Lam, lP):.6e};  3/(Lambda lP^2) = {3 / (Lam * lP ** 2):.6e};"
          f"  coupling(L)/coupling(2L) = {mm_coupling(Lam, lP) / mm_coupling(2 * Lam, lP):.12f}")
