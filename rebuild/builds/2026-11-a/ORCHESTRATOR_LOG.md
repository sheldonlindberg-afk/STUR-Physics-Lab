# Orchestrator log: build 2026-11-a

Kept by the orchestrator. It records anything that weakens the blindness or the gates, so the
verifier and auditor can weigh the results. Builders never see this file.

## Leaks found during the build

| # | What leaked | Where | Who could see it | Found by | Fixed |
|---|---|---|---|---|---|
| 1 | The exact fluctuation integral **23/4** and the entangling phase **2.19 rad** | SPEC.md line 5 ("no 2.19 rad, no 23/4") | the builders of toolkit, gauge331, chiral and casimir | the orchestrator, after the casimir builder reported leak 2 | yes, before graviton was built |
| 2 | A probe gap of **1.81e-4 m** (the Casimir-safe gap, to 3 digits) | harness.py, the crossbuild PROBES | the casimir builder, who reported it and says it didn't use it | the casimir builder | yes, before graviton was built (probe now 2.0e-4 m) |
| 3 | **Closed forms** that are themselves derivation results: M_W², the leading-order M_Z² and M_Z'², 1/e² = \|n\|², the photon direction, and κ = \|f′\|/2 | blind/checks.py, which builders may read | the gauge331 builder (and the later blackholes builder) | the orchestrator | no: open for build b (move these comparisons into the oracle and keep only identities and limits in the blind checks) |

**How much this weakens the results:**
- casimir's 23/4 was computed from a symbolically constructed Tr G·G, the polynomial coefficients
  were generated rather than typed, and a quadrature confirms it. Knowing the target could still
  have guided the work, so this result counts as **not fully blind**.
- casimir's gap, 181.107 µm, is a bisected root that the oracle confirms lies one reference grid
  step below the reference's grid point, and its code contains no such literal. It was still
  visible to the builder, so it too counts as **not fully blind**.
- gauge331's mass matrix is built from the generators and agrees with the reference to 1e-12 on
  random parameters. Its closed-form *leading-order* masses were visible, though, so build b
  must not show them.

## Stage gates (run by the orchestrator, not the builder)

| Stage | Builder gate | Connections | Early oracle check | Commit |
|---|---|---|---|---|
| toolkit | pass | (none needed) | 1/1 | c8946ac |
| gauge331 | pass | 1/1 | 6/6 | 790b163 |
| chiral | pass | 1/1 | 5/5 | 9c717e7 |
| casimir | pass | 1/1 | 6/6 | (this commit) |
