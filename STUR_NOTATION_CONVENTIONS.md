# STUR Framework Notation Conventions

**Document Type:** Reference Standard
**Framework:** STUR v4.4
**Date:** 2026-02-04
**Purpose:** Establish authoritative notation, sign conventions, and unit standards

---

## 1. Official Sign Conventions

### 1.1 XCRM Coupling (chi)

**Standard:** chi is NEGATIVE

```
chi = -2pi/(3*L_X) < 0
```

Physical interpretation:
- Negative chi provides attractive binding energy for the helix configuration
- The XCRM energy E_XCRM = (1/2)*v^2*chi^2 is always positive (stabilizing)
- The winding number k = -chi = +2pi/(3*L_X) is positive

References:
- XCRM_YUKAWA_SYMMETRY_DERIVATION.md (Section 3)
- VLX_QUANTIZATION_DERIVATION.md (line 157)
- DERIVATION_CHAIN_HELIX.md (line 588)

### 1.2 CKM CP Phase (delta_CKM)

**Standard:** delta_CKM ~ 67 degrees (PDG convention)

```
delta_CKM = gamma = 67 +/- 4 degrees
```

Note: Some derivations compute 2*arctan(eta/rho) ~ 132 degrees, which is 2*delta_CKM. The physical CKM phase in PDG convention is ~67 degrees.

References:
- DERIVATION_CHAIN_HELIX.md (line 1844-1847)
- ETA_BAR_CORRECTION_CHAIN.md (Section 1.2)

### 1.3 PMNS CP Phase (delta_CP)

**Standard:** delta_CP ~ -90 degrees = -pi/2

```
delta_CP = -90 +/- 6 degrees
```

The negative sign arises from helix chirality (left-handed).

References:
- HIGH_PRECISION_PREDICTIONS.md (Section 1.4)

### 1.4 Berry Phase

**Standard:** Negative Berry phase gamma = -pi/3

The Berry phase around one Z_3 period contributes suppression factor:

```
F_Berry = |1 - exp(i*gamma)|^2 / (4*pi^2)
        = |1 - exp(-i*pi/3)|^2 / (4*pi^2)
        = 1/(4*pi^2) = 0.0253
```

References:
- COMPLETE_CORRECTIONS_AND_RESOLUTIONS.md (Section 1.4)

### 1.5 Casimir Energy Sign

**Standard:** Fermion Casimir contribution is NEGATIVE (repulsive)

```
N_eff ~ -149 (net negative from SM fermion dominance)
```

- Bosons contribute POSITIVE (attractive, shrinks L_X)
- Fermions contribute NEGATIVE (repulsive, expands L_X)
- Net SM effect: repulsive

References:
- LX_CASIMIR_HOLONOMY_DERIVATION.md (lines 84-85, 238)

---

## 2. Symbol Definitions (Official Glossary)

### 2.1 Primary Framework Parameters

| Symbol | Name | Definition | Standard Value | Units |
|--------|------|------------|----------------|-------|
| L_X | Compactification scale | Size of compact S^1/Z_3 dimension | See Section 3.1 | m or GeV^-1 |
| kappa | Localization parameter | Gaussian width control: sigma = (2pi/3)/kappa | 2.52 +/- 0.16 | dimensionless |
| chi | XCRM coupling | Helix-curvature coupling: chi = -2pi/(3*L_X) | negative | m^-1 or GeV |
| v | R-field VEV | Magnitude of R-field vacuum expectation value | v*L_X = 3 | GeV |
| alpha | Localization strength | alpha = (y*v*L_X / 2pi)^2 | 1.0 (natural) | dimensionless |

### 2.2 Correction Factors

