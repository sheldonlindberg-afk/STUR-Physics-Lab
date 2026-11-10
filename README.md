<p align="center">
  <img src="assets/4.13.png" alt="STUR Physics Lab logo" width="160"/>
</p>

<h1 align="center">STUR Resistance Equation</h1>

<p align="center">
  <strong>A record of testing the STUR resistance equation: what failed, what survived as known physics, and the one open experimental question.</strong>
</p>

<p align="center">
  <a href="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml"><img src="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg" alt="License: CC0-1.0"></a>
</p>

<p align="center">
  <a href="https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/"><strong>Open the interactive site &rarr;</strong></a>
  &nbsp;&middot;&nbsp; <a href="docs/STUR_Resistance_Equation_Derivation_Record.pdf">Derivation record (PDF)</a>
</p>

---

## Status (November 2026)

- **The original postulate failed.** S_R = ½k_BΦ_R² matches no standard entropy, and its
  corollary E_R = ½k_BTΦ_R² has the wrong temperature dependence. The Smarr check was
  circular. See [REPORT.md](REPORT.md) and [ASSUMPTIONS.md](ASSUMPTIONS.md).
- **What stands** is a synthesis of known physics: one replica equation for horizons,
  confinement, decoherence and thermodynamics ([UNIFICATION.md](UNIFICATION.md)), plus the
  quantum-level-up derivation below.
- **Consistency audit and testable predictions:** [AUDIT.md](AUDIT.md).

<details><summary>The original candidate equation (superseded; kept for the record)</summary>

```
Phi_R = \oint_C A_mu dx^mu              <W(C)> = exp(-1/2 <Phi_R^2>)
S_R   = 1/2 k_B Phi_R^2   (postulate)   E_R    = 1/2 k_B T Phi_R^2
1/2 Phi_R^2 = sigma(mu) A  <=  A / (4 l_P^2)
```

| Result | Status now | Where |
|---|---|---|
| Visibility = Gaussian Wilson loop | Known physics | stur_verify.py |
| S_R = ½k_BΦ_R² | **Failed:** matches no standard entropy | ASSUMPTIONS.md |
| E_R = ½k_BTΦ_R² | **Failed:** Landauer covers erasure, not dephasing; wrong T-scaling | POSTULATE_TEST.md |
| Ceiling reproduces Smarr's Mc² = 2TS | **Circular:** restates an identity that was built in | ASSUMPTIONS.md §6 |
| ½Φ_R² = σ(μ)A from QCD to Planck | **Failed:** the two areas are different kinds | CONFINEMENT.md, OPEN_PROBLEMS.md |
| A fold resists collapse at a definite size | Known physics (Skyrme) | stur_verify.py |

</details>

## From the quantum level up: measurement and gravity in one equation

```
ρᵢⱼ(t) = ρᵢⱼ(0) · ⟨Eⱼ|Eᵢ⟩ · e^{i(Sᵢ − Sⱼ)/ħ}
Sᵢ = S_matter[i] + S_EM[i] + (c⁴/16πG) ∫ eᵢ T[eᵢ] d⁴x,     G = π a² c³ / (N c_s ħ),  c_s = 0.3046
```

Derived step by step from quantum fields, with gravity as TEGR torsion whose strength
comes from vacuum entanglement. It gives the double slit (V = |⟨E₁|E₂⟩|), GR's classic
tests, and a two-mass entanglement prediction. The Born rule is derived too
([BORN.md](BORN.md)). Web page: [quantum.html](https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/quantum.html).
See [DERIVATION.md](DERIVATION.md),
then [MEASUREMENT.md](MEASUREMENT.md), [GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md),
[TEGR.md](TEGR.md) and [EMERGENT.md](EMERGENT.md).

## Reproduce

```bash
pip install -r requirements.txt
python3 src/stur_verify.py        # ~20 s; prints every number in the record
python -m pytest tests/ -q        # output must match results/stur_verify_output.txt
```

## Open questions and tests

| # | Question | Test | Does it distinguish this work from standard physics? |
|---|---|---|---|
| 1 | Does gravity's field follow each branch (λ = 1) or an average (λ = 0)? | Two-diamond entanglement ([GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md)) | Only a null result would. λ = 1 is also perturbative quantum gravity's prediction |
| 2 | Diósi–Penrose collapse at 1.5×10⁻¹⁴ kg | One diamond held in superposition for 3 s ([EMERGENT.md](EMERGENT.md)) | Tests DP, not this framework |
| 3 | Kill test for the original corollary P2 | One trapped ion, two temperatures ([AUDIT.md](AUDIT.md), `src/stur_lab_test.py`) | Standard QM fixes the outcome; it can only rule P2 out |
| 4 | Equal quark and string weights in the continuum | DMRG ([NEXT_STEPS.md](NEXT_STEPS.md)) | No: it would confirm a theorem |
| 5 | 3-3-1 models behind "3 colours = 3 generations" | Z′ and bilepton searches ([REPORT.md](REPORT.md) §4) | Tests the 3-3-1 framework, which is published |

## Layout

```
index.html, assets/                 the site (GitHub Pages)
  assets/css/stur-roll-app.css      shared theme (tokens, light/dark)
  assets/css/stur-resistance.css    additions for this page
  assets/js/stur-resistance.js      reading mode, fringe visibility, Derrick curve
docs/                               derivation record (PDF)
src/stur_verify.py                  numerical verification (numpy, scipy)
src/*.py                            one script per report; outputs in results/
AUDIT.md                            consistency audit and testable predictions
results/stur_verify_output.txt      reference output, checked in CI
tests/                              regression tests
archive/                            superseded material, kept for the record
```

## Archive

The previous contents of this repository are preserved, not deleted:

- [`archive/stur-roll/`](archive/stur-roll/) &mdash; **STUR-ROLL** (cosmic birefringence,
  |&beta;| = &alpha;/2 = 0.2091&deg;): the former home page, docs, nine refinement
  rounds, code, results and tests. The site still renders at
  [`/archive/stur-roll/`](https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/archive/stur-roll/)
  and its tests still run in CI.
- [`archive/v7-toe/`](archive/v7-toe/) and [`archive/genesis-v10-stur-b/`](archive/genesis-v10-stur-b/)
  &mdash; older superseded material. See [`archive/README.md`](archive/README.md).

## License

CC0 1.0. See [LICENSE](LICENSE).
