# DERIVATION: nucleon polarizabilities at O(p^3) in HB ChPT (build a)

Units hbar = c = 1, metric (+,-,-,-), Heaviside-Lorentz, e^2 = 4 pi alpha. g = g_A, f = f_pi, m = m_pi.
Everything below was derived here; no numerical value was looked up.

## 0. Result

    alpha_E = 5 e^2 g^2 / (384 pi^2 f^2 m) = 5 alpha g^2 / (96 pi f^2 m)
    beta_M  =   e^2 g^2 / (768 pi^2 f^2 m) =   alpha g^2 / (192 pi f^2 m) = alpha_E / 10

Finite, no counterterm, no divergence (section 5). Isospin symmetric (section 1.3).
Numerical values printed by `python3 nucleon_pol.py` (outputs of the code, not inputs), at g=1.27, f=92.4 MeV,
m=139.57 MeV, alpha=1/137.036: alpha_E = 1.6375e-10 MeV^-3 = 1.258e-3 fm^3, beta_M = 1.258e-4 fm^3;
route B agrees to 2e-15, route C (Baldin, alpha+beta) to 2e-14.

## 1. Vertices from the Lagrangian (SPEC section 1)

### 1.1 Axial vertex and Kroll-Ruderman
u = sqrt(U) = exp(i tau.pi/2f). To first order in pions
u_mu = i(u^+ D_mu u - u D_mu u^+) = -tau_a (D_mu pi)_a / f + O(pi^3),
where D_mu pi is the pion covariant derivative (the photon enters through the external vector field
r_mu = l_mu = e Q A_mu; for the pion triplet it is the charge commutator, i.e. pi^+- carry charge +-e, pi^0 none).
In the rest frame v = (1,0,0,0), S = (0, sigma/2), so S.u = -(sigma_i/2) tau_a (D_i pi)_a / f and

    H_int = + (g/2f) sigma_i tau_a (D_i pi)_a  at the nucleon position (x = 0),

which contains the pseudovector pi N N vertex (D_i -> d_i) AND the Kroll-Ruderman gamma pi N N contact vertex
(the -ieA_i part of D_i). In charged fields, tau.pi = tau3 pi0 + sqrt2 (tau_+ phi + tau_- phi^+), with phi
annihilating pi^+ (charge +e), D_mu phi = (d_mu + i e A_mu) phi.

### 1.2 Photon-pion vertices
From (f^2/4)Tr(D U D U^+) at O(pi^2): (D_mu phi)^+(D^mu phi) - m^2 phi^+ phi + (1/2)[(d pi0)^2 - m^2 pi0^2]
(chi = m^2 gives the pion mass). This contains the gamma pi pi vertex i e A^mu (phi d_mu phi^+ - phi^+ d_mu phi)
and the gamma gamma pi pi seagull e^2 A^2 phi^+ phi.

