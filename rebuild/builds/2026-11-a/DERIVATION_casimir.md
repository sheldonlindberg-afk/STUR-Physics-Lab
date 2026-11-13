# DERIVATION: casimir (SPEC.md sections 0, 4 and "Connections between stages")

Postulates used (SPEC.md section 4 unless stated):
- (P1) electrostatics of a dielectric sphere (permittivity eps, radius R) in a uniform field E0:
  lap Phi = 0 inside and outside, Phi continuous at r = R, eps_in d_r Phi_in = eps_out d_r Phi_out
  (eps_out = 1), Phi -> -E0 r cos(theta) at infinity, Phi regular at r = 0;
- (P2) the dipole Green tensor at imaginary frequency xi, k = xi/c, u = k r:
  G_ij = e^{-u}/r^3 [(1+u+u^2) delta_ij - (3+3u+u^2) x_i x_j / r^2];
- (P3, QUOTED, Casimir & Polder, Phys. Rev. 73 (1948) 360) U = -(hbar/2pi) int_0^oo dxi a1 a2 Tr[G.G],
  a in units of 4 pi eps0 (a volume), constant a (static limit);
- (P4) safe-gap geometry and the entangling phase (tau/hbar)[-U(d_LL) - U(d_RR) + U(d_LR) + U(d_RL)],
  d_LL = d_RR = gap, d_LR = d_RL = sqrt(gap^2 + dx^2); the safe gap is the smallest gap with
  |phase_Casimir| <= fraction |phase_gravity|, found as a root to relative precision <= 1e-6;
- (P5) gravity between the two diamonds: the static potential U_g(r) = -G m^2 / r. In the ladder
  this is -4 pi G m1 m2 chiral.yukawa(r, 0) (SPEC "Connections", rung 2 -> 4, derived and
  connection-checked in stage graviton); see QUESTIONS casimir 1 for why this stage writes 1/r.
- Inputs: inputs.EPS_DIAMOND, RHO_DIAMOND, HBAR, C_LIGHT, G_NEWTON, read at call time.
SPEC.md section 0: only `cp_energy`'s fluctuation formula (P3) is quoted. Everything else is derived.
Numerics: toolkit.bisect (root), toolkit.trapezoid (second route of the integral).

---

## 1. `sphere_K(eps)` = alpha / (4 pi eps0 R^3)

Separation of variables, l = 1 only (the source -E0 r cos(theta) is pure l = 1; all other l are
forced to zero by regularity at 0, decay at infinity and the homogeneous matching conditions):

    Phi_in  = -B r cos(theta)                        (regular at 0)
    Phi_out = -E0 r cos(theta) + A cos(theta) / r^2  (uniform field + induced dipole)

Write a = A/(E0 R^3), b = B/E0 (dimensionless unknowns). At r = R:

    continuity:      -B R = -E0 R + A/R^2              =>   a + b = 1
    eps d_r Phi:     -eps B = -E0 - 2A/R^3              =>   2a - eps b = -1

Linear system M (a, b)^T = (1, -1)^T with M = [[1, 1], [2, -eps]], det M = -(eps + 2). The code
solves it by Gaussian elimination in exact arithmetic (Fraction in, Fraction out; a float eps
runs the same algebra in floats). Result:

    a = (eps - 1)/(eps + 2),   b = 3/(eps + 2).

The induced dipole potential is p cos(theta)/(4 pi eps0 r^2), so p/(4 pi eps0) = A = a E0 R^3 and

    K = alpha/(4 pi eps0 R^3) = a = (eps - 1)/(eps + 2)     (Clausius-Mossotti form, not typed in).

**Second route (independent: bound charge, not boundary matching).** Inside, the field is uniform,
E_in = b E0. The polarization P = eps0 (eps - 1) E_in is uniform, so the sphere's dipole is
p = P (4/3) pi R^3, i.e. p/(4 pi eps0 E0 R^3) = (eps - 1) b / 3. Checked exactly: (eps-1) b/3 == a.
Limits: eps = 1 gives K = 0 (no sphere); eps -> oo gives K -> 1 (conductor, p = 4 pi eps0 R^3 E0);
K < 1 for every finite eps.

---

## 2. `green_tensor(x, y, z, k)`

