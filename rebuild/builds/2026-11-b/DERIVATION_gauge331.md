# DERIVATION: stage `gauge331` (build 2026-11-b)

Postulates: SPEC.md section 2 (cited as S2). Conventions: S2 "Conventions" and contract.py.
Nothing is quoted; no value from `inputs.py` is needed inside this stage (the three numerical
functions take their numbers as arguments). Written before the code.

Notation. t_a = lambda_a/2 (a = 1..8), t_9 = X*1 (the U(1)_X generator on a multiplet of charge X).
g_a = g for a <= 8, g_9 = g_X. beta = -1/sqrt3 or +1/sqrt3. Components are numbered 1, 2, 3.

## 1. `triplet_charges(X, variant, anti)`

Rests on: S2 bullets 1, 2 (Q = T3 + beta T8 + X; antitriplet generators -t_a^*).

T3 = lambda_3/2 = diag(1/2, -1/2, 0).  T8 = lambda_8/2 = diag(1, 1, -2)/(2 sqrt3).
So beta T8 = b diag(1, 1, -2) with

    b = beta/(2 sqrt3) = -1/6  (beta = -1/sqrt3),   +1/6  (beta = +1/sqrt3).

b is rational, so all charges are exact Fractions:

    triplet:      Q = (1/2 + b + X,  -1/2 + b + X,  -2b + X)
    antitriplet:  T3, T8 are real and diagonal, so -t^* = -t on the Cartan generators, X unchanged (S2):
                  Q = (-1/2 - b + X,  1/2 - b + X,  2b + X)

Second route (identities, checked in `__main__` and by the blind tests): Q1 - Q2 = +1 (triplet), -1
(antitriplet), independent of X and beta, because only T3 distinguishes components 1 and 2; and
sum Q = 3X because T3, T8 are traceless. Also: independent float evaluation of the diagonal of
T3 + beta T8 + X built from the explicit Gell-Mann matrices used by `mass_matrix`.

## 2. `quark_charges(Nc)`

Rests on: S2 "Fermions" and "Q_u and Q_d are not inputs".

Unknown: Q_u. Doublet: Q_d = Q_u - 1.

Lepton triplet (nu, e, .): the electron is the T3 = -1/2 member with charge -1:
-1/2 + b + X_L = -1  =>  X_L = -1/2 - b   ( = -1/3 for b = -1/6, -2/3 for b = +1/6: agrees with S2's
stated X_L, which the code asserts in `__main__`; the neutrino charge 1/2 + b + X_L = 0 follows).

Quark triplet, first two components (Q_u, Q_d):  1/2 + b + X_t = Q_u   =>  X_t = Q_u - 1/2 - b.
Quark antitriplet, first two components (Q_d, Q_u) (the antitriplet reverses the T3 order):
-1/2 - b + X_a = Q_d = Q_u - 1   =>  X_a = Q_u - 1/2 + b.

[SU(3)_L]^2 U(1)_X anomaly: proportional to sum over left-handed multiplets of T(R) X, with
T(3) = T(3bar) = 1/2, each quark family counted N_c times (colour). With N_g = N_c generations,
n_A = (1 + N_c)/2 antitriplet quark families and N_g - n_A triplet families:

    A(Q_u) = N_g X_L + N_c [ (N_g - n_A) X_t + n_A X_a ] = 0.

A is affine in Q_u. Insert X's, use N_g = N_c and N_c - 2 n_A = -1:

    A = N_c(-1/2 - b) + N_c [ N_c (Q_u - 1/2) - b (N_c - 2 n_A) ]
      = N_c [ -1/2 - b + N_c (Q_u - 1/2) + b ] = N_c [ N_c (Q_u - 1/2) - 1/2 ]

    =>  Q_u = 1/2 + 1/(2 N_c) = (N_c + 1)/(2 N_c),     Q_d = Q_u - 1 = (1 - N_c)/(2 N_c).

