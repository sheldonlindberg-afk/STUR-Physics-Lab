# bos_se-b: bosonic gauge-boson self-energies, 't Hooft-Feynman gauge

Everything below is derived from the Lagrangian of SPEC section 1. Generator code: `gen/` (vtx.py = Feynman rules from L,
engine.py = diagrams + d-dim algebra + PV reduction, run_all.py, codegen.py -> the coefficients pasted into bos_se.py).

## 1. Lagrangian and Feynman rules (SPEC 1)
L = -1/4 W^a_{mn}W^{a mn} - 1/4 B_{mn}B^{mn} + (D_m Phi)^dag (D^m Phi) - V + L_gf + L_gh, with
W^a_{mn} = d_m W^a_n - d_n W^a_m + g eps^{abc} W^b_m W^c_n, D = d - i g W^a tau^a/2 - i g' B/2, Phi = (phi+, (v+H+i chi)/sqrt2),
V = -mu^2 Phi^dag Phi + lam (Phi^dag Phi)^2 (mu^2 = lam v^2 from the minimum), W+- = (W1 -+ i W2)/sqrt2, Z = c W3 - s B, A = s W3 + c B,
c = g/N, s = g'/N, N = sqrt(g^2+g'^2), e = g s.
* Vertices are extracted by machine (gen/vtx.py): all fields are plane waves exp(-ipx) with symbolic couplings, the L evaluated in
  explicit 4-d components at random integer kinematics, the coefficient of the product of slot amplitudes (this includes every
  assignment of slots to identical fields, i.e. the symmetry factors) is fitted on the complete basis of Lorentz structures
  (g_ij p_l.e_k for VVV; g_ij g_kl for VVVV; e.p for VSS; g for VVS, VVSS, ...) by exact rational least squares, and the
  residual must vanish identically (it does; this also proves the basis is complete). Vertex Feynman rule = i * coefficient.
* Quadratic part (checked from L, same machinery): M_W = g v/2, M_Z = N v/2 = M_W/c, M_H^2 = 2 lam v^2, phi+- have mass^2 M_W^2,
  chi has M_Z^2, A massless, kinetic terms canonical, A-Z and A-chi, Z-chi, W-phi mixings vanish, H has no linear term.
* Gauge fixing (xi=1): L_gf = -F^+F^- - F_Z^2/2 - F_A^2/2, F^+- = d.W+- (+-)(-)... fixed by requiring the W-phi and Z-chi mixing to
  cancel: F^+ = d.W^+ - i M_W phi^+, F^- = d.W^- + i M_W phi^-, F_Z = d.Z - M_Z chi, F_A = d.A  (gen/vtx.py, GF_A = GF_B = -1; the
  other sign leaves a mixing 2 M_W p.e). Vector propagators -i g^{mn}/(k^2-M^2), scalars i/(k^2-M^2).
