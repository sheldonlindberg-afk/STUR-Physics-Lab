#!/usr/bin/env python3
"""
Black holes: the strong-field end of gravity's side column (SYMMETRY_LADDER.md, rung 6).

A black hole is not a point where a symmetry breaks, so this rung does not extend the
chain 3-3-1 -> Standard Model -> electromagnetism. It sits in gravity's column beside the
chain, at the strong-field end, and it is the first place hbar, G, c and k_B all appear in
one formula, T_H = hbar c^3 / (8 pi G M k_B). It reuses rung 5's static spherical tetrad,
spin connection and Einstein tensor (src/macdowell_mansouri.py).

Units: G = c = 1 in the symbolic checks; SI in the numbers.

  H1  Horizon and temperature. f(r_h) = 0; the surface gravity is kappa = f'(r_h)/2, and it
      is read off rung 5's spin connection: omega^0_{1 t} = f'/2 on any static spherical
      metric. T_H = hbar c kappa / (2 pi k_B), kappa in 1/m. (CHECK; the Hawking formula is
      LIT: Hawking 1975, quantum fields on a fixed background.)
  H2  The Euclidean check. With t = -i tau, the (tau, r) plane near r_h is
      d(rho)^2 + kappa^2 rho^2 d(tau)^2 exactly to leading order, because d sqrt(f)/d rho =
      f'/2 for any f. The plane is smooth only if tau has period 2 pi / kappa; any other
      period is a cone. So the temperature 1/period is fixed by the geometry. Checked
      symbolically for any f, and numerically on both Schwarzschild-de Sitter horizons. (CHECK)
  H3  Thermodynamics, S = A / 4 l_P^2. Schwarzschild: dM = T dS and Smarr M = 2 T S.
      Kerr (horizon quantities quoted, LIT: Bardeen-Carter-Hawking 1973): dM = T dS + Omega dJ
      and M = 2 T S + 2 Omega J, exactly, in exact rational arithmetic. Reissner-Nordstrom,
      with kappa derived from its f: dM = T dS + Phi dQ and M = 2 T S + Phi Q. (CHECK)
  H4  Schwarzschild-de Sitter: two horizons, two temperatures. They merge at the Nariai
      limit 9 M^2 Lambda = 1 (G = c = 1), at r = 3M, where both kappas vanish. With the
      measured Lambda, the largest black hole the universe allows: M = c^2 / (3 G sqrt(Lambda)).
      (CHECK; LIT Lambda)
  H5  Geodesics, from the effective potentials: photon sphere 3M, critical impact parameter
      (the shadow radius seen from far away) sqrt(27) M, innermost stable circular orbit 6M
      with L^2 = 12 M^2 and E = sqrt(8/9). (CHECK)
  H6  Event Horizon Telescope: the predicted shadow diameters of M87* and Sgr A*, from
      masses and distances measured without the EHT, against the measured ring diameters.
      (CHECK against LIT data)
  H7  GW250114, Hawking's area law. Initial area: the published component masses, any spin
      up to 0.26. Final: the mass and spin from the ringdown-only 220 fit, inverted; the
      full-signal remnant is not used, because it assumes GR and obeys the area law by
      construction. The final area exceeds the initial one even at the least favourable
      corners of the published ranges. (CHECK against LIT data)
  H8  GW250114's full-signal remnant predicts the 220 mode (Berti-Cardoso-Will fit); the
      ringdown alone measures it. (CHECK against LIT data)
  Link 4 (rung 6 -> 4): design A's diamond has a Schwarzschild radius of 2.2e-41 m, a
      millionth of the Planck length.
  Link 5 (rung 6 -> link 3): a black hole of one Planck mass has k_B T_H = M_Pl c^2 / 8 pi,
      1/(8 pi) of the 3-3-1 cutoff, and a radius of 2 l_P: the formula is used where it is
      no longer trusted. (CHECK)
Labels: CHECK, LIT. Not measured: Hawking radiation (under stated assumptions: quantum
fields on a classical background); the information paradox (open).
"""
import math

import sympy as sp

import macdowell_mansouri as MM
import stur_gravity_full as GF

r, th = MM.r, MM.th
M, Q, l = sp.symbols("M Q l", positive=True)

