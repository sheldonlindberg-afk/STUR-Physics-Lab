# Physics Lab

A small set of physics/math notes that survived an explicit peer-review pass, after a
larger "unified resistance theory" framework did not.

## What happened

This repository previously hosted "Sheldon's Theory of Unified Resistance" (STUR): a
manuscript, ~60 markdown derivation documents, 123 interactive HTML pages, and 33 Python
verification scripts, developed across many iterations. A staged peer review — first of
the core manuscript, then of every other document, page, and script in the repo in
parallel batches — found that the theory's central unification claim does not hold up:

- Its foundational "geometric dual tensor" (and, in later iterations, its "Master
  Action") is invoked throughout but never actually defined.
- The one place a concrete unification mechanism is attempted (a tensor product of
  operator algebras) provably makes the force sectors mathematically *decoupled* —
  the opposite of unification.
- Nearly every quantitative "prediction" across the repository depended on chains of
  free "correction factors" tuned after the fact to match known experimental values —
  a pattern the documents' own text frequently admitted directly ("calibrated, not
  derived," "a target value, not a derived result").

Full details are in [`about.html`](about.html).

## What's here now

| File | Content |
|---|---|
| [`scripts/maxwell_equations.html`](scripts/maxwell_equations.html) | Maxwell's equations from the U(1) gauge action (standard field theory) |
| [`DOMAIN_WALL_ENERGY_CALCULATION.md`](DOMAIN_WALL_ENERGY_CALCULATION.md) | Domain wall energy bound (standard cosmology) |
| [`INSTANTON_PREFACTOR_EXPLICIT.md`](INSTANTON_PREFACTOR_EXPLICIT.md) | Zeta-function regularization on a Z₃ orbifold (standard QFT technique) |
| [`MPLANCK_DERIVATION_ANALYSIS.md`](MPLANCK_DERIVATION_ANALYSIS.md) | Why a dimensional constant needs a dimensional input (Buckingham-π) |

Each has been rewritten to remove framework-specific branding, since none of their
validity ever depended on it.

## Archival source material

The original manuscript and a handful of reference PDFs it cited remain in `scripts/`
for archival purposes. They are not linked from the live site and make no claims beyond
what they always contained.

## License

CC0 1.0 Universal (Public Domain) — see `LICENSE`.
</content>
