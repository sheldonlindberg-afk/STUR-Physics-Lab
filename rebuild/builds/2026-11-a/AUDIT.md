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

## Addendum 2026-11-14: weak, running, and the derived f_pi (P4)

Auditor session, 2026-11-14, following `rebuild/prompts/auditor.md` for both builds, on what the
2026-11-14 extension added: stages `weak` and `running`, `chiral.chpt_mpi_from_rungs`,
`links.pi0_width_from_rungs` and `links.g_window_from_rungs`, and the framework changes that came
with them (`contract.py`, SPEC §9 and §10, `blind/checks.py`, `oracle.py`, `harness.py`, the
reference adapter, `tests/test_rebuild_harness.py`).

Everything was run in a scratch clone of the branch. 58 mutants (a control and 57 wrong
implementations) were appended to a copy of **each** build and run through the harness command line,
`--mode builder --stage <stage>` and `--mode verifier`, before and after the new checks: 232 mutant
directories, 464 harness runs. Builds a and b gave the same verdict on every mutant.

Severity as above.

### HIGH: none open

No new or changed export in either build is wrong, typed in or read from outside `inputs.py`.
Evidence beyond the harness:

- Both builds compute `b_331` and `sm_coefficients` by a sum over a multiplet list with exact
  Fractions (a: `running.py` 81-121; b: `running.py` 90-124). No coefficient is typed. Every X charge
  is solved from rung 1's `triplet_charges` and `quark_charges` at call time. The three scalar X
  charges are SPEC §2 postulates, typed as thirds in both.
- Both builds' `__main__` self-checks were run. Build a: explicit 4×4 trace equals
  4 m_l²(m_π² − m_l²) to 1e-16, smeared phase space converges to k*/(4π m_π), b_X equals a closed form
  in N_c for N_c = 1..9, the pole equals a bisection. Build b: explicit spinors and a matrix trace
  agree with the trace formula to 1e-15, all five gauge anomalies of its 3-3-1 content vanish for
  N_c = 1..7 in both variants, the embedding identity b_Y(matter) = β² b_L(matter) + b_X holds, RK4
  reproduces the running.
- Neither build reads `inputs.F_PI` or `inputs.POLES_331` in a new export (only in `__main__`
  printouts, for comparison).
- Derivation and code agree: every equation of the four DERIVATION files that I checked against the
  code (the width, its inversion, the b sums, the matching, the pole) is the one the code evaluates.
  The numbers the notes quote (26/3, 14, 58/3, 82/3; poles 4.470e29, 1.900e15, 5.335e19, 7.265e11 GeV;
  f_π 130.567 MeV) are the ones the code prints.

### MEDIUM

