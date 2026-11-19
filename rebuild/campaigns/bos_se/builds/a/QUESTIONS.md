# SPEC ambiguities and how they were resolved (build bos_se-a)

1. Sign of Sigma^AZ. SPEC says "the transverse mixing term -i g Sigma^AZ_T in the inverse propagator matrix" while the diagonal
   entries are defined through the propagator -i g/(k^2 - M^2 + Sigma). Read as the vertex-function matrix
   Gamma = -i g (k^2 - M^2 + Sigma) (propagator = -Gamma^{-1}), whose off-diagonal entry is then -i g Sigma^AZ. Hence the same
   relation Sigma = -Pi (iPi = sum of 1PI diagrams) for all four. The sign also depends on A = s W3 + c B, Z = c W3 - s B and
   D = d - i g W tau/2 - i g' B/2 exactly as in SPEC 1 (used as given).
2. Sigma^W means the W+W- transverse self-energy; computed as Sigma^{W1 W1} after checking W1W1 = W2W2 and W1W2 = 0.
3. "O(eps) part of every d-dependent coefficient kept against the pole": implemented as c(d) X -> c(4) X^fin - 2 c'(4) Res X, with
   Delta = 1/eps - gamma_E + ln 4 pi dropped; the coefficients include the 1/(d-1) of the transverse projector and g^mu_mu = d.
4. Photon mass lambda -> 0: set to zero exactly in A0 and B0 (the limits exist; no B0' or 1/lambda terms occur in Feynman gauge).
5. Above thresholds: real part of B0 only (coefficients are real).
6. Tadpoles: the one-point-Higgs-attached diagrams are excluded; the Goldstone masses come only from the gauge fixing (xi M^2),
   the potential gives them zero mass at its tree minimum. Seagull (quartic-vertex) loops are included, as SPEC says.
