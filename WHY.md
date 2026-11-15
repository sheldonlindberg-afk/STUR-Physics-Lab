# Why these inputs? The 19 parameters and a unification attempt

*What can be said about why the Standard Model's measured inputs have their values, with
every claim computed and every source named. Companion to [FORCE_CHAIN.md](FORCE_CHAIN.md),
which takes the inputs as given. Independent work, not peer reviewed.*

Run it: `python3 src/why_parameters.py` (about 3 s; output in
[results/why/output.txt](results/why/output.txt)). The same calculation, restated with the
standard library, is step 9 of the merged simulation
[`src/chain_first_principles.py`](src/chain_first_principles.py)
([expected output](results/chain_first_principles.txt)). Pinned by
[`tests/test_why_parameters.py`](tests/test_why_parameters.py).

---

## The result in one paragraph

None of the 19 parameters is derived, here or anywhere. Sorted by what is known: **11** have
no explanation, **3** are related to other inputs by established physics, **2** follow an
empirical regularity nobody has derived, and **3** have an explanation that rests on a
conjecture. The strongest pattern is a condition at the Planck mass: if the Higgs
self-coupling and its rate of change both vanish there, the top and Higgs masses follow from
the gauge couplings to within 2% and 6%. That pattern does not carry over to this
repository's 3-3-1 model in its simplest form, and the 3-3-1 structure alone does not explain
quark mixing: with generic couplings it predicts the opposite of what is measured. What it
does give is one vev ratio that makes the top and bottom couplings equal, and a link from
that ratio to the Z mass.

## How to read the labels

| Label | Meaning |
|---|---|
| MEASURED | No explanation is used. The value is an input. |
| RELATION | Established physics relates it to other inputs. It does not fix the value. |
| EMPIRICAL | A numerical regularity with no accepted derivation. |
| CONJECTURE | Follows only under an unproven assumption, named in the row. |
| MODEL | A calculation of this repository's own that extends a published idea. |

Established physics stops at MEASURED and RELATION.

## The ledger (W0)

The list of 19 is Kronfeld's [1]: three gauge couplings, nine charged-fermion masses, four
quark-mixing parameters, the Higgs vev and self-coupling, and θ̄. With neutrino masses and
mixing it is 28; those are not treated here.

| Parameter | In this repository | Label | What is known |
|---|---|---|---|
| α_s | input 0.1180 | RELATION | Fixes the proton's mass scale exponentially (W4). Value unexplained. |
| α_QED | input 1/127.930 at M_Z | MEASURED | A gravity fixed point for g_X is a MODEL ([NOTE_331.md](NOTE_331.md), G1). |
| α_W (sin²θ_W) | input 0.23129 | RELATION | 3-3-1 bounds it below 3/4 (W5). Value unexplained. |
| v | from the measured G_F | MEASURED | None. |
| λ (Higgs mass) | input 125.20 GeV | CONJECTURE | λ(M_Pl) = 0 gives 128.7 GeV (W1). Zero quartics fail in 3-3-1 (W2). |
| m_t | input 172.57 GeV | CONJECTURE | With β_λ(M_Pl) = 0 as well: 170–174 GeV (W1). Asymptotic safety: 171 GeV (W3). |
| m_b | input | RELATION | 3-3-1: y_b = y_t at one vev ratio, which is a new parameter (W9). |
| m_c, m_s, m_d, m_u | inputs (m_s first used here) | MEASURED | None. m_u = 0 is excluded (W6). |
| m_τ | input | EMPIRICAL | Koide's relation fixes one of the three lepton masses (W8). |
| m_μ, m_e | inputs | MEASURED | None. |
| θ₁₂ (Cabibbo) | only \|V_ud\| is used | EMPIRICAL | arctan √(m_d/m_s) is 2.8% low, 5σ (W7). |
| θ₂₃, θ₁₃, δ | not used | MEASURED | None. 3-3-1's structure alone gives the wrong pattern (W9). |
| θ̄ | not used | CONJECTURE | Peccei–Quinn symmetry in 3-3-1 (W6). Needs an axion. |

## W1. The Higgs and top masses from conditions at the Planck mass (CONJECTURE)

**The idea.** If gravity is asymptotically safe and nothing new lies between the Fermi and
Planck scales, the Higgs self-coupling λ vanishes at the Planck mass, and the Higgs mass
follows from the top mass and α_s. Shaposhnikov and Wetterich predicted 126 GeV this way in
2009, before the discovery [2].

**One condition, at the PDG 2024 inputs** (M_t = 172.57 ± 0.29 GeV, α_s = 0.1180):

