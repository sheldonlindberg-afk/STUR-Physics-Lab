# Round 2, item 1: what distinguishes STUR-ROLL from hilltop domain walls?

Date: 2026-10-31. Code: [`src/checks/r2_distinct_prediction.py`](../src/checks/r2_distinct_prediction.py) (about 2 min).
Numbered references [n] refer to [`REFERENCES.md`](REFERENCES.md); new ones, [N1] onward, are listed at the end.

## The question

Lee, Murai, Takahashi & Yin [3] (LMTY) and STUR-ROLL share the same effective theory:

- the coupling L = (c&alpha;/4&pi;)&theta;FF&#771;;
- a field that starts at a hilltop and rolls to the minimum after recombination;
- an amplitude &beta; = c&alpha;/2 &asymp; 0.21c&deg;.

Any discriminator must therefore come from what STUR-ROLL's 5D sector **fixes** that LMTY leave free. Five candidates are checked below.

## Bottom line

| Rank | Observable | STUR-ROLL | LMTY | Discriminates? |
|---|---|---|---|---|
| 1 | **Tomographic difference &Delta;&beta; = &beta;_reio &minus; &beta;_rec** | **&minus;0.15&deg; to &minus;0.21&deg;** (&minus;0.70 to &minus;1.00 &times; &alpha;/2), required by the derived amplitude | m is not fixed by the abstract. In a late-roll (dark-energy-like) regime &Delta;&beta; &asymp; 0; in an early-roll regime it equals STUR's | **Conditionally**: it separates STUR-ROLL from the dark-energy-linked branch of LMTY. LiteBIRD, &sigma;(&Delta;&beta;) &asymp; 0.05&deg; [N1]: a 2.9&ndash;4.2&sigma; separation |
| 2 | **Contribution of &theta; to late-time evolving dark energy** | **None**: roll at z &asymp; 4&ndash;300, &le; 1% of &rho;_DE before it, &Omega;_&theta; &lesssim; 10&#8315;&#8309; today | the hilltop "naturally enhances its abundance &hellip; thus contributing to the dark energy component" [3] | **Yes, at the model level.** If the DESI evolving-dark-energy hint is confirmed *and* tied to the birefringent field, STUR-ROLL is disfavoured |
| 3 | Seed statistics / wall in our Hubble volume | mean displacement exactly 0; P(wall) &asymp; 0.1&ndash;0.2 | "near a hilltop" allows an offset &theta;&#772; &ne; 0 | No. Probabilistic, and identical to LMTY when &theta;&#772; = 0 |
| 4 | Potential shape (N_DW = 1, &Delta;&theta; = &pi;) | exact at one loop; harmonics suppressed by e^(&minus;ML) | observationally degenerate via the combination c_&gamma;/N_DW | No |
| 5 | UV relics: KK photon, &psi;, GW from T_c | KK photon at 1/L, anywhere from about 5 TeV to f/8; &psi; &gtrsim; 10&#8312; GeV; no GW | absent | Only if a KK photon happens to be light. **Not a prediction** |

**Honest summary.** STUR-ROLL has **no observable that differs from LMTY across all of LMTY's parameter space.** What it does have is a **sharp, falsifiable restriction**: the derived amplitude &alpha;/2 holds only in a window of &theta; masses (2&times;10&#8315;&sup3;&sup1; &lesssim; m &lesssim; 10&#8315;&sup2;&#8312; eV). That window forces

1. a large negative tomographic difference, &Delta;&beta; &asymp; &minus;(0.7&ndash;1.0)&alpha;/2, and
2. no birefringent contribution to late-time dark energy.

LMTY's dark-energy branch predicts the opposite on both counts.

## D1. The mass window required by the derived amplitude

&beta; = &alpha;/2 needs two things: &theta; must have reached &pi; by today, and &theta; must still be near 0 at recombination. With seed 10&#8315;&#8308; (the code's grid):

