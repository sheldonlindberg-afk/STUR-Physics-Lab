# Auditor prompt (red team)

*Give this to a third AI session. Its job is to find ways the build could pass without being
right. It reads everything and edits nothing.*

---

You are auditing a blind rebuild for **false confidence**. The harness has passed it. Assume
that proves less than it seems, and look for the gaps.

**Build:** `rebuild/builds/<BUILD_ID>/` (with `LEDGER.md`, `DERIVATION_*.md`, `FINDINGS.md`)

Check, stage by stage:

1. **Provenance honesty.** For each row of `LEDGER.md`, does the code actually do what the
   note claims? A "derived" export that only evaluates a closed form copied from a textbook
   is *quoted*. Flag it.
2. **Derivation ↔ code.** Every equation in `DERIVATION_<stage>.md` should appear in the
   code, and every computation in the code should be justified in the notes. List the
   mismatches.
3. **Hidden answers.** Look for constants computed from other constants to dodge the lint
   (e.g. `2 * 1.0934`), lookup tables, branches on argument values that the tests use, and
   inputs cached at import time.
4. **Weak checks.** For each blind check of the stage, write down a plausible *wrong*
   implementation that would still pass it. If you find one, propose the extra check that
   kills it: add it to `rebuild/blind/checks.py` (if it leaks no answer) or to
   `rebuild/oracle.py`. Add a matching mutant to `tests/test_rebuild_harness.py`, showing
   that the new check fails the mutant. **This is how the framework gets stronger with
   every rebuild.**
5. **Second-build agreement.** If two builds agree, check that they are actually
   independent: compare their derivation routes. Two builds that make the same mistake for
   the same reason are one build.

Write `rebuild/builds/<BUILD_ID>/AUDIT.md`: findings by severity, each with the file and line,
then the new checks you propose. Acceptance requires no open high-severity finding.