| Formula | M_H |
|---|---|
| Shaposhnikov–Wetterich, eq. (12) [2] | 128.7 GeV (theory ± 2.2) |
| λ(M_Pl) = 0 in Buttazzo et al., eq. (61e) [3] | 128.7 GeV |
| Stability bound, Buttazzo et al., eq. (64) [3] | 128.3 GeV |
| Measured | 125.20 GeV |

The prediction is 3.5 GeV (2.8%) high, 1.5σ with their theory error and the top-mass error.
Read the other way, the measured Higgs mass needs M_t < 171.53 ± 0.42 GeV (eq. (66) of [3]);
the measured top mass is 2.0σ above that. A one-loop cross-check with this repository's own
running gives 134.7 GeV, 6.1 GeV above the NNLO formulas, which is the size of the one-loop
error.

**Two conditions, two masses.** Adding β_λ(M_Pl) = 0, the vanishing of λ's rate of change,
gives two equations. They fix both masses from the gauge couplings alone:

| Method | M_t | M_H |
|---|---|---|
| NNLO couplings at M_Pl (eq. (61) of [3]), one-loop β_λ (eq. (8) of [2]) | 174.3 GeV (+1.0%) | 132.6 GeV (+5.9%) |
| One loop throughout | 169.6 GeV (−1.7%) | 128.6 GeV (+2.7%) |
| Measured | 172.57 GeV | 125.20 GeV |

The spread between the two rows (4.6 and 4.0 GeV) is the size of the method's error. The
combination of the two conditions is this repository's. Buttazzo et al. note that β_λ
vanishes near 10¹⁷–10¹⁸ GeV and call it "more like an accidental cancellation" (section 4.1
of [3]).

## W2. The same condition with the 3-3-1 scalars (MODEL, one loop)

All nine quartic couplings of the 3-3-1 scalar sector ([`src/m331_scalar.py`](src/m331_scalar.py))
were set to zero at M_Pl and run down to M_V = 4 TeV, for two values of the vev ratio and
three of the exotic Yukawa, in both variants. In 9 of the 12 cases the self-quartic of the
triplet that has no large Yukawa ends negative (−0.15 to −0.21), so the potential is
unbounded below. In the other 3 a quartic diverges above M_V. The reason is general: without
a large Yukawa, gauge terms alone drive a quartic, and they drive it negative toward low
energy.

So the Higgs-mass prediction does not carry over. In 3-3-1 the nine quartics would need
non-zero fixed-point values, which are new parameters unless a gravity fixed-point
calculation supplies them. That calculation has not been done here. Running upward,
`src/m331_scalar.py` S4 finds that up to 7% of sampled quartic sets stay perturbative and
stable to M_Pl, so viable sets exist; they are not predicted.

## W3. The top mass

- **Infrared quasi-fixed point (RELATION: an upper bound).** A large top Yukawa at a high
  scale is focused to one low-energy value (Pendleton and Ross; Hill; as described in [4]).
  At one loop from M_Pl, y_t(M_Pl) between 1 and 3.54 runs to y_t(M_t) between 1.19 and
  1.27, a spread of 6%. That is 28–36% above the measured 0.933, so it bounds the top mass
  and does not give it.
- **Asymptotic safety (CONJECTURE).** Eichhorn and Held find a top pole mass of about
  171 GeV [5], against 172.57 ± 0.29 GeV measured. They quote no error.

## W4. The strong coupling and the proton's mass scale (RELATION)

At one loop with six flavours, Λ = M_Pl exp(−2π / (7 α₃(M_Pl))). With α₃(M_Pl) = 1/52.9
(eq. (61c) of [3]) this is 0.028 GeV, 2.3×10⁻²¹ M_Pl. The sensitivity is
d ln Λ / d ln α₃ = 47.5: a 10% larger g₃ at M_Pl moves Λ to about 107 GeV, which agrees
with Fig. 5 of [3] ("makes Λ_QCD larger than the weak scale"). Lattice QCD then gets the
hadron masses from the quark masses and the coupling [6]. So the small proton-to-Planck
ratio is explained. The coupling's value is not.

## W5. The weak mixing angle in 3-3-1 (RELATION: a bound)

Rung 1's matching, 1/g_Y² = β²/g² + 1/g_X² with g_X² > 0, gives
sin²θ_W < 1/(1 + β²) = 3/4 for β = ±1/√3. The measured value is 0.231. This bounds the
angle and does not give it.

## W6. The strong CP angle (CONJECTURE: needs an axion)

In the 3-3-1 model with right-handed neutrinos, which has this repository's β = −1/√3
content, a Peccei–Quinn symmetry follows from a Z₁₁ ⊗ Z₂ symmetry (Dias, de S. Pires and
Rodrigues da Silva [7]). Checked here in exact fractions:

