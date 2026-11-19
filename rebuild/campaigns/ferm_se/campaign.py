"""Campaign: the fermionic one-loop gauge-boson self-energies, 't Hooft-Feynman gauge (SPEC.md)."""
import math

NAME = "ferm_se"
MODULE = "ferm_se"
ALLOWED_IMPORTS = {"math", "cmath", "fractions", "itertools", "functools", "numpy", "scipy", "mpmath", "sympy"}
QUOTED_ALLOWED = []
EXPORTS = {
    "sigma_AA": "sigma_AA(k2, fermions, MW, MZ, alpha, mu) -> float: fermionic transverse photon self-energy Sigma^AA_T(k^2) (SPEC section 2); fermions = ((m, Q, I3, NC), ...).",
    "sigma_AZ": "sigma_AZ(k2, fermions, MW, MZ, alpha, mu) -> float: fermionic transverse photon-Z mixing Sigma^AZ_T(k^2).",
    "sigma_ZZ": "sigma_ZZ(k2, fermions, MW, MZ, alpha, mu) -> float: fermionic transverse Z self-energy Sigma^ZZ_T(k^2).",
    "sigma_W": "sigma_W(k2, doublets, MW, MZ, alpha, mu) -> float: fermionic transverse W self-energy Sigma^W_T(k^2); doublets = ((m_up, m_down, w), ...), w = NC |V|^2.",
}
MW, MZ, ALPHA = 80.38, 91.19, 1 / 128.0
LEPTON = ((0.000511, -1, -0.5, 1), (0.0, 0, 0.5, 1))
TOP = ((172.5, 2 / 3, 0.5, 3), (4.7, -1 / 3, -0.5, 3))
FUNCS = ("sigma_AA", "sigma_AZ", "sigma_ZZ")


def b_photon_ward(m):
    worst = 0.0
    for mu in (MW, 3.0 * MW):
        for fs in (LEPTON, TOP, LEPTON + TOP):
            worst = max(worst, abs(m.sigma_AA(0.0, fs, MW, MZ, ALPHA, mu)) / (ALPHA * MW**2))
            worst = max(worst, abs(m.sigma_AZ(0.0, fs, MW, MZ, ALPHA, mu)) / (ALPHA * MW**2))
    return worst < 1e-12, f"|Sigma^AA_T(0)|, |Sigma^AZ_T(0)| / (alpha MW^2) (photon massless, no fermion-loop mixing at k^2 = 0): {worst:.1e}"


def b_alpha_linear(m):
    worst = 0.0
    for n in FUNCS:
        for k2 in (-0.7 * MW**2, 0.4 * MW**2, 0.0):
            a, b = getattr(m, n)(k2, TOP, MW, MZ, ALPHA, 1.7 * MW), getattr(m, n)(k2, TOP, MW, MZ, 3 * ALPHA, 1.7 * MW)
            if abs(a) > 1e-12:
                worst = max(worst, abs(b / a / 3 - 1))
    return worst < 1e-12, f"Sigma(3 alpha) / (3 Sigma(alpha)) - 1: {worst:.1e}"


def b_additive(m):
    worst = 0.0
    for n in FUNCS:
        for k2 in (-1000.0, 0.3 * MW**2):
            s = m.__dict__[n]
            a = s(k2, LEPTON, MW, MZ, ALPHA, MW) + s(k2, TOP, MW, MZ, ALPHA, MW)
            b = s(k2, LEPTON + TOP, MW, MZ, ALPHA, MW)
            worst = max(worst, abs(a - b) / (abs(b) + 1e-12))
    d = ((0.0, 0.0005, 1.0), (172.5, 4.7, 3 * 0.9), (1.5, 0.15, 3 * 0.05))
    for k2 in (-1000.0, 0.3 * MW**2):
        a = sum(m.sigma_W(k2, (x,), MW, MZ, ALPHA, MW) for x in d)
        b = m.sigma_W(k2, d, MW, MZ, ALPHA, MW)
        worst = max(worst, abs(a - b) / (abs(b) + 1e-12))
    return worst < 1e-12, f"the loops of different fermions add: {worst:.1e}"


def b_mu_linear_in_k2(m):
    worst = 0.0
    for n in FUNCS:
        d = lambda k2: getattr(m, n)(k2, LEPTON + TOP, MW, MZ, ALPHA, 2.7 * MW) - getattr(m, n)(k2, LEPTON + TOP, MW, MZ, ALPHA, MW)
        x = (-0.8 * MW**2, 0.0, 0.8 * MW**2)
        scale = max(abs(d(x[0])), abs(d(x[2])), 1e-30)
        worst = max(worst, abs(d(x[2]) - 2 * d(x[1]) + d(x[0])) / scale)
    return worst < 1e-9, f"second difference of the mu dependence over three equally spaced k^2: {worst:.1e}"


def b_continuity_finite(m):
    worst, bad = 0.0, []
    for n in FUNCS:
        a, b = getattr(m, n)(0.0, LEPTON + TOP, MW, MZ, ALPHA, 1.3 * MW), getattr(m, n)(1e-12, LEPTON + TOP, MW, MZ, ALPHA, 1.3 * MW)
        worst = max(worst, abs(b - a) / max(abs(a), 1e-3))
        for k2 in (-1e5, -3.0 * MW**2, 0.2 * MW**2, MW**2, MZ**2, 4 * 172.5**2 * 1.2):
            v = getattr(m, n)(k2, LEPTON + TOP, MW, MZ, ALPHA, MW)
            if not (isinstance(v, float) and math.isfinite(v)):
                bad.append((n, k2))
    return worst < 1e-6 and not bad, f"continuity at k^2 -> 0 (1e-12 GeV^2, well below m_e^2): {worst:.1e}; finite real values at sampled k^2: {bad or 'all finite'}"


BLIND = [
    ("photon Ward identity: Sigma^AA_T(0) = Sigma^AZ_T(0) = 0", b_photon_ward),
    ("Sigma is linear in alpha", b_alpha_linear),
    ("loops of different fermions and doublets add", b_additive),
    ("mu dependence of every Sigma is linear in k^2 (UV pole structure)", b_mu_linear_in_k2),
    ("continuous at k^2 -> 0 and finite at all sampled k^2", b_continuity_finite),
]
