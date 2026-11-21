"""Campaign: gauge-parameter independence of the whole bosonic one-loop Delta r (general R_xi), no provided module (SPEC.md)."""
import math

NAME = "dr_xi"
MODULE = "dr_xi"
ALLOWED_IMPORTS = {"math", "cmath", "fractions", "itertools", "functools", "numpy", "scipy", "mpmath", "sympy"}
QUOTED_ALLOWED = []
EXPORTS = {
    "delta_r_se": "delta_r_se(MW, MZ, MH, alpha, xi, mu) -> float: class SE of the bosonic one-loop Delta r (SPEC section 2), MS-bar at mu.",
    "delta_r_vbw": "delta_r_vbw(MW, MZ, alpha, xi, mu) -> float: class VBW (vertex + box + lepton wave function + Fermi subtraction), MS-bar at mu.",
    "delta_r_bos_xi": "delta_r_bos_xi(MW, MZ, MH, alpha, xi) -> float: the total bosonic one-loop Delta r in R_xi gauge (no mu, no xi dependence).",
}
MW, MZ, MH, ALPHA = 80.38, 91.19, 125.0, 1 / 128.0
XIS = (0.0, 0.3, 1.0, 4.0, 25.0)


def b_alpha_linear(m):
    a, b = m.delta_r_bos_xi(MW, MZ, MH, ALPHA, 0.5), m.delta_r_bos_xi(MW, MZ, MH, 2 * ALPHA, 0.5)
    a2, b2 = m.delta_r_vbw(MW, MZ, ALPHA, 0.5, MW), m.delta_r_vbw(MW, MZ, 2 * ALPHA, 0.5, MW)
    return abs(b / a - 2) < 1e-9 and abs(b2 / a2 - 2) < 1e-9, f"first order in alpha: total ratio {b / a:.9f}, VBW ratio {b2 / a2:.9f}"


def b_total_xi_independent(m):
    worst = 0.0
    for p in ((MW, MZ, MH, ALPHA), (75.0, 91.19, 300.0, 1 / 130.0)):
        v = [m.delta_r_bos_xi(*p, xi) for xi in XIS + (1e3,)]
        worst = max(worst, (max(v) - min(v)) / abs(v[2]))
    return worst < 1e-9, f"relative spread of the total over xi = 0, 0.3, 1, 4, 25, 1000: {worst:.1e}"


def b_parts_sum_and_mu(m):
    worst = 0.0
    for xi in (0.0, 1.0, 7.0):
        for mu in (30.0, MW, 900.0):
            tot = m.delta_r_se(MW, MZ, MH, ALPHA, xi, mu) + m.delta_r_vbw(MW, MZ, ALPHA, xi, mu)
            worst = max(worst, abs(tot / m.delta_r_bos_xi(MW, MZ, MH, ALPHA, xi) - 1))
    return worst < 1e-9, f"SE + VBW equals the total, any mu, any xi (mu independence of the sum): {worst:.1e}"


def b_higgs_slope(m):
    s2 = 1 - (MW / MZ) ** 2
    B = 11 * ALPHA / (48 * math.pi * s2)
    out = 0.0
    for xi in (0.0, 1.0, 9.0):
        f = lambda mh: m.delta_r_bos_xi(MW, MZ, mh, ALPHA, xi)
        h1, h2 = 1e5 * MW, 1e6 * MW
        out = max(out, abs((f(h2) - f(h1)) / math.log(h2**2 / h1**2) / B - 1))
    return out < 1e-4, f"d Delta r / d ln MH^2 at large MH (11 alpha / 48 pi s^2), every xi: deviation {out:.1e}"


def b_parts_depend_on_xi(m):
    a, b = m.delta_r_se(MW, MZ, MH, ALPHA, 0.0, MW), m.delta_r_se(MW, MZ, MH, ALPHA, 1.0, MW)
    c, d = m.delta_r_vbw(MW, MZ, ALPHA, 0.0, MW), m.delta_r_vbw(MW, MZ, ALPHA, 1.0, MW)
    return abs(a - b) > 1e-8 and abs(c - d) > 1e-8 and abs((a - b) + (c - d)) < 1e-10 * abs(b), f"class SE changes by {a - b:.3e} and VBW by {c - d:.3e} between xi = 0 and 1 (they must differ, and cancel in the sum)"


BLIND = [
    ("first order in alpha", b_alpha_linear),
    ("the total is independent of xi (0 ... 1000)", b_total_xi_independent),
    ("SE + VBW = total at every mu and xi", b_parts_sum_and_mu),
    ("large-MH slope 11 alpha / 48 pi s^2 in every xi", b_higgs_slope),
    ("the classes depend on xi and compensate", b_parts_depend_on_xi),
]
