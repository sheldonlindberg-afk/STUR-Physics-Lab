"""Red-team audit of bos_se: proposed additional checks (see AUDIT.md).

Each check takes the build module m and returns (ok, message). They are meant for the hidden oracle tier (some compare with
reference_denner.py); the ones marked BLIND-OK use no reference and could also go into campaign.BLIND.

Survivors they kill (mutants of build b, AUDIT.md section 4):
  asymptotic_spacelike        M06b (wrong Sigma_ZZ only at k^2 < -5e4 GeV^2)                         BLIND-OK
  custodial_limit             M17 (Sigma_ZZ wrong away from the three oracle c_W values)               BLIND-OK
  global_precision_untouched  M13 (mp.dps changed at import; SPEC 4)                                   BLIND-OK
  dense_higgs_mass            M05b (Sigma_W wrong only for 1.5e5 < M_H < 9e5 GeV)
  heavy_higgs_above_threshold M12 (Sigma_W wrong above the W-H threshold only for M_H > 200 GeV)
  wide_mu                     M15 (Sigma_W wrong only for mu > 2e4 GeV)
  mass_ratio_off_sm           M17 again, with the reference
  grid_check_absfloor         a REPLACEMENT for oracle.grid_check: same points, but an absolute floor 1e-12 alpha M_W^2 where the
                              reference is exactly zero (Sigma_AA(0); Sigma_AZ(0) at mu = M_W), so a correct double-precision build
                              is not rejected (control mutant M14).
Both blind builds pass all of them.
"""
import importlib.util, math, os

MW, MZ, MH, ALPHA = 80.38, 91.19, 125.0, 1 / 128.0
FUNCS = ("sigma_AA", "sigma_AZ", "sigma_ZZ", "sigma_W")
_R = None


def _ref():
    global _R
    if _R is None:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reference_denner.py")
        s = importlib.util.spec_from_file_location("bos_se_reference_audit", p)
        _R = importlib.util.module_from_spec(s)
        s.loader.exec_module(_R)
    R = _R
    return {"sigma_AA": R.sig_AA, "sigma_AZ": lambda *a: -R.sig_AZ(*a), "sigma_ZZ": R.sig_ZZ, "sigma_W": R.sig_W}


def _rel(v, r, floor):
    try:
        v = float(v)
    except Exception:
        return float("inf")
    if not math.isfinite(v):
        return float("inf")
    return abs(v - r) / max(abs(r), floor)


# ----------------------------------------------------------------------------------------------- reference-free (BLIND-OK)
def asymptotic_spacelike(m):
    """k^2 -> -infinity: masses drop out and Sigma -> -(g^2/16pi^2) k^2 X with the textbook massless coefficients in exact-d CDR,
    Feynman gauge: per unit C_A gauge+ghost loop 5/3 B0 + 1/9 (i.e. 5/3 L + 31/9), complex scalar of unit charge -(1/3)(B0 + 2/3),
    B0 = 2 - ln(-k^2/mu^2). SU(2) part: C_A = 2 plus the doublet (T = 1/2); hypercharge part: sum q^2 = 1/2 (times g'^2).
    Z = c W3 - s B, A = s W3 + c B (SPEC 1) fix the A-Z sign. Corrections are O(M^2/k^2 ln): ~1e-8 at k^2 = -1e12."""
    worst, where = 0.0, None
    mu = 300.0
    c2 = MW**2 / MZ**2
    s2 = 1 - c2
    c, s = math.sqrt(c2), math.sqrt(s2)
    g2 = 4 * math.pi * ALPHA / s2
    for k2 in (-1e12, -1e13):
        B0 = 2 - math.log(-k2 / mu**2)
        sc = -(B0 + 2.0 / 3) / 3
        xs, xb = 2 * (5.0 / 3 * B0 + 1.0 / 9) + 0.5 * sc, 0.5 * sc
        pre = -g2 / (16 * math.pi**2) * k2
        pred = {"sigma_W": pre * xs, "sigma_ZZ": pre * (c2 * xs + s2 * s2 / c2 * xb), "sigma_AA": pre * s2 * (xs + xb),
                "sigma_AZ": pre * c * s * (xs - s2 / c2 * xb)}
        for n in FUNCS:
            d = _rel(getattr(m, n)(k2, MW, MZ, MH, ALPHA, mu), pred[n], 1e-300)
            if d > worst:
                worst, where = d, (n, k2)
    return worst < 1e-7, f"large spacelike k^2 against the textbook massless (5/3, 31/9; 1/3, 8/9) coefficients: worst {worst:.1e} at {where}"


