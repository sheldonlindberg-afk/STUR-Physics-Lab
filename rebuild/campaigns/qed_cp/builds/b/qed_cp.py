"""Casimir-Polder energy of two identical isotropic two-level-type atoms from 4th-order RSPT (see DERIVATION.md)."""
import itertools
import math
import mpmath as mp
import sympy as sp

PROVENANCE = {
    "cp_energy": ("derived", "12 time-ordered 4th-order diagrams (enumerated), angle/polarisation sums, Abel-damped k,q integrals via 1/(k+q)=int ds e^{-(k+q)s}"),
    "far_coefficient": ("derived", "k,q<<w0 limit of the same double integral, exact Laplace transforms (sympy)"),
    "near_coefficient": ("derived", "k,q>>w0 limit of the same double integral, Abel integrals (sympy)"),
}

_DPS = 45


# ---------------------------------------------------------------- perturbation sum (symbolic)
def _diagram_sum():
    """S(k,q) = sum over the 12 time-ordered diagrams of 1/(D1 D2 D3); returns (sympy expr, count)."""
    k, q, a = sp.symbols("k q a", positive=True)
    tot, n = 0, 0
    for Apos in itertools.combinations(range(4), 2):
        atom = ["A" if i in Apos else "B" for i in range(4)]
        for pairing in [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]:
            if all(atom[p] != atom[s] for p, s in pairing):
                n += 1
                mom = {pairing[0]: k, pairing[1]: q}
                exc = {"A": 0, "B": 0}
                D = 1
                for slot in range(3):
                    exc[atom[slot]] ^= 1
                    E = a * (exc["A"] + exc["B"])
                    for pr, en in mom.items():
                        if pr[0] <= slot < pr[1]:
                            E += en
                    D *= E
                tot += 1 / D
    return sp.together(tot), n, (k, q, a)


# ---------------------------------------------------------------- one-photon integrals
def _H(m, n, w, a):
    """int_0^inf k^m (a+k)^(-n) e^{-k w} dk, Re w >= 0, w != 0 (a>0)."""
    def L(p):  # p>=1
        res = mp.exp(a * w) * mp.e1(a * w)
        for pp in range(1, p):
            res = (a ** (-pp) - w * res) / pp
        return res

    def H0(p):  # int (a+k)^(-p) e^{-kw}
        if p >= 1:
            return L(p)
        P = -p
        return sum(mp.binomial(P, i) * a ** (P - i) * mp.factorial(i) / w ** (i + 1) for i in range(P + 1))

    return sum(mp.binomial(m, j) * (-a) ** (m - j) * H0(n - j) for j in range(m + 1))


def _M(X, m_f, n_f, s, r, a):
    """int dk k^3 X(kr) k^(m_f)(a+k)^(-n_f) e^{-ks}, X in 'A','B' (Abel regularised at s=0)."""
    w = mp.mpf(s) - 1j * r
    if X == "A":
        val = 2 / r**3 * (_H(m_f, n_f, w, a) - 1j * r * _H(m_f + 1, n_f, w, a))
    else:
        val = 1 / r**3 * (r**2 * _H(m_f + 2, n_f, w, a) - _H(m_f, n_f, w, a) + 1j * r * _H(m_f + 1, n_f, w, a))
    return val.imag


def _u(rho, tol_refine=1):
    """U / (alpha0^2 w0^7) as a function of rho = r w0 (a = 1)."""
    with mp.workdps(_DPS * tol_refine):
        a = mp.mpf(1)
        r = mp.mpf(rho)
        d4 = mp.mpf(1) / 4  # d^4 = alpha0^2 a^2 / 4 with alpha0 = 1
        tot = mp.mpf(0)
        for X, wX in (("A", 1), ("B", 2)):
            g1 = lambda s: _M(X, 0, 1, s, r, a)
            sep = (2 / a) * _M(X, 1, 2, 0, r, a) * g1(0) + 6 * _M(X, 0, 2, 0, r, a) * g1(0)
            integrand = lambda s: 4 * a * _M(X, 0, 2, s, r, a) * g1(s)
            pts = sorted({mp.mpf(0), 1 / a, r, 10 * r, 10 / a})
            integ = mp.quad(integrand, pts + [mp.inf])
            tot += wX * (sep + integ)
        return float(-d4 / mp.pi**2 * tot)