| m [eV] | lands/&pi; | &theta;(z*) | z_roll (&theta; = &pi;/2) | &beta;_rec | &beta;_reio (&ell; = 2) | &Delta;&beta; | &alpha;/2 within 3%? |
|---|---|---|---|---|---|---|---|
| 1e-32 | 0.002 | 1e-4 | not yet | 0.0003&deg; | 0.0003&deg; | &minus;0.000&deg; | no |
| 3e-32 | 0.644 | 1e-4 | 0.4 | 0.135&deg; | 0.125&deg; | &minus;0.010&deg; | no |
| 1e-31 | 0.966 | 1e-4 | 2.4 | 0.202&deg; | 0.121&deg; | &minus;0.081&deg; | no (&minus;3.4%) |
| 2e-31 | 1.025 | 1e-4 | 4.4 | 0.214&deg; | 0.068&deg; | &minus;0.147&deg; | yes |
| 3e-31 | 0.984 | 1e-4 | 6.1 | 0.206&deg; | 0.019&deg; | &minus;0.187&deg; | yes |
| 1e-30 | 0.995 | 1e-4 | 14.9 | 0.208&deg; | &minus;0.001&deg; | &minus;0.209&deg; | yes |
| 1e-29 | 1.000 | 1e-4 | 72 | 0.209&deg; | 0.000&deg; | &minus;0.209&deg; | yes |
| 1e-28 | 1.000 | 1.7e-4 | 324 | 0.209&deg; | 0.000&deg; | &minus;0.209&deg; | yes |

&beta;_reio comes from the reionization-only projection in `stur_final.py` (`Reion`), which agrees with CLASS to &le; 0.004&deg; for &ell; &le; 5. The upper end of the window was not pushed beyond 10&#8315;&sup2;&#8312; eV. Above roughly H(z*) &asymp; 3&times;10&#8315;&sup2;&#8313; eV &times; ln(1/seed), &theta; starts moving before recombination, and [23] places the onset of high-&ell; oscillation signatures near 10&#8315;&sup2;&#8312; eV.

Our results agree with the qualitative thresholds of Nakatsuka, Namikawa & Komatsu [23]. A field with m &gtrsim; 10&#8315;&sup3;&sup2; eV evolves before reionization and produces different birefringence at low &ell; (&ell; &lesssim; 10) and high &ell;, whereas m &lesssim; H&#8320; behaves as dark energy.

## D2. Tomography is the sharpest test

Across the window, STUR-ROLL predicts

**&Delta;&beta; &equiv; &beta;_reio &minus; &beta;_rec &isin; [&minus;0.209&deg;, &minus;0.146&deg;],**

which is &minus;0.21&deg; for m &ge; 10&#8315;&sup3;&#8304; eV. In other words, the reionization bump is essentially unrotated. LiteBIRD can measure &Delta;&beta; to about 0.05&deg; [N1], which puts STUR-ROLL 2.9&ndash;4.2&sigma; away from &Delta;&beta; = 0. This measurement is insensitive to absolute angle miscalibration [N1], which is the main caveat on the current &beta; signal.

What it rules out:

- **Any hilltop or ALP model whose rotation happens after reionization**, which gives &Delta;&beta; &asymp; 0. That includes LMTY's dark-energy branch.
- **A miscalibration explanation**, which also gives &Delta;&beta; = 0.

What it does **not** rule out: LMTY with m in the same window. In that case both models give the same &beta;(&ell;).

This sharpens STUR-ROLL's falsification criteria in [`PREDICTIONS.md`](PREDICTIONS.md). Besides the bound |&Delta;&beta;| &le; &alpha;/2, STUR-ROLL now predicts **|&Delta;&beta;| &ge; 0.7 &times; &alpha;/2 &asymp; 0.15&deg;**. A LiteBIRD &Delta;&beta; consistent with 0, together with |&beta;| &asymp; 0.2&deg;, would falsify STUR-ROLL as formulated (the derived &alpha;/2).

## D3. Dark-energy budget

