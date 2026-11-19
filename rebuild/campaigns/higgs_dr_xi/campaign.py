"""Campaign: gauge-parameter dependence of the Higgs part of Delta r at one loop (SPEC.md)."""
import math

NAME = "higgs_dr_xi"
MODULE = "higgs_dr_xi"
ALLOWED_IMPORTS = {"math", "cmath", "fractions", "itertools", "functools", "numpy", "scipy", "mpmath", "sympy"}
QUOTED_ALLOWED = []
EXPORTS = {
    "sigma_W": "sigma_W(q2, mH, MW, MZ, alpha, xi, mu) -> float: MS-bar g^{mu nu} coefficient Pi_WW(q^2) from Higgs-containing diagrams in R_xi gauge (SPEC section 2).",
    "sigma_Z": "sigma_Z(q2, mH, MW, MZ, alpha, xi, mu) -> float: the same for Pi_ZZ(q^2).",
    "delta_r_higgs_rel": "delta_r_higgs_rel(mH, MW, MZ, alpha, xi, mu) -> float: Delta r_H(mH) - Delta r_H(mH = MW), dimensionless (SPEC section 3).",
    "log_coefficient": "log_coefficient(MW, MZ, alpha, xi) -> float: lim [Delta r_H(mH) - Delta r_H(MW)] / ln(mH^2/MW^2) as mH -> infinity.",
}
MW, MZ, ALPHA = 80.38, 91.19, 1 / 128.0
XIS = (0.0, 0.3, 1.0, 4.0, 25.0)


def b_reference_zero(m):
    v = [m.delta_r_higgs_rel(MW, MW, MZ, ALPHA, xi, MW) for xi in XIS]
    return max(abs(x) for x in v) < 1e-13, f"delta_r_higgs_rel at mH = MW for xi = {XIS}: {v}"


def b_mu_independent(m):
    worst = 0.0
    for mh in (50.0, 125.2, 400.0, 1500.0):
        for xi in (0.0, 1.0, 4.0):
            a = m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, xi, MW)
            b = m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, xi, 3.7 * MW)
            worst = max(worst, abs(b - a) / max(abs(a), 1e-30))
    return worst < 1e-9, f"change of delta_r_higgs_rel when the MS-bar scale moves from MW to 3.7 MW: {worst:.1e}"


def b_alpha_linear(m):
    a = m.delta_r_higgs_rel(250.0, MW, MZ, ALPHA, 2.0, MW)
    b = m.delta_r_higgs_rel(250.0, MW, MZ, 2 * ALPHA, 2.0, MW)
    return abs(b / a - 2) < 1e-9, f"first order in alpha: ratio {b / a:.9f}"


def b_pi_mu_linear_in_q2(m):
    worst = 0.0
    for xi in (0.0, 1.0, 4.0):
        for f in (m.sigma_W, m.sigma_Z):
            d = lambda q2: f(q2, 300.0, MW, MZ, ALPHA, xi, 2.5 * MW) - f(q2, 300.0, MW, MZ, ALPHA, xi, MW)
            x = (0.0, 0.5 * MW**2, MW**2)
            worst = max(worst, abs(d(x[2]) - 2 * d(x[1]) + d(x[0])) / max(abs(d(x[2])), 1e-30))
    return worst < 1e-9, f"second difference of the mu-dependence of Pi(q^2) at three equally spaced q^2 (xi = 0, 1, 4): {worst:.1e}"


def b_slope_matches_coefficient(m):
    worst = 0.0
    for xi in (0.0, 1.0, 4.0):
        B = m.log_coefficient(MW, MZ, ALPHA, xi)
        f = lambda mh: m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, xi, MW)
        h1, h2 = 1e5 * MW, 1e6 * MW
        slope = (f(h2) - f(h1)) / math.log((h2 / MW) ** 2 / (h1 / MW) ** 2)
        worst = max(worst, abs(slope / B - 1))
    return worst < 1e-4, f"measured large-mH slope against log_coefficient, xi = 0, 1, 4: {worst:.1e}"


def b_alpha_sigma(m):
    worst = 0.0
    for xi in (0.0, 2.0):
        for f in (m.sigma_W, m.sigma_Z):
            for q2 in (0.0, MW**2, -2.0 * MW**2):
                a, b = f(q2, 300.0, MW, MZ, ALPHA, xi, MW), f(q2, 300.0, MW, MZ, 3 * ALPHA, xi, MW)
                worst = max(worst, abs(b / a / 3 - 1))
    return worst < 1e-12, f"sigma(3 alpha)/(3 sigma(alpha)) - 1: {worst:.1e}"


def b_q2_continuity(m):
    worst = 0.0
    for xi in (0.0, 1.0, 4.0):
        for f in (m.sigma_W, m.sigma_Z):
            a, b = f(0.0, 200.0, MW, MZ, ALPHA, xi, MW), f(1e-6, 200.0, MW, MZ, ALPHA, xi, MW)
            worst = max(worst, abs(b - a) / max(abs(a), 1e-30))
    return worst < 1e-6, f"Pi(q^2 = 1e-6) vs Pi(0): {worst:.1e}"


def b_report_xi(m):
    """Information, not a physics claim: the spread of delta_r_higgs_rel over xi. The campaign's question is whether it vanishes; a build that finds a
    dependence must say so in DERIVATION.md rather than force it away."""
    vals = [m.delta_r_higgs_rel(300.0, MW, MZ, ALPHA, xi, MW) for xi in XIS]
    spread = (max(vals) - min(vals)) / abs(vals[2])
    return True, f"delta_r_higgs_rel(300 GeV) over xi = {XIS}: relative spread {spread:.1e} (reported, not judged here)"


BLIND = [
    ("delta_r_higgs_rel vanishes at the reference mass, any xi", b_reference_zero),
    ("delta_r_higgs_rel does not depend on the MS-bar scale", b_mu_independent),
    ("delta_r_higgs_rel is linear in alpha", b_alpha_linear),
    ("mu-dependence of the raw self-energies is linear in q^2", b_pi_mu_linear_in_q2),
    ("the large-mH slope equals log_coefficient", b_slope_matches_coefficient),
    ("self-energies are proportional to alpha", b_alpha_sigma),
    ("self-energies are continuous at q^2 -> 0", b_q2_continuity),
    ("the xi spread of delta_r_higgs_rel is reported", b_report_xi),
]
