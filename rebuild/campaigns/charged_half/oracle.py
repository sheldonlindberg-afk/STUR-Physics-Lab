# CANARY-2f6c9a47e1b05d83-charged_half: planted so a builder transcript that contains this string has read the oracle
"""Hidden oracle for the charged_half campaign.

Target: Page (PRD 16, 2402 (1977)) and MacGibbon (PRD 44, 376 (1991)), quoted by Carr, Kohri, Sendouda, Yokoyama (arXiv:2002.12778, eqs. 12-13): the charge-+-e spin-1/2
weight 0.142 against 0.147 for a neutral one, and mean emitted energies 4.18 and 4.22 T. The orchestrator's own reference (reference_solver.py: an amplitude-variable solver of the
radial system, validated at g = 0 against the accepted greybody references to 2e-7; reference_chain.py: grey-body grid, quadrature and the birth-death chain) gives, for the model
with every charge taken after the emission, weight ratio 0.9634 (f = 0.1416) and energy ratio 0.9960, and other charge-assignment rules give ratios from 0.93 to 1.05: the O(alpha)
effect depends on the assignment, which is the same order as the self-energy corrections Page ignored. The oracle checks the builds against the reference, not against the
literature numbers (the literature ratio 0.142 lies within the quoted digits for the principal rule (after, after) and also for (before, mid); the audit showed the thermodynamically consistent rule (after, mid) gives ~1.008)."""
import importlib.util, json, math, os

_here = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("charged_half_reference", os.path.join(_here, "reference_chain.py"))
R = importlib.util.module_from_spec(_s)
_s.loader.exec_module(R)
REF_GAMMA = json.load(open(os.path.join(_here, "reference_gamma.json")))
GREY = json.load(open(os.path.join(_here, "..", "greybody", "reference.json")))["gamma"]

ALPHA = 1 / 137.035999084
LINT_TARGETS = [0.96345, 0.9634, 0.99595, 0.1416, 4.0916e-5, 2.4284e-4, 11.81]
LINT_EXACT = []


def gamma_g0(m):
    worst = 0.0
    for (s, j, w), v in GREY:
        if s != 0.5:
            continue
        worst = max(worst, abs(m.transmission(j, w, 0.0) / v - 1))
    return worst < 1e-6, f"g = 0 against the accepted greybody fermion references (10 points): worst {worst:.1e}"


def gamma_charged(m):
    worst, where = 0.0, None
    for (j, w, g), v in REF_GAMMA:
        d = abs(m.transmission(j, w, g) / v - 1)
        if d > worst:
            worst, where = d, (j, w, g)
    return worst < 2e-6, f"Gamma at {len(REF_GAMMA)} reference (j, w, g) (g = -0.12..0.12, w below and above g/2): worst relative deviation {worst:.1e} at {where}"


def rates_check(m):
    worst, where = 0.0, None
    for gg, gm in ((0.0, 0.0), (0.0073, 0.0073), (-0.0073, -0.0073), (-0.0073, 0.0), (0.0, 0.05), (0.05, -0.03), (-0.08, 0.08), (0.1, 0.1)):
        Nr, Pr = R.rates(gg, gm)
        N, P = m.rates(gg, gm)
        d = max(abs(N / Nr - 1), abs(P / Pr - 1))
        if d > worst:
            worst, where = d, (gg, gm)
    return worst < 3e-5, f"rates(g_gb, g_mu) against the reference on eight couplings: worst {worst:.1e} at {where}"


def ratio_check(rule, al_f):
    def f(m):
        a = al_f * ALPHA
        wr, er, pi = R.weight_ratio(a, rule)
        w, e = m.weight_ratio(a, rule), m.energy_ratio(a, rule)
        ok = abs(w - wr) < 3e-4 and abs(e - er) < 3e-4
        return ok, f"rule {rule}, alpha x {al_f}: weight ratio {w:.5f} (reference {wr:.5f}), energy ratio {e:.5f} (reference {er:.5f})"
    return f


def distribution_check(m):
    wr, er, pi = R.weight_ratio(ALPHA)
    d = m.charge_distribution(ALPHA)
    worst = max(abs(d.get(n, 0.0) - pi[n]) for n in range(-30, 31))
    n2 = sum(n * n * v for n, v in d.items())
    n2r = sum(n * n * v for n, v in pi.items())
    return worst < 5e-5 and abs(n2 / n2r - 1) < 2e-3, f"stationary distribution against the reference: max |d pi| = {worst:.1e}; <n^2> {n2:.3f} (reference {n2r:.3f})"


ORACLE = [("g = 0 reproduces the accepted greybody fermion references", gamma_g0),
          ("Gamma_j(w; g) against the reference solver, 46 points, g = -0.12 .. 0.12", gamma_charged),
          ("rates(g_gb, g_mu) against the reference", rates_check),
          ("weight and energy ratios, principal rule (after, after), alpha", ratio_check(("after", "after"), 1.0)),
          ("weight and energy ratios, principal rule, alpha/2 and 2 alpha", lambda m: (ratio_check(("after", "after"), 0.5)(m)[0] and ratio_check(("after", "after"), 2.0)(m)[0], "principal rule at alpha/2 and 2 alpha")),
          ("weight and energy ratios, rule (before, before)", ratio_check(("before", "before"), 1.0)),
          ("weight and energy ratios, rules (after, mid) and (mid, mid)", lambda m: (ratio_check(("after", "mid"), 1.0)(m)[0] and ratio_check(("mid", "mid"), 1.0)(m)[0], "rules (after, mid) and (mid, mid)")),
          ("stationary charge distribution", distribution_check)]


# Checks adopted from the Opus audit (AUDIT.md): seven wrong mutants had survived the first gate.
import importlib.util as _iu, os as _os
_pa = _iu.spec_from_file_location("charged_half_audit_checks", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "audit_proposed_checks.py"))
AC = _iu.module_from_spec(_pa)
_pa.loader.exec_module(AC)
ORACLE = ORACLE + list(AC.CHECKS)
