# DERIVATION: blackholes (rung 6, SPEC.md section 7)

Conventions: G = c = 1 inside the geometry (lengths in units of M or of whatever unit M and l
are given in); SI only at the edges (`shadow_uas`, `kerr_area_km2`, `qnm_220`, `invert_220`,
`nariai_mass_kg`, `hawking_K`), with every constant read from `inputs` at call time.
Signature (-, +, +, +), coordinates x = (t, r, theta, phi). Exact quantities are Fractions.

Postulates (SPEC.md section 7, and section 6 for the metric and the spin connection):
- P1 static metric ds^2 = -f dt^2 + dr^2/f + r^2 dOmega^2; SdS f = 1 - 2M/r - r^2/l^2.
- P2 Killing vector xi = d_t; kappa^2 = -(1/2)(nabla_mu xi_nu)(nabla^mu xi^nu); Christoffels
  from the metric, i.e. from f only.
- P3 Euclidean time t = -i tau; proper radial distance rho = Int dr / sqrt f.
- P4 Kerr horizons p = r+, q = r-: M = (p+q)/2, a^2 = pq. QUOTED (Bardeen-Carter-Hawking 1973):
  S = pi(p^2 + a^2), T = (p - q)/(4 pi (p^2 + a^2)), Omega = a/(p^2 + a^2), J = M a.
- P5 geodesics: photons V = f/r^2 (impact parameter b^2 = 1/V at a turning point), massive
  particles V = f(1 + L^2/r^2) with (dr/dlambda)^2 = E^2 - V.
- P6 QUOTED: Berti-Cardoso-Will 2006 fit (inputs.BCW_220 = f1, f2, f3, q1, q2, q3):
  M omega = f1 + f2 (1-chi)^f3, Q = q1 + q2 (1-chi)^q3, damping rate omega/(2Q).
  QUOTED: Hawking 1975, T_H = hbar c^3/(8 pi G M k_B).
- P7 Kerr area A = 8 pi (GM/c^2)^2 (1 + sqrt(1 - chi^2)); shadow diameter 2 b_c GM/(c^2 D).
- Connections (SPEC "Connections between stages"): l from `desitter.ell_from_lambda`;
  kappa = |omega^0_{1t}| from `desitter.spin_connection`; maxima via `toolkit.golden_max`,
  roots via `toolkit.bisect`, exact derivatives via `toolkit.exact_derivative`.

---------------------------------------------------------------------------------------------------
## 1. sds_horizons(M, l) -> (r_b, r_c) or None

f(r) = 1 - 2M/r - r^2/l^2 on r > 0. Facts used (all from f itself):
- f'' = -4M/r^3 - 2/l^2 < 0: f is strictly concave on r > 0, so it has at most two zeros and a
  unique maximum r*.
- f(2M) = -4M^2/l^2 < 0 and f(r) <= 1 - r^2/l^2 - 2M/r < 0 for r >= l, so both zeros (if any) lie
  in (2M, l) and the maximum of f restricted to [2M, l] is the global one whenever horizons exist
  (concavity => unimodal on [2M, l]).
- Horizons exist iff f(r*) > 0 (f(r*) = 0 is the degenerate Nariai case: one double root; I return
  None there, since there is no static region between two horizons).

Algorithm: r* = toolkit.golden_max(f, 2M, l); if f(r*) <= 0 -> None; else
r_b = toolkit.bisect(f, 2M, r*), r_c = toolkit.bisect(f, r*, l).
Bisection runs to adjacent doubles, so |f(r_h)| ~ 1e-16.

Closed-form facts (used only as checks): r* = (M l^2)^(1/3) from f' = 0; f(r*) = 1 - 3 (M/l)^(2/3),
so horizons exist iff 27 M^2 < l^2. The cubic r^3 - l^2 r + 2 M l^2 = 0 (= -r l^2 f) has roots
r_b, r_c and r_n = -(r_b + r_c) (no r^2 term: Vieta), product r_b r_c r_n = -2 M l^2.

Second route: Vieta. r_b + r_c + r_n = 0 means the third root is -(r_b + r_c), and
r_b r_c (r_b + r_c) = 2 M l^2 and r_b^2 + r_b r_c + r_c^2 = l^2; printed in the self-check.

## 2. killing_kappa(f, r0, h)

