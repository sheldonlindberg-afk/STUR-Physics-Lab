# DERIVATION: O(alpha_s) correction to Delta rho of the (t, b) doublet

Status: v1. Sections 0-8 written before code; section 9 filled in from the computer-algebra run
(builds/a/qcd_drho.py, `python3 builds/a/qcd_drho.py` prints both routes).

## 0. Postulates used (SPEC refs)

* SPEC 1: doublet (t, b), SU(N) colour, C_F, Feynman gauge (I also keep a general covariant gauge
  parameter xi as a check), m_b = 0, left-handed currents J^a = qbar gamma_mu P_L tau^a/2 q, coupling g,
  M_W^2 = g^2 v^2/4, gaugeless limit (g, g' -> 0 at fixed v; hypercharge off so the Z couples as (g/c) J^3
  and M_Z^2 c^2 = M_W^2).
* SPEC 2: dressed propagator -i g/(q^2 - M^2 + Sigma_T), Delta rho = Sigma_Z(0)/M_Z^2 - Sigma_W(0)/M_W^2,
  dimensional regularization d = 4 - 2 eps, pole and MS-bar top mass.

## 1. Self-energy in terms of current correlators

Minkowski, mostly-minus metric. With L_int = g W^a_mu J^{a mu}, the second-order term of the effective
action is (1/2) W_mu W_nu g^2 Pi^{mu nu}(q), with the standard correlator

    Pi^{mu nu}_{ab}(q) = i \int d^4x e^{iqx} <T J^mu_a(x) J^nu_b(0)> = g^{mu nu} Pi_ab(q^2) + q^mu q^nu (...).

The free transverse quadratic Lagrangian is (1/2) W.W (M^2 - q^2), propagator -i g/(q^2 - M^2) (agrees with
SPEC). Adding g^2 Pi: (1/2) W.W (M^2 - q^2 + g^2 Pi), propagator -i g/(q^2 - M^2 - g^2 Pi). Hence in the SPEC
convention

    Sigma_W = - g^2 Pi_11,      Sigma_Z = -(g^2/c^2) Pi_33,

and, with M_Z^2 = M_W^2/c^2 and M_W^2 = g^2 v^2/4,

    Delta rho = -(g^2/M_W^2)[Pi_33(0) - Pi_11(0)] = (4/v^2) [Pi_11(0) - Pi_33(0)].        (1.1)

g drops out: this is the gaugeless limit; QCD corrections live entirely inside Pi_ab.

## 2. Flavour decomposition

Let Pi_X(m1, m2) be the q = 0 transverse correlator of the currents psibar_1 Gamma psi_2 and its hermitian
conjugate, X = V (Gamma = gamma^mu) or A (Gamma = gamma^mu gamma5), quark masses m1, m2.

* Left-handed: gamma P_L = (gamma - gamma gamma5)/2, so Pi_LL = (Pi_V + Pi_A - Pi_VA - Pi_AV)/4. The VA
  pieces need an epsilon tensor and vanish for the g^{mu nu} part at q = 0 (no vector available).
* With anticommuting gamma5 (consistent here: every trace has an even number of gamma5 on a single open
  fermion loop, no triangle subgraph appears at O(alpha_s)), the field redefinition psi_2 -> gamma5 psi_2
  maps gamma^mu -> gamma^mu gamma5 at both current vertices and m2 -> -m2 (including its counterterm, which
  is proportional to m2); the gluon vertex is invariant. Therefore, to all orders considered,

        Pi_A(m1, m2) = Pi_V(m1, -m2).                                                       (2.1)

* J^1 = (tbar G_L b + bbar G_L t)/2 gives Pi_11 = (1/4)(2 Pi_LL(t,b)) = Pi_LL(m,0)/2, and with m_b = 0,
  Pi_A(m,0) = Pi_V(m,0) by (2.1): Pi_11 = Pi_V(m,0)/4.
* J^3 = (tbar G_L t - bbar G_L b)/2 gives Pi_33 = (Pi_LL(t,t) + Pi_LL(b,b))/4 (t-b annihilation diagrams
  start at O(alpha_s^2): one gluon cannot connect two colour-singlet loops). Pi_LL(b,b)(0) is scaleless = 0.
  Pi_V(m,m)(0) = 0 by the vector Ward identity (conserved diagonal current, exact to all orders), so
  Pi_33 = Pi_A(m,m)/16.

    Delta rho = (1/v^2) [ Pi_V(m,0) - Pi_A(m,m)/4 ] = sqrt2 G_F [ Pi_V(m,0) - Pi_V(m,-m)/4 ].   (2.2)

## 3. Feynman rules, Wick rotation

