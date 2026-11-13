"""chiral: the strong force (SPEC.md section 3).

Derivations and second routes: DERIVATION_chiral.md. Numerics via toolkit only.
"""
import math

import inputs
import toolkit

PROVENANCE = {
    "goldstone_count": ("derived", "true vacuum by toolkit.bisect on dV/drho = lam rho(rho^2 - v^2) along a ray;"
                                   " Richardson-extrapolated toolkit.hessian of V (exact for a quartic), toolkit."
                                   "eigvalsh; zero modes |e| <= 1e-9 max|e| (closed form: 2 lam v^2 once, 0 x3 ="
                                   " dim O(4)/O(3)); minimum checked"),
    "sigma_model_vacuum": ("derived", "sigma0 from toolkit.bisect on lam s(s^2 - v^2) - H on [v, v + (H/lam)^(1/3)];"
                                      " m_pi^2 = mean of the 3 lowest eigenvalues of the Richardson Hessian at"
                                      " (sigma0, 0, 0, 0); equals H/sigma0 by the vacuum condition"),
    "gmor_mpi": ("derived", "sigma model m_pi^2 = H/<sigma> with <sigma> = f_pi, H f_pi = (m_u + m_d) cond13^3:"
                            " m_pi = sqrt(mq_sum cond13^3)/fpi"),
    "chpt_mpi": ("quoted", "Gasser & Leutwyler, Ann. Phys. 158 (1984) 142, FLAG conventions: M_pi^2 = M^2[1 -"
                           " M^2 lbar3/(32 pi^2 F^2)], M^2 = 2 mhat Sigma/F^2, F = fpi/(F_pi/F), Sigma = cond13^3"),
    "yukawa": ("derived", "inverse Fourier transform of 1/(q^2 + m^2) by residues: e^{-mr}/(4 pi r);"
                          " (lap - m^2)V = 0 for r > 0 and flux -4 pi r^2 V' -> 1 gives -delta^3"),
    "tensor_identity_residual": ("derived", "explicit 4x4 Kronecker products s1 = sigma x 1, s2 = 1 x sigma of the"
                                            " Pauli matrices; max |(s1.q)(s2.q) - (q^2/3)(s1.s2 + S12)|"),
    "goldberger_treiman": ("derived", "PCAC: q^mu <N|A_mu|N> = [2 M_N G_A + q^2 G_P] ubar g5 u; chiral-limit pion"
                                      " pole in G_P with residue -2 f_pi g_piNN gives g_piNN = g_A M_N / f_pi"
                                      " (sigma model with nucleons: g_A = 1, g = M_N/f_pi)"),
}


# ------------------------------------------------------------------------------------------
# the linear sigma model (SPEC 3)
# ------------------------------------------------------------------------------------------
def _potential(lam, v, H):
    def V(phi):
        p2 = math.fsum(x * x for x in phi)
        return lam / 4 * (p2 - v * v) ** 2 - H * phi[0]
    return V


def _richardson_hessian(f, x, h):
    """[4 D(h/2) - D(h)]/3 from toolkit.hessian: exact (up to rounding) for a quartic f."""
    A = toolkit.hessian(f, x, h)
    B = toolkit.hessian(f, x, h / 2)
    n = len(x)
    return [[(4 * B[i][j] - A[i][j]) / 3 for j in range(n)] for i in range(n)]


def _step(scale):
    return scale / 2 ** 6


def _ray_vacuum(lam, v, n):
    """rho0 > 0 minimizing V(rho n) at H = 0: root of dV/drho = lam rho (rho^2 - v^2)."""
    dV = lambda rho: lam * rho * (rho * rho - v * v)
    rho0 = toolkit.bisect(dV, v / 2, 2 * v)
    norm = math.sqrt(math.fsum(c * c for c in n))
    return [rho0 * c / norm for c in n]


def _spectrum(lam, v, H, phi):
    scale = max(math.sqrt(math.fsum(c * c for c in phi)), abs(v))
    M = _richardson_hessian(_potential(lam, v, H), phi, _step(scale))
    return toolkit.eigvalsh(M)


def _zero_modes(ev, tol=1e-9):
    big = max(abs(e) for e in ev)
    return sum(1 for e in ev if abs(e) <= tol * big)


