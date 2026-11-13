"""Stage `casimir` (build 2026-11-b): the electromagnetic background of the diamond experiment.

Dielectric-sphere polarizability, the imaginary-frequency dipole Green tensor, the exact Casimir-Polder
fluctuation integral, the retarded Casimir-Polder energy (quoted fluctuation formula, allowed) and the
Casimir-safe gap. Derivations and second routes: DERIVATION_casimir.md (same directory); section numbers are
cited below. Units: SI; polarizabilities in units of 4 pi eps0 (a volume).
"""
import math
from fractions import Fraction

import inputs
import toolkit

PROVENANCE = {
    "sphere_K": ("derived", "Laplace's equation for a sphere in a uniform field: l = 1 ansatz, continuity of Phi and"
                            " eps d_r Phi give the 2x2 system a + K = 1, eps a - 2K = 1, solved by Cramer's rule;"
                            " K = (eps - 1)/(eps + 2) (DERIVATION section 1)"),
    "green_tensor": ("derived", "SPEC section 4 form e^(-u)/r^3 [(1+u+u^2) delta - (3+3u+u^2) n n], u = k r, shown"
                                " equal to (k^2 delta_ij - d_i d_j) e^(-k r)/r (section 2)"),
    "cp_integral": ("derived", "Tr G.G r^6/2 = e^(-2u) (3A^2 - 2AB + B^2)/2 by exact polynomial algebra, integrated"
                               " term by term with int u^n e^(-2u) du = n!/2^(n+1), in Fractions (section 3)"),
    "cp_energy": ("quoted", "Casimir-Polder fluctuation formula U = -(hbar/2 pi) int d xi alpha1 alpha2 Tr[G.G]"
                            " (Casimir and Polder, Phys. Rev. 73 (1948) 360; SPEC section 4), not derived; from it,"
                            " with constant alpha_i = K_i R_i^3 and xi = c u/r, U = -(hbar c/pi) cp_integral()"
                            " alpha1 alpha2 / r^7 is derived (section 4)"),
    "diamond_radius": ("derived", "uniform sphere, m = rho (4 pi/3) R^3 with rho = inputs.RHO_DIAMOND (section 5)"),
    "casimir_safe_gap": ("derived", "unique root (toolkit.bisect, derived bracket g0 < g < 7^(1/6) g0) of"
                                    " phi_Casimir/phi_gravity = fraction, parallel geometry; ratio ="
                                    " C/(G m^2) sum_j g^-(6-j) d^-j, strictly decreasing in g; gravity taken as"
                                    " -G m^2/r (section 6)"),
}

# The SPEC section 4 Green-tensor polynomials, lowest power first: A = 1 + u + u^2, B = 3 + 3u + u^2.
_A_COEFFS = (1, 1, 1)
_B_COEFFS = (3, 3, 1)
_BRACKET_PAD = 1e-9       # relative widening of the derived bracket against rounding at its ends (section 6)


# ------------------------------------------------------------------------------------------
# 1. dielectric sphere
# ------------------------------------------------------------------------------------------
def _sphere_solve(eps):
    """(a, K) from the boundary conditions at r = R: a + K = 1, eps a - 2K = 1 (Cramer's rule)."""
    if not isinstance(eps, float):
        eps = Fraction(eps)
    one = eps / eps if isinstance(eps, float) else Fraction(1)
    # matrix [[1, 1], [eps, -2]], right-hand side (1, 1)
    det = one * (-2) - one * eps
    a = (one * (-2) - one) / det
    K = (one - eps) / det
    return a, K


def sphere_K(eps):
    """alpha/(4 pi eps0 R^3) of a dielectric sphere of relative permittivity eps (Fraction in, Fraction out)."""
    return _sphere_solve(eps)[1]


# ------------------------------------------------------------------------------------------
# 2. Green tensor
# ------------------------------------------------------------------------------------------
def _polyval(coeffs, u):
    tot = 0
    for c in reversed(coeffs):
        tot = tot * u + c
    return tot


