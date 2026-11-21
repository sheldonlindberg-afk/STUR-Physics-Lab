# QUESTIONS / ambiguities in SPEC.md and how they were resolved (build bos_dr-a)

1. Fermi-theory QED subtraction: SPEC does not say in which Fierz ordering the four-fermion operator is taken. In the
   charge-retention form [e gamma P_L mu][nu_mu gamma P_L nu_e] its QED correction is UV finite (conserved vector
   current); at zero momentum with a photon mass it is exactly zero (vertex + LSZ cancel by the Ward identity), so the
   subtraction removes nothing from the zero-momentum amplitude and the SM ln(lambda) terms cancel among themselves
   (photon box vs photon LSZ). Taken in the charge-exchange form and evaluated in NDR, the Fermi correction is UV
   divergent and scheme dependent; I used the finite (charge-retention) definition.
2. delta_vb: the raw vertex + box + LSZ sum is UV divergent (pole 4 alpha/(4 pi s^2) eps^-1) and hence mu dependent in
   MS-bar, while SPEC requires a mass-only (s^2-only) function. Resolution: delta_vb = delta_VB(MS-bar, mu = M_W),
   equivalently delta_VB(mu) + (2/(s c)) Sigma^AZ_T(0; mu)/M_Z^2, which is mu independent because the bosonic
   Feynman-gauge Sigma^AZ_T(0) = (alpha/4pi)(2 M_W^2/(s c)) ln(M_W^2/mu^2). The remaining terms of Delta r_bos then
   carry -2 (c/s) Sigma^AZ(0)/M_Z^2 (this sign is for SPEC's conventions, A = s W3 + c B).
3. Real parts: all needed self-energies are below threshold; vertices and boxes at zero momentum are real.
4. Tadpoles are excluded in bos_se; they cancel in Delta r (constants proportional to M_V^2 in each bracket).
5. Precision: bos_se exports return doubles and Sigma^W, Sigma^ZZ contain ~3.5e-4 M_H^2 that cancels in Delta r; for
   M_H up to 1e14 GeV I evaluate the M_H-dependent (Higgs-diagram) part myself at a local mpmath precision and use
   bos_se at M_H = M_W for the rest; agreement with the pure bos_se assembly is checked at moderate M_H.
