# DERIVATION: stage `links` (build 2026-11-b)

Written before the code. Postulates: SPEC.md section 8 (links), section 2 (charges), section 7 (Hawking
temperature, quoted there), "Connections between stages". Units: SI unless stated; particle quantities in GeV
with hbar = c = 1; charges in units of e. Metric signature (+,-,-,-), epsilon^{0123} = +1 (the plain
permutation symbol, `toolkit.levi_civita`).

Nothing in this stage could not be derived, except the pi0 amplitude, which SPEC section 8 quotes and the
contract allows as `quoted`.

---------------------------------------------------------------------------------------------------------

## 1. `qp_qe_minus_anomaly(Nc, b, XL, Xt)`: exact, Fraction

**Postulates** (SPEC section 8, "Anomaly identity"), all rational:

    Q_nu = 1/2 + b + XL,   Q_e = -1/2 + b + XL          (lepton triplet)
    Q_u  = 1/2 + b + Xt,   Q_d = -1/2 + b + Xt          (quark triplet)
    X_a  = Xt + 2b                                      (antitriplet)
    N_g  = Nc,   n = (1 + Nc)/2 antitriplet families
    anomaly = N_g XL + Nc [ (N_g - n) Xt + n X_a ]

Proton of Nc quarks (SPEC section 2 and section 8): (Nc+1)/2 u and (Nc-1)/2 d.

**Steps.**

    q_p = (Nc+1)/2 Q_u + (Nc-1)/2 Q_d
        = Nc (b + Xt) + (1/2)[(Nc+1)/2 - (Nc-1)/2]
        = Nc (b + Xt) + 1/2
    q_p + q_e = Nc (b + Xt) + b + XL                                          (1.1)

    anomaly = Nc XL + Nc [ (Nc - n) Xt + n Xt + 2 n b ]
            = Nc XL + Nc [ Nc Xt + (1 + Nc) b ]
    anomaly / N_g = XL + Nc Xt + (1 + Nc) b = Nc (b + Xt) + b + XL            (1.2)

