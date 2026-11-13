#!/usr/bin/env python3
"""
The electromagnetic rung of the ladder (SYMMETRY_LADDER.md): why electromagnetism is the
background in the diamond experiment, and its strength, derived.

U(1)_em is never broken, so the photon stays massless and electromagnetism is long-range.
Between two neutral, unpolarized diamonds what remains is the Casimir-Polder force, from
correlated zero-point fluctuations of the field and the induced dipoles. It is derived here
from classical electrostatics, the dipole field and one quantum step (the fluctuation sum
over imaginary frequencies, Casimir and Polder 1948).

  P1  Polarizability of a dielectric sphere (radius R, permittivity eps) in a uniform field,
      from Laplace's equation with the boundary conditions at r = R:
      alpha / (4 pi eps0) = K R^3, K = (eps - 1)/(eps + 2). (CHECK, symbolic)
  P2  The dipole field Green tensor at imaginary frequency xi (u = xi r / c):
      G_ij = e^{-u} / r^3 [(1 + u + u^2) delta_ij - (3 + 3u + u^2) rhat_i rhat_j],
      checked to satisfy the Helmholtz equation (nabla^2 - xi^2/c^2) away from the source;
      Tr G.G = 2 e^{-2u} (3 + 6u + 5u^2 + 2u^3 + u^4) / r^6. (CHECK, symbolic)
  P3  The interaction of two polarizable particles, U = -(hbar / 2 pi) int_0^oo dxi
      alpha1 alpha2 Tr G.G (Gaussian units for alpha = K R^3). For constant alpha (the
      retarded regime, r much larger than the wavelengths where alpha varies):
      int_0^oo e^{-2u}(3 + 6u + 5u^2 + 2u^3 + u^4) du = 23/4, so
      U = -(23 hbar c / 4 pi) alpha1 alpha2 / r^7. (CHECK, exact)
  P4  This is the formula used in src/stur_gravity_entanglement.py (then quoted as KNOWN), and
      at the design gap Casimir's entangling phase against gravity's: the gap that src/
      stur_gravity_full.py chose, 181 um, is where Casimir is 10% of gravity. (CHECK)
  P5  Finite temperature (Lifshitz; LIT: the Matsubara form of P3). In equilibrium at T the
      frequency integral becomes a sum over xi_n = 2 pi n k_B T / hbar, with the n = 0 term
      halved: (hbar/2pi) int dxi -> k_B T sum'_n. With constant alpha,
          U_T(r) = U_0(r) eta(tau),  tau = 2 pi k_B T r / (hbar c),
          eta = (2/23) tau sum'_n f(n tau),  f(u) = 2 e^(-2u)(3 + 6u + 5u^2 + 2u^3 + u^4).
      The sum is done in closed form (sums of n^k q^n, q = e^(-2 tau)). eta -> 1 as tau -> 0,
      and the first correction is at tau^6: eta = 1 + (22/21735) tau^6 + O(tau^8), because
      f's odd derivatives vanish at 0 up to the fifth (Euler-Maclaurin). As tau -> oo,
      eta -> 6 tau/23: U_T -> -3 k_B T alpha1 alpha2 / r^6, the classical (n = 0) limit.
      Constant alpha holds at every Matsubara frequency here: diamond is non-polar (no
      one-phonon infrared absorption) and its electronic gap is at ~1e16 rad/s, while xi_1 is
      below 1e14 rad/s up to 77 K. (CHECK, exact)
  P6  The Casimir-safe gap at finite temperature, the field in equilibrium with the walls at
      T_env (src/stur_gravity_full.py: 0.15 K). At 0.15 K, tau < 0.13 at every branch
      distance and the gap moves by 1e-11: the T = 0 formula is exact for the design. It still
      holds at 4.2 K (a helium bath: +0.2%, even with tau = 3.6 at the far branch, since the
      entangling phase is dominated by the nearest branches); only near 77 K does the gap
      grow (+6% at 10 K, 1.7x to 0.31 mm at 77 K). So at the design's temperature finite
      temperature does not tighten the gap. Computed
      for the branch separation the gap was set with (250 um, stur_gravity_entanglement BASE)
      and for design A's (721 um), where the gap is smaller: 181 um is conservative for
      design A. (CHECK)
  P7  Patch potentials (MODEL). A random surface potential of rms V over uncorrelated
      patches of size l on a sphere of radius R (l << R) has an l = 1 (dipole) component of
      rms p = sqrt(12 pi) eps0 R l V per axis: the potential outside of the surface pattern
      V_1 cos(theta) is V_1 R^2 cos(theta) / r^2, so p = 4 pi eps0 R^2 V_1, and V_1 sums
      area-weighted cos(theta) over ~4 pi R^2 / l^2 patches. Against H6's bound on a permanent
      dipole at design A (src/stur_gravity_full.py max_dipole), the product V l must stay
      below 8.3e-13 V m: for 0.1 um patches that is 8 uV rms, three orders of magnitude below
      the tens of mV measured on metal films (LIT: Garcia-Sanchez et al., PRL 109, 100801
      (2012)); diamond's own surface values depend on its termination and are not known here.
      At 10 mV and 0.1 um, no practical gap helps: the unshielded gap would be ~0.3 m. The
      conclusion of H6 stands, now quantified: the experiment needs a conducting shield
      between the diamonds; patch control alone would have to reach the microvolt level.
      (CHECK, given the model)
Labels: CHECK, LIT (eps of diamond, 5.7; the Matsubara form; patch measurements), MODEL (P7).
"""
import math
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def sphere_polarizability():
    """P1: potential inside A r cos(th), outside -E0 r cos(th) + B cos(th)/r^2; continuity of
    the potential and of eps * d(phi)/dr at r = R. Dipole moment p = 4 pi eps0 B."""
    A, B = sp.symbols("A B", real=True)
    R, E0, eps = sp.symbols("R E0 epsilon", positive=True)
    r = sp.Symbol("r", positive=True)
    phin = A * r
    phout = -E0 * r + B / r**2
    sol = sp.solve([sp.Eq(phin.subs(r, R), phout.subs(r, R)),
                    sp.Eq(eps * sp.diff(phin, r).subs(r, R), sp.diff(phout, r).subs(r, R))], [A, B])
    alpha_over_4pieps0 = sp.simplify(sol[B] / E0)
    return alpha_over_4pieps0, sp.simplify(alpha_over_4pieps0 - (eps - 1) / (eps + 2) * R**3)


