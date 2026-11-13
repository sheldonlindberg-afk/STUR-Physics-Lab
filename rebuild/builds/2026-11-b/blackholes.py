"""Stage `blackholes` (build 2026-11-b): horizons, surface gravity, the Euclidean section, Kerr's first law,
orbits, and the observables (shadow, area, ringdown, temperature).

Derivations and second routes: DERIVATION_blackholes.md (same directory); section numbers are cited below.
Geometry in G = c = 1 (M, l, r lengths) unless a function's name carries an SI unit.
"""
import math
from fractions import Fraction

import inputs
import toolkit
import desitter

PROVENANCE = {
    "sds_horizons": ("derived", "f = 1 - 2M/r - r^2/l^2 is concave with its maximum at r0 = (M l^2)^(1/3),"
                                " f(r0) = 1 - 3M/r0; if f(r0) > 0 the roots are bracketed by [2M, r0] and"
                                " [r0, l] and found with toolkit.bisect, else None (section 1)"),
    "killing_kappa": ("derived", "metric diag(-f, 1/f, r^2, r^2 sin^2) from f only; Christoffels from central"
                                 " differences of the metric; nabla_mu xi_nu for xi = d/dt; kappa^2 ="
                                 " -(nabla xi)^2/2 contracted with the inverse metric (section 2)"),
    "kappa_from_spin_connection": ("derived", "|omega^0_{1 t}| of desitter.spin_connection at r_b(1 + 1e-9) and"
                                              " r_c(1 - 1e-9), horizons from sds_horizons: the boost rate of"
                                              " the static frame equals |f'|/2 (section 3)"),
    "euclidean_cone_ratio": ("derived", "t = -i tau: circumference beta sqrt(f) over 2 pi times the proper"
                                        " radius int dr/sqrt(f), the integral done with r = rh + eps u^2 and"
                                        " toolkit.trapezoid on a grid that skips u = 0 (section 4)"),
    "kerr_first_law": ("derived", "from the SPEC's M, a^2, S, T, Omega, J in p, q: T dS = (p - q) dX/(4X) and"
                                  " Omega dJ = d(J^2)/(2MX), X = p^2 + a^2 (pi and a cancel), differentials by"
                                  " toolkit.exact_derivative along (dp, dq); Smarr likewise (section 5)"),
    "nariai_mass_kg": ("derived", "horizons merge when f(r0) = 0, i.e. G M/c^2 = l/sqrt(27), with l from"
                                  " desitter.ell_from_lambda (section 6)"),
    "photon_sphere": ("derived", "maximum of f/r^2 for f = 1 - 2/r by toolkit.golden_max, polished by"
                                 " toolkit.bisect on the exact derivative (toolkit.exact_derivative);"
                                 " b = 1/sqrt(max) (section 7)"),
    "isco": ("derived", "circular orbits of V = f(1 + L^2/r^2) have L^2(r) = -f'/(f/r^2)' (exact derivatives);"
                        " the ISCO is the minimum of L^2(r), found by toolkit.bisect on its exact symmetric"
                        " difference; E^2 = V there (section 8)"),
    "shadow_uas": ("derived", "2 b_c GM/(c^2 D) with b_c from photon_sphere(), GM = m_sun inputs.GM_SUN,"
                              " D = d_pc inputs.PARSEC, converted from radians to microarcseconds (section 9)"),
    "kerr_area_km2": ("derived", "A = 4 pi (p^2 + a^2) = 8 pi M p with p = M(1 + sqrt(1 - chi^2)) the larger"
                                 " root of x^2 - 2Mx + a^2, M -> GM/c^2 (section 10)"),
    "qnm_220": ("quoted", "Berti, Cardoso, Will 2006 fit M omega = f1 + f2 (1 - chi)^f3, Q = q1 + q2 (1 - chi)^q3"
                          " with inputs.BCW_220; f = omega/(2 pi), damping = omega/(2Q), time unit GM/c^3"
                          " (section 11)"),
    "invert_220": ("quoted", "algebraic inverse of the Berti-Cardoso-Will 2006 fit: Q = pi f/damp gives chi,"
                             " then M omega(chi) gives the detector mass, divided by 1 + z (section 12)"),
    "hawking_K": ("quoted", "Hawking 1975, T = hbar c^3/(8 pi G M k_B) as a radiation temperature; equals"
                            " hbar kappa/(2 pi k_B c) with the Killing kappa = c^4/(4GM) (section 13)"),
}