Quark propagator i(pslash+m)/(p^2-m^2), gluon -i delta^{ab}[g_{ab} - (1-xi) q_a q_b/q^2]/q^2, vertex
-i g_s gamma^alpha T^a, closed loop (-1), colour trace Tr 1 = N_C, Tr T^aT^a = C_F N_C.
Rotating every loop momentum (d^dk = i d^dk_E, p^2 = -p_E^2) and keeping the Dirac algebra Minkowskian
(dot products p.p' -> -p_E.p'_E after the trace), I find

* one loop:  Pi^(1) = - N_C \int_k Tr[gamma^mu N_2(k) gamma_mu N_1(k)] / (d D_2(k) D_1(k)),
* two loops: Pi^(2) = + g_s^2 C_F N_C \int_k \int_l Tr[...]/(d ...)   (sum of three diagrams below),

with N_i(p) = pslash + m_i, D_i(p) = p_E^2 + m_i^2, Q = (k-l)_E^2, \int_k = \int d^dk_E/(2pi)^d.
Sign bookkeeping of the two-loop prefactor: i(-1) [overall i, loop] x i^4 (4 quark propagators) x
(-i)^2 (vertices) x (-i) (gluon) = 1; Wick rotation of two loops i^2 = -1; four quark denominators
(-1)^4; the gluon denominator -1: total +1.
In each gluon exchange gamma^a X gamma_a -> gamma^a X gamma_a + (1-xi) qslash X qslash / Q.

Diagrams (fermion line 2 carries the current from nu to mu; at q = 0 all line momenta are k or l):

    SE1: Tr[g^mu N2(k) g_mu N1(k) g^a N1(l) g_a N1(k)] / [D2(k) D1(k)^2 D1(l) Q]
    SE2: Tr[g^mu N2(k) g^a N2(l) g_a N2(k) g_mu N1(k)] / [D2(k)^2 D2(l) D1(k) Q]
    V  : Tr[g^mu N2(k) g^a N2(l) g_mu N1(l) g_a N1(k)] / [D2(k) D2(l) D1(l) D1(k) Q]

One-loop check (paper): Pi_V(m1,m2) = -(4 N_C/d) \int [(d-2)k_E^2 + d m1 m2]/(D1 D2).
With T(a) = \int_k 1/(k^2+m^2)^a = Gamma(a-d/2)(m^2)^{d/2-a}/((4pi)^{d/2}Gamma(a)), (d-2)T(1) = -2 m^2 T(2):
Pi_V(m,m) = 0 (Ward identity, check), Pi_V(m,0) = 8 N_C m^2 T(2)/d, Pi_V(m,-m) = 8 N_C m^2 T(2), so

    Delta rho_0 = sqrt2 G_F 2 N_C m^2 T(2) (4-d)/d -> sqrt2 G_F N_C m^2/(16 pi^2) = N_C G_F m^2/(8 sqrt2 pi^2).

(Positive: the neutral current is strengthened.)  Note (4-d) T(2) is finite: the 1/eps of the two
correlators cancels in the combination (2.2), but their O(eps) parts are kept exactly in d below because
they multiply the 1/eps of the mass counterterm.

## 4. Two-loop vacuum integrals (Euclidean, measure d^dk/pi^{d/2})

(a) one massive line, two massless:
    J_m00(a; b, c) = \int\int 1/[(k^2+m^2)^a (l^2)^b ((k-l)^2)^c]
                   = (m^2)^{d-a-b-c} G(a+b+c-d) G(d/2-b) G(d/2-c) G(b+c-d/2) / [G(a) G(b) G(c) G(d/2)].
    Derivation: the massless l-loop gives (k^2)^{d/2-b-c} G(d/2-b)G(d/2-c)G(b+c-d/2)/(G(b)G(c)G(d-b-c));
    the remaining massive tadpole with that power of k^2 gives
    (m^2)^{d-a-b-c} G(d-b-c) G(a+b+c-d)/(G(d/2) G(a)); G(d-b-c) cancels.
(b) two massive lines (same mass), one massless:
    J_mm0(a, b; c) = (m^2)^{d-a-b-c} G(a+c-d/2) G(b+c-d/2) G(d/2-c) G(a+b+c-d) / [G(a) G(b) G(d/2) G(a+b+2c-d)].
    Derivation: Feynman-parametrize the (k^2+m^2)^a ((k-l)^2)^c pair, do k, then Mellin-Barnes /
    parametric l integral (checked: c = 0 gives the product of tadpoles; c = -1 reproduces the
    elementary expansion; numerically verified at convergent integer indices in d = 4, see section 8).
(c) Any integral whose massless lines are scaleless vanishes; 1/G(n) = 0 for integers n <= 0 implements this.
(d) on-shell one-loop (mass shell p_E^2 = -m^2):
    O(a, b) = \int 1/[(k^2+m^2)^a ((k-p)^2)^b] = (m^2)^{d/2-a-b} G(a+b-d/2) G(d-a-2b)/(G(a) G(d-a-b)),
    from Feynman parameters: x(1-x)p^2 + (1-x) m^2 = (1-x)^2 m^2 on shell.