def green_tensor():
    """P2: the Green tensor, the Helmholtz check and Tr G.G."""
    x, y, z, k = sp.symbols("x y z k", positive=True)                  # k = xi / c
    X = [x, y, z]
    r = sp.sqrt(x**2 + y**2 + z**2)
    u = k * r
    G = sp.Matrix(3, 3, lambda i, j: sp.exp(-u) / r**3 * ((1 + u + u**2) * (1 if i == j else 0)
                                                          - (3 + 3 * u + u**2) * X[i] * X[j] / r**2))
    # Helmholtz: each component of the field of a fixed dipole p_j solves (lap - k^2) E = 0 off the source
    lapm = lambda f: sum(sp.diff(f, v, 2) for v in X) - k**2 * f
    pt = {x: sp.Rational(3, 7), y: sp.Rational(-2, 5), z: sp.Rational(5, 11), k: sp.Rational(4, 3)}
    helm = max(abs(sp.N(lapm(G[i, j]).subs(pt), 30)) for i in range(3) for j in range(3))
    # divergence-free (transverse) off the source, like a radiation field
    div = max(abs(sp.N(sum(sp.diff(G[i, j], X[i]) for i in range(3)).subs(pt), 30)) for j in range(3))
    tr = sp.simplify((G * G).trace())
    uu, rr = sp.symbols("u r", positive=True)
    target = 2 * sp.exp(-2 * uu) * (3 + 6 * uu + 5 * uu**2 + 2 * uu**3 + uu**4) / rr**6
    trcheck = sp.simplify(tr.subs({x: rr, y: 0, z: 0}).subs(k, uu / rr) - target)
    return helm, div, trcheck


def frequency_integral():
    """P3: the integral, exactly."""
    u = sp.Symbol("u", positive=True)
    return sp.integrate(sp.exp(-2 * u) * (3 + 6 * u + 5 * u**2 + 2 * u**3 + u**4), (u, 0, sp.oo))


