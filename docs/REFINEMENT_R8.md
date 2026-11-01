# Refinement round 8: dark matter and dark energy

Date: 2026-10-31. Preregistration: [`R8_PREREGISTRATION.md`](R8_PREREGISTRATION.md)
(committed before any calculation, with one addendum fixing the frame reading
of D-A3 before production was computed). Scripts (captured output in [`results/`](../results/)):
[`src/checks/r8a_superheavy_dm.py`](../src/checks/r8a_superheavy_dm.py),
[`src/checks/r8b_holonomy_de.py`](../src/checks/r8b_holonomy_de.py).

## Bottom line

| Module | Verdict | Why |
|---|---|---|
| **8A** superheavy &phi; as dark matter | **no-go** (primary reading) | Masses light enough to make enough &phi; leave CMB isocurvature; masses heavy enough to avoid it make essentially none (&Omega;h&sup2; &lesssim; 10&#8315;&sup3;, needs 0.12). |
| **8B** second holonomy as dark energy | **no-go** | Works as thawing dark energy, but violates the weak gravity conjecture by ~10&#8309;&#8312; in vacuum energy. |

**STUR-ROLL does not explain dark matter or dark energy.** This is now a
calculated conclusion, against criteria fixed in advance, not a deferral.

## Module 8A: superheavy bulk scalar &phi; as dark matter

> **In plain terms.** The heavy particle &phi; that STUR-ROLL already contains
> could be dark matter if it is stable and if the end of inflation makes the
> right amount of it. It turns out there is no right amount. If &phi; is light
> enough to be made in quantity, it also leaves a pattern in the CMB that
> observations have already ruled out. If it is heavy enough to avoid that
> pattern, almost none of it is made. In R&sup2; inflation proper, the gap
> between the two is a factor of about 10 in mass, and STUR-ROLL's allowed
> range sits entirely on the "almost none" side.

**Verdict: no-go in the primary (Jordan-frame) reading. P1 and P2 cannot
hold together.**

**Inputs (computed).** R&sup2; background: scalaron mass &mu; = 2.97&times;10&sup1;&sup3;
GeV, H* = 1.47&times;10&sup1;&sup3; GeV, H_end = 7.1&times;10&sup1;&sup2; GeV. Reheating by
scalaron decay to the Higgs: T_RH = 4.6&times;10&#8313; GeV (no new parameter).
STUR-ROLL's window in the R&sup2; corner: M_&phi; &le; 2.23&times;10&sup1;&#8308; GeV =
7.52 &mu;.

| Condition | Jordan frame (primary) | Einstein frame (sensitivity) |
|---|---|---|
| P2 isocurvature threshold | M &ge; 6.59 &mu; = 1.96&times;10&sup1;&#8308; GeV, because &phi;'s mass during inflation is M e^(&minus;&phi;_s/&radic;6), ~9&times; smaller | M &ge; 0.74 &mu; = 2.2&times;10&sup1;&sup3; GeV |
| P1 abundance in the allowed range | **fails**: &Omega;h&sup2; &lesssim; 10&#8315;&sup3; at 6.59 &mu; and 7.52 &mu; (k&sup3;-weighted; &le; 10&#8315;&sup2;&ndash;4&times;10&#8315;&sup2; on the most conservative bound) | passes: &Omega;h&sup2; = 0.12 at M &asymp; 2.8 &mu; &asymp; 8.4&times;10&sup1;&sup3; GeV |
| P1 below the P2 threshold | M = 3 &mu;: &Omega;h&sup2; &asymp; 19 (overproduced), spectrum near scale-invariant on large scales | &mdash; |
| P3 no other channel | passes (M &gt; &mu;/2; T_RH &laquo; M) | passes |
| P4 correlated prediction | &mdash; | 1/L &asymp; 3.8&times;10&sup1;&sup1; GeV for any (m, f) in the corner, so the KK hypercharge boson sits at ~2.4&times;10&sup1;&sup2; GeV: **no collider signal**; r &asymp; 0.003 |

**How the Jordan-frame bound was established.** The production calculation
solves the &phi; mode equations from Bunch&ndash;Davies initial conditions through
the end of inflation and the scalaron oscillations, and reads off Bogoliubov
coefficients by projection onto the late-time adiabatic modes. Three
numerical effects were separated:

1. **Initial-condition error** scales as (aH/k_start)&#8308;. Moving the start
   from k/aH = 300 to 1000 removed an infrared excess (3&times;10&#8315;&sup1;&sup1; &rarr;
   6&times;10&#8315;&sup1;&#8308;).
2. **Virtual dressing.** The scalaron still oscillates slightly at readout
   (amplitude 4&times;10&#8315;&#8308;), dressing &phi;'s mass and producing an apparent
   n_k &asymp; 2&times;10&#8315;&sup1;&sup2;. Reading out 4&times; later, when the amplitude is 4&times;
   smaller, n_k falls 16&times;: n_k/amp&sup2; is constant to 1% (1.26 vs
   1.25&times;10&#8315;&#8309;). Subtracting it leaves real production consistent with
   zero (|n_k| &lesssim; 5&times;10&#8315;&sup1;&#8309; at the modes that dominate the number
   density).
3. **Earlier first-pass values** (&Omega;h&sup2; &asymp; 1.4&ndash;1.9 at the window edges)
   were this dressing, not production. They are recorded here because the
   first commit of this round flagged them as untrusted.

**Why the Einstein-frame pass does not rescue the module.** R&sup2; inflation is
defined in the Jordan frame, and the Jordan-frame coupling is the one that
reheats the universe (D-A4). Coupling &phi; to the Einstein-frame metric would
need a separate, unmotivated structure. The preregistration (addendum 1) fixed
the Jordan reading as primary before any production was computed, and the
Einstein reading as a sensitivity check only. It is reported because a
different inflation model, with &phi; a pure spectator, would behave like it:
**if the nucleation phase is not R&sup2; gravity, the dark-matter question
reopens** at M_&phi; &asymp; 2.8 &mu; &asymp; 6 H*, with no collider signal as its correlated
prediction.

## Module 8B: a second holonomy as dark energy

> **In plain terms.** A second hidden field, built the same way as the first,
> *can* act as dark energy, and it predicts a specific family of
> "slowly weakening" dark-energy histories. But it breaks a widely trusted
> rule of quantum gravity (the weak gravity conjecture): the field would
> need a partner particle that, if it existed, would make the vacuum energy
> about 10&#8309;&#8312; times too large. So STUR-ROLL does **not** explain dark
> energy. Dark energy stays the cosmological constant.

**Verdict: no-go (Q2 fails).**

| Condition | Result |
|---|---|
| Q1 background | **Pass.** A thawing hilltop with m&#8322; &asymp; 11&ndash;15 H&#8320; and f&#8322; &asymp; 0.08&ndash;0.09 M_Pl supplies &Omega;_DE = 0.685 with w&#8320; from &minus;1 to &minus;0.3. Lighter fields (m&#8322; &lesssim; 10 H&#8320;) never leave the hilltop from the random-walk offset and behave exactly like &Lambda;. |
| Q2 weak gravity conjecture | **Fail.** f&#8322; &ge; 0.05 M_Pl in every row with w&#8320; &lt; &minus;0.7, so the WGC needs a charged state with M_cL &le; &radic;2 M_Pl/f&#8322; &le; 28. But V&#8322; = &rho;_DE requires every charged state to have M_cL &ge; &minus;ln(&rho;_DE L&#8308;) = 134 (1/L = 0.9 TeV) to 223 (1/L = 4&times;10&sup1;&sup2; GeV). A state with M_cL ~ 1 would add ~1/L&#8308;, exceeding &rho;_DE by &ge; 2&times;10&#8309;&#8312;. Conversely, f&#8322; small enough for the WGC (&lesssim; 0.01 M_Pl) forces m&#8322; &asymp; 100 H&#8320;: the field has already rolled and oscillates (w &asymp; 0), failing Q1. |
| Q3 the core survives | **Conditional.** Wherever w&#8320; &gt; &minus;0.95, a photon coupling k&#8322; = 1 adds &ge; 0.078&deg; of rotation at every &ell;, spoiling &alpha;/2. So k&#8322; = 0 would be required, a new discrete choice. |
| Q4 prediction | **Pass (moot).** A one-parameter locus: (w&#8320;, w_a) = (&minus;0.99, &minus;0.02), (&minus;0.94, &minus;0.11), (&minus;0.80, &minus;0.37), (&minus;0.69, &minus;0.58), (&minus;0.57, &minus;0.80) for m&#8322; = 11, 12, 13, 13.5, 14 H&#8320;. It passes through the region favoured by the DESI evolving-dark-energy hint, but only for m&#8322; tuned to within ~10%: the coincidence problem restated as a mass. |
| refined de Sitter conjecture | M_Pl&sup2;\|V&Prime;\|/V = 1/(2f&#8322;&sup2;) &asymp; 60&ndash;80 on the viable rows: **satisfied**, not a tension. |

**The loophole, recorded.** A WGC-satisfying charged multiplet with exact
Bose&ndash;Fermi degeneracy contributes nothing to V&#8322;. It would need to be
degenerate to about 1 part in 10&#8309;&#8312;, which means unbroken bulk
supersymmetry for that multiplet. That is a large added assumption, so it is
recorded as an escape route, not a pass.

**Context.** The tension between axion quintessence and the weak gravity
conjecture is known in the literature (e.g. Agrawal, Obied, Steinhardt & Vafa,
arXiv:1806.09718; Ibe, Yamazaki & Yanagida, arXiv:1811.04664 &dagger;). What
round 8 adds is that, on STUR-ROLL's own circle, the gap is quantitative and
large: a factor of 5 to 10 in M_cL, i.e. 10&#8309;&#8312; in energy.
