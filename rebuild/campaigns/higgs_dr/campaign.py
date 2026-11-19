"""Campaign: the Higgs-mass dependence of the M_W prediction (Delta r) at one loop, with q^2-dependent self-energies (SPEC.md)."""
import math

NAME = "higgs_dr"
MODULE = "higgs_dr"
ALLOWED_IMPORTS = {"math", "cmath", "fractions", "itertools", "functools", "numpy", "scipy", "mpmath", "sympy"}
QUOTED_ALLOWED = []
EXPORTS = {
    "sigma_W": "sigma_W(q2, mH, MW, MZ, alpha, mu) -> float: MS-bar g^{mu nu} coefficient Pi_WW(q^2) from Higgs-containing diagrams (SPEC section 2).",
    "sigma_Z": "sigma_Z(q2, mH, MW, MZ, alpha, mu) -> float: the same for Pi_ZZ(q^2).",
    "delta_r_higgs_rel": "delta_r_higgs_rel(mH, MW, MZ, alpha, mu) -> float: Delta r_H(mH) - Delta r_H(mH = MW), dimensionless (SPEC section 3).",
    "log_coefficient": "log_coefficient(MW, MZ, alpha) -> float: lim [Delta r_H(mH) - Delta r_H(MW)] / ln(mH^2/MW^2) as mH -> infinity.",
}
MW, MZ, ALPHA = 80.38, 91.19, 1 / 128.0


def b_reference_zero(m):
    v = m.delta_r_higgs_rel(MW, MW, MZ, ALPHA, MW)
    return abs(v) < 1e-14, f"delta_r_higgs_rel at mH = MW: {v:.1e}"


def b_mu_independent(m):
    worst = 0.0
    for mh in (50.0, 125.2, 400.0, 1500.0):
        a = m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, MW)
        b = m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, 3.7 * MW)
        worst = max(worst, abs(b - a) / max(abs(a), 1e-30))
    return worst < 1e-9, f"relative change of delta_r_higgs_rel when the MS-bar scale moves from MW to 3.7 MW (poles and logs must cancel): {worst:.1e}"


def b_alpha_linear(m):
    a = m.delta_r_higgs_rel(250.0, MW, MZ, ALPHA, MW)
    b = m.delta_r_higgs_rel(250.0, MW, MZ, 2 * ALPHA, MW)
    return abs(b / a - 2) < 1e-9, f"first order in alpha at fixed masses: ratio {b / a:.9f}"


def b_self_energy_mu_polynomial(m):
    """The MS-bar scale dependence of Pi(q^2) comes from the UV pole: it is a polynomial of degree one in q^2 (dimensional analysis: dimension 2 and
    at most one power of q^2 multiplies a pole at one loop in a renormalizable theory)."""
    worst = 0.0
    for f in (m.sigma_W, m.sigma_Z):
        d = lambda q2: f(q2, 300.0, MW, MZ, ALPHA, 2.5 * MW) - f(q2, 300.0, MW, MZ, ALPHA, MW)
        x = (0.0, 0.5 * MW**2, MW**2)
        second = d(x[2]) - 2 * d(x[1]) + d(x[0])
        worst = max(worst, abs(second) / max(abs(d(x[2])), 1e-30))
    return worst < 1e-9, f"second difference of the mu-dependence of Pi(q^2) over three equally spaced q^2 (must vanish): {worst:.1e}"


def b_q2_continuity(m):
    worst = 0.0
    for f in (m.sigma_W, m.sigma_Z):
        a, b = f(0.0, 200.0, MW, MZ, ALPHA, MW), f(1e-6, 200.0, MW, MZ, ALPHA, MW)
        worst = max(worst, abs(b - a) / max(abs(a), 1e-30))
    return worst < 1e-6, f"Pi(q^2 = 1e-6 GeV^2) vs Pi(0): {worst:.1e} (finite, smooth below threshold)"


