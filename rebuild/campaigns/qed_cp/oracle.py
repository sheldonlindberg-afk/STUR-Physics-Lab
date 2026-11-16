"""Hidden oracle for the Casimir-Polder campaign.
Far zone: U = -23 hbar c alpha1 alpha2 / (4 pi r^7) (Casimir and Polder 1948), near zone: London, -(3/4) w0 alpha0^2 / r^6.
Crossover: the repository's own imaginary-frequency route, U = -(1/2 pi) int dxi alpha(i xi)^2 Tr G.G with
alpha(i xi) = alpha0 w0^2/(w0^2 + xi^2) and Tr G.G = 2 e^(-2u)(3 + 6u + 5u^2 + 2u^3 + u^4)/r^6, u = xi r (src/casimir_diamonds.py P2-P3);
it is a different route from the builders' mandatory perturbation theory, so agreement is evidence of both."""
import math
from scipy.integrate import quad

FAR, NEAR = 23 / (4 * math.pi), 0.75
LINT_TARGETS = [FAR, 1.8302, 1.83]


def reference(r, w0, alpha0):
    f = lambda xi: (alpha0 * w0**2 / (w0**2 + xi**2)) ** 2 * 2 * math.exp(-2 * xi * r) * (3 + 6 * xi * r + 5 * (xi * r) ** 2 + 2 * (xi * r) ** 3 + (xi * r) ** 4) / r**6
    return -quad(f, 0, math.inf, limit=400)[0] / (2 * math.pi)


def cross(rw):
    def f(m):
        v, ref = m.cp_energy(rw, 1.0, 1.0), reference(rw, 1.0, 1.0)
        return abs(v / ref - 1) < 2e-4, f"derived {v:.6e}, reference {ref:.6e} ({100 * (v / ref - 1):+.4f}%)"
    return f


ORACLE = [
    ("far-zone coefficient 23/(4 pi)", lambda m: (abs(m.far_coefficient() / FAR - 1) < 1e-4, f"derived {m.far_coefficient():.6f}, target {FAR:.6f}")),
    ("near-zone coefficient 3/4 (London)", lambda m: (abs(m.near_coefficient() / NEAR - 1) < 1e-4, f"derived {m.near_coefficient():.6f}")),
] + [(f"U(r w0 = {rw}) against the imaginary-frequency route", cross(rw)) for rw in (0.05, 0.5, 1.0, 3.0, 20.0)]
