"""graviton: gravity to the two-diamond experiment (SPEC.md section 5).

Derivations and second routes: DERIVATION_graviton.md. Rung connections: the static potential
is rung 2's exchange transform at m = 0 (chiral.yukawa), the gap is rung 3's
(casimir.casimir_safe_gap), time integrals go through toolkit.trapezoid.
"""
import math
from fractions import Fraction

import inputs
import toolkit
import chiral
import casimir

PROVENANCE = {
    "point_mass_metric": ("derived", "static Poisson lap hbar00 = -16 pi G M delta^3 solved with lap(1/4 pi r) ="
                                     " -delta^3 -> hbar00 = 4 GM/r; trace reversal h = hbar - eta hbar/2 with"
                                     " Fraction eta gives h00 = hii = 2 GM/(c^2 r); gamma = hii/h00 = 1"),
    "tpt": ("derived", "P = (eta eta + eta eta - eta eta)/2 contracted with diagonal T's (indices lowered by eta):"
                       " sum_mu a_mu b_mu - tr(T1) tr(T2)/2, tr = -T00 + sum Tii; mass-mass 1/2, mass-photon 1"),
    "ramp_profile": ("derived", "SPEC 5 profile: up(t/ramp), 1, up((T-t)/ramp); up(x) = 2x^2 | 1 - 2(1-x)^2 with"
                                " x clamped to [0, 1]; C^1, time-symmetric s(T-t) = s(t)"),
    "entangling_phase": ("derived", "Delta phi = phi_LL + phi_RR - phi_LR - phi_RL (invariant under local phase"
                                    " shifts phi_ij -> phi_ij + a_i + b_j), phi_ij = -(1/hbar) int U(d_ij) dt,"
                                    " U(r) = -8 pi G tpt(T_m, T_m) m^2 chiral.yukawa(r, 0) = -4 pi G m^2/(4 pi r)"
                                    " (inverse FT of the one-graviton amplitude -8 pi G tpt/q^2); parallel"
                                    " geometry d_LR = sqrt(gap^2 + (dx s)^2); toolkit.trapezoid on n samples"),
    "design_phase": ("derived", "entangling_phase(inputs.DESIGN_A_*) at casimir.casimir_safe_gap(inputs."
                                "GAP_BASELINE_MASS, _DX, _TAU, GAP_FRACTION), all read at call time"),
}

ETA = (-1, 1, 1, 1)          # diagonal of the Minkowski metric (signature postulate, SPEC 5)


# ------------------------------------------------------------------------------------------
# 1. linearized point mass
# ------------------------------------------------------------------------------------------
def point_mass_metric():
    """(h00, hii) in units GM/(c^2 r), from hbar00 solving Poisson and trace reversal."""
    eta = [Fraction(e) for e in ETA]
    # lap hbar00 = -16 pi G M delta^3 ; lap (1/(4 pi r)) = -delta^3  ->  hbar00 = 16 pi * 1/(4 pi) GM/r
    hbar00 = Fraction(16) * Fraction(1, 4)                       # the two 4 pi's cancel exactly
    hbar = [hbar00, Fraction(0), Fraction(0), Fraction(0)]       # hbar_{mu mu}, diagonal
    trace = sum(eta[mu] * hbar[mu] for mu in range(4))           # eta^{mu mu} = eta_{mu mu} for diag(+-1)
    h = [hbar[mu] - Fraction(1, 2) * eta[mu] * trace for mu in range(4)]
    return h[0], h[1]


# ------------------------------------------------------------------------------------------
# 2. one-graviton exchange contraction
# ------------------------------------------------------------------------------------------
def _trace(T):
    return sum(Fraction(ETA[mu]) * Fraction(T[mu]) for mu in range(4))


def tpt(T1, T2):
    """T2^{mu nu} P_{mu nu rho sigma} T1^{rho sigma} for diagonal T = (T00, T11, T22, T33)."""
    a = [Fraction(x) for x in T1]
    b = [Fraction(x) for x in T2]
    # eta_{mu rho} eta_{nu sigma} T2^{mu nu} T1^{rho sigma} = sum_mu eta_mumu^2 b_mu a_mu (twice, by symmetry)
    direct = sum(Fraction(ETA[mu] * ETA[mu]) * a[mu] * b[mu] for mu in range(4))
    return Fraction(1, 2) * (direct + direct - _trace(a) * _trace(b))


