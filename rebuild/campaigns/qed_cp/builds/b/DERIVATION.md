# qed_cp-b derivation (Casimir-Polder by 4th-order Rayleigh-Schrodinger PT; SPEC sections 1-2)

Units hbar=c=1, Gaussian. a := w0.

## 0. Atom
Per Cartesian direction the only excited state coupled is |e_i>, <e_i|d_i|0> = d. Second-order energy
of a static field: alpha_ii = 2 sum_n |<n|d_i|0>|^2 w_n0/(w_n0^2-w^2) = 2 d^2 a/(a^2-w^2) = alpha0 a^2/(a^2-w^2),
alpha0 = 2d^2/a  =>  d^4 = alpha0^2 a^2/4.   (SPEC section 1, checked.)

## 1. Which 4th-order terms depend on r
H_int = -d_A.E(x_A) - d_B.E(x_B).  Atoms start and end in |0>, so each atom has an even number of vertices.
r dependence needs a photon to join A and B. Terms with 4 vertices on one atom, or with a photon starting
and ending on the same atom, carry no phase e^{ik.r} (they are r independent; the -E2*sum|V|^2/D^2 term of
RSPT is built only from such pieces and cancels their unlinked parts). So: 2 vertices on A, 2 on B, two
photons (modes k,q), each photon created at an earlier slot and annihilated at a later slot, each
joining an A vertex to a B vertex.
Enumeration of 4 time slots: choose A slots (6 ways), pair the slots into two photons (3 pairings) keeping
the pairings that join A to B: 12 time-ordered diagrams (done by code, verify count = 12).
Vertex factors: emission -d.(-i sqrt(2 pi k/V) eps* e^{-ik.x}) , absorption -d.(i sqrt(..) eps e^{ik.x});
a created-then-annihilated photon gives (+i)(-i)=+1 times (2 pi k/V) eps_i eps*_m e^{ik.r}. Atom line (0->e_i ->0): d^2 delta_ij.
Energy denominators: E4 = sum V V V V /((E0-E1)(E0-E2)(E0-E3)) = - sum 1/(D1 D2 D3), with D = energy of the
intermediate state (excited atoms a each + photons present) > 0 : no principal values and no cut-offs
arise in the time-ordered form.
Index structure of every diagram: delta_ij delta_mn P_im(k) P_jn(q) = Tr[P(k)P(q)], P = delta - khat khat (polarisation sum).
Angle averages: <P_ij e^{ik.r}> = A(x) rhat rhat + B(x)(delta - rhat rhat), x=kr, with
<khat_i khat_j e^{ik.r}> = -(1/k^2) d_i d_j j0(kr) => A = 2 j1(x)/x = 2(sin x - x cos x)/x^3,
B = j0 - j1/x = ((x^2-1) sin x + x cos x)/x^3.  Tr[T(k)T(q)] = A A' + 2 B B'.
Mode sums: sum_k (2 pi k/V) -> (1/pi) int dk k^3 <.>_angle. Hence

 U = -(d^4/pi^2) int_0^inf int_0^inf dk dq k^3 q^3 [A(kr)A(qr) + 2B(kr)B(qr)] S(k,q),
 S = sum_diagrams 1/(D1D2D3)  (sympy, then symmetric under k<->q after integration):
 S = 2k/(a(a+k)^2(a+q)) + 6/((a+k)^2(a+q)) + 4a/((a+k)^2(a+q)(k+q)).

## 2. Evaluation (no cut-off; Abel damping e^{-eps(k+q)}, eps->0, which is how the oscillatory integral is defined)
1/(k+q) = int_0^inf ds e^{-(k+q)s}. Then everything factorises into one-photon integrals
M_X[f](s) = int dk k^3 X(kr) f(k) e^{-ks}, X=A,B, with
k^3 A = (2/r^3) Im[(1 - i k r) e^{ikr}],  k^3 B = (1/r^3) Im[(k^2 r^2 - 1 + i k r) e^{ikr}],
so with w = s - i r the needed integrals are H(m,n;w) = int k^m (a+k)^-n e^{-kw} dk, built from
L_1 = e^{aw} E_1(aw), L_{p+1} = (a^-p - w L_p)/p and elementary pieces. Then
 U = -(d^4/pi^2) sum_X w_X { M_X[f1](0) M_X[g1](0) + M_X[f2](0) M_X[g2](0) + int_0^inf ds M_X[f4](s) M_X[g4](s) },
 w_A=1, w_B=2, f1=2k/(a(a+k)^2), g1=1/(a+k), f2=6/(a+k)^2, g2=g1, f4=4a/(a+k)^2, g4=g1.
