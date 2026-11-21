# QUESTIONS / ambiguities (build higgs_rho-a)

1. Sign/normalisation of Pi: taken from SPEC 2, M_V^2(eff) = M_V^2 + Pi_VV(0), with the 1PI sum = i Pi g^{mu nu}
   (tree mass term gives i M^2 g^{mu nu}); equivalently full propagator -i/(k^2 - M^2 - Pi).
2. MS-bar convention: Delta = 1/eps - gamma + ln 4 pi dropped, mu^{2 eps} in the measure, A0 = m^2(1 - ln m^2/mu^2).
   The finite 1/d term of B00 is kept (it cancels in rho_higgs_rel anyway). self_energy_W/Z are convention-dependent
   in this respect; rho_higgs_rel is not.
3. g is reconstructed from the inputs as g^2 = 4 pi alpha / s^2 with s^2 = 1 - MW^2/MZ^2 (SPEC: e = g s, c = MW/MZ).
4. Which diagrams are "Higgs-containing": seagull H loop, H-V loop, H-Goldstone loop (no ghost diagram has an H at one
   loop except via the dropped tadpole). The xi argument is accepted but the sum is exactly xi-independent.
5. log_coefficient is defined as lim Delta rho / ln(mH^2/MW^2); it equals the coefficient of ln mH^2 in rho_higgs_rel
   (the limit of the ratio is the same since the constant is subleading).
6. campaign.b_custodial: the version first read divided by alpha*s^2 (proportional to s^4 at fixed g), inconsistent
   with its docstring (Delta rho ~ s^2 at fixed g) and with the derived result; it was replaced during the build by a
   version dividing by alpha, which is consistent and passes. I did not edit campaign.py.

7. Revision 2 (audit, documentation): explicit factors of i in all vertices and the sign of the V-phi-H product in each
   bubble; statement that no mixed W-Z / W-photon / photon loop contains an H and that H phi W Z, H phi W A cannot form a
   W+W- or ZZ seagull; how log_coefficient follows from the large-mH expansion, plus a numerical limit of rho_higgs_rel in
   __main__. One code change: working precision now grows with ln(mH/M) (previously a fixed 50 digits lost the result above
   ~1e25 MW). Exports are bit-identical in the tested range (tmp/cmp.py). SPEC 2's newly pinned conventions (k^mu k^nu ->
   g k^2/d with O(eps) kept, mu^{2 eps}, Delta dropped, 1PI = i Pi g) match what was already used.