_OFFSET = 1e-9            # relative distance from the horizon for the spin-connection route (SPEC section 7)
_NODES = 200              # even: the trapezoid grid on [-1, 1] then skips u = 0
_ANGLE_STEP = 1e-6        # step of the theta difference in killing_kappa


# ------------------------------------------------------------------------------------------
# 1. Schwarzschild-de Sitter horizons
# ------------------------------------------------------------------------------------------
def _sds(M, l):
    """f and f' of Schwarzschild-de Sitter."""
    return (lambda r: 1 - 2 * M / r - r * r / l ** 2), (lambda r: 2 * M / r ** 2 - 2 * r / l ** 2)


def sds_horizons(M, l):
    """(r_b, r_c), the black-hole and cosmological horizons of f = 1 - 2M/r - r^2/l^2, or None beyond the
    Nariai bound (section 1)."""
    if not (M > 0 and l > 0):
        raise ValueError("sds_horizons needs M > 0 and l > 0")
    f, _ = _sds(M, l)
    r0 = (M * l * l) ** (1 / 3)                    # f'(r0) = 0: the maximum of f
    top = f(r0)
    if top < 0:
        return None
    if top == 0:
        return r0, r0
    return toolkit.bisect(f, 2 * M, r0), toolkit.bisect(f, r0, l)


# ------------------------------------------------------------------------------------------
# 2. surface gravity from the Killing vector
# ------------------------------------------------------------------------------------------
def _metric(f, r, th):
    fv = f(r)
    return [-fv, 1 / fv, r * r, (r * math.sin(th)) ** 2]


def _killing_gradient(f, r0, h, th=1.0):
    """(g, K) at (r0, th): the diagonal metric and K[mu][nu] = nabla_mu xi_nu for xi = d/dt, with the
    Christoffel symbols from central differences of the metric (section 2)."""
    g = _metric(f, r0, th)
    ginv = [1 / v for v in g]
    # dg[lam][mu] = d_lam g_{mu mu}; the metric depends on r and theta only
    up, dn = _metric(f, r0 + h, th), _metric(f, r0 - h, th)
    tu, td = _metric(f, r0, th + _ANGLE_STEP), _metric(f, r0, th - _ANGLE_STEP)
    dg = [[0.0] * 4,
          [(up[i] - dn[i]) / (2 * h) for i in range(4)],
          [(tu[i] - td[i]) / (2 * _ANGLE_STEP) for i in range(4)],
          [0.0] * 4]

    def d(lam, mu, nu):                            # d_lam g_{mu nu}
        return dg[lam][mu] if mu == nu else 0.0

    def gamma(lam, mu, nu):                        # Gamma^lam_{mu nu}; the metric is diagonal
        return ginv[lam] * (d(mu, lam, nu) + d(nu, lam, mu) - d(lam, mu, nu)) / 2

    xi = [g[0], 0.0, 0.0, 0.0]                     # xi_nu = g_{nu t}
    K = [[d(mu, nu, 0) - sum(gamma(lam, mu, nu) * xi[lam] for lam in range(4)) for nu in range(4)]
         for mu in range(4)]
    return g, K


def killing_kappa(f, r0, h):
    """Surface gravity sqrt(-(nabla_mu xi_nu)(nabla^mu xi^nu)/2) of xi = d/dt at radius r0 for the metric
    -f dt^2 + dr^2/f + r^2 dOmega^2; h is the step of the metric's r difference (section 2)."""
    g, K = _killing_gradient(f, r0, h)
    square = sum(K[mu][nu] ** 2 / (g[mu] * g[nu]) for mu in range(4) for nu in range(4))
    return math.sqrt(max(-square / 2, 0.0))


def kappa_from_spin_connection(M, l):
    """(kappa_b, kappa_c) = |omega^0_{1 t}| of rung 5's spin connection just on the static side of each
    Schwarzschild-de Sitter horizon (section 3)."""
    hor = sds_horizons(M, l)
    if hor is None:
        raise ValueError("no horizons: M/l is beyond the Nariai bound")
    f, fp = _sds(M, l)
    out = []
    for r in (hor[0] * (1 + _OFFSET), hor[1] * (1 - _OFFSET)):
        _, w = desitter.spin_connection((0.0, r, math.pi / 2, 0.0), f, fp)
        out.append(abs(w[0][1][0]))
    return tuple(out)


