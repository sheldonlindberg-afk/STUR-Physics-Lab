# DERIVATION: stage `desitter` (build 2026-11-b)

Gravity as a broken SO(4,1) gauge theory. Postulates: SPEC.md section 6 (cited as S6) and the generator
formula in `contract.py`. Written before the code. Units G = c = 1 for the geometry (M and l are lengths);
SI metres for `ell_from_lambda` and `mm_coupling`.

Index conventions used throughout.
- A, B, C, D = 0..4, eta_AB = diag(-1, 1, 1, 1, 1). a, b, c, d = 0..3 (Lorentz), eta_ab = diag(-1, 1, 1, 1).
- mu, nu = 0..3 for x = (t, r, theta, phi).
- A p-form's components are the antisymmetric coefficients: w = w_mu dx^mu, R = (1/2) R_{mu nu} dx^mu ^ dx^nu.
- Matrices act on column vectors V^D; a matrix M has entries M^C_D = M[C][D].

Nothing in this stage is quoted and no measured number is needed (the self-check alone reads
`inputs.LAMBDA_SI` and `inputs.L_PLANCK`).

---

## 1. `so41_generator(A, B)`

**Postulate** (contract.py, S6): (J_AB)^C_D = delta^C_A eta_BD - delta^C_B eta_AD.

This is implemented verbatim with integer entries. Properties derived from it:

1. Antisymmetry J_AB = -J_BA (swap A and B in the formula); J_AA = 0. So there are 10 independent generators.
2. Lowering the row index, (eta J_AB)_{CD} = eta_CA eta_BD - eta_CB eta_AD, which is antisymmetric in C, D.
   Hence J^T eta + eta J = 0: each J_AB generates a transformation preserving eta, i.e. lies in so(4,1).
3. Product: (J_AB J_CD)^E_F = (delta^E_A eta_BG - delta^E_B eta_AG)(delta^G_C eta_DF - delta^G_D eta_CF)
   = delta^E_A eta_BC eta_DF - delta^E_A eta_BD eta_CF - delta^E_B eta_AC eta_DF + delta^E_B eta_AD eta_CF.
   Antisymmetrizing in (AB) <-> (CD):

   **[J_AB, J_CD] = eta_BC J_AD - eta_AC J_BD - eta_BD J_AC + eta_AD J_BC.**

4. With P_a = J_a4 (and eta_44 = +1, eta_a4 = 0): [P_a, P_b] = eta_44 ... only the eta_BD term survives:
   **[P_a, P_b] = -J_ab**. The translations close on the Lorentz algebra (with the scale restored,
   [P_a/l, P_b/l] = -J_ab/l^2: this is the origin of the -e^e/l^2 term in section 4).
   Also [J_ab, P_c] = eta_bc P_a - eta_ac P_b (P is a Lorentz vector).

**Second route.** Check item 3 by brute-force 5x5 matrix multiplication for all 10 x 10 pairs, and item 2
(eta J antisymmetric), in the self-check. The blind check tests item 4.

---

## 2. `unbroken_generators(V)`

**Postulate.** A vector V^D in the 5 of SO(4,1) (S6: "broken" gauge theory; the stabilizer of V is unbroken).

(J_AB V)^C = delta^C_A V_B - delta^C_B V_A, with V_B = eta_BD V^D.
For A != B this has exactly two possibly nonzero entries: row A holds V_B, row B holds -V_A.
So **J_AB V = 0 iff V_A = V_B = 0**, i.e. (eta is diagonal and invertible) iff V^A = V^B = 0.

Result: if V has k vanishing components, the generators J_AB that individually annihilate V number k(k-1)/2.
For V = (0,0,0,0,1): k = 4, the six J_ab with a < b <= 3: the Lorentz algebra so(3,1). The four P_a = J_a4
are broken (P_a V = e_a, the unit vector along a).

The implementation does not use the shortcut: it multiplies the matrix `so41_generator(A, B)` into V and
tests the result for zero (exactly; with a relative tolerance of 1e-12 of max|V| for float input).

**Second route.** The counting rule k(k-1)/2 and the explicit index criterion V^A = V^B = 0, compared with the
matrix route for several V in the self-check. (Note: the function lists basis generators annihilating V, as the
contract states. For a V not along a coordinate axis the full stabilizer also contains linear combinations of
the J_AB; e.g. a spacelike V always has a 6-dimensional stabilizer. The contract asks only for the J_AB.)