- all 27 components of the seven Yukawa terms of their eq. (6) and of the potential term
  ηρχφ are invariant under the charges of their eqs. (14)–(18);
- the colour anomaly, the sum over quarks of (q_R − q_L), is 2X_d. It is not zero only
  because of the exotic quarks: the ordinary u and d contributions cancel. It stays 2X_d
  for 5 and 7 colours.

A non-zero anomaly means θ̄ can be rotated away. The price is an axion, which has not been
observed. The other way out, a massless up quark, is excluded: m_u differs from zero "by
more than 30 times the quoted error" [8].

## W7. The Cabibbo angle from the quark masses (EMPIRICAL)

Gatto–Sartori–Tonin [9]: θ₁₂ = arctan √(m_d/m_s). With the PDG 2024 masses at 2 GeV,
m_d = 4.70 ± 0.04 and m_s = 93.5 ± 0.5 MeV (as listed in eq. (2.2) of [10]), this gives
0.2206 ± 0.0011, against θ₁₂ = arcsin(0.22501) = 0.2270 ± 0.0007 [11]: 2.8% low, 5.0σ.
Antusch, Hinze and Saad get 0.2205 ± 0.0012 from running Yukawas and conclude that "the
approximate GST relation is not accurate enough" (eq. (4.11) of [10]).

## W8. The charged-lepton masses (EMPIRICAL)

Koide's relation, (m_e + m_μ + m_τ)/(√m_e + √m_μ + √m_τ)² = 2/3, holds to 3 parts in a
million with the measured pole masses. Solved for the tau mass it gives 1776.97 MeV, the
value Koide predicted in 1982, against 1776.93 ± 0.09 MeV measured (+0.4σ). It fixes one
mass of three. It does not hold for running masses (2/3 × 1.00189 at M_Z), although a
field-theory derivation would give running masses: "a serious theoretical problem" in
Koide's own words [12]; see also [13].

## W9. Quark flavour in 3-3-1

**F1. The structure (RELATION).** Anomaly cancellation makes one quark family an SU(3)_L
triplet and two antitriplets. The Yukawa terms (eq. (6) of [7]) then feed the two
electroweak vevs into the mass matrices by rows:

| | antitriplet family 1 | antitriplet family 2 | triplet family |
|---|---|---|---|
| up-type quark gets its mass from | v_ρ | v_ρ | v_η |
| down-type quark gets its mass from | v_η | v_η | v_ρ |

**F2. One vev ratio (RELATION).** With tan b = v_η/v_ρ, the top and bottom Yukawas are
equal at tan b = y_t/y_b = 59.3 (Yukawas at M_Z from eq. (2.4) of [10]). The six quark
Yukawas there:

| y_t | y_b | y_c | y_u | y_s | y_d |
|---|---|---|---|---|---|
| 0.967 | 0.967 | 0.211 | 4.2×10⁻⁴ | 3.1×10⁻⁴ | 1.5×10⁻⁵ |

The triplet family's two Yukawas are equal, and the antitriplet families' four are 0.21 and
below. The largest-to-smallest ratio falls from 1.4×10⁵ in the Standard Model to 6.3×10⁴.
The vev ratio is a new parameter: it is traded for m_b/m_t, not derived.

**F3. Is the rest structure? No (MODEL).** Draw random complex Yukawas of order one with
the row structure of F1. At tan b = 59.3 the triplet family holds the heaviest up-type
quark and the lightest down-type quark, so the top would decay to the lightest down quark:
the median \|V_tb\| is 0.01, and \|V_tb\| > 0.9 never occurs in 4000 draws. At tan b = 1 it
occurs in 3.6%. The measured \|V_tb\| is 0.999 [11]. So the measured mixing needs a
hierarchy inside the Yukawas themselves; the vev structure works against it.

**F4. The same ratio moves the Z mass (RELATION).** tan b is the angle a of the ρ parameter
([`src/m331_rho_bound.py`](src/m331_rho_bound.py), R1):
ρ − 1 = (v/w)²(sin²a − sin²a₀)². At the LHC bound on w (10.3 TeV) this is 1.3×10⁻⁵ at
tan b = 1 and 6.9×10⁻⁵ at tan b = 59.3, against the global fit's
ρ₀ − 1 = (3.9 ± 1.9)×10⁻⁴ [14]: −2.0σ and −1.7σ. The merged simulation checks the closed
form against the blind build's gauge-boson mass matrix.

**F5. More mixing, not less (from the literature).** Because the third family's Z′
couplings differ, the left-handed rotations of the up and down quarks are separately
physical, and the Z′ changes flavour at tree level. 3-3-1 adds four mixing parameters to
the CKM matrix's four (Buras et al. [15], abstract and eqs. (53)–(56)).

