# SPEC ambiguities and how build `a` resolved them

1. **Split of the photon-Z mixing between SE and VBW.** Resolved: SE holds every two-point-function piece, in
   particular dZe = Sigma'_AA(0)/2 + (s/c) Sigma_AZ(0)/M_Z^2 (charge from the Thomson limit); VBW is the literal sum of
   1PI W l nu vertices, boxes and lepton wave functions. This VBW is UV divergent and mu dependent, as SPEC says. The
   other common bookkeeping (vertex remainder made finite by adding (2/sc) Sigma_AZ(0)/M_Z^2) would be UV finite, so it
   is not the SPEC's VBW. At xi = 1, VBW + (2/sc) Sigma_AZ(0)/M_Z^2 reproduces the known Feynman-gauge remainder.
2. **Fermi-theory subtraction.** Evaluated in the same regularization (photon mass lambda, dim reg for the UV), in
   charge-retention order: vertex + wave function cancel identically at zero momentum (Ward identity), so the term is
   zero. The lambda dependence of the full theory cancels by itself (checked). A fully dimensional IR treatment with
   4d boxes would shift the total by (3/2) alpha/4pi (evanescent mismatch), so the photon mass is used as SPEC says.
3. **IR regulator in the self-energies.** Massless photon (dim reg): the self-energies entering Delta r are IR
   finite for xi > 0, so this is the same as lambda -> 0.
4. **Landau gauge xi = 0.** The classes diverge like -/+ (3/4)(alpha/4pi) ln xi as xi -> 0+ (soft photon with the
   xi-pole of the W / the massless Goldstone), the total does not. At exactly xi = 0 they are computed in the Landau
   gauge with massless Goldstones, the IR divergence regulated dimensionally and subtracted in MS-bar with the UV
   poles (in the box: the photon x W-xi-pole terms with a massless photon). With this convention SE(0) + VBW(0)
   equals the xi > 0 total to all digits. A different IR convention at xi = 0 would move a constant between the
   classes; the total is unaffected.
5. **gamma5.** Anticommuting gamma5 on open lepton lines (only left-handed couplings enter); boxes reduced in 4d where
   they are not exactly gamma^a x gamma_a (those parts are UV finite).
6. **MS-bar** with the usual 1/eps - gamma + ln 4pi; O(eps) parts of d-dependent coefficients kept against the poles.
7. **Real parts.** For small xi the self-energies at p^2 = M_V^2 are above unphysical thresholds (e.g. photon +
   Goldstone, sqrt(xi) M_W); the real part of B0 is used as SPEC says.
8. **Tadpoles.** Excluded; the on-shell Sigma_V(M_V^2) then depend on xi, only through a common Sigma_V/M_V^2 shift
   that cancels in Delta r (DERIVATION section 6).
9. **The xi = 0 and xi = 1 degeneracies** (masses xi M^2 = 0 or = M^2) are handled exactly (equal masses merged in
   partial fractions; on-shell coefficients cancelled symbolically before setting p^2 = M^2).
