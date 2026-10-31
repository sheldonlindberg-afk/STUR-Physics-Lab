# Round 8 preregistration: dark matter and dark energy modules

Committed **before** any round-8 calculation was run. The git history of this
file is the record: the assumptions, pass conditions and kill criteria below
may not be edited after the results exist. Results go in
[`REFINEMENT_R8.md`](REFINEMENT_R8.md).

> **In plain terms.** Before checking whether STUR-ROLL can say anything
> about dark matter or dark energy, we write down exactly what we are adding,
> what counts as success, and what counts as failure. That way the answer
> cannot be bent to fit the hope.

## Ground rules (both modules)

1. **The core is frozen.** k = 1, the roll, &beta; = &alpha;/2 and the round-7
   kill criteria are not changed by either module.
2. **Modules are conditional.** Every result is stated as "if assumptions
   D-x hold, then &hellip;". Nothing in a module enters the derived chain.
3. **No fitting to hints.** Neither module may be tuned to the DESI
   evolving-dark-energy result. Data are compared to predicted loci only.
4. **Parameter accounting.** Each new continuous input is counted. A module
   that trades a &Lambda;CDM input (&Omega;_c or &Lambda;) for a new input of
   its own gains no AIC credit; it can claim only consistency and correlated
   predictions.
5. **A no-go is a valid outcome** and is reported with the same prominence as
   a success.

## Module 8A: superheavy bulk scalar &phi; as dark matter

**Added assumptions.**

| | Statement |
|---|---|
| D-A1 | A brane-localised &phi;-number (or Z&#8322;^&phi;) symmetry forbids every &phi; decay operator. The lightest &phi; KK state is stable. |
| D-A2 | The nucleation phase is R&sup2; (Starobinsky) inflation, the R3.3 corner, with A_s = 2.1&times;10&#8315;&#8313; at N* = 55. |
| D-A3 | &phi; is minimally coupled to curvature (&xi; = 0). &xi; = 1/6 is shown as a sensitivity check only. |
| D-A4 | Reheating is the scalaron's gravitational decay into the Higgs doublet (no new parameter). T_RH = 10&#8312;&ndash;10&sup1;&#8304; GeV is shown as a sensitivity band. |

**Already fixed by STUR-ROLL.** M_&phi; = M_f + 2/L (`stur_final` step 4);
M_fL = &minus;ln(m&sup2;f&sup2;L&#8308;); the R3.3 corner 2&times;10&#8315;&sup3;&sup1; &lesssim; m &lesssim;
3&times;10&#8315;&sup3;&#8304; eV, f &asymp; 2&ndash;8&times;10&sup1;&#8308; GeV; 0.9 TeV &lesssim; 1/L &lt;
H_inf/15.06.

**Method.** Solve the R&sup2; background exactly through the end of inflation
and the scalaron oscillations. Solve the &phi; mode equations from
Bunch&ndash;Davies initial conditions and compute the late-time occupation
numbers (Bogoliubov coefficients). Convert to &Omega;_&phi;h&sup2; with
D-A4's T_RH.

**Pass conditions (all required).**

- **P1 Abundance.** Some M_&phi; inside STUR-ROLL's allowed window gives
  &Omega;_&phi;h&sup2; = 0.12.
- **P2 Isocurvature.** At that M_&phi;, the &phi; spectrum is blue at CMB
  scales (equivalently M_&phi; &ge; 3H*/2), so the CDM isocurvature bound
  &beta;_iso &lt; 0.038 is met.
- **P3 No overproduction.** No other channel produces more &phi;: in
  particular M_&phi; &gt; &mu;/2, so the scalaron cannot decay into &phi; pairs,
  and T_RH &laquo; M_&phi;, so thermal production is negligible.
- **P4 A prediction beyond &Omega;.** The module fixes at least one other
  observable (for example 1/L, the collider status of the KK hypercharge
  boson, or the &theta; mass range).

**Kill criteria.** Failing P1, P2 or P3 makes 8A a no-go. Failing only P4
downgrades it to "a consistent fit, not an explanation".

## Module 8B: a second holonomy &theta;&#8322; as dark energy

**Added assumptions.**

| | Statement |
|---|---|
| D-B1 | A second Z&#8322;-odd U(1)_B&prime; lives on the **same** circle L. Its holonomy &theta;&#8322; gets the same kind of one-loop potential, V&#8322; = m&#8322;&sup2;f&#8322;&sup2;(1 + cos &theta;&#8322;), from its own bulk fields of mass M&#8322;: m&#8322;&sup2;f&#8322;&sup2; ~ e^(&minus;M&#8322;L)/L&#8308;. |
| D-B2 | The bare cosmological constant is zero, so &theta;&#8322; must supply all of &Omega;_DE = 0.685. |
| D-B3 | &theta;&#8322; is born at 0 and made a hilltop by the same brane mechanism (R6), with offset &theta;&#8322;,i from the inflationary random walk. |
| D-B4 | &theta;&#8322;'s photon coupling has integer level k&#8322; (possibly 0). |

**Method.** Solve the thawing hilltop quintessence background with
&Omega;_DE = 0.685 today, scanning m&#8322;/H&#8320; and &theta;&#8322;,i. Compute
f&#8322;, the CPL parameters (w&#8320;, w_a), the required M&#8322;L, the electric
weak gravity conjecture, the refined de Sitter conjecture at the hilltop, and
the extra late-time rotation (k&#8322;&alpha;/2&pi;)&Delta;&theta;&#8322;.

**Pass conditions (all required).**

- **Q1 Background.** &Omega;_DE = 0.685 is reached with w&#8320; &lt; &minus;0.7
  for some (m&#8322;, &theta;&#8322;,i).
- **Q2 Weak gravity conjecture.** U(1)_B&prime; has a charged state with
  mass &le; &radic;2 g&#8324;&prime;M_Pl, with g&#8324;&prime; = 1/(f&#8322;L), without that
  state's own contribution to V&#8322; exceeding &rho;_DE.
- **Q3 The core survives.** Either k&#8322; = 0, or the late rotation
  |(k&#8322;&alpha;/2&pi;)&Delta;&theta;&#8322;| since recombination is below 0.01&deg;, so
  |&beta;| = &alpha;/2 still holds to 5%.
- **Q4 A prediction beyond fit.** The module predicts a locus in the
  (w&#8320;, w_a) plane, not a point tuned to data.

**Kill criteria.** Failing Q1 or Q2 makes 8B a no-go. Failing Q3 with
k&#8322; &ne; 0 forces k&#8322; = 0, which is to be stated as an added discrete
choice. The refined de Sitter conjecture is reported as a tension, not a
kill criterion, because its constant is not fixed.

## What would change in the main documents

- If 8A passes, `HYPOTHESIS.md` changes "Dark matter is the &Lambda;CDM
  component" to "Dark matter *can* be &phi;, conditional on D-A1&ndash;D-A4", with
  the correlated predictions listed. If 8A fails, the sentence stays and links
  to the no-go.
- The same applies to 8B and dark energy.