b (hence the variant) cancels. Code: A(Q_u) is built literally from the multiplet content with
`triplet_charges`-consistent X's; the root of the affine function is Q_u = -A(0)/A'(0) with A' from
`toolkit.exact_derivative` (exact, Fractions). Computed in both variants and asserted equal.

Side remark (why n_A = (1+N_c)/2): the [SU(3)_L]^3 anomaly needs equal numbers of 3 and 3bar:
N_g + N_c (N_g - n_A) = N_c n_A  <=>  n_A = (1 + N_c)/2 for N_g = N_c. So n_A is an integer only for odd N_c;
for even N_c the formula is still evaluated as a rational continuation (not physical content).

Second route (S2 "Equivalently"): proton of (N_c+1)/2 u and (N_c-1)/2 d with q_p + q_e = 0, q_e = -1:
(N_c+1)/2 Q_u + (N_c-1)/2 (Q_u - 1) = 1  =>  N_c Q_u = 1 + (N_c - 1)/2  =>  Q_u = (N_c+1)/(2N_c). Same.
Printed side by side in `__main__`.

## 3. `doublet_charge_pairs(Nc, variant)`

Rests on: S2 "Fermions". The set of {Q1, Q2} over: the lepton triplet (X_L = -1/2 - b), the quark triplet
(X_t = Q_u - 1/2 - b), the quark antitriplet (X_a = Q_u - 1/2 + b), each evaluated through
`triplet_charges`. Expected from section 2: leptons {0, -1}; both quark kinds {Q_u, Q_d}. Second route: that
expectation in closed form (independent of the X bookkeeping), compared in `__main__` for several N_c.
(For N_c = 1, n_A = 1 and there are no triplet quark families; the set is unchanged since both quark kinds
give the same pair. The code only includes multiplets whose multiplicity is nonzero.)

## 4. Scalar vevs (used by `mass_matrix`)

Rests on: S2 "Scalars". Neutral components are derived with `triplet_charges`, not assumed:

beta = -1/sqrt3 (b = -1/6): Q = (1/3 + X, -2/3 + X, 1/3 + X).
  X = -1/3: (0, -1, 0)   neutral: 1, 3
  X = +2/3: (1,  0, 1)   neutral: 2
  X = -1/3: (0, -1, 0)   neutral: 1, 3
beta = +1/sqrt3 (b = +1/6): Q = (2/3 + X, -1/3 + X, -1/3 + X).
  X = +1/3: (1, 0, 0)    neutral: 2, 3
  X = +1/3: (1, 0, 0)    neutral: 2, 3
  X = -2/3: (0, -1, -1)  neutral: 1

Rule: first triplet neutral in component 3 takes w there (triplet 1 in both variants). The others take, in
order, v1 then v2 in their neutral component other than 3. Result in BOTH variants:

    phi_1 = (0, 0, w)/sqrt2,   phi_2 = (0, v1, 0)/sqrt2,   phi_3 = (v2, 0, 0)/sqrt2,

with X = (-1/3, 2/3, -1/3) resp. (1/3, 1/3, -2/3). The code runs the rule; it raises if a non-w triplet does
not have exactly one neutral component other than 3.

## 5. `mass_matrix`

Rests on: S2 bullet 1, conventions (basis W^1..W^8, B_X; <phi>_k = vev/sqrt2); contract formula.

D_mu phi = (d_mu - i sum_A g_A V^A_mu T_A) phi, T_A = t_A (A <= 8), T_9 = X 1.
|D phi|^2 at the vev contains V^A V^B g_A g_B <phi>^dag T_A T_B <phi> = (1/2) M2_AB V^A V^B, so (symmetrizing)

    M2_AB = g_A g_B sum_phi <phi>^dag {T_A, T_B} <phi>.

