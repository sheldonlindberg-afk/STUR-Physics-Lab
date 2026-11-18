"""Campaign: the Higgs-mass dependence of the rho parameter at one loop (SPEC.md)."""
import math

NAME = "higgs_rho"
MODULE = "higgs_rho"
ALLOWED_IMPORTS = {"math", "cmath", "fractions", "itertools", "functools", "numpy", "scipy", "mpmath", "sympy"}
QUOTED_ALLOWED = []
EXPORTS = {
    "self_energy_W": "self_energy_W(mH, MW, MZ, alpha, xi, mu) -> float: MS-bar Pi_WW(0) from Higgs-containing diagrams (SPEC section 2).",
    "self_energy_Z": "self_energy_Z(mH, MW, MZ, alpha, xi, mu) -> float: MS-bar Pi_ZZ(0) from Higgs-containing diagrams.",
    "rho_higgs_rel": "rho_higgs_rel(mH, MW, MZ, alpha, xi, mu) -> float: Delta rho(mH) - Delta rho(mH = MW), dimensionless.",
    "log_coefficient": "log_coefficient(MW, MZ, alpha, xi) -> float: lim Delta rho / ln(mH^2/MW^2) as mH -> infinity.",
}
MW, MZ, ALPHA = 80.38, 91.19, 1 / 128.0


def b_reference_zero(m):
    v = m.rho_higgs_rel(MW, MW, MZ, ALPHA, 1.0, MW)
    return abs(v) < 1e-14, f"rho_higgs_rel at mH = MW: {v:.1e}"


def b_mu_independent(m):
    worst = 0.0
    for mh in (50.0, 125.0, 400.0, 1500.0):
        for xi in (1.0, 0.4, 3.0):
            a = m.rho_higgs_rel(mh, MW, MZ, ALPHA, xi, MW)
            b = m.rho_higgs_rel(mh, MW, MZ, ALPHA, xi, 3.7 * MW)
            worst = max(worst, abs(b - a) / max(abs(a), 1e-30))
    return worst < 1e-9, f"relative change of rho_higgs_rel when the MS-bar scale moves from MW to 3.7 MW (all poles must cancel in the difference): {worst:.1e}"


def b_alpha_linear(m):
    a = m.rho_higgs_rel(250.0, MW, MZ, ALPHA, 1.0, MW)
    b = m.rho_higgs_rel(250.0, MW, MZ, 2 * ALPHA, 1.0, MW)
    return abs(b / a - 2) < 1e-9, f"rho_higgs_rel is first order in alpha: ratio {b / a:.9f}"


def b_custodial(m):
    """When M_Z -> M_W (s -> 0, g' -> 0) the hypercharge coupling vanishes and the custodial symmetry is exact, so Delta rho -> 0 like s^2
    at fixed alpha/s^2 (here: fixed g)."""
    out = []
    for eps in (2e-3, 1e-3):
        mz = MW * (1 + eps)
        s2 = 1 - (MW / mz) ** 2
        g2 = 4 * math.pi * ALPHA / (1 - (MW / MZ) ** 2)                 # the g of the physical point, kept fixed
        alpha = g2 * s2 / (4 * math.pi)
        out.append(m.rho_higgs_rel(400.0, MW, mz, alpha, 1.0, MW) / (alpha * s2))
    return abs(out[0] / out[1] - 1) < 0.01, f"rho_higgs_rel / (alpha s^2) at two small s^2: {out[0]:.5f}, {out[1]:.5f} (a finite limit means Delta rho ~ g'^2: custodial symmetry)"


def b_slope_matches_coefficient(m):
    B = m.log_coefficient(MW, MZ, ALPHA, 1.0)
    f = lambda mh: m.rho_higgs_rel(mh, MW, MZ, ALPHA, 1.0, MW)
    h1, h2 = 1e5 * MW, 1e6 * MW
    slope = (f(h2) - f(h1)) / math.log((h2 / MW) ** 2 / (h1 / MW) ** 2)
    return abs(slope / B - 1) < 1e-4, f"d rho / d ln mH^2 at mH ~ 1e5-1e6 MW: {slope:.6e}; log_coefficient {B:.6e}"


def b_sign_and_size(m):
    v = [m.rho_higgs_rel(mh, MW, MZ, ALPHA, 1.0, MW) for mh in (125.0, 300.0, 1000.0)]
    return v[0] < v[1] < v[2] or v[0] > v[1] > v[2], f"rho_higgs_rel at mH = 125, 300, 1000 GeV is monotone: {v}"


def b_difference_consistent(m):
    a = m.rho_higgs_rel(200.0, MW, MZ, ALPHA, 1.0, MW)
    f = lambda mh: m.self_energy_W(mh, MW, MZ, ALPHA, 1.0, MW) / MW**2 - m.self_energy_Z(mh, MW, MZ, ALPHA, 1.0, MW) / MZ**2
    return abs(a - (f(200.0) - f(MW))) < 1e-12 * max(1.0, abs(a)), "rho_higgs_rel equals Pi_WW/MW^2 - Pi_ZZ/MZ^2 at mH minus at MW (self_energy_* are the building blocks)"


BLIND = [
    ("rho_higgs_rel vanishes at the reference mass", b_reference_zero),
    ("rho_higgs_rel does not depend on the MS-bar scale (poles cancel)", b_mu_independent),
    ("rho_higgs_rel is linear in alpha", b_alpha_linear),
    ("custodial limit: Delta rho ~ g'^2 as M_Z -> M_W", b_custodial),
    ("the large-mH slope equals log_coefficient", b_slope_matches_coefficient),
    ("rho_higgs_rel is monotone in mH", b_sign_and_size),
    ("rho_higgs_rel is the difference of the two self-energy exports", b_difference_consistent),
]