| Symbol | Name | Value | Physical Origin |
|--------|------|-------|-----------------|
| f_boundary | Boundary factor | 0.65 +/- 0.05 | Finite-domain overlap truncation |
| f_sector | Sector factor | 0.62 +/- 0.05 | Z_3 sector confinement |
| f_holonomy | Holonomy factor (quarks) | 0.846 | SU(3) Haar average: exp(-1/6) |
| f_hol (eta-bar) | Holonomy factor (eta-bar) | 0.948 | Correlated fluctuations |
| f_RG | RG running factor | 0.87 | One-loop + KK thresholds |
| f_tail | Wavefunction tail factor | 1.131 +/- 0.023 | Analytic overlap ratio on S^1 |
| f_Berry | Berry phase factor | 0.975 | Geometric phase correction |
| f_EW | Electroweak threshold | 0.894 | W/Z loop corrections |

### 2.3 PMNS/CKM Parameters

| Symbol | Name | STUR Value | PDG 2024 |
|--------|------|------------|----------|
| lambda (Wolfenstein) | Cabibbo parameter | 0.220 +/- 0.016 | 0.2250 +/- 0.0007 |
| A | Wolfenstein A | 0.81 | 0.826 +/- 0.015 |
| rho-bar | Wolfenstein rho-bar | 0.159 | 0.159 +/- 0.010 |
| eta-bar | Wolfenstein eta-bar | 0.349 +/- 0.019 | 0.348 +/- 0.010 |
| theta_12 | PMNS solar angle | sin^2(theta_12) = 0.303 | 0.303 +/- 0.012 |
| theta_23 | PMNS atmospheric angle | sin^2(theta_23) = 0.558 | 0.572 +0.018/-0.023 |
| theta_13 | PMNS reactor angle | sin^2(theta_13) = 0.0220 | 0.0220 +/- 0.0007 |
| delta_CP | PMNS CP phase | -90 +/- 6 deg | -89 +/- 10 deg |

### 2.4 Greek Letter Usage Guide

**alpha (lowercase):**
1. Localization strength: alpha = (y*v*L_X / 2pi)^2 (primary STUR usage)
2. Fine structure constant: alpha_em ~ 1/137 (standard physics)
3. Fifth force coupling: alpha_fifth (gravitational deviation)
4. Positive roots in gauge theory (specialized)

**beta (lowercase):**
1. Beta function: d(coupling)/d(ln mu)
2. CKM unitarity triangle angle: beta = arg(-V_cd*V_cb / V_td*V_tb)

**gamma (lowercase):**
1. Berry phase: gamma_Berry
2. CKM unitarity triangle angle: gamma = delta_CKM ~ 67 deg
3. Anomalous dimension: gamma_R

**delta (lowercase):**
1. CP phase: delta_CKM, delta_CP
2. Corrections: delta_m, delta_theta
3. Dirac delta function: delta(x)
4. Boundary correction: delta_boundary

**eta (lowercase):**
1. CKM parameter: eta-bar (always with bar)

**theta (lowercase):**
1. Mixing angles: theta_12, theta_23, theta_13, theta_Cabibbo
2. Holonomy phase: theta_hol
3. Weinberg angle: theta_W
4. Generic phase coordinate

**kappa (lowercase):**
1. Localization parameter: kappa = (2pi/3)/sigma (PRIMARY USAGE)
2. Note: Avoid using kappa for other purposes in STUR context

**lambda (lowercase):**
1. Wolfenstein parameter: lambda = |V_us| ~ 0.225
2. Higgs quartic coupling: lambda_H
3. Fifth force range: lambda_fifth

**sigma (lowercase):**
1. Gaussian width: sigma = (2pi/3)/kappa (radians)
2. Pauli matrices: sigma^a
3. Uncertainty: sigma(x) = standard deviation

**chi (lowercase):**
1. XCRM coupling: chi = -2pi/(3*L_X) (PRIMARY USAGE)
2. Euler characteristic: chi(CY_4) (specialized)

---

## 3. Unit Conventions

### 3.1 The Two L_X Scales

**CRITICAL:** The framework contains TWO physically distinct length scales:

