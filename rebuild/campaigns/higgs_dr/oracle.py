# CANARY-3b8e51d07c4a9f26-higgs_dr: planted so a builder transcript that contains this string has read the oracle
"""Hidden oracle for the higgs_dr campaign.

Target: Delta r_H(m_H) - Delta r_H(M_W) from muon decay in the on-shell scheme, via the Higgs-containing q^2-dependent W and Z self-energies. The
orchestrator's independent reference (reference_dr.py, Feynman gauge, Feynman-parameter integrals at 40 digits) reproduces at q^2 = 0 the accepted
higgs_rho Delta rho to 2e-14 and has the heavy-Higgs coefficient 11 alpha/(48 pi s^2) (3/8 screening in Delta rho + 1/12 from the S-parameter piece;
PDG electroweak review, Hollik, Sirlin 1980, Marciano-Sirlin 1980). The reference is mine, not the builders'; the audit checks it independently."""
import importlib.util, math, os
import mpmath as mp

_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reference_dr.py")
_s = importlib.util.spec_from_file_location("higgs_dr_reference", _p)
R = importlib.util.module_from_spec(_s)
_s.loader.exec_module(R)

MW, MZ, ALPHA = 80.38, 91.19, 1 / 128.0
S2 = 1 - (MW / MZ) ** 2
B_REF = 11 * ALPHA / (48 * math.pi * S2)
C_INF = -0.0024006305111737986                 # lim [Delta r_rel - B ln(mH^2/MW^2)] at MW = 80.38, MZ = 91.19, alpha = 1/128 (reference at 1e8..1e14 MW)
LINT_TARGETS = [B_REF, 11 / (48 * math.pi), 0.002555, 0.0014774869, 0.0024006]
LINT_EXACT = [11 / (48 * math.pi), 11 / 48, 11 * ALPHA / (48 * math.pi * S2)]


def f(x):
    return float(x)


def _ref_call(fn, *a):
    return float(fn(*a))


def coeff_check(m):
    worst = 0.0
    for MW_, MZ_, al in ((80.38, 91.19, 1 / 128.0), (80.0, 92.0, 1 / 130.0), (75.0, 91.19, 1 / 125.0)):
        s2 = 1 - (MW_ / MZ_) ** 2
        worst = max(worst, abs(m.log_coefficient(MW_, MZ_, al) / (11 * al / (48 * math.pi * s2)) - 1))
    return worst < 1e-8, f"worst relative deviation of log_coefficient from the reference coefficient: {worst:.1e}"


def finite_check(m):
    w, where = 0.0, None
    for mh in (10.0, 50.0, 125.2, 300.0, 1000.0, 5000.0):
        for mu in (MW, 3.7 * MW):
            r = f(R.dr_h_rel(mh, MW, MZ, ALPHA, mu))
            d = abs(m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, mu) / r - 1)
            if d > w:
                w, where = d, (mh, mu)
    return w < 1e-9, f"worst relative deviation of delta_r_higgs_rel from the independent reference, mH = 10..5000 GeV, two scales: {w:.1e} at {where}"


def other_masses_check(m):
    w = 0.0
    for MW_, MZ_, al, mh in ((80.0, 92.0, 1 / 130.0, 200.0), (75.0, 91.19, 1 / 125.0, 700.0)):
        r = f(R.dr_h_rel(mh, MW_, MZ_, al, MW_))
        w = max(w, abs(m.delta_r_higgs_rel(mh, MW_, MZ_, al, MW_) / r - 1))
    return w < 1e-9, f"delta_r_higgs_rel at two other (MW, MZ, alpha) points against the reference: {w:.1e}"


def raw_check(m):
    w = 0.0
    for q2 in (0.0, 0.5 * MW**2, MW**2, MZ**2, -3.0 * MW**2):
        for mh, mu in ((125.0, MW), (400.0, 2.0 * MW), (1500.0, 0.7 * MW)):
            g2, c2, s2 = R.couplings(MW, MZ, ALPHA)
            pw = f(R.pi_v(q2, mh, MW, g2, mu))
            pz = f(R.pi_v(q2, mh, MZ, g2 / c2, mu))
            w = max(w, abs(m.sigma_W(q2, mh, MW, MZ, ALPHA, mu) / pw - 1), abs(m.sigma_Z(q2, mh, MW, MZ, ALPHA, mu) / pz - 1))
    return w < 1e-9, f"raw MS-bar Pi_WW(q^2), Pi_ZZ(q^2) in the convention of SPEC section 2, q^2 from -3 MW^2 to MZ^2: worst relative deviation {w:.1e}"


def constant_check(m):
    mh = 1e6 * MW
    C = m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, MW) - B_REF * math.log((mh / MW) ** 2)
    return abs(C / C_INF - 1) < 1e-5, f"large-mH constant {C:.9e} against the reference {C_INF:.9e}"


def extreme_mass_check(m):
    worst, where = 0.0, None
    for e in (6, 8, 10, 12, 14):
        mh = MW * 10.0**e
        v = m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, MW)
        d = abs((v - B_REF * math.log((mh / MW) ** 2) - C_INF) / (B_REF * math.log((mh / MW) ** 2)))
        if d > worst:
            worst, where = d, e
    return worst < 1e-8, f"worst |dr - B ln - C| / |B ln| at mH = 1e6 .. 1e14 MW: {worst:.1e} at 1e{where} MW"


