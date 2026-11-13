"""Stage `chiral` (build 2026-11-b): the strong force at low energy.

Linear sigma model, GMOR, one-pion exchange. Everything is derived from SPEC.md section 3 except `chpt_mpi`,
which is quoted (allowed). Derivations and second routes: DERIVATION_chiral.md (same directory); section
numbers are cited below.
"""
import math

import inputs
import toolkit

PROVENANCE = {
    "goldstone_count": ("derived", "zero eigenvalues (toolkit.eigvalsh) of the numerical Hessian (toolkit.hessian) of"
                                   " V = (lam/4)(phi.phi - v^2)^2 at the vacuum (v, 0, 0, 0); analytically"
                                   " diag(2 lam v^2, 0, 0, 0), and dim O(4) - dim O(3) = 3 (DERIVATION section 1)"),
    "sigma_model_vacuum": ("derived", "global minimum of V - H sigma: pi = 0 and the root sigma0 > v of"
                                      " lam sigma (sigma^2 - v^2) = H (toolkit.bisect on a derived bracket);"
                                      " m_pi^2 = lam (sigma0^2 - v^2) = H/sigma0 from the Hessian (section 2)"),
    "gmor_mpi": ("derived", "m_pi^2 = H/sigma0 of the sigma model with f_pi = sigma0 and H f_pi = (m_u + m_d)"
                            " |<qbar q>|: m_pi = sqrt(mq_sum cond13^3)/f_pi (section 3)"),
    "chpt_mpi": ("quoted", "O(p^4) SU(2) chiral perturbation theory, Gasser and Leutwyler, Annals Phys. 158 (1984)"
                           " 142, FLAG conventions: M_pi^2 = M^2 [1 - M^2 lbar3/(32 pi^2 F^2)], M^2 = 2 m_ud"
                           " cond13^3/F^2, F = f_pi/(F_pi/F); not derived here (section 4)"),
    "yukawa": ("derived", "Fourier transform of 1/(q^2 + m^2) by the residue at q = i m: e^(-m r)/(4 pi r), the"
                          " solution of (lap - m^2) V = -delta^3 with unit flux (section 5)"),
    "tensor_identity_residual": ("derived", "explicit 4x4 Kronecker products of Pauli matrices; both sides built"
                                            " independently, S12 from its definition with qhat = q/|q| (section 6)"),
    "goldberger_treiman": ("derived", "PCAC: conservation of the nucleon axial current in the chiral limit forces a"
                                      " pion pole whose residue gives f_pi g_piNN = g_A M_N (section 7)"),
}

ZERO_MODE_TOL = 1e-6      # relative to the largest |eigenvalue|; truncation error is ~2.5e-9 (section 1)
HESSIAN_REL_STEP = 1e-4   # Hessian step in units of the field scale v (SPEC section 1: the caller scales h)


# ------------------------------------------------------------------------------------------
# 1, 2. linear sigma model
# ------------------------------------------------------------------------------------------
def _potential(lam, v, H):
    """V(phi) = (lam/4)(phi.phi - v^2)^2 - H sigma, phi = (sigma, pi1, pi2, pi3)."""
    def V(phi):
        p2 = sum(x * x for x in phi)
        return lam / 4 * (p2 - v * v) ** 2 - H * phi[0]
    return V


def _mass_matrix_eigenvalues(lam, v, H, sigma0):
    """Eigenvalues of the Hessian of V at (sigma0, 0, 0, 0), numerically, through the toolkit."""
    scale = max(abs(sigma0), abs(v))
    hess = toolkit.hessian(_potential(lam, v, H), [sigma0, 0.0, 0.0, 0.0], h=HESSIAN_REL_STEP * scale)
    return toolkit.eigvalsh(hess)


