# DERIVATION: Higgs part of Sirlin's Delta r at one loop (Feynman gauge, MS-bar self-energies)

Build higgs_dr-a. All statements below are derived here from SPEC.md; no literature values are used.

## 0. Postulates used (SPEC section 1)

Phi = (phi+, (v + H + i chi)/sqrt2), D = d - i g W^a tau^a/2 - i g' B/2, V = -mu^2 Phi^+Phi + lambda (Phi^+Phi)^2.
W^pm = (W1 -/+ i W2)/sqrt2, Z = c W3 - s B, A = s W3 + c B, g' = g s/c, e = g s.

Write T = g W^a tau^a/2 + g' B/2. Using W3 = cZ + sA, B = -sZ + cA:

    T = 1/2 [[ (g/c)(c^2 - s^2) Z + 2 e A ,  sqrt2 g W+ ],
             [ sqrt2 g W- ,                  -(g/c) Z    ]]

Lower component of D Phi with phi0 = (v + H + i chi)/sqrt2:

    (D Phi)_2 = d phi0 - i (g/sqrt2) W- phi+ + i (g/2c) Z phi0 .

Upper component: d phi+ - (i/2)[(g/c)(c^2-s^2)Z + 2eA] phi+ - i (g/sqrt2) W+ phi0.

### Masses
* |(g/sqrt2) W+ v/sqrt2|^2 = (g^2 v^2/4) W+W-  =>  M_W^2 = g^2 v^2/4, M_W = g v/2.
* |(g/2c) Z v/sqrt2|^2 = (g^2 v^2/(8c^2)) Z^2 = (1/2) M_Z^2 Z^2  =>  M_Z^2 = g^2 v^2/(4 c^2), so M_W = c M_Z.
* Potential: minimum v^2 = mu^2/lambda; m_H^2 = 2 lambda v^2 (free input). In the Feynman gauge (xi = 1) the Goldstones
  phi^pm, chi have masses M_W, M_Z (SPEC) and the gauge propagators are -i g^{mu nu}/(k^2 - M_V^2).

### Higgs couplings (read off |D Phi|^2)
From (g^2/2) W+W- |phi0|^2 and (g^2/(4c^2)) Z^2 |phi0|^2, with |phi0|^2 = ((v+H)^2 + chi^2)/2:

| Lagrangian term | Feynman rule |
|---|---|
| g M_W H W+_mu W-^mu | i g M_W g^{mu nu} |
| (g^2/4) H^2 W+W- | i g^2/2 g^{mu nu} |
| (g M_Z/(2c)) H Z^2 | i (g M_Z/c) g^{mu nu} |
| (g^2/(8c^2)) H^2 Z^2 | i g^2/(2c^2) g^{mu nu} |
| (g/2c) Z^mu (H d_mu chi - chi d_mu H) | (g/2c)(p_chi - p_H)^mu (all momenta incoming) |
| i(g/2) W+^mu (phi- d_mu H - H d_mu phi-) + h.c. | +- i(g/2)(p_H - p_phi)^mu |

(The Z-H-chi term comes from i a Z (phi0 d phi0* - phi0* d phi0) = a Z (h d chi - chi d h), a = g/2c, h = v + H;
the W-H-phi term from the cross terms of d phi0, d phi+ with the W pieces.)  There is no H-photon, H-Z-W or
H-photon-Z coupling, so the photon self-energy and gamma-Z mixing have no Higgs-containing diagram (consistent with SPEC 3).

## 1. Integrals (SPEC section 2)

d = 4 - 2 eps, mu^{2eps} on the measure. Definitions (exact in d, then MS-bar: drop Delta = 1/eps - gamma_E + ln 4pi):

    int d^dk/(2pi)^d 1/(k^2 - m^2)                          = (i/16pi^2) A0(m),
    int d^dk/(2pi)^d 1/((k^2-m1^2)((k-q)^2-m2^2))           = (i/16pi^2) B0(q^2; m1, m2),
    int d^dk/(2pi)^d k^mu k^nu/(...) |_{g part}, after shift = (i/16pi^2) g^{mu nu} B00 .

