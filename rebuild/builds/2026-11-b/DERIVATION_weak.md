# DERIVATION: stage `weak` (build 2026-11-b)

Postulates: SPEC.md section 10 only. Inputs: `inputs.GAMMA_PI_MUNU, DELTA_PI, V_UD, G_F, M_MU, M_PIC, HBAR, E_CH`.
Nothing is quoted; nothing was left underived. Natural units (hbar = c = 1) until section 5.

## 0. Conventions fixed before deriving

SPEC fixes g_{mu nu} = diag(-1, 1, 1, 1) and gamma_5 = i gamma^0 gamma^1 gamma^2 gamma^3. It does not fix the
sign in the Clifford algebra. I take

    {gamma^mu, gamma^nu} = -2 g^{mu nu}                                   (C)

so (gamma^0)^2 = +1, (gamma^i)^2 = -1: the matrices are the familiar Hermitian gamma^0 and anti-Hermitian
gamma^i, gamma^0 gamma^mu^dagger gamma^0 = gamma^mu, and gamma_5 is Hermitian with gamma_5^2 = 1, anticommuting
with every gamma^mu. (The other choice, {gamma, gamma} = +2g, is gamma^mu -> i gamma^mu; gamma_5 is unchanged
because i^4 = 1, and |M|^2 is unchanged; see section 6, point 1.)

Consequences of (C), with a-slash = a_mu gamma^mu and a.b = g_{mu nu} a^mu b^nu (so p^2 = -m^2 on shell):

    a-slash b-slash + b-slash a-slash = -2 a.b ,      a-slash a-slash = -a^2
    Tr 1 = 4 ,   Tr[a-slash b-slash] = -4 a.b ,   Tr[gamma_5 a-slash b-slash] = 0 ,   Tr[odd number of gammas] = 0

(the third because gamma_5 a-slash b-slash needs four distinct gammas to have a trace; the trace of two is
symmetric, -4 g, and Tr gamma_5 = 0.)

Free Dirac field (i d-slash psi-type equation in this signature): the plane-wave spinors obey

    (p-slash + m) u(p, s) = 0 ,     (-p-slash + m) v(p, s) = 0 ,
    ubar (p-slash + m) = 0 ,        vbar (-p-slash + m) = 0 ,
    sum_s u ubar = -p-slash + m ,   sum_s v vbar = -p-slash - m ,       ubar u = 2m.

Check: p-slash = p_mu gamma^mu = -E gamma^0 + p.gamma (p_0 = -E), so (p-slash + m) u = 0 is
(E gamma^0 - p.gamma - m) u = 0, the usual equation, and the projector -p-slash + m = E gamma^0 - p.gamma + m is
the usual one. With relativistic normalization <p|p'> = 2E (2 pi)^3 delta^3 (SPEC) these are the spin sums that
go with it (u^dagger u = 2E).

## 1. The amplitude  (SPEC section 10, postulates 1-3)

