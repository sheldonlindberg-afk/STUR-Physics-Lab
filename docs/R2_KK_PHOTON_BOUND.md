# Round 2, item 3: collider bound on the KK photon (replaces the R1.4 placeholder)

Code: [`src/checks/r2_kk_photon_bound.py`](../src/checks/r2_kk_photon_bound.py), which runs in under 1 s.
Reference labels [N1]&ndash;[N6] are listed at the end. Entries marked † still
need their numbers checked against the full text.

## Result

| | M_1 (first KK hypercharge boson) | 1/L |
|---|---|---|
| Conservative: published Z&prime;_SSM limit, ATLAS Run 2 [N1] | &gt; 5.1 TeV | &gt; 0.81 TeV |
| Conservative: ATLAS Run 2+3 [N3] (preprint)† | &gt; 5.5 TeV | &gt; 0.88 TeV |
| Estimate, including B^(1)'s ~4&ndash;5&times; larger &sigma;&times;BR | &asymp; 6.0&ndash;6.3 TeV | &asymp; 0.96&ndash;1.01 TeV |
| Contact interactions from the whole tower, ATLAS [N4] (indicative) | &gtrsim; 5.3 TeV | &gtrsim; 0.85 TeV |
| Contact interactions, LEP-II &ell;&ell; RR [N5] (preliminary) | &gt; 1.8&ndash;2.8 TeV | &mdash; |

**1/L &gtrsim; 0.9&ndash;1.0 TeV.** This is weaker than R1.4's placeholder (1/L &gt; 5 TeV), because R1.4 applied a bound on the **KK mass** directly to **1/L**. In `stur_final.py`'s convention, M_1 = 2&pi;/L (see the convention section below).

## 1. Model: what must be in the bulk

- **Only U(1)_Y is required in the bulk.** &psi; is a bulk field with electric charge, and section E says it is an SU(2)-singlet vectorlike lepton, so Y = &minus;1. SU(2)_L and SU(3)_c can stay on the brane. The KK tower is then a set of hypercharge-like Z&prime;s, B^(n).
- **Couplings.** For SM fermions at a fixed point, the even-parity tower couples to brane fields with &radic;2 g_Y Y_f. At the other fixed point the sign is (&minus;1)^n, with the same magnitude. The &radic;2 and sign pattern match the standard statement for gauge KK modes coupled to fixed-point fermions [N6]†.
- **Anomalies.** The SM is anomaly-free on the brane. &psi; is vectorlike, and the KK sum in `stur_final.py` (masses M + i(n + &theta;/2&pi;)/r with no zero mode) treats it as a full Dirac tower with no chiral zero mode. It therefore adds no U(1)_Y&sup3; anomaly. *This requires that the orbifold projection leave no chiral zero mode of &psi;. That is an input to check in the orbifold level analysis (item 1 of round 2), not something verified here.*
- **Higgs on the brane.** This is consistent, but the vev mixes B^(1) with the Z at O(v&sup2;/M_1&sup2;) ~ 10&#8315;&sup3;. That mixing is the source of the classic electroweak-precision bounds (~4&ndash;5 TeV in the all-gauge-bulk case [N6]†; weaker here because only hypercharge is in the bulk). It is negligible for the resonance search.
- **Caveat.** Brane-localised kinetic terms can suppress the brane couplings and soften all of these bounds [N6]†. We assume none.

## 2. Recast of the dilepton resonance searches

Narrow width, tree level, three massless generations (top included), and the brane Higgs doublet counted in the width:

