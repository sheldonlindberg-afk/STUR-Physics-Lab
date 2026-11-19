# CANARY-8d1e5b3a7c924f06-ferm_se: planted so a builder transcript that contains this string has read the oracle
"""Hidden oracle for the ferm_se campaign.

Target: the fermionic transverse self-energies of Denner, Fortschr. Phys. 41 (1993) 307 (arXiv:0709.1075), appendix B, eqs. (B.1)-(B.4), fermion loops only, 't Hooft-Feynman gauge,
MS-bar, real parts. Transcribed by the orchestrator from the page images (reference_denner.py, the same transcription as the bos_se campaign; its fermionic Delta r is UV finite and
mu independent to 1e-16, and its M_W at the benchmark agrees with the paper's table to 0.01 GeV after the O(alpha alpha_s) correction). Class: reference is a published formula, not an independent derivation."""
import importlib.util, math, os

_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reference_denner.py")
_s = importlib.util.spec_from_file_location("ferm_se_reference", _p)
R = importlib.util.module_from_spec(_s)
_s.loader.exec_module(R)

MW, MZ, ALPHA = 80.38, 91.19, 1 / 128.0
LINT_TARGETS = []
LINT_EXACT = []
# Denner's photon field has the opposite sign to the SPEC's (A = s W3 + c B), so Sigma^AZ(SPEC) = - Sigma^AZ(Denner) (the bos_se campaign, class R there).
REF = {"sigma_AA": R.f_AA, "sigma_AZ": lambda *a: -R.f_AZ(*a), "sigma_ZZ": R.f_ZZ, "sigma_W": R.f_W}

LEP = ((0.000510998, -1, -0.5, 1), (0.0, 0, 0.5, 1), (0.105658, -1, -0.5, 1), (0.0, 0, 0.5, 1), (1.77686, -1, -0.5, 1), (0.0, 0, 0.5, 1))
QUA = ((0.062, 2 / 3, 0.5, 3), (0.083, -1 / 3, -0.5, 3), (1.27, 2 / 3, 0.5, 3), (0.095, -1 / 3, -0.5, 3), (172.76, 2 / 3, 0.5, 3), (4.18, -1 / 3, -0.5, 3))
SETS = {"leptons": LEP, "quarks": QUA, "all": LEP + QUA, "top only": ((172.76, 2 / 3, 0.5, 3),), "odd": ((300.0, 1.0, 1.5, 2), (0.0, -2 / 3, -0.5, 5), (91.0, 0.0, 0.0, 1))}
DOUB = {"leptons": ((0.0, 0.000510998, 1.0), (0.0, 0.105658, 1.0), (0.0, 1.77686, 1.0)),
        "quarks": ((0.062, 0.083, 3 * 0.9743**2), (0.062, 0.095, 3 * 0.225**2), (1.27, 0.095, 3 * 0.9735**2), (1.27, 0.083, 3 * 0.225**2), (172.76, 4.18, 3 * 0.9991**2), (172.76, 0.095, 3 * 0.0412**2)),
        "top-bottom": ((172.76, 4.18, 3.0),), "equal": ((91.0, 91.0, 1.0),), "odd": ((300.0, 10.0, 2.0), (0.0, 0.0, 1.0))}


def _dev(v, r, scale):
    try:
        v = float(v)
    except Exception:
        return float("inf")
    if not math.isfinite(v):
        return float("inf")
    return abs(v - r) / (abs(r) + 1e-9 * scale)


def _points():
    for k2 in (-5.0 * MW**2, -1000.0, 0.0, 0.3 * MW**2, MW**2, MZ**2, 3.0 * MW**2, 4 * 4.18**2 * 1.01, 4 * 172.76**2 * 1.2):
        for (mw, mz, al, mu) in ((MW, MZ, ALPHA, MW), (80.0, 92.0, 1 / 130.0, 2.2 * 80.0), (75.0, 91.19, 1 / 125.0, 0.6 * 75.0)):
            yield k2, mw, mz, al, mu


def grid_check(m):
    worst, where = 0.0, None
    for n in ("sigma_AA", "sigma_AZ", "sigma_ZZ"):
        for name, fs in SETS.items():
            for k2, mw, mz, al, mu in _points():
                ref = REF[n](k2, fs, mw, mz, al, mu)
                d = _dev(getattr(m, n)(k2, fs, mw, mz, al, mu), ref, al * mw**2)
                if d > worst:
                    worst, where = d, (n, name, k2, mw)
    for name, ds in DOUB.items():
        for k2, mw, mz, al, mu in _points():
            ref = REF["sigma_W"](k2, ds, mw, mz, al, mu)
            d = _dev(m.sigma_W(k2, ds, mw, mz, al, mu), ref, al * mw**2)
            if d > worst:
                worst, where = d, ("sigma_W", name, k2, mw)
    return worst < 1e-9, f"worst relative deviation from the reference over the fermion sets and (k^2, masses, alpha, mu) grid: {worst:.1e} at {where}"


