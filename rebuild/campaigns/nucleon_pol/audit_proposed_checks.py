"""Red-team proposed checks for the nucleon_pol campaign (see AUDIT.md).  Each takes the build module m and returns (ok, msg).

They close the gaps the surviving mutants of AUDIT.md section 3 went through:
  * the oracle samples gA in [0.5, 2] (positive only), f in [60, 130], m_pi in [50, 500], alpha in [1/150, 1/100]
                                                     -> audit_wide_grid (against the auditor's Compton-route coefficients)
  * reference-free structure: alpha_E, beta_M are even in gA, exactly homogeneous of degree -3 in (f, m_pi) jointly and
    -1 in m_pi alone over many decades (chiral limit), exactly linear in alpha (zero at alpha = 0), beta/alpha constant
                                                     -> audit_homogeneity
  * to_fm3 is only probed at positive x             -> audit_to_fm3_linear
  * a typed-in closed form passes lint (LINT_EXACT folds only pure-constant subtrees) -> audit_no_closed_form_literals
AUDIT values: the omega^2 coefficients of the auditor's real-photon Compton amplitude (radiation gauge, KR + pion-pole +
seagull + double-insertion diagrams, Feynman parameters, residue p0 integral, n = 3 - 2 eps; scratchpad compton.py/compton.log):
  T_perp = e^2 (10 + cos th) w^2 /(96 pi m),  T_par = e^2 (1 + 10 cos th) w^2 /(96 pi m)  (per 2 (gA/2f)^2)
  => alpha_E = (5/96 pi) alpha gA^2/(f^2 m),  beta_M = (1/192 pi) alpha gA^2/(f^2 m).
Usage: python3 audit_proposed_checks.py <build dir>
"""
import ast, importlib.util, math, os, sys

HBARC = 197.3269804
AUD_A = 5 / 96          # alpha_E * pi f^2 m / (alpha gA^2)   (Compton route)
AUD_B = 1 / 192         # beta_M  * pi f^2 m / (alpha gA^2)


def aud(gA, f, mp, al):
    s = al * gA * gA / (math.pi * f * f * mp)
    return AUD_A * s, AUD_B * s


def _rel(v, r):
    try:
        v = float(v)
    except Exception:
        return float("inf")
    return abs(v / r - 1) if math.isfinite(v) and r else float("inf")


def audit_wide_grid(m):
    """alpha_E, beta_M on 4 x 4 x 5 x 3 = 240 points, gA = -1.27 ... 3, f = 10 ... 5000 MeV, m_pi = 0.1 MeV ... 10 GeV,
    alpha = 1e-6 ... 0.5, against the auditor's values; relative 1e-10."""
    worst, where = 0.0, None
    for gA in (-1.27, 0.1, 1.27, 3.0):
        for f in (10.0, 92.4, 500.0, 5000.0):
            for mp in (0.1, 10.0, 139.57, 1000.0, 1e4):
                for al in (1e-6, 1 / 137.035999, 0.5):
                    ra, rb = aud(gA, f, mp, al)
                    d = max(_rel(m.alpha_E(gA, f, mp, al), ra), _rel(m.beta_M(gA, f, mp, al), rb))
                    if d > worst:
                        worst, where = d, (gA, f, mp, al)
    return worst < 1e-10, f"240 points: worst relative {worst:.1e} at (gA, f, m_pi, alpha) = {where}"


