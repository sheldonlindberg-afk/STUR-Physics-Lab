# DERIVATION (build l3): fermionic one-loop transverse self-energies of gamma, Z, W (Feynman gauge, NDR, MS-bar)

## 0. Postulates used (SPEC §1–§2)
* L = psibar i Dslash psi with D = d - i g W^a T^a - i g' Y B, so each chiral fermion couples as
  L_int = psibar gamma^mu [g W^a_mu T^a + g' Y B_mu] psi  -> vertex  +i gamma^mu (coupling).
* Neutral fields: Z = c W3 - s B, A = s W3 + c B  =>  W3 = c Z + s A, B = -s Z + c A.
  c = MW/MZ, s^2 = 1 - c^2, e = g s = g' c (so g'/g = s/c), alpha = e^2/4pi.
* Definition (SPEC §2): the 2-point vertex is -i g^{mu nu}[(k^2-M^2) delta + Sigma_T]; the sum of the one-loop
  1PI fermion-bubble diagrams (Feynman-rule amplitude) A^{mu nu} therefore equals  -i g^{mu nu} Sigma_T  (transverse
  = g^{mu nu} coefficient; k^mu k^nu terms dropped).

## 1. Couplings (derived)
Photon: g s T3 + g' c Y = e (T3+Y) = e Q for both chiralities:  g_L^A = g_R^A = eQ.
Z: g c T3 - g' s Y = (e/(s c)) (c^2 T3 - s^2 Y) = (e/(s c)) (T3 - s^2 Q).  Left (T3 = I3): g_L^Z = e (I3 - s^2 Q)/(s c);
right singlet (T3 = 0): g_R^Z = - e s Q / c.   (neutrino m=0,Q=0,I3=1/2: g_L=e/(2sc), g_R=0 automatically.)
Write g_R P_R + g_L P_L = v - a gamma5 :   v = (g_R+g_L)/2 ,  a = (g_L - g_R)/2.
 -> photon: v_A = eQ, a_A = 0;   Z: v_Z = e (I3 - 2 s^2 Q)/(2 s c), a_Z = e I3/(2 s c).
W: L = (g/sqrt2) (ubar gamma^mu P_L d W^+_mu + h.c.), from g W^a T^a = g/sqrt2 (W^+ T^+ + W^- T^-) + g W3 T3, W^± = (W1 ∓ i W2)/sqrt2
 => v = a = g/(2 sqrt2) (pure left), g^2 = e^2/s^2.

## 2. The loop
Vertices  i gamma^mu (v - a g5), (v' - a' g5); masses m1 (propagator momentum p), m2 (momentum p+k); fermion loop gives -1:
 A^{mu nu} = - Int d^dp/(2pi)^d Tr[ gamma^mu (v-a g5)(pslash+m1) gamma^nu (v'-a' g5)(pslash+kslash+m2) ] / (D1 D2)   (i^4 = 1).
Chirality algebra with anticommuting gamma5 (NDR): terms with an odd number of masses have an odd number of gammas -> 0;
 (v - a g5) pslash gamma^nu (v' - a' g5) = pslash gamma^nu (v+a g5)... => coefficient (v v' + a a') for the p-p' trace (the g5 piece
 gives eps^{mu nu a b} p_a k_b -> 0 after integration, no g^{mu nu}); mass term m1 m2 Tr[gamma^mu gamma^nu (v+a g5)(v'-a' g5)] = 4 m1 m2 (v v' - a a') g^{mu nu}.
