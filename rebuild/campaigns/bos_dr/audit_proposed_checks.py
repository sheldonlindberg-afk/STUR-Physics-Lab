"""Red-team audit of bos_dr: proposed additional checks (see AUDIT.md).

Each check takes the build module m and returns (ok, message). They are meant for the hidden oracle tier (most compare with
reference_denner.py or with the closed-form delta_VB). The ones marked BLIND-OK use neither and could go into campaign.BLIND.

The survivors they kill (mutants of build b, AUDIT.md section 4):
  alpha_linear_wide       M13 (both exports wrong only for alpha < 1/133, i.e. at the Thomson value)     BLIND-OK
  thomson_alpha_reference M13, against the reference at alpha = 1/137.035999
  vb_s2_sweep             M12 (delta_vb wrong only for s^2 < 0.1)
  dr_far_s2               M12, M20 (Delta r_bos wrong only for M_W/M_Z > 0.95); absolute floor at the zero of Delta r_bos
  dense_higgs_mass        M11 (wrong only for 2e3 < M_H < 4e3 GeV), M11b (only for 2e10 < M_H < 8e12 GeV)
  split_consistency       pins delta_vb = Delta r_bos - [Sigma part with -2(c/s) Sigma_AZ(0)], with the provided bos_se;
                          kills M09, M10, M18 (also killed by the oracle; included because it uses no reference)  BLIND-OK*
                          (*it uses the provided module and the Denner grouping, i.e. it pins the SPEC 4 resolution)
Both blind builds pass all of them. M04b (sign of the Sigma_AZ(0) term flipped while assembling at mu = M_W, where
Sigma_AZ(0) = 0 in MS-bar) is an equivalent mutant: no export-level check can see it.
"""
import importlib.util, math, os

MW, MZ, MH, ALPHA = 80.38, 91.19, 125.0, 1 / 128.0
_R = None


def _ref():
    global _R
    if _R is None:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reference_denner.py")
        s = importlib.util.spec_from_file_location("bos_dr_reference_audit", p)
        _R = importlib.util.module_from_spec(s)
        s.loader.exec_module(_R)
    return _R


def _vb_closed(mw, mz, al):
    s2 = 1 - (mw / mz) ** 2
    return al / (4 * math.pi * s2) * (6 + (7 - 4 * s2) / (2 * s2) * math.log(1 - s2))


def _dev(v, r, floor):
    try:
        v = float(v)
    except Exception:
        return float("inf")
    if not math.isfinite(v):
        return float("inf")
    return abs(v - r) / max(abs(r), floor)


# ------------------------------------------------------------------------------------------------ reference-free (BLIND-OK)
def alpha_linear_wide(m):
    """Both exports are exactly first order in alpha (SPEC 3): f(alpha)/alpha is the same for alpha = 1/300, the Thomson value
    1/137.035999, 1/128 and 1/60 (the blind check only compares 1/128 with 2/128)."""
    als = (1 / 300.0, 1 / 137.035999, 1 / 128.0, 1 / 60.0)
    worst = 0.0
    for f in (lambda a: m.delta_r_bos(MW, MZ, MH, a), lambda a: m.delta_vb(MW, MZ, a)):
        r = [f(a) / a for a in als]
        worst = max(worst, max(abs(x / r[2] - 1) for x in r))
    return worst < 1e-9, f"f(alpha)/alpha over alpha in [1/300, 1/60]: worst spread {worst:.1e}"


def split_consistency(m):
    """Delta r_bos - delta_vb must equal the self-energy part of the Denner grouping (SPEC photon sign),
    Sigma'_AA(0) - 2(c/s) Sigma_AZ(0)/M_Z^2 - (c^2/s^2)[Sigma_ZZ(M_Z^2)/M_Z^2 - Sigma_W(M_W^2)/M_W^2] + [Sigma_W(0) - Sigma_W(M_W^2)]/M_W^2,
    evaluated here from the provided bos_se at two scales mu (it is mu independent). Uses no reference."""
    import bos_se
    worst = 0.0
    for (mw, mz, mh, al) in ((MW, MZ, MH, ALPHA), (75.0, 91.19, 300.0, 1 / 137.035999)):
        c2 = (mw / mz) ** 2; s2 = 1 - c2; s, c = math.sqrt(s2), math.sqrt(c2)
        target = m.delta_r_bos(mw, mz, mh, al) - m.delta_vb(mw, mz, al)
        for mu in (mw, 300.0):
            f = lambda h: bos_se.sigma_AA(h, mw, mz, mh, al, mu) / h
            h = 1e-2 * mw ** 2
            a = [f(h / 2 ** k) for k in range(5)]
            for j in range(1, 5):
                a = [(2 ** j * a[i + 1] - a[i]) / (2 ** j - 1) for i in range(len(a) - 1)]
            sw = lambda k2: bos_se.sigma_W(k2, mw, mz, mh, al, mu)
            sig = (a[0] - 2 * (c / s) * bos_se.sigma_AZ(0, mw, mz, mh, al, mu) / mz ** 2
                   - (c2 / s2) * (bos_se.sigma_ZZ(mz ** 2, mw, mz, mh, al, mu) / mz ** 2 - sw(mw ** 2) / mw ** 2)
                   + (sw(0) - sw(mw ** 2)) / mw ** 2)
            worst = max(worst, _dev(target, sig, al / (4 * math.pi)))
    return worst < 1e-9, f"Delta r_bos - delta_vb against the Sigma part from bos_se (two points, two mu): worst {worst:.1e}"


