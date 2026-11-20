# CANARY-1d9f4c7a2e6b8350-nucleon_pol: planted so a builder transcript that contains this string has read the oracle
"""Hidden oracle for the nucleon_pol campaign.

Target (Bernard, Kaiser, Meissner, Phys. Rev. Lett. 67, 1515 (1991), the standard O(p^3) heavy-baryon result; recalled by the orchestrator, NOT transcribed from a page, so the two blind builds and the auditor are the check on it):
alpha_E = 5 e^2 g_A^2 / (384 pi^2 f_pi^2 m_pi) = 5 alpha g_A^2 / (96 pi f_pi^2 m_pi), beta_M = alpha_E / 10 = e^2 g_A^2 / (768 pi^2 f_pi^2 m_pi), in the convention H = -(1/2) 4 pi alpha_E E^2 of the SPEC.
At g_A = 1.27, f_pi = 92.4 MeV, m_pi = 139.57 MeV this is 12.6e-4 fm^3 (measured proton: 11.2 +- 0.4)."""
import math

LINT_TARGETS = [12.6e-4, 1.26e-3, 1.26e-4]
LINT_EXACT = [5 / (96 * math.pi), 1 / (192 * math.pi), 5 / (384 * math.pi**2), 1 / (768 * math.pi**2)]
HBARC = 197.3269804


def ref_alpha(gA, f, m, a):
    return 5 * a * gA**2 / (96 * math.pi * f**2 * m)


def ref_beta(gA, f, m, a):
    return a * gA**2 / (192 * math.pi * f**2 * m)


POINTS = [(1.27, 92.4, 139.57, 1 / 137.035999), (1.0, 80.0, 300.0, 1 / 100.0), (2.0, 120.0, 90.0, 1 / 150.0), (1.27, 130.0, 500.0, 1 / 137.0), (0.5, 60.0, 50.0, 1 / 120.0)]


def alpha_check(m):
    worst = max(abs(m.alpha_E(*p) / ref_alpha(*p) - 1) for p in POINTS)
    return worst < 1e-12, f"alpha_E against the reference at {len(POINTS)} parameter points: worst {worst:.1e}"


def beta_check(m):
    worst = max(abs(m.beta_M(*p) / ref_beta(*p) - 1) for p in POINTS)
    return worst < 1e-12, f"beta_M against the reference: worst {worst:.1e}"


def fm3_check(m):
    p = POINTS[0]
    v = m.to_fm3(m.alpha_E(*p))
    return abs(v / (ref_alpha(*p) * HBARC**3) - 1) < 1e-12 and abs(v - 12.6e-4) < 0.1e-4, f"alpha_E in fm^3: {v:.4e} (reference {ref_alpha(*p) * HBARC**3:.4e})"


ORACLE = [("alpha_E against 5 alpha gA^2 / (96 pi f^2 m_pi)", alpha_check), ("beta_M = alpha_E/10", beta_check), ("unit conversion and the physical-point value", fm3_check)]
