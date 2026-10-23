#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10f: can STUR's own structure close the theory gaps?
================================================================================
Three assumptions that the pre-registered hypotheses rest on but the repo does
not derive. Each is tested against terms already in the STUR action or the repo's
own constructions; nothing is tuned to hit a target number.

 (a) M3a/H1: a restoring force that makes the R-phase zero mode theta oscillate
     log-periodically, theta ~ sin(omega ln t), omega = 2 pi^2.
     Candidate sources in the repo:
       a1. the fermion phase potential y^2 v^2 (1 - cos(phi - phi_g)) |psi|^2
           (ALPHA_PARAMETER_DERIVATION.md sec. 1.3)
       a2. the Z3 twisted boundary condition R(X + L_X) = e^{2 pi i/3} R(X)
       a3. the Higgs Z3 modulation H(phi) = H0 [1 + eps_H cos 3 phi]
           (ABSOLUTE_MASS_DERIVATION.md sec. 2.2) through the fermion
           Coleman-Weinberg energy
       a4. the QCD anomaly (c_s = 3)
       a5. the Yukawa read literally: psibar_L (R_1 + R_2) psi_R (no i gamma^5)
 (b) M3a/H2: only leptons carry R-charge.
 (c) Inflation from the Master Action's own scalar |R|:
       V = lambda/4 (|R|^2 - v^2)^2,  gravity coupling alpha|R| T  (f(phi) T)

Usage:  python genesis_v10f_theory_gaps.py
================================================================================
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

OMEGA = 2 * np.pi ** 2
ALPHA_EM = 1 / 137.035999
M_T = 172.57                      # GeV
MPL_RED = 2.435e18                # GeV
H_REC = 3.0e-38                   # GeV, H(z*) ~ 3e-29 eV (Planck 2018 LCDM)
H0 = 1.44e-42                     # GeV
T0_OVER_TSTAR = 13.797e9 / 3.718e5
SIGMA_Q = 0.862                   # quark-brane localization width [rad] (repo)
M3A_A0 = (1.435, 2.931)           # registered A0 range for c_g = 3 [rad]
gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:56s} {detail:32s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 80 + "\n  " + s + "\n" + "=" * 80)


