# Bosonic one-loop gauge-boson self-energies, 't Hooft-Feynman gauge — derivation (build bos_se-a)

Everything below follows from SPEC.md section 1 (Lagrangian, gauge fixing, ghosts) and section 2 (definition of
Sigma_T, MS-bar, O(eps) terms kept). Metric (+,-,-,-). A field with incoming momentum p is e^{-ipx}, so
d_mu -> -i p_mu. The module `bos_se.py` re-derives every step mechanically with sympy (section 9 lists the
code path for each step) so that the hand derivation here and the code are two routes to the same rules.

## 1. Real-field form of the theory (SPEC 1)

Gauge fields in the gauge basis W^1, W^2, W^3, B. Generators with the couplings absorbed:
T^a = g tau^a/2 (a = 1,2,3), T^4 = g'/2 * 1 (hypercharge 1/2). Then D_mu Phi = (d_mu - i T^a W^a_mu) Phi,
[T^a, T^b] = i f^{abc} T^c with f^{abc} = g eps^{abc} (zero if any index is 4), and
F^a_{mu nu} = d_mu W^a_nu - d_nu W^a_mu + f^{abc} W^b_mu W^c_nu, L_YM = -1/4 F^a F^a.

Higgs doublet in real components: Phi = ((phi1 + i phi2)/sqrt2, (phi3 + i phi4)/sqrt2), phi = (phi1, phi2, H + v, chi).
The complex linear map -i T^a becomes a real 4x4 antisymmetric matrix theta^a (block [[Re, -Im],[Im, Re]] per entry),
so D phi = d phi + theta^a W^a phi and (D Phi)^dag (D Phi) = 1/2 (D phi).(D phi).

Mass basis: W^3 = c Z + s A, B = -s Z + c A, i.e. W^gauge = O V with O orthogonal, V = (W1, W2, Z, A).
Rotated couplings: fhat^{abc} = O_{a'a} O_{b'b} O_{c'c} f^{a'b'c'} (still totally antisymmetric),
thetahat^a = O_{a'a} theta^{a'}. From here on all indices are mass-basis indices and the hats are dropped.

Expanding phi = u + eta, u = (0, 0, v, 0), eta = (phi1, phi2, H, chi):

    1/2 (D phi)^2 = 1/2 (d eta)^2 + 1/2 M2_{ab} V^a.V^b + V^{a mu} d_mu eta^T theta^a u          (mass, mixing)
                  + V^{a mu} (d_mu eta)^T theta^a eta                                          (VSS)
                  + K^{ab}_i V^a.V^b eta_i                                                     (VVS)
                  + 1/2 S^{ab}_{ij} V^a.V^b eta_i eta_j                                        (VVSS)