(1.1) = (1.2), so the export is identically 0 for every rational (b, XL, Xt) and every Nc (the algebra never
uses that Nc is odd; odd Nc is needed only for n to be an integer). Why X_a = Xt + 2b: the antitriplet has
SU(3) charges (-1/2 - b, 1/2 - b, 2b) + X_a; its second component is Q_u iff X_a = Q_u - 1/2 + b = Xt + 2b
(consistent with rung 1's `_quark_X`).

**Closed form:** 0. The code does NOT return the literal 0: it evaluates q_p + q_e and anomaly/N_g separately
from the postulates in Fractions and subtracts.

**Second route.** (a) The difference is an affine function of each of b, XL, Xt (both sides are). An affine
function vanishes identically iff its value and its three partial derivatives vanish at one point: check
value 0 at a point and `toolkit.exact_derivative` = 0 in each argument. (b) With rung 1's actual charges
(`gauge331.quark_charges`, b = -/+ 1/6, XL = -1/3 or -2/3, Xt = Q_u - 1/2 - b) both q_p + q_e and the anomaly
are separately zero.

---------------------------------------------------------------------------------------------------------

## 2. `neutrality_per_nucleon(m)`: units of e per nucleon

**Postulates** (SPEC section 8, "Neutrality"). Two diamonds, each of mass m and net charge Q. Coulomb energy
U_C = k Q^2 / r, gravity U_G = -G m^2 / r (rung 4: U = -4 pi G m1 m2 yukawa(r, 0), yukawa(r, 0) = 1/(4 pi r)).
Both are (strength) x 1/r on the same branch trajectories, so every branch phase
phi = -(1/hbar) int U dt is the same functional of the trajectories times the strength:

    |phi_C / phi_G| = k Q^2 / (G m^2).                                          (2.1)

Requirement: |phi_C| <= F |phi_G|, F = inputs.GAP_FRACTION.

**Steps.** Nucleon count N = m / u, u = inputs.U_AMU; Q = N eps e with eps the net charge per nucleon in units
of e.

    k (m/u)^2 eps^2 e^2 / (G m^2) <= F
    eps_max = (u / e) sqrt(F G / k)                                             (2.2)

**Closed form:** (2.2); m cancels (size-free), eps ~ sqrt(F G), as the gates require. The code keeps the
m-dependence explicit (Q_max = m sqrt(F G/k), then divides by e and by m/u) so the cancellation is computed,
not assumed.

**Second route.** Do not use (2.2): build the two energies from rung 2's exchange transform,
U_G = -4 pi G m^2 `chiral.yukawa(r, 0)`, U_C(eps) = +4 pi k (m eps e/u)^2 `chiral.yukawa(r, 0)` at an
arbitrary r, and solve U_C(eps) + F U_G = 0 for eps with `toolkit.bisect`. Repeat at a different m and r.

**Assumptions flagged** (QUESTIONS.md): equal charges on the two diamonds; vacuum Coulomb law between net
monopoles (no dielectric factor: the permittivity enters induced-dipole terms, which are rung 3's Casimir
background, not this bound); one nucleon per atomic mass unit.

---------------------------------------------------------------------------------------------------------

## 3. `pi0_width_eV(alpha, fpi, mpi, Nc, Qu, Qd)`: eV (inputs in GeV)

**Quoted (allowed, SPEC section 8):** the anomaly amplitude

    M = A eps^{mu nu rho sigma} e1*_mu k1_nu e2*_rho k2_sigma,   A = (alpha / (pi f_pi)) Nc (Qu^2 - Qd^2).

Derived here: the polarization sum and the two-body phase space.

**3a. Polarization sum.** Rest frame, k1 = (m/2)(1, 0, 0, 1), k2 = (m/2)(1, 0, 0, -1) (upper indices), so
lower-index components k1_nu = (m/2)(1,0,0,-1), k2_sigma = (m/2)(1,0,0,1). Physical polarizations: the two
transverse unit vectors x, y for each photon. T(e1, e2) = eps^{mu nu rho sigma} e1_mu k1_nu e2_rho k2_sigma;
only nu, sigma in {0, 3} contribute:

    T(x, y) = eps^{1023} k1_0 k2_3 + eps^{1320} k1_3 k2_0 = (-1)(m^2/4) + (+1)(-m^2/4) = -m^2/2
    T(y, x) = eps^{2013} k1_0 k2_3 + eps^{2310} k1_3 k2_0 = (+1)(m^2/4) + (-1)(-m^2/4) = +m^2/2
    T(x, x) = T(y, y) = 0   (repeated index)

(lowering a spatial polarization index only flips a sign, irrelevant in the square). Hence

    sum_pol |M|^2 = A^2 (m^4/4 + m^4/4) = A^2 m^4 / 2.                           (3.1)

The code computes the dimensionless P = sum_pol |T|^2 / m^4 exactly in Fractions from `toolkit.levi_civita`
(it is not typed in).

**3b. Two-body phase space**, massless final state, pion at rest:

    Phi = int d^3k1/((2pi)^3 2E1) d^3k2/((2pi)^3 2E2) (2pi)^4 delta^4(p - k1 - k2)
        = (1/(4 pi^2)) int d^3k / (4 k^2) delta(m - 2k)
        = (1/(4 pi^2)) (4 pi) (1/4) int dk delta(m - 2k)
        = (1/(4 pi)) (1/2) = 1/(8 pi).                                          (3.2)

**3c. Width.** Gamma = (1/S) (1/(2m)) sum|M|^2 Phi with S = 2 for two identical photons:

    Gamma = (1/2) (1/(2m)) (A^2 m^4 / 2) (1/(8 pi)) = A^2 m^3 / (64 pi)
          = alpha^2 m^3 Nc^2 (Qu^2 - Qd^2)^2 / (64 pi^3 f_pi^2).                (3.3)

GeV -> eV: multiply by 10^9. Scalings alpha^2, Nc^2 (at fixed charges), m^3, f_pi^-2. With rung 1's charges
Nc (Qu^2 - Qd^2) = Nc (Qu - Qd)(Qu + Qd) = Nc (2 Qu - 1) = 1 for all Nc (Qu = (Nc+1)/(2Nc)), so the width is
then Nc-independent.

**Second route.** (a) Covariant: sum over polarizations -> (-g)(-g), so
sum|T|^2 = sum_{mu,rho} g_{mu mu} g_{rho rho} (eps^{mu nu rho sigma} k1_nu k2_sigma)^2; by the identity
eps^{mu nu rho sigma} eps_{mu alpha rho beta} = -2 (d^nu_alpha d^sigma_beta - d^nu_beta d^sigma_alpha) this is
-2 (k1^2 k2^2 - (k1.k2)^2) = 2 (k1.k2)^2 = m^4/2. Evaluate the brute-force contraction (no polarization
vectors) in a BOOSTED frame, k1 = (E1,0,0,E1), k2 = (E2,0,0,-E2), 4 E1 E2 = m^2, E1 != E2: must again give
1/2 exactly (Lorentz and gauge invariance). (b) Phase space numerically: replace delta(m - 2k) by a narrow
Gaussian and integrate with `toolkit.trapezoid`: -> 1/(8 pi). (c) Sanity: compare with inputs.GAMMA_PI0.

---------------------------------------------------------------------------------------------------------

## 4. `planck_mass_GeV(G, hbar, c)`: GeV

**Postulate** (SPEC section 8): M_Pl = sqrt(hbar c / G). (Dimensional analysis: hbar^a c^b G^g has dimension
of mass only for a = b = 1/2, g = -1/2: [hbar] = kg m^2/s, [c] = m/s, [G] = m^3/(kg s^2); kg: a - g = 1;
m: 2a + b + 3g = 0; s: -a - b - 2g = 0.)

    M_Pl c^2 [J] = sqrt(hbar c / G) c^2 = sqrt(hbar c^5 / G);   GeV = J / (10^9 e),  e = inputs.E_CH.   (4.1)

Scaling: G -> xG gives x^(-1/2).

**Second route.** At M = M_Pl the reduced Compton wavelength hbar/(M c) equals G M/c^2 (half of section 6's
Schwarzschild radius), and equals the independently tabulated inputs.L_PLANCK. Check both ratios -> 1.

---------------------------------------------------------------------------------------------------------

## 5. `g_window(p3, p5, mpl)`: (lo, hi), dimensionless x = G/G_meas

**Postulate:** M_Pl(xG) = x^(-1/2) mpl. Condition p5 < M_Pl(xG) < p3 (p3, p5: the N_c = 3 and N_c = 5
poles, same units as mpl):

    p5 < mpl / sqrt(x) < p3   <=>   (mpl/p3)^2 < x < (mpl/p5)^2
    lo = (mpl / p3)^2,   hi = (mpl / p5)^2.                                     (5.1)

x^(-1/2) is decreasing, so the higher pole gives the lower edge. At x = lo, M_Pl = p3; at x = hi, M_Pl = p5.
If p3 <= p5 there is no window; the function still returns (lo, hi) with lo >= hi (no clipping).

**Second route.** Root-find instead of inverting: solve planck_mass_GeV(10^t G) = pole for t with
`toolkit.bisect`, for both poles; compare 10^t with (5.1).

---------------------------------------------------------------------------------------------------------

## 6. `schwarzschild_radius(m)`: metres (m in kg)

**Postulates:** SPEC section 6's static metric with f = 1 - 2M/r (the l -> infinity limit of SdS), M the
geometric mass. The horizon is the zero of f: r = 2M. Geometric mass in SI: the Newtonian limit
g_tt = -(1 + 2 Phi/c^2), Phi = -G m/r, gives M = G m/c^2 (rung 4's point-mass metric). Hence

    r_s = 2 G m / c^2.                                                          (6.1)

Linear in m, ~ 1/c^2 (the gates).

**Second route.** (a) `blackholes.sds_horizons(M, l)` with M = G m/c^2 and l >> M: bisection on f gives
r_b = 2M (1 + 4M^2/l^2 + ...) -> r_s. (b) Hawking: k_B T_H = hbar kappa/(2 pi c) with kappa = c^2 f'(r_s)/2
= c^2/(2 r_s), so r_s = hbar c/(4 pi k_B T_H) with T_H from `blackholes.hawking_K(m)`.

---------------------------------------------------------------------------------------------------------

## 7. `matter_charges(Nc, variant)`: (q_p, q_n, q_e, Q_nu), Fractions

**Postulates** (SPEC section 8, section 2; connection L1). (Q_u, Q_d) = `gauge331.quark_charges(Nc)`.

    q_p = (Nc+1)/2 Q_u + (Nc-1)/2 Q_d,     q_n = (Nc-1)/2 Q_u + (Nc+1)/2 Q_d.
    lepton triplet: `gauge331.triplet_charges(X_L, variant)`, X_L = -1/3 (beta = -1/sqrt3) or -2/3 (+1/sqrt3);
    Q_nu = component 1, q_e = component 2.

**Expected result (derived, not typed in).** Rung 1 gives Q_u = (Nc+1)/(2Nc), Q_d = Q_u - 1, so
q_p = Nc Q_u - (Nc-1)/2 = 1, q_n = Nc Q_u - (Nc+1)/2 = 0. Lepton: b = -/+1/6; Q_e = -1/2 + b + X_L =
-1/2 - 1/6 - 1/3 = -1 or -1/2 + 1/6 - 2/3 = -1; Q_nu = Q_e + 1 = 0. So (1, 0, -1, 0) in both variants, all Nc.
X_L is taken from the SPEC's stated values (not solved from Q_e = -1), so q_e = -1 is a real check.

**Second route.** q_p - q_n = Q_u - Q_d = 1 and q_p + q_e = anomaly/N_g via `qp_qe_minus_anomaly` with
Xt = Q_u - 1/2 - b; and rung 1's anomaly cancels, so q_p + q_e = 0. Checked for Nc = 1..11 odd, both variants.

---------------------------------------------------------------------------------------------------------

## 8. `pi0_width_from_rungs()`: eV

(Q_u, Q_d) = `gauge331.quark_charges(3)`; return `pi0_width_eV(inputs.ALPHA_0, inputs.F_PI, inputs.M_PI0, 3,
Q_u, Q_d)` (connection L2: both calls are real). Quoted amplitude -> provenance `quoted`.
**Second route:** since Nc (Qu^2 - Qd^2) = 1, Gamma = alpha^2 m^3/(64 pi^3 f_pi^2) with no charges at all;
and rung 1's charges at Nc = 5, 7 must give the same width.

---------------------------------------------------------------------------------------------------------

## 9. `planck_bh_kT_GeV()`: GeV

**Postulates** (SPEC section 8; connection L5; T_H is quoted in section 7 and implemented in rung 6).

    m [kg] = planck_mass_GeV(G, hbar, c) x 10^9 e / c^2
    k_B T_H [GeV] = k_B `blackholes.hawking_K`(m) / (10^9 e).

**Closed form.** T_H = hbar c^3/(8 pi G M k_B) at M = sqrt(hbar c/G):
k_B T_H = hbar c^3/(8 pi G) sqrt(G/(hbar c)) = sqrt(hbar c^5/G)/(8 pi) = M_Pl c^2/(8 pi). k_B and e cancel.

**Second route.** planck_mass_GeV(...)/(8 pi) without calling rung 6; and the 1/M law: the temperature at
2 M_Pl is half.