def mu_check(m):
    worst, where = 0.0, None
    for n in ("sigma_AA", "sigma_AZ", "sigma_ZZ"):
        for mu in (1.0, 20.0, 400.0, 1.0e4):
            for k2 in (-3000.0, 0.0, MW**2):
                ref = REF[n](k2, SETS["all"], MW, MZ, ALPHA, mu)
                d = _dev(getattr(m, n)(k2, SETS["all"], MW, MZ, ALPHA, mu), ref, ALPHA * MW**2 * 10)
                if d > worst:
                    worst, where = d, (n, mu, k2)
    for mu in (1.0, 20.0, 400.0, 1.0e4):
        for k2 in (-3000.0, 0.0, MW**2):
            ref = REF["sigma_W"](k2, DOUB["quarks"], MW, MZ, ALPHA, mu)
            d = _dev(m.sigma_W(k2, DOUB["quarks"], MW, MZ, ALPHA, mu), ref, ALPHA * MW**2 * 10)
            if d > worst:
                worst, where = d, ("sigma_W", mu, k2)
    return worst < 1e-9, f"MS-bar scale from 1 GeV to 1e4 GeV: worst {worst:.1e} at {where}"


def mass_scan_check(m):
    """One fermion mass from 1e-6 GeV to 1e4 GeV (light-fermion logs, heavy-fermion decoupling)."""
    worst, where = 0.0, None
    for mass in (1e-6, 1e-3, 0.1, 5.0, 80.0, 500.0, 1e4):
        fs = ((mass, -1.0, -0.5, 1), (0.0, 0, 0.5, 1))
        dd = ((0.0, mass, 1.0),)
        for k2 in (-2000.0, 0.0, MW**2, 0.9 * 4 * mass**2):
            for n in ("sigma_AA", "sigma_AZ", "sigma_ZZ"):
                ref = REF[n](k2, fs, MW, MZ, ALPHA, MW)
                d = _dev(getattr(m, n)(k2, fs, MW, MZ, ALPHA, MW), ref, ALPHA * max(mass, MW) ** 2)
                if d > worst:
                    worst, where = d, (n, mass, k2)
            ref = REF["sigma_W"](k2, dd, MW, MZ, ALPHA, MW)
            d = _dev(m.sigma_W(k2, dd, MW, MZ, ALPHA, MW), ref, ALPHA * max(mass, MW) ** 2)
            if d > worst:
                worst, where = d, ("sigma_W", mass, k2)
    return worst < 1e-8, f"fermion mass from 1e-6 to 1e4 GeV: worst {worst:.1e} at {where}"


def above_threshold_check(m):
    worst, where = 0.0, None
    fs = ((172.76, 2 / 3, 0.5, 3), (4.18, -1 / 3, -0.5, 3))
    for k2 in (1.1 * (2 * 4.18) ** 2, 2 * 172.76**2 * 1.0, (2 * 172.76) ** 2 * 1.3, 4 * 172.76**2 * 5.0):
        for n in ("sigma_AA", "sigma_AZ", "sigma_ZZ"):
            ref = REF[n](k2, fs, MW, MZ, ALPHA, MW)
            d = _dev(getattr(m, n)(k2, fs, MW, MZ, ALPHA, MW), ref, ALPHA * k2)
            if d > worst:
                worst, where = d, (n, k2)
        ref = REF["sigma_W"](k2, ((172.76, 4.18, 3.0),), MW, MZ, ALPHA, MW)
        d = _dev(m.sigma_W(k2, ((172.76, 4.18, 3.0),), MW, MZ, ALPHA, MW), ref, ALPHA * k2)
        if d > worst:
            worst, where = d, ("sigma_W", k2)
    return worst < 1e-9, f"real parts above the thresholds: worst {worst:.1e} at {where}"


def own_precision_check(m):
    import mpmath as mp
    saved = mp.mp.dps
    try:
        mp.mp.dps = 15
        spec = importlib.util.spec_from_file_location(m.__name__ + "_own", m.__file__)
        m2 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m2)
        worst = 0.0
        for k2 in (0.0, MW**2):
            fs = SETS["all"]
            for n in ("sigma_AA", "sigma_ZZ"):
                worst = max(worst, _dev(getattr(m2, n)(k2, fs, MW, MZ, ALPHA, MW), REF[n](k2, fs, MW, MZ, ALPHA, MW), ALPHA * MW**2))
            worst = max(worst, _dev(m2.sigma_W(k2, DOUB["quarks"], MW, MZ, ALPHA, MW), REF["sigma_W"](k2, DOUB["quarks"], MW, MZ, ALPHA, MW), ALPHA * MW**2))
    finally:
        mp.mp.dps = saved
    return worst < 1e-8, f"at the build's own (default) precision: worst {worst:.1e}"


ORACLE = [("all four self-energies against the reference: fermion sets x (k^2, masses, alpha, mu) grid", grid_check),
          ("MS-bar scale from 1 GeV to 1e4 GeV", mu_check),
          ("one fermion mass from 1e-6 to 1e4 GeV", mass_scan_check),
          ("real parts above the thresholds", above_threshold_check),
          ("at the build's own precision", own_precision_check)]
