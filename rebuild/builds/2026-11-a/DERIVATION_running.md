# DERIVATION: running (SPEC.md sections 2 and 9)

Postulates used: SPEC 9 (one-loop beta function, the SM content below the 3-3-1 scale, boundary
values at M_Z, the 3-3-1 content above it including the SU(3)_L singlet partners, matching at mu
with no thresholds, the definition of the Landau pole as alpha_X = 1); SPEC 2 (Q = T3 + beta T8 + X,
the scalar X charges, the fermion families, Q_u, Q_d derived by rung 1). Inputs: MZ_MEAS,
ALPHA_MZ_INV, S2_MZ, MU_331. Nothing is quoted.

Notation: b = beta/(2 sqrt3), exact rational (b = -1/6 for "-1/sqrt3", +1/6 for "+1/sqrt3");
beta T8 = b diag(1, 1, -2). Rung 1 supplies triplet_charges (Q of each component) and
quark_charges(N_c) = (Q_u, Q_d) = ((N_c+1)/(2N_c), (1-N_c)/(2N_c)).

---

## 0. The one-loop coefficient (SPEC 9)

    d(1/alpha)/d ln mu = -b_i/(2 pi),
    b_i = -(11/3) C2(G) + (2/3) sum_Weyl T(R) + (1/3) sum_complex scalars T(R),

T(fund of SU(N)) = 1/2, times the dimension under every other factor; for a U(1) each component
of charge q contributes q^2 (so a multiplet contributes the sum of q^2 over all its components,
including colour and SU(N)_L components). C2 = N for SU(N), 0 for U(1).

Integrating (b_i constant between thresholds):

    1/alpha_i(mu) = 1/alpha_i(mu0) - (b_i/2 pi) ln(mu/mu0).                         (0.1)

---

## 1. `sm_coefficients()` -> (b_Y, b_2)

Content per generation (left-handed Weyl): Q (2, Y = 1/6, 3 colours), u^c (1, -2/3, 3),
d^c (1, 1/3, 3), L (2, -1/2), e^c (1, 1). Higgs: one complex doublet, Y = 1/2.

U(1)_Y, sum of Y^2 over components, per generation:

    Q: 6 (1/36) = 1/6;  u^c: 3 (4/9) = 4/3;  d^c: 3 (1/9) = 1/3;  L: 2 (1/4) = 1/2;  e^c: 1.
    total = 10/3 per generation, 10 for 3 generations.
    Higgs: 2 (1/4) = 1/2.
    b_Y = (2/3)(10) + (1/3)(1/2) = 41/6.

SU(2)_L: C2 = 2. Doublets per generation: Q gives 3 (colours), L gives 1 -> 4 doublets, 12 in all,
each T = 1/2. Higgs: one doublet.

    b_2 = -(11/3)(2) + (2/3)(12)(1/2) + (1/3)(1/2) = -22/3 + 4 + 1/6 = -19/6.

In code: the field table (multiplicities, Y as Fractions with the postulated SPEC values) is summed
mechanically; Y of each SU(2) component is listed but the hypercharges are SPEC postulates, so no
rung-1 call is needed here. The 11/3, 2/3, 1/3 and 1/2 are the postulated group-theory weights.

**Second route.** Q = T3 + Y must give each field's known electric charge: u_L: 1/2 + 1/6 = 2/3,
d_L: -1/3, u^c: -2/3, d^c: 1/3, nu: 0, e: -1, e^c: 1 (checked in __main__). Also the SM gauge
anomalies vanish for this table: sum Y^3 = 0 and sum Y (gravitational) = 0 per generation, and
[SU(2)]^2 U(1): 3(1/6) + (-1/2) = 0 (checked exactly in __main__). These confirm the table, and
the totals 10/3 per generation agree with the classic GUT-normalised (3/5)b_Y = 41/10 (identity).

---

## 2. `b_331(Nc, variant)` -> (b_X, b_L)

### 2.1 Field content (SPEC 2, 9), all charges via rung 1

N_g = N_c generations; n_A = (1+N_c)/2 antitriplet quark families, n_T = N_g - n_A triplet families,
each family N_c-coloured; one lepton triplet per generation (colour singlet).

