# Accepted: campaign `qcd_drho` (O(alpha_s) QCD correction to Delta rho of the top-bottom doublet)

*Result: two blind Opus builds derived, from the two-loop vacuum correlators of the weak currents (rung, self-energy insertions, vertex, top-mass counterterm, d-dimensional traces, closed-form masters, anticommuting gamma5), the coefficient of
alpha_s/pi in Delta rho = Delta rho_0 [1 + c alpha_s/pi]: **c_pole = -C_F (1/2 + pi^2/6)** (-2.859912 for C_F = 4/3) and **c_MSbar(mu) = C_F [3/2 - pi^2/6 + (3/2) ln(mu^2/mbar^2)]** (-0.193245 at mu = mbar), with Delta rho_0 = N_C G_F m^2/(8 sqrt2 pi^2).
An Opus auditor reproduced it by a different route (Goldstone-boson wave-function renormalization in the gaugeless limit, 150-digit evaluation, PSLQ: c_pole/C_F = -(3 + pi^2)/6, c_MS/C_F = (9 - pi^2)/6, xi independent to 25 digits).*

| Phase | Evidence |
|---|---|
| P0 clean rooms | Level 2 of PROTOCOL.md section 3 |
| P1 builders | `builds/a`, `builds/b` (both Opus); each passed `gate.py --mode builder` |
| P2 verifier | `gate.py --mode verifier` with the hidden oracle and the audit's five checks plus tightened lint: `builds/*/verifier_report.txt` (all PASS) |
| P3 cross-build | identical to every printed digit (pole -2.859912089130969, MS-bar -0.1932454224643019, four scheme/C_F/mu points) |
| P4 audit | `AUDIT.md`: independent Goldstone-route derivation, masters checked at 32 points in d, mass relation re-derived, 22 mutants of build a (15 killed by the first gate, all 22 by the adopted checks): no build bug |

## Class counts
B: 0. R: 0 in the physics; the oracle's reference was recalled from memory by the orchestrator and is now confirmed independently. C: the gate probed (N_C, C_F) only at (3, 4/3), the pole coefficient only at mu = m and narrow windows (seven wrong mutants passed:
C_F derived from N_C, C_F fixed, the MS-bar log in the pole coefficient, mu/m clipped, extra terms outside the window, N_C = 1 and N_C > 3 special cases); fixed by the adopted checks. Lint let a hard-coded answer through (a mutant typing the C_F-stripped values); `LINT_TARGETS` and `LINT_EXACT` extended.
N: positive confirmations (masters, mass relation, N_C and massless-b statements, gauge independence).

## What is and is not established
* **Established:** the coefficient in both schemes, its C_F and mu dependence, the pole-to-MS-bar relation m_pole = mbar[1 + C_F a (1 + (3/4) ln(mu^2/mbar^2))], gauge independence, the Ward identity Pi_+(0) = Pi_0(0) at two loops.
* **Limits (stated plainly):** (i) both builders and the auditor said they knew the textbook result beforehand; they are language models, so "blind" means blind to the oracle and the repository, **not** to the literature, and the agreement of the builds is weaker evidence of independence than in the campaigns where the answer was not a famous number. The auditor's route differs structurally from the builds' (Yukawa/chiral vertices, bare-mass propagators), and the numbers come out of code, not typed in, but a shared memory of the target cannot be excluded.
  (ii) the definition of Delta rho (SPEC section 2, gaugeless limit, leading order in G_F m_t^2) and the step Delta rho = A_+ - A_0 (checked at one loop only) are shared by all derivations. (iii) anticommuting gamma5 (argued safe at this order, not checked in the 't Hooft-Veltman scheme). (iv) the massless-bottom limit; m_b effects and the terms beyond leading m_t^2 are not covered.

## Isolation evidence
`builds/{a,b}/isolation_audit.txt`: transcript audit, clean. Level 2, not level 3.
