# DERIVATION: Higgs part of Delta r at one loop in the R_xi gauge (build higgs_dr_xi-a)

Answer to the campaign question, stated first: **Delta r_H(m_H) - Delta r_H(M_W) does not depend on xi.**
Stronger: the g^{mu nu} coefficient Pi_VV(q^2) of the sum of Higgs-containing 1PI diagrams is itself
xi-independent at every q^2 (not only on shell). The xi-dependent part of the gauge propagator in the H-V loop
and the H-Goldstone loop (Goldstone mass^2 xi M_V^2) cancel identically in the g^{mu nu} part, leaving only
q^mu q^nu terms (step 4). This was derived, not assumed, and is checked numerically by an independent route (step 9).

## 1. Lagrangian, masses and couplings (SPEC section 1)

Phi = (phi^+, (v+H+i chi)/sqrt2), D = d - i g W^a tau^a/2 - i g' B/2. With tau^a W^a = [[W3, sqrt2 W+],[sqrt2 W-, -W3]]:

* upper component of D Phi: d phi^+ - i (g/2)(W3 phi^+) - i(g'/2)B phi^+ - i (g/2) W^+ (v+H+i chi)
* lower component: d(H+i chi)/sqrt2 - i(g/sqrt2) W^- phi^+ + i (g/(2c)) Z (v+H+i chi)/sqrt2,
  using g W3 - g' B = sqrt(g^2+g'^2)(c W3 - s B) = (g/c) Z.

|D Phi|^2 then contains

| term | coefficient | consequence |
|---|---|---|
| (g^2/4)(v+H)^2 W+W- | M_W^2 = g^2 v^2/4 | M_W = g v/2 |
| (g^2/(8c^2))(v+H)^2 Z Z | M_Z^2/2 ZZ, M_Z^2 = g^2v^2/(4c^2) | M_W = c M_Z |
| H W+W- : g M_W | vertex i g M_W g_{mu nu} | |
| H H W+W- : g^2/4 | vertex i (g^2/2) g_{mu nu} | |
| H Z Z : g M_W/(2c^2) | vertex i (g M_W/c^2) g_{mu nu} = i (g M_Z/c) g | |
| H H Z Z : g^2/(8c^2) | vertex i g^2/(2c^2) g_{mu nu} | |
| i(g/2) W+_mu (phi^- d^mu H - H d^mu phi^-) + h.c. | vertex W+ phi- H: +i(g/2)(p_H - p_phi)_mu, W- phi+ H: -i(g/2)(p_H - p_phi)_mu (all momenta incoming) | |
| (g/(2c)) Z_mu (chi d^mu H - H d^mu chi) | vertex Z chi H: (g/(2c))(p_H - p_chi)_mu | |

The potential gives v^2 = mu^2/lambda and m_H^2 = 2 lambda v^2. The mixing terms -i(g/2) v W+ d phi^- + h.c. and
M_Z Z d chi are cancelled by the 't Hooft gauge fixing F = d.W -/+ i xi M_W phi^+-, d.Z - xi M_Z chi, which gives the
SPEC propagators and Goldstone masses^2 xi M_V^2.

Key ratio: (V-Goldstone-H coupling)/(V-V-H coupling) = (g/2)/(g M_W) = (g/(2c))/(g M_Z/c) = 1/(2 M_V) for both V.
This is what makes the cancellation of step 4 work.

g^2 = e^2/s^2 = 4 pi alpha / s^2, so g^2/(16 pi^2) = alpha/(4 pi s^2).

## 2. Ghosts

Ghost interactions are bilinear in ghost fields (cbar c X), so ghost number is conserved along a line and every ghost
loop consists of ghost propagators only. A one-loop two-point function of V whose loop contains an H propagator has
exactly two internal lines (H + one other) or one (seagull); the other line cannot be a ghost because no V-H-ghost vertex exists.
The R_xi ghost-ghost-H vertex (proportional to xi g M_V) appears only in the **H tadpole**, which is dropped (step 6).
So ghosts do not contribute to the Higgs-containing Pi_VV.

## 3. Integrals (SPEC sections 2, 6)

Measure mu^{2eps} int d^dk/(2pi)^d = (i/16 pi^2) x [PV function]. With D(x) = x m1^2 + (1-x) m0^2 - x(1-x) p^2 - i0:

