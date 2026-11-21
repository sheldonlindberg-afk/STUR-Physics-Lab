# Accepted: campaign `dr_xi` (gauge-parameter independence of the whole bosonic one-loop Delta r, general R_xi)

*Result: two blind Opus builds, with no provided module, derived the whole bosonic one-loop Delta r of muon decay in the general R_xi gauge (one xi for W, Z, photon; Feynman rules generated from the
Lagrangian in code): the gauge-boson self-energies, photon-Z mixing, on-shell renormalization (class SE) and the vertex, box and lepton wave-function diagrams with the Fermi-theory subtraction (class VBW).
The total is independent of xi from 1e-9 to 1e6 (relative spread 1e-13 or better), equals the xi = 1 Denner value to 1e-15, and is mu independent; the two classes depend on xi (SE changes by -2.5e-3 between xi = 0 and 1 at the
benchmark) and cancel exactly. The two builds agree on SE and VBW to 9e-15 for every xi > 0, and class SE agrees with an auditor's independent derivation at 49 points (xi 1e-12..1e6) to 3e-15.*

| Phase | Evidence |
|---|---|
| P0 clean rooms | Level 2 of PROTOCOL.md section 3. Build a was restarted from a fresh room after a container restart killed its first builder; the transcript audited covers the whole restarted build (see its isolation_audit.txt) |
| P1 builders | `builds/a`, `builds/b` (both Opus: the task is hard); each passed `gate.py --mode builder` |
| P2 verifier | `gate.py --mode verifier` with the hidden oracle and the audit's five checks: `builds/*/verifier_report.txt` (all PASS) |
| P3 cross-build | `cross_build_comparison.txt`: SE and VBW agree to 9e-15 (xi > 0, three points x six xi x three mu); at exactly xi = 0 they differ by a convention constant |
| P4 audit | `AUDIT.md` (Opus; independent derivation of class SE, 49 points; 21 mutants of build a, 19 wrong, 9 killed by the first gate, all 19 by the adopted checks): no build bug |

## Class counts
B: 0. R: 1 (the SPEC asked for the classes at xi = 0, where they are infrared divergent and their values a convention; clarified). C: the oracle sampled no xi between 0 and 0.2 or above 1000 and could not see anything moved
between SE and VBW (ten wrong mutants passed the first gate: an f(xi) added to SE and subtracted from VBW, a Feynman-gauge photon or Z, small-xi and xi = 0 branches, the AZ term moved between classes); fixed by the adopted checks.
N: structure confirmed (below); the two equivalent mutants (a consistent tadpole, a real-part error at thresholds that carry zero coefficient) confirm the builders' arguments.

## What is and is not established
* **Established:** the total is gauge-parameter independent in the whole range, including the photon's and the Z sector's xi separately; delta Z_e is xi independent; Sigma_W(M_W^2)/M_W^2 - Sigma_Z(M_Z^2)/M_Z^2 is xi independent; all of class SE's xi dependence sits in
  [Sigma_W(0) - Sigma_W(M_W^2)]/M_W^2 and the vertex, box and wave-function terms cancel it; as xi -> 0+ each class diverges like +-(3/4)(alpha/4 pi) ln xi (soft photon with the Goldstone and the W's xi-pole) and the total is finite.
* **Not established:** class VBW was not independently derived: its audit check (VBW against Denner's total minus the auditor's SE) follows from gauge independence. The two builds are independent derivations of VBW, but share the photon-mass infrared definition of the SPEC.
  The values of the classes at exactly xi = 0 are a convention (build a: kappa = 5/6, build b: kappa = 1, difference (1/8)(alpha/4 pi) in each class, equal and opposite). Build a's remark that a fully dimensional IR treatment would shift the total by (3/2)(alpha/4 pi) was not checked; the photon-mass
  definition is the SPEC's and Sirlin's charge-retention G_F. The match with Denner at xi = 1 shows the same Delta r as the literature, not that the classes are right at xi != 1. Fermion loops and QCD are excluded: the fermion-loop part (Link 31) was derived at xi = 1 only and its gauge independence at xi != 1 was not rechecked.

## Isolation evidence
`builds/{a,b}/isolation_audit.txt`: transcript audit, clean. Level 2, not level 3.
