"""Stage `weak` (build 2026-11-b): the charged pion's leptonic decay and f_pi from G_F.

Postulates: SPEC.md section 10. Derivation: DERIVATION_weak.md (same directory), sections cited below.
Nothing is quoted. Natural units, energies in GeV.
"""
import math

import inputs
import toolkit

PROVENANCE = {
    "pion_decay_width": ("derived", "tree amplitude of the V-A four-fermion interaction with <0|A^alpha|pi> = i f p^alpha;"
                                    " Dirac equation reduces it to m_l ubar(1-gamma_5)v; spin sum by the trace"
                                    " -8 m_l^2 k.q -> sum|M|^2 = 2 GF^2 V^2 f^2 m_l^2 (m_pi^2 - m_l^2); two-body phase"
                                    " space k*/(8 pi m_pi^2) from the delta-function integral (DERIVATION sections"
                                    " 1-4); checked against explicit spinors and a numerical phase-space integral"),
    "fpi_from_pion_decay": ("derived", "Gamma_tree = hbar GAMMA_PI_MUNU/(1 + DELTA_PI) in GeV, inverted with"
                                       " pion_decay_width itself using its exact f^2 homogeneity: f = f0"
                                       " sqrt(target/width(f0)) (DERIVATION section 5); checked by bisection"),
}


# ------------------------------------------------------------------------------------------
# the derived pieces
# ------------------------------------------------------------------------------------------
def _spin_summed_m2(fpi, GF, Vud, m_l, m_pi):
    """sum over spins of |M|^2 (DERIVATION eq. 2.1): (GF^2/2) V^2 f^2 m_l^2 x trace, trace = -8 k.q."""
    k_dot_q = -(m_pi * m_pi - m_l * m_l) / 2          # from p^2 = (k + q)^2, metric (-,+,+,+)
    trace = -8 * k_dot_q
    return (GF * GF / 2) * (Vud * Vud) * (fpi * fpi) * (m_l * m_l) * trace


def _decay_momentum(m_l, m_pi):
    """|k| of either product in the pion rest frame, the other being massless: root of sqrt(k^2+m^2) + k = M."""
    return (m_pi * m_pi - m_l * m_l) / (2 * m_pi)


def _two_body_rate_factor(m_l, m_pi):
    """Gamma / <sum|M|^2>_Omega for a parent at rest (DERIVATION eq. 3.1): k*/(8 pi M^2)."""
    return _decay_momentum(m_l, m_pi) / (8 * math.pi * m_pi * m_pi)


def pion_decay_width(fpi, GF, Vud, m_l, m_pi):
    """Tree-level width (GeV) of pi- -> l- nubar; fpi in the ~130 MeV convention; 0 if the channel is closed."""
    if m_pi <= 0 or m_l >= m_pi:
        return 0.0
    return _spin_summed_m2(fpi, GF, Vud, m_l, m_pi) * _two_body_rate_factor(m_l, m_pi)


def _hbar_gev_s():
    return inputs.HBAR / (inputs.E_CH * 1e9)


def _tree_width_target():
    """The measured pi -> mu nu width with the radiative correction removed, in GeV."""
    return inputs.GAMMA_PI_MUNU * _hbar_gev_s() / (1 + inputs.DELTA_PI)


def fpi_from_pion_decay():
    """f_pi (GeV, ~130 MeV convention) at which pion_decay_width reproduces the measured width."""
    f0 = 1.0
    w0 = pion_decay_width(f0, inputs.G_F, inputs.V_UD, inputs.M_MU, inputs.M_PIC)
    return f0 * math.sqrt(_tree_width_target() / w0)


# ------------------------------------------------------------------------------------------
# self-check: the second routes of DERIVATION_weak.md section 6
# ------------------------------------------------------------------------------------------
def _mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def _lin(terms):
    return [[sum(c * M[i][j] for c, M in terms) for j in range(4)] for i in range(4)]


def _gammas():
    """Dirac representation with {g^mu, g^nu} = -2 g^{mu nu}, g = diag(-1,1,1,1); gamma_5 = i g0 g1 g2 g3."""
    s = [[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]]
    g0 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]]
    gs = [g0]
    for a in range(3):
        g = [[0] * 4 for _ in range(4)]
        for i in range(2):
            for j in range(2):
                g[i][2 + j] = s[a][i][j]
                g[2 + i][j] = -s[a][i][j]
        gs.append(g)
    g5 = [[1j * x for x in row] for row in _mm(_mm(gs[0], gs[1]), _mm(gs[2], gs[3]))]
    return gs, g5, s


def _slash(gs, p):
    """p_mu gamma^mu for contravariant p = (E, px, py, pz): p_0 = -E."""
    return _lin([(-p[0], gs[0]), (p[1], gs[1]), (p[2], gs[2]), (p[3], gs[3])])


def _spinors(p, m, s):
    """[u_1, u_2], [v_1, v_2] of momentum p = (E, vec), mass m."""
    E = p[0]
    sp = [[sum(p[1 + a] * s[a][i][j] for a in range(3)) for j in range(2)] for i in range(2)]
    n = math.sqrt(E + m)
    us, vs = [], []
    for chi in ([1, 0], [0, 1]):
        low = [sum(sp[i][j] * chi[j] for j in range(2)) / (E + m) for i in range(2)]
        us.append([n * x for x in chi + low])
        vs.append([n * x for x in low + chi])
    return us, vs


def _bar(u, g0):
    return [sum(u[i].conjugate() * g0[i][j] for i in range(4)) for j in range(4)]


def _sandwich(a, M, b):
    return sum(a[i] * M[i][j] * b[j] for i in range(4) for j in range(4))


