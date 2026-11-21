# SPEC ambiguities and resolutions (build a)

1. **Ghost counting.** SPEC says Faddeev-Popov ghosts are "Grassmann scalars" without saying how many. Resolved as the
   standard complex ghost pair c, cbar with operator -nabla^2: Z_gh = det(-nabla^2)^{+1}, i.e. minus TWO real minimally
   coupled scalars, ghost part of k1 = -1/3 (independent of d, as the blind check requires).
2. **Ghost operator coupling.** Taken as -nabla^2 (xi = 0) on scalars, not -nabla^2 + xi R with the matter xi; the
   `xi` argument of k1 is ignored for non-scalar kinds.
3. **Vector operator.** Feynman-gauge operator taken as -nabla^2 + Ric on 1-forms (equal to the Hodge Laplacian), giving
   E = -Ric. Confirmed by the exact S^4 Hodge spectrum.
4. **Sign of the vector contribution to 1/G.** SPEC says the sign "follows from the conventions"; with these conventions
   a gauge vector with ghosts gives 1/G = -kappa^2/(3 pi) each. Kept as derived. The cutoff kappa is used identically for
   every field (a common proper-time cutoff), as SPEC states.
5. **mpl when 1/G = 0** (e.g. no fields, or conformal scalars only): returns None (SPEC says sqrt only when 1/G > 0).
6. **Weyl in odd d**: k1('weyl', odd d) raises ValueError (SPEC: even d only).
7. **Dirac kind in odd d**: spinor dimension 2^floor(d/2), per SPEC; no further choice needed.
8. **Zero modes** in the second route (scalar l = 0 at xi = 0, and the constant ghost mode) were dropped; they only
   contribute ln kappa terms, not kappa^2.
