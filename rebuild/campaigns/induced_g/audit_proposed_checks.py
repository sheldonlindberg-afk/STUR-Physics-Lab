"""Red-team proposed checks for the induced_g campaign (see AUDIT.md). Each takes the build module m and returns (ok, msg).

They close the gaps the surviving mutants of AUDIT.md section 4 went through:
  * the oracle checks k1 only for d = 2..10 and xi in {0, 0.25, -0.4} (scalar only)    -> audit_k1_wide
  * k1(kind, d, xi) for a non-scalar kind is only ever called with xi = 0              -> audit_xi_only_in_scalar
  * k1('weyl', odd d) is never called (SPEC: even d only)                             -> audit_weyl_odd_d_rejected
  * the only oracle point with xi < 0 has n_s = 0, so a clamp or |xi| in inv_G passes -> audit_inv_G_wide
  * mpl is never probed at 1/G = 0 exactly                                            -> audit_mpl_boundary
  * independent anchor: the kappa^2 a term of the zero-point energy on R x S^3 from the canonical mode content
    (transverse photons only, Dirac sea), the auditor's route of AUDIT.md section 1    -> audit_einstein_universe_route
  * heuristic: inv_G must be built from k1 (a typed-in closed form is not derived)    -> audit_inv_G_uses_k1
AUDIT reference values (AUDIT.md section 1): k1 = tr(E) / R + tr(1)/6 per kind: scalar 1/6 - xi; Dirac -2^floor(d/2)/12;
Weyl half of it; vector_no_ghosts (d - 6)/6; vector (d - 8)/6.  1/G = (kappa^2/2pi)[n_s (1/6 - xi) + n_w/6 - 2 n_v/3].
Usage: python3 audit_proposed_checks.py <build dir>
"""
import ast, importlib.util, inspect, math, os, sys


