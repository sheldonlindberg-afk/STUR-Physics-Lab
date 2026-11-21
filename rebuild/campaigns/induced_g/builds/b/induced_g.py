"""Induced Newton constant, one loop, proper-time cutoff (see DERIVATION.md)."""
import math
import numpy as np
from math import comb

PROVENANCE = {
    "k1": ("derived", "b1 = tr(R/6+E); E from Lichnerowicz / Ricci / xi R"),
    "inv_G": ("derived", "matching W_R = S_grav: 1/G = kappa^2/(2 pi) * (n_s k1_s + n_v k1_v - n_w k1_w)"),
    "mpl": ("derived", "sqrt(1/G) if positive"),
}


def _scalar(d, xi):
    return 1.0 / 6.0 - xi


def k1(kind, d=4, xi=0.0):
    if kind == "scalar":
        return _scalar(d, xi)
    if kind in ("dirac", "weyl"):
        n = 2 ** (d // 2)
        v = n * (1.0 / 6.0 - 1.0 / 4.0)
        if kind == "weyl":
            if d % 2:
                raise ValueError("Weyl only in even d")
            v /= 2
        return v
    if kind in ("vector", "vector_no_ghosts"):
        v = d / 6.0 - 1.0
        if kind == "vector":
            v -= 2 * _scalar(d, 0.0)
        return v
    raise ValueError(kind)


def inv_G(kappa, n_s, n_w, n_v, xi=0.0):
    S = n_s * k1("scalar", 4, xi) + n_v * k1("vector", 4) - n_w * k1("weyl", 4)
    return kappa ** 2 * S / (2.0 * math.pi)


def mpl(kappa, n_s, n_w, n_v, xi=0.0):
    g = inv_G(kappa, n_s, n_w, n_v, xi)
    return math.sqrt(g) if g > 0 else None


def _fit_b1(spec, V, R, ts):
    """spec: list of (eigenvalue, degeneracy); returns (b0, b1/R) from polynomial fit."""
    ev = np.array([e for e, _ in spec], float)
    dg = np.array([g for _, g in spec], float)
    y = np.array([(4 * math.pi * t) ** 2 * np.sum(dg * np.exp(-t * ev)) / V for t in ts])
    c = np.polyfit(ts, y, 6)[::-1]
    return c[0], c[1] / R


if __name__ == "__main__":
    V, R = 8 * math.pi ** 2 / 3, 12.0
    L = 400
    ts = np.linspace(0.004, 0.03, 40)
    sc = lambda xi: [(l * (l + 3) + 12 * xi, (2 * l + 3) * (l + 1) * (l + 2) // 6) for l in range(L)]
    r = {}
    for xi in (0.0, 0.1, 1 / 6):
        r[f"scalar xi={xi:.3f}"] = (_fit_b1(sc(xi), V, R, ts)[1], k1("scalar", 4, xi))
    dirac = [((n + 2) ** 2, 8 * comb(n + 3, 3)) for n in range(L)]
    r["dirac"] = (_fit_b1(dirac, V, R, ts)[1], k1("dirac", 4))
    coex = [((l + 1) * (l + 2), l * (l + 3) * (2 * l + 3) // 2) for l in range(1, L)]
    exact = sc(0.0)[1:]
    # Hodge vector = coexact + exact(=scalar nonzero modes, same eigenvalues); ghosts: 2 scalar ops, subtracted
    b = lambda s: _fit_b1(s, V, R, ts)[1]
    vec_ng = (b(coex + exact), k1("vector_no_ghosts", 4))
    # fit of coex+exact: zero-mode of scalar excluded; the constant term lies at O(t^2), no effect on b1
    vec = (b(coex + exact) - 2 * b(sc(0.0)), k1("vector", 4))
    r["vector_no_ghosts"], r["vector"] = vec_ng, vec
    for k, (num, cl) in r.items():
        print(f"{k:20s} spectral k1 = {num:+.6f}   closed form = {cl:+.6f}")
    # radius route: -(1/2) s K(s) -> constant = -(1/2) b1 V/(16 pi^2) = dW/dkappa^2 ; W_R = -kappa^2 k1 * 32 pi^2 a^2/(32 pi^2)
    k = r["scalar xi=0.000"][0]
    print("scalar xi=0: spectral k1 =", k, "=> W(a) ~ -kappa^2 k1 a^2 decreases with a => 1/G > 0 contribution:",
          inv_G(1.0, 1, 0, 0) > 0)
    print("vector (with ghosts): W(a) ~ -kappa^2 k1 a^2 with k1 =", vec[0], "=> 1/G contribution sign:", "+" if inv_G(1.0, 0, 0, 1) > 0 else "-")
    print("inv_G(1, 1,0,0) =", inv_G(1.0, 1, 0, 0), " (1,0,1,0)", inv_G(1.0, 0, 1, 0), " (0,0,1)", inv_G(1.0, 0, 0, 1))
