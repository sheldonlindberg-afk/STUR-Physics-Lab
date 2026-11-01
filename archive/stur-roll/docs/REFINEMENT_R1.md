# Refinement round 1: audit of the STUR-ROLL chain against the literature

> **Round 2 corrected two statements in this document**
> (see [`REFINEMENT_R2.md`](REFINEMENT_R2.md)):
>
> 1. **R1.4 bound.** The few-TeV bound applies to the KK mass M&#8321; = 2&pi;/L, not to 1/L, so the correct bound is 1/L &gtrsim; 0.8&ndash;1.0 TeV.
> 2. **Anisotropy limit.** The ACT DR6 limit is A_CB &lt; 0.15, not 0.52.
>
> R2.2 also showed that &beta; = k_eff&middot;&alpha;/2 holds **exactly**, with no e^(&minus;2&pi;MR) correction.

Date: 2026-10-31. Code: [`src/checks/refinement_r1.py`](../src/checks/refinement_r1.py), which runs in under 2 s.
References are labelled [n] and listed in [`REFERENCES.md`](REFERENCES.md).

## Summary

| # | Item | Verdict | Action |
|---|------|---------|--------|
| R1.1 | KK-tower coupling c_g = &frac12; | **Confirmed, and now exact**: closed form derived. The 0.49998 in `stur_final.py` is truncation of the KK sum, not physics | add the closed form to the derivation; level argument sharpened |
| R1.2 | Normalisation L = (k&alpha;/4&pi;)&theta;FF&#771; &rarr; &beta; = (k&alpha;/2&pi;)&Delta;&theta; | **Confirmed** against the standard rotation formula [1, 2] | none |
| R1.3 | Novelty of &beta; = &alpha;/2 | **Not new as an observable.** Lee, Murai, Takahashi & Yin [3] predict &beta; &asymp; 0.21 c_&gamma;&deg; from a hilltop axion whose walls form after recombination | **reframe** STUR-ROLL as a UV origin for c_&gamma; = 1 and for the hilltop start |
| R1.4 | Section E collider window | **Error.** A bulk fermion with electric charge needs a bulk photon, and its KK modes are bounded at roughly 4&ndash;7 TeV [8, 9] | replace "1/L &gtrsim; 10 GeV" with "1/L &gtrsim; few TeV" (pending a dedicated LHC recast) |
| R1.5 | Weak gravity conjecture for U(1)_B | **Passes** throughout the f window (f &lesssim; M_Pl/250) | none; record it |
| R1.6 | Measurement inputs | **Confirmed**: 0.215 &plusmn; 0.074&deg; [5], 0.277 &plusmn; 0.057&deg; [6], 0.342 (+0.094/&minus;0.091)&deg; [7] | none (the script symmetrises the WMAP+Planck error to 0.0925) |

## R1.1 The KK-tower coupling, in closed form

`stur_final.py` (section A) sums the phases of the KK masses
m_n = M + i(n + &theta;/2&pi;)/r numerically. The sum has a closed form:

&sum;_n a / (a&sup2; + (n+x)&sup2;) = &pi; sinh(2&pi;a) / (cosh(2&pi;a) &minus; cos 2&pi;x)

Hence

**c_g(&theta;) = &frac12; &middot; sinh(2&pi;Mr) / (cosh(2&pi;Mr) &minus; cos &theta;) = &frac12; [1 + 2e^(&minus;2&pi;Mr) cos &theta; + &hellip;]**

| M r | exact | numerical sum, \|n\| &le; 2&times;10&#8309; (as in `stur_final`) | sum, \|n\| &le; 2&times;10&#8311; |
|---|---|---|---|
| 0.2 | 0.594088 | 0.594088 | 0.594088 |
| 2 | 0.5000019 | 0.4999987 | 0.5000019 |
| 10 | 0.5000000 | 0.4999841 | 0.4999998 |

Two consequences:

