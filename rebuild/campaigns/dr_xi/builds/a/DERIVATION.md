# DERIVATION: the bosonic one-loop Delta r in the general R_xi gauge

Build `a`, module `dr_xi.py`. Section 0 was written before any code (the plan). The rest records what was
derived and checked. All numbers below come from `python3 dr_xi.py` (log in `tmp/main_out.txt`) at
M_W = 80.38, M_Z = 91.19, M_H = 125 GeV, alpha = 1/128.

## 0. Postulates used (SPEC section 1)
- SU(2)xU(1), D = d - i g W^a T^a - i g' Y B, Higgs doublet Phi = (phi+, (v+H+i chi)/sqrt2), Y = 1/2,
  V = -mu^2 Phi^+Phi + lambda (Phi^+Phi)^2 at its minimum (mu^2 = lambda v^2).
- W^pm = (W1 -/+ i W2)/sqrt2, Z = c W3 - s B, A = s W3 + c B, e = g s = g' c.
- Massless leptons (nu, l)_L (Y = -1/2), l_R (Y = -1). No fermion loops.
- R_xi with one xi: L_GF = -(1/2xi) sum_A (d.V^A - xi G_A.S)^2, summed over the real basis (W1, W2, W3, B),
  with G_{Ar} fixed by cancelling the V^A.dS_r mixing of the scalar kinetic term. Ghosts:
  L_FP = -cbar^A (dF^A/dtheta^B) c^B with dW^a = d theta^a + g eps^{abc} W^b theta^c, dPhi = i(g theta^a T^a + g' theta^4 Y) Phi.
- Higgs tadpoles: cancelled by the tadpole counterterm, not included (section 6).
- Inputs: pole masses M_W, M_Z, M_H; alpha = e^2/4pi with e the Thomson charge; s^2 = 1 - M_W^2/M_Z^2.
  G_F from muon decay at zero momentum transfer, massless leptons, Fermi-model QED subtracted;
  M_W^2 s^2 = pi alpha/(sqrt2 G_F) (1 + Delta r).

## 1. Feynman rules (derived in code, `Lagrangian` and `Mass-basis vertices` sections)
Each Lagrangian term is written as a product of field slots (field, derivative index, vector index) with all
Lorentz indices contracted pairwise: the scalar kinetic term (D Phi)^+(D Phi) is expanded with commuting symbols
(each monomial has exactly two Lorentz-carrying objects), the potential, the Yang-Mills cubic
-g eps^{abc}(d_a W^a_b) W^{b a} W^{c b} and quartic -(g^2/4) eps^{abe} eps^{cde} W^a W^b W^c W^d terms, the ghost
terms (d cbar^A).(g eps^{ABC} V^B c^C) + xi cbar^A G_{Ar} R_{rB}(S) c^B, and the lepton currents. The fields are then
rotated to the mass basis. A vertex = i x (sum over all assignments of the legs to the slots) x coefficient, momenta
incoming, d_mu -> -i k_mu. Propagator pairing follows from the quadratic form (<W+ W->, <phi+ phi->, <u- bar u+> ...).
Checks of the quadratic part (printed by `_mass_check`): photon massless, no A-Z mass mixing,
M_W^2 W+W-, M_Z^2/2 Z Z with M_Z = M_W/c, -M_H^2 H^2/2 (M_H^2 = 2 lambda v^2), Goldstone masses from L_GF
-xi M_W^2 phi+phi-, -xi M_Z^2 chi^2/2, ghost masses xi M_W^2, xi M_Z^2, photon ghost massless; the V-dS mixing is
cancelled by construction. Examples of derived vertices: A W+ phi-: i e M_W g^{mu nu}; W+ Z phi-: -i e M_W (s/c) g;
H W+W-: i e M_W/s g; lepton couplings: A: -e (L and R), Z: (e/sc)(T3 - s^2 Q), W: e/(sqrt2 s) P_L.
Propagators (SPEC): vector -i[g - (1-xi)kk/(k^2 - xi M^2)]/(k^2 - M^2), written as
-i g/(k^2-M^2) + i kk/(M^2 (k^2-M^2)) - i kk/(M^2 (k^2 - xi M^2)); photon -i g/k^2 + i(1-xi) kk/k^4;
scalars and ghosts i/(k^2 - m^2); leptons i kslash/k^2.

## 2. Renormalization and the two classes (my sign conventions)
1PI vector two-point function = -i g^{mu nu} Sigma_T(k^2) + k^mu k^nu terms; propagator -i/(k^2 - M^2 + Sigma_T).
Bare quantities: M_V0^2 = M_V^2 + Re Sigma_V(M_V^2), s0^2 = 1 - M_W0^2/M_Z0^2, e0 = e (1 + dZe).

**Charge.** Photon-Z propagator matrix near k^2 = 0 gives the effective photon current
J_A (1 - Sigma'_AA(0)/2) + J_Z Sigma_AZ(0)/M_Z^2 (Sigma_AA(0) = 0 is checked). For l_R the photon and Z vertex
corrections cancel the wave function exactly at zero momentum (abelian Ward identity, vector-like coupling along
one lepton line), J_Z(l_R) = -(e s/c) Q, hence

    dZe = Sigma'_AA(0)/2 + (s/c) Sigma_AZ(0)/M_Z^2 .

Cross-checks (computed diagrams, any xi): the neutrino charge vanishes, X_nu + (e/2sc) Sigma_AZ(0)/M_Z^2 = 0
(X_nu = W-loop photon vertices, photon on the W and on the internal lepton); and l_L has the same charge as l_R,
X_lW - eQ X_Sigma^W(l) - (e/2sc) Sigma_AZ(0)/M_Z^2 = 0. Both hold to 1e-58..1e-64 (poles and finite parts) at
xi = 0, 0.3, 1, 7, 1000.

**Muon decay at zero momentum.** G_F/sqrt2 = e0^2 / (8 s0^2 (M_W0^2 - Sigma_W(0))) (1 + d_VBW), so

    Delta r = SE + VBW,
    SE  = 2 dZe - (c^2/s^2)(Sigma_Z(M_Z^2)/M_Z^2 - Sigma_W(M_W^2)/M_W^2) + (Sigma_W(0) - Sigma_W(M_W^2))/M_W^2,
    VBW = 2 dv + d_box - (X_l + X_nu) - d_Fermi,

dv: 1PI W l nu vertex / tree vertex (both W vertices are equal); X_f: lepton 1PI self-energy i pslash P_L X_f at
p -> 0 (LSZ factor 1 - X_f/2 per leg, four legs: two charged leptons, two neutrinos); d_box: boxes / tree
(tree = (i e/(sqrt2 s))^2 (i/M_W^2) gamma^a P_L x gamma_a P_L).

**Diagrams.** SE class: gamma gamma, gamma Z, ZZ, WW two-point functions: VV, VS, SS bubbles (all
field pairs generated from the vertices), ghost loops (-1), seagulls (VVVV, VVSS); no fermion loops, no tadpoles.
VBW class (l -> nu W): (i) Z exchanged between l and nu; (ii) l emits gamma or Z, W internal, VWW vertex;
(iii) nu emits Z, W internal, ZWW vertex (Goldstones do not couple to massless leptons). Wave functions: l with
gamma, Z, W loops; nu with Z, W. Boxes (mu nu_e -> nu_mu e at zero momenta): W plus Z with the Z on any of the
four legs (4 boxes), W plus photon with the photon on mu and e (1 box). No WW box exists.

**Fermi subtraction.** In charge-retention order the one-loop photonic correction of the four-fermion theory at
zero momentum with massless leptons is vertex + wave function of a vector current, which cancel identically
(Lambda_mu(0,0) = -dSigma/dp^mu holds at the integrand level for any photon propagator and any shift-invariant
regulator, photon mass included). So d_Fermi = 0, and the lambda dependence of the full theory (gamma-W box,
lepton wave functions) must cancel by itself: checked (second route 4).

**Where the photon-Z mixing goes.** SE contains all of dZe (including Sigma_AZ(0)); VBW is the literal set of
1PI vertex, box and wave-function diagrams. VBW is UV divergent and mu dependent (SPEC). The combination
VBW + (2/sc) Sigma_AZ(0)/M_Z^2 is UV finite and mu independent for every xi; at xi = 1 it equals
0.00709277086384626, identical (15 digits) to the closed form alpha/(4 pi s^2)[6 + (7 - 4 s^2)/(2 s^2) ln c^2] that I
remember for the Feynman-gauge vertex+box remainder (used only as a check, not in the code).

## 3. Loop integrals and reductions
d = 4 - 2 eps, MS-bar at mu. int d^dq/(2pi)^d f = (i/16 pi^2) <f>, A0(m) = m^2(Delta + 1 - ln m^2/mu^2),
T_n(m) = <1/(q^2-m^2)^n> = prod_{j<n} (d-2j)/(2j) * A0/m^{2(n-1)}, B0(p^2; m1, m2) = Delta - int_0^1 ln[(x m1^2 + (1-x) m2^2
- x(1-x) p^2 - i0)/mu^2] dx (real part via the roots of the quadratic; checked against quadrature).
Coefficients c(d) are kept exact; the finite part of c(d) I is c(4) F - 2 c'(4) P (P = residue of the pole).
Scaleless integrals vanish. Sigma_T = -A/16pi^2 where A = (g_{mu nu}Sigma^{mu nu} - p_mu p_nu Sigma^{mu nu}/p^2)/(d-1).
- p^2 = M^2 (PV route): numerators in q^2, q.p are rewritten in the inverse propagators D1, D2 and reduced to A0,
  B0. The photon's (1-xi) kk/k^4 term produces B(2,1) and B(1,2), reduced by integration by parts:
  E1: (d-3) B11 - 2 m1^2 B21 - T2(m2) - (m1^2+m2^2-p^2) B12 = 0, E2: (d-3) B11 - 2 m2^2 B12 - T2(m1) - (m1^2+m2^2-p^2) B21 = 0.
  After cancellation the coefficients of Sigma_W(p^2), Sigma_Z(p^2) have no 1/(p^2 - M_W^2) or 1/(xi-1) factors:
  the on-shell self-energies are IR finite in every xi with a massless photon.
- p^2 -> 0 (Taylor route) for Sigma'_AA(0), Sigma_AZ(0), Sigma_W(0), Sigma_AA(0): expand in p, symmetric
  integration, vacuum integrals by numerical partial fractions (equal masses merged exactly, e.g. xi = 1).
- Lepton diagrams: all external momenta zero, vacuum integrals. Single lines: d-dimensional Dirac algebra with an
  anticommuting gamma5 (only left-handed couplings enter a left-handed line), reduced by d-dim traces
  Tr(gamma_mu S^mu)/(4d). Wave function: first order in p of S(p+q).
- Boxes: qslash qslash = q^2 is used on each line first. Every structure except (W g-part) x (V g-part) is then
  exactly gamma^a x gamma_a in d dimensions; the (g x g) structures are UV finite and are reduced in 4d by an
  explicit-matrix Fierz projection (residual checked to 1e-9; factors 16 and 4).
- Photon: in the lepton diagrams it has mass lambda in the R_xi form -i[g - (1-xi)kk/(k^2 - xi lambda^2)]/(k^2-lambda^2),
  lambda^2 = 1e-30 M_W^2, 60+ digits; except the box terms built with the xi-pole part kk/(M_W^2(k^2 - xi M_W^2))
  of the W propagator, which use a massless photon (they are IR finite for xi > 0, so this is the lambda -> 0
  limit; at xi = 0 they are dimensionally regulated, as in the self-energies). Self-energies: massless photon.

## 4. Results
| xi | SE (mu = M_W) | VBW (mu = M_W) | total |
|---|---|---|---|
| 0 | -5.263125102726e-03 | 9.560655834089e-03 | 4.297530731363824e-03 |
| 0.3 | -3.743383537985e-03 | 8.040914269349e-03 | 4.297530731363824e-03 |
| 1 | -2.795240132482e-03 | 7.092770863846e-03 | 4.297530731363824e-03 |
| 4 | 7.805993898808e-03 | -3.508463167444e-03 | 4.297530731363824e-03 |
| 25 | 1.530211636649e-01 | -1.487236329335e-01 | 4.297530731363824e-03 |
| 1000 | 1.445567922011e+01 | -1.445138168938e+01 | 4.297530731363824e-03 |

Total 1/eps poles: < 1e-33 (they cancel); total identical at mu = 30, M_W, 900 GeV.
(M_H = 1 GeV: -2.5226e-3; 1e4: 2.5078e-2; 1e10: 9.5677e-2 GeV, the same at every xi.)

## 5. Structure of the xi dependence (mu = M_W)
| xi | dZe | Sigma_W(M_W^2)/M_W^2 - Sigma_Z(M_Z^2)/M_Z^2 | (Sigma_W(0)-Sigma_W(M_W^2))/M_W^2 | 2 dv | box | -(X_l+X_nu) |
|---|---|---|---|---|---|---|
| 0 | -2.072330e-4 | -2.762263e-3 | 4.773974e-3 | 1.107569e-3 | 1.581195e-3 | 6.871892e-3 |
| 0.3 | -2.072330e-4 | -2.762263e-3 | 6.293715e-3 | 1.692564e-3 | 1.530045e-2 | -8.952096e-3 |
| 1 | -2.072330e-4 | -2.762263e-3 | 7.241859e-3 | -1.821816e-5 | 4.747001e-2 | -4.035902e-2 |
| 4 | -2.072330e-4 | -2.762263e-3 | 1.784309e-2 | -2.508206e-2 | 1.782214e-1 | -1.566479e-1 |
| 25 | -2.072330e-4 | -2.762263e-3 | 1.630583e-1 | -4.037943e-1 | 1.060309 | -8.052382e-1 |
| 1000 | -2.072330e-4 | -2.762263e-3 | 1.446572e+1 | -3.909838e+1 | 4.022481e+1 | -1.557781e+1 |

- xi independent: dZe (although Sigma'_AA(0) and Sigma_AZ(0) separately depend on xi) and the combination
  Sigma_W(M_W^2)/M_W^2 - Sigma_Z(M_Z^2)/M_Z^2, hence ds^2/s^2. The on-shell Sigma_W(M_W^2), Sigma_Z(M_Z^2) do depend on
  xi (tadpoles are excluded), but only through a common Sigma_V(M_V^2)/M_V^2 shift (the xi dependence a tadpole
  would remove; the pole masses are xi independent).
- So the whole xi dependence of SE is (Sigma_W(0) - Sigma_W(M_W^2))/M_W^2 (the W propagator at zero momentum);
  in VBW the vertex, box and wave function all depend on xi; [Sigma_W(0)-Sigma_W(M_W^2)]/M_W^2 + 2 dv + box - X_l - X_nu
  is xi independent.
- Landau limit: as xi -> 0+, (Sigma_W(0)-Sigma_W(M_W^2))/M_W^2 -> -(3/4)(alpha/4pi) ln xi and box -> +(3/4)(alpha/4pi) ln xi
  (soft photon with the gamma-W-phi coupling in Sigma_W(0); soft photon with the xi-pole part of the W in the
  gamma-W box), so the classes diverge logarithmically while the total stays fixed. At exactly xi = 0 (massless
  Goldstones) this IR divergence is regulated dimensionally on both sides and subtracted with the UV poles
  (MS-bar): SE(0) and VBW(0) above are those values; the total at xi = 0 agrees with xi > 0 to all digits.
- Large xi: the classes grow roughly like xi (14.46 at xi = 1000) and cancel to 1e-16 relative.

## 6. Tadpoles
A Higgs tadpole T adds a k-independent constant to Sigma_W and Sigma_Z proportional to M_V^2 (H V V coupling
proportional to M_V^2/v), so Sigma_W^T/M_W^2 = Sigma_Z^T/M_Z^2, and nothing to Sigma_AA, Sigma_AZ (no H A A, H A Z
couplings) or to the lepton diagrams (no Higgs coupling to massless leptons). In Delta r it would enter only through
Sigma_Z/M_Z^2 - Sigma_W/M_W^2 and Sigma_W(0) - Sigma_W(M_W^2), both of which cancel it. So cancelling the tadpoles
with the tadpole counterterm changes the individual mass counterterms (and makes Sigma_V(M_V^2) xi dependent)
but not Delta r.

## 7. Second route (independent checks, `python3 dr_xi.py`)
1. Ward identities: Sigma_AA(0) = 0 and transversality of Sigma_AA; neutrino charge zero; L/R charge universality.
2. Taylor (p -> 0) route vs PV/IBP route at p^2 = 1e-3 GeV^2 for AA, AZ, WW: agree (to O(p^4)).
3. B0 closed form vs Feynman-parameter quadrature.
4. lambda^2/M_W^2 = 1e-30 vs 1e-22: VBW unchanged (xi = 0, 1, 7).
5. Boxes entirely in 4d (alternative bookkeeping, valid for xi > 0): identical to the mixed treatment.
6. Feynman gauge: VBW + (2/sc) Sigma_AZ(0)/M_Z^2 = alpha/(4 pi s^2)[6 + (7-4 s^2)/(2 s^2) ln c^2] at mu = 30 and 300 GeV.
7. Large M_H: slope d Delta r/d ln M_H^2 between 1e5 M_W and 1e6 M_W equals 11 alpha/(48 pi s^2) to 9e-10 in every xi
   (the M_H^2 ln M_H^2 terms cancel between Sigma_W/M_W^2 and Sigma_Z/M_Z^2; what is left is
   (alpha/16 pi s^2)(11/3) ln M_H^2 + const).
8. Poles cancel, mu independence, xi independence (0 ... 1000).

A check that failed and was understood: with a massless dimensionally regulated photon in all lepton diagrams
(boxes in 4d) the total shifts by exactly (3/2) alpha/4pi (0.0042975 -> 0.0033650), the evanescent mismatch between the
4d Fierz reduction and the d-dim IR pole. The photon-mass regulator (SPEC) avoids it, and matches check 6.

## 8. What is not derived by hand
No closed-form expression in xi is written out: the general-xi results are produced by the code's computer
algebra (exact in d, masses and xi) and evaluated numerically. The closed form in check 6 is a recollection,
used only for comparison. See QUESTIONS.md for the conventions chosen where SPEC is open.
