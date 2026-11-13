"""blackholes: gravity's strong-field end (rung 6, SPEC.md section 7).

Derivations and second routes: DERIVATION_blackholes.md (section numbers below refer to it).
Roots, maxima and exact derivatives go through toolkit; the de Sitter radius and the spin
connection come from rung 5 (desitter), called at run time.
"""
import math
from fractions import Fraction

import inputs
import toolkit
import desitter

PROVENANCE = {
    "sds_horizons": ("derived", "f = 1 - 2M/r - r^2/l^2 is concave (f'' < 0), negative at 2M and for r >= l: maximum"
                                " r* = toolkit.golden_max(f, 2M, l); None if f(r*) <= 0, else toolkit.bisect on"
                                " [2M, r*] and [r*, l]; checked by Vieta on r^3 - l^2 r + 2Ml^2"),
    "killing_kappa": ("derived", "metric diag(-f, 1/f, r^2, r^2 sin^2) from f only; d g by central differences (step h);"
                                 " Christoffels; nabla_mu xi_nu = d_mu g_{nu t} - Gamma^l_{mu nu} g_{l t};"
                                 " kappa = sqrt(-(1/2) nabla xi . nabla xi) (= |f'|/2 by hand)"),
    "kappa_from_spin_connection": ("derived", "desitter.spin_connection at r_b(1+1e-9), r_c(1-1e-9) from sds_horizons,"
                                              " fp = toolkit.exact_derivative of the rational f; kappa = |w[0][1][0]| ="
                                              " |omega^0_{1t}| since K = -2 (omega^0_{1t})^2"),
    "euclidean_cone_ratio": ("derived", "tau = it: f dtau^2 + dr^2/f; C = beta sqrt f(rh+eps); rho = Int dr/sqrt f with"
                                        " r = rh + u^2 -> Int 2u du/sqrt f (smooth even integrand, endpoint by"
                                        " (4g(du) - g(2du))/3), toolkit.trapezoid; ratio C/(2 pi rho) -> beta kappa/(2 pi)"),
    "kerr_first_law": ("derived", "quoted BCH S, T, Omega, J only, with pi factored out (S/pi, T pi) and Omega dJ ="
                                  " d(J^2)/(2M(p^2+a^2)), Omega J = a^2 M/(p^2+a^2) (a^2 = pq rational); directional"
                                  " derivatives along (dp, dq) by toolkit.exact_derivative; exact Fractions"),
    "nariai_mass_kg": ("derived", "f = f' = 0: with r = x l, M = mu l, f' = 0 gives mu = x^3, then 1 - 3x^2 = 0 solved by"
                                  " toolkit.bisect; M = mu l, l = desitter.ell_from_lambda(Lam); kg = M c^2/G"
                                  " (closed form c^2/(3 G sqrt Lam))"),
    "photon_sphere": ("derived", "maximum of V = f/r^2 (M = 1) by toolkit.golden_max, polished as the root of the exact"
                                 " V' (toolkit.exact_derivative + bisect); b_c = 1/sqrt(V_max)"),
    "isco": ("derived", "V' = f' + L^2 (f/r^2)' is linear in L^2: L^2(r) = -f'/(f/r^2)' (exact derivatives); circular"
                        " orbits first exist at min L^2(r), found by toolkit.golden_max on (r_ph, 20 r_ph) and polished"
                        " by bisect on an exact symmetric difference; E^2 = f(1 + L^2/r^2)"),
    "shadow_uas": ("derived", "diameter 2 b_c GM/(c^2 D) with b_c from photon_sphere(), GM = m GM_SUN, D = d PARSEC,"
                              " radians to micro-arcseconds"),
    "kerr_area_km2": ("derived", "r+ = toolkit.bisect root of r^2 - 2r + chi^2 (horizons p, q with p+q = 2M, pq = a^2);"
                                 " A = 4 pi (r+^2 + a^2) (G M/c^2)^2 = 4 S_BCH; equals 8 pi M^2 (1 + sqrt(1-chi^2))"),
    "qnm_220": ("quoted", "Berti, Cardoso & Will, PRD 73, 064030 (2006) fit M omega = f1 + f2 (1-chi)^f3,"
                          " Q = q1 + q2 (1-chi)^q3 (inputs.BCW_220); f = omega/2pi, damping omega/(2Q), M = m GM_SUN/c^3"),
    "invert_220": ("quoted", "Berti-Cardoso-Will 2006 fit inverted algebraically: Q = pi f/damp -> 1 - chi ="
                             " ((Q-q1)/q2)^(1/q3), then M_det = (M omega)/omega, source mass M_det/(1+z)"),
    "hawking_K": ("quoted", "Hawking, Commun. Math. Phys. 43, 199 (1975): T_H = hbar c^3/(8 pi G M k_B);"
                            " = hbar kappa/(2 pi c k_B) with kappa = c^4/(4GM), cf. euclidean_cone_ratio"),
}


