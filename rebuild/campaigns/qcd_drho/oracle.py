# CANARY-6c3e8a1f5b9d2740-qcd_drho: planted so a builder transcript that contains this string has read the oracle
"""Hidden oracle for the qcd_drho campaign.

Target (Djouadi and Verzegnassi 1987; Kniehl 1990; the standard result, recalled by the orchestrator, NOT transcribed from a page, so the two blind builds and the auditor are the check on it):
Delta rho = N_C G_F m_t^2/(8 sqrt(2) pi^2) [1 - (C_F/2)(1 + pi^2/3)(alpha_s/pi)] with the pole mass (C_F = 4/3: -(2/3)(1 + pi^2/3) = -2.8599), and with the MS-bar mass m_t(mu = m_t) the
coefficient shifts by +2 C_F (m_pole = mbar [1 + C_F alpha_s/pi]) to -0.1932; for mu != mbar the running mbar(mu) adds (3 C_F/2) ln(mu^2/mbar^2) (anomalous dimension gamma_m^0 = 3 C_F/4 in a = alpha_s/pi)."""
import math

LINT_TARGETS = [2.8599, 2.859, 0.1932, 0.193, 2.1449, 0.14493]     # audit C5: the C_F-stripped values too
LINT_EXACT = [0.5 + math.pi**2 / 6, 1.5 - math.pi**2 / 6, -(0.5 + math.pi**2 / 6), -(1.5 - math.pi**2 / 6), (3 + math.pi**2) / 6, (9 - math.pi**2) / 6]
GF = 1.1663788e-5


def ref_oneloop(m, gf, nc):
    return nc * gf * m * m / (8 * math.sqrt(2) * math.pi**2)


def ref_coeff(scheme, cf, r):
    c = -(cf / 2) * (1 + math.pi**2 / 3)
    if scheme == "pole":
        return c
    return c + 2 * cf + 1.5 * cf * 2 * math.log(r)


def one_check(m):
    worst = 0.0
    for mm in (50.0, 172.5, 1000.0):
        for gf in (GF, 2e-5):
            for nc in (3, 2, 5):
                worst = max(worst, abs(m.delta_rho_oneloop(mm, gf, nc) / ref_oneloop(mm, gf, nc) - 1))
    return worst < 1e-12, f"one-loop Delta rho_0 against N_C G_F m^2/(8 sqrt2 pi^2): {worst:.1e}"


def coeff_check(m):
    worst, where = 0.0, None
    for cf in (4 / 3, 0.75, 1.0, 2.5, 3.0):
        for sch, r in (("pole", 1.0), ("msbar", 1.0), ("msbar", 0.3), ("msbar", 2.5), ("msbar", 20.0)):
            ref = ref_coeff(sch, cf, r)
            d = abs(m.qcd_coeff(sch, cf, r) - ref) / abs(ref) if abs(ref) > 1e-9 else abs(m.qcd_coeff(sch, cf, r))
            if d > worst:
                worst, where = d, (cf, sch, r)
    return worst < 1e-9, f"c(scheme, C_F, mu/m) against the reference over five C_F and five schemes/scales: worst relative {worst:.1e} at {where}"


def total_check(m):
    worst = 0.0
    for sch, r in (("pole", 1.0), ("msbar", 1.0), ("msbar", 0.5)):
        for a in (0.05, 0.118, 0.3):
            ref = ref_oneloop(172.5, GF, 3) * (1 + ref_coeff(sch, 4 / 3, r) * a / math.pi)
            worst = max(worst, abs(m.delta_rho_qcd(172.5, GF, 3, 4 / 3, a, sch, r) / ref - 1))
    return worst < 1e-10, f"delta_rho_qcd against the reference: {worst:.1e}"


ORACLE = [("one-loop Delta rho_0", one_check), ("O(alpha_s) coefficient, pole and MS-bar, general C_F and mu", coeff_check), ("Delta rho with QCD", total_check)]


# Checks adopted from the Opus audit (AUDIT.md): seven wrong mutants had survived the first gate (C_F or N_C handled only at the physical point, the pole coefficient probed only at mu = m, narrow windows).
import importlib.util as _iu
_pa = _iu.spec_from_file_location("qcd_drho_audit_checks", __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "audit_proposed_checks.py"))
AC = _iu.module_from_spec(_pa)
_pa.loader.exec_module(AC)
ORACLE = ORACLE + list(AC.CHECKS)