def b_slope_matches_coefficient(m):
    B = m.log_coefficient(MW, MZ, ALPHA)
    f = lambda mh: m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, MW)
    h1, h2 = 1e5 * MW, 1e6 * MW
    slope = (f(h2) - f(h1)) / math.log((h2 / MW) ** 2 / (h1 / MW) ** 2)
    return abs(slope / B - 1) < 1e-4, f"d Delta r / d ln mH^2 at mH ~ 1e5-1e6 MW: {slope:.6e}; log_coefficient {B:.6e}"


def b_sign(m):
    v = [m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, MW) for mh in (125.0, 300.0, 1000.0)]
    return v[0] < v[1] < v[2], f"delta_r_higgs_rel at mH = 125, 300, 1000 GeV is increasing: {v}"


def b_sigma_alpha_linear(m):
    """Pi_V is proportional to alpha at fixed masses (one loop, g^2 = 4 pi alpha/s^2). Kills sigma_* that ignore alpha."""
    worst = 0.0
    for f in (m.sigma_W, m.sigma_Z):
        for q2 in (0.0, MW**2, -2.0 * MW**2):
            a, b = f(q2, 300.0, MW, MZ, ALPHA, MW), f(q2, 300.0, MW, MZ, 3 * ALPHA, MW)
            worst = max(worst, abs(b / a / 3 - 1))
    return worst < 1e-12, f"sigma(3 alpha)/(3 sigma(alpha)) - 1, worst over W, Z and three q^2: {worst:.1e}"


def b_sigma_coupling_scaling(m):
    """At fixed MW the W self-energy depends on MZ only through g^2 = 4 pi alpha/s^2 (the H-W, H-phi+ and seagull loops contain
    no Z); at fixed MZ the Z self-energy depends on MW only through g^2/c^2 = 4 pi alpha/(s^2 c^2). Kills couplings taken from
    module-level defaults instead of the arguments."""
    worst = 0.0
    s2 = lambda w, z: 1 - (w / z) ** 2
    for q2 in (0.0, 0.7 * MW**2, -3.0 * MW**2):
        a, b = m.sigma_W(q2, 250.0, MW, MZ, ALPHA, MW), m.sigma_W(q2, 250.0, MW, 97.0, ALPHA, MW)
        worst = max(worst, abs(b / a / (s2(MW, MZ) / s2(MW, 97.0)) - 1))
        a, b = m.sigma_Z(q2, 250.0, MW, MZ, ALPHA, MW), m.sigma_Z(q2, 250.0, 77.0, MZ, ALPHA, MW)
        sc = lambda w, z: s2(w, z) * (w / z) ** 2
        worst = max(worst, abs(b / a / (sc(MW, MZ) / sc(77.0, MZ)) - 1))
    return worst < 1e-12, f"sigma_W(MZ')/sigma_W(MZ) against s^2/s'^2 and sigma_Z(MW')/sigma_Z(MW) against (s c)^2/(s' c')^2: worst {worst:.1e}"


BLIND = [
    ("delta_r_higgs_rel vanishes at the reference mass", b_reference_zero),
    ("delta_r_higgs_rel does not depend on the MS-bar scale", b_mu_independent),
    ("delta_r_higgs_rel is linear in alpha", b_alpha_linear),
    ("mu-dependence of the raw self-energies is linear in q^2 (UV pole structure)", b_self_energy_mu_polynomial),
    ("self-energies are continuous at q^2 -> 0", b_q2_continuity),
    ("the large-mH slope equals log_coefficient", b_slope_matches_coefficient),
    ("delta_r_higgs_rel increases with mH between 125 and 1000 GeV", b_sign),
    ("self-energies are proportional to alpha at fixed masses", b_sigma_alpha_linear),
    ("W self-energy depends on MZ only through 1/s^2, Z self-energy on MW only through 1/(s^2 c^2)", b_sigma_coupling_scaling),
]
