"""Red-team proposed checks for the ferm_se campaign (see AUDIT.md).  Each takes the build module m and returns (ok, msg).

They close the gaps that the surviving mutants of AUDIT.md section 4 went through:
  * no point in the window 1.5 < k^2/(4 m^2) < 4 of a neutral loop, no exact threshold,
    k^2 only down to -5 M_W^2, mu only up to 1e4 GeV, no massive Q = 0 fermion       -> audit_table
  * Sigma at 0 < |k^2| << m^2 is never resolved (oracle floor 1e-18 alpha M_W^2 absolute) -> audit_photon_slope_at_zero, audit_table
  * mu dependence beyond [1, 1e4] GeV                                                    -> audit_mu_log_linear (reference-free)
  * "keep any high-precision setting local" (SPEC 4) not enforced                        -> audit_global_precision (reference-free)
  * massless large-|k^2| limit (textbook)                                                -> audit_massless_asymptotics
AUDIT_TABLE comes from the auditor's independent numerics (a twice-subtracted dispersion relation over the Cutkosky imaginary part,
.../scratchpad/audit-ferm_se/indep.py, gen_table.py); it agrees with builds a and b and with the oracle reference to <= 1e-14
at 75 further points (compare.log).
Usage: python3 audit_proposed_checks.py <build dir>
"""
import importlib.util, math, os, sys

MW, MZ, AL = 80.38, 91.19, 1 / 128.0

