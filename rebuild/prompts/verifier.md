# Verifier prompt

*Give this to a separate AI session after the builder's stages pass the builder gate. The
verifier may read everything in the repository. It never edits the build.*

---

You are verifying an independent, blind rebuild of `src/ladder_standalone.py`.

**Build:** `rebuild/builds/<BUILD_ID>/`

1. Run `python3 rebuild/harness.py rebuild/builds/<BUILD_ID> --mode verifier --ledger`.
2. Classify **every** oracle failure, and every pass that looks too close to be
   independent, into exactly one class:
   - **B, build error:** the derivation or code is wrong. Locate the wrong step in
     `DERIVATION_<stage>.md`.
   - **R, reference error:** the build is right and `src/ladder_standalone.py` (or the pinned
     number) is wrong. Prove it with a third route: a closed form, a symbolic computation
     (sympy is available to you, not to the builder), or the literature. **This is the most
     valuable outcome. Do not explain it away.**
   - **C, convention or spec gap:** both are right under different conventions, or
     `SPEC.md` was ambiguous. Propose the SPEC.md wording that would have prevented it.
   - **N, numerical:** a tolerance, step size or grid issue. Quantify the error on both sides.
3. Write `rebuild/builds/<BUILD_ID>/FINDINGS.md` with a table: check, class, evidence, and the
   action needed.
4. **Feedback to the builder:** for class B, send back only the failing check's *label* and
   the physics question it raises, e.g. "the photon coupling is off; re-derive the
   normalization of n". **Never send the reference value**, or the next build is no longer
   blind.
5. For class R, open an issue-style note in FINDINGS.md that names the reference line and
   the proposed fix. Don't edit `src/` yourself without the owner's approval.

Report the class counts, then each R finding in full.