# ------------------------------------------------------------------------------------------ 1
def _sds_f(M, l):
    return lambda r: 1 - 2 * M / r - r * r / (l * l)


def sds_horizons(M, l):
    f = _sds_f(M, l)
    lo, hi = 2 * M, l
    if not lo < hi:
        return None
    rs = toolkit.golden_max(f, lo, hi)
    if not f(rs) > 0:
        return None
    return toolkit.bisect(f, lo, rs), toolkit.bisect(f, rs, hi)


# ------------------------------------------------------------------------------------------ 2
def _metric(f, x):
    r, th = x[1], x[2]
    s = math.sin(th)
    fv = f(r)
    return [[-fv, 0.0, 0.0, 0.0], [0.0, 1 / fv, 0.0, 0.0], [0.0, 0.0, r * r, 0.0], [0.0, 0.0, 0.0, r * r * s * s]]


def killing_kappa(f, r0, h):
    x0 = [0.0, float(r0), math.pi / 3, 0.0]
    g = _metric(f, x0)
    gi = [[(1 / g[i][i] if i == j else 0.0) for j in range(4)] for i in range(4)]   # diagonal metric
    dg = []                                         # dg[rho][mu][nu] = d_rho g_{mu nu}
    for rho in range(4):
        xp, xm = list(x0), list(x0)
        xp[rho] += h
        xm[rho] -= h
        gp, gm = _metric(f, xp), _metric(f, xm)
        dg.append([[(gp[m][n] - gm[m][n]) / (2 * h) for n in range(4)] for m in range(4)])
    Gam = [[[0.5 * sum(gi[l][s] * (dg[m][s][n] + dg[n][s][m] - dg[s][m][n]) for s in range(4))
             for n in range(4)] for m in range(4)] for l in range(4)]
    xi_low = [g[n][0] for n in range(4)]                       # xi_nu = g_{nu t}
    D = [[dg[m][n][0] - sum(Gam[l][m][n] * xi_low[l] for l in range(4)) for n in range(4)] for m in range(4)]
    K = sum(gi[m][a] * gi[n][b] * D[m][n] * D[a][b] for m in range(4) for n in range(4)
            for a in range(4) for b in range(4))
    return math.sqrt(-K / 2)


# ------------------------------------------------------------------------------------------ 3
def kappa_from_spin_connection(M, l):
    rb, rc = sds_horizons(M, l)
    Mq, lq = Fraction(M), Fraction(l)
    f = _sds_f(M, l)
    f_exact = lambda r: 1 - 2 * Mq / r - r * r / (lq * lq)
    fp = lambda r: float(toolkit.exact_derivative(f_exact, Fraction(r)))
    out = []
    for r in (rb * (1 + 1e-9), rc * (1 - 1e-9)):
        _, w = desitter.spin_connection([0.0, r, math.pi / 2, 0.0], f, fp)
        out.append(abs(w[0][1][0]))
    return tuple(out)