1. **The 0.49998 at Mr = 10 is a truncation artefact.** The tail of the sum is about Mr/(&pi;N). The exact deviation from &frac12; is e^(&minus;63).
2. **The level argument becomes exact.** The integral of c_g over one period of &theta; equals &pi; *for every* Mr, not just asymptotically. So a full turn of &theta; shifts the fermion-induced &theta;-term by &pi;, not 2&pi;. Invariance under &theta; &rarr; &theta; + 2&pi; therefore requires a bare level k&#8320; &isin; &Zopf; + &frac12;, and k_eff = k&#8320; + &frac12; sgn M. This is the 5D analogue of the parity anomaly [10]. On orbifolds, the bulk Chern&ndash;Simons term that cancels boundary anomalies is discussed in [11], and its one-loop generation by massive fermions in [12].

**Sharper statement of the discrete input.** With one fermion and k&#8320; = +&frac12;, k_eff is 1 for M &gt; 0 and **0 for M &lt; 0**. "k = 1 is the minimal level" is therefore equivalent to choosing the sign of the bulk mass relative to the bare term. k_eff = 0, which gives no birefringence at all, is equally consistent. The documentation should say this explicitly.

**Caveat on the charge assignment.** The coefficient of &theta;FF&#771; (photon) is proportional to q_B Q_EM&sup2;. The chain assumes q_B = 1 and Q_EM = 1. Larger charges would give k &gt; 1, which is disfavoured by the data (+2.5&sigma; for k = 2).

## R1.2 Normalisation

With F&#771;^{&mu;&nu;} = &frac12;&epsilon;^{&mu;&nu;&rho;&sigma;}F_{&rho;&sigma;}, the term L = (k&alpha;/4&pi;)&theta;FF&#771; matches L = &minus;&frac14;g a FF&#771; with g a = &minus;(k&alpha;/&pi;)&theta;. The rotation of linear polarisation along a path is &Delta;&psi; = (g/2)&Delta;a [1, 2]. Therefore &beta; = (k&alpha;/2&pi;)&Delta;&theta;, and &Delta;&theta; = &pi; gives &beta; = k&alpha;/2 = 0.20905&deg; for k = 1. The photon coupling used in section C, |g| = k&alpha;/(&pi;f), follows from the same matching. Its bound f &gt; 2.9&times;10&#8313; GeV uses g &lt; 8&times;10&#8315;&sup1;&sup3; GeV&#8315;&sup1;, the weaker end of the 6&ndash;8&times;10&#8315;&sup1;&sup3; GeV&#8315;&sup1; range of [13]. Using 6&times;10&#8315;&sup1;&sup3; would give f &gt; 3.9&times;10&#8313; GeV.

Because &beta; = (k&alpha;/2&pi;)[&theta;(observer) &minus; &theta;(emission)], independent of the path [1, 2], the claim of section C holds: with &theta; &asymp; 0 everywhere at recombination, the recombination-era rotation is isotropic even if walls separate +&pi; and &minus;&pi; regions today. Only the observer's own domain matters.

## R1.3 Prior art: the same number from hilltop domain walls

Lee, Murai, Takahashi & Yin [3] (abstract): domain walls of a string axion explain isotropic cosmic birefringence "mainly when the axion starts near a hilltop". The walls form after recombination, which avoids the domain-wall problem, and the predicted angle is **&beta; &asymp; 0.21 c_&gamma; degrees**, with c_&gamma; &asymp; 1 matching the data. Earlier work in the same programme: [14] introduced birefringence from ALP domain walls, [15] computed the wall-network power spectrum and anisotropic birefringence, and [16] showed that walls seeded by inflationary fluctuations are long-lived. A related idea, quantised O(&alpha;) rotations from axion strings set by an anomaly coefficient, is in [17].

**Consequence for STUR-ROLL.** The observable content of STUR-ROLL is the same as [3] with c_&gamma; = 1:

- amplitude &alpha;/2;
- isotropic rotation of recombination photons;
- patchy rotation of reionization photons;
- no rotation at emission.

