# SPEC ambiguities and how this build resolved them (higgs_dr_xi-a)

1. Sign/normalisation of Pi: taken literally from SPEC 2: i Pi g^{mu nu} is the sum of 1PI amplitudes and the effective mass^2 is
   M^2 + Pi (checked by resumming the propagator). This is minus the Denner-convention Sigma_T.
2. "g^{mu nu} coefficient" vs transverse self-energy: Pi g + Pi^L qq = Pi (g - qq/q^2) + (...) qq/q^2, so the g coefficient IS the
   transverse part; the physical pole is at M^2 = M_0^2 + Pi(M^2). q q pieces and V-Goldstone mixing never enter the transverse pole or G_F
   (massless lepton currents).
3. Seagull and tadpoles: the HH-VV seagull is kept in sigma_W/sigma_Z as SPEC says; it, like the dropped H tadpole, shifts Pi_W/M_W^2 and
   Pi_Z/M_Z^2 by the same constant and so drops out of Delta r exactly.
4. Reference subtraction: Delta r_H(M_W) is evaluated at the same xi, mu, M_W, M_Z, alpha.
5. "one xi for all three gauge sectors": the photon's xi is irrelevant (no Higgs-photon coupling); only xi_W = xi_Z = xi enters.
6. Above threshold (q^2 >= (m_H + M_V)^2) Pi has an imaginary part; the code returns the real part (ln|D|), which SPEC does not ask for and
   which is not used by Delta r (q^2 <= M_Z^2 < (m_H + M_V)^2 always).
7. log_coefficient takes xi but the result 11 alpha/(48 pi s^2) does not depend on it (derived, not imposed).