# ------------------------------------------------------------------------------
# (a) restoring force for the R-phase zero mode
# ------------------------------------------------------------------------------
def part_a():
    header("(a) Is there a restoring force for theta that gives sin(omega ln t)?")
    # a1/a2: shift symmetry is translation in X
    th, k, X, phig = sp.symbols('theta k X phi_g', real=True)
    phi = k * X + th
    Vf = 1 - sp.cos(phi - phig)
    Xg = (phig - th) / k                              # where the fermion sits
    print("  a1  fermion potential 1 - cos(kX + theta - phi_g) is minimised at X = (phi_g - theta)/k:")
    print(f"      d/dtheta of the minimum value = {sp.simplify(sp.diff(Vf.subs(X, Xg), th))}")
    print("      theta only MOVES every localised fermion by Delta X = -theta/k. All Yukawas are")
    print("      L-R overlaps (exp(-|X_i - X_j|^2/4 sigma^2)); every species moves together, so")
    print("      no mass and no energy depends on theta. Exact flat direction (combined U(1) x X-shift).")
    gate("a1  Yukawa phase potential gives theta a potential", False, "V(theta) = 0 identically")
    print("  a2  R(X + L_X) = w R(X) fixes the winding k L_X = 2 pi/3; a constant shift of phi")
    print("      preserves it. No theta dependence.")
    gate("a2  Z3 twisted boundary condition gives theta a potential", False, "V(theta) = 0 identically")

    # a3: Higgs pinned to the coordinate with a Z3 modulation -> CW potential
    print("  a3  Higgs H(phi) = H0[1 + eps_H cos 3phi] pinned to the coordinate breaks the X-shift.")
    print("      Overlap with Gaussians moved by theta: m_f(theta) = m_f0 [1 + eps_eff cos 3 theta],")
    supp = np.exp(-9 * SIGMA_Q ** 2 / 2)
    print(f"      eps_eff = eps_H exp(-9 sigma^2/2) = {supp:.4f} eps_H (sigma_q = {SIGMA_Q});"
          " phi_g = 2 pi g/3 gives cos 3theta for every generation.")
    print("      CW, top dominated: V(theta) = -(N_c/4 pi^2) m_t^4 eps_eff (ln m_t^2/mu^2 - 1) cos 3theta;")
    print("      the mu dependence needs a cos 3theta counterterm, so the amplitude is not calculable")
    print("      in the repo's model. Natural size |V| ~ (3/4 pi^2) m_t^4 eps_eff.")
    rows = []
    for eps_H in (1e-1, 1e-3, 1e-6):
        Vamp = 3 / (4 * np.pi ** 2) * M_T ** 4 * eps_H * supp
        m_th = 3 * np.sqrt(Vamp) / MPL_RED              # f <= M_Pl gives the SMALLEST mass
        rows.append((eps_H, m_th))
        print(f"      eps_H = {eps_H:7.0e}: m_theta >= {m_th:.2e} GeV (f <= M_Pl) = {m_th / H_REC:.1e} H(z*)")
    eps_crit = (H_REC * MPL_RED / 3) ** 2 / (3 / (4 * np.pi ** 2) * M_T ** 4 * supp)
    print(f"      m_theta < H(z*) needs eps_H < {eps_crit:.0e}.")
    print("      A static potential gives a CONSTANT mass: theta oscillates as a^-3/2 cos(m t), not as")
    print(f"      sin(omega ln t). Log-periodicity needs m(t) = omega/t; between recombination and today")
    print(f"      m t changes by t0/t* = {T0_OVER_TSTAR:.1e}. With m >> H the oscillation averages away in")
    print("      every visibility window and beta -> (c alpha/2pi)(theta(t0) - <theta>) oscillates in time")
    print("      with period ~ 1/m (sub-second), averaging to zero in any CMB observation.")
    gate("a3  Higgs-modulation CW gives the log-periodic H1 oscillation", False,
         f"m t not constant (x{T0_OVER_TSTAR:.0e})")
    print("  a4  QCD: c_s = 3 gives V = m_pi^2 f_pi^2 (1 - cos 6 theta): again a constant mass")
    print("      (a QCD axion), and M3a's H2 requires c_s = 0, which removes it.")
    gate("a4  QCD anomaly gives the log-periodic H1 oscillation", False, "constant mass; needs c_s != 0")
    print("  a5  Read literally, psibar_L (R_1 + R_2 gamma^5) psi_R = psibar_L (R_1 + R_2) psi_R since")
    print("      gamma^5 psi_R = psi_R. Then m_f = y v (cos theta + sin theta): explicit U(1) breaking,")
    print("      a tree-level potential ~ m_t^4 (constant mass again) and NO chiral phase, so c_g = 0:")
    print("      no birefringence at all. The text's own V_ferm uses the phase, i.e. the intended")
    print("      coupling is psibar (R_1 + i gamma^5 R_2) psi, the reading used everywhere else here.")
    print("  RESULT (a): NOT CLOSED. Nothing in the repo gives theta a restoring force ~ 1/t; the only")
    print("  potentials available (a3, a4, a5) are static and give ordinary constant-frequency")
    print("  oscillations that wash out of the CMB. A ~1/t mass needs a coupling to H^2 (e.g. xi T |R|^2),")
    print("  which is not in the Master Action.")
    return rows, eps_crit