| # | Finding | Status |
|---|---|---|
| M7 | **The builder gate can't see a wrong U(1)_X or U(1)_Y coefficient.** `blind/checks.py` `running.exact` tested only that b_X is an exact Fraction, positive and growing with N_c, and never looked at b_L. Mutants that passed the builder gate in both builds: b_X × 0.9 (R01), singlet partners without colour (R02), no singlets (R03), no lepton singlets (R04), scalars as real fields (R05), scalars with the fermion weight (R06), one component per scalar triplet (R07), no scalars (R08), three lepton generations for every N_c (R09), triplet and antitriplet families swapped (R10), all families triplets (R11), b_X × 4/3 (R12), b_L without colour (R13), b_L with C₂ of SU(2) (R14), b_L variant dependent (R15), b_Y GUT-normalized (R30), no Higgs (R31). **The oracle catches all seventeen exactly**, so no accepted build is at risk; the gap is that a blind builder gets no signal. | **Partly landed.** New blind checks `bl_variants` and `bl_decoupling` kill R05, R06, R08, R13, R14, R15, R31 at the builder gate. R01-R04, R07, R09-R12 and R30 still need the oracle: I found no property of b_X that pins its normalization without stating the field content. **Awaits the owner:** a contract change (see "Open"). |
| M8 | **An input cached at import, or typed where the lint can't see it, passed every tier, the oracle included.** The new two-route checks compare an export with a recomputation at the published inputs, and the sensitivity tier moved only G_F, Γ, α⁻¹(M_Z), s² and MU_331. Survivors of all tiers in both builds: the 3-3-1 scale typed as `4e3` in the pole's prefactor (R23; one significant digit passes the lint, and the pole still moved with MU_331 through the matching), M_Z read at import (R33), V_ud, δ_π, m_μ, m_π read at import (W13), δ_π typed as `Fraction(176, 10000)` (W14; passes the lint), the FLAG inputs or stage weak's f_π kept from import in chiral (C03, C04), α and G cached in links (L04, L14), the poles cached at import in links with the spy satisfied (L15). | **Landed:** `harness.tier_perturbed` (reported in the sensitivity tier) re-runs eight named blind checks of `running`, `weak`, `chiral` and `links` with every input they read moved. All nine mutants now fail the builder gate. Mutant tests `test_inputs_cached_or_typed_in_fpi_are_caught`, `test_pole_with_a_typed_scale_and_cached_MZ_are_caught`, `test_derived_fpi_cached_at_import_downstream_is_caught`, `test_links_hand_offs_with_cached_inputs_are_caught`. |
| M9 | **A branch on an untested argument passed every tier.** b_X wrong for N_c ≥ 9 (R16; the oracle stopped at 7), the pole wrong for N_c = 7 (R24; blind and oracle used 3 and 5), the width wrong for m_l/m_π < 0.05 (W15; the oracle sampled 0.07-0.72 at one pion mass). | **Landed:** blind `pole` now runs N_c = 3, 5, 7, 9; the oracle compares b_331 at N_c = 9, 11, the N_c = 7 pole with src, and the width at 25 random points (any pion mass, m_l/m_π from 1e-4 to 0.999). Mutant tests `test_pole_tuned_to_the_tested_colours_is_caught`, `test_bX_wrong_beyond_the_tested_colours_is_caught_by_the_oracle`, `test_width_wrong_outside_the_old_oracle_range_is_caught`. |
| M10 | **The builder gate can't see the width's normalization or the f_π convention.** Width × 2 (W01), f_π in the 92 MeV convention (W02), (1 − m_l²/m_π²)³ (W07) and (1 − m_l/m_π)² (W08) passed every blind check: `roundtrip` inverts the same wrong formula. The oracle caught all four (and their knock-on in chiral and links). | **Landed, owner to confirm:** blind `convention`: f_π/√2 within 2% of the lattice `inputs.F_PI` (the derived value is 0.28% above it; the four mutants miss by 29% to 76%). It is a [data] check in the blind tier and uses only a number builders already see. Mutant tests `test_wrong_width_normalization_is_caught_blind` (was `..._needs_the_oracle`), `test_fpi_in_the_92_MeV_convention_is_caught_blind`. |
| M11 | **For the new rungs the two builds are one SPEC-fixed route coded twice, except in three places** (detail under "Second-build agreement"). The 25/25 crossbuild agreement shows that the arithmetic is right, not that the physics is independently confirmed. | Open (noted). Build c: a different model family and isolation level 3, as M6 said. |

### LOW

