#!/usr/bin/env python3
"""
The strong-force rung of the symmetry-breaking ladder (SYMMETRY_LADDER.md): chiral symmetry
breaking, pions, and the nuclear force.

Colour SU(3)_C is never broken. What breaks, at about 1 GeV, is the approximate chiral
symmetry of the two light quarks, SU(2)_L x SU(2)_R -> SU(2)_V, through the quark
condensate <qbar q>. The pions are its (pseudo-)Goldstone bosons, and their exchange between
nucleons is the long-range part of the nuclear force.

Derived here in the linear sigma model (Gell-Mann and Levy 1960): the minimal model with
this breaking pattern, phi = (sigma, pi_1, pi_2, pi_3), O(4) = SU(2) x SU(2) symmetric
potential V = (lam/4)(phi^2 - v^2)^2 - H sigma, H the explicit breaking by the quark masses.
It is a MODEL of QCD's low-energy structure, not QCD itself.

  S1  Goldstone counting: with H = 0 the vacuum breaks O(4) -> O(3); the mass matrix has
      exactly 3 zero eigenvalues = dim O(4) - dim O(3) = 6 - 3. (CHECK)
  S2  With H > 0: m_pi^2 = H / <sigma>, f_pi = <sigma>, hence m_pi^2 f_pi^2 = H f_pi. The
      QCD identification H f_pi = (m_u + m_d)|<qbar q>| is the Gell-Mann-Oakes-Renner
      relation. (CHECK, symbolic)
  S3  GMOR with measured inputs: m_u + m_d (PDG, MS-bar 2 GeV), f_pi (PDG), the condensate
      (lattice, FLAG; LIT). The predicted m_pi against the measured one; the difference is
      the higher-order chiral correction, not derived here. (CHECK)
  S4  The nuclear force. Exchange of a particle of mass m gives V(q) ~ -1/(q^2 + m^2); its
      Fourier transform is the Yukawa potential e^{-m r}/(4 pi r), with range 1/m_pi = 1.41 fm
      (derived symbolically). The one-pion-exchange potential's spin-isospin structure,
      including the tensor force, from the pseudovector pi-N coupling. (CHECK)
  S5  The coupling: chiral symmetry gives the Goldberger-Treiman relation
      g_piNN = g_A M_N / f_pi; with measured g_A, M_N, f_pi, against the empirical g_piNN
      from pi-N and N-N scattering. (CHECK)
Labels: MODEL (linear sigma model), CHECK, LIT (measured or lattice inputs).
"""
import math

import sympy as sp

# measured inputs (PDG 2024; FLAG 2024 for the condensate)
MU_PLUS_MD = 2.16e-3 + 4.70e-3      # GeV, MS-bar at 2 GeV
F_PI = 0.1302 / math.sqrt(2)        # GeV (f_pi = 130.2 MeV in the sqrt2 convention -> 92.1 MeV)
SIGMA_CUBE_ROOT = 0.272             # GeV, |<qbar q>|^(1/3), N_f = 2+1, MS-bar 2 GeV (FLAG)
M_PI0, M_PIC = 0.1349768, 0.13957039
G_A = 1.2754                        # nucleon axial coupling
M_N = 0.9389187                     # GeV, average nucleon mass
G_PINN_EMP = 13.1                   # empirical pi-N coupling, g^2/4pi ~ 13.7 (LIT, approximate)
HBARC = 0.1973269804                # GeV fm


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def sigma_model():
    lam, v, H = sp.symbols("lambda v H", positive=True)
    s, p1, p2, p3 = sp.symbols("sigma pi1 pi2 pi3", real=True)
    phi2 = s**2 + p1**2 + p2**2 + p3**2
    V = lam / 4 * (phi2 - v**2) ** 2 - H * s
    return V, (s, p1, p2, p3), lam, v, H


def goldstone_count():
    """S1: H = 0, vacuum sigma = v: number of zero eigenvalues of the Hessian."""
    V, f, lam, v, H = sigma_model()
    V0 = V.subs(H, 0)
    vac = {f[0]: v, f[1]: 0, f[2]: 0, f[3]: 0}
    grad = [sp.simplify(sp.diff(V0, x).subs(vac)) for x in f]
    Hm = sp.Matrix(4, 4, lambda i, j: sp.diff(V0, f[i], f[j]).subs(vac))
    evs = Hm.eigenvals()
    zeros = sum(m for e, m in evs.items() if sp.simplify(e) == 0)
    return grad, zeros, {sp.simplify(e): m for e, m in evs.items()}


def gmor():
    """S2: with H > 0, the vacuum <sigma> = s0 solves lam s0 (s0^2 - v^2) = H; then
    m_pi^2 = H / s0 exactly (tree level), and f_pi = s0."""
    V, f, lam, v, H = sigma_model()
    s0 = sp.Symbol("s0", positive=True)
    vac = {f[0]: s0, f[1]: 0, f[2]: 0, f[3]: 0}
    stationarity = sp.simplify(sp.diff(V, f[0]).subs(vac))          # = lam s0 (s0^2 - v^2) - H
    Hsol = sp.solve(sp.Eq(stationarity, 0), H)[0]
    mpi2 = sp.simplify(sp.diff(V, f[1], 2).subs(vac).subs(H, Hsol))
    msig2 = sp.simplify(sp.diff(V, f[0], 2).subs(vac).subs(H, Hsol))
    return stationarity, sp.simplify(mpi2 - Hsol / s0), msig2


