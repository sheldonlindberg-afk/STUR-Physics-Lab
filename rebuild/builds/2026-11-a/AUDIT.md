# Audit (red team): builds 2026-11-a and 2026-11-b

Auditor session, 2026-11-13, following `rebuild/prompts/auditor.md` for both builds. Build b's
`AUDIT.md` points here. *Subagents can't write in the repository, so the orchestrator wrote this file
from the auditor's report. The orchestrator applied the checks marked "landed" itself, after
re-running the self-test and both builds.*

The auditor read the LEDGER files, all 16 DERIVATION files, all 16 stage modules, both orchestrator
logs, FINDINGS.md, harness.py, contract.py, blind/checks.py, oracle.py and the reference adapter.
Every mutant was run in a scratch copy of the repository.

Severity:
- **HIGH:** an export is wrong or dishonest and nothing catches it.
- **MEDIUM:** a gate can't fail, or independence isn't shown. The builds themselves were checked by hand and are right.
- **LOW:** labels, documentation or weak evidence.

## HIGH: none open

No export in either build is wrong, and none is a typed or hidden answer. One thing would have made
this HIGH: evidence that build b's builders read build a's files (M6). **Resolved by the
orchestrator: the transcripts show they did not** (see M6).

### How constant-valued exports were shown to be computed

Some exports have a constant correct value, so their output can't show whether they were computed.
For each one, the auditor perturbed the primitive it says it uses and checked that the output moved.

| Export | Primitive perturbed | Build a | Build b |
|---|---|---|---|
| `goldstone_count` | `eigvalsh` | moved (3 → 0) | moved (3 → 0) |
| `action_coefficients` | `levi_civita` | moved | moved |
| `curvature_split_residual` | `spin_connection` | moved | moved |
| `ds_curvature_max` | `spin_connection` | moved | moved |
| `photon_sphere`, `isco` | `bisect` | moved | moved |
| `kerr_first_law` | `exact_derivative` | moved | moved |
| `quark_charges` | `exact_derivative` | moved | moved |
| `matter_charges` | `triplet_charges` | moved | moved |
| `ell_from_lambda` | `levi_civita` | moved | **did not move**: `sqrt(3/Lam)` typed after derivation (L3) |

`cp_integral` is computed by exact polynomial algebra in both builds.

## MEDIUM