Reduction: after the trace, k.l = -(K + L - Q)/2, K = k_E^2 etc. Each line momentum then carries powers of
a single factor (K + m^2) or K, after partial fractions in K (and in L) when both D_1(k) and D_2(k) appear
with m_1 != m_2. Every term is one of (a), (b), (c).

## 5. Mass renormalization

Sigma(pslash) defined by full propagator i/(pslash - m_0 - Sigma); Euclidean form
Sigma = g^2 C_F \int [gamma^a N(k) gamma_a + (1-xi) qslash N qslash /Q]/((k^2+m^2) Q), q = p - k.
Pole mass: m_pole = m_0 + Sigma(pslash = m_pole). On shell Sigma = Tr[(pslash+m) Sigma]/(4m), reduced to O(a,b).
Write Sigma_OS/m = (alpha_s/4pi) e^{gamma eps} (mu^2/m^2)^eps S(eps), using the MS-bar bare coupling
g_0^2 = 4 pi alpha_s mu^{2eps} (e^gamma/4pi)^eps, so that g_0^2/(4pi)^{d/2} = (alpha_s/4pi) e^{gamma eps} mu^{2eps}.

* pole scheme: m_0 = m (1 - Sigma_OS/m);
* MS-bar: m_0 = mbar (1 - (alpha_s/4pi) S_{-1}/eps) (the pure pole; Z_m is mass independent),
  so m_pole/mbar = 1 + (alpha_s/4pi)[finite part of e^{gamma eps}(mu^2/m^2)^eps S(eps)].

## 6. Assembly

Pi(m_0) = Pi^(1)(m) + Pi^(2)(m) - sigma m d/dm Pi^(1)(m), m d/dm Pi^(1) = (2 - 2eps) Pi^(1) exactly in d
(Pi^(1) ~ (m^2)^{1-eps}). sigma = Sigma_OS/m (pole) or the MS pole term. The massless b has no counterterm.
Then c = lim_{eps->0} [Delta rho^(2) + counterterm]/Delta rho_0 in units alpha_s/pi.

## 7. Gauge independence (why)

Delta rho is a ratio of q = 0 correlators of colour-singlet, gauge-invariant currents; the gluon gauge
parameter enters only through gauge-invariant combinations (Ward identity between vertex and self-energy
subgraphs), and the pole mass is gauge independent (it is a pole of the propagator, an S-matrix property),
the MS-bar mass is gauge independent because Z_m is (minimal subtraction of a gauge-invariant operator
m psibar psi). Checked explicitly: the code carries xi and the result is xi-independent (section 8).

## 8. Independent second route(s)

1. General covariant gauge xi: different integrands, the xi terms must cancel in c and in the pole mass.
2. Vector Ward identity Pi_V(m,m)(0) = 0 at two loops (fixes vertex vs self-energy normalization).
3. Pole cancellation (1/eps^2 and 1/eps) and mu-independence of the pole-scheme coefficient.
4. Renormalization group: d c_MSbar/d ln mu^2 = -2 x (coefficient of alpha_s/pi in d ln mbar/d ln mu^2),
   obtained from the 1/eps residue of Z_m alone.
5. The master integrals (a), (b) are verified by direct numerical integration (4D radial x relative angle,
   scipy) at convergent indices in d = 4 (tmp/masters.py):
     J_mm0(2,2,1) = 1.00000009 (formula 1), J_mm0(2,1.5,1.5) = 1.3333332 (4/3),
     J_mm0(1.5,2.5,0.7) = 4.697809 (4.697801), J_m00(2,1.5,1.5) = 3.9999996 (4).
   (d) (on-shell) is not checked numerically; its 1/eps residue 3 C_F (alpha_s/4pi) is the UV divergence of the
   off-shell self-energy and its finite part enters only through m_pole/mbar, which check 4 ties to the RG.

Outcome of the second route (printed by `python3 qcd_drho.py`): with xi kept symbolic, individual diagrams
depend on xi (e.g. the t self-energy insertion in the t-b loop has a (1-xi)(4/eps^2 + 4/eps + ...) piece), but
each correlator, Sigma_OS (finite part 4 + 3 L for any xi), the poles (all zero) and c are xi independent;
Pi_V^(2)(m,m) = 0 through O(eps); d c_pole/d L = 0; d c_MSbar/d L = 3/2 = 2 x 3/4; (c_MSbar - c_pole)/C_F
= 2 + (3/2) L = 2 x finite(Sigma_OS)/4.

## 9. Results (computer algebra in qcd_drho.py, exact in d until the final eps expansion)

