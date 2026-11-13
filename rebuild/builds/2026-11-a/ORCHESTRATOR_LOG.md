# Orchestrator log: build 2026-11-a

Kept by the orchestrator. It records anything that weakens the blindness or the gates, so the
verifier and auditor can weigh the results. Builders never see this file.

## Leaks found during the build

| # | What leaked | Where | Who could see it | Found by | Fixed |
|---|---|---|---|---|---|
| 1 | The exact fluctuation integral **23/4** and the entangling phase **2.19 rad** | SPEC.md line 5 ("no 2.19 rad, no 23/4") | the builders of toolkit, gauge331, chiral and casimir | the orchestrator, after the casimir builder reported leak 2 | yes, before graviton was built |
| 2 | A probe gap of **1.81e-4 m** (the Casimir-safe gap, to 3 digits) | harness.py, the crossbuild PROBES | the casimir builder, who reported it and says it didn't use it | the casimir builder | yes, before graviton was built (probe now 2.0e-4 m) |
| 4 | The relation **l = sqrt(3/Lambda)** (the result of rung 5's action) | harness.py sensitivity tier: `ell_from_lambda(3.0) == 1` | the desitter builder, who flagged it; it derived Lambda l^2 = 3 from exact eps contractions, (cR, cV) = (2, 24) | the desitter builder | no: open for build b (test the scaling l ~ Lambda^-1/2 instead) |
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
| casimir | pass | 1/1 | 6/6 | 84c09f7 |
| graviton | pass | 2/2 (rung 2 -> 4, rung 3 -> 4) | 5/5 | 8289cae |
| desitter | pass | (none; rung 6 calls it) | 6/6 | b8e7f2a |
| blackholes | pass | 3/3 (rung 5 -> 6 twice, toolkit) | 18/18 | (this commit) |

## Notes per stage

- **graviton (first fully blind stage after the leak fixes):** design_phase = 2.18779 rad at the
  build's own Casimir root, 181.107 µm. The reference's 2.1868 rad is computed at its grid point,
  181.16 µm, and the build reproduces it there to within 5e-4. The 0.045% difference is the
  reference's grid choice (class N), not physics. The builder also derived the small-separation
  limit, with ∫up² = 23/60 exactly, and showed Δφ is the only phase combination invariant under
  local branch phase shifts. Spec gap to close for build b: the ½hT matter coupling that
  normalizes "amplitude ∝ T·P·T" is not written in SPEC §5 (QUESTIONS, graviton 3).
- **desitter:** l = 1.6473e26 m and coupling 1.0387e122 from the measured Lambda. (cR, cV) = (2, 24)
  exactly, from literal eps contractions. **Not fully blind for Lambda l^2 = 3** (leak 4).
  Spec gap for build b: the eps sign convention (eps_0123 = +1 and eps^0123 = +1) is not fixed,
  so a second build could get (-2, -24) and fail the cross-build probe on sign alone. The
  builder also notes two checks that are weak by construction: cR = 2 is insensitive to a wrong
  R^ab when the tetrad is diagonal, and the Lorentz block of the split residual is nearly an
  identity. Auditor: strengthen both (e.g. an off-diagonal tetrad, and R^ab checked against the
  metric's curvature).
- **blackholes:** the photon sphere (3M), b_c = sqrt(27) M, the ISCO (6M, L^2 = 12, E^2 = 8/9) and the
  Nariai mass (4.2689e52 kg) were all found numerically, and the closed forms appear only in the
  self-check. The Kerr first law and Smarr come out as exact Fraction(0). EHT pulls: M87* -0.40,
  Sgr A* +0.16. GW250114: A_f/A_i = 1.71 (ringdown M_f = 66.7, chi = 0.746). The 220 mode
  predicted from the full-signal remnant has pulls +0.33 and +0.59.
  **Partly not blind:** the formula kappa = |f'|/2 was visible in the blind checks (leak 3). The
  Nariai closed form was removed before this build (66e64f7).
  Spec gaps for build b: the damping-rate unit (s^-1, labelled "Hz"), the pull convention for
  Sgr A*, and the Kerr q = 0 limit of Omega dJ.