* A0(m) = m^2 (Delta - ln(m^2/mu^2) + 1)
* B0(p^2; m0, m1) = int_0^1 dx [Delta - ln(D/mu^2)]
* int k^mu k^nu /(D0 D1) = g^{mu nu} B00 + p^mu p^nu B11, with (tensor reduction l^mu l^nu -> g l^2/d, and
  1/d = (1 + eps/2)/4 kept against the 1/eps pole, which produces the "+1"):
  B00(p^2; m0, m1) = (1/2) int_0^1 dx D(x) [Delta - ln(D/mu^2) + 1].
  (UV part: [(m0^2+m1^2)/4 - p^2/12] Delta.)
* the three-point tensor integral needed for the second route,
  int k k /((k^2 - xi M^2)(k^2 - M^2)((k-q)^2 - m^2)) -> g^{mu nu} C00 + ..., with
  C00 = (1/2) int_simplex [Delta - ln(Delta3/mu^2)], Delta3 = x xi M^2 + y M^2 + z m^2 - z(1-z) q^2
  (the O(eps) part of 1/d cancels the -1/2 from int l^2/(l^2-Delta)^3 exactly).

MS-bar: Delta is dropped. Below threshold D > 0 on [0,1], so every function is real.
B00 is symmetric in m0 <-> m1 (x -> 1-x), so the routing of the loop momentum is irrelevant.

## 4. The Higgs-containing diagrams of Pi_WW (g^{mu nu} parts)

Resummation: -i/(k^2-M^2) sum (i Pi (-i)/(k^2-M^2))^n = -i/(k^2 - M^2 - Pi), so the effective mass^2 is M^2 + Pi
for i Pi g^{mu nu} = (sum of 1PI amplitudes), as the SPEC says.

Split the R_xi propagator by partial fractions, (1-xi)/((k^2-xi M^2)(k^2-M^2)) = [1/(k^2-M^2) - 1/(k^2-xi M^2)]/M^2:

  P^{mu nu}(k) = -i [g - k k/M^2]/(k^2 - M^2)  -  i k k /(M^2 (k^2 - xi M^2)).

(a) H-W loop, W momentum k, H momentum q-k: (i g M)^2 P (i/D_H). Unitary-like piece:
  Pi_a1 = -(g^2/16 pi^2) [ M^2 B0(q^2;M,m_H) - B00(q^2;M,m_H) ];
  xi piece: integrand -g^2 k^mu k^nu /(D_xi D_H), i.e. g-part Pi_a2 = -(g^2/16 pi^2) B00(q^2; sqrt(xi) M, m_H)
  plus q q terms.

(b) H-phi^+- loop: vertex product (+i g/2)(-i g/2) (2k - q)(q - 2k) times i/D_xi * i/D_H gives the integrand
  +(g^2/4)(q-2k)^mu (q-2k)^nu /(D_xi D_H) = g^2 [k k - (k q + q k)/2 + q q /4]/(D_xi D_H).
  g-part: Pi_b = +(g^2/16 pi^2) B00(q^2; sqrt(xi) M, m_H).

  **a2 + b**: the k^mu k^nu terms cancel exactly in the integrand; what is left, -(kq+qk)/2 + qq/4, integrates to
  q^mu q^nu only. Hence the g^{mu nu} part of the Higgs diagrams is xi-independent at all q^2; the whole xi dependence
  sits in Pi^L (the q^mu q^nu coefficient).

(c) Seagull with an H loop: (1/2)(i g^2/2) int i/(k^2 - m_H^2) gives Pi_c = -(g^2/16 pi^2) A0(m_H)/4.

Result (exact for any xi >= 0, Landau gauge xi = 0 included: B00 with m0 = 0 is finite and cancels the same way):

  **Pi_WW(q^2) = -(alpha/(4 pi s^2)) [ f_W(q^2) + A0(m_H)/4 ],   f_V(q^2) = M_V^2 B0(q^2;M_V,m_H) - B00(q^2;M_V,m_H).**

For Z replace g -> g/c and M_W -> M_Z (coupling ratio of step 1 is the same, so the same cancellation):

  **Pi_ZZ(q^2) = -(alpha/(4 pi s^2 c^2)) [ f_Z(q^2) + A0(m_H)/4 ].**

The code evaluates a1, a2, b, c separately and adds them (so the xi-dependent pieces are present in the code and cancel
there), and the second route (step 9) evaluates the H-W diagram with the unsplit SPEC propagator.