def _tpt_full(T1, T2):
    """Second route: build P_{mu nu rho sigma} as an explicit tensor and do the full sum."""
    eta = [[Fraction(ETA[i]) if i == j else Fraction(0) for j in range(4)] for i in range(4)]
    t1 = [[Fraction(T1[i]) if i == j else Fraction(0) for j in range(4)] for i in range(4)]
    t2 = [[Fraction(T2[i]) if i == j else Fraction(0) for j in range(4)] for i in range(4)]
    tot = Fraction(0)
    r4 = range(4)
    for m_ in r4:
        for n_ in r4:
            if not t2[m_][n_]:
                continue
            for r_ in r4:
                for s_ in r4:
                    if not t1[r_][s_]:
                        continue
                    P = Fraction(1, 2) * (eta[m_][r_] * eta[n_][s_] + eta[m_][s_] * eta[n_][r_]
                                          - eta[m_][n_] * eta[r_][s_])
                    tot += t2[m_][n_] * P * t1[r_][s_]
    return tot


# ------------------------------------------------------------------------------------------
# 3. branch-opening profile
# ------------------------------------------------------------------------------------------
def _up(x):
    x = min(max(x, 0.0), 1.0)
    if x < 0.5:
        return 2 * x * x
    return 1 - 2 * (1 - x) * (1 - x)


def ramp_profile(t, hold, ramp):
    """s(t) in [0, 1]: up(t/ramp), then 1 for the hold, then up((T - t)/ramp), T = hold + 2 ramp."""
    T = hold + 2 * ramp
    if t < ramp:
        return _up(t / ramp)
    if t <= ramp + hold:
        return 1.0
    return _up((T - t) / ramp)


# ------------------------------------------------------------------------------------------
# 4. entangling phase
# ------------------------------------------------------------------------------------------
def _potential(m1, m2):
    """U(r) = -8 pi G tpt(T_m, T_m) m1 m2 chiral.yukawa(r, 0): the m = 0 exchange transform of
    the one-graviton amplitude -8 pi G T2.P.T1 / q^2 (see DERIVATION section 3)."""
    G = inputs.G_NEWTON
    coupling = float(tpt((1, 0, 0, 0), (1, 0, 0, 0)))          # = 1/2 for static masses
    pref = -8 * math.pi * G * coupling * m1 * m2

    def U(r):
        return pref * chiral.yukawa(r, 0)
    return U


def entangling_phase(m, dx, hold, ramp, gap, n=4001):
    """Delta phi = phi_LL + phi_RR - phi_LR - phi_RL (rad), parallel geometry, trapezoid on n samples."""
    U = _potential(m, m)
    T = hold + 2 * ramp
    dt = T / (n - 1)
    U_near = U(gap)
    ws = []
    for k in range(n):
        sep = dx * ramp_profile(T * k / (n - 1), hold, ramp)      # 2 y(t) = dx s(t)
        d_far = math.sqrt(gap * gap + sep * sep)
        U_far = U(d_far)
        ws.append(-U_near - U_near + U_far + U_far)              # -U_LL - U_RR + U_LR + U_RL
    return toolkit.trapezoid(ws, dt) / inputs.HBAR


def design_phase():
    """Design A's phase at the Casimir-safe gap of the baseline (rung 3 -> 4)."""
    gap = casimir.casimir_safe_gap(inputs.GAP_BASELINE_MASS, inputs.GAP_BASELINE_DX,
                                   inputs.GAP_BASELINE_TAU, inputs.GAP_FRACTION)
    return entangling_phase(inputs.DESIGN_A_MASS, inputs.DESIGN_A_DX, inputs.DESIGN_A_HOLD,
                            inputs.DESIGN_A_RAMP, gap)


# ------------------------------------------------------------------------------------------
# second routes (self-check only)
# ------------------------------------------------------------------------------------------
def _phase_piecewise(m, dx, hold, ramp, gap, N=2000):
    """Hold exact + ramps on the smooth pieces of up (x in [0,1/2], [1/2,1]) by Richardson-
    extrapolated toolkit.trapezoid (composite Simpson); both ramps equal by s(T-t) = s(t)."""
    G, hb = inputs.G_NEWTON, inputs.HBAR

    def f(a):
        return 1 / gap - 1 / math.sqrt(gap * gap + a * a)

    def piece(lo, hi, N):
        h = (hi - lo) / N
        return toolkit.trapezoid([f(dx * _up(lo + h * k)) for k in range(N + 1)], h)

    def ramp_int(N):
        return piece(0.0, 0.5, N) + piece(0.5, 1.0, N)
    I = (4 * ramp_int(2 * N) - ramp_int(N)) / 3
    return 2 * G * m * m / hb * (hold * f(dx) + 2 * ramp * I)


