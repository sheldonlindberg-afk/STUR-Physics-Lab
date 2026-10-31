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

## Open items

- **k = 1 is a discrete choice**, not derived. It is the minimal nonzero level.
- **The initial seed** must be large enough (&gtrsim; 1e-20 at m = 1e-30 eV). It is
  set by H_nuc/(2&pi;f), which lies in a window rather than at a derived value.
- **The axiom J_a = B** is assumed.
- **The &beta; signal itself** may be a calibration systematic (see the caveat in
  [`HYPOTHESIS.md`](HYPOTHESIS.md)).
- **Against a generic axion** the AIC difference is &lt; 2: not yet significant.
