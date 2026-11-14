"""weak: the pion decay constant from G_F (SPEC.md section 10).

Derivation (amplitude, Dirac-equation reduction, spin trace, two-body phase space) and the
second routes: DERIVATION_weak.md. Inputs are read as inputs.NAME at call time.
"""
import math

import inputs
import toolkit

PROVENANCE = {
    "pion_decay_width": ("derived", "SPEC 10 V-A amplitude M = i(G_F/sqrt2)V_ud f ubar pslash(1-g5) v; Dirac eq."
                                    " gives m_l ubar(1-g5)v; spin trace Tr[(1-g5)(-qslash)(1+g5)(-kslash+m)] ="
                                    " -8 k.q = 4(m_pi^2-m_l^2); two-body phase space k*/(4 pi m_pi):"
                                    " Gamma = G_F^2 V^2 f^2 m_l^2 (m_pi^2-m_l^2)^2/(8 pi m_pi^3)"),
    "fpi_from_pion_decay": ("derived", "Gamma_tree = GAMMA_PI_MUNU hbar/(1+DELTA_PI), hbar = HBAR/(E_CH 1e9) GeV s;"
                                       " width is exactly quadratic in f, so f = sqrt(Gamma_tree /"
                                       " pion_decay_width(1, G_F, V_UD, M_MU, M_PIC))"),
}


def pion_decay_width(fpi, GF, Vud, m_l, m_pi):
    """Tree-level Gamma(pi- -> l- nubar) in GeV; fpi in the ~130 MeV convention."""
    if m_l >= m_pi:
        return 0.0                                     # kinematically closed
    kstar = (m_pi * m_pi - m_l * m_l) / (2 * m_pi)     # lepton momentum in the pion rest frame
    msq = 2 * GF * GF * Vud * Vud * fpi * fpi * m_l * m_l * (m_pi * m_pi - m_l * m_l)   # spin-summed |M|^2
    phase_space = kstar / (4 * math.pi * m_pi)
    return msq * phase_space / (2 * m_pi)


def _gamma_tree_measured():
    hbar_gev_s = inputs.HBAR / (inputs.E_CH * 1e9)
    return inputs.GAMMA_PI_MUNU * hbar_gev_s / (1 + inputs.DELTA_PI)


def fpi_from_pion_decay():
    """f_pi (GeV, ~130 MeV convention) from the measured pi -> mu nu width."""
    unit = pion_decay_width(1.0, inputs.G_F, inputs.V_UD, inputs.M_MU, inputs.M_PIC)
    return math.sqrt(_gamma_tree_measured() / unit)


# ------------------------------------------------------------------------------------------
# second routes (DERIVATION_weak.md 1f, 2)
# ------------------------------------------------------------------------------------------
def _mat(n=4):
    return [[0j] * n for _ in range(n)]


def _mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def _add(A, B, a=1, b=1):
    return [[a * A[i][j] + b * B[i][j] for j in range(4)] for i in range(4)]


def _dag(A):
    return [[A[j][i].conjugate() for j in range(4)] for i in range(4)]


def _gammas():
    s = [[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]]
    g0 = _mat()
    for i in range(2):
        g0[i][i + 2] = g0[i + 2][i] = 1
    gs = [g0]
    for sig in s:
        g = _mat()
        for i in range(2):
            for j in range(2):
                g[i][j + 2] = sig[i][j]
                g[i + 2][j] = -sig[i][j]
        gs.append(g)
    g5 = _mul(_mul(gs[0], gs[1]), _mul(gs[2], gs[3]))
    g5 = [[1j * x for x in row] for row in g5]
    return gs, g5


def _slash(p, gs):
    """p_m gamma^m with p_m = g_mn p^n, g = diag(-1,1,1,1)."""
    out = _mat()
    for mu in range(4):
        c = -p[0] if mu == 0 else p[mu]
        out = _add(out, gs[mu], 1, c)
    return out


