# Derivation: Higgs-mass dependence of rho at one loop (build higgs_rho-b)

## 1. Lagrangian and Feynman rules (SPEC section 1)
Write W^a tau^a = [[W3, sqrt2 W+],[sqrt2 W-, -W3]], W+- = (W1 -+ iW2)/sqrt2, g_Z = sqrt(g^2+g'^2) = g/c, Z = cW3 - sB
(so g W3 - g' B = g_Z Z). With Phi = (phi+, (v+H+i phi0)/sqrt2) the covariant derivative gives
 upper component  U = D phi+ - i(g/2) W+ (v+H+i phi0),
 lower component  L = (1/sqrt2)[ dH + i d phi0 - i g W- phi+ + (i g_Z/2) Z (v+H+i phi0) ].
|D Phi|^2 = |U|^2 + |L|^2 contains (I expanded by hand, only H-terms and the tree masses shown):
* masses: (g^2 v^2/4) W+W-  and (1/2)(g_Z^2 v^2/4) Z^2  =>  M_W = g v/2, M_Z = g_Z v/2 = M_W/c  (M_W = c M_Z).
* cubic HVV:  (g^2 v/2) H W+_mu W-^mu = g M_W H W+W-,    (g_Z^2 v/4) H Z^2 = (g_Z M_Z/2) H Z^2.
  Feynman rules: i g M_W g^{mu nu} (W), i g_Z M_Z g^{mu nu} (Z).
* quartic: (g^2/4) H^2 W+W-,  (g_Z^2/8) H^2 Z^2.
* derivative couplings:
  (i g/2) [ W+_mu (phi- d^mu H - H d^mu phi-) - W-_mu (phi+ d^mu H - H d^mu phi+) ],
  (g_Z/2) Z_mu (H d^mu phi0 - phi0 d^mu H).
* Vertex factors (vertex = i x coefficient in L; all momenta incoming, d_mu -> -i p_mu; identical-field factorials included):
  H W+_mu W-_nu : i g M_W g^{mu nu};   H Z Z : i g_Z M_Z g^{mu nu}  (L = (g_Z M_Z/2) H Z^2, factor 2! for the two Z).
  H H W+W- : i (g^2/2) g^{mu nu}  (L = (g^2/4) H^2 W+W-, factor 2! for H^2);   H H Z Z : i (g_Z^2/2) g^{mu nu} (L = (g_Z^2/8) H^2 Z^2, 2! x 2!).
  W+_mu phi- H : coefficient (i g/2)(-i)(p_H - p_phi)^mu, so vertex  i (g/2)(p_H - p_phi)^mu;
  W-_mu phi+ H : coefficient -(i g/2)(-i)(p_H - p_phi)^mu, so vertex -i (g/2)(p_H - p_phi)^mu;
  Z_mu H phi0  : coefficient (g_Z/2)(-i)(p_phi - p_H)^mu, so vertex  (g_Z/2)(p_phi - p_H)^mu.
* Sign of the product of the two V-phi-H vertices (q = 0, so the momentum k that flows through the H line also flows through the Goldstone line):
  W bubble: at the W+ phi- H vertex take H incoming -k and phi- incoming +k, at the W- phi+ H vertex H incoming +k and phi+ incoming -k
  (momentum conservation at each vertex with q = 0; the charged line is the same propagator <phi- phi+>).
    vertex1 = i(g/2)(-k - k)^mu = -i g k^mu,   vertex2 = -i(g/2)(k + k)^nu = -i g k^nu,   product = (-i g)^2 k k = -g^2 k^mu k^nu.
  Propagators: (i/(k^2-m^2))(i/(k^2-xi M_W^2)) = -1/[...]. Hence i Pi_W^{mu nu} = (-g^2 kk)(-1) \int = + g^2 \int k^mu k^nu/[(k^2-m^2)(k^2-xi M_W^2)].
  Z bubble: vertex1 (H in -k, phi0 in +k) = (g_Z/2)(k + k) = g_Z k^mu; vertex2 (H in +k, phi0 in -k) = (g_Z/2)(-k - k) = -g_Z k^nu;
  product = -g_Z^2 k k; times propagators (-1): i Pi_Z^{mu nu} = + g_Z^2 \int k^mu k^nu/[(k^2-m^2)(k^2-xi M_Z^2)].
  The two vertices are always opposite in sign times opposite momentum flow (they are Hermitian conjugates for W; antisymmetric derivative coupling for Z), which is what
  fixes the overall + sign; it follows from the Lagrangian terms listed above, not from requiring xi independence (that independence is only a later cross-check).
  Symmetry factor 1 for both (H and phi are distinct lines).
* Absent diagrams (from the cubic/quartic terms of |D Phi|^2). H is neutral and CP-even. The H V V terms come only from (v+H)^2 times the gauge-boson mass terms,
  which are diagonal: g_Z M_Z H Z Z/2 and g M_W H W+W-, with no H W Z, H W A, H Z A or H A A term (the photon is massless and does not couple to v+H).
  The derivative terms V phi H exist only for W+- phi-+ H and Z phi0 H (no A phi0 H, no A phi+ H with a neutral-H pair: the photon couples to phi+phi- only).
  Hence the W+W- two-point function has Higgs loops only with: W + H (cubic HWW twice), phi+- + H (W phi H twice) and the H^2 seagull; the ZZ two-point
  function: Z + H, phi0 + H, and the H^2 seagull. There are no mixed W-Z, W-photon, Z-photon or photon loops containing an H.
  The quartic vertices H phi W Z and H phi W A (terms of the type g g_Z W- Z phi+ (v+H), g e W- A phi+ (v+H) with one H) have three different fields
  besides the gauge legs: to appear in the W+W- or ZZ two-point function a quartic vertex must have both external legs on it and its two remaining
  legs contracted with each other; for H phi W Z the remaining legs (H, phi) or (W, Z) cannot be contracted with each other (<H phi+-> = 0 by charge,
  <W Z> = 0 by charge), and with an external W the other external leg cannot be a Z or A. So they cannot close a loop on W+W- or ZZ.

## 2. Diagrams at q = 0 (SPEC section 2)
Effective action: L_eff = Pi_WW W+W- + (1/2) Pi_ZZ Z^2, so i Pi g^{mu nu} = sum of amputated 1PI diagrams.
Loop measure in d=4-2eps, MS-bar normalised: (16 pi^2/i) mu^{2eps} (e^gamma/4pi)^eps \int d^dk/(2pi)^d.
Define (units 16pi^2/i):  A0(a) = a(1/eps - ln a/mu^2 + 1),   \int 1/(k^2-a) -> A0(a).
Exact partial fractions in d dimensions:
  1/((x-a)(x-b)) = [1/(x-a) - 1/(x-b)]/(a-b),   x/((x-a)(x-b)(x-c)) = sum_i a_i/[(x-a_i) prod_{j!=i}(a_i-a_j)].
Hence with g(a) = a A0(a), h(a) = A0(a) (finite parts g = a^2(1-ln a/mu^2), h = a(1-ln a/mu^2)) all integrals are divided differences:
  B0(M^2,m^2) = h[M^2,m^2],  L2(a,b) = (16pi^2/i)\int k^2/((k^2-a)(k^2-b)) = g[a,b],  K(a,b,c) = (16pi^2/i)\int k^2/(...) = g[a,b,c].
Poles: B0: 1/eps, L2: (a+b)/eps, K: 1/eps.   Tensor reduction k^mu k^nu -> k^2 g^{mu nu}/d, with 4/d = 1 + eps/2 + ...,
so (4/d) X = X_MSbar + (1/2)(pole coefficient of X)  (the eps*(1/eps) piece is kept).

Diagrams for V = W (M=M_W, g) and V = Z (M=M_Z, g_Z); g^2 = 4M_W^2/v^2, g_Z^2 = 4M_Z^2/v^2:
(a) seagull H loop: Pi = c <H^2> with c = g^2/4 (W), (g_Z^2/4) (Z, after the factor 2 from the 1/2 Z^2 normalisation); <H^2> = -A0(m_H)/16pi^2.
    Pi_a/M_V^2 = -A0(m_H)/(16 pi^2 v^2) for both.
(b) V-H bubble: i Pi = (i g M)^2 \int (-i)[g - (1-xi)kk/(k^2-xi M^2)]/(k^2-M^2) * i/(k^2-m^2)
    => Pi_b = -(g^2 M^2/16pi^2)[ B0(M^2,m^2) - (1-xi)(1/d) K(xi M^2, M^2, m^2) ].
(c) H-phi bubble (vertices g k^mu and g k^nu for W; -g_Z k, g_Z k for Z; same overall sign, checked against scalar QED):
    i Pi = g^2 \int k^mu k^nu /((k^2-m^2)(k^2-xi M^2))  =>  Pi_c = (g^2/16pi^2)(1/d) L2(m^2, xi M^2).
Collecting, Pi_V/M_V^2 = F(M_V)/(16 pi^2 v^2) with (g^2/M_W^2 = g_Z^2/M_Z^2 = 4/v^2)
  F(M) = -A0(m) - 4M^2 B0(M^2,m^2) + (1-xi) M^2 [K + 1/2] + L2(m^2,xi M^2) + (1/2)(m^2 + xi M^2)   (MS-bar finite part).
Pole of F: -m^2 - 4M^2 + (1-xi)M^2 + (m^2 + xi M^2) = -3M^2, independent of m_H and xi. (Check: pole of A0 -> m^2 etc.)
Since 1/v^2 = pi alpha/(s^2 M_W^2):  Pi_V = alpha M_V^2 F(M_V)/(16 pi s^2 M_W^2), s^2 = 1 - M_W^2/M_Z^2.
Pole and the mu dependence of F are -3M^2/eps and -3M^2 ln mu^2 ... : m_H independent, hence they cancel in Delta rho(m_H) - Delta rho(M_W).

Tadpoles: H tadpole shifts v -> v + <H>, i.e. Pi_V^tad = 2 M_V^2 <H>/v (from M_V^2 (1+H/v)^2), so Pi^tad/M_V^2 is the same for W and Z and drops from Delta rho.

Result: Delta rho = Pi_WW/M_W^2 - Pi_ZZ/M_Z^2 = alpha [F(M_W) - F(M_Z)] / (16 pi s^2 M_W^2).

## 3. Large-m_H asymptotics (log_coefficient)
For m^2 >> M^2: B0 -> 1 - ln m^2; K -> 1 - ln m^2 (g[a1,a2,m^2] -> g(m^2)/m^4 - g'(a)/m^2 -> 1 - ln m^2);
L2 = (g(m^2)-g(b))/(m^2-b) -> m^2(1 - ln m^2) + b(1 - ln m^2). A0(m) is M independent.
Coefficient of ln m^2 (M-dependent part): +4M^2 - (1-xi)M^2 - xi M^2 = 3M^2 (xi cancels).
So F(M_W)-F(M_Z) -> 3(M_W^2-M_Z^2) ln m^2 and
  B = lim Delta rho/ln(m^2/M_W^2) = 3 alpha (M_W^2 - M_Z^2)/(16 pi s^2 M_W^2)  ( = -3 alpha/(16 pi c^2) ).
Custodial limit: F(M_W)-F(M_Z) is O(M_Z^2-M_W^2) = O(s^2 M_Z^2) and alpha/s^2 = g^2/4pi fixed, so Delta rho ~ g'^2.

## 4. Independent second routes
1. Exact-d check: evaluate F in exact d = 4-2eps (Gamma functions, exact 4/d factor, exact partial fractions) at eps = 1e-12 (50 digits),
   subtract -3M^2/eps (MS-bar normalised) and compare with the closed form (checks the eps/eps bookkeeping and the confluent divided differences).
2. Feynman-parameter quadrature (mpmath.quad) of B0, L2, K as simplex integrals of h'', g'' etc.
3. xi-independence of Delta rho, mu-independence, numerical slope vs the analytic B.
These are executed under __main__ in higgs_rho.py.

Not derived: nothing. The signs of the H-phi bubbles follow from the explicit contraction above; xi independence of Delta rho is only a cross-check.

Landau gauge xi = 0: nodes a = xi M^2 = 0 appear in g[a,b,c], g[a,b]. The code uses the limits h(0) = g(0) = g'(0) = 0 (a ln a -> 0, a^2 ln a -> 0), since ln 0 would give nan. Results are continuous in xi (checked xi = 1e-9, 1e-5, 0).

## 5. Accuracy and validity range
All exports are evaluated in mpmath and returned as floats (relative accuracy ~1e-15 from the final conversion). The m_H^2-proportional terms
cancel between W and Z in Delta rho, costing about 2 log10(m_H/M) digits; the working precision is therefore 50 + 3 per decade of
|log10(m_H/M_W)|, |log10(m_H/M_Z)| (function `_dps`), so the result keeps full float accuracy for any m_H (tested: local slope of rho_higgs_rel
over B = 1 to ~4e-15 at 1e8, 1e16, 1e24, 1e32 M_W, under __main__). Values for 10 GeV .. 1e8 M_W are unchanged to float precision. Inputs must satisfy
m_H > 0, M_W, M_Z > 0, M_Z > M_W (s^2 > 0), mu > 0, xi >= 0.