# ((export, k2, fermions-or-doublets, MW, MZ, alpha, mu), auditor value)
AUDIT_TABLE = [
    (('sigma_AA', 262644.95488, ((172.76, 0.6666666666666666, 0.5, 3),), 80.38, 91.19, 0.0078125, 80.38), -326.9478231858384),
    (('sigma_AA', 209.66879999999998, ((4.18, -0.3333333333333333, -0.5, 3),), 80.38, 91.19, 0.0078125, 30.0), 0.21771779182930967),
    (('sigma_AA', 119384.07039999998, ((172.76, 0.6666666666666666, 0.5, 3),), 80.38, 91.19, 0.0078125, 80.38), 149.94490012860496),
    (('sigma_AA', -1000000.0, ((172.76, 0.6666666666666666, 0.5, 3), (4.18, -0.3333333333333333, -0.5, 3)), 80.38, 91.19, 0.0078125, 80.38), 4838.059335780291),
    (('sigma_AA', -100000000.0, ((172.76, 0.6666666666666666, 0.5, 3),), 80.38, 91.19, 0.0078125, 300.0), 591109.7794786693),
    (('sigma_AA', 8315.6161, ((172.76, 0.6666666666666666, 0.5, 3), (4.18, -0.3333333333333333, -0.5, 3), (0.000510998, -1, -0.5, 1)), 80.38, 91.19, 0.0078125, 1000000.0), 346.1214727496636),
    (('sigma_AA', 1e-12, ((1e-06, -1, -0.5, 1),), 80.38, 91.19, 0.0078125, 80.38), 3.0363630166919666e-14),
    (('sigma_AA', -3e-12, ((1e-06, -1, -0.5, 1),), 80.38, 91.19, 0.0078125, 80.38), -8.937572153842944e-14),
    (('sigma_AA', 1e-08, ((0.000510998, -1, -0.5, 1),), 80.38, 91.19, 0.0078125, 80.38), 1.9844227027832644e-10),
    (('sigma_AZ', 262644.95488, ((172.76, 0.6666666666666666, 0.5, 3),), 80.38, 91.19, 0.0078125, 80.38), -119.3536015171811),
    (('sigma_AZ', 209.66879999999998, ((4.18, -0.3333333333333333, -0.5, 3),), 80.38, 91.19, 0.0078125, 30.0), 0.27560606545031013),
    (('sigma_AZ', 119384.07039999998, ((172.76, 0.6666666666666666, 0.5, 3),), 80.38, 91.19, 0.0078125, 80.38), 54.73798138521514),
    (('sigma_AZ', -1000000.0, ((172.76, 0.6666666666666666, 0.5, 3), (4.18, -0.3333333333333333, -0.5, 3)), 80.38, 91.19, 0.0078125, 80.38), 2606.327044137753),
    (('sigma_AZ', -100000000.0, ((172.76, 0.6666666666666666, 0.5, 3),), 80.38, 91.19, 0.0078125, 300.0), 215786.97293452965),
    (('sigma_AZ', 8315.6161, ((172.76, 0.6666666666666666, 0.5, 3), (4.18, -0.3333333333333333, -0.5, 3), (0.000510998, -1, -0.5, 1)), 80.38, 91.19, 0.0078125, 1000000.0), 126.37947904139492),
    (('sigma_AZ', 1e-12, ((1e-06, -1, -0.5, 1),), 80.38, 91.19, 0.0078125, 80.38), 1.9668461435274636e-15),
    (('sigma_AZ', -3e-12, ((1e-06, -1, -0.5, 1),), 80.38, 91.19, 0.0078125, 80.38), -5.789435988595312e-15),
    (('sigma_AZ', 1e-08, ((0.000510998, -1, -0.5, 1),), 80.38, 91.19, 0.0078125, 80.38), 1.2854372545845468e-11),
    (('sigma_ZZ', 262644.95488, ((172.76, 0.6666666666666666, 0.5, 3),), 80.38, 91.19, 0.0078125, 80.38), -159.59768823543675),
    (('sigma_ZZ', 209.66879999999998, ((4.18, -0.3333333333333333, -0.5, 3),), 80.38, 91.19, 0.0078125, 30.0), 0.6729093808441664),
    (('sigma_ZZ', 119384.07039999998, ((172.76, 0.6666666666666666, 0.5, 3),), 80.38, 91.19, 0.0078125, 80.38), 66.21825432775388),
    (('sigma_ZZ', -1000000.0, ((172.76, 0.6666666666666666, 0.5, 3), (4.18, -0.3333333333333333, -0.5, 3)), 80.38, 91.19, 0.0078125, 80.38), 8742.975873905994),
    (('sigma_ZZ', -100000000.0, ((172.76, 0.6666666666666666, 0.5, 3),), 80.38, 91.19, 0.0078125, 300.0), 559265.3354274718),
    (('sigma_ZZ', 8315.6161, ((172.76, 0.6666666666666666, 0.5, 3), (4.18, -0.3333333333333333, -0.5, 3), (0.000510998, -1, -0.5, 1)), 80.38, 91.19, 0.0078125, 1000000.0), -2364.696390181615),
    (('sigma_ZZ', 1e-12, ((1e-06, -1, -0.5, 1),), 80.38, 91.19, 0.0078125, 80.38), -5.455823879758035e-14),
    (('sigma_ZZ', -3e-12, ((1e-06, -1, -0.5, 1),), 80.38, 91.19, 0.0078125, 80.38), -9.720707971946087e-14),
    (('sigma_ZZ', 1e-08, ((0.000510998, -1, -0.5, 1),), 80.38, 91.19, 0.0078125, 80.38), -1.1140197234088562e-08),
    (('sigma_ZZ', 8315.6161, ((50.0, 0, 0.5, 1),), 80.38, 91.19, 0.0078125, 80.38), 2.167407577127391),
    (('sigma_ZZ', 0.0, ((50.0, 0, 0.5, 1),), 80.38, 91.19, 0.0078125, 80.38), -4.257983702904415),
    (('sigma_ZZ', -2000.0, ((5.0, 0, 0.5, 1),), 80.38, 91.19, 0.0078125, 80.38), -3.4474453184754865),
    (('sigma_ZZ', 13000.0, ((50.0, 0, 0.5, 1),), 80.38, 91.19, 0.0078125, 200.0), 15.926002410651611),
    (('sigma_ZZ', 8315.6161, ((300.0, 1.0, 1.5, 2),), 80.38, 91.19, 0.0078125, 80.38), 7434.4372680452825),
    (('sigma_ZZ', 0.0, ((10000.0, -0.3333333333333333, -0.5, 3),), 80.38, 91.19, 0.0078125, 80.38), 5191540.770820823),
    (('sigma_W', 31307.7636, ((172.76, 4.18, 3.0),), 80.38, 91.19, 0.0078125, 80.38), 80.65492827841598),
    (('sigma_W', 33124.0, ((91.0, 91.0, 1.0),), 80.38, 91.19, 0.0078125, 80.38), 33.997096017461935),
    (('sigma_W', -1000000.0, ((172.76, 4.18, 3.0),), 80.38, 91.19, 0.0078125, 80.38), 10041.654675581305),
    (('sigma_W', 6460.944399999999, ((172.76, 4.18, 3.0),), 80.38, 91.19, 0.0078125, 1000000.0), -1906.39786873686),
    (('sigma_W', 1e-12, ((1e-06, 0.0, 1.0),), 80.38, 91.19, 0.0078125, 80.38), -1.67578043662803e-14),
    (('sigma_W', 0.0, ((1e-06, 2e-06, 1.0),), 80.38, 91.19, 0.0078125, 80.38), -2.468696449172885e-13),
    (('sigma_W', 78269.409, ((172.76, 4.18, 3.0),), 80.38, 91.19, 0.0078125, 80.38), 73.72908708812339),
    (('sigma_W', 0.0, ((4.18, 172.76, 3.0),), 80.38, 91.19, 0.0078125, 80.38), 128.64532123255222),
    (('sigma_W', 0.0, ((172.76, 4.18, 3.0),), 80.38, 91.19, 0.0078125, 2.0), 1051.04972979054),
    (('sigma_W', 1.0, ((10000.0, 0.0, 1.0),), 80.38, 91.19, 0.0078125, 80.38), 1274862.5195951331),
]