def goldstone_count(lam, v):
    """Number of zero modes of the O(4) model at its vacuum (v, 0, 0, 0), H = 0."""
    ev = _mass_matrix_eigenvalues(lam, v, 0.0, v)
    top = max(abs(e) for e in ev)
    return sum(1 for e in ev if abs(e) < ZERO_MODE_TOL * top)


def sigma_model_vacuum(lam, v, H):
    """(sigma0, m_pi^2): the global minimum of V and the pion mass^2 there. Needs lam > 0, v >= 0."""
    if H == 0:
        return float(v), 0.0
    if H < 0:                                   # sigma -> -sigma maps H -> -H
        s0, mpi2 = sigma_model_vacuum(lam, v, -H)
        return -s0, mpi2
    g = lambda s: lam * s * (s * s - v * v) - H
    # g(v) = -H < 0 and g(v + d) >= lam d^3 - H = 0 at d = (H/lam)^(1/3); g is increasing on s > v
    d = (H / lam) ** (1 / 3)
    sigma0 = toolkit.bisect(g, v, v + 2 * d)    # factor 2: keeps the sign change strict against rounding
    return sigma0, H / sigma0                   # = lam (sigma0^2 - v^2) by stationarity, without cancellation


# ------------------------------------------------------------------------------------------
# 3, 4. pion mass
# ------------------------------------------------------------------------------------------
def gmor_mpi(mq_sum, cond13, fpi):
    """Leading-order pion mass (GeV): m_pi^2 f_pi^2 = (m_u + m_d) |<qbar q>|, |<qbar q>| = cond13^3."""
    return math.sqrt(mq_sum * cond13 ** 3) / fpi


def chpt_mpi(m_ud, cond13, fpi_over_F, lbar3, fpi):
    """O(p^4) ChPT pion mass (GeV), quoted: M_pi^2 = M^2 [1 - M^2 lbar3/(32 pi^2 F^2)]."""
    F = fpi / fpi_over_F
    M2 = 2 * m_ud * cond13 ** 3 / (F * F)
    mpi2 = M2 * (1 - M2 * lbar3 / (32 * math.pi ** 2 * F * F))
    if mpi2 < 0:
        raise ValueError("chpt_mpi: the O(p^4) correction exceeds the leading order")
    return math.sqrt(mpi2)


# ------------------------------------------------------------------------------------------
# 5. exchange potential
# ------------------------------------------------------------------------------------------
def yukawa(r, m):
    """V(r) = e^(-m r)/(4 pi r): the Fourier transform of 1/(q^2 + m^2); (lap - m^2) V = -delta^3."""
    return math.exp(-m * r) / (4 * math.pi * r)


# ------------------------------------------------------------------------------------------
# 6. spin structure of one-pion exchange
# ------------------------------------------------------------------------------------------
def _pauli():
    return ([[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]])


def _kron(A, B):
    """Kronecker product of two 2x2 matrices: (A on spin 1) x (B on spin 2), as a 4x4 list."""
    return [[A[i][k] * B[j][l] for k in range(2) for l in range(2)] for i in range(2) for j in range(2)]


def _sigma_dot(a):
    s = _pauli()
    return [[sum(a[i] * s[i][r][c] for i in range(3)) for c in range(2)] for r in range(2)]


def _lin(ca, A, cb, B):
    return [[ca * A[i][j] + cb * B[i][j] for j in range(4)] for i in range(4)]


def _s1_dot_s2():
    s = _pauli()
    out = [[0] * 4 for _ in range(4)]
    for i in range(3):
        out = _lin(1, out, 1, _kron(s[i], s[i]))
    return out


def _s12(qhat):
    """S12 = 3 (s1.qhat)(s2.qhat) - s1.s2 for a unit vector qhat."""
    sq = _sigma_dot(qhat)
    return _lin(3, _kron(sq, sq), -1, _s1_dot_s2())


