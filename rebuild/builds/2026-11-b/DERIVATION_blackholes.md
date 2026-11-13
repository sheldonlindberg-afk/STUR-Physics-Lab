# DERIVATION: stage `blackholes` (build 2026-11-b)

Black holes of the static metrics of rung 5, and Kerr. Postulates: SPEC.md section 7 (cited as S7), the
metrics of section 6 (S6), the connections list (S-conn) and `contract.py`. Written before the code.

Units. G = c = 1 for the geometry (M, l, r are lengths) in `sds_horizons`, `killing_kappa`,
`kappa_from_spin_connection`, `euclidean_cone_ratio`, `kerr_first_law`, `photon_sphere`, `isco`. SI for
`nariai_mass_kg`, `shadow_uas`, `kerr_area_km2`, `qnm_220`, `invert_220`, `hawking_K`; every SI constant is
read from `inputs` at call time.

Conventions: x = (t, r, theta, phi), signature (-, +, +, +), a prime is d/dr.
Metric (S6): ds^2 = -f dt^2 + dr^2/f + r^2 (dtheta^2 + sin^2 theta dphi^2).

Quoted (allowed by the stage): the Berti-Cardoso-Will fit (`qnm_220`, `invert_220`) and the Hawking
temperature as a radiation temperature (`hawking_K`). The Kerr thermodynamic quantities S, T, Omega, J are
postulates of S7 (Bardeen-Carter-Hawking); what is derived in `kerr_first_law` is that they satisfy the first
law and Smarr's relation identically. Nothing else is assumed.

---

## 1. `sds_horizons(M, l)`

**Postulate** (S6): f(r) = 1 - 2M/r - r^2/l^2, M > 0, l > 0. Horizons are the positive roots of f.

1. f -> -infinity for r -> 0+ and for r -> infinity. f' = 2M/r^2 - 2r/l^2 and f'' = -4M/r^3 - 2/l^2 < 0, so f
   is concave on r > 0 with a single maximum at r0 where f'(r0) = 0:
       r0^3 = M l^2.
2. At r0, r0^2/l^2 = M/r0, so f(r0) = 1 - 3M/r0 = 1 - 3 (M/l)^(2/3).
3. Hence: two positive roots r_b < r0 < r_c iff f(r0) > 0 iff M/l < 1/sqrt(27) (the Nariai bound); they merge
   at r0 = 3M when M/l = 1/sqrt(27); no horizon (f < 0 everywhere, no static region) beyond it.
4. Brackets with a guaranteed sign change: f(2M) = -4M^2/l^2 < 0 and f(l) = -2M/l < 0, and
   2M < r0 < l whenever f(r0) > 0 (since f(2M) < 0 < f(r0) > f(l), and f is concave). So
       r_b = root in [2M, r0],  r_c = root in [r0, l],   2M < r_b < 3M < r_c < l,
   found with `toolkit.bisect`. (r0 < 3M... precisely: f(r0) > 0 means r0 > 3M; r_b < 3M follows from
   f(3M) = 1/3 - 9M^2/l^2 > 0 under the bound and r_b being the smaller root.)
5. Return value: `None` if f(r0) < 0. If f(r0) == 0 exactly in floating point (the degenerate Nariai case)
   the double root (r0, r0) is returned. M <= 0 or l <= 0 raises `ValueError` (no black hole).

**Second route.** r f = 0 is the depressed cubic r^3 - l^2 r + 2 M l^2 = 0. With r = (2l/sqrt3) cos(phi),
4cos^3 - 3cos = cos(3 phi) gives cos(3 phi) = -sqrt(27) M/l, so
    r_k = (2l/sqrt3) cos( (1/3) arccos(-sqrt(27) M/l) - 2 pi k/3 ),  k = 0, 1, 2:
k = 0 is r_c, k = 1 is r_b (k = 2 is the negative root; the three sum to zero, no r^2 term). The self-check
prints both, and also Vieta's r_b + r_c + r_- = 0, r_b r_c r_- = -2 M l^2.

