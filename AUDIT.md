# Audit of external inputs and citations

Checked 2026-11-13. Every measured input, literature value and citation in `src/` and the
documentation was compared with its primary source, read from the source itself: the
arXiv text or TeX, the PDG 2024 tables and reviews (pdg.lbl.gov), the CODATA tables
(physics.nist.gov), HEPData, and journal metadata from INSPIRE and Crossref. Where a source
could not be reached, the row says so. Nothing in this file is recalled.

Status: **ok** = matches the source; **fixed** = corrected in this commit; **relabelled** =
value kept, attribution corrected; **open** = a discrepancy recorded but not changed;
**unverified** = no primary source retrieved.

## Fundamental constants (CODATA 2018, NIST archive table `allascii_2018.txt`)

| Quantity | Repo | Source | Status |
|---|---|---|---|
| G | 6.67430e-11 | 6.674 30(15)e-11 | ok |
| ħ, c, k_B, e | exact SI values | exact | ok |
| atomic mass unit | 1.66053906660e-27 | 1.660 539 066 60(50)e-27 | ok |
| 1/α(0) | 137.035999084 | 137.035 999 084(21) | ok |
| ħc (GeV fm) | 0.1973269804 | 197.326 980 4 MeV fm | ok |
| ε₀, 1/4πε₀ | 8.8541878128e-12, 8.9875517923e9 | 8.854 187 8128(13)e-12 | ok |

## Particle physics (PDG 2024, Phys. Rev. D 110, 030001)

| Quantity | Repo | PDG 2024 | Status |
|---|---|---|---|
| G_F | 1.1663788e-5 | 1.166 378 8(6)e-5 GeV⁻² | ok |
| α_s(M_Z) | 0.1180 | 0.1180(9) | ok |
| m_t | 172.57 | 172.57 ± 0.29 | ok |
| m_u, m_d | 2.16, 4.70 MeV | 2.16 ± 0.07, 4.70 ± 0.07 | ok |
| m_c, m_b (α_s thresholds) | 1.27, 4.18 | 1.2730(46), 4.183(7) | ok (rounded) |
| m_π⁰, m_π± | 134.9768, 139.57039 MeV | same | ok |
| g_A | 1.2754 | λ = −1.2754(13) | ok |
| nucleon mass (average) | 0.9389187 | (938.27208816 + 939.5654205)/2 | ok |
| f_π | 130.2 MeV | 130.2(1.2), decay-constant review eq. (72.14) | ok (a lattice average) |
| heavy charged lepton floor | 100 GeV | > 100.8 GeV (L → νW) | ok (rounded) |
| exotic-quark floor | 1.3 TeV, "1.3–1.6 TeV" | t′ 1280–1350, b′ 1350–1570, T₅/₃ 1460 GeV | ok (the low end is 1.28) |
| **sin²θ̂_W(M_Z)** | **0.23122** | **0.23129(4)** | **open**: 0.23122 is PDG 2018 |
| **1/α̂⁽⁵⁾(M_Z)** | **127.951 (127.95)** | **127.930(8)** | **open**: 127.951 is PDG 2022 |
| **M_Z** | **91.1876** | **91.1880(20)** | **open**: 91.1876 is PDG 2022 and earlier |
| **Γ_Z (labelled PDG 2024)** | **2.4952** | **2.4955(23)** | **open**: 2.4952 is LEP/SLD 2005, as `m331_zpole` correctly says |

The four open rows are labelled "PDG 2024" in the code but come from older editions. The
3-3-1 results depend on them: moving to PDG 2024 shifts the β = +1/√3 reference pole from
2.893 to 2.859 M_Pl and the worst case from 1.276 to 1.262 M_Pl (about 1%). No conclusion
changes, but most pinned 3-3-1 numbers change in the third digit. Left for the author to
decide between relabelling and updating.

## Lattice inputs (FLAG, read from the arXiv TeX sources)

| Quantity | Repo | Source | Status |
|---|---|---|---|
| m_ud (N_f = 2+1) | 3.364(41) MeV | FLAG 2024, table `tab:mudms` | ok |
| Σ^(1/3), F_π/F, ℓ̄₃, ℓ̄₄ | 272(5), 1.062(7), 3.07(64), 4.02(45) | FLAG 19 averages, restated in FLAG 21 (FLAG 2024 omits the LEC chapter) | ok; catalogue relabelled from "FLAG 2024" |
| NLO formulas for M_π², F_π | | FLAG 19 eq. (MF) | ok |

