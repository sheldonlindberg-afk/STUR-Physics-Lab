# Accepted: campaign `induced_g` (Newton's constant induced by quantum fields at one loop, proper-time cutoff)

*Result: two blind builds (Opus a, Sonnet b) derived the per-field heat-kernel coefficient k₁ = b₁/R as a function of the
dimension d: 1/6 − ξ (real scalar), −2^⌊d/2⌋/12 (Dirac), half that (Weyl), (d − 6)/6 (vector without ghosts) and
(d − 8)/6 (vector with its Faddeev–Popov ghosts). They also derived the induced coupling in d = 4,*
***1/G = (κ²/2π) [n_s(1/6 − ξ) + n_w/6 − 2n_v/3]**:
*with the proper-time cutoff of the SPEC, minimally coupled scalars and fermions induce attractive gravity and gauge vectors
repulsive. Both builds checked the k₁ values against the exact spectra of the Laplacians on a round S⁴. Build a also
obtained the sign from the effective action itself, mode by mode. The auditor confirmed the sign and every k₁ by a third
route that uses no heat-kernel formula, no determinants for statistics and no ghosts: the zero-point energy of the physical
modes on the Einstein static universe R × S³.*

| Phase | Evidence |
|---|---|
| P0 clean rooms | Level 2 of PROTOCOL.md section 3, one room per build outside the repository |
| P1 builders | `builds/a` (Opus), `builds/b` (Sonnet); each passed `gate.py --mode builder` |
| P1 isolation | `builds/*/isolation_audit.txt`: transcript audit with every campaign canary, clean (SHA-256 of each transcript recorded) |
| P2 verifier | `gate.py --mode verifier` with the hidden oracle and the audit's seven adopted checks: `builds/*/verifier_report.txt`, all 11 oracle checks PASS |
| P3 cross-build | 362 probes (k₁ for every kind, d = 2–12, four ξ; 1/G and mpl on a 3 × 3 × 3 × 3 × 3 grid): worst relative difference 1.7×10⁻¹⁵, and the same None cases |
| P4 audit | `AUDIT.md`: an independent route on R × S³, 30 mutants of build a (28 wrong, 1 equivalent, 1 typed-in closed form). 20 of the 28 were killed by the first gate, all 28 by the adopted checks |
| Gate self-test | before the builds: a reference build with the overall sign reversed passed every blind check and failed three oracle checks |

## Class counts
- **B:** 2, in prose only, with the code right.
  - Build a writes the gauge-fixing term with the wrong sign in its prose; the operator it uses is right.
  - Build b's "radius route" is unfinished prose, so build b's statistics and matching signs rest on its main
    derivation. The auditor's route confirms them.
- **R:** 3 coverage gaps, closed by the adopted checks. The oracle sampled d ≤ 10 only, ξ on the scalar only, and never
  Weyl at odd d or mpl at 1/G = 0; one blind check accepted a d-independent vector; LINT_EXACT cannot catch a typed-in
  closed form. No oracle value was wrong.
- **C:** 4 SPEC wording gaps, clarified in SPEC.md without changing its meaning for either build: the ghost count and
  operator, ξ for non-scalar kinds, Weyl at odd d, and C2: the sign "follows from the conventions" only because the
  conventions include the proper-time regulator.
- **N:** 3, harmless. An exact cancellation gives −1.8×10⁻¹⁷ κ² in build b against 0 in build a (both mpl = None); build
  a's own W(κ) fit has a 2×10⁻⁸ residual; one mutant is equivalent.

## What is and is not established
* **Established (within the SPEC):** every k₁ as a function of d, the ghost count (forced: on R × S³, Feynman gauge with
  two ghosts reduces mode by mode to the transverse photons), and the induced 1/G with its sign **for the proper-time
  cutoff**.
* **The regulator fixes the sign and the factor** (AUDIT.md §1d). For a regulator ρ(κ²t) the κ² term is proportional to
  ∫ρ(u)/u² du: +1 for the proper-time cutoff. A positive cutoff on mode energies flips every sign and rescales the value
  (Gaussian −2×, exponential −4×); dimensional regularization has no κ² term; Pauli–Villars gives either sign. What is
  universal is the weighting 1 : 1 : −4 (scalar : Weyl : vector) for a common regulator. Physically the sign of induced G
  belongs to whatever completes the theory above the cutoff, so a statement that "matter induces attractive gravity"
  must carry the qualifier "with a proper-time (heat-kernel) cutoff".
* **Shared assumptions of all three routes:** one cutoff for all fields, no tree-level 1/G₀, no graviton loop, massless
  fields, d = 4 for 1/G.
* **Gauge fields and Kabat's contact term:** on a smooth manifold the vector's −tr Ric is an ordinary bulk term. The
  auditor's route gets −2/3 from physical photons alone, so the negative vector contribution to 1/G is not a ghost
  artefact. What fails without the contact term is "entanglement entropy = A/4G_induced", which nothing here uses.
* **Independence:** the builders and the auditor are language models that may know the standard heat-kernel
  coefficients. The independence evidence is the isolation record and the three different routes, not ignorance of the
  literature.

## Where it is used
Build a is embedded verbatim, minus its numpy-only second-route helpers, as stage `induced_g` of the merged chain
`src/chain_first_principles.py` (tools/build_chain_standalone.py). Step 1 uses it to induce gravity's scale from stage 1's
own fields at the U(1)_X pole, and checks the measured G against that band (INDUCED_GRAVITY.md).