# ------------------------------------------------------------------------------- inputs
G = 6.67430e-11               # m^3 kg^-1 s^-2 (CODATA 2018)
HBAR = 1.054571817e-34        # J s
C = 2.99792458e8              # m/s
KB = 1.380649e-23             # J/K
E_CH = 1.602176634e-19        # C
GM_SUN = 1.32712440018e20     # m^3 s^-2 (IAU)
PC = 3.0856775814913673e16    # m
UAS = math.pi / (180 * 3600e6)  # one micro-arcsecond in radians
LAMBDA_SI = 1.1056e-52        # m^-2 (Planck 2018)
L_PLANCK = 1.616255e-35       # m
M_PLANCK_GEV = 1.220890e19    # GeV, the 3-3-1 cutoff (src/m331_exact.py)

# EHT ring diameters (68%): M87*: EHT 2019, ApJL 875, L1; Sgr A*: EHT 2022, ApJL 930, L12.
RING_M87, RING_M87_ERR = 42.0, 3.0               # micro-arcseconds
RING_SGRA, RING_SGRA_ERR = 51.8, 2.3
# Masses and distances measured without the EHT.
# M87*: stellar dynamics, Gebhardt et al., ApJ 729, 119 (2011): (6.6 +- 0.4) e9 Msun at an
# assumed 17.9 Mpc. A dynamical mass scales with the assumed distance, so M/D does not
# depend on it. (Gas dynamics, Walsh et al. 2013, gives 3.5e9: GAS_M87 below.)
M87_MASS, M87_MASS_ERR, M87_DIST = 6.6e9, 0.4e9, 17.9e6
M87_GAS_MASS = 3.5e9
# Sgr A*: stellar orbits. GRAVITY, A&A 657, L12 (2022): 4.297e6 Msun, 8277 pc.
# Keck, Do et al., Science 365, 664 (2019): 3.975e6 Msun, 7935 pc. Their M/D differ by 3.5%,
# more than either error, so the spread is taken as the uncertainty.
SGRA_VLTI = (4.297e6, 8277.0)
SGRA_KECK = (3.975e6, 7935.0)
# How far the bright ring can sit from the shadow edge, and the Kerr spread of the shadow
# with spin and inclination (at most about 7%, all toward smaller): taken as 5% at 1 sigma.
RING_SYST = 0.05

# GW250114, LVK, PRL 135, 111403 (2025), arXiv:2509.08054 (NRSur7dq4, 90% intervals).
GW_M1, GW_M1_LO, GW_M1_HI = 33.6, 0.8, 1.2       # Msun, source frame
GW_M2, GW_M2_LO, GW_M2_HI = 32.2, 1.3, 0.8
GW_CHI_MAX = 0.26                                # chi_1, chi_2 <= 0.26
GW_MF, GW_MF_LO, GW_MF_HI = 62.7, 1.1, 1.0
GW_CHIF, GW_CHIF_ERR = 0.68, 0.01
GW_Z, GW_Z_ERR = 0.09, 0.01
F220, F220_ERR = 247.0, 6.0                      # Hz, redshifted, ringdown-only fit
G220, G220_LO, G220_HI = 221.0, 32.0, 39.0       # Hz, damping rate
# Berti, Cardoso and Will, PRD 73, 064030 (2006), Table VIII, l = m = 2, n = 0:
# M omega = f1 + f2 (1 - j)^f3; quality factor Q = q1 + q2 (1 - j)^q3. Accurate to a few
# per cent over 0 < j < 0.99.
BCW_220 = (1.5251, -1.1568, 0.1292, 0.7000, 1.4187, -0.4990)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ------------------------------------------------------------------- H1, H2: temperature
def surface_gravity_from_spin_connection():
    """omega^0_{1 t} of rung 5's tetrad equals f'/2 for any f(r)."""
    f = sp.Function("f")(r)
    E, g = MM.static_spherical(f)
    w = MM.spin_connection(E, g)
    return sp.simplify(w[0][1][0] - sp.diff(f, r) / 2)


def euclidean_ratio():
    """rho = proper radial distance from the horizon. d sqrt(f) / d rho = f'/2, so near the
    horizon the circumference of a circle of period beta, beta sqrt(f), over 2 pi rho tends
    to beta kappa / 2 pi. Returns d sqrt(f)/d rho - f'/2 (zero for any f)."""
    f = sp.Function("f")(r)
    drho_dr = 1 / sp.sqrt(f)
    return sp.simplify(sp.diff(sp.sqrt(f), r) / drho_dr - sp.diff(f, r) / 2)


