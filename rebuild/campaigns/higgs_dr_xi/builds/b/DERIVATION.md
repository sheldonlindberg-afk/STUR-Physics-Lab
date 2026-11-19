# DERIVATION: gauge-parameter dependence of the Higgs part of Delta r (build higgs_dr_xi-b)

## Answer first
In the R_xi gauge the g^{mu nu} part of the Higgs-containing W and Z self-energies is **exactly independent of xi**
(any xi >= 0, Landau gauge included), for every q^2 and m_H, before any on-shell condition is imposed. The reason is an
algebraic cancellation between the xi-dependent piece of the H-V diagram and the H-Goldstone diagram (section 3).
Consequently Delta r_H(m_H) - Delta r_H(M_W) is xi-independent, and B = 11 alpha / (48 pi s^2) is xi-independent.
I did not force this: the exports evaluate each diagram separately with its own xi and the cancellation appears numerically.

## 1. Postulates used (SPEC section 1)
Phi = (phi+, (v+H+i phi0)/sqrt2), D = d - i g W^a tau^a/2 - i g' B/2, M_W = g v/2, M_Z = M_W/c, s^2 = 1 - M_W^2/M_Z^2,
e = g s, alpha = e^2/4pi. Expanding |D Phi|^2 gives (v -> v + H):
* H W+ W-: g M_W (vertex i g M_W g^{mu nu});  H Z Z: g M_Z/c (vertex i g M_Z/c g^{mu nu}) [(1/2)(g^2/4c^2)(v+H)^2 Z^2 term]
* H H W+W-: (g^2/4) ; H H Z Z: g^2/(8c^2) (seagull; vertex i g^2/2 g^{mu nu} and i g^2/(2c^2) g^{mu nu})
* H W-+ phi+-: (g/2) W_mu (H d^mu phi - phi d^mu H); H Z phi0: (g/2c) Z_mu (H d^mu phi0 - phi0 d^mu H).
R_xi gauge fixing -(1/2xi)(d.V - xi M_V phi_V)^2 cancels V-phi mixing, gives Goldstone mass^2 xi M_V^2, propagator
-i[g - (1-xi)kk/(k^2 - xi M^2)]/(k^2-M^2) and ghost mass^2 xi M^2.

Ghosts: the ghost-ghost-V vertex and the ghost-ghost-H vertex (~ xi g M/2) exist, but a one-loop V two-point function with ghosts
is a closed ghost loop with two V vertices: no H line. Ghosts therefore do not enter the Higgs-containing V self-energies
(they enter the H self-energy and tadpoles, which are not needed).

## 2. Self-energies (SPEC section 2)
Convention: i[Pi g^{mu nu} + Pi^L q q]; propagator -i/(q^2-M^2-Pi) (checked by resumming the insertion), so the effective mass^2 is M^2+Pi.
Int d^dk/(2pi)^d = i/(16 pi^2) * (PV measure), K = 1/16pi^2, d=4-2eps, mu^{2eps}, drop Delta.
Feynman parameters, D_x = x m1^2 + (1-x) m2^2 - x(1-x) q^2:
* B0(q^2;m1,m2) = -Int_0^1 ln(D_x/mu^2) dx
* B00 = (1/2) Int_0^1 D_x [1 - ln(D_x/mu^2)] dx  (g^{mu nu} coefficient of Int k^mu k^nu/(..); exact d-dim integral
  Int l^mu l^nu/(l^2-D)^2 = g^{mu nu}/2 * (-Gamma(eps-1)) D^{1-eps}... , the "+1" is the O(eps) part of 1/d against the pole)
* A0(m) = m^2 (1 - ln(m^2/mu^2)).
Diagrams for W (Z: M_W->M_Z, g^2 -> g^2/c^2 in the vertices):
(a) H-V: iPi = (i g M)^2 Int g^{mu a} g^{nu b} [i/(k^2-mH^2)] D_ab(p), p=q-k, giving
    Pi_HV = -g^2 M^2 K [ B0 - (1-xi)*G ],  G = g-part of Int p^mu p^nu /((p^2-xi M^2)(p^2-M^2)(k^2-mH^2)).
    Partial fractions: (1-xi)/((p^2-xi M^2)(p^2-M^2)) = (1/M^2)[1/(p^2-M^2) - 1/(p^2-xi M^2)] so
    Pi_HV = -g^2 M^2 K [ B0(q^2;mH,M) - (1/M^2)( B00(q^2;mH,M) - B00(q^2;mH,sqrt(xi) M) ) ].
(b) H-phi: vertex a (p_phi - p_H)^mu, product of two vertices with i*i from propagators gives iPi = +a^2 Int (2k-q)^mu(2k-q)^nu/(..)
    so Pi_Hphi = a^2 K 4 B00(q^2;mH,sqrt(xi)M), a = g/2 (W), g/2c (Z)  -> g^2 K B00(q^2; mH, sqrt(xi)M) (W).