(Normalization check: one doublet-like vev v in component 2 gives M2_11 = g^2 * 2 * (1/4) * v^2/2 = g^2 v^2/4.)
The code evaluates this literally with the explicit 3x3 complex Gell-Mann matrices; the result is real
because {T_A, T_B} is Hermitian and M2 is symmetric under A <-> B (imaginary parts cancel; the code takes
the real part).

Closed form. Each vev sits in a single component k, magnitude u/sqrt2, so
<phi>^dag {T_A,T_B} <phi> = (u^2/2) ({T_A,T_B})_kk.
- Cartan block (A, B in {3, 8, 9}): ({T_A,T_B})_kk = 2 (T_A)_kk (T_B)_kk, so

      M2_neutral = sum_phi u_phi^2 q_phi q_phi^T,   q_phi = (g (t3)_kk, g (t8)_kk, g_X X_phi).

  q_w  = (0, -g/sqrt3, g_X X_1),  q_1 = (-g/2, g/(2 sqrt3), g_X X_2),  q_2 = (g/2, g/(2 sqrt3), g_X X_3).
- Off-diagonal generators: (t_A t_B)_kk with A off-diagonal, B Cartan vanishes; for the pairs (1,2), (4,5),
  (6,7), (t_A^2)_kk = 1/4 on the two components the pair connects, and all cross terms vanish on the diagonal.
  So M2 is diagonal there:

      M2_11 = M2_22 = g^2 (v1^2 + v2^2)/4      (connects components 1-2)   -> the W
      M2_44 = M2_55 = g^2 (w^2 + v2^2)/4       (components 1-3)
      M2_66 = M2_77 = g^2 (w^2 + v1^2)/4       (components 2-3)

Second route: `__main__` compares the anticommutator build with this closed form entry by entry.
M_W^2 = g^2 (v1^2+v2^2)/4 is independent of w and quadratic in v.

## 6. `photon_direction` and `inv_e2`

Rests on: S2 (Q definition; vevs only in Q = 0 components).

A gauge direction n generates G(n) = sum_A n_A g_A T_A. Choose G(n) = Q = T3 + beta T8 + X on every multiplet:
n_3 g = 1, n_8 g = beta, n_9 g_X = 1, all else 0:

    n = (0, 0, 1/g, 0, 0, 0, 0, beta/g, 1/g_X)        (0-based indices 2, 7, 8).

Massless for ANY vevs respecting Q (verifier question 1): (M2 n)_A = g_A sum_phi <phi>^dag {T_A, Q} <phi> = 0
because Q<phi> = 0 and <phi>^dag Q = 0 (Q Hermitian) whenever vevs sit only in neutral components. No dependence
on w, v1, v2.

Coupling: write V^A = n_A/|n| * A_gamma + ...; then sum_A g_A T_A V^A contains (Q/|n|) A_gamma, so e = 1/|n|:

    1/e^2 = |n|^2 = (1 + beta^2)/g^2 + 1/g_X^2 = 4/(3 g^2) + 1/g_X^2.

Homogeneous of degree -2 in (g, g_X); larger than 1/g^2 and 1/g_X^2 (e weaker than both).
Second route: (a) residual max|M2 n| at random vevs; (b) the photon is the numerically obtained null vector
of the Cartan block: n is orthogonal to q_w, q_1, q_2 (n.q_phi = Q of the vev component = 0), i.e. n is
parallel to the cross product q_w x q_1; `__main__` compares, and compares 1/e^2 = |n|^2 with the formula
(1+beta^2)/g^2 + 1/g_X^2. `inv_e2` is computed as |photon_direction|^2.

