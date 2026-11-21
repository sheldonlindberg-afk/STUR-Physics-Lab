"""Campaign: grey-body factors and Hawking emission power per degree of freedom (SPEC.md)."""
import math

NAME = "greybody"
MODULE = "greybody"
ALLOWED_IMPORTS = {"math", "cmath", "fractions", "itertools", "functools", "numpy", "scipy", "mpmath"}
QUOTED_ALLOWED = []
EXPORTS = {
    "transmission": "transmission(s, j, w) -> float in [0, 1]: the absorption probability of partial wave j of a massless field "
                    "of spin s (s in 0, 0.5, 1, 2) at energy w (units 1/M), SPEC sections 1-2.",
    "absorption_sum": "absorption_sum(s, w) -> float: sum over j of (2j + 1) * transmission(s, j, w), over all j >= s that matter.",
    "power_per_dof": "power_per_dof(s) -> float: P_s of SPEC section 3, in units 1/M^2 (G = c = hbar = 1).",
}


def _t(m, s, j, w):
    return m.transmission(s, j, w)


def b_range(m):
    vals = [_t(m, s, j, w) for s, j in ((0, 0), (0.5, 0.5), (1, 1), (2, 2), (0, 3)) for w in (0.05, 0.3, 1.0, 2.0)]
    return all(0.0 <= v <= 1.0 + 1e-9 for v in vals), f"min {min(vals):.3g}, max {max(vals):.6g}"


def b_low_scalar(m):
    r = _t(m, 0, 0, 0.005) / 0.005**2
    return 14.7 < r < 17.3, f"Gamma_00/w^2 at w = 0.005: {r:.3f}; the low-frequency scalar absorption cross section is the horizon area 16 pi M^2"


def b_slopes(m):
    out, ok = [], True
    for s, j, want in ((0, 1, 4), (1, 1, 4), (2, 2, 6), (0.5, 0.5, 2), (0.5, 1.5, 4)):
        a, b = _t(m, s, j, 0.01), _t(m, s, j, 0.02)
        slope = math.log(b / a) / math.log(2)
        out.append(f"({s},{j}): {slope:.2f}")
        ok &= abs(slope - want) < 0.25
    return ok, "low-frequency slopes d ln Gamma / d ln w, expected 2j+2 (bosons), 2j+1 (fermions): " + ", ".join(out)


def b_geometric(m):
    ok, out = True, []
    for s in (0, 1, 0.5):
        r = m.absorption_sum(s, 1.0) / 27.0
        out.append(f"s={s}: {r:.3f}")
        ok &= 0.88 < r < 1.12
    return ok, "sum (2j+1) Gamma / (27 w^2) at w = 1 (geometric optics: the capture cross section 27 pi M^2): " + ", ".join(out)


def b_monotone(m):
    ok = True
    for s in (0, 0.5, 1, 2):
        g = [_t(m, s, s if s != 0 else 0, w) for w in (0.05, 0.1, 0.2, 0.4, 0.8, 1.5)]
        ok &= all(b >= a - 1e-9 for a, b in zip(g, g[1:]))
    return ok, "the lowest partial wave's transmission rises with w"


def b_order(m):
    p = [m.power_per_dof(s) for s in (0, 0.5, 1, 2)]
    return all(x > 0 for x in p) and p[0] > p[1] > p[2] > p[3], "P_0 > P_1/2 > P_1 > P_2 > 0: " + ", ".join(f"{x:.3e}" for x in p)


def b_convergence_independent_of_call(m):
    a, b = _t(m, 1, 2, 0.37), _t(m, 1, 2, 0.37)
    return abs(a - b) < 1e-12, "the same arguments give the same answer"


def _fact(x):
    return math.gamma(x + 1)


def _dfact(n):
    out = 1
    while n > 1:
        out *= n
        n -= 2
    return out


def lowfreq_coeff(s, l):
    """Exact w -> 0 coefficient of Gamma_{s,l}: bosons 4 C^2 (2w)^(2l+2), fermions C^2 (2w)^(2l+1),
    C = (l - s)! (l + s)! / ((2l)! (2l + 1)!!) (matched asymptotics; a property of the equations, not of the answer)."""
    C = _fact(l - s) * _fact(l + s) / (_fact(2 * l) * _dfact(int(round(2 * l + 1))))
    fermion = abs(s - 0.5) < 1e-12
    p = int(round(2 * l + 1)) if fermion else int(round(2 * l + 2))
    return C * C * 2**p * (1 if fermion else 4), p


def b_lowfreq_coeff(m):
    out, ok = [], True
    for s, l in ((0, 0), (0, 1), (0.5, 0.5), (0.5, 1.5), (1, 1), (1, 2), (2, 2), (2, 3)):
        c, p = lowfreq_coeff(s, l)
        r1, r2 = m.transmission(s, l, 0.001) / 0.001**p, m.transmission(s, l, 0.002) / 0.002**p
        ext = 2 * r1 - r2                                    # the first correction is linear in w
        out.append(f"({s},{l}): {ext / c - 1:+.1e}")
        ok &= abs(ext / c - 1) < 2e-3
    return ok, "w -> 0 coefficient / exact - 1: " + ", ".join(out)


def b_power_assembly(m, nodes=24, edges=(0, 0.04, 0.1, 0.2, 0.35, 0.55, 0.8, 1.2, 1.8, 2.7)):
    """The gate recomputes P_s from m.transmission with its own quadrature, occupation, (2j+1) and temperature."""
    import numpy as np
    T = 1 / (8 * math.pi)
    x, wt = np.polynomial.legendre.leggauss(nodes)
    out, ok = [], True
    for s in (0, 0.5, 1, 2):
        fermion, tot, j = s == 0.5, 0.0, s
        while True:
            c = 0.0
            for a, b in zip(edges, edges[1:]):
                for xi, wi in zip(x, wt):
                    w = 0.5 * (b - a) * xi + 0.5 * (a + b)
                    occ = 1 / (math.exp(w / T) + 1) if fermion else 1 / math.expm1(w / T)
                    c += 0.5 * (b - a) * wi * w * m.transmission(s, j, w) * occ / (2 * math.pi)
            tot += (2 * j + 1) * c
            if (2 * j + 1) * c < 1e-9 * tot:
                break
            j += 1
        p = m.power_per_dof(s)
        out.append(f"s={s}: {p / tot - 1:+.1e}")
        ok &= abs(p / tot - 1) < 1e-5
    return ok, "power_per_dof / the gate's own sum over transmission - 1: " + ", ".join(out)


BLIND = [
    ("transmission lies in [0, 1]", b_range),
    ("low-frequency scalar limit: the horizon area", b_low_scalar),
    ("low-frequency power laws of the lowest partial waves", b_slopes),
    ("geometric-optics limit: capture cross section 27 pi M^2", b_geometric),
    ("transmission of the lowest partial wave is monotone in w", b_monotone),
    ("power per degree of freedom: positive and ordered by spin", b_order),
    ("determinism", b_convergence_independent_of_call),
    ("exact low-frequency coefficients of the partial waves", b_lowfreq_coeff),
    ("power_per_dof equals the gate's own assembly from transmission", b_power_assembly),
]
