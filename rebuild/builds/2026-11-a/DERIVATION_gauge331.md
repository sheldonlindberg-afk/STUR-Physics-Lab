# DERIVATION: gauge331 (SPEC.md sections 0 and 2)

Postulates used (all from SPEC.md section 2 unless stated): gauge group SU(3)_L x U(1)_X with
couplings g, g_X; t_a = lambda_a/2 with lambda_8 = diag(1,1,-2)/sqrt3; Q = T3 + beta T8 + X with
beta = -1/sqrt3 or +1/sqrt3; antitriplet generators -t_a^*; the three scalar triplets and their
X charges; "a vev may sit only in a Q = 0 component", the w / v1 / v2 assignment rule; the
fermion content (N_g = N_c, n_A = (1+N_c)/2 antitriplet quark families, lepton triplets);
Q_u - Q_d = 1, Q_e = -1, and [SU(3)_L]^2 U(1)_X anomaly cancellation. Conventions: basis
(W^1..W^8, B_X), <phi>_k = vev/sqrt2, and the tree relation for M_Z (SPEC.md section 2).
contract.py fixes M2_AB = g_A g_B sum_phi <phi>^dag {t_A, t_B} <phi>.

Index convention: A = 1..8 are SU(3)_L (g_A = g, t_A = lambda_A/2), A = 9 is U(1)_X
(g_9 = g_X, t_9 = X * 1 acting on a field of charge X). In code these are indices 0..8.

---

## 0. The exact rational number b = beta/(2 sqrt3)

beta T8 = beta diag(1,1,-2)/(2 sqrt3) = b diag(1,1,-2), with b = beta/(2 sqrt3).
For beta = s k/sqrt(r) (the variant string "s k/sqrt r", here k = 1, r = 3, s = +-1),

    b = s k / (2 sqrt(3 r)),

which is rational iff 3r is a perfect square; for r = 3, sqrt(3r) = 3 and b = s/6. The code parses
s, k, r from the variant string, checks that 3r is a perfect square (math.isqrt), and builds b as a
Fraction. Nothing is chosen by hand; the float beta = s k / sqrt(r) is used only in the mass matrix.

---

## 1. `triplet_charges(X, variant, anti=False)`

Triplet: Q = T3 + beta T8 + X 1 with T3 = diag(1/2, -1/2, 0):

    Q_triplet = (1/2 + b + X,  -1/2 + b + X,  -2b + X).

