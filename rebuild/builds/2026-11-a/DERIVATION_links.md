# DERIVATION: links (SPEC.md section 8, "Connections between stages")

The links stage carries no new dynamics: each export is a place where one rung's output feeds
another. Exact quantities (charges, the anomaly identity) are `fractions.Fraction`; every
measured constant is read as `inputs.NAME` at call time. Upstream results are reached only as
`gauge331.quark_charges`, `gauge331.triplet_charges`, `blackholes.hawking_K` (and, in the
self-check only, `graviton.entangling_phase`, `graviton.ramp_profile`, `toolkit.bisect`,
`toolkit.trapezoid`); `toolkit.levi_civita` builds the epsilon tensor of the pi0 amplitude.

Units: SI inside, GeV / eV at the edges via 1 GeV = 1e9 * inputs.E_CH J (the 1e9 is the
definition of the giga prefix, not a measured number).

---------------------------------------------------------------------------------------------------
## 1. qp_qe_minus_anomaly(Nc, b, XL, Xt) -> Fraction   [rung 1 -> 4]

**Postulates** (SPEC section 8, rung 1 = SPEC section 2). For rational b = beta/(2 sqrt3),
X_L, X_t and odd N_c:
- lepton triplet Q_nu = 1/2 + b + X_L, Q_e = -1/2 + b + X_L (components 1, 2 of Q = T3 + b diag(1,1,-2) + X);
- quark triplet Q_u = 1/2 + b + X_t, Q_d = -1/2 + b + X_t;
- antitriplet X_a = X_t + 2b (its first two components are then (Q_d, Q_u): -(+-1/2 + b) + X_t + 2b);
- N_g = N_c, n = (1 + N_c)/2 antitriplet families;
- anomaly = N_g X_L + N_c[(N_g - n) X_t + n X_a]
  (each lepton triplet contributes its X once; each quark (anti)triplet N_c times, with equal
  Dynkin index for 3 and 3bar, so the common index factors out);
- N_c-quark proton = ((N_c+1)/2 u, (N_c-1)/2 d); neutron the reverse.

**Derivation.**

    q_p = (N_c+1)/2 Q_u + (N_c-1)/2 Q_d
        = N_c (b + X_t) + (1/2)[(N_c+1)/2 - (N_c-1)/2] = N_c (b + X_t) + 1/2,
    q_p + q_e = N_c(b + X_t) + 1/2 - 1/2 + b + X_L = (N_c + 1) b + N_c X_t + X_L.

    anomaly = N_c X_L + N_c[(N_c - n) X_t + n X_t + 2 n b] = N_c X_L + N_c^2 X_t + N_c (1 + N_c) b
            = N_c [ (N_c+1) b + N_c X_t + X_L ] = N_g (q_p + q_e).

Hence (q_p + q_e) - anomaly/N_g = 0 identically in b, X_L, X_t. The only role of odd N_c is that
n = (1+N_c)/2 and the proton's quark numbers are integers; the cancellation of b uses
2 n = 1 + N_c, i.e. exactly the antitriplet count SPEC prescribes.

Neutron and neutrino:

    q_n = (N_c-1)/2 Q_u + (N_c+1)/2 Q_d = N_c(b + X_t) - 1/2,
    q_n + Q_nu = N_c(b + X_t) - 1/2 + 1/2 + b + X_L = (N_c+1) b + N_c X_t + X_L = q_p + q_e.

So the anomaly-free condition makes hydrogen neutral AND makes (neutron + neutrino) neutral
with the same linear form: q_n + Q_nu = q_p + q_e = anomaly/N_g. Note q_p - q_n = 1 = Q_nu - Q_e
(both are the T3 splitting), which is the same statement.

**Closed form.** The export evaluates both sides from the definitions (not from the closed form)
and returns their exact difference, which must be Fraction(0).

**Second route.** (a) Randomized exact test over rational (b, X_L, X_t) and N_c in {3,...,11}
(self-check); (b) the closed form (N_c+1) b + N_c X_t + X_L compared with both q_p + q_e and
anomaly/N_g separately; (c) q_n + Q_nu compared with q_p + q_e.

---------------------------------------------------------------------------------------------------
## 2. matter_charges(Nc, variant) -> (q_p, q_n, q_e, Q_nu)   [rung 1 -> links]

**Postulates.** SPEC section 8: proton/neutron quark content as above; electron and neutrino
are components 2 and 1 of the lepton triplet with X_L from SPEC section 2: X_L = -1/3 for
beta = -1/sqrt3 and -2/3 for beta = +1/sqrt3 (a postulate of rung 1, written as a Fraction).
Rung 1 supplies (Q_u, Q_d) = `gauge331.quark_charges(Nc)` (derived there from anomaly
cancellation) and the lepton triplet's charges `gauge331.triplet_charges(X_L, variant)`.

