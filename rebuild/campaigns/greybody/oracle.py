"""Hidden oracle for the grey-body campaign. Targets: Carr et al., Rept. Prog. Phys. 84, 116902 (2021), eqs. (11)-(13)
(weights 0.267, 0.147, 0.060, 0.007 per degree of freedom with dM/dt = -5.34e25 f/M^2 g^3/s, after MacGibbon-Webber)
converted with hbar c^4/G^2; and Page, PRD 13, 198 (1976) (photon 3.37e-5, graviton 3.84e-6 for two helicities).
The orchestrator's own quick integration (scratchpad) gave 7.41e-5, 4.09e-5, 1.68e-5, 1.92e-6."""
G, HBAR, C = 6.67430e-11, 1.054571817e-34, 2.99792458e8
UNIT = 5.34e25 / (HBAR * C**4 / G**2 * 1e9 * 1e3 / 1e3)       # 5.34e25 g^3/s over hbar c^4/G^2 in g^3/s (1 kg^3 = 1e9 g^3)
WEIGHTS = {0: 0.267, 0.5: 0.147, 1: 0.060, 2: 0.007}
TOL = {0: 0.015, 0.5: 0.015, 1: 0.02, 2: 0.06}
TARGET = {s: WEIGHTS[s] * UNIT for s in WEIGHTS}
TARGET[2] = 3.84e-6 / 2                                         # Page 1976, per helicity
# Two-route values (accepted builds a and the auditor's independent WKB-projection solver agree to < 1e-7): the sharp targets.
PRECISE = {0: 7.43868693871e-5, 0.5: 4.09165271219e-5, 1: 1.68192739347e-5, 2: 1.91836996439e-6}
LINT_TARGETS = [v for v in TARGET.values()] + list(PRECISE.values()) + [UNIT, 16.0 * 3.14159]
LINT_EXACT = [PRECISE[0], PRECISE[2]]


def mk(s):
    def f(m):
        v = m.power_per_dof(s)
        return abs(v / TARGET[s] - 1) < TOL[s], f"derived {v:.4e}, target {TARGET[s]:.4e} ({100 * (v / TARGET[s] - 1):+.2f}%, tolerance {100 * TOL[s]:.1f}%)"
    return f


ORACLE = [(f"power per degree of freedom, spin {s} (literature, loose)", mk(s)) for s in (0, 0.5, 1, 2)]
ORACLE.append(("grey-body factor at fixed arguments: Gamma(0,0,0.2) = 0.9089 +- 1e-3, Gamma(1,1,0.2) = 0.1299 +- 1e-3 (orchestrator's integration)",
               lambda m: (abs(m.transmission(0, 0, 0.2) - 0.9089) < 1e-3 and abs(m.transmission(1, 1, 0.2) - 0.1299) < 1e-3, f"{m.transmission(0, 0, 0.2):.4f}, {m.transmission(1, 1, 0.2):.4f}")))


import json as _json, os as _os
_REF = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "reference.json")))


def power_precise(m):
    out, ok = [], True
    for s, p in PRECISE.items():
        d = m.power_per_dof(s) / p - 1
        out.append(f"s={s}: {d:+.1e}")
        ok &= abs(d) < 1e-5
    return ok, "relative to the two-route value: " + ", ".join(out)


def gamma_dense(m):
    worst, where = 0.0, None
    pts = [(tuple(k), v) for k, v in _REF["gamma"]] + [(tuple(k), v) for k, v in _REF["gamma_lowfreq_fermion"]]
    for (s, j, w), g in pts:
        d = abs(m.transmission(s, j, w) / g - 1)
        if d > worst:
            worst, where = d, (s, j, w)
    return worst < 1e-6, f"worst relative deviation over {len(pts)} reference points: {worst:.1e} at (s, j, w) = {where}"


ORACLE += [("power per degree of freedom to 1e-5 against the two-route values", power_precise),
           ("grey-body factor at 46 reference points, including low-frequency fermions (independent WKB-projection solver) to 1e-6", gamma_dense)]
