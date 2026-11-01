# Archive triage: does anything in the archive work?

Criteria: [`ARCHIVE_TRIAGE_CRITERIA.md`](ARCHIVE_TRIAGE_CRITERIA.md), committed
before screening. Material: `archive/v7-toe/` (STUR v7 "Theory of Everything")
and `archive/genesis-v10-stur-b/` (STUR-B).

> **In plain terms.** We checked every number the old version of this project
> claimed to predict. None of them survives. Most were not predictions at all:
> the measured value was the target, and adjustable choices were made until
> the calculation hit it. A few were simply miscalculated. The archive had
> already found and admitted many of these problems itself. The ideas that
> do work, the extra-dimension holonomy and the whole-number coupling, were
> rebuilt from scratch as STUR-ROLL; that is why they survived and the rest
> did not.

## Bottom line

**No archive claim passes all four gates, so no claim becomes a round-9
candidate.** Two items are correct but are not STUR results (standard
Starobinsky inflation numbers; the integer-arithmetic checks of the F-theory
geometry). The archive's useful legacy is already inside STUR-ROLL.

## Claim by claim

G1 reproduces &middot; G2 not a fit &middot; G3 agrees with data &middot; G4 compatible with STUR-ROLL. The first gate failed is listed.

| # | Claim (archive value) | Fails | Reason |
|---|---|---|---|
| 1 | **Cabibbo angle** &lambda; = 0.229 &plusmn; 0.008 | **G2** | &lambda; = e^(&minus;&kappa;&sup2;/4) with &kappa; from a cosine potential of strength &alpha;_eff. `alpha_eff_rigorous_calculation.py` assembles &alpha;_eff = 1 &times; f_helix &times; f_KK &times; f_gauge and prints it beside "Target = 1.5000 (= 3/2)", the value "needed to reproduce &lambda;_obs". The twisted-sector factor depends on an orbifold-resolution knob &epsilon;/&sigma;, and the derivation table states "&epsilon;/&sigma; = 0.47 reproduces exact PDG Cabibbo angle". One output, at least one tuned input. (G3 alone would pass: 0.5&sigma;.) A companion document gives 0.220 for the same quantity. |
| 2 | **PMNS angles** &theta;&#8321;&#8322; = 33.41&deg; &plusmn; 0.28&deg;, etc. | **G2, G3** | The "self-consistent" &kappa;&sup2; = 6.35 does not solve its own equation &kappa;&sup2; = 8(1.916)/(1 + e^(&minus;&kappa;&sup2;/4)) (the right side gives 12.7; the solution is &kappa;&sup2; &asymp; 15). The Mathieu expansion uses a large-q series at q = 0.228. &sigma;(sin&sup2;&theta;&#8321;&#8322;) = 0.010 is &plusmn;0.62&deg;, not &plusmn;0.28&deg;. The result is assembled from unexplained terms (+0.012 "threshold", &minus;0.004 "higher order", a factor &minus;0.9). The archive's own canonical values are sin&sup2;&theta;&#8321;&#8322; = 0.249 and sin&sup2;&theta;&#8321;&#8323; = 0.0242, about 4.8&sigma; and 3.7&sigma; from NuFIT (0.307 &plusmn; 0.012; 0.0220 &plusmn; 0.0006 &dagger;). |
| 3 | **Higgs mass** 125.18 &plusmn; 1.2 GeV | **G2, G3** | The derivation computes &lambda;(M_GUT) = 0.0226, then writes "Wait, let me recalculate more carefully" and states 0.10 &plusmn; 0.01 with no calculation. Its running table is not Standard Model running: in the SM, &lambda; turns negative near 10&#8312;&ndash;10&sup1;&#8304; GeV (&asymp; &minus;0.03 at 2&times;10&sup1;&#8310; GeV at one loop), while the table stays at +0.075 to +0.100. Running down from the stated &lambda;(M_GUT) = 0.10 with SM couplings gives m_H &asymp; 150 GeV; from the first result 0.0226, about 139 GeV. The table ends at &lambda;(M_Z) = 0.1262, the measured value. |
| 4 | **&alpha;_s(M_Z)** = 0.1181 &plusmn; 0.0006 | **G1, G2** | Three attempts give &minus;0.081, 0.0164 and 0.0163; the final value is then stated as a "numerical result from DERIVATION_CHAIN" with no calculation. &alpha;_GUT&#8315;&sup1; &asymp; 24.3 with &alpha;_s &asymp; 0.118 is the textbook supersymmetric unification result; with the SM coefficients the document uses, the couplings do not unify. |
| 5 | **sin&sup2;&theta;_W, M_W, M_Z** | **G2** | sin&sup2;&theta;_W is stated equal to the measured value; M_W and M_Z then follow from standard SM relations with measured inputs. Outputs equal inputs. |
| 6 | **Muon g&minus;2** &delta;a_&mu; = 4&times;10&#8315;&sup1;&sup1; | not a test | About 50&times; below any current sensitivity; it cannot fail. |
| 7 | **Dark matter** B^(1) LKP, 920 &plusmn; 80 GeV, &Omega;h&sup2; = 0.119 | **G2, G4** | The archive's own note: "M_DM is solved for by requiring &Omega;_DM h&sup2; &asymp; 0.12" (circular). Stability needs a KK-parity-type symmetry on a Z&#8323; ("&infin;&#8323;") orbifold; STUR-ROLL is S&sup1;/Z&#8322; with brane couplings only at y = 0 (R2.2, R6), which break KK parity, so B^(1) decays. Round 8 tested STUR-ROLL's own dark-matter candidate separately (no-go). |
| 8 | **Baryon asymmetry** &eta;_B = (6.1 &plusmn; 3.0)&times;10&#8315;&sup1;&#8304; | **G2** | The archive labels the CP asymmetry &epsilon;&#8321; "fitted". With its own arithmetic fix the result is 1.76&times;10&#8315;&#8313; (2.9&times; observed); the headline combines an uncorrected intermediate with unexplained factors. It is standard neutrino leptogenesis, unrelated to the &theta; holonomy. |
| 9 | **Cosmological constant** 3.6&times;10&#8315;&#8308;&#8311; GeV&#8308; | **G2, G3** | (1/64&pi;&sup2;)m_&nu;&#8308; &times; four factors. Two factors are ones the archive's own audit refuted: F_hol = 0.846 ("NOT REPRODUCED", computed 1.311) and F_Berry = 1/4&pi;&sup2; (elsewhere "f_Berry = 1.000, verified"). With its own corrected factors the result is &asymp; 2.3&times;10&#8315;&#8308;&#8309; GeV&#8308;, 80&ndash;90&times; too large. Every heavier particle's vacuum energy (~10&#8312; GeV&#8308;) is set to zero by assertion. The quoted observation (2.846&times;10&#8315;&#8308;&#8311;) is also off; Planck gives &asymp; 2.5&times;10&#8315;&#8308;&#8311; GeV&#8308;. |
| 10 | **Fermion masses** | **G3** | Off by factors of 3.8 to 21,282 (the archive's own statement, `mass_spectrum_full.py`). |
| 11 | **Generation splitting** via Hosotani | **G4** (physics) | Models the Wilson line as a linear tilt Y&middot;v_W&middot;&theta;/2&pi; added to a periodic potential, which breaks periodicity. A Wilson line shifts KK momenta (n &rarr; n + q&theta;/2&pi;), as in STUR-ROLL; it does not tilt a localization potential. Feeds the mass spectrum of row 10. |
| 12 | **F-theory UV completion and swampland checks** | not a prediction | The integer arithmetic is consistent: &chi; = 48 + 6(h&sup1;&sup1; &minus; h&sup2;&sup1; + h&sup3;&sup1;) = 216 and h&sup2;&sup2; = 162. Whether this geometry exists, and whether it yields the Standard Model, is not shown and cannot be checked here. |
| 13 | **&theta;_QCD = 0** from a discrete symmetry | not testable here | No number is predicted; a working version needs spontaneous CP breaking with Nelson&ndash;Barr-type structure, which is not shown. |
| 14 | **STUR-2025 gravity** tanh(r/1 mm) | **G3, G4** | Fails E&ouml;t-Wash and does not flatten rotation curves (`stur_final.py` scoreboard). |
| 15 | **STUR-B** (GENESIS v10) | **G2** | The amplitude &kappa; is fitted to the measured &beta;; the file calls itself "bridge hypothesis; not derived from the STUR action". Its preregistration is intact (code hash 11dd1aaf&hellip;091e matches). Its R&sup2; fingerprint (r = 0.0035 at N* = 55) is correct but is standard Starobinsky inflation. Superseded by STUR-ROLL, which replaces the fitted &kappa; with the derived &alpha;/2. |

&dagger; Neutrino-oscillation central values and errors are approximate NuFIT
5/6 figures; the conclusions do not depend on the exact edition.

## The shortlist (checked regardless of gate order)

| Idea | Verdict |
|---|---|
| Generation splitting via Hosotani | Misapplies the Wilson line (row 11). The correct Wilson-line physics is already used in STUR-ROLL. |
| KK-triality dark matter | Incompatible with STUR-ROLL's S&sup1;/Z&#8322; and brane couplings at y = 0; its mass was set by the relic abundance (row 7). |
| Holonomy baryogenesis | Not present: the archive's mechanism is neutrino leptogenesis with a fitted CP asymmetry (row 8). A genuine holonomy mechanism would be new work, not salvage. |
| Swampland checks | Consistency arithmetic only (row 12). STUR-ROLL runs its own WGC check (R1.5, R8B). |

## What the archive does contribute

- **The idea lineage.** The orbifold holonomy, the Chern&ndash;Simons coupling and
  the tomographic test all first appeared in the archive or in STUR-B. They
  survive in STUR-ROLL because they were re-derived and checked there, not
  inherited.
- **A record of self-correction.** Many of the problems above were found and
  written into the archive itself (the audit notes, the corrected factors,
  the &chi;&sup2;/dof = 6.91 admission). This triage confirms those notes and adds
  the ones that were missed (rows 2&ndash;4, 9, 11).

## Gate 1: do the scripts run?

<!-- G1_TABLE -->