### 1.3 Nucleon-photon and Weinberg-Tomozawa terms
The nucleon couples to the photon only through v.D: -e Q v.A = -e Q A_0. The WT term is in v.Gamma (two pions,
one nucleon point, isovector tau3). Neither contributes to the polarizabilities:
* photon on a nucleon line couples to A_0 only. In the radiation gauge (A_0 = 0, eps.v = 0) it is absent; in a static
  scalar potential chosen with phi(0) = 0 at the (infinitely heavy, fixed) nucleon it is absent too; with plane-wave
  Coulomb photons it is present but cannot produce the E(q).E(q') structure (section 3.1, Born subtraction).
* WT (and the e A_0 pi pi N N piece of v.Gamma): a pion loop closing at one point on the nucleon line, i.e. the
  induced pion charge density <j_0(0)>. By charge conjugation (Furry) it is odd in the external field: no O(A^2) term.
  (Also it is isovector, tau3, while the result is isoscalar.)
* Isospin: the spin-isospin factor of the g^2 self-energy is <sigma_i sigma_j><tau_a tau_b>; only delta_ij delta_ab
  survives at O(E^2), O(B^2) (the epsilon pieces need an axial vector bilinear in E or B (none) or are odd in e).
  Proton: pi^+ (weight 2) and pi^0 (1); neutron: pi^- (2) and pi^0 (1). pi^0 is neutral, and pi^+ vs pi^- differ
  by e -> -e, which an O(e^2) quantity does not see: alpha_E^p = alpha_E^n, beta_M^p = beta_M^n.

## 2. The master formula (static source, Euclidean)

With m_N -> infinity the nucleon is a static source at x = 0 with spin-isospin operators and zero Hamiltonian.
The O(g^2) ground-state energy in a STATIC external field is (Euclidean, tau-ordered on the source)

    Delta E = -(g/2f)^2 sum_{ab} <sigma_i tau_a sigma_j tau_b> int_0^inf dtau  <(D_i pi)_a(0,tau) (D_j pi)_b(0,0)>.

(Check at zero field: G0(tau) = int d^3k e^{-w tau}/2w, int_0^inf -> 1/w, giving -sum_k |V_k|^2/w_k: second-order PT.)
The correlator summed over a (delta_ab part) is a bosonic Euclidean correlator of the same operator at two times in a
time-independent background, hence even in tau; therefore int_0^inf dtau = (1/2) int_-inf^inf dtau = (1/2) x (zero
Euclidean frequency nu = 0). The two charged real fields pi_1, pi_2 give <psi psi^*> + <psi^* psi> = charge +e and -e
propagators; their O(field^2) parts are equal. 2 x 1/2 = 1 and

    Delta E = -(g^2/4f^2) D[A],   D[A] = sum_i <x=0| Pi_i K^{-1} Pi_i |x=0>,
    Pi = p - eA,  K = Pi^2 + m^2 - e^2 A_0^2   (the nu = 0 charged-pion operator).

The nu=0 operator: the charged KG operator in a static potential, continued to Euclidean frequency nu, is
nu^2 - 2 i nu e A_0 - e^2 A_0^2 + Pi^2 + m^2; at nu = 0 only -e^2 A_0^2 survives (the single-A_0 insertions carry a
factor of the pion energy and drop out; physically the static Coulomb-photon vertex is ~ (2 k_0)).
D is manifestly gauge covariant (|x=0> only picks up the phase e^{ie Lambda(0)} on both sides).

Identification (SPEC section 2): Delta E = -2 pi (alpha_E E(0)^2 + beta_M B(0)^2).

Diagram content of D (expanding K^{-1} = G0 - G0 V G0 + G0 V G0 V G0, G0 = 1/(p^2+m^2), V = K - p^2 - m^2):
 * T1 (KR-KR):  e^2 <0|A_i G0 A_i|0>
 * T2 (KR-pion-line photon): <0|(-eA_i)(-G0 V1 G0) p_i|0> + mirror,  V1 = -e(p.A + A.p)
 * T3 (pi pi gamma gamma seagull): -<0| p_i G0 (e^2 A^2 - e^2 A_0^2) G0 p_i |0>
 * T4 (two single pi pi gamma insertions): <0| p_i G0 V1 G0 V1 G0 p_i |0>
plus diagrams with photons on the nucleon line (Born-type), discussed below.

## 3. Route A (main, implemented in nucleon_pol.py): momentum-space loop diagrams with plane waves

External fields A_0 = phi1 e^{iq.y} + phi2 e^{iq'.y}  (electric), or A = a e^{iq.y} + a' e^{iq'.y} with a.q = a'.q' = 0
(magnetic). Keep the term bilinear in the two photons and of order q q'. Momentum matrix elements:
<k'|e^{iq.y}|k> = (2pi)^3 delta(k'-k-q),  <k+q|V1|k> = -e a.(2k+q) = -2e a.k.

### 3.1 Electric, and the Born subtraction
E(0) = -grad A_0 => E^2 contains -2 (q.q') phi1 phi2, so -2 pi alpha_E E^2 contains 4 pi alpha_E (q.q') phi1 phi2.
Only T3 contributes:  D contains 2 e^2 phi1 phi2 Sigma(q+q'),

    Sigma(Q) = int d^3k/(2pi)^3  (k+Q).k / [((k+Q)^2+m^2)(k^2+m^2)],

whose (q.q') coefficient is 4 c with Sigma = Sigma(0) + c Q^2 + ...
**Born subtraction.** Diagrams with a Coulomb photon on the nucleon line (on an external leg: the nucleon pole, with
the singular static propagator 1/(v.p) at zero photon energy; or on the internal nucleon line between the two pi N
vertices) carry no dependence on that photon's 3-momentum, because the static propagator i/(v.l) is independent of l.
The loop in such a diagram depends on the other photon's momentum only. They contribute to the phi1 phi2 q^2,
phi1 phi2 q'^2 and q-independent terms (charge renormalization / gauge pieces) but never to (q.q') phi1 phi2.
So: the polarizability is read off from the (q.q') term, which is Born-free by construction. For real photons in the
radiation gauge (eps_0 = 0) all nucleon-line couplings (v.eps) vanish identically at this order, the nucleon pole
terms are zero, and the Thomson term -Z^2 e^2/m_N is O(1/m_N) and drops out; nothing else to subtract.

Closed form (n = d-1 spatial dimensions, dim reg): Feynman parameter x, Delta = m^2 + x(1-x) Q^2,
Sigma = int_0^1 dx [ A_n Delta^{n/2-1} - x(1-x) Q^2 B_n Delta^{n/2-2} ],
A_n = (n/2) Gamma(1-n/2)/(4pi)^{n/2}, B_n = Gamma(2-n/2)/(4pi)^{n/2}, hence

    c = -(1/6)(n/2+1) Gamma(2-n/2) m^{n-4}/(4pi)^{n/2}  ->(n=3)  -5/(96 pi m).

D contains d_E (q.q') phi1 phi2 with d_E = 4 c e^2 = -5 e^2/(24 pi m). Matching
-(g^2/4f^2) d_E = 4 pi alpha_E  =>  alpha_E = -g^2 d_E/(16 pi f^2) = 5 e^2 g^2/(384 pi^2 f^2 m).

### 3.2 Magnetic
B = curl A => B^2 contains -2 (q x a).(q' x a') = -2[(q.q')(a.a') - (q.a')(q'.a)];
-2 pi beta_M B^2 contains 4 pi beta_M [(q.q')(a.a') - (q.a')(q'.a)]. Writing D contains d_B[(q.q')(a.a') - (q.a')(q'.a)]:
beta_M = -g^2 d_B/(16 pi f^2).
* T1: independent of q, q' -> no contribution.
* T2: KR vertex at the origin carries no momentum; the loop depends on one photon's momentum only -> only
  (a.a') q^2, (a.a') q'^2 type terms, no (q,q') cross term -> no contribution.
* T3: -2 e^2 (a.a') Sigma(q+q') -> (q.q')(a.a') coefficient -4 c e^2 = +5 e^2/(24 pi m).
* T4: 4 e^2 int (k+Q).k [a.(k+q')][a'.k] G0(k+Q) G0(k+q') G0(k) + (q,a <-> q',a').
  Expanding to O(q q'), isotropic angular averages in n dims
  <k_1^a k_2^b k_3^c> = (a-1)!!(b-1)!!(c-1)!! k^{a+b+c} / [n(n+2)...(n+a+b+c-2)],
  and the radial dim-reg formula
  int d^nk/(2pi)^n k^{2j}/(k^2+m^2)^N = Gamma(j+n/2)Gamma(N-j-n/2)/(Gamma(n/2)Gamma(N)) m^{n+2j-2N}/(4pi)^{n/2},
  give (q.q')(a.a') coefficient -11 e^2/(48 pi m), (q.a')(q'.a) coefficient +e^2/(48 pi m).
* Sum: (q.q')(a.a'): -11/48 + 10/48 = -1/48;  (q.a')(q'.a): +1/48 (only T4). The two coefficients are equal and
  opposite, as gauge invariance requires (built-in check). d_B = -e^2/(48 pi m), beta_M = e^2 g^2/(768 pi^2 f^2 m).
* Which diagrams: alpha_E <- seagull (T3) only in this gauge (A_0 single insertions vanish at nu = 0; KR needs a
  vector potential). beta_M <- diamagnetic seagull (T3, negative) + paramagnetic double insertion (T4, positive),
  the paramagnetic one wins by 11:10.  In the radiation gauge with real photons (route C) the KR diagrams do the work.

## 4. Route B (independent, position space, uniform-field gauges; computed in __main__)
Uniform fields with potentials vanishing at the nucleon: A_0 = -E.y, A = (1/2) B x y. Then A(0) = 0 so KR vanishes
and no nucleon-line coupling exists at all (no Born term to subtract). chi_i(y) = d_{x_i} G0(x-y)|_{x=0} = yhat_i g(r),
g = (1+mr)e^{-mr}/(4 pi r^2), G0(r) = e^{-mr}/(4 pi r).
* E: D_E = e^2 int d^3y (E.y)^2 g^2 = (e^2 E^2/3) I,  I = int d^3y r^2 g^2 = (1/(4 pi m)) int_0^inf (1+x)^2 e^{-2x} dx = 5/(16 pi m).
* B: V1 = -e B.L, V2 = e^2 (B x y)^2/4.
  diamagnetic: -(e^2/4) int (B^2 r^2 - (B.y)^2) g^2 = -(e^2 B^2/6) I;
  paramagnetic: e^2 sum_i <chi_i|(B.L) G0 (B.L)|chi_i> = e^2 Tr_{l=1}[(B.L)^2] K1 = 2 e^2 B^2 K1,
  K1 = <chi_z|G0|chi_z> = int d^3p/(2pi)^3 p_z^2/(p^2+m^2)^3 = 1/(32 pi m).
  D_B = e^2 B^2 (-5/96 + 6/96)/(pi m) = e^2 B^2/(96 pi m).
* Delta E = -(g^2/4f^2) D = -2 pi(alpha E^2 + beta B^2) => alpha_E = g^2 (e^2/3) I/(8 pi f^2), beta_M = g^2 e^2/(768 pi^2 f^2 m):
  same as route A. (Different gauge, different diagram bookkeeping, position-space radial integrals.)

## 5. Route C (independent, real photons): unitarity + Baldin sum rule for alpha_E + beta_M
Tree-level LO static photoproduction gamma p -> pi^+ n (radiation gauge eps_0 = 0, no nucleon-photon coupling):
i M = (e g sqrt2 / 2f) [ sigma.eps + 2 (q.eps) sigma.(q-k) / ((q-k)^2 - m^2) ],  (q-k)^2 - m^2 = -2 w (w - |q| cos th)
(Kroll-Ruderman + pion pole; pi^0 production vanishes at this order; gamma n -> pi^- p is identical).
Spin and polarization average: |M|^2 = (e^2 g^2/2f^2)[1 + 2C X + C^2 X |q-k|^2], C = -1/(w(w-|q|cos th)), X = |q|^2 sin^2 th/2.
dsigma/dOmega = (|q|/w)|M|^2/(16 pi^2) (static target, Fermi golden rule).
Forward amplitude f(w) = f(0) + (alpha_E+beta_M) w^2 + ..., normalized as dsigma/dOmega = |f|^2 (from H_eff:
f = -2w <f|H_eff|i> V/(4 pi)), Im f = w sigma/(4 pi), crossing-even, f - f(0) grows at most like w at this order, so the
once-subtracted dispersion relation gives the Baldin sum rule
    alpha_E + beta_M = (1/2 pi^2) int_m^inf sigma_tot(w) / w^2 dw,
evaluated numerically: equals 11 e^2 g^2/(768 pi^2 f^2 m) = (11/10) alpha_E to quadrature precision.

## 6. Finiteness, divergences
All integrals are of the form int d^{d-1}k (after the static/energy integration), d-1 = 3; the dim-reg Gamma functions
at n = 3 have half-integer arguments, no poles. The individual zero-field self-energy (Sigma(0) ~ m^3) is linearly
divergent by power counting but has no pole in dim reg; the O(q q') coefficients are UV convergent (integrand ~ k^-4,
k^-6 in 3 dims) and IR finite because m > 0. The 1/m behaviour (alpha_E ~ 1/m_pi, chirally singular) is the hallmark of
a non-analytic loop effect: no counterterm at O(p^3) can produce it (the first gamma gamma N N polarizability
counterterms are O(p^4), analytic). Hence the result is finite and unambiguous.

## 7. Could not derive / not done
Nothing essential. I did not do the full real-photon Compton loop at arbitrary angle (which would give alpha - beta
separately with real photons); routes A+B separate alpha and beta with static fields, route C checks alpha + beta with
real photons and KR vertices.
