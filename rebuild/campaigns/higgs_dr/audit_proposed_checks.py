"""Auditor's proposed additional checks for the higgs_dr campaign (see AUDIT.md section 4).

Same shape as campaign.BLIND / oracle.ORACLE: functions taking the build module m and returning (ok: bool, detail: str).
B_* are blind (no reference value; may go into campaign.BLIND), O_* use the hidden reference (oracle tier), H_* is gate hygiene.

    python3 audit_proposed_checks.py <dir with higgs_dr.py> [...]
"""
import sys, math, importlib.util, os
sys.dont_write_bytecode = True
import mpmath as mp

_HERE = os.path.dirname(os.path.abspath(__file__))
MW, MZ, ALPHA = 80.38, 91.19, 1 / 128.0


def _reference():
    """reference_dr.py loaded with its global mpmath precision change undone afterwards (see AUDIT.md finding C1)."""
    dps = mp.mp.dps
    spec = importlib.util.spec_from_file_location("higgs_dr_reference_audit", os.path.join(_HERE, "reference_dr.py"))
    R = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R)
    mp.mp.dps = dps
    return R


def _ref_call(fn, *a):
    with mp.workdps(40):
        return float(fn(*a))


# ----------------------------------------------------------------------------------------------------------------- blind
def B_sigma_alpha_linear(m):
    """Pi_V is proportional to alpha at fixed masses (one loop, g^2 = 4 pi alpha/s^2). Kills sigma_* that ignore alpha."""
    worst = 0.0
    for f in (m.sigma_W, m.sigma_Z):
        for q2 in (0.0, MW**2, -2.0 * MW**2):
            a, b = f(q2, 300.0, MW, MZ, ALPHA, MW), f(q2, 300.0, MW, MZ, 3 * ALPHA, MW)
            worst = max(worst, abs(b / a / 3 - 1))
    return worst < 1e-12, f"sigma(3 alpha)/(3 sigma(alpha)) - 1, worst over W, Z and three q^2: {worst:.1e}"


def B_sigma_coupling_scaling(m):
    """At fixed MW the W self-energy depends on MZ only through g^2 = 4 pi alpha/s^2 (the H-W, H-phi+ and seagull loops contain
    no Z); at fixed MZ the Z self-energy depends on MW only through g^2/c^2 = 4 pi alpha/(s^2 c^2). Kills couplings taken from
    module-level defaults instead of the arguments."""
    worst = 0.0
    s2 = lambda w, z: 1 - (w / z) ** 2
    for q2 in (0.0, 0.7 * MW**2, -3.0 * MW**2):
        a, b = m.sigma_W(q2, 250.0, MW, MZ, ALPHA, MW), m.sigma_W(q2, 250.0, MW, 97.0, ALPHA, MW)
        worst = max(worst, abs(b / a / (s2(MW, MZ) / s2(MW, 97.0)) - 1))
        a, b = m.sigma_Z(q2, 250.0, MW, MZ, ALPHA, MW), m.sigma_Z(q2, 250.0, 77.0, MZ, ALPHA, MW)
        sc = lambda w, z: s2(w, z) * (w / z) ** 2
        worst = max(worst, abs(b / a / (sc(MW, MZ) / sc(77.0, MZ)) - 1))
    return worst < 1e-12, f"sigma_W(MZ')/sigma_W(MZ) against s^2/s'^2 and sigma_Z(MW')/sigma_Z(MW) against (s c)^2/(s' c')^2: worst {worst:.1e}"


# ----------------------------------------------------------------------------------------------------------------- oracle
def O_dense_mH(m):
    """delta_r_higgs_rel against the reference on a log grid that closes the gap 5 TeV .. 8e7 GeV left by finite_check and
    extreme_mass_check (and extends below 10 GeV), at two scales. Kills a switch to the heavy-Higgs asymptote at a few TeV."""
    R = _reference()
    worst, where = 0.0, None
    for mh in (1.0, 3.0, 7000.0, 2.0e4, 1.0e5, 5.0e5, 3.0e6, 2.0e7):
        for mu in (MW, 3.7 * MW):
            r = _ref_call(R.dr_h_rel, mh, MW, MZ, ALPHA, mu)
            d = abs(m.delta_r_higgs_rel(mh, MW, MZ, ALPHA, mu) / r - 1)
            if d > worst:
                worst, where = d, (mh, round(mu, 2))
    return worst < 1e-9, f"worst relative deviation, mH = 1 GeV .. 2e7 GeV: {worst:.1e} at {where}"


def _dev(call, ref):
    """relative deviation; a non-real or crashing value below threshold counts as infinitely wrong (SPEC 2: Pi is real there)."""
    try:
        v = complex(call())
        if v.imag != 0:
            return float("inf")
        return abs(v.real / ref - 1)
    except Exception:
        return float("inf")


def O_raw_wide(m):
    """Raw Pi_WW, Pi_ZZ against the reference at other (MW, MZ, alpha), deep spacelike q^2 and q^2 between MZ^2 and threshold.
    Kills self-energies that are wrong only outside the oracle's five q^2 points or only away from the campaign inputs."""
    R = _reference()
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


# ----------------------------------------------------------------------------------------------------------------- hygiene
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


CHECKS = [("B_sigma_alpha_linear", B_sigma_alpha_linear),
          ("B_sigma_coupling_scaling", B_sigma_coupling_scaling),
          ("O_dense_mH", O_dense_mH),
          ("O_raw_wide", O_raw_wide),
          ("H_own_precision_extreme", H_own_precision_extreme)]


if __name__ == "__main__":
    for d in sys.argv[1:]:
        spec = importlib.util.spec_from_file_location("higgs_dr", os.path.join(d, "higgs_dr.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("####", d.rstrip("/").split("/")[-1], flush=True)
        for name, fn in CHECKS:
            try:
                ok, det = fn(mod)
            except Exception as e:
                ok, det = False, f"{type(e).__name__}: {e}"
            print(f"   [{'PASS' if ok else 'FAIL'}] {name}: {det}", flush=True)
