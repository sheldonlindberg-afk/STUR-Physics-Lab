# Status: what is reproducible, what was corrected, what is open

Last updated after refinement round 7 (2026-10-31).

> **In plain terms.** This page is the honest ledger: what has been computed
> and can be rerun, what was found wrong and fixed, and what is still open.

## Reproducible in this repo

| File | What it does | Check |
|---|---|---|
| `src/stur_final.py` | the original chain (steps 4&ndash;5), audit A&ndash;E, scoreboard | output matches its embedded `EXPECTED_OUTPUT` line for line (CI) |
| `src/checks/refinement_r1.py` | KK closed form, normalisation, prior art, KK photon, WGC | runs, under 2 s |
| `src/checks/r2_*.py` | distinguishing prediction, orbifold level, LHC bound, seed and anisotropy | each re-run and verified (R2 synthesis) |
| `src/checks/r3_nucleation.py` | nucleation window, r link, R&sup2; corner | runs, under 1 s |
| `src/checks/r4_torsion.py` | torsion-twist dynamics (superseded physics, kept for the record) | runs, ~2 min |
| `src/checks/r5_lagrangian.py` | torsion parities, orbifold positivity, brane twist | runs, ~2 s |
| `src/checks/r6_brane_angle.py` | brane angle: exact &pi;, charges, timing, full chain | runs, ~3 s |
| `src/checks/r7_audit.py` | full math audit: sign of &beta;, tomography with domains, windows, couplings | runs, ~1.5 min |
| `assets/js/stur-roll-sim.js` | in-browser roll simulator used by the website | matches `stur_final` step 5 to 4 decimals (CI, `node --test`) |
| `tests/` | 12 Python tests (including the full-output regression) and the web-simulator test | all pass (CI) |

## Corrections to `stur_final.py`

The file is kept byte-for-byte as uploaded. These statements in it are
superseded:

| Section | Original statement | Corrected | Round |
|---|---|---|---|
| step 1, step 4 | &theta; = 0 at nucleation because the scalar dominates on de Sitter | that potential is about 10&#8315;&#8312;&#8311; too weak to hold &theta;; &theta; = 0 comes from the smooth birth (axiom A1) | review, R5, R6 |
| step 4 | fermions are periodic | derived: the brane twist &vartheta; = &pi; makes &psi; effectively periodic | R6 |
| step 5 | seed window 10&#8315;&#8308; to 0.3 | s&#8320;&radic;N &lesssim; 0.094 (3%), so s&#8320; &lesssim; 0.012 for N = 60 | R2.4 |
| A | c_g = 0.49998 at Mr = 10 | truncation of the KK sum; exactly &frac12;, and the roll gives exactly &pi;/2 | R1.1, R2.2 |
| C | DM fraction &le; 10&#8315;&#8311; | about 42&times; larger (&le; 2&times;10&#8315;&#8309;); still negligible | R2.1 |
| E | allowed from 1/L ~ 10 GeV | 1/L &gtrsim; 0.8&ndash;1.0 TeV (bulk hypercharge, KK boson &gt; 5.1&ndash;5.5 TeV) | R1.4, R2.3 |
| E | nucleation window 1/L &lt; f/8 | 1/L &lt; f/197 (from H_nuc &lt; 0.076f); two grid rows become excluded | R7 A3 |
| E | M_f &gtrsim; 10&#8309; GeV at 1/L &gtrsim; 1 TeV | lightest &psi; M_f &asymp; 1.2&times;10&#8309; GeV | R7 A5 |
| B | timely roll needs seed &gtrsim; 10&#8315;&#8308;&#8304; at m = 10&#8315;&sup2;&#8313; eV | conservative: seeds down to 10&#8315;&#8312;&#8304; land within 1.1% | R7 A7 |
| D | Reion agrees with CLASS to &le; 0.004&deg; | &le; 0.005&deg; | R7 A6 |
| E | brane mixing allowed (at both branes) | allowed only at y = 0 | R2.2 |
| header | "the R-field holonomy, J_a = B" | the holonomy of a Z&#8322;-odd bulk U(1)_B (no extra axiom needed) | R5 |
| framing | &beta; = &alpha;/2 as a new observable | the observable is prior art (Lee et al. 2025); STUR-ROLL derives its assumptions | R1.3 |