| Scale | Symbol | Value | Physical Origin | Usage |
|-------|--------|-------|-----------------|-------|
| Fundamental | L_X^fund | ~3 x 10^-32 m | Z_3 winding: v*L_X = 3 with v ~ M_GUT | KK mass, generation structure |
| Effective | L_X^eff or L_Casimir | ~0.8 micrometer | Casimir-holonomy balance | Fifth force, experimental tests |

**Standard convention:**
- When discussing UV physics, KK modes, proton decay: use L_X ~ 10^-32 m
- When discussing fifth force experiments, Casimir effects: use L_X ~ 0.8 micrometer
- Always specify which scale when L_X appears in new contexts

Relation:
```
L_Casimir / L_X^fund ~ (M_Pl / M_KK)^2.5 ~ 10^25
```

### 3.2 Energy Units

**Standard:** Natural units with hbar = c = 1

| Quantity | Natural Units | SI Conversion |
|----------|---------------|---------------|
| Mass | GeV | 1 GeV = 1.78 x 10^-27 kg |
| Length | GeV^-1 | 1 GeV^-1 = 1.97 x 10^-16 m |
| Energy | GeV | 1 GeV = 1.60 x 10^-10 J |
| Time | GeV^-1 | 1 GeV^-1 = 6.58 x 10^-25 s |

### 3.3 Angular Units

**Standard:** Radians for all calculations; degrees for experimental comparisons

| Context | Unit |
|---------|------|
| Z_3 phase coordinates | radians (0 to 2pi) |
| Generation positions: phi_g | 0, 2pi/3, 4pi/3 radians |
| Mixing angles (PMNS, CKM) | Report as sin^2(theta) (dimensionless) or degrees |
| CP phases | Degrees when comparing to experiment |

---

## 4. Version History and Standards

### 4.1 Current Framework Version

**Official Version:** v4.4 (2026-02-04)

Key changes in v4.4:
- Rigorous Berry phase derivation (F_Berry = 1/(4pi^2) = 0.0253)
- Two-scale L_X interpretation resolved
- chi discrepancy in F-theory resolved (chi = 216)
- All correction factors documented with provenance

### 4.2 Version Reference Standards

| Document Type | Should Reference |
|---------------|------------------|
| Core theoretical | v4.4 |
| Public-facing (web, paper) | v4.3 (public release) |
| Historical derivations | Original version + current status |

### 4.3 Documents Requiring Version Update

The following documents reference outdated versions:
- ALPHA_PARAMETER_DERIVATION.md: references v3.6 (line 916)
- KAPPA_HIGHER_ORDER_CORRECTIONS.md: references v3.6 (line 1949)
- BOUNDARY_CORRECTION_DERIVATION.md: references v3.5 (line 370)
- KAPPA_FIRST_PRINCIPLES_DERIVATION.md: references v3.5 (line 947)
- TOPOLOGICAL_NCRIT_DERIVATION.md: references v3.8 (line 493)
- STUR_WEB_OVERVIEW.md: references v5.0 (line 255) - ahead of current!

---

## 5. Derived vs. Fitted Parameters

### 5.1 Genuinely Derived (First Principles)

| Parameter | Derivation Method | Reference |
|-----------|-------------------|-----------|
| N_gen = 3 | Z_3 topology, stability | TOPOLOGICAL_NCRIT_DERIVATION.md |
| kappa = 2.52 | Mathieu equation eigenvalue | KAPPA_FIRST_PRINCIPLES_DERIVATION.md |
| f_holonomy = 0.846 | SU(3) Haar integral: exp(-1/6) | CORRECTION_FACTORS_COMPLETE.md |
| f_tail = 1.131 | Analytic overlap ratio | COMPLETE_CORRECTIONS_AND_RESOLUTIONS.md |
| chi = -2pi/(3*L_X) | XCRM-Yukawa symmetry | XCRM_YUKAWA_SYMMETRY_DERIVATION.md |
| delta_CP = -90 deg | Helix chirality | HIGH_PRECISION_PREDICTIONS.md |

