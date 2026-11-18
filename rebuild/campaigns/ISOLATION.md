# Isolation in a campaign: what is enforced, what is evidenced, what is not

| Layer | What it gives | Status |
|---|---|---|
| Instruction | the builder is told not to read outside its room | all builds |
| Clean room directory (`export_room.py`) | the room never contains the oracle, `src/`, `tests/` or results; it must be outside the repository | all builds (PROTOCOL.md level 2) |
| Lint | rejects imports of `os`, `sys`, `subprocess`, `open`, `exec`, ..., `from inputs import`, and literals or integer-built expressions equal to an oracle target | all builds |
| **Transcript audit** (`audit_transcript.py`) | every tool call of the builder is in its transcript; the audit flags web, delegation and MCP tools, any path outside the room that the same transcript did not create, `cd` out of the room, and canary strings | **evidence after the fact**; run on all four accepted builders: clean |
| Canaries (`CANARIES.txt`) | a unique token planted in each oracle (never in a room); if a transcript contains it, the builder read the oracle | planted for future runs; the four existing transcripts also scanned: absent |
| Private `tmp/` in each room | scratch files stay in the room instead of the shared session scratchpad (the environment tells agents to use the scratchpad, which held the orchestrator's own files) | new rooms only |
| Fresh machine (PROTOCOL.md level 3) | a room that physically contains nothing else | **not used** |

## What the transcript audit proves

For the four builders (greybody a, b; qed_cp a, b), the record of every Read, Write, Edit, Bash, Glob and Grep call shows no access
to the repository, another room, an oracle, the orchestrator's scratch directory, the literature or the web. The two Casimir-Polder
builders and build b of grey-body wrote helper scripts and profiles to the shared scratchpad (the environment's own instruction
to every agent); the audit accepts those because the same transcript created them, and it flags any read of a file the builder
did not create. The audit's rules were tightened three times while developing it, and the third was a real finding about the setup, not about the
builders: **a subagent's shell starts in the orchestrator's working directory, which was the repository (or one of its
subdirectories), not its room.** The transcript records that directory (`cwd`) on every record. So any command run before a `cd` into
the room resolves its relative paths against the repository, and a bare `ls`, `find .` or `grep -r` there would list or read repository
files. The audit therefore simulates the shell: it starts from the recorded cwd, follows every `cd`, resolves each space-free
path-like argument and each default-directory search (`ls`, `find`, `grep -r` with no path), ignores grep and pgrep pattern
arguments, and flags any result outside the room. Under that rule all four builders are clean: every relative path they used came after
a `cd` into the room, and none searched the starting directory. The test of the audit (`tests/test_campaign_gate.py`) covers the cases
it got wrong on the way: arithmetic that looks like a path, `..` inside a room versus out of it, `.` as a directory, and grep patterns.

## What it cannot prove

* The transcript records tool calls, not what a Python process a builder launched might open (an `open(...)` of an arbitrary path
  inside code it ran). The lint forbids `open` and `os` in the delivered module, but not in the throwaway scripts a builder runs.
  Those scripts' source is in the transcript and the audit sees their command text, but not a path assembled at run time.
* The canaries detect reading the oracle; they cannot detect knowing a published number the builder remembers (for example 23/(4 pi)
  is in the training data of any model). The defence against recalled constants is the lint on literals, the exports that exist
  only on the required route, and the auditor reading `DERIVATION.md`.
* Both builders of a campaign ran on the same machine as the orchestrator. Only level 3 (a fresh container holding just the room, no
  network) makes independence a property of the setup instead of a record of behaviour. That needs a second environment and a way
  to move a room into it and a build out; this session could not create one.

## Rules for the next builder, from what this showed

1. The builder's first command in every call must be `cd <room> && ...` (BUILDER.md now says so); the audit enforces it after the fact.
2. Scratch files go in `<room>/tmp/`, not in the shared scratchpad.
3. The orchestrator should keep no files of its own where a room can reach them that it would mind a builder reading; the canaries only
   detect a read, they do not prevent one.
4. For a result that must stand on independence alone, use level 3: a fresh machine or container holding just the room.

## Procedure now

P1 of README.md: after each builder returns, run `python3 audit_transcript.py <transcript> <room> --canary <each token>`; a flag
returns the build to the builder (or the orchestrator explains the flag) and is recorded in the campaign's `ACCEPTED.md`.
Save the output as `builds/<id>/isolation_audit.txt` with the transcript's SHA-256, because the transcript is ephemeral.
