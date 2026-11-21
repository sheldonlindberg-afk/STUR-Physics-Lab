# DERIVATION: fermion-loop transverse self-energies of gamma, Z, W ('t Hooft-Feynman gauge)

Everything below follows from SPEC.md sections 1-2. Units hbar = c = 1, metric (+,-,-,-).

## 1. Couplings from the Lagrangian (SPEC 1)

L_f = psibar i gamma^mu D_mu psi, D_mu = d_mu - i g W^a_mu T^a - i g' Y B_mu, so

    L_int = psibar gamma^mu ( g W^a_mu T^a + g' Y B_mu ) psi      (Y acts on each chirality).

**Neutral.** Invert Z = c W3 - s B, A = s W3 + c B:  W3 = c Z + s A, B = -s Z + c A. Then

    g T3 W3 + g' Y B = A (g s T3 + g' c Y) + Z (g c T3 - g' s Y).

With c = g/sqrt(g^2+g'^2), s = g'/sqrt(g^2+g'^2): g s = g' c = e, and
g c T3 - g' s Y = (g^2 T3 - g'^2 Y)/sqrt(g^2+g'^2) = (e/(s c)) (c^2 T3 - s^2 Y) = (e/(s c)) (T3 - s^2 Q),
using Q = T3 + Y. On a left-handed doublet component T3 = I3; on the right-handed singlet T3 = 0, Y = Q. Hence

    L_int = e Q psibar gamma^mu psi A_mu + e psibar gamma^mu (gL P_L + gR P_R) psi Z_mu,
    photon:  gL = gR = Q
    Z:       gL = (I3 - s^2 Q)/(s c),   gR = -s Q/c.

A neutrino (Q = 0, I3 = 1/2, m = 0) automatically has gR = 0, i.e. no right-handed coupling, as SPEC requires.
Vertex Feynman rule (i x coefficient): i e gamma^mu (gL P_L + gR P_R).

**Charged.** W^1 = (W^+ + W^-)/sqrt2, W^2 = i (W^+ - W^-)/sqrt2, so
W^1 T^1 + W^2 T^2 = (W^+ T^+ + W^- T^-)/sqrt2, T^+ = T^1 + i T^2 (raises d -> u, matrix element 1).
L_int contains (g/sqrt2) ubar gamma^mu P_L d W^+_mu V_ud + h.c.; g = e/s. So the W vertex is
i e gamma^mu (gL P_L), gL = V/(sqrt2 s), gR = 0; the loop carries |V|^2 and N_C, collected in w = N_C |V|^2.

The 't Hooft-Feynman gauge plays no role in the fermion loop itself (no gauge propagator inside it).

## 2. Definition of Sigma_T and its sign (SPEC 2)

Let i Pi^{mu nu}(k) be the sum of amputated 1PI diagrams, Pi^{mu nu} = g^{mu nu} Pi_T + k^mu k^nu (...).
Dyson series with D0 = -i g/(k^2 - M^2): D0 (i Pi) D0 = -i g Pi_T/(k^2-M^2)^2, so
D = -i g / (k^2 - M^2 - Pi_T). SPEC writes the dressed propagator as -i g/(k^2 - M^2 + Sigma_T), hence

    Sigma_T = - Pi_T .

(For A-Z the same identification holds entry-by-entry for the mixing matrix.)

## 3. The generic fermion bubble

Vertex mu: i e gamma^mu (aL P_L + aR P_R); vertex nu: i e gamma^nu (bL P_L + bR P_R); internal masses m1 (momentum q),
m2 (momentum q+k). With the fermion-loop sign (-1) and colour factor N_C:

    i Pi^{mu nu} = - N_C e^2 mu^{2eps} Int d^dq/(2pi)^d  Tr[gamma^mu (aL PL + aR PR)(qslash + m1) gamma^nu (bL PL + bR PR)(q'slash + m2)] / (D1 D2),
    D1 = q^2 - m1^2, D2 = (q+k)^2 - m2^2, q' = q + k   (the four factors of i multiply to 1).

**Trace.** Move projectors through: P_L qslash = qslash P_R. Odd numbers of gammas vanish. Terms:

* qslash q'slash: Tr[gamma^mu qslash gamma^nu q'slash (aL bL P_R + aR bR P_L)]
  = (G+/2) 4 (q^mu q'^nu + q^nu q'^mu - g^{mu nu} q.q') + (gamma5 part ~ eps^{mu nu rho sigma} q_rho k_sigma),
* m1 m2: m1 m2 Tr[gamma^mu gamma^nu (aL bR P_R + aR bL P_L)] = 2 G- m1 m2 g^{mu nu},

with  **G+ = aL bL + aR bR,  G- = aL bR + aR bL.**  The gamma5 (epsilon-tensor) part integrates to
eps^{mu nu rho sigma} k_rho k_sigma = 0, so it never reaches the transverse part. Treatment of gamma5: anticommuting
gamma5 (NDR); in a two-point function no trace with gamma5 survives, so the transverse part is unambiguous
(SPEC 2). Tr 1 = 4 is kept in d dimensions (only the g-contraction identities are d-dependent, below).

**Tensor reduction (Passarino-Veltman).** With (16 pi^2/i) mu^{2eps} Int d^dq/(2pi)^d {1, q^mu, q^mu q^nu}/(D1 D2)
= {B0, k^mu B1, g^{mu nu} B00 + k^mu k^nu B11} and A0(m) = (16 pi^2/i) mu^{2eps} Int 1/(q^2 - m^2):

* q^2 = D1 + m1^2;  q.k = (D2 - D1 + f)/2, f = m2^2 - m1^2 - k^2.
* Int (q^2 + q.k)/(D1 D2) = [A0(m1) + A0(m2)]/2 + (m1^2 + m2^2 - k^2) B0/2.
* k^2 B1 = [A0(m1) - A0(m2) + f B0]/2.
* B00 + k^2 B11 = [A0(m2) + f B1]/2 (from k_mu contraction; Int q_nu/D1 = 0, Int q_nu/D2 = -k_nu A0(m2)).
* d B00 + k^2 B11 = A0(m2) + m1^2 B0 (from g_mu nu contraction).
* => (d - 1) B00 = A0(m2)/2 + m1^2 B0 - f B1/2.

d - 1 = 3 - 2 eps, 1/(3-2eps) = (1 + 2eps/3)/3. The UV pole of the bracket is
Delta [m2^2/2 + m1^2 + f/4] = Delta (3 m1^2 + 3 m2^2 - k^2)/4 (A0 -> m^2 Delta, B0 -> Delta, B1 -> -Delta/2), so the
**O(eps) part of the d-dependent coefficient times the pole** leaves the finite piece (2/9)(3m1^2+3m2^2-k^2)/4:

    B00 = (1/6) [ A0(m2) + 2 m1^2 B0 + (k^2 + m1^2 - m2^2) B1 + m1^2 + m2^2 - k^2/3 ].

The g^{mu nu} coefficient of the numerator is 2G+ (2 B00 - Int(q^2+q.k)) + 2 G- m1 m2 B0, therefore

    Sigma_T(k^2) = N_C (alpha/4pi) { G+ [ 4 B00 - A0(m1) - A0(m2) - (m1^2 + m2^2 - k^2) B0 ] + 2 G- m1 m2 B0 }.   (*)

**MS-bar scalar integrals** (Delta = 1/eps - gamma_E + ln 4pi dropped, mu^{2eps} on the measure):

    A0(m)          = m^2 (1 - ln(m^2/mu^2))                 (A0(0) = 0)
    B0(k^2,m1,m2)  = - Int_0^1 dx ln[ Delta(x)/mu^2 - i0 ],   Delta(x) = (1-x) m1^2 + x m2^2 - x(1-x) k^2
    B1(k^2,m1,m2)  = + Int_0^1 dx x ln[ Delta(x)/mu^2 - i0 ]   (Feynman parameter x on D2, q = l - x k)

These come from Feynman parametrisation; B1 written this way needs no division by k^2, so k^2 = 0 is regular.
The real part (SPEC 2, above threshold) is obtained by replacing ln(Delta - i0) by ln|Delta|.

### Equal masses (gamma, Z): m1 = m2 = m
f = -k^2, B1 = -B0/2, A0 = m^2 (B0(0,m,m) + 1). Then
4 B00 - 2 A0 - (2m^2 - k^2) B0 = (2/3)[ (k^2 - m^2) B0(k^2) - 2 m^2 B0(0) - k^2/3 ], so

    Sigma_T = N_C (alpha/4pi) { (2/3) G+ [ (k^2 - m^2) B0 - 2 m^2 B0(0) - k^2/3 ] + 2 G- m^2 B0 }.

* **AA**: G+ = G- = 2Q^2:  Sigma^AA = (alpha/3pi) N_C Q^2 [ (k^2 + 2m^2) B0(k^2,m,m) - 2 m^2 B0(0,m,m) - k^2/3 ].
* **AZ**: a = (Q, Q), b = (gL, gR): G+ = G- = Q (gL + gR) = Q (I3 - 2 s^2 Q)/(s c):
  Sigma^AZ = (alpha/6pi) N_C Q (gL+gR) [ (k^2 + 2m^2) B0 - 2 m^2 B0(0) - k^2/3 ].
* **ZZ**: G+ = gL^2 + gR^2, G- = 2 gL gR:
  Sigma^ZZ = (alpha/6pi) N_C (gL^2+gR^2) [ (k^2+2m^2) B0 - 2m^2 B0(0) - k^2/3 ] - (alpha/2pi) N_C (gL-gR)^2 m^2 B0,
  with (gL - gR)^2 = I3^2/(s^2 c^2) = 1/(4 s^2 c^2).
* **W**: G+ = 1/(2 s^2) (times w), G- = 0, masses (m_up, m_down):
  Sigma^W = w (alpha/4pi) (1/(2 s^2)) [ 4 B00 - A0(mu) - A0(md) - (mu^2 + md^2 - k^2) B0(k^2, mu, md) ].

Inputs: e^2 = 4 pi alpha, c = MW/MZ, s^2 = 1 - c^2 (SPEC 1).

**Sign of Sigma^AZ.** It follows from SPEC's rotation A = s W3 + c B, Z = c W3 - s B together with D = d - i g W T - i g' Y B,
which give the photon and Z vertices the same overall sign (+ i e). A different field-sign convention (e.g. A -> -A)
would flip Sigma^AZ; SPEC fixes it, so no freedom remains.

## 4. Photon Ward identity
At k^2 = 0 with m1 = m2: (k^2 + 2m^2) B0(0) - 2 m^2 B0(0) = 0 identically, so Sigma^AA(0) = Sigma^AZ(0) = 0.
In the Feynman-parameter form (section 6) the same statement is G+(-m^2) + G- m^2 = 0 because G+ = G- whenever one
vertex is the vector photon. This holds per fermion, for any m (and Z-Z / W do not vanish: G+ != G-).

## 5. Numerics (SPEC 4)

* The finite parts reduce to the moments I_n = Int_0^1 x^n ln|Delta(x)/mu^2| dx, n = 0, 1, evaluated in closed form:
  Delta(x) = k^2 x^2 + (m2^2 - m1^2 - k^2) x + m1^2.
  - k^2 != 0: ln|Delta| = ln|k^2| + ln|x - x1| + ln|x - x2| for real roots, or ln|k^2| + 2 Re ln(x - a) for complex
    conjugate roots a, a*. Antiderivatives: Int ln(x-a) = (x-a) ln(x-a) - x, Int x ln(x-a) = (x^2 - a^2)/2 ln(x-a) - x^2/4 - a x/2
    (real a: ln|x-a| with 0 ln 0 = 0; complex a: principal log, continuous on the real segment because Im(x-a) is constant).
    Roots inside (0,1) are exactly the thresholds k^2 > (m1+m2)^2: the log singularity is integrable and the absolute value gives the real part.
  - k^2 = 0: Delta linear (ln|m2^2-m1^2| + ln|x - a|) or constant (m1 = m2: ln m^2). Both masses 0 and k^2 = 0:
    the integrals are scaleless but every one of them is multiplied by m^2 or k^2 = 0 in (*), so the contribution is 0
    (the k^2 -> 0 limit of k^2 ln(-k^2) is 0, consistent).
  - Very different masses (m_t against 0): one root at x = 0 or 1; handled by the same formulas.
  - All of this is evaluated in mpmath with 50 digits inside `mp.workdps` (local, the global precision is not changed),
    so cancellations at tiny k^2 (k^2 = 1e-12 against m_e^2) and between the two B0's in the Ward identity are harmless.
* UV pole coefficient (= coefficient of ln mu^2, since every Delta comes with -ln(.../mu^2)): in (*) set
  A0 -> m^2, B0 -> 1, B1 -> -1/2, B00 -> (3m1^2 + 3m2^2 - k^2)/12:
  4 B00 - A0(m1) - A0(m2) - (m1^2+m2^2-k^2) B0 -> (m1^2+m2^2 - k^2/3) - (m1^2+m2^2) - (m1^2+m2^2) + k^2 = 2k^2/3 - (m1^2+m2^2),
  so  dSigma_T/d ln mu^2 = N_C (alpha/4pi) [ G+ (2k^2/3 - m1^2 - m2^2) + 2 G- m1 m2 ]   (linear in k^2).
  The same follows from route 2: Int_0^1 {G+[2x(1-x)k^2 - (1-x)m1^2 - x m2^2] + G- m1 m2} dx times N_C alpha/(2pi).

## 6. Independent second route: direct Feynman-parameter integral

Combine D1, D2 with parameter x (on D2), shift q = l - x k, q' = l + (1-x) k. Denominator (l^2 - Delta(x))^2.
The g^{mu nu} part of the numerator: 2G+ [ (2/d - 1) l^2 + x(1-x) k^2 ] + 2 G- m1 m2. Using
mu^{2eps} Int d^dl/(2pi)^d 1/(l^2-Delta)^2 = (i/16pi^2)(Delta_eps - ln(Delta/mu^2)) and
(2/d - 1) Int l^2/(l^2-Delta)^2 = -(i/(4pi)^{d/2}) Gamma(2 - d/2) Delta^{d/2-1} -> -(i/16pi^2) Delta (Delta_eps - ln(Delta/mu^2))
(note: no extra rational term here; in route 1 it appears instead through B00), one gets after MS-bar

    Sigma_T = N_C (alpha/2pi) Int_0^1 dx [ - ln|Delta(x)/mu^2| ] { G+ [ 2x(1-x) k^2 - (1-x) m1^2 - x m2^2 ] + G- m1 m2 }.

This is evaluated by adaptive numerical quadrature (mpmath.quad, split at the real roots of Delta in (0,1)), entirely
independent of the PV reduction, the B00 O(eps) term and the closed-form log moments. Agreement of the two routes
checks the trace, the d-dimensional B00 term and the moments.

Checks printed by `python3 ferm_se.py`:
1. route 1 vs route 2 for AA, AZ, ZZ, W at spacelike, timelike-below and above-threshold k^2;
2. Ward identity Sigma^AA(0) = Sigma^AZ(0) = 0;
3. mu dependence vs the pole coefficient of section 5 (numerical d/d ln mu^2);
4. heavy-fermion limit: Sigma^AA(k^2) -> (alpha/3pi) N_C Q^2 k^2 (-ln(m^2/mu^2)) for m^2 >> |k^2|
   (expanding B0(k^2) = B0(0) + k^2/(6m^2) + ...: (k^2+2m^2)B0 - 2m^2 B0(0) - k^2/3 = k^2 B0(0) + O(k^4/m^2));
5. massless photon check: Sigma^AA = (alpha/3pi) N_C Q^2 k^2 (5/3 - ln(-k^2/mu^2)) for m = 0;
6. Sigma^W symmetric under m_up <-> m_down.

## Not derived / open
Nothing needed for the exports was left underived. The overall sign of Sigma^AZ is fixed by SPEC's field conventions (section 3).