# ------------------------------------------------------------------------------
# (b) leptons-only R-charge
# ------------------------------------------------------------------------------
def part_b():
    header("(b) Does STUR force quark R-charges to vanish or cancel?")
    print("  * stur_toe_closure.py PART 2 solves the Mathieu localization for BOTH the quark brane")
    print("    (alpha_q -> lambda_W, CKM) and the lepton brane (alpha_l -> PMNS). The Mathieu potential")
    print("    alpha(1 - cos theta) IS the R-Yukawa phase potential y^2 v^2 (1 - cos(phi - phi_g)).")
    print("    A quark with zero R-charge would not localize, and the CKM/mass derivations would fail.")
    print("  * The generation index enters as a POSITION phi_g = 2 pi g/3, not as a charge: the coupling")
    print("    psibar (R_1 + i gamma^5 R_2) psi has X = 1 for every species and generation, so the")
    print("    1 + w + w^2 = 0 cancellation does not act on R-charges.")
    from fractions import Fraction as Fr
    gen = [(3, Fr(2, 3)), (3, Fr(-1, 3)), (1, Fr(-1)), (1, Fr(0))]
    cg = 3 * sum(nc * q * q for nc, q in gen)
    cs = 3 * sum(Fr(1, 2) for nc, _ in gen if nc == 3)
    print(f"  forced anomaly coefficients: c_g = {cg}, c_s = {cs}")
    gate("b   repo structure allows c_s = 0 (H2)", cs == 0, f"c_s = {cs}")
    lo, hi = (a * 3 / 8 for a in M3A_A0)
    print(f"  M3a with the forced c_g = 8 (beta ~ c_g A0): A0 = {lo:.3f} - {hi:.3f} rad (more natural),")
    print(f"  but theta_QCD,eff = 2 c_s theta oscillates with amplitude {6 * lo:.1f} - {6 * hi:.1f} rad;")
    print("  the neutron EDM requires |theta| < 1e-10. Excluded by ~10 orders of magnitude.")
    gate("b   M3a with forced charges passes the nEDM bound", 6 * lo < 1e-10, f"|theta_QCD| ~ {6 * lo:.1f} rad")
    print("  RESULT (b): NOT CLOSED, and contradicted: STUR's own localization needs R-charged quarks.")
    return cg, cs, (lo, hi)