def green_tensor(x, y, z, k):
    """Dipole Green tensor at imaginary frequency xi = c k: 3x3 list, units 1/length^3."""
    pos = (x, y, z)
    r = math.sqrt(x * x + y * y + z * z)
    if r == 0:
        raise ValueError("green_tensor: undefined at r = 0")
    u = k * r
    pref = math.exp(-u) / r ** 3
    A, B = _polyval(_A_COEFFS, u), _polyval(_B_COEFFS, u)
    n = [p / r for p in pos]
    return [[pref * ((A if i == j else 0.0) - B * n[i] * n[j]) for j in range(3)] for i in range(3)]


# ------------------------------------------------------------------------------------------
# 3. fluctuation integral
# ------------------------------------------------------------------------------------------
def _polymul(p, q):
    out = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += Fraction(a) * b
    return out


def _trace_polynomial():
    """Coefficients of r^6 e^(2u) Tr[G.G] = 3A^2 - 2AB + B^2 (n n is a projector)."""
    AA, AB, BB = _polymul(_A_COEFFS, _A_COEFFS), _polymul(_A_COEFFS, _B_COEFFS), _polymul(_B_COEFFS, _B_COEFFS)
    return [3 * aa - 2 * ab + bb for aa, ab, bb in zip(AA, AB, BB)]


def cp_integral():
    """int_0^oo (1/2) r^6 Tr[G.G] du, exactly: sum_n c_n n!/2^(n+1) / 2."""
    return sum(c * Fraction(math.factorial(n), 2 ** (n + 1)) for n, c in enumerate(_trace_polynomial())) / 2


# ------------------------------------------------------------------------------------------
# 4. Casimir-Polder energy
# ------------------------------------------------------------------------------------------
def _cp_coefficient(R1, R2, K1, K2):
    """C in U = -C/r^7: (hbar c/pi) I alpha1 alpha2, alpha_i = K_i R_i^3."""
    I = cp_integral()
    return inputs.HBAR * inputs.C_LIGHT / math.pi * (I.numerator / I.denominator) * (K1 * R1 ** 3) * (K2 * R2 ** 3)


def cp_energy(R1, R2, K1, K2, r):
    """Retarded Casimir-Polder energy (J) of two spheres, radii R_i, K_i = alpha_i/(4 pi eps0 R_i^3), distance r."""
    return -_cp_coefficient(R1, R2, K1, K2) / r ** 7


# ------------------------------------------------------------------------------------------
# 5. diamond sphere
# ------------------------------------------------------------------------------------------
def diamond_radius(m):
    """Radius (m) of a uniform diamond sphere of mass m (kg)."""
    return (3 * m / (4 * math.pi * inputs.RHO_DIAMOND)) ** (1 / 3)


# ------------------------------------------------------------------------------------------
# 6. Casimir-safe gap
# ------------------------------------------------------------------------------------------
def _phase_ratio(gap, dx, strength):
    """|Casimir phase|/|gravity phase| = strength * sum_j gap^-(6-j) d^-j, strength = C/(G m^2); tau cancels."""
    a, b = 1 / gap, 1 / math.hypot(gap, dx)
    return strength * math.fsum(a ** (6 - j) * b ** j for j in range(7))


def _strength(m):
    R = diamond_radius(m)
    K = sphere_K(inputs.EPS_DIAMOND)
    return _cp_coefficient(R, R, K, K) / (inputs.G_NEWTON * m * m)


def casimir_safe_gap(m, dx, tau, fraction):
    """Smallest gap (m) with |Casimir phase| <= fraction |gravity phase|; parallel geometry, time tau (cancels)."""
    if not (m > 0 and fraction > 0 and tau > 0):
        raise ValueError("casimir_safe_gap: m, tau and fraction must be positive")
    s = _strength(m)
    g0 = (s / fraction) ** (1 / 6)                 # the dx >> gap limit; the dx << gap limit is 7^(1/6) g0
    lo, hi = g0 * (1 - _BRACKET_PAD), g0 * 7 ** (1 / 6) * (1 + _BRACKET_PAD)
    return toolkit.bisect(lambda g: _phase_ratio(g, dx, s) - fraction, lo, hi)