* Ghosts: L_gh = - sum_a cbar^a delta_c F^a, delta W^a = d theta^a + g eps^{abc} W^b theta^c, delta B = d theta^0,
  delta Phi = i (g tau.theta/2 + g' theta^0/2) Phi, theta -> ghost fields c^+-, c^Z, c^A (rotated like the gauge fields).
  The machine gives the kinetic terms and the ghost masses M_W^2 (c^+-), M_Z^2 (c^Z), 0 (c^A) (from the phi part of F), and the
  cbar c V couplings (the only ghost vertices a one-loop gauge-boson self-energy needs).

## 2. Diagrams (SPEC 2)
Amplitude of the 1PI two point function = -i Sigma_T g^{mn} + ... (from D = D0 + D0 (i Pi) D0 = -i g/(k^2-M^2-Pi), Sigma = -Pi), so
Sigma_T = i * (g^{mn} coefficient). With operators X, Y external (k incoming at X), internal ordered pair (a,b), partners a~,b~:
* bubble:  Sigma = (1/2) sum_{(a,b)} c_a c_b/(16 pi^2) R,  c = i (scalar), -i (vector, contraction with g), R = g^{mn} coefficient of
  the PV-reduced int V1(X,a,b) V2(Y,a~,b~)/(D1 D2), vertices = coefficients of L. Ordered pairs with 1/2 gives the right symmetry
  factor for identical and for distinct internal lines.
* ghost loop: Sigma = + R/(16 pi^2) (fermi sign -1 included), sum over (cbar_i, c_j) once (arrow orientation).
* seagull (quartic vertex, no momentum dependence): Sigma = (1/2) sum_a c_a/i^... = +- (1/32 pi^2) A0 * (g^{mn} coefficient of the contracted L4),
  + for scalars, - for vectors, ordered a over all operators (a, a~ = partner).
Diagram content (all generated; entries whose coupling vanishes identically are dropped automatically):
* AA: W+W- (triple), W phi (A W phi vertex = e M_W), phi+phi-, c^+- ghosts, seagulls WWAA, phi phi AA.
* AZ: the same set with the Z couplings (Z W W: e c/s, Z phi phi: e(c^2-s^2)/(2sc), Z W phi: -e M_W s/c).
* ZZ: W+W-, W phi, phi phi, ghosts c^+-, Z H, chi H, seagulls WWZZ, phi phi ZZ, chi chi ZZ, HHZZ (and WWZZ).
* W: gamma W, Z W, H W, gamma phi, Z phi, phi H, phi chi, ghosts (c^Z, c^+-), (c^A, c^+-), seagulls gamma gamma, Z Z, gamma Z (cancels or not as generated), W W, phi phi, chi chi, H H.
Excluded: Higgs tadpoles (SPEC); fermion loops (not in the theory here).

## 3. d-dimensional reduction (conventional DR, g^m_m = d)
Denominators D1 = q^2 - m1^2 (momentum q), D2 = (q+k)^2 - m2^2; int d^dq/(2pi)^d mu^{2e} -> (i/16 pi^2) x [PV function], Delta = 1/e - gamma + ln 4pi.
* A0(m) = int 1/D = m^2(Delta + 1 - ln m^2/mu^2); B0 = Delta - int_0^1 dx ln[(x m2^2 + (1-x) m1^2 - x(1-x) k^2 - i0)/mu^2].
* Numerator algebra: contract all indices with g (g^a_a = d), leaving scalars q.q, q.k, k.k and external g^{mn}, q^m q^n, ...
  q.q = D1 + m1^2  ->  int q.q/(D1D2) = A0(m2) + m1^2 B0;  2 q.k = D2 - D1 - k^2 - m1^2 + m2^2 -> int q.k/(D1D2) = [A0(m1) - A0(m2) - f B0]/2, f = k^2+m1^2-m2^2;
  int q^m q^n -> g^{mn} B00 + k^m k^n B11 with (contracting with g and kk, using int (q.k)^2 = [k^2 A0(m2) - f int q.k]/2)
  B00 = [A0(m2) + 2 m1^2 B0 + f B1]/(2(d-1)), B1 = int q.k/(k^2 D1D2).
* O(eps): every coefficient is a rational function of d = 4-2 ep; with Delta = 1/ep, the finite part is c(0)*[finite loop function] + c'(0)*(pole coefficient)
  (= the "-2 x residue" rational terms), the remaining Delta terms are subtracted (MS-bar). The pole coefficients are polynomials of degree 1 in k^2 (checked by the gate).
* **Second route (independent algebra)**: the g^{mn} coefficient was extracted twice: (i) direct tensor reduction as above, (ii) transverse projector
  A_T = [g_mn T^{mn} - k_m k_n T^{mn}/k^2]/(d-1) with scalar integrals only (needs int (q.k)^2, no B00). run_all.py checks they agree identically for all four Sigma (they do).
Result in units alpha/(4 pi) = e^2/16 pi^2 (A0f(m) = m^2(1 - ln m^2/mu^2), B0f the finite B0; kk = k^2): see the `_terms_*` functions in bos_se.py, e.g.
 Sigma_AA = -(3 k^2 + 4 M_W^2) B0f(k^2;W,W) + 4 A0f(W) - 4 M_W^2,  pole -3k^2;
 Sigma_AZ(0) = -(alpha/2pi) M_W^2/(s c) B0(0;W,W);  W pole (19 k^2/6 + ...)/(-s^2) etc.

## 4. Numerics (SPEC 4)
B0 finite part is evaluated in closed form: Q(x) = k^2 x^2 + (m2^2-m1^2-k^2) x + m1^2 = k^2 (x-r1)(x-r2),
-int ln|Q/mu^2| = -ln|k^2/mu^2| - Re[(1-r)ln(1-r) + r ln(-r) - 1] summed over the two (possibly complex) roots (real part above threshold; thresholds
and zero masses handled: roots at 0/1 contribute their limits). mpmath workdps is set inside every export (70 + 4 log10 of the scale ratio,
~300 digits at M_H = 1e14 and k^2 = 0), never globally. k^2 = 0 is evaluated as the analytic limit k^2 = 1e-30 M_W^2 (error O(1e-30)).
Photon mass -> 0 is taken inside (m = 0 in B0 and A0(0) = 0).

## 5. Checks performed (bos_se.py `__main__`, gen/)
* photon Ward identity Sigma_AA(0) = 0 (analytic: -4M_W^2 B0(0;W,W) + 4 A0 - 4 M_W^2 = 0, and numerically ~1e-30).
* UV pole is a polynomial of degree 1 in k^2 and d Sigma/d ln mu^2 = (alpha/4pi) pole (numerical derivative agrees to 1e-7).
* B0 closed form vs numerical Feynman-parameter quadrature (below/above threshold, massless lines).
* Sigma_AZ(0) = -(alpha/2pi) M_W^2/(sc) B0(0;W,W) (closed form vs module).
* Higgs screening: d[Sigma_ZZ(0)/M_Z^2 - Sigma_W(0)/M_W^2]/d ln M_H^2 -> -3 alpha/(16 pi c^2) for M_H >> M_W (agrees to 6 digits at M_H = 1e6): checks the H, chi, phi, ghost sectors of ZZ and W together.
* two independent tensor-algebra routes agree identically (above); the precision of every sampled point was re-run with +150 digits (no change at 1e-9).
Not derived/unverified: nothing omitted; the overall sign of Sigma follows the SPEC definition (positive Sigma lowers M^2 - Sigma) as derived in section 2.