def tensor_identity_residual(q):
    """max |(s1.q)(s2.q) - (q^2/3)(s1.s2 + S12)| over the 4x4 two-spin matrix."""
    q2 = sum(x * x for x in q)
    if q2 == 0:
        return 0.0                              # both sides vanish; qhat is undefined
    sq = _sigma_dot(q)
    lhs = _kron(sq, sq)
    norm = math.sqrt(q2)
    rhs = _lin(q2 / 3, _s1_dot_s2(), q2 / 3, _s12([x / norm for x in q]))
    return max(abs(lhs[i][j] - rhs[i][j]) for i in range(4) for j in range(4))


# ------------------------------------------------------------------------------------------
# 7. Goldberger-Treiman
# ------------------------------------------------------------------------------------------
def goldberger_treiman(gA, MN, fpi):
    """g_piNN = g_A M_N / f_pi (f_pi in the ~92 MeV normalization)."""
    return gA * MN / fpi


# ------------------------------------------------------------------------------------------
# self-check: second routes (DERIVATION_chiral.md)
# ------------------------------------------------------------------------------------------
def _cubic_closed_form(lam, v, H):
    """Largest root of sigma^3 - v^2 sigma - H/lam = 0 by the trigonometric/hyperbolic formula."""
    c = 3 * math.sqrt(3) * H / (2 * lam * v ** 3)
    amp = 2 * v / math.sqrt(3)
    return amp * (math.cos(math.acos(c) / 3) if c <= 1 else math.cosh(math.acosh(c) / 3))


def _unbroken_generator_count(phi0):
    """Number of so(4) generators (J_ij phi)_k = delta_ki phi_j - delta_kj phi_i that annihilate phi0."""
    n = len(phi0)
    return sum(1 for i in range(n) for j in range(i + 1, n) if phi0[i] == 0 and phi0[j] == 0), n * (n - 1) // 2


def _yukawa_proper_time(r, m, n=6001, tmin=-40.0, tmax=60.0):
    """V(r) = int_0^oo ds (4 pi s)^(-3/2) exp(-r^2/(4s) - m^2 s), trapezoid rule in t = ln s."""
    dt = (tmax - tmin) / (n - 1)
    ys = []
    for k in range(n):
        s = math.exp(tmin + k * dt)
        ys.append(s * (4 * math.pi * s) ** -1.5 * math.exp(-r * r / (4 * s) - m * m * s))
    return toolkit.trapezoid(ys, dt)