def ref_k1(kind, d, xi=0.0):
    if kind == "scalar":
        return 1 / 6 - xi
    if kind == "dirac":
        return -(2 ** (d // 2)) / 12
    if kind == "weyl":
        return -(2 ** (d // 2)) / 24
    if kind == "vector_no_ghosts":
        return (d - 6) / 6
    if kind == "vector":
        return (d - 8) / 6
    raise KeyError(kind)


def ref_inv_G(kappa, n_s, n_w, n_v, xi=0.0):
    return kappa ** 2 / (2 * math.pi) * (n_s * (1 / 6 - xi) + n_w / 6 - 2 * n_v / 3)


def _dev(v, r):
    try:
        v = float(v)
    except Exception:
        return float("inf")
    return abs(v - r) / max(1.0, abs(r)) if math.isfinite(v) else float("inf")


XIS = (-1e3, -10.0, -1.0, -0.4, -1 / 12, 0.0, 1 / 6, 0.25, 0.75, 1.0, 10.0, 1e3)


def audit_k1_wide(m):
    """k1 for every kind at d = 1..26 (Weyl at even d), the scalar at 12 values of xi from -1e3 to 1e3; 1e-12."""
    worst, where = 0.0, None
    for d in range(1, 27):
        for kind in ("scalar", "dirac", "vector", "vector_no_ghosts") + (("weyl",) if d % 2 == 0 else ()):
            for xi in (XIS if kind == "scalar" else (0.0,)):
                e = _dev(m.k1(kind, d, xi), ref_k1(kind, d, xi))
                if e > worst:
                    worst, where = e, (kind, d, xi)
    return worst < 1e-12, f"worst {worst:.1e}" + (f" at (kind, d, xi) = {where}" if where else "")


def audit_xi_only_in_scalar(m):
    """xi is the scalar's curvature coupling only: k1 of dirac, weyl, vector (ghosts are -nabla^2) and vector_no_ghosts
    must not depend on it."""
    bad = []
    for d in range(2, 13):
        for kind in ("dirac", "vector", "vector_no_ghosts") + (("weyl",) if d % 2 == 0 else ()):
            base = m.k1(kind, d, 0.0)
            for xi in XIS:
                if _dev(m.k1(kind, d, xi), base) > 1e-14:
                    bad.append((kind, d, xi))
    return not bad, "no xi dependence outside the scalar" if not bad else f"{len(bad)} cases, first {bad[:3]}"


def audit_weyl_odd_d_rejected(m):
    """SPEC: Weyl only in even d. k1('weyl', odd d) must raise (or return None / nan), not a number."""
    bad = []
    for d in (1, 3, 5, 7, 9, 11):
        try:
            v = m.k1("weyl", d)
        except Exception:
            continue
        if v is not None and not (isinstance(v, float) and math.isnan(v)):
            bad.append((d, v))
    return not bad, "rejected at every odd d" if not bad else f"returns values at odd d: {bad[:3]}"


def audit_inv_G_wide(m):
    """1/G on 6 x 5 x 4 x 4 x 12 = 5760 points, kappa = 1e-3 ... 1e19, counts 0 ... 1000 (fractional too), xi = -1e3 ... 1e3
    (negative xi with n_s > 0), relative to the largest single-species term, 1e-12; plus exact linearity in xi and in each
    count (reference-free)."""
    worst, where = 0.0, None
    for kappa in (1e-3, 0.37, 1.0, 7.5, 2.4e18, 1e19):
        for n_s in (0, 1, 4, 18, 1000):
            for n_w in (0, 1, 45, 69):
                for n_v in (0, 1, 12, 17):
                    for xi in XIS:
                        r = ref_inv_G(kappa, n_s, n_w, n_v, xi)
                        scale = kappa ** 2 / (2 * math.pi) * (n_s * (1 / 6 + abs(xi)) + n_w / 6 + 2 * n_v / 3) or 1.0
                        try:
                            e = abs(float(m.inv_G(kappa, n_s, n_w, n_v, xi)) - r) / scale
                        except Exception:
                            e = float("inf")
                        if not math.isfinite(e) or e > worst:
                            worst, where = (e if math.isfinite(e) else float("inf")), (kappa, n_s, n_w, n_v, xi)
    lin = 0.0
    for xi in (-3.0, -0.5, 0.2, 2.0):
        g = [m.inv_G(1.0, 7, 3, 2, xi + h) for h in (0.0, 0.5, 1.0)]
        lin = max(lin, abs(g[0] - 2 * g[1] + g[2]) / max(abs(g[1]), 1.0))
    for n in (2.5, 11.0):
        for args in ((n, 0, 0, -0.7), (0, n, 0, -0.7), (0, 0, n, -0.7)):
            one = m.inv_G(1.0, *[1 if a == n else a for a in args[:3]], args[3])
            lin = max(lin, abs(m.inv_G(1.0, *args) - n * one) / max(abs(n * one), 1e-300))
    ok = worst < 1e-12 and lin < 1e-12
    return ok, f"worst relative {worst:.1e}" + (f" at {where}" if worst > 1e-12 else "") + f"; linearity defect {lin:.1e}"


def audit_mpl_boundary(m):
    """mpl is None at 1/G = 0 exactly (no fields; conformal scalars only), None for 1/G < 0, sqrt(1/G) for 1/G > 0,
    including negative xi with scalars."""
    bad = []
    for p in ((1.0, 0, 0, 0, 0.0), (3.0, 5, 0, 0, 1 / 6), (2.0, 0, 0, 0, -0.3)):
        if m.mpl(*p) is not None:
            bad.append(("zero", p, m.mpl(*p)))
    for p in ((1.0, 1, 0, 0, 0.5), (1.0, 0, 0, 1, 0.0), (1.0, 18, 66, 17, 1 / 6), (1e19, 3, 0, 0, 10.0)):
        if m.mpl(*p) is not None:
            bad.append(("negative", p, m.mpl(*p)))
    for p in ((1.0, 1, 0, 0, -0.3), (5.3e19, 18, 69, 17, -1.0), (0.01, 0, 1, 0, 0.0), (2.0, 10, 0, 1, -2.0)):
        v, r = m.mpl(*p), math.sqrt(ref_inv_G(*p))
        if v is None or abs(v / r - 1) > 1e-12:
            bad.append(("positive", p, v))
    return not bad, "None at zero and negative 1/G, sqrt elsewhere" if not bad else f"{bad[:3]}"


# ------------------------------------------------------------------ the auditor's independent route (AUDIT.md section 1)
def _f_boson(w, k):
    """SPEC proper-time cutoff after the exact S^1 trace: -(1/2)(4 pi)^(-1/2) int_{1/k^2}^inf dt t^(-3/2) e^(-t w^2)."""
    if w == 0:
        return -k / (2 * math.sqrt(math.pi))
    x = (w / k) ** 2
    return -w / (2 * math.sqrt(math.pi)) * (math.exp(-x) / math.sqrt(x) - math.sqrt(math.pi) * math.erfc(math.sqrt(x)))


def _E0(field, k, xi=0.0, N=1500):
    """Zero-point energy on R x S^3 of radius 1 from the canonical (Hamiltonian) mode content."""
    if field == "scalar":                 # w^2 = l(l + 2) + 6 xi, deg (l + 1)^2
        return sum((l + 1) ** 2 * _f_boson(math.sqrt(l * (l + 2) + 6 * xi), k) for l in range(N))
    if field == "weyl":                   # w = n + 3/2, 2 (n + 1)(n + 2) modes, Dirac sea: -w/2 each
        return -sum(2 * (n + 1) * (n + 2) * _f_boson(n + 1.5, k) for n in range(N))
    if field == "photon":                 # Coulomb gauge: transverse only, w = n + 1, deg 2 n (n + 2)
        return sum(2 * n * (n + 2) * _f_boson(n + 1.0, k) for n in range(1, N))


def _kappa2_coefficient(field, xi=0.0):
    import numpy as np
    ks = [10 + 0.5 * i for i in range(25)]
    A = np.array([[k ** 4, k ** 2, k, math.log(k), 1.0, k ** -2, k ** -4] for k in ks])
    return float(np.linalg.lstsq(A, np.array([_E0(field, k, xi) for k in ks]), rcond=None)[0][1])


def audit_einstein_universe_route(m):
    """W = beta E0 on S^1_beta x S^3_a (beta -> inf); S_grav = -(3 pi/4) beta a / G, so 1/G = -(4/(3 pi)) [kappa^2 a term
    of E0] per kappa^2. Per species: a scalar at xi = 0 and xi = 0.4, one Weyl fermion, one Maxwell field (transverse
    photons, no ghosts). Agreement 1e-7 relative."""
    rows, worst = [], 0.0
    for label, field, xi, args in (("scalar xi=0", "scalar", 0.0, (1, 0, 0, 0.0)), ("scalar xi=0.4", "scalar", 0.4, (1, 0, 0, 0.4)),
                                   ("Weyl", "weyl", 0.0, (0, 1, 0, 0.0)), ("vector", "photon", 0.0, (0, 0, 1, 0.0))):
        route = -(4 / (3 * math.pi)) * _kappa2_coefficient(field, xi)
        got = m.inv_G(1.0, *args)
        e = abs(got / route - 1)
        worst = max(worst, e)
        rows.append(f"{label} {got:+.6f} vs {route:+.6f}")
    return worst < 1e-7, f"worst {worst:.1e}: " + "; ".join(rows)


def audit_inv_G_uses_k1(m):
    """Heuristic: inv_G's body calls k1 (1/G is the statistics-weighted sum of the k1's; a closed form typed into inv_G is
    not derived). Evadable; the transcript audit remains the guard."""
    try:
        tree = ast.parse(inspect.getsource(m.inv_G))
    except Exception as e:
        return False, f"no source: {e}"
    calls = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    return "k1" in calls, "inv_G calls k1" if "k1" in calls else "inv_G does not call k1"


CHECKS = [("k1 for every kind at d = 1..26 and xi = -1e3..1e3 (auditor's tr(E + R/6))", audit_k1_wide),
          ("xi enters only the scalar k1", audit_xi_only_in_scalar),
          ("k1('weyl', odd d) is rejected", audit_weyl_odd_d_rejected),
          ("1/G on a wide grid, negative xi with scalars, exact linearity", audit_inv_G_wide),
          ("mpl at 1/G = 0, < 0, > 0", audit_mpl_boundary),
          ("1/G per species against the Einstein-static-universe zero-point route", audit_einstein_universe_route),
          ("inv_G is built from k1 (heuristic)", audit_inv_G_uses_k1)]

if __name__ == "__main__":
    sys.dont_write_bytecode = True
    d = os.path.abspath(sys.argv[1])
    s = importlib.util.spec_from_file_location("induced_g", os.path.join(d, "induced_g.py"))
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