**Derivation.** Let f(r) = e^{-k r}/r. For r > 0, (lap - k^2) f = (1/r) d^2(r f)/dr^2 - k^2 f
= (1/r) k^2 e^{-kr} - k^2 f = 0 (the imaginary-frequency Helmholtz equation, obtained from
(lap + omega^2/c^2) at omega = i xi). Define

    G_ij = (k^2 delta_ij - d_i d_j) f.                                            (2.1)

Because d_i d_j commutes with lap, (lap - k^2) G_ij = (k^2 delta_ij - d_i d_j)(lap - k^2) f = 0 for
r > 0: G solves the imaginary-frequency wave equation; it is transverse-projected
(the electric field of an oscillating dipole, continued to omega = i xi). With
d_i d_j f = (f'/r) delta_ij + (f'' - f'/r) x_i x_j / r^2:

    f'  = -e^{-kr}(1 + u)/r^2,       f'' = e^{-kr}(2 + 2u + u^2)/r^3,
    k^2 f - f'/r = e^{-u}/r^3 (u^2 + 1 + u),
    f'' - f'/r   = e^{-u}/r^3 (2 + 2u + u^2 + 1 + u) = e^{-u}/r^3 (3 + 3u + u^2),

so G_ij = e^{-u}/r^3 [(1+u+u^2) delta_ij - (3+3u+u^2) x_i x_j/r^2], exactly P2. The code
reproduces these two polynomials SYMBOLICALLY (module helper `_green_polys`): it represents
functions e^{-kr} sum c_{pq} k^p r^q, differentiates them term by term, forms k^2 f - f'/r and
f'' - f'/r, multiplies by r^3 e^{kr}, checks that every monomial collapses to u^p = (kr)^p, and
returns the coefficient lists a(u) = [1, 1, 1], b(u) = [3, 3, 1]. `green_tensor` evaluates
G = e^{-u}/r^3 [a(u) delta - b(u) n n] with those derived polynomials.

**Second routes.** (i) Finite-difference Laplacian: (lap - k^2) G = 0 at a generic point
(Richardson-extrapolated second differences), as the blind check does. (ii) Static limit k = 0:
G = (delta - 3 n n)/r^3, the static dipole-dipole tensor (field of a unit dipole). (iii) Build
(2.1) directly by finite differences of the scalar f and compare with the closed form.

---

## 3. `cp_integral()` = int_0^oo Tr[G.G] r^6 / 2 du (exact Fraction)

**Structure of G.** G = (e^{-u}/r^3)[a delta - b n n], |n| = 1. The matrix a 1 - b n n has eigenvalue
a - b on n and a on the two transverse directions, hence

    Tr[G.G] r^6 = e^{-2u} [ (a - b)^2 + 2 a^2 ].

The code computes Tr[G.G] without that eigenvalue shortcut: it takes the exact rational unit
vector n = (2, 3, 6)/7, forms the 3x3 matrix of polynomials a delta_ij - b n_i n_j (Fraction
coefficients), and evaluates sum_ij G_ij G_ji by polynomial multiplication. Both give

    h(u) = Tr[G.G] r^6 e^{2u} / 2 = (1+u+u^2)^2 + 2(1+u)^2
         = 3 + 6u + 5u^2 + 2u^3 + u^4                     (a - b = -2(1+u)).

**Integral.** I_n = int_0^oo u^n e^{-2u} du: integration by parts, I_n = (n/2) I_{n-1}, I_0 = 1/2,
so I_n = n!/2^{n+1}. Term by term, in Fractions:

    cp_integral = sum_n h_n n!/2^{n+1}
                = 3(1/2) + 6(1/4) + 5(2/8) + 2(6/16) + 1(24/32).

(The value is printed by the self-check, not written here.)

**Second route.** Numerical quadrature: toolkit.trapezoid of (1/2) Tr[G.G] r^6 with G taken from
the floating `green_tensor` at r = 1 along an arbitrary direction, u in [0, 60], step 1e-3, plus
Richardson (h, h/2) to remove the O(h^2) error; must agree with the Fraction to ~1e-9.

---

## 4. `cp_energy(R1, R2, K1, K2, r)`

alpha_i/(4 pi eps0) = K_i R_i^3 (section 1). In P3, xi = c k = c u / r, d xi = (c/r) du, and
Tr[G.G] = (2/r^6) h(u) e^{-2u}. So

    U = -(hbar/2pi) (K1 R1^3)(K2 R2^3) (c/r)(2/r^6) int_0^oo h e^{-2u} du
      = -(hbar c / pi) cp_integral() K1 K2 R1^3 R2^3 / r^7.