| | B^(1) | Z&prime;_SSM |
|---|---|---|
| couplings | &radic;2 g_Y Y_f | (g/c_W)(T&#8323; &minus; Q s_W&sup2;) |
| &Gamma;/M | 3.5% | 3.0% (matches the ~3% quoted by ATLAS and CMS) |
| BR(ee) | 12.2% | 3.1% |

Drell&ndash;Yan &sigma;&times;BR(&ell;&ell;) relative to Z&prime;_SSM at the same mass, scanning the uū : dd̄ luminosity ratio w (no PDF set used):

| w | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| r = &sigma;B(B^(1)) / &sigma;B(Z&prime;_SSM) | 4.20 | 4.63 | 4.89 | 5.07 |

Since r &gt; 1 at every mass, and the &sigma;&times;BR limit is close to flat at high mass (about 0.014 fb at 6 TeV for ATLAS 139 fb&#8315;&sup1; [N1]), **the published Z&prime;_SSM mass limits are conservative lower bounds on M_1.** These are 5.1 TeV (ATLAS [N1]), 5.15 TeV (CMS [N2]) and 5.5 TeV (ATLAS Run 2+3 [N3]). The widths are similar (3.5% vs 3.0%), so the comparison is like for like.

**Estimated gain from r &gt; 1.** Going from Run 2 to Run 2+3 moved the SSM limit by 0.4 TeV for roughly a 2&ndash;3&times; gain in sensitivity. That implies d ln &sigma; / dM &asymp; 1.7&ndash;2.7 TeV&#8315;&sup1;, so r &asymp; 4.2 buys 0.5&ndash;0.8 TeV and gives **M_1 &asymp; 6.0&ndash;6.3 TeV**. This is an empirical estimate and should be replaced with the HEPData &sigma;&times;BR limit curve together with a proper PDF convolution.

## 3. Contact interactions from the whole tower

Integrating out the full tower, with M_n = nM_1 and &sum;1/n&sup2; = &pi;&sup2;/6, gives

L_eff = &minus;(&pi;&sup2;g_Y&sup2; / 3M_1&sup2;) Y_i Y_j (f&#772;_i&gamma;f_i)(f&#772;_j&gamma;f_j)   (i &ne; j), so  **&Lambda;/M_1 = &radic;(12 / (&pi; g_Y&sup2; |Y_iY_j|))**

with the normalisation 4&pi;/&Lambda;&sup2;. The ratio is 6.7 for u_Re_R, 5.5 for e_R&mu;_R, 9.5 for d_Re_R and 10.9 for e_L&mu;_L. The ATLAS non-resonant search reaches &Lambda; = 35.8 TeV [N4]; which chirality model gives this is still †. Applied to u_Re_R, that gives M_1 &gtrsim; 5.3 TeV. This is only indicative, because the ATLAS benchmarks assume u = d universal couplings and B^(1) does not. The LEP-II &ell;&ell; RR limits (&Lambda; &gt; 9.6 / 15.3 TeV, from a preliminary combination [N5]) give M_1 &gt; 1.8 / 2.8 TeV. Interference signs were not tracked.

## 4. Convention: what L means in `stur_final.py`

`g_mass(x)` = (3 + 3x + x&sup2;)e^(&minus;x)/3 with x = ML is the first-winding term of a mass-M field on a circle of **circumference L**: the worldline wraps once and costs e^(&minus;ML). `th_ratio` sums windings on the same L. So L = 2&pi;R is the covering circle, and the Z&#8322;-even photon tower has

**M_n = n/R = 2&pi;n/L, so 1/L = M_1/(2&pi;).**

The orbifold interval has length L/2 = &pi;R. Section E's "B KK modes (n/r_c)" agrees if r_c = R.

## 5. Section E grid, re-run

Using the conservative bound 1/L &gt; 0.88 TeV and the estimate 1/L &gt; 1.01 TeV:

| f [GeV] | 1/L = 1 TeV | 10&#8310; GeV | 10&sup1;&#8304; GeV | 10&sup1;&sup3; GeV |
|---|---|---|---|---|
| 3&times;10&#8313; | edge (M_f = 1.6&times;10&#8309; GeV) | allowed (1.9&times;10&#8312;) | H_nuc window closed | closed |
| 10&sup1;&sup2; | edge (1.5&times;10&#8309;) | allowed (1.8&times;10&#8312;) | allowed (2.2&times;10&sup1;&sup2;) | closed |
| 3&times;10&sup1;&#8308; | edge (1.4&times;10&#8309;) | allowed (1.7&times;10&#8312;) | allowed (2.1&times;10&sup1;&sup2;) | allowed (2.3&times;10&sup1;&#8309;) |

"Edge" means allowed under the conservative bound and excluded under the estimate.

**Impact.** Section E's "allowed from 1/L ~ 10 GeV" is still wrong. The lower end is **1/L &asymp; 0.9&ndash;1 TeV**, not the 5 TeV of R1.4. The lightest viable &psi; is M_f &asymp; 1.4&times;10&#8309; GeV, so the &psi; mass range is about 10&#8309;&ndash;10&sup1;&#8309; GeV, beyond any collider. The KK hypercharge boson at M_1 &asymp; 2&pi;/L is the **only** collider-accessible state, and only at the 1/L &asymp; 1 TeV edge, where M_1 &asymp; 6 TeV is within reach of the HL-LHC. Its &sigma;&times;BR being about 4.2&ndash;5&times; that of Z&prime;_SSM at fixed mass is a distinguishing signature. This is a candidate for round-2 item 1, a prediction distinct from Lee et al., although it only arises at the edge of parameter space.

## New references

- [N1] ATLAS Collaboration, "Search for high-mass dilepton resonances using 139 fb&#8315;&sup1; of pp collision data collected at &radic;s = 13 TeV with the ATLAS detector," *Phys. Lett. B* **796**, 68 (2019), arXiv:1903.06248. Z&prime;_SSM &gt; 5.1 TeV; &sigma;&times;BR limit ~0.014 fb at 6 TeV.
- [N2] CMS Collaboration, "Search for resonant and nonresonant new phenomena in high-mass dilepton final states at &radic;s = 13 TeV," *JHEP* **07** (2021) 208, arXiv:2103.02708. Z&prime;_SSM &gt; 5.15 TeV.
- [N3] ATLAS Collaboration, "Search for high-mass dilepton resonances in pp collisions at &radic;s = 13.6 TeV combined with 13 TeV results using the ATLAS detector," arXiv:2607.28334 (165 fb&#8315;&sup1; Run 3 + 140 fb&#8315;&sup1; Run 2). Z&prime;_SSM &gt; 5.5 TeV. † Preprint; publication status not checked.
- [N4] ATLAS Collaboration, "Search for new non-resonant phenomena in high-mass dilepton final states with the ATLAS detector," *JHEP* **11** (2020) 005, erratum *JHEP* **04** (2021) 142, arXiv:2006.12946. &Lambda; up to 35.8 TeV (observed). † Per-chirality values not checked.
- [N5] LEP Electroweak Working Group, "A combination of preliminary electroweak measurements and constraints on the Standard Model," arXiv:hep-ex/0103048 (preliminary &ell;&ell; contact-interaction limits, 133&ndash;209 GeV). † Superseded by the final LEP combination (*Phys. Rep.* 532, 2013), not checked.
- [N6] Review of gauge KK states with brane fermions: arXiv:hep-ph/0110346 (&radic;2 coupling, (&minus;1)^n sign, EWPT bounds of ~4&ndash;5 TeV, softening by brane kinetic terms). † Authors and numbers not checked against the full text. Already cited as [8], [9] in `REFERENCES.md`.
