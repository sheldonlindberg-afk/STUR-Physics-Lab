# STUR Framework Version History

**Current Version:** v7.0.2 (2026-06-29), with a post-release canonical-script correction
applied 2026-07 (see final entry below).

---

## Post-v7.0.2 Canonical Script Correction (2026-07)

After v7.0.2, the canonical closure script (`stur_toe_closure.py`) was further audited and
corrected:
- The fitted f_hol=0.948 holonomy constant was removed from the η̄ derivation; η̄ is now computed
  as 0.3947 (13.4% deviation from PDG), still classified D.
- M_DM and Ω_DM h² were downgraded from D to U after an extensive documented search found no
  independent first-principles derivation for these two observables anywhere in the codebase
  (they had been carried as D on the strength of a self-consistency freeze-out fit, not an
  independent derivation).
- Current canonical scorecard: **24D + 3P + 2U + 1I = 30 observables, 83% closure**
  (κ_q = 2.417, κ_l = 2.367; 4 numerical inputs: M_Planck, v_EW, m_t, α_em).

This supersedes the "29D+0P+0U+1I=30, 100% closure" figure reported in the v7.0.0–v7.0.2 entries
below, which reflected the state of the script before this correction.

---

## Version 7.0.2 — NLO PMNS + Fermion Masses Fixed + F_XCRM Derived + dS Conjecture Proven (2026-06-29)

### Major Changes
- PMNS NLO corrections (Wolfenstein + KK tower): sin²θ₁₃ deviation improved 17% → 9.9%
- Fermion mass formula fix: m_b/m_t 292% off → 10.4%; m_τ/m_t 16.4% off → 12.9%
- de Sitter swampland conjecture proof (`DS_CONJECTURE_PROOF.md`): all 4 swampland constraints
  satisfied (Distance, WGC, Cobordism, dS); moduli-stabilization assumption honestly flagged
- F_XCRM derived (replacing hardcoded F_RG=0.47): Λ_residual deviation reduced 16.8% → 10.8%

---

## Version 7.0.1 — Tensor-to-Scalar Ratio r Added (2026-06-29)

### Major Changes
- r_eff = 0.0139 derived via XCRM Kirchhoff torsion damping of chaotic inflation (D status,
  within BICEP/Keck bound); new script `scripts/stur_inflation.py`
- CKM parameter A = 0.814 documented (NLO Mathieu half-period correction; was previously
  misdocumented as the LO value 0.655 alone)
- Scorecard at time of release: 29D+0P+0U+1I=30 (100%) — see post-v7.0.2 correction above,
  which has since revised this figure

---

## Version 7.0.0 — v7.0 Closure Series (2026-05-12 to 2026-06-29)

Five dated releases under the v7.0.0 tag, in order:

- **2026-05-12 (Leading-Order Closure):** `scripts/stur_v7_full_closure.py` introduced —
  29 observables (24D+3P+1U+1I) from 4 inputs + 3 axioms. CKM A=0.655, PMNS via U_ℓ†×U_TBM,
  dark matter M_DM=949 GeV, all per-particle fitted correction factors removed.
- **2026-05-22 (Honest Scorecard + Lemniscate CM δ_CP):** δ_CP=267.9° derived from lemniscate
  complex multiplication; repo-wide scorecard corrected to 24D+3P+1U+1I=29 (replacing an
  earlier inflated 31D+1I=32 figure).
- **2026-06-19 (Five Priority Improvements):** conceptual additions only (triangle-genesis
  ω=2π² derivation, solar neutrino Δm²₂₁ Z₃ selection rule, geological log-periodic prediction,
  XCRM_YUKAWA_SYMMETRY_DERIVATION.md §6b topological-winding argument); no scorecard change.
- **2026-06-27 (Resistance Physics Framework):** ERP axiom (E=½RΦ²), TEGR torsion resistance,
  Z₃ Mathieu-fixed-point PMNS computation, m_u status U→P; scorecard 24D+4P+0U+1I=29.
- **2026-06-29 (Full PMNS Derivation):** `scripts/stur_toe_closure.py` introduced (11-part
  canonical closure script); sin²θ₁₃ status P→D; scorecard 25D+3P+0U+1I=29.
- **2026-06-29 (100% First-Principles Closure):** m_u, Δm²₂₁, sin²θ₁₂ all P→D; scorecard
  28D+0P+0U+1I=29 — see post-v7.0.2 correction above, which has since revised this figure.

---

## Version 6.0.0 — Dynamic Infinity Helix Phase-Lock Unification (2026-02-13)

### Major Changes
- Dynamic ∞-helix topology: twist angle θ(t) as a dynamical degree of freedom; chronomagnetic
  modulation M(t); phase-lock mechanism at M=1
- TEGR (Teleparallel Gravity) adopted as foundational gravitational framework; three-pillar
  structure TEGR + XCRM + Chronomagnetics
- DERIVATION_CHAIN_INFINITY.md rewritten (9270 → ~950 lines)
- Correction-factor audit: f_boundary, f_holonomy, f_RG, N_eff flagged as unreproduced;
  χ²/dof honestly reported as 6.91 (not the previously claimed 0.009); fermion mass hierarchy
  honestly reported (4.4× geometric max vs. observed 44×)
- L_X status changed from "derived" to "OPEN"; cosmological constant changed from "solved" to
  "OPEN" (∞₃ reduces but does not solve it)

---

## Version 4.3 — Final Public Release (2026-01-27)

### Major Changes
- Complete TOE derivation chain (Parts I-XXXII)
- All 26 SM parameters derived or constrained from 4 inputs
- UV completion via F-theory identified
- Black hole entropy and holographic correspondence derived

### Documents Updated
- DERIVATION_CHAIN_INFINITY.md — Complete derivation chain

---

## Version 4.0 (2026-01-26)

### Changes
- Cosmological constant mechanism improved
- ∞-helix discrete gauge Ward identity derivation

---

## Version 3.9 (2026-01-25)

### Changes
- UV completion exploration added
- STUR paper draft prepared

---

## Version 3.8 (2026-01-24)

### Changes
- XCRM-Yukawa symmetry derivation
- Topological N_crit derivation

---

## Version 3.7 (2026-01-23)

### Changes
- Scale derivations (L_X, v, M_R)
- Holonomy enhancement mechanism

---

## Version 3.6 (2026-01-22)

### Changes
- κ corrections and η̄ derivation chain
- α parameter derivation

---

## Version 3.5 (2026-01-21)

### Initial Release
- Core derivation framework
- Boundary correction derivation