## 5. Pole mass and the q q pieces

The full 1PI function is Pi g + Pi^L q q = Pi (g - qq/q^2) + (Pi + q^2 Pi^L) qq/q^2, so the g^{mu nu} coefficient is
the transverse self-energy. The transverse part of the propagator, -i(g - qq/q^2)/(q^2 - M_0^2 - Pi(q^2)), has its pole at
M^2 = M_0^2 + Pi(M^2) (at one loop, Re; real here below threshold). The longitudinal part (Pi^L, and the Higgs-containing
V-Goldstone mixing two-point function, which is proportional to q^mu) only affects the xi-dependent unphysical poles, never
the transverse pole. In muon decay at q^2 -> 0 the q^mu q^nu terms are contracted with massless lepton currents
(q.J = 0 for massless fermions), and the Goldstones do not couple to massless leptons, so neither enters G_F.

## 6. Delta r (SPEC section 3)

Bare quantities: M_W0^2 = M_W^2 - Pi_W(M_W^2), M_Z0^2 = M_Z^2 - Pi_Z(M_Z^2), e_0 = e (no Higgs-containing photon or
gamma-Z diagram), bare tree relations g_0 = e/s_0, s_0^2 = 1 - M_W0^2/M_Z0^2. To first order,

  s_0^2 = s^2 + c^2 [Pi_W(M_W^2)/M_W^2 - Pi_Z(M_Z^2)/M_Z^2],

  G_F/sqrt2 = g_0^2 /(8 (M_W0^2 + Pi_W(0))) = (pi alpha/(2 s^2 M_W^2)) / {[1 + (c^2/s^2)(Pi_W(M_W^2)/M_W^2 - Pi_Z(M_Z^2)/M_Z^2)][1 + (Pi_W(0) - Pi_W(M_W^2))/M_W^2]}.

Comparing with G_F/sqrt2 = (pi alpha /(2 s^2 M_W^2))/(1 - Delta r):

  **Delta r_H = [Pi_W(M_W^2) - Pi_W(0)]/M_W^2 + (c^2/s^2) [Pi_Z(M_Z^2)/M_Z^2 - Pi_W(M_W^2)/M_W^2].**

Tadpoles: an H tadpole T attaches through the HVV vertex and an H propagator at zero momentum, giving a q^2-independent
Pi_V proportional to (HVV coupling) = g M_W for W and g M_Z/c for Z; divided by M_V^2 both are g T/(M_W m_H^2) x common factor. A common
constant t in Pi_W/M_W^2 and Pi_Z/M_Z^2 drops out of both brackets of Delta r. The seagull (c) has the same property
(A0/4 times g^2/M_W^2 vs (g^2/c^2)/M_Z^2 = g^2/M_W^2) and therefore also drops out of Delta r, though it is in sigma_W, sigma_Z.
(The tadpole is xi dependent through Goldstone and ghost loops; it is m_H dependent too; both drop out.)

Inserting step 4:

  Delta r_H = -(alpha/(4 pi s^2 M_W^2)) { f_W(M_W^2) - f_W(0) + (c^2/s^2) [ f_Z(M_Z^2) - f_W(M_W^2) ] }

and the export is Delta r_H(m_H) - Delta r_H(M_W). Since Pi has no xi dependence, neither has Delta r_H: **xi-independent**.

## 7. Scale independence (check)

The mu dependence equals the Delta dependence (ln mu^2 comes with Delta). Delta-coefficient of f_V(p^2): M_V^2 - (M_V^2 + m_H^2)/4 + p^2/12.
In Delta r_H: f_W(M_W^2) - f_W(0) -> M_W^2/12; f_Z(M_Z^2) - f_W(M_W^2) -> (M_Z^2 - M_W^2)(1 - 1/4 + 1/12) = (5/6) s^2 M_Z^2.
Total: -(alpha/(4 pi s^2))(1/12 + 5/6) = -(alpha/(4 pi s^2)) (11/12) times Delta: m_H-independent, so it cancels in
Delta r_H(m_H) - Delta r_H(M_W) (the subtraction also removes the m_H-independent polynomial terms, e.g. the "+1" of B00
whose m_H^2/4 is q^2-independent and common to W and Z). The raw Pi(q^2) have mu-dependence linear in q^2 (A0, B0, B00 UV parts).

