# Orchestrator log: build 2026-11-b

Kept by the orchestrator, outside `builds/2026-11-b/` so `cleanroom.py export` never copies it into
the room. Builders never see it.

**Isolation:** level 2 (clean room in the session scratchpad, outside the repository). Each stage has
its own fresh builder session, run on a different model from the orchestrator and from build a's
desitter update, with no information about build a. Framework state at the start: leaks 1-8 closed
(see build a's log), SPEC folded with build a's resolutions, C1 (`ricci_scalar`) added before desitter.

## Stage gates (run by the orchestrator)

| Stage | Builder gate | Connections | Early oracle check | Commit |
|---|---|---|---|---|
| toolkit | pass | (none needed) | 1/1 | 1f2b8ea |
| gauge331 | pass | 1/1 | 18/18 | caf1bf2 |
| chiral | pass | 1/1 | 7/7 | 035377e |
| casimir | pass | 1/1 | 6/6 | dfea68b |
| graviton | pass | 2/2 | 5/5 | 0fc07e4 |
| desitter | pass | (none; rung 6 calls it) | 10/10 | 30c7655 |
| blackholes | pass | 3/3 | 21/21 | 76a5e96 |
| links | pass | 3/3 | 8/8 | (this commit) |
| **all stages** | **pass** | **15/15** | **76/76** | |

## Notes per stage

- **gauge331:** the builder's report was lost in a container restart; its files and QUESTIONS.md
  survived and the gate was re-run by the orchestrator. `photon_direction` is the closed form
  (1/g, beta/g, 1/gX) after a short derivation, as in build a, so the a/b agreement on it is weak evidence.
- **chiral:** `sigma_model_vacuum` finds sigma0 by `toolkit.bisect` and returns m_pi^2 = H/sigma0 from
  its own analytic Hessian (the blind check no longer shows that form; leak 6 was closed first).
  The Hessian route is in its self-check. The a/b probe should agree to rounding; both differ from the
  reference's 1e-6 (F1).
- **casimir (fully blind):** 23/4 computed by exact polynomial algebra, with a trapezoid route; safe gap
  1.811072783e-4 m by `toolkit.bisect` on a derived bracket. Neither 23/4 nor the gap was visible to
  this builder (leaks 1 and 2 were closed before build b). `cp_energy` is tagged quoted (the CP formula),
  the r^-7 reduction derived. Spec gap noted: SPEC §4 doesn't state the gravity potential used in the
  safe-gap ratio (the builder used -G m^2/r, as the blind check does).
- **graviton (fully blind):** design_phase = 2.187786760330193 rad at its own Casimir root, the same as
  build a's 2.18779 and the verifier's mpmath 2.187786760309 (to 1e-11, the trapezoid error). The
  exchange normalization (1/2 h T with 16 pi G) is now in SPEC §5 and was not guessed. PPN gamma = 1 and
  the light ratio 2 were visible as blind-check targets (see build a's log, auditor's call).
- **desitter (fully blind; the first build to derive Lambda l^2 = 3 without seeing it):** leaks 4 and 8
  were closed before this builder. It got (cR, cV) = (2, 24) under the SPEC §6 epsilon convention (no
  sign ambiguity this time), Lambda l^2 = 3 from the action reduced to e(R - 6/l^2), a second route
  R l^2/4 = 3, and ricci_scalar = 12/l^2 in closed form. l = 1.647258e26 m, coupling 1.038732e122.
  Spec gap for the verifier: SPEC §6 never says that Lambda means the constant in e(R - 2 Lambda);
  the builder assumed it (QUESTIONS, desitter 2).
- **blackholes (fully blind; leaks 3, 5 and 7 closed before it):** the first builder hit an API rate
  limit before writing anything, and a fresh one was started. Photon sphere 3M, b_c = sqrt(27) M and the
  ISCO (6, 12, 8/9) were found numerically, golden-section search polished by bisection on exact
  derivatives. The Nariai mass G M/c^2 = l/sqrt(27) was derived analytically from f = f' = 0 (no longer
  visible in the blind checks). Kerr first law and Smarr are exactly 0. EHT pulls -0.40 and +0.16;
  GW250114 220-mode pulls +0.33 and +0.59, all the same as build a.
  For the verifier: `killing_kappa` returns the value at the sample point, not extrapolated (same SPEC
  reading as build a?); the `kerr_*` provenance labels (C2); `euclidean_cone_ratio` uses 200 trapezoid nodes.
- **links (fully blind):** neutrality 2.8243652699e-19 e per nucleon; pi0 width 7.785499435771721 eV
  (-0.14 sigma); M_Pl = 1.2208901282e19 GeV; k_B T_H(M_Pl) = 4.857767471917444e17 GeV, all as build a.
  pi0 widths tagged quoted, the rest derived.

## P3: cross-build

`python3 rebuild/harness.py rebuild/builds/2026-11-a --mode verifier --compare rebuild/builds/2026-11-b`:
**crossbuild 18/18, RESULT: ALL GATES PASS.** Every probe agrees to 1e-8, the new `ricci_scalar` probe
included. Against the reference adapter build b gives 17/18, the one failure being F1
(`chiral.sigma_model_vacuum`, 1.03e-6), the same as build a: two independent builds agree with each
other and disagree with the reference in the same place, by the same amount.