Feynman parameter x, k = l + x q, X(x) = (1-x) m1^2 + x m2^2 - x(1-x) q^2:

    A0(m)   = m^2 (Delta + 1 - ln(m^2/mu^2))                         -> m^2 (1 - ln(m^2/mu^2))
    B0      = Delta - int_0^1 dx ln(X/mu^2)                          -> - int_0^1 ln(X/mu^2)
    B00     = (1/2) int_0^1 dx X (Delta + 1 - ln(X/mu^2))            -> (1/2) int_0^1 X (1 - ln(X/mu^2))

The B00 line uses int l^mu l^nu/(l^2-X)^2 = (g^{mu nu}/d) int l^2/(l^2-X)^2 = (-i/(4pi)^{d/2}) (g/2) Gamma(-1+eps) X^{1-eps}:
the exact d-dimensional 1/d is kept, and Gamma(-1+eps) = -(1/eps + 1 - gamma_E + O(eps)); the "+1" is the O(eps) of 1/d (and of Gamma)
against the pole, as SPEC demands. (Check: the PV reduction B00 = [A0(m2) + 2 m1^2 B0 + (q^2+m1^2-m2^2) B1 + m1^2 + m2^2 - q^2/3]/6
gives the same function; verified numerically, route 2 below.)

For q^2 < (m1+m2)^2, X(x) > 0 on [0,1] (its minimum over x is positive exactly below threshold), so all integrals are real and smooth.

## 2. The Higgs-containing self-energies

Convention (SPEC): amputated 1PI = i Pi g^{mu nu} + ..., effective mass^2 = M^2 + Pi (D = D0 + D0 (i Pi) D0 = -i/(q^2 - M^2 - Pi)).

(a) Seagull with an H loop, vertex i C g^{mu nu}, symmetry factor 1/2:
    i Pi = (1/2)(i C) int i/(k^2-m_H^2) = (1/2)(iC)(-A0/16pi^2)  =>  Pi = -C A0(m_H)/(32 pi^2).
    Equivalently: the effective mass term from (g^2/4) <H^2> W+W-, <H^2> = -A0/16pi^2.
    W: C = g^2/2  ->  -g^2 A0/(64 pi^2).   Z: C = g^2/(2c^2)  ->  -g^2 A0/(64 pi^2 c^2).

(b) H + V loop: (i g M_W)^2 (i)(-i) int 1/(D_H D_W) = -g^2 M_W^2 (i/16pi^2) B0
    =>  Pi_W = -g^2 M_W^2 B0(q^2; m_H, M_W)/16pi^2,   Pi_Z = -(g^2 M_Z^2/c^2) B0(q^2; m_H, M_Z)/16pi^2. No symmetry factor (distinct lines).

(c) H + Goldstone loop, vertex kappa (p_B - p_A): with H momentum k and Goldstone q-k, the vertices are kappa(2k-q)^mu and kappa(q-2k)^nu,
    the propagators give i*i = -1, so the integrand is kappa^2 (2k-q)^mu (2k-q)^nu/(D_H D_G); the g part is 4 kappa^2 (i/16pi^2) B00
    =>  Pi = 4 kappa^2 B00/16pi^2. W: kappa^2 = (g/2)^2 (the two vertex prefactors i g/2 and -i g/2 multiply to g^2/4);  Z: kappa = g/2c.

Total (m1 = m_H, m2 = M_V in X):

    Pi_W(q^2) = (g^2/16pi^2)      h(q^2; m_H, M_W),
    Pi_Z(q^2) = (g^2/(16pi^2 c^2)) h(q^2; m_H, M_Z),
    h(q^2; m, M) = -A0(m)/4 - M^2 B0(q^2; m, M) + B00(q^2; m, M),

with g^2 = e^2/s^2 = 4 pi alpha/s^2, s^2 = 1 - M_W^2/M_Z^2. Since g^2/(c^2 M_Z^2) = g^2/M_W^2,

    Pi_V(q^2)/M_V^2 = (K/M_W^2) h(q^2; m_H, M_V),    K = g^2/16pi^2 = alpha/(4 pi s^2).