def _selfcheck():
    fpi, GF, Vud, m_l, m_pi = 0.13, 1e-5, 0.97, 0.11, 0.14
    gs, g5, s = _gammas()
    one = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
    eta = [-1, 1, 1, 1]
    # Clifford algebra and gamma_5
    worst = 0.0
    for mu in range(4):
        for nu in range(4):
            A = _lin([(1, _mm(gs[mu], gs[nu])), (1, _mm(gs[nu], gs[mu]))])
            tgt = -2 * eta[mu] if mu == nu else 0
            worst = max(worst, max(abs(A[i][j] - tgt * one[i][j]) for i in range(4) for j in range(4)))
    print(f"Clifford {{g,g}} = -2 eta: max residual {worst:.1e}")

    kst = _decay_momentum(m_l, m_pi)
    Ek = math.sqrt(kst * kst + m_l * m_l)
    PL = _lin([(1, one), (-1, g5)])
    PR = _lin([(1, one), (1, g5)])
    p = (m_pi, 0.0, 0.0, 0.0)
    pslash = _slash(gs, p)

    def m2_at(c):
        sn = math.sqrt(1 - c * c)
        k = (Ek, kst * sn, 0.0, kst * c)
        q = (kst, -kst * sn, 0.0, -kst * c)
        us, _ = _spinors(k, m_l, s)
        _, vs = _spinors(q, 0.0, s)
        O = _mm(pslash, PL)
        tot = 0.0
        for u in us:
            ub = _bar(u, gs[0])
            for v in vs:
                tot += abs(_sandwich(ub, O, v)) ** 2
        return (GF * GF / 2) * Vud * Vud * fpi * fpi * tot, k, q, us

    # spin-sum check of the spinor construction
    _, k, q, us = m2_at(0.3)
    S = [[sum(u[i] * _bar(u, gs[0])[j] for u in us) for j in range(4)] for i in range(4)]
    T = _lin([(-1, _slash(gs, k)), (m_l, one)])
    print("sum u ubar = -kslash + m: max residual",
          f"{max(abs(S[i][j] - T[i][j]) for i in range(4) for j in range(4)):.1e}")

    # route A: explicit spinors, angular average by trapezoid
    n = 201
    cs = [-1 + 2 * i / (n - 1) for i in range(n)]
    vals = [m2_at(c)[0] for c in cs]
    avg = toolkit.trapezoid(vals, 2 / (n - 1)) / 2
    main_m2 = _spin_summed_m2(fpi, GF, Vud, m_l, m_pi)
    print(f"sum|M|^2   trace formula {main_m2:.15e}   explicit spinors {avg:.15e}   ratio {avg / main_m2:.15f}")
    print(f"           isotropy: (max-min)/mean = {(max(vals) - min(vals)) / avg:.1e}")

    # route B: matrix trace of the unreduced amplitude
    X = _mm(_mm(_mm(T, _mm(pslash, PL)), _lin([(-1, _slash(gs, q))])), _mm(PR, pslash))
    tr = sum(X[i][i] for i in range(4))
    print(f"matrix trace {tr.real:.15e} (imag {tr.imag:.1e})   vs 4 m_l^2 (m_pi^2 - m_l^2) ="
          f" {4 * m_l**2 * (m_pi**2 - m_l**2):.15e}")

    # route C: phase space with a smeared delta function
    sig = 1e-3 * m_pi
    N = 4 * 10 ** 4 + 1
    lo, hi = max(kst - 10 * sig, 0.0), kst + 10 * sig
    dk = (hi - lo) / (N - 1)
    ys = []
    for i in range(N):
        kk = lo + i * dk
        E = math.sqrt(kk * kk + m_l * m_l)
        x = (m_pi - E - kk) / sig
        ys.append(kk * kk / (E * kk) * math.exp(-x * x / 2) / (sig * math.sqrt(2 * math.pi)) if kk > 0 else 0.0)
    num = toolkit.trapezoid(ys, dk)
    print(f"int k^2 dk/(E k) delta(M - E - k): numeric {num:.9f}   k*/M {kst / m_pi:.9f}")
    gam_num = (1 / (2 * m_pi)) * (1 / (16 * math.pi ** 2)) * num * 4 * math.pi * avg
    print(f"width      main {pion_decay_width(fpi, GF, Vud, m_l, m_pi):.12e}   second route {gam_num:.12e} GeV")

    # route D: inversion by bisection
    f = fpi_from_pion_decay()
    tgt = _tree_width_target()
    fb = toolkit.bisect(lambda x: pion_decay_width(x, inputs.G_F, inputs.V_UD, inputs.M_MU, inputs.M_PIC) - tgt,
                        1e-3, 10.0)
    print(f"f_pi       main {f:.12f}   bisection {fb:.12f} GeV   (/sqrt2 = {f / math.sqrt(2):.6f})")
    back = pion_decay_width(f, inputs.G_F, inputs.V_UD, inputs.M_MU, inputs.M_PIC) * (1 + inputs.DELTA_PI) / _hbar_gev_s()
    print(f"round trip width {back:.6e} s^-1   measured {inputs.GAMMA_PI_MUNU:.6e} s^-1")
    # route E: limits
    r = [pion_decay_width(fpi, GF, Vud, x, m_pi) / x ** 2 for x in (1e-5, 1e-6)]
    print(f"Gamma/m_l^2 as m_l -> 0: {r[0]:.9e}, {r[1]:.9e};  closed channel: {pion_decay_width(fpi, GF, Vud, m_pi, m_pi)}")


if __name__ == "__main__":
    _selfcheck()