Gamma functions: every Gamma(n + c eps) is written exactly as Gamma(1 + c eps) x (rational in eps), so a
two-loop term carries one of two transcendental "signatures":
  (m,m,0) and factorized tadpoles: Gamma(1+eps)^2;
  (m,0,0):                         Gamma(1+2eps) Gamma(1-eps) Gamma(1+eps)
                                   = Gamma(1+eps)^2 [1 + 2 zeta_2 eps^2 + O(eps^3)].
In the full renormalized combination E^{-1} x [P2 - sigma (2-2eps) P1] (pole scheme) the computer algebra gives

    Gamma(1+eps)^2 [ 2/eps^2 + 5/eps + 17/2 ]  +  Gamma(1+2eps)Gamma(1-eps)Gamma(1+eps) [ -2/eps^2 - 5/eps - 21/2 ]
  = Gamma(1+eps)^2 [ (17/2 - 21/2) - 2 x 2 zeta_2 + O(eps) ] = -2 - 2 pi^2/3,

so the rational part (-2) is the mismatch of the finite parts and the whole pi^2 is the 2 zeta_2 eps^2 of the
(m,0,0) signature (charged t-b correlator, massless b and gluon lines) multiplying its 1/eps^2.
Then c/C_F = (-2 - 2 pi^2/3)/4 = -1/2 - pi^2/6 (factor 1/4: alpha_s/4pi -> alpha_s/pi; one-loop lead = 1).

One loop (units N_C/(4pi)^{d/2}, m = 1):
  Pi_V(1,1) = 0,  Pi_V(1,0) = 8 Gamma(eps)/(4-2eps),  Pi_V(1,-1) = 8 Gamma(eps),
  Pi_V(1,0) - Pi_V(1,-1)/4 = 1 + eps(1/2 - gamma) + O(eps^2)  ->  Delta rho_0 = N_C G_F m^2/(8 sqrt2 pi^2).

Mass renormalization (independent of xi, as it must be):
  Sigma_OS/m = (alpha_s/4pi) C_F e^{gamma eps}(mu^2/m^2)^eps [3/eps + 4 - 3 gamma + O(eps)]
             = (alpha_s/4pi) C_F [3/eps + 4 + 3 ln(mu^2/m^2) + O(eps)].
  Z_m = 1 - 3 C_F alpha_s/(4 pi eps)  (gamma_m > 0: mbar decreases with mu),
  m_pole = mbar(mu) [1 + C_F (alpha_s/pi)(1 + (3/4) ln(mu^2/mbar^2))],  m_pole^2 = mbar^2 [1 + 2 C_F (alpha_s/pi)(1 + (3/4) L)].

Two loops: the vector Ward identity Pi_V^(2)(1,1) = 0 holds identically in d and in xi (bare, before the
counterterm, as it must since the diagonal vector current is conserved for any m_0).
Combination E [P2 - sigma (2-2eps) P1] (E = e^{gamma eps} mu^{2eps}): the 1/eps^2 and 1/eps poles cancel
(UV subdivergences of the self-energy subgraphs against the mass counterterm; the overall divergence
cancels between the charged and neutral correlators exactly as at one loop), leaving

  c_pole  = - C_F (1/2 + pi^2/6) = - C_F (3 + pi^2)/6          [C_F = 4/3: -(2/9)(3 + pi^2) = -2.8599]
  c_MSbar = c_pole + 2 C_F (1 + (3/4) L) = C_F (3/2 - pi^2/6 + (3/2) ln(mu^2/mbar^2))   [mu = mbar, C_F = 4/3: -0.19325]

Colour: one gluon exchange inside a single quark loop, colour factor Tr(T^a T^a)/Tr(1) = C_F relative to the
one-loop N_C; so c is linear in C_F and N_C-independent at this order.
Scheme relation: c_MSbar - c_pole = 2 C_F (1 + (3/4) L), from m_pole^2/mbar^2 at O(alpha_s), since
Delta rho_0 ~ m^2.
RG check: d c_MSbar/d ln mu^2 = (3/2) C_F = 2 x (3/4) C_F = 2 x (Z_m residue 3 C_F/4 in units alpha_s/pi),
i.e. it compensates d ln mbar^2/d ln mu^2 = -(3/2) C_F alpha_s/pi.

## 10. What was not derived / caveats

* The (m,m,0) closed form (4b) is quoted from its derivation sketch (Feynman parameters + parametric/
  Mellin-Barnes l integral) rather than carried through line by line here; it is instead verified numerically
  (section 8.5), in its c = 0 and c = -1 limits, and indirectly by the exact two-loop Ward identity
  Pi_V^(2)(m,m) = 0, which uses only (m,m,0) integrals and fails for any wrong normalization or index dependence.
* Anticommuting gamma5 is assumed (justified in section 2).
* The number c is not typed in anywhere: the module rebuilds it from the traces, the Gamma-function masters
  and the counterterm on first call (about 8 s, cached).