---

## 3. `spin_connection(x, f, fp)`

**Postulates** (S6). Metric ds^2 = -f dt^2 + dr^2/f + r^2 (dtheta^2 + sin^2 theta dphi^2), f = f(r) > 0;
diagonal tetrad
  e^0 = sqrt(f) dt,  e^1 = dr/sqrt(f),  e^2 = r dtheta,  e^3 = r sin(theta) dphi,
so that eta_ab e^a_mu e^b_nu = g_mu nu. The Levi-Civita spin connection is the unique omega^a_b with
(i) omega_ab = -omega_ba (metric) and (ii) de^a + omega^a_b ^ e^b = 0 (torsion-free).

**Derivation.** Exterior derivatives (f' = df/dr):

  de^0 = (f'/(2 sqrt f)) dr ^ dt
  de^1 = 0
  de^2 = dr ^ dtheta
  de^3 = sin(theta) dr ^ dphi + r cos(theta) dtheta ^ dphi

Solve (ii) equation by equation.

- a = 0: need omega^0_b ^ e^b = -(f'/(2 sqrt f)) dr ^ dt = +(f'/2) dt ^ (dr/sqrt f) = (f'/2) dt ^ e^1.
  Take omega^0_1 = (f'/2) dt, omega^0_2 = omega^0_3 = 0.
  Metricity: omega^0_1 = eta^00 omega_01 = -omega_01, omega^1_0 = omega_10 = -omega_01, so
  **omega^1_0 = omega^0_1 = (f'/2) dt** (a boost: symmetric with one index up).
- a = 2: need omega^2_b ^ e^b = -dr ^ dtheta = dtheta ^ dr = sqrt(f) dtheta ^ e^1.
  Take omega^2_1 = sqrt(f) dtheta; then **omega^1_2 = -sqrt(f) dtheta** (rotation: antisymmetric).
- a = 3: need omega^3_b ^ e^b = sin(theta) dphi ^ dr + r cos(theta) dphi ^ dtheta
  = sqrt(f) sin(theta) dphi ^ e^1 + cos(theta) dphi ^ e^2.
  Take omega^3_1 = sqrt(f) sin(theta) dphi, omega^3_2 = cos(theta) dphi; then
  **omega^1_3 = -sqrt(f) sin(theta) dphi, omega^2_3 = -cos(theta) dphi**.
- a = 1 (consistency; de^1 = 0): omega^1_0 ^ e^0 + omega^1_2 ^ e^2 + omega^1_3 ^ e^3
  = (f'/2) sqrt(f) dt ^ dt - sqrt(f) r dtheta ^ dtheta - sqrt(f) r sin^2(theta) dphi ^ dphi = 0. OK.
- remaining pieces of a = 0, 2, 3: omega^0_1 ^ e^1 is the only term for a = 0 (done);
  for a = 2, omega^2_3 ^ e^3 = -cos(theta) r sin(theta) dphi ^ dphi = 0; for a = 3, omega^3_0 = 0. OK.

All other components vanish. Uniqueness of the solution of (i)+(ii) guarantees this is the Levi-Civita connection.

**Result (closed form).** Nonzero components w[a][b][mu] = omega^a_{b mu}:

| component | value |
|---|---|
| w[0][1][t] = w[1][0][t] | f'/2 |
| w[1][2][theta] = -w[2][1][theta] | -sqrt(f) |
| w[1][3][phi] = -w[3][1][phi] | -sqrt(f) sin(theta) |
| w[2][3][phi] = -w[3][2][phi] | -cos(theta) |

and E[a][mu] = diag(sqrt f, 1/sqrt f, r, r sin theta). (Rung 6 reads kappa = |omega^0_{1 t}| = |f'|/2 at a horizon.)

Domain: f(r) > 0 (static region). f <= 0 raises ValueError.

**Second route.** Numerical torsion: T^a_{mu nu} = d_mu e^a_nu - d_nu e^a_mu + omega^a_{b mu} e^b_nu -
omega^a_{b nu} e^b_mu with the derivatives of the tetrad taken by central finite differences, for an SdS f;
plus eta_aa w[a][b] + eta_bb w[b][a] = 0. (Same property the blind check tests, computed in the self-check
with an independent 5-point stencil.)

---

## 4. The SO(4,1) curvature and `curvature_split_residual(M, l, x)`

**Postulates** (S6). A_mu = (1/2) omega^{ab}_mu J_ab + (1/l) e^a_mu J_a4;
F_{mu nu} = d_mu A_nu - d_nu A_mu + [A_mu, A_nu]. SdS: f = 1 - 2M/r - r^2/l^2.

**Matrix form of A.** Using the generator formula,
((1/2) omega^{ab} J_ab)^c_d = (1/2) omega^{ab}(delta^c_a eta_bd - delta^c_b eta_ad) = omega^c_d (omega^{ab}
antisymmetric), and it has no (.,4) or (4,.) entries. (J_a4)^C_D = delta^C_a eta_4D - delta^C_4 eta_aD, so
(e^a J_a4 / l) has entries [a][4] = e^a/l and [4][d] = -e_d/l. Hence, as a 5x5 matrix of 1-forms,

  A = [[ omega^a_b ,  e^a/l ],
       [ -e_b/l    ,  0     ]].

**Curvature.** F = dA + A ^ A (the commutator of components is the matrix wedge product):

- (a, b) block: d omega^a_b + omega^a_c ^ omega^c_b + (e^a/l) ^ (-e_b/l) = R^a_b - e^a ^ e_b / l^2,
- (a, 4) column: (1/l)(de^a + omega^a_c ^ e^c) = T^a / l,
- (4, 4): -(1/l^2) e_c ^ e^c = 0.

Decomposing F = (1/2) F^{ab} J_ab + F^{a4} J_a4 (same reading of the matrix as for A: F^{ab} = F[a][b] eta_bb,
F^{a4} = F[a][4]):

  **F^{ab} = R^{ab} - (1/l^2) e^a ^ e^b,   F^{a4} = T^a / l,**   R^{ab} = d omega^{ab} + omega^a_c ^ omega^{cb}.

So with the Levi-Civita omega the translation part of F vanishes and the Lorentz part is the Riemann curvature
shifted by the constant-curvature term.

**What the function computes.** Two independent constructions at the point x:

- Route F: build the 5x5 matrices A_mu(x) from `so41_generator` and `spin_connection`; differentiate A_nu
  numerically (5-point central stencil, 4th order) and add the matrix commutator [A_mu, A_nu]; read off
  F^{ab}_{mu nu} and F^{a4}_{mu nu}.
- Route R: R^{ab}_{mu nu} = d_mu omega^{ab}_nu - d_nu omega^{ab}_mu + omega^a_{c mu} omega^{cb}_nu -
  omega^a_{c nu} omega^{cb}_mu with the **analytic** derivatives of section 3's table (needs f''; section 5),
  and (e^a_mu e^b_nu - e^a_nu e^b_mu)/l^2.

Returned: max over a, b, mu, nu of |F^{ab} - R^{ab} + (e^a e^b - e^b e^a)_{mu nu}/l^2| and of |F^{a4}_{mu nu}|
(coordinate components). Expected: zero up to the finite-difference error (~1e-10).

Finite-difference step: h = 1e-3 x (1 for t, theta, phi; r for r), halved until f > 0 on the whole stencil.

**Second route.** That is the function itself (numerical F against analytic R). In addition the self-check
verifies that F[4][4] = 0 and that eta F is antisymmetric (F is so(4,1)-valued).

---

## 5. The Riemann curvature 2-form, `ricci_scalar(M, l, x)`

**Derivatives of the connection** (only r and theta dependence):

  d_r w[0][1][t] = f''/2;   d_r w[1][2][theta] = -f'/(2 sqrt f);
  d_r w[1][3][phi] = -f' sin(theta)/(2 sqrt f);   d_theta w[1][3][phi] = -sqrt(f) cos(theta);
  d_theta w[2][3][phi] = sin(theta);   (and the index-swapped partners with the symmetry of section 3).

**Closed form** (used as the second route; the code contracts the generic formula). With e^a ^ e^b as basis:

- R^{01} = d omega^0_1 = (f''/2) dr ^ dt = -(f''/2) e^0 ^ e^1.
- R^{02} = omega^0_1 ^ omega^1_2 = -(f'/2) sqrt(f) dt ^ dtheta = -(f'/(2r)) e^0 ^ e^2;  same for R^{03}.
- R^{12} = d omega^1_2 + omega^1_3 ^ omega^3_2 = -(f'/(2 sqrt f)) dr ^ dtheta = -(f'/(2r)) e^1 ^ e^2.
- R^{13} = -(f'/(2 sqrt f)) sin(theta) dr ^ dphi - sqrt(f) cos(theta) dtheta ^ dphi + omega^1_2 ^ omega^2_3
  = -(f'/(2r)) e^1 ^ e^3 (the cos(theta) terms cancel: omega^1_2 ^ omega^2_3 = +sqrt(f) cos(theta) dtheta ^ dphi).
- R^{23} = d(-cos(theta) dphi) + omega^2_1 ^ omega^1_3 = sin(theta)(1 - f) dtheta ^ dphi = ((1 - f)/r^2) e^2 ^ e^3.

**Ricci scalar.** R = E_a^mu E_b^nu R^{ab}_{mu nu} = sum_{a != b} (coefficient of e^a ^ e^b in R^{ab})
= 2 [ -f''/2 - 4 f'/(2r) + (1 - f)/r^2 ]:

  **R = -f'' - 4 f'/r + 2(1 - f)/r^2.**

For SdS, f' = 2M/r^2 - 2r/l^2, f'' = -4M/r^3 - 2/l^2, 1 - f = 2M/r + r^2/l^2:
R = (4M/r^3 + 2/l^2) + (-8M/r^3 + 8/l^2) + (4M/r^3 + 2/l^2) = **12/l^2**, independent of M and of x
(the mass term is Ricci-flat). It scales as 1/length^2.

The function evaluates the generic contraction sum_{a,b,mu,nu} E_a^mu E_b^nu R^{ab}_{mu nu} of the same array
`action_coefficients` uses (E_a^mu = 1/E[a][a], diagonal).

**Second route.** (i) the closed form 12/l^2; (ii) R^{ab} with d omega taken by finite differences of
`spin_connection` instead of the analytic table (what the blind check does); both in the self-check.

---

## 6. `ds_curvature_max(l, x)`

De Sitter: f = 1 - r^2/l^2, f' = -2r/l^2, f'' = -2/l^2. Insert in section 5:
R^{01} = (1/l^2) e^0 ^ e^1; R^{0i} = (1/l^2) e^0 ^ e^i; R^{1i} = (1/l^2) e^1 ^ e^i; R^{23} = (1/l^2) e^2 ^ e^3.
So R^{ab} = e^a ^ e^b / l^2 for all a, b: constant curvature, and by section 4
**F^{ab} = 0, F^{a4} = 0: de Sitter space is a flat SO(4,1) connection** (the vacuum), precisely when the l in
the connection equals the l in the metric.

The function returns max |F^C_{D mu nu}| over all 5x5 entries and mu < nu, from Route F of section 4 with
M = 0 (numerical derivative), so the expected value is the finite-difference noise, ~1e-10 or less.

**Second route.** The analytic statement above (R^{ab} - e^a e^b/l^2 evaluated from section 5's closed form
gives exactly zero), compared in the self-check; and mismatching the two l's must give a nonzero F.

---

## 7. `action_coefficients(M, l, x)` -> (cR, cV)

**Postulates** (S6). Lorentz symbol with lowered indices eps_0123 = +1 (`toolkit.levi_civita`); coordinate
density epst^{0123} = +1, a 4-form's component is its coefficient on dt ^ dr ^ dtheta ^ dphi.
Definitions: eps_abcd R^{ab} ^ e^c ^ e^d = cR e R d^4x and eps_abcd e^a ^ e^b ^ e^c ^ e^d = cV e d^4x,
with e = det(e^a_mu) and R the Ricci scalar of section 5.

**Derivation.** For any 4-form W = W_{mu nu rho sigma} dx^mu dx^nu dx^rho dx^sigma (no antisymmetrization
factor), its component on d^4x is epst^{mu nu rho sigma} W_{mu nu rho sigma}.

- Volume term: eps_abcd e^a_mu e^b_nu e^c_rho e^d_sigma = e [mu nu rho sigma] (definition of the determinant;
  [..] the permutation symbol). Contract with epst: [mu nu rho sigma][mu nu rho sigma] = 4! = 24.
  **cV = 24.**
- Curvature term: R^{ab} = (1/2) R^{ab}_{mu nu} dx^mu ^ dx^nu, so the component is
  (1/2) eps_abcd R^{ab}_{mu nu} e^c_rho e^d_sigma epst^{mu nu rho sigma}.
  Insert e^a_alpha E_a'^alpha = delta: eps_abcd e^c_rho e^d_sigma = e E_a^alpha E_b^beta [alpha beta rho sigma],
  and [alpha beta rho sigma][mu nu rho sigma] = 2(delta^mu_alpha delta^nu_beta - delta^mu_beta delta^nu_alpha).
  So the component is (1/2) R^{ab}_{mu nu} 2 e (E_a^mu E_b^nu - E_a^nu E_b^mu) = 2 e R.
  **cR = 2.**

No signs from the signature appear, because both symbols are plain permutation symbols.

**What the function computes.** The two 4-form components by explicit 24 x 24 sums over permutations with
`toolkit.levi_civita`, using section 5's R^{ab}_{mu nu} and the tetrad, divided by e R (R from `ricci_scalar`,
e = product of the diagonal tetrad) and by e. Both are geometry independent. (cR is undefined where R = 0, i.e.
l -> infinity; on SdS R = 12/l^2 > 0.)

**Second route.** The index identities above (2 and 24); and geometry independence at different (M, l, x).

**Consequence: the MacDowell-Mansouri action.** With F^{ab} = R^{ab} - e^a e^b/l^2 (section 4),

  N eps_abcd F^{ab} ^ F^{cd} = N eps R R - (2N/l^2) eps R e e + (N/l^4) eps e e e e
  = N eps_abcd R^{ab} ^ R^{cd} - (4N/l^2) e (R - 6/l^2) d^4x.

The first term is the Euler (Gauss-Bonnet) density, a total derivative that does not affect the field
equations. The rest is the Einstein-Hilbert form (1/(16 pi G)) e (R - 2 Lambda) with

  **Lambda = 3/l^2,   -4N/l^2 = 1/(16 pi G)  =>  |N| = l^2/(64 pi G)** (hbar = c = 1: l^2/(64 pi lP^2)).

---

## 8. `ell_from_lambda(Lam)`

From section 7: matching the action to e(R - 2 Lambda) gives Lambda = 3/l^2, so

  **l = sqrt(3/Lambda).**

The identification of "cosmological constant" with the Lambda of the Einstein-Hilbert form (R - 2 Lambda) is
the standard definition and is the one assumption here beyond S6.

**Second route** (independent of the action). The field equation of e(R - 2 Lambda) in vacuum is
G_mu nu + Lambda g_mu nu = 0, whose trace is R = 4 Lambda. Section 5 gives R = 12/l^2 for the SdS/de Sitter
metric with radius l. Hence Lambda = 3/l^2 again. Self-check: `ricci_scalar(M, l, x)` x l^2 / 4 == 3 numerically,
and 4 Lam == ricci_scalar at l = ell_from_lambda(Lam).

Lam <= 0 raises ValueError (no de Sitter radius).

---

## 9. `mm_coupling(Lam, lP)`

The contract defines the export as "the dimensionless MacDowell-Mansouri coupling l^2/lP^2, l =
ell_from_lambda(Lam)". From section 7 the action's coefficient is N = -l^2/(64 pi G) in units hbar = c = 1,
i.e. N = -(1/(64 pi)) l^2/lP^2 with lP^2 = hbar G/c^3: the only dimensionless parameter of the theory is the
ratio l^2/lP^2. The function returns exactly that ratio,

  **mm_coupling = l^2/lP^2 = 3/(Lambda lP^2),**

computed through `ell_from_lambda` (not the 1/(64 pi) normalized N; see QUESTIONS.md). It scales as 1/Lambda.

**Second route.** 3/(Lam lP^2) directly, and the scaling coupling(Lam)/coupling(2 Lam) = 2.

---

## Not derived / assumptions

- The identification Lambda <-> (R - 2 Lambda) (standard definition of the cosmological constant).
- The Gauss-Bonnet term being a total derivative is stated, not proven here; it does not enter any export.
- Nothing else. No quoted results.
