"""links: where one rung feeds another (SPEC.md section 8 and "Connections between stages").

Derivations and second routes: DERIVATION_links.md. Exact charges are fractions.Fraction.
Upstream rungs are reached only as gauge331.<fn>, blackholes.<fn>, toolkit.<fn> at call time.
"""
import itertools
import math
from fractions import Fraction

import inputs
import toolkit
import gauge331
import blackholes
import graviton  # self-check second route only (rung 4's entangling phase)

PROVENANCE = {
    "qp_qe_minus_anomaly": ("derived", "SPEC 8 charges: q_p + q_e = (N_c+1) b + N_c X_t + X_L and anomaly ="
                                       " N_c X_L + N_c^2 X_t + N_c(1+N_c) b (2n = 1+N_c) = N_g (q_p + q_e);"
                                       " evaluated exactly from the definitions, difference is 0"),
    "neutrality_per_nucleon": ("derived", "Coulomb and gravity both c/r on the same trajectories, phases in ratio"
                                          " k Q^2/(G m^2) <= GAP_FRACTION with Q = eps e m/u => eps = (u/e)"
                                          " sqrt(f G/k), size independent"),
    "pi0_width_eV": ("quoted", "anomaly amplitude A = alpha N_c (Q_u^2 - Q_d^2)/(pi f_pi) quoted (Adler 1969;"
                               " Bell-Jackiw 1969); polarization sum done explicitly with toolkit.levi_civita and"
                               " real transverse polarizations (= m^4/2), two-body phase space p/(4 pi m) = 1/(8 pi)"
                               " and identical-photon 1/2 derived: Gamma = A^2 m^3/(64 pi)"),
    "planck_mass_GeV": ("derived", "SPEC 8 definition M_Pl = sqrt(hbar c/G), times c^2, / (1e9 e) to GeV"),
    "g_window": ("derived", "M_Pl(xG) = x^(-1/2) M_Pl; p5 < M_Pl(xG) < p3 <=> (mpl/p3)^2 < x < (mpl/p5)^2"),
    "schwarzschild_radius": ("derived", "zero of f = 1 - 2GM/(c^2 r): r_s = 2 G m / c^2"),
    "matter_charges": ("derived", "q_p, q_n from gauge331.quark_charges (rung 1, anomaly-derived) with proton"
                                  " ((N_c+1)/2 u, (N_c-1)/2 d); q_e, Q_nu = components 2, 1 of"
                                  " gauge331.triplet_charges(X_L, variant), X_L per SPEC 2"),
    "pi0_width_from_rungs": ("quoted", "pi0_width_eV (quoted ABJ amplitude) at N_c = 3 with rung 1's"
                                       " gauge331.quark_charges(3) and inputs.ALPHA_0, F_PI, M_PI0"),
    "planck_bh_kT_GeV": ("derived", "blackholes.hawking_K (rung 6) at m = planck_mass_GeV * 1e9 e/c^2, times"
                                    " k_B, in GeV; = M_Pl c^2/(8 pi); rests on the quoted Hawking temperature"
                                    " hawking_K, evaluated at the Planck mass"),
}


def _gev_J():
    """1 GeV in joules: 1e9 (the prefix) times the elementary charge."""
    return 1e9 * inputs.E_CH


# ------------------------------------------------------------------------------------------
# 1. the anomaly identity
# ------------------------------------------------------------------------------------------
def _section8_charges(b, XL, Xt):
    half = Fraction(1, 2)
    return {"nu": half + b + XL, "e": -half + b + XL, "u": half + b + Xt, "d": -half + b + Xt,
            "Xa": Xt + 2 * b}


def _nucleons(Nc, Qu, Qd):
    big, small = Fraction(Nc + 1, 2), Fraction(Nc - 1, 2)
    return big * Qu + small * Qd, small * Qu + big * Qd


def _anomaly_331(Nc, XL, Xt, Xa):
    Ng, n = Nc, (1 + Nc) // 2
    return Ng * XL + Nc * ((Ng - n) * Xt + n * Xa)


def qp_qe_minus_anomaly(Nc, b, XL, Xt):
    if Nc < 1 or Nc % 2 == 0:
        raise ValueError("N_c must be a positive odd integer (n = (1+N_c)/2 antitriplet families)")
    b, XL, Xt = Fraction(b), Fraction(XL), Fraction(Xt)
    q = _section8_charges(b, XL, Xt)
    qp, _ = _nucleons(Nc, q["u"], q["d"])
    anomaly = _anomaly_331(Nc, XL, Xt, q["Xa"])
    Ng = Nc
    return (qp + q["e"]) - anomaly / Ng