## 2. `killing_kappa(f, r0, h)`

**Postulates** (S7): xi = d/dt, kappa^2 = -(1/2)(nabla_mu xi_nu)(nabla^mu xi^nu); Christoffel symbols from the
metric, using f only (never f').

Derivation of what the code computes (no analytic derivative of f is used anywhere in the code):
1. g_{mu nu}(r, theta) = diag(-f, 1/f, r^2, r^2 sin^2 theta); the inverse is the reciprocal diagonal.
2. d_lambda g_{mu nu} by central differences: step h in r, a fixed dimensionless step in theta, zero in t, phi.
3. Gamma^lambda_{mu nu} = (1/2) g^{lambda sigma} (d_mu g_{sigma nu} + d_nu g_{sigma mu} - d_sigma g_{mu nu}).
4. xi^mu = (1, 0, 0, 0), xi_nu = g_{nu t}; nabla_mu xi_nu = d_mu xi_nu - Gamma^lambda_{mu nu} xi_lambda, with
   d_mu xi_nu = d_mu g_{nu t} from the same difference table.
5. kappa^2 = -(1/2) g^{mu alpha} g^{nu beta} (nabla_mu xi_nu)(nabla_alpha xi_beta).

Closed form (used only as the check, section "second route"): the only nonzero Gamma^t are
Gamma^t_{tr} = f'/(2f). Then
    nabla_r xi_t = d_r(-f) - Gamma^t_{rt}(-f) = -f' + f'/2 = -f'/2,
    nabla_t xi_r = -Gamma^t_{tr}(-f) = +f'/2          (antisymmetric: Killing's equation holds),
    (nabla xi)^2 = 2 g^{tt} g^{rr} (f'/2)^2 = 2 (-1/f)(f)(f'^2/4) = -f'^2/2,
    kappa^2 = f'^2/4,   kappa = |f'(r0)|/2.
The 1/f in g^{tt} cancels the f in g^{rr}: the scalar is regular at the horizon, and its horizon value is the
surface gravity. For Schwarzschild kappa(r0) = M/r0^2 -> 1/(4M) at r0 = 2M: positive, ~ 1/M, and changing the
sample point from 2M(1 + 1e-6) to 2M(1 + 1e-5) changes it by 2e-5 relative only.