## 8. Large m_H (log_coefficient)

For m_H -> infinity at fixed p^2, M: B0 = -ln(m_H^2/mu^2) + 1 + O(M^2/m_H^2 ln), and, splitting ln D = ln m_H^2 + ln(x + (1-x)M^2/m_H^2 - ...),
the ln m_H^2 coefficient of B00 is -(1/2) int D = -[(M^2+m_H^2)/4 - p^2/12]; the remaining integral has no further ln m_H^2 except in
terms suppressed by M^2/m_H^2 (checked: int_0^1 x ln(x+eps) and int ln(x+eps) contain eps ln eps only at O(eps)).
So the ln m_H^2 coefficient of f_V(p^2) is -M_V^2 + (M_V^2 + m_H^2)/4 - p^2/12 (minus the Delta coefficient, as it must be),
and in Delta r_H:

  B = -(alpha/(4 pi s^2)) [ -1/12 - (c^2/s^2)(5/6)(M_Z^2 - M_W^2)/M_W^2 ] = (alpha/(4 pi s^2)) (1/12 + 5/6) = **11 alpha /(48 pi s^2)**,

xi independent (screening: only logarithmic m_H growth). The code builds B from these Feynman-parameter coefficients.

## 9. Independent second route (run `python3 higgs_dr_xi.py`)

1. **Unsplit R_xi propagator.** Evaluate the H-W diagram with the SPEC propagator as written:
   Pi_HW = -(g^2/16 pi^2) M^2 [B0(q^2;M,m_H) - (1-xi) C00(q^2; xi)], with C00 from step 3 by direct 2-D numerical quadrature
   over the Feynman simplex (no partial fractions), plus Pi_b (B00 by direct 1-D numerical quadrature of the Feynman integral, not the closed
   form) plus Pi_c. Compare with sigma_W, sigma_Z for xi = 0, 0.3, 4, 25 at several q^2.
2. Measured large-m_H slope of delta_r_higgs_rel vs the analytic B.
3. mu-independence and xi-spread of delta_r_higgs_rel printed.

## 10. Numerics (SPEC section 6)

* Closed forms: D = a x^2 + b x + c, a = p^2, b = m1^2 - m0^2 - p^2, c = m0^2. ln D = ln|a| + ln|x - r1| + ln|x - r2| (real parts;
  D > 0 on [0,1] below threshold, so no branch issue), roots by the cancellation-free quadratic formula; int_0^1 x^n ln|x - r| (n = 0,1,2)
  from the antiderivatives in u = x - r (u^k ln u -> 0 at u = 0 handles the massless Landau-gauge Goldstone). Linear and constant D
  (p^2 = 0, equal masses) are separate branches.
* Precision: mpmath with a local working precision (mp.workdps inside each export, never global), chosen as
  40 + 3 log10(1 + |b/a|) + 2 log10(1 + m_H^2/M^2) + ... digits, which covers the cancellations from a large root (|r|^3 terms)
  and the m_H^2 terms that cancel in the q^2 differences, up to m_H = 1e14 M_W. Exports return floats; relative accuracy ~1e-15 (float limited).
* Threshold: the formulas assume q^2 < (m_H + M_V)^2 (real Pi); above threshold the code returns Re Pi (ln|D| = Re ln(D - i0)), which is
  not validated beyond a spot check and not needed.
* Checks run: route 2 (unsplit propagator, numerical quadrature) agrees with the closed form to all printed 13 digits for xi = 0, 0.3, 1, 4, 25
  at q^2 = -2 M_W^2, 0, M_W^2, M_Z^2 (m_H = 300), and at m_H = 1, 11, M_Z, 2 M_W (pseudo-threshold), M_W(1+1e-12); delta_r_higgs_rel at
  m_H = 1e10, 1e14 M_W is unchanged when 60 extra digits are added; measured slope between 1e12 and 1e14 M_W equals B to 1e-15;
  the xi spread of delta_r_higgs_rel is exactly 0 and the mu shift is 0 to float precision. Only q^2 <= M_Z^2 enters Delta r, and (m_H + M_V)^2 > M_Z^2 always.

## Not derived / limitations

Nothing in the requested chain was left underived. Not claimed: the region q^2 >= (m_H + M_V)^2, and Pi^L (only the statement that it carries
the xi dependence).
