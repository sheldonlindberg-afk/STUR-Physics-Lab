<p align="center">
  <img src="assets/4.13.png" alt="STUR Physics Lab logo" width="160"/>
</p>

<h1 align="center">STUR Resistance Equation</h1>

<p align="center">
  <strong>Resistance is one loop phase, &Phi;<sub>R</sub>: its variance is entropy, its energy cost is set by temperature, and its ceiling is set by boundary area.</strong>
</p>

<p align="center">
  <a href="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml"><img src="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg" alt="License: CC0-1.0"></a>
  <img src="https://img.shields.io/badge/New_postulates-1-orange" alt="New postulates: 1">
  <img src="https://img.shields.io/badge/Smarr_check-E_R%2FMc%C2%B2%3D0.5-brightgreen" alt="Smarr check passed">
</p>

<p align="center">
  <a href="https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/"><strong>Open the interactive site &rarr;</strong></a>
  &nbsp;&middot;&nbsp; <a href="docs/STUR_Resistance_Equation_Derivation_Record.pdf">Derivation record (PDF)</a>
</p>

---

## The candidate equation

```
Phi_R = \oint_C A_mu dx^mu              <W(C)> = exp(-1/2 <Phi_R^2>)
S_R   = 1/2 k_B Phi_R^2   (postulate)   E_R    = 1/2 k_B T Phi_R^2
1/2 Phi_R^2 = sigma(mu) A  <=  A / (4 l_P^2)
```

One line is a STUR postulate: **S_R = &frac12; k_B &Phi;_R&sup2;**. Everything else
is established physics or follows from it.

| Result | Status | Check |
|---|---|---|
| Visibility = Gaussian Wilson loop | Known physics | Monte Carlo agrees to 3 decimals |
| S_R = &frac12; k_B &Phi;_R&sup2; | **STUR postulate** | Must be tested by experiment |
| E_R = &frac12; k_B T &Phi;_R&sup2; | Follows (Landauer) | &mdash; |
| Ceiling reproduces black-hole entropy and Smarr's Mc&sup2; = 2TS | Consistency check, passed | E_R/Mc&sup2; = 0.500000 for all masses tested |
| &frac12;&Phi;_R&sup2; = &sigma;(&mu;)A spans QCD to Planck | STUR hypothesis | Running of &sigma;(&mu;) not yet derived |
| A fold resists collapse at a definite size | Known physics (Skyrme) | B=1 energy 1.2317 &times; 12&pi;&sup2;, literature 1.232 |

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

## Open problems (falsification targets)

1. **Test the postulate.** It predicts &Phi;_R&sup2; = 2E/(k_B T): at fixed energy
   deposited, a colder interferometer loses more visibility. First check whether
   standard decoherence theory already predicts this scaling.
2. **Fix the connection A_&mu;** (spin connection, U(1), or a new field).
3. **Derive &sigma;(&mu;)** across 38 orders of magnitude, keeping EM on the perimeter law.
4. **Show the QCD area and the horizon area are the same kind** (positive &Lambda;).
5. **Quark quantum numbers** from spacetime folds.
6. **Write R(&rho;) and &rho;_c in terms of &Phi;_R.**
7. **Information paradox:** where does black-hole information go?

Full statements are in the [derivation record](docs/STUR_Resistance_Equation_Derivation_Record.pdf).

## Layout

```
index.html, assets/                 the site (GitHub Pages)
  assets/css/stur-roll-app.css      shared theme (tokens, light/dark)
  assets/css/stur-resistance.css    additions for this page
  assets/js/stur-resistance.js      reading mode, fringe visibility, Derrick curve
docs/                               derivation record (PDF)
src/stur_verify.py                  numerical verification (numpy, scipy)
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