Metric at x0 = (0, r0, theta0, 0) with a generic theta0 (pi/3; the answer cannot depend on it):
g = diag(-f(r), 1/f(r), r^2, r^2 sin^2 theta). Derivatives d_rho g_{mu nu} by central differences
with step h in every coordinate (t and phi derivatives vanish identically, theta derivative is the
sphere's). Christoffels
  Gamma^l_{mu nu} = (1/2) g^{l s} (d_mu g_{s nu} + d_nu g_{s mu} - d_s g_{mu nu}).
Killing vector xi^mu = delta^mu_t; lowered xi_nu = g_{nu t} (so d_mu xi_nu = d_mu g_{nu t}, also by
the same finite differences);
  nabla_mu xi_nu = d_mu xi_nu - Gamma^l_{mu nu} xi_l,
  K = g^{mu a} g^{nu b} nabla_mu xi_nu nabla_a xi_b,   kappa = sqrt(-K/2).
No f' is ever formed analytically: only f is evaluated.

Closed form (by hand, as the check): xi_t = -f; Gamma^t_{rt} = f'/(2f);
nabla_r xi_t = d_r xi_t - Gamma^t_{rt} xi_t = -f' + (f'/(2f)) f = -f'/2,
nabla_t xi_r = d_t xi_r - Gamma^t_{tr} xi_t = +f'/2 (antisymmetric, as Killing's equation requires);
all other components vanish (Gamma^l_{mu nu} xi_l = -f Gamma^t_{mu nu}, nonzero only for (t r), (r t)). K = 2 g^{tt} g^{rr} (f'/2)^2 = -f'^2/2, so
kappa = |f'|/2, at any r (the horizon value is kappa evaluated at r_h).
On SdS: kappa_b = f'(r_b)/2, kappa_c = -f'(r_c)/2.

Second routes: (i) |f'|/2 with f' from the analytic derivative (self-check only); (ii) section 3,
rung 5's spin connection; (iii) section 4, Euclidean smoothness.

Numerics: the blind test evaluates at r_h(1 +- 1e-6) where f ~ 1e-7; g^{tt} = -1/f is large but the
contraction is g^{tt} g^{rr} = -1 times (d_r g_tt)^2/4 and finite differences of f with h = 1e-8 r
carry roundoff ~ eps/h ~ 1e-8 relative. The value differs from the horizon value by O(1e-6)
relative (f'' r 1e-6 / f').

## 3. kappa_from_spin_connection(M, l)

From rung 5 (DERIVATION_desitter.md section 3): on the diagonal tetrad e^0 = sqrt f dt,
omega^0_1 = (f'/2) dt, i.e. omega^0_{1 t} = f'/2. Relation to kappa: the only nonzero nabla xi is
nabla_r xi_t = -f'/2 (section 2). In the orthonormal frame, (nabla xi)_{10} = E_1^r E_0^t nabla_r xi_t
= sqrt f (1/sqrt f)(-f'/2) = -f'/2 = -omega^0_{1t}. Equivalently xi_a = e_a . d_t has only the
component xi_0 = -sqrt f, and nabla_mu xi_a = d_mu xi_a - omega^b_{a mu} xi_b; at mu = t the
connection term gives -omega^0_{1t} xi_0 ~ sqrt f f'/2 for the frame component. So
K = 2 eta^{00} eta^{11} (omega^0_{1t})^2 = -2 (omega^0_{1t})^2 and kappa = |omega^0_{1t}|, the
boost rate of the static frame: rung 5's spin connection IS the surface gravity.

Procedure (SPEC section 7): (r_b, r_c) = sds_horizons(M, l) (this module); evaluate
`desitter.spin_connection(x, f, fp)` at x = (0, r_b (1 + 1e-9), pi/2, 0) and
x = (0, r_c (1 - 1e-9), pi/2, 0) (just inside the static region, f > 0 so sqrt f is real), read
w[0][1][0] = omega^0_{1 t}, return its absolute value.
The fp argument rung 5 requires is supplied as the EXACT derivative of the postulated f:
fp(r) = toolkit.exact_derivative(f_exact, Fraction(r)), where f_exact uses Fraction(M), Fraction(l)
(the float r, M, l are exactly representable as Fractions). So no hand-typed f' enters.

Second route: compare with killing_kappa (section 2) at the same horizons; the blind check
requires agreement to 1e-5 (the Killing route sits at r_h(1 +- 1e-6)).

## 4. euclidean_cone_ratio(f, rh, beta, eps)

Euclidean section: t = -i tau turns -f dt^2 into +f dtau^2: ds_E^2 = f dtau^2 + dr^2/f (+ sphere).
At fixed r = rh + eps the tau-circle (period beta) has circumference C = beta sqrt(f(rh+eps)).
Its proper radius (distance from the horizon r = rh, where the circle shrinks to a point) is
rho = Int_{rh}^{rh+eps} dr / sqrt f. Ratio = C/(2 pi rho); a smooth disc (no conical singularity)
needs ratio -> 1 as eps -> 0.

Endpoint singularity: f(rh) = 0, so 1/sqrt f ~ 1/sqrt(f'(rh)(r - rh)) is integrable but infinite.
Substitute r = rh + u^2, dr = 2u du:
  rho = Int_0^{sqrt eps} g(u) du,  g(u) = 2u / sqrt(f(rh + u^2)).
Near u = 0, f(rh + u^2) = f'(rh) u^2 + f''(rh) u^4/2 + ..., so g(u) = 2/sqrt(f' + f'' u^2/2 + ...) is
a smooth EVEN function of u, finite at u = 0. Its endpoint value is not evaluated at u = 0
(0/0 with f only); it is obtained from two interior samples by the even-function extrapolation
g(0) = (4 g(du) - g(2 du))/3 + O(du^4). The integral is toolkit.trapezoid on n = 401 samples
(the integrand varies by O(f'' eps / f') ~ 1e-7 across the interval, so the trapezoid error is
negligible). Only f is evaluated.

Closed form (check): rho -> 2 sqrt(eps/f'), C -> beta sqrt(f' eps), ratio -> beta f'/(4 pi) =
beta kappa/(2 pi). Smooth iff beta = 2 pi/kappa: T = 1/beta = kappa/(2 pi) (Hawking/Gibbons-Hawking
temperature from geometry). For beta = 8 pi at M = 1, l = 9 the ratio is 4 kappa_b, far from 1.

Second route: the self-check prints the ratio next to beta kappa/(2 pi) with kappa from rung 5's spin
connection (section 3), for the smooth period and for beta = 8 pi. Residual 1 - ratio ~ 5e-7 at
eps = 1e-7 r_b is the O(eps f''/f') finite-eps correction.

## 5. kerr_first_law(p, q, dp, dq) -> (first, smarr)

Only the quoted P4 quantities. pi is irrational, so work with S/pi = p^2 + a^2 and T pi = (p-q)/(4(p^2+a^2));
T dS = (T pi) d(S/pi), TS = (T pi)(S/pi) are exact rationals.
a = sqrt(pq) is irrational in general, but Omega and J enter the first law and Smarr only through
rational combinations:
- Omega J = a^2 M/(p^2 + a^2)  (rational: a^2 = pq).
- Omega dJ: J^2 = M^2 a^2 is rational, and dJ = d(J^2)/(2J), so
  Omega dJ = (Omega/(2J)) d(J^2) = d(J^2) / (2 M (p^2 + a^2)),   Omega/J = 1/(M (p^2+a^2)) rational.
  This form is also the correct limit at a = 0 (q = 0), where J = M sqrt(pq) has an infinite
  derivative along dq but Omega dJ = (a^2 dM + M d(a^2)/2)/(p^2+a^2) stays finite.
Directional derivatives along (dp, dq): parametrize p(s) = p + s dp, q(s) = q + s dq and take
d/ds at s = 0 with toolkit.exact_derivative (dual numbers over Fraction):
  first = dM - (T pi) d(S/pi) - d(J^2)/(2 M (p^2 + a^2)),
  smarr = M - 2 (T pi)(S/pi) - 2 a^2 M/(p^2 + a^2).
Both are Fractions and compared with == 0.

Closed form (check): p^2 + a^2 = p(p+q) = 2Mp.
smarr = (p+q)/2 - (p-q)/2 - 2 M pq/(2 M p) = q - q = 0.
first along dp: dM = 1/2, d(S/pi) = 2p + q, T pi (2p+q) = (p-q)(2p+q)/(4p(p+q)),
d(J^2) = d(M^2 pq) = 2M (1/2) pq + M^2 q = Mq(p + M) ... -> d(J^2)/(4M^2 p) = q(p + M)/(4Mp);
sum = (p-q)(2p+q)/(4p(p+q)) + q(3p+q)/(4p(p+q)) = (2p^2 + 2pq)/(4p(p+q)) = 1/2 = dM. Similarly along dq.
Second route: the blind check's random rational (p, q) incl. q = 0, and the self-check
evaluates a float version with a = sqrt(pq) and a finite-difference dJ.

## 6. nariai_mass_kg(Lam)

Largest SdS mass: the two horizons r_b < r_c merge, f = f' = 0 at one radius. Write r = x l, M = mu l:
  F(x, mu) = 1 - 2 mu/x - x^2.
F is linear in mu, and d_x F = 2 mu/x^2 - 2x = 0 gives mu = x^3 (the double-root branch). Then
  F(x, x^3) = 1 - 3 x^2 = 0  =>  x = 1/sqrt 3, mu = x^3 = 1/(3 sqrt 3) = 1/sqrt(27).
Numerically: x = toolkit.bisect(x -> F(x, x^3), 0, 1) (F(0) = 1 > 0, F(1) = -2 < 0, monotone),
mu = x^3. Geometric mass M = mu l with l = desitter.ell_from_lambda(Lam) (rung 5: l = sqrt(3/Lam)),
SI mass M_kg = M c^2/G (inputs.C_LIGHT, inputs.G_NEWTON at call time).
Closed form: M_kg = c^2/(3 sqrt(Lam) G) (since l/sqrt27 = sqrt(3/Lam)/sqrt(27) = 1/(3 sqrt Lam)).
Why it is the LARGEST: f(r*) = 1 - 3 (M/l)^(2/3) decreases with M, horizons exist iff M < mu l.
Second routes: (i) closed form above; (ii) sds_horizons(M(1 -+ delta) , l) exists / is None;
(iii) at r = l/sqrt3, f and f' vanish (blind check).

## 7. photon_sphere() -> (r, b), M = 1

Null geodesics: (dr/dlambda)^2 = E^2 - L^2 f/r^2, i.e. (dr/dlambda)^2 / L^2 = 1/b^2 - V(r), V = f/r^2,
b = L/E. A circular photon orbit sits at the maximum of V (unstable), and a photon from infinity is
captured iff 1/b^2 > V_max: critical impact parameter b_c = 1/sqrt(V_max).
Numerics: V = (1 - 2/r)/r^2 on [2, 10] (V(2) = 0, V -> 0 as r grows; one interior maximum since
V' changes sign once). r = toolkit.golden_max(V, 2, 10); golden section locates a flat maximum only
to ~ sqrt(eps) relative, so the location is polished as the root of the EXACT derivative
V'(r) = toolkit.exact_derivative(V, Fraction(r)) with toolkit.bisect in a 1e-5 bracket around the
golden-section result. b = 1/sqrt(V(r)).
Closed form (check only, not in the code path): V' = (6 - 2r)/r^4 => r = 3, b = sqrt(27) = 3 sqrt3.

## 8. isco() -> (r, L2, E2), M = 1

Massive geodesics: (dr/dtau)^2 = E^2 - V(r; L^2), V = f (1 + L^2/r^2). Circular orbit at r: V' = 0.
V' is LINEAR in L^2: V'(r) = d_r f + L^2 d_r(f/r^2), so the circular orbit at r needs
  L^2(r) = - d_r f / d_r(f/r^2),
each derivative from toolkit.exact_derivative (exact at the float r converted to a Fraction).
d_r(f/r^2) vanishes at the photon sphere (section 7) and is negative outside it, so L^2(r) > 0 for
r > r_ph, L^2 -> +infinity at r_ph and as r -> infinity (L^2 ~ M r): it has a minimum. Circular
orbits exist for L^2 >= min L^2(r) and FIRST appear at that minimum, where the stable (V'' > 0)
and unstable branches merge (V' = V'' = 0, inflection): that is the ISCO.
Numerics: r_isco = toolkit.golden_max(-L^2, r_ph (1 + 1e-6), 20 r_ph) with r_ph from photon_sphere();
polished as the root of the exact symmetric difference D(r) = L^2(r(1+eta)) - L^2(r(1-eta)),
eta = 1e-6, via toolkit.bisect (D is evaluated in exact Fractions; the bias of the root is
O(eta^2 r) ~ 1e-12 r). L2 = L^2(r_isco), E2 = V(r_isco; L2) = f (1 + L2/r^2).
Closed form (check only): L^2(r) = M r^2/(r - 3M); dL^2/dr = 0 at r = 6M; L^2 = 12 M^2;
E^2 = (1 - 1/3)(1 + 12/36) = 8/9.
Second route (self-check): at L^2 = L2 (1 - 1e-3) V' has no sign change on (2, 50), at L2 (1 + 1e-3)
it has two (stable + unstable orbits), counted on a grid.

## 9. shadow_uas(m_sun, d_pc)

Shadow diameter (P7) = 2 b_c GM/(c^2 D) radians, b_c from photon_sphere(), GM = m_sun inputs.GM_SUN,
D = d_pc inputs.PARSEC, c = inputs.C_LIGHT; radians -> micro-arcseconds: x (180/pi) 3600 1e6.
Scaling: proportional to m_sun / d_pc (and to GM_SUN). The angular gravitational radius used to
compare with EHT is theta_g = GM/(c^2 D) = shadow/(2 b_c).

## 10. kerr_area_km2(m_sun, chi)

Kerr horizons (P4): r+- are the roots of r^2 - 2Mr + a^2 (Vieta from M = (p+q)/2, a^2 = pq). In units of
M with a = chi M: r+ = toolkit.bisect(r^2 - 2r + chi^2, 1, 2) (value chi^2 - 1 <= 0 at 1, chi^2 >= 0 at 2;
the bisection returns exact endpoints at chi = 0 and 1). The horizon 2-surface (t, r = r+ fixed) of
Kerr has area 4 pi (r+^2 + a^2), equal to 4 S of P4 (in units G = hbar = 1): A = 4 pi (r+^2 + chi^2) M^2.
SI: M -> GM/c^2 = m_sun GM_SUN / c^2 metres; km^2 = m^2 / 1e6.
Closed form (P7, check): r+ = 1 + sqrt(1 - chi^2), r+^2 + chi^2 = 2 r+ => A = 8 pi M^2 (1 + sqrt(1 - chi^2)).
Extremal chi = 1 gives half the chi = 0 area.

## 11. qnm_220(m_det_sun, chi)  [QUOTED: Berti, Cardoso & Will 2006, Phys. Rev. D 73, 064030]

M omega = f1 + f2 (1 - chi)^f3 (dimensionless, G = c = 1); M in seconds = m_det GM_SUN/c^3.
omega = (M omega)/M_s rad/s; frequency f = omega/(2 pi) Hz; Q = q1 + q2 (1-chi)^q3; damping rate
gamma = omega/(2Q) s^-1 (= 1/tau). Detector-frame mass: redshifted, m_det = (1+z) m_source.

## 12. invert_220(f, damp, z)  [QUOTED fit, inverted algebraically]

omega = 2 pi f; Q = omega/(2 damp) = pi f/damp. Q(chi) is monotone in chi (q2 > 0, q3 < 0: Q grows as
chi -> 1), inverted in closed form: 1 - chi = ((Q - q1)/q2)^(1/q3). Then M omega from the fit at that
chi, M_det(s) = (M omega)/omega, m_det = M_det c^3/GM_SUN, m_source = m_det/(1+z).
Second route: round trip qnm_220(invert) and a bisection solve of Q(chi) = Q in the self-check.

## 13. hawking_K(m_kg)  [QUOTED: Hawking 1975]

T_H = hbar c^3/(8 pi G M k_B), inputs at call time. Consistency with section 4: kappa = 1/(4M) for
Schwarzschild (f' = 2M/r^2 at r = 2M), T = hbar kappa c/(2 pi k_B) with kappa = c^4/(4GM) in SI
gives exactly the quoted formula (self-check compares the two).

---------------------------------------------------------------------------------------------------
## Self-check (module __main__)
Prints: SdS kappas (Killing, spin connection, |f'|/2) at M = 1, l = 9; Vieta check; Euclidean ratio;
first-law float cross-check; photon sphere / b_c / ISCO vs closed forms; Nariai mass vs closed form;
M87* and Sgr A* theta_g pulls; GW250114 area theorem; QNM pulls; Hawking temperature of the remnant.