X charges (derived with rung 1's triplet_charges, Q_u, Q_d from gauge331.quark_charges):
- lepton triplet: X_L fixed by Q_e = -1 in component 2:
      X_L = -1 - triplet_charges(0, variant)[1] = -1/2 - b,
  equal to SPEC 2's listed -1/3 (b = -1/6) and -2/3 (b = +1/6); the code asserts that and that
  component 1 (the neutrino) is neutral.
- quark triplet: components 1, 2 = (Q_u, Q_d):
      X_t = Q_u - triplet_charges(0, variant)[0] = Q_u - 1/2 - b; then component 2 = Q_d (asserted).
- quark antitriplet: first two components = {Q_u, Q_d} in some order. With
  Q_anti(X) = (-1/2 - b + X, 1/2 - b + X, 2b + X), try X = Q_u - c_1 and X = Q_d - c_1
  (c_1 = triplet_charges(0, variant, anti=True)[0]) and keep the one whose first two charges are the
  set {Q_u, Q_d}: X_a = Q_d + 1/2 + b = X_t + 2b (component 1 = Q_d, component 2 = Q_u).
- scalars: three complex triplets, X = (-1/3, 2/3, -1/3) or (1/3, 1/3, -2/3) (SPEC 2 postulate).

Component charges (closed forms, epsilon = 1/(2 N_c)):

    lepton triplet: (0, -1, -1/2 - 3b)
    quark triplet:  (Q_u, Q_d, epsilon - 3b)       X_t = epsilon - b
    antitriplet:    (Q_d, Q_u, epsilon + 3b)       X_a = epsilon + b

SU(3)_L singlet partners (SPEC 9): one left-handed Weyl singlet per electrically charged fermion
component, with X = -Q of that component, carrying the component's colour multiplicity
(N_c for quarks). A neutral component has none; since it would contribute Q^2 = 0 anyway, the
U(1)_X sum below does not depend on that rule's treatment of neutral components (the code still
applies it literally, q != 0).

### 2.2 b_L (SU(3)_L, C2 = 3)

Triplets/antitriplets of SU(3)_L, each T = 1/2: fermions N_g (leptons) + N_c N_g (quarks, all
families, with colour) = N_c + N_c^2; scalars 3 complex triplets.

    b_L = -11 + (2/3)(1/2)(N_c + N_c^2) + (1/3)(1/2)(3) = -11 + N_c(N_c+1)/3 + 1/2.

N_c = 3: b_L = -13/2.  (Independent of the variant.)

### 2.3 b_X (U(1)_X, C2 = 0)

    b_X = (2/3)[ F_trip + F_sing ] + (1/3) S,

    F_trip = 3 N_g X_L^2 + 3 N_c (n_T X_t^2 + n_A X_a^2)           (3 components each)
    F_sing = sum over charged fermion components of (colour mult) Q^2
           = N_g [1 + (1/2 + 3b)^2] + N_c n_T [Q_u^2 + Q_d^2 + (eps - 3b)^2]
                                    + N_c n_A [Q_u^2 + Q_d^2 + (eps + 3b)^2]
    S      = 3 sum_s X_s^2 = 3 (2/3) = 2 in both variants  ->  (1/3) S = 2/3.

Worked values (the code computes these by enumeration; listed for the reader):

    N_c = 3, b = -1/6: X_L = -1/3, X_t = 1/3, X_a = 0;
        F_trip = 1 + 1 + 0 = 2;  F_sing = 3 + 3 + 4 = 10;  b_X = (2/3)(12) + 2/3 = 26/3.
    N_c = 3, b = +1/6: X_L = -2/3, X_t = 0, X_a = 1/3;
        F_trip = 4 + 0 + 2 = 6;  F_sing = 6 + 2 + 6 = 14;  b_X = (2/3)(20) + 2/3 = 14.

**Second route.** The closed form above (in terms of N_c and b only, no rung-1 calls) is evaluated
independently in __main__ and compared exactly with the enumeration for N_c = 1, 3, 5, 7, 9 and both
variants. A further identity check: for each triplet sum_components X^2 = sum Y^2 - 6 b^2 where
Y = b T8-shape + X is the SM hypercharge of the components (2(X+b)^2 + (X-2b)^2 = 3X^2 + 6b^2).

Monotonicity (blind check): every term of b_X is a sum of squares with positive multiplicities
growing with N_c (N_g = N_c generations of N_c colours), so b_X > 0 and increases with N_c.

---

## 3. `couplings_at(mu)` -> (1/alpha_Y, 1/alpha_2)

Boundary (SPEC 9): at mu = M_Z, 1/alpha_Y = (1 - s^2)/alpha_hat, 1/alpha_2 = s^2/alpha_hat
(from e = g s = g' c, 1/e^2 = 1/g^2 + 1/g'^2). Then by (0.1):

    1/alpha_Y(mu) = (1 - s^2) A - (b_Y/2pi) ln(mu/M_Z),
    1/alpha_2(mu) = s^2 A - (b_2/2pi) ln(mu/M_Z),         A = inputs.ALPHA_MZ_INV.

