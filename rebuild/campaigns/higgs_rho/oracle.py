# CANARY-060158c59f054784-higgs_rho: planted so a builder transcript that contains this string has read the oracle
"""Hidden oracle for the higgs_rho campaign.

Target: the m_H dependence of Delta rho (equivalently of the Peskin-Takeuchi T parameter, alpha T = Delta rho) from the Higgs sector at one
loop, for m_H >> M_W:  Delta rho = -(3 alpha / (16 pi c^2)) ln(m_H^2 / M_W^2) + const   ("Veltman screening": the logarithm is proportional to
the hypercharge coupling g'^2 = 4 pi alpha / c^2, so it vanishes in the custodial limit). LIT: Peskin and Takeuchi, PRD 46, 381 (1992);
PDG electroweak review, Delta rho ~ (3 G_F M_W^2 / 8 sqrt2 pi^2)[m_t^2/M_W^2 - (s^2/c^2) ln(m_H^2/M_W^2)]  (same coefficient with
G_F M_W^2 = pi alpha / (sqrt2 s^2)). Not an independent derivation; the builds are the derivation."""
import math

MW, MZ, ALPHA = 80.38, 91.19, 1 / 128.0
C2 = (MW / MZ) ** 2
LINT_TARGETS = [3 / (16 * math.pi), 0.0597, 3 * ALPHA / (16 * math.pi * C2)]
LINT_EXACT = [3 * ALPHA / (16 * math.pi * C2), 3 / (16 * math.pi)]


def target(MW_, MZ_, alpha):
    return -3 * alpha / (16 * math.pi * (MW_ / MZ_) ** 2)


def coeff_check(m):
    worst = 0.0
    for MW_, MZ_, al in ((80.38, 91.19, 1 / 128.0), (80.0, 92.0, 1 / 130.0), (75.0, 91.19, 1 / 125.0)):
        for xi in (1.0,):
            worst = max(worst, abs(m.log_coefficient(MW_, MZ_, al, xi) / target(MW_, MZ_, al) - 1))
    return worst < 1e-8, f"worst relative deviation of log_coefficient from -3 alpha/(16 pi c^2): {worst:.1e}"


def slope_check(m):
    f = lambda mh: m.rho_higgs_rel(mh, MW, MZ, ALPHA, 1.0, MW)
    h1, h2 = 3e4 * MW, 3e5 * MW
    slope = (f(h2) - f(h1)) / math.log((h2 / MW) ** 2 / (h1 / MW) ** 2)
    return abs(slope / target(MW, MZ, ALPHA) - 1) < 1e-4, f"measured slope {slope:.6e}, target {target(MW, MZ, ALPHA):.6e}"


# Finite-function references (audit of the first two builds): two independent routes by the auditor (exact-d Feynman parameters and a 4D
# Euclidean radial integral) agree with each other and with both builds to the double; the large-mH constant is the auditor's analytic expansion.
RHO_REF = {10.0: 2.670871522034841e-04, 50.0: 1.3757666827149537e-04, 125.0: -2.052058478215137e-04,
           200.0: -5.1519672846123684e-04, 300.0: -8.5333946660786364e-04, 1000.0: -2.1114244848310153e-03,
           5000.0: -4.0063294083988911e-03}
PI_REF = {(125.0, 1.0, 80.38): (14.526123781738889, 24.17600733749247),
          (400.0, 0.3, 80.38): (89.667178211043535, 128.54381711225607),
          (1000.0, 4.0, 297.406): (370.37767292928746, 484.97112298255361)}
C_INF = 9.53900888026996e-04          # lim [rho_rel - B ln(mH^2/MW^2)]
LINT_TARGETS += [9.539e-4, 2.0520584e-4, 2.67087e-4]


def finite_function_check(m):
    w, where = 0.0, None
    for mh, r in RHO_REF.items():
        d = abs(m.rho_higgs_rel(mh, MW, MZ, ALPHA, 1.0, MW) / r - 1)
        if d > w:
            w, where = d, mh
    return w < 1e-9, f"worst relative deviation of rho_higgs_rel from the independent reference at mH = 10..5000 GeV: {w:.1e} at {where}"


def xi_finite_check(m):
    w = max(abs(m.rho_higgs_rel(mh, MW, MZ, ALPHA, xi, mu) / RHO_REF[mh] - 1)
            for mh in (50.0, 300.0, 1000.0) for xi in (0.3, 4.0, 25.0) for mu in (MW, 3.7 * MW))
    return w < 1e-9, f"rho_higgs_rel at finite mH for xi = 0.3, 4, 25 and two MS-bar scales: worst deviation from the xi = 1 reference {w:.1e}"


def landau_check(m):
    v = m.rho_higgs_rel(300.0, MW, MZ, ALPHA, 0.0, MW)
    return abs(v / RHO_REF[300.0] - 1) < 1e-9, f"rho_higgs_rel in the Landau gauge xi = 0 at mH = 300 GeV: {v}"


def constant_check(m):
    B = target(MW, MZ, ALPHA)
    mh = 1e6 * MW
    C = m.rho_higgs_rel(mh, MW, MZ, ALPHA, 1.0, MW) - B * math.log((mh / MW) ** 2)
    return abs(C / C_INF - 1) < 1e-5, f"large-mH constant {C:.9e} against the analytic {C_INF:.9e}"


def extreme_mass_check(m):
    """The exact large-mH form B ln(mH^2/MW^2) + C is analytic, so it is a reference up to masses far beyond any physical scale; a fixed working
    precision loses the m_H^2 terms that cancel only between W and Z (about 2 log10(mH/M) digits)."""
    B = target(MW, MZ, ALPHA)
    worst, where = 0.0, None
    for e in (6, 8, 12, 16, 20):                       # the asymptotic form's own corrections are ~ (MW/mH)^2 ln: 1e-12 at 1e6 MW
        mh = MW * 10.0**e
        v = m.rho_higgs_rel(mh, MW, MZ, ALPHA, 1.0, MW)
        d = abs((v - B * math.log((mh / MW) ** 2) - C_INF) / (B * math.log((mh / MW) ** 2)))
        if d > worst:
            worst, where = d, e
    return worst < 1e-8, f"worst |rho - B ln - C| / |B ln| at mH = 1e6 .. 1e20 MW: {worst:.1e} at 1e{where} MW"


def raw_check(m):
    w = 0.0
    for (mh, xi, mu), (pw, pz) in PI_REF.items():
        w = max(w, abs(m.self_energy_W(mh, MW, MZ, ALPHA, xi, mu) / pw - 1), abs(m.self_energy_Z(mh, MW, MZ, ALPHA, xi, mu) / pz - 1))
    return w < 1e-9, f"raw MS-bar Pi_WW(0), Pi_ZZ(0) in the convention of SPEC section 2: worst relative deviation {w:.1e}"


ORACLE = [("log_coefficient = -3 alpha/(16 pi c^2)", coeff_check),
          ("measured large-mH slope of rho_higgs_rel = -3 alpha/(16 pi c^2)", slope_check),
          ("rho_higgs_rel against the independent finite-function reference, mH = 10..5000 GeV, 1e-9", finite_function_check),
          ("rho_higgs_rel is xi- and mu-independent at finite mH (xi = 0.3, 4, 25)", xi_finite_check),
          ("Landau gauge xi = 0 is accepted", landau_check),
          ("large-mH constant term", constant_check),
          ("exact large-mH form B ln + C holds from mH = 1e6 MW to 1e20 MW", extreme_mass_check),
          ("raw self-energies in the pinned convention", raw_check)]
