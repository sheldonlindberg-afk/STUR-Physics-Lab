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
LINT_TARGETS = [v for v in TARGET.values()] + [UNIT, 16.0 * 3.14159]


def mk(s):
    def f(m):
        v = m.power_per_dof(s)
        return abs(v / TARGET[s] - 1) < TOL[s], f"derived {v:.4e}, target {TARGET[s]:.4e} ({100 * (v / TARGET[s] - 1):+.2f}%, tolerance {100 * TOL[s]:.1f}%)"
    return f


ORACLE = [(f"power per degree of freedom, spin {s}", mk(s)) for s in (0, 0.5, 1, 2)]
ORACLE.append(("weights ratio to the scalar: 0.551 (1/2), 0.225 (1), 0.026 (2)",
               lambda m: (lambda p: (abs(p[1] / p[0] - 0.147 / 0.267) < 0.02 and abs(p[2] / p[0] - 0.060 / 0.267) < 0.02, ", ".join(f"{x / p[0]:.3f}" for x in p)))([m.power_per_dof(s) for s in (0, 0.5, 1, 2)])))
ORACLE.append(("grey-body factor at fixed arguments: Gamma(0,0,0.2) = 0.9089 +- 1e-3, Gamma(1,1,0.2) = 0.1299 +- 1e-3 (orchestrator's integration)",
               lambda m: (abs(m.transmission(0, 0, 0.2) - 0.9089) < 1e-3 and abs(m.transmission(1, 1, 0.2) - 0.1299) < 1e-3, f"{m.transmission(0, 0, 0.2):.4f}, {m.transmission(1, 1, 0.2):.4f}")))
