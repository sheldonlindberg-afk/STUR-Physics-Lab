# R2.4: Seed statistics, domain walls, and anisotropic / time-dependent birefringence

Date: 2026-10-31. Code: [`src/checks/r2_seed_anisotropy.py`](../src/checks/r2_seed_anisotropy.py), which runs in about 25 s.
References [n] are listed in [`REFERENCES.md`](REFERENCES.md); new ones are listed at the end of this file as [R2.4-n].

## Summary

| Claim or question | Verdict |
|---|---|
| Seed window H_nuc/(2&pi;f) = 10&#8315;&#8308; &ndash; 0.3 (`stur_final`, step 5) | **Too wide.** &theta; random-walks during the de Sitter phase, so &beta; = (&alpha;/2)(1 &minus; \|&theta;_i\|/&pi;) with \|&theta;_i\| ~ s&#8320;&radic;N_tot. With &ge; 60 e-folds, &beta; within 3% (1%) of &alpha;/2 requires **s&#8320; &lesssim; 1.2&times;10&#8315;&sup2; (4&times;10&#8315;&sup3;)**. The upper part of the window is excluded |
| "&theta; = 0 at nucleation" because the scalar dominates on de Sitter | **Not sufficient.** The de Sitter minimum has curvature ~m&sup2; &#8810; H&sup2;, so it does not pin &theta;. Only a finite duration N_tot keeps &theta; near 0 |
| Recombination rotation is isotropic (section C) | **Holds.** The anisotropy from &theta;_i(n&#770;) is D_L = (&alpha;/2&pi;)&sup2;s&#8320;&sup2; &le; 1.2&times;10&#8315;&#8311; rad&sup2;, at most 10&#8315;&sup3; of the ACT DR6 bound |
| Walls only make reionization-era rotation patchy | **Holds, but the patchiness can be large.** A reionization point in an opposite-sign domain is rotated by **&alpha; = 0.418&deg;** (&Delta;&theta; = 2&pi;) for m &ge; 10&#8315;&sup3;&#8304; eV, not by ~0. The sky rms ranges from 0.02&deg; to 0.20&deg; depending on N_extra (table below) |
| Excluded by current A_CB limits? | **No.** D_L &lesssim; 0.045&times;10&#8315;&#8308; rad&sup2; at all L for every mass. The ACT/SPT/BICEP estimators also use small-scale (recombination) modes, which this signal does not touch. The relevant probe is reionization tomography [R2.4-4]†, whose bound could not be verified |
| Wall bound &sigma; &lesssim; (1 MeV)&sup3; (section C) | **Consistent.** At the section C upper edge &delta;T/T ~ 3&times;10&#8315;&#8309; and &Omega;_wall ~ 4&times;10&#8315;&#8309;, which is marginal and order-of-magnitude only. The bound applies only if a sign change lies inside our horizon |
| Time-dependent &beta; today (R1 open item 5) | **Unobservable.** Period 4&times;10&#8311;&ndash;4&times;10&#8312; yr, amplitude &le; 7&times;10&#8315;&sup3;&deg;, change over 5 yr ~5&times;10&#8315;&sup1;&#8304;&deg; |

**Correction to R1.** REFINEMENT_R1 open item 4 quotes "ACT DR6 A_CB &lt; 0.52". The ACT DR6 paper [R2.4-1] gives **A_CB = 0.05 &plusmn; 0.06, with A_CB &lt; 0.15**. The number 0.53 is an SPT limit obtained with a lensing prior [R2.4-2]. The R1 text and reference [21] should be updated.

## 1. Seed: magnitude and the hilltop requirement

**Model** (stated, not derived from the 5D action). During the de Sitter phase at Hubble rate H, the curvature of &theta;'s potential is of order m&sup2; &#8810; H&sup2;. &theta; is therefore effectively massless and random-walks: P_&theta;(k) = s&#8320;&sup2; per ln k, with s&#8320; = H/(2&pi;f). Afterwards &theta; is frozen (m &#8810; H) until H ~ m. The field at the moment of the roll is a Gaussian random field with three pieces:

- a patch mean &theta;&#772; with variance s&#8320;&sup2;N_extra, where N_extra is the number of e-folds before our present horizon scale exited;
- fluctuations with variance s&#8320;&sup2; ln(R_H0/R_s) inside our horizon;
- a smoothing scale R_s equal to the comoving Hubble radius when H = m, because sub-horizon modes have decayed by then.

**Hilltop requirement.** Since &theta;_i stays frozen through recombination, &Delta;&theta; = &pi; &minus; |&theta;_i| and &beta; = (&alpha;/2)(1 &minus; |&theta;_i|/&pi;). With |&theta;_i| ~ s&#8320;&radic;N_tot:

| s&#8320; = H/2&pi;f | max N_tot for \|&delta;&beta;\| &lt; 1% | &lt; 3% |
|---|---|---|
| 0.3 | 0.011 | 0.099 |
| 3&times;10&#8315;&sup2; | 1.1 | 9.9 |
| 4&times;10&#8315;&sup3; | 62 | 555 |
| 10&#8315;&#8308; | 9.9&times;10&#8308; | 8.9&times;10&#8309; |

With N_tot &ge; 60 the requirement is s&#8320; &lesssim; 1.2&times;10&#8315;&sup2; (3%). The lower bound s&#8320; &gtrsim; 10&#8315;&sup2;&#8304; from `stur_final` section B, needed for a timely roll, is easily compatible with this. The allowed seed window is therefore **10&#8315;&sup2;&#8304; &lesssim; s&#8320; &lesssim; 10&#8315;&sup2;**, not 10&#8315;&#8308;&ndash;0.3. This translates to **H_nuc &lesssim; 0.08 f**, which tightens `stur_final`'s condition H_nuc &lt; 2f.

**Scenario: archived GENESIS R&sup2; inflation.** If the de Sitter phase is the R&sup2; inflation of the archived GENESIS v10 pre-registration (r = 0.00355 at N* = 55, A_s = 2.1&times;10&#8315;&#8313;), then H_inf = &pi;M_Pl&radic;(A_s r/2) &asymp; 1.5&times;10&sup1;&sup3; GeV. N &ge; 55 then requires f &gtrsim; 1.8&times;10&sup1;&#8308; GeV, compared with the section C upper limits of 6.5, 3.5 and 1.1&times;10&sup1;&#8308; GeV for m = 3&times;10&#8315;&sup3;&sup1;, 10&#8315;&sup3;&#8304; and 10&#8315;&#178;&#8313; eV. **That scenario would exclude m &gtrsim; 10&#8315;&#178;&#8313; eV and leave only a narrow f band at lower m.** Whether STUR-ROLL's "nucleation" phase is this inflation is not specified in `stur_final.py`, so this is conditional.

**Comparison with the literature.** Walls seeded by inflationary fluctuations, rather than white noise, are long-lived and reflect the super-horizon structure of the initial field [16]. The wall-network power spectrum shows an excess near the Hubble scale [15]. Our random-sign model with smoothing at R_s is the simplest version of this picture. A lattice treatment as in [15, 16] would be needed for precise spectra.

## 2. Anisotropic birefringence

Convention: D_L &equiv; L(L+1)C_L^&alpha;&alpha;/2&pi; = A_CB &times; 10&#8315;&#8308; rad&sup2;. This is the BICEP/Keck XVII definition [R2.4-3]. That ACT DR6 uses the same normalisation is assumed†.

**(a) Recombination photons.** &beta;(n&#770;) = (&alpha;/2&pi;)[&theta;_obs &minus; &theta;_i(n&#770;)]. For a scale-invariant field on the sphere, D_L = s&#8320;&sup2; in units of &theta;&sup2;. Therefore D_L^&alpha;&alpha; = (&alpha;/2&pi;)&sup2;s&#8320;&sup2;:

| s&#8320; | D_L [rad&sup2;] | A_CB |
|---|---|---|
| 0.3 | 1.2&times;10&#8315;&#8311; | 1.2&times;10&#8315;&sup3; |
| 4&times;10&#8315;&sup3; | 2.2&times;10&#8315;&sup1;&sup1; | 2.2&times;10&#8315;&#8311; |
| 10&#8315;&#8308; | 1.3&times;10&#8315;&sup1;&#8308; | 1.3&times;10&#8315;&sup1;&#8304; |

This is at least a factor of 100 below ACT DR6 (A_CB &lt; 0.15) [R2.4-1] and Planck (A^&alpha;&alpha; &lt; 0.104 deg&sup2; = 0.32&times;10&#8315;&#8308; rad&sup2;) [R2.4-5]. **The section C claim holds.**

**(b) Reionization photons: random-sign domain model.** A domain of sign s sits at s&Theta;(z). The angle is

&beta;_re(n&#770;) = (&alpha;/2&pi;)[s_obs&theta;&#8320; &minus; s(n&#770;)&Theta;_re]

so the anisotropic part is &minus;(&alpha;/2&pi;)&Theta;_re s(n&#770;). The sign correlation is &lang;ss'&rang; = (2/&pi;)arcsin &rho;(r), where &rho; is the correlation coefficient of the smoothed Gaussian seed field. &Theta;_re is |&theta;| averaged over the reionization visibility function (z &lt; 30). For a field still in its linear phase this is an upper bound.

| m [eV] | z(H = m) | R_s [Mpc] | &Theta;_re/&pi; | N_extra | P_opp | sky rms [deg] | D_2 | D_10 | D_30 |
|---|---|---|---|---|---|---|---|---|---|
| 10&#8315;&sup3;&sup1; | 24 | 1586 | 0.23 | 0 / 60 / 10&#8308; | 0.49 / 0.05 / 0.005 | 0.048 / 0.017 / 0.005 | 3.6e-3 / 3.6e-4 / 3.1e-5 | 1.2e-3 / 1.3e-4 / 1.1e-5 | 3.7e-4 / 4.2e-5 / 3.6e-6 |
| 3&times;10&#8315;&sup3;&sup1; | 51 | 1097 | 0.80 | 0 / 60 / 10&#8308; | 0.49 / 0.06 / 0.005 | 0.163 / 0.060 / 0.018 | 3.5e-2 / 4.0e-3 / 3.5e-4 | 1.9e-2 / 2.4e-3 / 2.1e-4 | 5.5e-3 / 7.0e-4 / 6.1e-5 |
| 10&#8315;&sup3;&#8304; | 113 | 730 | 1.00 | 0 / 60 / 10&#8308; | 0.49 / 0.07 / 0.006 | 0.204 / 0.079 / 0.023 | 4.5e-2 / 5.9e-3 / 5.1e-4 | 3.8e-2 / 5.4e-3 / 4.7e-4 | 1.2e-2 / 1.7e-3 / 1.5e-4 |
| 3&times;10&#8315;&sup3;&#8304; | 234 | 500 | 1.00 | 0 / 60 / 10&#8308; | 0.50 / 0.08 / 0.007 | 0.204 / 0.082 / 0.024 | 3.8e-2 / 5.5e-3 / 4.7e-4 | 4.1e-2 / 6.3e-3 / 5.5e-4 | 1.6e-2 / 2.6e-3 / 2.3e-4 |
| 10&#8315;&#178;&#8313; | 510 | 327 | 1.00 | 0 / 60 / 10&#8308; | 0.50 / 0.08 / 0.007 | 0.203 / 0.085 / 0.025 | 3.1e-2 / 5.0e-3 / 4.3e-4 | 4.0e-2 / 6.5e-3 / 5.7e-4 | 2.5e-2 / 4.3e-3 / 3.8e-4 |

D_L is given in units of 10&#8315;&#8308; rad&sup2;, i.e. as an A_CB equivalent. P_opp is the probability that a reionization scattering point lies in a domain of opposite sign to ours. Distances: &chi;(z_re = 7.69) = 9037 Mpc; &chi;(z*) = 13870 Mpc.

**Reading the table.**

- **Bounded.** D_L &le; (&alpha;/2)&sup2; &asymp; 1.3&times;10&#8315;&#8309; rad&sup2; (A_CB &le; 0.13) in every case. The largest value found is 0.045, below even the ACT DR6 limit of 0.15 read naively.
- **Not probed by current A_CB limits.** Reionization E modes live at &ell; &lesssim; 10, while the ACT/SPT/BICEP estimators reconstruct rotation from small-scale, recombination-era E/B modes. The appropriate probe is reionization tomography: Planck PR4 [R2.4-4] gives the first such bound. Its numerical value and units could not be verified here†. If it were 1.3&times;10&#8315;&sup2; (in units of 10&#8315;&#8308; rad&sup2;, 1&sigma;), the N_extra &asymp; 0 rows for m &ge; 3&times;10&#8315;&sup3;&sup1; eV would be in mild tension. **Verify before using.**
- **Correction to the stur_final wording.** "&beta;_reio &asymp; 0 for m &ge; 10&#8315;&sup3;&#8304; eV" is true only within our own domain. In an opposite domain the reionization-photon rotation is &alpha; = 0.418&deg;.
- **Effect on the calibration-free test.** The low-&ell; angle becomes &beta;(2) &asymp; &alpha;&middot;f_opp, where f_opp is the opposite-domain sky fraction. Then &beta;(2) &minus; &beta;(30) &asymp; &alpha;(f_opp &minus; &frac12;). Its magnitude is still &le; &alpha;/2, so **the &alpha;/2 bound in PREDICTIONS.md survives**, but its sign is no longer fixed.
- **Large N_extra** (a long de Sitter phase before our horizon exited) makes our observable universe a single domain: P_opp &rarr; 0 and the original `stur_final` picture is recovered.

## 3. Walls today

Wall tension &sigma; = 8mf&sup2;. Assuming a scaling network with about one wall per Hubble volume, &rho; ~ &sigma;H&#8320;, and &delta;T/T ~ 2&pi;G&sigma;/H&#8320;:

| m [eV] | f [GeV] | &sigma; [eV&sup3;] | &Omega;_wall | &delta;T/T |
|---|---|---|---|---|
| 3&times;10&#8315;&sup3;&sup1; | 3&times;10&#8313; / 6.5&times;10&sup1;&#8308; | 2.2e7 / 1.0e18 | 8e-16 / 4e-5 | 6e-16 / 3e-5 |
| 10&#8315;&sup3;&#8304; | 3&times;10&#8313; / 3.5&times;10&sup1;&#8308; | 7.2e7 / 1.0e18 | 3e-15 / 4e-5 | 2e-15 / 3e-5 |
| 10&#8315;&#178;&#8313; | 3&times;10&#8313; / 1.1&times;10&sup1;&#8308; | 7.2e8 / 1.0e18 | 3e-14 / 4e-5 | 2e-14 / 3e-5 |

At the section C upper edge, &delta;T/T ~ 3&times;10&#8315;&#8309;. This is marginal, and consistent with &sigma; &lesssim; (1 MeV)&sup3; being an order-of-magnitude bound. A precise bound needs the wall-network CMB calculation. With large N_extra, so that there is no sign change inside our horizon, there is no wall bound and the upper limit on f relaxes.

## 4. Time-dependent birefringence today

After the roll, &theta; oscillates about &pi; with period 2&pi;&#8463;/m. The residual amplitude is taken from the same equation as `stur_final.roll` with seed 10&#8315;&#8308;:

| m [eV] | period [yr] | amplitude in &beta; [deg] | max change in 5 yr [deg] |
|---|---|---|---|
| 3&times;10&#8315;&sup3;&sup1; | 4.4&times;10&#8312; | 6.8&times;10&#8315;&sup3; | 4.9&times;10&#8315;&sup1;&#8304; |
| 10&#8315;&sup3;&#8304; | 1.3&times;10&#8312; | 2.0&times;10&#8315;&sup3; | 4.9&times;10&#8315;&sup1;&#8304; |
| 3&times;10&#8315;&sup3;&#8304; | 4.4&times;10&#8311; | 6.9&times;10&#8315;&#8308; | 4.9&times;10&#8315;&sup1;&#8304; |

The ACT DR6 time-dependent search [22] looks for rotation that varies within its 2017&ndash;2022 data. STUR-ROLL's oscillation is about 10&#8312; times slower, so it is **unobservable**, which closes R1 open item 5. The same residual oscillation is already part of the "lands/&pi;" spread in `stur_final` (&beta;_rec 0.206&ndash;0.210&deg;).

## Open points

- The value and units of the Planck PR4 reionization-tomography bound [R2.4-4] need checking against the full text.
- Lattice simulation of the wall network with inflationary initial conditions [15, 16] to replace the random-sign model.
- Specify what STUR-ROLL's "nucleation" phase is (its H and N_tot). This decides P_opp and, in the R&sup2;-inflation scenario, the allowed f.

## New references

Verified on 2026-10-31 through web-search abstracts and snippets only; full texts were not read. † marks items whose exact numbers or conventions are unconfirmed.

- [R2.4-1] ACT Collaboration, "The Atacama Cosmology Telescope: Constraints on the anisotropic screening and birefringence effects with DR6," arXiv:2608.27458. A_CB = 0.05 &plusmn; 0.06, A_CB &lt; 0.15 (corresponding to g_a&gamma; &lt; 4.9&times;10&#8315;&sup2;/H_I). Normalisation assumed to be the 10&#8315;&#8308; rad&sup2; convention†. This **corrects** the "0.52" quoted in R1 and in reference [21].
- [R2.4-2] SPT B-mode analysis: A_CB &lt; 1.2&times;10&#8315;&#8308;, or 0.53&times;10&#8315;&#8308; with a lensing prior (95%), as reported in arXiv:2504.13154 and 2510.07928†.
- [R2.4-3] BICEP/Keck Collaboration, "BICEP/Keck XVII: Line of sight distortion analysis&hellip;," arXiv:2210.08038. Definition L(L+1)C_L^&alpha;&alpha;/2&pi; = A_CB &times; 10&#8315;&#8308; rad&sup2; (their eq. 43).
- [R2.4-4] T. Namikawa, "Tomographic constraint on anisotropic cosmic birefringence," arXiv:2410.05149 (Planck PR4). This is the first constraint on anisotropic birefringence generated at reionization, and it is consistent with null; the numerical value is unverified†.
- [R2.4-5] A. Gruppuso et al., "Planck 2018 constraints on anisotropic birefringence and its cross-correlation with CMB anisotropy," arXiv:2008.10334. A^&alpha;&alpha; &lt; 0.104 deg&sup2; (95%).