Antitriplet: generators -t_a^*. T3 and T8 are real diagonal, so they flip sign; X is the U(1)
charge of the field itself (not conjugated: the X given is the antitriplet's own charge):

    Q_anti = (-1/2 - b + X,  1/2 - b + X,  2b + X).

Closed form above, exact Fractions.

**Second route.** Q - X 1 is traceless (T3, T8 traceless) so sum Q = 3X; the T3 spacing gives
Q_1 - Q_2 = +1 (triplet) and -1 (antitriplet). Also Q_anti(X) = -Q_triplet(-X) componentwise
(conjugate representation has opposite charges). Self-check in `__main__`.

### Neutral components of the scalar triplets (derived, not assumed)

b = -1/6 (beta = -1/sqrt3), X = (-1/3, 2/3, -1/3):
  phi1: (0, -1, 0)  neutral {1, 3};  phi2: (1, 0, 1)  neutral {2};  phi3: (0, -1, 0)  neutral {1, 3}.
b = +1/6 (beta = +1/sqrt3), X = (1/3, 1/3, -2/3):
  phi1: (1, 0, 0)  neutral {2, 3};   phi2: (1, 0, 0)  neutral {2, 3};  phi3: (0, -1, -1) neutral {1}.

(The table is what the code computes; it is listed here for the reader.)

Rule (SPEC): the first triplet with component 3 neutral takes w there (phi1 in both variants).
Every other triplet takes "its remaining neutral component", read as: its neutral components
other than component 3 (the w direction), which in both variants is exactly one; they take v1
then v2 in triplet order. Result: beta = -1/sqrt3: w in phi1_3, v1 in phi2_2, v2 in phi3_1;
beta = +1/sqrt3: w in phi1_3, v1 in phi2_2, v2 in phi3_1. The code raises if the rule ever does
not single out exactly one component (see QUESTIONS.md).

---

## 2. `quark_charges(Nc)`

Unknowns: Q_u, Q_d with Q_d = Q_u - 1 (SU(2) doublet). For a variant b:

- Lepton triplet: Q_e = -1/2 + b + X_L = -1, so X_L = -1/2 - b. (b = -1/6: X_L = -1/3;
  b = +1/6: X_L = -2/3, agreeing with SPEC's listed values; the code asserts this.)
- Quark triplet, first two components (Q_u, Q_d): 1/2 + b + X_t = Q_u, so X_t = Q_u - 1/2 - b.
- Quark antitriplet, first two components (Q_d, Q_u) (the only order compatible with the
  antitriplet spacing Q_2 - Q_1 = +1): -1/2 - b + X_a = Q_d, so X_a = X_t + 2b.
- [SU(3)_L]^2 U(1)_X: each triplet or antitriplet contributes T(3) X = X/2 (the Dynkin index of 3
  and 3bar is the same), weighted by colour multiplicity:

      A = N_g X_L + N_c [ (N_g - n_A) X_t + n_A X_a ] = 0,   N_g = N_c, n_A = (1 + N_c)/2.

Substituting: A/N_c = X_L + N_c X_t + 2 b n_A = -1/2 - b + N_c Q_u - N_c/2 - N_c b + b(1 + N_c)
= N_c Q_u - (N_c + 1)/2. The b dependence cancels identically, so

    Q_u = (N_c + 1)/(2 N_c),   Q_d = (1 - N_c)/(2 N_c).      (N_c = 3: 2/3, -1/3)

**Implementation.** A(Q_u) is affine in Q_u. The code builds A exactly from the content above
(with X_L derived from Q_e = -1), takes its exact slope with toolkit.exact_derivative (dual
numbers over Fraction), and solves Q_u = Q0 - A(Q0)/A'(Q0) exactly (Newton on an affine function is
exact in one step). It does this for both variants and asserts the same answer (b-independence).
Odd N_c is required (n_A must be an integer).

**Second route.** The N_c-quark proton ((N_c+1)/2 u + (N_c-1)/2 d) has charge
[(N_c+1)^2 - (N_c-1)^2]/(4 N_c) = 1 = -Q_e, i.e. q_p + q_e = 0. Checked in `__main__` for odd N_c.

---

## 3. `doublet_charge_pairs(Nc, variant)`

The set of frozenset({Q_1, Q_2}) over all fermion multiplets: lepton triplets (X_L),
quark triplets (X_t), quark antitriplets (X_a = X_t + 2b), with Q_u from section 2, charges from
section 1. Result {frozenset{0, -1}, frozenset{Q_u, Q_d}}; leptons: Q_nu = 1/2 + b + X_L = 0.
Antitriplets are present only if n_A >= 1 and triplets only if N_g - n_A >= 1 (both hold for
N_c >= 3; for N_c = 1 there are no quark triplets).

**Second route.** Both quark multiplet kinds give the same pair, which the code asserts
before taking the set.

---

## 4. `mass_matrix(variant, g, gX, w, v1, v2)`

Kinetic term (D phi)^dag (D phi), D = d - i sum_A g_A V^A t_A. Inserting <phi>:
<phi>^dag (sum g_A V^A t_A)^2 <phi> = (1/2) sum_AB V^A V^B g_A g_B <phi>^dag {t_A, t_B} <phi>,
which equals (1/2) M2_AB V^A V^B with

    M2_AB = g_A g_B sum_phi <phi>^dag {t_A, t_B} <phi>,  t_9 = X_phi 1,   <phi>_k = vev/sqrt2 (k from section 1).

Computed with explicit Gell-Mann matrices (complex arithmetic, real part; the imaginary part
vanishes because the matrix is hermitian-symmetric and <phi> is real). Each <phi> has one nonzero
real component k, so <phi>^dag {t_A,t_B} <phi> = vev^2 Re (t_A t_B)_kk.

Checks/closed forms. W^1 W^1 entry: (lambda_1^2)_{kk}/4 x 2 x vev^2/2 = vev^2/4 for k = 1, 2, 0 for
k = 3, so M2_11 = M2_22 = g^2 (v1^2 + v2^2)/4 = M_W^2. Block structure: for diagonal t_A (A = 3, 8, 9)
and off-diagonal t_B, (t_A t_B)_kk = t_A,kk t_B,kk = 0, so the neutral block (W^3, W^8, B) decouples.

## 5. `photon_direction`, `inv_e2`

The coupling of the direction n (V^A = n_A A) to matter is sum_A g_A n_A t_A. Requiring it to be
e Q = e (T3 + beta T8 + X) gives

    n = (0, 0, 1/g, 0, 0, 0, 0, beta/g, 1/g_X)  (times e).

**Why M n = 0 for any vevs that respect Q.** (M n)_A = g_A sum_phi <phi>^dag {t_A, Q} <phi>
= g_A sum_phi [ <phi>^dag t_A (Q <phi>) + (Q <phi>)^dag t_A <phi> ] = 0, since Q <phi> = 0 when
every vev sits in a Q = 0 component. This holds for any w, v1, v2 and any g, g_X.

**1/e^2.** With V = n_hat A canonically normalized, the coupling is Q/|n| per unit e, so e = 1/|n|:

    1/e^2 = |n|^2 = (1 + beta^2)/g^2 + 1/g_X^2.

**Second route.** (a) Evaluate |M n| numerically from `mass_matrix` (self-check). (b) Matching
through the SM: 1/e^2 = 1/g^2 + 1/g_Y^2 with 1/g_Y^2 = beta^2/g^2 + 1/g_X^2 (section 7).

## 6. Massless states at v1 = v2 = 0 (step 1: 3-3-1 -> SM)

Only phi1 = (0, 0, w/sqrt2), charge X_1. M2_AB = w^2 g_A g_B Re(t_A t_B)_33. Generators with
t_A e_3 = 0: t_1, t_2, t_3 (upper 2x2 block) and the combination of t_8 and X that vanishes on
component 3, i.e. Y = beta T8 + X (it equals Q - T3 on component 3, = 0 since that component is
neutral). Also t_4..t_7 move e_3, and their M2 block is (g^2 w^2/4) 1_4 (nonzero). In the neutral
block, M = w^2 u u^T with u = (0, -g/sqrt3, g_X X_1) on (W3, W8, B) (t_8,33 = -1/sqrt3). Rank 1.
Therefore exactly 4 massless: W^1, W^2, and the 2D kernel of u u^T in the neutral block
(the SU(2)_L x U(1)_Y bosons). Massive: W^4..W^7 (four states, w^2 g^2/4) and Z' with

    M_Z'^2(0) = w^2 |u|^2 = w^2 (g^2/3 + g_X^2 X_1^2).

With X_1 = -1/3 (beta < 0) or +1/3 (beta > 0), X_1^2 = beta^2/3, so M_Z'^2 = (g^2 + beta^2 g_X^2) w^2/3.

## 7. `neutral_masses` and the leading order in v/w

The neutral block N (3x3, indices W3, W8, B) has exact zero mode n (section 5), so
det(N - lambda) = -lambda (lambda^2 - tr N lambda + c2), c2 = sum of principal 2x2 minors.
The export: eigenvalues of N by toolkit.eigvalsh, drop the one of smallest modulus (the photon),
return the other two ascending.

**Leading order.** Write N = w^2 u u^T + N_v (N_v from v1, v2). Let z be the unit vector orthogonal
to both n and u. (n and u are orthogonal: n . u = (beta/g)(-g/sqrt3) + (1/g_X)(g_X X_1)
= -beta/sqrt3 + X_1 = 0 in both variants: beta = -1/sqrt3, X_1 = -1/3 -> 1/3 - 1/3; beta = +1/sqrt3,
X_1 = 1/3 -> -1/3 + 1/3. This is just Q = 0 on phi1's component 3.) For z ⊥ u the
generator G(z) = sum g_A z_A t_A has G_33 = z . u = 0 on phi1, so G(z) lies in span{T3, Y}, Y = beta T8
+ X. Hence z^T N z = z^T N_v z is the SM tree Z mass:

    M_Z0^2 = (g^2 + g_Y^2) (v1^2 + v2^2)/4,   1/g_Y^2 = beta^2/g^2 + 1/g_X^2

(in the (W3, W8, B) plane orthogonal to u, the Y gauge boson is B_Y with coupling g_Y fixed by
the normalization of the combination, which is the same matching that gives 1/e^2 = 1/g^2 + 1/g_Y^2).
Second-order perturbation in the 2x2 (z, u_hat) block:

    M_Z^2 = M_Z0^2 - (z^T N_v u_hat)^2 / M_Z'^2 + ...,   M_Z'^2 = w^2 |u|^2 + O(v^2).

Since z^T N_v u_hat = O(g^2 v^2), the relative corrections to both masses are O(v^2/w^2).

**Second routes.** (a) Closed form from the characteristic polynomial,
lambda_+- = [tr N +- sqrt(tr^2 - 4 c2)]/2 with the small root as 2 c2/(tr N + sqrt(...)) to avoid
cancellation; compared with eigvalsh in `__main__`. (b) Leading-order formulas above.

## 8. rho - 1

rho = M_W^2/(M_Z^2 c_W^2) with c_W^2 = g^2/(g^2 + g_Y^2), and M_W^2 = g^2 v^2/4 exactly, so
rho = M_Z0^2/M_Z^2. **rho >= 1:** the light nonzero eigenvalue M_Z^2 is the minimum of the Rayleigh
quotient over unit vectors orthogonal to the zero mode n (Courant-Fischer); z is one such vector with
quotient M_Z0^2, so M_Z^2 <= M_Z0^2. **Scaling:** from section 7,
rho - 1 = (z^T N_v u_hat)^2/(M_Z0^2 M_Z'^2) + ... proportional to v^2/w^2; doubling w divides rho - 1 by 4
(up to O(v^2/w^2) corrections). It vanishes only for the special ratio v1/v2 where z^T N_v u_hat = 0.
Self-check in `__main__` prints the ratio on doubling w.

## 9. `vev_from_GF(G_F)`

Muon decay at tree level: G_F/sqrt2 = g^2/(8 M_W^2). With M_W^2 = g^2 v^2/4 (section 4, v^2 = v1^2 + v2^2)
G_F/sqrt2 = 1/(2 v^2), so

    v = (sqrt2 G_F)^(-1/2).

**Second route.** Build `mass_matrix` with v1^2 + v2^2 = v^2, read M_W^2 = M2_11 and check
g^2/(8 M_W^2) * sqrt2 = G_F.

## 10. `mz_tree(G_F, alpha_inv, s2)`

e = g s_W, e^2 = 4 pi alpha, alpha = 1/alpha_inv. M_W^2 = g^2 v^2/4 = pi alpha v^2/s^2 =
pi alpha/(sqrt2 G_F s^2) and M_Z^2 = M_W^2/c^2:

    M_Z^2 = pi alpha / (sqrt2 G_F s^2 (1 - s^2))   (the SPEC convention).

**Second route.** Choose g = e/s, g_Y = e/c, and g_X from 1/g_X^2 = 1/g_Y^2 - beta^2/g^2 (needs
c^2/s^2 > beta^2, i.e. s^2 < 1/(1+beta^2) = 3/4), v = vev_from_GF, split v into v1, v2, take w >> v,
and compute M_Z from `neutral_masses`; it tends to mz_tree as w grows (difference O(v^2/w^2)).
Both variants are checked in `__main__`.

## Scaling (blind tier)

v ~ G_F^(-1/2) and M_Z ~ alpha^(1/2) G_F^(-1/2) follow from the closed forms; no constants are cached.

## Self-check output (`python3 gauge331.py`, g = 0.65, g_X = 0.8, w = 4000, v1 = 150, v2 = 190)

|M n| ~ 1e-9 against entries ~ 3e6 (round-off); 4 massless states at v = 0; 1/e^2 equals
1/g^2 + 1/g_Y^2 to all digits; eigvalsh and characteristic-polynomial roots agree to ~1e-14
relative; M_Z^2, M_Z'^2 within O(v^2/w^2) of the leading-order forms; rho - 1 ratio on doubling w
= 4.008 (both variants); G_F recovered from M2_11; M_Z from the full matrix -> mz_tree as w grows
(gap shrinking ~ 1/w^2).
