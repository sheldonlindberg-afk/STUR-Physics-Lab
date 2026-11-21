# DERIVATION: bosonic one-loop Delta r of muon decay in the general R_xi gauge (build b)

Sections 0-4, 6, 7 were written before the code (plan and equations). One sign was corrected afterwards
(section 3: Delta r is the *plus* relative correction to G_F, see the note there); sections 5, 8, 9 were filled in
from the computation.

## 0. Postulates used (SPEC sections 1, 2)

SU(2)_L x U(1)_Y, D = d - i g W^a T^a - i g' Y B, Higgs doublet of Y = 1/2 with V = -mu^2 Phi^+Phi + lambda (Phi^+Phi)^2
at its minimum, massless leptons (left doublet, right charged singlet), one R_xi gauge parameter xi for W^+-, Z and gamma,
Higgs tadpoles cancelled by the tadpole counterterm, on-shell inputs M_W, M_Z, M_H, alpha(0), s^2 = 1 - M_W^2/M_Z^2.
Dimensional regularisation d = 4 - 2 eps; MS-bar = drop 1/epsbar = 1/eps - gamma_E + ln 4 pi, scale mu. d-dependent
coefficients are expanded to O(eps) against the pole. Anticommuting gamma_5 (every lepton line ends in P_L; massless
propagators preserve chirality, so every vertex on the line contributes its left-handed coupling).

## 1. Lagrangian in a real basis and the Feynman rules (all generated in the code from these definitions)

