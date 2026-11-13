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
      (lattice, FLAG; LIT). The predicted m_pi against the measured one. This is leading
      order with the physical f_pi standing in for the chiral-limit F; S7 does it at O(p^4).
      (CHECK)
  S4  The nuclear force. Exchange of a particle of mass m gives V(q) ~ -1/(q^2 + m^2); its
      Fourier transform is the Yukawa potential e^{-m r}/(4 pi r), with range 1/m_pi = 1.41 fm
      (derived symbolically). The one-pion-exchange potential's spin-isospin structure,
      including the tensor force, from the pseudovector pi-N coupling. (CHECK)
  S5  The coupling: chiral symmetry gives the Goldberger-Treiman relation
      g_piNN = g_A M_N / f_pi; with measured g_A, M_N, f_pi, against the empirical g_piNN
      from pi-N and N-N scattering. (CHECK)
  S6  Beyond the model: chiral perturbation theory (Weinberg, Physica A 96 (1979) 327;
      Gasser and Leutwyler, Ann. Phys. 158 (1984) 142), the effective theory of QCD itself
      at low energy. At O(p^2) its Lagrangian is
      fixed by the symmetry: L2 = (F^2/4) Tr(d U d U^+) + (F^2 M^2/4) Tr(U + U^+), F and
      M^2 = 2 B m_hat the pion decay constant and mass in the chiral limit. The O(p^4) mass is
      its one loop, the tadpole: Wick-contracting the quartic terms (<pi_a pi_b> = delta_ab
      Delta, <d pi_a . d pi_b> = delta_ab M^2 Delta in dimensional regularization) gives
      M_pi^2 = M^2 (1 + Delta / 2F^2), derived here in two parametrizations of U (exponential
      and sigma-model). They split the loop differently between wave function and mass, and
      agree on the physical mass, as they must. The tadpole itself, from Gamma(1 - d/2) at
      d = 4 - 2 eps: Delta = (M^2/16 pi^2)[ln(M^2/mu^2) - 1/eps_bar - 1]. Its log is the
      chiral log, M_pi^2 = M^2 [1 + (M^2/32 pi^2 F^2) ln(M^2/mu^2) + ...]; the O(p^4)
      constant l_3 absorbs the pole and the scale: M_pi^2 = M^2 [1 - (M^2/32 pi^2 F^2) lbar_3],
      the NLO term of FLAG 19 eq. (MF) (from Colangelo, Gasser and Leutwyler, Nucl. Phys.
      B603 (2001) 125). (CHECK, symbolic)
  S7  S3 at O(p^4). S3 used the physical f_pi with the chiral-limit condensate; the
      consistent leading order uses F: M^2 = (m_u + m_d) Sigma / F^2. With FLAG's lattice
      inputs (N_f = 2+1: m_ud, Sigma^(1/3), F_pi/F and lbar_3; LIT), m_pi = 132.6 +- 3.8 MeV
      against 135.0 (-1.7%, -0.6 sigma; the condensate dominates the error). The O(p^4) term
      itself is -2.3% of M^2: the SU(2) chiral series converges well. Most of S3's -5.5% was
      f_pi used for F (6%), not the loop. f_pi itself is S3's PDG input, 92.07 MeV; FLAG 19
      quotes 92.2(1) MeV, a 0.1% difference in m_pi. (CHECK; LIT)
  S8  f_pi at O(p^4): F_pi = F [1 + (M^2/16 pi^2 F^2) lbar_4] (LIT: FLAG 19 eq. (MF), NLO).
      With FLAG's lbar_4, F_pi/F = 1.062, FLAG's own 1.062(7): a consistency check of the
      lattice inputs used in S7, not an independent test, since both come from the same fits.
      (CHECK; LIT)
  What changes: S1-S5 remain the linear sigma model (MODEL): the breaking pattern, GMOR's
  form, the one-pion exchange. The pion mass is now an O(p^4) result of QCD's own effective
  theory, with lattice low-energy constants, and no longer carries the model's caveat. The
  sigma resonance of the model is not QCD's broad f_0(500); ChPT has no sigma field.