def goldstone_count(lam, v):
    """Zero modes of the O(4) sigma model's Hessian at its true vacuum, H = 0."""
    if lam <= 0 or v == 0:
        raise ValueError("need lam > 0 and v != 0 for spontaneous breaking")
    phi0 = _ray_vacuum(lam, abs(v), [1.0, 0.0, 0.0, 0.0])
    ev = _spectrum(lam, v, 0.0, phi0)
    big = max(abs(e) for e in ev)
    if ev[0] < -1e-9 * big:
        raise ArithmeticError(f"not a minimum: eigenvalues {ev}")
    return _zero_modes(ev)


def sigma_model_vacuum(lam, v, H):
    """(sigma0, m_pi^2): true vacuum with explicit breaking -H sigma, pion mass^2 from the Hessian."""
    if lam <= 0:
        raise ValueError("need lam > 0")
    s, Ha = (1.0 if H >= 0 else -1.0), abs(H)
    va = abs(v)
    g = lambda x: lam * x * (x * x - va * va) - Ha
    if Ha == 0:
        sigma0 = va
    else:
        sigma0 = toolkit.bisect(g, va, va + (Ha / lam) ** (1 / 3))
    sigma0 *= s
    ev = _spectrum(lam, v, H, [sigma0, 0.0, 0.0, 0.0])
    big = max(abs(e) for e in ev)
    if ev[0] < -1e-9 * big:
        raise ArithmeticError(f"not a minimum: eigenvalues {ev}")
    mpi2 = math.fsum(ev[:3]) / 3          # the three pions lie below m_sigma^2 (DERIVATION eq. 2)
    return sigma0, mpi2


# ------------------------------------------------------------------------------------------
# GMOR and O(p^4) ChPT
# ------------------------------------------------------------------------------------------
def gmor_mpi(mq_sum, cond13, fpi):
    """Leading-order pion mass (GeV): m_pi^2 = H/f_pi, H = (m_u + m_d) cond13^3 / f_pi."""
    H = mq_sum * cond13 ** 3 / fpi
    return math.sqrt(H / fpi)


def chpt_mpi(m_ud, cond13, fpi_over_F, lbar3, fpi):
    """O(p^4) ChPT pion mass (GeV), quoted formula (Gasser-Leutwyler, FLAG conventions)."""
    F = fpi / fpi_over_F
    M2 = 2 * m_ud * cond13 ** 3 / F ** 2
    x = M2 * lbar3 / (32 * math.pi ** 2 * F ** 2)
    if x >= 1:
        raise ValueError("O(p^4) correction >= 1: outside the chiral expansion")
    return math.sqrt(M2 * (1 - x))


# ------------------------------------------------------------------------------------------
# Yukawa potential
# ------------------------------------------------------------------------------------------
def yukawa(r, m):
    """e^{-m r}/(4 pi r): Fourier transform of 1/(q^2 + m^2); (lap - m^2)V = -delta^3."""
    return math.exp(-m * r) / (4 * math.pi * r)


# ------------------------------------------------------------------------------------------
# spin algebra with explicit Pauli matrices
# ------------------------------------------------------------------------------------------
def _pauli():
    return [[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]]