### mu dependence (UV pole structure)
d/d ln mu^2: A0 -> m^2, B0 -> 1, B00 -> (1/2) int X = (m^2 + M^2)/4 - q^2/12. Hence

    dh/d ln mu^2 = -m^2/4 - M^2 + (m^2+M^2)/4 - q^2/12 = -(3/4) M^2 - q^2/12 ,

linear in q^2 (the blind check) and independent of m_H: the 1/eps poles (same coefficient) and the ln mu^2 terms cancel in
any difference at fixed M_V, q^2 between two Higgs masses.

### Tadpoles
A Higgs tadpole <H> = t enters through the H V V vertices: Pi_W = g M_W t, Pi_Z = (g M_Z/c) t, so Pi_W/M_W^2 = Pi_Z/M_Z^2 = g t/M_W:
the same q^2-independent shift of both ratios (it is the shift delta v/v of the common vev). It drops out of Delta r below, because
Delta r contains only Pi_W(M_W^2) - Pi_W(0) and Pi_Z(M_Z^2)/M_Z^2 - Pi_W(M_W^2)/M_W^2. Dropping the tadpoles is therefore exact for Delta r.

## 3. Delta r_H (SPEC section 3)

Bare quantities (index 0): G_F/sqrt2 = g_0^2/(8 (M_W0^2 + Pi_W(0))), g_0^2 = e^2/s_0^2 (e has no Higgs correction),
s_0^2 = 1 - M_W0^2/M_Z0^2. Pole masses: M_V^2 = M_V0^2 + Pi_V(M_V^2), so M_V0^2 = M_V^2 - Pi_V(M_V^2). Then, to first order,

    c_0^2 = c^2 [1 - Pi_W(M_W^2)/M_W^2 + Pi_Z(M_Z^2)/M_Z^2],
    s_0^2 = s^2 + c^2 [Pi_W(M_W^2)/M_W^2 - Pi_Z(M_Z^2)/M_Z^2],
    M_W0^2 + Pi_W(0) = M_W^2 [1 + (Pi_W(0) - Pi_W(M_W^2))/M_W^2],

    G_F/sqrt2 = (pi alpha/(2 s^2 M_W^2)) [1 - (c^2/s^2)(Pi_W(M_W^2)/M_W^2 - Pi_Z(M_Z^2)/M_Z^2) - (Pi_W(0) - Pi_W(M_W^2))/M_W^2].

Comparing with G_F/sqrt2 = pi alpha/(2 s^2 M_W^2 (1 - Delta r)) ~ (pi alpha/(2 s^2 M_W^2))(1 + Delta r):

    Delta r_H = [Pi_W(M_W^2) - Pi_W(0)]/M_W^2 + (c^2/s^2) [Pi_Z(M_Z^2)/M_Z^2 - Pi_W(M_W^2)/M_W^2]

    = (K/M_W^2) { h(M_W^2; m_H, M_W) - h(0; m_H, M_W) + (c^2/s^2)[h(M_Z^2; m_H, M_Z) - h(M_W^2; m_H, M_W)] }.

(At q^2 -> 0 the second bracket is -(c^2/s^2) Delta rho with Delta rho = Pi_W(0)/M_W^2 - Pi_Z(0)/M_Z^2, the familiar structure.)
The export is Delta r_H(m_H) - Delta r_H(M_W) at the same mu: by section 2 it is mu-independent, proportional to alpha at fixed masses,
and exactly zero at m_H = M_W.

## 4. Large-m_H expansion and the log coefficient B