def casimir_coefficient():
    """U = -(hbar/2pi) int dxi a1 a2 Tr G.G = -(hbar/2pi)(c/r) a1 a2 (2/r^6) * I, I = 23/4."""
    I = frequency_integral()
    return sp.Rational(1, 2) / sp.pi * 2 * I                            # U = -coef hbar c a1 a2 / r^7


def compare_with_experiment_code():
    import stur_gravity_entanglement as GE
    import stur_gravity_full as GF
    m, r = GF.design_a()["m"], 200e-6                                   # design A's mass
    R = GE.radius(m)
    K = (GE.EPS_DIAMOND - 1) / (GE.EPS_DIAMOND + 2)
    coef = float(casimir_coefficient())
    mine = -coef * GE.HBAR * GE.C * (K * R**3) ** 2 / r**7
    theirs = GE.casimir_energy(m, r)
    grav = -GE.G * m * m / r
    return mine, theirs, grav, R


# ---------------------------------------------------------------------- P5: finite T
def matsubara_eta():
    """P5: eta(tau) = (2/23) tau sum'_n f(n tau), in closed form, with its series at small tau
    and its large-tau limit."""
    tau = sp.Symbol("tau", positive=True)
    q = sp.exp(-2 * tau)
    u = sp.Symbol("u")
    f = sp.expand(2 * (3 + 6 * u + 5 * u**2 + 2 * u**3 + u**4))       # f = e^(-2u) * this
    x = sp.Symbol("x")
    S = [x / (1 - x)]                                                 # sum_{n>=1} n^k x^n
    for _ in range(4):
        S.append(sp.simplify(x * sp.diff(S[-1], x)))
    poly = sp.Poly(f, u)
    total = f.subs(u, 0) / 2 + sum(c * tau**k * S[k].subs(x, q) for (k,), c in poly.terms())
    eta = sp.Rational(2, 23) * tau * total
    series = sp.series(eta, tau, 0, 7).removeO()
    limit_hi = sp.limit(eta / tau, tau, sp.oo)
    return eta, tau, sp.nsimplify(sp.expand(series)), limit_hi


_ETA = None


def eta(tau):
    """Numerical eta(tau) from the closed form (vectorized); 1 at tau = 0."""
    global _ETA
    if _ETA is None:
        e, t, _, _ = matsubara_eta()
        _ETA = sp.lambdify(t, e, "numpy")
    import numpy as np
    tau = np.asarray(tau, dtype=float)
    small = tau < 0.2                         # the series: closed form loses digits to cancellation
    out = np.where(small, 1 + 22 / 21735 * tau**6, _ETA(np.where(small, 1.0, tau)))
    return out


def eta_direct(tau, nmax=200000):
    """eta from the Matsubara sum term by term (for checking the closed form)."""
    import numpy as np
    n = np.arange(1, nmax + 1)
    fu = lambda v: 2 * np.exp(-2 * v) * (3 + 6 * v + 5 * v**2 + 2 * v**3 + v**4)
    return 2 / 23 * tau * (3.0 + fu(n * tau).sum())


def tau_of(r, T):
    import stur_gravity_entanglement as GE
    return 2 * math.pi * GE.KB * T * r / (GE.HBAR * GE.C)


def casimir_energy_T(m, r, T):
    """U_T(r) = U_0(r) eta(tau(r)): retarded Casimir-Polder in equilibrium at temperature T."""
    import stur_gravity_entanglement as GE
    return GE.casimir_energy(m, r) * (eta(tau_of(r, T)) if T > 0 else 1.0)


def safe_gap_T(T, dx, frac=0.1):
    """P6: the gap (parallel geometry) where the thermal Casimir entangling phase is `frac` of
    gravity's. Mass- and time-independent, as at T = 0."""
    import numpy as np
    from scipy.optimize import brentq
    import stur_gravity_entanglement as GE
    m, tau = GE.BASE["m"], GE.BASE["tau"]

    def excess(lg):
        gap = math.exp(lg)
        r = GE.branch_distances(dx, gap, "parallel")
        cas = abs(GE.entangling_phase(-casimir_energy_T(m, r, T) * tau / GE.HBAR))
        grv = abs(GE.entangling_phase(GE.phases(m, dx, gap, tau, "parallel")))
        return math.log(cas / (frac * grv))
    return math.exp(brentq(excess, math.log(1e-6), math.log(1e-2), xtol=1e-10))