# ------------------------------------------------------------------------------------------
# 3. the Euclidean section
# ------------------------------------------------------------------------------------------
def _proper_radius(f, rh, eps):
    """|int_rh^{rh + eps} dr/sqrt(f)| with r = rh + eps u^2 (section 4)."""
    def g(u):
        fv = f(rh + eps * u * u)
        if not fv > 0:
            raise ValueError("f <= 0 between the horizon and rh + eps: eps is on the wrong side")
        return 2 * abs(eps * u) / math.sqrt(fv)

    dx = 2 / (_NODES - 1)
    return toolkit.trapezoid([g(-1 + i * dx) for i in range(_NODES)], dx) / 2


def euclidean_cone_ratio(f, rh, beta, eps):
    """Circumference/(2 pi proper radius) of the circle r = rh + eps in f dtau^2 + dr^2/f, tau of period beta:
    1 where the Euclidean section is smooth (section 4)."""
    return beta * math.sqrt(f(rh + eps)) / (2 * math.pi * _proper_radius(f, rh, eps))


# ------------------------------------------------------------------------------------------
# 4. Kerr: first law and Smarr relation, exactly
# ------------------------------------------------------------------------------------------
def _kerr_mass(p, q):
    return (p + q) / 2


def _kerr_x(p, q):
    """p^2 + a^2 with a^2 = p q: S/pi."""
    return p * p + p * q


def _kerr_j2(p, q):
    """J^2 = M^2 a^2."""
    return _kerr_mass(p, q) ** 2 * p * q


def kerr_first_law(p, q, dp, dq):
    """(dM - T dS - Omega dJ along (dp, dq), M - 2TS - 2 Omega J) for Kerr with r+ = p, r- = q, as exact
    Fractions (section 5)."""
    p, q, dp, dq = Fraction(p), Fraction(q), Fraction(dp), Fraction(dq)

    def along(fn):                                 # directional derivative of fn(p, q) along (dp, dq)
        return toolkit.exact_derivative(lambda s: fn(p + s * dp, q + s * dq), 0)

    M, X = _kerr_mass(p, q), _kerr_x(p, q)
    t_ds = (p - q) * along(_kerr_x) / (4 * X)      # T dS: the pi of T and S cancel
    om_dj = along(_kerr_j2) / (2 * M * X)          # Omega dJ = (a/X) d(J^2)/(2 M a)
    first = along(_kerr_mass) - t_ds - om_dj
    smarr = M - (p - q) / 2 - 2 * M * p * q / X    # 2TS = (p - q)/2, 2 Omega J = 2 M a^2/X
    return Fraction(first), Fraction(smarr)


# ------------------------------------------------------------------------------------------
# 5. the largest black hole
# ------------------------------------------------------------------------------------------
def nariai_mass_kg(Lam):
    """Largest Schwarzschild-de Sitter mass in kg for Lambda in m^-2: G M/c^2 = l/sqrt(27) (section 6)."""
    l = desitter.ell_from_lambda(Lam)
    return l / math.sqrt(27) * inputs.C_LIGHT ** 2 / inputs.G_NEWTON


# ------------------------------------------------------------------------------------------
# 6. orbits (M = 1)
# ------------------------------------------------------------------------------------------
def _f_schw(r):
    return 1 - 2 / r


def _photon_potential(r):
    return _f_schw(r) / (r * r)


def photon_sphere():
    """(r, b): radius of the maximum of f/r^2 and b = 1/sqrt(maximum), M = 1 (section 7)."""
    r = toolkit.golden_max(_photon_potential, 2, 20)
    slope = lambda x: float(toolkit.exact_derivative(_photon_potential, Fraction(x)))
    w = r / 1000
    if slope(r - w) > 0 > slope(r + w):            # polish: the maximum is where the exact slope changes sign
        r = toolkit.bisect(slope, r - w, r + w)
    return r, 1 / math.sqrt(_photon_potential(r))


def _circular_l2(r):
    """L^2 of the circular orbit at radius r: V' = f' + L^2 (f/r^2)' = 0, exactly for a Fraction r."""
    r = Fraction(r)
    return -toolkit.exact_derivative(_f_schw, r) / toolkit.exact_derivative(_photon_potential, r)


def isco():
    """(r, L2, E2) of the innermost stable circular orbit of V = f(1 + L^2/r^2), M = 1: the minimum of the
    circular orbits' L^2(r) (section 8)."""
    h = Fraction(1, 10 ** 9)
    rise = lambda x: float(_circular_l2(Fraction(x) + h) - _circular_l2(Fraction(x) - h))
    r_ph = photon_sphere()[0]
    r = toolkit.bisect(rise, r_ph + 1 / 2, 10 * r_ph)
    L2 = float(_circular_l2(r))
    return r, L2, _f_schw(r) * (1 + L2 / (r * r))