def custodial_limit(m):
    """g' -> 0 at fixed g (alpha = g^2 s^2/4pi, M_Z = M_W/c -> M_W): Sigma_ZZ -> Sigma_W and Sigma_AZ = O(s) (exact identities)."""
    g2 = 4 * math.pi * ALPHA / (1 - MW**2 / MZ**2)
    worst_zw, worst_az = 0.0, 0.0
    for s2 in (1e-7, 1e-8):
        mz, al = MW / math.sqrt(1 - s2), g2 * s2 / (4 * math.pi)
        for k2 in (-3000.0, 0.0, 0.5 * MW**2, MW**2):
            for mh, mu in ((125.0, MW), (700.0, 2.3 * MW)):
                w, z = m.sigma_W(k2, MW, mz, mh, al, mu), m.sigma_ZZ(k2, MW, mz, mh, al, mu)
                az = m.sigma_AZ(k2, MW, mz, mh, al, mu)
                scale = max(abs(w), g2 / (16 * math.pi**2) * MW**2)
                worst_zw = max(worst_zw, abs(z - w) / scale)
                worst_az = max(worst_az, abs(az) / (math.sqrt(s2) * scale))
    return worst_zw < 1e-5 and worst_az < 30, (f"custodial limit s^2 -> 0 at fixed g: |Sigma_ZZ - Sigma_W|/|Sigma_W| = {worst_zw:.1e} (must be O(s^2)), "
                                               f"|Sigma_AZ|/(s |Sigma_W|) = {worst_az:.1e} (must stay O(1))")


def global_precision_untouched(m):
    """SPEC 4: keep any high-precision setting local. Re-import the module and call every export; mpmath's global precision
    must be unchanged afterwards."""
    import mpmath as mp
    saved = mp.mp.dps
    try:
        mp.mp.dps = 15
        spec = importlib.util.spec_from_file_location(m.__name__ + "_dps", m.__file__)
        m2 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m2)
        after_import = mp.mp.dps
        for n in FUNCS:
            getattr(m2, n)(0.3 * MW**2, MW, MZ, MH, ALPHA, MW)
            getattr(m2, n)(0.0, MW, MZ, 1e6, ALPHA, MW)
        after_calls = mp.mp.dps
    finally:
        mp.mp.dps = saved
    return after_import == 15 and after_calls == 15, f"mp.dps after import {after_import}, after calls {after_calls} (must stay 15)"


# ----------------------------------------------------------------------------------------------- against the reference
def dense_higgs_mass(m):
    """M_H on a dense log grid (5 per decade, 1 GeV - 1e9 GeV), k^2 in {0, -M_W^2, M_W^2}: closes the windows between the oracle's points."""
    REF = _ref()
    worst, where = 0.0, None
    mhs = [10 ** (j / 5) for j in range(0, 46)]
    for n in ("sigma_ZZ", "sigma_W"):
        for mh in mhs:
            for k2 in (0.0, -MW**2, MW**2):
                d = _rel(getattr(m, n)(k2, MW, MZ, mh, ALPHA, MW), REF[n](k2, MW, MZ, mh, ALPHA, MW), 1e-9 * ALPHA * max(MW, mh) ** 2)
                if d > worst:
                    worst, where = d, (n, mh, k2)
    return worst < 1e-8, f"dense M_H grid 1 GeV - 1e9 GeV: worst {worst:.1e} at {where}"


def heavy_higgs_above_threshold(m):
    """Real parts above the W-H / Z-H thresholds for M_H != 125 GeV (the oracle samples k^2 above threshold only at M_H = 125)."""
    REF = _ref()
    worst, where = 0.0, None
    for mh in (300.0, 700.0, 3000.0):
        for n in FUNCS:
            for k2 in (1.2 * (MW + mh) ** 2, 1.2 * (MZ + mh) ** 2, 3.0 * (MZ + mh) ** 2, 0.5 * (MW + mh) ** 2):
                d = _rel(getattr(m, n)(k2, MW, MZ, mh, ALPHA, 1.4 * MW), REF[n](k2, MW, MZ, mh, ALPHA, 1.4 * MW), 1e-9 * ALPHA * mh**2)
                if d > worst:
                    worst, where = d, (n, mh, k2)
    return worst < 1e-9, f"real parts above the Higgs thresholds, M_H = 300, 700, 3000 GeV: worst {worst:.1e} at {where}"


