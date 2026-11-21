# CANARY-7c1d92e45b8a3f60-higgs_dr_xi: planted so a builder transcript that contains this string has read the oracle
"""Hidden oracle for the higgs_dr_xi campaign.

Claim tested: delta_r_higgs_rel does not depend on the gauge parameter xi. Argument (mine, not the builders'): m_H enters one-loop two-point functions only
through Higgs propagators, i.e. only through the Higgs-containing diagrams; Delta r is a physical (gauge-parameter independent) observable; so the
m_H dependence of the sum of Higgs-containing contributions to Delta r cannot depend on xi. The Feynman-gauge reference (reference_dr.py, validated in
campaign higgs_dr, whose audit confirmed it by three routes) is therefore the value at every xi. If a build finds a xi dependence that is not an
error of its own, the argument is wrong and the campaign is class C. The raw self-energies at xi != 1 have no reference here (only xi = 1 does); the audit
must verify them by an independent derivation."""
import importlib.util, math, os

_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reference_dr.py")
_s = importlib.util.spec_from_file_location("higgs_dr_xi_reference", _p)
R = importlib.util.module_from_spec(_s)
_s.loader.exec_module(R)

MW, MZ, ALPHA = 80.38, 91.19, 1 / 128.0
S2 = 1 - (MW / MZ) ** 2
B_REF = 11 * ALPHA / (48 * math.pi * S2)
C_INF = -0.0024006305111737986
LINT_TARGETS = [B_REF, 11 / (48 * math.pi), 0.002555, 0.0014774869, 0.0024006]
LINT_EXACT = [11 / (48 * math.pi), 11 / 48, 11 * ALPHA / (48 * math.pi * S2)]
XIS = (0.0, 0.3, 1.0, 4.0, 25.0)


def _ref(mh, mw, mz, al, mu):
    return float(R.dr_h_rel(mh, mw, mz, al, mu))


def finite_check(m):
    w, where = 0.0, None
    for xi in XIS:
        for mh in (10.0, 125.2, 300.0, 1000.0, 5000.0):
            for mu in (MW, 3.7 * MW):
                d = abs(m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, xi, mu) / _ref(mh, MW, MZ, ALPHA, mu) - 1)
                if d > w:
                    w, where = d, (xi, mh, mu)
    return w < 1e-9, f"worst relative deviation of delta_r_higgs_rel from the Feynman-gauge reference over xi = {XIS}: {w:.1e} at {where}"


def other_points_check(m):
    w = 0.0
    for xi in (0.0, 3.0):
        for mw, mz, al, mh in ((80.0, 92.0, 1 / 130.0, 200.0), (75.0, 91.19, 1 / 125.0, 700.0)):
            w = max(w, abs(m.delta_r_higgs_rel(mh, mw, mz, al, xi, mw) / _ref(mh, mw, mz, al, mw) - 1))
    return w < 1e-9, f"other (MW, MZ, alpha) points at xi = 0, 3: {w:.1e}"


def coeff_check(m):
    w = 0.0
    for xi in XIS:
        for mw, mz, al in ((80.38, 91.19, 1 / 128.0), (80.0, 92.0, 1 / 130.0)):
            s2 = 1 - (mw / mz) ** 2
            w = max(w, abs(m.log_coefficient(mw, mz, al, xi) / (11 * al / (48 * math.pi * s2)) - 1))
    return w < 1e-8, f"log_coefficient at xi = {XIS}: {w:.1e}"


def feynman_raw_check(m):
    """At xi = 1 the raw self-energies are the pinned-convention reference."""
    w = 0.0
    g2, c2, s2 = R.couplings(MW, MZ, ALPHA)
    for q2 in (0.0, 0.5 * MW**2, MW**2, MZ**2, -3.0 * MW**2):
        for mh, mu in ((125.0, MW), (1500.0, 0.7 * MW)):
            pw, pz = float(R.pi_v(q2, mh, MW, g2, mu)), float(R.pi_v(q2, mh, MZ, g2 / c2, mu))
            w = max(w, abs(m.sigma_W(q2, mh, MW, MZ, ALPHA, 1.0, mu) / pw - 1), abs(m.sigma_Z(q2, mh, MW, MZ, ALPHA, 1.0, mu) / pz - 1))
    return w < 1e-9, f"raw self-energies at xi = 1 against the reference: {w:.1e}"


def constant_check(m):
    mh = 1e6 * MW
    w = 0.0
    for xi in (0.0, 4.0):
        C = m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, xi, MW) - B_REF * math.log((mh / MW) ** 2)
        w = max(w, abs(C / C_INF - 1))
    return w < 1e-5, f"large-mH constant at xi = 0, 4 against {C_INF:.9e}: {w:.1e}"


def dense_check(m):
    w, where = 0.0, None
    for xi in (0.0, 5.0):
        for mh in (1.0, 3.0, 7000.0, 2.0e4, 1.0e5, 5.0e5, 3.0e6, 2.0e7):
            d = abs(m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, xi, MW) / _ref(mh, MW, MZ, ALPHA, MW) - 1)
            if d > w:
                w, where = d, (xi, mh)
    return w < 1e-9, f"dense m_H grid 1 GeV .. 2e7 GeV at xi = 0, 5: {w:.1e} at {where}"


