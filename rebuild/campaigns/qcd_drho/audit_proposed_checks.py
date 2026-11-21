"""Red-team proposed checks for the qcd_drho campaign (see AUDIT.md).  Each takes the build module m and returns (ok, msg).

They close the gaps the surviving mutants of AUDIT.md section 3 went through:
  * delta_rho_qcd is only probed at (N_C, C_F) = (3, 4/3)                -> audit_total_general_colour
  * c_pole is only probed at mu/m = 1 (a mu-dependent pole coefficient passes) -> audit_pole_mu_independent, audit_coeff_wide
  * c is only probed for C_F in [0.75, 3] and mu/m in [0.3, 20]          -> audit_coeff_wide
  * the pole/MS-bar consistency of delta_rho_qcd itself (reference-free, uses only m_pole = mbar[1 + C_F a (1 + 3/4 L)])
                                                                          -> audit_scheme_consistency
  * delta_rho_qcd is exactly linear in alpha_s (SPEC 3)                   -> audit_alpha_linear
AUDIT values: c_pole/C_F, c_MSbar(mu = mbar)/C_F and the ln(mu^2/mbar^2) coefficient come from the auditor's independent
Goldstone-route computation (.../scratchpad/audit-qcd_drho/goldstone.py, goldstone.log; numerical eps -> 0 limit at
eps = 1e-30 with 150 digits; PSLQ identifies -(3 + pi^2)/6 and (9 - pi^2)/6).
Usage: python3 audit_proposed_checks.py <build dir>
"""
import importlib.util, math, os, sys

GF = 1.1663788e-5
AUD_POLE = -2.14493406684822643647241516665      # c_pole / C_F           (Goldstone route)
AUD_MS0 = -0.144934066848226436472415166646      # c_MSbar(mu = mbar)/C_F (Goldstone route)
AUD_LOG = 1.5                                    # d (c_MSbar/C_F) / d ln(mu^2/mbar^2)


def aud_coeff(scheme, cf, r):
    return cf * AUD_POLE if scheme == "pole" else cf * (AUD_MS0 + AUD_LOG * math.log(r * r))


def aud_oneloop(mm, gf, nc):
    return nc * gf * mm * mm / (8 * math.sqrt(2) * math.pi ** 2)


def _rel(v, r, floor=1e-12):
    try:
        v = float(v)
    except Exception:
        return float("inf")
    return abs(v - r) / max(abs(r), floor) if math.isfinite(v) else float("inf")


def audit_coeff_wide(m):
    """c over C_F = 0.05 ... 12 and mu/m = 1e-4 ... 1e4 (pole at mu/m = 1e-3, 1, 1e3), against the auditor's values; relative 1e-9."""
    worst, where = 0.0, None
    for cf in (0.05, 1 / 3, 4 / 3, 4.5, 12.0):
        pts = [("pole", r) for r in (1e-3, 1.0, 1e3)] + [("msbar", r) for r in (1e-4, 0.01, 0.7, 1.3, 50.0, 1e4)]
        for sch, r in pts:
            d = _rel(m.qcd_coeff(sch, cf, r), aud_coeff(sch, cf, r))
            if d > worst:
                worst, where = d, (cf, sch, r)
    return worst < 1e-9, f"45 points: worst relative {worst:.1e} at {where}"


def audit_pole_mu_independent(m):
    """Reference-free: the pole coefficient and delta_rho_qcd(pole) do not depend on mu_over_m (SPEC 3: it is ignored)."""
    worst = 0.0
    for cf in (0.5, 4 / 3, 3.0):
        c1 = m.qcd_coeff("pole", cf, 1.0)
        t1 = m.delta_rho_qcd(172.5, GF, 3, cf, 0.118, "pole", 1.0)
        for r in (1e-6, 0.1, 0.5, 2.0, 37.0, 1e6):
            worst = max(worst, _rel(m.qcd_coeff("pole", cf, r), c1), _rel(m.delta_rho_qcd(172.5, GF, 3, cf, 0.118, "pole", r), t1))
    return worst < 1e-13, f"max relative change of c_pole and Delta rho(pole) over mu/m = 1e-6 ... 1e6: {worst:.1e}"