# ------------------------------------------------------------------------------------------
# self-check: second routes (DERIVATION_casimir.md)
# ------------------------------------------------------------------------------------------
if __name__ == "__main__":
    ok_all = True

    def show(label, main, second, ok):
        global ok_all
        ok_all = ok_all and ok
        print(f"{'ok  ' if ok else 'FAIL'} {label}: main = {main}, second route = {second}")

    def rel(a, b):
        return abs(a - b) / abs(b)

    # 1. K from the boundary conditions vs K = (eps - 1) a / 3 (polarization x volume)
    eps = Fraction(inputs.EPS_DIAMOND).limit_denominator(1000)
    a_in, K = _sphere_solve(eps)
    show("sphere_K(eps_diamond)", K, (eps - 1) * a_in / 3, K == (eps - 1) * a_in / 3)
    show("sphere_K(1)", sphere_K(Fraction(1)), 0, sphere_K(1) == 0)
    show("sphere_K float vs Fraction", sphere_K(float(eps)), float(K), rel(sphere_K(float(eps)), float(K)) < 1e-14)

    # 2. Green tensor vs (k^2 delta - d_i d_j) e^(-k r)/r by finite differences
    pt, k, h = (0.4, -0.3, 0.5), 1.5, 1e-3

    def g(p):
        rr = math.sqrt(sum(c * c for c in p))
        return math.exp(-k * rr) / rr

    def dd(i, j):
        def sh(si, sj):
            p = list(pt)
            p[i] += si * h
            p[j] += sj * h
            return g(p)
        if i == j:
            return (sh(1, 0) - 2 * g(pt) + sh(-1, 0)) / (h * h)
        return (sh(1, 1) - sh(1, -1) - sh(-1, 1) + sh(-1, -1)) / (4 * h * h)

    G = green_tensor(*pt, k)
    worst = max(abs(G[i][j] - ((k * k * g(pt) if i == j else 0.0) - dd(i, j))) for i in range(3) for j in range(3))
    scale = max(abs(G[i][j]) for i in range(3) for j in range(3))
    show("green_tensor vs (k^2 delta - dd) e^(-kr)/r, max rel. deviation", f"{scale:.6f} (scale)",
         f"{worst / scale:.2e}", worst / scale < 1e-5)

    # 3. cp_integral: eigenvalue route (exact) and numerical quadrature of Tr G.G from green_tensor
    I = cp_integral()
    lam_t = [Fraction(c) for c in _A_COEFFS]                              # transverse eigenvalue A (twice)
    lam_l = [Fraction(a - b) for a, b in zip(_A_COEFFS, _B_COEFFS)]       # longitudinal eigenvalue A - B
    eig_poly = [2 * t for t in _polymul(lam_t, lam_t)]
    for n_, c in enumerate(_polymul(lam_l, lam_l)):
        eig_poly[n_] += c
    I_eig = sum(c * Fraction(math.factorial(n_), 2 ** (n_ + 1)) for n_, c in enumerate(eig_poly)) / 2
    show("cp_integral (exact, eigenvalue route)", I, I_eig, I == I_eig and isinstance(I, Fraction))
    direction = (0.6, -0.5, 0.7)
    r0 = math.sqrt(sum(c * c for c in direction))
    N, umax = 4 * 10 ** 4, 40.0
    du = umax / N

    def half_trace(u):
        Gm = green_tensor(*direction, u / r0)
        return sum(Gm[i][j] * Gm[j][i] for i in range(3) for j in range(3)) * r0 ** 6 / 2

    I_num = toolkit.trapezoid([half_trace(i * du) for i in range(N + 1)], du)
    show("cp_integral (numerical, trapezoid on Tr G.G)", float(I), I_num, rel(I_num, float(I)) < 1e-6)

    # 4. cp_energy vs the quoted xi-integral done directly in SI
    R1, R2, K1, K2, r = 1e-6, 2e-6, 0.5, 0.75, 1e-4
    U = cp_energy(R1, R2, K1, K2, r)
    c_, hb = inputs.C_LIGHT, inputs.HBAR
    dxi = umax * c_ / r / N

    def tr(xi):
        Gm = green_tensor(0.0, 0.0, r, xi / c_)
        return sum(Gm[i][j] * Gm[j][i] for i in range(3) for j in range(3))

    U_num = -hb / (2 * math.pi) * (K1 * R1 ** 3) * (K2 * R2 ** 3) * toolkit.trapezoid(
        [tr(i * dxi) for i in range(N + 1)], dxi)
    show("cp_energy vs direct xi-integral (J)", f"{U:.9e}", f"{U_num:.9e}", rel(U_num, U) < 1e-6 and U < 0)

    # 5. diamond radius: mass recovered from the volume
    mb = inputs.GAP_BASELINE_MASS
    Rb = diamond_radius(mb)
    m_back = inputs.RHO_DIAMOND * 4 * math.pi / 3 * Rb ** 3
    show("diamond_radius: mass from volume (kg)", mb, m_back, rel(m_back, mb) < 1e-14)
    print(f"     R(baseline mass) = {Rb:.6e} m")

    # 6. safe gap
    dxb, taub, frb = inputs.GAP_BASELINE_DX, inputs.GAP_BASELINE_TAU, inputs.GAP_FRACTION
    gap = casimir_safe_gap(mb, dxb, taub, frb)
    Kd = sphere_K(inputs.EPS_DIAMOND)
    d_far = math.sqrt(gap * gap + dxb * dxb)
    ph_c = taub / hb * 2 * (-cp_energy(Rb, Rb, Kd, Kd, gap) + cp_energy(Rb, Rb, Kd, Kd, d_far))
    ph_g = taub / hb * 2 * inputs.G_NEWTON * mb * mb * (1 / gap - 1 / d_far)
    show("safe gap: Casimir/gravity phase ratio, direct route", frb, ph_c / ph_g, rel(ph_c / ph_g, frb) < 1e-9)
    print(f"     gap = {gap:.9e} m; gap/R = {gap / Rb:.3f}; Casimir phase = {ph_c:.6e} rad, gravity phase = {ph_g:.6e} rad")

    s = _strength(mb)
    g0 = (s / frb) ** (1 / 6)
    show("safe gap inside derived bracket (g0, 7^(1/6) g0)", f"{gap:.9e}", f"({g0:.9e}, {g0 * 7 ** (1 / 6):.9e})",
         g0 < gap < g0 * 7 ** (1 / 6))
    big, small = casimir_safe_gap(mb, 1e6 * g0, taub, frb), casimir_safe_gap(mb, 1e-3 * g0, taub, frb)
    show("limit dx >> gap: gap/g0", big / g0, 1, rel(big / g0, 1) < 1e-6)
    show("limit dx << gap: gap/g0", small / g0, 7 ** (1 / 6), rel(small / g0, 7 ** (1 / 6)) < 1e-5)

    # independent solver: Newton on ln(ratio) = ln(fraction) in ln(gap)
    x = math.log(g0)
    for _ in range(60):
        f0 = math.log(_phase_ratio(math.exp(x), dxb, s)) - math.log(frb)
        e = 1e-6
        slope = (math.log(_phase_ratio(math.exp(x + e), dxb, s)) - math.log(_phase_ratio(math.exp(x - e), dxb, s))) / (2 * e)
        x -= f0 / slope
    show("safe gap: bisection vs Newton in log variables (m)", f"{gap:.12e}", f"{math.exp(x):.12e}",
         rel(math.exp(x), gap) < 1e-10)
    g_m, g_t = casimir_safe_gap(10 * mb, dxb, taub, frb), casimir_safe_gap(mb, dxb, 4 * taub, frb)
    show("safe gap independent of m and tau", f"{gap:.9e}", f"{g_m:.9e}, {g_t:.9e}",
         rel(g_m, gap) < 1e-12 and rel(g_t, gap) < 1e-12)

    print("ALL SELF-CHECKS PASS" if ok_all else "SELF-CHECK FAILURES")
