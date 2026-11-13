"""Stage `links` (build 2026-11-b): the links between the rungs.

Every formula is derived in DERIVATION_links.md (section numbers are cited below). Measured numbers come
from `inputs`, read inside the functions; upstream rungs are called as `<stage>.<function>` at call time.
"""
import math
from fractions import Fraction

import inputs
import toolkit
import gauge331
import chiral
import blackholes

PROVENANCE = {
    "qp_qe_minus_anomaly": ("derived", "q_p + q_e and anomaly/N_g are each evaluated in exact Fractions from"
                                       " the SPEC section 8 charge assignments and subtracted; both reduce to"
                                       " Nc (b + Xt) + b + XL, so the difference is identically 0 (section 1)"),
    "neutrality_per_nucleon": ("derived", "Coulomb and gravity are both strength/r on the same trajectories, so"
                                          " the phase ratio is k Q^2/(G m^2) <= GAP_FRACTION; Q_max ="
                                          " m sqrt(F G/k), divided by e and by the nucleon count m/u"
                                          " (section 2)"),
    "pi0_width_eV": ("quoted", "anomaly amplitude A = (alpha/(pi f_pi)) Nc (Qu^2 - Qd^2) quoted (SPEC section"
                               " 8; Adler, Bell-Jackiw). Derived here: the polarization sum m^4/2 (explicit"
                               " transverse polarizations with toolkit.levi_civita), the massless two-body"
                               " phase space 1/(8 pi) and the identical-photon factor 1/2, giving"
                               " A^2 m^3/(64 pi) (section 3)"),
    "planck_mass_GeV": ("derived", "sqrt(hbar c/G) c^2, the only mass that hbar, c, G form, converted from J to"
                                   " GeV with inputs.E_CH (section 4)"),
    "g_window": ("derived", "M_Pl(xG) = mpl x^(-1/2) inverted at each pole: lo = (mpl/p3)^2, hi = (mpl/p5)^2"
                            " (section 5)"),
    "schwarzschild_radius": ("derived", "zero of f = 1 - 2M/r with the geometric mass M = G m/c^2 fixed by the"
                                        " Newtonian limit: r_s = 2 G m/c^2 (section 6)"),
    "matter_charges": ("derived", "gauge331.quark_charges(Nc) weighted by the Nc-quark proton ((Nc+1)/2 u,"
                                  " (Nc-1)/2 d) and neutron (reversed); electron and neutrino are components 2"
                                  " and 1 of gauge331.triplet_charges(X_L, variant) with the SPEC's X_L"
                                  " (section 7)"),
    "pi0_width_from_rungs": ("quoted", "pi0_width_eV (quoted anomaly amplitude; Adler, Bell-Jackiw) at"
                                       " inputs.ALPHA_0, F_PI, M_PI0 with N_c = 3 and the charges derived by"
                                       " gauge331.quark_charges(3) (section 8)"),
    "planck_bh_kT_GeV": ("derived", "k_B blackholes.hawking_K(m) at m = planck_mass_GeV(inputs G, hbar, c)"
                                    " converted to kg, expressed in GeV; equals M_Pl c^2/(8 pi) (section 9)."
                                    " Rests on the quoted blackholes.hawking_K (Hawking 1975 temperature"
                                    " formula): only the Planck mass and the unit conversion are derived here"),
}

_GEV_IN_EV = 10 ** 9


# ------------------------------------------------------------------------------------------
# link 1: neutral matter
# ------------------------------------------------------------------------------------------
def _proton_content(Nc):
    """(number of u, number of d) in the Nc-quark proton."""
    return Fraction(Nc + 1, 2), Fraction(Nc - 1, 2)


def _qp_plus_qe(Nc, b, XL, Xt):
    half = Fraction(1, 2)
    Qu, Qd = half + b + Xt, -half + b + Xt
    Qe = -half + b + XL
    nu, nd = _proton_content(Nc)
    return nu * Qu + nd * Qd + Qe


def _anomaly_per_generation(Nc, b, XL, Xt):
    Ng = Fraction(Nc)
    n = Fraction(1 + Nc, 2)
    Xa = Xt + 2 * b
    return (Ng * XL + Nc * ((Ng - n) * Xt + n * Xa)) / Ng