def _kron(a, b):
    na, nb = len(a), len(b)
    return [[a[i // nb][j // nb] * b[i % nb][j % nb] for j in range(na * nb)] for i in range(na * nb)]


def _mm(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def _lin(coefs, mats):
    n = len(mats[0])
    return [[sum(c * M[i][j] for c, M in zip(coefs, mats)) for j in range(n)] for i in range(n)]


def _spin_ops():
    one = [[1, 0], [0, 1]]
    P = _pauli()
    return [_kron(p, one) for p in P], [_kron(one, p) for p in P]


def _s12(qhat, s1, s2):
    a = _lin(qhat, s1)
    b = _lin(qhat, s2)
    s1s2 = _lin([1, 1, 1], [_mm(s1[i], s2[i]) for i in range(3)])
    return _lin([3, -1], [_mm(a, b), s1s2]), s1s2


def tensor_identity_residual(q):
    """max |(s1.q)(s2.q) - (q^2/3)(s1.s2 + S12)| over the 4x4 spin matrix."""
    q = [float(c) for c in q]
    s1, s2 = _spin_ops()
    A = _mm(_lin(q, s1), _lin(q, s2))
    q2 = math.fsum(c * c for c in q)
    if q2 == 0:
        return max(abs(x) for row in A for x in row)          # B = 0 (prefactor q^2 = 0)
    qn = math.sqrt(q2)
    S12, s1s2 = _s12([c / qn for c in q], s1, s2)
    B = _lin([q2 / 3, q2 / 3], [s1s2, S12])
    return max(abs(A[i][j] - B[i][j]) for i in range(4) for j in range(4))


# ------------------------------------------------------------------------------------------
# Goldberger-Treiman
# ------------------------------------------------------------------------------------------
def goldberger_treiman(gA, MN, fpi):
    """g_piNN = g_A M_N / f_pi (PCAC, pion-pole dominance in the chiral limit)."""
    return gA * MN / fpi


# ------------------------------------------------------------------------------------------
# self-check: second routes (DERIVATION_chiral.md)
# ------------------------------------------------------------------------------------------
def _hermitian_eigs(M):
    n = len(M)
    R = [[0.0] * (2 * n) for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            z = complex(M[i][j])
            R[i][j] = R[i + n][j + n] = z.real
            R[i][j + n] = -z.imag
            R[i + n][j] = z.imag
    return toolkit.eigvalsh(R)[::2]          # each eigenvalue appears twice


if __name__ == "__main__":
    print("== 1. Goldstone count ==")
    for lam, v in ((2.0, 1.0), (0.7, 3.0)):
        phi = _ray_vacuum(lam, v, [0.3, -0.5, 0.7, 0.2])
        ev = _spectrum(lam, v, 0.0, phi)
        ev0 = _spectrum(lam, v, 0.0, [0.0, 0.0, 0.0, 0.0])
        print(f" lam={lam} v={v}: count {goldstone_count(lam, v)}; generic direction eigs {ev}"
              f" (closed form 0 x3, {2 * lam * v * v}); zero modes there {_zero_modes(ev)};"
              f" false vacuum eigs {ev0} (expect -lam v^2 = {-lam * v * v})")

    print("== 2. sigma-model vacuum ==")
    for lam, v, H in ((2.0, 1.0, 0.05), (1.0, 2.0, 0.01), (1.7, 0.9, 0.03), (1.0, 1.0, -0.2)):
        s0, m2 = sigma_model_vacuum(lam, v, H)
        ev = _spectrum(lam, v, H, [s0, 0.0, 0.0, 0.0])
        print(f" lam={lam} v={v} H={H}: sigma0 {s0!r}, m_pi^2 {m2!r}, H/sigma0 {H / s0!r},"
              f" rel diff {abs(m2 - H / s0) / abs(H / s0):.1e}, pion spread {ev[2] - ev[0]:.1e},"
              f" m_sigma^2 {ev[3]!r} vs 2 lam s0^2 + H/s0 {2 * lam * s0 * s0 + H / s0!r}")

    print("== 3. GMOR ==")
    mq, c, f = inputs.MU_PLUS_MD, inputs.COND_13, inputs.F_PI
    m_lo = gmor_mpi(mq, c, f)
    H = mq * c ** 3 / f
    for lam in (10.0, 100.0, 1000.0):     # need lam > m_pi^2/f_pi^2 for v^2 > 0
        v = math.sqrt(f * f - H / (lam * f))
        s0, m2 = sigma_model_vacuum(lam, v, H)
        print(f" sigma-model route lam={lam}: <sigma> {s0:.12f} (f_pi {f:.12f}), m_pi {math.sqrt(m2):.12f}"
              f" vs gmor_mpi {m_lo:.12f}")
    d_lo = 0.5 * math.hypot(inputs.MU_PLUS_MD_ERR / mq, 3 * inputs.COND_13_ERR / c) * m_lo
    print(f" GMOR m_pi = {m_lo * 1e3:.2f} +- {d_lo * 1e3:.2f} MeV   (M_PI0 = {inputs.M_PI0 * 1e3:.4f} MeV)")

    print("== 4. O(p^4) ChPT ==")
    args = [inputs.M_UD_FLAG, inputs.COND_13, inputs.FPI_OVER_F, inputs.LBAR3, inputs.F_PI]
    errs = [inputs.M_UD_FLAG_ERR, inputs.COND_13_ERR, inputs.FPI_OVER_F_ERR, inputs.LBAR3_ERR, 0.0]
    m4 = chpt_mpi(*args)
    F = inputs.F_PI / inputs.FPI_OVER_F
    M2 = 2 * inputs.M_UD_FLAG * inputs.COND_13 ** 3 / F ** 2
    x = M2 * inputs.LBAR3 / (32 * math.pi ** 2 * F ** 2)
    k = x / (1 - x)
    rel = [(1 - k), 3 * (1 - k), 2 - 4 * k, -k]
    dL = math.sqrt(math.fsum((rel[i] * errs[i] / args[i]) ** 2 for i in range(4)))
    d4 = 0.5 * dL * m4
    fd = []
    for i in range(4):
        hi, lo = list(args), list(args)
        hi[i] += errs[i] * 1e-3
        lo[i] -= errs[i] * 1e-3
        fd.append((chpt_mpi(*hi) - chpt_mpi(*lo)) / 2e-3)
    d4_fd = math.sqrt(math.fsum(d * d for d in fd))
    print(f" LO (lbar3 = 0): {chpt_mpi(*args[:3], 0.0, args[4]) * 1e3:.3f} MeV, x = {x:.4f}")
    print(f" per-input contributions (MeV): " + ", ".join(f"{d * 1e3:.2f}" for d in fd))
    print(f" O(p^4) m_pi = {m4 * 1e3:.2f} +- {d4 * 1e3:.2f} MeV (finite-difference propagation"
          f" {d4_fd * 1e3:.2f})   (M_PI0 = {inputs.M_PI0 * 1e3:.4f} MeV, pull"
          f" {(m4 - inputs.M_PI0) / d4:+.2f} sigma)")

    print("== 5. Yukawa ==")
    for m in (0.7, 2.0):
        for qq in (0.5, 2.0):
            L, n = 40 / m, 2 * 10 ** 5 + 1
            dx = L / (n - 1)
            ys = [4 * math.pi * (i * dx) * (yukawa(i * dx, m) if i else 1 / (4 * math.pi)) * math.sin(qq * i * dx)
                  for i in range(n)]
            ft = toolkit.trapezoid(ys, dx) / qq
            print(f" m={m} q={qq}: numeric FT {ft:.10f} vs 1/(q^2+m^2) {1 / (qq * qq + m * m):.10f}")
        for r in (1e-3, 1e-5):
            hh = r * 1e-3
            flux = -4 * math.pi * r * r * (yukawa(r + hh, m) - yukawa(r - hh, m)) / (2 * hh)
            print(f"  flux at r={r}: {flux:.8f} (closed form {math.exp(-m * r) * (1 + m * r):.8f})")

    print("== 6. tensor identity ==")
    s1, s2 = _spin_ops()
    for q in ([0.3, -1.1, 0.7], [0.0, 0.0, 1.0], [1.0, 1.0, 0.0], [0.0, 0.0, 0.0]):
        print(f" q={q}: residual {tensor_identity_residual(q):.1e}")
        qn = math.sqrt(sum(c * c for c in q))
        if qn == 0:
            continue
        S12, s1s2 = _s12([c / qn for c in q], s1, s2)
        S2 = _mm(S12, S12)
        rhs = _lin([6, 2, -2], [[[1 if i == j else 0 for j in range(4)] for i in range(4)], s1s2, S12])
        print(f"   S12 spectrum {[round(e, 12) for e in _hermitian_eigs(S12)]} (expect -4, 0, 2, 2);"
              f" s1.s2 spectrum {[round(e, 12) for e in _hermitian_eigs(s1s2)]};"
              f" trace {sum(S12[i][i] for i in range(4))};"
              f" |S12^2 - (6 + 2 s1.s2 - 2 S12)| {max(abs(S2[i][j] - rhs[i][j]) for i in range(4) for j in range(4)):.1e}")

    print("== 7. Goldberger-Treiman ==")
    g = goldberger_treiman(inputs.G_A, inputs.M_N, inputs.F_PI)
    print(f" g_piNN = {g:.4f} vs empirical {inputs.G_PINN_EMP} +- {inputs.G_PINN_ERR};"
          f" GT discrepancy {1 - g / inputs.G_PINN_EMP:+.4f}")
    print(f" sigma model with nucleons (g_A = 1): g = M_N/f_pi = {inputs.M_N / inputs.F_PI:.6f},"
          f" GT at g_A = 1: {goldberger_treiman(1, inputs.M_N, inputs.F_PI):.6f}")