def euclidean_cone(f, fp, rh, beta, eps):
    """Circumference / (2 pi x radius) of the Euclidean (tau, r) circle at r_h + eps, for a
    tau period beta: 1 if smooth, otherwise a cone. rho = int dr / sqrt(f) with r = r_h + u^2."""
    n = 200
    U = math.sqrt(eps)
    h = U / n
    g = lambda u: 2 * u / math.sqrt(abs(f(rh + u * u))) if u > 0 else 2 / math.sqrt(abs(fp(rh)))
    rho = h / 3 * sum((1 if k in (0, n) else 4 if k % 2 else 2) * g(k * h) for k in range(n + 1))
    return beta * math.sqrt(abs(f(rh + eps))) / (2 * math.pi * rho)


def sds_horizons(Mv, lv):
    """Positive roots of r f = r - 2M - r^3/l^2 (bisection): black-hole and cosmological."""
    F = lambda x: x - 2 * Mv - x**3 / lv**2
    rm = lv / math.sqrt(3)                         # maximum of F
    def bis(a, b):
        for _ in range(200):
            m = (a + b) / 2
            if (F(a) > 0) == (F(m) > 0):
                a = m
            else:
                b = m
        return (a + b) / 2
    return bis(2 * Mv, rm), bis(rm, lv)


def euclidean_checks():
    """Schwarzschild-de Sitter, M = 1, l = 9 (27 M^2 / l^2 = 1/3): the period 2 pi / kappa
    is smooth at each horizon, and each horizon wants a different period."""
    Mv, lv = 1.0, 9.0
    f = lambda x: 1 - 2 * Mv / x - x * x / lv**2
    fp = lambda x: 2 * Mv / x**2 - 2 * x / lv**2
    rb, rc = sds_horizons(Mv, lv)
    kb, kc = fp(rb) / 2, -fp(rc) / 2
    out = {}
    for name, rh, k in (("black hole", rb, kb), ("cosmological", rc, kc)):
        out[name] = (rh, k, euclidean_cone(f, fp, rh, 2 * math.pi / k, 1e-7 * rh),
                     euclidean_cone(f, fp, rh, 1.1 * 2 * math.pi / k, 1e-7 * rh))
    return out


# --------------------------------------------------------------------- H3: thermodynamics
def thermodynamics():
    """First laws and Smarr relations, symbolic and exact. Returns a dict of residuals."""
    rp, rm = sp.symbols("r_p r_m", positive=True)
    res = {}
    # Schwarzschild: kappa from rung 5's f.
    f = 1 - 2 * M / r
    rh = sp.solve(f, r)[0]
    kap = sp.diff(f, r).subs(r, rh) / 2
    T = kap / (2 * sp.pi)
    S = 4 * sp.pi * rh**2 / 4
    res["schw_first_law"] = sp.simplify(1 - T * sp.diff(S, M))
    res["schw_smarr"] = sp.simplify(M - 2 * T * S)
    # Kerr in terms of the two horizon radii: M = (r+ + r-)/2, a^2 = r+ r-.
    Mk, a2 = (rp + rm) / 2, rp * rm
    a = sp.sqrt(a2)
    A = 4 * sp.pi * (rp**2 + a2)
    Tk = (rp - rm) / (4 * sp.pi * (rp**2 + a2))
    Om = a / (rp**2 + a2)
    J = Mk * a
    Sk = A / 4
    for x in (rp, rm):
        res[f"kerr_first_law_d{x}"] = sp.simplify(sp.diff(Mk, x) - Tk * sp.diff(Sk, x) - Om * sp.diff(J, x))
    res["kerr_smarr"] = sp.simplify(Mk - 2 * Tk * Sk - 2 * Om * J)
    chi = sp.Symbol("chi", positive=True)
    res["kerr_area_formula"] = sp.simplify(
        (4 * sp.pi * (rp**2 + a2)).subs({rp: M * (1 + sp.sqrt(1 - chi**2)), rm: M * (1 - sp.sqrt(1 - chi**2))})
        - 8 * sp.pi * M**2 * (1 + sp.sqrt(1 - chi**2)))
    # Reissner-Nordstrom: f = 1 - 2M/r + Q^2/r^2, kappa derived from f, Phi = Q / r+.
    fq = (r - rp) * (r - rm) / r**2
    Mq, Q2 = (rp + rm) / 2, rp * rm
    kq = sp.diff(fq, r).subs(r, rp) / 2
    Tq, Sq = kq / (2 * sp.pi), sp.pi * rp**2
    Qq = sp.sqrt(Q2)
    Phi = Qq / rp
    res["rn_f_matches"] = sp.simplify(fq - (1 - 2 * Mq / r + Q2 / r**2))
    for x in (rp, rm):
        res[f"rn_first_law_d{x}"] = sp.simplify(sp.diff(Mq, x) - Tq * sp.diff(Sq, x) - Phi * sp.diff(Qq, x))
    res["rn_smarr"] = sp.simplify(Mq - 2 * Tq * Sq - Phi * Qq)
    return res


