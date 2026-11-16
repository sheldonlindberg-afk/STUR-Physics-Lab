# Builder instructions (one campaign, one build)

You are deriving one physics result **from first principles** and implementing it. A number that
happens to match is not enough: the derivation is the deliverable, and it will be audited.

**Working directory:** the clean room you were started in. Run every command there. Do not read any
path outside it. There is no repository, no web, no literature lookup for numerical values: if you need a
value that SPEC.md does not give, derive it or stop and write the question in `QUESTIONS.md`.

You may read: `SPEC.md` (postulates, conventions, the exact exports), `campaign.py` (the exports and the
blind checks, in full), `gate.py`, `inputs.py`. You may not edit them, loosen a check, special-case a
check's arguments, or detect that you are being tested.

## Procedure

1. **Derive on paper first.** Write `builds/<id>/DERIVATION.md` before any code: the postulates used
   (cite the SPEC section), each step in equations, the closed form where there is one, and an **independent
   second route** you will use to check the main result (a limit, an identity, a different numerical method).
   Mark anything you could not derive.
2. **Implement** `builds/<id>/<module>.py` (the module named in `campaign.py`): every export, plus
   `PROVENANCE = {export: (kind, note)}` with kind `derived`, `input` or `quoted`. `quoted` is allowed only for
   exports listed in `campaign.QUOTED_ALLOWED`. Do not type in any answer-like number; the lint rejects
   literals that match the answers. Constants that SPEC.md gives you are fine.
3. **Second route.** Under `if __name__ == "__main__":` compute your independent check from step 1 and print it
   next to the main result.
4. **Run the gate:** `python3 gate.py builds/<id> --mode builder`. Every tier must pass. When a check fails,
   look for the error in your derivation first, then in the code. Fix `DERIVATION.md` to match.
5. **Report**: the gate summary verbatim; every ambiguity in SPEC.md and how you resolved it (also append it
   to `builds/<id>/QUESTIONS.md`); anything you could not derive. If you cannot make the gate pass honestly,
   say so plainly and stop: a failed honest build is worth more than a forced pass.

Allowed imports are listed in `campaign.ALLOWED_IMPORTS`. Keep runtime of each export reasonable.