# ------------------------------------------------------------------------------------------
# 7. observables in SI
# ------------------------------------------------------------------------------------------
def _uas_per_radian():
    return math.degrees(1) * 3600 * 1e6


def _theta_g_uas(m_sun, d_pc):
    """G M/(c^2 D) in microarcseconds."""
    return m_sun * inputs.GM_SUN / (inputs.C_LIGHT ** 2 * d_pc * inputs.PARSEC) * _uas_per_radian()


def shadow_uas(m_sun, d_pc):
    """Schwarzschild shadow diameter 2 b_c GM/(c^2 D) in microarcseconds (section 9)."""
    return 2 * photon_sphere()[1] * _theta_g_uas(m_sun, d_pc)


def kerr_area_km2(m_sun, chi):
    """Kerr horizon area 8 pi (GM/c^2)^2 (1 + sqrt(1 - chi^2)) in km^2 (section 10)."""
    if abs(chi) > 1:
        raise ValueError("no horizon for |chi| > 1")
    m = m_sun * inputs.GM_SUN / inputs.C_LIGHT ** 2          # G M/c^2 in metres
    p = m * (1 + math.sqrt(1 - chi * chi))                    # r+
    return 8 * math.pi * m * p / 1e6


def _bcw(chi):
    """(M omega, Q) of the 220 mode from the quoted fit."""
    f1, f2, f3, q1, q2, q3 = inputs.BCW_220
    return f1 + f2 * (1 - chi) ** f3, q1 + q2 * (1 - chi) ** q3


def _solar_time():
    """G M_sun/c^3 in seconds."""
    return inputs.GM_SUN / inputs.C_LIGHT ** 3


def qnm_220(m_det_sun, chi):
    """(frequency in Hz, damping rate in 1/s) of the 220 mode for a detector-frame mass (section 11)."""
    mw, Q = _bcw(chi)
    omega = mw / (m_det_sun * _solar_time())
    return omega / (2 * math.pi), omega / (2 * Q)


def invert_220(f, damp, z):
    """(source-frame mass in M_sun, chi) from the 220 mode's frequency (Hz), damping rate (1/s) and the
    redshift (section 12)."""
    _, _, _, q1, q2, q3 = inputs.BCW_220
    Q = math.pi * f / damp
    ratio = (Q - q1) / q2
    if not ratio > 0:
        raise ValueError("quality factor outside the range of the fit")
    chi = 1 - ratio ** (1 / q3)
    m_det = _bcw(chi)[0] / (2 * math.pi * f * _solar_time())
    return m_det / (1 + z), chi


def hawking_K(m_kg):
    """Hawking temperature hbar c^3/(8 pi G M k_B) in K (section 13)."""
    return inputs.HBAR * inputs.C_LIGHT ** 3 / (8 * math.pi * inputs.G_NEWTON * m_kg * inputs.K_B)


# ------------------------------------------------------------------------------------------
# self-check: second routes (DERIVATION_blackholes.md)
# ------------------------------------------------------------------------------------------
def _pull(pred, meas):
    """(prediction - measured)/sigma with sigma on the side facing the prediction; meas = (value, -, +)."""
    return (pred - meas[0]) / (meas[2] if pred > meas[0] else meas[1])