def _dev(v, r, floor):
    try:
        v = float(v)
    except Exception:
        return float("inf")
    return abs(v - r) / (abs(r) + floor) if math.isfinite(v) else float("inf")


def audit_table(m):
    """Thresholds (exact, and the window 1.5-4 x threshold), k^2 = -1e6, -1e8, mu = 1e6, tiny masses at k^2 ~ m^2, massive Q = 0 fermions,
    general I3, heavy fermions; relative 1e-9 with the floor 1e-12 alpha max(|k^2|, m^2) (no M_W^2 floor: the values at k^2 ~ m^2 are tiny)."""
    worst, where, bad = 0.0, None, 0
    for (f, k2, fs, mw, mz, al, mu), r in AUDIT_TABLE:
        masses = [x for t in fs for x in (t[:2] if f == "sigma_W" else t[:1])]
        floor = 1e-12 * al * max([abs(k2)] + [x * x for x in masses] + [1e-30])
        d = _dev(getattr(m, f)(k2, fs, mw, mz, al, mu), r, floor)
        bad += d > 1e-9
        if d > worst:
            worst, where = d, (f, k2, fs, mu)
    return worst < 1e-9, f"{len(AUDIT_TABLE)} auditor points, {bad} off: worst {worst:.1e} at {where}"


def audit_photon_slope_at_zero(m):
    """dSigma^AA/dk^2 at 0 = (alpha/3pi) N_C Q^2 ln(mu^2/m^2) (textbook charge renormalisation), central difference with h = 1e-6 m^2; relative 1e-6."""
    worst, where = 0.0, None
    for mass, Q, NC in ((1e-6, -1.0, 1), (0.000510998, -1.0, 1), (1.0, 2 / 3, 3), (172.76, 2 / 3, 3), (1e4, -1 / 3, 3)):
        fs = ((mass, Q, -0.5 if Q < 0 else 0.5, NC),)
        h = 1e-6 * mass * mass
        num = (m.sigma_AA(h, fs, MW, MZ, AL, MW) - m.sigma_AA(-h, fs, MW, MZ, AL, MW)) / (2 * h)
        ana = AL / (3 * math.pi) * NC * Q * Q * math.log(MW**2 / mass**2)
        d = abs(num / ana - 1)
        if d > worst:
            worst, where = d, mass
    return worst < 1e-6, f"Sigma^AA'(0) against (alpha/3pi) N Q^2 ln(mu^2/m^2): worst relative {worst:.1e} at m = {where}"


def audit_mu_log_linear(m):
    """Sigma is exactly A + B ln mu^2 (MS-bar): second difference over mu = 1e-2, 1e2, 1e6 GeV (equal steps in ln mu), relative to the first; < 1e-9."""
    fs = ((172.76, 2 / 3, 0.5, 3), (4.18, -1 / 3, -0.5, 3), (0.000510998, -1, -0.5, 1), (0.0, 0, 0.5, 1))
    ds = ((172.76, 4.18, 3.0), (0.0, 0.000510998, 1.0))
    worst, where = 0.0, None
    for f in ("sigma_AA", "sigma_AZ", "sigma_ZZ", "sigma_W"):
        arg = ds if f == "sigma_W" else fs
        for k2 in (-3e4, 0.0, MZ**2):
            v = [getattr(m, f)(k2, arg, MW, MZ, AL, mu) for mu in (1e-2, 1e2, 1e6)]
            scale = abs(v[2] - v[0])
            if scale < 1e-30:
                continue
            d = abs(v[2] - 2 * v[1] + v[0]) / scale
            if d > worst:
                worst, where = d, (f, k2)
    return worst < 1e-9, f"(Sigma(1e6) - 2 Sigma(1e2) + Sigma(1e-2)) / |Sigma(1e6) - Sigma(1e-2)|: worst {worst:.1e} at {where}"


