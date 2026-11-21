# DERIVATION: O(alpha_s) correction to Delta rho from the (t, b) doublet

Status markers: [P] = done by hand on paper (below); [M] = the same algebra carried out mechanically
by the code in `qcd_drho.py` (exact rational/Gamma-function arithmetic in sympy, no fitted or typed-in
answer); [C] = cross-check.

## 0. Postulates used (SPEC sections)

* SPEC 1: doublet (t, b) in the fundamental of SU(N_C), colour generators T^a with T^a T^a = C_F 1,
  Tr 1_colour = N_C; gluons in a covariant gauge (Feynman gauge xi = 1 for the main route; general xi
  used for the gauge check). m_b = 0, m_t = m. Currents J^a_mu = qbar gamma_mu P_L (tau^a/2) q coupled as
  g W^a_mu J^{a mu}; gaugeless limit: M_W^2 = g^2 v^2/4, M_Z^2 c^2 = M_W^2, G_F = 1/(sqrt2 v^2).
* SPEC 2: Delta rho = Sigma_Z(0)/M_Z^2 - Sigma_W(0)/M_W^2 with propagator -i g/(q^2 - M^2 + Sigma).
  Dimensional regularisation d = 4 - 2 eps. Pole mass and MS-bar mass m(mu).

## 1. Delta rho in terms of current correlators [P]

Dressed propagator: D + D (i X g) D + ... = -i g/(q^2 - M^2 - X) for a 1PI insertion i X g^{mu nu}.
So Sigma = -X. The 1PI insertion from the quark loop with vertices i g gamma^mu P_L tau^a/2 is
(i g)^2 L_aa^{mu nu} where

    L_ab^{mu nu}(q) = (-1) Tr_{colour,Dirac} \int d^dk/(2pi)^d [Gamma_a^mu S(k+q) Gamma_b^nu S(k)],
    S(p) = i/(pslash - m) = i (pslash + m)/(p^2 - m^2).

Hence Sigma_a = -i g^2 L_aa (coefficient of g^{mu nu} at q = 0), and with M_W^2 = M_Z^2 c^2 = g^2 v^2/4

    Delta rho = (Sigma_33 - Sigma_11)/M_W^2 = -(4 i/v^2) (L_33 - L_11).

Flavour algebra (J^1 = (tbar b + bbar t)/2, J^3 = (tbar t - bbar b)/2, Dirac structure gamma P_L):
L_11 = L_tb/2, L_33 = (L_tt + L_bb)/4, so L_33 - L_11 = (L_tt + L_bb - 2 L_tb)/4.

Chirality: gamma P_L = (gamma - gamma gamma5)/2. At q = 0 the V-A interference needs an epsilon tensor
with two free indices and no external vector: it vanishes. With an anticommuting gamma5 (legitimate here:
the traces contain an even number of gamma5 and no anomaly-type trace survives) the axial correlator
of masses (m1, m2) equals the vector correlator with masses (m1, -m2) (move gamma5 through the m2
propagator: gamma5 (pslash + m2) gamma5... = -(pslash - m2) structure). Therefore

    L^{LL}(m1, m2) = [L_V(m1, m2) + L_V(m1, -m2)]/4,

L_bb = 0 (massless tadpoles vanish at q = 0 in dim reg), L_V(m, m)(0) = 0 (vector current conserved for
equal masses: Ward identity, checked [C] at one and two loops), so

    L_33 - L_11 = (1/16) [ L_V(m, -m) - 4 L_V(m, 0) ] =: X/16,     Delta rho = -(i/(4 v^2)) X.

## 2. One loop [P]

Dirac trace with Tr 1 = 4, contracted with g_{mu nu}/d:
(1/d) Tr[gamma^mu (kslash + m1) gamma_mu (kslash + m2)] = (4/d)[(2 - d) k^2 + d m1 m2].
With the fermion-loop sign, two propagator factors i^2 and Wick rotation (d^dk -> i d^dK, k^2 -> -K^2,
(k^2 - M^2) -> -(K^2 + M^2)), and the tadpoles

    T(a, a0) = \int d^dK/pi^{d/2} (K^2)^{-a0}/(K^2 + m^2)^a = (m^2)^{d/2-a-a0} Gamma(d/2-a0) Gamma(a+a0-d/2)/(Gamma(d/2) Gamma(a)),