if __name__ == "__main__":
    print("== sds_horizons ==")
    M, l = 1.0, 9.0
    rb, rc = sds_horizons(M, l)
    ang = math.acos(-math.sqrt(27) * M / l) / 3
    trig = [2 * l / math.sqrt(3) * math.cos(ang - 2 * math.pi * k / 3) for k in range(3)]
    print("  bisect:", rb, rc, "  trigonometric cubic roots:", trig[1], trig[0], " (negative root", trig[2], ")")
    print("  Vieta with r_- = -(rb + rc): product/(-2 M l^2) =", rb * rc * (rb + rc) / (2 * M * l * l))
    print("  beyond the bound (M/l = 1/5):", sds_horizons(1.0, 5.0))

    print("== killing_kappa ==")
    f, fp = _sds(M, l)
    fd = lambda r, s: (-f(r + 2 * s) + 8 * f(r + s) - 8 * f(r - s) + f(r - 2 * s)) / (12 * s)
    for name, r in (("black hole", rb * (1 + 1e-6)), ("cosmological", rc * (1 - 1e-6))):
        print(f"  {name}: Killing {killing_kappa(f, r, 1e-8 * r)}  |f'|/2 (5-point stencil) {abs(fd(r, 1e-4)) / 2}")
    g, K = _killing_gradient(f, rb * (1 + 1e-6), 1e-8 * rb)
    print("  max |nabla_mu xi_nu + nabla_nu xi_mu| (Killing's equation):",
          max(abs(K[i][j] + K[j][i]) for i in range(4) for j in range(4)))
    sch = lambda m, d: killing_kappa(lambda r: 1 - 2 * m / r, 2 * m * (1 + d), 1e-8 * m)
    print("  Schwarzschild 4 M kappa at M = 1, 3:", 4 * sch(1.0, 1e-6), 12 * sch(3.0, 1e-6))

    print("== kappa_from_spin_connection ==")
    kb, kc = kappa_from_spin_connection(M, l)
    rm = -(rb + rc)
    print("  spin connection:", kb, kc)
    print("  from the roots: ", (rc - rb) * (rb - rm) / (2 * l * l * rb), (rc - rb) * (rc - rm) / (2 * l * l * rc))

    print("== euclidean_cone_ratio ==")
    for name, rh, k, eps in (("black hole", rb, kb, 1e-7 * rb), ("cosmological", rc, kc, -1e-7 * rc)):
        print(f"  {name}: ratio at beta = 2 pi/kappa {euclidean_cone_ratio(f, rh, 2 * math.pi / k, eps)},"
              f"  at 1.3 x that {euclidean_cone_ratio(f, rh, 2.6 * math.pi / k, eps)}")
    fs = lambda r: 1 - 2 / r
    for eps in (1e-6, 0.5):
        r = 2 + eps
        closed = math.sqrt(r * (r - 2)) + 2 * math.log(math.sqrt(r / 2) + math.sqrt(r / 2 - 1))
        print(f"  Schwarzschild proper radius, eps = {eps}: trapezoid {_proper_radius(fs, 2.0, eps)}  closed form {closed}")

    print("== kerr_first_law ==")
    p, q, dp, dq = Fraction(7, 2), Fraction(3, 5), 2, -3
    print("  exact residuals:", kerr_first_law(p, q, dp, dq), "  Schwarzschild along dq:", kerr_first_law(5, 0, 0, 1))

    def kerr_float(pv, qv):
        m, a = (pv + qv) / 2, math.sqrt(pv * qv)
        x = pv * pv + a * a
        return m, math.pi * x, m * a, (pv - qv) / (4 * math.pi * x), a / x

    s = 1e-6
    hi, lo = kerr_float(float(p) + s * dp, float(q) + s * dq), kerr_float(float(p) - s * dp, float(q) - s * dq)
    m0, S0, J0, T0, O0 = kerr_float(float(p), float(q))
    dM, dS, dJ = ((hi[i] - lo[i]) / (2 * s) for i in range(3))
    print("  floating point with sqrt and pi kept: first", dM - T0 * dS - O0 * dJ, " smarr", m0 - 2 * T0 * S0 - 2 * O0 * J0)
    print("  negative control (T doubled): first", dM - 2 * T0 * dS - O0 * dJ)

    print("== nariai_mass_kg ==")
    Lam = inputs.LAMBDA_SI
    m_n = nariai_mass_kg(Lam)
    Mg, lg = m_n * inputs.G_NEWTON / inputs.C_LIGHT ** 2, desitter.ell_from_lambda(Lam)
    fN, fpN = _sds(Mg, lg)
    r0 = toolkit.bisect(fpN, Mg, lg)
    print("  M_Nariai:", m_n, "kg =", m_n * inputs.G_NEWTON / inputs.GM_SUN, "M_sun")
    print("  f at f' = 0:", fN(r0), "  r0/(3M):", r0 / (3 * Mg), "  r0 sqrt3/l:", r0 * math.sqrt(3) / lg)
    print("  horizons just inside / outside:", sds_horizons(Mg, lg * (1 + 1e-6)) is not None,
          sds_horizons(Mg, lg * (1 - 1e-6)) is not None)

    print("== photon_sphere ==")
    r_ph, b_c = photon_sphere()
    r_gold = toolkit.golden_max(_photon_potential, 2, 20)
    print("  polished:", r_ph, b_c, "  golden section only:", r_gold, "  closed form 3, sqrt(27):", 3, math.sqrt(27))

    print("== isco ==")
    ri, L2, E2 = isco()
    r_gold = toolkit.golden_max(lambda r: -float(_circular_l2(r)), r_ph + 1 / 2, 10 * r_ph)
    V = lambda r: _f_schw(r) * (1 + L2 / (r * r))
    s = 1e-3
    print("  bisect on exact difference:", ri, L2, E2, "  golden section on -L^2(r):", r_gold)
    print("  V'(r) and V''(r) by finite differences:", (V(ri + s) - V(ri - s)) / (2 * s),
          (V(ri + s) - 2 * V(ri) + V(ri - s)) / (s * s))
    print("  closed form r = 6, L^2 = 12, E^2 = 8/9:", 6, 12, float(Fraction(8, 9)))

    print("== shadow_uas, kerr_area_km2 ==")
    print("  shadow/theta_g:", shadow_uas(1e6, 8000.0) / _theta_g_uas(1e6, 8000.0), "  2 sqrt(27):", 2 * math.sqrt(27))
    mg = 10 * inputs.GM_SUN / inputs.C_LIGHT ** 2
    chi = 0.6
    pp, qq = mg * (1 + math.sqrt(1 - chi * chi)), mg * (1 - math.sqrt(1 - chi * chi))
    print("  area(10, 0.6):", kerr_area_km2(10.0, chi), "km^2   4 S = 4 pi (p^2 + pq):", 4 * math.pi * (pp * pp + pp * qq) / 1e6)
    print("  area(10, 0):", kerr_area_km2(10.0, 0.0), "km^2   4 pi (2GM/c^2)^2:", 4 * math.pi * (2 * mg) ** 2 / 1e6)

    print("== qnm_220, invert_220 ==")
    z = inputs.GW_Z[0]
    f_pred, g_pred = qnm_220(inputs.GW_MF * (1 + z), inputs.GW_CHIF)
    m_back, chi_back = invert_220(f_pred, g_pred, z)
    Qv = math.pi * f_pred / g_pred
    chi_bis = toolkit.bisect(lambda c: _bcw(c)[1] - Qv, 0, 1 - 1e-9)
    print("  predicted 220 mode:", f_pred, "Hz,", g_pred, "1/s")
    print("  round trip:", m_back, chi_back, "  chi by bisection:", chi_bis)
    print("  pulls against the ringdown fit: f", _pull(f_pred, inputs.F220), " damping", _pull(g_pred, inputs.G220))
    m_inf, chi_inf = invert_220(inputs.F220[0], inputs.G220[0], z)
    print("  inverted from the measured mode: M", m_inf, "M_sun, chi", chi_inf,
          "  (inspiral:", inputs.GW_MF, inputs.GW_CHIF, ")")
    a_f = kerr_area_km2(inputs.GW_MF, inputs.GW_CHIF)
    a_i = kerr_area_km2(inputs.GW_M1[0], 0.0) + kerr_area_km2(inputs.GW_M2[0], 0.0)
    print("  area theorem: final", a_f, "km^2, largest possible initial", a_i, "km^2, ratio", a_f / a_i)

    print("== hawking_K ==")
    m_sun_kg = inputs.GM_SUN / inputs.G_NEWTON
    kappa_si = sch(1.0, 1e-6) / (inputs.G_NEWTON * m_sun_kg / inputs.C_LIGHT ** 2)       # 1/m
    print("  T(M_sun):", hawking_K(m_sun_kg), "K   hbar c kappa/(2 pi k_B) with the Killing kappa:",
          inputs.HBAR * inputs.C_LIGHT * kappa_si / (2 * math.pi * inputs.K_B), "K")

    print("== shadows against the EHT ==")
    m87 = _theta_g_uas(inputs.M87_STARS[0], inputs.M87_STARS[2])
    print("  M87*: theta_g from stars", m87, "uas, EHT", inputs.THETA_G_M87[0], " pull", _pull(m87, inputs.THETA_G_M87),
          "  shadow", shadow_uas(inputs.M87_STARS[0], inputs.M87_STARS[2]), "uas")
    sgr = (_theta_g_uas(*inputs.SGRA_VLTI) + _theta_g_uas(*inputs.SGRA_KECK)) / 2
    print("  Sgr A*: mean theta_g (VLTI, Keck)", sgr, "uas, EHT", inputs.THETA_G_SGRA[0], " pull",
          _pull(sgr, inputs.THETA_G_SGRA), "  shadow", 2 * b_c * sgr, "uas")
