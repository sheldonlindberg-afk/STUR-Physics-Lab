"""Casimir-Polder energy of two identical isotropic two-level-type atoms from 4th-order RSPT (see DERIVATION.md)."""
import itertools
import math
import mpmath as mp
import sympy as sp

PROVENANCE = {
    "cp_energy": ("derived", "12 time-ordered 4th-order diagrams (enumerated), angle/polarisation sums, Abel-damped k,q integrals via 1/(k+q)=int ds e^{-(k+q)s}"),
    "far_coefficient": ("derived", "k,q<<w0 limit of the same double integral, exact Laplace transforms (sympy)"),
    "denominator_sum": ("derived", "explicit enumeration of the 24 four-vertex orderings (toggle atom excitation / photon occupation), sum of 1/(E1E2E3), divided by 2"),
    "damped_energy": ("derived", "same double integral as cp_energy with e^{-eps(k+q)}: absolutely convergent, evaluated at finite eps via s-representation shifted to s>=eps; no extrapolation"),
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


def _u(rho, tol_refine=1, eps=0.0):
    """U / (alpha0^2 w0^7) as a function of rho = r w0 (a = 1); eps = damping length (units 1/w0), 0 = Abel limit."""
    # working precision grows for rho >> 1e4: the 1/r^3-per-photon cancellations eat ~6 digits per decade
    extra = int(6 * max(0.0, math.log10(rho) - 4.0))
    with mp.workdps(_DPS * tol_refine + extra):
        a = mp.mpf(1)
        r = mp.mpf(rho)
        d4 = mp.mpf(1) / 4  # d^4 = alpha0^2 a^2 / 4 with alpha0 = 1
        tot = mp.mpf(0)
        for X, wX in (("A", 1), ("B", 2)):
            g1 = lambda s: _M(X, 0, 1, s, r, a)
            e0 = mp.mpf(eps)
            sep = (2 / a) * _M(X, 1, 2, e0, r, a) * g1(e0) + 6 * _M(X, 0, 2, e0, r, a) * g1(e0)
            integrand = lambda s: 4 * a * _M(X, 0, 2, s, r, a) * g1(s)
            pts = sorted({e0} | {p for p in (1 / a, r, 10 * r, 10 / a) if p > e0})
            integ = mp.quad(integrand, pts + [mp.inf])
            tot += wX * (sep + integ)
        return float(-d4 / mp.pi**2 * tot)


def _S_decomp(k, q, a=1.0):
    """The three terms used inside _u: f1 g1 + f2 g2 (separable) + f4 g4/(k+q) (the ds-integral term)."""
    g1 = 1 / (a + q)
    return (2 * k / (a * (a + k) ** 2)) * g1 + 6 / (a + k) ** 2 * g1 + (4 * a / (a + k) ** 2) * g1 / (k + q)


def _S_independent(k, q, a=1.0):
    """Independent enumeration: all strings of 4 vertices (atom, photon label, create/annihilate) with explicit
    photon occupation and atom excitation tracking; labelled photons (k, q) count each physical diagram twice."""
    verts = [(at, ph, op) for at in "AB" for ph in (0, 1) for op in ("c", "d")]
    en = (k, q)
    total, count = 0.0, 0
    for seq in itertools.product(verts, repeat=4):
        if sorted(v[0] for v in seq) != ["A", "A", "B", "B"]:
            continue
        occ, exc, ok, D, ends = [0, 0], {"A": 0, "B": 0}, True, 1.0, {0: [], 1: []}
        for i, (at, ph, op) in enumerate(seq):
            if op == "c":
                ok = ok and occ[ph] == 0
                occ[ph] += 1
            else:
                ok = ok and occ[ph] == 1
                occ[ph] -= 1
            ends[ph].append(at)
            exc[at] ^= 1
            if not ok:
                break
            if i < 3:
                D *= a * (exc["A"] + exc["B"]) + occ[0] * en[0] + occ[1] * en[1]
        if not ok or occ != [0, 0] or exc != {"A": 0, "B": 0}:
            continue
        if any(sorted(ends[ph]) != ["A", "B"] for ph in (0, 1)):   # each photon joins A and B
            continue
        total += 1.0 / D
        count += 1
    return total / 2, count


def denominator_sum(k, q, a, b):
    """SPEC 3b: sum over the 24 orderings of the events (A,k),(A,q),(B,k),(B,q) of 1/(E1 E2 E3), divided by 2.
    E_n = energy of the state after n events; each event toggles its atom's excitation (a or b) and its photon's occupation (k or q)."""
    events = [("A", 0), ("A", 1), ("B", 0), ("B", 1)]
    en = (k, q)
    tot = 0.0
    for order in itertools.permutations(events):
        exc = {"A": 0, "B": 0}
        occ = [0, 0]
        D = 1.0
        for atom, ph in order[:3]:
            exc[atom] ^= 1
            occ[ph] ^= 1
            D *= a * exc["A"] + b * exc["B"] + occ[0] * en[0] + occ[1] * en[1]
        tot += 1.0 / D
    return tot / 2


def damped_energy(r, w0, alpha0, eps):
    """U with every photon integrand multiplied by exp(-eps (k+q)); finite eps, no extrapolation. U = alpha0^2 w0^7 u(r w0; eps w0)."""
    return alpha0**2 * w0**7 * _u(float(r) * float(w0), 1, float(eps) * float(w0))


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


def _brute(rho, eps, n=1500, kmax=None, shape="exp"):
    """Second route: direct 2D Riemann/trapezoid quadrature of the double k,q integral with damping e^{-eps(k+q)}."""
    import numpy as np
    kmax = kmax or (40.0 if shape == "exp" else 8.0) / eps
    k = (np.arange(n * 40) + 0.5) * (kmax / (n * 40))
    dk = kmax / (n * 40)
    x = k * rho
    A = 2 * (np.sin(x) - x * np.cos(x)) / rho**3
    B = ((x**2 - 1) * np.sin(x) + x * np.cos(x)) / rho**3
    damp = np.exp(-eps * k) if shape == "exp" else np.exp(-(eps * k) ** 2)
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
    worst = 0.0
    for kk, qq in ((0.3, 1.7), (2.2, 0.15), (4.1, 3.3), (0.9, 0.9), (0.05, 5.0)):
        Si, cnt = _S_independent(kk, qq)
        Su = 0.5 * (_S_decomp(kk, qq) + _S_decomp(qq, kk))
        worst = max(worst, abs(Si / Su - 1))
    print("independent 4-vertex enumeration: labelled sequences =", cnt, "(expect 2 x 12 = 24); max rel diff vs _u terms:", worst)
    dmax = max(abs(denominator_sum(kk, qq, 1.0, 1.0) / (0.5 * (_S_decomp(kk, qq) + _S_decomp(qq, kk))) - 1) for kk, qq in ((0.3, 1.7), (2.2, 0.15), (4.1, 3.3)))
    print("denominator_sum(a=b=1) vs symmetrised _S_decomp: max rel diff", dmax, "; a!=b example", denominator_sum(0.7, 1.9, 1.3, 0.6))
    for rho_, e_ in ((0.3, 0.25), (1.0, 0.5), (3.0, 1.0)):
        dd = damped_energy(rho_, 1.0, 1.0, e_)
        print("damped_energy rho", rho_, "eps", e_, dd, "brute 2D (n=200):", float(_brute(rho_, e_, n=200)), "rel diff", float(_brute(rho_, e_, n=200)) / dd - 1)
    print("damped/cp - 1 at rho=1, eps=1e-4, 1e-5 (expect -3.35 eps):", [damped_energy(1.0, 1.0, 1.0, e_) / cp_energy(1.0, 1.0, 1.0) - 1 for e_ in (1e-4, 1e-5)])
    print("far C =", far_coefficient(), " near D =", near_coefficient())
    for rho in (0.01, 1.0, 1e3):
        print("rho", rho, "u", _u(rho), "u at higher precision", _u(rho, 2))
    for shape, order in (("exp", 1), ("gauss", 2)):
        for rho in (0.5, 1.0, 3.0):
            vals = [_brute(rho, e, n=100, shape=shape) for e in (0.1, 0.05, 0.025)]
            if order == 1:
                r1 = [2 * vals[j + 1] - vals[j] for j in range(2)]
                ext = (4 * r1[1] - r1[0]) / 3
            else:
                r1 = [(4 * vals[j + 1] - vals[j]) / 3 for j in range(2)]
                ext = (16 * r1[1] - r1[0]) / 15
            print("brute", shape, "rho", rho, "damped:", [float(v) for v in vals], "extrapolated:", float(ext), "main route:", _u(rho))
