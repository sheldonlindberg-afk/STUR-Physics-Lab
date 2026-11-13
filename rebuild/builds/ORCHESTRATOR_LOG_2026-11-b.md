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
| chiral | pass | 1/1 | 7/7 | (this commit) |

## Notes per stage

- **gauge331:** the builder's report was lost in a container restart; its files and QUESTIONS.md
  survived and the gate was re-run by the orchestrator. `photon_direction` is the closed form
  (1/g, beta/g, 1/gX) after a short derivation, as in build a, so the a/b agreement on it is weak evidence.
- **chiral:** `sigma_model_vacuum` finds sigma0 by `toolkit.bisect` and returns m_pi^2 = H/sigma0 from
  its own analytic Hessian (the blind check no longer shows that form; leak 6 was closed first).
  The Hessian route is in its self-check. The a/b probe should agree to rounding; both differ from the
  reference's 1e-6 (F1).
