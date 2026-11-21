"""Induced Newton constant at one loop (Sakharov), proper-time cutoff. See DERIVATION.md."""
import math
from fractions import Fraction

_SIXTH = Fraction(1, 6)


def _spinor_dim(d):
    return 2 ** (d // 2)


def k1(kind, d=4, xi=0.0):
    """Coefficient of R in b1 = tr(E) + tr(1) R/6, per field, bare trace (ghosts subtracted inside 'vector')."""
    if kind == "scalar":                       # E = -xi R, tr 1 = 1
        return float(_SIXTH) - xi
    if kind in ("dirac", "weyl"):              # E = -R/4 (Lichnerowicz), tr 1 = 2^floor(d/2)
        if kind == "weyl" and d % 2:
            raise ValueError("Weyl fermions only in even d")
        val = _spinor_dim(d) * (_SIXTH - Fraction(1, 4))
        return float(val / 2 if kind == "weyl" else val)
    if kind == "vector_no_ghosts":             # E_m^n = -R_m^n, tr E = -R, tr 1 = d
        return float(d * _SIXTH - 1)
    if kind == "vector":                       # minus two real xi = 0 scalars (complex Grassmann ghost pair)
        return float(d * _SIXTH - 1 - 2 * _SIXTH)
    raise ValueError(f"unknown kind {kind}")


def inv_G(kappa, n_s, n_w, n_v, xi=0.0):
    """1/G from W = -ln Z matched to S_grav = -(1/16 pi G) int sqrt(g) R, d = 4.
    W ⊃ -(kappa^2/(32 pi^2)) K int R, K = sum_bosons k1 - sum_fermions k1  =>  1/G = kappa^2 K / (2 pi)."""
    K = n_s * k1("scalar", 4, xi) + n_v * k1("vector", 4) - n_w * k1("weyl", 4)
    return kappa ** 2 * K / (2 * math.pi)


def mpl(kappa, n_s, n_w, n_v, xi=0.0):
    g = inv_G(kappa, n_s, n_w, n_v, xi)
    return math.sqrt(g) if g > 0 else None


PROVENANCE = {
    "k1": ("derived", "b1 = tr E + tr1 R/6 with E from each operator (DERIVATION.md sec 2)"),
    "inv_G": ("derived", "kappa^2 term of W = -ln Z with proper-time cutoff matched to S_grav (sec 3-5)"),
    "mpl": ("derived", "sqrt of inv_G when positive"),
}


# ---------------------------------------------------------------- second route: exact spectra on round spheres
def _spectra_S4(kind, xi=0.0, L=3000):
    """List of (eigenvalue, degeneracy, sign) on S^4 of radius 1; sign = +1 counted, -1 subtracted (ghosts)."""
    import numpy as np
    l = np.arange(0, L, dtype=float)
    dsc = (2 * l + 3) * (l + 1) * (l + 2) / 6
    if kind == "scalar":
        return [(l * (l + 3) + 12 * xi, dsc, 1.0)]
    if kind == "dirac":
        return [((l + 2) ** 2, 8 * (l + 1) * (l + 2) * (l + 3) / 6, 1.0)]
    lv = l[1:]
    ex = (lv * (lv + 3), dsc[1:], 1.0)
    co = ((lv + 1) * (lv + 2), lv * (lv + 3) * (2 * lv + 3) / 2, 1.0)
    if kind == "vector_no_ghosts":
        return [ex, co]
    if kind == "vector":
        return [ex, co, (l * (l + 3), dsc, -2.0)]
    raise ValueError(kind)


def _heat_fit_S4(kind, xi=0.0):
    import numpy as np
    ts = np.linspace(0.002, 0.02, 40)
    y = []
    for t in ts:
        s = 0.0
        for lam, deg, sg in _spectra_S4(kind, xi):
            s += sg * float(np.sum(deg * np.exp(-t * lam)))
        y.append(t * t * s)
    c = np.polyfit(ts, np.array(y), 6)[::-1]
    return c[0], c[1]          # c0 = tr1 * Vol/(16 pi^2) = tr1/6 ; c1 = 2 k1


def _heat_fit_S2(xi=0.0):
    import numpy as np
    l = np.arange(0, 4000, dtype=float)
    ts = np.linspace(0.001, 0.02, 40)
    y = [t * float(np.sum((2 * l + 1) * np.exp(-t * (l * (l + 1) + 2 * xi)))) for t in ts]
    c = np.polyfit(ts, np.array(y), 6)[::-1]
    return c[1] / 2            # t K = 1 + t (2 k1) + ...


def _W_route_S4(kind, xi=0.0, sign=1.0):
    """W(kappa) from exact spectrum, fitted for its kappa^2 coefficient B; returns 1/G per kappa^2 = -B/(2 pi)."""
    import numpy as np
    from scipy.special import exp1
    kap = np.linspace(8.0, 20.0, 25)
    W = []
    for k in kap:
        s = 0.0
        for lam, deg, sg in _spectra_S4(kind, xi, L=1200):
            m = lam > 1e-12                     # drop zero modes (they only give ln kappa)
            s += sg * float(np.sum(deg[m] * exp1(lam[m] / k ** 2)))
        W.append(-0.5 * sign * s)
    A = np.vstack([kap ** 4, kap ** 2, np.log(kap), np.ones_like(kap), kap ** -2, kap ** -4]).T
    coef = np.linalg.lstsq(A, np.array(W), rcond=None)[0]
    return -coef[1] / (2 * math.pi)


if __name__ == "__main__":
    print("k1 (d=4): main formula vs exact S^4 spectrum fit (c1/2)")
    for kind, xi in (("scalar", 0.0), ("scalar", 0.3), ("dirac", 0.0), ("vector", 0.0), ("vector_no_ghosts", 0.0)):
        c0, c1 = _heat_fit_S4(kind, xi)
        print(f"  {kind:17s} xi={xi}: k1={k1(kind, 4, xi):+.10f}  spectrum={c1 / 2:+.10f}  (tr1/6 check c0={c0:.8f})")
    print(f"  S^2 scalar xi=0: k1 spectrum = {_heat_fit_S2(0.0):+.10f}")
    print("1/G per kappa^2 per field: formula vs W(kappa) from exact S^4 spectrum")
    for label, kind, xi, sg, args in (("scalar xi=0", "scalar", 0.0, 1, (1, 0, 0, 0.0)),
                                      ("scalar xi=0.5", "scalar", 0.5, 1, (1, 0, 0, 0.5)),
                                      ("Weyl", "dirac", 0.0, -0.5, (0, 1, 0, 0.0)),
                                      ("vector+ghosts", "vector", 0.0, 1, (0, 0, 1, 0.0))):
        print(f"  {label:14s}: formula {inv_G(1.0, *args):+.10f}   W-route {_W_route_S4(kind, xi, sg):+.10f}")
