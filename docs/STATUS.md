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
  fermion requires a bulk photon, whose KK modes are bounded at a few TeV, so
  1/L &gtrsim; few TeV and M_f &gtrsim; 10&#8312; GeV in every allowed row.
- **Framing:** &beta; = &alpha;/2 from a hilltop roll is prior art (Lee et al. 2025).
  STUR-ROLL is a UV origin for c_&gamma; = 1 and for the hilltop start.

## Open items

- **k = 1 is a discrete choice**, not derived. Equivalently, it is the sign of the bulk mass
  relative to the half-integer bare level; k_eff = 0 is equally consistent (R1.1).
- **The initial seed** must be large enough (&gtrsim; 1e-20 at m = 1e-30 eV). It is
  set by H_nuc/(2&pi;f), which lies in a window rather than at a derived value.
- **The axiom J_a = B** is assumed.
- **The &beta; signal itself** may be a calibration systematic (see the caveat in
  [`HYPOTHESIS.md`](HYPOTHESIS.md)).
- **Against a generic axion** the AIC difference is &lt; 2: not yet significant.
