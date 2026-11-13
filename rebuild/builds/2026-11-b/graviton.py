"""Stage `graviton` (build 2026-11-b): linearized gravity, from the field equation to the diamond experiment.

The point-mass metric, the one-graviton-exchange contraction T2.P.T1, the static exchange potential (rung 2's
exchange transform at m = 0), the branch-opening profile and the gravitational entangling phase. Derivations
and second routes: DERIVATION_graviton.md (same directory); section numbers are cited below.
Signature eta = diag(-1, 1, 1, 1). SI units for the phase.
"""
import math
from fractions import Fraction

import inputs
import toolkit
import chiral
import casimir

PROVENANCE = {
    "point_mass_metric": ("derived", "static point mass in box hbar_mn = -16 pi G T_mn: hbar_00 = 16 pi G M Y(r),"
                                     " Y = 1/(4 pi r) the Green function of -laplacian, so hbar_00 = 4 GM/r; then"
                                     " h = hbar - eta hbar/2 (trace reversal is its own inverse in 4D), all in"
                                     " Fractions (DERIVATION section 1)"),
    "tpt": ("derived", "explicit four-index contraction T2^mn P_mnrs T1^rs with P = (eta eta + eta eta - eta eta)/2"
                       " built from eta = diag(-1,1,1,1); equals sum T2 T1 - tr T2 tr T1/2 (section 2)"),
    "ramp_profile": ("derived", "SPEC section 5 profile: up(clamp(t/ramp)), 1 in the hold, up(clamp((T-t)/ramp)),"
                                " up(x) = 2x^2 or 1 - 2(1-x)^2 (section 4); a postulate, implemented verbatim"),
    "entangling_phase": ("derived", "U(r) = -(1/2)(16 pi G) (T2.P.T1) chiral.yukawa(r, 0) from the coupling h T/2 and"
                                    " the field equation (= -G m^2/r for masses at rest); Delta phi ="
                                    " (1/hbar) int [-2U(gap) + 2U(sqrt(gap^2 + (2y)^2))] dt by toolkit.trapezoid on"
                                    " n samples (sections 3, 5)"),
    "design_phase": ("derived", "entangling_phase at inputs.DESIGN_A_* and the gap from casimir.casimir_safe_gap"
                                " for inputs.GAP_BASELINE_*, GAP_FRACTION (section 6)"),
}

# ------------------------------------------------------------------------------------------
# postulated structure (SPEC section 5): the metric, the field equation, the coupling
# ------------------------------------------------------------------------------------------
_DIM = 4
_FIELD_EQ = Fraction(16)          # box hbar_mn = -(16) pi G T_mn: coefficient in units of pi G
_GREEN = Fraction(1, 4)           # lap Y = -delta^3  =>  Y = (1/4)/(pi r): coefficient in units of 1/pi
_COUPLING = Fraction(1, 2)        # L_int = (1/2) h_mn T^mn


def _eta(mu, nu):
    """Minkowski metric diag(-1, 1, 1, 1) (identical with upper or lower indices)."""
    if mu != nu:
        return Fraction(0)
    return Fraction(-1) if mu == 0 else Fraction(1)


def _P(mu, nu, rho, sigma):
    """P_mnrs = (eta_mr eta_ns + eta_ms eta_nr - eta_mn eta_rs)/2."""
    return (_eta(mu, rho) * _eta(nu, sigma) + _eta(mu, sigma) * _eta(nu, rho)
            - _eta(mu, nu) * _eta(rho, sigma)) / 2


def _exact(x):
    """Ints become Fractions (so exact inputs give exact outputs); other numbers pass through."""
    return Fraction(x) if isinstance(x, int) else x


# ------------------------------------------------------------------------------------------
# 1. the linearized metric of a point mass
# ------------------------------------------------------------------------------------------
def point_mass_metric():
    """(h00, hii) in units of GM/(c^2 r) for a static point mass (DERIVATION section 1)."""
    # hbar_mn = 16 pi G Y(r) tau_mn with tau_mn = M delta_m0 delta_n0 (lower indices: eta_00^2 = 1)
    hbar = [[_FIELD_EQ * _GREEN if mu == nu == 0 else Fraction(0) for nu in range(_DIM)] for mu in range(_DIM)]
    trace = sum(_eta(mu, nu) * hbar[mu][nu] for mu in range(_DIM) for nu in range(_DIM))
    h = [[hbar[mu][nu] - _eta(mu, nu) * trace / 2 for nu in range(_DIM)] for mu in range(_DIM)]
    if not (h[1][1] == h[2][2] == h[3][3]):
        raise ArithmeticError("spatial metric perturbation is not isotropic")
    return h[0][0], h[1][1]


