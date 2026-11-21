# Can the induced G be made independent of the regulator?

*Written and committed before any number below is computed. The derivation of every formula
used is part of the registration, so a sign or factor error is visible before the result is.
Independent work, not peer reviewed. Status: **registered (commit c1beae2), then computed: every item as registered** (result below; the registration above unchanged).*

## The question

[INDUCED_GRAVITY.md](INDUCED_GRAVITY.md) gets G from stage 1's fields with a proper-time cutoff κ
at the U(1)_X pole. The audit of campaign `induced_g` showed that the sign and size belong to
the regulator: a cutoff on mode energies flips the sign, and Pauli–Villars can give either sign.
A cutoff stands in for unknown physics above it. The induced G becomes **finite and
regulator-free** if the fields obey Pauli's sum rules (M. Visser, arXiv:gr-qc/0204062, Sec. 5;
D. Frolov and D. Fursaev's induced-gravity models, as summarized there). This registration asks
three questions:

1. Can stage 1's own spectrum, with masses from its own vacuum values, give the measured G that way?
2. If heavier states are needed, what does the minimal set of them give, and is its sign fixed?
3. Is the sign fixed for any larger set?

## Derivation (re-derived here, conventions of INDUCED_GRAVITY.md)

Euclidean action −(1/16πG)∫√g R with G > 0 attractive, and R > 0 on spheres. Each field has a
Laplace-type operator D + m². The heat kernel is Tr e^{−t(D+m²)} = (4πt)^{−2} e^{−tm²} ∫√g (b₀ + b₁ t + …),
with b₁ = k₁ R and k₁ the per-field coefficient of the accepted campaign. W = −ln Z contains

  W ⊃ −(1/32π²) ∫√g R · Σ_fields (±) k₁ I(m),   I(m) = ∫_ε^∞ dt t^{−2} e^{−tm²},

where + is for bosons, − for fermions, and ε = 1/κ² is any small proper-time cutoff. With
u = tm², I = m² Γ(−1, εm²). Since Γ(−1, x) = 1/x + ln x + γ − 1 + O(x),

  I(m) = κ² + m² ln(m²/κ²) + (γ − 1) m² + O(1/κ²).

So Σ(±)k₁ I = κ² str[k₁] − ln κ² str[k₁m²] + (γ − 1) str[k₁m²] + str[k₁ m² ln m²], with
str[X] = Σ_fields (±) X. If and only if

  (S1) str[k₁] = 0  and  (S2) str[k₁ m²] = 0,

every κ-dependent and scheme-dependent piece cancels. What remains is finite and independent of
the regulator:

  **1/G = (1/2π) str[k₁ m² ln m²]**  (independent of the mass unit, because of S2).

The prefactor is the same as INDUCED_GRAVITY.md's 1/G = (1/2π) str[k₁] κ², which this
reproduces for one level as κ² → m².

**(A) A bound when every mass is at most m_max.** By S2, 1/G = (1/2π) Σ(±)k₁ m² ln(m²/m_max²), and
|x ln x| ≤ 1/e for 0 < x ≤ 1. Hence

  **M_Pl² = 1/G ≤ (Σ|k₁|) m_max² / (2π e)**,

for any masses up to m_max, any signs and any ξ.

**(B) Two heavy levels.** Let the light fields (stage 1, masses m ≪ M) have str[k₁] = S, and add heavy states
whose weighted k₁ totals K₁ at mass M₁ and K₂ at mass M₂ > M₁. Up to O(m²/M²) the light masses drop out
of S2 and of the finite formula, since m² ln m² ≪ M² ln M². Then:
- S1 gives K₁ + K₂ = −S;
- S2 gives K₁M₁² + K₂M₂² = 0;
- so K₁ = −S M₂²/(M₂² − M₁²) and K₂ = S M₁²/(M₂² − M₁²);
- 1/G = (1/2π)(K₁M₁² ln M₁² + K₂M₂² ln M₂²).

This gives

  **1/G = (S/2π) M₁² · r ln r/(r − 1),  r = M₂²/M₁²,**

and r ln r/(r − 1) lies in [1, r] for r ≥ 1. So **the sign is the sign of S**, the light fields' own
str[k₁], whatever the heavy states are. The size is exactly the proper-time formula
(S/2π)κ², with κ² = M₁² r ln r/(r − 1), somewhere between M₁² and M₂².

**(C) Three or more levels.** S1 and S2 leave a free direction, so the sign is not expected to be
fixed. To be shown by an explicit example.

## What will be computed (stage 1's inputs, from the merged simulation's functions)

1. **Stage 1 alone.** For β = +1/√3: the counting supertrace str[1] = N_S + 2N_V − 2N_W, the
   condition for a finite cosmological term (its κ⁴ term). Also the ξ at which stage 1 satisfies S1
   by itself.