## What this means for a unification

- **What worked.** A boundary condition at the Planck mass plus running reaches two of the
  19 to a few percent (W1). The 3-3-1 anomaly structure supplies a Peccei–Quinn symmetry
  (W6) and separates the O(1) Yukawas from the small ones by representation (F2).
- **What failed.** The Planck condition in its simplest form is incompatible with the
  3-3-1 scalar sector (W2). The 3-3-1 vev structure with generic Yukawas gives the wrong
  mixing (F3). The Cabibbo relation misses at 5σ (W7).
- **What is still open.** A gravity fixed-point calculation for the nine 3-3-1 quartics;
  a symmetry that distinguishes the triplet family from the antitriplets and so explains
  F2's split; bounds on the four new mixing parameters from meson mixing.
- **What has no handle at all.** v, the four lightest quark masses, m_e and m_μ, α_QED,
  and three of the four CKM parameters.
- **A geometric attempt.** [TRIANGLE.md](TRIANGLE.md) tries to get the 3-3-1 group, three
  generations and the parameters from one fixed geometry. The group, the charges and the
  number of generations follow; the couplings, masses and mixing do not. The tally above is
  unchanged.

## Limits

- Everything in W1–W3 is one loop for this repository's own running. The published NNLO
  formulas are quoted, not derived.
- W2 scans six points per variant, not the full parameter space.
- F3 assumes Gaussian random Yukawas. Another distribution would change the numbers, not
  the alignment.
- The ledger's labels are this repository's judgement of the cited literature.

## Sources

Each was read from the source itself (arXiv PDF or the PDG 2024 review); journal references
were checked on the arXiv record.

1. A. Kronfeld, "Twenty-five Years of Lattice Gauge Theory", [arXiv:1007.1444](https://arxiv.org/abs/1007.1444), section 5.
2. M. Shaposhnikov and C. Wetterich, Phys. Lett. B 683, 196 (2010), [arXiv:0912.0208](https://arxiv.org/abs/0912.0208), abstract and eqs. (8), (12).
3. Buttazzo et al., JHEP 12 (2013) 089, [arXiv:1307.3536](https://arxiv.org/abs/1307.3536), eqs. (55)–(66), section 4.1, Fig. 5.
4. W. Bardeen, M. Carena, S. Pokorski and C. Wagner, [arXiv:hep-ph/9309293](https://arxiv.org/abs/hep-ph/9309293), introduction.
5. A. Eichhorn and A. Held, Phys. Lett. B 777, 217 (2018), [arXiv:1707.01107](https://arxiv.org/abs/1707.01107), abstract.
6. Dürr et al., Science 322, 1224 (2008), [arXiv:0906.3599](https://arxiv.org/abs/0906.3599).
7. A. Dias, C. de S. Pires and P. Rodrigues da Silva, Phys. Rev. D 68, 115009 (2003), [arXiv:hep-ph/0309058](https://arxiv.org/abs/hep-ph/0309058), eqs. (1)–(6), (12)–(19).
8. PDG 2024, review "Quark masses", after eq. (60.9), [pdg.lbl.gov](https://pdg.lbl.gov/2024/reviews/rpp2024-rev-quark-masses.pdf).
9. R. Gatto, G. Sartori and M. Tonin, Phys. Lett. B 28, 128 (1968), as cited in [10].
10. S. Antusch, K. Hinze and S. Saad, [arXiv:2510.01312](https://arxiv.org/abs/2510.01312), eqs. (2.2), (2.4), (4.11).
11. PDG 2024, review "CKM quark-mixing matrix", eqs. (12.27), (12.28), [pdg.lbl.gov](https://pdg.lbl.gov/2024/reviews/rpp2024-rev-ckm-matrix.pdf).
12. Y. Koide, [arXiv:1809.00425](https://arxiv.org/abs/1809.00425), eqs. (0.2), (1.1).
13. Xing and Zhang, Phys. Lett. B 635, 107 (2006), [arXiv:hep-ph/0602134](https://arxiv.org/abs/hep-ph/0602134).
14. J. Erler, [arXiv:1908.07346](https://arxiv.org/abs/1908.07346), as used in `src/m331_rho_bound.py`.
15. A. Buras, F. De Fazio, J. Girrbach and M. Carlucci, JHEP 02 (2013) 023, [arXiv:1211.1237](https://arxiv.org/abs/1211.1237), abstract and eqs. (53)–(56).

Also used: PDG 2024 review "Electroweak model and constraints on new physics", section 10.2,
for the statement of which parameters the Standard Model has.