# ------------------------------------------------------------------ H4: Schwarzschild-de Sitter
def nariai():
    """Double root of f = 1 - 2M/r - r^2/l^2: f = f' = 0. Returns (r, l^2) and the residual
    of 9 M^2 Lambda - 1 with Lambda = 3/l^2."""
    f = 1 - 2 * M / r - r**2 / l**2
    sol = sp.solve([sp.numer(sp.together(f)), sp.numer(sp.together(sp.diff(f, r)))], [r, l], dict=True)
    sol = [s for s in sol if s[r].is_positive and s[l].is_positive][0]
    return sol[r], sol[l] ** 2, sp.simplify(9 * M**2 * 3 / sol[l] ** 2 - 1)


def sds_temperatures(x):
    """kappa_b and kappa_c (units of 1/M) for 27 M^2 / l^2 = x; both vanish as x -> 1."""
    Mv = 1.0
    lv = math.sqrt(27 / x)
    rb, rc = sds_horizons(Mv, lv)
    fp = lambda y: 2 * Mv / y**2 - 2 * y / lv**2
    return rb, rc, fp(rb) / 2, -fp(rc) / 2


def nariai_numbers():
    """Measured Lambda: Nariai mass, radius; de Sitter temperature of the empty universe."""
    m = C**2 / (3 * G * math.sqrt(LAMBDA_SI))      # GM/c^2 = 1 / (3 sqrt(Lambda))
    radius = 1 / math.sqrt(LAMBDA_SI)               # r = 3 GM / c^2
    t_ds = HBAR * C * math.sqrt(LAMBDA_SI / 3) / (2 * math.pi * KB)
    return m, m * G / GM_SUN, radius, t_ds


# --------------------------------------------------------------------------- H5: geodesics
def geodesics():
    f = 1 - 2 * M / r
    Vph = f / r**2                                  # photons: (dr/dl)^2 = 1/b^2 - f/r^2
    r_ph = [s for s in sp.solve(sp.diff(Vph, r), r) if s.is_positive][0]
    b_c = sp.simplify(1 / sp.sqrt(Vph.subs(r, r_ph)))
    L2 = sp.Symbol("L2", positive=True)
    V = f * (1 + L2 / r**2)                         # massive: E^2 = (dr/dtau)^2 + V
    L2c = sp.solve(sp.diff(V, r), L2)[0]            # circular orbits
    r_isco = [s for s in sp.solve(sp.diff(L2c, r), r) if s.is_positive and s != 3 * M][0]
    stab = sp.factor(sp.simplify(sp.diff(V, r, 2).subs(L2, L2c)))   # sign of V'' on circular orbits
    E2 = sp.simplify(V.subs(L2, L2c).subs(r, r_isco))
    return r_ph, b_c, r_isco, sp.simplify(L2c.subs(r, r_isco)), E2, stab


# ------------------------------------------------------------------------------ H6: EHT
def shadow_diameter_uas(m_sun, d_pc):
    """Schwarzschild shadow diameter 2 sqrt(27) GM / (c^2 D) in micro-arcseconds."""
    return 2 * math.sqrt(27) * m_sun * GM_SUN / C**2 / (d_pc * PC) / UAS


def eht():
    out = {}
    p = shadow_diameter_uas(M87_MASS, M87_DIST)
    s_pred = M87_MASS_ERR / M87_MASS
    sig = math.sqrt((RING_M87_ERR / RING_M87) ** 2 + s_pred**2 + RING_SYST**2)
    out["M87*"] = (p, RING_M87, RING_M87_ERR, (RING_M87 / p - 1) / sig, shadow_diameter_uas(M87_GAS_MASS, M87_DIST))
    pv, pk = shadow_diameter_uas(*SGRA_VLTI), shadow_diameter_uas(*SGRA_KECK)
    p = (pv + pk) / 2
    s_pred = abs(pv - pk) / p
    sig = math.sqrt((RING_SGRA_ERR / RING_SGRA) ** 2 + s_pred**2 + RING_SYST**2)
    out["Sgr A*"] = (p, RING_SGRA, RING_SGRA_ERR, (RING_SGRA / p - 1) / sig, (pv, pk))
    return out