## Experiments and measurements

| Quantity | Repo | Source | Status |
|---|---|---|---|
| Γ(π⁰ → γγ) | 7.802 ± 0.052 ± 0.105 eV | Larin et al., Science 368, 506 (2020), abstract | ok |
| R below charm | 2.225 ± 0.020 ± 0.047 | Anashin et al., PLB 770, 174 (2017) | ok |
| \|q_p + q_e\|, q_n bound | 1e-21 e | Bressi et al., PRA 83, 052101 (2011), arXiv:1102.2766 | ok |
| q_n | (−0.4 ± 1.1)e-21 e | Baumann et al., PRD 37, 3107 (1988), abstract | ok |
| R₀ (Diósi–Penrose) | 0.54e-10 m | Donadi et al., Nat. Phys. 17, 74 (2021), eq. (6) | ok |
| inverse-square law | 38.6 µm (95% CL), separations to 52 µm | Lee et al., PRL 124, 101101 (2020) | ok; "recalled" label removed |
| g²/4π (πN) | 13.69 ± 0.12 ± 0.15 | Baru et al., NPA 872, 69 (2011), eq. (9.13) | ok |
| positronium 1S–2S | 1 233 607 216.4 MHz | Fee et al., PRL 70, 1397 (1993), abstract | ok |
| H ionization energy | 13.598434 eV | NIST ASD: 13.598434599702 | ok |
| LISA Pathfinder | 1.74 fm s⁻² Hz⁻¹ᐟ² | Armano et al., PRL 120, 061101 (2018) | ok (abstract via web search; not on arXiv) |
| NV T₂ at 77 K | comment said ~0.6 s | Bar-Gill et al., Nat. Commun. 4, 1743 (2013): T₂ ≈ 0.5 s | fixed (comment) |
| 25 kDa interference | 25 000 u | Fein et al., Nat. Phys. 15, 1242 (2019) | ok |
| Earth's heat flow | 47 TW | Davies and Davies, Solid Earth 1, 5 (2010): 47 ± 2 TW | ok; "recalled" label removed |
| silica-sphere dipoles, patches | ~100 e µm; 15–28 mV, 30–1000 nm | Afek et al. 2021; Garrett, Somers and Munday 2015 | ok |
| Cassini γ − 1 | (2.1 ± 2.3)e-5 | Bertotti, Iess and Tortora, Nature 425, 374 (2003); Will, Living Rev. Rel. (2014) | ok; full reference added |
| VLBI γ | 0.99983 ± 0.00045 | Shapiro et al., PRL 92, 121101 (2004), abstract | ok; reference added |
| ρ₀ | 1.00039 ± 0.00019 | Erler, arXiv:1908.07346 | ok |
| Z-pole data and correlations | 14 observables | LEP/SLD, Phys. Rept. 427, 257: Tables 2.13, 5.11; Gfitter Table 1 | ok (every value and both matrices) |
| Z′ validation | sin θ_ZZ′ ranges | Erler et al., JHEP 08 (2009) 017, Tables 4–5 | ok |
| ATLAS dilepton, VLL limits | HEPData files | ins1725190, ins2847252, ins2034279 | ok: a fresh download is byte-identical |
| 3-3-1 Z′ limits | 3.7, 4.2–5.4, 4, 2.64, ~2.9 TeV | Nepomuceno; Long (Table VI); Lindner; de Jesus; Salazar (Table 2) | ok |
| diamond permittivity | 5.7 | tabulated value (e.g. arXiv:2601.19054) | unverified: primary measurement not retrieved |
| diamond density | 3510 kg/m³ | 8 m_C / a³ with a = 3.5667 Å gives 3516 | open (0.17% low; lattice constant from a secondary source) |

## Astrophysics and cosmology

