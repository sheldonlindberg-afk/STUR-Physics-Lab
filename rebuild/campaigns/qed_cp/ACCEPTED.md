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

## Revision: build a corrected after acceptance

While fixing the audit's documentation findings, build a's builder found a real bug: for r w0 <= 1e-7 `cp_energy` was low
by 4.2e-4 relative (the integration under-sampled a slowly decaying tail on one long panel; breakpoints at every decade now
fix it, and the near zone gives U r^6 = -3/4 to nine digits). **The original gate and the original oracle missed it**: the
oracle probed r w0 = 0.05 and above, and its random points started at 1e-2. The oracle is therefore extended: the random
points now span r w0 = 1e-8 to 1e5 (fresh seed each run) and a fixed check at r w0 = 1e-8, 1e-7, 1e-6, 1e-5, 1e3, 1e4, 1e5
holds each build to 1e-7 against the accurate reference (which reproduces the analytic limits to 1e-9 over that range).

| Version | Extreme-separation check |
|---|---|
| Build a as first accepted | FAIL (4.2e-4 at 1e-8) |
| Build a revised (this repository now) | PASS (2.2e-16); full verifier PASS (`builds/a/verifier_report.txt`) |
| Build b | PASS (5.3e-14) |

Elsewhere (r w0 >= 1e-6) the revised build a's values differ from the first accepted ones by at most 2e-13, so Link 23's
comparison (r w0 = 0.05 to 20) is unchanged. Documentation fixes in the revised DERIVATION.md: the denominator identity is
"posited, then proved by residues" (and was first found by fitting a two-coefficient ansatz); the claimed random-point and
precision checks now exist under `__main__` (8.9e-16 and 2.2e-16); the provenance note says what runs (a one-dimensional
imaginary-frequency integral derived from the 12 diagrams); the validity range is 1e-12 <= r w0 <= 1e5.
