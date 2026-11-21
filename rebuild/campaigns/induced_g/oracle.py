"""Hidden oracle for the induced_g campaign.

Targets (LIT, independent of the builds): heat-kernel b1 = tr(E + R/6) for D = -(nabla^2 + E)
(D. Vassilevich, Phys. Rept. 388 (2003) 279, arXiv:hep-th/0306138); per field: scalar 1/6 - xi; Dirac
2^floor(d/2) (1/6 - 1/4); vector E = -Ric: d/6 - 1, ghosts -2/6, total (d - 8)/6 (Solodukhin, Living Rev. Rel. 14
(2011) 8, arXiv:1104.3712, D_1/6 - 1 with D_1 = d - 2). In d = 4: 1/6 - xi, -1/3 (Dirac), -2/3 (vector), matching
M. Visser, arXiv:gr-qc/0204062, Table I. Induced coupling: 1/G = (kappa^2/2 pi) [n_s (1/6 - xi) + n_w/6 - 2 n_v/3]
(sign: F. Larsen and F. Wilczek, arXiv:hep-th/9506066, sec. 3.3, 1/G_ren = 1/G_bare + (1/2 pi)(1/6 - xi)/eps^2;
scalars and fermions positive, vectors negative)."""
import math

LINT_TARGETS = []
LINT_EXACT = [1 / (2 * math.pi), -2 / 3, 2 / 3]


def ref_k1(kind, d, xi=0.0):
    if kind == "scalar":
        return 1 / 6 - xi
    sd = 2 ** (d // 2)
    if kind == "dirac":
        return sd * (1 / 6 - 1 / 4)
    if kind == "weyl":
        return sd * (1 / 6 - 1 / 4) / 2
    if kind == "vector_no_ghosts":
        return d / 6 - 1
    if kind == "vector":
        return d / 6 - 1 - 2 / 6
    raise KeyError(kind)


def ref_inv_G(kappa, n_s, n_w, n_v, xi=0.0):
    return kappa ** 2 / (2 * math.pi) * (n_s * (1 / 6 - xi) + n_w / 6 - 2 * n_v / 3)


def k1_check(m):
    worst = 0.0
    for d in (2, 3, 4, 5, 6, 8, 10):
        for kind in ("scalar", "dirac", "vector", "vector_no_ghosts") + (("weyl",) if d % 2 == 0 else ()):
            for xi in ((0.0, 0.25, -0.4) if kind == "scalar" else (0.0,)):
                worst = max(worst, abs(m.k1(kind, d, xi) - ref_k1(kind, d, xi)))
    return worst < 1e-12, f"k1 for every kind at d = 2..10 against tr(E + R/6): worst {worst:.1e}"


def sign_check(m):
    s, v, w = m.inv_G(1.0, 1, 0, 0), m.inv_G(1.0, 0, 0, 1), m.inv_G(1.0, 0, 1, 0)
    return s > 0 and w > 0 and v < 0, f"one minimal scalar {s:+.4f}, one Weyl {w:+.4f}, one vector {v:+.4f} (scalars and fermions positive, vectors negative)"


def inv_G_check(m):
    pts = [(1.0, 1, 0, 0, 0.0), (2.0, 18, 69, 17, 0.0), (3.0, 18, 69, 17, 1 / 6), (1.7, 4, 45, 12, 0.3), (5.0, 0, 3, 1, -0.2)]
    worst = max(abs(m.inv_G(*p) - ref_inv_G(*p)) / max(abs(ref_inv_G(*p)), 1e-300) for p in pts)
    return worst < 1e-12, f"1/G against (kappa^2/2pi) str[k1] at {len(pts)} points: worst {worst:.1e}"


def stage1_check(m):
    a = m.mpl(5.3355e19, 18, 69, 17, 0.0)
    b = m.mpl(5.3355e19, 18, 66, 17, 1 / 6)
    return a is not None and abs(a / 3.788e19 - 1) < 1e-3 and b is None, f"stage 1's content at its pole: M_Pl = {a} (beta = +1/sqrt3, xi = 0); beta = -1/sqrt3 at xi = 1/6 has no positive G: {b}"


ORACLE = [("k1 per kind and dimension", k1_check), ("the signs of 1/G per species", sign_check),
          ("1/G at general counts", inv_G_check), ("stage 1's content", stage1_check)]
# CANARY-5a8c2e7f1d3b6094-induced_g: planted so a builder transcript that contains this string has read the oracle
