# CANARY-5e2a8b13c9d47f10-bos_se: planted so a builder transcript that contains this string has read the oracle
"""Hidden oracle for the bos_se campaign.

Target: the bosonic transverse self-energies of Denner, Fortschr. Phys. 41 (1993) 307 (arXiv:0709.1075), appendix B, eqs. (B.1)-(B.4) without the fermion loops,
't Hooft-Feynman gauge, tadpoles excluded, MS-bar, real parts, photon mass -> 0. Transcribed by the orchestrator from the page images (reference_denner.py).
Evidence for the transcription: the sum Delta r (eq. 8.14) is UV finite and mu independent separately for the fermionic and the bosonic part (5e-17), its M_H
dependence equals to 1e-16 the independently derived higgs_dr reference, and the full M_W at the benchmark parameters agrees with the paper's table to 0.01 GeV after
the O(alpha alpha_s) correction. The non-Higgs gauge-boson coefficients are checked beyond that only by the two blind builds agreeing with the oracle."""
import importlib.util, math, os

_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reference_denner.py")
_s = importlib.util.spec_from_file_location("bos_se_reference", _p)
R = importlib.util.module_from_spec(_s)
_s.loader.exec_module(R)

MW, MZ, MH, ALPHA = 80.38, 91.19, 125.0, 1 / 128.0
LINT_TARGETS = []
LINT_EXACT = []
FUNCS = ("sigma_AA", "sigma_AZ", "sigma_ZZ", "sigma_W")
# Denner's covariant derivative has +i g1 Y B/2, so his A = -s W3 + c B; SPEC pins -i g' Y B/2 and A = s W3 + c B: the photon field differs by a sign, so
# Sigma^AZ(SPEC) = - Sigma^AZ(Denner) (found when the first blind build, which followed the SPEC, disagreed by exactly 2 = a sign: class R of the orchestrator).
REF = {"sigma_AA": R.sig_AA, "sigma_AZ": lambda *a: -R.sig_AZ(*a), "sigma_ZZ": R.sig_ZZ, "sigma_W": R.sig_W}


def _dev(v, r, scale):
    try:
        v = float(v)
    except Exception:
        return float("inf")
    if not math.isfinite(v):
        return float("inf")
    return abs(v - r) / (abs(r) + 1e-9 * scale)


def grid_check(m):
    worst, where = 0.0, None
    pts = [(k2, mw, mz, mh, al, mu) for k2 in (-5.0 * MW**2, -1000.0, 0.0, 0.3 * MW**2, 0.99 * MW**2, MW**2, MZ**2)
           for (mw, mz, mh, al, mu) in ((MW, MZ, 125.0, ALPHA, MW), (80.0, 92.0, 300.0, 1 / 130.0, 2.2 * 80.0), (75.0, 91.19, 60.0, 1 / 125.0, 0.6 * 75.0))]
    for n in FUNCS:
        for p in pts:
            if n in ("sigma_AA", "sigma_AZ") and p[0] > 3.9 * p[1] ** 2:
                continue
            ref = REF[n](*p)
            d = _dev(getattr(m, n)(*p), ref, p[4] * p[1] ** 2)
            if d > worst:
                worst, where = d, (n, p)
    return worst < 1e-9, f"worst relative deviation from the reference over {len(pts)} points x 4 functions: {worst:.1e} at {where}"


def high_k2_check(m):
    """Above the thresholds: real parts (W-Z at k^2 > (MW+MZ)^2, W-H, Z-H, WW)."""
    worst, where = 0.0, None
    for n in FUNCS:
        for k2 in (1.3 * (MW + MZ) ** 2, 2.5 * (MW + MZ) ** 2, 4.2 * MW**2):
            ref = REF[n](k2, MW, MZ, MH, ALPHA, MW)
            d = _dev(getattr(m, n)(k2, MW, MZ, MH, ALPHA, MW), ref, ALPHA * MW**2)
            if d > worst:
                worst, where = d, (n, k2)
    return worst < 1e-9, f"real parts above the thresholds: worst {worst:.1e} at {where}"


def higgs_mass_check(m):
    worst, where = 0.0, None
    for n in ("sigma_ZZ", "sigma_W"):
        for mh in (1.0, 10.0, 91.19, 500.0, 5e3, 1e5, 1e7, 1e9):
            for k2 in (0.0, MW**2):
                ref = REF[n](k2, MW, MZ, mh, ALPHA, MW)
                d = _dev(getattr(m, n)(k2, MW, MZ, mh, ALPHA, MW), ref, ALPHA * max(MW, mh) ** 2)
                if d > worst:
                    worst, where = d, (n, mh, k2)
    return worst < 1e-8, f"M_H from 1 GeV to 1e9 GeV (both Sigma with a Higgs loop): worst {worst:.1e} at {where}"


def mu_check(m):
    worst, where = 0.0, None
    for n in FUNCS:
        for mu in (1.0, 20.0, 400.0, 1.0e4):
            for k2 in (-3000.0, 0.0, MW**2):
                ref = REF[n](k2, MW, MZ, MH, ALPHA, mu)
                d = _dev(getattr(m, n)(k2, MW, MZ, MH, ALPHA, mu), ref, ALPHA * MW**2 * 10)
                if d > worst:
                    worst, where = d, (n, mu, k2)
    return worst < 1e-9, f"MS-bar scale from 1 GeV to 1e4 GeV: worst {worst:.1e} at {where}"


def own_precision_check(m):
    """The build at mpmath's default global precision (nothing the oracle imports may raise it)."""
    import mpmath as mp
    saved = mp.mp.dps
    try:
        mp.mp.dps = 15
        spec = importlib.util.spec_from_file_location(m.__name__ + "_own", m.__file__)
        m2 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m2)
        worst = 0.0
        for n in ("sigma_ZZ", "sigma_W"):
            for mh in (1e6, 1e10, 1e14):
                ref = REF[n](0.0, MW, MZ, mh * 1.0, ALPHA, MW) if mh < 1e12 else None
                if ref is None:
                    ref = REF[n](MW**2, MW, MZ, mh, ALPHA, MW)
                    v = getattr(m2, n)(MW**2, MW, MZ, mh, ALPHA, MW)
                else:
                    v = getattr(m2, n)(0.0, MW, MZ, mh, ALPHA, MW)
                worst = max(worst, _dev(v, ref, ALPHA * mh**2))
    finally:
        mp.mp.dps = saved
    return worst < 1e-8, f"large M_H (1e6, 1e10, 1e14 GeV) at the build's own precision: worst {worst:.1e}"


ORACLE = [("all four self-energies against the reference on a (k^2, masses, alpha, mu) grid, 1e-9", grid_check),
          ("real parts above the thresholds", high_k2_check),
          ("M_H from 1 GeV to 1e9 GeV", higgs_mass_check),
          ("MS-bar scale from 1 GeV to 1e4 GeV", mu_check),
          ("large M_H at the build's own precision", own_precision_check)]


# Checks adopted from the Opus audit (AUDIT.md section 4): six wrong mutants had survived the first gate. grid_check_absfloor replaces grid_check (an absolute floor where the
# reference is exactly zero, so a correct double-precision build is not rejected); the rest are new.
_pa = importlib.util.spec_from_file_location("bos_se_audit_checks", os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_proposed_checks.py"))
AC = importlib.util.module_from_spec(_pa)
_pa.loader.exec_module(AC)
ORACLE = [(n, f) for n, f in ORACLE if f is not grid_check] + list(AC.CHECKS)
