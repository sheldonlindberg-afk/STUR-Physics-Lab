# DERIVATION: stage `casimir` (build 2026-11-b)

Postulates: SPEC.md section 4. Numerics: `toolkit` (SPEC.md section 1). Measured numbers: `inputs.py` only
(HBAR, C_LIGHT, G_NEWTON, RHO_DIAMOND, EPS_DIAMOND), read inside functions. Written before the code.
Units: SI, with polarizabilities in units of 4 pi eps0 (so alpha is a volume, m^3), as SPEC section 4 states.

Provenance summary: `cp_energy` rests on the **quoted** fluctuation formula (allowed); everything else is derived.
Nothing could not be derived. One physical assumption is not in SPEC section 4 and is flagged in section 6
(the gravitational potential -G m^2/r used in the safe-gap criterion).

---------------------------------------------------------------------------------------------------------------

## 1. `sphere_K(eps)`: polarizability of a dielectric sphere, K = alpha / (4 pi eps0 R^3)

**Postulate** (SPEC 4, first bullet). Sphere of radius R, permittivity eps (relative), in a uniform applied field
E0 along z. Laplace's equation inside and outside; Phi and eps d_r Phi continuous at r = R.

**Solution.** The applied potential is -E0 r cos(theta), an l = 1 harmonic. The boundary conditions do not mix l,
so only l = 1 appears. The l = 1 solutions of Laplace's equation are r cos(theta) and cos(theta)/r^2.
Regular at the origin, and -> -E0 r cos(theta) at infinity:

    Phi_in  = -a E0 r cos(theta)                          (r < R)
    Phi_out = -E0 r cos(theta) + p' cos(theta) / r^2      (r > R),   p' = p / (4 pi eps0)

Phi_out's second term is the potential of a point dipole p. Write p' = K R^3 E0; then alpha/(4 pi eps0) = p'/E0
= K R^3, which is the definition of K. Dividing by E0 cos(theta) at r = R:

    continuity of Phi:            -a R = -R + K R            =>   a + K = 1
    continuity of eps d_r Phi:    -eps a = -1 - 2 K          =>   eps a - 2 K = 1

A 2x2 linear system for (a, K). Determinant D = (1)(-2) - (1)(eps) = -(eps + 2). Cramer's rule:

    K = det[[1, 1], [eps, 1]] / D = (1 - eps) / (-(eps + 2)) = (eps - 1) / (eps + 2)
    a = det[[1, 1], [1, -2]] / D = 3 / (eps + 2)

**Closed form.** K(eps) = (eps - 1)/(eps + 2) (Clausius-Mossotti form). Exact for rational eps.

**Implementation.** The code solves the 2x2 system by Cramer's rule in whatever arithmetic eps comes in
(Fraction/int -> Fraction; float -> float). The closed form is not typed in.