With L = ln(m^2/mu^2), m >> M, q (X = (1-x) m^2 + delta, delta = x M^2 - x(1-x) q^2; corrections O(M^4/m^2 ln)):

    A0 = m^2 (1 - L),  B0 = 1 - L + O(M^2/m^2 ln),
    int X ln X = m^2 (L/2 - 1/4) + (M^2/2 - q^2/6)(L + 1) - 3M^2/4 + 5 q^2/36
      [using int (1-x) ln(1-x) = -1/4, int x ln(1-x) = -3/4, int x(1-x) ln(1-x) = -5/36],
    B00 = 3m^2/8 - m^2 L/4 - (M^2/4 - q^2/12) L + 3M^2/8 - 5q^2/72,

    h(q^2; m, M) = m^2/8 + (3M^2/4 + q^2/12) L - 5M^2/8 - 5q^2/72 + O(M^4/m^2 ln m).

The m^2/8 term is common to W and Z ratios (like a tadpole) and cancels in Delta r. Coefficient of ln m^2 in h: lambda(q^2, M) = 3M^2/4 + q^2/12
(= -dh/d ln mu^2, as it must, since at large m the mu dependence only enters through L). Then

    B = (K/M_W^2) { lambda(M_W^2,M_W) - lambda(0,M_W) + (c^2/s^2)[lambda(M_Z^2,M_Z) - lambda(M_W^2,M_W)] }
      = K { 1/12 + (c^2/s^2)(5/6)(1/c^2 - 1) } = K (1/12 + 5/6) = (11/12) K = 11 alpha/(48 pi s^2).

Constant terms: -5/72 + (c^2/s^2)(-25/36)(s^2/c^2) = -55/72 = (11/12)(-5/6), so at large m_H

    Delta r_H(m_H) = (11/12) K [ln(m_H^2/mu^2) - 5/6] + (m_H-independent) + O(M^2/m_H^2 ln m_H).

B > 0: the M_W prediction decreases (Delta r increases) as m_H grows.

## 5. Numerics (SPEC section 5)

* Main route: Feynman-parameter integrals int_0^1 ln X and int_0^1 X ln X by mpmath tanh-sinh quadrature at 40 digits, the interval
  split at x_c = m1^2/(m1^2 + m2^2) (where the m_H and M_V terms of X cross; essential for m_H >> M_V). Poles were removed analytically
  (MS-bar); ln mu^2 enters only through the explicit factors above. Thresholds: q^2 >= (m1+m2)^2 raises ValueError (not needed; SPEC 2).
  The 40-digit arithmetic is needed in Delta r because the m_H^2/8 pieces of Pi_W/M_W^2 and Pi_Z/M_Z^2 cancel (relative 1e-12 at
  m_H ~ 1e6 M_W). Accuracy of every export: ~1e-30 relative before the final float conversion (i.e. double precision).
* log_coefficient: the closed form of section 4, assembled in code from lambda(q^2, M).
* Route 2 (independent, in `__main__`): (i) closed-form B0 (log/arctan form, double precision) and the PV reduction formula for B00,
  compared with the quadrature self-energies; (ii) the asymptotic formula of section 4 compared with the numerical Delta r at large m_H,
  including the -5/6 constant; (iii) mu-independence and q^2 -> 0 smoothness.

### Route-2 results (run `python3 higgs_dr.py`)
* Quadrature Pi_W, Pi_Z agree with the PV-reduction route (double-precision Gauss-Legendre B0 + PV B00) to ~1e-12 relative.
* log_coefficient = 2.555165e-3 at the campaign inputs, equal to (11/12) alpha/(4 pi s^2); numerical slope / B = 0.990, 0.99978,
  0.9999967 at m_H = 1e3, 1e4, 1e5 GeV; Delta r_H - (11/12)K[ln(m_H^2/mu^2) - 5/6] -> 1.2e-4, 2.6e-6, 4.0e-8 (confirms the -5/6 constant
  and the absence of any other m_H-independent piece at mu = M_W in this subset).
* delta_r_higgs_rel identical at mu = M_W and 5 M_W to 12 digits; Pi(1e-6) - Pi(0) ~ 4e-12 relative.
* Gate (builder mode): all tiers pass.

## 6. Not derived / open
Nothing left open. Scheme remark: the result is the Feynman-gauge Higgs-containing subset, as SPEC prescribes; its m_H dependence
(the difference) is what the reference subtraction isolates.