one gets, in units (N_C/(16 pi^2)) m^2 (outer (4 pi mu^2/m^2)^eps factor suppressed; it is common to all orders and
multiplies a finite total):

    L_V(m, m)  = 0                      (Ward identity, exact in d)
    L_V(m, -m) = -8 i [1/eps - gamma_E] + O(eps)
    L_V(m, 0)  = -i [2/eps + 1 - 2 gamma_E] + O(eps)
    X^(1) = L_V(m,-m) - 4 L_V(m,0) = 4 i        (divergences ~ (m1 - m2)^2: 4 m^2 vs 4 x m^2 cancel)

    Delta rho_0 = -(i/(4 v^2)) (N_C m^2/(16 pi^2)) 4 i = N_C m^2/(16 pi^2 v^2) = N_C G_F m^2/(8 sqrt2 pi^2).

Scaling ~ m^2 and ~ N_C. (Hand check: this is the familiar N_C G_F F0(m,0)/(8 sqrt2 pi^2) with F0(m,0) = m^2.)

## 3. Two loops at q = 0: diagrams [P]

At q = 0 the outer momentum k runs through both quark lines. Gluon of momentum G = k - l, vertex
-i g_s gamma^alpha T^a, propagator -i [g_{alpha beta} - (1 - xi) G_alpha G_beta/G^2]/G^2. Colour factor of
every diagram: Tr(T^a T^a) = C_F N_C. Three diagrams per correlator L_V(m1, m2):

  (R)  rung:       Tr[gamma^mu S1(k) G^alpha S1(l) gamma_mu S2(l) G^beta S2(k)] D_{alpha beta}(k-l)
  (S1) self-energy on line 1: Tr[gamma^mu S1(k) G^alpha S1(l) G^beta S1(k) gamma_mu S2(k)] D_{alpha beta}
  (S2) self-energy on line 2: Tr[gamma^mu S1(k) gamma_mu S2(k) G^alpha S2(l) G^beta S2(k)] D_{alpha beta}

plus the mass-counterterm insertions S(k) (-i dm) S(k) on each massive line, with m0 = m + dm
(note dm(-m) = -dm(m): the counterterm follows the sign trick automatically). The bare-field correlators
of the (conserved / partially conserved) currents need no field or vertex renormalisation (Z1 = Z2).

Reduction [M]: the traces give polynomials in k^2, l^2, k.l; after Wick rotation K.L = (K^2 + L^2 - G^2)/2,
then partial fractions per momentum, 1/(x^p (x + m^2)^q) -> sum of pure massive / pure massless powers.
Every term is then one of three two-loop vacuum masters (Euclidean, measure d^dK d^dL/pi^d):

  (VM1) massive-massive-massless, the sunset with masses (m, m, 0):
        I(a,b,c) = \int 1/[(K^2+m^2)^a (L^2+m^2)^b ((K-L)^2)^c]
                 = (m^2)^{d-a-b-c} Gamma(a+b+c-d) Gamma(a+c-d/2) Gamma(b+c-d/2) Gamma(d/2-c)
                   / [Gamma(a) Gamma(b) Gamma(d/2) Gamma(a+b+2c-d)].
        Derivation [P]: insert the Mellin-Barnes representation of the massive L-propagator,
        1/(L^2+m^2)^b = 1/(2 pi i) \int ds Gamma(-s) Gamma(b+s)/Gamma(b) (m^2)^s/(L^2)^{b+s};
        the L integral is then massless one-loop, giving (K^2)^{d/2-b-c-s} G(b+s, c); the K tadpole gives
        Gamma functions of s; the remaining MB integral is a Barnes-lemma (first lemma) integral and
        closes to the product above. Limit c = 0 reproduces the product of two tadpoles [C].
  (VM2) massive-massless-massless (masses (m, 0, 0)):
        J(a; b, c) = \int 1/[(K^2+m^2)^a (L^2)^b ((K-L)^2)^c]
                   = (m^2)^{d-a-b-c} G(b,c) Gamma(d-b-c) Gamma(a+b+c-d)/(Gamma(d/2) Gamma(a)),
        G(b,c) = Gamma(d/2-b) Gamma(d/2-c) Gamma(b+c-d/2)/(Gamma(b) Gamma(c) Gamma(d-b-c)),
        (massless one-loop subintegral in L, then a tadpole with a non-integer power of K^2) [P].
  (VM3) fully massless: scaleless, 0.

Both masters are checked numerically in d = 4 at convergent indices by a different method (radial
integration with the 4-dimensional angular average <1/(K-L)^2> = 1/max(K^2, L^2)) [C].

All Gamma functions reduce by recursion to Gamma(1 +- eps), Gamma(1 +- 2 eps) times rational functions of
eps; the per-loop normalisation is g_s^2 mu^{2 eps}(4 pi)^{-d/2} = (alpha_s/(4 pi)) (e^{gamma_E} mu_bar^2)^eps
(MS-bar scale mu_bar^2 = 4 pi e^{-gamma_E} mu^2).

