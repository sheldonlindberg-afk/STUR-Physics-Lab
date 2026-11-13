"""casimir: the electromagnetic background (SPEC.md section 4).

Derivations and second routes: DERIVATION_casimir.md. Numerics via toolkit only.
"""
import math
from fractions import Fraction

import inputs
import toolkit

PROVENANCE = {
    "sphere_K": ("derived", "Laplace: Phi_in = -B r cos, Phi_out = -E0 r cos + A cos/r^2; continuity and eps d_r Phi"
                            " at R give a + b = 1, 2a - eps b = -1 (a = A/E0R^3, b = B/E0), solved by exact"
                            " Gaussian elimination; K = a. Checked against bound-charge route (eps-1) b/3"),
    "green_tensor": ("derived", "G_ij = (k^2 delta_ij - d_i d_j) e^{-kr}/r, which solves (lap - k^2)G = 0 for r > 0;"
                                " the polynomials (1+u+u^2), (3+3u+u^2) are produced symbolically by term-by-term"
                                " differentiation of e^{-kr} k^p r^q monomials (_green_polys)"),
    "cp_integral": ("derived", "Tr G.G r^6 e^{2u} from the polynomial matrix a delta - b n n, n = (2,3,6)/7 exact;"
                               " int u^n e^{-2u} = n!/2^{n+1} (parts); summed term by term in Fractions"),
    "cp_energy": ("quoted", "Casimir & Polder, Phys. Rev. 73 (1948) 360: U = -(hbar/2pi) int dxi a1 a2 Tr G.G,"
                            " a = K R^3 (units 4 pi eps0); with xi = c u/r this is"
                            " -(hbar c/pi) cp_integral() K1 K2 R1^3 R2^3 / r^7"),
    "diamond_radius": ("derived", "m = rho (4/3) pi R^3, rho = inputs.RHO_DIAMOND at call time"),
    "casimir_safe_gap": ("derived", "phase = (tau/hbar)[-2U(g) + 2U(sqrt(g^2+dx^2))] for U = cp_energy (K from"
                                    " sphere_K(inputs.EPS_DIAMOND), R from diamond_radius) and U = -G m^2/r;"
                                    " ratio strictly decreasing (geometric sum), tau- and m-free; unique root"
                                    " by toolkit.bisect on ln ratio - ln fraction in [g0, 7^(1/6) g0]"),
}


# ------------------------------------------------------------------------------------------
# 1. dielectric sphere
# ------------------------------------------------------------------------------------------
def _solve2(M, rhs):
    """Gaussian elimination (with pivoting on the first column) for a 2x2 system; exact for Fractions."""
    (a11, a12), (a21, a22) = M
    r1, r2 = rhs
    if abs(a21) > abs(a11):
        a11, a12, r1, a21, a22, r2 = a21, a22, r2, a11, a12, r1
    l = a21 / a11
    a22 -= l * a12
    r2 -= l * r1
    y = r2 / a22
    x = (r1 - a12 * y) / a11
    return x, y


def _sphere_coeffs(eps):
    """(a, b) = (A/(E0 R^3), B/E0) from continuity of Phi and of eps d_r Phi at r = R (R = 1 units)."""
    if isinstance(eps, int):
        eps = Fraction(eps)
    one = eps / eps                       # 1 in eps's number type (Fraction or float)
    # continuity:  -b = -1 + a           ->  a + b = 1
    # eps d_r:     -eps b = -1 - 2a      ->  2a - eps b = -1
    return _solve2([[one, one], [2 * one, -eps]], [one, -one])


def sphere_K(eps):
    """alpha/(4 pi eps0 R^3) of a dielectric sphere, from Laplace's equation."""
    a, _ = _sphere_coeffs(eps)
    return a


# ------------------------------------------------------------------------------------------
# 2. Green tensor: symbolic derivation of its two polynomials
# ------------------------------------------------------------------------------------------
def _d_dr(fn):
    """d/dr of e^{-kr} sum c_{pq} k^p r^q (dict {(p, q): c})."""
    out = {}
    for (p, q), c in fn.items():
        if q:
            out[(p, q - 1)] = out.get((p, q - 1), 0) + c * q
        out[(p + 1, q)] = out.get((p + 1, q), 0) - c
    return {k: v for k, v in out.items() if v}