*Scalars.* Phi = ((phi1 + i phi2)/sqrt2, (phi3 + i phi4)/sqrt2), phi3 = v + H, phi4 = chi. Then |D Phi|^2 = 1/2 (D phi)^T (D phi),
D phi = d phi + A^a T^a phi, with A^a = (W1, W2, W3, B) and real antisymmetric T^a = Real4x4(-i g tau^a/2), T^B = Real4x4(-i g'/2)
(Real4x4 maps a complex entry a + i b to the block [[a, -b], [b, a]]). [T^a, T^b] = C^{abc} T^c with C^{abc} = g eps^{abc}
(checked numerically). Expanding phi = v + h:

    1/2 (D phi)^2 = 1/2 (dh)^2 + A^a . (dh)^T T^a v + A^a . (dh)^T T^a h + 1/2 A^a A^b (T^a(v+h)).(T^b(v+h)).

Mass matrix M^2_ab = F_a . F_b, F_a := T^a v: M_W = g v/2 for W1, W2, M_Z^2 = (g^2 + g'^2) v^2/4 for Z = c W3 - s B, and
A = s W3 + c B massless (checked). e = g s = g' c, so g = e/s, g' = e/c, v = 2 M_W/g.

*Gauge fields.* -1/4 F^a F^a, F^c_mn = d_m A^c_n - d_n A^c_m + C^{abc} A^a_m A^b_n (from [D_m, D_n]).

*Gauge fixing.* L_gf = -1/(2 xi) sum_a (d.A^a - xi F_a . h)^2. Its cross term (d.A^a)(F_a.h) = -A^a . d(F_a.h) cancels the
mixing A^a . (dh)^T F_a. Goldstone mass^2 matrix xi F_a F_a^T: G_F = F_F . h / M_F has mass^2 xi M_F^2. The quadratic gauge
part gives -i[g - (1 - xi) k k/(k^2 - xi M^2)]/(k^2 - M^2), i.e. the SPEC propagator.

*Ghosts.* With delta phi = alpha^a T^a phi, covariance of D requires delta A^c = -d alpha^c - C^{abc} A^a alpha^b, and
L_gh = cbar^a delta G^a[alpha -> c] = cbar^a(-d^2 - xi M^2_ab) c^b + (d^m cbar^a) C^{dba} A^d_m c^b - xi cbar^a F_a^T T^b h c^b.

*Leptons.* L = psibar_L i gamma.D psi_L + lbar_R i gamma.D l_R: vertex i gamma^mu G^V P_L with the doublet (nu, l) matrices
G^F = sum_a R_aF g_a t^a: G^{W1} = g tau^1/2, G^{W2} = g tau^2/2, G^Z = (g/c)(tau^3/2 - s^2 Q), G^A = e Q, Q = diag(0, -1);
[G^a, G^b] = i C^{abc} G^c (checked).

*Mass basis.* A^a = R_aF F (W3 = c Z + s A, B = -s Z + c A), h = O hhat with orthonormal columns (G_W1, G_W2, G_Z, H) (checked).
All coupling tensors (C^{FGH}, That^F = O^T T^F O, the V V S couplings) are rotated numerically: no vertex is transcribed by hand.

Feynman rules (all momenta incoming; vertex = i times the coefficient in L, summed over identical-field assignments):
* V V V (a mu k1)(b nu k2)(c rho k3): C^{abc}[g_{mu nu}(k1-k2)_rho + g_{nu rho}(k2-k3)_mu + g_{rho mu}(k3-k1)_nu]
* V V V V: -i[C^{abe}C^{cde}(g^{mu rho}g^{nu sig} - g^{mu sig}g^{nu rho}) + C^{ace}C^{bde}(g^{mu nu}g^{rho sig} - g^{mu sig}g^{nu rho})
  + C^{ade}C^{bce}(g^{mu nu}g^{rho sig} - g^{mu rho}g^{nu sig})]
* V(mu) S_i(p_i) S_j(p_j): T^a_ij (p_i - p_j)_mu
* V V S_i: i g_{mu nu}[(F_a^T T^b)_i + (F_b^T T^a)_i]
* V V S_i S_j: i g_{mu nu}[(T^{aT} T^b)_ij + (T^{aT} T^b)_ji]
* ghost: antighost a (incoming momentum q), ghost b, gauge field d: C^{dba} q_mu
* lepton: i gamma^mu G^V P_L
Propagators: gauge -i[g/(k^2-M^2) - (k k/M^2)(1/(k^2-M^2) - 1/(k^2-xi M^2))]; Goldstone, ghost i/(k^2 - xi M^2);
Higgs i/(k^2 - M_H^2); lepton i kslash/k^2. The photon uses the same form with M -> lambda (photon mass, lambda -> 0) in
all its parts, so one single infrared regulator is used everywhere; its k k part tends to -(1-xi) k k/k^4. Every gauge line
is thus a sum of three simple-pole terms (g part with M, k k part with M and with xi M), which makes all loop integrals
simple-pole integrals and keeps xi = 1 and xi = 0 regular.

## 2. Gauge-boson self-energies

Convention: sum of 1PI two-point diagrams = i Pi^{mu nu} = -i[Sigma_T (g - pp/p^2) + Sigma_L pp/p^2]; the transverse
propagator is -i/(k^2 - M_0^2 + Sigma_T(k^2)), the pole is at M^2 = M_0^2 - Re Sigma_T(M^2), so delta M^2 = Re Sigma_T(M^2).
Sigma_T = -(g_{mu nu} - p_mu p_nu/p^2) Pi^{mu nu}/(d - 1) (projector with its d dependence).
Diagrams for external (F, mu, p), (G, nu, -p), summing over all mass-basis internal fields and over the three parts of
every gauge line:
 (1) gauge loop, 1/2 C^{F V1 V2} C^{G V1 V2} V3 Delta Delta V3;  (2) gauge-scalar loop (VVS)^2, symmetry 1;
 (3) scalar loop 1/2 That^F_ij That^G_ij (2k+p)(2k+p);  (4) ghost loop (-1) C^{F b a} C^{G a b} k_mu (k+p)_nu;
 (5) VVVV tadpole -i C^{FVe}C^{GVe}[g Delta^r_r - Delta];  (6) VVSS tadpole;  Higgs one-point insertions omitted (SPEC, sec. 6).
Bubbles with one Feynman parameter: k = l - x p, Delta = x m2^2 + (1-x) m1^2 - x(1-x) p^2,
(l.p)^{2j} -> (l^2 p^2)^j (2j-1)!!/prod_{i<j}(d+2i), and

    int d^dl/(2 pi)^d (l^2)^n/(l^2 - Delta)^2 = i/(16 pi^2) (n+1) Delta^n [1/epsbar - ln(Delta/mu^2) + n/(n+1)] + O(eps)
    int d^dk/(2 pi)^d (k^2)^n/(k^2 - m^2)     = i/(16 pi^2) m^{2n} A0(m),   A0 = m^2 (1/epsbar + 1 - ln m^2/mu^2)

(from Gamma(n + d/2) Gamma(2 - n - d/2)/Gamma(d/2); the O(eps) of the numerator coefficient C(d) gives -2 C'(4) x pole).
The x integrals int_0^1 x^j ln|Delta| are done in closed form through the roots of Delta (real part = ln|.|, valid above
thresholds too), with a series for distant roots. Sigma(0) and dSigma/dp^2(0) come from the analytic p^2 dependence of
the integrand (d ln Delta/dp^2 = -x(1-x)/Delta). Results at xi = 1 (my sign of A):
Sigma^AA_T(0) = 0 in every xi (checked to 1e-48), dSigma^AA/dp^2 pole -3 alpha/(4 pi), Sigma^AZ_T(0) = -(alpha/4 pi)(2 M_W^2/(s c)) B0(0, M_W, M_W).

## 3. Charge, mixing angle, masses: class SE

Bare parameters e0, M_W0, M_Z0, s0^2 = 1 - M_W0^2/M_Z0^2. Muon decay at zero momentum transfer: the W propagator at k = 0 is
i g/(M_W0^2 - Sigma^W_T(0)) (the k k and Goldstone parts do not couple to massless leptons), so

    G_F/sqrt2 = e0^2/(8 s0^2 (M_W0^2 - Sigma^W_T(0))) (1 + delta_VBW).

M_V0^2 = M_V^2 + Re Sigma^V_T(M_V^2) (Z-gamma mixing enters the Z pole only at two loops); s0^2 = s^2(1 + delta s^2/s^2),
delta s^2/s^2 = (c^2/s^2)(dM_Z^2/M_Z^2 - dM_W^2/M_W^2); e0 = e(1 + dZ_e).
Thomson charge: the external photon at q -> 0 receives the residue factor (1 + Sigma'^AA(0))^{-1/2} and the A -> Z transition
(-i Sigma^AZ)(-i/(-M_Z^2)) = Sigma^AZ(0)/M_Z^2 times the Z coupling (g/c)(T^3 P_L - s^2 Q). Its T^3 part must be cancelled by the
W-loop vertex of the photon; the -s^2 Q part is universal:

    dZ_e = 1/2 Sigma'^AA_T(0) + (s/c) Sigma^AZ_T(0)/M_Z^2        (verified directly, section 7a, in every xi)

SPEC: M_W^2 s^2 = pi alpha/(sqrt2 G_F) (1 + Delta r), i.e. G_F/sqrt2 = e^2/(8 s^2 M_W^2) (1 + Delta r).
[Correction to the first draft: I had written (1 - Delta r); with it every term had the opposite sign. Found by the xi = 1
comparison of section 9 (a pure sign of the definition, no term was adjusted).] Hence Delta r = SE + VBW with

    SE  = Sigma'^AA(0) + 2 (s/c) Sigma^AZ(0)/M_Z^2 - (c^2/s^2)[Sigma^ZZ(M_Z^2)/M_Z^2 - Sigma^W(M_W^2)/M_W^2]
          + [Sigma^W(0) - Sigma^W(M_W^2)]/M_W^2          (all Sigma_T, real parts, MS-bar at mu)
    VBW = delta_VBW (MS-bar at mu)

Renormalization constants used: dM_W^2 = Re Sigma^W_T(M_W^2), dM_Z^2 = Re Sigma^ZZ_T(M_Z^2), delta s^2/s^2 as above, dZ_e as
above; no field renormalization is needed (bare perturbation theory; the lepton legs enter through LSZ factors).

## 4. Vertex, boxes, wave function, Fermi subtraction: class VBW

All external momenta are zero (massless leptons, zero momentum transfer). Diagrams (G^X the external W^a = W1, W2):
* vertex (A), neutral or charged boson V between the two legs: (i g^s G^V)(i(-k)/k^2)(i g^a G^X)(i(-k)/k^2)(i g^r G^V) Delta^V_sr(k)
  (the W W W-on-the-line terms cancel between W1 and W2; Z between nu and l survives);
* vertex (B), non-abelian, internal (W, Z) and (W, gamma) on either side:
  (i g^s G^{V2})(i(-k)/k^2)(i g^r G^{V1}) Delta^{V1}_{rb}(k) Delta^{V2}_{sc}(k) C^{X V1 V2}[-g_ab k_c + 2 g_bc k_a - g_ca k_b];
* lepton self-energy (Z, gamma, W loops): (i g^s G^V) i(p-k)/(p-k)^2 (i g^r G^V) Delta^V_sr, expanded to O(p): 1PI = i pslash K P_L;
  LSZ factor 1 - K/2 per leg, four legs: -(K_l + K_nu);
* boxes: W x Z and W x gamma between line 1 (mu -> nu_mu) and line 2 (nu_e -> e), direct and crossed, every ordering.
Dirac algebra: d-dimensional reduction of the gamma strings (anticommutation; gamma^a gamma_a = d) after angular averaging
k^{a1}..k^{a2n} -> (k^2)^n/(d(d+2)..(d+2n-2)) sum over pairings; results e.g. (A, g part) (d-2)^2/d gamma^alpha,
(B, g g) 4(d-1)/d gamma^alpha, self-energy -(d-2)^2/d pslash. Boxes: finite structure by structure, reduced in 4 dimensions with
explicit gamma matrices to r gamma P_L x gamma P_L (r = -16/d direct, 4/d crossed for the g g parts, etc.); the pole of each box
structure vanishes, so no evanescent ambiguity. Vacuum integrals int (k^2)^n/prod(k^2 - m_j^2)^{a_j} by exact partial
fractions in t = k^2 (Taylor coefficients at each pole, repeated poles included) and int 1/(k^2-m^2)^q:
q = 1: A0, q = 2: 1/epsbar - ln(m^2/mu^2), q >= 3: (-1)^q m^{2(2-q)}/((q-1)(q-2)); massless: 0 (only when IR safe).
    delta_VBW = sum_a [dLam^a_12 G^a_21 + G^a_12 dLam^a_21]/sum_a G^a_12 G^a_21 - (K_l + K_nu) + box/tree - Fermi.
Fermi subtraction: the one-loop photonic correction of the four-fermion theory in the charge-retention (Fierz) order, at the
same zero momenta and with the same photon mass, is vertex + legs of a conserved current at zero momentum transfer; it vanishes
identically by the abelian Ward identity Lambda^a(p,p) = -dSigma/dp_a (any xi, in d dimensions). Hence the SM photonic pieces
(W-gamma box, l-gamma self-energy) must be lambda independent by themselves: they are (for xi > 0 the legs carry
+xi alpha/(4 pi) ln lambda^2 and the boxes -xi alpha/(4 pi) ln lambda^2; the sum is lambda independent to 1e-15).

## 5. Structure of the xi dependence (results), and the Landau gauge

Pieces at M_W = 80.38, M_Z = 91.19, M_H = 125, alpha = 1/128, mu = M_W (units of 1; 'AZ' = Sigma^AZ(0)/M_Z^2, 'W0' =
Sigma^W(0)/M_W^2, 'WM' = Sigma^W(M_W^2)/M_W^2, 'ZM' = Sigma^ZZ(M_Z^2)/M_Z^2):

    xi     Sigma'AA     AZ          dZ_e        W0          WM          ZM          SE          vertex      wf          box         VBW
    0      1.1398e-3  -1.4505e-3  -2.0723e-4  -6.2158e-3  -1.0912e-2  -8.1498e-3  -5.3408e-3   1.1076e-3   6.8719e-3   1.6589e-3   9.6384e-3
    1e-6   1.1398e-3  -1.4504e-3  -2.0723e-4   6.9233e-4  -1.0912e-2  -8.1498e-3   1.5673e-3   1.1076e-3   6.8718e-3  -5.2491e-3   2.7303e-3
    0.3    4.9522e-4  -8.4894e-4  -2.0723e-4  -3.1717e-3  -9.4654e-3  -6.7032e-3  -3.7434e-3   1.6926e-3   4.1180e-3   2.2303e-3   8.0409e-3
    1     -4.1447e-4   0          -2.0723e-4  -1.6059e-3  -8.8478e-3  -6.0855e-3  -2.7952e-3  -1.8218e-5   3.2081e-3   3.9029e-3   7.0928e-3
    4     -4.5117e-3   3.8236e-3  -2.0723e-4   2.4862e-3  -1.5357e-2  -1.2595e-2   7.8060e-3  -2.5082e-2   1.7621e-2   3.9529e-3  -3.5085e-3
    25    -4.7372e-2   4.3822e-2  -2.0723e-4   1.9422e-2  -1.4364e-1  -1.4087e-1   1.5302e-1  -4.0379e-1   2.8394e-1  -2.8870e-2  -1.4872e-1
    1000  -3.9955     3.7283     -2.0723e-4   6.9598e-1  -1.3770e+1  -1.3767e+1   1.4456e+1  -3.9098e+1   2.7989e+1  -3.3423     -1.4451e+1

(wf and box are each shown with their photon ln lambda^2 replaced as in the IR rule below; only their sum is meaningful.)
* Every self-energy (Sigma'^AA, Sigma^AZ, Sigma^W(0), Sigma^W(M_W^2), Sigma^ZZ(M_Z^2)) depends on xi; the photon one at q^2 = 0 only
  through charged-W/Goldstone/ghost loops; Sigma^AA_T(0) = 0 for every xi.
* The xi dependence of Sigma'^AA(0) and of 2(s/c)Sigma^AZ(0)/M_Z^2 cancels exactly inside the charge: dZ_e is xi independent
  (it is a physical coupling), so the charge renormalization carries no xi.
* The mass counterterms dM_W^2, dM_Z^2 are xi dependent because the tadpoles are excluded (section 6); in the mixing-angle
  combination c^2/s^2(ZM - WM) and in W0 - WM a xi dependence remains; together with W0 this is the xi dependence of SE.
* In VBW the xi dependence comes from the k k parts of the propagators: non-abelian vertex (B) and abelian Z vertex (A),
  the lepton self-energies (Z, W and photon k k parts) and the boxes (W x Z, W x gamma k k parts).
* SE(xi) - SE(1) = -(VBW(xi) - VBW(1)) to 1e-13; at large xi both classes grow like xi (and like xi ln xi), the total does not.
Total Delta r_bos (this parameter point): 0.004297530731364 for xi = 0, 0.3, 1, 4, 25, 1000 (spread 1e-13 relative);
at (75, 91.19, 300, 1/130): 0.007037199500109 for xi = 0, 1, 1000.

*Landau gauge and the infrared.* For every xi > 0 each class is infrared finite (the lambda -> 0 limit exists; checked
numerically, the residual lambda dependence is the O(lambda) non-analytic term of Sigma^W(M_W^2)). At xi = 0 exactly the
Goldstones and the k k/k^2 parts are massless and Sigma^W_T(0) acquires an infrared logarithm from the (Landau photon,
massless Goldstone) and (photon, W k k) loops at zero momentum: Sigma^W(0)/M_W^2 = a - (3 alpha/16 pi) ln lambda^2, cancelled in the total
by the W-gamma box (+(3 alpha/16 pi) ln lambda^2). As xi -> 0+ (lambda -> 0 first) this shows up as the same coefficient times ln xi,
so the classes are not continuous at xi = 0. Rule used for the classes (uniform in xi, and it only acts at xi = 0): the
dependence a + b ln lambda^2 is extracted from two tiny lambda and the infrared pole is treated like the UV one in MS-bar,
ln(lambda^2/mu^2) -> 1 (the replacement that maps int 1/((k^2-lambda^2) k^2 ...) onto its dimensionally regularised value with
the 1/eps_IR pole dropped, e.g. B0(0, lambda, 0) -> B0(0, 0, 0) = 0). The total is untouched (b_SE + b_VBW = 0).

## 6. Tadpoles

A Higgs one-point insertion T attached through the H V V vertex (i g M_W g^{mu nu}, i (g/c) M_Z g^{mu nu}) and a zero-momentum Higgs
propagator adds to Sigma^V_T a momentum-independent constant k M_V^2 with the same k for W and Z (both couplings are 2 M_V^2/v), and
nothing to Sigma^AA, Sigma^AZ (no H A A, H A Z vertex) or to the lepton diagrams (no H l l, chi l l, phi l nu coupling for massless
leptons). In SE it enters only through Sigma^ZZ(M_Z^2)/M_Z^2 - Sigma^W(M_W^2)/M_W^2 (k - k = 0) and Sigma^W(0) - Sigma^W(M_W^2) (0): the
gauge-independent total is unchanged. Dropping them does make dM_W^2, dM_Z^2 gauge dependent, which is why the classes depend on xi.

## 7. Independent second routes

(a) Thomson charge recomputed directly: photon-lepton vertex at q = 0 (abelian Z and gamma vertices, the W W nu triangle with the
photon on the W line, all with their k k parts), the four lepton legs, the photon residue and the A -> Z transition, for the
doublet (nu, l)_L. Result, at xi = 0, 1, 7: the neutrino charge shift vanishes (1e-92, finite and pole parts), and the charged
lepton gives dZ_e = 0.018883500481378 (finite, mu = M_W) and pole -0.002175946487585, identical to 1/2 Sigma'^AA + (s/c)Sigma^AZ/M_Z^2.
(b) xi = 1 VBW reduced by hand (section 9) and compared with the code: identical to 1e-15.
(c) The total is xi independent (1e-13), lambda independent, UV finite (pole coefficients cancel to 1e-27 relative), mu
independent, has the large-M_H slope 11 alpha/(48 pi s^2) in every xi (deviation 1e-9), and is linear in alpha.
(d) Numerics: 90-digit mpmath, lambda = 1e-14 and 1e-17 GeV. Against (70 digits, lambda = 1e-12, 1e-15) the total changes by
3e-13 relative and against lambda = 1e-10 by 2e-11: the residual is the O(lambda) term of Sigma^W(M_W^2), linear in lambda.

## 8. Not derived / open

* The Fermi-theory subtraction is taken in the charge-retention (Fierz) order where it is defined and UV finite; it then
  vanishes at zero momenta. In the charge-exchange order with d-dimensional Dirac algebra it would differ by an evanescent
  O(eps)/eps constant; I did not adopt that scheme (it would shift VBW and the total by a constant).
* Class values at exactly xi = 0 depend on the infrared rule of section 5 (the total does not).
* No closed form was derived for the xi-dependent parts in general xi (they are computed exactly but numerically).

## 9. Results and the xi = 1 closed form

Hand reduction at xi = 1 (MS-bar, mu = M_W, S(M) = -1/2 - ln(M^2/mu^2), B0 finite parts, g_nu = g/(2c), g_l = (g/c)(s^2 - 1/2)):
16 pi^2 delta_VBW = 2[g_nu g_l S(M_Z) + g^2(c^2(3 B0(0,M_W,M_Z) - 1/2) + s^2(3 B0(0,M_W,0) - 1/2))] - [S(M_Z)(g_nu^2 + g_l^2) + e^2 S(lambda)
+ g^2 S(M_W)] - M_W^2 ln(M_Z^2/M_W^2)/(M_W^2 - M_Z^2) (g_nu^2 + g_l^2 - 8 g_nu g_l) + e^2 ln(M_W^2/lambda^2),
which simplifies (sympy, exactly) to

    VBW(xi = 1) = alpha/(4 pi s^2) [6 + (7 - 4 s^2)/(2 s^2) ln c^2 - 4 ln(M_W^2/mu^2)],

UV divergent and mu dependent as the SPEC says. The code reproduces it at mu = 30, M_W, 900 GeV to 1e-16.
Total at the gate point: Delta r_bos = 0.004297530731364 for xi = 0, 0.3, 1, 4, 25, 1000.
SE / VBW at mu = M_W: xi = 0: -0.005340837477 / 0.009638368209; xi = 1: -0.002795240132 / 0.007092770864;
xi = 1000: 14.455679220113 / -14.451381689382.
