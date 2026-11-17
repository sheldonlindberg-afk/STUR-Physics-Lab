"""Campaign: Casimir-Polder interaction by fourth-order perturbation theory (SPEC.md)."""
import math

NAME = "qed_cp"
MODULE = "qed_cp"
ALLOWED_IMPORTS = {"math", "cmath", "fractions", "itertools", "functools", "numpy", "scipy", "mpmath", "sympy"}
QUOTED_ALLOWED = []
EXPORTS = {
    "cp_energy": "cp_energy(r, w0, alpha0) -> float: U(r), hbar = c = 1, Gaussian units (SPEC sections 1-2).",
    "far_coefficient": "far_coefficient() -> float: C with U -> -C alpha0^2 / r^7 for r w0 >> 1.",
    "near_coefficient": "near_coefficient() -> float: D with U -> -D w0 alpha0^2 / r^6 for r w0 << 1.",
}


def b_negative(m):
    vals = [m.cp_energy(r, 1.0, 1.0) for r in (0.01, 0.3, 1.0, 3.0, 30.0, 300.0)]
    return all(v < 0 for v in vals), "attractive at every separation: " + ", ".join(f"{v:.3e}" for v in vals)


def b_alpha_squared(m):
    a, b = m.cp_energy(2.0, 1.0, 1.0), m.cp_energy(2.0, 1.0, 3.0)
    return abs(b / a - 9.0) < 1e-6, f"U scales as alpha0^2: ratio {b / a:.9f} (expected 9)"


def b_dimensions(m):
    lam = 2.5
    a, b = m.cp_energy(1.7, 1.3, 0.8), m.cp_energy(lam * 1.7, 1.3 / lam, lam**3 * 0.8)
    return abs(b * lam / a - 1) < 1e-6, f"U(lam r, w0/lam, lam^3 alpha0) lam / U = {b * lam / a:.9f} (expected 1)"


def slope(m, r):
    h = 1e-3
    return (math.log(abs(m.cp_energy(r * (1 + h), 1.0, 1.0))) - math.log(abs(m.cp_energy(r * (1 - h), 1.0, 1.0)))) / (math.log(1 + h) - math.log(1 - h))


def b_slopes(m):
    s_near, s_far = slope(m, 1e-2), slope(m, 1e3)
    return abs(s_near + 6) < 0.1 and abs(s_far + 7) < 0.1, f"d ln|U| / d ln r: {s_near:.3f} at r w0 = 1e-2 (expected -6), {s_far:.3f} at 1e3 (expected -7)"


def b_limits_agree(m):
    far, near = m.far_coefficient(), m.near_coefficient()
    r_far, r_near = 1e4, 1e-3
    c_far = -m.cp_energy(r_far, 1.0, 1.0) * r_far**7
    c_near = -m.cp_energy(r_near, 1.0, 1.0) * r_near**6
    return abs(c_far / far - 1) < 2e-3 and abs(c_near / near - 1) < 2e-3, \
        f"far {far:.6f} vs U at r w0 = 1e4: {c_far:.6f}; near {near:.6f} vs U at 1e-3: {c_near:.6f}"


def b_crossover_monotone(m):
    rs = [10**(k / 4 - 2) for k in range(0, 21)]
    g = [abs(m.cp_energy(r, 1.0, 1.0)) * r**6 for r in rs]
    return all(b < a * (1 + 1e-9) for a, b in zip(g, g[1:])), "|U| r^6 decreases monotonically as retardation sets in"


def b_far_approach(m):
    """U r^7 / C -> 1 with a 1/rho^2 deficit (the integrand is analytic in 1/rho^2): kills asymptotic-switch and small systematic errors."""
    C = m.far_coefficient()
    d = [1 + m.cp_energy(x, 1.0, 1.0) * x**7 / C for x in (100.0, 200.0)]
    ok = d[0] > 0 and d[1] > 0 and abs(d[0] / d[1] - 4) < 0.1
    return ok, f"far deficits {d[0]:.3e}, {d[1]:.3e}, ratio {d[0] / d[1] if d[1] else float('inf'):.3f} (expected 4)"


def b_near_approach(m):
    """U r^6 / (D w0) -> 1 with a rho^2 deficit (no odd power)."""
    D = m.near_coefficient()
    d = [1 + m.cp_energy(x, 1.0, 1.0) * x**6 / D for x in (0.005, 0.01)]
    ok = d[0] > 0 and d[1] > 0 and abs(d[1] / d[0] - 4) < 0.1
    return ok, f"near deficits {d[0]:.3e}, {d[1]:.3e}, ratio {d[1] / d[0] if d[0] else float('inf'):.3f} (expected 4)"


def b_alpha_everywhere(m):
    """U / alpha0^2 independent of alpha0 at w0 != 1 (kills a dependence on alpha0 w0^3)."""
    base = m.cp_energy(5.1, 0.37, 1.0)
    rs = [m.cp_energy(5.1, 0.37, a) / a**2 / base for a in (0.1, 2.0, 7.0)]
    return all(abs(x - 1) < 1e-9 for x in rs), f"ratios {rs}"


BLIND = [
    ("attractive at every separation", b_negative),
    ("proportional to alpha0^2", b_alpha_squared),
    ("dimensional scaling U(lam r, w0/lam, lam^3 alpha0) = U/lam", b_dimensions),
    ("log-slopes -6 (near) and -7 (far)", b_slopes),
    ("far and near coefficients agree with cp_energy's limits", b_limits_agree),
    ("retardation weakens the interaction monotonically", b_crossover_monotone),
    ("far zone approached with a 1/rho^2 deficit", b_far_approach),
    ("near zone approached with a rho^2 deficit", b_near_approach),
    ("U / alpha0^2 independent of alpha0 at w0 != 1", b_alpha_everywhere),
]