def qp_qe_minus_anomaly(Nc, b, XL, Xt):
    return _qp_plus_qe(Nc, b, XL, Xt) - _anomaly_per_generation(Nc, b, XL, Xt)


def _lepton_X(variant):
    """SPEC section 2: X_L = -1/3 (beta = -1/sqrt3), -2/3 (beta = +1/sqrt3)."""
    table = {"-1/sqrt3": Fraction(-1, 3), "+1/sqrt3": Fraction(-2, 3)}
    if variant not in table:
        raise ValueError(f"unknown variant {variant!r}")
    return table[variant]


def matter_charges(Nc, variant):
    Qu, Qd = gauge331.quark_charges(Nc)
    nu, nd = _proton_content(Nc)
    q_p = nu * Qu + nd * Qd
    q_n = nd * Qu + nu * Qd
    lepton = gauge331.triplet_charges(_lepton_X(variant), variant)
    return Fraction(q_p), Fraction(q_n), Fraction(lepton[1]), Fraction(lepton[0])


def neutrality_per_nucleon(m):
    q_max = m * math.sqrt(inputs.GAP_FRACTION * inputs.G_NEWTON / inputs.K_COUL)   # coulombs
    nucleons = m / inputs.U_AMU
    return q_max / inputs.E_CH / nucleons


# ------------------------------------------------------------------------------------------
# link 2: pi0 -> gamma gamma
# ------------------------------------------------------------------------------------------
def _epsilon_contract(a, k1, b, k2):
    """eps^{mu nu rho sigma} a_mu k1_nu b_rho k2_sigma (all lower-index components)."""
    total = 0
    for mu in range(4):
        if a[mu] == 0:
            continue
        for nu in range(4):
            if k1[nu] == 0:
                continue
            for rho in range(4):
                if b[rho] == 0:
                    continue
                for sigma in range(4):
                    s = toolkit.levi_civita((mu, nu, rho, sigma))
                    if s:
                        total += s * a[mu] * k1[nu] * b[rho] * k2[sigma]
    return total


def _polarization_sum():
    """sum over photon polarizations of |eps^{mnrs} e1_m k1_n e2_r k2_s|^2 in units of m_pi^4 (exact).

    Rest frame, k1 = (1/2)(1,0,0,1), k2 = (1/2)(1,0,0,-1) (upper), transverse linear polarizations x, y."""
    half = Fraction(1, 2)
    k1 = (half, 0, 0, -half)          # lower indices
    k2 = (half, 0, 0, half)
    pols = ((0, 1, 0, 0), (0, 0, 1, 0))
    return sum(Fraction(_epsilon_contract(e1, k1, e2, k2)) ** 2 for e1 in pols for e2 in pols)


def _two_body_phase_space():
    """int dPhi_2 for two massless particles: (1/(4 pi^2)) (4 pi) (1/4) int dk delta(m - 2k) = 1/(8 pi)."""
    solid_angle = 4 * math.pi
    radial = Fraction(1, 4) * Fraction(1, 2)          # d^3k/(4 k^2) = dOmega dk/4; int dk delta(m - 2k) = 1/2
    return solid_angle * float(radial) / (2 * math.pi) ** 2


def pi0_width_eV(alpha, fpi, mpi, Nc, Qu, Qd):
    amplitude = alpha / (math.pi * fpi) * float(Nc * (Qu * Qu - Qd * Qd))      # quoted, GeV^-1
    summed = amplitude ** 2 * mpi ** 4 * float(_polarization_sum())
    identical = Fraction(1, 2)
    width = float(identical) * summed * _two_body_phase_space() / (2 * mpi)     # GeV
    return width * _GEV_IN_EV


def pi0_width_from_rungs():
    Nc = 3
    Qu, Qd = gauge331.quark_charges(Nc)
    return pi0_width_eV(inputs.ALPHA_0, inputs.F_PI, inputs.M_PI0, Nc, Qu, Qd)


# ------------------------------------------------------------------------------------------
# link 3: the Planck mass and the 3-3-1 poles
# ------------------------------------------------------------------------------------------
def _joule_per_GeV():
    return _GEV_IN_EV * inputs.E_CH


def planck_mass_GeV(G, hbar, c):
    return math.sqrt(hbar * c / G) * c * c / _joule_per_GeV()