if __name__ == "__main__":
    print("== 1. Goldstone count ==")
    for lam, v in ((2.0, 1.0), (0.7, 3.0)):
        ev = _mass_matrix_eigenvalues(lam, v, 0.0, v)
        unbroken, total = _unbroken_generator_count([v, 0, 0, 0])
        print(f" lam={lam} v={v}: Hessian zero modes {goldstone_count(lam, v)}; dim O(4) - dim O(3) ="
              f" {total} - {unbroken} = {total - unbroken}")
        print(f"   numerical eigenvalues {['%.3e' % e for e in ev]}; analytic (0, 0, 0, {2 * lam * v * v})")

    print("== 2. sigma-model vacuum ==")
    for lam, v, H in ((2.0, 1.0, 0.05), (1.0, 2.0, 0.01), (1.7, 0.9, 0.03), (1.0, 0.5, 3.0)):
        s0, mpi2 = sigma_model_vacuum(lam, v, H)
        ev = _mass_matrix_eigenvalues(lam, v, H, s0)
        print(f" lam={lam} v={v} H={H}: sigma0 bisect {s0!r}, closed form {_cubic_closed_form(lam, v, H)!r}")
        print(f"   m_pi^2 = H/sigma0 {mpi2!r}; lam(sigma0^2 - v^2) {lam * (s0 * s0 - v * v)!r};"
              f" Hessian {['%.8f' % e for e in ev]}; m_sigma^2 analytic {lam * (3 * s0 * s0 - v * v):.8f}")

    print("== 3. GMOR ==")
    mq, c13, fpi = inputs.MU_PLUS_MD, inputs.COND_13, inputs.F_PI
    mpi = gmor_mpi(mq, c13, fpi)
    print(f" gmor_mpi = {mpi:.6f} GeV  (measured pi0 {inputs.M_PI0}, pi+- {inputs.M_PIC})")
    H = mq * c13 ** 3 / fpi
    for lam in (5.0, 40.0):
        v = math.sqrt(fpi * fpi - H / (lam * fpi))
        s0, mpi2 = sigma_model_vacuum(lam, v, H)
        print(f"   second route, sigma model at lam={lam}: sigma0/f_pi = {s0 / fpi!r}, sqrt(mpi2) = {math.sqrt(mpi2):.6f}")
    dm = 0.5 * inputs.MU_PLUS_MD_ERR / mq
    dc = 1.5 * inputs.COND_13_ERR / c13
    print(f"   input uncertainty: +-{mpi * math.hypot(dm, dc):.4f} GeV (quark masses {dm:.3%}, condensate {dc:.3%})")

    print("== 4. ChPT O(p^4) (quoted) ==")
    args = (inputs.M_UD_FLAG, inputs.COND_13, inputs.FPI_OVER_F, inputs.LBAR3, inputs.F_PI)
    full = chpt_mpi(*args)
    lo = chpt_mpi(args[0], args[1], args[2], 0.0, args[4])
    F = inputs.F_PI / inputs.FPI_OVER_F
    x = lo * lo * inputs.LBAR3 / (32 * math.pi ** 2 * F * F)
    print(f" chpt_mpi = {full:.6f} GeV; LO (lbar3 = 0) {lo:.6f}; gmor_mpi(2 m_ud, cond13, F) ="
          f" {gmor_mpi(2 * inputs.M_UD_FLAG, inputs.COND_13, F):.6f}")
    print(f"   expansion parameter {x:.5f}; first-order M(1 - x/2) = {lo * (1 - x / 2):.6f}")

    print("== 5. Yukawa ==")
    for r, m in ((0.3, 1.5), (2.1, 1.5), (2.0, 0.0), (1.0, 0.0)):
        print(f" r={r} m={m}: residue {yukawa(r, m)!r}; proper-time integral {_yukawa_proper_time(r, m)!r}")
    m_pi_fm = inputs.M_PIC / inputs.HBARC_GEV_FM
    print(f"   pion range 1/m_pi = {1 / m_pi_fm:.4f} fm")

    print("== 6. tensor identity ==")
    q = [0.8, 0.0, -1.1]
    q2 = sum(x * x for x in q)
    print(f" residual at q={q}: {tensor_identity_residual(q):.2e}; at [0.3, -1.7, 0.9]:"
          f" {tensor_identity_residual([0.3, -1.7, 0.9]):.2e}")
    nq = math.sqrt(q2)
    S = [[x.real for x in row] for row in _s12([x / nq for x in q])]
    sq = _sigma_dot(q)
    L = [[x.real for x in row] for row in _kron(sq, sq)]
    print(f"   eigenvalues of S12 {['%.6f' % e for e in toolkit.eigvalsh(S)]} (expect -4, 0, 2, 2)")
    print(f"   eigenvalues of (s1.q)(s2.q)/q^2 {['%.6f' % (e / q2) for e in toolkit.eigvalsh(L)]} (expect -1, -1, 1, 1)")

    print("== 7. Goldberger-Treiman ==")
    g = goldberger_treiman(inputs.G_A, inputs.M_N, inputs.F_PI)
    print(f" g_piNN = {g:.4f}; sigma model with nucleons (g_A = 1): M_N/f_pi = "
          f"{goldberger_treiman(1, inputs.M_N, inputs.F_PI):.4f}")
    print(f"   measured {inputs.G_PINN_EMP} +- {inputs.G_PINN_ERR}: discrepancy {1 - g / inputs.G_PINN_EMP:.3%}")
