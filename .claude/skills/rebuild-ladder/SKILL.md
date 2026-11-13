---
name: rebuild-ladder
description: Orchestrate a blind, first-principles AI rebuild of src/ladder_standalone.py using the rebuild/ framework (clean room, staged builder gates, verifier triage, second independent build, red-team audit). Use when asked to rebuild, re-derive or independently verify the symmetry ladder.
---

# Orchestrating a first-principles rebuild

You are the **orchestrator**. Follow `rebuild/PROTOCOL.md` exactly. You never write build code
yourself, and you never pass oracle values to a builder.

Arguments (optional): a build id prefix and the stages to run, e.g. `2026-11 gauge331`.
Default: every stage, two builds `<prefix>-a` and `<prefix>-b`.

1. **Preflight.** Run `python -m pytest tests/test_rebuild_harness.py -q`. If it fails, stop:
   the gatekeeper itself is broken.
2. **Clean rooms.** For each build id, run
   `python3 rebuild/cleanroom.py export <scratchpad>/room-<id> <id>`, in your scratchpad,
   outside the repository.
3. **Build loop.** For each build, and for each stage in `contract.STAGE_NAMES` order:
   - Start a **fresh** builder subagent (Agent tool, general-purpose; never a fork, which
     would inherit your context and the oracle). Its prompt is the text of
     `rebuild/prompts/builder.md` with BUILD_ID and STAGE filled in, plus:
     "Your working directory is <room>. Run every command there. Do not read any path
     outside it."
     Build b's builders get no information about build a.
   - When it returns, **run the gate yourself**:
     `cd <room> && python3 harness.py builds/<id> --mode builder --stage <stage>`.
     Trust that exit code, not the agent's report.
   - If the gate fails, resend the failing check *labels* (no values) to the same agent
     with SendMessage. After three failures, read `builds/<id>/QUESTIONS.md` and ask the
     user whether SPEC.md needs clarifying.
   - When the gate passes, copy the room's build back
     (`python3 rebuild/cleanroom.py import <room> <id>`) and commit with the message
     `rebuild <id>: <stage> passes builder gate`.
4. **Verify.** Start a verifier subagent with `rebuild/prompts/verifier.md`. Then run
   `python3 rebuild/harness.py rebuild/builds/<id> --mode verifier --ledger` yourself. Class B
   findings go back to step 3 for that stage, as labels only. Class C findings: propose the
   SPEC.md change to the user. Class R findings: report them to the user, with evidence.
5. **Cross-build.** `python3 rebuild/harness.py rebuild/builds/<prefix>-a --mode verifier --compare rebuild/builds/<prefix>-b`.
6. **Audit.** Start an auditor subagent with `rebuild/prompts/auditor.md`. Accept new checks
   and mutants only if `pytest tests/test_rebuild_harness.py` still passes on the reference.
7. **Accept.** Write `rebuild/builds/<id>/ACCEPTED.md` (PROTOCOL.md P5), commit and push.
   Report to the user:
   - each phase's gate result;
   - the class counts;
   - every class R finding;
   - the isolation level used.

Never mark a phase done on an agent's word. The harness exit code and the report JSON are
the only evidence.
