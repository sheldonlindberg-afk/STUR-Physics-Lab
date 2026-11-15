# Three colours and three generations from asymptotic freedom and Planck-scale perturbativity in 3-3-1 models

The repository's one research note. Everything else in the repository is worked examples
of known physics; this is the only part that claims something new. Not peer reviewed.

- **Read it:** [note331.pdf](note331.pdf) (LaTeX source [note331.tex](note331.tex));
  [NOTE_331.md](../NOTE_331.md) has the same content with more detail on each check.
- **Run it in one paste:** [src/m331_standalone.py](../src/m331_standalone.py), standard
  library only, about 15 s, 28 PASS/FAIL checks
  ([expected output](../results/m331/standalone.txt)).
- **What is new and what is not:** [NOVELTY.md](../NOVELTY.md).
- **Comments:** [open an issue](https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/issues).

## The claim in four lines

1. *Exact.* In 3-3-1 models with β = ±1/√3, anomaly cancellation fixes the quark charges
   for every N_c and makes N_g a multiple of N_c; baryons are fermions of integer charge
   only for odd N_c.
2. *One input about colour.* Baryons like ours (N_c odd, at least 3), or equivalently a
   non-abelian, asymptotically free colour group.
3. *Numerical.* Requiring every gauge coupling to stay perturbative to the Planck scale,
   from the measured TeV-scale couplings, then leaves only N_c = N_g = 3.
4. *Condition.* For β = +1/√3 this holds only if the three heavy charged leptons have a
   geometric-mean mass above 0.65 ± 0.13 TeV, which the LHC has not yet tested.

## Where each part is computed

| Part of the argument | Script | Output |
|---|---|---|
| Charges, anomalies, N_g = N_c, the colour conditions, the flipped model's relation | [m331_exact.py](../src/m331_exact.py) (core: [m331_core.py](../src/m331_core.py)) | [331_exact.txt](../results/m331/331_exact.txt) |
| The β-function coefficients a second time, from explicit matrices | [m331_matrix_check.py](../src/m331_matrix_check.py) | [331_matrix_check.txt](../results/m331/331_matrix_check.txt) |
| Two-loop Yukawa terms, dependence on the measured couplings | [m331_yukawa.py](../src/m331_yukawa.py) | [331_yukawa.txt](../results/m331/331_yukawa.txt) |
| The selection as a map of coupling space | [m331_coupling_map.py](../src/m331_coupling_map.py) | [331_coupling_map.txt](../results/m331/331_coupling_map.txt) |
| One-loop threshold matching over the heavy spectrum | [m331_threshold.py](../src/m331_threshold.py) | [331_threshold.txt](../results/m331/331_threshold.txt) |
| Three-loop gauge running and the criterion | [m331_three_loop.py](../src/m331_three_loop.py) | [three_loop.txt](../results/m331/three_loop.txt) |
| The β = +1/√3 heavy-lepton condition and its error budget | [m331_margin.py](../src/m331_margin.py) | [margin.txt](../results/m331/margin.txt) |
| Heavy leptons against the LHC and HL-LHC | [m331_heavy_lepton.py](../src/m331_heavy_lepton.py) | [heavy_lepton.txt](../results/m331/heavy_lepton.txt) |
| The scalar sector to the Planck scale | [m331_scalar.py](../src/m331_scalar.py) | [331_scalar.txt](../results/m331/331_scalar.txt) |
| The Z′ recast of the ATLAS dilepton search | [m331_zprime_recast.py](../src/m331_zprime_recast.py) | [zprime_recast.txt](../results/m331/zprime_recast.txt) |

Tests: `python -m pytest tests/test_331_*.py -q`.

## Known limits

- The β-function coefficients are derived twice inside this repository, but have not been
  compared with an external package (PyR@TE or SARAH).
- The heavy-lepton threshold carries a 20% truncation error. Three-loop Yukawa terms and
  two-loop threshold matching would be needed to reduce it; neither is computed.
- The flipped 3-3-1 model and values of β other than ±1/√3 are outside the claim.
- Alternatives to N_c = 3 are run from couplings measured in our three-colour world. The
  coupling-space map removes that assumption for the gauge running only.

## Building the PDF

```bash
cd paper && pdflatex note331.tex && pdflatex note331.tex
```

The source is a single file with an inline bibliography, so it can be submitted to arXiv
as it stands (category hep-ph).
