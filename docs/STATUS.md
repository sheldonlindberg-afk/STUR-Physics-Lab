# Status: what is in this repo and what is still open

## Reproducible here

| File | What it does | Verified |
|---|---|---|
| `src/stur_final.py` | steps 4&ndash;5, audit A&ndash;E, scoreboard | output matches its embedded `EXPECTED_OUTPUT` line for line (numpy 2.5, scipy 1.18, Python 3.13); checked in CI by `tests/` |
| `results/stur_final_output.txt` | captured output of the above | &mdash; |

## Referenced but not yet in the repo

`stur_final.py` cites several companion scripts that are **not** included yet.
Until they are added, the claims that depend on them cannot be reproduced
from this repo:

| Missing file | Claims that depend on it |
|---|---|
| `stur_genesis_simulation.py` (sections 1&ndash;11) | steps 1&ndash;3 in full; the reionization ratio &beta;_reio/&beta;_rec (sec. 10); the choice x_f = 137 that sets m (sec. 9); the exclusions of &theta; tunnelling, STUR-B, M3a, U0 and C0 |
| `precision_harness.py` | the extended precision gates |
| `z3_bounce_check.py` | the Z&#8323; bounce check |
| `class_check.py` | the CLASS run that produces the &beta;(&ell;) table, which `stur_final.py` currently **hard-codes**, and the run directory that `src/alp_vs_stur.py` needs |

`src/alp_vs_stur.py` does `import stur_final`, so run it from `src/` or with
`src/` on the path: `cd src && python alp_vs_stur.py <class run dir>`.

## Corrections to `stur_final.py` found in refinement round 1

`stur_final.py` is kept byte-for-byte as uploaded. These corrections apply to
its text (details in [`REFINEMENT_R1.md`](REFINEMENT_R1.md)):

- **Section A:** "c_g = 0.49998 at Mr = 10" is truncation of the KK sum. The
  exact closed form gives &frac12; to e^(&minus;63).
- **Section E:** "allowed from 1/L ~ 10 GeV" is superseded. The charged bulk
  fermion requires bulk hypercharge. Its KK bosons (M&#8321; = 2&pi;/L) are excluded
  below 5.1&ndash;5.5 TeV, so **1/L &gtrsim; 0.8&ndash;1.0 TeV** and M_f &gtrsim; 1.4&times;10&#8309; GeV (round 2,
  correcting round 1&rsquo;s 2&pi; slip).
- **Section C:** the DM fractions are about 42&times; too small, because release happens
  at H &asymp; m/19.5, not m/3. They are still negligible (R2.1).
- **Step 5 seed window** "1e-4 to 0.3": the upper end is excluded; the seed must be
  &lesssim; 1.2e-2 (R2.4).
- **Section A:** &beta; = k_eff&middot;&alpha;/2 holds exactly on the orbifold (R2.2).
- **Framing:** &beta; = &alpha;/2 from a hilltop roll is prior art (Lee et al. 2025).
  STUR-ROLL is a UV origin for c_&gamma; = 1 and for the hilltop start.

## Open items

- **k = 1 is a discrete choice**, not derived. Equivalently, it is the sign of the bulk mass
  relative to the half-integer bare level; k_eff = 0 is equally consistent (R1.1).
- **The initial seed** must lie between about 1e-20 and 1.2e-2 (at m = 1e-30 eV). It is
  set by H_nuc/(2&pi;f) and the number of e-folds, neither of which is derived yet.
- **Global structure:** STUR-ROLL adopts [SU(3)&times;SU(2)&times;U(1)]/Z&#8326; (round 3, R3.2), so k &isin; &Zopf;.
  The model therefore predicts no fractionally charged colour-singlet particles.
- **Nucleation phase:** H_nuc lies between 15/L and about 0.6 f/&radic;N. This implies r &lesssim; 10&#8315;&sup3; unless
  f &gtrsim; 10&sup1;&#8308; GeV. If the phase is R&sup2; inflation, then m &lesssim; 3&times;10&#8315;&sup3;&#8304; eV (R3.3).
- **The hilltop start is not derived.** &theta;'s potential is ~1e-87 too weak to hold &theta; at 0 at nucleation.
  A smooth birth fixes &theta; = 0 but makes it a minimum; round 5 proves this exactly (positivity
  theorem). The 5D torsion twist of round 4 does not exist, so the R4 dark-matter link is
  withdrawn. The one local escape is an orbifold-parity-breaking brane coupling
  &Sigma;&psi;&#772;&Gamma;^y&psi;, which works if its twist &delta; is within 0.094 of &pi;
  ([`REFINEMENT_R5.md`](REFINEMENT_R5.md)). Deriving &delta; = &pi; is open.
- See [`REFINEMENT_R2.md`](REFINEMENT_R2.md) for the round-3 list.
- **The axiom J_a = B** is assumed.
- **The &beta; signal itself** may be a calibration systematic (see the caveat in
  [`HYPOTHESIS.md`](HYPOTHESIS.md)).
- **Against a generic axion** the AIC difference is &lt; 2: not yet significant.