**Second route / checks.** (i) eps = 1: no sphere, K = 0. (ii) eps -> oo: conductor, the interior field a -> 0 and
K -> 1 (alpha = 4 pi eps0 R^3, the conducting-sphere result obtained independently by demanding Phi = const on
r = R: -E0 R + p'/R^2 = 0). (iii) Independent identity: the field inside is uniform, E_in = a E0, and the dipole
moment is the polarization times the volume, p = (eps - 1) eps0 E_in (4 pi R^3/3), so
K = (eps - 1) a / 3 = (eps - 1)/(eps + 2). `__main__` checks K == (eps - 1) a / 3 exactly, with a from the
same linear solve (it is a different equation: it uses the constitutive relation, not the boundary conditions).

---------------------------------------------------------------------------------------------------------------

## 2. `green_tensor(x, y, z, k)`

**Postulate** (SPEC 4, second bullet), taken as given, with r = |x|, u = k r, n = x/r:

    G_ij = e^(-u)/r^3 [ A(u) delta_ij - B(u) n_i n_j ],   A = 1 + u + u^2,   B = 3 + 3u + u^2.

**Where it comes from (consistency derivation, used as the second route).** With g(r) = e^(-k r)/r, which solves
(lap - k^2) g = 0 for r > 0, the field of a dipole at imaginary frequency is G_ij = (k^2 delta_ij - d_i d_j) g.
Using g' = -(1 + u) e^(-u)/r^2 and g'' = (2 + 2u + u^2) e^(-u)/r^3,

    d_i d_j g = (g'/r)(delta_ij - n_i n_j) + g'' n_i n_j = e^(-u)/r^3 [ -(1 + u) delta_ij + (3 + 3u + u^2) n_i n_j ],
    k^2 delta_ij g = u^2 e^(-u)/r^3 delta_ij,

so G_ij = e^(-u)/r^3 [(1 + u + u^2) delta_ij - (3 + 3u + u^2) n_i n_j]: the SPEC form. Consequences:
- every component obeys (lap - k^2) G_ij = 0 for r > 0 (derivatives commute with lap - k^2);
- k = 0: G_ij = (delta_ij - 3 n_i n_j)/r^3, the static dipole field (sign: energy-like, G_zz = -2/r^3 on the z axis);
- symmetric, traceless only at k = 0: Tr G = e^(-u) (3A - B)/r^3 = 2 u^2 e^(-u)/r^3.

**Implementation.** Direct evaluation; returns a 3x3 list of lists of floats. r = 0 raises ValueError.

**Second route.** `__main__` builds (k^2 delta_ij - d_i d_j) g by central finite differences of g = e^(-kr)/r
(four-point stencil for mixed derivatives) and compares with `green_tensor`.

---------------------------------------------------------------------------------------------------------------

## 3. `cp_integral()`: I = int_0^oo (1/2) r^6 Tr[G.G] du, exact

**Step 1: the trace.** n n is a projector (n.n = 1), so

    G.G = e^(-2u)/r^6 [ A^2 delta - 2AB nn + B^2 nn ],
    Tr[G.G] = e^(-2u)/r^6 [ 3A^2 - 2AB + B^2 ].

Expanding:
    3A^2  =  3 +  6u +  9u^2 + 6u^3 + 3u^4
    -2AB  = -6 - 12u - 14u^2 - 8u^3 - 2u^4        (AB = 3 + 6u + 7u^2 + 4u^3 + u^4)
    B^2   =  9 + 18u + 15u^2 + 6u^3 +  u^4
    sum   =  6 + 12u + 10u^2 + 4u^3 + 2u^4

    (1/2) r^6 Tr[G.G] = e^(-2u) P(u),   P(u) = 3 + 6u + 5u^2 + 2u^3 + u^4.

The integrand depends on u only (not on r or direction), so the integral is a pure number.

**Step 2: the integral.** int_0^oo u^n e^(-2u) du = n!/2^(n+1) (Gamma function; by n integrations by parts).

    I = 3 (1/2) + 6 (1/4) + 5 (2/8) + 2 (6/16) + 1 (24/32) = 3/2 + 3/2 + 5/4 + 3/4 + 3/4 = 23/4.

**Closed form.** I = 23/4.

**Implementation.** The code does not type 23/4. It holds A and B as integer coefficient lists (the SPEC
postulate), forms 3A^2 - 2AB + B^2 by exact polynomial multiplication, and sums c_n n!/2^(n+1)/2 with Fractions.

**Second routes.** (a) Eigenvalues: G has eigenvalue A (twice, transverse) and A - B = -2(1 + u) (once, along n),
so Tr G^2 = 2A^2 + 4(1+u)^2 = 6 + 12u + 10u^2 + 4u^3 + 2u^4: same polynomial, checked exactly in `__main__` by a
separate polynomial computation. (b) Numerical: `toolkit.trapezoid` of (1/2) r^6 sum_ij G_ij G_ji computed from
`green_tensor` at an oblique point, u in [0, 40] (tail e^(-80)); must reproduce I to ~1e-7.

---------------------------------------------------------------------------------------------------------------

## 4. `cp_energy(R1, R2, K1, K2, r)`: retarded Casimir-Polder energy, constant alpha

**Quoted** (SPEC 4, third bullet; allowed): U = -(hbar/2 pi) int_0^oo d xi alpha1 alpha2 Tr[G.G], alpha in units
of 4 pi eps0, G at k = xi/c. Source: Casimir and Polder, Phys. Rev. 73 (1948) 360; in this Green-tensor form
e.g. Craig and Thirunamachandran, *Molecular Quantum Electrodynamics* (1984), ch. 7. Not derived here.

**From the quoted formula to the closed form (derived).** Constant (static) alpha_i = K_i R_i^3 (section 1).
Substituting xi = c u / r, d xi = (c/r) du, and Tr[G.G] = 2 e^(-2u) P(u)/r^6 (section 3):

    U = -(hbar/2 pi) alpha1 alpha2 (c/r) (2/r^6) int_0^oo e^(-2u) P(u) du
      = -(hbar c / pi) I alpha1 alpha2 / r^7
      = -(hbar c / pi) I K1 K2 R1^3 R2^3 / r^7,        I = cp_integral().

With I = 23/4 this is U = -23 hbar c alpha1 alpha2 / (4 pi r^7).

**Units.** hbar c: J m; alpha1 alpha2: m^6; / r^7: m^-7 -> J. Attractive (U < 0), ~ R1^3 R2^3 / r^7, linear in hbar.

**Validity (not enforced).** Constant alpha means the retarded regime, r >> c/omega_0 of the material, and point
dipoles means r >> R1, R2.

**Second route.** `__main__` evaluates the quoted formula directly as a xi-integral in SI, with
`green_tensor(0, 0, r, xi/c)` and `toolkit.trapezoid`, and compares with the closed form.

---------------------------------------------------------------------------------------------------------------

## 5. `diamond_radius(m)`

Uniform sphere: m = rho (4 pi/3) R^3  =>  R = (3 m / (4 pi rho))^(1/3), rho = inputs.RHO_DIAMOND.
Second route: `__main__` recomputes the mass from the volume and checks R ~ m^(1/3), R ~ rho^(-1/3).

---------------------------------------------------------------------------------------------------------------

## 6. `casimir_safe_gap(m, dx, tau, fraction)`

**Postulate** (SPEC 4, last bullet). Branch distances d_LL = d_RR = g (the gap), d_LR = d_RL = d = sqrt(g^2 + dx^2).
Entangling phase of a potential U: phi[U] = (tau/hbar) [ -U(d_LL) - U(d_RR) + U(d_LR) + U(d_RL) ]
= (2 tau/hbar) [ U(d) - U(g) ].

**Casimir phase.** Two identical diamonds: R = diamond_radius(m), K = sphere_K(inputs.EPS_DIAMOND),
U_C(r) = -C/r^7 with C = (hbar c/pi) I K^2 R^6 = -cp_energy(R, R, K, K, r) r^7 (section 4):

    phi_C = (2 tau/hbar) C (g^-7 - d^-7)  > 0.

**Gravity phase.** U_G(r) = -G m^2/r:   phi_G = (2 tau/hbar) G m^2 (g^-1 - d^-1) > 0.
(*Assumption flagged:* SPEC section 4 does not state the gravitational potential; Newton's -G m^2/r is used. It is
derived from graviton exchange only in the later stage `graviton`, which this stage cannot import. See QUESTIONS.)

**Ratio.** With a = 1/g, b = 1/d (0 < b < a), using a^7 - b^7 = (a - b) sum_{j=0}^{6} a^(6-j) b^j:

    rho(g) = phi_C/phi_G = (C / (G m^2)) S(g),      S(g) = sum_{j=0}^{6} g^-(6-j) d^-j .

- tau and hbar/tau cancel: the gap is independent of tau.
- C ~ R^6 ~ m^2 (section 5), so C/(G m^2) is independent of m: the gap is independent of m.
- C/(G m^2) = (hbar c/(pi G)) I K^2 (3/(4 pi rho))^2: depends only on constants, eps and rho.
- The factored form has no cancellation (the direct differences g^-1 - d^-1 lose digits when dx << g).

**Monotonic, so the criterion is a single root.** Both a = 1/g and b = (g^2 + dx^2)^(-1/2) decrease strictly
with g, and S is a sum of products of positive powers of a and b; so rho(g) is strictly decreasing, from +oo
(g -> 0) to 0 (g -> oo). Hence {g : rho(g) <= fraction} = [g*, oo) and the smallest safe gap g* is the unique
root of

    h(g) = rho(g) - fraction = 0.

**Bracket (derived, not guessed).** Since 0 < b < a: a^6 < S < 7 a^6, i.e. g^-6 < S < 7 g^-6. With
g0 = (C/(fraction G m^2))^(1/6):

    rho(g0) > fraction                      (S > g^-6)          -> h(g0) > 0
    rho(7^(1/6) g0) < fraction              (S < 7 g^-6)        -> h(7^(1/6) g0) < 0

so g* lies in (g0, 7^(1/6) g0). The two ends are the limits dx >> g (far branches irrelevant: g* -> g0) and
dx << g (expansion: g^-7 - d^-7 ~ 7 dx^2/(2 g^9), g^-1 - d^-1 ~ dx^2/(2 g^3), ratio 7 C/(G m^2 g^6):
g* -> 7^(1/6) g0). The bracket is widened by a factor (1 -+ 1e-9) against rounding at the ends.

**Root finding.** `toolkit.bisect(h, lo, hi)` (contract.CONNECTIONS T-casimir); it runs to floating-point
resolution, far below the 1e-6 relative precision SPEC demands.

**Not enforced.** g* >= 2R (spheres not overlapping) and g* >> R (point-dipole regime) are not imposed; the
function returns the root of the stated criterion. `__main__` prints g*/R so the regime can be seen.

**Second routes.** (a) At the returned gap, recompute the ratio the "direct" way, from four calls of `cp_energy`
and the unfactored gravity differences, and check it equals `fraction`. (b) Check g0 < g* < 7^(1/6) g0 and the two
limits: dx -> large gives g*/g0 -> 1, dx -> small gives g*/g0 -> 7^(1/6). (c) An independent solver: Newton
iteration on ln rho(g) = ln fraction in ln g with a numerical derivative, started from g0, compared with the
bisection root. (d) m- and tau-independence.