def audit_massless_asymptotics(m):
    """k^2 = -1e14 GeV^2 against the massless one-loop form Sigma = N (alpha/4pi) G+ (2/3) k^2 (5/3 - ln(-k^2/mu^2)), G+ = aL bL + aR bR
    (AA: 2Q^2, AZ: Q(gL+gR), ZZ: gL^2+gR^2, W: 1/(2 s^2)); mass corrections are O(m^2/k^2 ln) ~ 1e-8. Relative 1e-6."""
    k2, mu = -1e14, MW
    s2 = 1 - MW**2 / MZ**2
    s, c = math.sqrt(s2), MW / MZ
    L = 5 / 3 - math.log(-k2 / mu**2)
    fs = ((172.76, 2 / 3, 0.5, 3), (4.18, -1 / 3, -0.5, 3), (0.000510998, -1, -0.5, 1), (0.0, 0, 0.5, 1))
    G = {"sigma_AA": 0.0, "sigma_AZ": 0.0, "sigma_ZZ": 0.0}
    for (mass, Q, I3, NC) in fs:
        gL, gR = (I3 - s2 * Q) / (s * c), -s * Q / c
        G["sigma_AA"] += NC * 2 * Q * Q
        G["sigma_AZ"] += NC * Q * (gL + gR)
        G["sigma_ZZ"] += NC * (gL * gL + gR * gR)
    worst, where = 0.0, None
    for f, g in G.items():
        ana = AL / (4 * math.pi) * g * 2 / 3 * k2 * L
        d = abs(getattr(m, f)(k2, fs, MW, MZ, AL, mu) / ana - 1)
        if d > worst:
            worst, where = d, f
    ana = AL / (4 * math.pi) * (3.0 + 1.0) / (2 * s2) * 2 / 3 * k2 * L
    d = abs(m.sigma_W(k2, ((172.76, 4.18, 3.0), (0.0, 0.000510998, 1.0)), MW, MZ, AL, mu) / ana - 1)
    if d > worst:
        worst, where = d, "sigma_W"
    return worst < 1e-6, f"against the massless form at k^2 = -1e14: worst relative {worst:.1e} at {where}"


def audit_global_precision(m):
    """SPEC section 4: the global mpmath precision is the same before and after calling every export (and loading the module)."""
    try:
        import mpmath as mp
    except ImportError:
        return True, "mpmath not installed"
    saved = mp.mp.dps
    mp.mp.dps = before = 15
    spec = importlib.util.spec_from_file_location(m.__name__ + "_reload_audit", m.__file__)
    m2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m2)
    after_import = mp.mp.dps
    fs = ((172.76, 2 / 3, 0.5, 3),)
    for f in ("sigma_AA", "sigma_AZ", "sigma_ZZ"):
        getattr(m2, f)(MZ**2, fs, MW, MZ, AL, MW)
    m2.sigma_W(MW**2, ((172.76, 4.18, 3.0),), MW, MZ, AL, MW)
    after = mp.mp.dps
    mp.mp.dps = saved
    return before == after_import == after, f"mp.dps before {before}, after import {after_import}, after calls {after}"


CHECKS = [("auditor table: thresholds, wide k^2 and mu, tiny masses, massive Q = 0, general I3", audit_table),
          ("photon slope at k^2 = 0 (charge renormalisation)", audit_photon_slope_at_zero),
          ("exact ln mu^2 linearity for mu in [1e-2, 1e6] GeV", audit_mu_log_linear),
          ("massless asymptotics at k^2 = -1e14", audit_massless_asymptotics),
          ("global mpmath precision untouched (SPEC 4)", audit_global_precision)]

if __name__ == "__main__":
    sys.dont_write_bytecode = True
    d = os.path.abspath(sys.argv[1])
    s = importlib.util.spec_from_file_location("ferm_se", os.path.join(d, "ferm_se.py"))
    mod = importlib.util.module_from_spec(s)
    s.loader.exec_module(mod)
    allok = True
    for label, fn in CHECKS:
        try:
            ok, msg = fn(mod)
        except Exception as e:
            ok, msg = False, f"{type(e).__name__}: {e}"
        allok &= ok
        print(f"[{'PASS' if ok else 'FAIL'}] {label}: {msg}", flush=True)
    print("PROPOSED CHECKS PASSED" if allok else "PROPOSED CHECKS FAILED")