# ------------------------------------------------------------------------------------------
# 2. the one-graviton-exchange contraction
# ------------------------------------------------------------------------------------------
def tpt(T1, T2):
    """T2^mn P_mnrs T1^rs for diagonal stress tensors (T^00, T^11, T^22, T^33) (DERIVATION section 2)."""
    a = [_exact(x) for x in T1]
    b = [_exact(x) for x in T2]
    total = Fraction(0)
    for mu in range(_DIM):              # T2^{mu mu}: diagonal, so nu = mu
        for rho in range(_DIM):         # T1^{rho rho}: diagonal, so sigma = rho
            total = total + b[mu] * _P(mu, mu, rho, rho) * a[rho]
    return total


# ------------------------------------------------------------------------------------------
# 3. the static exchange potential
# ------------------------------------------------------------------------------------------
def _exchange_energy(m1, m2, r):
    """U(r) = -(1/2)(16 pi G)(T2.P.T1) Y(r), Y = chiral.yukawa(r, 0), two masses at rest (section 3), in J."""
    rest = (Fraction(1), 0, 0, 0)                       # T^mn / (m c^2) of a mass at rest
    strength = float(_COUPLING * _FIELD_EQ * tpt(rest, rest)) * math.pi * inputs.G_NEWTON * m1 * m2
    return -strength * chiral.yukawa(r, 0)


# ------------------------------------------------------------------------------------------
# 4. the branch profile
# ------------------------------------------------------------------------------------------
def _up(x):
    x = min(1, max(0, x))
    if 2 * x < 1:
        return 2 * x * x
    return 1 - 2 * (1 - x) * (1 - x)


def ramp_profile(t, hold, ramp):
    """s(t) in [0, 1]: smooth opening over `ramp`, 1 for `hold`, smooth closing over `ramp` (section 4)."""
    total = hold + 2 * ramp
    if ramp <= 0:                                       # no ramp: the limit of the profile
        return 1 if 0 <= t <= total else 0
    if t < ramp:
        return _up(t / ramp)
    if t <= ramp + hold:
        return 1
    return _up((total - t) / ramp)


# ------------------------------------------------------------------------------------------
# 5. the entangling phase
# ------------------------------------------------------------------------------------------
def entangling_phase(m, dx, hold, ramp, gap, n=4001):
    """Delta phi = phi_LL + phi_RR - phi_LR - phi_RL in rad, parallel geometry (DERIVATION section 5)."""
    total = hold + 2 * ramp
    step = total / (n - 1)
    u_same = _exchange_energy(m, m, gap)                # d_LL = d_RR = gap at all times
    samples = []
    for i in range(n):
        y = dx / 2 * ramp_profile(total * i / (n - 1), hold, ramp)
        d_cross = math.sqrt(gap * gap + (2 * y) * (2 * y))
        samples.append(-2 * u_same + 2 * _exchange_energy(m, m, d_cross))
    return toolkit.trapezoid(samples, step) / inputs.HBAR


def design_phase():
    """Design A's phase at the Casimir-safe gap of the baseline (DERIVATION section 6)."""
    gap = casimir.casimir_safe_gap(inputs.GAP_BASELINE_MASS, inputs.GAP_BASELINE_DX,
                                   inputs.GAP_BASELINE_TAU, inputs.GAP_FRACTION)
    return entangling_phase(inputs.DESIGN_A_MASS, inputs.DESIGN_A_DX, inputs.DESIGN_A_HOLD,
                            inputs.DESIGN_A_RAMP, gap)


# ------------------------------------------------------------------------------------------
# second routes (self-check only; not used by the exports)
# ------------------------------------------------------------------------------------------
def _tpt_closed(T1, T2):
    """sum_m T2^mm T1^mm - tr T2 tr T1 / 2, tr T = -T^00 + T^11 + T^22 + T^33."""
    tr = lambda T: -T[0] + T[1] + T[2] + T[3]
    return sum(Fraction(x) * Fraction(y) for x, y in zip(T1, T2)) - Fraction(tr(T1)) * Fraction(tr(T2)) / 2


def _metric_from_P():
    """h_mn = 16 pi G Y (P tau)_mn, eq. (A): the metric from the propagator numerator instead of trace reversal."""
    lower = lambda mu: sum(_P(mu, mu, rho, rho) * (1 if rho == 0 else 0) for rho in range(_DIM))
    return _FIELD_EQ * _GREEN * lower(0), _FIELD_EQ * _GREEN * lower(1)


def _simpson(f, a, b, n):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def _phase_simpson(m, dx, hold, ramp, gap, n=2000):
    """Explicit 1/r integrand, composite Simpson on each smooth piece (kinks of s'' at the half-ramps)."""
    f = lambda t: 2 * (1 / gap - 1 / math.sqrt(gap * gap + (dx * ramp_profile(t, hold, ramp)) ** 2))
    total = hold + 2 * ramp
    cuts = [0, ramp / 2, ramp, ramp + hold, total - ramp / 2, total]
    integral = sum(_simpson(f, a, b, n) for a, b in zip(cuts, cuts[1:]) if b > a)
    return inputs.G_NEWTON * m * m / inputs.HBAR * integral


