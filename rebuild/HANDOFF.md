# Handoff: after build 2026-11-a's first pass

*For the next orchestrating agent. Read this, then [PROTOCOL.md](PROTOCOL.md) and
[builds/2026-11-a/ORCHESTRATOR_LOG.md](builds/2026-11-a/ORCHESTRATOR_LOG.md). This file contains
answers, so it must never be copied into a clean room (`cleanroom.py` doesn't copy it).*

## Where things stand

**Phase P1 is done for build `2026-11-a`.** Each of the eight stages was written by its own
fresh, blind builder agent in a clean room outside the repository (isolation level 2), and
then gated by the orchestrator, not by the builder.

| | Result |
|---|---|
| Builder gate (contract, lint, blind, sensitivity, connections) | **all 8 stages pass** |
| Connections (the rungs call each other) | **15/15** spy checks, covering all 11 links in `contract.CONNECTIONS` |
| Early oracle check against `src/ladder_standalone.py` | **55/55** |
| Probe comparison against the reference adapter | 16/17. F1: the build is more precise than the reference |
| Provenance ledger | 57 derived, 0 input, 7 quoted (all on the allowed lists) |

**Not done yet:** P2 (the verifier session and FINDINGS.md), P3 (build b and the a/b
cross-build), P4 (the audit) and P5 (acceptance). `ACCEPTED.md` doesn't exist, so CI does
not yet re-run this build.

## How blind build a is

Five leaks were found while building. See the log for who could see what.

| Leak | Fixed? | Affected results in build a |
|---|---|---|
| 1. SPEC.md named 23/4 and 2.19 rad | yes (before graviton) | casimir's 23/4 |
| 2. a probe gap of 1.81e-4 m in harness.py | yes (before graviton) | casimir's safe gap |
| 3. closed forms in blind/checks.py (M_W², leading-order M_Z² and M_Z'², 1/e², the photon direction, κ = \|f′\|/2) | **no** | gauge331's leading-order masses and coupling; blackholes' κ |
| 4. `ell_from_lambda(3) == 1` in harness.py's sensitivity tier | **no** | desitter's Λℓ² = 3 |
| 5. the closed forms of the Nariai mass, k_BT(M_Pl) and the G window, in blind/checks.py | yes (before blackholes and links were built) | none |

So build a is **blind except for** casimir's 23/4 and gap, desitter's Λℓ² = 3, gauge331's
leading-order closed forms, and blackholes' κ formula. In every one of those cases the code
computes the result rather than typing it in, but the builder could see the target.

## Do these before build b (in this order)

1. **Close leaks 3 and 4.**
   - In `blind/checks.py`, keep only identities, limits, symmetries and scaling. Move every
     comparison with a closed-form derivation result into `oracle.py`: in `gauge331`, the
     `masses` and `photon_form` closed forms; in `blackholes`, `kappa_two_routes` and the
     `euclid` use of f′/2. Replace each with a builder-visible *property*, for example "M n = 0
     for the returned n" (already present), "the Killing κ equals the spin-connection κ"
     (already present), or "the Euclidean ratio is 1 at the returned period".
   - In `harness.py`, `tier_sensitivity` for desitter: test ℓ ∝ Λ^(−1/2) (a ratio), not
     ℓ(3) = 1.
   - Then grep every builder-visible file (SPEC.md, contract.py, harness.py, blind/,
     prompts/builder.md) for each oracle number and closed form. The grep used for this
     build is in the log.
2. **Fold the builders' resolutions into SPEC.md** (from builds/2026-11-a/QUESTIONS.md),
   so build b doesn't have to guess:
   - §2: the "remaining neutral component" rule for β = −1/√3 (the third scalar is neutral
     in components 1 and 3; v₂ takes component 1). Also that the X passed to
     `triplet_charges(…, anti=True)` is the antitriplet's own charge.
   - §5: the matter coupling ½h_μνT^μν, which fixes the normalization of "∝ T·P·T". The
     clamp in the branch profile applies to x before up(x).
   - §6: the ε sign convention, ε₀₁₂₃ = +1 and ε̃^{0123} = +1. Without it, build b may get
     (cR, cV) = (−2, −24) and fail the cross-build on sign alone.
   - §7: damping rates are in s⁻¹; the pull convention; Sgr A* takes the mean of the two
     θ_g values; at q = 0 Kerr uses the finite limit of Ω dJ.
   - toolkit: the Hessian's h is absolute, and callers scale it.
3. **Re-run `python -m pytest tests/test_rebuild_harness.py`.** Every change above must keep the
   reference passing and the mutants failing. Add a mutant for each new oracle check.
4. **Build a is not rebuilt.** Its results stand, with the blindness caveats above. Build b
   is the first build made entirely under the closed framework.

## Then continue the protocol

- **P2 verify build a:** start a fresh verifier session with `prompts/verifier.md`. It should
  confirm F1 (class N, the reference is less precise; any fix to `src/` is the owner's
  decision) and triage everything else.
- **P3 build b:** `python3 rebuild/cleanroom.py export <scratchpad>/room-2026-11-b 2026-11-b`.
  Use fresh builders, one per stage, with no information about build a. Ideally use a
  different model, or at least different phrasing. Then run
  `python3 rebuild/harness.py rebuild/builds/2026-11-a --mode verifier --compare rebuild/builds/2026-11-b`.
- **P4 audit both builds** with `prompts/auditor.md`. Known weak checks to strengthen:
  - desitter's cR = 2 can't detect a wrong R^ab when the tetrad is diagonal;
  - the Lorentz block of its split residual is nearly an identity;
  - the links phase-space numerical check only tests the δ-function Jacobian.
- **P5 accept:** write `ACCEPTED.md` as PROTOCOL.md P5 describes. CI then re-runs the build on
  every push.

## Prompt for the next orchestrator

> Read rebuild/HANDOFF.md, rebuild/PROTOCOL.md and
> rebuild/builds/2026-11-a/ORCHESTRATOR_LOG.md. Do the "Do these before build b" list,
> committing after each item, then continue the protocol from P2 with `/rebuild-ladder`.
> Run every gate yourself, never pass oracle values to a builder, and report each phase's
> gate result.
