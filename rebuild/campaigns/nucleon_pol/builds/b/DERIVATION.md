# Derivation: alpha_E, beta_M of the nucleon, LO heavy-baryon ChPT (SPEC sections 1-4)

## 1. Postulates used (SPEC 1, 2)
- HB Lagrangian N^dag(i v.D + gA S.u)N, pion Lagrangian with D_mu pi^+- = (d_mu -+ i e A_mu) pi^+-. Delta and counterterms excluded.
- Gauge: A_0 treated explicitly only for E; vertices from L: pi N N (gA/2f) tau^a sigma.D pi^a, with D = grad - i e A [Q,.]
  acting on the pion (this contains the Kroll-Ruderman NN pi gamma vertex); gamma pi pi and gamma gamma pi pi vertices from the pion kinetic term
  (i.e. the covariant operator below). Weinberg-Tomozawa vertices: NN pi pi gamma carries v.A or v.(l+l'); they drop (A_0=0 in the
  B case; in the E case WT with two photons attached to a pion loop is C-odd, Furry, vanishes). Nucleon-photon LO vertex v.A: nucleon sits at x=0 where A_0=0.
- H_eff = -2pi alpha_E E^2 - 2pi beta_M B^2 (SPEC 2), so dE = -2pi(alpha_E E^2 + beta_M B^2).

## 2. Which diagrams contribute, and the Born subtraction
One-loop, O(p^3), irreducible w.r.t. the nucleon line (the loop is a pion emitted and reabsorbed; the nucleon propagator inside the loop is static, i/(v.l)):
 (a) KR-KR: photons at both pi N vertices, pion free between them;
 (b) KR + photon on the pion line (gamma pi pi), both orderings;
 (c) two gamma pi pi vertices on the pion line;
 (d) gamma gamma pi pi seagull on the pion line;
 (e) photon-nucleon (v.A) diagrams: vanish for A_0 = 0 / static source at origin (Thomson term absent in HB at LO).
Both alpha_E and beta_M receive contributions from the same set (a)-(d); in the explicit calculation below, for E the pieces are (c)+(d) combined in V^2 [A_0 gauge, no KR since A_i=0],
for B in the symmetric gauge the L.B-squared term is the (b)/(c) (pion-line) group and the A^2 term the seagull (d) plus KR-seagull-type pieces from D_i (which vanish at x=0 since A(0)=0).
Gauge-dependent assignment between (a)-(d) differs between gauges; only the sum is meaningful.
Born subtraction: the Born (nucleon-pole) graphs are those reducible by cutting one nucleon line (photons on the external nucleon: charge v.A, magnetic moment, and their one-loop vertex corrections
sandwiching a nucleon propagator 1/(v.k)). They are O(gA^4) (or vanish at LO) in the pinned-nucleon picture and are NOT in the O(gA^2) functional used here: the energy functional is strictly second order in the pi N vertex, 1PI
in the nucleon line, so the subtraction is exactly "drop all nucleon-reducible graphs". The first-order magnetic term (linear in B, the loop magnetic moment) is the vertex of a Born graph; only the O(B^2) term is kept.

## 3. Reduction to a static pion functional
Second-order energy of the static source: dE = -int_0^inf dtau <H_I(tau)H_I(0)>, H_I = (gA/2f) tau^a sigma_i D_i pi^a(0).
Isospin for the proton: tau.pi = sqrt2(tau_+ phi^dag + tau_- phi) with phi = (pi1 + i pi2)/sqrt2; the charged part has weight 2 (the neutral pi0 weight 1, no photon coupling, no field dependence).
sigma_i sigma_j -> delta_ij for the scalar polarizabilities (the antisymmetric part gives linear-in-field terms, i.e. spin-dependent/magnetic-moment terms).
In frequency space the nucleon propagator -1/(l0 - i eps) = -P/l0 - i pi delta(l0). The pion propagator in a static background is [(l0 - V)^2 - (p - eA)^2 - m^2]^-1; the E^2 and B^2 terms are even in l0 (terms odd in l0 occur only at odd order in the fields), so the principal part vanishes and the delta function sets l0 = 0, giving (the free check: int_0^inf e^{-w tau}/(2w) = 1/(2 w^2) = (1/2)/(p^2+m^2) agrees):
  dE_charged = -(gA^2/4f^2) [D^x_i D^{y*}_i G(x,y)]_{x=y=0},   G = (m^2 - D^2 - V^2)^{-1},  D = grad - i e A  (a pion of unit charge e).
Since A(0)=0, D_i -> d_i at the vertex points.
UV: all integrals below converge in d=3 (no divergence at all in the field-dependent terms: m is the only scale, the coefficient is odd in m, ~1/m, which no local counterterm can produce, and in dim. reg. there is no pole; the polynomial divergences of the field-independent self-energy are removed in dim. reg.).

## 4. Electric polarizability
A_0 gauge: V = e E.x, A=0. G = G0 + G0 V^2 G0 + ..., G0 = e^{-mr}/(4 pi r). Kernel: int d^3z (d_i G0(z))^2 V(z)^2 = e^2E^2 (1/3) int d^3z r^2 G0'^2,
G0' = -e^{-mr}(1+mr)/(4 pi r^2), so (1/3)(4pi/(16 pi^2)) int_0^inf e^{-2mr}(1+mr)^2 dr = (1/(12 pi))(5/(4m)) = 5/(48 pi m).
dE = -(gA^2/4f^2) e^2 E^2 5/(48 pi m) = -2 pi alpha_E E^2  =>  alpha_E = 5 e^2 gA^2 /(384 pi^2 f^2 m) = 5 alpha gA^2/(96 pi f^2 m).

## 5. Magnetic polarizability
Symmetric gauge A = B x r/2, V=0: -D^2 = p^2 + e B.L + e^2 A^2. G = G0 - G0 W G0 + G0 W G0 W G0 with W = e B.L + e^2A^2:
 - A^2 term: -e^2 (1/6) B^2 int d^3z r^2 G0'^2 = -e^2B^2 (1/6)(5/(16 pi m)) = -5 e^2B^2/(96 pi m);
 - (B.L)^2 term: L commutes with G0, states d_j delta are l=1: sum_j <(B.L)^2> = 2B^2 over 3 states -> (2/3) e^2 B^2 int d^3p/(2pi)^3 p^2/(p^2+m^2)^3 = (2/3)(3/(32 pi m)) e^2B^2 = e^2B^2/(16 pi m).
Sum = e^2B^2/(96 pi m). dE = -(gA^2/4f^2) e^2B^2/(96 pi m) = -2 pi beta_M B^2 => beta_M = e^2 gA^2/(768 pi^2 f^2 m) = alpha_E/10.

## 6. Independent second route (implemented in __main__ and tmp/route2.py)
Momentum-space calculation in a different gauge: Landau A=(0,Bx,0) (x = i d/dp_x, W = -2eB x p_y + e^2B^2x^2), and the electric case as <V chi|V chi> with chi_i = p_i/(p^2+m^2), V=i e E d/dp_z.
Evaluated by 3D numerical quadrature (and symbolically in sympy): coefficients 5/(48 pi m) and 1/(96 pi m), ratio to route 1 = 1.000000 for both.
## 7. Not derived / caveats
- The step "static-field energy = Born-subtracted Compton O(omega^2) coefficient", and the l0-parity argument, are argued, not checked against an explicit covariant Feynman-diagram Compton computation (which I did not carry out).
- The identification of which graphs of the covariant (gauge epsilon.v=0) calculation correspond to which term is gauge dependent (see section 2).
