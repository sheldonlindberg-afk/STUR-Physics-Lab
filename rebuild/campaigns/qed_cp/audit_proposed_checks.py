"""Auditor's proposed extra checks (blind ones B*, oracle ones O*). Run: python3 proposed_checks.py <dir with qed_cp.py> ..."""
import sys, math, importlib.util, random
sys.dont_write_bytecode = True
import mpmath as mp


def ref(rho):
    """Fixed oracle reference (the shipped oracle.reference loses accuracy for r w0 > ~30: 4e-5 at 50, 9% at 1e3)."""
    mp.mp.dps = 30
    r = mp.mpf(rho)
    f = lambda s: (1 / (1 + (s / r) ** 2)) ** 2 * 2 * mp.exp(-2 * s) * (3 + 6 * s + 5 * s**2 + 2 * s**3 + s**4)
    return float(-mp.quad(f, [0, 1, 5, 20, 60, mp.inf]) / (2 * mp.pi) / r**7)


def B_far_approach(m):
    """blind: U r^7 / C -> 1 with a 1/rho^2 deficit (analytic in 1/rho^2); no target value used."""
    C = m.far_coefficient()
    d = [1 + m.cp_energy(x, 1.0, 1.0) * x**7 / C for x in (100.0, 200.0)]
    ok = d[0] > 0 and d[1] > 0 and abs(d[0] / d[1] - 4) < 0.1
    return ok, f"far deficits {d[0]:.3e}, {d[1]:.3e}, ratio {d[0] / d[1] if d[1] else float('inf'):.3f} (expected 4)"


def B_near_approach(m):
    """blind: U r^6 / (D w0) -> 1 with a rho^2 deficit (no odd power: the integrand is analytic at rho = 0 to O(rho^2))."""
    D = m.near_coefficient()
    d = [1 + m.cp_energy(x, 1.0, 1.0) * x**6 / D for x in (0.01, 0.02)]
    ok = d[0] > 0 and d[1] > 0 and abs(d[1] / d[0] - 4) < 0.1
    return ok, f"near deficits {d[0]:.3e}, {d[1]:.3e}, ratio {d[1] / d[0] if d[0] else float('inf'):.3f} (expected 4)"


def B_alpha_everywhere(m):
    """blind: U / alpha0^2 independent of alpha0 at w0 != 1 too (kills dependence on alpha0 w0^3)."""
    base = m.cp_energy(5.1, 0.37, 1.0)
    rs = [m.cp_energy(5.1, 0.37, a) / a**2 / base for a in (0.1, 2.0, 7.0)]
    return all(abs(x - 1) < 1e-9 for x in rs), f"ratios {rs}"


def O_dense(m, n=12, seed=None):
    """oracle: random log-uniform r w0 in [1e-2, 1e3] at w0 != 1, tolerance 1e-6 (builds reach ~1e-12)."""
    rnd = random.Random(seed)
    worst = 0.0
    for _ in range(n):
        rho = 10 ** rnd.uniform(-2, 3)
        w0, al = 10 ** rnd.uniform(-1, 1), 10 ** rnd.uniform(-1, 1)
        v = m.cp_energy(rho / w0, w0, al)
        rv = ref(rho) * al**2 * w0**7
        worst = max(worst, abs(v / rv - 1))
    return worst < 1e-6, f"worst relative deviation {worst:.2e}"


def O_coeff_tight(m):
    C, D = m.far_coefficient(), m.near_coefficient()
    tc, td = ref(1e7) * -1e49, -ref(1e-4) * 1e-24 / (1 - 1e-8 / 3)
    return abs(C / tc - 1) < 1e-8 and abs(D / td - 1) < 1e-8, f"C rel {C / tc - 1:.1e}, D rel {D / td - 1:.1e}"


CHECKS = [("B_far_approach", B_far_approach), ("B_near_approach", B_near_approach), ("B_alpha_everywhere", B_alpha_everywhere),
          ("O_dense(seed=7)", lambda m: O_dense(m, seed=7)), ("O_coeff_tight", O_coeff_tight)]

if __name__ == "__main__":
    import warnings; warnings.filterwarnings("ignore")
    for d in sys.argv[1:]:
        spec = importlib.util.spec_from_file_location("qed_cp_" + str(abs(hash(d))), d + "/qed_cp.py")
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        print("####", d.rstrip('/').split('/')[-1])
        for name, fn in CHECKS:
            try: ok, det = fn(m)
            except Exception as e: ok, det = False, repr(e)
            print(f"   [{'PASS' if ok else 'FAIL'}] {name}: {det}")