with M2_{ab} = (theta^a u).(theta^b u), K^{ab} = -1/2 {theta^a, theta^b} u, S^{ab} = -1/2 {theta^a, theta^b}
(using theta^T = -theta). The mass matrix is M2 = diag(g^2 v^2/4, g^2 v^2/4, (g^2+g'^2) v^2/4, 0), so
M_W = g v/2, M_Z = sqrt(g^2+g'^2) v/2 = M_W/c, M_A = 0 (checked by the code, `_check_tree`).

Potential: V = -mu^2 Phi^dag Phi + lambda (Phi^dag Phi)^2, minimum v^2 = mu^2/lambda, M_H^2 = 2 lambda v^2, the three
Goldstone directions are massless from V. Scalar self-couplings do not enter: the only diagrams with them are
Higgs tadpoles, which SPEC 2 excludes. Hence M_H enters only through the Higgs propagator.

Couplings in terms of the inputs: e = sqrt(4 pi alpha), c = M_W/M_Z, s = sqrt(1 - c^2), g = e/s, g' = e/c, v = 2 M_W/g.

## 2. Gauge fixing and ghosts (SPEC 1)

F^a = d.V^a - xi eta^T theta^a u, L_gf = -1/(2 xi) F^a F^a. The cross term -(1/xi)(d.V^a)(-xi eta^T theta^a u)
= (d.V^a) eta^T theta^a u cancels the mixing V^{a mu} d_mu eta^T theta^a u (integrate by parts). It leaves
-xi/2 sum_a (eta.theta^a u)^2: Goldstone G_a = eta.theta^a u / M_a with mass^2 xi M_a^2. In the real basis
theta^{W1} u, theta^{W2} u, theta^Z u each point along a single coordinate of eta (checked in code), so phi1, phi2
have mass^2 M_W^2, chi has M_Z^2 at xi = 1, and H has M_H^2.

Gauge transformation with parameter alpha^a: delta V^a = d alpha^a + f^{abc} V^b alpha^c, delta phi = -alpha^a theta^a phi.
L_FP = -cbar^a delta F^a [alpha -> c]
     = d cbar^a . d c^a + (d^mu cbar^a) f^{abc} V^b_mu c^c - xi cbar^a c^b (theta^b(u+eta)).(theta^a u)    (after integration by parts).
Ghost masses xi M2_ab (diagonal: u^{W1,W2} M_W, u^Z M_Z, u^A 0). The ghost-scalar vertices only enter diagrams with
external scalars, so the ghost-gauge vertex is the only one needed here.

Propagators (xi = 1), from the quadratic part (propagator = -(two-point vertex function)^{-1}, checked in code):
vector -i g^{mu nu}/(q^2 - M^2), scalar i/(q^2 - m^2), ghost i/(q^2 - m^2).

## 3. Feynman rules (vertex function = i x functional derivative of the action, all momenta incoming)

* VVV  V^a_mu(p1) V^b_nu(p2) V^c_rho(p3):  f^{abc} [g_{mu nu}(p1-p2)_rho + g_{nu rho}(p2-p3)_mu + g_{rho mu}(p3-p1)_nu]
  (from L_3 = -f^{abc} (d_mu V^a_nu) V^{b mu} V^{c nu}).
* VVVV a mu, b nu, c rho, d sigma:  -i [ f^{abe}f^{cde}(g_{mu rho}g_{nu sigma} - g_{mu sigma}g_{nu rho})
  + f^{ace}f^{bde}(g_{mu nu}g_{rho sigma} - g_{mu sigma}g_{nu rho}) + f^{ade}f^{bce}(g_{mu nu}g_{rho sigma} - g_{mu rho}g_{nu sigma}) ]
* VSS  V^a_mu, eta_i(p_i), eta_j(p_j):  theta^a_{ij} (p_i - p_j)_mu
* VVS  V^a_mu V^b_nu eta_i:  2 i K^{ab}_i g_{mu nu}
* VVSS V^a_mu V^b_nu eta_i eta_j:  2 i S^{ab}_{ij} g_{mu nu}
* ghost cbar^a(p) V^b_mu c^c:  f^{abc} p_mu   (p = incoming momentum on the antighost leg)

The code does not use this list: it extracts every vertex from the Lagrangian monomials (all leg permutations,
d -> -i p) and the list above is the hand check of that extractor (`_check_rules`).

## 4. Diagrams

External V^a_mu with momentum k into vertex 1, V^b_nu with k out of vertex 2. Line 1 carries q (vertex 1 -> 2),
line 2 carries k - q. D_1 = q^2 - m_1^2, D_2 = (q-k)^2 - m_2^2. With real fields and fully symmetrized vertex functions
the sum of 1PI diagrams iPi^{mu nu}_{ab} is

    (1/2) sum_{c,d} int Gamma^{(1)}_{a c d} P_c P_d Gamma^{(2)}_{b c d}           (c, d over all V and eta fields: VV, SS, VS, SV)
  - sum_{x,y}     int Gamma(cbar^x V^a c^y) P_x P_y Gamma(cbar^y V^b c^x)          (ghost loop, -1, no 1/2)
  + (1/2) sum_c   int Gamma^{(4)}_{a b c c} P_c                                    (seagulls: VVVV and VVSS)

with int = int d^dq/(2pi)^d mu^{2eps}. For the W (external W^1) this is, concretely:
VV bubbles (W^2 Z), (W^2 A); SS bubbles (phi H), (phi chi); VS bubbles (W H), (Z phi), (A phi) in both orderings;
ghost loops (u^W u^Z), (u^Z u^W), (u^W u^A), (u^A u^W); seagulls with W, Z, A loops (VVVV) and H, chi, phi loops (VVSS).
For gamma-gamma, gamma-Z, ZZ the code sums the same generic expressions over all fields; couplings that vanish drop out.

The 1PI sum is iPi^{mu nu}; with the tree vertex function -i g(k^2 - M^2) the dressed vertex function is
-i g (k^2 - M^2 - Pi), so SPEC's Sigma_T = -Pi_T (a mass counterterm (1/2) dM^2 V^2 gives Pi = dM^2, M^2 -> M^2 + dM^2,
i.e. Sigma = -dM^2: positive Sigma lowers the mass, as SPEC 2 says). The same sign is used for the A-Z mixing.

Transverse projection in d dimensions: Pi^{mu nu} = (g - kk/k^2) Pi_T + (kk/k^2) Pi_L,

    Pi_T = [ g_{mu nu} Pi^{mu nu} - k_mu k_nu Pi^{mu nu}/k^2 ] / (d - 1).

## 5. Loop reduction

int d^dq/(2pi)^d mu^{2eps} N/(D_1 D_2) = (i/16pi^2) I[N]. With 2 q.k = D_1 - D_2 + f, f = k^2 + m_1^2 - m_2^2, q^2 = D_1 + m_1^2,
int 1/D_2 = A0(m_2) (shift), int q.k/D_1 = 0, int q.k/D_2 = k^2 A0(m_2):

    I[1] = B0,  I[q.k] = (A0(m_2) - A0(m_1) + f B0)/2,  I[q^2] = A0(m_2) + m_1^2 B0,  I[(q.k)^2] = (k^2 A0(m_2) + f I[q.k])/2.

Seagull: int N/D_1 = (i/16 pi^2) N A0(m_1) for q-independent N (the only kind that occurs: asserted in code).
After both contractions the numerators have q-degree <= 2 (asserted). A0(m) = m^2 (Delta - ln(m^2/mu^2) + 1),
B0(k^2, m1, m2) = Delta - int_0^1 dx ln[(x m1^2 + (1-x) m2^2 - x(1-x) k^2 - i0)/mu^2], Delta = 1/eps - gamma_E + ln 4 pi.

O(eps) terms: each diagram is sum_j c_j(d) X_j with X_j in {A0, B0}, c_j rational in d. With d = 4 - 2 eps,
c_j(d) X_j = c_j(4) X_j^fin - 2 c_j'(4) Res(X_j) + c_j(4) Res(X_j) Delta + O(eps), Res(A0(m)) = m^2, Res(B0) = 1.
MS-bar drops the Delta term. The Delta coefficient (the UV pole) is kept separately as a check: it must equal
d Sigma / d ln mu^2 and be linear in k^2.

## 6. k^2 -> 0 and thresholds

B0^fin(k^2) = B0^fin(0) + k^2 Bbar(k^2), Bbar = (B0(k^2) - B0(0))/k^2, B0(0, m1, m2) = (A0(m1) - A0(m2))/(m1^2 - m2^2),
B0(0,m,m) = A0(m)/m^2 - 1, B0(0,0,m) = A0(m)/m^2. After this substitution every explicit 1/k^2 must cancel
symbolically (asserted in code), so the result is a polynomial in k^2, logs ln(m^2/mu^2) and k^2-polynomial x Bbar.
Bbar(0) = B0'(0) = int_0^1 x(1-x)/(x m1^2 + (1-x) m2^2) dx (closed form in code). Above threshold Re B0 is taken:
Re B0^fin = -int_0^1 ln|f(x)/mu^2| dx with f = k^2 (x - x_1)(x - x_2), integrated in closed form over the roots.
Photon in a loop: m = 0 is put directly in A0 (= 0) and B0 (finite: no IR divergence in these functions).

## 7. Second routes (checks)

1. Photon: Sigma^AA_T(0) = 0 symbolically, and the longitudinal part Pi^AA_L(k^2) = 0 for all k^2 (gauge invariance).
2. Independent loop integration: the same diagram numerators integrated with Feynman parameters (q = l + x k, d-dimensional
   angular average <(l.k)^2> = l^2 k^2/d, int 1/(l^2-D)^2 -> Delta - ln D, int l^2/(l^2-D)^2 -> (d/2) D (Delta + 1 - ln D),
   O(eps) rule applied to these d-dependent coefficients) and the x-integral done numerically; must agree with the closed
   A0/B0 form at every k^2, below and above thresholds.
3. Custodial limit g' -> 0 (s -> 0, M_Z -> M_W): Sigma^ZZ = Sigma^W identically.
4. mu dependence: d Sigma/d ln mu^2 equals the separately computed pole coefficient, linear in k^2; the AA pole has no k^0 term.
5. Feynman rules extracted by the code compared with section 3.

## 8. Results (produced by `_derive()`; Sigma = (alpha/4pi) x {...}, s^2 = 1 - c^2, B0(k^2) = B0^fin(k^2, ., .), A0 = A0^fin)

Each line: integral : coefficient (inside the braces). These are the code's output (`_derive()[name]["bfin"]`
collected by integral), with g^2 = e^2/s^2 and e^2/(16 pi^2) = alpha/(4 pi).

Sigma^AA:  B0(k^2,W,W) : -(3k^2 + 4M_W^2);  A0(W) : +4;  1 : -4 M_W^2
           equivalently  -(3k^2 + 4M_W^2) B0(k^2,W,W) + 4 M_W^2 B0(0,W,W)   (no rational term survives).
Sigma^AZ:  B0(k^2,W,W) : -[(18c^2+1)k^2 + (24c^2+8) M_W^2]/(6cs);  A0(W) : 2(6c^2-1)/(3cs);  1 : -[k^2 + (36c^2-6) M_W^2]/(9cs)
           at k^2 = 0 this is 2 M_W^2 ln(M_W^2/mu^2)/(sc) (non-zero in this gauge; vanishes at mu = M_W).
Sigma^ZZ:  B0(k^2,W,W) : -[48M_W^2c^4 + 32M_W^2c^2 - 20M_W^2 + (36c^4+4c^2-1)k^2]/(12c^2s^2)
           B0(k^2,H,Z) : +[(M_H^2c^2 - M_W^2)^2 - 2c^2 k^2 (M_H^2c^2 - 5M_W^2) + c^4 k^4]/(12c^6 s^2 k^2)
           A0(W) : (12c^4-4c^2+1)/(3c^2s^2);  A0(H) : -(M_H^2c^2 - M_W^2 - 2c^2k^2)/(12c^4s^2k^2);  A0(Z) : +(M_H^2c^2 - M_W^2 + 2c^2k^2)/(12c^4s^2k^2)
           1 : -[3M_H^2c^2 + 72M_W^2c^6 - 24M_W^2c^4 + 6M_W^2c^2 + 3M_W^2 + (4c^4-2c^2)k^2]/(18c^4s^2)
Sigma^W:   B0(k^2,0,W) : 2(M_W^4 - 2M_W^2k^2 - 5k^4)/(3k^2)
           B0(k^2,H,W) : +[(M_H^2 - M_W^2)^2 - 2k^2(M_H^2 - 5M_W^2) + k^4]/(12 s^2 k^2)
           B0(k^2,W,Z) : +[8M_W^4c^6 - 15M_W^4c^4 + 6M_W^4c^2 + M_W^4 - (16c^6+54c^4-10c^2)M_W^2k^2 - (40c^6-c^4)k^4]/(12c^4s^2k^2)
           A0(W) : +(M_H^2c^2 - 2M_W^2c^2 + M_W^2 + 20c^2k^2)/(12c^2s^2k^2);  A0(H) : -(M_H^2 - M_W^2 - 2k^2)/(12s^2k^2)
           A0(Z) : +(8c^2+1)(2c^2k^2 - s^2M_W^2)/(12c^2s^2k^2)
           1 : -[3M_H^2c^2 + 54M_W^2c^2 + 3M_W^2 + 2c^2k^2]/(18c^2s^2)

UV poles (coefficient of Delta, = d Sigma/d ln mu^2), x alpha/(4 pi):
AA: -3k^2;  AZ: -[(18c^2+1)k^2 + 12M_W^2]/(6cs);  ZZ: -[(18c^6+2c^4-c^2)k^2 + (24c^4-12c^2-6)M_W^2]/(6c^4s^2);
W: -[19c^2k^2 + (12c^2-6)M_W^2]/(6c^2s^2). All linear in k^2; the AA pole has no k^0 term (photon stays massless);
M_H does not appear in any pole (it would come only from tadpoles, excluded).

## 10. Numerics (SPEC 4)

* Scalar integrals: A0^fin(m) = m^2(1 - ln(m^2/mu^2)), A0(0) = 0; Re B0^fin by the closed root formula of section 6;
  Bbar(k^2) = (B0(k^2) - B0(0))/k^2 with exact B0'(0) = (a^2 - b^2 - 2ab ln(a/b))/(2(a-b)^3) (a = b: 1/(6a), one mass 0: 1/(2a)).
* The exported expression is `res[name]["num"]`: B0^fin(k^2) -> B0z + k^2 Bbar, where B0z = B0^fin(0) stays a numerical function
  (so M_H = M_W or M_Z needs no special case). The k^-2 part of that expression is a combination of B0z and logs that the code proves
  zero (B0z written out explicitly) and drops; what remains is a polynomial in k^2. So k^2 = 0 is exact (not extrapolated).
* Poles: cancelled only by MS-bar subtraction of Delta; the O(eps) x pole rational pieces are kept (section 5).
* Thresholds: real part (ln|f|); the photon in a loop is exactly massless (A0(0) = 0, B0(k^2, 0, M) finite).
* Precision: every export runs inside mp.workdps(40 + 3 ceil(log10 R)), R = ratio of the largest to the smallest non-zero scale among
  M_W^2, M_Z^2, M_H^2, mu^2, |k^2|. M_H = 1e14 GeV with k^2 = 1e-7 gives ~145 digits. The global mp.dps is never changed.
* Large M_H: Sigma^W(0), Sigma^ZZ grow like M_H^2 (no M_H^2 ln M_H^2 at k^2 = 0 after the A0(H)/B0 cancellations); checked to be
  finite and stable at M_H = 1e6, 1e14 GeV, continuous at k^2 -> 0.

## 11. Checks performed (output of `python3 bos_se.py`)

* 739 vertex cases (all label combinations of VVV, VVVV, VSS, VVS, VVSS, ghost) extracted from the Lagrangian = section 3 rules.
* Masses read from the quadratic Lagrangian: V (M_W, M_W, M_W/c, 0), S (M_W, M_W, M_H, M_Z), ghosts (M_W, M_W, M_Z, 0);
  V-S mixing cancelled by the gauge fixing; Feynman-gauge propagator form; potential minimum has no tadpole.
* Photon: Sigma^AA_T(0) = 0 identically; Pi^AA_L(k^2) = 0 identically (finite part and pole).
* W^1W^1 = W^2W^2, W^1W^2 = 0 (so Sigma^{W+W-} = Sigma^{W1W1}).
* Custodial limit c -> 1 (g' -> 0): Sigma^ZZ - Sigma^W = 0 identically, Sigma^AZ = 0.
* Second loop-integration route (Feynman parameters, q = l + xk, d-dim angular average, numerical x-integral split at the zeros
  of Delta): agrees with the PV closed form to all printed digits for all four Sigma at k^2 = -3, -0.7, +0.4 M_W^2, and above
  thresholds (k^2 = 4.5, 5, 7 M_W^2, M_H from 1 GeV to 1e14 GeV).
* mu dependence: numerical d Sigma/d ln mu^2 = the separately accumulated pole coefficient (10 digits).
* B0 real part above threshold vs direct numerical integration.

Nothing in the derivation is quoted; no step is left underived. The checks share the Lagrangian -> vertex extractor and the
diagram symmetry factors (these are cross-checked by the hand rules, by the photon Ward identity and by the custodial limit).
