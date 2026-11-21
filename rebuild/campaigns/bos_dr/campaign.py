"""Campaign: the bosonic part of the on-shell Delta r of muon decay at one loop (SPEC.md); the stage-1 module bos_se is provided."""
import math

NAME = "bos_dr"
MODULE = "bos_dr"
ALLOWED_IMPORTS = {"math", "cmath", "fractions", "itertools", "functools", "numpy", "scipy", "mpmath", "sympy", "bos_se"}
QUOTED_ALLOWED = []
EXPORTS = {
    "delta_r_bos": "delta_r_bos(MW, MZ, MH, alpha) -> float: the non-fermionic part of the one-loop on-shell Delta r (SPEC section 3).",
    "delta_vb": "delta_vb(MW, MZ, alpha) -> float: vertex + box + lepton wave-function contribution after the Fermi-theory QED subtraction (SPEC section 4).",
}
MW, MZ, MH, ALPHA = 80.38, 91.19, 125.0, 1 / 128.0


def b_alpha_linear(m):
    a, b = m.delta_r_bos(MW, MZ, MH, ALPHA), m.delta_r_bos(MW, MZ, MH, 2 * ALPHA)
    a2, b2 = m.delta_vb(MW, MZ, ALPHA), m.delta_vb(MW, MZ, 2 * ALPHA)
    ok = abs(b / a - 2) < 1e-9 and abs(b2 / a2 - 2) < 1e-9
    return ok, f"first order in alpha: Delta r_bos ratio {b / a:.9f}, delta_vb ratio {b2 / a2:.9f}"


def b_slope_matches_higgs(m):
    """For M_H >> M_W the log M_H^2 dependence of Delta r is the Higgs term derived in the earlier campaigns: 11 alpha/(48 pi s^2)."""
    s2 = 1 - (MW / MZ) ** 2
    B = 11 * ALPHA / (48 * math.pi * s2)
    f = lambda mh: m.delta_r_bos(MW, MZ, mh, ALPHA)
    h1, h2 = 1e5 * MW, 1e6 * MW
    slope = (f(h2) - f(h1)) / math.log((h2 / MW) ** 2 / (h1 / MW) ** 2)
    return abs(slope / B - 1) < 1e-4, f"d Delta r_bos / d ln MH^2 at MH ~ 1e5-1e6 MW: {slope:.6e}; expected {B:.6e}"


def b_smooth_in_mh(m):
    v = [m.delta_r_bos(MW, MZ, mh, ALPHA) for mh in (10.0, 50.0, 125.0, 300.0, 1000.0)]
    return all(math.isfinite(x) for x in v) and all(v[i] < v[i + 1] for i in range(len(v) - 1)), f"Delta r_bos(MH) increases with MH: {v}"


def b_vb_depends_on_s2_only(m):
    """delta_vb depends on the masses only through s^2 = 1 - MW^2/MZ^2 (dimensionless, one coupling alpha): rescale both masses."""
    a, b = m.delta_vb(MW, MZ, ALPHA), m.delta_vb(3.1 * MW, 3.1 * MZ, ALPHA)
    return abs(b / a - 1) < 1e-12, f"delta_vb under a common rescaling of M_W and M_Z: {abs(b / a - 1):.1e}"


def b_scale_invariance(m):
    """Delta r_bos is dimensionless: scaling all masses together leaves it unchanged."""
    a, b = m.delta_r_bos(MW, MZ, MH, ALPHA), m.delta_r_bos(2.3 * MW, 2.3 * MZ, 2.3 * MH, ALPHA)
    return abs(b / a - 1) < 1e-9, f"Delta r_bos under a common rescaling of M_W, M_Z, M_H: {abs(b / a - 1):.1e}"


BLIND = [
    ("Delta r_bos and delta_vb are first order in alpha", b_alpha_linear),
    ("the large-MH slope of Delta r_bos is 11 alpha/(48 pi s^2)", b_slope_matches_higgs),
    ("Delta r_bos is finite and increases with MH", b_smooth_in_mh),
    ("delta_vb depends on the masses only through s^2", b_vb_depends_on_s2_only),
    ("Delta r_bos is dimensionless (mass-scale invariant)", b_scale_invariance),
]
