# SPEC ambiguities and how they were resolved (build b)

1. **"MS-bar mass at the scale mu"**: taken as the standard MS-bar scheme, mu_bar^2 = 4 pi e^{-gamma_E} mu^2
   (only 1/eps poles subtracted with the (4pi)^eps e^{-gamma eps} convention per loop). `mu_over_m` = mu_bar/mbar(mu_bar),
   so the log is ln(mu^2/mbar^2) = 2 ln(mu_over_m).
2. **Delta rho_0(m) in the MS-bar scheme**: the one-loop formula N_C G_F m^2/(8 sqrt2 pi^2) with m = mbar(mu)
   inserted; c_MSbar is the coefficient that goes with that choice (no re-expansion of G_F or alpha_s running at this order).
3. **gamma5**: anticommuting gamma5 in d dimensions. Justified: at q = 0 the V-A interference needs an epsilon tensor and
   vanishes; the surviving VV and AA traces contain an even number of gamma5, and AA(m1, m2) = VV(m1, -m2).
4. **Sign convention for Sigma**: SPEC's propagator -i g/(q^2 - M^2 + Sigma) used literally (Sigma = minus the 1PI
   insertion coefficient); this gives Delta rho_0 > 0.
5. **Tr 1 in d dimensions**: Tr 1 = 4 (common to every order, cancels in c and fixed by the 4-dimensional value of Delta rho_0).
6. **"Keep N_C and C_F general"**: N_C enters only Delta rho_0 (closed quark loop); at O(alpha_s) every diagram has the
   single colour factor C_F N_C (no gluon self-coupling or extra quark loop enters), so c is C_F times a pure number.
   The b quark is massless, so it has no mass counterterm; the massless b-b correlator vanishes at q = 0 in dim reg.
7. **Gauge**: Feynman gauge for the main computation, as the SPEC prescribes; the (1 - xi) part of the gluon propagator
   was computed separately and its contribution to R + S1 + S2 vanishes exactly for every correlator, and the one-loop
   mass counterterm (pole or MS-bar) is gauge independent, so the result is xi-independent.
8. **"Pole mass"**: one-loop on-shell condition dm = -Sigma(pslash = m), kept exact in eps (its O(eps) terms multiply the
   divergent one-loop integrals with a doubled propagator).
