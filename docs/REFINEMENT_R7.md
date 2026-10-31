# Refinement round 7: a full audit of the math

Date: 2026-10-31. Script: [`src/checks/r7_audit.py`](../src/checks/r7_audit.py) (about 1.5 min).

> **In plain terms.** Every number in the repository was recomputed: by
> rerunning all the code, by hand, and with an independent integration that
> shares no code with the original. The core result survives untouched. Seven
> statements needed correcting; two of them changed what the theory claims,
> and both are now fixed.

## How the audit was done

1. All tests and every check script were rerun; `stur_final.py` reproduces
   [`results/stur_final_output.txt`](../results/stur_final_output.txt) line for line.
2. Key numbers were recomputed by hand: &alpha;/2, the pulls and AIC values,
   the KK closed form and its exact half-period integral, the wall bound, the
   energy fraction, the KK-boson width, branching ratio and rate ratio, the
   contact-interaction ratios, the seed bounds, the R&sup2; inflation scale and
   the oscillation period.
3. The roll was re-integrated in cosmic time with a different integrator
   (LSODA instead of DOP853). All six (m, seed) values of `stur_final`
   step 5 agree to four decimals, including &beta; = 0.2080&deg;.

## Confirmed

The headline &beta; = k&alpha;/2 = 0.20905&deg;, the normalisation
(k&alpha;/4&pi;)&theta;FF&#771; &rarr; &beta; = (k&alpha;/2&pi;)&Delta;&theta;, the exact
&Phi;(&pi;) &minus; &Phi;(0) = (&pi;/2) sgn M, the roll equation, the positivity
theorem, the parity-fixed brane extrema, the scoreboard arithmetic, and every
number quoted from the check scripts of rounds 1&ndash;6.

## Corrections

| # | Where | Was | Now | Effect |
|---|---|---|---|---|
| A1 | HYPOTHESIS step 7, PREDICTIONS | "the sign of &beta; is set once for the whole universe, at the brane twist" | V(&theta;) is even; the roll direction follows each region's &theta;_i. &beta;_rec has one sign on our sky, set by &theta; in our region; other regions can differ | **physics**: restores consistency with R2.4's patchy reionization |
| A2 | HYPOTHESIS prediction 2, PREDICTIONS, README | &Delta;&beta; &isin; [&minus;0.209&deg;, &minus;0.146&deg;]; &Delta;&beta; &asymp; 0 with \|&beta;\| &asymp; 0.2&deg; falsifies | single domain: unchanged. Expected opposite fraction (&le; 0.085): [&minus;0.209&deg;, &minus;0.122&deg;], 2.4&ndash;4.2&sigma;. &Delta;&beta; &asymp; 0 falsifies **unless** a large-scale anisotropic rotation (rms &asymp; 0.2&deg;) is also seen | **physics**: the kill criterion is now logically sound |
| A3 | `stur_final` section E, R2.3 grid | 1/L &lt; f/8 (from H_nuc &lt; 2f) | 1/L &lt; f/197 (from H_nuc &lt; 0.076f, R2.4) | two grid points change from allowed to excluded |
| A4 | HYPOTHESIS step 1 | g&#8324; ~ 10&#8315;&#8310;&ndash;10&#8315;&sup1;&sup1; | g&#8324; spans 10&#8315;&sup1;&sup2; to 5&times;10&#8315;&sup3; | none: the action cost is still &ge; 4&times;10&#8308;&theta;&sup2; |
| A5 | HYPOTHESIS, R2.3 | lightest &psi;: M_f &gtrsim; 1.4&times;10&#8309; GeV | M_f &gtrsim; 1.2&times;10&#8309; GeV | none (log accuracy) |
| A6 | PREDICTIONS, R2.1 | Reion agrees with CLASS to &le; 0.004&deg; | &le; 0.005&deg; (0.0045&deg; at m = 3&times;10&#8315;&sup3;&sup1; eV, &ell; = 4) | none |
| A7 | `stur_final` section B | timely roll needs seed &gtrsim; 10&#8315;&#8308;&#8304; at m = 10&#8315;&sup2;&#8313; eV | seeds down to 10&#8315;&#8312;&#8304; land within 1.1% | none: the original was conservative |

### A1 in detail: what fixes the sign of &beta;

After the brane twist, V(&theta;) = m&sup2;f&sup2;(1 + cos &theta;) is even in
&theta;. A region with &theta;_i &gt; 0 rolls to +&pi;; one with &theta;_i &lt; 0
rolls to &minus;&pi;. The observed angle is path-independent,
&beta; = (&alpha;/2&pi;)(&theta;_obs &minus; &theta;_emit), and &theta;_emit &asymp; 0
at recombination everywhere, so every recombination photon we receive is
rotated with the sign of &theta;_obs. The script shows this on 10&#8309; sky
points: all lie in [+0.2088&deg;, +0.2093&deg;] for &theta;_obs = +&pi;.

### A2 in detail: tomography with opposite domains

In an opposite domain the reionization-era field sits at &minus;&Theta; instead
of +&Theta;, so its photons are rotated by (&alpha;/2&pi;)(&pi; + &Theta;) =
&alpha; &minus; &beta;_own. The large-scale estimator averages the shell
(sin 2&beta; &asymp; 2&beta; to 10&#8315;&#8309;), giving

    beta_reio = (1 - f) beta_own + f (alpha - beta_own)

| m [eV] | &beta;_rec | &beta;_own | &Delta;&beta; (f = 0) | f = 0.085 | f = 0.5 |
|---|---|---|---|---|---|
| 2e-31 | 0.2144 | 0.0679 | &minus;0.1465 | &minus;0.1225 | &minus;0.0053 |
| 3e-31 | 0.2058 | 0.0188 | &minus;0.1870 | &minus;0.1546 | +0.0033 |
| 1e-30 | 0.2080 | &minus;0.0009 | &minus;0.2089 | &minus;0.1732 | +0.0010 |
| 1e-29 | 0.2091 | 0.0001 | &minus;0.2090 | &minus;0.1735 | 0.0000 |
| 1e-28 | 0.2090 | 0.0000 | &minus;0.2090 | &minus;0.1735 | 0.0000 |

f = 0.085 is the largest P_opp found in R2.4 for N_extra = 60. A half-and-half
shell (f &asymp; 0.5) needs N_extra &asymp; 0; R2.4's N_extra = 0 rows show that
it carries a sky rms of about 0.2&deg; and D_2 &asymp; 0.04&times;10&#8315;&#8308;
rad&sup2;, which reionization tomography (Planck PR4 [N4.4], LiteBIRD) can see.

### A3 in detail: the nucleation window

R2.4 tightened H_nuc &lt; 2f to H_nuc &lt; 2&pi;f(0.03&pi;)/&radic;N = 0.0764f for
N = 60. With H_nuc &gt; H_c = 15.06/L this gives 1/L &lt; f/197. On the
`stur_final` section E grid, (f, 1/L) = (10&sup1;&sup2;, 10&sup1;&#8304;) GeV and
(3&times;10&sup1;&#8308;, 10&sup1;&sup3;) GeV move from allowed to excluded. No
prediction changes; the excluded rows had &psi; at &gtrsim; 10&sup1;&sup2; GeV.

## Status after round 7

No result of rounds 1&ndash;6 that bears on the headline &beta; = &alpha;/2 was
wrong. The two physics corrections (A1, A2) sharpen how the theory is tested,
not what it predicts for the angle. `stur_final.py` remains byte-for-byte as
uploaded; [`STATUS.md`](STATUS.md) lists all its superseded statements.