Numerical error: f is known to ~1e-16 absolute, so f' from a central difference with h = 1e-8 r has error
~1e-8/r, i.e. ~1e-7 relative; truncation h^2 f'''/6 is negligible.

**Second route.** (a) |f'|/2 with f' from a 5-point stencil (self-check). (b) Rung 5's spin connection,
section 3. (c) The Euclidean period, section 4. (d) Symmetric part of nabla_mu xi_nu must vanish (Killing).

## 3. `kappa_from_spin_connection(M, l)`

**Postulates** (S-conn, S7 conventions): kappa = |omega^0_{1 t}| from `desitter.spin_connection`, evaluated at
r_b (1 + 1e-9) and r_c (1 - 1e-9), the horizons from `sds_horizons`.

Why this is the surface gravity: rung 5's torsion-free connection for the tetrad e^0 = sqrt(f) dt,
e^1 = dr/sqrt(f) has de^0 = (f'/(2 sqrt f)) dr ^ dt = -omega^0_1 ^ e^1, so omega^0_1 = (f'/2) dt, i.e.
omega^0_{1 t} = f'/2. Section 2 gave kappa = |f'|/2. So |omega^0_{1 t}| at the horizon is kappa; it is the
boost rate, per unit Killing time, of the static frame. On r_b, f' > 0; on r_c, f' < 0; the absolute value is
taken. The function passes f and its analytic derivative f' = 2M/r^2 - 2r/l^2 to rung 5 (rung 5's signature
requires f'); this is independent of section 2, where no f' is used.
If there are no horizons (`sds_horizons` returns None) a `ValueError` is raised.

**Second route.** `killing_kappa` on the same f (the harness's check), and the closed form from the roots:
writing f = -(r - r_b)(r - r_c)(r - r_-)/(l^2 r), kappa_b = (r_c - r_b)(r_b - r_-)/(2 l^2 r_b),
kappa_c = (r_c - r_b)(r_c - r_-)/(2 l^2 r_c), with r_- = -(r_b + r_c).

## 4. `euclidean_cone_ratio(f, rh, beta, eps)`

**Postulates** (S7): t = -i tau; proper radial distance rho = integral dr/sqrt(f).

1. With t = -i tau the (t, r) part becomes f dtau^2 + dr^2/f, positive definite where f > 0.
2. tau is periodic with period beta. The circle r = r_h + eps has circumference C = beta sqrt(f(r_h + eps)).
3. Its proper radius, measured from the horizon (the fixed point of d/dtau), is
   rho = | integral_{r_h}^{r_h + eps} dr/sqrt(f) |.
4. The export is C/(2 pi rho). eps may be negative (cosmological horizon, static side is r < r_c).
5. Near a simple zero, f = f'(r_h) x + ..., x = r - r_h: rho = 2 sqrt(x/f'), sqrt(f) = sqrt(f' x) = (f'/2) rho,
   so the metric is dρ^2 + (kappa rho)^2 dtau^2 with kappa = |f'(r_h)|/2: flat polar coordinates with angle
   kappa tau. C/(2 pi rho) -> kappa beta/(2 pi): 1 (smooth) iff beta = 2 pi/kappa, a cone otherwise
   (ratio 1.3 for a period 1.3 times too long). Corrections are O(eps f''/f').

Numerics. The integrand 1/sqrt(f) has an integrable inverse-square-root singularity at r_h. Substituting
r = r_h + eps u^2, rho = |eps| integral_0^1 2u du/sqrt(f(r_h + eps u^2)) = integral_0^1 g(u) du with
g(u) = 2 |eps| u / sqrt(f(r_h + eps u^2)), which is smooth and a function of u^2 only (g -> 2 sqrt(|eps/f'|)
at u = 0). Because g is even, integral_0^1 g = (1/2) integral_{-1}^{1} g; the trapezoid rule
(`toolkit.trapezoid`) on an even number n of equally spaced nodes over [-1, 1] never samples u = 0 (where g
is 0/0), and its error is (dx^2/12)(g'(1) - g'(-1)) = (dx^2/6) g'(1), with g'(1) ~ -g eps f''/(2f') small.
n = 200. Rounding: at the innermost nodes f ~ f' eps u^2 is small, but the relative noise there
(1e-16/(f' eps u^2)) on 2 nodes of 200 is < 1e-6 for eps >= 1e-7 r_h.
If f <= 0 at a node (eps on the wrong side) a `ValueError` is raised.

**Second route.** Schwarzschild in closed form: rho = sqrt(r(r - 2M)) + 2M ln( sqrt(r/2M) + sqrt(r/2M - 1) )
(differentiate: d rho/dr = sqrt(r/(r - 2M))); and the limit kappa beta/(2 pi) with kappa from section 2.

## 5. `kerr_first_law(p, q, dp, dq)`

**Postulates** (S7, quoted there from Bardeen-Carter-Hawking): p = r_+, q = r_-, M = (p + q)/2, a^2 = p q,
S = pi (p^2 + a^2), T = (p - q)/(4 pi (p^2 + a^2)), Omega = a/(p^2 + a^2), J = M a.

Everything must be exact (Fractions), but a = sqrt(pq) and pi are irrational. Both drop out:
- X := p^2 + a^2 = p (p + q)  (rational).
- T dS = (p - q)/(4 pi X) . pi dX = (p - q) dX/(4 X).            (pi cancels)
- Omega dJ: J dJ = d(J^2)/2 so dJ = d(J^2)/(2 M a), and Omega dJ = (a/X) d(J^2)/(2 M a) = d(J^2)/(2 M X),
  with J^2 = M^2 a^2 = M^2 p q rational.                           (a cancels)
  At q = 0, dJ = d(J^2)/(2Ma) diverges along dq (a = 0), but Omega dJ = d(J^2)/(2MX) is finite: this is the
  finite limit S7's convention asks for.
- 2 T S = (p - q)/2; 2 Omega J = 2 M a^2/X.

The differentials along the direction (dp, dq) are directional derivatives d/ds at s = 0 of
M(s), X(s), J^2(s) with p -> p + s dp, q -> q + s dq, taken exactly with `toolkit.exact_derivative`
(dual numbers over Fractions); the code does not contain the expanded differentials.

    first = dM - (p - q) dX/(4X) - d(J^2)/(2 M X),      smarr = M - (p - q)/2 - 2 M p q/X.

By hand (the proof that both vanish): dM = (dp + dq)/2, dX = (2p + q) dp + p dq,
d(J^2) = 2 M p q dM + M^2 (q dp + p dq), so Omega dJ = [p q (dp + dq)/2 + (p + q)(q dp + p dq)/4]/X.
X . first, coefficient of dp:  p(p+q)/2 - (p-q)(2p+q)/4 - pq/2 - (p+q)q/4
   = p^2/2 - (2p^2 - pq - q^2)/4 - (pq + q^2)/4 = 0.
coefficient of dq:  p(p+q)/2 - (p-q)p/4 - pq/2 - (p+q)p/4 = p^2/2 - p^2/4 + pq/4 - p^2/4 - pq/4 = 0.
smarr = (p+q)/2 - (p-q)/2 - pq(p+q)/(p(p+q)) = q - q = 0.
So both residuals are identically zero for all p > 0, q >= 0 and all directions.

**Second route.** Floating point with the irrational quantities kept: M, S, J, T, Omega as floats (math.sqrt,
math.pi), dS and dJ by central differences along (dp, dq); the residual must be ~1e-9. Negative control: the
same residual with T replaced by 2T (or the code's exact residual with S -> pi p^2) is not zero.

## 6. `nariai_mass_kg(Lam)`

**Postulates** (S-conn): l = `desitter.ell_from_lambda(Lam)` (rung 5: l = sqrt(3/Lambda)); section 1.

From section 1, horizons exist iff M/l <= 1/sqrt(27) in G = c = 1. The geometric mass is G m/c^2, so
    m_max = l c^2/(sqrt(27) G) = c^2/(3 G sqrt(Lambda)).
Scalings: ~ Lambda^(-1/2), ~ 1/G.

**Second route.** Numerically: with M = G m_max/c^2 the maximum of f (at f' = 0, found by bisection) must be
zero, and `sds_horizons` must flip from a pair to None across the bound; also r0 = 3M = l/sqrt3.

## 7. `photon_sphere()`

**Postulates** (S7): photons have the effective potential W(r) = f/r^2; M = 1, f = 1 - 2/r.

Null geodesics in the equatorial plane with E = f dt/dlambda, L = r^2 dphi/dlambda:
0 = -E^2/f + (dr/dlambda)^2/f + L^2/r^2, so (dr/dlambda)^2 = E^2 - L^2 W(r), i.e. with b = L/E,
(dr/dlambda)^2/L^2 = 1/b^2 - W(r). A circular photon orbit sits at W' = 0; it is the maximum of W (W -> 0 at
r = 2 and at infinity, W > 0 between). A ray from infinity is captured iff 1/b^2 > W_max, so the critical
impact parameter is b_c = 1/sqrt(W_max).

Numerics: (i) `toolkit.golden_max` on W over [2, 20] (W is unimodal there). Golden section locates a smooth
maximum only to ~sqrt(machine eps) in r. (ii) Polish: the root of W'(r) in [r_g - w, r_g + w] by
`toolkit.bisect`, where W' is the exact derivative from `toolkit.exact_derivative` (dual numbers, r converted
exactly to a Fraction). No closed form is used. If the polish bracket has no sign change, the golden-section
value is kept. b = 1/sqrt(W(r)).

**Second route (closed form).** W' = f'/r^2 - 2f/r^3 = 0 gives r f' = 2 f: 2/r = 2 - 4/r, r = 3 (= 3M);
W_max = (1/3)/9 = 1/27, b_c = sqrt(27) M. Printed next to the numerical values.

## 8. `isco()`

**Postulates** (S7): massive particles have V(r) = f (1 + L^2/r^2); M = 1.

Timelike geodesics: -1 = -E^2/f + rdot^2/f + L^2/r^2, so rdot^2 = E^2 - V(r). Circular orbit: V' = 0 and
E^2 = V. Stable iff V'' > 0. The ISCO is the circular orbit with V'' = 0.

V' = 0 is linear in L^2: V = f + L^2 W, with W = f/r^2 of section 7, so the circular orbit at radius r has
    L^2(r) = -f'(r)/W'(r)        (positive for r beyond the photon sphere, where W' < 0; -> infinity at the
                                  photon sphere and, ~ r, at infinity).
Differentiating V'(r; L^2(r)) = 0 along the family: V'' + W' dL^2/dr = 0. Since W' != 0, V'' = 0 iff
dL^2/dr = 0: the ISCO is the minimum of L^2(r) over circular orbits (below that L^2 no circular orbit exists).

Numerics: f' and W' exactly by `toolkit.exact_derivative`, so L^2(r) is an exact rational at a rational r.
The minimum is located as the sign change of the exact symmetric difference L^2(r + h) - L^2(r - h)
(Fractions, h = 1e-9; no rounding, truncation shifts the root by ~h^2) with `toolkit.bisect` on
[r_ph + 1/2, 10 r_ph], r_ph from `photon_sphere`. Then L2 = L^2(r) and E2 = V(r; L2).

**Second route.** (a) `toolkit.golden_max` on -L^2(r): agrees to ~1e-8. (b) V' and V'' at the result by
floating-point finite differences are ~0. (c) Closed form: f' = 2/r^2, W' = 2/r^3 - 2(1 - 2/r)/r^3... i.e.
W' = (6 - 2r)/r^4, L^2 = r^2/(r - 3), dL^2/dr = r (r - 6)/(r - 3)^2 = 0 at r = 6;
L^2 = 12, E^2 = (2/3)(1 + 1/3) = 8/9. Printed next to the numerical values.

## 9. `shadow_uas(m_sun, d_pc)`

**Postulate** (S7): diameter = 2 b_c G M/(c^2 D).

b_c is dimensionless here (in units of GM/c^2): `photon_sphere()[1]`, called at call time.
G M = m_sun . inputs.GM_SUN (the solar mass parameter, more precise than G times a mass), D = d_pc .
inputs.PARSEC, c = inputs.C_LIGHT. The angle in radians (small-angle: the shadow's apparent radius for a
distant observer is b_c, by section 7) is converted to microarcseconds: x (180/pi) x 3600 x 1e6.
Scalings: ~ M/D, ~ GM_SUN.

**Second route.** theta_g = GM/(c^2 D) computed separately and the ratio shadow/theta_g = 2 sqrt(27).

## 10. `kerr_area_km2(m_sun, chi)`

**Postulate** (S7): A = 8 pi (GM/c^2)^2 (1 + sqrt(1 - chi^2)).

Consistency with section 5 (derivation from S7's own Kerr data): M = (p + q)/2 and a^2 = pq mean p, q are the
roots of x^2 - 2Mx + a^2, p = M + sqrt(M^2 - a^2) = M (1 + sqrt(1 - chi^2)) with chi = a/M. The horizon area
is A = 4 pi (p^2 + a^2) = 4 pi p (p + q) = 8 pi M p = 8 pi M^2 (1 + sqrt(1 - chi^2)), with S = A/4 = pi(p^2+a^2)
matching S7's S. (4 pi (r_+^2 + a^2) is the integral of sqrt(g_thth g_phph) over the Boyer-Lindquist horizon,
where the integrand reduces to (r_+^2 + a^2) sin theta; the Kerr metric itself is not in the SPEC, see
QUESTIONS.) In SI, M -> G M/c^2 = m_sun inputs.GM_SUN/c^2 metres; result divided by 1e6 for km^2.
|chi| > 1 raises ValueError. Scalings: ~ M^2; chi = 1 gives half the chi = 0 area.

**Second route.** 4 S with S = pi (p^2 + pq) from p, q = M (1 +- sqrt(1 - chi^2)); chi = 0 gives 16 pi M^2 =
4 pi (2M)^2, the sphere of radius r_b = 2M of section 1 (l -> infinity).

## 11. `qnm_220(m_det_sun, chi)`  (QUOTED: Berti, Cardoso, Will 2006 fit, coefficients inputs.BCW_220)

**Quoted** (S7): M omega = f1 + f2 (1 - chi)^f3, Q = q1 + q2 (1 - chi)^q3, damping rate omega/(2Q);
inputs.BCW_220 = (f1, f2, f3, q1, q2, q3).

M omega is dimensionless in G = c = 1; the time unit is G M/c^3 = m_det_sun . GM_SUN/c^3. So
    omega = (M omega) c^3/(m_det_sun GM_SUN),   f = omega/(2 pi) [Hz],   damping = omega/(2Q) [1/s].
The mass is the detector-frame (redshifted) mass, since f is the observed frequency. Not derived.

## 12. `invert_220(f, damp, z)`  (QUOTED: inverse of the same fit)

1. Q = omega/(2 damp) = pi f/damp: depends on chi only.
2. Solve Q = q1 + q2 (1 - chi)^q3: chi = 1 - ((Q - q1)/q2)^(1/q3). (Needs (Q - q1)/q2 > 0.)
3. M_det = (M omega)(chi) c^3/(2 pi f GM_SUN) in solar masses.
4. Source frame: M = M_det/(1 + z) (frequencies redshift by 1 + z, so the mass inferred from them is
   (1 + z) times the source mass).

**Second route.** chi by `toolkit.bisect` on Q(chi) - Q over [0, 1) (Q is monotonic); round trip with
`qnm_220`.

## 13. `hawking_K(m_kg)`  (QUOTED as a radiation temperature)

**Quoted** (S7): T_H = hbar c^3/(8 pi G M k_B).

What is derived here is only the geometry behind it: section 4 shows the Euclidean section is smooth iff
tau has period 2 pi/kappa; reading that period as hbar/(k_B T) gives T = hbar kappa/(2 pi k_B) (geometric
kappa -> kappa c in 1/s), and kappa = c^2.(1/(4 G M/c^2)) = c^4/(4GM) is the Schwarzschild value of section
2, giving T = hbar c^3/(8 pi G M k_B). That the periodicity is a temperature of emitted radiation is the
quoted part.

**Second route.** T = hbar c kappa_SI/(2 pi k_B) with kappa_SI = `killing_kappa`(M = 1)/(G m/c^2) (self-check).

---

## Self-check comparisons with measurements (not exports)

Pull = (prediction - measured)/sigma, sigma on the side of the measurement facing the prediction (S7).
- M87*: theta_g = G M/(c^2 D) from inputs.M87_STARS vs inputs.THETA_G_M87.
- Sgr A*: theta_g = mean of the VLTI and Keck theta_g values (each GM/(c^2 D)) vs inputs.THETA_G_SGRA.
- GW250114: `qnm_220`(GW_MF (1 + z), GW_CHIF) vs F220, G220; `invert_220`(F220, G220, z) vs (GW_MF, GW_CHIF);
  area theorem: A(M_f, chi_f) against the largest possible initial area A(m1, 0) + A(m2, 0).

## Not derived

- The BCW fit and the interpretation of 2 pi/kappa as a thermal period (quoted, allowed).
- S, T, Omega, J of Kerr (postulated by S7); the Kerr metric is not in the SPEC, so T and Omega are not
  re-derived from a Kerr Killing horizon here.
