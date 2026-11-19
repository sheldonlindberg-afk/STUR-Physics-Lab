# Accepted: campaign `charged_half` (Carr's charged spin-1/2 weight 0.142, Page's charge-fluctuation mechanism)

*Result: for a massless Dirac field around a Schwarzschild hole of fluctuating charge n (Coulomb energy g/r, g = alpha q n, chemical potential g/2 at the horizon), the
grey-body factors, the emission rates and the stationary charge distribution were derived by two blind builds. With the rule that a particle sees the hole charge after its
emission (rule (after, after)) the emitted-power weight is 0.1465 x 0.96345 = 0.1411 against the quoted 0.142; the energy-weighted ratio is 0.99595 against the literature's 0.9905.
**The audit shows the agreement is convention dependent: the thermodynamically consistent rule (after, mid) gives 1.0077 (f = 0.1476), essentially the neutral value.**
0.142 is consistent with a Page-type model, not derived by first principles.*

| Phase | Evidence |
|---|---|
| P0 clean rooms | Level 2 of PROTOCOL.md section 3 (same caveat as `greybody`) |
| P1 builders | `builds/a` (Opus), `builds/b` (Sonnet) |
| P2 verifier | the orchestrator ran `gate.py --mode verifier`; both PASS, including the audit's five adopted checks: `builds/*/verifier_report.txt` |
| P3 cross-build | both agree with the reference and the auditor's solver to ~1e-7 on Gamma, rates and ratios (weight ratio 0.963447 for the principal rule) |
| P4 audit | `AUDIT.md` (Opus, independent sympy derivation of the radial Dirac system, independent Whittaker-matching Gamma solver, 20 mutants of build a, 13 killed by the first gate, all 20 by the adopted checks) |

## Class counts
B (builder bug): 1, closed. Build b truncated the large-r asymptotic series at its first increasing term (Gamma off by 7e-6 near g = 0); label-only round trip; the fixed build passes.
R (oracle bug or weakness): 4, all addressed: the oracle's claim that the literature ratio is reproduced "by the principal rule only" was false (the 3-digit window of 0.142 also
contains (before, mid)); the gate's narrow probes (7 wrong mutants passed: wrong Gamma at |g| > 0.125 or j >= 4.5 or w > 1.2, three partial waves only, mixed rules swapped, g clipped,
rates() not tied to the build's transmission()), fixed by the five adopted checks. C (spec change): 0. N: dead code in the reference scripts; reference Gamma good to ~1e-7 (4e-7 at very small Gamma).

## What is and is not established
* **Established:** the radial equations, the flux identity, the horizon condition and mu = g/2 (audit derivation); Gamma from three solvers; the birth-death chain and its distribution (<n^2> = 11.81;
  the equilibrium value 1/(4 pi alpha) = 10.9 is not reached because emission into vacuum is not a bath).
* **Not established:** which O(alpha) charge assignment is physical. Weight ratio by rule at alpha: (after, after) 0.9634, (mid, mid) 0.9882, (after, mid) 1.0077, (before, before) 1.0136; nine rules span 0.927-1.054.
  Small-alpha: 1 + alpha (1.846 + 5.356 s_gb - 12.297 s_mu); only +1.85 alpha is the fluctuation effect. The literature energy ratio 0.9905 is not reproduced and cannot be in this model (bound >= 0.9959).
  Self-energy corrections of the same order are outside the SPEC. Page (1977) could not be read; only its abstract.

## Isolation evidence
`builds/{a,b}/isolation_audit.txt`: transcript audit after all rounds, clean (no web, no outside reads, no canaries). Level 2, not level 3.