def g_window(p3, p5, mpl):
    return (mpl / p3) ** 2, (mpl / p5) ** 2


def schwarzschild_radius(m):
    return 2 * inputs.G_NEWTON * m / inputs.C_LIGHT ** 2


def planck_bh_kT_GeV():
    mpl = planck_mass_GeV(inputs.G_NEWTON, inputs.HBAR, inputs.C_LIGHT)
    m_kg = mpl * _joule_per_GeV() / inputs.C_LIGHT ** 2
    return inputs.K_B * blackholes.hawking_K(m_kg) / _joule_per_GeV()


# ------------------------------------------------------------------------------------------
# self-check: second routes (DERIVATION_links.md)
# ------------------------------------------------------------------------------------------
def _covariant_polarization_sum(E1, E2):
    """sum_{mu,rho} g_mumu g_rhorho (eps^{mu nu rho sigma} k1_nu k2_sigma)^2 / m^4 in a boosted frame."""
    k1 = (E1, 0, 0, -E1)              # lower indices of (E1, 0, 0, E1)
    k2 = (E2, 0, 0, E2)               # lower indices of (E2, 0, 0, -E2)
    g = (1, -1, -1, -1)
    m2 = 4 * E1 * E2
    total = Fraction(0)
    for mu in range(4):
        for rho in range(4):
            emu = tuple(int(i == mu) for i in range(4))
            erho = tuple(int(i == rho) for i in range(4))
            total += g[mu] * g[rho] * Fraction(_epsilon_contract(emu, k1, erho, k2)) ** 2
    return total / m2 ** 2


def _phase_space_numeric(m=1.0, width=0.01, n=4001):
    """(1/(4 pi)) int dk delta(m - 2k) with a Gaussian of the given width for the delta function."""
    lo, hi = m / 2 - 10 * width, m / 2 + 10 * width
    dk = (hi - lo) / (n - 1)
    ys = [math.exp(-(m - 2 * (lo + i * dk)) ** 2 / (2 * width ** 2)) / (width * math.sqrt(2 * math.pi))
          for i in range(n)]
    return toolkit.trapezoid(ys, dk) / (4 * math.pi)


def _neutrality_by_root(m, r):
    """Solve U_Coulomb(eps) + F U_gravity = 0 with both energies built on rung 2's exchange transform."""
    shape = chiral.yukawa(r, 0)
    u_grav = -4 * math.pi * inputs.G_NEWTON * m * m * shape
    def excess(eps):
        Q = m / inputs.U_AMU * eps * inputs.E_CH
        return (4 * math.pi * inputs.K_COUL * Q * Q * shape + inputs.GAP_FRACTION * u_grav) / abs(u_grav)
    return toolkit.bisect(excess, 0.0, 1.0)


def _window_by_root(pole):
    f = lambda t: math.log(planck_mass_GeV(10.0 ** t * inputs.G_NEWTON, inputs.HBAR, inputs.C_LIGHT) / pole)
    return 10.0 ** toolkit.bisect(f, -80.0, 80.0)