# ------------------------------------------------------------------------------------------
# 2. matter charges from rung 1
# ------------------------------------------------------------------------------------------
def _lepton_X(variant):
    """SPEC section 2 postulate: X_L = -1/3 (beta = -1/sqrt3), -2/3 (beta = +1/sqrt3)."""
    table = {"-1/sqrt3": Fraction(-1, 3), "+1/sqrt3": Fraction(-2, 3)}
    if variant not in table:
        raise ValueError(f"unknown variant {variant!r}")
    return table[variant]


def matter_charges(Nc, variant):
    Qu, Qd = gauge331.quark_charges(Nc)
    qp, qn = _nucleons(Nc, Fraction(Qu), Fraction(Qd))
    lep = gauge331.triplet_charges(_lepton_X(variant), variant)
    Qnu, qe = Fraction(lep[0]), Fraction(lep[1])
    return qp, qn, qe, Qnu


# ------------------------------------------------------------------------------------------
# 3. the neutrality requirement of the experiment
# ------------------------------------------------------------------------------------------
def neutrality_per_nucleon(m):
    # k (eps e N)^2 <= f G m^2,  N = m/u
    f, G, k = inputs.GAP_FRACTION, inputs.G_NEWTON, inputs.K_COUL
    N = m / inputs.U_AMU
    Qmax = math.sqrt(f * G / k) * m          # coulombs
    return Qmax / (N * inputs.E_CH)


# ------------------------------------------------------------------------------------------
# 4. pi0 -> gamma gamma
# ------------------------------------------------------------------------------------------
def _kallen(x, y, z):
    return x * x + y * y + z * z - 2 * (x * y + y * z + z * x)


def _two_body_momentum(M, m1, m2):
    return math.sqrt(_kallen(M * M, m1 * m1, m2 * m2)) / (2 * M)


def _two_body_phase_space(M, m1, m2):
    """Int dPhi_2 = p / (4 pi M) (isotropic integrand), DERIVATION section 4."""
    return _two_body_momentum(M, m1, m2) / (4 * math.pi * M)


def _eps_contract(a, b, c, d):
    """eps_{mu nu rho sigma} a^mu b^nu c^rho d^sigma, eps_{0123} = +1 (toolkit.levi_civita)."""
    s = 0.0
    for idx in itertools.permutations(range(4)):
        mu, nu, rho, sg = idx
        s += toolkit.levi_civita(idx) * a[mu] * b[nu] * c[rho] * d[sg]
    return s


def _polarization_sum(M):
    """sum over real transverse polarizations of |eps e1 e2 k1 k2|^2, pion rest frame."""
    p = _two_body_momentum(M, 0.0, 0.0)
    k1 = (p, 0.0, 0.0, p)
    k2 = (p, 0.0, 0.0, -p)
    pols = ((0.0, 1.0, 0.0, 0.0), (0.0, 0.0, 1.0, 0.0))   # x_hat, y_hat: transverse to both k
    return sum(_eps_contract(e1, e2, k1, k2) ** 2 for e1 in pols for e2 in pols)


def pi0_width_eV(alpha, fpi, mpi, Nc, Qu, Qd):
    A = alpha / (math.pi * fpi) * Nc * float(Qu * Qu - Qd * Qd)      # quoted ABJ amplitude, GeV^-1
    msq = A * A * _polarization_sum(mpi)
    identical = 2                                                    # 2! for two photons
    gamma_GeV = msq * _two_body_phase_space(mpi, 0.0, 0.0) / (2 * mpi * identical)
    return gamma_GeV * 1e9


def pi0_width_from_rungs():
    Qu, Qd = gauge331.quark_charges(3)
    return pi0_width_eV(inputs.ALPHA_0, inputs.F_PI, inputs.M_PI0, 3, Qu, Qd)


# ------------------------------------------------------------------------------------------
# 5. Planck mass, the G window, Schwarzschild radius, the Planck-mass black hole
# ------------------------------------------------------------------------------------------
def planck_mass_GeV(G, hbar, c):
    m_kg = math.sqrt(hbar * c / G)
    return m_kg * c * c / _gev_J()


def g_window(p3, p5, mpl):
    return (mpl / p3) ** 2, (mpl / p5) ** 2


def schwarzschild_radius(m):
    return 2 * inputs.G_NEWTON * m / inputs.C_LIGHT ** 2