Numerics: mpmath, 40+ digits (the integrand has 1/r^3 cancellations), tanh-sinh quadrature in s,
refinement shown in __main__.

## 3. Limits (derived from the same double integral)
Near (r a << 1): relevant k,q ~ 1/r >> a, S -> 2/(a k q), A,B functions of x=kr:
 U -> -(2 d^4/(pi^2 a r^6)) [ (int x^2 A)^2 + 2 (int x^2 B)^2 ], Abel integrals: int x^2 A = pi, int x^2 B = -pi/2
 => U = -3 d^4/(a r^6) = -(3/4) a alpha0^2/r^6, D = 3/4 (computed by code with sympy, not typed).
Far (r a >> 1): k,q << a, S -> 4/(a^2 (k+q)):
 U -> -(alpha0^2/pi^2) int int dk dq k^3 q^3 F/(k+q) = -C alpha0^2/r^7,
 C = (1/pi^2) int_0^inf ds [G_A(s)^2 + 2 G_B(s)^2], G_X(s) = int x^3 X(x) e^{-xs} dx (Laplace transforms, exact via sympy).

## 4. Independent second route
(i) Limits above from the closed integrals vs the full cp_energy at r a=1e-3 and 1e4.
(ii) A direct 2D check of the double integral at moderate r with a different numerical method
(2D brute-force quadrature with damping, eps->0 extrapolation) -- see __main__. Two damping shapes were run:
exponential e^{-eps(k+q)} (linear-in-eps Richardson) and Gaussian e^{-eps^2(k^2+q^2)} (quadratic Richardson),
eps = 0.1, 0.05, 0.025, at r a = 0.5, 1, 3. Results (U/(alpha0^2 w0^7)):
  r a = 1:   exp -0.65153, gauss -0.651267, main route -0.651266
  r a = 3:   exp -5.987e-4, gauss -5.963978e-4, main route -5.963977e-4
  r a = 0.5: exp -45.73, gauss -45.62, main route -45.68  (grid coarse and eps too large here; ~0.1-0.2% scatter)
The Gaussian shape converges to the main route to ~1e-6 relative at r a = 1, 3; the exponential shape agrees to
0.05-0.4% (its eps->0 convergence is slow, only linear). This supports, but does not prove, that the eps->0 limit
is the same for these two smooth dampings. Not tested: other shapes, other separations, rigorous convergence proof.
Nothing left underived except the Abel/damping prescription for the oscillatory integrals (taken as the
definition of the conditionally convergent integral; checked as above).

## 5. Map from the 12 diagrams to the code (_u) and independent check
sympy sums the 12 enumerated diagrams to S (section 1). By partial fractions in the code's decomposition
 S = f1(k) g1(q) + f2(k) g2(q) + f4(k) g4(q)/(k+q),  f1 = 2k/(a(a+k)^2), f2 = 6/(a+k)^2, f4 = 4a/(a+k)^2, g = 1/(a+q)
(valid as integrand because F is symmetric in k<->q). In _u: `sep` = f1 g1 + f2 g2 terms evaluated at s=0
(M[1,2]*M[0,1]*2/a and 6*M[0,2]*M[0,1]); `integrand` = f4 g4 with e^{-(k+q)s} (4a*M[0,2](s)*M[0,1](s)), integrated over s.
Check in __main__: `_S_independent` enumerates all strings of 4 vertices (atom, photon label, create/annihilate) with
explicit photon occupation / atom excitation tracking (a different enumeration from the slot/pairing one), obtains
24 = 2 x 12 labelled sequences, and compares its sum/2 with the symmetrised f1g1+f2g2+f4g4/(k+q) used by _u at five fixed
(k,q) points: max relative difference 3e-16.

## 6. Validity range of cp_energy
Checked for 1e-4 <= r w0 <= 1e8: -U r^7/alpha0^2 / far_coefficient - 1 = -5.6e-8 (1e4), -5.6e-12 (1e6), -4e-16 (1e8)
(the residual is the physical retardation correction, falling like 1/(r w0)^2); -U r^6/(w0 alpha0^2)/near_coefficient - 1 = -3.3e-7 (1e-3), -3.3e-9 (1e-4). Not checked outside this range. The mpmath working precision is 45 digits for
r w0 <= 1e4 and grows by 6 digits per decade above that, because each photon integral carries 1/r^3 cancellations
(with fixed 45 digits the error was ~1e-8 at 1e6 and ~3e-6 at 1e8). Runtime grows with the precision (about 5-20 s at 1e6-1e8).

