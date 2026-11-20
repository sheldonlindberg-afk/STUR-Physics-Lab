# SPEC ambiguities and how they were resolved (build a)

1. **Sign of Sigma_T.** SPEC gives the dressed propagator -i g/(k^2 - M^2 + Sigma_T); a Dyson resummation of the
   amputated 1PI sum i Pi^{mu nu} gives -i g/(k^2 - M^2 - Pi_T), so Sigma_T = -Pi_T. (The stated vertex function
   Gamma = -i g[(k^2 - M^2) + Sigma] is read only as fixing the same sign; "positive Sigma lowers M^2 - Sigma" agrees.)
2. **Sign of Sigma^AZ.** Fixed by SPEC's rotation A = s W3 + c B, Z = c W3 - s B and D = d - i g W T - i g' Y B: photon
   vertex +i e Q, Z vertex +i e (gL PL + gR PR), gL = (I3 - s^2 Q)/(sc), gR = -sQ/c. Sigma^AZ is proportional to
   +Q (gL + gR). A convention with A -> -A (common elsewhere) would flip this sign; I followed SPEC.
3. **gamma5.** Anticommuting gamma5; the only gamma5 trace in a two-point bubble is the epsilon tensor, which
   integrates to eps k k = 0. Tr 1 = 4 in d dimensions. The d-dependence enters through (d-1) B00 = ..., and its O(eps)
   part times the pole is kept (finite term (m1^2 + m2^2 - k^2/3)/6 in B00).
4. **Real part above threshold.** Implemented as ln|Delta(x)| in the Feynman-parameter logs (Re ln(Delta - i0)).
5. **m = 0 and k^2 = 0 together** (neutrino at k^2 = 0): scaleless integrals, every one multiplied by m^2 or k^2 = 0;
   returned as 0, which equals the k^2 -> 0 limit (k^2 ln(-k^2) -> 0).
6. **CKM / colour in the W loop:** taken entirely from the weight w (no extra N_C), as SPEC section 3 says.
7. **mu argument** is the MS-bar scale itself (enters as ln(.../mu^2)).
