# Accepted: campaign `greybody` (Hawking emission power per degree of freedom)

*Result: the energy emitted per degree of freedom by a Schwarzschild black hole, for spins 0, 1/2, 1 and 2, derived from the
Regge-Wheeler and Chandrasekhar master equations (grey-body factors from the horizon solution matched to the large-r
asymptotic series, Bose/Fermi occupation at T = 1/8 pi): P_s = 7.43869e-5, 4.09165e-5, 1.68193e-5, 1.91837e-6 in units
1/M^2. They reproduce Carr et al.'s quoted weights to their digits (0.2664, 0.1465, 0.0602, 0.00687 against 0.267, 0.147,
0.060, 0.007) and an independent solver to 1e-9.*

| Phase | Evidence |
|---|---|
| P0 clean rooms | Level 2 of PROTOCOL.md section 3. **Caveat:** both rooms shared a filesystem with the repository, where the literature weights (L7) and the orchestrator's own scratch solver (`scratchpad/orch/gb_check.py`, written before the rooms) were readable; the audit found no sign of copying, but independence relied on the agents' compliance |
| P1 builders | `builds/a` (Opus), `builds/b` (Sonnet); each passed `gate.py --mode builder` |
| P2 verifier | the orchestrator ran `gate.py --mode verifier` with the hidden oracle on each build, first with the original gate and again after the audit's strengthening: `builds/*/verifier_report.txt` (all tiers PASS, including the exact low-frequency coefficients, the gate's own assembly of P_s from `transmission`, P_s against the two-route values to 1e-5, and Gamma at 40 reference points to 1e-4) |
| P3 cross-build | `cross_build_comparison.txt`: Gamma agrees to 4e-9 at ten (s, j, w); P_s to 2e-9, 2.5e-8, 2.3e-8 and 3.4e-7 |
| P4 audit | `AUDIT.md` (Opus auditor with an independent series-free solver, `audit_indep_solver.py`; eight mutants): verdict ACCEPT the result; one **high** finding against the gate, not the builds |
| Gate strengthening | the audit's two blind and two oracle checks, adopted in `campaign.py` / `oracle.py`; six of the audit's eight mutants passed the old gate and are killed by the new one |

## Class counts

B (builder bug): 2, both recorded, neither blocking: build b's fermion Gamma is wrong by up to 1.4e-4 relative at low w
(horizon start without a sqrt(f) correction; P_1/2 moves by 2.5e-8); build a clips Gamma to 1 without saying so (126 of
3886 power-grid evaluations, values 1 + 1e-10). R (oracle bug or weakness): 1, high: the original oracle accepted -1.3% to
+1.7% on spin 0, -2.4% to +1.6% on spin 1 and +-6% on spin 2 (fixed by the sharper targets). C (spec change): 0. N: the
low-frequency fermion Gamma of build a is accurate to about 1e-7 rather than 1e-10.

## What is and is not established

* **Established:** both builds, an independent third solver and the exact low-frequency limits agree; the master equations,
  the flux identity, the occupation signs, T, the 1/(2 pi), j >= s and the (2j+1) degeneracy were each checked in the audit.
* **Not established:** the gate cannot enforce the route. A build that typed in correct high-precision numbers while labelled
  "derived" (the audit's mutant M0) passes every numerical check; only reading DERIVATION.md catches it, and the auditor did.
  The two builds use the same method (outward from the horizon, the same asymptotic series), so their agreement checks the
  implementations; the auditor's WKB-projection solver is what makes the agreement meaningful.
* **Open follow-ups:** build b's fermion horizon boundary condition; build a's undocumented clip and wording; the charged
  spin-1/2 weight of Carr et al. (0.142 against 0.147) is not reproduced by massless grey-body factors (Link 24, FOLLOWS).

## Revision after acceptance: build b returned to its builder

The audit's medium finding on build b (fermion Gamma wrong by up to 1.4e-4 at low w) was turned into a gate check: the
oracle's Gamma set now has 46 reference points, six of them low-frequency fermion partial waves computed with the
auditor's independent solver, at tolerance 1e-6 (was 40 points at 1e-4). Build a passes it (worst 9.7e-8 at
(1/2, 1/2, 0.002)). **Build b fails it** (worst 1.4e-4 at (1/2, 7/2, 0.02)), so build b is not accepted under the stricter
gate until its builder fixes it (class B, label only; see the log below). The ladder (Link 24) uses build a and P_s agrees
between a, b and the auditor's solver to 3e-7 or better, so Link 24 does not depend on this fix.

| Step | Result |
|---|---|
| Tightened oracle, build a | PASS (9.7e-8) |
| Tightened oracle, build b | FAIL (1.4e-4), returned to builder |
