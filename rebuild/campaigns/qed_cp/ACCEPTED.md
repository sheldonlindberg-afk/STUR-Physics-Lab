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

## Revision: build b's documentation findings addressed

Build b's builder fixed the audit's documentation findings and one precision item; the full verifier on the extended
oracle passes (`builds/b/verifier_report.txt`, 28 passes including the extreme-separation check, which is exact to the
double), and the values agree with the revised build a to 2e-16 or better at every separation tried. Changes:
the transcription typo and the "Gaussian" wording fixed; the claim that the result is independent of the damping shape
was **tested** instead of softened (a Gaussian damping, with quadratic Richardson extrapolation, agrees with the main route to
3e-7 at r w0 = 1 and 3; the exponential damping to 0.05-0.4%, as its linear convergence allows), and DERIVATION.md says
this supports but does not prove the limit is shape-independent; a new section maps the 12-diagram sum onto the helper `_u`
and `__main__` checks it against an independent enumeration of all 24 labelled four-vertex sequences (6.7e-16); working
precision grows above r w0 = 1e4 (the earlier ~1e-8 at 1e6 and ~3e-6 at 1e8 are gone), and the checked range is stated as
1e-4 <= r w0 <= 1e8 (the oracle now also holds it to 1e-7 down to 1e-8).

Open: a rigorous proof of the Abel-damping limit (supported by two damping shapes in each build and by the audit's three
regularizers); the intermediate-export contract change that would let the gate check the 12-diagram sum numerically.

## Contract change (class C): route enforcement, in progress

The audit's one high finding was that no numerical check could force SPEC section 2's route (mutant M1, the banned formula typed
in, passed every numerical check). The contract now has two more exports that exist only on the perturbation-theory route
(SPEC 3b): `denominator_sum(k, q, a, b)`, the sum over 24 orderings of four vertex events of 1/(E1 E2 E3) divided by 2, with
the two atoms' energies independent; and `damped_energy(r, w0, alpha0, eps)`, the fourth-order energy with every photon
integrand damped by exp(-eps (k+q)). The oracle checks them against references that share nothing with the builds: the
auditor's independent 24-ordering enumeration (agrees with build a's closed form to the double) and a separable double
integral by the orchestrator (`reference_damped.py`), which a degree-4 extrapolation to eps -> 0 matches to the main route
at r w0 = 1 to 1e-8 (-0.6512664067 against -0.6512664). A banned-route build cannot produce either quantity.

Status: closed. Both builders added the two exports (class C, no formulas given) and both builds pass the full strengthened
verifier, 36 checks each and no failures (`builds/verifier_report_contract_change.txt`):

* `denominator_sum`: matches the independent 24-ordering enumeration exactly (build a) and to 2e-16 (build b), with the two
  atoms' energies independent.
* `damped_energy`: both builds agree with the orchestrator's separable double integral to 6.1e-8 at worst (the same value for
  both, so it is the reference's own residual at (3, 0.5)), and with each other to ~1e-15 at three points, although they
  evaluate it differently (a: Gauss-Legendre panels and a quadrature over the Laplace variable; b: exact finite-eps shift of the
  Laplace integral with mpmath). Neither extrapolates in eps and neither uses the imaginary-frequency formula. Both observe the
  same approach to cp_energy, damped/cp_energy - 1 = -3.3 eps w0 at r w0 = 1, linear and from the weak side (build b at eps =
  1e-4 and 1e-5).
* `cp_energy` is identical to the previously accepted values.

One oracle bug (class R) was found on the way: my first reference scaling for w0 != 1 passed the wrong argument, which made
build a fail at the single w0 != 1 point; the fix is in the oracle and both builds then pass.

The audit's high finding (the gate could not force the route; mutant M1 passed every numerical check) is closed for these two
builds: a build using the Green-tensor formula cannot produce the 12-diagram denominator sum or the finite-eps double integral.
Still not enforced numerically: that cp_energy itself is computed from the diagrams (its link to the exports rests on the
derivations, which the audit read), and the Abel-damping limit remains supported, not proved.

## Isolation evidence

Transcript audit of both builders (`builds/a/isolation_audit.txt`, `builds/b/isolation_audit.txt`, with transcript hashes): no web,
delegation or MCP tool, no read of a file outside the room that the transcript did not create, no `cd` out of the room, no canary
token. Helper scripts and profiles were written to the shared session scratchpad (the environment instructs agents to use it) and
are accepted only because the same transcript created them. This is evidence after the fact, level 2 plus a transcript record; it
is not level 3 (a fresh machine). What the audit cannot show is in `../ISOLATION.md`.