So the "discriminators against a generic ALP" in [`PREDICTIONS.md`](PREDICTIONS.md) do **not** distinguish STUR-ROLL from [3]. What STUR-ROLL can claim is narrower and still non-trivial: it supplies a **UV origin for the two assumptions [3] makes.**

1. **c_&gamma; = 1.** This comes from the half-integer bare level plus one bulk fermion (R1.1). It is still a discrete choice, but a minimal one.
2. **The hilltop initial condition.** This comes from the Wilson-line potential, which has a minimum at &theta; = 0 while the scalar dominates (high T and de Sitter) and a maximum there once the fermions dominate below T_c. Finite-temperature Wilson-line potentials are standard (Hosotani mechanism [18, 19]), and the Wilson-line axion with a loop-induced potential is the extranatural set-up [20]. What is specific to STUR-ROLL is the **sign flip** between regimes.

Any distinct observable prediction would have to come from this UV sector: the &psi; particle, the B KK modes, or a relation between m and f. This is an open item.

## R1.4 The photon must live in the bulk

&psi; is a 5D field carrying electric charge (section E calls it "a charge-1 vectorlike lepton"). Gauge invariance therefore requires U(1)_Y to propagate in the bulk. Its KK excitations, with masses of order n/L up to O(1) convention factors, couple to the brane-localised SM fermions. Bounds on gauge KK modes with brane fermions are roughly 4&ndash;5 TeV from electroweak precision data, and 6.8 TeV from a combined fit that includes Tevatron and HERA data [8, 9]. Current LHC dilepton searches are likely stronger; **a dedicated recast is an open item.**

Impact on section E, using a placeholder 1/L &gt; 5 TeV:

- the 1/L = 1 TeV rows become excluded;
- every remaining allowed row has M_f &gtrsim; 10&#8312; GeV;
- the statement "allowed from 1/L ~ 10 GeV (M_f &gt; 1 TeV)" is wrong and has to change. The conclusion that the sector is "testable only through birefringence" becomes stronger.

The finite-temperature trigger T_c &asymp; 9.8/L stays far above any cosmological scale of interest, so steps 4&ndash;5 are unaffected.

## R1.5 Weak gravity conjecture for U(1)_B

For a Wilson-line axion, f = 1/(g&#8324;L) [20], up to O(2&pi;) factors that depend on the circle length. The electric WGC asks for a state with m &le; &radic;2 g&#8324;qM_Pl; the natural candidate is &psi; with q = 1. Since g&#8324;M_Pl / M_f = M_Pl / (f &middot; M_fL), and M_fL &asymp; 150&ndash;250, the condition holds for f &lesssim; 10&sup1;&#8310; GeV, which covers the entire section C window. The magnetic WGC cutoff g&#8324;M_Pl exceeds 1/L in every allowed row. No new constraint arises, but the check is now recorded.

## Open items carried to round 2

1. **Orbifold version of the level argument.** R1.1 works on the covering circle. Check, with anomaly inflow on S&sup1;/Z&#8322; [11], that a Z&#8322;-odd B with Z&#8322;-even B&#8325; leaves k&#8320; &isin; &Zopf; + &frac12; and k_eff = 1 intact, including the fixed-point contributions.
2. **LHC recast** of KK photons with brane fermions, to replace the 5 TeV placeholder.
3. **Distinct prediction versus [3].** Look for a relation that the UV sector fixes, for example between m, f and L, or a correlated signal from &psi; or the B KK modes.
4. **Seed statistics.** Compute the &theta; fluctuation spectrum through nucleation, the probability of a wall inside our Hubble volume, and the reionization-era anisotropic birefringence. Compare with [15, 16] and with the ACT DR6 bound A_CB &lt; 0.15 [21] *(corrected from 0.52 in round 2)*.
5. **Time-dependent birefringence today.** &theta; oscillates around &pi; with period 2&pi;/m, about 130 Myr for m = 10&#8315;&sup3;&#8304; eV, so the ACT DR6 time-dependent search [22] does not apply. Confirm this quantitatively.
6. **Missing companion scripts** (see [`STATUS.md`](STATUS.md)), in particular `class_check.py`.