The code evaluates exactly this, with cp_integral() (the Fraction) called at run time and
hbar, c read from inputs at call time.

**Second routes.** Scaling U ~ R1^3 R2^3 / r^7 (doubling r divides by 2^7, doubling R1
multiplies by 8), U < 0 (attractive), U ~ hbar. Direct numerical xi-integration of P3 in physical
units (trapezoid in xi with G from `green_tensor`) reproduces the closed form.

---

## 5. `diamond_radius(m)`

m = rho (4/3) pi R^3  =>  R = (3 m / (4 pi rho))^{1/3}, rho = inputs.RHO_DIAMOND at call time.
Second route: (4/3) pi R^3 rho == m back-substituted; R ~ m^{1/3}, R ~ rho^{-1/3}.

---

## 6. `casimir_safe_gap(m, dx, tau, fraction)`

**Phases.** For any central potential U, P4 gives
phase[U] = (tau/hbar)[-2U(g) + 2U(d)], g = gap, d = sqrt(g^2 + dx^2). Two equal diamonds:
R = diamond_radius(m), K = sphere_K(inputs.EPS_DIAMOND).

    Casimir: U_c(r) = cp_energy(R, R, K, K, r) = -C / r^7,  C = (hbar c/pi) I K^2 R^6,
    gravity: U_g(r) = -G m^2 / r.

phase_c = (2 tau/hbar) C (g^-7 - d^-7),  phase_g = (2 tau/hbar) G m^2 (g^-1 - d^-1), both > 0.

**Ratio and its properties.** rho(g) = |phase_c|/|phase_g| = C (g^-7 - d^-7) / (G m^2 (g^-1 - d^-1)).
- tau cancels (both phases are tau/hbar times an energy difference).
- R^6 ~ m^2 (section 5), so C ~ m^2 cancels G m^2: rho is mass-independent. (This is why the
  safe gap depends only on dx, fraction, eps, rho_diamond, G, hbar, c.)
- Monotonicity. With y = d/g > 1, (g^-7 - d^-7)/(g^-1 - d^-1) = d^-6 (y^7 - 1)/(y - 1)
  = sum_{j=0}^{6} g^{-j} d^{j-6}. Every term is non-increasing in g (g^{-j} with j >= 0 and
  d^{j-6} with j - 6 <= 0, d increasing in g), and the j = 0 term d^-6 is strictly decreasing.
  So rho is strictly decreasing, rho -> oo as g -> 0 and rho -> 0 as g -> oo: the set
  {g : rho(g) <= fraction} is [g*, oo), and the smallest safe gap is the unique root
  rho(g*) = fraction.
- Bracket. Writing x = dx/g, rho g^6 G m^2 / C = (1 - (1+x^2)^{-7/2})/(1 - (1+x^2)^{-1/2}) =
  sum_{j=0}^6 y^{j-6} in (1, 7) (each term of the sum is <= 1 since y > 1, and > 0). Hence with
  g0 = (C/(fraction G m^2))^{1/6}: rho(g0) > fraction and rho(7^{1/6} g0) < fraction. The root
  lies in [g0, 7^{1/6} g0]; the code widens the bracket by factors of 2 if a sign test ever fails
  (it never should).

**Root.** toolkit.bisect on F(g) = |phase_c(g)| - fraction |phase_g(g)| in log form
F(g) = ln rho(g) - ln fraction (same root, better scaled), where the phases are formed
literally from cp_energy and U_g at the four branch distances. toolkit.bisect halves to machine
precision (relative ~1e-16 >> 1e-6 requirement).

**Second route.** (i) Closed-form ratio using the geometric sum (no subtraction):
rho(g*) recomputed as C/(G m^2) sum_j g^-j d^(j-6) must equal fraction. (ii) Mass and time
independence: the root for (m, tau) and (10 m, 3.6 tau) agree. (iii) Far-gap limit
(g >> dx): rho -> 7 C/(G m^2 g^6), near-gap limit (g << dx): rho -> C/(G m^2 g^6), bracketing g*.

---

## Self-check output requested

Design A (inputs.DESIGN_A_MASS) at r = 200 um: energy ratio |U_c|/|U_g| = C/(G m^2 r^6), printed
both from cp_energy/U_g and from the closed form. Safe gap for the baseline inputs.GAP_BASELINE_*
with inputs.GAP_FRACTION, printed together with its second routes.

Nothing in this stage was left underived except P3 (quoted, allowed).