# ------------------------------------------------------------------------- H7: GW250114
def kerr_area_km2(m_sun, chi):
    rg = m_sun * GM_SUN / C**2 / 1e3                # GM/c^2 in km
    return 8 * math.pi * rg**2 * (1 + math.sqrt(1 - chi**2))


def invert_220(freq, damp, z):
    """Remnant source-frame mass (Msun) and spin from the 220 frequency and damping rate
    alone, by inverting the Berti-Cardoso-Will fit: Q = pi f / gamma fixes the spin, then
    M omega fixes the mass. Uses no inspiral or merger data."""
    f1, f2, f3, q1, q2, q3 = BCW_220
    qual = math.pi * freq / damp
    chi = 1 - ((qual - q1) / q2) ** (1 / q3)
    m_det = (f1 + f2 * (1 - chi) ** f3) / (2 * math.pi * freq * GM_SUN / C**3)
    return m_det / (1 + z), chi


def area_law():
    """Initial area from the published component masses, spins anywhere in 0..0.26; final
    area from the ringdown-only 220 fit (not from the full-signal remnant, which assumes GR
    and obeys the area law by construction). Medians, and the least favourable corners of
    the 90% ranges (largest initial area, smallest final area)."""
    a_i = kerr_area_km2(GW_M1, 0) + kerr_area_km2(GW_M2, 0)
    mf, chif = invert_220(F220, G220, GW_Z)
    a_f = kerr_area_km2(mf, chif)
    a_i_max = kerr_area_km2(GW_M1 + GW_M1_HI, 0) + kerr_area_km2(GW_M2 + GW_M2_HI, 0)
    a_f_min = min(kerr_area_km2(*invert_220(f, g, z)) for f in (F220 - F220_ERR, F220 + F220_ERR)
                  for g in (G220 - G220_LO, G220 + G220_HI) for z in (GW_Z - GW_Z_ERR, GW_Z + GW_Z_ERR))
    return a_i, a_f, a_i_max, a_f_min, (mf, chif)


def qnm_220(m_det_sun, chi):
    f1, f2, f3, q1, q2, q3 = BCW_220
    t_m = m_det_sun * GM_SUN / C**3                  # GM/c^3 in s
    omega = (f1 + f2 * (1 - chi) ** f3) / t_m
    qual = q1 + q2 * (1 - chi) ** q3
    freq = omega / (2 * math.pi)
    return freq, omega / (2 * qual)                  # frequency (Hz), damping rate 1/tau (Hz)


def ringdown():
    f, g = qnm_220((1 + GW_Z) * GW_MF, GW_CHIF)
    # spread of the prediction from z, M_f and chi_f, each moved alone across its range
    fs, gs = [], []
    for z, mf, ch in ((GW_Z + GW_Z_ERR, GW_MF, GW_CHIF), (GW_Z - GW_Z_ERR, GW_MF, GW_CHIF),
                      (GW_Z, GW_MF + GW_MF_HI, GW_CHIF), (GW_Z, GW_MF - GW_MF_LO, GW_CHIF),
                      (GW_Z, GW_MF, GW_CHIF + GW_CHIF_ERR), (GW_Z, GW_MF, GW_CHIF - GW_CHIF_ERR)):
        a, b = qnm_220((1 + z) * mf, ch)
        fs.append(a - f)
        gs.append(b - g)
    return f, g, math.sqrt(sum(x * x for x in fs) / 2), math.sqrt(sum(x * x for x in gs) / 2)


def hawking_temperature(m_kg):
    return HBAR * C**3 / (8 * math.pi * G * m_kg * KB)


# ------------------------------------------------------------------------ links 4 and 5
def links():
    rs = 2 * G * GF.design_a()["m"] / C**2          # design A's diamond, from its one source
    mpl_kg = math.sqrt(HBAR * C / G)
    kT_gev = KB * hawking_temperature(mpl_kg) / E_CH / 1e9
    mpl_gev = mpl_kg * C**2 / E_CH / 1e9
    rs_pl = 2 * G * mpl_kg / C**2 / math.sqrt(HBAR * G / C**3)
    return rs, rs / L_PLANCK, mpl_gev, kT_gev, kT_gev * 8 * math.pi / M_PLANCK_GEV, rs_pl