def _trace_route(m_l, m_pi):
    """Spin sum of |ubar pslash(1-g5) v|^2 with explicit matrices, no Dirac-equation shortcut."""
    gs, g5 = _gammas()
    one = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
    eta = [-1, 1, 1, 1]
    cliff = 0.0
    for a in range(4):
        for b in range(4):
            ac = _add(_mul(gs[a], gs[b]), _mul(gs[b], gs[a]))
            for i in range(4):
                for j in range(4):
                    want = -2 * eta[a] if (a == b and i == j) else 0
                    cliff = max(cliff, abs(ac[i][j] - want))
    ks = (m_pi * m_pi - m_l * m_l) / (2 * m_pi)
    n = (0.3, -0.5, math.sqrt(1 - 0.34))                 # an arbitrary unit direction
    k = (math.sqrt(ks * ks + m_l * m_l), ks * n[0], ks * n[1], ks * n[2])
    q = (ks, -ks * n[0], -ks * n[1], -ks * n[2])
    p = tuple(a + b for a, b in zip(k, q))
    G = _mul(_slash(p, gs), _add(one, g5, 1, -1))
    Gbar = _mul(_mul(gs[0], _dag(G)), gs[0])
    sum_v = _add(_mat(), _slash(q, gs), 1, -1)          # -qslash
    sum_u = _add(one, _slash(k, gs), m_l, -1)           # -kslash + m
    T = _mul(_mul(G, sum_v), _mul(Gbar, sum_u))
    return sum(T[i][i] for i in range(4)), cliff


def _smeared_phase_space(m_l, m_pi, s, n=8001):
    """Int 4 pi k^2/((2pi)^2 4 E_l k) g_s(m_pi - E_l - k) dk with a normalized Gaussian g_s."""
    ks = (m_pi * m_pi - m_l * m_l) / (2 * m_pi)
    a, b = max(ks - 12 * s, 0.0), ks + 12 * s
    dk = (b - a) / (n - 1)
    ys = []
    for i in range(n):
        kk = a + i * dk
        El = math.sqrt(kk * kk + m_l * m_l)
        x = m_pi - El - kk
        g = math.exp(-x * x / (2 * s * s)) / (s * math.sqrt(2 * math.pi))
        ys.append(4 * math.pi * kk * kk / ((2 * math.pi) ** 2 * 4 * El * kk) * g if kk > 0 else 0.0)
    return toolkit.trapezoid(ys, dk)


if __name__ == "__main__":
    mpi, mmu = inputs.M_PIC, inputs.M_MU
    tr, cliff = _trace_route(mmu, mpi)
    print("Clifford residual max|{g,g} + 2 eta| :", cliff)
    print("spin sum, explicit matrices          :", tr)
    print("spin sum, m_l^2 * 4 (m_pi^2 - m_l^2) :", mmu * mmu * 4 * (mpi * mpi - mmu * mmu))
    ks = (mpi * mpi - mmu * mmu) / (2 * mpi)
    for s in (1e-3, 3e-4, 1e-4):
        print(f"phase space smeared s={s:g}       :", _smeared_phase_space(mmu, mpi, s))
    print("phase space k*/(4 pi m_pi)           :", ks / (4 * math.pi * mpi))
    f = fpi_from_pion_decay()
    gt = _gamma_tree_measured()
    fb = toolkit.bisect(lambda x: pion_decay_width(x, inputs.G_F, inputs.V_UD, mmu, mpi) - gt, 0.0, 1.0)
    fc = math.sqrt(8 * math.pi * mpi ** 3 * gt) / (inputs.G_F * inputs.V_UD * mmu * (mpi * mpi - mmu * mmu))
    print("f_pi (GeV) main route                :", f)
    print("f_pi (GeV) bisect route              :", fb)
    print("f_pi (GeV) closed form               :", fc)
    print("f_pi / sqrt2 (GeV)                   :", f / math.sqrt(2))
    lim = pion_decay_width(f, inputs.G_F, inputs.V_UD, 1e-6, mpi) / 1e-12
    print("m_l -> 0: Gamma/m_l^2 vs G^2V^2f^2 m_pi/(8pi):", lim, (inputs.G_F * inputs.V_UD * f) ** 2 * mpi / (8 * math.pi))
