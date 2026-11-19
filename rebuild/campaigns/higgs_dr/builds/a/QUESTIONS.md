# SPEC ambiguities and how build higgs_dr-a resolved them

1. Sign of Pi: SPEC fixes "effective mass^2 = M_V^2 + Pi" with 1PI = i Pi g^{mu nu}; adopted literally (Pi = +delta M^2; opposite to Denner's Sigma).
2. "Higgs-containing diagrams": taken as exactly three per vector: HHVV seagull (H loop), H-V bubble (HVV trilinear), H-Goldstone bubble.
   Tadpoles dropped; shown to shift Pi_W/M_W^2 and Pi_Z/M_Z^2 by the same constant, which cancels exactly in Delta r.
3. Couplings in Pi use the on-shell g^2 = 4 pi alpha/s^2 and c^2 = M_W^2/M_Z^2 (bare vs on-shell differences are two-loop).
4. Delta r is linearised (1/(1 - Delta r) -> 1 + Delta r), consistent with one loop.
5. Reference Delta r_H(m_H = M_W) is evaluated at the same mu as Delta r_H(m_H); the result is mu-independent anyway, because
   d Pi/d ln mu^2 does not depend on m_H.
6. Above threshold (q^2 >= (m_H + M_V)^2) the exports raise ValueError rather than return a real part (SPEC only defines the real region).
7. B00 kept with the exact d-dimensional 1/d (the "+1" finite term), per SPEC section 2.