## 4. Mass renormalisation [P]

One-loop self-energy, Feynman gauge, gamma^alpha pslash gamma_alpha = (2-d) pslash:
Sigma(pslash) = g^2 C_F (4pi)^{-d/2} mu^{2eps} Gamma(eps) \int_0^1 dx (x m^2 - x(1-x) p^2)^{-eps} [(2-d)(1-x) pslash + d m].
On shell (p^2 = m^2, Delta = x^2 m^2):  Sigma(m) = (alpha_s C_F/(4pi)) m (e^{gamma} mu_bar^2/m^2)^eps Gamma(eps) (3 - 2 eps)/(1 - 2 eps).
* pole scheme: dm = -Sigma(m)   (pole of i/(pslash - m - dm - Sigma) at pslash = m), exact in eps.
* MS-bar: dm = -(pure 1/eps pole of Sigma(m)) = -(alpha_s C_F/(4 pi)) 3 m/eps.
* relation: m_pole = mbar(mu) [1 + C_F (alpha_s/pi)(1 + (3/4) ln(mu^2/mbar^2))], i.e.
  m_pole^2 = mbar^2 [1 + C_F (alpha_s/pi)(2 + (3/2) ln(mu^2/mbar^2))].
  Since Delta rho_0 ~ m^2: c_MSbar = c_pole + C_F (2 + (3/2) ln(mu^2/mbar^2)), so (c_MS - c_pole)/C_F = 2
  at mu = mbar, and d c_MS/d ln mu^2 = (3/2) C_F, which is minus the one-loop running of mbar^2:
  d ln mbar^2/d ln mu^2 = -(3/2) C_F alpha_s/pi (from Z_m = 1 - 3 C_F alpha_s/(4 pi eps)); so the product
  Delta rho_0(mbar(mu)) (1 + c_MS alpha_s/pi) is mu-independent at O(alpha_s), as it must be.
  The code computes the MS-bar coefficient directly (MS-bar counterterm in the two-loop diagrams) and
  separately checks that it equals c_pole + this shift.

## 5. Pole cancellation [M, structure P]

Laurent coefficients [eps^-2, eps^-1, eps^0] of each two-loop piece, in units
(N_C m^2/(16 pi^2)) (g_s^2 C_F/(16 pi^2)), L = ln(mu_bar^2/m^2), outer-loop gamma_E set to its MS-bar value
(tmp/poles_out.txt):

Pole scheme (dm = -Sigma(m), exact in eps):

    L_V(m,-m):  R   [-8i, -i(8L+4),  i(-4L^2-4L-4pi^2/3+2)]
                S1  [-8i, 8i(2-L),   i(-4L^2+16L-4pi^2/3-2)]      S2 = S1
                CT1 [24i, i(24L+8),  4i(3L^2+2L+8+pi^2)]          CT2 = CT1
                sum [24i, i(24L+44), i(12L^2+44L+4pi^2+62)]
    L_V(m, 0):  R   [-2i, -i(2L+3),  i(-L^2-3L-19/2-pi^2/3)]
                S1  [-5i, i(5/2-5L), i(-10L^2+10L-2pi^2+13)/4]
                S2  [ i,  i(L+3/2),  i(2L^2+6L+11+2pi^2)/4]
                CT1 [12i, i(12L+10), i(6L^2+10L+2pi^2+21)]        CT2 = 0 (massless b)
                sum [6i,  i(6L+11),  i(18L^2+66L+10pi^2+105)/6]
    X = sum(m,-m) - 4 sum(m,0):  eps^-2: 24i - 24i = 0;  eps^-1: (24L+44) i - 4(6L+11) i = 0;
                                 eps^0:  i(-8 - 8 pi^2/3), L-independent.

MS-bar scheme (dm = -3 m/eps): R, S1, S2 as above; CT1(m,-m) = [24i, -24i, 2 i pi^2], CT1(m,0) = [12i, -6i, i(pi^2-3)];
sums (m,-m): [24i, -i(24L+20), i(-12L^2+28L-2)], (m,0): [6i, -i(6L+5), i(-18L^2+6L-39+4pi^2)/6];
X: poles cancel; finite part i(24 + 24L - 8pi^2/3), so c_MS/C_F = (24 + 24L - 8pi^2/3)/16.

