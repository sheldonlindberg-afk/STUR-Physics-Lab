# QUESTIONS / ambiguities in SPEC.md and how build b resolved them

1. Fermi-theory subtraction (SPEC 1). The one-loop photonic correction of the four-fermion theory is taken in the
   charge-retention (Fierz) order, where it is UV finite and scheme free; at zero momenta and massless leptons it is
   vertex + legs of a conserved current and vanishes by the abelian Ward identity, with the same photon mass lambda as the SM
   diagrams. A charge-exchange-order evaluation with d-dimensional Dirac algebra would differ by an evanescent constant; not used.
   With this choice VBW(xi = 1) = alpha/(4 pi s^2)[6 + (7-4s^2)/(2s^2) ln c^2 - 4 ln(M_W^2/mu^2)].
2. Where the photon-Z mixing goes (SPEC 2). SE contains every two-point-function term, i.e. the charge renormalization
   2 dZ_e = Sigma'^AA(0) + 2 (s/c) Sigma^AZ(0)/M_Z^2 (the Thomson-limit form, verified by the direct q = 0 photon vertex in every
   xi). VBW is purely diagrammatic: 1PI W-lepton vertices + boxes + LSZ legs - Fermi, MS-bar. (Other bookkeepings, which rewrite
   part of the vertex divergence as a multiple of Sigma^AZ(0), would move a term ~ Sigma^AZ(0)/(s c M_Z^2) between the classes.)
3. Landau gauge xi = 0 (SPEC 1, 4). For xi > 0 both classes are infrared finite. At xi = 0 exactly Sigma^W_T(0) has an infrared
   log (Landau photon with massless Goldstone / massless k k pole), -(3 alpha/16 pi) ln lambda^2 in SE, cancelled by the W-gamma
   box in VBW; as xi -> 0+ it appears as ln xi, so the classes are discontinuous at xi = 0. The classes at xi = 0 are returned
   with the infrared pole subtracted like the UV one in MS-bar (ln(lambda^2/mu^2) -> 1, i.e. dimensional IR regularization with
   B0(0,0,0) = 0). A different IR rule changes SE(0) and VBW(0) by equal and opposite amounts, never the total.
4. "MS-bar at mu" is 1/epsbar = 1/eps - gamma_E + ln 4 pi dropped, with the O(eps) of d-dependent coefficients kept against the
   pole; anticommuting gamma_5. Sign convention: Sigma_T defined by 1PI = -i Sigma_T, delta M^2 = Re Sigma_T(M^2).
5. Real part above thresholds (small xi puts Goldstone/ghost thresholds below M_W, M_Z): ln|Delta| in the Feynman-parameter
   integrals.
6. delta_r_vbw has no M_H argument: VBW indeed has no Higgs line (no H l l coupling), so it is M_H independent.
