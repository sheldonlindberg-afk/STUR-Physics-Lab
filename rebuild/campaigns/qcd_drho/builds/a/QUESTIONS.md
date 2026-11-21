# SPEC ambiguities and how build a resolved them

1. Sign of Sigma and of Delta rho. SPEC fixes the propagator -i g/(q^2 - M^2 + Sigma). With
   L_int = g W J this gives Sigma = -g^2 Pi, Pi = i \int e^{iqx} <T J J>, hence
   Delta rho = (4/v^2)[Pi_11(0) - Pi_33(0)], which comes out positive (N_C G_F m^2/(8 sqrt2 pi^2)).
2. Z coupling in the gaugeless limit. "Hypercharge switched off" read as s_W -> 0: the Z is W^3 with
   coupling g/c to J^3; the s^2 J_em piece is dropped (it does not contribute at leading order in G_F m^2
   anyway, the electromagnetic current being conserved).
3. MS-bar scheme. mu_over_m = mu/mbar(mu); the log in c is ln(mu^2/mbar(mu)^2); Delta rho_0 is evaluated
   with mbar(mu) at the same mu. alpha_s is the MS-bar coupling; its scheme/scale is an O(alpha_s^2)
   effect and does not enter c.
4. delta_rho_qcd with scheme "pole" ignores mu_over_m (pole coefficient is mu independent; verified).
5. gamma5: anticommuting gamma5 (NDR). Justified: every trace has an even number of gamma5 on one open
   fermion line pair, no anomalous triangle subgraph exists at O(alpha_s); implemented through the exact
   field redefinition psi_b,t -> gamma5 psi, i.e. Pi_A(m1,m2) = Pi_V(m1,-m2).
6. "keep N_C general": Delta rho_0 is proportional to N_C; c is independent of N_C (colour factor C_F of one
   gluon exchange inside a single quark loop). The t-b annihilation (two-loop-colour-singlet) topologies
   that would bring other colour factors start at O(alpha_s^2).
7. Bottom mass: exactly zero, so no bottom mass counterterm (massless b remains massless in dim. reg.).