Structure: the 1/eps^2 of each correlator is the overall divergence (~ (m1-m2)^2: 24 = 4 x 6) times the
subdivergence; mass counterterms remove the m-dependent subdivergences (the vertex/self-energy ones, ~ Z1 - Z2,
cancel between R and S1 + S2); the remaining overall divergences ~ (m1 - m2)^2 cancel in X exactly as at one
loop. The code asserts that the eps^-1 ... eps^-4 coefficients of X vanish identically and that gamma_E drops out.

## 6. Results

Writing Delta rho = Delta rho_0(m)[1 + c alpha_s/pi]:

    c_pole  = -C_F (1 + pi^2/3)/2           ( = -(2/3)(1 + pi^2/3) = -2.8599 for C_F = 4/3 )
    c_MSbar = C_F [ 3/2 - pi^2/6 + (3/2) ln(mu^2/mbar^2) ],   mu_over_m = mu/mbar(mu).

These closed forms are what the exact sympy computation returns [M] (X = (N_C m^2/16pi^2)[4i + (g_s^2 C_F/16pi^2) X2], g_s^2/(16pi^2) = (alpha_s/pi)/4, so c/C_F = X2/(16 i):
pole X2 = i(-8 - 8pi^2/3) -> c/C_F = -1/2 - pi^2/6); the pi^2 arises from zeta(2) in the
Gamma-function expansion of the (m, m, 0) and (m, 0, 0) sunsets. The coefficient is linear in C_F (every
two-loop diagram and dm carry exactly one C_F, and no N_C-dependent piece exists at this order: no gluon
self-interaction or closed quark loop enters at O(alpha_s)); the overall N_C sits in Delta rho_0.

## 7. Gauge independence [P + C]

The xi-dependent part of the gluon propagator is G_alpha G_beta. Contracted into a quark line,
Gslash = S^{-1}(k) - S^{-1}(l) (up to factors of i), so the longitudinal gluon telescopes: the xi-terms of
R, S1 and S2 cancel in the sum for each L_V(m1, m2), and the counterterm dm (pole or MS-bar) is
gauge independent at one loop (on shell the xi-part of Sigma is proportional to (pslash - m)). This is
checked exactly by the code (xi-coefficient of R + S1 + S2 = 0). Physically Delta rho at q = 0 is a
low-energy S-matrix ratio (neutral/charged current strength), hence gauge independent.

## 8. Independent second route [C]: the Ward identity / scalar correlator

For the vector current V = qbar1 gamma q2 with bare masses, d_mu V^mu = i(m01 - m02) qbar1 q2, so
q_mu q_nu L_V^{mu nu}(q) = (m01 - m02)^2 L_S(q) + (q-independent contact terms). With
L^{mu nu}(q) = g^{mu nu} A(q^2) + q^mu q^nu B(q^2), the O(q^2) coefficient gives

    L_V(m1, m2)(0) = A(0) = (m01 - m02)^2 * [coefficient of q^2 in L_S(q)],

a completely different set of traces (scalar vertices, propagators Taylor-expanded in the external q,
q^alpha q^beta -> q^2 g^{alpha beta}/d), and the bare mass factor (m01-m02)^2 = (m1-m2)^2 + 2(m1-m2)(dm1-dm2)
supplies an extra counterterm term. The code computes X through this route at one and two loops (pole
scheme) and prints it next to the main result; they must agree exactly.
RESULT (tmp/main_out3.txt): one loop X = 4i by both routes; two loops, Ward route, all poles cancel and
c/C_F = -1/2 - pi^2/6 (pole), 3/2 - pi^2/6 + (3/2) L (MS-bar), identical to the main route.
Gauge check: the (1-xi) terms of R + S1 + S2 vanish exactly for (m,m), (m,-m), (m,0).
Masters: numerical radial integration (d = 4: I(2,2,1) = 1, I(3,2,1) = 1/4; d = 3: I(2,1,1) = pi, J(2;1,1) = 2 pi)
agrees with the general-d formulas to ~1e-14; the engine's eps-reduced Gamma basis agrees with them at eps = 0.3.

Further checks: Ward identity L_V(m, m)(0) = 0 at two loops including counterterms; mu-independence of
c_pole; the MS-bar result computed directly with the MS-bar counterterm equals c_pole + the scheme shift of
section 4; numerical checks of the masters.

## Not derived / caveats
* Section 6 closed forms: I knew the expected structure (zeta(2) from the masters) beforehand; the
  numbers themselves are produced by the code from the diagrams and were not entered anywhere.
* The Barnes-lemma step for VM1 is sketched, not written out line by line; it is verified numerically in d=4
  (section 3) and by its c = 0 limit.
* The gamma5 treatment is the anticommuting one (justified in section 1); no trace with a single gamma5
  survives.