def _add(*terms):
    out = {}
    for s, fn in terms:
        for k, v in fn.items():
            out[k] = out.get(k, 0) + s * v
    return {k: v for k, v in out.items() if v}


def _shift(fn, dp, dq):
    return {(p + dp, q + dq): v for (p, q), v in fn.items()}


def _to_u_poly(fn):
    """r^3 e^{kr} * fn must be a polynomial in u = k r: every monomial k^p r^q with q + 3 = p."""
    deg = max(p for p, _ in fn)
    poly = [Fraction(0)] * (deg + 1)
    for (p, q), v in fn.items():
        if q + 3 != p:
            raise ArithmeticError("Green tensor term is not a function of u alone")
        poly[p] += v
    return poly


def _green_polys():
    """(a(u), b(u)) with G = e^{-u}/r^3 [a delta - b n n], from G = (k^2 delta - d_i d_j) e^{-kr}/r.

    d_i d_j f = (f'/r) delta_ij + (f'' - f'/r) n_i n_j, so a = k^2 f - f'/r and b = f'' - f'/r."""
    f = {(0, -1): Fraction(1)}
    f1 = _d_dr(f)
    f2 = _d_dr(f1)
    a = _add((1, _shift(f, 2, 0)), (-1, _shift(f1, 0, -1)))
    b = _add((1, f2), (-1, _shift(f1, 0, -1)))
    return _to_u_poly(a), _to_u_poly(b)


def _peval(poly, u):
    s = 0.0
    for c in reversed(poly):
        s = s * u + float(c)
    return s


def green_tensor(x, y, z, k):
    """Dipole Green tensor at imaginary frequency, k = xi/c (SPEC.md section 4)."""
    a, b = _green_polys()
    r = math.sqrt(x * x + y * y + z * z)
    u = k * r
    n = (x / r, y / r, z / r)
    pre = math.exp(-u) / r ** 3
    A, B = _peval(a, u), _peval(b, u)
    return [[pre * ((A if i == j else 0.0) - B * n[i] * n[j]) for j in range(3)] for i in range(3)]


# ------------------------------------------------------------------------------------------
# 3. exact fluctuation integral
# ------------------------------------------------------------------------------------------
def _pmul(p, q):
    out = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return out


def _padd(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)]


def _trace_poly():
    """h(u) = Tr[G.G] r^6 e^{2u} / 2 as Fraction coefficients, from the 3x3 polynomial matrix
    a delta_ij - b n_i n_j with the exact rational unit vector n = (2, 3, 6)/7."""
    a, b = _green_polys()
    n = [Fraction(2, 7), Fraction(3, 7), Fraction(6, 7)]
    assert sum(c * c for c in n) == 1
    M = [[_padd(a if i == j else [Fraction(0)], [-c * n[i] * n[j] for c in b]) for j in range(3)] for i in range(3)]
    tr = [Fraction(0)]
    for i in range(3):
        for j in range(3):
            tr = _padd(tr, _pmul(M[i][j], M[j][i]))
    h = [c / 2 for c in tr]
    while len(h) > 1 and h[-1] == 0:
        h.pop()
    return h


def cp_integral():
    """int_0^oo Tr[G.G] r^6 / 2 du, exactly: sum_n h_n n!/2^{n+1}."""
    h = _trace_poly()
    total, In = Fraction(0), Fraction(1, 2)       # I_0 = int e^{-2u} du = 1/2
    for nn, c in enumerate(h):
        if nn:
            In = In * nn / 2                      # I_n = (n/2) I_{n-1}
        total += c * In
    return total


# ------------------------------------------------------------------------------------------
# 4. Casimir-Polder energy
# ------------------------------------------------------------------------------------------
def cp_energy(R1, R2, K1, K2, r):
    """Retarded Casimir-Polder energy (J) of two spheres with constant alpha_i = K_i R_i^3 (4 pi eps0)."""
    I = float(cp_integral())
    return -(inputs.HBAR * inputs.C_LIGHT / math.pi) * I * K1 * K2 * R1 ** 3 * R2 ** 3 / r ** 7