| # | Finding | Status |
|---|---|---|
| M1 | **desitter's residual exports can't fail.** A stub `curvature_split_residual = ds_curvature_max = lambda *a: 0.0` passes every tier, the oracle included (blind/checks.py `split`, `vacuum`). In build a the Lorentz block cancels by construction; in build b it is a real comparison. Both compute the exports honestly. Fix: an `l_conn` argument on both exports (contract change) and a blind check that a wrong radius gives exactly \|1/l² − 1/l_conn²\|·max\|e∧e\|. | **Partly landed.** `flat_from_primitives` (below) builds F from the build's own `spin_connection` and `so41_generator`, so the de Sitter flatness is now gated independently of `ds_curvature_max`. The `l_conn` contract change awaits the owner. |
| M2 | **A wrong tetrad, or an ω tuned to the torsion check's θ = 1.1, passes the builder tier.** The torsion and `ricci_two_routes` checks use the build's own tetrad and ω. (The oracle catches both.) | **Landed:** blind `tetrad_metric` (e^T η e = the contract's metric at random points), blind `flat_from_primitives` (de Sitter F = 0 at random points, and F ≠ 0 with a wrong l), and the oracle compares `spin_connection` with the reference at 5 points. Mutants `test_wrong_tetrad_is_caught_by_blind_checks` and `test_omega_tuned_to_the_torsion_point_is_caught`. |
| M3 | **`kerr_first_law` has a constant correct value.** A stub returning (0, 0) passes every tier; the crossbuild probe compares 0 with 0. Both builds compute it, by an identical decomposition. Fix: a new export `kerr_terms` (contract change), with blind combination and limit checks and oracle BCH values. | **Awaits the owner** (contract change). |
| M4 | **The π⁰ width's dependence on m_π is checked nowhere.** A width that is right at `M_PI0` with the wrong power of m passes every tier, the oracle included. | **Landed:** blind `pi0_dimensions` (Γ = pure number · A²m³ by dimensional analysis). Mutant `test_pi0_mass_dependence_is_caught`. |
| M5 | **Provenance hides quoted dependencies (C2).** `casimir_safe_gap` and `design_phase` (the 2.19 rad headline) rest on the quoted `cp_energy`, and `planck_bh_kT_GeV` on the quoted `hawking_K`, yet are labelled "derived" without naming them. Build b reaches the Casimir-Polder formula through a private helper. Fix: a contract-tier rule, `tier_provenance_deps`; the builds then need three note edits each. | **Awaits the owner** (C2 was deferred to this audit). |
| M6 | **Second-build independence not shown.** Many shared routes and even shared private names (`_NEUTRAL`, `_scalar_X`, `_vev_slots`, `_lepton_X` with the same error string). b's room was on the same machine as build a's files (isolation level 2). If b read a, its "fully blind" claims would be void. | **Resolved by the orchestrator.** The transcripts of all nine build-b builder sessions were scanned (script `scratchpad/m6/scan.py`): every session ran on one model, and no tool call touched a path outside the room, build a, `src/`, the oracle or the web (the only `../` hits are `builds/2026-11-b/../..`, the room itself). The shared names are consistent with the same model family meeting the same SPEC wording. Build a's stage builders ran in an earlier session, so their model can't be checked here. Build c should use isolation level 3 and a different model family. |

## LOW

| # | Finding | Status |
|---|---|---|
| L1 | graviton's PPN check stated the stage's result (γ = 1) and missed the normalization: `point_mass_metric = (1, 1)` passed the builder tier. The light ratio 2 is arithmetic on SPEC §5's postulated P and is fair. | **Landed:** `ppn` replaced by `metric_from_propagator` (h = 16πG·Y·P·τ by two routes, no value). Mutant `test_point_mass_metric_normalization_is_caught_blind`. |
| L2 | gauge331's `photon_direction` and `inv_e2` are closed forms in both builds; M n = 0 pins the direction, only the oracle pins the normalization. The a/b agreement there is not evidence. | Open (build c: compute the null vector numerically). |
| L3 | Build b's `ell_from_lambda` returns `sqrt(3/Lam)`, typed after an honest derivation; build a computes the 3 as cV/(4cR). Weakens a/b independence on Λℓ² = 3. | Open (noted). |
| L4 | links' phase-space self-checks test only the δ-function's 1/2 Jacobian; the (2π) and 1/(2E) prefactors are typed identically in both routes. The oracle pins the value, and M4 now pins the m³ dependence. | Open (build c: integrate the full d³k₁d³k₂δ⁴). |
| L5 | Build a's LEDGER.md was stale (57 derived, no `ricci_scalar`). | **Fixed:** regenerated, 58 derived, 0 input, 7 quoted. |
| L6 | Build b's `kerr_first_law` note doesn't say the BCH S, T, Ω, J are quoted (build a's does). | Open (folds into M5). |
| L7 | Constant-valued exports (`goldstone_count`, `action_coefficients`, `unbroken_generators`, `cp_integral`, `point_mass_metric`, `photon_sphere`, `isco`, `qp_qe_minus_anomaly`) can only be told from typed answers by reading or perturbing the code. All are computed in both builds. | Open (keep the perturbation probe as an audit tool; it can't be a gate). |
| L8 | gauge331's charge check: q_p = 1 and Q_u − Q_d = 1 alone fix Q_u, so it doesn't force the anomaly route. Both builds use the anomaly. | Open (noted). |
| L9 | Build b's `green_tensor` is labelled derived but evaluates SPEC §4's postulated form; its note says so. | Open (noted). |

## What landed in this commit

- `rebuild/blind/checks.py`: `metric_from_propagator` (replaces `ppn`), `tetrad_metric`, `flat_from_primitives`, `pi0_dimensions`. None states an answer: each is a definition, a two-route identity or a dimensional law.
- `rebuild/oracle.py`: `spin_connection` compared with the reference at 5 points.
- `tests/test_rebuild_harness.py`: four mutants, each of which passed every relevant tier before and now fails.
- Gate: `pytest tests/test_rebuild_harness.py` 32 passed, 1 skipped; builds a and b `--mode verifier` ALL GATES PASS; crossbuild a/b 18/18.

The auditor's code for M1 (`l_conn`), M3 (`kerr_terms`) and M5 (`tier_provenance_deps`) was run in
the scratch copy: the reference passed, 36 tests passed, and shim updates of both builds passed
verifier mode with crossbuild 18/18. It is kept in `scratchpad/audit/` until the owner decides.
