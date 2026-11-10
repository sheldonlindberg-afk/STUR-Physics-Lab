# The Born rule, derived from the quantum level

Reproduce: `python3 src/stur_born.py` (about 10 s). The full output is in
`results/born/output.txt`, and `tests/test_born.py` pins it. This replaces the one
postulate that [DERIVATION.md](DERIVATION.md) D0 used to take as given:
probability = |amplitude|².

## What is assumed instead

| | Assumption | In words |
|---|---|---|
| A1 | Unitary quantum mechanics, with tensor products | The branch equation of DERIVATION.md |
| A2 | Locality (no-signaling) | Acting only on a separate system E can't change what can be learned about S |
| A3 | Non-contextuality | An outcome's probability depends only on the state and that outcome, not on what else is measured with it |

## Four routes to |c|², each computed

**B1. Envariance (Zurek 2003, 2005; uses A1 + A2).**
- **Equal amplitudes.** In (|0⟩|e₀⟩ + |1⟩|e₁⟩)/√2, a swap on S changes the state by 1.414.
  A counter-swap on E *alone* restores it exactly (residual 0). By A2, then, p₀ = p₁ = ½.
  A phase on S is undone on E too (residual 6×10⁻¹⁷), so phases don't affect probabilities.
- **Unequal amplitudes.** A unitary acting only on E splits each branch into equal pieces:

| \|c₀\|² | Fine-grained amplitudes | Envariance residual | p₀ by counting equal branches |
|---|---|---|---|
| 1/3 | all 0.577350 = 1/√3 | 0 | 0.333333 |
| 2/5 | all 0.447214 = 1/√5 | 2×10⁻¹⁶ | 0.400000 |
| 3/7 | all 0.377964 = 1/√7 | 8×10⁻¹⁷ | 0.428571 |
| 5/8 | all 0.353553 = 1/√8 | 0 | 0.625000 |

  So p = |c|² for every rational value, and by continuity for all values. Any other rule
  contradicts itself on the *same* state. For |c₀|² = 2/5, p ∝ |c| gives 0.4495 before
  fine-graining and 0.4000 after; p ∝ |c|⁴ gives 0.3077 and 0.4000.

**B2. Additivity (Gleason-type; uses A3).** If p = F(|⟨e|ψ⟩|²) in every basis, the
probabilities of a complete set must sum to 1. Over 20,000 random states and bases in
dimension 3:

| F(x) | Largest \|Σ − 1\| |
|---|---|
| x^0.5 | 0.73 |
| x^0.9 | 0.12 |
| **x** | **1.8×10⁻¹⁵** |
| x^1.1 | 0.10 |
| x² | 0.67 |

Only F(x) = x works. Gleason (1957, LIT) proves the general case: in dimension ≥ 3,
every non-contextual probability assignment is p = Tr(ρP), mixed states included.

**B3. No-signaling (uses A2).** Two entangled qubits. Bob's statistics must not depend
on what Alice chooses to measure far away. I checked the largest shift in Bob's P(+)
when only Alice's setting changes:

| Rule | Shift |
|---|---|
| \|c\|^1.0 (power 2q = 1) | 0.10 |
| \|c\|^1.8 | 0.026 |
| **\|c\|²** | **3×10⁻¹⁶** |
| \|c\|^2.2 | 0.028 |
| \|c\|⁴ | 0.23 |

Any rule other than |c|² is a faster-than-light telegraph. This is the "instant
reaction, but no message" of [MEASUREMENT.md](MEASUREMENT.md) T4: **the Born rule is
exactly what makes "one object stretched across space" safe.**

**B4. Frequencies (Hartle 1968; Farhi–Goldstone–Gutmann 1989).** Repeat a measurement
with |c₀|² = 0.4 N times. The total weight of branches whose observed frequency is off
by more than 0.05:

| N | Weight of wrong-frequency branches |
|---|---|
| 10 | 0.75 |
| 100 | 0.31 |
| 1,000 | 1.2×10⁻³ |
| 10,000 | 2.0×10⁻²⁴ |

Almost all of the state sits where the observed frequency is |c|². This route treats
small weight as negligible, so on its own it isn't free of the rule it derives. B1–B3
don't need that step.

## Status

- **The Born rule is no longer an input.** It follows from unitarity plus locality
  (B1, B3), or from unitarity plus non-contextuality (B2). B4 shows the frequencies
  that experiments see.
- **What remains assumed:** A1–A3, and that outcomes are records (the ⟨Eⱼ|Eᵢ⟩ of
  DERIVATION.md).
- **LIT caveat:** envariance assumes that probabilities exist and depend only on the
  state, and that step is debated (Schlosshauer & Fine 2005). B2 and B3 don't rely on it.
