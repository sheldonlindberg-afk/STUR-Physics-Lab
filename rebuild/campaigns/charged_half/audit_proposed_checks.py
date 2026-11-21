"""Red-team proposed checks for the charged_half campaign (see AUDIT.md).  Each takes the build module m and returns (ok, msg).

They close the gaps the mutants in AUDIT.md section 4 went through:
  * Gamma only checked for g in [-0.12, 0.12], j <= 3.5 and w <= 0.8 (+ g = 0 points)   -> audit_gamma_wide
  * only four of the nine rules checked, and the distribution only for the principal rule -> audit_all_rules, audit_mixed_rule_balance
  * rates() never checked against the build's own transmission() (rates could integrate a different Gamma) -> audit_rates_self_consistent
  * the small-alpha structure of the chain never checked for the mixed rules -> audit_small_alpha_structure
The Gamma table comes from the auditor's own solver (Coulomb-Whittaker matching, Frobenius horizon start,
.../scratchpad/audit-charged_half/indep_solver.py); its accuracy is about 1e-7 or better and it agrees with build a to <= 3e-8.
Usage: python3 audit_proposed_checks.py <build dir>
"""
import importlib.util, math, os, sys

ALPHA = 1 / 137.035999084
_here = os.path.dirname(os.path.abspath(__file__))

# (j, w, g) -> Gamma from the auditor's independent solver (35 points: w below and above g/2, j to 9.5, |g| to 0.6)
AUDIT_GAMMA = [
    ((0.5, 0.01, -0.12), 0.00023633087829847974),
    ((0.5, 0.2, -0.12), 0.8418171145698683),
    ((1.5, 0.45, -0.12), 0.9693574691685793),
    ((4.5, 1.2, -0.12), 0.9998608489931509),
    ((0.5, 0.03, -0.06), 0.0018121228924419031),
    ((2.5, 0.6, -0.06), 0.8060848841200096),
    ((3.5, 0.9, -0.06), 0.9922090553891174),
    ((0.5, 0.1, -0.02), 0.04889827580405622),
    ((1.5, 0.3, -0.02), 0.0685418341016129),
    ((4.5, 1.4, -0.02), 0.9999990345422785),
    ((0.5, 0.25, 0.0), 0.8733869116027976),
    ((2.5, 0.5, 0.0), 0.07280022959033262),
    ((4.5, 1.0, 0.0), 0.7766794378434693),
    ((0.5, 0.005, 0.03), 2.3655255517959645e-05),
    ((0.5, 0.012, 0.03), 0.00014119980667009875),
    ((1.5, 0.2, 0.03), 0.0009845708224845357),
    ((3.5, 0.75, 0.03), 0.27899042544181735),
    ((0.5, 0.02, 0.08), 0.0003610394791265099),
    ((0.5, 0.06, 0.08), 0.004265628142706492),
    ((2.5, 0.03, 0.08), 1.911034465660703e-13),
    ((2.5, 0.45, 0.08), 0.005855171539179155),
    ((4.5, 1.1, 0.08), 0.9723581151411955),
    ((0.5, 0.001, 0.12), 9.520940853376653e-07),
    ((0.5, 0.05, 0.12), 0.002325503397053683),
    ((1.5, 0.04, 0.12), 6.410790667007622e-08),
    ((1.5, 0.35, 0.12), 0.08311941302064875),
    ((3.5, 0.05, 0.12), 5.216681348475848e-17),
    ((4.5, 1.3, 0.12), 0.9999077005268064),
    ((0.5, 0.1, 0.3), 0.007948754124013017),
    ((1.5, 0.4, -0.3), 0.9789181111059847),
    ((0.5, 0.2, 0.6), 0.029140289983737473),
    ((2.5, 0.8, -0.6), 0.9999988730923601),
    ((5.5, 1.5, 0.0), 0.9999816228261804),
    ((6.5, 1.7, 0.05), 0.9999758277448138),
    ((9.5, 2.4, -0.05), 0.9999998375969488),
]

_ref = None


def _R():
    global _ref
    if _ref is None:
        s = importlib.util.spec_from_file_location("charged_half_reference_chain", os.path.join(_here, "reference_chain.py"))
        _ref = importlib.util.module_from_spec(s)
        s.loader.exec_module(_ref)
    return _ref


_SHIFT = {"before": 0.0, "mid": 0.5, "after": 1.0}
RULES = [(a, b) for a in ("before", "mid", "after") for b in ("before", "mid", "after")]


def _couplings(alpha, rule, q, n):
    """SPEC section 3, written out independently: g = alpha q n_rule, n_before = n, n_mid = n - q/2, n_after = n - q."""
    nb = {"before": n, "mid": n - q / 2, "after": n - q}
    return alpha * q * nb[rule[0]], alpha * q * nb[rule[1]]


def audit_gamma_wide(m):
    """Gamma against the auditor's independent solver, incl. j = 4.5 .. 9.5, |g| = 0.3, 0.6 and w < g/2; relative 1e-6."""
    worst, where = 0.0, None
    for (j, w, g), v in AUDIT_GAMMA:
        x = m.transmission(j, w, g)
        d = abs(x / v - 1)
        if d > worst:
            worst, where = d, (j, w, g)
    return worst < 1e-6, f"Gamma at {len(AUDIT_GAMMA)} auditor points: worst {worst:.1e} at {where}"


