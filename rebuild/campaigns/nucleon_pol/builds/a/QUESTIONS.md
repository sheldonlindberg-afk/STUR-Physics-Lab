# SPEC ambiguities and how build a resolved them

1. Normalization of alpha_E, beta_M: taken literally from SPEC section 2, H_eff = -2 pi (alpha_E E^2 + beta_M B^2) with
   Heaviside-Lorentz fields and e^2 = 4 pi alpha. For real photons this is the convention in which the forward amplitude
   is f = f(0) + (alpha_E + beta_M) w^2 and the Baldin sum rule reads (1/2pi^2) int sigma/w^2 (checked, route C).
2. "Born subtraction" with m_N -> infinity: the SPEC Lagrangian has only the charge coupling v.A of the nucleon (no
   anomalous magnetic moment, no 1/m_N terms). In the radiation gauge eps.v = 0 the nucleon pole terms vanish identically
   and the Thomson term -Z^2 e^2/m_N is O(1/m_N), dropped. With static Coulomb photons the nucleon-line diagrams are
   singular (1/(v.p) at zero energy) but carry no dependence on the photon's 3-momentum, so they cannot produce the
   E(q).E(q') = -(q.q') phi phi' structure; alpha_E is read from that structure only. In the uniform-field gauge with
   A_0(0) = 0, A(0) = 0 (route B) there is no nucleon-photon coupling at all.
3. The pi^0 -> gamma gamma (WZW anomaly) t-channel pole is not in the SPEC Lagrangian; it would anyway not contribute to
   the spin-independent alpha_E, beta_M (it is a spin-dependent pole term, removed with the Born terms by convention).
4. "Regularize in dimensional regularization": d = 4 space-time; after the static (energy) integration the loops are
   n = d-1 = 3 dimensional; the closed forms are given for general n and evaluated at n = 3, where no pole appears.
5. One pion mass m_pi for charged and neutral pions (isospin limit, SPEC "isospin symmetry holds"); only charged pions
   contribute, so the distinction would not matter at this order except through m_pi+.
6. Sign conventions for e and for the covariant derivative are not fixed by the SPEC; the result is O(e^2) and both the
   KR and pi pi gamma vertices come from the same covariant derivative, so they cannot matter.