# ------------------------------------------------------------------------------
# (c) inflation from |R| with F(|R|) T, F = 2 alpha |R|
# ------------------------------------------------------------------------------
def part_c():
    header("(c) Inflation from the Master Action's own scalar (scalar-torsion f(phi) T)")
    t = sp.symbols('t')
    N_ = sp.Function('N')(t)
    a = sp.Function('a')(t)
    p = sp.Function('p')(t)
    al, lam, v = sp.symbols('alpha lambda v', positive=True)
    F = 2 * al * p
    V = lam / 4 * (p ** 2 - v ** 2) ** 2
    T = -6 * a.diff(t) ** 2 / (N_ ** 2 * a ** 2)        # flat FRW, diagonal tetrad
    L = N_ * a ** 3 * (F / 2 * T + p.diff(t) ** 2 / (2 * N_ ** 2) - V)
    con = sp.simplify(sp.diff(L, N_).subs(N_, 1).doit())
    H = sp.symbols('H')
    con_H = sp.simplify((con / a ** 3).subs(a.diff(t), H * a))
    print(f"  constraint (lapse variation, N = 1): {sp.factor(con_H)} = 0")
    print("    i.e. 3 F H^2 = phi_dot^2/2 + V: no H F_dot term (unlike F R), as expected for f(phi) T")
    ELp = sp.simplify((sp.diff(sp.diff(L, p.diff(t)), t) - sp.diff(L, p)).subs(N_, 1).doit() / a ** 3)
    print(f"  scalar equation / a^3: {sp.simplify(ELp.subs(a.diff(t), H * a).subs(a.diff(t, 2), 0))} (+ a_ddot terms vanish)")
    print("    i.e. phi_ddot + 3 H phi_dot + V' + 3 F' H^2 = 0")
    # slow roll, v << phi: V ~ lambda phi^4/4, F'/F = 1/phi
    print("  slow roll (phi >> v): 3 H phi_dot = -(V' + F'V/F) = -(5/4) lambda phi^3,  H^2 = lambda phi^3/(24 alpha)")
    print("    eps_H = 15 alpha/phi,  dN = -dphi/(10 alpha),  phi_end = 15 alpha")
    print("    => eps_H(N) = 15/(10 N + 15): scale-free, independent of alpha, lambda (v << phi)")
    for Nst in (50, 60):
        print(f"       N = {Nst}: eps_H = {15 / (10 * Nst + 15):.4f}")

    # exact background numerically (alpha = lambda = 1, v = 0), checks the slow-roll result
    def rhs(tt, y):
        ph, pd, Ne = y
        Hh = np.sqrt((0.5 * pd ** 2 + 0.25 * ph ** 4) / (3 * 2 * ph))
        return [pd, -3 * Hh * pd - ph ** 3 - 3 * 2 * Hh ** 2, Hh]

    def eps_of(y):
        ph, pd, _ = y
        Hh2 = (0.5 * pd ** 2 + 0.25 * ph ** 4) / (6 * ph)
        Hh = np.sqrt(Hh2)
        # H_dot from differentiating the constraint along the trajectory
        dd = -3 * Hh * pd - ph ** 3 - 6 * Hh2
        dH2 = (pd * dd + ph ** 3 * pd) / (6 * ph) - Hh2 * pd / ph
        return -dH2 / (2 * Hh2 * Hh)
    ev = lambda tt, y: eps_of(y) - 1
    ev.terminal = True
    ph0 = 2000.0
    H0_ = np.sqrt(0.25 * ph0 ** 4 / (6 * ph0))
    s = solve_ivp(rhs, [0, 1e6], [ph0, -(1.25 * ph0 ** 3) / (3 * H0_), 0.0], events=ev,
                  rtol=1e-10, atol=1e-12, dense_output=True)
    te = s.t_events[0][0]
    tt = np.linspace(0, te, 400001)
    Y = s.sol(tt)
    Nleft = Y[2, -1] - Y[2]
    for Nst in (50, 60):
        i = np.argmin(np.abs(Nleft - Nst))
        en = eps_of(Y[:, i])
        print(f"    numerical background, N = {Nst}: eps_H = {en:.4f}  (slow roll {15 / (10 * Nst + 15):.4f})")
        if Nst == 60:
            gate("c   exact background confirms eps_H = 15/(10N+15)", abs(en / (15 / 615) - 1) < 0.05,
                 f"{en:.4f} vs {15 / 615:.4f}")
    print("""
  Perturbations: Raatikainen & Rasanen, JCAP 12 (2019) 021 (arXiv:1910.03488) show that a
  teleparallel theory with a non-minimally coupled scalar, with coupling functions F (to T),
  G (torsion vector x d phi) and P, has NO linear scalar perturbations unless F, G, P satisfy a
  particular relation. STUR has F = 2 alpha|R|, G = 0, P = 0. Whether that combination meets the
  relation could not be verified here (full text not reachable); the metric-equivalent choice
  needs G proportional to F', which STUR does not have.
  => n_s and r cannot be computed defensibly from the Master Action. If scalar perturbations
     exist, the scale-free background means n_s and r would depend on N only (no free
     parameter), which would make this a sharp prediction worth the full calculation.
  Also: today M_Pl^2 = 2 alpha v, so the requirement phi_* ~ alpha (10 N + 15) >> v is
  v/alpha << ~600, i.e. alpha^2 >> M_Pl^2/1200; alpha and v are not separately fixed in the repo.
  RESULT (c): PARTIALLY CLOSED. Background is derived and parameter-free (eps_* = 0.024 at
  N = 60); perturbations are not established, so no n_s or r.""")
    gate("c   n_s and r computable from the Master Action", False, "scalar perturbations not established")


def main():
    part_a()
    part_b()
    part_c()
    header("SUMMARY")
    print("""  (a) not closed: Yukawa and Z3 structure leave theta exactly flat; the static potentials that
      exist (Higgs-modulation CW, QCD, literal Yukawa) give constant-frequency oscillations, not
      sin(omega ln t).
  (b) not closed, contradicted: STUR's quark localization needs R-charged quarks; c_g = 8, c_s = 3.
      M3a with those charges would make theta_QCD oscillate by ~3-7 rad.
  (c) partially closed: parameter-free slow-roll background eps_H = 15/(10N+15); no defensible
      n_s, r because scalar-torsion scalar perturbations are absent unless a coupling relation holds.""")
    print(f"\n  gates: {sum(gates)}/{len(gates)} passed (FAILs are results, not code errors; one PASS is a numerical check)")


if __name__ == "__main__":
    main()