def main():
    banner("H1  Horizon and surface gravity, from rung 5's spin connection (CHECK)")
    print(f"   omega^0_(1 t) - f'/2 = {surface_gravity_from_spin_connection()}  (any static spherical f)")
    print("   kappa = f'(r_h)/2; Schwarzschild: r_h = 2M, kappa = 1/(4M), T_H = hbar c^3/(8 pi G M k_B)")

    banner("H2  The Euclidean check: smooth only for tau-period 2 pi / kappa (CHECK)")
    print(f"   d sqrt(f) / d rho - f'/2 = {euclidean_ratio()}  ->  circumference/(2 pi rho) -> beta kappa / 2 pi")
    for name, (rh, k, ok, cone) in euclidean_checks().items():
        print(f"   SdS (M = 1, l = 9), {name:12s} horizon r = {rh:.6f}, kappa = {k:.6f}: ratio {ok:.8f}"
              f" with beta = 2 pi/kappa; {cone:.6f} with beta 10% longer (a cone)")

    banner("H3  Thermodynamics, S = A/4 (CHECK; Kerr horizon quantities LIT)")
    for k, v in thermodynamics().items():
        print(f"   {k:28s} residual = {v}")

    banner("H4  Schwarzschild-de Sitter: two horizons, two temperatures, the Nariai limit (CHECK)")
    rN, l2N, res = nariai()
    print(f"   f = f' = 0 at r = {rN}, l^2 = {l2N}: 9 M^2 Lambda - 1 = {res}")
    for x in (0.3, 0.9, 0.99, 0.9999):
        rb, rc, kb, kc = sds_temperatures(x)
        print(f"   27M^2/l^2 = {x:<7}: r_b = {rb:.4f} M, r_c = {rc:.4f} M, kappa_b = {kb:.5f}/M, kappa_c = {kc:.5f}/M")
    m, msun, rad, tds = nariai_numbers()
    print(f"   Measured Lambda: the largest black hole has M = {m:.3e} kg = {msun:.3e} M_sun, horizon at {rad:.3e} m")
    print(f"   De Sitter temperature of the cosmological horizon: {tds:.3e} K")

    banner("H5  Geodesics (CHECK)")
    r_ph, b_c, r_isco, L2i, E2, stab = geodesics()
    print(f"   photon sphere r = {r_ph}; shadow radius b_c = {b_c} = sqrt(27) M")
    print(f"   ISCO r = {r_isco}, L^2 = {L2i}, E^2 = {E2}; V'' on circular orbits = {stab}")

    banner("H6  Event Horizon Telescope: shadow against ring (CHECK against LIT)")
    for name, (p, meas, err, pull, extra) in eht().items():
        print(f"   {name:6s}: predicted shadow {p:.1f} uas, measured ring {meas} +- {err} uas: {pull:+.2f} sigma")
    print(f"   (M87* with the gas-dynamics mass instead: {eht()['M87*'][4]:.1f} uas, excluded)")

    banner("H7-H8  GW250114: Hawking's area law, and the 220 mode (CHECK against LIT)")
    a_i, a_f, a_i_max, a_f_min, (mf, chif) = area_law()
    print(f"   ringdown alone: M_f = {mf:.1f} Msun, chi_f = {chif:.2f} (full-signal fit: {GW_MF}, {GW_CHIF})")
    print(f"   initial area {a_i:,.0f} km^2 (spins 0; smaller for any spin), final {a_f:,.0f} km^2")
    print(f"   least favourable corners of the 90% ranges: initial {a_i_max:,.0f}, final {a_f_min:,.0f} km^2")
    f, g, df, dg = ringdown()
    print(f"   220 mode from (1+z) M_f, chi_f: f = {f:.1f} +- {df:.1f} Hz (measured {F220} +- {F220_ERR}),"
          f" damping {g:.0f} +- {dg:.0f} Hz (measured {G220} -{G220_LO} +{G220_HI})")
    print(f"   Hawking temperature of the remnant: {hawking_temperature(GW_MF * GM_SUN / G):.2e} K (unmeasured)")

    banner("Links 4-5: the diamond as a black hole; a Planck-mass black hole (CHECK)")
    rs, ratio, mpl, kT, frac, rs_pl = links()
    print(f"   design A diamond: r_s = {rs:.3e} m = {ratio:.2e} l_P")
    print(f"   Planck-mass black hole: k_B T_H = {kT:.3e} GeV = M_Pl c^2 / 8 pi ({frac:.6f} x 8 pi); r_s = {rs_pl:.4f} l_P")


if __name__ == "__main__":
    main()