T_ENV = 0.15                     # K, src/stur_gravity_full.py BASE_ENV (dilution refrigerator)
TEMPS = (0.0, 0.15, 1.0, 4.2, 10.0, 77.0)


def thermal_gaps():
    import stur_gravity_entanglement as GE
    import stur_gravity_full as GF
    dxA = GF.design_a()["dx"]
    return {T: (safe_gap_T(T, GE.BASE["dx"]), safe_gap_T(T, dxA)) for T in TEMPS}, GE.BASE["dx"], dxA


# ---------------------------------------------------------------------- P7: patch potentials
EPS0 = 8.8541878128e-12
PATCH_V_METAL = 0.01             # V rms: the low end of tens of mV on metal films (LIT, Garcia-Sanchez 2012)
PATCH_SIZES = (0.03e-6, 0.1e-6, 0.3e-6)    # l << R = 1 um


def patch_dipole(R, l, V):
    """P7: rms dipole (per axis) of random patches of rms V and size l on a sphere of radius R."""
    return math.sqrt(12 * math.pi) * EPS0 * R * l * V


def patch_dipole_mc(R, l, V, trials=400, seed=1):
    """The same by Monte Carlo: equal-area cells of size ~l, independent potentials of rms V,
    p_z = 4 pi eps0 R^2 V_1 with V_1 = (3 / 4 pi) sum V_cell cos(theta) dOmega."""
    import numpy as np
    rng = np.random.default_rng(seed)
    N = int(round(4 * math.pi * R**2 / l**2))
    k = np.arange(N) + 0.5                                         # Fibonacci sphere: equal areas
    ct = 1 - 2 * k / N
    dOm = 4 * math.pi / N
    V1 = (3 / (4 * math.pi)) * (rng.normal(0, V, (trials, N)) * ct * dOm).sum(axis=1)
    return float(np.sqrt(np.mean((4 * math.pi * EPS0 * R**2 * V1) ** 2)))


def patch_budget():
    import stur_gravity_full as GF
    from scipy.optimize import brentq
    A = GF.design_a()
    pmax = GF.max_dipole(A["m"], A["dx"], A["gap"], A["total"])
    Vl_max = pmax / (math.sqrt(12 * math.pi) * EPS0 * A["R"])
    rows = []
    for l in PATCH_SIZES:
        p = patch_dipole(A["R"], l, PATCH_V_METAL)
        f = lambda lg: math.log(GF.em_entangling_ratio(A["m"], A["dx"], math.exp(lg), A["total"], p=p) / 0.1)
        gap_needed = math.exp(brentq(f, math.log(1e-5), math.log(1e2)))
        rows.append((l, Vl_max / l, p, p / pmax, gap_needed))
    return A, pmax, Vl_max, rows


