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
Energy denominators: E4 = sum V V V /((E0-E1)(E0-E2)(E0-E3)) = - sum 1/(D1 D2 D3), with D = energy of the
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
(Gaussian-damped e^{-eps(k+q)} brute force quadrature, eps->0 extrapolation) -- see __main__.
Nothing left underived except: Abel (damping) prescription for the oscillatory k integrals (physical
finiteness; justified by the result being independent of eps-shape).
