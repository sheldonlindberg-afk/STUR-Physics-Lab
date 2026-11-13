# Builder prompt

*Give this to the AI that writes the code, one stage per session or per turn. Replace
`<BUILD_ID>` and `<STAGE>`.*

---

You are rebuilding one stage of a physics computation **from first principles**. Your work
is correct only if it is derived. A number that happens to match is not enough.

**Build:** `builds/<BUILD_ID>/`  **Stage:** `<STAGE>`

## What you may read

- `SPEC.md`: the postulates and conventions for your stage. This is the physics you assume.
- `contract.py`: the exact functions your module must export, their signatures and units.
- `inputs.py`: the only source of measured numbers.
- `blind/checks.py` and `harness.py`: the tests you must pass. You may read them in full.
- The modules of **earlier** stages in your own build directory.

## What you must not do

- Read anything outside this directory: no repository source, no tests, no results, no
  papers' numerical values, no web search for the answers. If a value you need is not in
  `inputs.py` and you cannot derive it, stop and write it in `QUESTIONS.md` (step 5).
- Type in any physical or derived number. Read inputs as `inputs.NAME` **inside** functions
  (never `from inputs import`), and compute everything else.
- Edit `SPEC.md`, `contract.py`, `inputs.py`, `blind/` or `harness.py`, loosen a tolerance,
  special-case a test's arguments, or detect that you are being tested.
- Claim `quoted` provenance for anything outside the stage's `quoted_allowed` list, or claim
  `derived` for something you looked up.

## Procedure (follow it in order)

1. **Derive on paper first.** Write `builds/<BUILD_ID>/DERIVATION_<STAGE>.md` before any
   code. For every export, give:
   - the postulates it rests on (cite the SPEC.md section);
   - each step of the derivation in equations;
   - the result in closed form, where one exists;
   - **an independent second route** you will use to check it: a limit, an identity, a
     different numerical method, or a symmetry argument.

   Mark anything you could not derive.
2. **Implement** `builds/<BUILD_ID>/<module>.py`.
   - Use only the standard library, `inputs`, and earlier stages' modules.
   - Reuse `toolkit` for the numerics; don't write private copies.
   - Define `PROVENANCE = {export: (kind, note)}`. The note says *how* the export was
     derived, e.g. "massless direction n_A = q_A/g_A; M n = 0 because Q<phi> = 0".
   - Exact quantities (charges, rational integrals, the first law) must be
     `fractions.Fraction` and compare with `==`.
3. **Self-check beyond the harness.** At the bottom of the module, under
   `if __name__ == "__main__":`, compute your second route from step 1 and print it next to
   the main result.
4. **Run the gate:** `python3 harness.py builds/<BUILD_ID> --mode builder --stage <STAGE>`.
   Every tier must pass: contract, lint, blind, sensitivity. When a check fails, find the
   error in your *derivation*, not just the code, and fix `DERIVATION_<STAGE>.md` to match.
5. **Report.** Finish with:
   - the harness summary, verbatim;
   - any spec ambiguity you hit and how you resolved it, also appended to
     `builds/<BUILD_ID>/QUESTIONS.md`;
   - anything you are unsure of.

   Do not say a stage is done unless the harness says `ALL GATES PASS` for it.

Your result will later be compared, number by number, with an independent implementation
and with a second blind build. Disagreements will be traced back to your derivation notes,
so make them complete enough for someone else to follow.
