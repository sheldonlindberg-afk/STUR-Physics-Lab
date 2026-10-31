<p align="center">
  <img src="assets/4.13.png" alt="STUR Physics Lab Logo" width="200"/>
</p>

<h1 align="center">STUR Physics Lab</h1>

<p align="center">
  <strong>STUR-ROLL: cosmic birefringence from integers</strong><br>
  <em>Lambda-CDM plus one derived sector &mdash; |&beta;| = k&alpha;/2, k = 1 &rArr; 0.2091&deg;</em>
</p>

<p align="center">
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg" alt="License: CC0-1.0"></a>
  <img src="https://img.shields.io/badge/Prediction-%7C%CE%B2%7C%3D%CE%B1%2F2%3D0.209%C2%B0-brightgreen" alt="Prediction">
  <img src="https://img.shields.io/badge/Fitted_parameters-0-blue" alt="Fitted parameters: 0">
  <img src="https://img.shields.io/badge/Decided_by-LiteBIRD-orange" alt="Decided by LiteBIRD">
</p>

---

## The hypothesis

STUR-ROLL adds a single sector to Lambda-CDM, and that sector predicts the
isotropic CMB birefringence angle from integers alone:

> **|&beta;| = k&alpha;/2, with k = 1 (the minimal level) &rArr; 0.2091&deg;. No continuous parameter is fitted.**

The scope is narrow on purpose. STUR-ROLL is **not** a replacement for
established physics:

- **Gravity is TEGR, which is GR.** STUR-ROLL therefore passes the GR
  precision tests by construction. This is consistency, not a new success.
- **The new sector carries &lesssim; 10&#8315;&#8311; of the dark-matter
  energy** in the allowed window. CMB spectra, BAO, supernovae, lensing and BBN
  are exactly those of Lambda-CDM, so the global model comparison reduces to
  the &beta; likelihood.
- **The alternatives** are GR+QFT (&beta; = 0) and a generic axion (&beta; fitted).

> **Prior art (refinement round 1).** The same observable, &beta; &asymp; 0.21 c_&gamma;&deg;
> from a hilltop axion whose walls form after recombination, was predicted by
> Lee, Murai, Takahashi & Yin, *Phys. Rev. D* 112, 043538 (2025). STUR-ROLL's
> contribution is a **UV origin** for their two assumptions: c_&gamma; = 1 from
> the 5D level quantisation, and the hilltop start from the Wilson-line
> potential flipping sign as the universe cools. See
> [`docs/REFINEMENT_R1.md`](docs/REFINEMENT_R1.md).

## The derived chain