Valid for any mu > 0 (no threshold below the 3-3-1 scale is modelled; the formula is also used
below M_Z if asked). **Second route:** a step-wise (Euler, 100 steps) integration of the ODE
d(1/alpha)/dt = -b/2pi in t = ln mu (trivially exact for a constant right side, so this is a
code-path check), plus the identity (1/alpha_Y + 1/alpha_2)(M_Z) = A.

---

## 4. `matching_331(mu, variant)` -> (1/alpha_X, 1/alpha_L)

SU(2)_L in SU(3)_L: g_L(mu) = g_2(mu), so 1/alpha_L = 1/alpha_2(mu).

Photon continuity: rung 1's gauge331.inv_e2(variant, g_L, g_X) = 1/e^2 equals the SM's
(1/alpha_Y + 1/alpha_2)/(4 pi). Rung 1 derived inv_e2 = (1+beta^2)/g^2 + 1/g_X^2, which is affine in
u = 1/g_X^2 with unit slope. The code does not assume that form: it evaluates the rung-1 function
F(u) = inv_e2(variant, g_L, u^(-1/2)) at two values u1, u2 and solves the affine equation

    u* = u1 + (target - F(u1)) (u2 - u1)/(F(u2) - F(u1)),     1/alpha_X = 4 pi u*.

(Exact for an affine F up to rounding; the code then verifies F(u*) = target to 1e-12 and raises if
u* <= 0, i.e. no real g_X.)

Closed form (second route, from rung 1's formula):

    1/alpha_X = 1/alpha_Y - beta^2/alpha_2 = 1/alpha_Y - (1/3)/alpha_2   (beta^2 = 12 b^2 = 1/3).

This is the usual 3-3-1 relation g_X^-2 = g'^-2 - beta^2 g^-2 (U(1)_Y = beta T8 + X).

---

## 5. `landau_pole(Nc, variant)` -> GeV

From mu0 = inputs.MU_331 with 1/alpha_X0 = matching_331(mu0, variant)[0] and b_X = b_331(Nc, variant)[0],
(0.1) gives 1/alpha_X(mu) = 1/alpha_X0 - (b_X/2pi) ln(mu/mu0). Setting alpha_X = 1:

    mu_pole = mu0 exp[ 2 pi (1/alpha_X0 - 1) / b_X ].

Closed form, no root-finding needed (the code uses it). Since b_X > 0 and 1/alpha_X0 > 1, the pole lies
above mu0 and falls as b_X grows (N_c = 5 below N_c = 3). **Second route:** toolkit.bisect on
g(t) = 1/alpha_X(mu0 e^t) - 1 over t in [0, 400] in __main__, compared with the closed form.

Order of magnitude (for the reader, not used): N_c = 3, +1/sqrt3: 1/alpha_X(4 TeV) ~ 84, b_X = 14,
pole ~ 5e19 GeV; the quoted three-loop reference (inputs.POLES_331) is 3.5e19, same order, as
expected for one loop.

---

## Not derived / marked

Nothing quoted. The group-theory weights (11/3, 2/3, 1/3, T = 1/2, C2 = N) and the hypercharge table
are SPEC postulates, typed as small Fractions; the scalar X charges are SPEC 2 postulates.

## Results (computed by the code, recorded for cross-build comparison)

    sm_coefficients = (41/6, -19/6)
    b_331(N_c, "-1/sqrt3"): N_c = 1, 3, 5, 7, 9 -> b_X = 22/9, 26/3, 58/3, 310/9, 54
    b_331(N_c, "+1/sqrt3"): N_c = 1, 3, 5, 7, 9 -> b_X = 46/9, 14, 82/3, 406/9, 202/3
    b_L (both variants)   : -59/6, -13/2, -1/2, 49/6, 39/2
    matching_331(4000, either variant) = (83.7307, 31.4946)   (beta^2 = 1/3 in both)
    landau_pole: -1/sqrt3: N_c = 3: 4.470e29, N_c = 5: 1.900e15 GeV
                 +1/sqrt3: N_c = 3: 5.335e19, N_c = 5: 7.265e11 GeV
    (closed form and toolkit.bisect agree to all printed digits; the one-loop poles are 1.4-2x the
    quoted three-loop inputs.POLES_331, in the same order.)
