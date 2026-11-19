"""Campaign: the bosonic one-loop gauge-boson self-energies, 't Hooft-Feynman gauge (SPEC.md)."""
import math

NAME = "bos_se"
MODULE = "bos_se"
ALLOWED_IMPORTS = {"math", "cmath", "fractions", "itertools", "functools", "numpy", "scipy", "mpmath", "sympy"}
QUOTED_ALLOWED = []
EXPORTS = {
    "sigma_AA": "sigma_AA(k2, MW, MZ, MH, alpha, mu) -> float: bosonic transverse photon self-energy Sigma^AA_T(k^2) (SPEC section 2).",
    "sigma_AZ": "sigma_AZ(k2, MW, MZ, MH, alpha, mu) -> float: bosonic transverse photon-Z mixing Sigma^AZ_T(k^2).",
    "sigma_ZZ": "sigma_ZZ(k2, MW, MZ, MH, alpha, mu) -> float: bosonic transverse Z self-energy Sigma^ZZ_T(k^2).",
    "sigma_W": "sigma_W(k2, MW, MZ, MH, alpha, mu) -> float: bosonic transverse W self-energy Sigma^W_T(k^2).",
}
MW, MZ, MH, ALPHA = 80.38, 91.19, 125.0, 1 / 128.0
FUNCS = ("sigma_AA", "sigma_AZ", "sigma_ZZ", "sigma_W")


def _all(m):
    return [(n, getattr(m, n)) for n in FUNCS]


def b_photon_ward(m):
    worst = 0.0
    for mu in (MW, 3.0 * MW):
        for mh in (50.0, 125.0, 700.0):
            worst = max(worst, abs(m.sigma_AA(0.0, MW, MZ, mh, ALPHA, mu)) / (ALPHA * MW**2))
    return worst < 1e-12, f"|Sigma^AA_T(0)| / (alpha MW^2) over mu, MH (the photon stays massless): {worst:.1e}"


def b_alpha_linear(m):
    worst = 0.0
    for n, f in _all(m):
        for k2 in (-0.7 * MW**2, 0.4 * MW**2, 0.0):
            a, b = f(k2, MW, MZ, MH, ALPHA, 1.7 * MW), f(k2, MW, MZ, MH, 3 * ALPHA, 1.7 * MW)
            if abs(a) > 1e-12:
                worst = max(worst, abs(b / a / 3 - 1))
    return worst < 1e-12, f"Sigma(3 alpha) / (3 Sigma(alpha)) - 1 for all four, three k^2: {worst:.1e}"


def b_mu_linear_in_k2(m):
    """The scale dependence comes only from the UV pole: a polynomial of degree one in k^2 (a mass^2 and a k^2 term)."""
    worst = 0.0
    for n, f in _all(m):
        d = lambda k2: f(k2, MW, MZ, MH, ALPHA, 2.7 * MW) - f(k2, MW, MZ, MH, ALPHA, MW)
        x = (-0.8 * MW**2, 0.0, 0.8 * MW**2)
        scale = max(abs(d(x[0])), abs(d(x[2])), 1e-30)
        worst = max(worst, abs(d(x[2]) - 2 * d(x[1]) + d(x[0])) / scale)
    return worst < 1e-9, f"second difference of the mu dependence of each Sigma over three equally spaced k^2 (must vanish): {worst:.1e}"


def b_continuity(m):
    worst = 0.0
    for n, f in _all(m):
        a, b = f(0.0, MW, MZ, MH, ALPHA, 1.3 * MW), f(1e-7, MW, MZ, MH, ALPHA, 1.3 * MW)
        worst = max(worst, abs(b - a) / max(abs(a), 1e-3))
    return worst < 1e-6, f"Sigma(k^2 = 1e-7 GeV^2) against Sigma(0): {worst:.1e}"


def b_finite_everywhere(m):
    bad = []
    for n, f in _all(m):
        for k2 in (-1e5, -3.0 * MW**2, 0.0, 0.2 * MW**2, MW**2, MZ**2, 0.95 * 4 * MW**2):
            v = f(k2, MW, MZ, MH, ALPHA, MW)
            if not (isinstance(v, float) and math.isfinite(v)):
                bad.append((n, k2))
    return not bad, f"finite real values at k^2 from -1e5 to 3.8 MW^2 (and at MW^2, MZ^2): {bad or 'all finite'}"


BLIND = [
    ("photon Ward identity: Sigma^AA_T(0) = 0", b_photon_ward),
    ("all four Sigma are linear in alpha", b_alpha_linear),
    ("mu dependence of every Sigma is linear in k^2 (UV pole structure)", b_mu_linear_in_k2),
    ("Sigma is continuous at k^2 -> 0", b_continuity),
    ("Sigma is finite and real at all sampled k^2 including thresholds", b_finite_everywhere),
]