| # | Step | Result |
|---|------|--------|
| 1 | Zero-energy start (Wheeler&ndash;DeWitt H&Psi; = 0) | the universe nucleates whole; &theta; (the R-field holonomy on S&sup1;/Z&#8322;) starts at rest in a minimum |
| 2 | 5D Chern&ndash;Simons term | L = (k&alpha;/4&pi;) &theta; F F&#771;, with k an integer |
| 3 | Bulk content: a charge-1 fermion and a neutral scalar | KK tower gives c_g = &frac12; sgn M; the parity anomaly makes the bare level half-integer &rArr; k_eff is an integer; k = 1 is minimal |
| 4 | Wilson-line potential (exact one loop) | the scalar dominates on de Sitter and at high T, so &theta; = 0 at nucleation; below T_c &asymp; 9.8/L the fermions dominate: V = m&sup2;f&sup2;(1 + cos &theta;), so &theta; = 0 becomes a hilltop and **cooling triggers the roll** |
| 5 | Roll &theta;: 0 &rarr; &pi; | &beta; = (k&alpha;/2&pi;)&middot;&pi; = **&alpha;/2** |

**Derived:** steps 1&ndash;5, k integer, the step size &pi;, and a random sign
of &beta; per region. **Discrete choice:** k = 1 (minimal). k = 2 or 3 give
0.418&deg; or 0.627&deg;, which sit at +2.5&sigma; and +6.1&sigma; from the
joint measurement. **Conditions:** the roll must start early enough (seed
&gtrsim; 10&#8315;&sup2;&#8304; at m = 10&#8315;&sup3;&#8304; eV), and f must lie in the
window 2.9&times;10&#8313; GeV to about 10&sup1;&#8308; GeV. **Assumed axiom:** the field
B with J_a = B.

Full detail: [`docs/HYPOTHESIS.md`](docs/HYPOTHESIS.md).

## Scoreboard

The scoring rule was fixed before the numbers were computed: pass/fail gates
against published measurements at 2&sigma;, then AIC = &chi;&sup2; + 2&times;(fitted
parameters) on &beta;.

| Test | GR+QFT | GR+QFT+axion | **STUR-ROLL** | STUR-2025 (superseded) |
|---|:-:|:-:|:-:|:-:|
| Cassini &gamma;, Mercury perihelion, GW speed, Eot-Wash, MICROSCOPE, electron g&minus;2, BH thermodynamics | 7 PASS | 7 PASS | **7 PASS** | Eot-Wash FAIL |
| CMB birefringence \|&beta;\| (2&sigma;) | FAIL | PASS (fitted) | **PASS (predicted)** | n.d. |
| **passed / failed** | 7 / 1 | 8 / 0 | **8 / 0** | 0 / 2 |

| AIC on &beta; | GR+QFT | axion | **STUR-ROLL** |
|---|--:|--:|--:|
| joint 2026 (ACT DR6 + Planck), 0.277 &plusmn; 0.057&deg; | 23.62 | 2.00 | **1.46** |
| ACT DR6, 0.215 &plusmn; 0.074&deg; | 8.44 | 2.00 | **0.01** |
| WMAP + Planck PR4, 0.342 &plusmn; 0.0925&deg; | 13.67 | 2.00 | 2.10 |

Computed &beta; = 0.2080&deg; (m = 10&#8315;&sup3;&#8304; eV, seed 10&#8315;&#8308;). Pulls:
&minus;1.21, &minus;0.09, &minus;1.45&sigma;.

**Reading this honestly:** against GR+QFT, &Delta;AIC = 8&ndash;22, but that is
the &beta; measurement itself, and it rests on polarization-angle calibration
via Galactic foregrounds. The ACT+Planck authors call the signal a hint. A
systematic would remove the test. Against a generic axion, STUR-ROLL does better
on 2 of 3 datasets, but &Delta;AIC &lt; 2, so the difference is **not yet
significant**. STUR-ROLL's edge is that its &beta; is a prediction while the
axion's is a fit.

## How it can be falsified (LiteBIRD)

STUR-ROLL is ruled out if any of these holds:

0. **&Delta;&beta; = &beta;_reio &minus; &beta;_rec is not in [&minus;0.21&deg;, &minus;0.15&deg;]** (round 2). This
   tomographic test is the sharpest one: about 3&ndash;4&sigma; at LiteBIRD.
1. **|&beta;| moves away from 0.209&deg;.** The amplitude is fixed at &alpha;/2.
2. **|&beta;(low &ell;) &minus; &beta;(high &ell;)| exceeds 0.209&deg;.** This
   test is calibration-free: a miscalibration rotates every &ell; by the same
   angle, so the difference is immune to it. A generic ALP has no such bound.
3. **No single &theta; mass fits the measured &beta;(&ell;).**
4. **Anisotropic birefringence appears at high &ell;.** &theta; = 0 at every
   emission point, so the recombination-era rotation is exactly uniform.

The *shape* of &beta;(&ell;) on its own does **not** discriminate: a generic ALP
with a free mass and a free amplitude reproduces it to an rms of
0.0003&ndash;0.007&deg; ([`src/alp_vs_stur.py`](src/alp_vs_stur.py)). See
[`docs/PREDICTIONS.md`](docs/PREDICTIONS.md).

## Reproduce

```bash
pip install -r requirements.txt
python src/stur_final.py          # ~30 s; output identical to results/stur_final_output.txt
python -m pytest tests/ -q        # regression: output must match EXPECTED_OUTPUT exactly
```

`src/alp_vs_stur.py` additionally needs a CLASS run directory (see
[`docs/STATUS.md`](docs/STATUS.md)).

## Repository layout

```
src/stur_final.py           derived chain, audit (A–E), scoreboard
src/alp_vs_stur.py          can a generic ALP mimic STUR-ROLL's beta(l)?
results/                    captured output of stur_final.py
tests/                      regression + sanity tests (run in CI)
docs/HYPOTHESIS.md          claim, chain, status, consistency checks, new particles
docs/PREDICTIONS.md         beta(l) tables and falsification criteria
docs/STATUS.md              what is derived, assumed, missing, and open
docs/REFINEMENT_R1.md       round 1: literature audit, corrections, open items
docs/REFINEMENT_R2.md       round 2: synthesis of four parallel checks (R2_*.md)
docs/REFERENCES.md          bibliography (with verification status)
src/checks/                 independent checks for each refinement round
index.html                  project website (GitHub Pages)
archive/v7-toe/             superseded STUR v7 "Theory of Everything" material
archive/genesis-v10-stur-b/ superseded STUR-B bridge hypothesis (GENESIS v10)
```

## What happened to STUR v7?

The previous framing of this repo (the v7.0 "Theory of Everything" with a
30-observable scorecard, the infinity helix, ERP, and the 2025 tanh(r/1 mm)
gravity law) is superseded. It is preserved unchanged in
[`archive/v7-toe/`](archive/v7-toe/) for the record, together with its website.
The 2025 tanh gravity law fails Eot-Wash and does not flatten rotation curves.
STUR-B (GENESIS v10) needed initial &theta; energy and is excluded by the full
code. See [`archive/README.md`](archive/README.md).

## License

[CC0 1.0](LICENSE) &mdash; Sheldon Lindberg, 2026.