if __name__ == "__main__":
    F = Fraction
    print("== qp_qe_minus_anomaly ==")
    pt = (F(2, 7), F(-5, 3), F(11, 13))
    print("  value at a generic point (Nc = 5):", qp_qe_minus_anomaly(5, *pt))
    grads = [toolkit.exact_derivative(lambda t, i=i: qp_qe_minus_anomaly(5, *[t if j == i else pt[j]
                                                                             for j in range(3)]), pt[i])
             for i in range(3)]
    print("  second route: exact partial derivatives in (b, XL, Xt):", grads, " (affine => identically 0)")

    print("== matter_charges ==")
    for variant in ("-1/sqrt3", "+1/sqrt3"):
        b = gauge331.triplet_charges(0, variant)[2] / -2
        for Nc in (1, 3, 5, 7, 9, 11):
            qp, qn, qe, qnu = matter_charges(Nc, variant)
            Qu, Qd = gauge331.quark_charges(Nc)
            Xt = Qu - F(1, 2) - b
            XL = _lepton_X(variant)
            route2 = (qp_qe_minus_anomaly(Nc, b, XL, Xt), _anomaly_per_generation(Nc, b, XL, Xt), qp - qn)
            print(f"  {variant} Nc={Nc:2d}: (q_p, q_n, q_e, Q_nu) = ({qp}, {qn}, {qe}, {qnu});"
                  f" second route (q_p+q_e - anomaly/N_g, anomaly/N_g, q_p - q_n) = "
                  f"({route2[0]}, {route2[1]}, {route2[2]})")

    print("== neutrality_per_nucleon ==")
    a = neutrality_per_nucleon(inputs.GAP_BASELINE_MASS)
    print("  closed form:", a, "e/nucleon")
    print("  second route (bisect on rung-2 energies), m = 1e-14 kg, r = 2e-4 m:",
          _neutrality_by_root(inputs.GAP_BASELINE_MASS, 2e-4))
    print("  second route, m = 3e-12 kg, r = 7e-3 m:", _neutrality_by_root(3e-12, 7e-3))
    print("  requirement / measured bound |q_p + q_e| < EPS_PE_BOUND:", a / inputs.EPS_PE_BOUND)

    print("== pi0_width_eV ==")
    print("  polarization sum / m^4, explicit polarizations (rest frame):", _polarization_sum())
    print("  second route, covariant -g sum, boosted frames:", _covariant_polarization_sum(F(2), F(1, 8)),
          _covariant_polarization_sum(F(5, 3), F(7, 11)))
    print("  phase space: analytic", _two_body_phase_space(), " 1/(8 pi) =", 1 / (8 * math.pi),
          " numeric (Gaussian delta, trapezoid):", _phase_space_numeric())
    w = pi0_width_from_rungs()
    closed = inputs.ALPHA_0 ** 2 * inputs.M_PI0 ** 3 / (64 * math.pi ** 3 * inputs.F_PI ** 2) * _GEV_IN_EV
    print("  width from rungs:", w, "eV;  second route alpha^2 m^3/(64 pi^3 f^2) (anomaly factor 1):", closed)
    for Nc in (5, 7):
        print(f"  rung-1 charges at Nc = {Nc}:",
              pi0_width_eV(inputs.ALPHA_0, inputs.F_PI, inputs.M_PI0, Nc, *gauge331.quark_charges(Nc)))
    print("  measured:", inputs.GAMMA_PI0, "+-", inputs.GAMMA_PI0_ERR, "eV; pull =",
          (w - inputs.GAMMA_PI0) / inputs.GAMMA_PI0_ERR)

    print("== planck_mass_GeV ==")
    mpl = planck_mass_GeV(inputs.G_NEWTON, inputs.HBAR, inputs.C_LIGHT)
    m_kg = mpl * _joule_per_GeV() / inputs.C_LIGHT ** 2
    compton = inputs.HBAR / (m_kg * inputs.C_LIGHT)
    print("  M_Pl =", mpl, "GeV =", m_kg, "kg")
    print("  second route: Compton / (r_s/2) =", compton / (schwarzschild_radius(m_kg) / 2),
          "  Compton / inputs.L_PLANCK =", compton / inputs.L_PLANCK)

    print("== g_window ==")
    for variant, (p3, p5) in inputs.POLES_331.items():
        lo, hi = g_window(p3, p5, mpl)
        print(f"  {variant}: closed form ({lo:.6e}, {hi:.6e});  second route (bisect on M_Pl(xG) = pole):"
              f" ({_window_by_root(p3):.6e}, {_window_by_root(p5):.6e});  contains G_meas: {lo < 1 < hi}")

    print("== schwarzschild_radius ==")
    m = 1e30
    rs = schwarzschild_radius(m)
    M = inputs.G_NEWTON * m / inputs.C_LIGHT ** 2
    print("  2Gm/c^2:", rs, "m;  second route sds_horizons(M, 1e6 M)[0]:", blackholes.sds_horizons(M, 1e6 * M)[0],
          ";  hbar c/(4 pi k_B T_H):",
          inputs.HBAR * inputs.C_LIGHT / (4 * math.pi * inputs.K_B * blackholes.hawking_K(m)))

    print("== planck_bh_kT_GeV ==")
    kT = planck_bh_kT_GeV()
    print("  via rung 6:", kT, "GeV;  second route M_Pl/(8 pi):", mpl / (8 * math.pi),
          ";  T(2 M_Pl)/T(M_Pl) =", blackholes.hawking_K(2 * m_kg) / blackholes.hawking_K(m_kg))