Round 4's torsion twist is **withdrawn** (R5): it does not exist on S&sup1;/Z&#8322;.

## Corrections to the documents in round 7

| Statement | Corrected | Round |
|---|---|---|
| "the sign of &beta; is set once for the whole universe at the brane twist" | the twist leaves a symmetric hilltop; the sign follows &theta;_i in our region, is uniform on our sky, and can differ in distant regions | R7 A1 |
| &Delta;&beta; &isin; [&minus;0.209&deg;, &minus;0.146&deg;]; &Delta;&beta; &asymp; 0 falsifies | [&minus;0.209&deg;, &minus;0.122&deg;] with the expected opposite-domain fraction; &Delta;&beta; &asymp; 0 falsifies only without a large-scale anisotropic rotation | R7 A2 |
| g&#8324; ~ 10&#8315;&#8310;&ndash;10&#8315;&sup1;&sup1; | 10&#8315;&sup1;&sup2; to 5&times;10&#8315;&sup3; (conclusion unchanged) | R7 A4 |
| R2.1 and R2.3 bounds quoted with the superseded 1/L &gt; 5 TeV or f/8 | marked superseded in those files | R7 |

## Closed in round 6 (finishing the open list)

- **The hilltop start**: derived (R6). The smooth birth gives &theta; = 0, and the
  brane twist at exactly &pi; makes it the hilltop.
- **&delta; = &pi;**: fixed by the orbifold parity of an angle-valued brane field (R6).
- **The brane domain walls and isocurvature** of R4/R5: absent for m_&vartheta; &gtrsim; 2H (R6).
- **The R&sup2; random walk**: the exact Starobinsky &int;H&sup2;dN is 0.945&ndash;1.017 of the
  single-H estimate, so the R3.3 bounds hold to &le; 3%.
- **The origin of &vartheta;**: a field redefinition &psi; &rarr; e^{&minus;iq&vartheta;(x)&Theta;(y)}&psi; turns the brane term
  &vartheta;qJ^y into a phase e^{iq&vartheta;} in &psi;'s boundary condition at y = 0. So &vartheta; *is* the
  dynamical twist angle of the orbifold boundary condition. A UV completion
  is the phase of a brane complex scalar &Phi;_b, with the orbifold parity acting as
  &Phi;_b &rarr; &Phi;_b* and V &sup; &mu;&sup3;(&Phi;_b + &Phi;_b*) = 2&mu;&sup3;v cos &vartheta;, whose minimum is at &pi; for &mu;&sup3; &gt; 0.
  This is a construction, not a derivation from STUR's axioms.
- **The axiom J_a = B**: not needed. &theta; is just the holonomy of U(1)_B.
- **Dark matter and dark energy**: settled as **outside the theory's scope**.
  The sector has no stable particle and no field that could act as dark
  energy (`HYPOTHESIS.md`). This is a conclusion, not a deferral: the math
  checked and excluded the torsion route (R4, R5).

## Still open (cannot be closed from this session)

| Item | What is needed |
|---|---|
| Full-text check of † references, and Planck PR4 reionization bandpowers [N4.4] | arxiv.org / journals.aps.org allowed in the environment's network settings |
| `stur_genesis_simulation.py`, `precision_harness.py`, `z3_bounce_check.py`, `class_check.py` | the author's files; the CLASS &beta;(&ell;) table is hard-coded until `class_check.py` is added |
| Full CLASS/CAMB tomography for &Delta;&beta; (R2.1 used a simplified reionization model) | CLASS, plus `class_check.py` |
| Whether the &beta; signal is a calibration systematic | LiteBIRD / Simons Observatory data |

## Inputs that remain choices (not tunings)

- k = 1;
- the sign of V(&vartheta;) (minimum at &pi;);
- the charges q_&psi; odd and q_&phi; even;
- the Z&#8326; global structure;
- the smooth-birth axiom A1;
- the magnitude of m (set by M_fL, an exponentially sensitive input).
