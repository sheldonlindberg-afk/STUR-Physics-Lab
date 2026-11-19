# CANARY-9a4f6e2d1b8c3057-bos_dr: planted so a builder transcript that contains this string has read the oracle
"""Hidden oracle for the bos_dr campaign.

Target: the non-fermionic part of Delta r of Denner, Fortschr. Phys. 41 (1993) 307 (arXiv:0709.1075) eq. (8.14) with the self-energies of appendix B and
delta_VB = (alpha/4 pi s^2)[6 + (7 - 4 s^2)/(2 s^2) ln c^2] (the textbook vertex + box + wave-function term in the 't Hooft-Feynman gauge). The bosonic self-energies were
checked by two blind builds (campaign bos_se); the sum is UV finite and mu independent, its M_H dependence equals the independently derived Higgs result
(campaigns higgs_dr, higgs_dr_xi) to 1e-16, and the full Delta r reproduces the paper's M_W at its benchmark within 0.01 GeV (after the O(alpha alpha_s) term)."""
import importlib.util, math, os

_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reference_denner.py")
_s = importlib.util.spec_from_file_location("bos_dr_reference", _p)
R = importlib.util.module_from_spec(_s)
_s.loader.exec_module(R)

MW, MZ, MH, ALPHA = 80.38, 91.19, 125.0, 1 / 128.0
LINT_TARGETS = []
LINT_EXACT = []
POINTS = [(80.38, 91.19, 125.0, 1 / 128.0), (80.0, 92.0, 300.0, 1 / 130.0), (75.0, 91.19, 60.0, 1 / 125.0), (85.0, 91.19, 1000.0, 1 / 129.0), (70.0, 100.0, 200.0, 1 / 132.0)]


def vb_ref(mw, mz, al):
    s2 = 1 - (mw / mz) ** 2
    return al / (4 * math.pi * s2) * (6 + (7 - 4 * s2) / (2 * s2) * math.log(1 - s2))


def total_check(m):
    worst, where = 0.0, None
    for p in POINTS:
        ref = R.dr_bos(*p)
        d = abs(m.delta_r_bos(*p) / ref - 1)
        if d > worst:
            worst, where = d, p
    return worst < 1e-9, f"Delta r_bos against the reference at {len(POINTS)} (MW, MZ, MH, alpha): worst relative deviation {worst:.1e} at {where}"


def vb_check(m):
    worst = 0.0
    for (mw, mz, mh, al) in POINTS:
        worst = max(worst, abs(m.delta_vb(mw, mz, al) / vb_ref(mw, mz, al) - 1))
    return worst < 1e-9, f"delta_vb against the textbook value: worst {worst:.1e}"


def mh_scan_check(m):
    worst, where = 0.0, None
    for mh in (1.0, 20.0, 91.19, 400.0, 5e3, 1e5, 1e7):
        ref = R.dr_bos(MW, MZ, mh, ALPHA)
        d = abs(m.delta_r_bos(MW, MZ, mh, ALPHA) / ref - 1)
        if d > worst:
            worst, where = d, mh
    return worst < 1e-8, f"M_H from 1 GeV to 1e7 GeV: worst {worst:.1e} at {where}"


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
            worst = max(worst, abs(m2.delta_r_bos(MW, MZ, mh, ALPHA) / R.dr_bos(MW, MZ, mh, ALPHA) - 1))
    finally:
        mp.mp.dps = saved
    return worst < 1e-8, f"large M_H at the build's own precision: {worst:.1e}"


ORACLE = [("Delta r_bos against the reference at five (MW, MZ, MH, alpha), 1e-9", total_check),
          ("delta_vb against the textbook vertex+box+wave-function value", vb_check),
          ("Delta r_bos for M_H from 1 GeV to 1e7 GeV", mh_scan_check),
          ("large M_H at the build's own precision", own_precision_check)]