Process: pi^-(p) -> l^-(k, s) + nubar(q, s'), p = k + q, p^2 = -m_pi^2, k^2 = -m_l^2, q^2 = 0.

The term written out in L (not its h.c.) does it: ubar ... d annihilates the d quark and the u antiquark of the
pi^-; lbar creates l^-; nu creates the antineutrino. To first order, <f| i int L |i> = i (2 pi)^4 delta^4 M with

    M = -(G_F/sqrt2) V_ud <0| ubar gamma^alpha (1 - gamma_5) d |pi^-(p)>  ubar_l(k) gamma_alpha (1 - gamma_5) v_nu(q).

Hadronic factor: the vector part vanishes (parity; SPEC), the axial part is -<0|ubar gamma^alpha gamma_5 d|pi>
= -i f_pi p^alpha. So

    M = i (G_F/sqrt2) V_ud f_pi  ubar_l(k) p-slash (1 - gamma_5) v_nu(q).                       (1.1)

Reduce with p = k + q and the Dirac equations:
- ubar(k) k-slash = -m_l ubar(k);
- q-slash (1 - gamma_5) v(q) = (1 + gamma_5) q-slash v(q) = 0, since the neutrino is massless (-q-slash v = 0).

    M = -i (G_F/sqrt2) V_ud f_pi m_l  ubar_l(k) (1 - gamma_5) v_nu(q).                          (1.2)

The explicit m_l is the helicity suppression: V - A forces the antineutrino right-handed and (for m_l = 0) the
lepton left-handed, which a spin-0 parent at rest cannot emit back to back; the amplitude needs a helicity flip,
proportional to m_l.

## 2. The spin sum (the trace)

[ubar (1 - gamma_5) v]^* = vbar (1 + gamma_5) u   (gamma^0 (1-gamma_5)^dagger gamma^0 = 1 + gamma_5). Summing
over the lepton spin and over both spin labels of v (the unwanted antineutrino helicity is removed by the
projector, so summing over two labels is the same as keeping the one physical state):

    sum |M|^2 = (G_F^2/2) |V_ud|^2 f_pi^2 m_l^2  T ,
    T = Tr[ (-k-slash + m_l) (1 - gamma_5) (-q-slash) (1 + gamma_5) ].

(1 - gamma_5)(-q-slash)(1 + gamma_5) = -q-slash (1 + gamma_5)^2 = -2 q-slash (1 + gamma_5). Then

    T = -2 Tr[(-k-slash + m_l) q-slash (1 + gamma_5)]
      = 2 Tr[k-slash q-slash] + 2 Tr[k-slash q-slash gamma_5] - 2 m_l Tr[q-slash (1 + gamma_5)]
      = 2 (-4 k.q) + 0 - 0 = -8 k.q .

Kinematics: p^2 = (k+q)^2  =>  -m_pi^2 = -m_l^2 + 2 k.q  =>  k.q = -(m_pi^2 - m_l^2)/2. Hence T = 4 (m_pi^2 - m_l^2),

    sum |M|^2 = 2 G_F^2 |V_ud|^2 f_pi^2 m_l^2 (m_pi^2 - m_l^2).                                 (2.1)

It is a constant (no angle): a spin-0 parent decays isotropically.

## 3. Two-body phase space

With <p|p'> = 2E (2pi)^3 delta^3, the rate of a particle of mass M at rest is

    Gamma = (1/2M) int d^3k/((2pi)^3 2E_k) d^3q/((2pi)^3 2E_q) (2pi)^4 delta^4(p - k - q) sum|M|^2 .

(Derivation of the 1/2M: probability = |<f|i>|^2/<i|i>, <i|i> = 2M V, one factor (2pi)^4 delta^4(0) = V T, final
states counted with d^3k/((2pi)^3 2E) each, divide by T.) The delta^3 sets q = -k, E_q = |k| = k:

    Gamma = (1/2M) (1/(4 pi^2)) int d^3k/(4 E_k k) delta(M - E_k - k) sum|M|^2 ,   E_k = sqrt(k^2 + m_l^2).

d^3k = k^2 dk dOmega; the argument's derivative is d(E_k + k)/dk = k/E_k + 1 = (E_k + k)/E_k = M/E_k at the root:

    int k^2 dk/(E_k k) delta(M - E_k - k) = (k/E_k)(E_k/M) = k*/M ,
    root: sqrt(k^2 + m_l^2) = M - k  =>  k* = (M^2 - m_l^2)/(2M)   (needs m_l <= M).

    Gamma = (1/2M) (1/(16 pi^2)) (k*/M) int dOmega sum|M|^2 = (k*/(8 pi M^2)) <sum|M|^2>_Omega .          (3.1)

## 4. Result: `pion_decay_width(fpi, GF, Vud, m_l, m_pi)`

(2.1) in (3.1) with M = m_pi:

    Gamma_tree = G_F^2 |V_ud|^2 f_pi^2 m_l^2 (m_pi^2 - m_l^2)^2 / (8 pi m_pi^3)
               = (G_F^2 |V_ud|^2 f_pi^2 / (8 pi)) m_pi m_l^2 (1 - m_l^2/m_pi^2)^2 .                       (4.1)

Units: GeV^-4 GeV^2 GeV^3 = GeV. f_pi is the ~130 MeV convention because the postulate is <0|A|pi> = i f p
(no sqrt2). For m_l >= m_pi the channel is closed: the function returns 0. The code evaluates it as the
product of its derived pieces (spin sum (2.1) x phase space (3.1)), not as a remembered formula.

Checks visible in (4.1): ~ f^2 G_F^2 V^2; dimension of mass; ~ m_l^2 as m_l -> 0, exactly 0 at m_l = 0;
~ (m_pi - m_l)^2 -> 0 at threshold.

## 5. `fpi_from_pion_decay()`

Measured: Gamma_meas = inputs.GAMMA_PI_MUNU (s^-1), radiation inclusive; Gamma_meas = Gamma_tree (1 + DELTA_PI).
Conversion: Gamma[GeV] = hbar Gamma[s^-1], hbar = inputs.HBAR/(inputs.E_CH x 10^9) GeV s (J s -> eV s -> GeV s).

    Gamma_tree,target = hbar GAMMA_PI_MUNU/(1 + DELTA_PI) .

Inversion "using pion_decay_width itself": by (4.1) the width is exactly homogeneous of degree 2 in f_pi, so
with a reference f_0 = 1 GeV

    f_pi = f_0 sqrt( Gamma_tree,target / pion_decay_width(f_0, G_F, V_UD, M_MU, M_PIC) ),   positive root.

Scalings: f ~ sqrt(Gamma)/G_F (the harness's sensitivity check).

## 6. Independent second routes (run under `__main__`)

A. **Explicit spinors, no trace technology, no Dirac-equation reduction.** Dirac-representation matrices
   satisfying (C); u = sqrt(E+m) (chi, sigma.p chi/(E+m)), v = sqrt(E+m) (sigma.p eta/(E+m), eta); evaluate the
   unreduced amplitude (1.1), i.e. ubar(k) p-slash (1 - gamma_5) v(q) with p-slash = -m_pi gamma^0, for the four
   spin combinations, sum the squares, and average over the lepton direction with `toolkit.trapezoid` in
   cos(theta). Tests (1.2), the trace, the sign conventions and isotropy at once. The spinors are first checked
   against the spin sums of section 0.
B. **Matrix trace of the unreduced amplitude:** Tr[(-k-slash + m) p-slash (1 - gamma_5)(-q-slash)(1 + gamma_5) p-slash]
   by 4x4 matrix multiplication, compared with m_l^2 T = 4 m_l^2 (m_pi^2 - m_l^2).
C. **Phase space numerically:** replace delta(M - E_k - k) by a narrow Gaussian and integrate over k with
   `toolkit.trapezoid`; compare with k*/M.
D. **Inversion by a different method:** solve pion_decay_width(f) = target with `toolkit.bisect`; compare with
   the square-root scaling.
E. Limits: Gamma/m_l^2 constant as m_l -> 0; lepton universality ratio Gamma(e)/Gamma(mu) depends only on masses.

## 7. Interpretation points (also in QUESTIONS.md)

1. Clifford sign not fixed by SPEC for the mostly-plus metric; chose {gamma,gamma} = -2g. Result independent.
2. m_l >= m_pi: returns 0.0 (closed channel) rather than raising.
3. |V_ud| enters squared; a negative or complex-phase convention is irrelevant (abs taken via the square).
4. Neutrino "left-handed": the (1 - gamma_5) projector already selects the one antineutrino helicity, so no
   extra factor 1/2 in the spin sum.

## 8. Self-check results (python3 weak.py, probe f=0.13, GF=1e-5, V=0.97, m_l=0.11, m_pi=0.14)

- A: explicit-spinor sum|M|^2 / trace formula = 1 to 1e-15; angular spread 1e-15 (isotropic).
- B: matrix trace of the unreduced amplitude = 4 m_l^2 (m_pi^2 - m_l^2) to 1e-15.
- C: Gaussian-smeared delta (sigma = 1e-3 m_pi) reproduces k*/M to a few 1e-6, the expected O(sigma^2) smearing
  bias; so the full second-route width agrees with (4.1) to the same few 1e-6.
- D: bisection f_pi = square-root-scaling f_pi to 12 digits.
