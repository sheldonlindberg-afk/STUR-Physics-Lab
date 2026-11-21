# DERIVATION: m_H dependence of Delta r at one loop (Feynman gauge, MS-bar)

## 1. Couplings (SPEC s1)
|DPhi|^2 with Phi=(phi+,(v+H+i phi0)/sqrt2): M_W^2=g^2v^2/4, M_Z^2=g^2v^2/(4c^2) (M_W=cM_Z), and
L ∋ g M_W H W+W-  + (g^2/4)H^2 W+W-  + (g/(2c)) M_Z... : precisely
 HWW vertex  i g M_W g^{mu nu};  HZZ vertex i (g/c) M_Z g^{mu nu};
 HHWW seagull i g^2/2 g^{mu nu};  HHZZ seagull i g^2/(2c^2) g^{mu nu};
 W+ phi- H and Z phi0 H: (g/2)(p_H-p_phi)^mu and (g/(2c))(p_H-p_phi)^mu.
Feynman gauge: phi± mass M_W, phi0 mass M_Z; propagators -i g/(k^2-M^2), i/(k^2-m^2).
Convention: a 1PI insertion i Pi g^{mu nu} gives propagator -i/(q^2-M^2-Pi), i.e. effective mass^2 M^2+Pi (SPEC s2).

## 2. Self-energies
Loop integrals (1/16pi^2 factored): int d^dk/(2pi)^d 1/(k^2-m^2) = i A0/16pi^2, A0=m^2(Delta+1-ln m^2/mu^2);
int 1/(D1 D2) = i B0/16pi^2, B0 = Delta - int_0^1 dx ln(Delta_x/mu^2),
Delta_x = x m2^2+(1-x) m1^2 - x(1-x) q^2.
* V-H loop: i Pi = (i g_V M_V)^2 (-i)(i) int 1/(D D) -> Pi = -g_V^2 M_V^2 B0/16pi^2 (g_W^2 M_W^2 = g^2 M_W^2; g_Z^2M_Z^2 = g^2M_Z^2/c^2).
* phi-H loop: i Pi = (g_s)^2 int (2k-q)^mu(2k-q)^nu/(D1 D2) (sign fixed by scalar-QED transversality check: bubble+seagull
  cancel the quadratic term at q=0). Feynman parameters, k=l+xq, g^{mu nu} part 4 l^2/d; the dim-reg identity
  int l^2/(l^2-D)^2 = (d/2) int 1/(l^2-D) is exact, so 4/d*(d/2)=2 and the O(eps) of 1/d against the pole is
  already inside A0(D_x) (the "+1"): Pi = g_s^2/(16pi^2) * 2 int dx A0(Delta_x), g_s^2 = g^2/4 (W), g^2/(4c^2) (Z).
* Seagull: delta M^2 = (g^2/4)<H^2> (W), (g^2/(4c^2))<H^2> (Z), <H^2> = -A0(m_H)/16pi^2.
Result (g^2=4 pi alpha/s^2, s^2=1-M_W^2/M_Z^2):
 Pi_W(q^2) = g^2/16pi^2 [ -M_W^2 B0(q^2;m_H,M_W) + 1/2 int dx Delta_x(Delta+1-ln Delta_x/mu^2) - A0(m_H)/4 ]
 Pi_Z(q^2) = g^2/(16pi^2 c^2) [ -M_Z^2 B0(q^2;m_H,M_Z) + 1/2 int dx Delta_x(...) - A0(m_H)/4 ]   (masses M_Z in Delta_x)
Pole (Delta) coefficient: -(3/4)M_V^2 - q^2/12 (times g^2/16pi^2, Z with 1/c^2): linear in q^2, so mu-dependence is
linear in q^2 (blind check). Below thresholds Delta_x>0 (at q^2<=M_V^2, Delta_x>=x^2M^2+(1-x)m_H^2).
Tadpoles: they come from the shift v->v+dv, so Pi^t_V = tau M_V^2, same tau for W and Z.

## 3. Delta r
Bare relation: G_F/sqrt2 = g0^2/(8 (M0_W^2+Pi_W(0))), pole mass M_W^2=M0_W^2+Pi_W(M_W^2) =>
 G_F/sqrt2 = g0^2/(8M_W^2) [1+(Pi_W(M_W^2)-Pi_W(0))/M_W^2]   (tadpole constant cancels in the difference).
e0=e (no Higgs in photon sector); g0^2 = e^2/s0^2, c0^2=M0_W^2/M0_Z^2 = c^2(1+delta),
 delta = Pi_Z(M_Z^2)/M_Z^2 - Pi_W(M_W^2)/M_W^2 (tadpoles cancel), s0^2 = s^2 - c^2 delta.
Then pi alpha/(sqrt2 G_F) = s0^2 M_W^2/[1+...], and with M_W^2 s^2 = that/(1-Delta r):
 Delta r_H = [Pi_W(M_W^2)-Pi_W(0)]/M_W^2 + (c^2/s^2)[Pi_Z(M_Z^2)/M_Z^2 - Pi_W(M_W^2)/M_W^2].
Reported: Delta r_H(m_H) - Delta r_H(M_W); Delta (pole) and mu cancel because the pole coefficient is m_H independent.

## 4. Large m_H and B
Writing L=ln(m_H^2/mu^2): the coefficient of L in Pi_V is the negative of the Delta coefficient (m_H^2 pieces cancel
between 1/2 int Delta and the seagull): Pi_W -> g^2/16pi^2 (3M_W^2/4+q^2/12) L, Pi_Z -> g^2/(16pi^2c^2)(3M_Z^2/4+q^2/12) L.
 Pi_W(M_W^2)-Pi_W(0) -> (g^2/16pi^2) M_W^2/12 L;  Pi_W(M_W^2)/M_W^2 -> (g^2/16pi^2)(5/6)L;  Pi_Z(M_Z^2)/M_Z^2 -> (g^2/16pi^2c^2)(5/6)L.
 Delta r -> (g^2/16pi^2)[1/12 + (c^2/s^2)(5/6)(1/c^2-1)] L = (g^2/16pi^2)(11/12) L
 B = 11 g^2/(192 pi^2) = 11 alpha/(48 pi s^2)   (the familiar (11/3)(alpha/16 pi s^2) form).
## 5. Independent checks
(a) B vs numerical slope of the full integrals at m_H ~ 1e5-1e6 M_W (gate); (b) q^2=0 integrals vs the closed form
B0(0)=(A0(m1)-A0(m2))/(m1^2-m2^2) and int Delta lnDelta closed form; (c) mu-independence; (d) alpha linearity.
Nothing here is un-derived. Note the integrals are evaluated in 30-digit mpmath because m_H^2-sized terms cancel.
