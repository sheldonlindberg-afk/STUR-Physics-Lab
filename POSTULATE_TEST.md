# Testing the STUR postulate against standard decoherence theory

**Verdict: standard decoherence theory contradicts the postulate.** Ordinary
thermal environments do not satisfy either half of it, and at high temperature
the temperature scaling is opposite to what it predicts. So STUR's version is falsified for
ordinary environments. It survives only if spacetime is a special kind of
environment, one whose noise breaks the standard fluctuation–dissipation
relation (see §5). Because the result is a contradiction and not a measurable
difference, this report gives no MAGIS-100 or AION signal.

Follow-up: every assumption below is varied, and every exact match listed, in
[ASSUMPTIONS.md](ASSUMPTIONS.md).

Reproduce: `python3 src/stur_postulate_test.py` (about 35 s). The full output is in
`results/postulate_test/output.txt`, and `tests/test_postulate_test.py` pins the
key numbers. Every number below comes from that output.

## 1. What was tested

Write Γ ≡ −ln(V/V₀) = ½Φ_R². The postulate and its corollary say:

| | Claim | Label |
|---|---|---|
| P1 | S/k_B = Γ (visibility loss is entropy) | STUR POSTULATE |
| P2 | E_exchanged = k_B T Γ, so Γ = E/(k_B T) at fixed E | FOLLOWS from P1 by Landauer, as stated in the record |

Models, all KNOWN PHYSICS:

- **A. Pure-dephasing spin-boson.** H = Σω_k b†b + σ_z Σ g_k(b+b†), with an Ohmic
  spectral density J(ω) = ηω e^(−ω/ω_c). The qubit and bath start uncorrelated:
  ρ_S ⊗ ρ_β.
- **A′. An independent check.** The qubit plus two discrete modes, simulated
  directly in a truncated Fock space, without using any of the formulas from A.
- **B. Caldeira–Leggett free particle** in the superposition |+Δx/2⟩ + |−Δx/2⟩,
  treated two ways: B1 in the recoilless limit (exact, and the same mathematics
  as model A), and B2 with the high-T Markovian master equation, including the
  particle's own motion.

## 2. The exact result for model A (KNOWN; FOLLOWS from the model)

- Visibility loss: Γ(t) = Σ_k 4g_k²(1−cos ω_k t)/ω_k² · coth(ħω_k/2k_BT).
- Energy given to the bath: ΔE_B(t) = Σ_k 2ħg_k²(1−cos ω_k t)/ω_k. **This does
  not depend on T.** The interaction energy changes by −ΔE_B. The qubit's own
  energy does not change at all.
- Combining the two, mode by mode:

  **Γ_k = ΔE_k / (k_B T · x_k tanh x_k),  with x_k = ħω_k/(2k_BT).**

  The postulate requires x tanh x = 1 for every mode that matters. That holds for
  exactly one frequency, **ħω\* = 2.3994 k_BT**. Above it the postulate
  over-predicts the visibility loss per unit energy, and below it the postulate
  under-predicts it: 100× at ħω = 0.2 k_BT, and 10⁴× at ħω = 0.02 k_BT. See
  `results/postulate_test/single_mode_ratio.png`.

The simulation matches the analytic formulas to better than 10⁻⁶ at T ≤ 1. At
T = 3 it matches to 5×10⁻⁴; the gap comes from cutting off the Fock space. It
also satisfies the exact identity Σ = I(S:B) + D(ρ_B‖ρ_β) to within 9×10⁻¹³, a
CONSISTENCY CHECK that passed.

## 3. Results

### (a) Visibility, energy and temperature: P2 fails

Fixed energy given to the bath, ΔE_B = 0.0900 ħω_c (Ohmic, η = 0.05, ω_c t = 3):

| k_BT/ħω_c | Γ, standard | Γ, thermal part only | Γ, postulate = ΔE/k_BT |
|---|---|---|---|
| 0.01 | 0.231 | 0.0003 | 9.00 |
| 0.1 | 0.256 | 0.025 | 0.90 |
| 1 | 1.067 | 0.837 | 0.090 |
| 10 | 10.39 | 10.16 | 0.0090 |

Log-log slope d ln Γ / d ln T:

| Regime | Standard | Thermal part only | Postulate |
|---|---|---|---|
| High T | **+1.000** | | **−1.000** |
| Low T | +0.009 | +1.97 | −1.000 |

Plot: `results/postulate_test/gamma_vs_T_fixed_energy.png`.

- **High T:** at fixed energy, a colder interferometer loses *less* visibility,
  the opposite of the postulate.
- **Low T:** the visibility loss stops depending on T. If the reversible vacuum
  "dressing" part is removed (the "thermal part only" column), the loss goes to
  zero as T → 0, while the postulate's prediction grows without limit.
- The two curves cross once, near k_BT ≈ 0.25 ħω_c. That is a coincidence point,
  not an identity.

