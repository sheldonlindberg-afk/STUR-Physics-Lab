"""
Standalone real-physics LambdaCDM backward integrator.

Purpose: start from TODAY's measured dark-matter + dark-energy (+ baryon +
radiation) content and integrate the standard Friedmann equation BACKWARD in
cosmic time, with H0 left as a free dial (the Planck vs SH0ES tension is
real and unresolved, so it is not hardcoded). No STUR-specific content, no
inflaton potential, no new physics -- this is the honest GR+LambdaCDM
baseline: what does standard cosmology alone say about the early universe
and about whether backward integration "reveals" a beginning?

Physical (H0-independent) density parameters, fixed from real measurements
(Planck 2018 TT,TE,EE+lowE+lensing, Planck VI 2020 / Planck X 2018; N_eff
standard value 3.046):
    Omega_b h^2 = 0.02237   (baryons)
    Omega_c h^2 = 0.1200    (cold dark matter)
    Omega_r h^2 = 4.16e-5   (photons + 3 neutrino species, N_eff=3.046)
Flat universe assumed (Omega_k = 0) -- this is an assumption, not derived,
and is flagged everywhere it matters.

H0 is the free dial: Omega_m(h) = (Omega_b h^2 + Omega_c h^2)/h^2,
Omega_r(h) = (Omega_r h^2)/h^2, Omega_Lambda(h) = 1 - Omega_m(h) - Omega_r(h).

All derived quantities (age, equality epochs, acceleration onset) are
computed numerically from these, not quoted from memory.
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# ---- Fixed physical density parameters (independent of the H0 dial) ----
OMEGA_B_H2 = 0.02237
OMEGA_C_H2 = 0.1200
OMEGA_M_H2 = OMEGA_B_H2 + OMEGA_C_H2          # 0.14237
OMEGA_R_H2 = 4.16e-5                          # N_eff = 3.046

GYR_PER_INV_H0_UNIT = 977.792   # 1/(100 km/s/Mpc) in Gyr, i.e. Gyr = GYR_PER_INV_H0_UNIT / H0[km/s/Mpc/100]


def h_of_H0(H0_kmsMpc):
    return H0_kmsMpc / 100.0


def omegas(H0_kmsMpc):
    """Return (Omega_m, Omega_r, Omega_Lambda) for this H0, flat universe."""
    h = h_of_H0(H0_kmsMpc)
    Om = OMEGA_M_H2 / h**2
    Or = OMEGA_R_H2 / h**2
    OL = 1.0 - Om - Or
    return Om, Or, OL


def E2(a, Om, Or, OL):
    """ (H(a)/H0)^2 , flat FRW, matter+radiation+Lambda. """
    return Or * a**-4 + Om * a**-3 + OL


def H_of_a_Gyr(a, H0_kmsMpc, Om, Or, OL):
    """H(a) in Gyr^-1."""
    H0_Gyr = H0_kmsMpc / GYR_PER_INV_H0_UNIT
    return H0_Gyr * np.sqrt(E2(a, Om, Or, OL))


def age_integral(a_target, H0_kmsMpc, Om, Or, OL):
    """ t(a_target) - t(0) in Gyr, i.e. cosmic time elapsed from the a->0
    singularity to scale factor a_target. Converges because near a->0 the
    integrand ~ a/(H0*sqrt(Omega_r)) -> 0 (radiation-domination limit). """
    H0_Gyr = H0_kmsMpc / GYR_PER_INV_H0_UNIT

    def integrand(a):
        return 1.0 / (a * H0_Gyr * np.sqrt(E2(a, Om, Or, OL)))

    val, err = quad(integrand, 0.0, a_target, limit=200)
    return val


def q_of_a(a, Om, Or, OL):
    """Deceleration parameter, derived from first principles:
       q(a) = [Omega_m a^-3 + 2 Omega_r a^-4 - 2 Omega_Lambda] / (2 E^2(a))
    (derived here, not quoted, from q = -1 - a H'/H with H^2=H0^2 E^2(a);
    cross-checked numerically below against a finite-difference H'(a).)
    """
    num = Om * a**-3 + 2 * Or * a**-4 - 2 * OL
    return num / (2 * E2(a, Om, Or, OL))


def q_of_a_numeric(a, Om, Or, OL, da=1e-6):
    """Finite-difference cross-check of q(a) directly from H(a)."""
    def Hfun(x):
        return np.sqrt(E2(x, Om, Or, OL))
    H = Hfun(a)
    Hp = (Hfun(a + da) - Hfun(a - da)) / (2 * da)
    return -1.0 - a * Hp / H


def matter_radiation_equality(Om, Or):
    a_eq = Or / Om
    return a_eq, 1.0 / a_eq - 1.0


def matter_lambda_equality(Om, OL):
    a_eq = (Om / OL) ** (1.0 / 3.0)
    return a_eq, 1.0 / a_eq - 1.0


def acceleration_onset(Om, Or, OL):
    """a where q(a) crosses zero, found by bisection on the real q(a),
    not the radiation-negligible shortcut formula."""
    lo, hi = 1e-3, 1.5
    f = lambda a: q_of_a(a, Om, Or, OL)
    if f(lo) * f(hi) > 0:
        return None
    a_star = brentq(f, lo, hi, xtol=1e-12)
    return a_star, 1.0 / a_star - 1.0


def report(H0_kmsMpc, label):
    Om, Or, OL = omegas(H0_kmsMpc)
    t0 = age_integral(1.0, H0_kmsMpc, Om, Or, OL)
    a_eq_mr, z_eq_mr = matter_radiation_equality(Om, Or)
    a_eq_ml, z_eq_ml = matter_lambda_equality(Om, OL)
    a_acc, z_acc = acceleration_onset(Om, Or, OL)
    t_acc = age_integral(a_acc, H0_kmsMpc, Om, Or, OL)
    t_eq_mr = age_integral(a_eq_mr, H0_kmsMpc, Om, Or, OL)

    # q(a) analytic vs numeric cross-check at a few points
    qa_checks = []
    for a in [a_eq_mr, 0.3, a_acc, 1.0]:
        qa_checks.append((a, q_of_a(a, Om, Or, OL), q_of_a_numeric(a, Om, Or, OL)))

    print(f"\n=== H0 = {H0_kmsMpc:.2f} km/s/Mpc  ({label}) ===")
    print(f"  Omega_m = {Om:.5f}   Omega_r = {Or:.3e}   Omega_Lambda = {OL:.5f}")
    print(f"  Age of universe (a=0 -> a=1):            t0       = {t0:.4f} Gyr")
    print(f"  Matter-radiation equality:                z_eq_mr  = {z_eq_mr:9.2f}   t = {t_eq_mr*1e6:.2f} kyr")
    print(f"  Matter-Lambda equality (energy density):  z_eq_mL  = {z_eq_ml:9.4f}   a = {a_eq_ml:.4f}")
    print(f"  Acceleration onset (q=0):                 z_acc    = {z_acc:9.4f}   t = {t_acc:.4f} Gyr  (a={a_acc:.4f})")
    print("  q(a) analytic vs finite-difference numeric cross-check:")
    for a, qan, qnum in qa_checks:
        print(f"    a={a:9.5f}  q_analytic={qan:+.6f}  q_numeric={qnum:+.6f}  diff={qan-qnum:+.2e}")
    return dict(H0=H0_kmsMpc, Om=Om, Or=Or, OL=OL, t0=t0, z_eq_mr=z_eq_mr,
                z_eq_ml=z_eq_ml, a_eq_ml=a_eq_ml, z_acc=z_acc, t_acc=t_acc)


if __name__ == "__main__":
    print("Fixed physical density parameters (H0-independent, Planck 2018 + N_eff=3.046):")
    print(f"  Omega_b h^2 = {OMEGA_B_H2}")
    print(f"  Omega_c h^2 = {OMEGA_C_H2}")
    print(f"  Omega_m h^2 = {OMEGA_M_H2}")
    print(f"  Omega_r h^2 = {OMEGA_R_H2}")
    print("  Flat universe assumed: Omega_k = 0 (assumption, not derived)")

    results = []
    for H0, label in [
        (67.36, "Planck 2018 CMB"),
        (68.6, "2025 Cepheid reanalysis, Freedman et al.-style reconciliation"),
        (73.04, "SH0ES 2022 local distance ladder (Riess et al., arXiv:2112.04510)"),
    ]:
        results.append(report(H0, label))

    print("\n=== H0 scan: age of universe vs H0 (the actual free-dial sweep) ===")
    print(f"{'H0':>8} {'Omega_m':>9} {'t0 [Gyr]':>10}")
    scan = []
    for H0 in np.linspace(60, 80, 21):
        Om, Or, OL = omegas(H0)
        t0 = age_integral(1.0, H0, Om, Or, OL)
        scan.append((H0, Om, t0))
        print(f"{H0:8.2f} {Om:9.5f} {t0:10.4f}")

    print("\n=== Independent (H0-free) age-of-universe constraint ===")
    print("  Oldest globular clusters (Valcin, Jimenez, Verde, Bernal & Wandelt 2021,")
    print("  arXiv:2102.04486): t_U = 13.5 (+0.16/-0.14 stat) +/- 0.23(0.33 sys) Gyr")
    t_gc_central, t_gc_lo2sig = 13.5, 13.5 - 2 * np.sqrt(0.16**2 + 0.33**2)
    print(f"  -> conservative ~2-sigma lower bound used here: {t_gc_lo2sig:.2f} Gyr")
    for H0, Om, t0 in scan:
        tag = "OK" if t0 >= t_gc_lo2sig else "TENSION (universe younger than oldest clusters)"
        if H0 in (65.0, 67.0, 69.0, 71.0, 73.0, 75.0) or abs(t0 - t_gc_lo2sig) < 0.05:
            print(f"    H0={H0:5.1f}: t0={t0:.3f} Gyr  -> {tag}")
