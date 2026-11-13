"""Reference adapter: src/ladder_standalone.py wrapped to the rebuild contract.

HARNESS SELF-TEST ONLY. It exists to prove that the harness passes a correct build and fails
broken ones (tests/test_rebuild_harness.py). It is NOT an independent build: it imports the
reference. A builder must never read this directory.

Module-level constants of the reference are synced from rebuild/inputs.py before each call,
so the harness's sensitivity tier (which mutates inputs) sees the response it should.
"""
import importlib.util
import os
import sys
from fractions import Fraction as F
from math import exp, pi, sqrt
from itertools import permutations

import inputs

# located through inputs.py (always rebuild/inputs.py), so copies of this build elsewhere work too
_P = os.path.join(os.path.dirname(os.path.abspath(inputs.__file__)), "..", "src", "ladder_standalone.py")
_spec = importlib.util.spec_from_file_location("_ladder_ref_for_selftest", _P)
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)


def _m(stage):
    """The loaded stage module, so connected calls go through it (and the harness's spies)."""
    return sys.modules[stage]


def sync():
    for k in dir(inputs):
        if k.isupper() and hasattr(L, k):
            setattr(L, k, getattr(inputs, k))


def _prov(names, kind="derived", quoted=()):
    return {n: (("quoted" if n in quoted else kind), "reference adapter (self-test)") for n in names}


# --- toolkit ------------------------------------------------------------------------------
def eigvalsh(A):
    return L.jacobi_eigenvalues(A)


def hessian(f, x, h=1e-4):
    return L.hessian(f, x, h)


def exact_derivative(f, x):
    return f(L.Dual(x, 1)).b