def audit_rates_self_consistent(m):
    """rates() recomputed from the build's own transmission() by Gauss-Legendre quadrature (k <= 7, w <= 2.4), incl. |g| up to 0.3."""
    import numpy as np
    T = 1 / (8 * math.pi)
    xg, wg = np.polynomial.legendre.leggauss(24)
    br = (0.0, 0.06, 0.2, 0.45, 0.8, 1.3, 2.4)
    om, wt = [], []
    for a, b in zip(br[:-1], br[1:]):
        om += list(0.5 * (b - a) * xg + 0.5 * (a + b)); wt += list(0.5 * (b - a) * wg)
    worst, where = 0.0, None
    for gg, gm in ((0.1, 0.1), (0.3, 0.3), (-0.15, 0.15), (0.12, -0.2)):
        N = P = 0.0
        for w, c in zip(om, wt):
            nf = 1 / (math.exp((w - gm / 2) / T) + 1)
            G = sum((2 * k) * m.transmission(k - 0.5, w, gg) for k in range(1, 8))
            N += c * G * nf / (2 * math.pi); P += c * w * G * nf / (2 * math.pi)
        Nm, Pm = m.rates(gg, gm)
        d = max(abs(Nm / N - 1), abs(Pm / P - 1))
        if d > worst:
            worst, where = d, (gg, gm)
    return worst < 1e-6, f"rates() against quadrature of the build's own transmission(): worst {worst:.1e} at {where}"


def audit_all_rules(m):
    """Weight and energy ratios for all nine rules against the orchestrator's reference chain (tolerance 3e-4, as the oracle)."""
    R = _R()
    worst, where, bad = 0.0, None, []
    for rule in RULES:
        wr, er, _ = R.weight_ratio(ALPHA, rule)
        w, e = m.weight_ratio(ALPHA, rule), m.energy_ratio(ALPHA, rule)
        d = max(abs(w - wr), abs(e - er))
        if d > worst:
            worst, where = d, rule
        if d >= 3e-4:
            bad.append(rule)
    return worst < 3e-4, f"nine rules: worst |d ratio| {worst:.1e} at {where}; failing {bad}"


def audit_mixed_rule_balance(m):
    """Detailed balance pi(n+1)/pi(n) = up(n)/down(n+1) from the exported rates, for the mixed rules (after, mid) and (before, after),
    with the couplings written out from SPEC section 3, and <n^2> against the reference."""
    R = _R()
    worst, wn2, msg = 0.0, 0.0, []
    for rule in (("after", "mid"), ("before", "after"), ("mid", "before")):
        pi = m.charge_distribution(ALPHA, rule)
        for n in range(-6, 7):
            up = m.rates(*_couplings(ALPHA, rule, -1, n))[0]
            dn = m.rates(*_couplings(ALPHA, rule, +1, n + 1))[0]
            worst = max(worst, abs(pi[n + 1] / pi[n] / (up / dn) - 1))
        pir = R.chain(ALPHA, rule)[0]
        n2, n2r = sum(n * n * v for n, v in pi.items()), sum(n * n * v for n, v in pir.items())
        msg.append(f"{rule}: <n^2> {n2:.3f} (ref {n2r:.3f})")
        wn2 = max(wn2, abs(n2 / n2r - 1))
    return worst < 1e-6 and wn2 < 2e-3, f"mixed-rule detailed balance from rates(): worst {worst:.1e}; <n^2> worst {wn2:.1e}; " + "; ".join(msg)


def audit_small_alpha_structure(m):
    """(ratio - 1)/alpha at alpha/8 against the first-order expansion built from rates() derivatives (AUDIT.md section 3):
    c = P_dd/(4 L P0) - (s_gb P_gb + s_mu P_mu)/P0, s = 0, 1/2, 1 for before, mid, after; L = d ln N(g, g)/dg. Tolerance 0.15 on c."""
    h = 2e-3
    N0, P0 = m.rates(0.0, 0.0)
    P = lambda a, b: m.rates(a, b)[1]
    N = lambda a, b: m.rates(a, b)[0]
    P_gb = (P(h, 0) - P(-h, 0)) / (2 * h); P_mu = (P(0, h) - P(0, -h)) / (2 * h)
    P_dd = (P(h, h) - 2 * P0 + P(-h, -h)) / h ** 2
    L = (math.log(N(h, h)) - math.log(N(-h, -h))) / (2 * h)
    worst, where = 0.0, None
    a = ALPHA / 8
    for rule in RULES:
        c = P_dd / (4 * L * P0) - (_SHIFT[rule[0]] * P_gb + _SHIFT[rule[1]] * P_mu) / P0
        d = abs((m.weight_ratio(a, rule) - 1) / a - c)
        if d > worst:
            worst, where = d, rule
    return worst < 0.15, f"small-alpha slope of the weight ratio vs the expansion from rates(): worst {worst:.3f} at {where}"


CHECKS = [("Gamma beyond the oracle's range (auditor solver)", audit_gamma_wide),
          ("rates() consistent with the build's own transmission()", audit_rates_self_consistent),
          ("all nine rules against the reference", audit_all_rules),
          ("detailed balance and <n^2> for mixed rules", audit_mixed_rule_balance),
          ("small-alpha structure of every rule", audit_small_alpha_structure)]

if __name__ == "__main__":
    sys.dont_write_bytecode = True
    d = os.path.abspath(sys.argv[1])
    s = importlib.util.spec_from_file_location("charged_half", os.path.join(d, "charged_half.py"))
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
