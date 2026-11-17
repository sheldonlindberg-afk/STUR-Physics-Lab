# Accepted: campaign `qed_cp` (Casimir-Polder by fourth-order perturbation theory)

*Result: the full retarded, three-dimensional, two-polarization Casimir-Polder interaction of two single-resonance atoms,
derived from the 12 time-ordered photon-exchange diagrams, agrees with the repository's imaginary-frequency (Green-tensor)
route to 1e-15 over r w0 = 1e-2 to 1e3 (against an extended-precision reference; 6e-12 against rung 3's double-precision quad), with far coefficient 23/(4 pi) and near coefficient 3/4 derived, not typed.*

| Phase | Evidence |
|---|---|
| P0 clean rooms | Level 2 of PROTOCOL.md section 3: two rooms outside the repository, no oracle, no src/. Both rooms shared one filesystem with the repository, so independence relied on the agents' compliance (the audit found no sign of copying) |
| P1 builders | `builds/a` (Opus), `builds/b` (Sonnet), each passed `gate.py --mode builder` |
| P2 verifier | the orchestrator ran `gate.py --mode verifier` with the hidden oracle on each build, before and after the audit's strengthening: `builds/*/verifier_report.txt` (23 + 2 + 1 tiers, all PASS) |
| P3 cross-build | a and b agree to 4e-16 on random (r, w0, alpha0) (orchestrator's comparison) |
| P4 audit | `AUDIT.md` (Opus auditor, six mutants, five proposed checks): verdict ACCEPT; the one high finding is against the gate, not the builds |
| Gate strengthening | the audit's three blind and two oracle checks, an accurate large-r oracle reference, and a lint that folds integer-built constant expressions were added (commit d74c037) |

## Class counts

B (builder bug): 0 found after the gate. R (reference/oracle bug): 1, the oracle's own reference loses accuracy for r w0 > 30
(fixed). C (spec change): 0. N (numerical): 2 notes, both builders' brute-force Abel-damping checks agree to 3e-4 to 4e-4,
which is the extrapolation error they state.

## What is and is not established

* **Established:** the 12-diagram sum with the exact photon polarization sum and angular average reproduces the
  Green-tensor formula, including the dyadic (3 x 3, two-polarization) structure, to machine precision; the ban on
  assuming that formula was honoured in both derivations (the audit checked each step).
* **Not established:** that the Abel-damping limit equals the physical value is supported (three regularizers agree;
  a sharp cut-off has no limit) but not proved; the gate cannot enforce SPEC section 2 numerically (mutant M1 passed
  every numerical check and is now caught only by the lint and by reading DERIVATION.md).
* **Open follow-ups** (from AUDIT.md): intermediate-result exports so the banned route fails numerically; wording
  fixes in both DERIVATION files ("posited, proved by residues" in build a; "exponential" not "Gaussian" damping in b).