After step 1 only (v1 = v2 = 0; verifier question 2): only q_w is nonzero, the Cartan block has rank 1, and
W^1, W^2 are massless: 4 massless = W^1, W^2, W^3 and the combination of (W^8, B_X) orthogonal to q_w,
i.e. SU(2)_L x U(1)_Y with Y = beta T8 + X; 5 massive (W^4..W^7 and Z'), matching 9 - 4.

## 7. `neutral_masses`

Rests on: sections 5, 6. The block (W^3, W^8, B_X) (0-based 2, 7, 8) decouples (section 5). It is
sum_phi u^2 q q^T with all three q orthogonal to n, so it has rank 2: eigenvalues (0, M_Z^2, M_Z'^2).
Main route: `toolkit.eigvalsh` on the 3x3 block cut from `mass_matrix`; return the two largest, ascending.

Second route (closed form, independent of the solver and of the anticommutator assembly): the nonzero
eigenvalues of sum_i u_i^2 q_i q_i^T are those of the Gram matrix G_ij = u_i u_j q_i.q_j; with det = 0 the
characteristic polynomial is lambda (lambda^2 - T lambda + P), where

    T = sum_i u_i^2 |q_i|^2,     P = sum_{i<j} u_i^2 u_j^2 ( |q_i|^2 |q_j|^2 - (q_i.q_j)^2 ),
    M^2_{Z', Z} = [ T +- sqrt(T^2 - 4P) ] / 2.

Scaling (verifier question 3). For w >> v: M_Z'^2 = w^2 |q_w|^2 [1 + O(v^2/w^2)] (grows as w^2), and
M_Z^2 = P/M_Z'^2 -> sum_j v_j^2 |q_j,perp|^2 (q_perp = part of q_j orthogonal to q_w), independent of w, with
relative correction -O(v^2/w^2) (second-order level repulsion pushes the light eigenvalue DOWN). The w -> infinity
limit is the SM: with only the doublet vevs the light state has M_Z^2 = (g^2 + g_Y^2) v^2/4, v^2 = v1^2 + v2^2,
1/g_Y^2 = beta^2/g^2 + 1/g_X^2, so M_W^2/M_Z^2 -> cos^2 theta_W = g^2/(g^2+g_Y^2), and
rho - 1 = M_W^2/(M_Z^2 c_W^2) - 1 = +O(v^2/w^2) > 0: M_W^2/M_Z^2 approaches its limit from above, successive
differences under w -> 2w fall by 4. `__main__` checks the limit value against g^2/(g^2 + g_Y^2).

## 8. `vev_from_GF(G_F)`

Rests on: sections 5 (M_W^2 = g^2 v^2/4) plus the definition of G_F as the coefficient of the low-energy
charged-current four-fermion interaction: W exchange at q^2 << M_W^2 gives G_F/sqrt2 = g^2/(8 M_W^2).
Hence G_F/sqrt2 = 1/(2 v^2):   v = (sqrt2 G_F)^(-1/2).  (The matching G_F/sqrt2 = g^2/(8 M_W^2) is the standard
tree-level definition, used here as the definition of G_F; it is the formula the contract fixes.)
Second route: v^2 * sqrt2 * G_F = 1 and v ~ G_F^(-1/2) scaling.

## 9. `mz_tree(G_F, alpha_inv, s2)`

Rests on: S2 conventions (the tree relation is stated there), re-derived: in the w -> infinity limit
M_Z^2 = M_W^2/c^2, M_W^2 = g^2 v^2/4, e = g s (from section 6 in the SM limit: 1/e^2 = 1/g^2 + 1/g_Y^2,
s^2 = e^2/g^2), alpha = e^2/(4 pi):  g^2 = 4 pi alpha/s^2,

    M_Z^2 = pi alpha v^2/(s^2 c^2) = pi alpha / (sqrt2 G_F s^2 (1 - s^2)).

Second route: M_Z = g v/(2 c) evaluated step by step through `vev_from_GF` (g = sqrt(4 pi alpha/s2)) versus the
one-line formula; printed in `__main__` with inputs.G_F, ALPHA_MZ_INV, S2_MZ.

## Not derived / caveats

- The Fermi matching G_F/sqrt2 = g^2/(8 M_W^2) is taken as the definition of G_F (section 8), not derived from
  a muon-decay amplitude.
- Even N_c in `quark_charges`: rational continuation only (n_A non-integer).
