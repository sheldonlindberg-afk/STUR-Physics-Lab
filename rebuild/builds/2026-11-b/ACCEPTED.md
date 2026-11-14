# Accepted: build 2026-11-b

Accepted 2026-11-13 by the orchestrator, following PROTOCOL.md P5. From now on
`tests/test_rebuild_harness.py::test_accepted_builds_stay_green` re-runs this build in verifier mode
on every push.

## Commits

| Phase | Commit |
|---|---|
| P1 toolkit, gauge331, chiral, casimir | 1f2b8ea, caf1bf2, 035377e, dfea68b |
| P1 graviton, desitter, blackholes, links; P3 | 0fc07e4, 30c7655, 76a5e96, 584b83c |
| P2 findings | facbada |
| P4 audit; audit checks landed | 05539b1 |
| M5 provenance notes; all gates pass | e479380 |
| Acceptance | this commit |

## Harness reports (re-run for acceptance)

| Command | Result |
|---|---|
| `python3 rebuild/harness.py rebuild/builds/2026-11-b --mode verifier --ledger` | **ALL GATES PASS**; oracle 1+18+7+6+5+10+21+8 = 76/76 |
| `... 2026-11-a --mode verifier --compare rebuild/builds/2026-11-b` (P3) | **crossbuild 18/18, ALL GATES PASS** |
| `... 2026-11-b --mode verifier --compare rebuild/_selftest/reference_build` | crossbuild 17/18; the one difference is F1 (N), the same place and size as build a |
| `python -m pytest tests/test_rebuild_harness.py -q` | 33 passed, 1 skipped (before this file existed) |

## Class counts (FINDINGS.md)

| B | R | C | N |
|---|---|---|---|
| 0 | 0 | 7 | 7 |

- Resolved: C1 (`ricci_scalar`), C2 (M5 rule), C3, C5, C6 (SPEC wording).
- Open by the owner's decision: C4, C7.
- **No class R finding.** F1, N2 and N3 are reference-side precision issues left to the owner.

## Ledger

58 derived, 0 input, 7 quoted (every quoted export on its stage's `quoted_allowed` list).

## Audit

See [../2026-11-a/AUDIT.md](../2026-11-a/AUDIT.md). No HIGH finding open; M1 and M3 open (owner's
decision). The auditor's M6 concern (did build b read build a?) was resolved by a transcript scan: no
builder tool call touched a path outside the clean room.

## Isolation and blindness

- **Level 2** (clean room in the session scratchpad, outside the repository; same machine as the repository).
- **Fully blind:** leaks 1-8 were closed before each affected stage was built. Each stage had its own
  fresh builder session, all on one model, different from the orchestrator's. No builder read build a,
  `src/`, the oracle or the web (transcript scan, ORCHESTRATOR_LOG_2026-11-b.md).
- Weaker independence where the SPEC fixes the route (toolkit algorithms, graviton's phase, links'
  conventions), or where both builds use the same closed form (gauge331's photon direction, the Kerr
  algebra). Build b's `ell_from_lambda` types √(3/Λ) after deriving it (audit L3).
- The provenance-note update ran as one builder session for the three stages (notes only, no code).

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
