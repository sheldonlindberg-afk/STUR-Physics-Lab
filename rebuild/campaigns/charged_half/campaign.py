"""Campaign: emission of a charged massless spin-1/2 particle from a Schwarzschild hole with fluctuating charge (SPEC.md)."""
import math

NAME = "charged_half"
MODULE = "charged_half"
ALLOWED_IMPORTS = {"math", "cmath", "fractions", "itertools", "functools", "numpy", "scipy", "mpmath"}
QUOTED_ALLOWED = []
EXPORTS = {
    "transmission": "transmission(j, w, g) -> float: Gamma_j(w; g) of SPEC section 2 (j = 1/2, 3/2, ...; w in 1/M; any real g, any real w > 0).",
    "rates": "rates(g_gb, g_mu) -> (N, P): the number rate and the power per helicity state of SPEC section 3, with the grey-body coupling g_gb and the chemical-potential coupling g_mu.",
    "charge_distribution": "charge_distribution(alpha, rule=('after', 'after')) -> dict {n: pi(n)}: the stationary distribution of the charge process (SPEC sections 3-4), tails below 1e-14 dropped.",
    "weight_ratio": "weight_ratio(alpha, rule=('after', 'after')) -> float: <P> / P(0) (SPEC section 4).",
    "energy_ratio": "energy_ratio(alpha, rule=('after', 'after')) -> float: (<P>/<N>) / (P(0)/N(0)) (SPEC section 4).",
}
ALPHA = 1 / 137.035999084


def b_range(m):
    vals = [m.transmission(j, w, g) for g in (-0.1, -0.02, 0.0, 0.02, 0.1) for j, w in ((0.5, 0.05), (0.5, 0.3), (1.5, 0.2), (2.5, 0.6), (4.5, 1.0))]
    return all(0.0 <= v <= 1.0 + 1e-9 for v in vals), f"Gamma over g = -0.1..0.1, five (j, w): min {min(vals):.3g}, max {max(vals):.9g}"


def b_low_slope(m):
    out, ok = [], True
    for j, want in ((0.5, 2), (1.5, 4)):
        a, b = m.transmission(j, 0.01, 0.0), m.transmission(j, 0.02, 0.0)
        s = math.log(b / a) / math.log(2)
        out.append(f"j = {j}: {s:.2f}")
        ok &= abs(s - want) < 0.25
    return ok, "g = 0 low-frequency slopes d ln Gamma / d ln w (neutral massless Dirac, expected 2j + 1): " + ", ".join(out)


def b_high_frequency(m):
    v = [m.transmission(j, 1.5, g) for j in (0.5, 1.5) for g in (-0.1, 0.0, 0.1)]
    return min(v) > 0.999, f"Gamma at w = 1.5 for j = 1/2, 3/2 and g = -0.1, 0, 0.1: min {min(v):.6f}"


def b_neutral_power(m):
    N0, P0 = m.rates(0.0, 0.0)
    return 3.9e-5 < P0 < 4.3e-5 and 2.2e-4 < N0 < 2.7e-4, f"neutral massless Dirac, per helicity state: N = {N0:.5e}, P = {P0:.5e}"


def b_rates_monotone(m):
    """With the chemical potential g/2 (all else fixed) the occupation, hence the number rate, increases with g_mu."""
    v = [m.rates(0.0, g)[0] for g in (-0.1, -0.05, 0.0, 0.05, 0.1)]
    return all(v[i] < v[i + 1] for i in range(4)), f"N(0, g_mu) increases with g_mu: {v}"


def b_distribution(m):
    pi = m.charge_distribution(ALPHA)
    s = sum(pi.values())
    sym = max(abs(pi[n] - pi.get(-n, -1)) for n in pi)
    dec = all(pi[n + 1] <= pi[n] * (1 + 1e-12) for n in pi if n >= 0 and n + 1 in pi)
    return abs(s - 1) < 1e-9 and sym < 1e-10 and dec, f"sum = {s:.12f}; max |pi(n) - pi(-n)| = {sym:.1e}; pi non-increasing for n >= 0: {dec}"


def b_detailed_balance(m):
    """The stated process: pi(n+1) down(n+1) = pi(n) up(n) with up(n) = N(electron at n), down(n) = N(positron at n), rule ('before', 'before'): couplings -alpha n and +alpha n."""
    pi = m.charge_distribution(ALPHA, ("before", "before"))
    worst = 0.0
    for n in range(0, 8):
        up = m.rates(-ALPHA * n, -ALPHA * n)[0]
        dn = m.rates(ALPHA * (n + 1), ALPHA * (n + 1))[0]
        worst = max(worst, abs(pi[n + 1] / pi[n] / (up / dn) - 1))
    return worst < 1e-6, f"pi(n+1)/pi(n) against up(n)/down(n+1) from rates(), rule ('before', 'before'), n = 0..7: {worst:.1e}"


def b_weak_coupling(m):
    far = abs(m.weight_ratio(0.25 * ALPHA) - 1)
    near = abs(m.weight_ratio(ALPHA) - 1)
    return far < near, f"|ratio - 1| shrinks as alpha -> 0: {far:.4f} at alpha/4, {near:.4f} at alpha"


def b_neutral_limit_rates(m):
    N0, P0 = m.rates(0.0, 0.0)
    N1, P1 = m.rates(1e-9, 1e-9)
    return abs(N1 / N0 - 1) < 1e-6 and abs(P1 / P0 - 1) < 1e-6, f"rates continuous at g -> 0: {abs(N1 / N0 - 1):.1e}, {abs(P1 / P0 - 1):.1e}"


BLIND = [
    ("Gamma in [0, 1] for either sign of g", b_range),
    ("neutral low-frequency slopes 2j + 1", b_low_slope),
    ("Gamma -> 1 at high frequency", b_high_frequency),
    ("neutral massless Dirac power and number rate are of the expected size", b_neutral_power),
    ("the number rate increases with the chemical-potential coupling", b_rates_monotone),
    ("the stationary distribution is normalized, symmetric and bell-shaped", b_distribution),
    ("detailed balance of the birth-death chain with the exported rates", b_detailed_balance),
    ("the effect of the charge vanishes as alpha -> 0", b_weak_coupling),
    ("the rates are continuous at g -> 0", b_neutral_limit_rates),
]
