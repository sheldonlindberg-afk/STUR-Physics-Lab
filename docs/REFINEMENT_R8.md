# Refinement round 8: dark matter and dark energy

Date: 2026-10-31. Preregistration: [`R8_PREREGISTRATION.md`](R8_PREREGISTRATION.md)
(committed before any calculation, with one addendum fixing the frame reading
of D-A3 before production was computed). Scripts:
[`src/checks/r8a_superheavy_dm.py`](../src/checks/r8a_superheavy_dm.py),
[`src/checks/r8b_holonomy_de.py`](../src/checks/r8b_holonomy_de.py).

## Module 8A: superheavy bulk scalar &phi; as dark matter

**Status: in progress.** The first production run at the isocurvature
threshold gave occupation numbers at the level of the initial-condition error
floor (~10&#8315;&sup1;&#8304;), so its &Omega;h&sup2; is not yet trusted. A convergence
test with deeper initial conditions is running; the verdict will be added
here only after it converges.

<!-- 8A_SUMMARY -->

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