| # | Finding | Status |
|---|---|---|
| L10 | `pion_decay_width` is labelled derived in both builds, and the export evaluates the closed form typed after the derivation (a: `weak.py` 27-34; b: `weak.py` 27-50). The explicit trace and the phase-space integral that justify it live in `__main__` and are never run by the harness. Same class as L2 and L3. The notes say so honestly. | Open (noted). |
| L11 | The phase-space second routes of both builds integrate only the δ-function's Jacobian; the 1/(2E), (2π) and 1/(16π²) prefactors are typed in the route and in the result (a: `weak.py` `_smeared_phase_space`; b: `weak.py` route C). Same as L4. | Open (build c: integrate d³k d³q δ⁴). |
| L12 | **Leak review of what builders see** (SPEC.md, contract.py, harness.py, blind/checks.py, prompts/builder.md, inputs.py): no exact answer for the new stages (grep for the f_π value, the b coefficients, the poles, the π⁰ width, the pion mass: no hit). Two near-answers are in `inputs.py`: `F_PI` (0.28% below the derived f_π/√2) and `POLES_331` (the three-loop poles, a factor 1.4-2.0 below the one-loop ones). Neither passes a gate if returned (round trip, pole self-consistency, mutants L10, L11), but both let a builder tune towards the answer. Both builds print them beside their results in `__main__`. | Open (noted). |
| L13 | **The JSON report wrote some oracle verdicts as the string `"False"`.** The oracle compares with numpy floats, so `ok` was a `numpy.bool_`, which `json.dump(default=str)` turns into a string that reads as true. The exit code and the printed summary were right; a consumer of the report was not (my own mutant runner misread four failures before I saw it). | **Fixed:** `harness.run` stores plain bools. Test `test_report_json_has_real_booleans`. |
| L14 | SPEC §9's two readings (singlet partners per colour and per family; the 3-colour Standard Model below the 3-3-1 scale for every N_c) were written into the SPEC in de2fce7, **after** both running builds (890ab61, e5431c7). So the builds' agreement on the singlet counting is real evidence: a chose it as a reading, b because the anomalies cancel only with it. A later build no longer tests it. | Open (noted). |
| L15 | The Standard Model below the 3-3-1 scale is the 3-colour one also for N_c = 5. Both builds chose it for the same reason: `couplings_at(mu)` has no N_c argument, so the contract forces it. It matches src. It is a convention about a counterfactual, not a result. Also, `landau_pole` returns the scale where α_X = 1, a factor exp(2π/b_X) below the pole itself (SPEC-defined; build b's note says so). | Open (noted). |
| L16 | The connection spies are satisfied by a call whose value is thrown away (C01, L02, L10 call upstream and ignore it). The blind two-route checks catch all three, and with M8 the cached variants too. | Covered. |
| L17 | The new blind check `bl_decoupling` states a relation between two exports (b_L(N_c = 3) − b_2 = the gauge and scalar terms of SPEC §9's own formula). It gives no value, but it is closer to a closed form than the other blind checks. | Owner to confirm it is within the blind tier's leak policy; otherwise move it to the oracle. |

### Mutants: what caught each, before and after

Builder gate = contract, lint, blind, sensitivity, connections. Identical for builds a and b.

| Mutant | Before: builder gate | Before: oracle | After: builder gate | New check that kills it |
|---|---|---|---|---|
| R01 b_X × 0.9 | pass | fail | pass | (oracle only; M7) |
| R02 singlets without colour | pass | fail | pass | (oracle only; M7) |
| R03 no singlet partners | pass | fail | pass | (oracle only; M7) |
| R04 no lepton singlets | pass | fail | pass | (oracle only; M7) |
| R05 scalars real (1/6) | pass | fail | **fail** | blind `bl_decoupling` |
| R06 scalars weight 2/3 | pass | fail | **fail** | blind `bl_decoupling` |
| R07 one component per scalar triplet | pass | fail | pass | (oracle only; M7) |
| R08 no scalars | pass | fail | **fail** | blind `bl_decoupling` |
| R09 3 lepton generations for all N_c | pass | fail | pass | (oracle only; M7) |
| R10 n_A and n_T swapped | pass | fail | pass | (oracle only; M7) |
| R11 all families triplets | pass | fail | pass | (oracle only; M7) |
| R12 U(1)_X normalization, b_X × 4/3 | pass | fail | pass | (oracle only; M7) |
| R13 b_L without colour | pass | fail | **fail** | blind `bl_decoupling` |
| R14 b_L with C₂(SU(2)) | pass | fail | **fail** | blind `bl_decoupling` |
| R15 b_L variant dependent | pass | fail | **fail** | blind `bl_variants`, `bl_decoupling` |
| R16 b_X wrong for N_c ≥ 9 | pass | **pass** | pass | oracle: b_331 at N_c = 9, 11 |
| R20 exponent 4π | fail (blind pole) | fail | fail | already caught |
| R21 pole at 1/α = 0 | fail (blind pole) | fail | fail | already caught |
| R22 pole run from M_Z | fail (blind pole) | fail | fail | already caught |
| R23 prefactor typed 4e3 | pass | **pass** | **fail** | perturbed `pole` |
| R24 pole wrong for N_c = 7 | pass | **pass** | **fail** | blind `pole` at N_c = 7, 9; oracle N_c = 7 |
| R25 pole with b_L | fail (blind pole) | fail | fail | already caught |
| R30 b_Y GUT-normalized | pass | fail | pass | (oracle only; M7) |
| R31 no Higgs | pass | fail | **fail** | blind `bl_decoupling` |
| R32 matching with β² = 1 | fail (blind, connection) | fail | fail | already caught |
| R33 M_Z cached at import | pass | **pass** | **fail** | perturbed `sm_two_routes` |
| R34 running sign flipped | fail (blind) | fail | fail | already caught |
| W01 width × 2 | pass | fail | **fail** | blind `convention` |
| W02 f_π in the 92 MeV convention | pass | fail | **fail** | blind `convention` |
| W03 inversion without V_ud | fail (blind roundtrip) | fail | fail | already caught |
| W04 width ignores V_ud | fail (blind scaling) | fail | fail | already caught |
| W05 width linear in V_ud | fail (blind scaling) | fail | fail | already caught |
| W06 suppression to the power 1 | fail (blind helicity) | fail | fail | already caught |
| W07 suppression to the power 3 | pass | fail | **fail** | blind `convention` |
| W08 (1 − m_l/m_π)² | pass | fail | **fail** | blind `convention` |
| W09 no helicity suppression | fail (blind helicity) | fail | fail | already caught |
| W10 no radiative correction | fail (blind roundtrip) | fail | fail | already caught |
| W11 radiative correction multiplied | fail (blind roundtrip) | fail | fail | already caught |
| W12 neutral pion mass | fail (blind roundtrip) | fail | fail | already caught |
| W13 V_ud, δ, masses cached at import | pass | **pass** | **fail** | perturbed `roundtrip` |
| W14 δ typed as Fraction(176, 10000) | pass | **pass** | **fail** | perturbed `roundtrip` |
| W15 width wrong for m_l/m_π < 0.05 | pass | **pass** | pass | oracle: 25 random points |
| W16 f_π by a closed form, no width call | fail (connection W-fpi) | pass | fail | already caught |
| C01 input F_PI, spy satisfied | fail (blind) | fail | fail | already caught |
| C02 no √2 | fail (blind) | fail | fail | already caught |
| C03 FLAG inputs cached | pass | **pass** | **fail** | perturbed `chpt_rungs` |
| C04 derived f_π cached at import | pass | **pass** | **fail** | perturbed `chpt_rungs` |
| L01 π⁰ with input F_PI, no weak call | fail (blind, connection L2) | fail | fail | already caught |
| L02 π⁰ with input F_PI, spy satisfied | fail (blind) | fail | fail | already caught |
| L03 π⁰ with the charged pion's mass | fail (blind) | fail | fail | already caught |
| L04 α, m_π⁰ cached | pass | **pass** | **fail** | perturbed `pi0_rungs` |
| L10 window from POLES_331, spy satisfied | fail (blind) | fail | fail | already caught |
| L11 window from POLES_331, no call | fail (blind, connection L6) | fail | fail | already caught |
| L12 window ignores the variant | fail (blind) | fail | fail | already caught |
| L13 window from N_c = 3 and 7 | fail (blind) | fail | fail | already caught |
| L14 G cached | pass | **pass** | **fail** | perturbed `g_window_rungs` |
| L15 poles cached at import, spy satisfied | pass | **pass** | **fail** | perturbed `g_window_rungs` |

Counts (57 mutants): before, 33 passed the builder gate and 12 of those passed every tier. After,
12 pass the builder gate and **none passes every tier**. The 12 are the M7 group (R01-R04, R07,
R09-R12, R30) and the two argument-range branches (R16, W15), all caught by the oracle.

The suspicions the orchestrator listed, in order: b_X off by 10% passes the builder gate, oracle
only (confirmed, still so). Wrong family counting, wrong U(1)_X normalization, wrong scalar
contribution to b_X: same. A pole off by a factor in the exponent: caught blind. f_π off by √2:
passed the builder gate, now caught blind. Missing |V_ud|: caught blind. Wrong helicity factor:
power 1 caught blind, power 3 passed, now caught blind. π⁰ width with the input f_π: caught by the
blind two-route check; the spy alone catches it only if stage weak is not called at all.
`g_window_from_rungs` returning the POLES_331 window: caught blind and by the oracle.

### Second-build agreement

| Part | Independent? |
|---|---|
| weak: amplitude → Dirac equation → trace → two-body phase space | **Same route**, fixed by SPEC §10. Both arrive at Σ\|M\|² = 2G_F²V²f²m_l²(m_π² − m_l²) and code it, split differently. |
| weak: verification of the trace | **Independent.** a: 4×4 matrix trace in the Weyl basis. b: explicit u, v spinors in the Dirac basis, averaged over angle, plus a matrix trace. Not gated (L10). |
| weak: phase space | Same Jacobian argument and the same smeared-δ check (L11). |
| weak: inversion | Same (f² homogeneity, one call at f = 1): the W-fpi connection forces it. |
| weak: ħ conversion, 1 + δ_π | SPEC-fixed. |
| running: the one-loop formula, the SM table, the pole formula | SPEC-fixed, coded twice. |
| running: enumeration of the 3-3-1 content | **Independent code**, same charges (the R-content connection forces rung 1's). a: tuples of (X, charges, colours, copies). b: a typed field list. |
| running: singlet counting | **Independent choice**, made before the SPEC stated it (L14). a by reading, b by anomaly cancellation. **The choice is right:** b's `_anomalies_331` sums vanish for N_c = 1..7 in both variants only with it (run), and it equals src's field content exactly (oracle). |
| running: SM below the 3-3-1 scale for all N_c | Same choice for the same reason: the contract's signature forces it (L15). A convention, not evidence. |
| running: matching | Same idea in both (inv_e2 is affine in 1/g_X², two-point solve); the R-match connection forces the use of `inv_e2`. |
| running: second routes | Different. a: closed form in N_c, Euler steps, bisection. b: anomalies, the hypercharge embedding identity, RK4, bisection. b's are the stronger ones. |
| hand-off (chiral, links) | SPEC-fixed one-liners (f/√2), identical. |

Not run: a transcript scan of the extension's builder sessions (as was done for M6). ACCEPTED.md
states isolation level 2 for them.

### What the patch changes (`new_checks.patch`)

- `rebuild/blind/checks.py`: running `bl_variants`, `bl_decoupling`; `pole` over N_c = 3, 5, 7, 9;
  weak `convention`.
- `rebuild/harness.py`: `PERTURBED` and `tier_perturbed` (eight blind checks re-run with their inputs
  moved, reported under sensitivity); oracle verdicts stored as plain bools.
- `rebuild/oracle.py`: b_331 at N_c = 9, 11; the N_c = 7 pole against src; the width at 25 random
  points.
- `tests/test_rebuild_harness.py`: 13 new test functions, 14 cases (11 mutant tests, a pass test parametrized over the two
  accepted builds, a report-format test), and three existing tests updated for the new labels.
- No build file, no `src/` file and no SPEC or contract line is touched.

Gate after the patch: `pytest tests/test_rebuild_harness.py` 55 passed (41 before). Builds a and b
`--mode verifier`: ALL GATES PASS, each contract 87/87, lint 40/40, blind 88/88 (85 before),
sensitivity 20/20 (12 before), connections 17/17, oracle 98/98 (96 before). Builder mode: both pass.
Crossbuild a/b 25/25. The reference build passes through the test suite (`lint=False`).
The patch applies cleanly to the branch head (`git apply --check`, then 55 passed in a fresh clone).

### Open, for the owner

1. **M7, contract change.** Export the field content, e.g. `content_331(Nc, variant)` and
   `content_sm()` as lists of (kind, SU(3)_L or SU(2) dimension, colour dimension, copies, charge), and a
   generic `one_loop_b(C2, weyl, scalars)`, with a connection `b_331 → content_331, one_loop_b`. Blind
   checks could then require every gauge anomaly of the content to cancel (a postulate-level property
   that fixes the singlet counting, as build b found) and test `one_loop_b` on textbook cases
   (pure SU(N), QED, QCD with n_f flavours) without stating any 3-3-1 number. That would move R01-R04,
   R07, R09-R12 and R30 to the builder gate. It needs a rebuild of `running` in both builds. Not
   implemented.
2. **M10, L17.** Confirm that a 2% [data] anchor against `inputs.F_PI`, and the b_L/b_2 decoupling
   relation, are acceptable in the blind tier.
3. **L10.** Whether a "derived" closed form whose derivation is verified only in `__main__` should be
   gated (e.g. exports `spin_sum` and `two_body_phase_space`, checked blind against explicit matrices
   and a numerical integral). Contract change.

### Orchestrator's gate (after applying the auditor's patch)

Re-run by the orchestrator on the branch, not taken from the auditor's report:
`pytest tests/test_rebuild_harness.py tests/test_chain_vs_rebuild.py tests/test_force_chain.py` 65 passed;
builds a and b `--mode verifier --ledger` ALL GATES PASS (contract 87/87, lint 40/40, blind 88/88,
sensitivity 20/20, connections 17/17, oracle 98/98 each); `--mode builder` passes for both; crossbuild
a/b 25/25. No new check fails an accepted build. No HIGH finding; P4's gate is met. M7 (content
exports), the blind-tier policy for the two new anchors (M10, L17) and L10 are the owner's decisions.