def _poly_int01_up2():
    """Int_0^1 up(x)^2 dx exactly, by polynomial integration in Fractions."""
    def integ(coefs, a, b):           # coefs[k] x^k
        return sum(c * (b ** (k + 1) - a ** (k + 1)) / (k + 1) for k, c in enumerate(coefs))
    half = Fraction(1, 2)
    first = integ([0, 0, 0, 0, Fraction(4)], Fraction(0), half)                 # (2x^2)^2
    # 1 - 2(1-x)^2 = -1 + 4x - 2x^2 ; squared:
    p = [Fraction(-1), Fraction(4), Fraction(-2)]
    sq = [Fraction(0)] * 5
    for i, a in enumerate(p):
        for j, b in enumerate(p):
            sq[i + j] += a * b
    second = integ(sq, half, Fraction(1))
    return first + second


if __name__ == "__main__":
    print("== point_mass_metric ==")
    h00, hii = point_mass_metric()
    P_T1 = [Fraction(ETA[mu]) ** 2 * Fraction(t) - Fraction(1, 2) * Fraction(ETA[mu]) * _trace((1, 0, 0, 0))
            for mu, t in enumerate((1, 0, 0, 0))]
    print(f" trace reversal: h00 = {h00}, hii = {hii}, gamma = {hii / h00}")
    print(f" second route (16 pi P.T1 / 4 pi): {[4 * x for x in P_T1]}")

    print("== tpt ==")
    Tm, Tph = (1, 0, 0, 0), (1, 0, 0, 1)
    print(f" mass-mass {tpt(Tm, Tm)} (full tensor {_tpt_full(Tm, Tm)}),"
          f" mass-photon {tpt(Tm, Tph)} (full {_tpt_full(Tm, Tph)}), ratio {tpt(Tm, Tph) / tpt(Tm, Tm)}")
    print(f" metric route (h00 + hii)/h00 = 1 + gamma = {(h00 + hii) / h00}")
    import random
    rng = random.Random(7)
    ok = True
    for _ in range(50):
        A = tuple(Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(4))
        B = tuple(Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(4))
        ok &= tpt(A, B) == _tpt_full(A, B) == tpt(B, A)
    print(f" closed form == full contraction == symmetric for 50 random pairs: {ok}")
    print(f" U coefficient -8 pi tpt = -4 pi: {-8 * float(tpt(Tm, Tm))} pi;"
          f" -4 pi yukawa(2, 0) * 2 = {-4 * math.pi * chiral.yukawa(2.0, 0) * 2} (Newton: -1)")

    print("== ramp_profile ==")
    hold, ramp = 1.0, 2.0
    T = hold + 2 * ramp
    sym = max(abs(ramp_profile(t, hold, ramp) - ramp_profile(T - t, hold, ramp))
              for t in [T * k / 997 for k in range(998)])
    nn = 2 * 10000 + 1
    I = toolkit.trapezoid([_up(k / (nn - 1)) for k in range(nn)], 1 / (nn - 1))
    print(f" max |s(t) - s(T-t)| = {sym:.1e}; int_0^1 up = {I:.12f} (exact 1/2)")

    print("== entangling_phase ==")
    args = (1e-14, 5e-4, 0.1, 1.0, 2e-4)
    print(f" probe {args}: trapezoid {entangling_phase(*args):.12e}, piecewise Simpson {_phase_piecewise(*args):.12e}")
    c = _poly_int01_up2()
    m_, dx_, ho, ra, g_ = 1e-14, 1e-7, 0.1, 1.0, 2e-4
    lim = inputs.G_NEWTON * m_ ** 2 * dx_ ** 2 / (inputs.HBAR * g_ ** 3) * (ho + 2 * ra * float(c))
    print(f" small-dx limit: int up^2 = {c}; limit {lim:.10e}, piecewise {_phase_piecewise(m_, dx_, ho, ra, g_):.10e},"
          f" trapezoid {entangling_phase(m_, dx_, ho, ra, g_):.10e}")

    print("== design_phase ==")
    gap = casimir.casimir_safe_gap(inputs.GAP_BASELINE_MASS, inputs.GAP_BASELINE_DX,
                                   inputs.GAP_BASELINE_TAU, inputs.GAP_FRACTION)
    dA = (inputs.DESIGN_A_MASS, inputs.DESIGN_A_DX, inputs.DESIGN_A_HOLD, inputs.DESIGN_A_RAMP, gap)
    ref = _phase_piecewise(*dA)
    print(f" casimir-safe gap = {gap!r} m")
    print(f" design_phase() = {design_phase()!r} rad")
    print(f" piecewise Simpson second route = {ref!r} rad")
    print(" convergence of entangling_phase in n (design A at the safe gap):")
    print(f"   {'n':>7} {'phase (rad)':>22} {'rel diff to Simpson':>20}")
    for n in sorted({100 * 4 ** k + 1 for k in range(5)} | {1000 + 1, 4000 + 1}):
        p = entangling_phase(*dA, n=n)
        print(f"   {n:>7} {p:>22.15e} {abs(p - ref) / ref:>20.3e}")