### 5.2 Constrained (Derived with Some Inputs)

| Parameter | Input Required | Reference |
|-----------|----------------|-----------|
| L_X (Casimir) | N_eff from SM spectrum | LX_CASIMIR_HOLONOMY_DERIVATION.md |
| f_RG = 0.87 | alpha_s(M_Z), gauge couplings | CORRECTION_FACTORS_COMPLETE.md |
| All masses | v = 246.22 GeV (from M_Planck chain) | ABSOLUTE_MASS_DERIVATION.md |

### 5.3 Calibrated or Fitted (Requires Caution)

| Parameter | Issue | Reference |
|-----------|-------|-----------|
| f_boundary = 0.65 | Cannot derive from stated method | BOUNDARY_FACTOR_RESOLUTION.md |
| f_sector = 0.62 | Modeling choices affect value | CORRECTION_FACTORS_COMPLETE.md |
| PMNS f = 5.83 | "Effectively fitted" (admitted) | DERIVATION_CHAIN_HELIX.md:4001 |
| M_R hierarchy | Adjusted to match neutrino masses | ABSOLUTE_MASS_DERIVATION.md:1192 |

---

## 6. Standard Formulas

### 6.1 Master Mass Formula

```
m_f = m_f^naive x f_boundary x f_holonomy x f_RG x f_tail
```

For leptons, add:
```
m_l = m_f x (f_sector^lepton / f_sector^quark) x f_EW
```

### 6.2 Cabibbo Angle Formula

```
lambda = exp[-kappa^2 / 8] x f_sector x f_holonomy x f_RG x f_tail

With kappa = 2.52:
    lambda_bare = exp[-0.794] = 0.452
    lambda_phys = 0.452 x 0.62 x 0.846 x 0.87 x 1.131 = 0.233
```

### 6.3 Cosmological Constant Formula

```
Lambda_residual = (1/64*pi^2) x |Sigma| x F_RG x F_hol x F_Berry

Where:
    |Sigma| = |sum_g omega^g m_g^4| = 6.29 x 10^-42 GeV^4
    F_RG = 0.52
    F_hol = 0.846
    F_Berry = 1/(4*pi^2) = 0.0253

Result: Lambda = (1.1 +/- 0.8) x 10^-46 GeV^4
```

### 6.4 L_X Casimir-Holonomy Balance

```
L_X = (5*zeta(5)*|N_eff| / ((2*pi)^5 * c_h * ||h||^2))^(1/4)

Where:
    N_eff ~ -149 (SM fermion content)
    c_h ~ 1.35 (holonomy coupling)
    ||h||^2 = kappa^2/16 ~ 0.40

Result: L_X ~ 0.8 micrometer
```

---

## 7. Deprecated Notation

The following notation should NOT be used:

| Deprecated | Preferred | Reason |
|------------|-----------|--------|
| L_X without qualifier | L_X^fund or L_X^eff | Ambiguous scale |
| F_Berry = 1/6 | F_Berry = 0.0253 | Old estimate, now rigorously derived |
| kappa = 2.5 (exact) | kappa = 2.52 +/- 0.16 | Include uncertainty |
| f_tail = 1.05 | f_tail = 1.131 | Old value, now from analytic overlap |
| chi > 0 | chi < 0 | Sign convention standardized |

---

## 8. Document Update Protocol

When updating STUR documents:

1. **Check version reference** - Update to v4.4 if making substantive changes
2. **Verify sign conventions** - Especially for chi, delta_CP, Berry phase
3. **Specify L_X scale** - Always clarify which scale (fundamental or effective)
4. **Mark derivation status** - Use DERIVED, CONSTRAINED, or FITTED labels
5. **Cross-reference** - Link to authoritative source documents
6. **Uncertainty propagation** - Include error estimates where possible

---

**Document Status:** AUTHORITATIVE REFERENCE
**Maintainer:** Framework documentation team
**Last Updated:** 2026-02-04
