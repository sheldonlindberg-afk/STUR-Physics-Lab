# Stage 10m: scalarons and scalar perturbations in teleparallel gravity

**Script:** `scripts/genesis_v10m_teleparallel_inflation.py` (about 15 min; every conclusion below is a gated computation)
**Replaces:** the argued claim "f(T) gravity does not propagate a scalaron, so R²/Starobinsky inflation is not in STUR" (claim 9 of the argued-vs-computed inventory). Also attempts the open n_s/r question for STUR's own scalar (`docs/GENESIS_V10F_THEORY_GAPS.md` (c)).

**Conventions.**
- Metric signature (−,+,+,+), with Weitzenböck torsion and zero spin connection.
- With the standard combination T = ¼T^{ρμν}T_{ρμν} + ½T^{ρμν}T_{νμρ} − T^ρ_{μρ}T^{νμ}_ν, flat FRW gives T = +6H².
- GR is L = −e·T/2 (M_Pl = 1).
- R = −T + B, with B = −(2/e)∂_μ(e T^{ρμ}_ρ). The sign is fixed on FRW, where B = 6(ä/a + 2H²).

## (a) f(T) has no scalaron (confirmed by calculation)

**Minisuperspace** (flat FRW with lapse N). Differential order in a(t), and linearized modes:

| Theory | a-equation | Constraint | Minkowski modes | de Sitter modes (synchronous gauge) |
|---|---|---|---|---|
| GR | 2 | 1 | s = 0 | s = 0 |
| f(R) = R + R²/6M² | 4 | 3 | s = 0, **±iM** | s = 0, **−3H₀/2 ± √(9H₀²/4 − M²)** |
| f(T) = T + βT² | 2 | 1 | s = 0 | s = 0 (the constraint carries only the factor 1 + 36βH₀² = f_T + 2T f_TT) |

The gate passes: f(R) shows the Starobinsky scalaron at exactly mass M. f(T) has the same order and the same modes as GR. Its T² term only rescales the effective Newton constant.

**Full scalar sector.** The second-order action is computed in comoving gauge (δχ = 0) for a Fourier mode, with every scalar tetrad field: lapse α, shift ∂B, curvature ζ, and the local-Lorentz boost (rapidity ∂λ). It is evaluated for L = −e[G + S(T−T₀) + Q(T−T₀)²/2]/2 + e[χ̇²/2N² − V]. This covers:
- GR (S = 1, Q = 0);
- f(T) (S = f_T, Q = f_TT);
- STUR's F(χ)T (S = 2αχ, Q = 0).

**Gates.** GR reproduces Mukhanov's action exactly: K = a³χ̇²/4H², the gradient term is −aχ̇²k²/4H², and the superhorizon mass is 0. The boost decouples completely in GR, which is local Lorentz invariance.

**f(T) result.**
- Lapse, shift and boost are all auxiliary, with a unique algebraic solution. Exactly **one** scalar propagates, the same as GR plus a scalar field. **There is no scalaron.**
- An exact k-scan on a numerical f(T) background (β = 0.05, V = χ²/2, both Friedmann equations satisfied to 10⁻⁶) gives:
  - K = a³(f_T + 2T f_TT)(−Ḣ)/2H² at every k (no ghost while f_T + 2T f_TT > 0);
  - c_s² → 1 for k ≫ aH.
- **New, beyond the argued claim:** the integrated-out Lorentz mode gives ζ a superhorizon mass. At k = 10⁻³ aH, M/(K H²) ≈ 1.4 for β = 0.05. It falls continuously to 0 as f_TT → 0, roughly as 3βT₀. So ζ is **not conserved** on superhorizon scales in f(T) beyond GR.

**Consequence.** Starobinsky R² inflation cannot come from a TEGR-based action. The pre-registered r = 0.0035 is therefore a GENESIS assumption, not a STUR output.

## (b) STUR's own scalar: not healthy, so n_s and r are not computable

For S = F(χ) = 2α|R| and Q = 0, after integration by parts the boost enters **only** as the linear term −k a² Ḟ ζ λ, with no λ² term. It is a Lagrange multiplier. The Euler–Lagrange system is solved explicitly in the script:

1. EL(λ): k a² Ḟ ζ = 0, so **ζ = 0** whenever Ḟ = 2αχ̇ ≠ 0.
2. EL(shift): k S (a ζ̇ − ȧ α) = 0, so α = 0.
3. EL(lapse) then gives the shift = 0, and EL(ζ) gives λ = 0.

**There are zero propagating scalar modes at linear order.** The kinetic structure is degenerate, and the true dynamics appear only at higher order (strong coupling).

**The healthy condition, derived.** Adding a boundary-term coupling +e·D(χ)·B/2 contributes **+k a² Ḋ ζ λ** (computed, with no λ² term). The total boost coupling becomes −k a² (Ḟ − Ḋ) ζ λ. A scalar propagates only if **Ḋ = Ḟ**. Then −eFT/2 + eFB/2 = eFR/2 up to a total derivative, which is the scalar-curvature theory F(χ)R. This is the structure Raatikainen & Räsänen (JCAP 12 (2019) 021) describe, now derived here. STUR has D = 0 and fails the condition.

So **n_s and r are not computable for STUR's inflation as written.** The background is parameter-free (ε_H = 15/(10N + 15), from `genesis_v10f_theory_gaps.py`), but it has no linear curvature perturbation.

**Counterfactual (computed).** If STUR's coupling were α|R|R instead of α|R|𝕋, the Einstein frame gives (dσ/dx)² = 1/2x + 3/2x² and U ∝ x², with x = χ/α and v ≪ χ. That is parameter-free:

| N* | n_s | r |
|---|---|---|
| 50 | 0.9366 | 0.340 |
| 55 | 0.9426 | 0.308 |
| 60 | 0.9475 | 0.281 |

This is quartic-like chaotic inflation, excluded by BICEP/Keck (r < 0.036).

## Bugs found and fixed during the work (not affecting the results above)

- The first Fourier ansatz gave the shift and rapidity a cos(kx) phase. Gradients of cos(kx) scalars must go as sin(kx), and the wrong phase made the shift drop out of GR. That was caught by the GR gate and fixed.
- The numerical f(T) background first used a wrong root of T/2 + 3βT²/2 = ρ (12βρ for 24βρ). It was caught by the Friedmann-residual gate and fixed.
- A first extraction of the f(T) gradient term by `coeff(k, 2)` was invalid, because the reduced action is rational in k. It was replaced by the exact k-scan.