def _dev(call, ref):
    """relative deviation; a non-real or crashing value below threshold counts as infinitely wrong (SPEC 2: Pi is real there)."""
    try:
        v = complex(call())
        if v.imag != 0:
            return float("inf")
        return abs(v.real / ref - 1)
    except Exception:
        return float("inf")


def O_dense_mH(m):
    """delta_r_higgs_rel against the reference on a log grid that closes the gap 5 TeV .. 8e7 GeV left by finite_check and
    extreme_mass_check (and extends below 10 GeV), at two scales. Kills a switch to the heavy-Higgs asymptote at a few TeV."""
    worst, where = 0.0, None
    for mh in (1.0, 3.0, 7000.0, 2.0e4, 1.0e5, 5.0e5, 3.0e6, 2.0e7):
        for mu in (MW, 3.7 * MW):
            r = _ref_call(R.dr_h_rel, mh, MW, MZ, ALPHA, mu)
            d = abs(m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, mu) / r - 1)
            if d > worst:
                worst, where = d, (mh, round(mu, 2))
    return worst < 1e-9, f"worst relative deviation, mH = 1 GeV .. 2e7 GeV: {worst:.1e} at {where}"

def O_raw_wide(m):
    """Raw Pi_WW, Pi_ZZ against the reference at other (MW, MZ, alpha), deep spacelike q^2 and q^2 between MZ^2 and threshold.
    Kills self-energies that are wrong only outside the oracle's five q^2 points or only away from the campaign inputs."""
    worst, where = 0.0, None
    pts = [(80.38, 91.19, 1 / 128.0), (80.0, 92.0, 1 / 130.0), (75.0, 91.19, 1 / 125.0)]
    for (w, z, al) in pts:
        g2, c2, s2 = (float(t) for t in R.couplings(w, z, al))
        for mh, mu in ((60.0, w), (125.0, 1.9 * w), (900.0, 0.6 * w)):
            for q2 in (-500.0 * w**2, -50.0 * w**2, -7.0 * w**2, 0.25 * w**2, 1.6 * z**2, 0.95 * (mh + w) ** 2):
                rw = _ref_call(R.pi_v, q2, mh, w, g2, mu)
                dw = _dev(lambda: m.sigma_W(q2, mh, w, z, al, mu), rw)
                dz = 0.0
                if q2 < (mh + z) ** 2:
                    rz = _ref_call(R.pi_v, q2, mh, z, g2 / c2, mu)
                    dz = _dev(lambda: m.sigma_Z(q2, mh, w, z, al, mu), rz)
                if max(dw, dz) > worst:
                    worst, where = max(dw, dz), (w, z, round(al, 5), mh, round(q2 / w**2, 3))
    return worst < 1e-9, f"worst relative deviation {worst:.1e} at (MW, MZ, alpha, mH, q2/MW^2) = {where}"

def H_own_precision_extreme(m):
    """extreme_mass_check with the build at its OWN mpmath precision. oracle.py imports reference_dr.py, which sets the global
    mp.mp.dps = 40 and so silently raises the working precision of any build that relies on the global setting (AUDIT.md C1).
    Here the build is re-executed after the global precision is put back to mpmath's default, so its module-level settings
    take effect as they would without the oracle."""
    S2 = 1 - (MW / MZ) ** 2
    B = 11 * ALPHA / (48 * math.pi * S2)
    C_INF = -0.0024006305111737986
    saved = mp.mp.dps
    try:
        mp.mp.dps = 15
        spec = importlib.util.spec_from_file_location(m.__name__ + "_own_precision", m.__file__)
        m2 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m2)
        worst, where = 0.0, None
        for e in (6, 8, 10, 12, 14):
            mh = MW * 10.0**e
            v = m2.delta_r_higgs_rel(mh, MW, MZ, ALPHA, MW)
            L = B * math.log((mh / MW) ** 2)
            d = abs((v - L - C_INF) / L)
            if d > worst:
                worst, where = d, e
        own = mp.mp.dps
    finally:
        mp.mp.dps = saved
    return worst < 1e-8, f"at the build's own precision (global mp.dps after import: {own}): worst |dr - B ln - C|/|B ln| = {worst:.1e} at 1e{where} MW"


ORACLE = [("log_coefficient = 11 alpha/(48 pi s^2)", coeff_check),
          ("delta_r_higgs_rel against the independent reference, mH = 10..5000 GeV, two scales, 1e-9", finite_check),
          ("delta_r_higgs_rel at two other (MW, MZ, alpha) points", other_masses_check),
          ("raw q^2-dependent self-energies in the pinned convention, q^2 = -3 MW^2 .. MZ^2", raw_check),
          ("large-mH constant term", constant_check),
          ("exact large-mH form B ln + C holds from mH = 1e6 MW to 1e14 MW", extreme_mass_check),
          ("delta_r_higgs_rel on a dense log grid, mH = 1 GeV .. 2e7 GeV", O_dense_mH),
          ("raw self-energies at other (MW, MZ, alpha), deep spacelike q^2 and near threshold", O_raw_wide),
          ("extreme-mass check with the build at its own mpmath precision (the gate must not raise it)", H_own_precision_extreme)]
