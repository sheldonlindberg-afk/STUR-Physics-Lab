# Orchestrator log: build 2026-11-a

Kept by the orchestrator. It records anything that weakens the blindness or the gates, so the
verifier and auditor can weigh the results. Builders never see this file.

## Leaks found during the build

| # | What leaked | Where | Who could see it | Found by | Fixed |
|---|---|---|---|---|---|
| 1 | The exact fluctuation integral **23/4** and the entangling phase **2.19 rad** | SPEC.md line 5 ("no 2.19 rad, no 23/4") | the builders of toolkit, gauge331, chiral and casimir | the orchestrator, after the casimir builder reported leak 2 | yes, before graviton was built |
| 2 | A probe gap of **1.81e-4 m** (the Casimir-safe gap, to 3 digits) | harness.py, the crossbuild PROBES | the casimir builder, who reported it and says it didn't use it | the casimir builder | yes, before graviton was built (probe now 2.0e-4 m) |
| 4 | The relation **l = sqrt(3/Lambda)** (the result of rung 5's action) | harness.py sensitivity tier: `ell_from_lambda(3.0) == 1` | the desitter builder, who flagged it; it derived Lambda l^2 = 3 from exact eps contractions, (cR, cV) = (2, 24) | the desitter builder | yes, after build a (the sensitivity tier tests l(L)/l(4L) = 2; Lambda l^2 = 3 is now an oracle check) |
| 3 | **Closed forms** that are themselves derivation results: M_W², the leading-order M_Z² and M_Z'², 1/e² = \|n\|², the photon direction, and κ = \|f′\|/2 | blind/checks.py, which builders may read | the gauge331 builder (and the later blackholes builder) | the orchestrator | yes, after build a (moved to oracle.py; the blind checks now test neutrality, masslessness for random vevs, homogeneity, eigenvalue consistency, v and w scaling, κ ~ 1/M and the Euclidean period at the build's own κ) |

| 6 | The closed form **m_pi^2 = H/<sigma>** for `sigma_model_vacuum` | blind/checks.py (chiral `gmor_form`) | the chiral builder | the orchestrator, in the post-build grep | yes, after build a (blind check is now the Goldstone limit, m_pi^2 linear in H; the closed form is an oracle check) |
| 7 | The **Nariai bound l = sqrt(27) M**, as the sample `sds_horizons(1.0, sqrt(27 / 1.01))` | blind/checks.py (blackholes `horizons`) | the blackholes builder | the orchestrator, in the post-build grep | yes, after build a (the sample is now l = 5) |
| 8 | **Lambda l^2 = 3** again, in the contract's docstring for `mm_coupling` ("3/(lP^2 Lam)") | contract.py | every builder from desitter on (build a), and build b's toolkit and gauge331 builders | the orchestrator, while adding C1 | yes, before build b's desitter (now "l^2/lP^2, l = ell_from_lambda(Lam)") |

**Post-build grep (before build b).** Every builder-visible file (SPEC.md, contract.py, inputs.py,
harness.py, blind/, prompts/builder.md, README.md) was grepped for each number and closed form in
oracle.py: 246.2, 91.5, 127.6, 132.6, 1.414, 13.01, 23/4, 2.335, 181., 1.81, 2.18, 2.19, 1.647,
1.04e122, 1.0387, 4.26, sqrt(27, 8/9, 2.82, 7.78, 1.2208, 8.18, 2.180, 4.86, 47/77, f'/2,
sqrt(3/, 1/4M, 1 + beta, w^2/3, v^2/4, 8 pi, (2, 24), H/s0, 23/60, ell(3). The only hits left are
`1/(8 pi)` (the m = 0 Yukawa at r = 2, which SPEC's normalization fixes). The blind checks were
then read in full. Left for the auditor to judge: graviton's "light couples twice as strongly"
(ratio 2) and "PPN gamma = 1" are textbook results stated as checks; chiral's
"N_c(Q_u^2 - Q_d^2) = 1" follows algebraically from SPEC §2's two charge conditions.
**Effect on build a:** F1 stands: build a's `sigma_model_vacuum` computes m_pi^2 from a
Richardson-extrapolated `toolkit.hessian` (chiral.py, `_richardson_hessian`) and compares with H/s0
only in its self-test; the Nariai mass was found
by root-finding, but the bound was visible.

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
| blackholes | pass | 3/3 (rung 5 -> 6 twice, toolkit) | 18/18 | eb57db1 |
| links | pass | 3/3 (rung 1 -> links twice, rung 6 -> link 3) | 8/8 | (this commit) |
| **all stages** | **pass** | **15/15** | **55/55** | |

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
- **links:** neutrality needed is 2.8244e-19 e per nucleon (282x margin over the measured bound);
  the pi0 width is 7.7855 eV (-0.14 sigma from PrimEx); M_Pl = 1.22089e19 GeV; the G windows are
  0.122 to 5.6e14 (+1/sqrt3) and 2.8e-21 to 1.2e8 (-1/sqrt3); r_s = 2.180e-41 m = 1.349e-6 l_P;
  k_B T_H(M_Pl) = M_Pl c^2/(8 pi). **Blind:** the two closed forms that would have leaked
  (k_B T = M_Pl/8 pi and the G-window formula) were removed in e4cae14, before this builder started.

## First findings (for the verifier to confirm and classify)

| # | Check | Observation | Provisional class |
|---|---|---|---|
| F1 | crossbuild probe `chiral.sigma_model_vacuum(1.7, 0.9, 0.03)` against the reference adapter | differs by 1.03e-6 relative. The exact answer is m_pi^2 = H/sigma0: **the build is right to 1.4e-12, the reference is off by 1.0e-6** (its plain central-difference Hessian, h = 1e-4) | N; the reference is the less precise side. Not a physics error: every published number is unaffected. Fix (owner's call): Richardson in `src/ladder_standalone.py`'s rung 2 Hessian |
| F2 | provenance ledger | 57 derived, 0 input, 7 quoted; every quoted export is on its stage's allowed list | for the auditor to check each claim against the code |

## After P2 (verifier) on build a

- **Findings:** B 0, R 0, C 2, N 4 (FINDINGS.md). The verifier's write to FINDINGS.md was blocked by
  the tool layer; the orchestrator wrote it from the verifier's report, with the owner's approval.
- **C1, owner approved:** the export `desitter.ricci_scalar(M, l, x)` is added to the contract (SPEC §6
  says what it contracts, not its value). Blind check: it must equal the contraction of
  d omega + omega^omega built by finite differences of the build's own `spin_connection`, and scale as
  1/length^2. Oracle: 12/l^2 at three points. New probe and mutant. Build a's desitter lacks the
  export, so a fresh builder adds it to build a's desitter (class C rule: rebuild the affected stage
  in both builds). Its room held only build a's stages up to desitter.
- **C2, owner deferred** to the auditor.