**Derivation.** q_p = (N_c+1)/2 Q_u + (N_c-1)/2 Q_d, q_n = (N_c-1)/2 Q_u + (N_c+1)/2 Q_d,
(Q_nu, Q_e, Q_3) = triplet_charges(X_L, variant), q_e = Q_e, Q_nu = Q_nu.

**Closed form.** With b = -1/6 (beta = -1/sqrt3) or +1/6 (beta = +1/sqrt3) and X_L as above,
Q_e = -1/2 + b + X_L = -1 and Q_nu = 0 in both variants. Rung 1 gives Q_u = (N_c+1)/(2N_c),
Q_d = Q_u - 1 = -(N_c-1)/(2N_c), so
q_p = [(N_c+1)^2 - (N_c-1)^2]/(4 N_c) = 1 and q_n = [(N_c-1)(N_c+1) - (N_c+1)(N_c-1)]/(4N_c) = 0.
Result (1, 0, -1, 0) for every odd N_c and both variants: Q_u, Q_d individually depend on N_c, the
nucleon charges do not.

**Second route.** Section 1's identity: with b read off rung 1 (b = Q_1 - 1/2 of
triplet_charges(0, variant)) and X_t = Q_u - 1/2 - b, q_p + q_e must equal anomaly/N_g, and rung 1
chose Q_u to set the anomaly to zero, so q_p + q_e = 0 = q_n + Q_nu. The self-check also confirms that
SPEC section 2's X_L equals -1/2 - b (i.e. the postulated X_L is the one that makes Q_e = -1).

---------------------------------------------------------------------------------------------------
## 3. neutrality_per_nucleon(m) -> e   [rung 1 -> rung 4 (the experiment)]

**Postulates.** SPEC section 8: Coulomb and gravity both go as 1/r on the same branch
trajectories, so their entangling phases are in the ratio k Q^2/(G m^2); divide by the nucleon
count N = m/u. Rung 4 (SPEC section 5, graviton stage): the entangling phase is
Delta phi = (1/hbar) Int dt [-U(d_LL) - U(d_RR) + U(d_LR) + U(d_RL)], linear in the potential.
The safety requirement is the same fraction as rung 3's Casimir criterion: Coulomb phase
<= inputs.GAP_FRACTION x gravity phase. Two identical diamonds of mass m, each with net charge
Q = eps e N (eps = net charge per nucleon in units of e).

**Derivation.** U_grav(r) = -G m^2 / r, U_C(r) = +k Q^2 / r with k = inputs.K_COUL. Both are
c/r with the same distances d(t) on the same trajectories, so
Delta phi_C / Delta phi_grav = (k Q^2) / (-G m^2) exactly (the time integral is common).
Requirement |Delta phi_C| <= f |Delta phi_grav|  <=>  k eps^2 e^2 N^2 <= f G m^2. With N = m/u:

    eps_max = sqrt(f G / k) * (m / N) / e = sqrt(f G / k) * u / e.