def _up_squared_integral():
    """int_0^1 up(x)^2 dx exactly: 4x^4 on [0, 1/2] plus (1 - 2u^2)^2 = 1 - 4u^2 + 4u^4 on u in [0, 1/2]."""
    half = Fraction(1, 2)
    mono = lambda c, p: c * half ** (p + 1) / (p + 1)   # int_0^(1/2) c x^p dx
    return mono(4, 4) + mono(1, 0) + mono(-4, 2) + mono(4, 4)


if __name__ == "__main__":
    import random

    print("== point_mass_metric ==")
    print("  trace-reversal route (h00, hii):", point_mass_metric())
    print("  propagator route 16 pi G Y P.tau:", _metric_from_P())
    print("  16 pi * yukawa(1, 0) =", 16 * math.pi * chiral.yukawa(1, 0), " (rational bookkeeping:",
          _FIELD_EQ * _GREEN, ")")

    print("== tpt ==")
    rng = random.Random(7)
    worst = 0
    for _ in range(200):
        A = tuple(Fraction(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(4))
        B = tuple(Fraction(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(4))
        worst = max(worst, abs(tpt(A, B) - _tpt_closed(A, B)), abs(tpt(A, B) - tpt(B, A)))
    rest, light = (Fraction(1), 0, 0, 0), (Fraction(1), 0, 0, Fraction(1))
    print("  max |contraction - closed form|, |asymmetry| over 200 random pairs:", worst)
    print("  mass-mass:", tpt(rest, rest), " mass-light:", tpt(rest, light), " ratio:", tpt(rest, light) / tpt(rest, rest))

    print("== exchange potential ==")
    r0, eps = 3.0, 1e-5
    flux = -4 * math.pi * r0 * r0 * (chiral.yukawa(r0 + eps, 0) - chiral.yukawa(r0 - eps, 0)) / (2 * eps)
    print("  Gauss flux of -grad Y (should be 1):", flux)
    print("  U(r) r / (G m1 m2) (should be -1):", _exchange_energy(2.0, 5.0, r0) * r0 / (inputs.G_NEWTON * 10))

    print("== ramp_profile ==")
    hold, ramp = 0.3, 0.7
    T = hold + 2 * ramp
    sym = max(abs(ramp_profile(T * i / 997, hold, ramp) - ramp_profile(T - T * i / 997, hold, ramp)) for i in range(998))
    comp = max(abs(_up(i / 64) + _up(1 - i / 64) - 1) for i in range(65))
    print("  up(0), up(1/2), up(1):", _up(0), _up(Fraction(1, 2)), _up(1), " max|up(x)+up(1-x)-1|:", comp)
    print("  max |s(t) - s(T - t)|:", sym, " s outside [0, T]:", ramp_profile(-1, hold, ramp), ramp_profile(T + 1, hold, ramp))

    print("== entangling_phase ==")
    m, dx, hold, ramp = inputs.DESIGN_A_MASS, inputs.DESIGN_A_DX, inputs.DESIGN_A_HOLD, inputs.DESIGN_A_RAMP
    gap = casimir.casimir_safe_gap(inputs.GAP_BASELINE_MASS, inputs.GAP_BASELINE_DX,
                                   inputs.GAP_BASELINE_TAU, inputs.GAP_FRACTION)
    main = entangling_phase(m, dx, hold, ramp, gap)
    simp = _phase_simpson(m, dx, hold, ramp, gap)
    print("  gap from casimir.casimir_safe_gap:", gap, "m")
    print("  trapezoid n=4001 via yukawa:", main, " Simpson, explicit 1/r:", simp, " rel diff:", abs(main / simp - 1))
    print("  trapezoid convergence n=2001, 4001, 8001:", entangling_phase(m, dx, hold, ramp, gap, 2001), main,
          entangling_phase(m, dx, hold, ramp, gap, 8001))
    pref = inputs.G_NEWTON * m * m / inputs.HBAR
    lim0 = pref * 2 * hold * (1 / gap - 1 / math.sqrt(gap * gap + dx * dx))
    print("  ramp -> 0: ", entangling_phase(m, dx, hold, 0, gap), " closed form:", lim0)
    small = dx / 1000
    I2 = _up_squared_integral()
    lim_small = pref * small * small / gap ** 3 * (hold + 2 * ramp * float(I2))
    print("  dx << gap: ", entangling_phase(m, small, hold, ramp, gap), " closed form with int up^2 =", I2, ":", lim_small)

    print("== design_phase ==")
    print("  design_phase():", design_phase(), "rad   second route (Simpson):", simp, "rad")
