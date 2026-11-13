# DERIVATION: desitter (rung 5, SPEC.md section 6)

Conventions: Lorentz/tetrad indices a, b, ... = 0..3; so(4,1) indices A, B, ... = 0..4;
eta_AB = diag(-1, 1, 1, 1, 1) (contract.py). Coordinates x = (t, r, theta, phi), index mu = 0..3.
epsilon symbols are the plain permutation sign, `toolkit.levi_civita`: eps_{0123} = +1 for the
Lorentz symbol eps_abcd and eps~^{0123} = +1 for the coordinate density eps~^{mu nu rho sigma}
(d^4x := dt^dr^dtheta^dphi). Wedge components: a p-form alpha = (1/p!) alpha_{mu...} dx^mu ^ ...;
(alpha ^ beta)_{mu nu} = alpha_mu beta_nu - alpha_nu beta_mu for 1-forms.

Postulates (SPEC.md section 6, contract.py "desitter"):
- P1 (J_AB)^C_D = delta^C_A eta_BD - delta^C_B eta_AD.
- P2 A_mu = (1/2) omega^{ab}_mu J_ab + (1/l) e^a_mu J_a4, F_{mu nu} = d_mu A_nu - d_nu A_mu + [A_mu, A_nu].
- P3 metric -f dt^2 + dr^2/f + r^2 dOmega^2, diagonal tetrad (sqrt f, 1/sqrt f, r, r sin th);
  Levi-Civita omega: torsion T^a = de^a + omega^a_b ^ e^b = 0, omega_ab = -omega_ba.
- P4 SdS f = 1 - 2M/r - r^2/l^2; dS f = 1 - r^2/l^2.
- P5 MacDowell-Mansouri action N Int eps_abcd F^ab ^ F^cd.

---------------------------------------------------------------------------------------------------
## 1. so41_generator(A, B)

Direct from P1: a 5x5 matrix with entry [C][D] = delta_{CA} eta_{BD} - delta_{CB} eta_{AD}.
Antisymmetric in (A, B) by construction. Lowering, (J_AB)_{CD} = eta_CA eta_BD - eta_CB eta_AD is
antisymmetric in C, D, so J_AB is in so(4,1) (preserves eta).

Algebra (derived by multiplying the matrices, checked numerically in the self-check):
[J_AB, J_CD] = eta_BC J_AD - eta_AC J_BD - eta_BD J_AC + eta_AD J_BC.
With P_a = J_a4: [P_a, P_b] = -eta_44 J_ab = -J_ab (so (1/l) P_a gives -(1/l^2) J_ab: the
translations close on Lorentz with positive cosmological curvature).

Second route: the blind check computes [P_a, P_b] + J_ab = 0 numerically; the self-check also
verifies the general commutator formula for all 10x10 pairs.

## 2. unbroken_generators(V)

A vector V^C is left invariant by J_AB iff (J_AB V)^C = delta^C_A V_B - delta^C_B V_A = 0
(V_B = eta_BD V^D). Computed literally: build each J_AB (A < B), multiply by V, keep those with
|J_AB V| = 0 (tolerance relative to |V|).
For V = (0,0,0,0,1): J_ab V = delta_a (eta_b4) - ... = 0 for a, b < 4 (6 Lorentz generators),
J_a4 V = e_a != 0. Unbroken: so(3,1), 6 generators. The four "translations" J_a4 are broken; the
de Sitter vector is the Higgs-like field of MacDowell-Mansouri / Stelle-West.

Second route: the stabilizer of a spacelike unit vector in R^{4,1} is SO(3,1), dimension
4*3/2 = 6; the count 10 - 4 matches (the orbit, de Sitter space, is 4-dimensional).

## 3. spin_connection(x, f, fp)

Tetrad: e^0 = sqrt f dt, e^1 = dr/sqrt f, e^2 = r dth, e^3 = r sin th dph, so
E[a][mu] = diag(sqrt f, 1/sqrt f, r, r sin th).

