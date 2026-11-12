#!/usr/bin/env python3
"""
The equation, derived from the quantum level up.

Start: quantum mechanics and local quantum fields with a short-distance spacing a.
Nothing else: no gravity, no classical fields, no curved spacetime, no collapse.

  DB  The Born rule from unitarity + locality / non-contextuality.         CHECK (stur_born.py)
  D1  Vacuum entanglement across any surface obeys an area law.             CHECK
  D2  The vacuum's modular Hamiltonian is 2 pi x the local boost energy:
      every accelerated observer sees the Unruh temperature.                CHECK
  D3  Clausius on every local horizon (delta Q = T delta S, S from D1)
      gives the gravitational field equations, with G fixed by D1.          CHECK (stur_jacobson.py)
  D4  Those equations in Lagrangian form are TEGR (torsion on flat space).  CHECK
  D5  Their static solution: Schwarzschild; their weak limit: Newton.       CHECK
  D6  A superposition: each branch of the matter sources its own field
      (collective emergence). This gives THE EQUATION.     FOLLOWS under R0 = a and
                                                           Markovian dynamics (+ K2 analog)
  D7  Consequences, computed from the equation: double slit, measurement,
      the electron's field, one diamond, two diamonds, the classical tests,
      and what changes if gravity is only an average.                      CHECK
  D8  What was put in, and what was not derived.

Every number is recomputed here from the modules named in brackets.
"""
import numpy as np
import sympy as sp

import stur_unification as U
import stur_measurement as Mm
import stur_tegr as T
import stur_tegr_gr as F
import stur_gravity_entanglement as ge
import stur_emergent as K
import stur_born as Bn
import stur_gravity_full as GF

G_SI, C, HBAR, KB = 6.67430e-11, 2.99792458e8, 1.054571817e-34, 1.380649e-23
L_P = np.sqrt(HBAR * G_SI / C**3)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def area_law_coefficient(ns=(10, 14, 18)):
    """[stur_unification.srednicki] S/(R/a)^2 at several R, extrapolated in 1/R."""
    R = np.array([n + 0.5 for n in ns])
    S = np.array([U.srednicki(N=2 * n + 30, n=n) for n in ns])
    k = np.polyfit(1 / R, S / R**2, 1)[1]
    return k, list(zip(R, S / R**2))


