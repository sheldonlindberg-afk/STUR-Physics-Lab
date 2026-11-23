<p align="center">
  <img src="assets/logo.svg" alt="" width="120"/>
</p>

<h1 align="center">STUR Physics Lab: one simulation</h1>

<p align="center">
  <strong><a href="production_v2_2.py">production_v2_2.py</a>: one script, Python standard library only, nothing tuned, nothing fitted.</strong><br>
  Every number it prints is calculated from measured inputs, and the measured results it is judged against never enter the calculation.<br>
  Independent work, not peer reviewed.
</p>

<p align="center">
  <a href="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml"><img src="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg" alt="License: CC0-1.0"></a>
</p>

---

## Run it

```
python3 production_v2_2.py                     # full report, about 5 s
python3 production_v2_2.py --json-out out.json # every number, as JSON
python3 production_v2_2.py --scales 2000 5000  # other evaluation scales (GeV, above m_t)
```

Or copy the file (the [website](https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/) has a
**Copy Python script** button; on GitHub use *Copy raw file*) and paste it into any Python 3.8+
runner, notebook or AI assistant's code tool. The expected output is
[results/production_v2_2.txt](results/production_v2_2.txt). It ends with 15 self-checks, which test
the calculation itself, not its agreement with data.

## The rule

**Nothing is tuned or fitted. Everything is calculated.**

| Kind of number | Where it lives | Example |
|---|---|---|
| Measured or defined input | `INPUTS`, each with uncertainty and source | quark masses (PDG 2024), H0 (Planck 2018), T_CMB |
| Measured result, used only to judge | `COMPARISONS` | CKM fit (PDG 2024), the age of the universe (Planck 2018) |
| Numerical-method setting | `NUMERICS`; the self-checks vary each one | RK4 steps, phase-grid size, Decimal digits |
| Everything else | calculated | β-functions from Casimirs, the CKM matrix from an exact diagonalization |

[`tests/test_production.py`](tests/test_production.py) enforces the rule. It fails if any
non-integer number appears anywhere in the script outside those three tables, or if any
calculating function reads `COMPARISONS`.

Where the inputs cannot determine a quantity, the script does not pick a value. The two
phases of the quark mass matrices are the only such quantities, and each is scanned over its
whole range, [0, 2π). The prediction is the band that the scan sweeps out, and it is
compared with the measurement as a band.

## What it calculates

**Part A: cosmology** (flat ΛCDM, the Friedmann equation, 50-digit Decimal arithmetic)

| Quantity | How | Result | Measured |
|---|---|---|---|
| Ω_γ | Stefan–Boltzmann law from T_CMB | 5.450 × 10⁻⁵ | |
| Ω_r | photons + N_eff = 3.044 neutrinos | 9.218 × 10⁻⁵ | |
| Ω_Λ | flatness: 1 − Ω_m − Ω_r | 0.6846 ± 0.0073 | 0.6847 ± 0.0073 |
| Age t₀ | Romberg quadrature of ∫ da / (a H) | 13.795 Gyr | 13.787 ± 0.020 Gyr |
| q₀, z_acc, z_eq | closed forms and root finding | −0.527, 0.631, 3420 | |
| Horizon entropies | π c⁵ / (G ħ H²) | 2.27 × 10¹²² k_B today, 3.31 × 10¹²² k_B de Sitter | |

**Part B: quark flavour** (the Fritzsch six-zero texture)

1. The six measured quark masses are run with the renormalization group. Below the top mass
   this is two-loop QCD and one-loop QED, with flavour thresholds at m_c, m_b and m_t. Above
   it, the same-type mass ratios are run with one-loop Standard Model Yukawa and gauge terms,
   up to each of the four 3-3-1 benchmark scales (1.5, 3.5, 7 and 10 TeV). The top pole mass
   is converted to MS-bar at two loops. Every β-function and anomalous-dimension coefficient
   is computed from SU(N) Casimirs and the Standard Model field content, and checked against
   the textbook value.
