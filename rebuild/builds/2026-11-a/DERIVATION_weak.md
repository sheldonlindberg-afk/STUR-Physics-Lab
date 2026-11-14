# DERIVATION: weak (SPEC.md section 10)

Postulates used (all SPEC 10): the V-A charged-current Lagrangian below M_W; the pion matrix
element <0| ubar gamma^a gamma5 d |pi-(p)> = i f p^a (the ~130 MeV convention), vector current
not contributing; relativistic normalization <p|p'> = 2E (2pi)^3 delta^3(p - p'); massless
left-handed neutrino; sum over lepton spin; Gamma_meas = Gamma_tree (1 + DELTA_PI); hbar in GeV s
= HBAR / (E_CH 1e9). Inputs: G_F, V_UD, M_MU, M_PIC, GAMMA_PI_MUNU, DELTA_PI, HBAR, E_CH.
Nothing is quoted.

## Conventions

Metric g = diag(-1, 1, 1, 1), so p^2 = -m^2 on shell and p.q = -p^0 q^0 + p.q (3-vectors).
Clifford algebra {gamma^m, gamma^n} = -2 g^{mn} (so (gamma^0)^2 = +1, (gamma^i)^2 = -1),
gamma5 = i gamma^0 gamma^1 gamma^2 gamma^3, gamma5^2 = 1, {gamma5, gamma^m} = 0, gamma5 Hermitian.
pslash = p_m gamma^m = -p^0 gamma^0 + p^i gamma^i, so pslash pslash = -p^2 = m^2.
Dirac bar psibar = psi^dag beta with beta = gamma^0 (Weyl basis below); the bar of a matrix is
Gbar = beta G^dag beta, so (ubar_1 G u_2)^* = ubar_2 Gbar u_1, and Gbar for (1 - gamma5) is (1 + gamma5)
(gamma5 Hermitian, anticommutes with beta), gamma^m bar = gamma^m.
Free spinors in this metric: (-pslash + m) u = 0, (pslash + m) v = 0; spin sums
sum_s u ubar = -pslash + m, sum_s v vbar = -pslash - m. Traces: Tr 1 = 4,
Tr(aslash bslash) = -4 a.b, Tr(odd # gammas) = 0, Tr(gamma5 aslash bslash) = 0.

Explicit Weyl basis (used in the numerical second route): gamma^0 = [[0, I],[I, 0]],
gamma^i = [[0, sigma^i],[-sigma^i, 0]]; one checks {gamma^m, gamma^n} = -2 g^{mn} directly.

## 1. `pion_decay_width(fpi, GF, Vud, m_l, m_pi)` -> Gamma_tree (GeV)

### 1a. Amplitude
The pi- = (d, ubar) is annihilated by ubar ... d. The h.c.-free term of L acting on |pi-> and
creating l- and nubar:

    M = -(G_F/sqrt2) V_ud <0| ubar gamma^a (1 - gamma5) d |pi-(p)> * ubar_l(k) gamma_a (1 - gamma5) v_nu(q).

(An overall phase, including the i of i M = i <f|L|i>, drops out of |M|^2.) By parity the vector
part vanishes, so <0| ubar gamma^a (1-gamma5) d |pi-> = -i f p^a, and

    M = i (G_F/sqrt2) V_ud f * ubar_l(k) pslash (1 - gamma5) v(q),     p = k + q.

### 1b. Dirac equation reduction (helicity suppression)
pslash (1 - gamma5) = kslash (1 - gamma5) + qslash (1 - gamma5) and qslash(1 - gamma5) = (1 + gamma5) qslash,
with qslash v(q) = 0 (massless: (qslash + 0) v = 0). From (-kslash + m_l) u = 0, ubar kslash = m_l ubar
(take the bar: ubar(-kslash + m) = 0 since kslash bar = kslash). Hence

    ubar_l pslash (1 - gamma5) v = m_l ubar_l (1 - gamma5) v,
    M = i (G_F/sqrt2) V_ud f m_l ubar_l (1 - gamma5) v.

The amplitude is proportional to m_l: it vanishes for a massless lepton (helicity suppression).

### 1c. Spin sum (the trace)
sum_spins |ubar (1-gamma5) v|^2 = sum ubar (1-gamma5) v vbar (1+gamma5) u
  = Tr[(1-gamma5)(-qslash)(1+gamma5)(-kslash + m_l)].
Since gamma5 anticommutes with qslash, (1-gamma5) qslash (1+gamma5) = qslash (1+gamma5)^2 = 2 qslash (1+gamma5);
the two minus signs of (-qslash)(-kslash) cancel. The m_l term: Tr[2 qslash (1+gamma5) m_l] = 0
(one or three-plus-gamma5 gammas: odd count, trace 0); its overall sign is -, irrelevant since it is 0.
The kslash term: Tr[(1-gamma5) qslash (1+gamma5) kslash] = 2 Tr[qslash (1+gamma5) kslash]
= 2 Tr[qslash kslash] = -8 q.k (the gamma5 piece has only two gammas, trace 0).
Kinematics: p = k + q, -m_pi^2 = -m_l^2 + 2 k.q + 0 so k.q = -(m_pi^2 - m_l^2)/2. Hence

    sum_spins |ubar (1-gamma5) v|^2 = 4 (m_pi^2 - m_l^2),
    sum |M|^2 = (G_F^2/2) V_ud^2 f^2 m_l^2 * 4 (m_pi^2 - m_l^2) = 2 G_F^2 V_ud^2 f^2 m_l^2 (m_pi^2 - m_l^2).

(No average: the pion has spin 0. The neutrino has one helicity; the trace over v's with the
(1+gamma5) projector already selects it, so summing over the "neutrino spin" in the completeness
relation is the same as taking the single physical state.)

### 1d. Two-body phase space
With the normalization <p|p'> = 2E (2pi)^3 delta^3, the rest-frame width is

    Gamma = (1/(2 m_pi)) Int d^3k/((2pi)^3 2E_k) d^3q/((2pi)^3 2E_q) (2pi)^4 delta^4(p - k - q) sum|M|^2.

Do the d^3q integral with delta^3 (q = -k), then angles (|M|^2 is isotropic), leaving

    Phi_2 = Int 4pi k^2 dk /((2pi)^2 4 E_l E_nu) delta(m_pi - E_l(k) - k),  E_nu = k, E_l = sqrt(k^2 + m_l^2).

Root: m_pi - sqrt(k^2 + m^2) = k  =>  k* = (m_pi^2 - m_l^2)/(2 m_pi). Jacobian
|d(E_l + k)/dk| = k/E_l + 1 = (k + E_l)/E_l = m_pi/E_l. So

    Phi_2 = 4pi k*^2 E_l/(4 pi^2 * 4 E_l k* m_pi) = k*/(4 pi m_pi).

### 1e. Result (closed form)

    Gamma_tree = (1/(2 m_pi)) * k*/(4 pi m_pi) * 2 G_F^2 V_ud^2 f^2 m_l^2 (m_pi^2 - m_l^2)
               = G_F^2 V_ud^2 f^2 m_l^2 (m_pi^2 - m_l^2)^2 / (8 pi m_pi^3)
               = (G_F^2 V_ud^2 f^2 / (8 pi)) m_pi m_l^2 (1 - m_l^2/m_pi^2)^2.

Below threshold (m_l >= m_pi) the decay is closed; the code returns 0 there (and at m_l = 0
the formula gives exactly 0). Properties: ~ f^2 G_F^2 V^2; dimension [GeV^-4][GeV^2][GeV^5]/[GeV^3]
= GeV; ~ m_l^2 for m_l << m_pi; vanishes as (m_pi - m_l)^2 at threshold.

### 1f. Second routes (in `weak.py` __main__)
(i) Trace by explicit 4x4 complex Dirac matrices in the Weyl basis: build kslash, qslash, pslash,
gamma5 numerically for a rest-frame configuration, form G = pslash(1 - gamma5) WITHOUT using the
Dirac-equation reduction, and evaluate Tr[G (-qslash) Gbar (-kslash + m)] with Gbar = beta G^dag beta.
This must equal m_l^2 * 4(m_pi^2 - m_l^2). It independently tests 1b and 1c (including the sign
conventions of the metric, gamma5 and the spin sums). Also checks the Clifford relation numerically.
(ii) Phase space by smearing: replace delta(m_pi - E_l - k) by a narrow normalized Gaussian of
width s and integrate Int 4pi k^2/((2pi)^2 4 E_l k) g_s(m_pi - E_l - k) dk with toolkit.trapezoid;
as s -> 0 it must tend to k*/(4 pi m_pi) (error O(s^2)).
(iii) Limit m_l -> 0: Gamma / m_l^2 -> G^2 V^2 f^2 m_pi/(8 pi).

## 2. `fpi_from_pion_decay()` -> f_pi (GeV)

Gamma_tree,meas = GAMMA_PI_MUNU * hbar_GeVs / (1 + DELTA_PI), hbar_GeVs = HBAR/(E_CH * 1e9)
(converts s^-1 to GeV: E = hbar omega). Gamma_tree is exactly quadratic in f (section 1e) with f > 0,
so inverting via pion_decay_width itself:

    f_pi = sqrt( Gamma_tree,meas / pion_decay_width(1, G_F, V_UD, M_MU, M_PIC) ).

Closed form: f_pi = sqrt(8 pi m_pi^3 Gamma_tree,meas) / (G_F V_ud m_mu (m_pi^2 - m_mu^2)).
Scalings: f ~ sqrt(Gamma)/G_F.

Second route (in __main__): solve pion_decay_width(f, ...) = Gamma_tree,meas for f by
toolkit.bisect on [0, 1] GeV, and also print the closed form above evaluated directly.

## Not derived / caveats
- The radiative correction DELTA_PI is an input (SPEC 10), not derived.
- The ~130 MeV convention is fixed by the SPEC's matrix element; the ~92 MeV value is f/sqrt2
  (used by later stages, not here).
