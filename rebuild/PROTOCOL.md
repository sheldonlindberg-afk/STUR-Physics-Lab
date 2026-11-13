# Protocol: an AI rebuild of the symmetry ladder from first principles

*The procedure an orchestrating AI (or a person) follows to have the ladder rebuilt blind,
then verified, cross-checked and audited. Each phase has an exit gate that a program
checks, not the AI's own judgement.*

## Why a protocol and not a prompt

Asking one AI to "rebuild this from first principles" fails in predictable ways:

| Failure | What it looks like | What stops it here |
|---|---|---|
| **Answer leakage** | It reads the existing code or the pinned numbers and reproduces them | Clean room (§3); the lint rejects typed-in numbers and references to `src/` |
| **Hard-coding** | `return 2.1868` | Sensitivity tier: mutated inputs must move the output; scaling-law checks |
| **Plausible but wrong** | Right shape, wrong factor of 2 | Oracle comparison on the *same* arguments, random ones included |
| **Self-grading** | "All checks pass" without running them | The harness decides; its JSON report is the evidence |
| **Moving the goalposts** | Loosening a tolerance, editing a test | The builder can't edit the framework; CI runs the harness self-test |
| **Shared blind spots** | The builder and the reference make the same mistake | A second blind build (N-version), and the verifier's third route for disagreements |
| **Provenance inflation** | Calling a looked-up formula "derived" | `PROVENANCE` per export, the quoted whitelist, and an auditor who checks the claims against the code |
| **Weak tests** | A check that a wrong implementation also passes | The auditor writes mutants; each surviving mutant becomes a new check |

## 1. Roles

| Role | Sees | Writes | Prompt |
|---|---|---|---|
| **Orchestrator** | everything | build directory scaffolding, the run log | this file |
| **Builder** (×2, independent) | the clean room only | `builds/<id>/<stage>.py`, `DERIVATION_<stage>.md`, `QUESTIONS.md` | [`prompts/builder.md`](prompts/builder.md) |
| **Verifier** | everything | `FINDINGS.md`, `LEDGER.md` | [`prompts/verifier.md`](prompts/verifier.md) |
| **Auditor** | everything | `AUDIT.md`, new checks and mutants | [`prompts/auditor.md`](prompts/auditor.md) |

The builder, verifier and auditor must be **separate sessions** (separate context windows).
A session that has seen the oracle can't build blind afterwards. Ideally the two builders
run on different models, or at least with different seeds and phrasing.

## 2. Phases and gates

```
P0 setup ─► P1 build stage by stage (×2 builds) ─► P2 verify ─► P3 cross-build ─► P4 audit ─► P5 accept
                 ▲            │ fail                 │ B findings                   │ new checks
                 └────────────┴──────────────────────┴──────────────────────────────┘
```

**P0, setup.** Choose build ids, e.g. `2026-11-a` and `2026-11-b`. Run
`python3 rebuild/cleanroom.py export /path/outside/repo/room-a 2026-11-a`, and the same for
`room-b`.
*Gate:* the clean room contains no `src/`, `tests/`, `oracle.py` or `_selftest/` (the script
asserts this).

**P1, build, one stage at a time, in contract order**
(toolkit → gauge331 → chiral → casimir → graviton → desitter → blackholes → links).
For each stage, start a builder with `prompts/builder.md`.
*Gate:* `python3 harness.py builds/<id> --mode builder --stage <stage>` exits 0. Commit
the stage before starting the next. If a builder fails the gate three times, stop and look
at its `QUESTIONS.md`. The spec may be ambiguous, and fixing the spec beats forcing the
build.

**P2, verify.** `python3 rebuild/cleanroom.py import <room> <id>`, then a verifier session
runs `python3 rebuild/harness.py rebuild/builds/<id> --mode verifier --ledger` and triages
every finding as B, R, C or N.
*Gate:* no untriaged oracle failure. Class B goes back to P1 with *the label only*. Class
C changes SPEC.md, and then the stages it affects are rebuilt in both builds. Class R is
reported to the owner.

**P3, cross-build.** `python3 rebuild/harness.py rebuild/builds/a --mode verifier --compare rebuild/builds/b`.
*Gate:* every probe agrees to 1e−8 (or the difference is explained as class N).

**P4, audit.** An auditor session runs `prompts/auditor.md` on each build.
*Gate:* no open high-severity finding. Every surviving mutant has become a new check, and
`python -m pytest tests/test_rebuild_harness.py` passes with it.

**P5, accept.** Write `rebuild/builds/<id>/ACCEPTED.md` with:
- the commit hashes;
- the harness reports (verifier mode, cross-build);
- the class counts from FINDINGS.md;
- the ledger's counts of derived, input and quoted exports.

From then on, `tests/test_rebuild_harness.py` re-runs every accepted build in CI, so a
later change to the reference that breaks agreement shows up at once.

## 3. Isolation levels

From weakest to strongest. Use the strongest you can.

1. **Instruction only:** the builder is told not to read `src/`. This is not enough on its
   own. The lint catches the crudest leaks.
2. **Clean room directory:** `cleanroom.py export` to a path outside the repository, with
   the builder's working directory set there. The answers aren't on the builder's path.
3. **Clean room machine:** a fresh cloud session or container that has only the clean room
   (for example a new repository holding just its contents), and no network. Nothing
   leaks.

Level 2 is the minimum for a result you'd call independent. Note in `ACCEPTED.md` which
level you used.

## 4. What "accurate" means at the end

An accepted build establishes, for every export:
- it was derived (or quoted, and the source is named) from the SPEC.md postulates and the
  inputs.py numbers;
- it passes identities, limits and scaling laws that don't depend on the reference;
- it agrees with the reference implementation on the same arguments;
- it agrees with a second build made independently;
- an adversary tried to break each check and failed, or the check was strengthened.

It does **not** establish that the postulates are true of nature. That is what the
`[data]` comparisons with measurements are for, and they stay exactly as good as the
inputs. The quoted results (contract `quoted_allowed`) remain quoted until a stage derives
them; [FIRST_PRINCIPLES.md](../FIRST_PRINCIPLES.md) §10 lists how.

## 5. Extending the framework

To bring a quoted result inside, or to add a stage:
1. Add the export to `contract.py` (and remove it from `quoted_allowed`).
2. Add its postulates, without its answer, to `SPEC.md`.
3. Add blind checks (properties) and oracle checks (values) for it.
4. Implement it in `_selftest/reference_build/_ref.py`.
5. Add at least one mutant to `tests/test_rebuild_harness.py` that the new checks catch.
6. Rebuild the affected stages in both builds.