| Quantity | Repo | Source | Status |
|---|---|---|---|
| Λ | 1.1056e-52 m⁻² | Planck 2018 (A&A 641, A6), Table 2 with BAO: 3H₀²Ω_Λ/c² at H₀ = 67.66, Ω_Λ = 0.6889 | relabelled; Planck itself quotes (4.24 ± 0.11)e-66 eV² = 1.089e-52 m⁻² without BAO |
| GM☉ | 1.32712440018e20 | IAU 2015 nominal 1.3271244e20 (exact; arXiv:1510.07674) | fixed (1.4e-10 relative) |
| R☉ | 6.957e8 m | IAU 2015 nominal | ok |
| GM⊕, R⊕ | 3.986004418e14, 6.378137e6 | IAU 2015 nominal 3.986004e14, 6.3781e6 | ok to the IAU's precision |
| M87* ring, θ_g | 42 ± 3, 3.8 ± 0.4 µas | EHT 2019 Papers I, VI | ok |
| M87* masses | 6.6 ± 0.4e9 (stars), 3.5e9 (gas) at 17.9 Mpc | Gebhardt et al. 2011; Walsh et al. 2013 | ok |
| Sgr A* ring | 51.8 ± 2.3 µas | EHT 2022 Paper I | ok |
| **Sgr A* θ_g** | **4.8 −0.7 +0.4** | **4.8 −0.7 +1.4 µas (EHT 2022 Paper I, Table 1)** | **fixed**: the pull goes from −0.53σ to −0.16σ |
| Sgr A*, GRAVITY | 4.297e6 M☉, 8277 pc | Abuter et al., A&A 657, L12 (2022) | ok |
| **Sgr A*, Keck** | **3.975e6 M☉, 7935 pc** | **3.975e6 M☉, R₀ = 7.959 kpc (Do et al. 2019, Table 1)** | **fixed**: θ_g 4.94 → 4.93 µas, as EHT lists for Keck |
| GW250114 | m₁, m₂, M_f, χ_f, z, f₂₂₀, γ₂₂₀ | LVK, PRL 135, 111403 (2025) and its supplement | ok |
| QNM fit (l = m = 2) | (1.5251, −1.1568, 0.1292, 0.7000, 1.4187, −0.4990) | Berti, Cardoso and Will 2006, Table VIII | ok |
| Mercury's perihelion, observed | 43.1 ± 0.5″/cy | Will's review says 43″/cy | unverified (the uncertainty) |
| Mercury's orbit, GPS orbit and 38.6 µs/day | | JPL and Ashby not reachable | unverified |

## Theory results quoted

| Claim | Source | Status |
|---|---|---|
| SM couplings at m_t | Buttazzo et al., JHEP 12 (2013) 089, eqs. (55)–(60) | fixed: the central values were for M_t = 173.34 GeV, α_s = 0.1184. Now evaluated at the PDG 2024 inputs (y_t 0.9369 → 0.9329) |
| SM λ crosses zero near 1e10 GeV; metastable | same, section 4 | ok |
| Thermal Casimir–Polder | Boyer 1975 via Passante and Spagnolo 2007, eq. (11) | ok: machine-precision agreement |
| Blackbody localization rates | Romero-Isart 2011, eqs. (28)–(29) | ok |
| Gas-rate interpolation | Romero-Isart 2011, eq. (27) | open: the code uses the rms speed where the paper has the mean speed (4.19× vs 4.55× the derived rate). Design A was found with it and is kept; the conclusions use the derived rate |
| Minimum CQ noise | Tilloy and Diósi, PRD 93, 024026 (2016), eqs. (41)–(42) | open: their minimum is twice the original DP rate. Whether the repo's kernel 4πG/ħq² is the original or doubled rate depends on a normalization not resolved here; the heating ħG/(4√π R₀³) matches Donadi et al.'s original-DP figure |
| Contact term for gauge fields | Kabat, NPB 453, 281 (1995) | ok |
| Srednicki's area coefficient | 0.30 (PRL 71, 666 (1993)) | ok |
| SL(2,C) Plancherel density | arXiv:2403.17180: dm = \|µ + iλ\|² dµ dλ | ok; "from memory" label removed |
| Matching and RGE formulas | Weinberg 1980; Hall 1981; Machacek–Vaughn; Luo–Wang–Xiao | references ok; formulas validated numerically in the code, not compared with the texts |

## Citations

Every journal reference (about 95: 75 matched automatically, the rest one by one) was
resolved against INSPIRE or Crossref by journal, volume and page, and its first author and
title compared with the repo's text; every arXiv number (95) was resolved against INSPIRE. All match. Corrections: Shiryaev et al.
gains its volume and pages (57, 730); David et al. its JHEP page (065); `NOVELTY.md` dates
Barela's paper 2023 where its publication is NPB 1000 (2024).