def audit_total_general_colour(m):
    """delta_rho_qcd at (N_C, C_F) away from (3, 4/3), both schemes, alpha_s = 0.01, 0.2: against the auditor's
    Delta rho_0 (1 + c alpha_s/pi) and against the module's own delta_rho_oneloop x (1 + qcd_coeff alpha_s/pi); relative 1e-10."""
    worst, where = 0.0, None
    for nc, cf in ((2, 0.75), (5, 2.4), (3, 1.0), (8, 0.5), (4, 15 / 8), (1, 0.0)):
        for sch, r in (("pole", 1.0), ("msbar", 1.0), ("msbar", 3.0)):
            for a in (0.01, 0.2):
                v = m.delta_rho_qcd(150.0, GF, nc, cf, a, sch, r)
                ref = aud_oneloop(150.0, GF, nc) * (1 + aud_coeff(sch, cf, r) * a / math.pi)
                own = m.delta_rho_oneloop(150.0, GF, nc) * (1 + m.qcd_coeff(sch, cf, r) * a / math.pi)
                d = max(_rel(v, ref), _rel(v, own))
                if d > worst:
                    worst, where = d, (nc, cf, sch, r, a)
    return worst < 1e-10, f"worst relative {worst:.1e} at (N_C, C_F, scheme, mu/m, alpha_s) = {where}"


def audit_scheme_consistency(m):
    """Reference-free physics: Delta rho is scheme independent at O(alpha_s). With m_pole = mbar[1 + C_F a (1 + (3/4) L)],
    a = alpha_s/pi, L = ln(mu^2/mbar^2), delta_rho_qcd(mbar, 'msbar', mu/mbar) / delta_rho_qcd(m_pole, 'pole') - 1 = O(a^2):
    at a ~ 3e-6 it must be below 20 (1 + |L|)^2 (C_F a)^2 (a wrong O(a) shift gives ~ C_F a ~ 1e-5)."""
    worst, where = 0.0, None
    for cf in (0.5, 4 / 3, 3.0):
        for r in (0.05, 0.5, 1.0, 2.0, 40.0):
            alphas = 1e-5
            a = alphas / math.pi
            Lg = math.log(r * r)
            mbar = 160.0
            mpole = mbar * (1 + cf * a * (1 + 0.75 * Lg))
            dms = m.delta_rho_qcd(mbar, GF, 3, cf, alphas, "msbar", r)
            dpo = m.delta_rho_qcd(mpole, GF, 3, cf, alphas, "pole", 1.0)
            x = abs(dms / dpo - 1) / (20 * (1 + abs(Lg)) ** 2 * (cf * a) ** 2)
            if x > worst:
                worst, where = x, (cf, r)
    return worst < 1, f"max |ratio - 1| / bound = {worst:.2e} at (C_F, mu/mbar) = {where}"


def audit_alpha_linear(m):
    """delta_rho_qcd = Delta rho_0 (1 + c alpha_s/pi) is exactly linear in alpha_s (no resummation): second difference."""
    worst = 0.0
    for sch, r in (("pole", 1.0), ("msbar", 0.2), ("msbar", 5.0)):
        v = [m.delta_rho_qcd(172.5, GF, 3, 4 / 3, a, sch, r) for a in (0.0, 0.25, 0.5)]
        worst = max(worst, abs(v[2] - 2 * v[1] + v[0]) / abs(v[0]))
    return worst < 1e-13, f"second difference over alpha_s = 0, 0.25, 0.5 relative to Delta rho_0: {worst:.1e}"


CHECKS = [("coefficient for C_F in [0.05, 12], mu/m in [1e-4, 1e4] (auditor's Goldstone route)", audit_coeff_wide),
          ("pole coefficient and pole Delta rho independent of mu_over_m", audit_pole_mu_independent),
          ("delta_rho_qcd at general (N_C, C_F)", audit_total_general_colour),
          ("pole vs MS-bar Delta rho agree to O(alpha_s^2) (reference-free)", audit_scheme_consistency),
          ("delta_rho_qcd exactly linear in alpha_s", audit_alpha_linear)]

if __name__ == "__main__":
    sys.dont_write_bytecode = True
    d = os.path.abspath(sys.argv[1])
    s = importlib.util.spec_from_file_location("qcd_drho", os.path.join(d, "qcd_drho.py"))
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
