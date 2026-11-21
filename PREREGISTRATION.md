# Pre-registration: rules, and the registry

*How a result whose outcome is not known in advance is tested here, so that neither the
calculation nor the pass condition can be fitted to the answer. Independent work, not peer
reviewed.*

## Why the rules have this form

The first induced-gravity test in this repository was registered with a formula quoted from
the literature whose overall sign had not been re-derived. It failed as registered. Re-deriving
the sign afterwards reversed the result. The correction was forced by the literature, but it
came after the result was known, so it carries less weight than a result that passes as first
registered. The rules below exist so that cannot happen again.

## Rules

1. **Derive before registering.** The registration contains its own derivation of every
   formula the computation uses: every sign, factor and convention. Formulas from the literature
   are re-derived in the registration's conventions, not quoted.
2. **Fix the pass condition, and what each outcome means.** A table of items: what is expected,
   and what counts as a failure. Each item has an expectation that could be wrong.
3. **Commit before computing.** The registration is committed and pushed before any number in it
   is computed. Its registration hash (`python3 tools/prereg.py <file>`) is entered in the
   registry below with the commit.
4. **Never edit a registration.** The result goes below a separator line, `---` followed by
   `## Result`. Only the title and the status line may change. `tests/test_preregistration.py`
   recomputes each registration's hash and fails on any other edit.
5. **Errors found later are reported below the result, not fixed above it.** Then the registered
   computation is repeated with only that error corrected, and both outcomes are stated.

## Registry

| Document | Registered at commit | Registration hash (sha256) | Outcome |
|---|---|---|---|
| [INDUCED_GRAVITY_FINITE.md](INDUCED_GRAVITY_FINITE.md) | c1beae2 | 2a8e696679591acca28dd308e50298dd48219f3be7f5d64cd32dbb9da1ed6045 | every item as registered |

The earlier induced-gravity registration predates these rules. Its record is
[INDUCED_GRAVITY.md](INDUCED_GRAVITY.md), which states that the sign was corrected after a first
computation. The git history (commits 296e157 and 2cea040) keeps the original.