(c) seagull with H (symmetry factor 1/2): Pi = -(g^2/4) K A0(mH) (W), -(g^2/4c^2) K A0(mH) (Z). Sign check: delta M^2 = (g^2/4)<H^2>,
    <H^2> = -K A0.
Tadpoles dropped (section 4 below).

## 3. The xi cancellation
Sum: Pi_V = K g_V^2 { -M^2 B0 + [B00(M) - B00(sqrt(xi) M)] + B00(sqrt(xi) M) - A0(mH)/4 }
          = K g_V^2 { -M_V^2 B0(q^2;mH,M_V) + B00(q^2;mH,M_V) - A0(mH)/4 },   g_V^2 = g^2 (W), g^2/c^2 (Z).
The two B00(q^2;mH,sqrt(xi)M) cancel identically (same q^2, same masses): this equals the unitary-gauge expression.
No xi-dependence survives in the g^{mu nu} part. The xi dependence lives only in the q^mu q^nu / V-phi mixing parts.

## 4. Observable (SPEC section 3)
Bare: M_W0^2 = g0^2 v0^2/4, M_Z0^2 = (g0^2+g0'^2)v0^2/4, c0^2 = M_W0^2/M_Z0^2, e = g0 s0 (no Higgs in photon sector).
Pole masses: M_V^2 = M_V0^2 + Pi_VV(M_V^2) (transverse part: the inverse transverse propagator is q^2-M0^2-Pi(q^2), the q^mu q^nu term
only enters the longitudinal part; the V-phi mixing is longitudinal q^mu and decouples from the transverse part.
So the pole needs only the g^{mu nu} coefficient, at first order evaluated at q^2=M^2 of the tree mass.)
Hence s0^2 = s^2 + c^2 [Pi_W(M_W^2)/M_W^2 - Pi_Z(M_Z^2)/M_Z^2].
Muon decay: the 4-fermion amplitude is W exchange with massless conserved currents, so the q^mu q^nu and phi pieces drop:
G_F/sqrt2 = g0^2/(8 (M_W0^2 + Pi_W(0))) = e^2 / (8 s0^2 (M_W^2 + Pi_W(0) - Pi_W(M_W^2))).
pi alpha/(sqrt2 G_F) = s0^2 (M_W^2 + Pi_W(0) - Pi_W(M_W^2)) = M_W^2 s^2 (1 - Delta r)  (SPEC definition), to first order:
  Delta r_H = [Pi_W(M_W^2) - Pi_W(0)]/M_W^2 - (c^2/s^2) [Pi_W(M_W^2)/M_W^2 - Pi_Z(M_Z^2)/M_Z^2].
Tadpoles: Pi_V -> Pi_V + M_V^2 tau (same tau) cancels in both brackets. Sign check: large-m_H limit below gives +11 alpha/(48 pi s^2) (M_W falls with m_H).
Above threshold (e.g. xi=0, m_H < M_V) the Goldstone loop has an imaginary part (gauge artefact threshold); the real part is used. It cancels anyway.

## 5. Large m_H, log coefficient
Coefficient of L=ln m_H^2 (m_H^2 terms and O(1) after cancellation): B0 -> -1, B00(q^2;mH,m) -> -(1/2)(mH^2/2 + m^2/2 - q^2/6), A0 -> -mH^2.
Pi_V -> K g_V^2 L (3 M_V^2/4 + q^2/12) (xi cancels diagram by diagram combos: HV gives M^2(1-(1-xi)/4), H-phi gives -mH^2/4 - xi M^2/4 + q^2/12, seagull mH^2/4).
Delta r: [Pi_W(M^2)-Pi_W(0)]/M^2 -> K g^2 L/12 ; -(c^2/s^2)[...] -> K g^2 L (5/6): B = K g^2 (11/12) = 11 alpha/(48 pi s^2), g^2 = 4 pi alpha/s^2. 
mu-dependence: coefficient of ln mu^2 in Pi_V is -K g_V^2 (3M^2/4 + q^2/12): independent of m_H, linear in q^2 -> Delta r_H(mH)-Delta r_H(MW) mu-independent.

## 6. Numerics and independent checks
B0, B00 via exact closed forms of the Feynman-parameter integrals (real parts, ln|D|; roots of D_x factorised; q^2=0 linear case separately),
mpmath with dps adaptive (>= 80, more for large mass ratio since m_H^2 terms cancel). Pole cancellations are exact (Delta dropped, MS-bar).
Second route (in __main__): (i) direct mp.quad of the Feynman integrals vs closed forms; (ii) PV reduction B00 = [A0(m2)+2 m1^2 B0 + (q^2+m1^2-m2^2)B1]/(2(d-1)) with the eps-pole rational term;
(iii) unitary-gauge sum vs the diagram-by-diagram xi sum; (iv) slope of Delta r vs 11 alpha/(48 pi s^2). Not derived: the q^mu q^nu parts and V-phi mixing (not exported, argued irrelevant for transverse pole and massless-fermion currents).