**Closed form.** eps_max = (u / e) sqrt(f G / k): the diamond mass cancels (both charge and mass
scale with N), so the bound is a material-independent property per nucleon.
Scalings: ~ sqrt(G), ~ sqrt(f) (the sensitivity tier's 4G -> 2x, 4f -> 2x), ~ u.
Here u = inputs.U_AMU is used as the mass per nucleon (m/u is the nucleon count SPEC prescribes;
binding energy and the n-p mass difference are below the precision of "per nucleon").

**Second route.** Compute both entangling phases explicitly for design A's trajectory with
graviton's ramp profile and the trapezoid rule, and the gravity phase also through
`graviton.entangling_phase`; solve |phi_C(eps)| = f |phi_grav| for eps by `toolkit.bisect`
(in log eps), compare with the closed form (self-check). Also: the comparison with
inputs.EPS_PE_BOUND (measured |q_p + q_e|) gives the margin eps_max / bound, and one stray
electron per diamond gives phi_C/phi_grav = k e^2/(G m^2) (printed).

---------------------------------------------------------------------------------------------------
## 4. pi0_width_eV(alpha, fpi, mpi, Nc, Qu, Qd) -> eV   [quoted amplitude A; rest derived]

**Postulates.** SPEC section 8, QUOTED (allowed): the anomaly amplitude A = (alpha/(pi f_pi)) N_c
(Q_u^2 - Q_d^2) for pi0 -> gamma gamma (Adler-Bell-Jackiw; Bardeen), meaning the invariant amplitude
    M = A eps^{mu nu rho sigma} e1*_mu e2*_nu k1_rho k2_sigma.
Standard relativistic normalization: Gamma = (1/(2 m)) (1/S) Int dPhi_2 sum_pol |M|^2, with
S = 2! = 2 for two identical photons and
    dPhi_2 = d^3k1/((2pi)^3 2E1) d^3k2/((2pi)^3 2E2) (2pi)^4 delta^4(P - k1 - k2).
Metric (+,-,-,-); eps_{0123} = +1 = toolkit.levi_civita((0,1,2,3)) (the sign drops out of |M|^2).

**Polarization sum.** Rest frame of the pion: k1 = (m/2)(1, 0, 0, 1), k2 = (m/2)(1, 0, 0, -1)
(Section "phase space": |k| = m/2). Real transverse polarizations e1, e2 in {x_hat, y_hat}
(any real orthonormal transverse basis; real vectors so e* = e).
T(e1, e2) = sum_{mu nu rho sigma} eps_{mu nu rho sigma} e1^mu e2^nu k1^rho k2^sigma.
Since k1, k2 have only t and z components, the nonzero terms need {mu, nu} = {x, y}, so only
(e1, e2) = (x, y) and (y, x) contribute:
    T(x, y) = eps_{12 rho sigma} k1^rho k2^sigma = eps_{1203} k1^0 k2^3 + eps_{1230} k1^3 k2^0
            = (+1)(m/2)(-m/2) + (-1)(m/2)(m/2) = -m^2/2,   T(y, x) = +m^2/2,
    T(x, x) = T(y, y) = 0.
    sum_pol |T|^2 = 2 (m^2/2)^2 = m^4 / 2.
Covariant check: with sum e_mu e*_mu' -> -g_mu mu' (allowed: k_mu eps^{mu...} k... = 0 by
antisymmetry, so gauge terms drop),
    sum |T|^2 = eps^{mu nu rho sigma} eps_{mu nu}^{rho' sigma'} k1_rho k2_sigma k1_rho' k2_sigma'
              = -2 (g^rho_rho' g^sigma_sigma' - g^rho_sigma' g^sigma_rho') k1 k2 k1 k2
              = -2 (k1^2 k2^2 - (k1.k2)^2) = 2 (k1.k2)^2 = 2 (m^2/2)^2 = m^4/2,
using eps^{mu nu rho sigma} eps_{mu nu alpha beta} = -2 (delta delta - delta delta) and
k1.k2 = (P^2 - k1^2 - k2^2)/2 = m^2/2. Both agree. The code does the explicit contraction with
toolkit.levi_civita over all 4^4 index tuples and the 2 x 2 real polarizations, numerically in the
rest frame: eps_{mu nu rho sigma} (lower) contracted with the contravariant components
e1^mu e2^nu k1^rho k2^sigma is a Lorentz scalar, so no metric factor is needed (no closed form typed).

**Two-body phase space.** Do d^3k2 with delta^3: k2 = -k1, |k1| = |k2| = p. Then
    Phi_2 = (1/(4 pi^2)) Int d^3p /(2E1 2E2) delta(m - E1 - E2) = (1/(4 pi^2)) 4 pi p^2 / (4 p^2) * 1/|d(E1+E2)/dp|
with E1 = E2 = p for massless photons, d(2p)/dp = 2, and the root p = m/2. General masses:
p = sqrt(lambda(m^2, m1^2, m2^2))/(2m), Phi_2 = p/(4 pi m) (with lambda the Kallen function;
massless: lambda = m^4, p = m/2), so Phi_2 = 1/(8 pi) for two photons. The amplitude
squared is isotropic here, so Int dPhi_2 |M|^2 = Phi_2 |M|^2.

**Closed form.**
    Gamma = (1/(2m)) (1/2) (1/(8 pi)) A^2 m^4/2 = A^2 m^3 / (64 pi)
          = alpha^2 m^3 N_c^2 (Q_u^2 - Q_d^2)^2 / (64 pi^3 f_pi^2).
Output in eV: Gamma[GeV] * 1e9 (inputs in GeV). Scalings: alpha^2 (blind check: 2 alpha -> 4x),
N_c^2 at fixed charges ((5/3)^2), m^3, f_pi^-2. With rung 1's charges N_c(Q_u^2 - Q_d^2) =
N_c (Q_u + Q_d)(Q_u - Q_d) = N_c (2Q_u - 1) = N_c * (1/N_c) = 1 for every N_c: the width is
N_c-independent once the charges are rung 1's (the classic N_c-cancellation).

**Second route.** (a) The covariant trace formula above (2 (k1.k2)^2, printed next to the
explicit sum); (b) phase space by numerical integration of Int d^3p/(4 pi^2 4 E^2) delta(m - 2E)
with a narrow normalized Gaussian for the delta, trapezoid rule over p (self-check), compared
with 1/(8 pi); (c) the closed form A^2 m^3/(64 pi).

---------------------------------------------------------------------------------------------------
## 5. pi0_width_from_rungs() -> eV   [rung 1 -> 2]

**Postulates.** Section 4 with N_c = 3, (Q_u, Q_d) = gauge331.quark_charges(3) (rung 1),
alpha = inputs.ALPHA_0 (on-shell photons, q^2 = 0), f_pi = inputs.F_PI, m = inputs.M_PI0.
Returns pi0_width_eV(...) of those. Second route: the closed form with N_c(Q_u^2 - Q_d^2) = 1;
pull against inputs.GAMMA_PI0 +- GAMMA_PI0_ERR printed in the self-check.

---------------------------------------------------------------------------------------------------
## 6. planck_mass_GeV(G, hbar, c) -> GeV   [rung 4's G -> rung 1's cutoff]

**Postulate.** SPEC section 8: M_Pl = sqrt(hbar c / G) (kg); energy M_Pl c^2 (J); / (1e9 e) -> GeV
with e = inputs.E_CH. Closed form: M_Pl c^2 = sqrt(hbar c^5 / G).
Second route: dimensional check l_P = hbar/(M_Pl c) equals sqrt(hbar G/c^3); compared with
inputs.L_PLANCK in the self-check; scaling M_Pl(4G) = M_Pl(G)/2.

## 7. g_window(p3, p5, mpl) -> (lo, hi)

**Postulates.** SPEC section 8: G -> x G gives M_Pl -> x^(-1/2) M_Pl. The 3-3-1 theory is cut off at
M_Pl; a colour number survives if its Landau pole lies above the cutoff and fails if below.
Poles p3 (N_c = 3), p5 (N_c = 5) are QUOTED inputs (inputs.POLES_331, layer QUOTED in inputs.py);
mpl = M_Pl at the measured G.

**Derivation.** Require p5 < mpl x^(-1/2) < p3. Squaring positive quantities:
x > (mpl/p3)^2 and x < (mpl/p5)^2, so lo = (mpl/p3)^2, hi = (mpl/p5)^2 (non-empty iff p5 < p3).
At the edges M_Pl(lo G) = p3, M_Pl(hi G) = p5 exactly.
**Second route.** Solve M_Pl(x G) = pole for log x with toolkit.bisect, using planck_mass_GeV
itself at x G (self-check).

## 8. schwarzschild_radius(m) -> m   [rung 6 -> rung 4's diamond]

r_s: the zero of f = 1 - 2GM/(c^2 r) of SPEC section 6/7's Schwarzschild metric (restoring G, c:
the G = c = 1 mass M is GM/c^2 in metres): r_s = 2 G m / c^2, G = inputs.G_NEWTON,
c = inputs.C_LIGHT at call time. Second route: toolkit.bisect on f(r) for design A's mass
(self-check); in Planck units r_s/l_P = 2 m/M_Pl (since G/c^2 = l_P/M_Pl).

## 9. planck_bh_kT_GeV() -> GeV   [rung 6 -> link 3]

**Postulates.** SPEC section 8: m = M_Pl in kg, then k_B T_H in GeV; T_H from rung 6
(`blackholes.hawking_K`, quoted Hawking formula T_H = hbar c^3/(8 pi G M k_B)).
Steps: M_Pl[GeV] = planck_mass_GeV(G, hbar, c); m_kg = M_Pl[GeV] 1e9 e / c^2;
T = blackholes.hawking_K(m_kg); k_B T [GeV] = K_B T / (1e9 e).
**Closed form in units of M_Pl c^2.**
    k_B T_H = hbar c^3/(8 pi G M_Pl) = (1/(8 pi)) hbar c^3 sqrt(G/(hbar c)) / G = (1/(8 pi)) sqrt(hbar c^5/G)
            = M_Pl c^2 / (8 pi).
The temperature of a Planck-mass hole is 1/(8 pi) of the Planck energy: semiclassical gravity
puts it just below the cutoff, independent of G, hbar, c.
Second route: the ratio planck_bh_kT_GeV()/planck_mass_GeV(...) compared with 1/(8 pi) (self-check).