def main():
    banner("P1  Polarizability of a dielectric sphere, from electrostatics (CHECK)")
    a, resid = sphere_polarizability()
    print(f"   alpha / (4 pi eps0) = {a};  minus K R^3 with K = (eps-1)/(eps+2): {resid}")

    banner("P2  The dipole Green tensor at imaginary frequency (CHECK)")
    helm, div, trc = green_tensor()
    print(f"   (nabla^2 - xi^2/c^2) G = 0 off the source: max residual {helm:.1e}")
    print(f"   div G = 0 off the source: max residual {div:.1e}")
    print(f"   Tr G.G - 2 e^(-2u)(3 + 6u + 5u^2 + 2u^3 + u^4)/r^6 = {trc}")

    banner("P3  The Casimir-Polder coefficient (CHECK, exact)")
    I = frequency_integral()
    print(f"   int_0^oo e^(-2u)(3 + 6u + 5u^2 + 2u^3 + u^4) du = {I}")
    print(f"   U = -({casimir_coefficient()}) hbar c alpha1 alpha2 / r^7 = -(23/(4 pi)) hbar c alpha1 alpha2 / r^7")

    banner("P4  In the diamond experiment")
    mine, theirs, grav, R = compare_with_experiment_code()
    import stur_gravity_full as GF
    print(f"   design A, m = {GF.design_a()['m']:.3e} kg (R = {R * 1e6:.2f} um), r = 200 um: derived U = {mine:.4e} J,"
          f" src/stur_gravity_entanglement.py {theirs:.4e} J (ratio {mine / theirs:.12f})")
    print(f"   Gravity at the same r: {grav:.4e} J; Casimir/gravity = {mine / grav:.3e}")
    print("   Casimir ~ R^6/r^7 and gravity ~ R^6/r, so the safe gap does not depend on the mass:")
    print("   181 um is where Casimir's entangling phase is 10% of gravity's (src/stur_gravity_full.py, H0).")

    banner("P5  Finite temperature: the Matsubara sum in closed form (CHECK, exact)")
    e, t, ser, hi = matsubara_eta()
    print("   U_T = U_0 eta(tau), tau = 2 pi k_B T r / (hbar c); eta = (2/23) tau sum'_n f(n tau)")
    print(f"   small tau: eta = {ser} + O(tau^8)")
    print(f"   large tau: eta / tau -> {hi}  (U_T -> -3 k_B T alpha1 alpha2 / r^6, the n = 0 term)")
    for tv in (0.2, 0.5, 2.0, 20.0):
        print(f"   tau = {tv}: closed form {float(eta(tv)):.12f}, term-by-term sum {eta_direct(tv):.12f}")
    import stur_gravity_entanglement as GE
    xi1 = lambda T: 2 * math.pi * GE.KB * T / GE.HBAR
    print(f"   xi_1 = 2 pi k_B T / hbar: {xi1(0.15):.1e} rad/s at 0.15 K, {xi1(77):.1e} at 77 K;"
          " diamond's eps is static far above that")

    banner("P6  The Casimir-safe gap at finite temperature (10% of gravity's entangling phase)")
    gaps, dxB, dxA = thermal_gaps()
    print(f"   T (K)    gap, dx = {dxB * 1e6:.0f} um (as H0)   gap, dx = {dxA * 1e6:.0f} um (design A)   tau at the far branch")
    for T, (gB, gA) in gaps.items():
        far = math.hypot(gB, dxB)
        print(f"   {T:6.2f}   {gB * 1e6:10.2f} um              {gA * 1e6:10.2f} um                  {tau_of(far, T):.3g}")
    g0, g15 = gaps[0.0][0], gaps[T_ENV][0]
    print(f"   (T = 0 by root-finding: {g0 * 1e6:.2f} um; H0's grid gives 181.16 um.)")
    print(f"   at the design's {T_ENV} K the gap moves by {g15 / g0 - 1:+.1e}: the T = 0 formula holds there.")
    print(f"   at 4.2 K it is {gaps[4.2][0] / g0 - 1:+.2%}, at 77 K {gaps[77.0][0] / g0:.2f}x the T = 0 gap:")
    print(f"   up to a helium bath the T = 0 gap stands; at 10 K it grows by {gaps[10.0][0] / g0 - 1:.0%}.")

    banner("P7  Patch potentials as a permanent dipole (MODEL), against H6's bound at design A")
    A, pmax, Vl, rows = patch_budget()
    R = A["R"]
    print(f"   p_rms = sqrt(12 pi) eps0 R l V per axis (l << R); Monte Carlo at l = R/10:"
          f" {patch_dipole_mc(R, R / 10, 1.0) / patch_dipole(R, R / 10, 1.0):.3f} of the formula")
    print(f"   H6 bound at design A (R = {R * 1e6:.2f} um, gap {A['gap'] * 1e6:.0f} um): p < {pmax:.2e} C m,"
          f" so V l < {Vl:.2e} V m")
    for l, Vmax, p, ratio, gneed in rows:
        print(f"   patches of {l * 1e9:3.0f} nm: V_rms must be < {Vmax * 1e6:4.1f} uV;  at {PATCH_V_METAL * 1e3:.0f} mV,"
              f" p = {ratio:.0f}x the bound, unshielded gap needed {gneed:.2g} m")
    print("   -> patch potentials of the size measured on metals exceed the bound by orders of magnitude.")
    print("      H6's conclusion stands, now quantified: a conducting shield, or microvolt patch control.")


if __name__ == "__main__":
    main()
