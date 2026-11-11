# Archive: superseded material

## `notes/`: working notes

The process records behind the current research notes: the tests of the original STUR
postulate (POSTULATE_TEST, ASSUMPTIONS, OPEN_PROBLEMS, OPTION_A), the unification
search (UNIFICATION, CONFINEMENT, Z2_GAUGE, NEXT_STEPS, UNIFYING_SEARCH, WALL), and the
consistency and recheck logs (CONSISTENCY, RECHECK). Their scripts and tests still live
in `src/` and `tests/` and run in CI.

Everything here is kept for the record and is **not** the current claim of
this repository. The current work is measurement and gravity from the quantum
level up; see the [top-level README](../README.md).

## `resistance-equation/`: the STUR Resistance Equation (archived 2026-11-10)

The former home page, moved with `git mv`. Only paths changed: links to `assets/`,
`manifest.json` and `docs/` go up two levels. Its derivation record stays at
`docs/STUR_Resistance_Equation_Derivation_Record.pdf`, and `src/stur_verify.py`
still reproduces its numbers. 

## `stur-roll/`: STUR-ROLL (archived 2026-11-01)

The entire repository as of commit `b75d7ef` (round 9): the STUR-ROLL home
page, `README.md`, `docs/`, `src/`, `results/` and `tests/`, plus copies of
`CITATION.cff`, `llms.txt` and `requirements.txt`. The full pre-archive state
is commit `b75d7ef`; files moved with `git mv` keep their history under
`git log --follow`. Only paths were changed: the page's
links to `assets/` and `manifest.json` now go up two levels, its document links
point to `archive/stur-roll/docs/`, and the JS test loads the simulator from
`../../../assets/js/`. The site renders at `/archive/stur-roll/` and its Python
and JS tests still run in CI.

STUR-ROLL predicts |&beta;| = k&alpha;/2 = 0.2091&deg; for CMB birefringence, to
be tested by LiteBIRD. It was archived when the home page moved to the
resistance-equation work.

## `v7-toe/`: STUR v7.0 "Theory of Everything" (superseded)

This is the entire former repo: about 60 derivation documents, more than 120
web pages (`v7-toe/index.html` was the old home page), Python scripts, PDFs
and the browser tests. They were moved here unchanged except for one thing:
the relative paths to the shared `assets/` folder and to `manifest.json` were
rewritten so the archived site still renders at
`/archive/v7-toe/`. Old links of the form `/scripts/<page>.html` now live at
`/archive/v7-toe/scripts/<page>.html`.

Why it is superseded: STUR-ROLL is scoped as Lambda-CDM plus one derived
sector, not as a theory of everything. The 2025 tanh(r/1 mm) gravity law
(STUR-2025) fails the Eot-Wash inverse-square test and does not flatten
rotation curves. STUR-ROLL uses TEGR = GR for all gravity tests.

## `genesis-v10-stur-b/`: GENESIS v10 / STUR-B (superseded)

The LiteBIRD pre-registration of STUR-B, the earlier birefringence bridge
hypothesis (&beta; accrued in chronomagnetic log-time, with one fitted
parameter &kappa;). The files were renamed from `scripts/genesis V10 Light Bird`
and `scripts/genesis V10 preregistration`, and their **contents are unchanged**: `sha256sum genesis_v10_litebird.py` still equals the pre-registered `code_sha256` (11dd1aaf…091e).

STUR-B needs initial &theta; energy and is excluded by the full STUR-ROLL code.
STUR-ROLL replaces its fitted &kappa; with the derived &alpha;/2.

## Triage (2026-10-31)

Every claim here was screened against four gates fixed in advance
([`docs/ARCHIVE_TRIAGE_CRITERIA.md`](stur-roll/docs/ARCHIVE_TRIAGE_CRITERIA.md)).
None survives; the reasons, claim by claim, are in
[`docs/ARCHIVE_TRIAGE.md`](stur-roll/docs/ARCHIVE_TRIAGE.md).