def planck_bh_kT_GeV():
    mpl = planck_mass_GeV(inputs.G_NEWTON, inputs.HBAR, inputs.C_LIGHT)
    m_kg = mpl * _gev_J() / inputs.C_LIGHT ** 2
    T = blackholes.hawking_K(m_kg)
    return inputs.K_B * T / _gev_J()


# ------------------------------------------------------------------------------------------
# self-check: second routes of DERIVATION_links.md
# ------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import random

    print("== 1. anomaly identity")
    rng = random.Random(7)
    worst = 0
    for _ in range(2000):
        Nc = rng.choice((1, 3, 5, 7, 9, 11))
        b, XL, Xt = (Fraction(rng.randint(-99, 99), rng.randint(1, 40)) for _ in range(3))
        q = _section8_charges(b, XL, Xt)
        qp, qn = _nucleons(Nc, q["u"], q["d"])
        closed = (Nc + 1) * b + Nc * Xt + XL
        assert qp + q["e"] == closed == _anomaly_331(Nc, XL, Xt, q["Xa"]) / Nc == qn + q["nu"]
        assert qp_qe_minus_anomaly(Nc, b, XL, Xt) == 0
    print("  2000 random rational models: q_p+q_e = (N_c+1)b + N_c X_t + X_L = anomaly/N_g = q_n+Q_nu, diff = 0")

    print("== 2. matter charges (q_p, q_n, q_e, Q_nu)")
    for v in ("-1/sqrt3", "+1/sqrt3"):
        b = gauge331.triplet_charges(0, v)[0] - Fraction(1, 2)
        assert _lepton_X(v) == -Fraction(1, 2) - b, "SPEC 2's X_L is the one with Q_e = -1"
        for Nc in (3, 5, 7):
            mc = matter_charges(Nc, v)
            Qu, Qd = gauge331.quark_charges(Nc)
            Xt = Qu - Fraction(1, 2) - b
            route2 = qp_qe_minus_anomaly(Nc, b, _lepton_X(v), Xt)
            print(f"  {v:9s} N_c={Nc}: {tuple(str(x) for x in mc)}   (Q_u, Q_d) = ({Qu}, {Qd}),"
                  f" b = {b}, X_L = {_lepton_X(v)}; identity residual {route2}")

    print("== 3. neutrality")
    m = inputs.DESIGN_A_MASS
    eps = neutrality_per_nucleon(m)
    print(f"  eps_max(design A) = {eps:.6e} e/nucleon; at 1e-14 kg and 1e-12 kg: "
          f"{neutrality_per_nucleon(1e-14):.6e}, {neutrality_per_nucleon(1e-12):.6e}")
    print(f"  margin over EPS_PE_BOUND = {inputs.EPS_PE_BOUND:.1e}: {eps / inputs.EPS_PE_BOUND:.4g}x")
    stray = inputs.K_COUL * inputs.E_CH ** 2 / (inputs.G_NEWTON * m * m)
    print(f"  one stray electron per diamond: phi_C/phi_grav = k e^2/(G m^2) = {stray:.4e}"
          f" (= {stray / inputs.GAP_FRACTION:.3e} x the allowed fraction)")
    # second route: explicit phases on design A's trajectory at a sample gap
    gap = 2e-4
    hold, ramp, dx = inputs.DESIGN_A_HOLD, inputs.DESIGN_A_RAMP, inputs.DESIGN_A_DX
    n = 4001
    T = hold + 2 * ramp

    def phase(coupling):          # U(r) = coupling / r
        ws = []
        for i in range(n):
            sep = dx * graviton.ramp_profile(T * i / (n - 1), hold, ramp)
            ws.append(-2 * coupling / gap + 2 * coupling / math.sqrt(gap * gap + sep * sep))
        return toolkit.trapezoid(ws, T / (n - 1)) / inputs.HBAR

    phig = phase(-inputs.G_NEWTON * m * m)
    phig_rung4 = graviton.entangling_phase(m, dx, hold, ramp, gap)
    N = m / inputs.U_AMU

    def excess(logeps):
        Q = math.exp(logeps) * inputs.E_CH * N
        return abs(phase(inputs.K_COUL * Q * Q)) - inputs.GAP_FRACTION * abs(phig)
    eps2 = math.exp(toolkit.bisect(excess, math.log(1e-25), math.log(1e-15), iters=80))
    print(f"  route 2: phi_grav = {phig:.6e} rad (graviton.entangling_phase: {phig_rung4:.6e});"
          f" bisected eps = {eps2:.6e}, rel diff {abs(eps2 / eps - 1):.1e}")

    print("== 4/5. pi0 -> gamma gamma")
    S = _polarization_sum(inputs.M_PI0)
    k1k2 = inputs.M_PI0 ** 2 / 2
    print(f"  polarization sum / m^4 = {S / inputs.M_PI0 ** 4:.15f}; covariant 2(k1.k2)^2/m^4 ="
          f" {2 * k1k2 ** 2 / inputs.M_PI0 ** 4:.15f}")
    # phase space by integrating a narrow normalized Gaussian delta(m - 2p)
    M = inputs.M_PI0
    sig = M * 1e-3
    npts = 4001
    lo_p, hi_p = M / 2 - 10 * sig, M / 2 + 10 * sig
    dp = (hi_p - lo_p) / (npts - 1)
    ys = []
    for i in range(npts):
        p = lo_p + i * dp
        delta = math.exp(-((M - 2 * p) ** 2) / (2 * sig * sig)) / (sig * math.sqrt(2 * math.pi))
        ys.append(4 * math.pi * p * p / (4 * math.pi ** 2 * 4 * p * p) * delta)
    phs_num = toolkit.trapezoid(ys, dp)
    print(f"  Phi_2 * 8 pi: analytic {_two_body_phase_space(M, 0.0, 0.0) * 8 * math.pi:.12f},"
          f" numerical {phs_num * 8 * math.pi:.12f}")
    w = pi0_width_from_rungs()
    Qu, Qd = gauge331.quark_charges(3)
    A = inputs.ALPHA_0 / (math.pi * inputs.F_PI) * 3 * float(Qu * Qu - Qd * Qd)
    closed = A * A * M ** 3 / (64 * math.pi) * 1e9
    pull = (w - inputs.GAMMA_PI0) / inputs.GAMMA_PI0_ERR
    print(f"  Gamma(pi0 -> gg) = {w:.6f} eV (closed form {closed:.6f}); N_c(Q_u^2-Q_d^2) = {3 * (Qu * Qu - Qd * Qd)}")
    print(f"  measured {inputs.GAMMA_PI0} +- {inputs.GAMMA_PI0_ERR:.4f} eV: pull = {pull:+.3f} sigma")

    print("== 6/7. Planck mass and the G window")
    mpl = planck_mass_GeV(inputs.G_NEWTON, inputs.HBAR, inputs.C_LIGHT)
    lP = inputs.HBAR / (mpl * _gev_J() / inputs.C_LIGHT ** 2 * inputs.C_LIGHT)
    print(f"  M_Pl = {mpl:.6e} GeV; hbar/(M_Pl c) = {lP:.6e} m vs L_PLANCK {inputs.L_PLANCK:.6e}")
    for v in ("+1/sqrt3", "-1/sqrt3"):
        p3, p5 = inputs.POLES_331[v]
        lo, hi = g_window(p3, p5, mpl)
        G0 = inputs.G_NEWTON
        lo2 = math.exp(toolkit.bisect(lambda lx: math.log(planck_mass_GeV(math.exp(lx) * G0, inputs.HBAR,
                                                                          inputs.C_LIGHT) / p3), -120.0, 120.0))
        hi2 = math.exp(toolkit.bisect(lambda lx: math.log(planck_mass_GeV(math.exp(lx) * G0, inputs.HBAR,
                                                                          inputs.C_LIGHT) / p5), -120.0, 120.0))
        print(f"  {v}: poles (N_c=3, 5) = ({p3:.5e}, {p5:.5e}) GeV; G/G_meas in ({lo:.6e}, {hi:.6e});"
              f" bisection ({lo2:.6e}, {hi2:.6e}); measured G inside: {lo < 1 < hi}")

    print("== 8. Schwarzschild radius of the diamond")
    rs = schwarzschild_radius(m)
    c2 = inputs.C_LIGHT ** 2
    rs2 = toolkit.bisect(lambda r: 1 - 2 * inputs.G_NEWTON * m / (c2 * r), rs / 3, 3 * rs)
    mkg = mpl * _gev_J() / c2
    print(f"  r_s = {rs:.6e} m (bisection {rs2:.6e}) = {rs / inputs.L_PLANCK:.6e} l_P;"
          f" 2 m/M_Pl = {2 * m / mkg:.6e}")

    print("== 9. Planck-mass black hole")
    kT = planck_bh_kT_GeV()
    print(f"  k_B T_H(M_Pl) = {kT:.6e} GeV = {kT / mpl:.12f} M_Pl c^2; 1/(8 pi) = {1 / (8 * math.pi):.12f}")