def gmor_numbers():
    """S3: m_pi from GMOR with measured inputs."""
    cond = SIGMA_CUBE_ROOT**3
    mpi = math.sqrt(MU_PLUS_MD * cond) / F_PI
    return mpi, MU_PLUS_MD * cond, F_PI


def yukawa():
    """S4: Fourier transform of 1/(q^2 + m^2) in three dimensions, and the range."""
    q, r, m = sp.symbols("q r m", positive=True)
    # (1/(2 pi)^3) int d^3q e^{i q.r} / (q^2 + m^2) = (1/(2 pi^2 r)) int_0^oo q sin(q r)/(q^2 + m^2) dq
    radial = sp.integrate(q * sp.sin(q * r) / (q**2 + m**2), (q, 0, sp.oo), conds="none")
    V = sp.simplify(radial / (2 * sp.pi**2 * r))
    return V, HBARC / M_PIC


def ope_structure():
    """S4: the pseudovector coupling (f/m_pi) sigma.grad tau gives, between nucleons,
    V(q) ~ -(sigma1.q)(sigma2.q)/(q^2 + m^2). Decompose (s1.q)(s2.q) = (q^2/3) s1.s2 +
    (tensor part); check the identity with explicit Pauli matrices for random q."""
    import random
    sx = sp.Matrix([[0, 1], [1, 0]]); sy = sp.Matrix([[0, -sp.I], [sp.I, 0]]); sz = sp.Matrix([[1, 0], [0, -1]])
    S = [sx, sy, sz]
    kron = lambda A, B: sp.Matrix(sp.BlockMatrix([[A[i, j] * B for j in range(2)] for i in range(2)]))
    rng = random.Random(3)
    q = [sp.Rational(rng.randint(-5, 5), 3) for _ in range(3)]
    q2 = sum(x**2 for x in q)
    msum = lambda it, n: sum(it, sp.zeros(n, n))
    s1q = msum((q[i] * S[i] for i in range(3)), 2)
    lhs = kron(s1q, s1q)                                                 # (s1.q)(s2.q)
    s1s2 = msum((kron(S[i], S[i]) for i in range(3)), 4)
    qhat = [x / sp.sqrt(q2) for x in q]
    sq = msum((qhat[i] * S[i] for i in range(3)), 2)
    S12 = 3 * kron(sq, sq) - s1s2
    rhs = q2 / 3 * (s1s2 + S12)
    return sp.simplify(lhs - rhs) == sp.zeros(4, 4)


def goldberger_treiman():
    """S5: g_piNN = g_A M_N / f_pi."""
    g = G_A * M_N / F_PI
    return g, G_PINN_EMP


def main():
    banner("S1  Goldstone counting in the chiral limit (MODEL: linear sigma model)")
    grad, zeros, evs = goldstone_count()
    print(f"   Vacuum sigma = v is stationary: gradient {grad}")
    print(f"   Hessian eigenvalues {evs}: {zeros} zero modes = dim O(4) - dim O(3) = 6 - 3 (the pions)")

    banner("S2  Explicit breaking by quark masses: the GMOR relation (MODEL, symbolic)")
    stat, resid, msig2 = gmor()
    print(f"   Vacuum condition: {stat} = 0")
    print(f"   m_pi^2 - H/<sigma> = {resid}   (so m_pi^2 f_pi^2 = H f_pi, f_pi = <sigma>)")
    print(f"   m_sigma^2 = {msig2}")
    print("   QCD: H f_pi = (m_u + m_d) |<qbar q>|  ->  m_pi^2 f_pi^2 = (m_u + m_d)|<qbar q>|  (GMOR)")

    banner("S3  GMOR with measured inputs (LIT: PDG quark masses and f_pi; FLAG condensate)")
    mpi, num, fpi = gmor_numbers()
    print(f"   (m_u + m_d)|<qbar q>| = {num:.4e} GeV^4, f_pi = {fpi * 1e3:.1f} MeV")
    print(f"   m_pi (GMOR) = {mpi * 1e3:.1f} MeV;  measured pi0 {M_PI0 * 1e3:.1f}, pi+ {M_PIC * 1e3:.1f} MeV"
          f"  ({100 * (mpi / M_PI0 - 1):+.1f}%: higher-order chiral terms, not derived here)")

    banner("S4  The nuclear force: one-pion exchange (CHECK)")
    V, rng = yukawa()
    print(f"   FT[1/(q^2 + m^2)] = {V}   (the Yukawa potential)")
    print(f"   Range 1/m_pi = hbar c / m_pi = {rng:.3f} fm")
    print(f"   (s1.q)(s2.q) = (q^2/3)[s1.s2 + S12(q)] with Pauli matrices: {ope_structure()}"
          "  -> central + tensor force")

    banner("S5  The pion-nucleon coupling from chiral symmetry (Goldberger-Treiman)")
    g, emp = goldberger_treiman()
    print(f"   g_piNN = g_A M_N / f_pi = {g:.2f};  empirical about {emp} ({100 * (g / emp - 1):+.1f}%,"
          " the known Goldberger-Treiman discrepancy)")


if __name__ == "__main__":
    main()
