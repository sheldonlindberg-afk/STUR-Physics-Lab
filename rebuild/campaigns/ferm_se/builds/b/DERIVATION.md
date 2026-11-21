# Derivation: fermionic gauge-boson self-energies (SPEC sections 1, 2)

## 1. Couplings (SPEC 1, D = d - i g W^a T^a - i g' Y B)
L = psi-bar i gamma.D psi gives +psi-bar gamma^mu (g W^a T^a + g' Y B) psi. With W3 = cZ + sA, B = -sZ + cA,
g s = g' c = e, Q = T3 + Y:
- A: e Q for both chiralities (aL = aR = eQ).
- Z: gL = (g/c)(T3 - s^2 Q), gR = -(g/c) s^2 Q  (neutrino: gR absent; Q=0 anyway).
- W+-: (g/sqrt2) gamma^mu P_L between doublet partners (W^+- = (W1 -+ iW2)/sqrt2).
e^2 = 4 pi alpha, s^2 = 1 - MW^2/MZ^2, g^2 = e^2/s^2, (g/c)^2 = e^2/(s^2 c^2).
Everything is quadratic in couplings, hence linear in alpha.

## 2. The bubble
Vertices i gamma^mu (aL PL + aR PR), i gamma^nu (bL PL + bR PR); loop fermion masses m1 (momentum q), m2 (q+k);
closed-loop sign -1; i^4 = 1. The 1PI amplitude equals -i g^{mu nu} Sigma_T (SPEC 2: D (-i Sigma) D = i Sigma/(k^2-M^2)^2 matches the expansion of the dressed propagator).
Numerator trace (gamma5 pieces are antisymmetric eps^{mu nu a b} q_a k_b -> vanish after integration; no gamma5 ambiguity in the g^{mu nu} part):
 N^{mu nu} = 2A [q^mu p^nu + q^nu p^mu - g^{mu nu} q.p] + 2B m1 m2 g^{mu nu},  p = q+k,
 A = aL bL + aR bR,  B = aL bR + aR bL.
Feynman parameter x (weight of the m2 propagator), q = l - x k, Delta = x m2^2 + (1-x) m1^2 - x(1-x)k^2.
g^{mu nu} part: 2A[(2/d - 1) l^2 + x(1-x)k^2] + 2B m1 m2.  Using
 int l^2/(l^2-Delta)^2 = (d/(d-2)) Delta I0,  I0 = i/(16 pi^2) (Delta_eps - ln(Delta/mu^2)) (+O(eps)),
(2/d - 1) l^2 -> -Delta I0 EXACTLY in d dimensions: no O(eps)*pole leftover (finite rational terms vanish; check: massless QED gives the known 5/3).
Result (MS-bar: drop Delta_eps = 1/eps - gamma_E + ln4pi):
 Sigma_T = (N/16 pi^2) int_0^1 dx P(x) [ -ln(Delta/mu^2) ],
 P(x) = 2A[2x(1-x)k^2 - x m2^2 - (1-x) m1^2] + 2B m1 m2.
Real part above threshold: ln|Delta|. (N = NC for neutral; for W the weight w, A = g^2/2, B = 0.)
Couplings: AA: A = B = 2e^2Q^2.  AZ: A = B = eQ(gL+gR).  ZZ: A = gL^2+gR^2, B = 2 gL gR.  W: A = g^2/2, B = 0, m1,m2 = m_up, m_down.

## 3. Closed form
Delta = k^2 (x-r1)(x-r2). int_0^1 x^n ln|Delta/mu^2| = ln|k^2/mu^2|/(n+1) + sum_r Re G_n(r),
G_n(r) = 1/(n+1) [ ln(1-r) - sum_{j=0}^n r^{n-j}/(j+1) - r^{n+1}(ln(1-r) - ln(-r)) ]  (|.| logs for real r; 0*log0 = 0).
Polynomial P has degree 2, so n = 0,1,2. k^2 = 0: Delta linear (m1 != m2) or constant; handled separately in closed form
(m1=m2=m: ln(m^2/mu^2); m1 != m2: int x^n ln(m1^2 + (m2^2-m1^2)x) elementary; m1=m2=0 and k^2=0: P=0 so Sigma=0).
Evaluated in mpmath with a local workdps (cancellation of r^{n+1} terms for tiny k^2); global precision untouched.

## 4. Second route (run under __main__)
(a) direct mpmath quadrature of int P(x)(-ln|Delta|) splitting at real roots in (0,1);
(b) known equal-mass form: Sigma_AA = -(alpha/4pi)(4/3) N Q^2 [ -(k^2+2m^2)B0(k^2) + 2 m^2 B0(0) + k^2/3 ], B0 = -ln... + 2 - ...
    (the B0 is evaluated by quadrature of -ln|Delta|; this is a differently arranged integrand: the integration by parts equivalence is a check);
(c) UV pole coefficient: coefficient of Delta_eps = (N/16pi^2) int P = proportional to k^2 plus constant; the mu-derivative d Sigma/d ln mu^2 = (N/16pi^2) int P, checked against finite difference;
    for AA: = (alpha/4pi)(4/3) N Q^2 k^2;
(d) heavy-fermion limit k^2 << m^2: Sigma_AA -> (alpha/3pi) N Q^2 k^2 ln(mu^2/m^2) (decoupling in MS-bar).
(e) photon Ward identity Sigma_AA(0)=Sigma_AZ(0)=0 (exact: A=B at k=0 integrand vanishes).
Not derivable/unresolved: nothing.