Labels: MODEL (linear sigma model, S1-S5), CHECK, LIT (measured or lattice inputs; the
O(p^4) formula for F_pi, FLAG 19 eq. (MF)). Every LIT number is from the source named
beside it.
"""
import math

import sympy as sp

# measured inputs (PDG 2024; the condensate is the FLAG 19 average, restated in FLAG 21)
MU_PLUS_MD = 2.16e-3 + 4.70e-3      # GeV, MS-bar at 2 GeV
F_PI = 0.1302 / math.sqrt(2)        # GeV (f_pi = 130.2 MeV in the sqrt2 convention -> 92.1 MeV)
SIGMA_CUBE_ROOT = 0.272             # GeV, |<qbar q>|^(1/3), N_f = 2+1, MS-bar 2 GeV (FLAG)
M_PI0, M_PIC = 0.1349768, 0.13957039
G_A = 1.2754                        # nucleon axial coupling
M_N = 0.9389187                     # GeV, average nucleon mass
G_PINN_EMP = 13.1                   # g_c^2/4pi = 13.69 +- 0.12 +- 0.15 (Baru et al., NPA 872, 69 (2011), eq. 9.13)
HBARC = 0.1973269804                # GeV fm
# Lattice inputs, N_f = 2+1, all checked against the FLAG sources:
#  m_ud: FLAG 2024 (arXiv:2411.04268), table "tab:mudms", MS-bar at 2 GeV.
#  Sigma^(1/3), F_pi/F, lbar_3, lbar_4: the FLAG 19 averages (Eur. Phys. J. C 80 (2020) 113),
#  restated unchanged in FLAG 21 (arXiv:2111.09849, section "SU2_averages"). FLAG 2024 omits
#  the LEC chapter, so these are the latest FLAG averages. Sigma is MS-bar at 2 GeV, SU(2)
#  chiral limit; the lbar_i are defined at the physical pion mass.
M_UD_FLAG = (3.364e-3, 0.041e-3)    # GeV, m_ud = (m_u + m_d)/2
SIGMA_ERR = 0.005                   # GeV, on Sigma^(1/3) = 272(5) MeV
FPI_OVER_F = (1.062, 0.007)
LBAR3 = (3.07, 0.64)
LBAR4 = (4.02, 0.45)


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


# ------------------------------------------------------------------ S6-S8: ChPT at O(p^4)
def chpt_lagrangian(param):
    """L2 = (F^2/4) Tr(dU dU^+) + (F^2 M^2/4) Tr(U + U^+), expanded to fourth order in the pion
    fields p_a. D_a stands for d_mu pi_a; every term carries the two derivatives contracted with
    each other, so commuting symbols D_a represent them. Returns (quadratic, quartic) parts."""
    F, M, eps = sp.symbols("F M epsilon", positive=True)
    p = sp.symbols("p1:4", real=True)
    D = sp.symbols("D1:4", real=True)
    tau = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.Matrix([[1, 0], [0, -1]])]
    A = sum((p[a] * tau[a] for a in range(3)), sp.zeros(2)) * eps / F
    dA = sum((D[a] * tau[a] for a in range(3)), sp.zeros(2)) * eps / F
    if param == "exponential":                                   # U = exp(i tau.pi / F)
        U = sum(((sp.I * A) ** n / sp.factorial(n) for n in range(5)), sp.zeros(2))
        dU = sp.zeros(2)
        for n in range(1, 5):
            for k in range(n):
                dU += sp.I**n / sp.factorial(n) * A**k * dA * A ** (n - 1 - k)
    else:                                                        # U = (sigma + i tau.pi)/F
        pi2 = sum(x**2 for x in p) * eps**2
        pdp = sum(p[a] * D[a] for a in range(3)) * eps**2
        sig = F * (1 - pi2 / (2 * F**2) - pi2**2 / (8 * F**4))   # sqrt(F^2 - pi^2) to O(pi^4)
        dsig = -pdp / F * (1 + pi2 / (2 * F**2))                 # -(pi.dpi)/sigma
        U = sig / F * sp.eye(2) + sp.I * A
        dU = dsig / F * sp.eye(2) + sp.I * dA
    L = F**2 / 4 * (dU * dU.conjugate().T).trace() + F**2 * M**2 / 4 * (U + U.conjugate().T).trace()
    L = sp.expand(sp.series(sp.expand(L), eps, 0, 5).removeO())
    return sp.expand(L.coeff(eps, 2)), sp.expand(L.coeff(eps, 4)), (F, M, p, D)


def chpt_mass_shift(param):
    """S6: contract one pair of fields in the quartic terms (the tadpole), read off the
    wave-function and mass terms, and return M_pi^2 / M^2 - 1 to first order in Delta."""
    L2, L4, (F, M, p, D) = chpt_lagrangian(param)
    Dl = sp.Symbol("Delta")
    contr = sp.expand(sum(Dl / 2 * sp.diff(L4, p[a], 2) + M**2 * Dl / 2 * sp.diff(L4, D[a], 2) for a in range(3)))
    z, m = contr.coeff(D[0], 2), contr.coeff(p[0], 2)            # L_eff = (1/2)(1 + 2z) D^2 - (1/2)(M^2 - 2m) pi^2
    free = sp.simplify(L2 - sum(D[a]**2 / 2 - M**2 * p[a]**2 / 2 for a in range(3)))
    shift = sp.simplify(sp.series((M**2 - 2 * m) / (1 + 2 * z) / M**2, Dl, 0, 2).removeO() - 1)
    return free, sp.simplify(z), sp.simplify(m), shift, (F, Dl)


def tadpole():
    """S6: Delta = int d^dk_E/(2 pi)^d 1/(k^2 + M^2) = M^(d-2) Gamma(1 - d/2)/(4 pi)^(d/2) at
    d = 4 - 2 eps, with the MS-bar scale mu_bar^2 = 4 pi e^(-gamma) mu^2; the finite part."""
    e, M, mu = sp.symbols("epsilon M mu", positive=True)
    d = 4 - 2 * e
    expr = M ** (d - 2) * sp.gamma(1 - d / 2) / (4 * sp.pi) ** (d / 2) * (mu**2 * sp.exp(sp.EulerGamma) / (4 * sp.pi)) ** e
    ser = sp.expand(sp.series(expr, e, 0, 1).removeO())
    pole = sp.simplify(ser.coeff(e, -1))
    finite = sp.simplify(sp.expand_log(ser.coeff(e, 0), force=True))
    target = M**2 / (16 * sp.pi**2) * (sp.log(M**2) - sp.log(mu**2) - 1)
    return pole, finite, sp.simplify(sp.expand_log(finite - target, force=True))


def chpt_numbers():
    """S7-S8: M^2 = (m_u + m_d) Sigma / F^2, then the O(p^4) mass with lbar_3 and F_pi/F with
    lbar_4; the uncertainty from the FLAG inputs in quadrature."""
    def mpi(mud, sig3, r, l3):
        Fc = F_PI / r
        M2 = 2 * mud * sig3**3 / Fc**2
        x = M2 / (32 * math.pi**2 * Fc**2)
        return math.sqrt(M2 * (1 - x * l3)), math.sqrt(M2), x * l3, M2, Fc
    c = (M_UD_FLAG[0], SIGMA_CUBE_ROOT, FPI_OVER_F[0], LBAR3[0])
    m, M, corr, M2, Fc = mpi(*c)
    errs = {}
    for i, (name, err) in enumerate((("m_ud", M_UD_FLAG[1]), ("Sigma^(1/3)", SIGMA_ERR),
                                     ("F_pi/F", FPI_OVER_F[1]), ("lbar_3", LBAR3[1]))):
        up = list(c)
        up[i] += err
        errs[name] = mpi(*up)[0] - m
    dm = math.sqrt(sum(v**2 for v in errs.values()))
    ratio = 1 + M2 / (16 * math.pi**2 * Fc**2) * LBAR4[0]
    return dict(mpi=m, M=M, corr=corr, err=dm, errs=errs, F=Fc, fpi_over_F=ratio)


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
          f"  ({100 * (mpi / M_PI0 - 1):+.1f}%: leading order with f_pi for F; S7 does O(p^4))")

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

    banner("S6  Chiral perturbation theory: the one-loop pion mass (CHECK, symbolic)")
    for param in ("exponential", "sigma-model"):
        free, z, m, shift, _ = chpt_mass_shift(param)
        print(f"   U {param:12s}: L2 quadratic part is the free pion (residual {free});"
              f" tadpole gives Z-term {z}, mass term {m} -> M_pi^2/M^2 - 1 = {shift}")
    pole, finite, resid = tadpole()
    print(f"   tadpole at d = 4 - 2 eps: pole {pole} / eps, finite part {finite}")
    print(f"   finite part - (M^2/16 pi^2)(ln(M^2/mu^2) - 1) = {resid}")
    print("   -> M_pi^2 = M^2 [1 + (M^2/32 pi^2 F^2) ln(M^2/mu^2) + 2 l_3^r M^2/F^2]"
          " = M^2 [1 - (M^2/32 pi^2 F^2) lbar_3]")

    banner("S7  The pion mass at O(p^4) with lattice inputs (LIT: FLAG 2024 m_ud; FLAG 19/21 LECs; N_f = 2+1)")
    n = chpt_numbers()
    print(f"   m_ud = {M_UD_FLAG[0] * 1e3:.3f} MeV, Sigma^(1/3) = {SIGMA_CUBE_ROOT * 1e3:.0f} MeV,"
          f" F = f_pi / {FPI_OVER_F[0]} = {n['F'] * 1e3:.2f} MeV, lbar_3 = {LBAR3[0]}")
    print(f"   leading order M = sqrt(2 m_ud Sigma)/F = {n['M'] * 1e3:.1f} MeV;"
          f"  O(p^4) term -(M^2/32 pi^2 F^2) lbar_3 = {-n['corr']:+.4f}")
    print(f"   m_pi = {n['mpi'] * 1e3:.1f} +- {n['err'] * 1e3:.1f} MeV;  measured pi0 {M_PI0 * 1e3:.1f} MeV"
          f"  ({100 * (n['mpi'] / M_PI0 - 1):+.1f}%, {(n['mpi'] - M_PI0) / n['err']:+.1f} sigma)")
    print("   uncertainty from: " + ", ".join(f"{k} {abs(v) * 1e3:.2f} MeV" for k, v in n["errs"].items()))
    m3 = gmor_numbers()[0]
    stepF = m3 * FPI_OVER_F[0]
    print(f"   from S3 to here: S3 {m3 * 1e3:.1f} MeV; F in place of f_pi {stepF * 1e3:.1f};"
          f" FLAG's m_ud in place of PDG's {n['M'] * 1e3:.1f}; O(p^4) {n['mpi'] * 1e3:.1f} MeV")
    print("   -> most of S3's -5.5% was f_pi used where the chiral-limit F belongs, not the loop.")

    banner("S8  f_pi at O(p^4) (LIT: FLAG 19 eq. (MF); FLAG 19/21 lbar_4)")
    print(f"   F_pi / F = 1 + (M^2/16 pi^2 F^2) lbar_4 = {n['fpi_over_F']:.4f};"
          f" FLAG {FPI_OVER_F[0]} +- {FPI_OVER_F[1]} (the same lattice fits: consistency, not a test)")
    print("   -> the pion mass is an O(p^4) result of QCD's effective theory; S1-S5 keep the model's caveat.")


if __name__ == "__main__":
    main()