# ------------------------------------------------------------------------------------------
# 5, 6. diamonds and the safe gap
# ------------------------------------------------------------------------------------------
def diamond_radius(m):
    """Radius (m) of a diamond sphere of mass m (kg)."""
    return (3 * m / (4 * math.pi * inputs.RHO_DIAMOND)) ** (1 / 3)


def _phase(U, gap, dx, tau):
    d = math.sqrt(gap * gap + dx * dx)
    return (tau / inputs.HBAR) * (-U(gap) - U(gap) + U(d) + U(d))


def casimir_safe_gap(m, dx, tau, fraction):
    """Smallest gap (m) with |Casimir phase| <= fraction |gravity phase|, parallel geometry."""
    R = diamond_radius(m)
    K = sphere_K(inputs.EPS_DIAMOND)
    G = inputs.G_NEWTON

    def Uc(r):
        return cp_energy(R, R, K, K, r)

    def Ug(r):
        return -G * m * m / r

    def F(lng):
        g = math.exp(lng)
        return math.log(abs(_phase(Uc, g, dx, tau))) - math.log(fraction * abs(_phase(Ug, g, dx, tau)))

    C = -cp_energy(R, R, K, K, 1.0)               # U_c = -C / r^7
    g0 = (C / (fraction * G * m * m)) ** (1 / 6)
    lo, hi = math.log(g0), math.log(g0) + math.log(7) / 6
    while F(lo) <= 0:
        lo -= math.log(2)
    while F(hi) >= 0:
        hi += math.log(2)
    return math.exp(toolkit.bisect(F, lo, hi))