The ratio also fails at fixed T. With an Ohmic bath, ΔE_B levels off at 2ηħω_c,
but Γ keeps growing as 4πηk_BT t/ħ. At T = 1, k_BTΓ/ΔE_B goes from 3.8 to 50,
then 606, then 6252 at t = 1, 10, 100, 1000. **Dephasing continues after the
energy exchange has stopped.**

### (b) Entropy: P1 fails for every standard entropy

The qubit's von Neumann entropy is h((1+e^(−Γ))/2), which can never exceed
ln 2, while Γ has no upper limit. The table below shows three of the six runs of
model A′ (all in nats):

| T | t | Γ | S_qubit | ΔS_bath | I(S:B) | Σ = ΔS + βQ | −ln F (bath records) |
|---|---|---|---|---|---|---|---|
| 0.3 | 2.0 | 1.067 | 0.633 | 0.570 | 1.203 | 2.293 | 0.873 |
| 1.0 | 2.0 | 2.201 | 0.687 | 0.335 | 1.022 | 1.185 | 0.450 |
| 3.0 | 2.0 | 6.171 | 0.693 | 0.143 | 0.836 | 0.859 | 0.164 |

None of these entropies tracks Γ: Γ rises while the qubit entropy levels off at
ln 2, and the other entropies even fall. Plot: `results/postulate_test/entropy_vs_gamma.png`.

The one quantity that matches Γ exactly is at **T → 0**: there,
Γ = −ln F of the bath's two records (0.961874 = 0.961874). This is the
**KNOWN** which-path identity V = |⟨χ₀|χ₁⟩| (Englert 1996; Zurek). It measures
how distinguishable the environment's records are. It is not a thermodynamic
entropy, and at finite T it falls below Γ.

### (c) Caldeira–Leggett

- **B1, recoilless limit.** This is model A with σ_z replaced by 2x/Δx and
  J_eff = (mγΔx²/2πħ) ω e^(−ω/ω_c). Every conclusion above carries over.
- **B2, high-T Markovian master equation.** The decoherence is Γ = 2mγk_BTΔx²t/ħ².
  The bath's noise feeds energy into the particle at the gross rate 2γk_BT.
  Therefore:
  - Γ / E_in = mΔx²/ħ², which **does not depend on T** (the postulate says 1/k_BT);
  - k_BTΓ / E_in = (Δx/λ_th)², with λ_th = ħ/√(mk_BT);
  - for Rb-87 with Δx = 1 µm, this ratio runs from 0.18 at 1 nK to 1.8×10³ at
    10 µK and 5.4×10¹⁰ at 300 K. The postulate is right only where Δx ≈ λ_th,
    which is exactly where the high-T master equation stops being valid.
  - A particle already at thermal equilibrium has **zero net energy exchange**
    (E_net = 0) yet still decoheres at the full rate. P2 would require Γ = 0.

## 4. Choices that could have changed the verdict

| Choice | Effect |
|---|---|
| Energy taken as the qubit's own (zero), ΔE_B, or Caldeira–Leggett net vs gross flow | The verdict holds under all of them. Zero and net-zero exchange alongside nonzero Γ are the sharpest failures. |
| Uncorrelated start vs vacuum-dressing subtracted | Changes only the T → 0 end: there the loss levels off (uncorrelated start) or goes to zero (dressing removed). Neither grows like 1/T. |
| Ohmic spectrum, cutoff ω_c | Changes the numbers, not the formula Γ_k = ΔE_k/(k_BT·x tanh x), which holds for any linearly coupled bosonic bath in a thermal state. |
| Caldeira–Leggett Markov validity | B2 is an illustration only. B1 is exact and gives the same verdict. |

## 5. What STUR would need, stated as a requirement (FOLLOWS; no new structure added)

For P2 to hold exactly, spacetime's noise would have to replace coth(x) with x
in the formula for Γ_k. That means noise that vanishes at low frequency instead
of growing there. No environment in thermal equilibrium at temperature T behaves
this way: it breaks the KMS condition, which is the fluctuation–dissipation
theorem. So **spacetime would have to be a non-thermal environment, or one that
couples only at ħω ≈ 2.40 k_BT**. Either is a new assumption. Testing it needs
open problem #2, which is to say what A_μ couples to.

## 6. Referee note on the "FOLLOWS (Landauer)" label

Landauer's bound limits the heat from *erasing* information: Q ≥ −T ΔS_system
when the system's entropy goes down. Dephasing *raises* the system's entropy, so
the bound says nothing here: in the runs above, βQ can be smaller or larger than
ΔS_S. E_R = ½k_BTΦ² therefore does not follow from Landauer as an equality. It
is an extra assumption, and it is the part that fails most clearly.

## 7. What survives

- V = exp(−½⟨Φ²⟩) for Gaussian noise: KNOWN, and confirmed again here.
- −ln V = −ln F(environment records) for pure records: KNOWN (Englert), so not new.
- The Smarr check in `stur_verify.py` uses the black-hole temperature T_H and is
  not affected by this test. But it can no longer count as support for P2 in
  laboratory-scale systems.
