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
Class B (builder bug), found by the audit-derived check. A label-only round trip to the pilot session follows (round 2 below, if it finishes).