# ------------------------------------------------------------------------------------------------ against reference / closed form
def thomson_alpha_reference(m):
    """At the physical alpha(0) = 1/137.035999 (the SPEC's alpha is the Thomson-limit one; the oracle uses 1/125 .. 1/132)."""
    al = 1 / 137.035999
    d1 = _dev(m.delta_r_bos(MW, MZ, MH, al), _ref().dr_bos(MW, MZ, MH, al), al / (4 * math.pi))
    d2 = _dev(m.delta_vb(MW, MZ, al), _vb_closed(MW, MZ, al), al / (4 * math.pi))
    return max(d1, d2) < 1e-9, f"alpha = 1/137.036: Delta r_bos {d1:.1e}, delta_vb {d2:.1e}"


def vb_s2_sweep(m):
    """delta_vb against the closed form for M_W/M_Z from 0.1 to 0.995 (s^2 from 0.99 to 0.01); the oracle samples s^2 in [0.13, 0.51]."""
    worst, where = 0.0, None
    for r in (0.1, 0.3, 0.5, 0.7, 0.85, 0.93, 0.96, 0.98, 0.995):
        for mz in (91.19, 250.0):
            dv = _dev(m.delta_vb(r * mz, mz, ALPHA), _vb_closed(r * mz, mz, ALPHA), ALPHA / (4 * math.pi))
            if dv > worst:
                worst, where = dv, r
    return worst < 1e-9, f"delta_vb over M_W/M_Z in [0.1, 0.995]: worst {worst:.1e} at M_W/M_Z = {where}"


def dr_far_s2(m):
    """Delta r_bos against the reference far from the SM s^2, including M_W/M_Z ~ 0.97 where Delta r_bos changes sign: an absolute
    floor alpha/(4 pi) replaces the pure relative test there."""
    worst, where = 0.0, None
    for mw in (30.0, 88.6, 89.5, 90.5):
        d = _dev(m.delta_r_bos(mw, 91.19, MH, ALPHA), _ref().dr_bos(mw, 91.19, MH, ALPHA), ALPHA / (4 * math.pi))
        if d > worst:
            worst, where = d, mw
    return worst < 1e-9, f"Delta r_bos at M_W = 30 .. 90.5 GeV (M_Z = 91.19): worst {worst:.1e} at M_W = {where}"


def dense_higgs_mass(m):
    """M_H between the oracle's scan points (1, 20, 91.19, 400, 5e3, 1e5, 1e7, 1e10, 1e13 GeV)."""
    worst, where = 0.0, None
    for mh in (2.5e3, 3.5e3, 3e4, 3e6, 3e8, 5e10, 1e12):
        d = _dev(m.delta_r_bos(MW, MZ, mh, ALPHA), _ref().dr_bos(MW, MZ, mh, ALPHA), ALPHA / (4 * math.pi))
        if d > worst:
            worst, where = d, mh
    return worst < 1e-9, f"Delta r_bos at 7 M_H between the oracle scan points: worst {worst:.1e} at M_H = {where}"


CHECKS = [("exports exactly linear in alpha over [1/300, 1/60] (BLIND-OK)", alpha_linear_wide),
          ("Delta r_bos - delta_vb = Sigma part (Denner grouping) from bos_se (BLIND-OK*)", split_consistency),
          ("both exports at the Thomson alpha against the reference", thomson_alpha_reference),
          ("delta_vb over s^2 in [0.01, 0.99]", vb_s2_sweep),
          ("Delta r_bos far from the SM s^2 (absolute floor at its zero)", dr_far_s2),
          ("Delta r_bos at M_H between the oracle scan points", dense_higgs_mass)]


if __name__ == "__main__":
    import sys
    d = os.path.abspath(sys.argv[1])
    sys.path.insert(0, d)
    s = importlib.util.spec_from_file_location("bos_dr", os.path.join(d, "bos_dr.py"))
    mod = importlib.util.module_from_spec(s)
    s.loader.exec_module(mod)
    only = sys.argv[2:]
    for lab, fn in CHECKS:
        if only and fn.__name__ not in only:
            continue
        ok, msg = fn(mod)
        print(f"[{'PASS' if ok else 'FAIL'}] {lab}: {msg}", flush=True)