Take the hilltop energy 2m&sup2;f&sup2; at the largest f allowed by the wall bound of section C, f_max = &radic;(10&sup1;&#8312; eV&sup3;/8m):

| m [eV] | f_max [GeV] | 2m&sup2;f&sup2; / &rho;_DE | z_roll | &Omega;_&theta; today (matter-like) |
|---|---|---|---|---|
| 2e-31 | 7.9e14 | 2.0e-3 | 4.4 | 8.5e-6 |
| 3e-31 | 6.5e14 | 3.0e-3 | 6.1 | 5.6e-6 |
| 1e-30 | 3.5e14 | 9.9e-3 | 14.9 | 1.7e-6 |
| 1e-29 | 1.1e14 | 9.9e-2 | 72 | 1.8e-7 |
| 1e-28 | 3.5e13 | 0.99 | 324 | 2.0e-8 |

Before rolling, &theta; is a small cosmological-constant-like term. It rolls at z &ge; 4, above DESI's redshift range, and where the hilltop energy is not negligible compared with &rho;_DE (m &gtrsim; 10&#8315;&sup2;&#8313; eV), the roll happens at z &gtrsim; 70, when that energy is a negligible fraction of the total. **The birefringent field cannot be the source of a z &lesssim; 2 evolving dark energy** in STUR-ROLL. LMTY explicitly link their hilltop axion to dark energy and DESI [3]. Fits of ultralight axion dark energy to DESI favour m &asymp; 10^(&minus;32.6) eV [N2], which in STUR's potential with c = 1 has not reached &pi; today (D1).

**Error found in existing docs.** Section C of `stur_final.py` (and README, HYPOTHESIS.md) estimates the &theta; energy fraction as 6(f/M_Pl)&sup2;, assuming release at H &asymp; m/3. A hilltop start delays the roll to H &asymp; m/19.5 (seed 10&#8315;&#8308;; computed). The fraction is therefore larger by (19.5/3)&sup2; &asymp; 42: about 2&times;10&#8315;&#8309; of the matter density at m = 3&times;10&#8315;&sup3;&sup1; eV, rather than &le; 4&times;10&#8315;&#8311;. The conclusion that the sector is invisible except through &beta; still holds, at the 10&#8315;&#8309; level rather than 10&#8315;&#8311;.

## D4. Seed statistics

During nucleation the scalar dominates and V''(0) &sim; m&sup2;. Since m/H_nuc &lesssim; 10&#8315;&#8308;&#8307;, the &theta; fluctuation spectrum is that of a massless field: &delta;&theta; = H_nuc/(2&pi;f) per e-fold, scale invariant. This is the same as an exact-hilltop start with inflationary fluctuations, whose wall networks are long-lived [16].

The one structural difference is that STUR-ROLL starts **exactly** at &theta; = 0 (the old minimum), so the mean in our patch is pure fluctuation, whereas "near a hilltop" in LMTY allows a classical offset. The probability that our Hubble volume contains a wall is about &radic;(2/&pi;)&radic;(&Delta;N/N_early), where &Delta;N = ln(aH|_roll / a&#8320;H&#8320;) &asymp; 0.8 at m = 10&#8315;&sup3;&#8304; eV:

| N_early | P(wall in our volume) |
|---|---|
| 10 | 0.23 |
| 30 | 0.13 |
| 60 | 0.09 |

This is a statistical statement that depends on the unknown number of e-folds, not a prediction. Item 4 of round 2 treats the seed in detail.

## D5. UV relics

- **No gravitational waves.** At T_c only the &theta;-dependent part of the free energy changes sign. &Delta;V/&rho;_rad &le; 10&#8315;&#8310;&#8313; for 1/L = 5 TeV.
- **KK photon.** It is required at 1/L, and 1/L can lie anywhere from the collider bound (a few TeV, R1.4) up to f/8 &asymp; 10&sup1;&sup3; GeV. A dilepton resonance would be suggestive, but its absence says nothing.
- **&psi;, &phi; and the B KK modes** are at &gtrsim; 10&#8312; GeV, or couple only through &psi; loops.
- **The m&ndash;f&ndash;L relation** m&sup2;f&sup2; &sim; e^(&minus;M_fL)/L&#8308; has three unknowns. It leaves the only low-energy observable, g = &alpha;/(&pi;f) between about 7&times;10&#8315;&sup1;&#8312; and 8&times;10&#8315;&sup1;&sup3; GeV&#8315;&sup1;, uncorrelated with m beyond the shared wall bound.

## New references

N1. B. D. Sherwin, T. Namikawa, "Cosmic birefringence tomography and calibration-independence with reionization signals in the CMB," *MNRAS* **520**, 3298 (2023), arXiv:2108.09287. LiteBIRD can measure &beta;_reio &minus; &beta;_rec to about 0.05&deg; (from the abstract).

N2. "Updated cosmological constraints on axion dark energy with DESI," arXiv:2503.20178. log&#8321;&#8320;(m/eV) &asymp; &minus;32.60 &plusmn; 0.12 in the ultralight regime (from search excerpts).† Authors and full numbers need to be checked against the full text.

Also used: [3] (hilltop &rarr; dark energy and DESI, from the abstract), [16], and [23] (thresholds near 10&#8315;&sup3;&sup2; and 10&#8315;&sup2;&#8312; eV, from the abstract).