def wide_mu(m):
    """MS-bar scale far outside 1 - 1e4 GeV (the mu dependence is a pure log: no reason for a build to be limited)."""
    REF = _ref()
    worst, where = 0.0, None
    for n in FUNCS:
        for mu in (1e-2, 3e4, 1e6, 1e9):
            for k2 in (-3000.0, 0.3 * MW**2, MW**2):
                d = _rel(getattr(m, n)(k2, MW, MZ, MH, ALPHA, mu), REF[n](k2, MW, MZ, MH, ALPHA, mu), 1e-8 * ALPHA * MW**2)
                if d > worst:
                    worst, where = d, (n, mu, k2)
    return worst < 1e-9, f"mu from 1e-2 GeV to 1e9 GeV: worst {worst:.1e} at {where}"


def mass_ratio_off_sm(m):
    """c_W far from the SM value (M_Z = 120, 300 GeV at M_W = 80): a coefficient error that happens to vanish at the oracle's three
    c_W values is caught here."""
    REF = _ref()
    worst, where = 0.0, None
    for mz in (82.0, 120.0, 300.0):
        for n in FUNCS:
            for k2 in (-2000.0, 0.0, 0.7 * 80.0**2):
                if n == "sigma_AA" and k2 == 0.0:
                    continue
                d = _rel(getattr(m, n)(k2, 80.0, mz, 150.0, ALPHA, 100.0), REF[n](k2, 80.0, mz, 150.0, ALPHA, 100.0), 1e-12 * ALPHA * 80.0**2)
                if d > worst:
                    worst, where = d, (n, mz, k2)
    return worst < 1e-9, f"M_Z = 82, 120, 300 GeV at M_W = 80 GeV: worst {worst:.1e} at {where}"


def grid_check_absfloor(m):
    """Replacement for oracle.grid_check: identical points, but deviations are measured against max(|ref|, 1e-12 alpha M_W^2), so
    an exact zero of the reference (Sigma_AA(0); Sigma_AZ(0) = 0 at mu = M_W because B0(0, M_W, M_W) = 0 there) is tested at
    1e-21 alpha M_W^2 absolute = far below double-precision roundoff only if the build returns an exact zero. The oracle's
    floor 1e-9 alpha M_W^2 with tolerance 1e-9 demands |Sigma_AA(0)| < 5e-17 GeV^2, which a correct build that sums
    diagrams in double precision cannot guarantee (roundoff ~1e-14 alpha M_W^2; control mutant M14 fails the oracle)."""
    REF = _ref()
    worst, where = 0.0, None
    pts = [(k2, mw, mz, mh, al, mu) for k2 in (-5.0 * MW**2, -1000.0, 0.0, 0.3 * MW**2, 0.99 * MW**2, MW**2, MZ**2)
           for (mw, mz, mh, al, mu) in ((MW, MZ, 125.0, ALPHA, MW), (80.0, 92.0, 300.0, 1 / 130.0, 2.2 * 80.0), (75.0, 91.19, 60.0, 1 / 125.0, 0.6 * 75.0))]
    for n in FUNCS:
        for p in pts:
            r = REF[n](*p)
            v = getattr(m, n)(*p)
            floor = 1e-12 * p[4] * p[1] ** 2 / 1e-9          # with tolerance 1e-9: absolute 1e-12 alpha M_W^2 at a zero of the reference
            d = _rel(v, r, floor if abs(r) < floor else 0.0)
            if d > worst:
                worst, where = d, (n, p)
    return worst < 1e-9, f"oracle grid with an absolute floor at the reference's zeros: worst {worst:.1e} at {where}"


CHECKS = [("asymptotic large spacelike k^2 (textbook massless coefficients)", asymptotic_spacelike),
          ("custodial limit g' -> 0", custodial_limit),
          ("mpmath global precision untouched (SPEC 4)", global_precision_untouched),
          ("dense M_H grid", dense_higgs_mass),
          ("real parts above Higgs thresholds at M_H != 125", heavy_higgs_above_threshold),
          ("wide MS-bar scale", wide_mu),
          ("c_W far from the SM", mass_ratio_off_sm),
          ("grid with absolute floor at zeros (replacement)", grid_check_absfloor)]