Hence, with A = v v' + a a', B = v v' - a a':
 numerator (g^{mu nu} part) = A Tr[gamma^mu p gamma^nu p'] + 4 B m1 m2 g^{mu nu}, Tr[g^mu p g^nu p'] = 4(p^mu p'^nu + p^nu p'^mu - g^{mu nu} p.p').
Feynman parameter x on D2: l = p + x k, Delta(x) = (1-x) m1^2 + x m2^2 - x(1-x) k^2, p = l - x k, p' = l + (1-x) k.
g^{mu nu} part of the trace: 4[(2/d - 1) l^2 + x(1-x) k^2 ].  With (d-dim)
 Int l^2/(l^2-Delta)^2 = [d/(d-2)] Delta I0,  I0 = Int 1/(l^2-Delta)^2 = i/(4pi)^{d/2} Gamma(eps) Delta^{-eps},
 so (2/d - 1) * d/(d-2) = -1 EXACTLY: the O(eps) of the d-dependent coefficient multiplies the pole and cancels completely
 (no extra rational finite term). Result:
 g^{mu nu} coefficient of Int N/(D1 D2) = 4 Int dx I0(Delta) { A [x(1-x)k^2 - Delta] + B m1 m2 }.
 Then  -i Sigma = -(that)  =>
  Sigma_T = -(1/4pi^2) Int_0^1 dx P(x) [ ln(|Delta - i0|/mu^2) ]            (MS-bar: Delta_eps dropped, mu^{2 eps} in measure)
  P(x) = A [ 2x(1-x) k^2 - (1-x) m1^2 - x m2^2 ] + B m1 m2.
 Real part: ln|Delta|.  (Re ln(-|D|-i0) = ln|D|.)
Fermion sums: Sigma^{VV'} = sum_f N_C^f S(k^2; m,m; v_V v_V', a_V a_V') with equal masses (P = A(2x(1-x)k^2 - m^2) + B m^2),
 AA: v=v'=eQ, a=0 ; AZ: A = B = eQ v_Z ; ZZ: A = v_Z^2 + a_Z^2, B = v_Z^2 - a_Z^2.
W: Sigma_W = sum_doublets w S(k^2; m_u, m_d; A = g^2/4, B = 0).   (colour & CKM only via w.)

## 3. Closed form and checks
UV pole: Sigma_T has the pole -(1/4pi^2)(1/eps-ish) Int P dx; Int P dx = A[k^2/3 - (m1^2+m2^2)/2] + B m1 m2 is linear in k^2, so
 d Sigma/d ln mu^2 = (1/4pi^2) Int P dx  is linear in k^2 (blind check 4). The subtraction is the MS-bar pole.
Photon Ward: for AA, AZ: a_A = 0 and A = B = vv' => P = vv'[2x(1-x)k^2], at k^2=0 identically zero => Sigma^{AA}(0) = Sigma^{AZ}(0) = 0 exactly
 (the m^2 terms cancel between -A m^2 and +B m^2: gauge invariance), independent of mu.
QED limit: AA: Sigma = -(2 alpha/pi) Q^2 N k^2 Int x(1-x) ln(Delta/mu^2), equal to the standard Pi(k^2) with Sigma = -k^2 Pi (checked against the
 equivalent form -(alpha/4pi)(4/3)NQ^2[-(k^2+2m^2)B0(k^2)+2m^2 B0(0)+k^2/3]; large -k^2: -(alpha/3pi) NQ^2 k^2 (ln(-k^2/mu^2) - 5/3)).
Heavy fermion (k^2 << m^2): AA -> -(alpha/3pi) N Q^2 k^2 [ln(m^2/mu^2) - k^2/(5 m^2)]  (decoupling: finite, absorbed in alpha running).
Thresholds: Delta(x) = k^2 (x-r_-)(x-r_+): real roots in (0,1) iff k^2 > (m1+m2)^2; there Re ln = ln|k^2| + ln|x-r_-| + ln|x-r_+|
 (principal value; integrable log singularities). m=0 (neutrino, massless limit): Delta = u m2^2 ... all fine as roots at 0/1 (r=0 or 1 exactly).
 k^2 = 0, m1=m2=0: P ≡ 0 -> 0 (continuity: Sigma ~ k^2 ln k^2 -> 0).  Large mass hierarchy (m_t vs 0): Delta kept in the form (1-x)m1^2 + x m2^2 - x(1-x)k^2, no cancellations.

## 4. Numerics
Int_0^1 P(x) ln|Delta| dx by tanh-sinh (double-exponential) quadrature on sub-intervals split at the real roots of Delta (so every log singularity
is an end-point), each node carrying distances to both sub-interval ends so that x, 1-x, x-r_± are accurate even for m_e^2/k^2 ~ 1e-12 and
tiny roots. mu enters only through the exact polynomial integral Int P dx times ln(mu^2/MW^2): Sigma = -(1/4pi^2)[ Int P ln(|Delta|/MW^2) - ln(mu^2/MW^2) Int P ].
No global precision settings; pure math.

## 5. Independent second route (run under __main__)
(i) Analytic: Delta = k^2 (x-r1)(x-r2) with complex roots, Int_0^1 x^n ln(x-r) dx = [ (x^{n+1}-r^{n+1})/(n+1) ln(x-r) ]_0^1
 - (1/(n+1)) sum_{j=0}^n r^{n-j}/(j+1) (complex logs, real part), compared with the quadrature at k^2 below/above threshold, equal and unequal masses.
(ii) Dispersion relation (different method): Sigma(k^2) - Sigma(0) - k^2 Sigma'(0) = k^4/pi Int_{s_th}^inf ds ImSigma(s)/(s^2 (s - k^2)), with Im Sigma = (1/4pi) Int_{Delta<0} P dx
 (sign fixed by the QED check), done for the equal-mass top/bottom case for a negative k^2 where everything is real.
(iii) Heavy-mass decoupling, UV (mu-derivative), Ward identity printed.
Not derived / not needed: nothing outstanding; the O(eps) bookkeeping is exact as shown (coefficient identity), HV scheme not asked.