# ------------------------------------------------------------------------------------------ 4
def euclidean_cone_ratio(f, rh, beta, eps, n=401):
    U = math.sqrt(eps)
    du = U / (n - 1)
    g = lambda u: 2 * u / math.sqrt(f(rh + u * u))
    ys = [g(k * du) for k in range(1, n)]
    g0 = (4 * ys[0] - ys[1]) / 3                     # g even and smooth in u: g(0) from two samples
    rho = toolkit.trapezoid([g0] + ys, du)
    circ = beta * math.sqrt(f(rh + eps))
    return circ / (2 * math.pi * rho)


# ------------------------------------------------------------------------------------------ 5
def _kerr(p, q):
    """Quoted BCH quantities in exact form: M, S/pi, T pi, a^2, J^2 (a = sqrt(pq) never formed)."""
    M = (p + q) / 2
    a2 = p * q
    S_pi = p * p + a2
    T_pi = (p - q) / (4 * S_pi)
    J2 = M * M * a2
    return M, S_pi, T_pi, a2, J2


def kerr_first_law(p, q, dp, dq):
    p, q = Fraction(p), Fraction(q)
    dp, dq = Fraction(dp), Fraction(dq)
    along = lambda k: (lambda s: _kerr(p + s * dp, q + s * dq)[k])
    d = lambda k: toolkit.exact_derivative(along(k), Fraction(0))
    M, S_pi, T_pi, a2, J2 = _kerr(p, q)
    dM, dS_pi, dJ2 = d(0), d(1), d(4)
    T_dS = T_pi * dS_pi                              # T dS = (T pi) d(S/pi)
    Omega_dJ = dJ2 / (2 * M * S_pi)                  # Omega dJ = (Omega/2J) d(J^2), Omega/J = 1/(M (p^2+a^2))
    first = dM - T_dS - Omega_dJ
    Omega_J = a2 * M / S_pi
    smarr = M - 2 * T_pi * S_pi - 2 * Omega_J
    return first, smarr


# ------------------------------------------------------------------------------------------ 6
def nariai_mass_kg(Lam):
    F = lambda x, mu: 1 - 2 * mu / x - x * x       # f in units of l: r = x l, M = mu l
    # f' = 0  <=>  2 mu/x^2 = 2x  <=>  mu = x^3 (the branch where the horizons merge)
    x = toolkit.bisect(lambda x: F(x, x ** 3), 1e-3, 1.0)
    mu = x ** 3
    l = desitter.ell_from_lambda(Lam)
    M_geo = mu * l                                   # metres
    return M_geo * inputs.C_LIGHT ** 2 / inputs.G_NEWTON


# ------------------------------------------------------------------------------------------ 7
def _V_photon(r):
    f = 1 - 2 / r                                     # M = 1
    return f / (r * r)


def photon_sphere():
    rg = toolkit.golden_max(_V_photon, 2.0, 10.0)
    dV = lambda r: float(toolkit.exact_derivative(_V_photon, Fraction(r)))
    lo, hi = rg * (1 - 1e-5), rg * (1 + 1e-5)
    r = toolkit.bisect(dV, lo, hi) if dV(lo) * dV(hi) < 0 else rg
    return r, 1 / math.sqrt(_V_photon(r))


# ------------------------------------------------------------------------------------------ 8
def _f_schw(r):
    return 1 - 2 / r                                  # M = 1


def _L2_circular(r):
    """L^2 of the circular orbit at r: V' = f' + L^2 (f/r^2)' = 0 (exact derivatives at Fraction r)."""
    rq = Fraction(r)
    df = toolkit.exact_derivative(_f_schw, rq)
    dB = toolkit.exact_derivative(lambda s: _f_schw(s) / (s * s), rq)
    return -df / dB


