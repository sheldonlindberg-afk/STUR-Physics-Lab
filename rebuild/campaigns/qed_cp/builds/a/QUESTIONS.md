# Spec ambiguities (build qed_cp-a) and how they were resolved

1. **How far the "do not use the Green-tensor formula" ban reaches.** The perturbative route, done analytically,
   ends at the same one-dimensional imaginary-frequency integral U = −(1/πr⁶)∫du α(iu)² e^{−2ur} p(ur). I took the
   ban to mean that this formula may not be the *starting point*, not that it may not come out at the end. Here it
   is reached from the 12-diagram sum by a denominator identity proved by residues (DERIVATION §3) plus closed-form
   photon k-integrals (§4). An independent direct evaluation of the double photon integral (§6b), which skips that
   identity, agrees to 3e−4.
2. **What makes the photon integrals converge.** The double k-integral grows like k sin kr and only converges in the
   Abel sense (factor e^{−εk}, ε→0). SPEC says no cut-off should be needed. I used the Abel limit as the definition
   of the integral and introduced no cut-off. Nothing needed a principal value, because every 4th-order denominator
   is positive for a ground-state system.
3. **Renormalisation term and disconnected diagrams.** I took these to be r-independent and dropped them, as SPEC §1
   says to (argued in DERIVATION §1).
4. **The sign/phase convention of E⊥** (i in front, ε versus ε*) drops out: each exchanged photon contributes
   (+i)(−i) = +1.
5. **Audit follow-up (near zone).** For rω₀ ≤ 1e-7, `cp_energy` came out low by 4.2e-4 relative because `quad` under-sampled one long
   integration panel. That was a numerical bug, not a spec ambiguity. It is fixed with decade breakpoints, and the
   validity range is now stated in DERIVATION §6(d).