# ------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("== 1. sphere K ==")
    for e in (Fraction(57, 10), Fraction(3), Fraction(1), Fraction(10 ** 9)):
        a, b = _sphere_coeffs(e)
        print(f" eps={e}: K = {a}  bound-charge route (eps-1) b/3 = {(e - 1) * b / 3}  equal: {a == (e - 1) * b / 3}")
    print(f" float eps = inputs.EPS_DIAMOND: K = {sphere_K(inputs.EPS_DIAMOND)!r}")

    print("== 2. Green tensor ==")
    print(" polynomials a(u), b(u) from (k^2 delta - dd) e^{-kr}/r:", *[[str(c) for c in p] for p in _green_polys()])
    pt, k, h = (0.37, -0.29, 0.41), 1.7, 1e-3
    G0 = green_tensor(*pt, k)

    def lap(i, j, hs):
        tot = 0.0
        for d in range(3):
            p1, p2 = list(pt), list(pt)
            p1[d] += hs
            p2[d] -= hs
            tot += (green_tensor(*p1, k)[i][j] - 2 * G0[i][j] + green_tensor(*p2, k)[i][j]) / (hs * hs)
        return tot
    res = max(abs((4 * lap(i, j, h / 2) - lap(i, j, h)) / 3 - k * k * G0[i][j]) for i in range(3) for j in range(3))
    print(f" (lap - k^2) G residual: {res:.2e}")

    def fsc(x, y, z):
        r = math.sqrt(x * x + y * y + z * z)
        return math.exp(-k * r) / r
    sc0, worst = max(abs(G0[i][j]) for i in range(3) for j in range(3)), 0.0
    for i in range(3):
        for j in range(3):
            def shifted(si, sj):
                p = list(pt)
                p[i] += si
                p[j] += sj
                return fsc(*p)

            def dd(hs):
                return (shifted(hs, hs) - shifted(hs, -hs) - shifted(-hs, hs) + shifted(-hs, -hs)) / (4 * hs * hs)
            Gfd = (k * k * fsc(*pt) if i == j else 0.0) - (4 * dd(h / 2) - dd(h)) / 3
            worst = max(worst, abs(Gfd - G0[i][j]) / sc0)
    print(f" (k^2 delta - d_i d_j) e^(-kr)/r by Richardson finite differences vs closed form: {worst:.2e}")
    print(f" static limit k = 0 at (0,0,2): Gxx = {green_tensor(0, 0, 2.0, 0)[0][0]}, Gzz = {green_tensor(0, 0, 2.0, 0)[2][2]}")

    print("== 3. fluctuation integral ==")
    hp = _trace_poly()
    print(" h(u) = Tr G.G r^6 e^{2u}/2 coefficients:", [str(c) for c in hp])
    I = cp_integral()

    def quad(step, umax=60.0):
        nn = int(umax / step) + 1
        ys = []
        for i in range(nn):
            u = i * step
            Gm = green_tensor(0.3, -0.4, math.sqrt(1 - 0.25), u) if u else green_tensor(0.3, -0.4, math.sqrt(0.75), 0.0)
            ys.append(sum(Gm[a][b] * Gm[b][a] for a in range(3) for b in range(3)) / 2)
        return toolkit.trapezoid(ys, step)
    q1, q2 = quad(2e-3), quad(1e-3)
    print(f" exact: {I} = {float(I)!r}; trapezoid (Richardson): {(4 * q2 - q1) / 3!r}")

    print("== 4. Casimir-Polder energy ==")
    R0, Kd, r0 = 1e-6, sphere_K(inputs.EPS_DIAMOND), 1e-4
    closed = cp_energy(R0, R0, Kd, Kd, r0)
    a1 = Kd * R0 ** 3
    step = 1e-3
    ys = []
    for i in range(int(60 / step) + 1):
        xi = i * step * inputs.C_LIGHT / r0
        Gm = green_tensor(0.0, 0.0, r0, xi / inputs.C_LIGHT)
        ys.append(sum(Gm[a][b] * Gm[b][a] for a in range(3) for b in range(3)))
    direct = -(inputs.HBAR / (2 * math.pi)) * a1 * a1 * toolkit.trapezoid(ys, step * inputs.C_LIGHT / r0)
    print(f" closed form {closed!r} J; direct xi-quadrature of the CP formula {direct!r} J")

    print("== 5. diamond radius ==")
    Rm = diamond_radius(inputs.DESIGN_A_MASS)
    print(f" design A: R = {Rm!r} m; back-substituted mass / m = {4 / 3 * math.pi * Rm ** 3 * inputs.RHO_DIAMOND / inputs.DESIGN_A_MASS!r}")

    print("== 6. energies and safe gap ==")
    mA, r200 = inputs.DESIGN_A_MASS, 200e-6
    Uc = cp_energy(Rm, Rm, Kd, Kd, r200)
    Ug = -inputs.G_NEWTON * mA * mA / r200
    Cc = (inputs.HBAR * inputs.C_LIGHT / math.pi) * float(I) * Kd * Kd * Rm ** 6
    print(f" design A at 200 um: U_Casimir/U_gravity = {Uc / Ug!r}; closed form C/(G m^2 r^6) ="
          f" {Cc / (inputs.G_NEWTON * mA * mA * r200 ** 6)!r}")
    m0, dx0, tau0, fr0 = inputs.GAP_BASELINE_MASS, inputs.GAP_BASELINE_DX, inputs.GAP_BASELINE_TAU, inputs.GAP_FRACTION
    g = casimir_safe_gap(m0, dx0, tau0, fr0)
    R0 = diamond_radius(m0)
    C0 = (inputs.HBAR * inputs.C_LIGHT / math.pi) * float(I) * Kd * Kd * R0 ** 6
    d = math.sqrt(g * g + dx0 * dx0)
    geo = C0 / (inputs.G_NEWTON * m0 * m0) * sum(g ** -j * d ** (j - 6) for j in range(7))
    print(f" baseline safe gap = {g!r} m ({g * 1e6:.6f} um)")
    print(f"  ratio at the gap by geometric-sum closed form = {geo!r} (fraction {fr0})")
    print(f"  m x10, tau x3.6: {casimir_safe_gap(10 * m0, dx0, 3.6 * tau0, fr0)!r} m")
    gnear = (C0 / (fr0 * inputs.G_NEWTON * m0 * m0)) ** (1 / 6)
    print(f"  bracket from limits: [{gnear!r}, {gnear * 7 ** (1 / 6)!r}] m")