def isco():
    r_ph, _ = photon_sphere()
    neg = lambda r: -float(_L2_circular(r))
    rg = toolkit.golden_max(neg, r_ph * (1 + 1e-6), 20 * r_ph)
    eta = Fraction(1, 10 ** 6)
    D = lambda r: float(_L2_circular(Fraction(r) * (1 + eta)) - _L2_circular(Fraction(r) * (1 - eta)))
    lo, hi = rg * (1 - 1e-5), rg * (1 + 1e-5)
    r = toolkit.bisect(D, lo, hi) if D(lo) * D(hi) < 0 else rg
    L2 = float(_L2_circular(r))
    E2 = _f_schw(r) * (1 + L2 / (r * r))
    return r, L2, E2


# ------------------------------------------------------------------------------------------ 9, 10
def _uas_per_rad():
    return 180 / math.pi * 3600 * 1e6


def shadow_uas(m_sun, d_pc):
    _, b = photon_sphere()
    GM_c2 = m_sun * inputs.GM_SUN / inputs.C_LIGHT ** 2
    D = d_pc * inputs.PARSEC
    return 2 * b * GM_c2 / D * _uas_per_rad()


def kerr_area_km2(m_sun, chi):
    rp = toolkit.bisect(lambda r: r * r - 2 * r + chi * chi, 1.0, 2.0)    # r+ in units of M
    GM_c2 = m_sun * inputs.GM_SUN / inputs.C_LIGHT ** 2
    return 4 * math.pi * (rp * rp + chi * chi) * GM_c2 ** 2 / 1e6


# ------------------------------------------------------------------------------------------ 11-13
def _bcw(chi):
    f1, f2, f3, q1, q2, q3 = inputs.BCW_220
    return f1 + f2 * (1 - chi) ** f3, q1 + q2 * (1 - chi) ** q3


def qnm_220(m_det_sun, chi):
    Mw, Q = _bcw(chi)
    M_s = m_det_sun * inputs.GM_SUN / inputs.C_LIGHT ** 3
    w = Mw / M_s
    return w / (2 * math.pi), w / (2 * Q)


def invert_220(f, damp, z):
    f1, f2, f3, q1, q2, q3 = inputs.BCW_220
    w = 2 * math.pi * f
    Q = w / (2 * damp)
    chi = 1 - ((Q - q1) / q2) ** (1 / q3)
    Mw, _ = _bcw(chi)
    m_det = (Mw / w) * inputs.C_LIGHT ** 3 / inputs.GM_SUN
    return m_det / (1 + z), chi


def hawking_K(m_kg):
    return inputs.HBAR * inputs.C_LIGHT ** 3 / (8 * math.pi * inputs.G_NEWTON * m_kg * inputs.K_B)