2. **Bound (A) for stage 1's spectrum.**
   - Σ|k₁| is computed at ξ = 0, at ξ = 1/6, and at the ξ that satisfies S1.
   - m_max = √(4π) w is the largest mass a perturbative coupling gives at the 3-3-1 scale w.
   - Find the w at which bound (A) first reaches the measured M_Pl.
3. **(B) checked numerically**, with random S, M₁ and M₂ and with stage 1's light masses kept (not
   dropped): 1/G from the full finite formula against (B), and its sign against the sign of S.
4. **(C)**: a three-level example satisfying S1 and S2 whose 1/G has the opposite sign to S.
5. **The asymptotic I(m)** checked by direct numerical integration.

## Pass and fail, fixed now

| Item | Expected | Fail if |
|---|---|---|
| 1 | str[1] ≠ 0 for stage 1 | (no fail: it is a count) |
| 2 | bound (A) needs w ≳ 10¹⁷ GeV, far above any 3-3-1 scale the LHC allows (w ~ 10 TeV) | the bound reaches the measured M_Pl for w ≤ 10⁷ GeV: the finite version would then be possible within 3-3-1 |
| 3 | (B) agrees with the full formula to O(m²/M²), and the sign equals the sign of S in every case | any disagreement beyond O(m²/M²), or any sign different from S |
| 4 | a three-level counterexample exists | none found in a random search: then the sign would be more robust than claimed |
| 5 | I(m) matches to 10⁻⁶ relative | otherwise the derivation is wrong |

## What a pass would mean

- **(A)** The regulator-free version is impossible from 3-3-1's own masses. States near the
  Planck mass are necessary, so the regulator dependence is physical: it is a statement about what
  completes 3-3-1 at its pole.
- **(B)** For the minimal completion with two heavy levels near the pole, the proper-time result
  is exact. The sign is fixed by stage 1's own fields, attractive for β = +1/√3. κ becomes an
  effective mass between the two levels.
- **(C)** With more levels it is not fixed.

That is the strongest statement the physics allows. The audit's sign-flipping energy cutoff
then corresponds to no physical completion of this two-level kind.

---

## Result (computed after registration)

Run it: `python3 src/induced_gravity_finite.py` (standard library only, under a second; output in
[results/induced_gravity/finite.txt](results/induced_gravity/finite.txt)). Pinned by
[`tests/test_induced_gravity_finite.py`](tests/test_induced_gravity_finite.py).

| Item | Result | Registered expectation |
|---|---|---|
| 1 | str[1] = 18 + 34 − 138 = **−86**. S1 alone would need ξ = 0.17593 for all 18 scalars | as registered |
| 2 | Bound (A): the measured M_Pl is reached only for **w ≥ 2.8×10¹⁸ GeV** (Σ\|k₁\| = 23–26) | as registered (needed w ≫ 10⁷ GeV) |
| 3 | 600 random two-level completions, stage 1's light masses kept: formula (B) exact to **3×10⁻¹³**, and the sign of 1/G equals the sign of S **in every case** | as registered |
| 4 | Three levels: S = +3.17 with weights −13.8, +39.3, −28.7 at 1.4×10¹⁷, 3.1×10¹⁹, 3.6×10¹⁹ GeV gives **1/G < 0** | as registered |
| 5 | I(m) asymptotics against direct integration: **3.5×10⁻⁸** | as registered |

**What it means.**
- **The regulator dependence is physical, not a defect of the calculation.** No spectrum with masses from
  3-3-1's own vacuum values can induce the measured G finitely: that needs w ≳ 3×10¹⁸ GeV, or states near the
  Planck mass. So G is set by whatever completes 3-3-1 at its pole, and a cutoff is how one writes that.
- **For the minimal completion the sign and size are fixed.** That completion is two heavy levels satisfying the
  sum rules. The induced G is then exactly the proper-time result of INDUCED_GRAVITY.md, with
  κ² = M₁² r ln r/(r − 1) between the two levels. Its sign is the sign of stage 1's own str[k₁]: attractive for
  β = +1/√3, whatever the heavy states are. With the levels at the one-loop pole and up to 10× above it, the
  induced M_Pl is 3.1–6.7 × measured at ξ = 0.
- **Beyond the minimal completion the sign is open.** With three or more levels, or with a mode-energy cutoff,
  either sign is possible.

So the sharpest form of the result is: *if 3-3-1 is completed at its Landau pole by the minimal set of heavy
states that makes induced gravity finite, gravity comes out attractive, with G within an order of magnitude of
the measured value.* The cosmological term still needs str[1] = str[m²] = str[m⁴] = 0, which takes more states;
that is not addressed here.
