"""Campaign: Newton's constant induced by quantum fields at one loop, proper-time cutoff (SPEC.md)."""
import math

NAME = "induced_g"
MODULE = "induced_g"
ALLOWED_IMPORTS = {"math", "cmath", "fractions", "itertools", "functools", "numpy", "scipy", "mpmath", "sympy"}
QUOTED_ALLOWED = []
EXPORTS = {
    "k1": "k1(kind, d=4, xi=0.0) -> float: the coefficient of R in the heat-kernel b1 of the field, per field, bare trace (SPEC section 2).",
    "inv_G": "inv_G(kappa, n_s, n_w, n_v, xi=0.0) -> float: induced 1/G (hbar = c = 1, d = 4), in units of kappa^2.",
    "mpl": "mpl(kappa, n_s, n_w, n_v, xi=0.0) -> float or None: sqrt(1/G) if 1/G > 0, else None.",
}


def b_conformal_scalar(m):
    s = [m.k1("scalar", 4, x) for x in (0.0, 0.1, 0.3)]
    lin = abs((s[1] - s[0]) / 0.1 - (s[2] - s[0]) / 0.3) < 1e-12 and abs((s[1] - s[0]) / 0.1 + 1) < 1e-12
    return lin, f"the scalar k1 is linear in xi with slope -1 (xi R enters E directly): {s}"


def b_spinor_scaling(m):
    r = m.k1("dirac", 6) / m.k1("dirac", 4)
    w = m.k1("weyl", 4) / m.k1("dirac", 4)
    return abs(r - 2) < 1e-12 and abs(w - 0.5) < 1e-12, f"Dirac k1 scales with the spinor dimension (d = 6 / d = 4: {r}); Weyl = Dirac / 2 ({w})"


def b_vector_linear_in_d(m):
    v = [m.k1("vector", d) for d in (3, 4, 5, 6, 7)]
    g = [m.k1("vector", d) - m.k1("vector_no_ghosts", d) for d in (3, 4, 5, 6, 7)]
    lin = max(abs((v[i + 1] - v[i]) - (v[1] - v[0])) for i in range(4)) < 1e-12
    ghosts_const = max(g) - min(g) < 1e-12
    return lin and ghosts_const, "the vector k1 is linear in d (tr 1 = d), and the ghosts' part does not depend on d"


def b_induced_scaling(m):
    a = m.inv_G(2.0, 3, 5, 1, 0.0)
    ok = abs(m.inv_G(4.0, 3, 5, 1, 0.0) / a - 4) < 1e-12
    add = abs(m.inv_G(2.0, 3, 5, 1) - (m.inv_G(2.0, 3, 0, 0) + m.inv_G(2.0, 0, 5, 0) + m.inv_G(2.0, 0, 0, 1))) < 1e-12 * abs(a)
    zero = m.inv_G(2.0, 0, 0, 0) == 0
    return ok and add and zero, "1/G scales as kappa^2, adds over species, vanishes with no fields"


def b_mpl_consistent(m):
    pts = [(3.0, 2, 7, 1, 0.0), (1.5, 0, 0, 3, 0.0), (2.0, 4, 0, 0, 0.5)]
    good = True
    for p in pts:
        g, mp = m.inv_G(*p), m.mpl(*p)
        good &= (mp is None) if g <= 0 else abs(mp * mp / g - 1) < 1e-12
    return good, "mpl = sqrt(1/G) when positive, None otherwise"


BLIND = [("scalar k1: linear in xi, slope -1", b_conformal_scalar),
         ("spinor k1 scales with the spinor dimension; Weyl = Dirac/2", b_spinor_scaling),
         ("vector k1 linear in d; ghost part independent of d", b_vector_linear_in_d),
         ("1/G: kappa^2 scaling, additive, zero without fields", b_induced_scaling),
         ("mpl consistent with inv_G", b_mpl_consistent)]