def bisect(f, a, b, iters=200):
    fa = f(a)
    for _ in range(iters):
        m = (a + b) / 2
        fm = f(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


def golden_max(f, a, b, iters=200):
    return L.golden_max(f, a, b, iters)


def trapezoid(ys, dx):
    return dx * (sum(ys) - 0.5 * (ys[0] + ys[-1]))


def levi_civita(p):
    return 0 if len(set(p)) < len(p) else L.parity(p)


# --- gauge331 -----------------------------------------------------------------------------
def triplet_charges(X, variant, anti=False):
    return L.triplet_charges(F(X), variant, anti)


def quark_charges(Nc):
    return L.model(Nc, "-1/sqrt3")[2:4]


def doublet_charge_pairs(Nc, variant):
    ferm = L.model(Nc, variant)[0]
    return {frozenset(L.triplet_charges(X, variant, anti)[:2]) for _, dL, _, X, anti in ferm if dL == 3}


def mass_matrix(variant, g, gX, w, v1, v2):
    return L.mass_matrix(variant, g, gX, w, v1, v2)


def photon_direction(variant, g, gX):
    return [0, 0, 1 / g, 0, 0, 0, 0, L.BETA[variant] / g, 1 / gX]


def inv_e2(variant, g, gX):
    return sum(x * x for x in photon_direction(variant, g, gX))


def neutral_masses(variant, g, gX, w, v1, v2):
    M = L.mass_matrix(variant, g, gX, w, v1, v2)
    ev = _m("toolkit").eigvalsh([[M[i][j] for j in (2, 7, 8)] for i in (2, 7, 8)])
    return ev[1], ev[2]


def vev_from_GF(G_F):
    return (sqrt(2) * G_F) ** -0.5


def mz_tree(G_F, alpha_inv, s2):
    return sqrt(pi / alpha_inv / (sqrt(2) * G_F) / (s2 * (1 - s2)))


# --- chiral -------------------------------------------------------------------------------
def goldstone_count(lam, v):
    t = _m("toolkit")
    ev = t.eigvalsh(t.hessian(lambda p: L.sigma_potential(lam, v, 0.0, p), [v, 0, 0, 0]))
    return sum(abs(x) < 1e-6 * max(1, abs(ev[-1])) for x in ev)


def sigma_model_vacuum(lam, v, H):
    s0 = v
    for _ in range(80):
        s0 -= (lam * s0 * (s0 * s0 - v * v) - H) / (lam * (3 * s0 * s0 - v * v))
    return s0, L.hessian(lambda p: L.sigma_potential(lam, v, H, p), [s0, 0, 0, 0])[1][1]


def gmor_mpi(mq_sum, cond13, fpi):
    return sqrt(mq_sum * cond13**3) / fpi


def chpt_mpi(m_ud, cond13, fpi_over_F, lbar3, fpi):
    Fc = fpi / fpi_over_F
    M2 = 2 * m_ud * cond13**3 / Fc**2
    return sqrt(M2 * (1 - M2 / (32 * pi * pi * Fc * Fc) * lbar3))


def yukawa(r, m):
    return exp(-m * r) / (4 * pi * r)


def tensor_identity_residual(q):
    S = L.pauli()
    q2 = sum(x * x for x in q)
    sq = [[sum(q[i] * S[i][a][b] for i in range(3)) for b in range(2)] for a in range(2)]
    qh = [x / sqrt(q2) for x in q]
    sqh = [[sum(qh[i] * S[i][a][b] for i in range(3)) for b in range(2)] for a in range(2)]
    s1s2 = [[sum(L.kron(S[i], S[i])[a][b] for i in range(3)) for b in range(4)] for a in range(4)]
    S12 = L.mat_add(L.mat_scale(L.kron(sqh, sqh), 3), s1s2, -1)
    lhs, rhs = L.kron(sq, sq), L.mat_scale(L.mat_add(s1s2, S12), q2 / 3)
    return max(abs(lhs[a][b] - rhs[a][b]) for a in range(4) for b in range(4))


def goldberger_treiman(gA, MN, fpi):
    return gA * MN / fpi


# --- casimir ------------------------------------------------------------------------------
def sphere_K(eps):
    return (eps - 1) / (eps + 2)


def green_tensor(x, y, z, k):
    return L.green(x, y, z, k)


def cp_integral():
    return sum(F(c) * F(L.factorial(n), 2 ** (n + 1)) for n, c in enumerate((3, 6, 5, 2, 1)))


def cp_energy(R1, R2, K1, K2, r):
    return -float(cp_integral()) / pi * inputs.HBAR * inputs.C_LIGHT * K1 * R1**3 * K2 * R2**3 / r**7


def diamond_radius(m):
    sync()
    return L.diamond_radius(m)


def casimir_safe_gap(m, dx, tau, fraction):
    R, K = diamond_radius(m), sphere_K(inputs.EPS_DIAMOND)
    def excess(gap):
        d = sqrt(gap * gap + dx * dx)
        gr = 2 * inputs.G_NEWTON * m * m * (1 / gap - 1 / d)
        cs = 2 * (-cp_energy(R, R, K, K, gap) + cp_energy(R, R, K, K, d))
        return abs(cs) - fraction * abs(gr)
    return _m("toolkit").bisect(excess, 1e-6, 1e-3, 200)


# --- graviton -----------------------------------------------------------------------------
def point_mass_metric():
    hbar00 = F(4)
    trace = L.ETA4[0] * hbar00
    return hbar00 - F(L.ETA4[0]) * trace / 2, 0 - F(L.ETA4[1]) * trace / 2


def tpt(T1, T2):
    return L.tpt(T1, T2)


def ramp_profile(t, hold, ramp):
    return L.ramp_profile(t, hold, ramp)


def entangling_phase(m, dx, hold, ramp, gap, n=4001):
    total = hold + 2 * ramp
    inv_r = lambda r: 4 * pi * _m("chiral").yukawa(r, 0.0)        # rung 2's transform at m = 0
    ys = []
    for i in range(n):
        y = 0.5 * dx * L.ramp_profile(total * i / (n - 1), hold, ramp)
        ys.append(2 * (inv_r(gap) - inv_r(sqrt(gap * gap + (2 * y) ** 2))))
    return inputs.G_NEWTON * m * m / inputs.HBAR * _m("toolkit").trapezoid(ys, total / (n - 1))


def design_phase():
    gap = _m("casimir").casimir_safe_gap(inputs.GAP_BASELINE_MASS, inputs.GAP_BASELINE_DX,
                                         inputs.GAP_BASELINE_TAU, inputs.GAP_FRACTION)
    return _m("graviton").entangling_phase(inputs.DESIGN_A_MASS, inputs.DESIGN_A_DX, inputs.DESIGN_A_HOLD,
                                           inputs.DESIGN_A_RAMP, gap)


# --- desitter -----------------------------------------------------------------------------
def so41_generator(A, B):
    return L.J(A, B)


def spin_connection(x, f, fp):
    return L.tetrad_and_spin(x, f, fp)


def unbroken_generators(V):
    return [(A, B) for A in range(5) for B in range(A + 1, 5) if L.mat_vec(L.J(A, B), V) == [0] * 5]


def _sds(M, l):
    return (lambda r: 1 - 2 * M / r - r * r / l**2), (lambda r: 2 * M / r**2 - 2 * r / l**2)


def curvature_split_residual(M, l, x):
    f, fp = _sds(M, l)
    E, _ = L.tetrad_and_spin(x, f, fp)
    Fm, Rm = L.curvature(x, f, fp, l, True), L.curvature(x, f, fp, l, False)
    worst = 0.0
    for m in range(4):
        for n in range(4):
            for a in range(4):
                for b in range(4):
                    ee = (E[a][m] * E[b][n] - E[a][n] * E[b][m]) * L.ETA4[b]
                    worst = max(worst, abs(Fm[m][n][a][b] - Rm[m][n][a][b] + ee / l**2))
                worst = max(worst, abs(Fm[m][n][a][4]))
    return worst


def ds_curvature_max(l, x):
    Fd = L.curvature(x, lambda r: 1 - r * r / l**2, lambda r: -2 * r / l**2, l, True)
    return max(abs(Fd[m][n][i][j]) for m in range(4) for n in range(4) for i in range(5) for j in range(5))


def action_coefficients(M, l, x):
    f, fp = _sds(M, l)
    E, _ = L.tetrad_and_spin(x, f, fp)
    Rm = L.curvature(x, f, fp, l, False)
    Einv = [[(1 / E[a][a] if a == b else 0.0) for b in range(4)] for a in range(4)]
    Rup = [[[[Rm[m][n][a][b] * L.ETA4[b] for n in range(4)] for m in range(4)] for b in range(4)] for a in range(4)]
    EE = [[[[E[a][m] * E[b][n] - E[a][n] * E[b][m] for n in range(4)] for m in range(4)] for b in range(4)] for a in range(4)]
    e_det = E[0][0] * E[1][1] * E[2][2] * E[3][3]
    Rs = sum(Rm[m][n][a][b] * L.ETA4[b] * Einv[a][m] * Einv[b][n] for m in range(4) for n in range(4)
             for a in range(4) for b in range(4))
    return L.wedge(Rup, EE) / (e_det * Rs), L.wedge(EE, EE) / e_det


def ricci_scalar(M, l, x):
    f, fp = _sds(M, l)
    E, _ = L.tetrad_and_spin(x, f, fp)
    Rm = L.curvature(x, f, fp, l, False)
    return sum(Rm[m][n][a][b] * L.ETA4[b] / (E[a][m] * E[b][n]) for m in range(4) for n in range(4)
               for a in range(4) for b in range(4) if a == m and b == n)


def ell_from_lambda(Lam):
    return sqrt(3 / Lam)


def mm_coupling(Lam, lP):
    return 3 / (lP**2 * Lam)


# --- blackholes ---------------------------------------------------------------------------
def sds_horizons(M, l):
    return L.sds_horizons(M, l)


def killing_kappa(f, r0, h):
    return L.killing_kappa(f, r0, h)


def euclidean_cone_ratio(f, rh, beta, eps):
    return L.euclidean_cone(f, rh, beta, eps)


def kerr_first_law(p, q, dp, dq):
    return L.kerr_first_law(L.Dual(p, dp), L.Dual(q, dq))


def nariai_mass_kg(Lam):
    return inputs.C_LIGHT**2 * _m("desitter").ell_from_lambda(Lam) / (3 * sqrt(3) * inputs.G_NEWTON)


def kappa_from_spin_connection(M, l):
    f, fp = _sds(M, l)
    rb, rc = _m("blackholes").sds_horizons(M, l)
    sc = _m("desitter").spin_connection
    return tuple(abs(sc([0.0, r, 1.0, 0.0], f, fp)[1][0][1][0]) for r in (rb * (1 + 1e-9), rc * (1 - 1e-9)))


def photon_sphere():
    r = _m("toolkit").golden_max(lambda x: (1 - 2 / x) / x**2, 2.01, 20)
    return r, 1 / sqrt((1 - 2 / r) / r**2)


def isco():
    dV = lambda r, L2: 2 / r**2 * (1 + L2 / r**2) - (1 - 2 / r) * 2 * L2 / r**3
    min_dV = lambda L2: L.golden_max(lambda r: -dV(r, L2), 4, 9)
    lo, hi = 10.0, 14.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if dV(min_dV(mid), mid) > 0 else (lo, mid)
    r = min_dV(hi)
    return r, hi, (1 - 2 / r) * (1 + hi / r**2)


def shadow_uas(m_sun, d_pc):
    sync()
    return L.shadow_uas(m_sun, d_pc)


def kerr_area_km2(m_sun, chi):
    sync()
    return L.kerr_area_km2(m_sun, chi)


def qnm_220(m_det_sun, chi):
    sync()
    return L.qnm_220(m_det_sun, chi)


def invert_220(f, damp, z):
    sync()
    return L.invert_220(f, damp, z)


def hawking_K(m_kg):
    sync()
    return L.hawking_K(m_kg)


# --- links --------------------------------------------------------------------------------
def qp_qe_minus_anomaly(Nc, b, XL, Xt):
    Xa = Xt + 2 * b
    Qu, Qd = F(1, 2) + b + Xt, F(-1, 2) + b + Xt
    Qe = F(-1, 2) + b + XL
    Ng, n = Nc, F(Nc * (1 + Nc), 2 * Nc)
    anomaly = Ng * XL + Nc * ((Ng - n) * Xt + n * Xa)
    qp, _ = L.baryons(Qu, Qd, Nc)
    return qp + Qe - anomaly / Ng


def neutrality_per_nucleon(m):
    return sqrt(inputs.GAP_FRACTION * inputs.G_NEWTON / inputs.K_COUL) * m / inputs.E_CH / (m / inputs.U_AMU)


def pi0_width_eV(alpha, fpi, mpi, Nc, Qu, Qd):
    A = alpha / (pi * fpi) * float(Nc * (Qu * Qu - Qd * Qd))
    return 0.5 * (mpi / 2) / (8 * pi * mpi**2) * 0.5 * A**2 * mpi**4 * 1e9


def planck_mass_GeV(G, hbar, c):
    return sqrt(hbar * c / G) * c**2 / inputs.E_CH / 1e9


def g_window(p3, p5, mpl):
    return (mpl / p3) ** 2, (mpl / p5) ** 2


def schwarzschild_radius(m):
    return 2 * inputs.G_NEWTON * m / inputs.C_LIGHT**2


def matter_charges(Nc, variant):
    g = _m("gauge331")
    Qu, Qd = g.quark_charges(Nc)
    XL = L.model(Nc, variant)[0][0][3]
    lep = g.triplet_charges(XL, variant)
    qp, qn = L.baryons(Qu, Qd, Nc)
    return qp, qn, lep[1], lep[0]


def pi0_width_from_rungs():
    Qu, Qd = _m("gauge331").quark_charges(3)
    return _m("links").pi0_width_eV(inputs.ALPHA_0, inputs.F_PI, inputs.M_PI0, 3, Qu, Qd)


def planck_bh_kT_GeV():
    mpl = _m("links").planck_mass_GeV(inputs.G_NEWTON, inputs.HBAR, inputs.C_LIGHT)
    m_kg = mpl * 1e9 * inputs.E_CH / inputs.C_LIGHT**2
    return inputs.K_B * _m("blackholes").hawking_K(m_kg) / inputs.E_CH / 1e9
