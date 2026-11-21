# Derivation: bosonic part of the on-shell Delta r (build bos_dr-b)

Conventions are SPEC section 1 (D = d - i g W^a T^a - i g' Y B, Z = cW3 - sB, A = sW3 + cB, e = g s, 't Hooft-Feynman gauge).
Units 1/(16 pi^2) throughout; u = g^2/(16 pi^2) = alpha/(4 pi s^2). Delta = 1/eps - gamma + ln 4pi, d = 4 - 2 eps, L_m = ln(m^2/mu^2).

## 1. Couplings (from the Lagrangian)
Fermion currents psibar gamma^mu (g W^a T^a + g' Y B) psi. With T^+ the isospin raising matrix, (g/sqrt2)(W^+ nubar_L gamma ell_L + h.c.): vertex i g/(2 sqrt2) gamma^mu (1-gamma5).
Neutral: A couples with eQ (Q=T3+Y), Z with (g/c)(T3 - s^2 Q). Hence for massless leptons
 gL = (g/c)(s^2 - 1/2) (left charged lepton), gR = (g/c) s^2, g_nu = g/(2c), photon -e (both chiralities), W: g/sqrt2 (left).
Triple vertex (Peskin form, same covariant derivative), all momenta incoming:
 g eps^{abc}[g^{mu nu}(k1-k2)^rho + g^{nu rho}(k2-k3)^mu + g^{rho mu}(k3-k1)^nu], with W3 = cZ + sA, so the Z (photon) leg gets an extra c (s).
Goldstone couplings to massless leptons vanish, so no scalar lines appear in vertices, boxes or lepton self-energies.

## 2. Bare-parameter assembly (which counterterms enter)
Everything is done with bare parameters; the on-shell relations convert them.
* G_F: amplitude at q^2 = 0 is proportional to g0^2 / (M_W0^2 - Sigma_W(0)) times (1 + delta_V), with M_W0^2 = M_W^2 + Re Sigma_W(M_W^2) (pole), delta_V = vertex + box + lepton wave-function (LSZ) correction. W-propagator dressing at k^2=0: [Sigma_W(0) - Sigma_W(M_W^2)]/M_W^2.
* g0^2 = e0^2/s0^2 with s0^2 = 1 - M_W0^2/M_Z0^2 = s^2 + c^2 X, X = Sigma_ZZ(M_Z^2)/M_Z^2 - Sigma_W(M_W^2)/M_W^2 (Z pole mass, W pole mass).
* Thomson charge: the photon-pole (1/k^2) residue of the exchange between conserved currents is read from the inverse propagator matrix [[k^2 + Sigma_AA, Sigma_AZ],[Sigma_AZ, k^2 - M_Z^2 + Sigma_ZZ]] at k^2 -> 0 (Sigma_AA(0)=0): P^-1_AA = 1/(k^2(1+Sigma'_AA(0))), P^-1_AZ = Sigma_AZ(0)/(M_Z^2 k^2); the charge part of the Z coupling is -e0 (s/c) Q. So
  e^2 = e0^2 [1 - Sigma'_AA(0) - 2 (s/c) Sigma_AZ(0)/M_Z^2]
  (the T3 part of the mixing is cancelled by the non-universal part of the photon-lepton vertex through the Ward identity; I did not recompute that vertex: see 'not derived').
* Combining: M_W^2 s^2 = (pi alpha/(sqrt2 G_F)) (1 + Delta r) with
  Delta r = Sigma'_AA(0) + 2 (s/c) Sigma_AZ(0)/M_Z^2 - (c^2/s^2)[Sigma_ZZ(M_Z^2)/M_Z^2 - Sigma_W(M_W^2)/M_W^2] + [Sigma_W(0) - Sigma_W(M_W^2)]/M_W^2 + delta_V.   (*)
  Counterterms used: M_W, M_Z pole (through M0^2 = M^2 + Re Sigma), charge (Thomson, with mixing), s^2 from the masses. Field renormalizations of W, Z, A and of the leptons do not appear except through the LSZ factors in delta_V (the W-field renormalization cancels between the two vertices and the propagator).
* Sigma's: bos_se (tadpoles excluded, fermion loops excluded). Sigma'_AA(0) by Neville extrapolation of Sigma_AA(h)/h (Sigma_AA(0)=0); k^2=0 values of Sigma_AZ, Sigma_W are the limit supplied by the module. For M_H >> M_W the Sigma's contain O(M_H^2) pieces that cancel in (*); they are evaluated as mpf (same lambdified expression as the module, working precision 60+ digits, local mp.workdps) so that nothing is rounded to float before the cancellation.
  Numerical check of (*): its mu dependence cancels only with delta_V's poles: slope per ln mu^2 of the Sigma part is exactly -4u (see 8), as required.

## 3. Diagrams of delta_V
Relative to the tree W-l-nu vertex, delta_V = 2 [Lambda + 1/2 (dZ_l + dZ_nu)] + boxes (two identical vertices, four external legs each with 1/2 dZ). All with zero external momenta (the W is at q^2=0; leptons massless; photon mass lambda regulates the IR). Loop integrals depend on x=k^2 only; the d-dim Dirac algebra is kept (O(eps) x pole), tensor reduction k^mu k^nu -> x g^{mu nu}/d.
Vertex (1PI, per W-l-nu vertex; no scalar lines, no W-W-W vertex since lepton number forbids it):
* D: Z exchanged between lepton and neutrino leg. (d-2)^2/d x ... gives  Lambda_D = g_nu gL [Delta + 1 - L_Z - 3/2].
* A1(V): V = gamma, Z on the lepton leg, V-W-W vertex to the external W. Numerator gamma_b(-kslash)gamma_a V^{b a mu} = -4(d-1)/d x gamma^mu; isospin factor eps^{b3a}T^b gives -i; result  Lambda_A1(V) = -g c_V q_V [3(Delta + B0(0;M_W,M_V)_fin) - 1/2], c_gamma = s, q_gamma = -e; c_Z = c, q_Z = gL. (4(d-1)/d = 3 - eps/2.)
* A2: Z on the neutrino leg, Z-W-W vertex: Lambda_A2 = +g c g_nu [3(Delta + B0_fin(0;M_W,M_Z)) - 1/2] (opposite orientation of the triple vertex flips the sign).
 B0(0;M_W,M_Z)_fin = 1 + (c^2 L_W - L_Z)/s^2, B0(0;M_W,0)_fin = 1 - L_W.
Lepton wave functions: Sigma(p) = pslash P_L Sigma_L; Feynman parameters give delta Z = -G, G = q^2 [Delta - L_m - 1/2] (massless internal fermion), per boson with left coupling q and mass m.
 dZ_l = -[e^2 G_lambda + gL^2 G_Z + g^2/2 G_W],  dZ_nu = -[g_nu^2 G_Z + g^2/2 G_W],  G_lambda = Delta - ln(lambda^2/mu^2) - 1/2.
Boxes (one W + one V in the loop; V = Z in four topologies, photon only mu-e). Only chains gamma^a kslash gamma^b (x) ... survive; 4D identities (checked numerically with explicit matrices): gamma^a gamma^r gamma^m P_L (x) gamma_a gamma_r gamma_m P_L = 16 gamma^m P_L (x) gamma_m P_L, reversed second chain = 4. The relative sign of the two internal fermion momenta is s1 s2 = (+,-,-,+) for V on (mu,e),(mu,nu_e),(nu_mu,e),(nu_mu,nu_e). Result: box = -q1 q2 s1 s2 (T/4) M_W^2 I, I = -ln(M_V^2/M_W^2)/(M_V^2 - M_W^2) (Z) or I M_W^2 = ln(lambda^2/M_W^2) (photon), T = 4 or 16.
 Z: sum = gL^2 - 8 gL g_nu + g_nu^2, box_Z = -(gL^2 - 8 gL g_nu + g_nu^2)(c^2/s^2) ln c^2;  photon: box_gamma = -e^2 ln(lambda^2/M_W^2).

## 4. IR cancellation and the Fermi-theory subtraction
The Fermi-theory photonic correction (G_F is defined without it) is, in charge-retention (Fierz) order, a vertex-type correction of the conserved vector-like current plus the lepton wave functions. At zero external momenta Lambda_F(0,0) = -dZ (Ward identity, algebraic in d dims, any lambda), so the Fermi-theory total vanishes there; the physical (finite, 4D) Fermi correction is Lambda_F(p',p) - Lambda_F(0,0). The difference (full - Fermi) has an integrand that vanishes like k^2/M_W^2 at small k, hence is IR safe and may be evaluated at zero external momenta; so the subtraction removes nothing at p=0 and delta_V is the full-theory total at p = 0. The photon-mass dependence: wave functions give +e^2 ln(lambda^2) (from -e^2 G_lambda), the box gives -e^2 ln(lambda^2): they cancel identically (verified numerically in bos_dr.py main for lambda = 1e-2..1e-9 M_W). The real-emission IR divergence is the same in the full and Fermi theory and drops with the definition of G_F.

## 5. Closed form and UV check
Summing the diagrams (sympy):
 delta_V = u [4 Delta + 6 + L_W(-6 + 7/(2 s^2)) + L_Z(2 - 7/(2 s^2))].
The pole 4u (2u per vertex = C_A g^2, i.e. Z_1F/Z_2 for SU(2): checked by hand in the pure SU(2) limit: vertex 11/4 g^2 = C_F + C_A, dZ_2 = -C_F g^2) is cancelled by the poles of the Sigma terms of (*): numerically the mu-slope of the Sigma part of (*) is -4u per unit ln mu^2 (0.011155 at alpha=1/128, M_W=80.38, M_Z=91.19), the mu-independence of the total is checked to 1e-14 (bos_dr.py main). lambda drops out; the dependence on M_H is entirely in the Sigma's (delta_V is Higgs independent).

## 6. Decomposition of Delta r_bos and delta_vb
Delta r_bos = [Sigma part of (*)] + delta_V. Equivalent regrouping (Denner/Hollik form): the charge relation can be written with the mixing coefficient -2(c/s) instead of +2(s/c) if the difference 2 Sigma_AZ(0)/(s c M_Z^2) is moved into the vertex group:
 Delta r_bos = Sigma'_AA(0) - 2 (c/s) Sigma_AZ(0)/M_Z^2 - (c^2/s^2)[...] + [Sigma_W(0)-Sigma_W(M_W^2)]/M_W^2 + delta_vb,
 delta_vb = delta_V + 2 Sigma_AZ(0)/(s c M_Z^2)  =  (alpha/(4 pi s^2)) (6 + (7 - 4 s^2)/(2 s^2) ln c^2).
This Sigma part is finite and mu-independent by itself (numerically checked), so delta_vb is a finite, scale-free function of s^2 only (it equals delta_V at mu = M_W because Sigma_AZ(0) vanishes there in MS-bar). I export this delta_vb. The explicitly UV-divergent unrenormalized sum delta_V (pole 4u) is not a number without a scheme; see QUESTIONS.md.

## 7. Second routes (all in bos_dr.py `__main__`)
1. closed form of delta_vb vs. the diagram numbers (agree to 1e-16);
2. lambda independence; 3. mu independence of Delta r_bos (30, 80, 500 GeV agree to 1e-14);
4. regrouped form (Sigma with -2c/s) + delta_vb equals form (*) + delta_V;
5. large-M_H slope 11 alpha/(48 pi s^2) at M_H = 1e13..1e14 GeV (agrees to 1e-15), and the gate's blind checks.

## Not derived / assumed
* The statement that the T3 part of the gamma-Z mixing cancels against the non-universal part of the photon-lepton vertex (Ward/BRST identity) was used, not recomputed. Evidence: with it the total Delta r is mu independent and has the correct Higgs slope.
* Sigma's are taken from bos_se (SPEC).
* Fierz-order Fermi theory at zero momentum: Ward identity argument, not a separate explicit integral.

## 9. Higgs-mass dependent parts of Sigma_W and Sigma_ZZ (for M_H up to 1e14 GeV)
The float exports of bos_se carry ~M_H^2 pieces that cancel in Delta r_bos; at M_H >~ 1e9 the cancellation is lost in float (QUESTIONS.md 6). The M_H dependence of the Sigma's comes only from Higgs diagrams (Sigma_AA, Sigma_AZ have none; ghosts do not couple to H in a vector self-energy; tadpoles excluded):
* V-H loop with vertex i g_V M_V g^{mu nu} (g_V = g for HWW with M_W, g/c for HZZ with M_Z): Sigma = g_V^2 M_V^2 B0(k^2; M_V, M_H)/16 pi^2.
* Goldstone-H loop with vertex (g_V/2)(p_H - p_phi)^mu: the g^{mu nu} part is 4 times the q^mu q^nu coefficient; with Feynman parameter x, l = q - x k, int d^dl l^2/(l^2-D)^2 gives (1/d)(d/2) cancel exactly, so no d-dependent factor: Sigma = -(g_V^2/2) Bt/16 pi^2, Bt = int_0^1 dx D_x(Delta + 1 - ln D_x/mu^2), D_x = (1-x)M_V^2 + x M_H^2 - x(1-x)k^2.
* Seagull VVHH (vertex i g_V^2/2, symmetry factor 1/2): Sigma = (g_V^2/4) A0(M_H)/16 pi^2, A0 = M_H^2(Delta + 1 - ln M_H^2/mu^2).
 Sigma^H_V = (g_V^2/16 pi^2)[M_V^2 B0 - Bt/2 + A0/4]  (MS-bar, Delta dropped).
Implementation: Sigma(M_H) = Sigma_export(M_H0 = M_W) + F(M_H) - F(M_H0), F above, evaluated with mp.quad (breakpoints log-spaced down to 1e-40) in mp.workdps(60+...). Checked against the exports at M_H = 10, 300, 1000 GeV (differences relative to M_H = 125, for k^2 = 0, M_V^2): agreement to 1e-15. Delta r_bos then equals the earlier values and has the 11 alpha/(48 pi s^2) slope at 1e13..1e14. No private bos_se helper is used.
