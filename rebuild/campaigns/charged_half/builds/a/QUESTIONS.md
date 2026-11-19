# SPEC ambiguities and how build charged_half-a resolved them

1. Γ definition: SPEC gives 1 − |A_out|²/|A_in|² and calls it "transmitted over incident flux". With the horizon
   normalisation |R_+| = 1 these are identical by flux conservation (Γ = 1/|A_in|²); both are computed, the 1/|A_in|²
   form is exported (no cancellation when Γ is tiny).
2. Overall phases of the horizon solution and of φ(r*) are irrelevant to |A|; Φ = ωr* − g ln(r−2) is used (exact ∫ω̃ dr*).
3. "Per helicity state": taken literally as Σ_j (2j+1) ∫ dω/2π Γ n_F with no further factor (no sum over the two
   helicities, no particle+antiparticle doubling). This gives N0 = 2.428e-4, P0 = 4.092e-5, inside the gate's window.
4. Thermal integral over ω > 0 only, as written, including 0 < ω < g_μ/2 where n_F > 1/2 (no superradiance for fermions,
   Γ ≥ 0 always).
5. transmission(j, ...) accepts j = 1/2, 3/2, ...; k = j + 1/2 is rounded to the nearest integer.
6. charge_distribution: π built until π(n)/π(max) < 1e-17, then entries < 1e-14 dropped and the rest renormalised so Σπ = 1
   exactly; ⟨P⟩, ⟨N⟩ use this truncated distribution (effect < 1e-13).
7. ⟨P⟩ = Σ π(n)[P_e−(n) + P_e+(n)]/2 taken literally (average over the two species, per helicity state).
8. "mid" rule: n − q/2 is half-integer; the coupling α q (n − q/2) is used as a real number (no rounding).
9. up(n)/down(n) are the number rates N of section 3 with g_gb and g_μ from the rule (the same rule for the chain and the
   averages).