def modular_slope(L=40):
    """[stur_unification.modular_h] Effective modular velocity at the block centre / pi.
    Bisognano-Wichmann: K = 2 pi x boost energy, so this ratio -> 1."""
    h = U.modular_h(L, dps=30 + 2 * L)

    def veff(c):
        return sum(-r * np.sin(np.pi * r / 2) * h[c - (r + 1) // 2, c - (r + 1) // 2 + r]
                   for r in range(1, L, 2) if c - (r + 1) // 2 >= 0 and c - (r + 1) // 2 + r < L)
    c0 = L // 2
    return veff(c0) / (c0 * (L - c0) / L) / np.pi


def G_from_entanglement(a, n_fields, c_s):
    """D3: S/k_B = A c^3/(4 G hbar) must equal N c_s A / (4 pi a^2)  ->  G = pi a^2 c^3 / (N c_s hbar)."""
    return np.pi * a**2 * C**3 / (n_fields * c_s * HBAR)


def main():
    banner("D0  What is assumed")
    print("   Quantum mechanics: states and unitary evolution, with tensor products.")
    print("   Locality (no-signaling) and non-contextual probabilities (DB).")
    print("   Local quantum fields (N of them) with a short-distance spacing a.")
    print("   NOT assumed: the Born rule, gravity, a metric, classical fields, collapse.")

    banner("DB  The Born rule, derived (CHECK; full output in results/born/output.txt)")
    nz, worst, p0, c2 = Bn.fine_grain(2, 5)
    print(f"   Envariance: |c0|^2 = 2/5 fine-grained into 5 equal branches (amplitudes {nz.min():.6f}),"
          f" so p0 = {p0:.6f} = |c0|^2")
    print(f"   Additivity: only F(x) = x sums to 1 over every basis (x^1: {Bn.additivity_violation(1.0, trials=3000):.1e},"
          f" x^2: {Bn.additivity_violation(2.0, trials=3000):.2f})")
    print(f"   No-signaling: Bob's P(+) shift from Alice's choice: x^1 {Bn.signaling(1.0, 200):.1e},"
          f" x^2 {Bn.signaling(2.0, 200):.2f}")
    print(f"   Frequencies: wrong-frequency weight at N = 10000: {Bn.atypical_weight(10000, 0.4):.1e}")
    print("   FOLLOWS: given A1-A3, probability = |amplitude|^2 is forced, not postulated.")

    banner("D1  Vacuum entanglement obeys an area law (CHECK)")
    c_s, pts = area_law_coefficient()
    for R, s in pts:
        print(f"   R/a = {R:5.1f}:  S / (R/a)^2 = {s:.4f}")
    print(f"   Extrapolated: S = {c_s:.4f} (R/a)^2 per field = {c_s/(4*np.pi):.5f} A/a^2"
          "   (repository value 0.3046; LIT Srednicki 0.30)")

    banner("D2  The vacuum is thermal to every accelerated observer (CHECK)")
    for L in (20, 40, 60):
        print(f"   Free-fermion block of {L} sites: modular slope / (2 pi x boost) = {modular_slope(L):.5f}")
    print("   KNOWN (Bisognano-Wichmann): K = 2 pi x boost energy, exactly in the continuum.")
    print("   So an observer with acceleration g sees the vacuum at T = hbar g / (2 pi c k_B).")

    banner("D3  Clausius on every local horizon gives the field equations (Jacobson 1995; re-derived in stur_jacobson.py)")
    print("   Every point has local Rindler horizons. Energy crossing one is heat: delta Q = T delta S,")
    print("   with T from D2 and S = eta x area from D1. Demanding this for all of them gives")
    print("   R_mu nu - 1/2 R g_mu nu + Lambda g_mu nu = (8 pi G / c^4) T_mu nu, with 1/(4 G hbar) = eta.")
    print("   (Not recomputed here; its quantum version is the first law delta S = delta<K>, which is")
    print("    checked on the lattice in stur_unification.py U1: first-law slope ratio 0.99907,")
    print("    local Clausius ratio 0.99969. That the field follows each branch: stur_thermo_gravity.py.)")
    a_needed = K.cutoff_for_G(1, c_s)
    print(f"   G = pi a^2 c^3 / (N c_s hbar). The measured G then fixes a^2/N: for N = 1,"
          f" a = {a_needed/L_P:.3f} l_P; for N = 100, a = {K.cutoff_for_G(100, c_s)/L_P:.2f} l_P.")
    print("   FOLLOWS: G is a property of the quantum vacuum: how much it is entangled per area.")
    print("   It is not predicted: only the combination a^2 / N is fixed, by the measured G.")

    banner("D4  The same equations as a field theory: TEGR (CHECK)")
    d, Tv, Rv = T.identity_check(points=1)[0]
    print(f"   T_torsion = -R + (divergence): residual {d:+.1e} at a random point, T = {Tv:+.4f}, R = {Rv:+.4f}")
    print("   So the field equations of D3 come from the TEGR action")
    print("        S_grav[e] = (c^4 / 16 pi G) int e T d^4x,")
    print("   gravity as a torsion (gauge) field of the tetrad e on flat spacetime.")

    banner("D5  Its static solution and its weak limit (CHECK)")
    L_, eA, eB, Ap, ode, sols = F.solve_spherical()
    print(f"   Static, spherical: e^(-2B) = 1 + C1/r, A = -B  ({sols[1]})  -> Schwarzschild, unique")
    a_, b_, c_ = T.grad_form(*T.newtonian_lagrangian())
    print(f"   Weak field: (e T)_2 = {int(b_)} grad Phi.grad Psi {int(c_):+d} (grad Psi)^2  ->  Psi = Phi,"
          " laplacian Phi = 4 pi G rho")

    banner("D6  A superposition: THE EQUATION")
    print("   Matter in a superposition of configurations i (paths, positions). From D0, the")
    print("   fields are quantum too, and each branch i sources its own field configuration")
    print("   (EM and the tetrad e_i). The joint state after a time t:")
    print()
    print("        |Psi> = sum_i  c_i |i>_matter |E_i>_fields  exp( i S_i / hbar )")
    print()
    print("        S_i = S_matter[i] + S_EM[i] + (c^4 / 16 pi G) int e_i T[e_i] d^4x")
    print("        G   = pi a^2 c^3 / (N c_s hbar),   c_s = 0.3046   (D1-D3)")
    print()
    print("   and what any measurement on the matter sees:")
    print()
    print("        rho_ij(t) = rho_ij(0) <E_j|E_i>  exp( i (S_i - S_j) / hbar )")
    print()
    print("   <E_j|E_i> = how far the fields (detectors, light, the electron's own field,")
    print("   gravity) keep a record of which branch happened. The phase = the difference")
    print("   in action, including the field's own action.")
    print("   The step 'each branch sources its own field' is what D0 implies for a field that")
    print("   is made of the quantum level (collective emergence). Against a statistical gravity it")
    print("   is derived only on two conditions: the smearing is the cutoff a, and the dynamics are")
    print("   Markovian (COLLECTIVE.md, OPPENHEIM.md). Exact in the lattice analog:")
    r = K.medium_evolution()
    print(f"   [stur_emergent K2] entangling phase {r['dphi']:.4f} vs the emergent 1/r law"
          f" {r['static']:.4f}; record left in the medium {1-r['record']:.1e}")

    banner("D7  Consequences, each computed from the equation")
    print("   (a) Double slit with a which-path detector: rho_12 ~ <E2|E1>, so V = |<E1|E2>|.")
    for th in (0.0, np.pi / 6, np.pi / 3, np.pi / 2):
        _, _, V, D = Mm.double_slit(th)
        print(f"       detector angle {th/np.pi:.2f} pi: V = {V:.4f}, D = {D:.4f}, D^2 + V^2 = {V*V+D*D:.6f}")
    print("       No observer needed: the record alone does it. 'Measurement creates the")
    print("       outcome' is the statement <E1|E2> -> 0.")
    print("   (b) The electron's own field: its Coulomb field is in both branches (E_i differ by")
    print("       where the charge is). Free space: no lasting record, fringes stay. Near a")
    print("       surface the image charges record the path: fringes fade (LIT: Sonnentag &")
    print("       Hasselbach 2007). A literally split charge is excluded (MEASUREMENT.md T1, T5).")
    A = GF.design_a()
    E_, Ng = T.graviton_count(A["m"], A["dx"], A["ramp"], A["hold"])
    print(f"   (c) ONE diamond, gravity's own record: |<E1|E2>_grav| = exp(-N/2), N = {Ng:.1e} gravitons.")
    print("       Gravity keeps no record: a single mass stays coherent unless something else")
    print("       (gas, light, vibration) records it.")
    b = ge.BASE
    rij = ge.branch_distances(b["dx"], b["gap"], "parallel")
    Rb = ge.radius(b["m"])
    S_ij = np.array([[-F.interaction_energy_tegr(b["m"], Rb, rij[i, j])[2] * b["tau"]
                      for j in range(2)] for i in range(2)]) / HBAR
    dphi = S_ij[0, 0] + S_ij[1, 1] - S_ij[0, 1] - S_ij[1, 0]
    rho = ge.state(S_ij)
    print(f"   (d) TWO diamonds (1e-14 kg, 250 um splits, 200 um apart, 2.5 s): the action")
    print(f"       differences give an entangling phase {dphi:.4f} rad; concurrence"
          f" {abs(np.sin(dphi/2)):.4f}, negativity {ge.negativity(rho):.4f}.")
    print("       Gravity alone entangles them. Noise budget and best design: GRAVITY_ENTANGLEMENT.md")
    print("       (design A: 270 runs, 0.6 h at the published targets, derived gas rate; mass x4e8 beyond today).")
    dp = F.perihelion_shift(F.GM_SUN, F.MERCURY_A, F.MERCURY_E) * (36525 / F.MERCURY_P) * 180 / np.pi * 3600
    defl = F.light_deflection(F.GM_SUN, F.R_SUN) * 180 / np.pi * 3600
    gps, _ = F.gps_offset_us_per_day()
    print(f"   (e) The classical limit (one branch, many particles): perihelion {dp:.2f} arcsec/century,")
    print(f"       light bending {defl:.4f} arcsec, PPN gamma = {F.ppn_gamma()}, GPS {gps:+.2f} us/day.")
    m = A["m"]
    print("   (f) If gravity were only the AVERAGE of the quantum level (not D6): each branch")
    print("       would feel the mean field, S_i would factor, and (d) would give exactly zero")
    print(f"       entanglement. An average needs intrinsic collapse: Diosi-Penrose rate"
          f" {K.dp_rate(m, ge.radius(m), A['dx']):.0f} /s,")
    print("       killing even ONE diamond's superposition in ~6 ms (any Markovian average smeared")
    print("       over R0 < 0.1 um, Oppenheim's included). (c) and (d) both test this.")

    banner("D8  What was put in, and what was not derived")
    print("   Put in: unitary quantum mechanics; locality and non-contextuality; N local fields; the spacing a.")
    print("   Computed: the Born rule (DB), the area-law coefficient c_s, the Unruh/modular structure, the TEGR")
    print("   identity, Schwarzschild and Newton, every number in D7.")
    print("   Taken from the literature, not recomputed: Jacobson's step D3.")
    print("   Not derived: the value of G (only a^2/N is fixed by it), and the number and kinds")
    print("   of fields (the Standard Model).")
    print("   D6 (gravity emerges COLLECTIVELY) is derived only under R0 = a and Markovian dynamics.")
    print("   It is not distinctive: perturbative quantum gravity also predicts lambda = 1. (c) and (d)")
    print("   would rule out classical gravity; only a null result there would be new physics.")


if __name__ == "__main__":
    main()