def cp_energy(r, w0, alpha0):
    """U(r) for two identical atoms (hbar=c=1, Gaussian); U = alpha0^2 w0^7 u(r w0)."""
    return alpha0**2 * w0**7 * _u(float(r) * float(w0))


# ---------------------------------------------------------------- limits
def _x_functions():
    x, s, eps = sp.symbols("x s epsilon", positive=True)
    xA3 = 2 * (sp.sin(x) - x * sp.cos(x))                   # x^3 A(x)
    xB3 = (x**2 - 1) * sp.sin(x) + x * sp.cos(x)            # x^3 B(x)
    return x, s, eps, xA3, xB3


def far_coefficient():
    x, s, eps, xA3, xB3 = _x_functions()
    G = [sp.simplify(sp.integrate(sp.expand(f * sp.exp(-s * x)), (x, 0, sp.oo), conds="none")) for f in (xA3, xB3)]
    integrand = sp.simplify(G[0] ** 2 + 2 * G[1] ** 2)
    return float(sp.integrate(integrand, (s, 0, sp.oo)) / sp.pi**2)


def near_coefficient():
    x, s, eps, xA3, xB3 = _x_functions()
    # int x^2 X(x) dx with Abel damping e^{-eps x}, eps -> 0
    IA = sp.limit(sp.integrate(sp.expand(xA3 / x * sp.exp(-eps * x)), (x, 0, sp.oo)), eps, 0, "+")
    IB = sp.limit(sp.integrate(sp.expand(xB3 / x * sp.exp(-eps * x)), (x, 0, sp.oo)), eps, 0, "+")
    # U -> -(2 d^4 /(pi^2 a r^6)) [IA^2 + 2 IB^2], d^4 = alpha0^2 a^2/4  =>  D = (1/(2 pi^2)) [IA^2 + 2 IB^2]
    return float(sp.simplify((IA**2 + 2 * IB**2) / (2 * sp.pi**2)))


def _brute(rho, eps, n=1500, kmax=None):
    """Second route: direct 2D Riemann/trapezoid quadrature of the double k,q integral with damping e^{-eps(k+q)}."""
    import numpy as np
    kmax = kmax or 40.0 / eps
    k = (np.arange(n * 40) + 0.5) * (kmax / (n * 40))
    dk = kmax / (n * 40)
    x = k * rho
    A = 2 * (np.sin(x) - x * np.cos(x)) / rho**3
    B = ((x**2 - 1) * np.sin(x) + x * np.cos(x)) / rho**3
    damp = np.exp(-eps * k)
    tot = 0.0
    kk = k[:, None]
    step = 400
    for i in range(0, len(k), step):
        ki = k[i:i + step][:, None]
        qq = k[None, :]
        S = 2 * (2 + 3 * (ki + qq) + ki * (ki + qq)) / ((1 + ki) ** 2 * (1 + qq) * (ki + qq))
        W = (A[i:i + step, None] * A[None, :] + 2 * B[i:i + step, None] * B[None, :]) * S
        tot += np.sum(W * damp[i:i + step, None] * damp[None, :])
    return -0.25 / np.pi**2 * tot * dk * dk


if __name__ == "__main__":
    S, n, syms = _diagram_sum()
    print("diagrams:", n, " S =", sp.factor(S))
    print("far C =", far_coefficient(), " near D =", near_coefficient())
    for rho in (0.01, 1.0, 1e3):
        print("rho", rho, "u", _u(rho), "u at higher precision", _u(rho, 2))
    vals = [_brute(1.0, e, n=100) for e in (0.1, 0.05, 0.025)]
    print("brute 2D rho=1, eps=0.1,0.05,0.025:", vals)
    r1 = [2 * vals[i + 1] - vals[i] for i in range(2)]
    print("Richardson (linear in eps):", r1, " second:", (4 * r1[1] - r1[0]) / 3, " vs main route", _u(1.0))
