"""Orchestrator's reference for the finite-eps fourth-order energy, a = w0 = alpha0 = 1 (units 1/length), exponential damping
exp(-eps (k+q)) on the two exchanged photons. Separable form of the denominator sum, 1/(k+q) = int ds e^{-s(k+q)}."""
import math
from scipy.integrate import quad

def Af(k, rho): x = k * rho; return 2 * (math.sin(x) - x * math.cos(x)) / rho**3
def Bf(k, rho): x = k * rho; return ((x * x - 1) * math.sin(x) + x * math.cos(x)) / rho**3

def Iint(fn, g, eps, rho):
    L = 45.0 / eps
    f = lambda k: fn(k, rho) * g(k) * math.exp(-eps * k)
    n = max(1, int(L * rho / math.pi / 3))
    pts = [i * L / n for i in range(n + 1)]
    return sum(quad(f, a, b, epsabs=1e-15, epsrel=1e-12, limit=200)[0] for a, b in zip(pts, pts[1:]))

def F(rho, eps):
    tot = 0.0
    for X, c in ((Af, 1.0), (Bf, 2.0)):
        I1 = Iint(X, lambda k: (2 * k + 6) / (1 + k) ** 2, eps, rho)
        I0 = Iint(X, lambda k: 1 / (1 + k), eps, rho)
        inner = lambda s: Iint(X, lambda k: math.exp(-s * k) / (1 + k) ** 2, eps, rho) * Iint(X, lambda k: math.exp(-s * k) / (1 + k), eps, rho)
        S = quad(inner, 0, 30.0, epsabs=1e-13, epsrel=1e-10, limit=100)[0]
        tot += c * (I1 * I0 + 4 * S)
    return -tot / (4 * math.pi**2)