def audit_homogeneity(m):
    """Reference-free: even in gA; alpha_E(gA, l f, l m, a) = l^-3 alpha_E; alpha_E ~ 1/m_pi for m_pi = 1e-3 ... 1e5 MeV;
    linear in alpha with alpha_E(alpha = 0) = 0; beta_M/alpha_E the same number everywhere."""
    p = (1.27, 92.4, 139.57, 1 / 137.035999)
    a0, b0 = m.alpha_E(*p), m.beta_M(*p)
    r0 = b0 / a0
    worst = 0.0
    for gA in (-2.0, -1.27, 0.3, 4.0):
        worst = max(worst, _rel(m.alpha_E(gA, *p[1:]), a0 * gA**2 / p[0]**2), _rel(m.beta_M(-gA, *p[1:]), m.beta_M(gA, *p[1:])))
    for lam in (1e-4, 0.01, 3.0, 1e3, 1e5):
        worst = max(worst, _rel(m.alpha_E(p[0], lam * p[1], lam * p[2], p[3]), a0 / lam**3), _rel(m.beta_M(p[0], lam * p[1], lam * p[2], p[3]), b0 / lam**3))
    for mp in (1e-3, 0.5, 20.0, 700.0, 1e5):
        worst = max(worst, _rel(m.alpha_E(p[0], p[1], mp, p[3]), a0 * p[2] / mp), _rel(m.beta_M(p[0], p[1], mp, p[3]) / m.alpha_E(p[0], p[1], mp, p[3]), r0))
    for f in (1.0, 30.0, 300.0, 1e4):
        worst = max(worst, _rel(m.alpha_E(p[0], f, p[2], p[3]), a0 * p[1]**2 / f**2), _rel(m.beta_M(p[0], f, p[2], p[3]) / m.alpha_E(p[0], f, p[2], p[3]), r0))
    for al in (1e-9, 0.02, 0.3, 1.0):
        worst = max(worst, _rel(m.alpha_E(p[0], p[1], p[2], al), a0 * al / p[3]), _rel(m.beta_M(p[0], p[1], p[2], al), b0 * al / p[3]))
    zero = m.alpha_E(p[0], p[1], p[2], 0.0) == 0 and m.beta_M(p[0], p[1], p[2], 0.0) == 0
    return worst < 1e-12 and zero, f"worst relative deviation from exact gA^2 f^-2 m^-1 alpha scaling: {worst:.1e}; zero at alpha = 0: {zero}"


def audit_to_fm3_linear(m):
    """to_fm3(x) = x (hbar c)^3 for negative, zero, tiny and huge x."""
    worst = 0.0
    for x in (-3.5e-10, -1.0, 1e-300, 2.0, 7.3e40):
        worst = max(worst, _rel(m.to_fm3(x), x * HBARC**3))
    return worst < 1e-14 and m.to_fm3(0.0) == 0, f"worst relative {worst:.1e}; to_fm3(0) = {m.to_fm3(0.0)}"


def audit_no_closed_form_literals(m):
    """Heuristic lint: the target's denominators 96, 192, 384, 768 (and 5/96, 1/192 as floats) must not be typed in
    the module source. The oracle's LINT_EXACT only catches constant subtrees such as 5/(96*pi), not
    5*alpha*gA**2/(96*math.pi*f**2*m)."""
    src = open(m.__file__).read()
    bad = []
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            v = float(node.value)
            if v in (96.0, 192.0, 384.0, 768.0) or any(v and abs(v / t - 1) < 1e-9 for t in (5 / 96, 1 / 192, 5 / 384, 1 / 768, 0.1)):
                bad.append(f"line {node.lineno}: {node.value!r}")
    return not bad, "no target denominators typed in" if not bad else "; ".join(bad)


CHECKS = [("alpha_E, beta_M on a wide (gA, f, m_pi, alpha) grid (auditor's Compton route)", audit_wide_grid),
          ("exact gA^2 / (f^2 m_pi) x alpha homogeneity, evenness, chiral-limit 1/m_pi (reference-free)", audit_homogeneity),
          ("to_fm3 is exactly x (hbar c)^3", audit_to_fm3_linear),
          ("no typed-in closed-form denominators (heuristic lint)", audit_no_closed_form_literals)]

if __name__ == "__main__":
    sys.dont_write_bytecode = True
    d = os.path.abspath(sys.argv[1])
    s = importlib.util.spec_from_file_location("nucleon_pol", os.path.join(d, "nucleon_pol.py"))
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