# ------------------------------------------------------------------------------------------ self-check
if __name__ == "__main__":
    M, l = 1.0, 9.0
    f = _sds_f(M, l)
    fp = lambda r: 2 * M / r ** 2 - 2 * r / l ** 2          # hand derivative: second route only
    rb, rc = sds_horizons(M, l)
    print(f"SdS M = 1, l = 9: r_b = {rb:.12f}, r_c = {rc:.12f}, f = {f(rb):.1e}, {f(rc):.1e}")
    print(f"  Vieta: r_b r_c (r_b + r_c) / (2 M l^2) = {rb * rc * (rb + rc) / (2 * M * l * l):.15f};"
          f" (r_b^2 + r_b r_c + r_c^2)/l^2 = {(rb * rb + rb * rc + rc * rc) / l ** 2:.15f}")
    kb = killing_kappa(f, rb * (1 + 1e-6), 1e-8 * rb)
    kc = killing_kappa(f, rc * (1 - 1e-6), 1e-8 * rc)
    sb, sc = kappa_from_spin_connection(M, l)
    print(f"  kappa_b: Killing {kb:.10f}  spin connection {sb:.10f}  |f'|/2 {fp(rb) / 2:.10f}")
    print(f"  kappa_c: Killing {kc:.10f}  spin connection {sc:.10f}  |f'|/2 {-fp(rc) / 2:.10f}")
    print(f"  Killing vs |f'(r0)|/2 at the same r0 = r_h(1 +- 1e-6) (the offset above is the r0 shift):"
          f" {kb / (fp(rb * (1 + 1e-6)) / 2) - 1:.1e}, {kc / (-fp(rc * (1 - 1e-6)) / 2) - 1:.1e}")
    for beta, lab in ((2 * math.pi / sb, "2 pi/kappa_b"), (8 * math.pi, "8 pi")):
        cr = euclidean_cone_ratio(f, rb, beta, 1e-7 * rb)
        print(f"  Euclidean cone ratio, beta = {lab}: {cr:.9f}  (beta kappa/2pi = {beta * sb / (2 * math.pi):.9f})")
    fl = lambda r: 1 - 2 * 1.0 / r
    print(f"  Schwarzschild: Killing kappa at 2(1+1e-7) = {killing_kappa(fl, 2 * (1 + 1e-7), 1e-9):.9f} (1/4M = 0.25)")

    print("Kerr first law (exact):", kerr_first_law(Fraction(7, 2), Fraction(3, 5), 1, 1),
          kerr_first_law(Fraction(3), Fraction(0), 0, 1))
    p, q = 3.5, 0.6
    def kerr_float(p, q):
        Mm, a = (p + q) / 2, math.sqrt(p * q)
        return Mm, math.pi * (p * p + a * a), (p - q) / (4 * math.pi * (p * p + a * a)), a / (p * p + a * a), Mm * a
    hh = 1e-6
    A, B = kerr_float(p + hh, q + hh), kerr_float(p - hh, q - hh)
    Mm, S, T, Om, J = kerr_float(p, q)
    print(f"  float route, a = sqrt(pq), central differences: first = "
          f"{(A[0] - B[0]) - T * (A[1] - B[1]) - Om * (A[4] - B[4]):.2e}, smarr = {Mm - 2 * T * S - 2 * Om * J:.2e}")

    r, b = photon_sphere()
    print(f"photon sphere r = {r:.15f}, b_c = {b:.15f}   (closed form 3, sqrt27 = {math.sqrt(27):.15f})")
    ri, L2, E2 = isco()
    print(f"ISCO r = {ri:.12f}, L^2 = {L2:.12f}, E^2 = {E2:.12f}   (closed form 6, 12, 8/9 = {8 / 9:.12f})")
    def sign_changes(L2v):
        V = lambda x: fl(x) * (1 + L2v / (x * x))
        dV = [float(toolkit.exact_derivative(lambda s: (1 - 2 / s) * (1 + Fraction(L2v) / (s * s)),
                                             Fraction(2 + 0.01 * k))) for k in range(1, 4801)]
        return sum(1 for u, v in zip(dV, dV[1:]) if (u > 0) != (v > 0))
    print(f"  circular orbits (V' sign changes on (2, 50)): L^2 (1-1e-3): {sign_changes(L2 * (1 - 1e-3))},"
          f" L^2 (1+1e-3): {sign_changes(L2 * (1 + 1e-3))}")

    Lam = inputs.LAMBDA_SI
    Mn = nariai_mass_kg(Lam)
    closed = inputs.C_LIGHT ** 2 / (3 * math.sqrt(Lam) * inputs.G_NEWTON)
    Msun_kg = inputs.GM_SUN / inputs.G_NEWTON
    print(f"Nariai mass (Lambda = {Lam:.4e} m^-2): {Mn:.6e} kg = {Mn / Msun_kg:.6e} M_sun;"
          f" closed form c^2/(3 G sqrt Lam) = {closed:.6e} kg")
    ln = desitter.ell_from_lambda(Lam)
    Mg = Mn * inputs.G_NEWTON / inputs.C_LIGHT ** 2
    print(f"  horizons at M(1 - 1e-6): {sds_horizons(Mg * (1 - 1e-6), ln) is not None},"
          f" at M(1 + 1e-6): {sds_horizons(Mg * (1 + 1e-6), ln) is not None}")

    def pull(pred, meas):
        val, lo, hi = meas
        sig = hi if pred > val else lo
        return (pred - val) / sig

    m87, m87_err, m87_d = inputs.M87_STARS
    th_m87 = shadow_uas(m87, m87_d) / (2 * b)
    th_m87_err = th_m87 * m87_err / m87
    print(f"M87*: theta_g = shadow/(2 b_c) = {th_m87:.4f} +- {th_m87_err:.4f} uas (stellar-dynamics mass);"
          f" shadow {shadow_uas(m87, m87_d):.3f} uas; EHT {inputs.THETA_G_M87}; pull {pull(th_m87, inputs.THETA_G_M87):+.3f}")
    ths = [shadow_uas(mm, dd) / (2 * b) for mm, dd in (inputs.SGRA_VLTI, inputs.SGRA_KECK)]
    th_sgr = sum(ths) / 2
    print(f"Sgr A*: theta_g VLTI {ths[0]:.4f}, Keck {ths[1]:.4f}, average {th_sgr:.4f} uas; EHT {inputs.THETA_G_SGRA};"
          f" pull {pull(th_sgr, inputs.THETA_G_SGRA):+.3f}")

    z = inputs.GW_Z[0]
    A1, A2 = kerr_area_km2(inputs.GW_M1[0], 0.0), kerr_area_km2(inputs.GW_M2[0], 0.0)
    mf_rd, chi_rd = invert_220(inputs.F220[0], inputs.G220[0], z)
    Af = kerr_area_km2(mf_rd, chi_rd)
    print(f"GW250114: A_initial = {A1:.1f} + {A2:.1f} = {A1 + A2:.1f} km^2; ringdown-only 220 ->"
          f" M_f = {mf_rd:.2f} M_sun, chi_f = {chi_rd:.4f}, A_final = {Af:.1f} km^2; A_f/A_i = {Af / (A1 + A2):.4f}")
    # crude spread of A_f over the 220 measurement box (corners), for orientation only
    corners = []
    for df in (-inputs.F220[1], inputs.F220[2]):
        for dg in (-inputs.G220[1], inputs.G220[2]):
            mm, cc = invert_220(inputs.F220[0] + df, inputs.G220[0] + dg, z)
            corners.append(kerr_area_km2(mm, cc))
    print(f"  A_final over the (f, gamma) 1-sigma box: {min(corners):.1f} .. {max(corners):.1f} km^2")
    f_full, g_full = qnm_220(inputs.GW_MF * (1 + z), inputs.GW_CHIF)
    print(f"  full-signal remnant ({inputs.GW_MF} M_sun, chi {inputs.GW_CHIF}, z {z}): f220 = {f_full:.2f} Hz"
          f" (pull {pull(f_full, inputs.F220):+.3f}), damping = {g_full:.2f} /s (pull {pull(g_full, inputs.G220):+.3f})")
    mm, cc = invert_220(f_full, g_full, z)
    # bisection inverse of Q(chi) as the second route
    _, _, _, q1, q2, q3 = inputs.BCW_220
    Qt = math.pi * f_full / g_full
    cb = toolkit.bisect(lambda c: _bcw(c)[1] - Qt, 0.0, 1 - 1e-12)
    print(f"  round trip: M = {mm:.10f}, chi = {cc:.12f} (bisection chi = {cb:.12f})")
    mkg = inputs.GW_MF * Msun_kg
    TH = hawking_K(mkg)
    kap_SI = inputs.C_LIGHT ** 4 / (4 * inputs.G_NEWTON * mkg)
    print(f"  Hawking temperature of the remnant: {TH:.4e} K (hbar kappa/(2 pi c k_B) = "
          f"{inputs.HBAR * kap_SI / (2 * math.pi * inputs.C_LIGHT * inputs.K_B):.4e} K)")
