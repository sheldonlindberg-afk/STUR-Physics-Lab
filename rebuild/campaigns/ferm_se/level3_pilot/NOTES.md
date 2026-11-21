# Level-3 isolation pilot (ferm_se, one Sonnet builder in a fresh cloud session)

**What was done.** A new cloud session (`session_01P5oiB2ekzW2y9Mk1GbvPTJ`, tag `config:no-git-repo`, created by `create_session` with no `source_url`) received the five room files inline (BUILDER.md, SPEC.md, campaign.py, gate.py, inputs.py, with
sha256 checksums), built `builds/l3` and returned the module and derivation in its final message. The orchestrator ran the hidden verifier on the returned module.

**Isolation evidence (stronger than level 2, still not proof).**
* The container held no repository and no oracle: the session had no git source, so the only files it could read were the ones it wrote. A fresh container cannot contain a file the room never had.
* Transcript (9 tool calls: 5 `Write`, 4 `Bash`), all paths under `/root/room`; no web fetch or search (the result's own counters: `web_fetch_requests` 0, `web_search_requests` 0, `webSearchRequests` 0), no sub-agent (`spawned` 0), no permission denials, no repository tool call.
  Its first command checked the five file hashes (all matched, per its report); a `python3 -c "import numpy,mpmath,sympy"` probe showed scipy and mpmath not installed and nothing was pip-installed.
* **What the setup does not enforce.** The session's tool list (from `get_session`) included WebFetch, WebSearch, Agent, `add_repo` and `list_repos`; isolation of the *tools* rests on the builder's compliance and on this transcript record, not on a network or tool block. The checks above show it did not use them.
  The builder is a language model that may know these formulas (see ACCEPTED.md); a fresh container does not remove that.

**Result.** Round 1 passes the builder gate and the original oracle (worst deviation 7e-16) but **fails the audit's table of 43 points at 5 points** (worst relative error 0.44): the quadrature of the single-loop integral is wrong **just below the threshold k^2 = (m1+m2)^2** (36% at 1e-6 below, 2% at 1e-3 below, 80% at 1e-9 below for a top loop;
above threshold it agrees to 1e-15). Cause (orchestrator's reading, not yet confirmed by the builder): tanh-sinh nodes cluster at the interval ends, but just below threshold ln(Delta) has a sharp dip at the interior minimum of Delta, which is not resolved;
above threshold the integral is split at the roots. Neither the original oracle nor the builder's blind checks probed this window; the first accepted builds (a, b) were closed-form and had no such problem. This is the kind of defect an independent fresh build can have that two builds of the same style do not.
Class B (builder bug), found by the audit-derived check.

## Round 2 (label-only report, same session)

The orchestrator sent only the failing check's label, "5 of 43 points off, worst relative 0.44, a single heavy-fermion loop" (no values). The builder found the cause by derivation and its own scans against its analytic second route: below threshold the integrand has a
narrow dip at the interior vertex x0 of Delta(x), unresolved by tanh-sinh nodes clustered at the ends; it added a branch that splits at x0 (DERIVATION section 4b) and reported agreement to <= 1.2e-12 at 12 near-threshold points and with a 3000-point random scan.
Orchestrator's check of the returned module (extracted from its final message): **the near-threshold window is fixed** (all original oracle checks pass, worst 3e-15), **but the audit table now raises `ValueError: math domain error` at the 5 points that sit exactly on a threshold k^2 = (m1+m2)^2**
(three top-loop points, the t-b doublet and an equal-mass (91, 91) doublet): the new branch evaluates a square root or logarithm of a quantity that is exactly zero or rounds negative at threshold, instead of returning the real part, which the SPEC asks for "at or above" a threshold.
Class B again, narrower than round 1. **The pilot is recorded at this point: two rounds, one defect remaining; no third round was run** (the session was archived; unarchiving would provision a fresh container, which would blur the isolation evidence).

## What the pilot shows
* The level-3 procedure works end to end: a fresh no-repo session, the room delivered inline with checksums, the build and the fix loop carried out from the labels only, the module returned through the final message, the verification and the transcript audit done by the orchestrator.
* A fresh independent build can have defects that two builds of the same (closed-form) style do not, and the audit-derived checks, not the original oracle, found them; this is evidence for the value of the audit stage, not a statement about the accepted builds a and b, which pass everything.
* The builder was a language model: the isolation is of files and tools, not of its prior knowledge.

## Stray messages (not part of the build)
After round 2, three unrelated messages were sent by mistake to this session from another chat ("Next item", "Give me a summary of where the repo stands and push", "I need to merge this with my repo"). The session answered each by asking for clarification, ran only `ls` and the builder gate in `/root/room`, pushed nothing, used no repository or connector tool, and did not modify the build. They come after the build and verification and are recorded here for completeness.