Cartan's first equation de^a = -omega^a_b ^ e^b, using dr = sqrt f e^1, dt = e^0/sqrt f, dth = e^2/r:
- de^0 = (f'/(2 sqrt f)) dr ^ dt = (f'/(2 sqrt f)) e^1 ^ e^0  =>  omega^0_1 = (f'/(2 sqrt f)) e^0 = (f'/2) dt.
- de^1 = d(f^{-1/2}) ^ dr = 0 (proportional to dr ^ dr).
- de^2 = dr ^ dth = (sqrt f / r) e^1 ^ e^2  =>  omega^2_1 = (sqrt f / r) e^2 = sqrt f dth.
- de^3 = sin th dr ^ dph + r cos th dth ^ dph  =>  omega^3_1 = sqrt f sin th dph, omega^3_2 = cos th dph.
Metric compatibility (omega_ab = -omega_ba with omega_ab = eta_ac omega^c_b) fixes the rest:
omega^1_0 = +omega^0_1 (boost, eta_00 = -1), omega^1_2 = -omega^2_1, omega^1_3 = -omega^3_1,
omega^2_3 = -omega^3_2. Check that these extra terms don't spoil the other equations:
-omega^1_0 ^ e^0 = -(f'/2) sqrt f dt ^ dt = 0; -omega^1_2 ^ e^2 = sqrt f r dth ^ dth = 0;
-omega^1_3 ^ e^3 = 0 (dph ^ dph); -omega^2_3 ^ e^3 = cos th r sin th dph ^ dph = 0. So all four
equations hold, and Levi-Civita uniqueness makes this THE torsion-free metric connection.

Closed form (w[a][b][mu] = omega^a_{b mu}, nonzero only):
  w[0][1][t] = w[1][0][t] = f'/2,
  w[2][1][th] = -w[1][2][th] = sqrt f,
  w[3][1][ph] = -w[1][3][ph] = sqrt f sin th,
  w[3][2][ph] = -w[2][3][ph] = cos th.

At a horizon f -> 0: |omega^0_{1 t}| = |f'|/2 = kappa (rung 6 connection).

Proof (the SPEC requires it numerically): torsion T^a_{mu nu} = d_mu e^a_nu - d_nu e^a_mu
+ omega^a_{b mu} e^b_nu - omega^a_{b nu} e^b_mu, with d computed by central finite differences
of E(x) (step h ~ 1e-5), max |T| ~ 1e-10. Done in the module (`_torsion`), self-check prints it.

Second route: Ricci scalar from the curvature built from this omega (section 5) vs the known
value for f = 1 - r^2/l^2 (maximally symmetric, R = 12/l^2), and vs SdS (R = 12/l^2: the 2M/r
part is Ricci-flat); also the Riemann component R^{01}_{01} = -f''/2 (= 1/l^2 for dS).

## 4. Curvature of A; curvature_split_residual(M, l, x)

Matrix form of A (from P1): ((1/2) omega^{ab} J_ab)^c_d = (1/2)(omega^{cb} eta_bd - omega^{ac} eta_ad)
= omega^c_d (antisymmetry of omega^{ab}); ((1/l) e^b J_b4)^a_4 = e^a/l, (...)^4_d = -e_d/l.
So A_mu = [[omega^a_{d mu}, e^a_mu/l], [-e_{d mu}/l, 0]].
F_{mu nu} = d_mu A_nu - d_nu A_mu + [A_mu, A_nu]; block by block:
- Lorentz block: d omega + omega ^ omega + (column)(row) term:
  F^a_d = R^a_d + (e^a/l) ^ (-e_d/l) = R^a_d - e^a ^ e_d / l^2,
  i.e. F^{ab} = R^{ab} - e^a ^ e^b / l^2 (raise d with eta).
- (a,4) entry: F^a_4 = (de^a + omega^a_b ^ e^b)/l = T^a / l.
- (4,4) entry: -e_d ^ e^d / l^2 = 0.
The J_AB-components are read off the matrix: F^{ab} = (F)^a_c eta^{cb} (a, b < 4), F^{a4} = (F)^a_4
(coefficient of J_a4, since (J_a4)^a_4 = eta_44 = 1); the module verifies that
sum_{A<B} F^{AB} J_AB reconstructs the matrix (i.e. F really lies in so(4,1)).

Implementation (no algebra assumed): A_mu(x) assembled from `so41_generator` matrices and
`spin_connection`; d_mu A_nu by central differences; commutators by matrix products.
R^a_b from omega ALONE: R^a_{b mu nu} = d_mu omega^a_{b nu} - d_nu omega^a_{b mu}
+ omega^a_{c mu} omega^c_{b nu} - omega^a_{c nu} omega^c_{b mu} (same finite differences).
Residual = max over a, b, mu, nu of |F^ab - R^ab + (e^a e^b - e^b e^a)_{mu nu}/l^2| and |F^{a4}|.
Expected ~ 1e-9 (finite-difference error of the torsion; the Lorentz block identity is algebraic).

## 5. ds_curvature_max(l, x)

For f = 1 - r^2/l^2, a maximally symmetric space of curvature +1/l^2: R^{ab} = e^a ^ e^b / l^2, so
F^{ab} = 0, and F^{a4} = T/l = 0: the de Sitter connection is FLAT as an SO(4,1) connection
(de Sitter = SO(4,1)/SO(3,1), the "vacuum" of the gauge theory). Implementation: max |F_{mu nu}|
matrix entry, computed exactly as in section 4 with M = 0.
Second route: Riemann components from omega: R^{01}_{01} = -f''/2 = 1/l^2,
R^{02}_{02} = R^{03}_{03} = -f'/(2r) = 1/l^2, R^{12}_{12} = R^{13}_{13} = -f'/(2r), R^{23}_{23} = (1-f)/r^2 = 1/l^2.
Ricci scalar 12/l^2 (self-check prints it).

## 6. action_coefficients(M, l, x) -> (cR, cV)

As 4-forms, X = X_{0123} d^4x. Wedge of forms in components:
e^a ^ e^b ^ e^c ^ e^d = e^a_mu e^b_nu e^c_rho e^d_sig dx^mu^dx^nu^dx^rho^dx^sig
  = eps~^{mu nu rho sig} e^a_mu e^b_nu e^c_rho e^d_sig d^4x.
R^ab ^ e^c ^ e^d = (1/2) R^ab_{mu nu} e^c_rho e^d_sig eps~^{mu nu rho sig} d^4x.
So [eps_abcd e^a^e^b^e^c^e^d]_{0123} = sum eps_abcd eps~^{mu nu rho sig} e^a_mu ... and
[eps_abcd R^ab^e^c^e^d]_{0123} = (1/2) sum eps_abcd eps~^{mu nu rho sig} R^ab_{mu nu} e^c_rho e^d_sig.
The module performs these sums literally (toolkit.levi_civita for both epsilons, R^ab from omega by
finite differences, section 4), and divides by e = det(e^a_mu) and by e R, where the Ricci scalar
R = R^{ab}_{mu nu} E_a^mu E_b^nu (inverse tetrad) is computed from the same R^ab.

Closed form (algebra): eps~^{mu nu rho sig} e^a_mu e^b_nu e^c_rho e^d_sig = e eps~^{abcd}, so
cV = sum_abcd eps_abcd eps~^{abcd} = 4! = 24. Writing R^ab_{mu nu} = R^ab_{ef} e^e_mu e^f_nu,
[eps R e e] = (1/2) e R^ab_{ef} sum_cd eps~^{efcd} eps_abcd = (1/2) e R^ab_{ef} 2(d^e_a d^f_b - d^e_b d^f_a)
= 2 e R^{ab}_{ab} = 2 e R, so cR = 2. Both are integers fixed by the epsilon contraction alone, so
independent of the geometry (blind check), and the exact values are computed in the module as
Fractions from toolkit.levi_civita (`_exact_coefficients`):
cV = sum_{abcd} eps_abcd^2, cR = (1/2) sum_{cd} (eps~^{01cd} eps_{01cd} - eps~^{10cd} eps_{01cd}).
Sign convention: with eps_{0123} = +1 for the lowered Lorentz symbol. (If one instead took
eps^{0123} = +1 and lowered with eta, both flip sign; the ratio cV/cR, which is the physics, does not.)

Second route: the numerical geometric contraction at two different SdS geometries reproduces the
exact integers (self-check), and the ratio is used below.

## 7. Lambda from l; ell_from_lambda(Lam); mm_coupling(Lam, lP)

Expand the MM Lagrangian with F^ab = R^ab - e^a e^b/l^2 (torsion-free):
eps F^F = eps R^R - (2/l^2) eps R^e^e + (1/l^4) eps e^e^e^e
        = [Euler density, topological] - (2 cR/l^2) e R + (cV/l^4) e
        = -(2 cR/l^2) e [ R - cV/(2 cR l^2) ].
(the cross terms eps_abcd R^ab^e^c^e^d and eps_abcd e^a^e^b^R^cd are equal since 2-forms commute.)
Compare with Einstein-Hilbert with cosmological constant, e (R - 2 Lambda):
2 Lambda = cV/(2 cR l^2)  =>  Lambda = cV/(4 cR l^2) = 24/(8 l^2) = 3/l^2,
ell_from_lambda(Lam) = sqrt(cV/(4 cR Lam)) = sqrt(3/Lam).

Coupling: matching -(2 cR N/l^2) e R to the EH normalization (1/(16 pi G)) e R fixes
N = -l^2/(32 pi G cR); the dimensionless combination quoted by the contract is
mm_coupling = l^2/lP^2 = cV/(4 cR) / (lP^2 Lam) = 3/(lP^2 Lam). It is computed as
ell_from_lambda(Lam)^2 / lP^2 (so it uses the same derived ratio). Sign: N < 0 for cR > 0 is a
convention of the overall action sign; the contract asks for the positive ratio l^2/lP^2.

Second routes: (i) de Sitter's Ricci scalar from section 5 equals 12/l^2, and the vacuum Einstein
equation with Lambda gives R = 4 Lambda, so Lambda = 3/l^2 again; (ii) the Ricci contraction of F,
F^{ab}_{cb} (with E_b^nu), vanishes for SdS (Ric = (3/l^2) g) but equals -3/l^2 delta^a_c for
Schwarzschild (f = 1 - 2M/r, l only in the connection), i.e. F's Ricci part encodes exactly the
Einstein equation with Lambda = 3/l^2. Scaling: ell ~ Lam^{-1/2}, coupling ~ 1/Lam.

Nothing in this stage was quoted or looked up.

---------------------------------------------------------------------------------------------------
## 8. ricci_scalar(M, l, x)

Definition (SPEC section 6): R = E_a^mu E_b^nu R^{ab}_{mu nu}, with R^{ab} = d omega^{ab} + omega^a_c ^ omega^{cb}
the Lorentz curvature 2-form and indices raised with eta. Implementation: exactly the objects
action_coefficients already uses, with no new derivation of the curvature:
- f, f' of SdS from `_sds(M, l)`; tetrad and omega from `spin_connection`;
- R^{ab}_{mu nu} from `_riemann_up` (d omega by central differences of `spin_connection`, plus omega^omega,
  then the second index raised with eta^{cb});
- the contraction `_ricci_scalar` with the inverse diagonal tetrad E_a^mu = 1/e^a_mu (the same function
  action_coefficients divides by). So a wrong R^{ab} would show up here directly.

Closed form. From omega of section 3, Cartan's second equation gives the only independent components
(orthonormal frame, R^{ab}_{cd} = R^{ab}_{mu nu} E_c^mu E_d^nu):
  R^{01}_{01} = -f''/2,
  R^{02}_{02} = R^{03}_{03} = -f'/(2r),
  R^{12}_{12} = R^{13}_{13} = -f'/(2r),
  R^{23}_{23} = (1 - f)/r^2.
(e.g. R^0_1 = d(f'/2 dt) = (f''/2) dr^dt = -(f''/2) e^0^e^1, and R^0_1 = R^{01} since eta^{11} = 1, so
R^{01}_{01} = -f''/2; R^2_3 = d(-cos th dph) + omega^2_1^omega^1_3 = (sin th - f sin th) dth^dph = ((1-f)/r^2) e^2^e^3.)
R = sum_{a,b} R^{ab}_{ab} = 2 sum_{a<b} R^{ab}_{ab} = -f'' - 4f'/r + 2(1 - f)/r^2.
For f = 1 - 2M/r - r^2/l^2: f' = 2M/r^2 - 2r/l^2, f'' = -4M/r^3 - 2/l^2, so
  -f'' = 4M/r^3 + 2/l^2,  -4f'/r = -8M/r^3 + 8/l^2,  2(1-f)/r^2 = 4M/r^3 + 2/l^2,
  R = 12/l^2, independent of M, r, theta (the Schwarzschild part is Ricci-flat; Ric = (3/l^2) g).
Consistent with section 7: R = 4 Lambda with Lambda = 3/l^2. Sign: positive for de Sitter in this
convention (R^{ab} = +e^a^e^b/l^2 for the maximally symmetric space, F^{ab} = 0).
Scaling: R ~ 1/length^2, so (M, l, r) -> 2(M, l, r) divides R by 4.

Second route (printed under __main__, `_ricci_scalar_coordinate`): no tetrad, no spin connection.
Coordinate Christoffels Gamma^k_{ij} = (1/2) g^{kk}(d_i g_kj + d_j g_ki - d_k g_ij) of the diagonal metric by
central differences, R_ij = d_k Gamma^k_ij - d_j Gamma^k_ik + Gamma^k_kp Gamma^p_ij - Gamma^k_jp Gamma^p_ik,
R = g^{ii} R_ii. Self-check output (M, l) = (0.3, 7), (0.1, 4), (0, 5): tetrad route, coordinate route
(~1e-8 finite-difference agreement), the f-formula above and 12/l^2 all agree; scaling ratio 4.