2. The Fritzsch matrix [[0, A, 0], [A, 0, B], [0, B, C]] has its entries fixed exactly by its
   three eigenvalues. The script tries every sign assignment, finds that exactly one gives
   real entries, builds both quark sectors, and diagonalizes them exactly (Jacobi).
3. V = O_uᵀ · diag(1, e^{iσ}, e^{iτ}) · O_d for every (σ, τ). Each observable's band over the
   full phase torus is found and given the propagated input uncertainty.

Result at 3.5 TeV (the four scales agree to within 1%):

| Observable | Band over all phases | Measured (PDG 2024) | Verdict |
|---|---|---|---|
| \|V_us\| | 0.1758 – 0.2614 | 0.22501 ± 0.00068 | inside |
| \|V_cb\| | 0.0743 – 0.1949 | 0.04183 ± 0.0007 | **outside by 32σ** |
| \|V_ub\| | 0.00267 – 0.00919 | 0.00373 ± 0.00009 | inside |
| \|V_ub/V_cb\| | 0.0359 – 0.0519 | 0.0892 ± 0.0026 | **outside by 14σ** |
| \|V_td/V_ts\| | 0.2274 – 0.2328 | 0.207 ± 0.003 | **outside by 5σ** |
| J | −3.55 – 3.55 × 10⁻⁴ | 3.12 × 10⁻⁵ | inside |

**Conclusion.** With nothing tuned, the quark masses in the six-zero texture reproduce the
Cabibbo angle, |V_ub| and the size of CP violation, but for no value of the phases do they
reproduce |V_cb|. The texture is excluded. This agrees with the literature, where the
six-zero Fritzsch texture is excluded by the heavy top quark.

## What changed from production v1

The first version of `production_v2_2.py` (commit `2fa12f0`) gave χ² ≈ 3,600 for its Fritzsch
module and χ² ≈ 359,000 for its "resistance" module. Its outputs depended on hand-set numbers.
v2.2 replaces each one:

| v1 | Problem | v2.2 |
|---|---|---|
| `cp_phase_rad = 1.144` | the measured CKM phase, put in as input | removed; phases scanned over [0, 2π) |
| `theta_23_rad = 0` | a free phase set by hand | scanned |
| overlap model: `c1..c3, w1..w3, phi_12..phi_13`, `(abs(m) - 0.5)` and `2, 3 × eps` factors | arbitrary parameters, no derivation | removed |
| resistance model: `r1..r3`, `0.45 + 1.55 s^p`, widths `0.85/(1 + 0.45 r)`, phase coefficients `0.25, 0.18, 0.15, 0.22, 0.37, 0.05` | arbitrary parameters, no derivation | removed |
| cosmology–flavour feedback: `delta Omega_L = -(J/J0) ... × 1e-4`, entropy couplings `1e-6`, `1e-5`, `j_ref_scale = 3e-5` | invented couplings; `J0` was the measured J | removed: no calculated coupling exists, so there is no loop to close |
| `"status": "verified_within_1.3_sigma"` | hard-coded verdict string | removed; verdicts are computed |
| `Omega_r = 9.2e-5`, `Omega_Lambda = 0.685` | entered by hand | calculated from T_CMB, N_eff and flatness |
| `v_ew = 246.22` | entered by hand | (√2 G_F)^(−1/2) |
| FLRW ODE over `t_span = (0, 10)` from `a0 = 0.01` | arbitrary span; `a_final` meaningless | the age, by quadrature from a = 0 |
| two-loop mass anomalous dimension | off by a factor of 2 | corrected, and computed from Casimirs |
| up-type-only `3 y_t² / (32 π²)` term | not the Standard Model RGE | SM one-loop Yukawa RGE for the ratios |

## Repository layout

```
production_v2_2.py            the simulation (the only script in this repository)
results/production_v2_2.txt   its expected output
tests/test_production.py      the no-tuning rule, the self-checks, the pinned numbers
index.html                    website: one page, one Copy button
archive/                      notes and the 3-3-1 paper from the earlier codebase (prose only)
```

The earlier modules, notebooks and tools are in the git history (last at commit `2fa12f0`).
The files in `archive/` refer to them by their old paths.

## Licence

CC0 1.0: public domain. Copy it freely.
