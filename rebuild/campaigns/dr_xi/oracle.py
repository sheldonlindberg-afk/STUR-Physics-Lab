# CANARY-4b7a2e9c6d1f8035-dr_xi: planted so a builder transcript that contains this string has read the oracle
"""Hidden oracle for the dr_xi campaign.

Target: the xi = 1 value is the bos_dr reference (Denner eq. 8.14, appendix B, bosonic part; reference_denner.dr_bos), accepted from two blind builds; the physical requirement is that the total be
independent of xi. A build that ignores xi passes both of those, so the classes SE and VBW are compared between the two builds by the orchestrator (cross_build.py) and by the auditor's independent
derivation; this oracle checks the total against the reference at every xi, the sum rule of the classes, and mu independence of the sum."""
import importlib.util, math, os

_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reference_denner.py")
_s = importlib.util.spec_from_file_location("dr_xi_reference", _p)
R = importlib.util.module_from_spec(_s)
_s.loader.exec_module(R)

LINT_TARGETS = []
LINT_EXACT = []
POINTS = [(80.38, 91.19, 125.0, 1 / 128.0), (80.0, 92.0, 300.0, 1 / 130.0), (75.0, 91.19, 60.0, 1 / 125.0), (85.0, 91.19, 1000.0, 1 / 129.0), (70.0, 100.0, 200.0, 1 / 132.0)]
XIS = (0.0, 0.2, 1.0, 3.0, 25.0, 400.0)


def total_check(m):
    worst, where = 0.0, None
    for p in POINTS:
        ref = R.dr_bos(*p)
        for xi in XIS:
            d = abs(m.delta_r_bos_xi(*p, xi) / ref - 1)
            if d > worst:
                worst, where = d, (p, xi)
    return worst < 1e-9, f"total against the xi = 1 reference at {len(POINTS)} points x {len(XIS)} xi: worst {worst:.1e} at {where}"


def sum_check(m):
    worst, where = 0.0, None
    for (mw, mz, mh, al) in POINTS:
        ref = R.dr_bos(mw, mz, mh, al)
        for xi in (0.0, 0.7, 5.0):
            for mu in (10.0, mw, 3000.0):
                tot = m.delta_r_se(mw, mz, mh, al, xi, mu) + m.delta_r_vbw(mw, mz, al, xi, mu)
                d = abs(tot / ref - 1)
                if d > worst:
                    worst, where = d, (mw, mz, mh, xi, mu)
    return worst < 1e-9, f"SE + VBW against the reference, xi and mu varied: worst {worst:.1e} at {where}"


def mh_xi_check(m):
    worst, where = 0.0, None
    for mh in (1.0, 20.0, 400.0, 5e3, 1e6, 1e9):
        for xi in (0.0, 1.0, 6.0):
            ref = R.dr_bos(80.38, 91.19, mh, 1 / 128.0)
            d = abs(m.delta_r_bos_xi(80.38, 91.19, mh, 1 / 128.0, xi) / ref - 1)
            if d > worst:
                worst, where = d, (mh, xi)
    return worst < 1e-8, f"M_H from 1 GeV to 1e9 GeV at three xi: worst {worst:.1e} at {where}"


def own_precision_check(m):
    import mpmath as mp
    saved = mp.mp.dps
    try:
        mp.mp.dps = 15
        spec = importlib.util.spec_from_file_location(m.__name__ + "_own", m.__file__)
        m2 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m2)
        worst = 0.0
        for mh in (1e6, 1e9):
            for xi in (0.0, 5.0):
                worst = max(worst, abs(m2.delta_r_bos_xi(80.38, 91.19, mh, 1 / 128.0, xi) / R.dr_bos(80.38, 91.19, mh, 1 / 128.0) - 1))
    finally:
        mp.mp.dps = saved
    return worst < 1e-8, f"large M_H at the build's own precision: {worst:.1e}"


ORACLE = [("total against the reference at every xi", total_check),
          ("SE + VBW against the reference, xi and mu varied", sum_check),
          ("M_H scan at three xi", mh_xi_check),
          ("at the build's own precision", own_precision_check)]


# Checks adopted from the Opus audit (AUDIT.md): ten wrong mutants had survived the first gate (anything moved between the classes SE and VBW, small-xi branches, a Feynman-gauge photon or Z).
_pa = importlib.util.spec_from_file_location("dr_xi_audit_checks", os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_proposed_checks.py"))
AC = importlib.util.module_from_spec(_pa)
_pa.loader.exec_module(AC)
ORACLE = ORACLE + list(AC.CHECKS)
