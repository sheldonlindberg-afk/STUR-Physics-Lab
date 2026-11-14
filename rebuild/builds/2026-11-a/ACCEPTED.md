# Accepted: build 2026-11-a

Accepted 2026-11-13 by the orchestrator, following PROTOCOL.md P5. From now on
`tests/test_rebuild_harness.py::test_accepted_builds_stay_green` re-runs this build in verifier mode
on every push.

## Commits

| Phase | Commit |
|---|---|
| P1, stages (first pass) | c8946ac, 790b163, 9c717e7, 84c09f7, 8289cae, b8e7f2a, eb57db1, fd9e2c0 |
| Leaks 3, 4, 6, 7 closed (framework) | 154bff4 |
| C1: `desitter.ricci_scalar` added (framework 6c4477e, build 728aafc) | 728aafc |
| P2 findings | caf1bf2 |
| P4 audit; audit checks landed | 05539b1 |
| C3/C5/C6 SPEC; M5 provenance rule (framework) | 59dd9e9 |
| M5 provenance notes; all gates pass | e479380 |
| Acceptance | this commit |

## Harness reports (re-run for acceptance)

| Command | Result |
|---|---|
| `python3 rebuild/harness.py rebuild/builds/2026-11-a --mode verifier --ledger` | **ALL GATES PASS**; oracle 1+18+7+6+5+10+21+8 = 76/76 |
| `... --mode verifier --compare rebuild/builds/2026-11-b` (P3) | **crossbuild 18/18, ALL GATES PASS** |
| `... --mode verifier --compare rebuild/_selftest/reference_build` | crossbuild 17/18; the one difference is F1 (N, the reference is the less precise side) |
| `python -m pytest tests/test_rebuild_harness.py -q` | 33 passed, 1 skipped (before this file existed) |

## Class counts (FINDINGS.md)

| B | R | C | N |
|---|---|---|---|
| 0 | 0 | 2 | 4 |

- C1 resolved (`ricci_scalar`). C2 resolved by the M5 rule.
- **No class R finding.** The reference-side precision issues (F1 Hessian, N3 safe-gap grid point and the 2.1868 rad pin, N2 ISCO search) are left to the owner; no published claim changes.

## Ledger

58 derived, 0 input, 7 quoted (every quoted export on its stage's `quoted_allowed` list).

## Audit (AUDIT.md)

No HIGH finding open. Open MEDIUM, by the owner's decision: M1 (desitter residual exports need
`l_conn` to be able to fail; de Sitter flatness is now gated by `flat_from_primitives`) and M3
(`kerr_first_law` has a constant correct value; `kerr_terms` proposed). Open LOW: L2, L3, L4, L6-L9.
Open class C from build b's verifier: C4 (`killing_kappa` oracle tolerance) and C7 (σ₀ not
oracle-tested).

## Isolation and blindness

- **Level 2** (clean room in the session scratchpad, outside the repository).
- **Not fully blind** for: casimir's 23/4 and safe gap (leaks 1 and 2); desitter's Λℓ² = 3 (leaks 4 and 8)
  and therefore its later `ricci_scalar` = 12/ℓ²; gauge331's leading-order closed forms and blackholes'
  κ = |f′|/2 (leak 3); chiral's m_π² = H/⟨σ⟩ (leak 6); the Nariai bound (leak 7). In every case the code
  computes the result rather than typing it (verifier and auditor). See ORCHESTRATOR_LOG.md.
- The model of the first-pass stage builders was not recorded; the `ricci_scalar` and provenance-note
  updates ran on the orchestrator's model.

## Addendum, 2026-11-14: two new rungs, and the derived f_pi

Owner-approved extension. New stages `weak` (f_pi from G_F and Gamma(pi -> mu nu)) and `running`
(one-loop 3-3-1 running to the Landau poles), each written by a fresh blind builder; then one builder
session moved chiral's O(p^4) pion mass and links' pi0 width onto the derived f_pi and added
`g_window_from_rungs`. Re-run for re-acceptance:

| Check | Result |
|---|---|
| `--mode verifier --ledger` | **ALL GATES PASS**, 10 stages; 66 derived, 0 input, 8 quoted |
| crossbuild a/b | **25/25** |
| crossbuild against the reference adapter | 24/25 (F1 only, as before) |
| `rebuild/chain_compare.py` (the force chain) | **22/22 overlaps agree** |
| `pytest tests/test_rebuild_harness.py tests/test_chain_vs_rebuild.py tests/test_force_chain.py` | 51 passed |

What the new rungs derive: f_pi = 130.5674 MeV (both builds identical; `src` to 3e-10); the pi0 width
7.7417 eV (was 7.7855 eV with the lattice f_pi input), the O(p^4) pion mass 132.29 MeV (was 132.65);
one-loop poles, and with them the N_c = 3 selection, for both variants (+1/sqrt3: 5.34e19 and
7.27e11 GeV; -1/sqrt3: 4.47e29 and 1.90e15 GeV, 1.4-2x the quoted three-loop values). `POLES_331`
remains a quoted input only for `g_window` itself. Isolation level 2, as before; the new stages' rooms
held no findings, audit, log or acceptance files.