def own_precision_check(m):
    import mpmath as mp
    saved = mp.mp.dps
    try:
        mp.mp.dps = 15
        spec = importlib.util.spec_from_file_location(m.__name__ + "_own", m.__file__)
        m2 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m2)
        w = 0.0
        for xi in (0.0, 1.0, 4.0):
            for e in (6, 10, 14):
                mh = MW * 10.0**e
                L = B_REF * math.log((mh / MW) ** 2)
                w = max(w, abs((m2.delta_r_higgs_rel(mh, MW, MZ, ALPHA, xi, MW) - L - C_INF) / L))
    finally:
        mp.mp.dps = saved
    return w < 1e-8, f"extreme masses at the build's own precision, xi = 0, 1, 4: {w:.1e}"


XI_WIDE = (0.0, 1e-6, 1e-3, 0.01, 0.1, 0.2, 0.3, 2.0, 4.0, 25.0, 100.0, 1e3, 1e4)


def _rel(a, b):
    if not (isinstance(a, float) and math.isfinite(a)):
        return float("inf")
    return abs(a / b - 1) if b != 0 else abs(a)


def O_sigma_xi_independent(m):
    """sigma_W, sigma_Z at xi != 1 equal their xi = 1 values (1e-9), W and Z, q^2 from -50 MW^2 to MZ^2 (below the physical threshold),
    m_H from 1 GeV (Goldstone loop above its unphysical threshold at small xi) to 1500 GeV, xi from 0 to 1e4.
    Kills mutants whose raw self-energies carry a xi dependence that Delta r does not see (common shifts, off-shell Pi_Z, q^2 < 0) and
    xi errors outside the oracle's xi grid (xi > 25, 0 < xi < 0.3)."""
    worst, where = 0.0, None
    for f, M in ((m.sigma_W, MW), (m.sigma_Z, MZ)):
        for mh in (1.0, 10.0, 40.0, 125.2, 300.0, 1500.0):
            for q2 in (-50 * MW**2, -3 * MW**2, 0.0, 0.5 * MW**2, MW**2, MZ**2):
                if q2 >= (mh + M)**2:
                    continue
                ref = f(q2, mh, MW, MZ, ALPHA, 1.0, MW)
                for xi in XI_WIDE:
                    d = _rel(f(q2, mh, MW, MZ, ALPHA, xi, MW), ref)
                    if d > worst:
                        worst, where = d, (f.__name__, mh, q2, xi)
    return worst < 1e-9, f"worst |sigma(xi)/sigma(1) - 1| over xi = {XI_WIDE}: {worst:.1e} at {where}"


def O_delta_r_xi_wide(m):
    """delta_r_higgs_rel(xi) = delta_r_higgs_rel(1) (1e-9) at xi values and m_H values the oracle does not test (m_H up to 1e9 GeV,
    xi up to 1e4, small nonzero xi with a light Higgs). Self-consistency only: xi = 1 itself is pinned by the oracle."""
    worst, where = 0.0, None
    for mh in (1.0, 10.0, 30.0, 60.0, 125.2, 1000.0, 1e5, 3e7, 1e9):
        ref = m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, 1.0, MW)
        for xi in (0.0, 1e-3, 0.01, 0.1, 0.2, 100.0, 1e3, 1e4):
            d = _rel(m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, xi, MW), ref)
            if d > worst:
                worst, where = d, (mh, xi)
    return worst < 1e-9, f"worst |dr(xi)/dr(1) - 1|: {worst:.1e} at (mH, xi) = {where}"


def O_log_coefficient_xi_wide(m):
    """log_coefficient does not depend on xi, including xi outside the oracle grid."""
    ref = m.log_coefficient(MW, MZ, ALPHA, 1.0)
    w = max(_rel(m.log_coefficient(MW, MZ, ALPHA, xi), ref) for xi in (1e-3, 0.1, 100.0, 1e4))
    return w < 1e-12, f"worst |B(xi)/B(1) - 1| for xi = 1e-3, 0.1, 100, 1e4: {w:.1e}"


ORACLE = [("delta_r_higgs_rel equals the Feynman-gauge reference at every xi (xi independence), 1e-9", finite_check),
          ("xi independence at other (MW, MZ, alpha)", other_points_check),
          ("log_coefficient is xi independent and equals 11 alpha/(48 pi s^2)", coeff_check),
          ("raw self-energies at xi = 1 in the pinned convention", feynman_raw_check),
          ("large-mH constant at xi = 0 and 4", constant_check),
          ("dense mH grid 1 GeV .. 2e7 GeV at xi = 0, 5", dense_check),
          ("extreme masses at the build's own precision", own_precision_check),
          ("raw self-energies are xi independent (audit theorem, AUDIT.md section 2), wide xi grid", O_sigma_xi_independent),
          ("delta_r_higgs_rel on a wide xi grid", O_delta_r_xi_wide),
          ("log_coefficient on a wide xi grid", O_log_coefficient_xi_wide)]
