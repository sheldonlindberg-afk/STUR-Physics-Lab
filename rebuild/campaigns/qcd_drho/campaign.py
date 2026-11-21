"""Campaign: the O(alpha_s) QCD correction to Delta rho of the top-bottom doublet (SPEC.md)."""
import math

NAME = "qcd_drho"
MODULE = "qcd_drho"
ALLOWED_IMPORTS = {"math", "cmath", "fractions", "itertools", "functools", "numpy", "scipy", "mpmath", "sympy"}
QUOTED_ALLOWED = []
EXPORTS = {
    "delta_rho_oneloop": "delta_rho_oneloop(m, GF, NC) -> float: one-loop Delta rho of the (t, b = massless) doublet, leading order in G_F m^2 (SPEC section 2).",
    "qcd_coeff": "qcd_coeff(scheme, CF, mu_over_m) -> float: the O(alpha_s/pi) coefficient c; scheme 'pole' or 'msbar' (mu_over_m = mu / mbar(mu))",
    "delta_rho_qcd": "delta_rho_qcd(m, GF, NC, CF, alphas, scheme, mu_over_m) -> float: Delta rho_0(m) (1 + c alpha_s/pi).",
}
GF = 1.1663788e-5


def b_oneloop_scaling(m):
    a, b = m.delta_rho_oneloop(100.0, GF, 3), m.delta_rho_oneloop(200.0, GF, 3)
    c = m.delta_rho_oneloop(150.0, GF, 6)
    d = m.delta_rho_oneloop(150.0, GF, 3)
    return abs(b / a - 4) < 1e-12 and abs(c / d - 2) < 1e-12, f"Delta rho_0 ~ m^2 and ~ N_C: {b / a:.12f}, {c / d:.12f}"


def b_linear_in_cf(m):
    c1, c2, c3 = (m.qcd_coeff("pole", cf, 1.0) for cf in (0.5, 1.0, 2.0))
    return abs(c3 - 2 * c2) < 1e-12 * abs(c2) and abs(c2 - 2 * c1) < 1e-12 * abs(c2), f"c ~ C_F at fixed N_C-independent colour structure: {c1:.10f}, {c2:.10f}, {c3:.10f}"


def b_scheme_shift(m):
    """m_pole^2 = mbar^2 (1 + k C_F alpha_s/pi): the two schemes' coefficients differ by that k C_F, independent of the quantity."""
    k = [(m.qcd_coeff("msbar", cf, 1.0) - m.qcd_coeff("pole", cf, 1.0)) / cf for cf in (0.5, 1.0, 2.0)]
    return max(k) - min(k) < 1e-12, f"(c_MSbar - c_pole)/C_F is a pure number: {k}"


def b_running(m):
    """d c / d ln(mu^2) of the MS-bar coefficient is a pure anomalous-dimension term, linear in ln mu and in C_F."""
    f = lambda r: m.qcd_coeff("msbar", 4 / 3, r)
    x = [f(1.0), f(math.e), f(math.e**2)]
    second = x[2] - 2 * x[1] + x[0]
    return abs(second) < 1e-10, f"second difference of c_MSbar over mu/m = 1, e, e^2 (linear in ln mu): {second:.1e}"


def b_total_consistent(m):
    v = m.delta_rho_qcd(172.0, GF, 3, 4 / 3, 0.118, "pole", 1.0)
    w = m.delta_rho_oneloop(172.0, GF, 3) * (1 + m.qcd_coeff("pole", 4 / 3, 1.0) * 0.118 / math.pi)
    return abs(v / w - 1) < 1e-12, f"delta_rho_qcd = Delta rho_0 (1 + c alpha_s/pi): {abs(v / w - 1):.1e}"


BLIND = [("one-loop Delta rho scales as m^2 and N_C", b_oneloop_scaling),
         ("coefficient is linear in C_F", b_linear_in_cf),
         ("scheme shift is C_F times a pure number", b_scheme_shift),
         ("MS-bar coefficient is linear in ln mu", b_running),
         ("delta_rho_qcd = Delta rho_0 (1 + c alpha_s/pi)", b_total_consistent)]
