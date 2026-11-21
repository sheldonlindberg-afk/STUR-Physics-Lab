"""Auditor's proposed additional checks for the higgs_dr_xi campaign (see AUDIT.md section 5).

Same shape as campaign.BLIND / oracle.ORACLE: functions taking the build module m and returning (ok: bool, detail: str).
All three are blind (no reference value). They rest on a theorem the audit derived independently (AUDIT.md section 2), not on the builds' word:
the g^{mu nu} coefficient of the sum of the Higgs-containing 1PI diagrams (H-V, H-Goldstone, HH seagull; tadpoles excluded as SPEC section 2 says)
is xi independent at every q^2 below the physical threshold, for every xi >= 0, because the xi-dependent parts of the H-V and H-Goldstone
integrands cancel pointwise in k after transverse projection. So sigma_V(q2, ..., xi) must equal sigma_V(q2, ..., 1), which the oracle already pins
to the Feynman-gauge reference. The oracle compares only Delta r at xi != 1 (and only xi <= 25); these checks close that gap.

    python3 audit_proposed_checks.py <dir with higgs_dr_xi.py> [...]
"""
import sys, math, importlib.util
sys.dont_write_bytecode = True

MW, MZ, ALPHA = 80.38, 91.19, 1 / 128.0
XI_WIDE = (0.0, 1e-6, 1e-3, 0.01, 0.1, 0.2, 0.3, 2.0, 4.0, 25.0, 100.0, 1e3, 1e4)


def _rel(a, b):
    if not (isinstance(a, float) and math.isfinite(a)):
        return float("inf")
    return abs(a / b - 1) if b != 0 else abs(a)


def B_sigma_xi_independent(m):
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


def B_delta_r_xi_wide(m):
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


def B_log_coefficient_xi_wide(m):
    """log_coefficient does not depend on xi, including xi outside the oracle grid."""
    ref = m.log_coefficient(MW, MZ, ALPHA, 1.0)
    w = max(_rel(m.log_coefficient(MW, MZ, ALPHA, xi), ref) for xi in (1e-3, 0.1, 100.0, 1e4))
    return w < 1e-12, f"worst |B(xi)/B(1) - 1| for xi = 1e-3, 0.1, 100, 1e4: {w:.1e}"


CHECKS = [("B_sigma_xi_independent", B_sigma_xi_independent),
          ("B_delta_r_xi_wide", B_delta_r_xi_wide),
          ("B_log_coefficient_xi_wide", B_log_coefficient_xi_wide)]


def _load(d):
    import os
    p = os.path.join(d, "higgs_dr_xi.py")
    spec = importlib.util.spec_from_file_location("higgs_dr_xi_under_test_" + str(abs(hash(d))), p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


if __name__ == "__main__":
    for d in sys.argv[1:]:
        mod = _load(d)
        print("==", d)
        for name, fn in CHECKS:
            try:
                ok, msg = fn(mod)
            except Exception as e:
                ok, msg = False, f"{type(e).__name__}: {e}"
            print(f"   [{'PASS' if ok else 'FAIL'}] {name}: {msg}")
